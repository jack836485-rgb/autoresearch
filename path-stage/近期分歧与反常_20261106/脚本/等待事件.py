"""前台等待：新卡攒够一批、查新子代理交回、或找卡子任务全部交回，三者之一发生即返回。
用法: python 等待事件.py <批量阈值> <超时秒> <查新agent输出> <找卡agent输出...>
"""
import glob, json, os, sys, time

slot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
batch, timeout, checker, finders = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4:]


def handbacks(path):
    n = 0
    try:
        for line in open(path, encoding="utf-8"):
            c = json.loads(line).get("message", {}).get("content")
            if isinstance(c, list):
                n += sum(1 for i in c if i.get("type") == "tool_use" and "Handback" in i.get("name", ""))
    except FileNotFoundError:
        pass
    return n


def unsubmitted():
    out = []
    for f in sorted(glob.glob(f"{slot}/资料/问题卡/Q*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if d.get("拥挤度") is None and not str(d.get("查新状态", "")).startswith("查新中"):
            out.append(os.path.basename(f)[:-5])
    return out


c0 = handbacks(checker)
f0 = [handbacks(f) for f in finders]
t0 = time.time()
while time.time() - t0 < timeout:
    new = unsubmitted()
    done = [handbacks(f) > b for f, b in zip(finders, f0)]
    if handbacks(checker) > c0:
        why = "查新子代理交回"; break
    if len(new) >= batch:
        why = "新卡够一批"; break
    if all(done):
        why = "找卡全部交回"; break
    time.sleep(15)
else:
    why = "超时"
print(why, "| 未提交:", new, "| 找卡交回:", done, "| 查新交回次数:", handbacks(checker), "| 用时", round(time.time() - t0), "秒")
