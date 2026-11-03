# -*- coding: utf-8 -*-
"""按标题关键词给窗口内候选计数（只描述分布；检索有分页与查询式边界，不据此判断趋势）。可多标签。"""
import json, re, sys, collections
C = {
 "标题含 RSI/递归自我改进": r"\bRSI\b|recursive(ly)? self-improv|recursive.*self-improv",
 "Harness 演化/优化": r"harness",
 "AI4AI/自动化研究/AI 科学家": r"auto-?research|AI scientist|research agent|autonomous research|AI R&D|post-training|AI4AI|machine learning engineering|\bMLE\b",
 "技能/记忆/经验自进化": r"skill|memory|memories|experien",
 "权重级自训练/自博弈": r"self-play|self-train|self-reward|label-free|unsupervised RLVR|self-distill|intrinsic reward",
 "崩溃/退化": r"collapse|degrad|regress|forget|amnesia|drift",
 "评测/基准": r"bench|evaluat|audit|arena|gym",
 "安全/作弊/监督": r"safe|hack|sabotage|cheat|tamper|poison|control|oversight|misevol|guardrail",
 "理论/极限": r"theor|limit|bound|convergence|dynamics|kinetic|criticality",
}
j = json.load(open(sys.argv[1], encoding="utf-8"))
ps = [p for p in j["papers"] if "2026-05-03" <= p["published"] <= "2026-11-03"]
cnt = collections.Counter(); half = collections.Counter()
for p in ps:
    for k, rx in C.items():
        if re.search(rx, p["title"], re.I):
            cnt[k] += 1; half[(k, "5-7月" if p["published"] < "2026-08-03" else "8-10月")] += 1
print("窗口内候选", len(ps))
for k in C: print(f"{k}\t{cnt[k]}\t前半 {half[(k,'5-7月')]}\t后半 {half[(k,'8-10月')]}")
