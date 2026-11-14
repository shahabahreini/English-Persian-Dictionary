import sys,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import fanorm
S=sys.argv[1]
rows=[l.rstrip('\n').split('\t',1) for l in open(S+'/unpacked/v24.tsv',encoding='utf-8')]
H={h for h,_ in rows}
web={}
for i,l in enumerate(open(S+'/ref/count_1w.txt')): web[l.split('\t')[0]]=i
sysd={x.strip().lower() for x in open('/usr/share/dict/words')}
known=set(web)|sysd
strong={w for w,r in web.items() if r<150000}|sysd
AL='abcdefghijklmnopqrstuvwxyz'
def ed1(w):
    s=set()
    for i in range(len(w)+1):
        a,b=w[:i],w[i:]
        if b: s.add(a+b[1:])
        if len(b)>1: s.add(a+b[1]+b[0]+b[2:])
        for c in AL:
            s.add(a+c+b)
            if b: s.add(a+c+b[1:])
    s.discard(w); return s
def sugg(t):
    c=[x for x in ed1(t) if x in strong]
    c.sort(key=lambda x:(x not in H, web.get(x,10**7)))
    return c[:3]
out=[]
for h,d in rows:
    toks=h.split()
    bad=[t for t in toks if re.fullmatch(r'[a-z]{4,}',t) and t not in known]
    if not bad or len(bad)>1: continue
    t=bad[0]; sg=sugg(t)
    if not sg: continue
    out.append('%s\t%s\t%s'%(h,' / '.join(h.replace(t,x,1) for x in sg),fanorm.normalize(d)[:110]))
print(len(out))
N=3
for i in range(N): open(S+'/typo/typo_%d.tsv'%i,'w',encoding='utf-8').write('\n'.join(out[i::N])+'\n')
print('\n'.join(out[::400]))
