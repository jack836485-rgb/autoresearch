# -*- coding: utf-8 -*-
"""由 arXiv totalResults 计算各主题在当前窗口与去年同期的篇数、相对 LLM 总量的份额变化；只描述关键词分布。"""
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8")); A = r.pop("__LLM全部__")
rows = []
for k, v in r.items():
    s1, s0 = v["W1"] / A["W1"], v["W0"] / max(A["W0"], 1)
    rows.append((k, v["W0"], v["W1"], v["W1"] / max(v["W0"], 1), s1 / s0 if s0 else float("inf"), v["前后半"]))
rows.sort(key=lambda x: -x[4])
print(f"LLM锚定词总量: 去年同期 {A['W0']}  当前 {A['W1']}  前/后半 {A['前后半']}")
print("主题\t去年同期\t当前窗口\t篇数倍数\t份额倍数\t前半/后半")
for k, a, b, g, s, h in rows: print(f"{k}\t{a}\t{b}\t{g:.2f}\t{s:.2f}\t{h[0]}/{h[1]}")
