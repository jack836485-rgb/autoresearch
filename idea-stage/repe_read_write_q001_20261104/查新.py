import sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
NS = "{http://www.w3.org/2005/Atom}"
Q = {
 "output-null/potent": '(abs:"output-null" OR abs:"output-potent" OR abs:"null space" OR abs:"nullspace") AND (abs:steering OR abs:probe OR abs:probing) AND (abs:"language model" OR abs:LLM)',
 "forking/decision token steering": '(abs:"forking token" OR abs:"forking tokens" OR abs:"decision point" OR abs:"decision points" OR abs:"high-entropy tokens" OR abs:"critical tokens") AND (abs:steering OR abs:"activation steering" OR abs:intervention)',
 "input-dependent / hypernetwork steering": '(abs:hypernetwork OR abs:"input-dependent" OR abs:"input-conditioned" OR abs:"instance-specific" OR abs:"per-input") AND (abs:"steering vector" OR abs:"activation steering" OR abs:"steering vectors")',
 "probe direction vs steering direction": '(abs:"probe direction" OR abs:"probing direction" OR abs:"probe directions") AND (abs:"steering" ) AND (abs:causal OR abs:intervention)',
}
for k, q in Q.items():
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": 25, "sortBy": "relevance"})
    root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "nov/1.0"}), timeout=120).read())
    print("##", k)
    for e in root.findall(NS + "entry"):
        print(e.find(NS + "id").text.split("/abs/")[-1][:-2], e.find(NS + "published").text[:10], " ".join(e.find(NS + "title").text.split())[:100])
    time.sleep(3)
