import sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
NS = "{http://www.w3.org/2005/Atom}"
Q = {
 "反馈/PID steering": '(abs:"feedback control" OR abs:PID OR abs:"closed-loop" OR abs:"controller") AND (abs:"activation steering" OR abs:"steering vector" OR abs:"representation steering")',
 "steering 随生成累积/漂移/多轮": '(abs:"activation steering" OR abs:"steering vector" OR abs:"steering vectors") AND (abs:"long-form" OR abs:"generation length" OR abs:decay OR abs:drift OR abs:"multi-turn")',
 "KV 与残差通路": '(abs:"activation steering" OR abs:steering) AND (abs:"KV cache" OR abs:"key-value" OR abs:"attention keys") AND (abs:"residual stream" OR abs:pathway OR abs:propagate OR abs:propagation)',
 "推理模型 steering 前缀/一次性": '(abs:"activation steering" OR abs:"steering vector") AND (abs:"reasoning model" OR abs:"reasoning models" OR abs:"long chain-of-thought") AND (abs:prefix OR abs:"first token" OR abs:"one-shot")',
}
def get(u):
    for a in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "nov/1.0"}), timeout=120).read()
        except Exception as e: time.sleep(20*(a+1))
for k, q in Q.items():
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": 25, "sortBy": "relevance"})
    b = get(u)
    print("##", k)
    if not b: print("失败"); continue
    for e in ET.fromstring(b).findall(NS + "entry"):
        print(e.find(NS + "id").text.split("/abs/")[-1][:-2], e.find(NS + "published").text[:10], " ".join(e.find(NS + "title").text.split())[:100])
    time.sleep(5)
