# -*- coding: utf-8 -*-
"""表示工程子问题 arXiv 检索（只用于发现，不判资格）。窗口 2026-05-04~2026-11-04，摘要落盘不打印。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W1 = ("202605040000", "202611042359")
LLM = '(abs:"language model" OR abs:"language models" OR abs:LLM OR abs:LLMs OR abs:transformer OR abs:transformers)'
T = {
 "steering核心": 'abs:"activation steering" OR abs:"steering vector" OR abs:"steering vectors" OR abs:"representation engineering" OR abs:"representation steering" OR abs:"activation addition" OR abs:"contrastive activation addition" OR abs:"inference-time intervention" OR abs:"latent steering" OR abs:"hidden state steering" OR abs:"steering directions" OR abs:"steering direction"',
 "steering泛称": '(abs:steering OR abs:steer) AND (abs:activation OR abs:activations OR abs:"hidden states" OR abs:"residual stream" OR abs:representation OR abs:representations)',
 "SAE特征干预": '(abs:"sparse autoencoder" OR abs:"sparse autoencoders" OR abs:SAE OR abs:SAEs OR abs:transcoder OR abs:transcoders) AND (abs:steering OR abs:steer OR abs:intervention OR abs:interventions OR abs:ablation OR abs:clamping)',
 "表示微调与编辑": 'abs:"representation fine-tuning" OR abs:"representation finetuning" OR abs:ReFT OR abs:"activation editing" OR abs:"representation editing" OR abs:"low-rank intervention" OR abs:"activation patching" OR abs:"directional ablation"',
 "概念方向与擦除": 'abs:"refusal direction" OR abs:"persona vector" OR abs:"persona vectors" OR abs:"concept erasure" OR abs:"linear representation hypothesis" OR abs:"concept vector" OR abs:"concept vectors" OR abs:"function vector" OR abs:"function vectors" OR abs:"task vector" OR abs:"in-context vector"',
 "表示级安全": 'abs:"circuit breakers" OR abs:"representation rerouting" OR abs:"latent adversarial training" OR (abs:"representation" AND abs:"unlearning" AND abs:"steering") OR (abs:"activation" AND abs:"jailbreak" AND abs:"steering")',
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
out = Path(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
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
