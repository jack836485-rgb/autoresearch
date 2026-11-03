# -*- coding: utf-8 -*-
"""RSI 子问题 arXiv 检索：窗口内按提交日倒序分页取候选（只用于发现，不判资格）；
同时统计去年同期 totalResults 作对照。摘要落盘，不打印。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W1 = ("202605030000", "202611032359"); W0 = ("202505030000", "202511032359")
LLM = '(abs:"language model" OR abs:"language models" OR abs:LLM OR abs:LLMs OR abs:agent OR abs:agents)'
T = {
 "RSI核心": 'abs:"recursive self-improvement" OR abs:"recursively self-improving" OR abs:"recursive self-improving" OR ti:"self-improving"',
 "自改进agent": 'abs:"self-improving agent" OR abs:"self-improving agents" OR abs:"self-improving AI" OR abs:"self-improving system" OR abs:"self-improving systems" OR abs:"self-improving LLM"',
 "自修改/自指": 'abs:"self-modifying" OR abs:"self-referential" OR abs:"Godel agent" OR abs:"Gödel agent" OR abs:"Darwin Godel" OR abs:"Darwin Gödel" OR abs:"self-rewriting"',
 "harness/agent设计自动化": 'abs:"harness optimization" OR abs:"self-evolving harness" OR abs:"harness evolution" OR abs:"automated agent design" OR abs:"meta-agent" OR abs:"agentic system design" OR abs:"agent design search"',
 "AI4AI/自动化研究": 'abs:"automated AI research" OR abs:"AI research agent" OR abs:"AI research agents" OR abs:"automating AI research" OR abs:"AI R&D" OR abs:"automated ML research" OR abs:"research automation" OR abs:"AI scientist" OR abs:"autonomous research" OR abs:"automated post-training" OR abs:"MLE-bench"',
 "自奖励/自博弈训练": 'abs:"self-rewarding" OR abs:"self-play" OR abs:"self-questioning" OR abs:"proposer-solver" OR abs:"Absolute Zero" OR abs:"self-generated curriculum" OR abs:"self-challenging"',
 "无标签/内在奖励RL": 'abs:"label-free" OR abs:"unsupervised RLVR" OR abs:"intrinsic reward" OR abs:"self-certainty" OR abs:"test-time reinforcement learning" OR abs:"without ground truth" OR (abs:"unlabeled data" AND abs:"reinforcement learning")',
 "自我改进(泛)": 'abs:"self-improvement" OR abs:"self-improve" OR abs:"self-evolution" OR abs:"self-evolving"',
 "上下文/提示自进化": 'abs:"prompt optimization" OR abs:"context evolution" OR abs:"evolving context" OR abs:"playbook" OR abs:"prompt evolution" OR abs:"reflective prompt"',
 "自生成数据/崩溃": 'abs:"model collapse" OR abs:"self-consuming" OR abs:"self-generated data" OR abs:"iterative self-training" OR abs:"self-training"',
 "生成-验证差距/理论": 'abs:"generation-verification gap" OR abs:"verification gap" OR abs:"self-verification" OR abs:"sharpening" OR (abs:"self-improvement" AND abs:theory)',
 "安全/监督": 'abs:"recursive self-improvement" OR abs:"AI R&D automation" OR abs:"automated alignment research" OR abs:"research sabotage" OR (abs:sandbagging AND abs:research) OR (abs:"scalable oversight" AND abs:"self-improvement")',
}
def call(sq, start=0, maxr=1, sort="submittedDate"):
    p = {"search_query": sq, "start": start, "max_results": maxr, "sortBy": sort, "sortOrder": "descending"}
    req = urllib.request.Request("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(p), headers={"User-Agent": "landscape-search/1.0"})
    for a in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: root = ET.fromstring(r.read())
            t = root.find(OS + "totalResults"); time.sleep(3)
            return root, int(t.text) if t is not None else -1
        except Exception: time.sleep(10 * (a + 1))
    return None, -1
def win(w): return f" AND submittedDate:[{w[0]} TO {w[1]}]"
out = Path(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 600
papers, log = {}, []
for name, qq in T.items():
    base = f"({qq}) AND {LLM}"
    _, tot0 = call(base + win(W0))
    got, start, total = 0, 0, None
    dates = []
    while True:
        root, total = call(base + win(W1), start, 200)
        if root is None: log.append({"topic": name, "error": f"fetch failed at {start}"}); break
        es = root.findall(NS + "entry")
        for e in es:
            aid = e.find(NS + "id").text.split("/abs/")[-1].rsplit("v", 1)[0]
            pub = e.find(NS + "published").text[:10]; dates.append(pub)
            rec = papers.setdefault(aid, {"id": aid, "title": " ".join(e.find(NS + "title").text.split()), "published": pub,
                "summary": " ".join(e.find(NS + "summary").text.split()), "topics": []})
            rec["topics"].append(name)
        got += len(es); start += 200
        if not es or start >= min(total, cap): break
    log.append({"topic": name, "W1": total, "W0": tot0, "got": got, "最早": min(dates) if dates else None, "最晚": max(dates) if dates else None})
    print(log[-1], flush=True)
    out.write_text(json.dumps({"log": log, "papers": list(papers.values())}, ensure_ascii=False, indent=0), encoding="utf-8")
print("unique", len(papers))
