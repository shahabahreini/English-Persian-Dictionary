import sys,re,os
S=sys.argv[1]
H={l.split('\t',1)[0].lower() for l in open(S+'/unpacked/v24.tsv',encoding='utf-8')}
def has(w):
    if w in H: return True
    for suf,rep in [('s',''),('es',''),('ies','y'),('ed',''),('ed','e'),('d',''),('ing',''),('ing','e'),('ly',''),('er',''),('er','e'),('est',''),('est','e'),("'s",''),('ier','y'),('iest','y'),('ied','y'),('ily','y'),('ness',''),('ment','')]:
        if w.endswith(suf) and len(w)-len(suf)>=2:
            b=w[:-len(suf)]+rep
            if b in H: return True
            if suf in('ed','ing','er','est') and len(b)>2 and b[-1]==b[-2] and b[:-1] in H: return True
    return False
sub={}
for i,l in enumerate(open(S+'/ref/en_50k.txt',encoding='utf-8')):
    w=l.split()[0]; sub[w]=i
web={}
for i,l in enumerate(open(S+'/ref/count_1w.txt')):
    w=l.split('\t')[0]; web[w]=i
    if i>120000: break
sysd={x.strip().lower() for x in open('/usr/share/dict/words')}
cand=[]
for w,r in web.items():
    if not re.fullmatch(r'[a-z]{3,}',w) or has(w): continue
    cand.append((r,sub.get(w,10**6),w, w in sysd))
print('missing in web top120k',len(cand),'of which in sysdict',sum(c[3] for c in cand),'in subs50k',sum(1 for c in cand if c[1]<10**6))
both=[c for c in cand if c[1]<10**6 or c[3]]
print('both-ish',len(both))
print(' '.join(c[2] for c in cand[:400]))
print('-----in sysdict or subs, top 500')
print(' '.join(c[2] for c in both[:500]))
print('----- tail sample'); print(' '.join(c[2] for c in both[3000:3200]))
open(S+'/ref/gap_all.txt','w').write('\n'.join('%d\t%d\t%s\t%d'%c for c in cand))
# also inflected forms count present directly
