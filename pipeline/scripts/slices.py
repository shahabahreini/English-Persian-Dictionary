import sys,re
S=sys.argv[1]
rows=[l.split('\t') for l in open(S+'/ref/gap_all.txt').read().split('\n')]
sel=[r[2] for r in rows if (int(r[1])<10**6 or r[3]=='1') or int(r[0])<30000]
print(len(sel))
N=8
for i in range(N):
    open(S+'/cand/slice_%d.txt'%i,'w').write('\n'.join(sel[i::N])+'\n')
# typo candidates: single-word heads not in any list
H=[l.split('\t',1)[0] for l in open(S+'/unpacked/v24.tsv',encoding='utf-8')]
web={l.split('\t')[0] for l in open(S+'/ref/count_1w.txt')}
sysd={x.strip().lower() for x in open('/usr/share/dict/words')}
unk=[h for h in H if re.fullmatch(r'[a-z]{4,}',h) and h not in web and h not in sysd]
print('unknown single heads',len(unk)); print(' '.join(unk[::60]))
multi=[h for h in H if ' ' in h]
bad=[h for h in multi if any(re.fullmatch(r'[a-z]{4,}',t) and t not in web and t not in sysd for t in h.split())]
print('multiword with unknown token',len(bad)); print(' | '.join(bad[::150]))
