# For recurrent (same action within 3 steps) steps, fetch decision screenshots of the two occurrences and test equality.
import sys,io,zipfile,urllib.request,json,re,difflib,random,collections,concurrent.futures as cf
from PIL import Image, ImageChops
url,files,out=sys.argv[1],sys.argv[2],sys.argv[3]; N=int(sys.argv[4])
sys.path.insert(0,sys.argv[5]); 
F=json.load(open(files))
class R(io.RawIOBase):
    def __init__(s,u,n=None):
        s.u=u; s.p=0
        s.n=n or int(urllib.request.urlopen(urllib.request.Request(u,method='HEAD')).headers['Content-Length'])
    def seekable(s): return True
    def readable(s): return True
    def seek(s,o,w=0): s.p= o if w==0 else (s.p+o if w==1 else s.n+o); return s.p
    def tell(s): return s.p
    def readinto(s,b):
        if s.p>=s.n: return 0
        e=min(s.n,s.p+len(b))-1
        d=urllib.request.urlopen(urllib.request.Request(s.u,headers={'Range':f'bytes={s.p}-{e}'})).read()
        b[:len(d)]=d; s.p+=len(d); return len(d)
r0=R(url); Z=zipfile.ZipFile(io.BufferedReader(r0,buffer_size=1<<20)); names=set(Z.namelist())
infos={i.filename:i for i in Z.infolist()}
def readm(n):
    zz=zipfile.ZipFile.__new__(zipfile.ZipFile)
    z2=zipfile.ZipFile(io.BufferedReader(R(url,r0.n),buffer_size=1<<16)) if False else None
    # reuse central dir: open member via fresh file handle
    fh=io.BufferedReader(R(url,r0.n),buffer_size=1<<16)
    zi=infos[n]; fh.seek(zi.header_offset); 
    h=fh.read(30); import struct
    fnl,exl=struct.unpack('<HH',h[26:30]); fh.read(fnl+exl)
    data=fh.read(zi.compress_size)
    import zlib
    return data if zi.compress_type==0 else zlib.decompress(data,-15)
ack=re.compile(r"(didn't work|did not work|not work|hasn't|has not|still (not|no|the same|hasn)|no effect|nothing (happened|changed)|unsuccessful|failed|isn't respond|not respond|didn't (change|open|appear|seem)|same (screen|state)|stuck|loop|again)",re.I)
def thought(resp):
    if 'Thought:' in resp: resp=resp.split('Thought:',1)[1]
    t=resp.split('</think>')[0]; t=re.split(r'\nAction:|<tool_call>|```|## Action|\n## Code|\'\'\'',t)[0]; return t.strip()
def actkey(a):
    ls=[l.strip() for l in a.splitlines() if l.strip().startswith('pyautogui.') or l.strip() in ('WAIT','DONE','FAIL')]
    return '\n'.join(ls) if ls else a.strip()
trajs=collections.defaultdict(dict)
for k,v in F.items(): d=k.rsplit('/',1)[0]; trajs[d][k.rsplit('/',1)[1]]=v
cands=[]
for d,fs in trajs.items():
    if 'traj.jsonl' not in fs: continue
    st=[json.loads(l) for l in fs['traj.jsonl'].splitlines() if l.strip()]
    try: succ=float(fs.get('result.txt','0').strip() or 0)>0
    except: succ=False
    acts=[actkey(str(s.get('action'))) for s in st]
    for j in range(1,len(st)-1):
        if acts[j+1]!=acts[j] or acts[j] in ('WAIT','DONE','FAIL','None'): continue
        p=[d+'/'+str(st[k].get('screenshot_file')) for k in (j-1,j,j+1)]
        if all(x in names for x in p):
            cands.append(dict(d=d,j=j,p=p,succ=succ,act=acts[j][:60],typ=acts[j].split('(')[0]))
random.seed(0); random.shuffle(cands); cands=cands[:N]
def eq(c):
    try:
        I=[Image.open(io.BytesIO(readm(x))).convert('L').resize((480,270)) for x in c['p']]
        f=lambda A,B: sum(1 for q in ImageChops.difference(A,B).getdata() if q>12)/(480*270)
        c['d01']=f(I[0],I[1]); c['d12']=f(I[1],I[2]); c['diff']=0
    except Exception as e: c['diff']=None; c['err']=str(e)[:80]
    return c
with cf.ThreadPoolExecutor(12) as ex: res=list(ex.map(eq,cands))
json.dump(res,open(out,'w'),ensure_ascii=False)
print('cands',len(res),'errors',sum(r['diff'] is None for r in res))
