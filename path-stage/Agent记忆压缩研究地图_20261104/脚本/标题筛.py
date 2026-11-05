# -*- coding: utf-8 -*-
"""本地：相关性过滤（压缩/记忆操作 × agent/多轮/长程）+ 标题主题计数 + 可选输出标题列表。只用于发现。
用法：python 标题筛.py [diag|all|kv]"""
import json, re, sys, collections
d = json.load(open("资料/arxiv候选.json", encoding="utf-8"))["papers"]
CMP = r"compress|compaction|condens|summar|prun|evict|forget|drop|KV[- ]cache|key-value cache|memory management|consolidat|token budget|context management|context folding|fold|rewrit|distill|gist|sparsif|retention|discard|truncat|offload|token reduction|token-efficient|context engineering"
AGT = r"\bagent|agentic|multi-turn|multi-round|tool[- ]use|tool call|long-horizon|long horizon|interactive|conversation|dialog|web brows|deep research|SWE|software engineering|terminal"
def rel(p):
    s = p["title"] + " " + p["summary"]
    return re.search(CMP, s, re.I) and re.search(AGT, s, re.I)
R = [p for p in d if rel(p)]
KVONLY = [p for p in d if not rel(p) and re.search(r"KV|cache", p["title"] + p["summary"])]
TOP = {
 "KV cache 压缩/驱逐": r"KV|cache|evict",
 "上下文压缩/摘要/折叠": r"context|compress|compaction|summar|fold|condens",
 "记忆系统/管理": r"memory|memor",
 "遗忘/删除/剪枝": r"forget|prun|drop|discard|delet|evict",
 "记忆重写/更新/整合": r"rewrit|updat|consolidat|evolv|refine|revis",
 "RL 训练": r"reinforcement|\bRL\b|GRPO|policy optim|reward",
 "评测/benchmark": r"bench|evaluat|arena",
 "失败/诊断/实证": r"fail|limitation|pitfall|rethink|revisit|why|when|empirical|study|survey|understand|lesson|illusion|really|hidden|gap|matter|does|do |analy",
 "深度研究/搜索": r"research|search|web|brows",
 "代码/SWE/终端": r"code|coding|SWE|software|terminal|repositor",
 "效率/系统/服务": r"efficien|latency|throughput|serving|system|fast|speed",
}
c = collections.Counter(); mon = collections.defaultdict(collections.Counter)
for p in R:
    for k, rx in TOP.items():
        if re.search(rx, p["title"], re.I): c[k] += 1; mon[k][p["published"][:7]] += 1
months = sorted({p["published"][:7] for p in R})
print("相关", len(R), "/", len(d), "；未入相关但含 KV/cache", len(KVONLY))
print("主题\t合计\t" + "\t".join(m[5:] for m in months))
for k in TOP: print(f"{k}\t{c[k]}\t" + "\t".join(str(mon[k][m]) for m in months))
tot = collections.Counter(p["published"][:7] for p in R); print("全部\t" + str(len(R)) + "\t" + "\t".join(str(tot[m]) for m in months))
json.dump(R, open("资料/相关候选.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
mode = sys.argv[1] if len(sys.argv) > 1 else ""
TT = r"compress|compaction|condens|summar|prun|evict|forget|drop|KV|cache|memory|memor|context|fold|rewrit|consolidat|token|retention|discard|long-horizon|long horizon|budget"
if mode == "all":
    for p in sorted(R, key=lambda x: x["published"]):
        if re.search(TT, p["title"], re.I): print(p["id"], p["title"])
if mode == "kv":
    for p in sorted(KVONLY, key=lambda x: x["published"]): print(p["id"], p["title"])
