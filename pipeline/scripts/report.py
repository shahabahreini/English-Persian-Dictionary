import sys,re,os,json,collections,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build as B
S=sys.argv[1]
m=json.load(open(S+'/master.json',encoding='utf-8'))
st=json.load(open(S+'/stats_build.json'))
EN={'general':'General','computing':'Computing','electronics':'Electronics','engineering':'Engineering','medicine':'Medicine','biology':'Biology','chemistry':'Chemistry','physics':'Physics','math':'Mathematics','law':'Law','business':'Business & economics','military':'Military','aviation':'Aviation','maritime':'Maritime','architecture':'Architecture','civil':'Civil engineering','sports':'Sports','botany':'Botany','zoology':'Zoology','astronomy':'Astronomy','anatomy':'Anatomy','psychology':'Psychology','music':'Music','geography':'Geography','politics':'Politics','religion':'Religion','linguistics':'Linguistics','food':'Food & drink','slang':'Informal & slang','abbr':'Abbreviations','philosophy':'Philosophy & logic','earth':'Earth & environmental sciences','statistics':'Statistics','arts':'Arts (visual, film, theatre)','literature':'Literature','history':'History & archaeology','sociology':'Sociology & anthropology','education':'Education','agriculture':'Agriculture & veterinary','transport':'Transport & logistics','media':'Media & communication','fashion':'Fashion & textiles'}
# v2.4 section counts from raw tags
old=collections.Counter(); n24=0
for l in open(S+'/unpacked/v24.tsv',encoding='utf-8'):
    h,d=l.rstrip('\n').split('\t',1); n24+=1
    tags={B.OLDTAG[t.strip()] for t in re.findall(r'\[([^\]]*)\]',B.fanorm.basic(d)) if t.strip() in B.OLDTAG}
    tags|={B.PAREN[t.strip()] for t in re.findall(r'\(([^()]*)\)',B.fanorm.basic(d)) if t.strip() in B.PAREN and B.PAREN[t.strip()]!='general'}
    if not tags: old['general']+=1
    for t in tags: old[t]+=1
new=collections.Counter(); tot=collections.Counter(); upd=collections.Counter()
for e in m:
    ds=set(e['doms'])|set(e.get('inl',[]))
    if len(ds)>1: ds.discard('general')
    for d in ds:
        tot[d]+=1
        if e['status']=='new': new[d]+=1
        elif e['status'] in('improved','rewritten'): upd[d]+=1
rows=[]
for k in sorted(EN,key=lambda k:-tot[k]):
    rows.append({'k':k,'en':EN[k],'fa':B.DOM[k],'old':old[k],'tot':tot[k],'new':new[k],'upd':upd[k]})
sc=collections.Counter(e['status'] for e in m)
spell=sum(1 for e in m if e.get('was'))
DK=list(EN)
data=[]
def cut(s,n): return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+' …'
for e in m:
    s=e['status']
    if s=='new': c='n'
    elif s=='rewritten': c='r'
    elif s=='improved': c='i'
    elif e.get('was'): c='s'
    else: continue
    r=[e['head'],c,[DK.index(d) for d in e['doms']],cut(e['def'].replace(' ▪ ',' | '),150)]
    if c=='s': r.append(e['was'])
    elif e.get('before'): r.append(cut(e['before'].replace(' ▪ ',' | '),90))
    data.append(r)
D={e['head']:e for e in m}
def ex(h): 
    e=D.get(h); return (e.get('before') or '', e['def']) if e else ('','')
