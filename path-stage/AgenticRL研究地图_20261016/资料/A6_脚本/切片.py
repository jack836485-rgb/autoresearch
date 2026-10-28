import json,sys,re
# 用法: python -X utf8 -I 切片.py <json> mode args
# mode: range start end | grep "regex" ctx [max]
f=sys.argv[1]; d=json.load(open(f,encoding='utf-8')); t=d['text']
mode=sys.argv[2]
if mode=='range':
    a,b=int(sys.argv[3]),int(sys.argv[4]); print(t[a:b])
elif mode=='grep':
    pat=re.compile(sys.argv[3],re.I); ctx=int(sys.argv[4]); mx=int(sys.argv[5]) if len(sys.argv)>5 else 30
    last=-1;n=0
    for m in pat.finditer(t):
        if m.start()<last: continue
        s=max(0,m.start()-ctx); e=min(len(t),m.end()+ctx)
        print(f'--- @{m.start()} ---'); print(t[s:e]); last=e; n+=1
        if n>=mx: break
elif mode=='heads':
    # 粗略找章节标题: 数字编号+大写词
    for m in re.finditer(r'(?:(?<=\s)|^)((?:\d+(?:\.\d+)*|[A-H](?:\.\d+)*)\s+[A-Z][A-Za-z\-:,&\' ]{3,80}?)(?=\s[A-Z][a-z])',t):
        pass
    for m in re.finditer(r'\n',t): pass
    print(t.count('\n'))
