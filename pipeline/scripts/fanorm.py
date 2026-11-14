# Persian normalisation for the dictionary (pure functions + lexicon-driven maps)
import re, collections, os
REF=os.environ.get('DICT_REF')
ZW='‌'
FA=r'ء-غف-يپچژکگیًٔ'
def basic(s):
    return s.replace('ى','ی').replace('ي','ی').replace('ك','ک')
_lex=None
def lex():
    global _lex
    if _lex is None:
        _lex=collections.Counter()
        for l in open(os.path.join(REF,'fa_full.txt'),encoding='utf-8'):
            p=l.split()
            if len(p)==2: _lex[basic(p[0])]+=int(p[1])
    return _lex
AMAD_BLACK={'اشغالی','ابش','ابه','ادام','اهان','اریل','اوره','ارتو','ازاره','ایید','اره','افت','اشغال','امین','ازان','اها','ارا','ایه','اخته','ارس','اریس','ارجی','ارمش','اکاد','ازی','ابل','ادمن','اروزی','اسای','الاینده','اباد','اذر','ارش','اریا','ارمان','اوا','ایت','اسی','الا','اهی','اخه','اخی','ادا','اکی','اسه','الو','انا','اسیه','اتی','اشی','ارت','اری','انی','ابا','اقای','امل','امر','اثر','اجل','اخذ','ادب','ارک','ارن','ازر','اسر','اشک','امد','اش','ام','ای','المان','اجر','ات','ار','اری','اسم','ان‌ها','اب‌ها','این','اید','ایم','اند','است','اسمان‌ها','اهل','ال','اخ','اقا'}
_amap=None
def amap():
    global _amap
    if _amap is None:
        L=lex(); _amap={}
        for w,f in L.items():
            if 'آ' in w and f>=40 and ZW not in w and not w.endswith('آ'):
                k=w.replace('آ','ا')
                if k in AMAD_BLACK or len(k)<2: continue
                if f>=5*L.get(k,0):
                    if k not in _amap or L[_amap[k]]<f: _amap[k]=w
        _amap.update({'ان':'آن','اب':'آب','اقا':'آقا','انها':'آنها','انکه':'آنکه','انچه':'آنچه','انجا':'آنجا','اید':'آید','ایند':'آیند','امدن':'آمدن','اوردن':'آوردن','امیختن':'آمیختن','اموختن':'آموختن','ازمودن':'آزمودن','اشامیدن':'آشامیدن','اراستن':'آراستن','افریدن':'آفریدن','الودن':'آلودن','اسودن':'آسودن','اغشتن':'آغشتن','امیز':'آمیز','اور':'آور','اسا':'آسا','الود':'آلود','الت':'آلت','الات':'آلات','اهن':'آهن','اینده':'آینده','ایین':'آیین','ائین':'آیین','ازمایى':'آزمایی','اگاه':'آگاه','اماده':'آماده','اسان':'آسان','ارام':'آرام','ازاد':'آزاد','اشکار':'آشکار','اغاز':'آغاز','اخر':'آخر','امار':'آمار','اثار':'آثار','اداب':'آداب','اتش':'آتش','اسیب':'آسیب','اموزش':'آموزش','ازمایش':'آزمایش','ارایش':'آرایش','اواز':'آواز','اهنگ':'آهنگ','ارزو':'آرزو','اشنا':'آشنا','اسمان':'آسمان','افتاب':'آفتاب','ادم':'آدم','امد':'آمد','اخته':'اخته','اهسته':'آهسته','ابى':'آبی','ابی':'آبی','اهو':'آهو','اینه':'آینه','ایه':'آیه','امریکا':'آمریکا','امریکایی':'آمریکایی','اسیا':'آسیا','افریقا':'آفریقا','المانی':'آلمانی','اید':'آید'})
        for k in list(_amap):
            if k in ('اید',): del _amap[k]
    return _amap
SUFF=['های','ها','هایی','ی','یی','ای','ها','ان','تر','ترین','اً']
def fix_alef_tok(core):
    A=amap()
    if core in A: return A[core]
    if 'ا' not in core or 'آ' in core: return core
    # prefix/suffix tolerant: known stem + simple suffix
    for suf in ('هایی','های','ها','ترین','تر','ی'):
        if core.endswith(suf) and len(core)-len(suf)>=3:
            st=core[:-len(suf)]
            if st in A and st not in ('ان','اب','اور','اسا','الت','انجا','امیز','الود') and (suf!='ی' or len(st)>=4):
                return A[st]+suf
    return core
