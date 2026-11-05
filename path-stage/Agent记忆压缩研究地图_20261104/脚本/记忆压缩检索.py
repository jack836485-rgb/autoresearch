# -*- coding: utf-8 -*-
"""Agent 记忆/上下文压缩广筛：按子问题查询 arXiv，窗口内全部取回（仅发现，不判资格）。stdout 只打印每个查询的计数与日期跨度。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W = ("202605040000", "202611042359")
AG = '(abs:agent OR abs:agents OR abs:agentic OR abs:"multi-turn" OR abs:"tool use" OR abs:"tool-use" OR abs:"long-horizon")'
Q = {
 "上下文压缩/管理": f'(abs:"context compression" OR abs:"context compaction" OR abs:"context management" OR abs:"context folding" OR abs:"context summarization" OR abs:"context pruning" OR abs:"context engineering" OR abs:"context window management" OR abs:"context condensation") AND {AG}',
 "记忆管理/重写/遗忘": f'(abs:"memory management" OR abs:"memory consolidation" OR abs:"memory rewriting" OR abs:"memory update" OR abs:"memory compression" OR abs:"memory forgetting" OR abs:"forgetting mechanism" OR abs:"memory eviction" OR abs:"memory pruning" OR abs:"agentic memory" OR abs:"agent memory" OR abs:"memory agent") AND {AG}',
 "KV cache+agent/多轮": f'(abs:"KV cache" OR abs:"KV-cache" OR abs:"key-value cache") AND {AG}',
 "KV 压缩通用": 'abs:"KV cache compression" OR abs:"KV cache eviction" OR abs:"token eviction" OR abs:"KV eviction" OR abs:"KV compression" OR abs:"cache eviction"',
 "轨迹/历史/观察压缩": '(abs:"trajectory compression" OR abs:"history compression" OR abs:"observation pruning" OR abs:"observation compression" OR abs:"trajectory reduction" OR abs:"history summarization" OR abs:"interaction history" OR abs:"tool output" OR abs:"tool outputs") AND (abs:compress OR abs:compression OR abs:prune OR abs:pruning OR abs:summarization OR abs:token)',
 "长程 agent 上下文": '(abs:"long-horizon" OR abs:"long horizon") AND (abs:"context length" OR abs:"context window" OR abs:"context limit" OR abs:"context overflow" OR abs:memory) AND (abs:agent OR abs:agents OR abs:agentic)',
 "潜在/参数化记忆": f'(abs:"latent memory" OR abs:"memory tokens" OR abs:"gist tokens" OR abs:"compressed memory" OR abs:"parametric memory" OR abs:"soft prompt compression" OR abs:"context distillation") AND {AG}',
 "prompt 压缩+agent": f'(abs:"prompt compression" OR abs:"token pruning" OR abs:"token reduction" OR abs:"token budget" OR abs:"token efficiency" OR abs:"token-efficient") AND {AG}',
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
out = Path(sys.argv[1]); papers, log = {}, []
for name, qq in Q.items():
    base = f"({qq}) AND submittedDate:[{W[0]} TO {W[1]}]"
    got, start, dates, total = 0, 0, [], -1
    while True:
        root, total = call(base, start)
        if root is None: log.append({"q": name, "error": f"fetch failed at {start}"}); break
        es = root.findall(NS + "entry")
        for e in es:
            aid = e.find(NS + "id").text.split("/abs/")[-1].rsplit("v", 1)[0]
            pub = e.find(NS + "published").text[:10]; dates.append(pub)
            rec = papers.setdefault(aid, {"id": aid, "title": " ".join(e.find(NS + "title").text.split()), "published": pub,
                "summary": " ".join(e.find(NS + "summary").text.split()), "cats": [c.get("term") for c in e.findall(NS + "category")], "q": []})
            rec["q"].append(name)
        got += len(es); start += 200
        if not es or start >= total: break
    log.append({"q": name, "total": total, "got": got, "最早": min(dates) if dates else None, "最晚": max(dates) if dates else None})
    print(log[-1], flush=True)
    out.write_text(json.dumps({"log": log, "papers": list(papers.values())}, ensure_ascii=False, indent=0), encoding="utf-8")
print("unique", len(papers))
