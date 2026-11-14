import sys,json,re
S=sys.argv[1]
m=json.load(open(S+'/master.json',encoding='utf-8'))
web={};sub={}
for i,l in enumerate(open(S+'/ref/count_1w.txt')): web[l.split('\t')[0]]=i
for i,l in enumerate(open(S+'/ref/en_50k.txt',encoding='utf-8')): sub[l.split()[0]]=i
sel=[]
for e in m:
    h=e['head']
    if e['status']=='new' or not re.fullmatch(r'[a-z]{2,}',h): continue
    r=min(web.get(h,10**9), sub.get(h,10**9)*1.3)
    if r<9000: sel.append((r,h,e['def']))
sel.sort()
print(len(sel))
N=7
for i in range(N):
    open(S+'/review/rev_%d.tsv'%i,'w',encoding='utf-8').write('\n'.join('%s\t%s'%(h,d) for r,h,d in sel[i::N])+'\n')
print(sel[10][1:],sel[3000][1:],sel[-1][1:])
