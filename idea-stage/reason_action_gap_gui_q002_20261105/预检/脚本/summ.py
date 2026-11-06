import json,re,sys,difflib,collections
ack=re.compile(r"(didn't work|did not work|not work|hasn't|has not|still (not|no|the same|hasn)|no effect|nothing (happened|changed)|unsuccessful|failed|isn't respond|not respond|didn't (change|open|appear|seem)|same (screen|state)|stuck|loop|again|different approach|没有(成功|反应|变化|生效)|仍然|依然|还是没|失败|无效|没反应|再次|重新|换一种|不同的方法)",re.I)
for m in sys.argv[1:]:
    R=[r for r in json.load(open(f'traj/{m}/screenrec.json')) if r['diff'] is not None]
    for r in R: r['ack']=bool(ack.search(r['th']))
    same=[r for r in R if r['diff']<0.002]
    def st(g):
        n=len(g); a=[r for r in g if r['ack']]
        return dict(n=n, fail=round(100*sum(not r['succ'] for r in g)/n), ack=round(100*len(a)/n), copied90=round(100*sum(r['copy']>0.9 for r in g)/n),
                    ack_copied90=round(100*sum(r['copy']>0.9 for r in a)/max(1,len(a))), fresh_ack=round(100*sum(r['copy']<=0.9 for r in a)/n))
    print(m,'all',st(R)); print(m,'screen-same',st(same))
