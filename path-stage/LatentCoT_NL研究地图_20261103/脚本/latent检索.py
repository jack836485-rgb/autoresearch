# -*- coding: utf-8 -*-
"""latent reasoning 子问题 arXiv 检索（只用于发现，不判资格）。窗口 2026-05-03~2026-11-03，摘要落盘不打印。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W1 = ("202605030000", "202611032359")
LLM = '(abs:"language model" OR abs:"language models" OR abs:LLM OR abs:LLMs OR abs:reasoning)'
T = {
 "latent CoT核心": 'abs:"latent reasoning" OR abs:"latent chain-of-thought" OR abs:"latent chain of thought" OR abs:"latent CoT" OR abs:"continuous chain-of-thought" OR abs:"continuous chain of thought" OR abs:"continuous thought" OR abs:"continuous thoughts" OR abs:"latent thoughts" OR abs:"latent thought"',
 "隐式推理": 'abs:"implicit chain-of-thought" OR abs:"implicit chain of thought" OR abs:"implicit reasoning" OR abs:"implicit CoT"',
 "方法名": 'abs:Coconut OR abs:CODI OR abs:CoLaR OR abs:"SIM-CoT" OR abs:"soft thinking" OR abs:"soft tokens" OR abs:"latent tokens" OR abs:"reasoning in latent space" OR abs:"continuous latent space"',
 "CoT压缩到隐空间": '(abs:"chain-of-thought compression" OR abs:"CoT compression" OR abs:"compressed chain-of-thought" OR abs:"compress reasoning") AND (abs:latent OR abs:continuous OR abs:hidden)',
 "循环/深度推理": 'abs:"looped transformer" OR abs:"looped transformers" OR abs:"recurrent depth" OR abs:"latent recurrence" OR abs:"depth-recurrent"',
}
def call(sq, start=0, maxr=200):
    p = {"search_query": sq, "start": start, "max_results": maxr, "sortBy": "submittedDate", "sortOrder": "descending"}
    req = urllib.request.Request("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(p), headers={"User-Agent": "landscape-search/1.0"})
    for a in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: root = ET.fromstring(r.read())
            t = root.find(OS + "totalResults"); time.sleep(3)
            return root, int(t.text) if t is not None else -1
        except Exception: time.sleep(10 * (a + 1))
    return None, -1
out = Path(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 800
papers, log = {}, []
for name, qq in T.items():
    base = f"({qq}) AND {LLM} AND submittedDate:[{W1[0]} TO {W1[1]}]"
    got, start, total, dates = 0, 0, None, []
    while True:
        root, total = call(base, start)
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
    log.append({"topic": name, "total": total, "got": got, "最早": min(dates) if dates else None, "最晚": max(dates) if dates else None})
    print(log[-1], flush=True)
    out.write_text(json.dumps({"log": log, "papers": list(papers.values())}, ensure_ascii=False, indent=0), encoding="utf-8")
print("unique", len(papers))
