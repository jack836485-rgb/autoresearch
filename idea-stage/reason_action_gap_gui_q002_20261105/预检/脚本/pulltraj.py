import sys,io,zipfile,urllib.request,json,os,concurrent.futures as cf
url,out=sys.argv[1],sys.argv[2]; lim=int(sys.argv[3]) if len(sys.argv)>3 else 10**9
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
r0=R(url); z=zipfile.ZipFile(io.BufferedReader(r0,buffer_size=1<<20))
want=[n for n in z.namelist() if n.endswith('traj.jsonl') or n.endswith('result.txt')][:lim]
os.makedirs(out,exist_ok=True)
def get(n):
    zz=zipfile.ZipFile(io.BufferedReader(R(url,r0.n),buffer_size=1<<16))
    return n, zz.read(n)
res={}
with cf.ThreadPoolExecutor(16) as ex:
    for n,b in ex.map(get,want): res[n]=b.decode('utf-8','replace')
json.dump(res,open(os.path.join(out,'files.json'),'w'))
print(len(want),'files')
