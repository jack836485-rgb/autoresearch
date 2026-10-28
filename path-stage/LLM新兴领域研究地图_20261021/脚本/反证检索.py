# -*- coding: utf-8 -*-
"""对候选领域盲区做定向反证检索（不限窗口与机构），只打印标题、日期、摘要前段。"""
import sys, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
NS = "{http://www.w3.org/2005/Atom}"
Q = {
 "自动研究-择优噪声": '(abs:"AI scientist" OR abs:autoresearch OR abs:"automated research" OR abs:"research agent" OR abs:"ML engineering agent" OR abs:"MLE-bench") AND (abs:"selection bias" OR abs:"winner\'s curse" OR abs:"seed variance" OR abs:"multiple comparisons" OR abs:"overfit" OR abs:"validation set" OR abs:"noisy evaluation")',
 "循环深度-等FLOPs": '(abs:looped OR abs:"recurrent depth" OR abs:"depth-recurrent" OR abs:"latent reasoning" OR abs:"continuous thought") AND (abs:"FLOP-matched" OR abs:"FLOPs-matched" OR abs:"iso-FLOP" OR abs:"compute-matched" OR abs:"same compute" OR abs:"matched compute")',
 "OPD-与RL等计算": '(abs:"on-policy distillation" OR abs:"self-distillation") AND (abs:"compute-matched" OR abs:"same compute" OR abs:"matched compute" OR abs:"compute budget" OR abs:"FLOPs" OR abs:"cost") AND (abs:"reinforcement learning" OR abs:GRPO)',
}
for name, q in Q.items():
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": 15, "sortBy": "relevance"})
    root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "landscape/1.0"}), timeout=120).read())
    print("##", name, root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)
    for e in root.findall(NS + "entry"):
        i = e.find(NS + "id").text.split("/abs/")[-1]
        print(f"[{i}] {e.find(NS+'published').text[:10]} {' '.join(e.find(NS+'title').text.split())[:110]}\n   {' '.join(e.find(NS+'summary').text.split())[:260]}")
    time.sleep(3)
