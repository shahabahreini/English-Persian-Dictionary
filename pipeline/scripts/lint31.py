"""Lint v3.1 subject files and say how each line will land in the build.
usage: python3 scripts/lint31.py new/v3.1/<file>.tsv [...]   (run from pipeline/, needs master.json of v3.0)
       add --show to list the NEW / ADDS / REDUNDANT status of every line
NEW / ADDS / REDUNDANT are measured against the master.json present the first time the script runs
(cached in work31/base.json). For writing v3.1 that was the v3.0 build; delete the cache to re-measure.
"""
import sys,re,os,json,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import DOM, split_items
here=os.path.dirname(os.path.abspath(__file__))
M=os.path.join(here,'..','work31','base.json')
if not os.path.exists(M):
    m=json.load(open(os.path.join(here,'..','master.json'),encoding='utf-8'))
    json.dump({e['head']:e['def'] for e in m},open(M,'w',encoding='utf-8'),ensure_ascii=False)
BASE=json.load(open(M,encoding='utf-8'))
norm=lambda x:re.sub(r'[\s\u200c\u0654\u064b-\u0652-]','',re.sub(r'\([^)]*\)|\[[^\]]*\]','',x)).replace('آ','ا').replace('أ','ا').replace('ة','ه').replace('ؤ','و')
CHECKS=[
 (r'[يكى٠-٩]','Arabic letter or digit (use ی ک and Persian digits)'),
 (r'(^|[\s(،؛])ن?می [؀-ۿ]','prefix می/نمی needs ZWNJ (می‌شود)'),
 (r'[آ-یپچژکگ] (ها|های|هایی|ای|اید|ترین)(?=$|[\s،؛).])','suffix needs ZWNJ (کتاب‌ها، خانه‌ای، بزرگ‌تر)'),
 (r'[,;]','ASCII , or ; in definition (use ، or ؛)'),
 (r'\s[،؛]|[،؛](?=[^\s])','spacing around ، ؛ (no space before, one after)'),
 (r'\t','TAB inside field'),
 (r'\s{2,}','double space'),
]
args=[a for a in sys.argv[1:] if not a.startswith('--')]; show='--show' in sys.argv
seen={}; err=0; tot=collections.Counter()
for f in args:
    c=collections.Counter()
    for i,l in enumerate(open(f,encoding='utf-8'),1):
        l=l.rstrip('\n'); where='%s:%d'%(os.path.basename(f),i)
        if not l.strip(): print(where,'blank line'); err+=1; continue
        p=l.split('\t')
        if len(p)!=3: print(where,'needs exactly 3 TAB-separated fields:',l[:80]); err+=1; continue
        h,dm,df=p
        if dm not in DOM: print(where,'unknown domain',repr(dm)); err+=1
        if h!=h.strip() or h!=h.lower() or not h or re.search(r'[.,;:!?]$',h) or re.search(r'[؀-ۿ]',h):
            print(where,'headword must be lowercase English, no trailing punctuation:',repr(h)); err+=1
        if not re.search(r'[؀-ۿ]',df): print(where,'definition has no Persian'); err+=1
        for rx,msg in CHECKS:
            if re.search(rx,df): print(where,msg,'|',h,'|',df[:90]); err+=1
        if re.match(r'[A-Za-z]',df) and '؛' not in df: print(where,'starts with Latin but no ؛ after the expansion |',h); err+=1
        k=(h,dm)
        if k in seen: print(where,'duplicate of',seen[k],'|',h,dm); err+=1
        seen[k]=where
        if h not in BASE: st='NEW'
        else:
            have={norm(x) for x in re.split(r'[،؛▪]',BASE[h])}
            items=split_items(df); keep=[x for x,_ in items if norm(x) and norm(x) not in have]
            st='ADDS' if keep and len(keep)*2>=len(items) else 'REDUNDANT'
        c[st]+=1
        if show: print(st,'\t',h,'\t',dm,'\t',df[:60], ('\t<- now: '+BASE[h][:80]) if h in BASE else '')
    tot+=c
    print('%s: %d lines  NEW %d  ADDS %d  REDUNDANT %d'%(os.path.basename(f),sum(c.values()),c['NEW'],c['ADDS'],c['REDUNDANT']))
print('TOTAL errors %d  NEW %d  ADDS %d  REDUNDANT %d'%(err,tot['NEW'],tot['ADDS'],tot['REDUNDANT']))
sys.exit(1 if err else 0)
