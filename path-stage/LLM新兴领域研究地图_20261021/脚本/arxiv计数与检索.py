# -*- coding: utf-8 -*-
"""阶段1：按主题统计 arXiv totalResults（当前窗口、去年同期、当前窗口逐月）；阶段2：按主题+诊断词按相关度取候选。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); from 主题定义 import TOPICS, LLM, DIAG, q
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W1 = ("202604210000", "202610212359"); W0 = ("202504210000", "202510212359")
MONTHS = [("202604210000","202607202359"),("202607210000","202610212359")]  # 当前窗口前/后半
def call(sq, start=0, maxr=1, sort="submittedDate"):
    p = {"search_query": sq, "start": start, "max_results": maxr, "sortBy": sort, "sortOrder": "descending"}
    req = urllib.request.Request("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(p), headers={"User-Agent": "landscape-search/1.0"})
    for a in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as r: root = ET.fromstring(r.read())
            t = root.find(OS + "totalResults"); time.sleep(3)
            return root, int(t.text) if t is not None else -1
        except Exception: time.sleep(8 * (a + 1))
    return None, -1
def win(w): return f" AND submittedDate:[{w[0]} TO {w[1]}]"
out = Path(sys.argv[1]); stage = sys.argv[2]
if stage == "count":
    res = {}
    for name in ["__LLM全部__"] + list(TOPICS):
        base = LLM if name == "__LLM全部__" else q(name)
        r = {"W1": call(base + win(W1))[1], "W0": call(base + win(W0))[1], "前后半": [call(base + win(m))[1] for m in MONTHS]}
        res[name] = r; print(name, r, flush=True)
        out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
else:
    papers, log = {}, []
    for name in TOPICS:
        root, total = call(f"({q(name)}) AND {DIAG}" + win(W1), 0, 80, "relevance")
        if root is None: log.append({"topic": name, "error": "fetch failed"}); continue
        es = root.findall(NS + "entry")
        for e in es:
            aid = e.find(NS + "id").text.split("/abs/")[-1].rsplit("v", 1)[0]
            rec = papers.setdefault(aid, {"id": aid, "title": " ".join(e.find(NS + "title").text.split()),
                "published": e.find(NS + "published").text[:10], "summary": " ".join(e.find(NS + "summary").text.split())[:900], "topics": []})
            rec["topics"].append(name)
        log.append({"topic": name, "total": total, "got": len(es)}); print(name, total, len(es), flush=True)
    out.write_text(json.dumps({"log": log, "papers": list(papers.values())}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("unique", len(papers))