MIA={'اید':'آید','ایند':'آیند','امد':'آمد','امدند':'آمدند','اورد':'آورد','اورند':'آورند','اموزد':'آموزد','اید':'آید','اورد':'آورد','ازماید':'آزماید','اشامد':'آشامد','اشامند':'آشامند','امیزد':'آمیزد','افریند':'آفریند','الاید':'آلاید','اراید':'آراید','اغازد':'آغازد'}
VERB_END=('د','ند','م','یم','ید','ی','ست')
def zwnj(tokens):
    L=lex(); out=[]
    STOP={'هیچ','آن','این','هر','چون','که','و','یا','از','در','به','با','تو','من','او','ما','شما'}
    for t in tokens:
        prev=out[-1] if out else ''
        core=re.fullmatch(r'([%s]+)([،)]?)'%FA,t)
        if re.fullmatch(r'\(?(می|نمی)',prev) and core and len(core.group(1))>1 and core.group(1).endswith(VERB_END) and L.get(core.group(1),0)>0:
            out[-1]=prev+ZW+MIA.get(core.group(1),core.group(1))+core.group(2); continue
        if re.fullmatch(r'(ها|های|هایی|هایش|هایشان)[،)]?',t) and re.search(r'[%s]$'%FA,prev) and prev not in ('و','یا'):
            out[-1]=prev+ZW+t; continue
        if re.fullmatch(r'(ای|ایی)[،)]?',t) and prev.endswith('ه') and len(prev)>2:
            out[-1]=prev+ZW+t.replace('ایی','ای'); continue
        if re.fullmatch(r'اند[،)]?',t) and prev.endswith('ه') and len(prev)>2:
            out[-1]=prev+ZW+t; continue
        if re.fullmatch(r'ترین[،)]?',t) and re.search(r'[%s]$'%FA,prev) and prev not in ('و','یا'):
            out[-1]=prev+ZW+t; continue
        if re.fullmatch(r'\(?بی',prev) and core and len(core.group(1))>1 and core.group(1) not in STOP and core.group(1) not in ('متال','پلار','اچ','سی','تی','بی','ام','اس'):
            out[-1]=prev+ZW+t; continue
        mm=re.fullmatch(r'(می|نمی)([%s]{2,})([،)]?)'%FA,t)
        if mm and (mm.group(2).endswith('د') or mm.group(2) in ('توان','شویم','کنیم','کنم','شوم')) and L.get(mm.group(2),0)>=20:
            out.append(mm.group(1)+ZW+MIA.get(mm.group(2),mm.group(2))+mm.group(3)); continue
        out.append(t)
    return out
def fix_digits(s):
    def rep(m):
        z=len(m.group(1)); body=m.group(2).rstrip()
        body=re.sub(r'\s*/\s*','/',body)
        return body+'0'*z+(' ' if m.group(2).endswith(' ') else '')
    return re.sub(r'(¹+)((?:\d|¹)*(?: ?/ ?\d+)? ?)',rep,s) if '¹' in s else s
def fix_quotes(s):
    if '"' not in s or re.search(r'\d"',s): return s
    s=re.sub(r'([%s]{2,})ا " ?(?=[%s])'%(FA,FA),r'\1اً ',s)
    s=re.sub(r'([%s]+)" ([%s]+)"'%(FA,FA),r'\1 «\2»',s)      # X" Y"  -> X «Y»
    s=re.sub(r'"([%s]+) ([%s]+)"'%(FA,FA),r'«\1 \2»',s)
    def tan(m): return m.group(1)+'اً'
    if s.count('"')%2==1 or re.search(r'[%s]ا" ?(،|$|\))'%FA,s):
        s=re.sub(r'([%s]{2,})ا ?"(?=[%s])'%(FA,FA),lambda m:m.group(1)+'اً ',s)
        s=re.sub(r'([%s]{2,})ا"(?=\s|،|$|\))'%FA,tan,s)
    s=re.sub(r'"\s*([^"]*?)\s*"',r'«\1»',s)
    return s
def normalize(d):
    s=basic(d)
    s=fix_digits(s)
    s=fix_quotes(s)
    s=re.sub(r'شیی ء','شیء',s)
    s=re.sub(r'ه ?ء ?(?=[%s(])'%FA,'هٔ ',s)
    s=re.sub(r'ه ء(?=\s|،|$|\))','هٔ',s)
    s=re.sub(r'\s+',' ',s).strip()
    toks=s.split(' ')
    nt=[]
    for t in toks:
        m=re.fullmatch(r'([^%s]*)([%s]+)([^%s]*)'%(FA,FA,FA),t)
        if m: t=m.group(1)+fix_alef_tok(m.group(2))+m.group(3)
        nt.append(t)
    nt=zwnj(nt)
    s=' '.join(nt)
    s=re.sub(r'\s+،','،',s); s=re.sub(r'،(?=\S)','، ',s)
    s=re.sub(r'\(\s+','(',s); s=re.sub(r'\s+\)',')',s)
    s=re.sub(r'(?<=[%s])\((?=[%s])'%(FA,FA),' (',s); s=re.sub(r'\)(?=[%s])'%FA,') ',s)
    if ')' in s and '(' in s and s.find(')')<s.find('('):
        s=re.sub(r'\)\s*([A-Za-z][A-Za-z .\'-]*?)\s*\(',r'(\1) ',s,count=1)
    s=re.sub(r'^\(([a-z][a-z ,\'-]*)\)،?\s*',r'(= \1) ',s)
    s=re.sub(r'(،\s*){2,}','، ',s).strip(' ،')
    return s
