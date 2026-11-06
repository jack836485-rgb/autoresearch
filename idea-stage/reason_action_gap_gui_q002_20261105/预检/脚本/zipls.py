import sys,io,zipfile,urllib.request
url=sys.argv[1]
class R(io.RawIOBase):
    def __init__(s,u):
        s.u=u; s.p=0
        h=urllib.request.urlopen(urllib.request.Request(u,method='HEAD')); s.n=int(h.headers['Content-Length'])
    def seekable(s): return True
    def readable(s): return True
    def seek(s,o,w=0):
        s.p= o if w==0 else (s.p+o if w==1 else s.n+o); return s.p
    def tell(s): return s.p
    def readinto(s,b):
        if s.p>=s.n: return 0
        e=min(s.n,s.p+len(b))-1
        d=urllib.request.urlopen(urllib.request.Request(s.u,headers={'Range':f'bytes={s.p}-{e}'})).read()
        b[:len(d)]=d; s.p+=len(d); return len(d)
z=zipfile.ZipFile(io.BufferedReader(R(url),buffer_size=1<<20))
names=z.namelist(); print('N',len(names))
import collections
print([n for n in names[:40]])
want=[n for n in names if n.endswith('traj.jsonl')][:1]
for w in want:
    t=z.read(w).decode('utf-8','replace'); print('==',w,len(t)); print(t[:2500])
