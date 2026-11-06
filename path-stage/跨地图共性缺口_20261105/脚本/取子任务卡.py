# -*- coding: utf-8 -*-
"""从并行检索子任务的记录中取出交回的 JSON 卡片数组，落到 资料/扩展候选卡_<路>.json。"""
import json, sys
src, out = sys.argv[1], sys.argv[2]
best = None
for line in open(src, encoding="utf-8"):
    d = json.loads(line)
    c = d.get("message", {}).get("content")
    if not isinstance(c, list):
        continue
    for i in c:
        blobs = [i.get("text", "")] if i.get("type") == "text" else []
        if i.get("type") == "tool_use":
            blobs += [v for v in (i.get("input") or {}).values() if isinstance(v, str)]
        for s in blobs:
            k = s.find("[\n{") if "[\n{" in s else s.find("[{")
            if k < 0:
                continue
            try:
                arr, _ = json.JSONDecoder().raw_decode(s[k:])
                if isinstance(arr, list) and arr and "具体问题" in arr[0]:
                    best = arr
            except json.JSONDecodeError:
                pass
for card in best:
    for e in card["证据"]:
        if e.get("作品ID") == "2611.11647":
            e["作品ID"] = "2610.11647"
        if e.get("证据边界") and "作者 Gün" in e["证据边界"]:
            e["证据边界"] = "摘要级；作者与机构本轮未核实"
json.dump(best, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, len(best), [c["临时id"] for c in best])
