# -*- coding: utf-8 -*-
"""标题筛：去掉已有地图覆盖方向与应用领域噪声，只保留强诊断词标题；按主题输出 ID+标题，并做主题计数。"""
import json, re, sys, collections
j = json.load(open(sys.argv[1], encoding="utf-8"))
STRONG = r"fail|pitfall|revisit|rethink|\bwhy\b|illusion|myth|really|hidden|paradox|collapse|empirical study|systematic study|surpris|diagnos|mirage|limitation|brittle|lessons|n't|\bnot\b|\bdoes\b|\?|counterintuit|shortcut|overestimat|underestimat|negative result|break|trap"
COVERED = r"\bagent|agentic|RLVR|reasoning model|chain-of-thought|\bCoT\b|misalign|self-improv|self-evolv|latent reasoning|diffusion language|\bdLLM|jailbreak|reward hack|on-policy distill|\bLLM-as|tool[- ]use|tool[- ]call|quantiz|looped|recurrent depth"
APP = r"medical|clinical|patient|radiolog|patholog|remote sensing|satellite|traffic|financ|stock|legal|EEG|fMRI|brain|surgical|agricult|crop|cancer|tumor|MRI|CT\b|ultrasound|histopath|dental|retina|power grid|battery|manufactur|education|student|student's|news|social media|hate|fake|misinformation|e-commerce|wireless|5G|6G|IoT|UAV|drone|autonomous driving|driving"
out = collections.defaultdict(list); cnt = collections.Counter(); kept = 0
for p in j["papers"]:
    if not ("2026-05-04" <= p["published"] <= "2026-11-04"): continue
    t = p["title"]
    for tp in p["topics"]: cnt[tp] += 1
    if re.search(COVERED, t, re.I) or re.search(APP, t, re.I) or not re.search(STRONG, t, re.I): continue
    kept += 1; out[p["topics"][0]].append(p)
print("kept", kept)
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for tp, L in out.items():
        f.write(f"## {tp} ({len(L)}/{cnt[tp]})\n")
        for p in sorted(L, key=lambda x: x["published"]): f.write(f"{p['id']} {p['title'][:120]}\n")
