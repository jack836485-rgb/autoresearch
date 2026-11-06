#!/usr/bin/env python3
"""问题卡台账：一卡一文件，主执行者与查新子代理分字段写入，最后合成 研究问题.json。

主执行者写卡的内容字段；查新子代理只写 "拥挤度" 与 "查新状态"。两者并行时互不覆盖。

用法（在项目根目录运行，<slot> 为 path-stage/<slot> 目录）：
  init    <slot> [--领域 ... --窗口 起 止 --机构口径 ...]   建立 资料/问题卡/ 与 资料/查新/
  submit  <slot> Q001 [Q002 ...]                          把卡标为"查新中"，打印要发给查新子代理的批次消息
  mark    <slot> Q001 <结论.json>                          查新子代理写回结论（只改 拥挤度、查新状态，并把近邻追加进台账）
  note    <slot> <作品ID> <标题> --覆盖 "..." [--卡 Q001] [--深度 摘要]   主执行者登记已读论文，供子代理复用
  status  <slot>                                          列出各卡查新状态与待查卡
  export  <slot> [--allow-pending]                        按 ID 合成 研究问题.json；有卡仍在查新中时默认拒绝
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

结论取值 = {"不拥挤", "偏拥挤", "拥挤", "前提不成立"}
子代理字段 = {"拥挤度", "查新状态"}


def 路径(slot):
    root = Path(slot)
    return root, root / "资料" / "问题卡", root / "资料" / "查新" / "近邻台账.jsonl"


def 读卡(d, qid):
    f = d / f"{qid}.json"
    if not f.exists():
        sys.exit(f"找不到问题卡 {f}；主执行者先把卡写成该文件再提交查新")
    return f, json.loads(f.read_text(encoding="utf-8"))


def 写(f, obj):
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(f)


def 追加台账(ledger, row):
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("init"); a.add_argument("slot"); a.add_argument("--领域"); a.add_argument("--窗口", nargs=2); a.add_argument("--机构口径")
    a = sub.add_parser("submit"); a.add_argument("slot"); a.add_argument("ids", nargs="+")
    a = sub.add_parser("mark"); a.add_argument("slot"); a.add_argument("qid"); a.add_argument("verdict_json")
    a = sub.add_parser("note"); a.add_argument("slot"); a.add_argument("作品ID"); a.add_argument("标题"); a.add_argument("--覆盖", required=True); a.add_argument("--卡"); a.add_argument("--深度", default="摘要")
    a = sub.add_parser("status"); a.add_argument("slot")
    a = sub.add_parser("export"); a.add_argument("slot"); a.add_argument("--allow-pending", action="store_true")
    args = p.parse_args()
    root, d, ledger = 路径(args.slot)
    today = datetime.date.today().isoformat()

    if args.cmd == "init":
        d.mkdir(parents=True, exist_ok=True); ledger.parent.mkdir(parents=True, exist_ok=True); ledger.touch()
        meta = root / "资料" / "问题卡" / "_元信息.json"
        if not meta.exists():
            写(meta, {"领域": args.领域, "检索日期": today, "近期窗口": args.窗口, "机构口径": args.机构口径})
        print(f"已建立 {d} 与 {ledger}")

    elif args.cmd == "submit":
        lines = []
        for qid in args.ids:
            f, card = 读卡(d, qid)
            card["查新状态"] = f"查新中（{today} 提交）"
            card.setdefault("拥挤度", None)
            写(f, card)
            lines.append(f"- {qid}：{card.get('具体问题', '')}")
        print("请对以下问题卡做问题级拥挤度检查（卡文件在 " + str(d) + "）：\n" + "\n".join(lines))

    elif args.cmd == "mark":
        f, card = 读卡(d, args.qid)
        v = json.loads(Path(args.verdict_json).read_text(encoding="utf-8"))
        if v.get("结论") not in 结论取值:
            sys.exit(f"结论必须是 {sorted(结论取值)} 之一，收到 {v.get('结论')!r}")
        for k in ("依据", "近邻", "剩余空间", "查询记录"):
            if k not in v:
                sys.exit(f"结论 JSON 缺少字段：{k}")
        v["审查日期"] = today
        card["拥挤度"] = v
        card["查新状态"] = (f"已做问题级拥挤度检查（{today}，查新子代理）：{v['结论']}。"
                        f"查询：{'；'.join(v['查询记录'])}。未做 idea 级新意打分，下游打磨仍需针对具体主张查新")
        写(f, card)
        for n in v["近邻"]:
            追加台账(ledger, {**n, "关联卡": args.qid, "发现者": "查新子代理", "日期": today})
        print(f"{args.qid}：{v['结论']}（近邻 {len(v['近邻'])} 篇已入台账）")

    elif args.cmd == "note":
        ledger.parent.mkdir(parents=True, exist_ok=True)
        追加台账(ledger, {"作品ID": args.作品ID, "标题": args.标题, "覆盖了什么": args.覆盖, "读取深度": args.深度,
                     "关联卡": args.卡, "发现者": "主执行者", "日期": today})
        print("已登记")

    elif args.cmd == "status":
        pending = []
        for f in sorted(d.glob("Q*.json")):
            card = json.loads(f.read_text(encoding="utf-8"))
            v = (card.get("拥挤度") or {}).get("结论")
            st = v or ("查新中" if str(card.get("查新状态", "")).startswith("查新中") else "未提交")
            if st in ("查新中", "未提交"):
                pending.append(f.stem)
            print(f"{f.stem}\t{st}\t{card.get('具体问题', '')[:60]}")
        print("待查：" + ("、".join(pending) if pending else "无"))

    elif args.cmd == "export":
        meta_f = d / "_元信息.json"
        meta = json.loads(meta_f.read_text(encoding="utf-8")) if meta_f.exists() else {}
        cards, pending = [], []
        for f in sorted(d.glob("Q*.json")):
            card = json.loads(f.read_text(encoding="utf-8"))
            if not card.get("拥挤度"):
                pending.append(f.stem)
            cards.append(card)
        if pending and not args.allow_pending:
            sys.exit("以下卡尚无拥挤度结论，先等查新子代理返回或补交：" + "、".join(pending))
        out = {**meta, "研究问题": cards}
        写(root / "研究问题.json", out)
        print(f"已合成 {root / '研究问题.json'}：{len(cards)} 张卡" + (f"（{len(pending)} 张无拥挤度结论）" if pending else ""))


if __name__ == "__main__":
    main()
