#!/usr/bin/env python3
"""等服务器 GPU 空出来：ssh 到各服务器跑 nvidia-smi 轮询，条件满足即退出。

用法（条件由调用的 Claude/Codex 决定）：
  python gpu_watch.py --once                       # 只看一眼当前状态
  python gpu_watch.py --gpus 2 --min-free-gb 40    # 等到某台服务器同时有 2 张满足条件的卡
  python gpu_watch.py --servers A100,L40 --gpus 1 --timeout 3000

退出码：0 条件满足；2 等待超时；3 --once 且当前不满足；1 参数/配置错误。
服务器启用状态、可用卡、排除卡、自己的占卡进程见同目录 servers.json。
"""
import argparse
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).with_name("servers.json")

# 通过 stdin 交给远端 bash，避免 Windows 下多层引号转义
REMOTE_SCRIPT = r"""
nvidia-smi --query-gpu=index,uuid,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits || echo NVSMI_FAIL
echo @@
nvidia-smi --query-compute-apps=gpu_uuid,pid,used_memory --format=csv,noheader,nounits 2>/dev/null
echo @@
whoami
echo @@
pids=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader,nounits 2>/dev/null | tr -d ' ' | sort -u | paste -sd, -)
[ -n "$pids" ] && ps -o pid=,user:32=,args= -p "$pids" 2>/dev/null
true
"""


def to_num(s):
    try:
        return float(s)
    except ValueError:
        return None  # "[N/A]"、"[GPU requires reset]" 之类


