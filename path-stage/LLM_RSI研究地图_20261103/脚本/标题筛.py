# -*- coding: utf-8 -*-
"""核心 RSI 主题全量列标题；泛主题只列带诊断词的标题。只决定哪些标题进入人工通读。"""
import json, re, sys
CORE = {"RSI核心", "自改进agent", "自修改/自指", "harness/agent设计自动化", "AI4AI/自动化研究", "安全/监督"}
D = r"fail|failure|limit|pitfall|\bwhen\b|\bwhy\b|\bdoes\b|\bdo\b|\bcan\b|\bis\b|\bare\b|illusion|myth|revisit|rethink|empirical|systematic|\bstudy\b|understanding|collapse|hidden|trap|really|\bnot\b|n't|unreliab|brittle|fragil|break|counter|paradox|surpris|degrad|harm|trade-?off|survey|lesson|\bwhat\b|\bhow\b|diagnos|mirage|overestimat|blind|gap|vulnerab|hack|plateau|regress|overfit|bound|theory|theoretical|dynamics|stagnat"
j = json.load(open(sys.argv[1], encoding="utf-8"))
ps = [p for p in j["papers"] if "2026-05-03" <= p["published"] <= "2026-11-03"]
core = [p for p in ps if CORE & set(p["topics"])]
other = [p for p in ps if not (CORE & set(p["topics"])) and re.search(D, p["title"], re.I)]
print("window", len(ps), "core", len(core), "other_diag", len(other))
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for tag, L in (("C", core), ("O", other)):
        for p in sorted(L, key=lambda x: x["published"]):
            f.write(f"{tag} {p['id']} {p['title']}\n")
