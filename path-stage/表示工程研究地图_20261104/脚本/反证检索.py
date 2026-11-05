# -*- coding: utf-8 -*-
"""不限窗口的反证检索：只打印 ID、日期、标题。"""
import sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
NS = "{http://www.w3.org/2005/Atom}"
Q = {
 "KV/多轮传播": '(abs:steering OR abs:"steering vector" OR abs:"activation steering") AND (abs:"KV cache" OR abs:"key-value cache" OR abs:"multi-turn") AND (abs:activation OR abs:representation)',
 "随机方向副作用": '(abs:"activation steering" OR abs:"steering vector" OR abs:"steering vectors") AND (abs:"random direction" OR abs:"random directions" OR abs:"random vector" OR abs:"random vectors" OR abs:"norm-matched")',
 "MoE steering": '(abs:steering OR abs:"representation engineering") AND (abs:"mixture-of-experts" OR abs:MoE) AND (abs:activation OR abs:routing OR abs:router)',
}
for k, q in Q.items():
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": 40, "sortBy": "submittedDate", "sortOrder": "descending"})
    root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "landscape/1.0"}), timeout=120).read())
    print("##", k)
    for e in root.findall(NS + "entry"):
        print(e.find(NS + "id").text.split("/abs/")[-1][:-2], e.find(NS + "published").text[:10], " ".join(e.find(NS + "title").text.split())[:95])
    time.sleep(3)
