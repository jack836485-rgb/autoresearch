import urllib.request, urllib.parse, xml.etree.ElementTree as ET, json, sys, time
Q = [
 'abs:"pass@k" AND abs:agent AND abs:"multi-turn"',
 'abs:"pass@k" AND abs:agentic AND abs:RL',
 'abs:"sharpening" AND abs:agent AND abs:RL',
 'abs:coverage AND abs:"multi-turn" AND abs:"reinforcement learning" AND abs:agent',
 'abs:"reasoning boundary" AND abs:agent',
 'abs:"capability boundary" AND abs:agent AND abs:RL',
 'abs:diversity AND abs:"multi-turn" AND abs:agent AND abs:RL AND abs:collapse',
 'abs:"forward KL" AND abs:agent AND abs:RL',
 'abs:WebShop AND abs:ALFWorld AND abs:"pass@k"',
 'abs:"turn-level" AND abs:diversity AND abs:agent AND abs:RL',
 'abs:exploration AND abs:"pass@k" AND abs:"multi-turn"',
 'abs:"replay" AND abs:diversity AND abs:agent AND abs:RLVR',
]
NS={'a':'http://www.w3.org/2005/Atom'}
seen={}
for q in Q:
    url='http://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':q,'sortBy':'submittedDate','sortOrder':'descending','max_results':40})
    try:
        x=urllib.request.urlopen(url,timeout=60).read()
    except Exception as e:
        print('ERR',q,e); continue
    for en in ET.fromstring(x).findall('a:entry',NS):
        pid=en.find('a:id',NS).text.split('/abs/')[-1]
        pub=en.find('a:published',NS).text[:10]
        if pub < sys.argv[1]: continue
        t=' '.join(en.find('a:title',NS).text.split())
        s=' '.join(en.find('a:summary',NS).text.split())
        seen.setdefault(pid,{'id':pid,'date':pub,'title':t,'abs':s,'q':[]})['q'].append(q)
    time.sleep(3)
json.dump(sorted(seen.values(),key=lambda r:r['date'],reverse=True),open('候选.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(seen))
