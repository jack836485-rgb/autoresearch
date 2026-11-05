# -*- coding: utf-8 -*-
"""本地：GUI 相关性过滤 + 标题主题计数 + 诊断类标题输出。只用于发现。"""
import json, re, sys, collections
d = json.load(open("资料/arxiv候选.json", encoding="utf-8"))["papers"]
REL = r"\bGUI|computer[- ]us|OSWorld|AndroidWorld|ScreenSpot|screenshot|mobile agent|phone|smartphone|Android|desktop|browser|web agent|web navigation|WebArena|Mind2Web|user interface|\bUI\b|screen"
rel = [p for p in d if re.search(REL, p["title"] + " " + p["summary"], re.I) and re.search(r"agent|grounding|navigation|automation", p["title"] + " " + p["summary"], re.I)]
TOP = {
 "grounding/感知": r"ground|screen|perception|locat|element|click|visual",
 "RL/训练": r"reinforcement|\bRL\b|GRPO|policy optim|reward|train",
 "数据/轨迹合成": r"data|synthe|trajector|corpus|scal",
 "环境/仿真/世界模型": r"environment|world model|simulat|sandbox|emulat|gym",
 "评测/benchmark": r"bench|evaluat|arena|leaderboard",
 "安全/攻击/注入": r"safety|safe|attack|injection|adversar|jailbreak|risk|harm|privacy|secur|trust",
 "记忆/经验/自进化": r"memory|experience|self-evolv|skill|continual|lifelong",
 "规划/长程/反思": r"plan|long-horizon|reflect|recover|error|verif|critic",
 "效率/延迟/token": r"efficien|latency|token|fast|cost|compress|cache",
 "失败/诊断/实证": r"fail|limitation|pitfall|rethink|revisit|why|when|empirical|study|survey|understand|lesson|illusion|really|hidden|gap",
 "移动端": r"mobile|phone|android|smartphone",
 "网页": r"\bweb|browser",
}
c = collections.Counter(); mon = collections.defaultdict(collections.Counter)
for p in rel:
    for k, rx in TOP.items():
        if re.search(rx, p["title"], re.I): c[k] += 1; mon[k][p["published"][:7]] += 1
months = sorted({p["published"][:7] for p in rel})
print("相关", len(rel), "/", len(d))
print("主题\t合计\t" + "\t".join(m[5:] for m in months))
for k in TOP: print(f"{k}\t{c[k]}\t" + "\t".join(str(mon[k][m]) for m in months))
tot = collections.Counter(p["published"][:7] for p in rel); print("全部\t" + str(len(rel)) + "\t" + "\t".join(str(tot[m]) for m in months))
json.dump(rel, open("资料/相关候选.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
DIAG = r"fail|limitation|pitfall|rethink|revisit|why |when |empirical|systematic|survey|understand|lesson|illusion|really|hidden|gap|does |do |are |can |brittle|paradox|collapse|degrad|beyond|audit|analys|diagnos|myth|matter|not |vs\.?|versus|trade-?off|bottleneck|challenge|position|towards|toward|benchmark"
if len(sys.argv) > 1:
    for p in sorted(rel, key=lambda x: x["published"]):
        if re.search(DIAG, p["title"], re.I): print(p["id"], p["title"])
