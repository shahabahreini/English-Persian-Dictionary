import sys,re,glob,os,collections
S=sys.argv[1]
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8'):
        l=l.rstrip('\n')
        if not l.strip(): continue
        m=re.match(r'^(.+?)\s*(?:\t|@@|¦|\|)\s*(.+)$',l)
        if m: out.append((m.group(1).strip().lower(),m.group(2).strip()))
    return out
rev={i:[l.split('\t',1)[0] for l in open(S+'/review/rev_%d.tsv'%i,encoding='utf-8')] for i in range(7)}
owner={h:i for i,hs in rev.items() for h in hs}
got=collections.defaultdict(dict)
files=glob.glob(S+'/review/out_*.tsv')+glob.glob(S+'/review/_w5/*')+glob.glob(S+'/review/parts4/*')+glob.glob(S+'/review/parts6/*')+glob.glob(S+'/out2_parts/*')+[S+'/chunk.txt']+glob.glob(S+'/review/out2_*.tsv')
for f in files:
    rows=parse(f); own=collections.Counter(owner.get(h) for h,_ in rows)
    for h,d in rows:
        if h in owner and re.search(r'[؀-ۿ]',d): got[owner[h]].setdefault(h,d)
    print(os.path.relpath(f,S),len(rows),dict(own))
os.makedirs(S+'/review/merged',exist_ok=True); os.makedirs(S+'/review/todo',exist_ok=True)
tot=0
for i in range(7):
    with open(S+'/review/merged/out_%d.tsv'%i,'w',encoding='utf-8') as f:
        for h in rev[i]:
            if h in got[i]: f.write(h+'\t'+got[i][h]+'\n')
    todo=[l for l in open(S+'/review/rev_%d.tsv'%i,encoding='utf-8') if l.split('\t',1)[0] not in got[i]]
    open(S+'/review/todo/rev_%d.tsv'%i,'w',encoding='utf-8').writelines(todo)
    tot+=len(got[i]); print('slice',i,'done',len(got[i]),'todo',len(todo))
print('rewrites salvaged',tot)
# everyday
n=0
with open(S+'/new/theme_everyday.tsv','w',encoding='utf-8') as f:
    for p in sorted(glob.glob(S+'/tmp_everyday/*.txt'))+sorted(glob.glob(S+'/tmp_everyday2/*.txt')):
        dom=os.path.basename(p).rsplit('_',1)[1][:-4]
        for h,d in parse(p):
            if re.search(r'[؀-ۿ]',d) and '\t' not in d: f.write('%s\t%s\t%s\n'%(h,dom,d)); n+=1
print('everyday salvaged',n)
