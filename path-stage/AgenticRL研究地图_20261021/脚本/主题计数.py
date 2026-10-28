"""按标题关键词给已核实候选打主题标签并按月计数；标签仅用于描述分布，不作资格或质量判断。"""
import json, re, sys, collections
TOPICS = {
 "信用分配/优势估计": r"credit|advantage|turn-level|step-level|process reward|value function|pivotal|progress|bellman",
 "OPD/自蒸馏/特权信息": r"distill|\bOPD\b|OPSD|hindsight|privileged",
 "环境/任务合成与模拟器": r"environment|\benv|gym\b|gyms|world model|synthetic|synthesi|simulat|sandbox|fictional",
 "训练系统/rollout效率": r"asynchron|\basync|scheduling|throughput|prefill|weight transfer|fault toleran|goodput|serving|elastic|kernel|framework|rollout",
 "记忆/技能/自进化/上下文": r"memory|skill|self-evolv|context|compaction|experience|evolving",
 "奖励/验证器/hacking/安全": r"reward hack|verif|rubric|reward model|safety|hack|backdoor|spurious|abuse",
 "探索/熵/稳定性": r"explor|entropy|stabil|collapse",
 "多智能体": r"multi-agent|multi agent",
 "领域:搜索/深度研究": r"search|deep research|\bRAG\b|retriev",
 "领域:代码/SWE/终端": r"\bSWE|cod(e|ing)|terminal|\bCLI\b|software|SQL",
 "领域:GUI/网页/计算机使用": r"\bGUI|\bweb|computer[- ]use|phone|mobile|\bUI\b",
}
a = json.load(open(sys.argv[1], encoding="utf-8"))
ok = [x for x in a if (x["hits"] or x["qs"]) and x["date"] and x["date"] >= sys.argv[2]]
months = sorted({x["date"][:7] for x in ok})
table = collections.defaultdict(collections.Counter)
for x in ok:
    for name, rx in TOPICS.items():
        if re.search(rx, x["title"] or "", re.I):
            table[name][x["date"][:7]] += 1
print("主题\t合计\t" + "\t".join(m[5:] for m in months))
for name in TOPICS:
    print(f"{name}\t{sum(table[name].values())}\t" + "\t".join(str(table[name][m]) for m in months))
total = collections.Counter(x["date"][:7] for x in ok)
print("全部\t" + str(len(ok)) + "\t" + "\t".join(str(total[m]) for m in months))