summary={'n24':n24,'n30':len(m),'new':sc['new'],'rew':sc['rewritten'],'imp':sc['improved'],'norm':sc['normalized'],'same':sc['unchanged'],'spell':spell,'dup':st.get('merged_dup',0),'alts':st.get('alts',0),'senses':st.get('sense_added',0),'v31new':st.get('v31_new_entry',0),'v31senses':st.get('v31_sense_added',0)}
json.dump({'summary':summary,'rows':rows},open(S+'/report/summary.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
raw={}
nrev=0; ndig=0
for l in open(S+'/unpacked/v24.tsv',encoding='utf-8'):
    h,d=l.rstrip('\n').split('\t',1); raw.setdefault(h,d)
    if len(d.split())>1: nrev+=1
    if '¹' in d: ndig+=1
def stored(h): return ' '.join(reversed(raw[h].split()))
def cur(h,n=170): return cut(D[h]['def'].replace(' ▪ ',' | '),n) if h in D else '(missing)'
sp=next((e for e in m if e.get('was')=='illustrous'),None) or next(e for e in m if e.get('was') and ' ' not in e['head'])
EX=[
 {'t':'Persian word order restored','n':nrev,'u':'definitions','p':'v2.4 stores every definition with its words in reverse, a workaround for Kindle pop-ups that place words left to right. Since v3.0 the text is kept in natural reading order and reversed only in the build made for those Kindles.','b':stored('a clean shave'),'a':cur('a clean shave'),'fa':1},
 {'t':'Persian spelling brought up to standard','n':summary['norm'],'u':'entries','p':'Arabic ى and ك replaced with Persian ی and ک, missing آ restored from a 445,000-word Persian frequency list, half-spaces added (می‌کند، خانه‌ای، بی‌سیم), tanvin and ezafe marks written properly, comma spacing fixed.','b':raw['halcyon'],'a':cur('halcyon'),'fa':1},
 {'t':'Corrupted numbers repaired','n':ndig,'u':'definitions','p':'A conversion fault had turned trailing zeros into a superscript ¹ in front of the number, so 600 read as ¹¹6.','b':raw['ball (basketball)'],'a':cur('ball (basketball)'),'fa':1},
 {'t':'Misspelled headwords corrected','n':summary['spell'],'u':'headwords','p':'6,600 headwords containing a word found in no English word list were checked against their Persian definition. Confirmed typos were corrected, and where the correct spelling already existed the two entries were merged.','b':sp['was'],'a':sp['head'],'fa':0},
 {'t':'Broken characters in headwords','n':st.get('head_cleaned',0),'u':'headwords','p':'An encoding fault had replaced apostrophes and commas with Š, and a few headwords carried stray Persian text, so they could never be matched by a look-up.','b':'to hug oneŠs chains','a':"to hug one's chains",'fa':0},
 {'t':'Duplicate entries merged','n':summary['dup'],'u':'entries','p':'Headwords that appeared twice, or became identical once a typo was fixed, are merged into one entry that keeps every distinct equivalent.','b':raw['abstract'][:60]+' … (and a second entry)','a':cur('abstract',120),'fa':1},
 {'t':'Empty cross-references filled in','n':st.get('xref_resolved',0),'u':'entries','p':'Entries that contained nothing but a pointer to another headword now carry that headword\'s definition as well.','b':raw['administrate'],'a':cur('administrate',110),'fa':1},
 {'t':'Core vocabulary rewritten','n':summary['rew'],'u':'entries','p':'The 7,000 most frequently looked-up words were rewritten one by one: commonest meaning first, grouped by part of speech, wrong or truncated equivalents removed, missing everyday and modern senses added.','b':cut(D['that'].get('before') or raw['that'],110),'a':cur('that',170),'fa':1},
 {'t':'New entries','n':summary['new'],'u':'entries','p':'v2.4 stops in the early 1990s. For v3.0, 20,658 frequent English words missing from it were screened, and four subject glossaries were written for technology, science and medicine, business and society, and everyday English with idioms and phrasal verbs. v3.1 added 21 subject glossaries (see below).','b':'internet — not in v2.4','a':cur('internet'),'fa':1},
 {'t':'Modern senses added to old words','n':summary['senses'],'u':'entries','p':'Existing words that gained a new meaning now open with it, ahead of the senses v2.4 already had.','b':cut(D['cookie'].get('before') or raw.get('cookie',''),90) if 'cookie' in D else '','a':cur('cookie',150),'fa':1},
 {'t':'Subject glossaries (v3.1)','n':summary['v31new'],'u':'entries','p':'v3.1 adds twelve new sections (philosophy and logic, earth and environmental sciences, statistics, arts, literature, history and archaeology, sociology and anthropology, education, agriculture and veterinary science, transport and logistics, media, fashion and textiles) and deepens mathematics, physics, astronomy, psychology, linguistics, music, architecture, sports, slang and everyday idioms. Each glossary was written and then reviewed line by line by a second pass. On an existing word the subject sense is added after the current definition, never ahead of it: '+'{:,}'.format(summary['v31senses'])+' senses were added this way.','b':cut(D['chiaroscuro'].get('before') or '',100),'a':cur('chiaroscuro',170),'fa':1},
 {'t':'Inflected forms found by look-up','n':summary['alts'],'u':'forms','p':'Attested plurals, past tenses and -ing forms now lead to their base entry, as do bracketed headwords such as theurgic(al) and infinitives listed under "to …".','b':'walked — not found','a':'walked → walk: '+cur('walk',70),'fa':0},
]
static=json.load(open(S+'/report/static.json',encoding='utf-8'))
tpl=open(S+'/report/template.html',encoding='utf-8').read()
page=tpl.replace('/*DATA*/','const SUM=%s;const ROWS=%s;const DOMS=%s;const UPD=%s;'%(json.dumps(summary),json.dumps(rows,ensure_ascii=False),json.dumps([[EN[k],B.DOM[k]] for k in DK],ensure_ascii=False),json.dumps(data,ensure_ascii=False,separators=(',',':')))+'const EX=%s;const COMPAT=%s;const COMPATNOTE=%s;const LIMITS=%s;'%tuple(json.dumps(x,ensure_ascii=False) for x in (EX,static['compat'],static['note'],static['limits'])))
open(S+'/report/dictionary-v3-report.html','w',encoding='utf-8').write(page)
print(summary, 'page bytes',len(page.encode()), 'browse rows',len(data))
for h in ['that','tension','mouse','cloud','administrate','set']: print(h, ex(h))