def query(host, ssh_timeout):
    """返回 (me, gpus) 或抛出 RuntimeError。gpus: list[dict]。"""
    try:
        r = subprocess.run(
            ["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host, "bash", "-s"],
            # 用字节传，Windows 文本模式会把换行写成 \r\n，远端 bash 会执行 "whoami\r"
            input=REMOTE_SCRIPT.encode(), capture_output=True, timeout=ssh_timeout,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"ssh 超时（{ssh_timeout}s）")
    out = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0 and "@@" not in out:
        err = r.stderr.decode("utf-8", "replace").strip().splitlines()
        raise RuntimeError(f"ssh 失败：{err[-1] if err else '未知错误'}")

    parts = [[ln.strip() for ln in p.strip().splitlines() if ln.strip()]
             for p in re.split(r"^@@\r?$", out, flags=re.M)]
    if len(parts) < 4:
        raise RuntimeError("输出格式异常")
    gpu_lines, app_lines, me_lines, ps_lines = parts[:4]
    if any("NVSMI_FAIL" in ln for ln in gpu_lines):
        raise RuntimeError("nvidia-smi 执行失败：" + " ".join(gpu_lines)[:200])
    me = me_lines[0] if me_lines else "?"

    ps = {}
    for ln in ps_lines:
        f = ln.split(None, 2)
        if len(f) >= 2:
            ps[f[0]] = (f[1], f[2] if len(f) > 2 else "")

    gpus, by_uuid = [], {}
    for ln in gpu_lines:
        f = [x.strip() for x in ln.split(",")]
        if len(f) < 5:
            continue
        g = {"index": int(f[0]), "total": to_num(f[2]), "used": to_num(f[3]),
             "util": to_num(f[4]), "procs": []}
        g["broken"] = None in (g["total"], g["used"], g["util"])
        gpus.append(g)
        by_uuid[f[1]] = g
    for ln in app_lines:
        f = [x.strip() for x in ln.split(",")]
        if len(f) < 3 or f[0] not in by_uuid:
            continue
        user, args = ps.get(f[1], ("?", ""))  # 容器内进程可能看不到属主
        by_uuid[f[0]]["procs"].append(
            {"pid": f[1], "mem": to_num(f[2]) or 0, "user": user, "args": args})
    return me, gpus


def evaluate(name, cfg, me, gpus, a):
    """给每张卡打上 ok/why/free，返回满足条件的卡（按空闲显存降序）。"""
    allowed = cfg.get("gpus", "all")
    exclude = set(cfg.get("exclude_gpus", []))
    reclaim_re = re.compile(cfg["own_placeholder"]) if cfg.get("own_placeholder") else None
    ok = []
    for g in gpus:
        g["ok"], g["why"], g["reclaim"] = False, "", []
        if (allowed != "all" and g["index"] not in allowed) or g["index"] in exclude:
            g["why"] = "不可用卡"
            continue
        if g["broken"]:
            g["why"] = "状态异常"
            continue
        reclaim = [p for p in g["procs"]
                   if reclaim_re and p["user"] == me and reclaim_re.search(p["args"])]
        others = [p for p in g["procs"] if p not in reclaim]
        g["reclaim"] = reclaim
        free_gb = (g["total"] - g["used"] + sum(p["mem"] for p in reclaim)) / 1024
        g["free"] = free_gb
        # 卡上只剩自己的占卡进程时，利用率是占卡程序造成的，不算
        util = 0 if (reclaim and not others) else g["util"]
        need_free = a.min_free_gb if a.min_free_gb is not None else 0.9 * g["total"] / 1024
        if others and not a.allow_shared:
            g["why"] = "有他人进程" if any(p["user"] != me for p in others) else "有自己的任务"
        elif free_gb < need_free:
            g["why"] = f"空闲 {free_gb:.1f}G < {need_free:.1f}G"
        elif util > a.max_util:
            g["why"] = f"利用率 {util:.0f}% > {a.max_util:.0f}%"
        else:
            g["ok"] = True
            ok.append(g)
    return sorted(ok, key=lambda g: -g["free"])


def fmt_server(name, cfg, st):
    head = f"== {name}"
    if cfg.get("note"):
        head += f"（{cfg['note']}）"
    if not cfg.get("enabled", True):
        return f"{head}\n   已停用：{cfg.get('reason', '未注明原因')}"
    if "error" in st:
        return f"{head}\n   连接失败：{st['error']}"
    lines = [head + f"  [ssh 用户 {st['me']}]"]
    for g in st["gpus"]:
        if g["broken"]:
            lines.append(f"   {g['index']}  状态异常（nvidia-smi 返回 N/A，可能需要重置）")
            continue
        owners = ",".join(sorted({f"{p['user']}({p['mem'] / 1024:.0f}G)" for p in g["procs"]})) or "-"
        mark = "【可用】" if g["ok"] else "× " + g["why"]
        lines.append(f"   {g['index']}  用 {g['used'] / 1024:5.1f}/{g['total'] / 1024:.0f}G  "
                     f"利用率 {g['util']:3.0f}%  进程 {owners}  {mark}")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="轮询服务器 GPU，满足条件即退出")
    p.add_argument("--servers", help="逗号分隔，按偏好排序；默认 servers.json 中全部启用的服务器")
    p.add_argument("--gpus", type=int, default=1, help="同一台服务器上需要的卡数（默认 1）")
    p.add_argument("--min-free-gb", type=float, default=None,
                   help="每张卡至少空闲显存 GB；默认为该卡总显存的 90%%")
    p.add_argument("--max-util", type=float, default=10, help="每张卡利用率上限 %%（默认 10）")
    p.add_argument("--allow-shared", action="store_true",
                   help="允许和别人的进程共用一张卡（默认不允许，卡上有他人进程即视为不可用）")
    p.add_argument("--stable", type=int, default=2,
                   help="需连续满足的检查次数，避免别人任务间隙的瞬时空闲（默认 2）")
    p.add_argument("--interval", type=int, default=120, help="轮询间隔秒（默认 120）")
    p.add_argument("--timeout", type=int, default=0, help="最长等待秒，0 为不限（默认 0）")
    p.add_argument("--once", action="store_true", help="只检查一次并打印状态")
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("-v", "--verbose", action="store_true", help="每轮打印一行摘要")
    for f in (sys.stdout, sys.stderr):
        f.reconfigure(encoding="utf-8")  # Windows 控制台默认 GBK，agent 按 UTF-8 读
    a = p.parse_args()

    try:
        servers = json.loads(a.config.read_text(encoding="utf-8"))["servers"]
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"读取配置失败 {a.config}：{e}")
    names = [s.strip() for s in a.servers.split(",")] if a.servers else list(servers)
    unknown = [n for n in names if n not in servers]
    if unknown:
        print(f"配置中没有这些服务器：{unknown}；已有：{list(servers)}", file=sys.stderr)
        sys.exit(1)
    active = [n for n in names if servers[n].get("enabled", True)]
    if not active:
        print("指定的服务器都已停用：" + "；".join(
            f"{n}：{servers[n].get('reason', '未注明原因')}" for n in names), file=sys.stderr)
        sys.exit(1)

    start, streak = time.time(), {n: 0 for n in active}
    while True:
        with ThreadPoolExecutor(len(active)) as ex:
            futs = {n: ex.submit(query, n, 60) for n in active}
        status, ready = {}, None
        for n in active:
            try:
                me, gpus = futs[n].result()
            except RuntimeError as e:
                status[n] = {"error": str(e)}
                streak[n] = 0
                continue
            ok = evaluate(n, servers[n], me, gpus, a)
            status[n] = {"me": me, "gpus": gpus, "ok": ok}
            streak[n] = streak[n] + 1 if len(ok) >= a.gpus else 0
            need = 1 if a.once else a.stable
            if ready is None and streak[n] >= need:
                ready = n
        now = datetime.now().strftime("%m-%d %H:%M:%S")

        if a.verbose:
            summ = "  ".join(f"{n}:{'ERR' if 'error' in s else len(s['ok'])}卡({streak[n]})"
                             for n, s in status.items())
            print(f"[{now}] {summ}", flush=True)

        done = ready is not None or a.once or (a.timeout and time.time() - start >= a.timeout)
        if done:
            for n in names:
                print(fmt_server(n, servers[n], status.get(n, {})))
            if ready:
                picked = status[ready]["ok"][:a.gpus]
                idx = [g["index"] for g in picked]
                print(f"\n[{now}] GPU 就绪：{ready} 卡 {','.join(map(str, idx))}"
                      f"（最少空闲 {min(g['free'] for g in picked):.1f}G）")
                for g in picked:
                    for pr in g["reclaim"]:
                        print(f"   注意：卡 {g['index']} 上是自己的占卡进程 pid {pr['pid']}，用卡前先停掉")
                if servers[ready].get("note"):
                    print(f"   服务器备注：{servers[ready]['note']}")
                print("GPU_READY " + json.dumps({"server": ready, "gpus": idx}))
                sys.exit(0)
            if a.once:
                print(f"\n[{now}] 当前没有服务器满足条件")
                sys.exit(3)
            print(f"\n[{now}] 等待超时（{a.timeout}s），仍没有服务器满足条件")
            print("GPU_TIMEOUT")
            sys.exit(2)
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
