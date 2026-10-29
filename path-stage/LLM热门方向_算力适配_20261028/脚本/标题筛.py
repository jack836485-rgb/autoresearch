# -*- coding: utf-8 -*-
"""按标题诊断词筛候选；只决定哪些标题进入人工通读，不判断质量。"""
import json, re, sys, collections
D = r"fail|failure|limit|pitfall|\bwhen\b|\bwhy\b|\bdoes\b|\bdo\b|\bcan\b|\bis\b|\bare\b|illusion|myth|revisit|rethink|empirical|systematic|\bstudy\b|understanding|collapse|hidden|trap|really|\bnot\b|n't|unreliab|brittle|fragil|break|counter|paradox|surpris|degrad|harm|\btax\b|trade-?off|survey|lesson|\bwhat\b|\bhow\b|diagnos|mirage|overestimat|blind|gap|beyond|vulnerab|sensitiv|robust"
j = json.load(open(sys.argv[1], encoding="utf-8"))
ps = [p for p in j["papers"] if p["published"] >= "2026-04-28"]
sel = [p for p in ps if re.search(D, p["title"], re.I)]
print("window", len(ps), "selected", len(sel))
c = collections.Counter(t for p in sel for t in p["topics"]); print(dict(c))
json.dump(sel, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
