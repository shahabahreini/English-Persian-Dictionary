# Build the v3.0 master data from v2.4 + reviewed additions.
import sys,re,os,json,glob,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import fanorm
S=sys.argv[1]
DOM={'general':'عمومی','computing':'رایانه','electronics':'الکترونیک','engineering':'مهندسی','medicine':'پزشکی','biology':'زیست‌شناسی','chemistry':'شیمی','physics':'فیزیک','math':'ریاضی','law':'حقوق','business':'بازرگانی و اقتصاد','military':'نظامی','aviation':'هوانوردی','maritime':'دریانوردی','architecture':'معماری','civil':'عمران','sports':'ورزش','botany':'گیاه‌شناسی','zoology':'جانورشناسی','astronomy':'نجوم','anatomy':'کالبدشناسی','psychology':'روان‌شناسی','music':'موسیقی','geography':'جغرافیا','politics':'سیاست','religion':'دین','linguistics':'زبان‌شناسی','food':'خوراک','slang':'عامیانه','abbr':'کوته‌نوشت',
     # v3.1 sections
     'philosophy':'فلسفه و منطق','earth':'علوم زمین و محیط زیست','statistics':'آمار','arts':'هنر','literature':'ادبیات','history':'تاریخ و باستان‌شناسی','sociology':'جامعه‌شناسی و مردم‌شناسی','education':'آموزش','agriculture':'کشاورزی و دامپزشکی','transport':'حمل‌ونقل','media':'رسانه و ارتباطات','fashion':'پوشاک و نساجی'}
OLDTAG={'علوم مهندسی':'engineering','کامپیوتر':'computing','ورزش':'sports','قانون ـ فقه':'law','شیمی':'chemistry','بازرگانی':'business','الکترونیک':'electronics','علوم نظامی':'military','معماری':'architecture','علوم هوایی':'aviation','عمران':'civil','گیاه شناسی':'botany','علوم دریایی':'maritime','جانور شناسی':'zoology','زیست شناسی':'biology','نجوم':'astronomy','کالبد شکافی':'anatomy'}
PAREN={'پزشکی':'medicine','جراحی':'medicine','طب':'medicine','شیمی':'chemistry','موسیقی':'music','حقوق':'law','علوم نظامی':'military','زیست شناسی':'biology','نجوم':'astronomy','ریاضی':'math','هندسه':'math','در ریاضیات':'math','فیزیک':'physics','روان شناسی':'psychology','برق':'electronics','مکانیک':'engineering','معماری':'architecture','دستور زبان':'linguistics','زبان عامیانه':'slang','گیاه شناسی':'botany','جانور شناسی':'zoology','جغرافی':'geography','در کالبدشناسی':'anatomy','منطق':'general'}
PAREN_RW={'زیست شناسی':'زیست‌شناسی','روان شناسی':'روان‌شناسی','گیاه شناسی':'گیاه‌شناسی','جانور شناسی':'جانورشناسی','زبان عامیانه':'عامیانه','جغرافی':'جغرافیا','در کالبدشناسی':'کالبدشناسی','درامار':'آمار','در آمار':'آمار','در امار':'آمار','مج':'مجازی','درجمع':'در جمع','افسانه ء یونان':'افسانهٔ یونان','افسانهٔ یونان':'افسانهٔ یونان','ز.ع -.امر.':'عامیانهٔ آمریکایی','گ.ش -.ج.ش.':'گیاه‌شناسی، جانورشناسی','ج.ش -.گ.ش.':'جانورشناسی، گیاه‌شناسی','انگلیس':'بریتانیایی','امریکایی':'آمریکایی'}
def clean_head(h):
    o=h
    h=re.sub(r'[؀-ۿ]+','',h)
    h=re.sub(r"Šs\b","'s",h); h=re.sub(r'\s*Š\s*',', ',h)
    h=re.sub(r'\s+',' ',h).strip(' ,')
    h=re.sub(r'\s+([?!,;:])',r'\1',h)
    return h
def fix_xref(s):
    s=re.sub(r'\(\s*=\s*([^()=]+?)\s*\)',r'(= \1)',s)
    s=re.sub(r'\(([^()=]+?)\s*=\s*\)',r'(= \1)',s)
    return s
def fix_pos(t):
    t=t.replace('.& ','./').strip()
    parts=[p.strip('. ') for p in re.split(r'/',t) if p.strip('. ')]
    return '/'.join(p+'.' for p in parts)
def parse_def(d):
    """returns list of segments (kind,label,text); kind in dom,pos,None"""
    s=fanorm.normalize(d)
    s=fix_xref(s)
    def prw(m):
        k=m.group(1).strip()
        return '('+PAREN_RW.get(k,k)+')'
    doms=set(); inl=set()
    for k in re.findall(r'\(([^()]*)\)',s):
        if k.strip() in PAREN: inl.add(PAREN[k.strip()])
    s=re.sub(r'\(([^()]*)\)',prw,s)
    segs=[]; pos=0
    for m in re.finditer(r'(?:ـ\s*)?\[([^\]]*)\]\s*:?\s*',s):
        pre=s[pos:m.start()].strip(' ،ـ')
        if pre or not segs:
            if segs: segs[-1][2]=pre
            elif pre: segs.append([None,None,pre])
        lab=m.group(1).strip()
        if lab in OLDTAG: segs.append(['dom',OLDTAG[lab],'']); doms.add(OLDTAG[lab])
        elif re.fullmatch(r"[.a-z/&\s]+",lab): segs.append(['pos',fix_pos(lab),''])
        else: segs.append(['raw',lab,''])
        pos=m.end()
    tail=s[pos:].strip(' ،ـ')
    if segs and pos>0: segs[-1][2]=tail
    else: segs.append([None,None,tail])
    segs=[x for x in segs if x[2] or x[0]]
    return segs,doms,inl
def render(segs):
    out=[]
    for k,l,t in segs:
        if k=='dom': out.append('[%s] %s'%(DOM[l],t))
        elif k=='pos': out.append('[%s] %s'%(l,t))
        elif k=='raw': out.append('[%s] %s'%(l,t))
        else: out.append(t)
    return ' ▪ '.join(x.strip() for x in out if x.strip())
def dedup_senses(t):
    parts=[p.strip() for p in t.split('،')]
    seen=set(); o=[]
    for p in parts:
        k=p.replace('‌','').replace(' ','')
        if p and k not in seen: seen.add(k); o.append(p)
    return '، '.join(o)
def split_items(t):
    """split a definition into (item, separator) pairs on ، and ؛ outside parentheses"""
    out=[]; buf=''; depth=0
    for ch in t:
        if ch=='(': depth+=1
        elif ch==')': depth=max(0,depth-1)
        if depth==0 and ch in '،؛':
            out.append((buf.strip(),ch)); buf=''
        else: buf+=ch
    out.append((buf.strip(),''))
    return [(x,sp) for x,sp in out if x]
def main():
    rows=[l.rstrip('\n').split('\t',1) for l in open(S+'/unpacked/v24.tsv',encoding='utf-8')]
    typo={}
    for f in glob.glob(S+'/typo/fix_*.tsv'):
        for l in open(f,encoding='utf-8'):
            p=l.rstrip('\n').split('\t')
            if len(p)==2 and p[0] and p[1] and p[0]!=p[1]: typo[p[0]]=p[1].strip().lower()
    E=collections.OrderedDict(); log=[]; st=collections.Counter()
    for h0,d0 in rows:
        h=clean_head(h0); fixed_from=None
        if not h: st['dropped_empty']+=1; log.append(('removed',h0,d0,'','empty or non-English headword')); continue
        if h!=h0: st['head_cleaned']+=1; log.append(('headword-cleaned',h0,'',h,'mojibake/spacing'))
        if h0 in typo or h in typo:
            nh=typo.get(h0) or typo.get(h); st['head_typo']+=1; log.append(('headword-spelling',h,'',nh,'')); fixed_from=h; h=nh
        segs,doms,inl=parse_def(d0)
        for s_ in segs: s_[2]=dedup_senses(s_[2]) if '(' not in s_[2] else s_[2]
        k=h.lower()
        if k in E:
            e=E[k]; old=render(e['segs'])
            have={x.replace('‌','').replace(' ','') for sg in e['segs'] for x in sg[2].split('،')}
            for sg in segs:
                keep=[x.strip() for x in sg[2].split('،') if x.replace('‌','').replace(' ','') not in have] if '(' not in sg[2] else [sg[2]]
                if keep and keep!=['']:
                    e['segs'].append([sg[0],sg[1],'، '.join(keep)])
            e['doms']|=doms; e['inl']|=inl; e['v24'].append(d0); st['merged_dup']+=1; log.append(('merged-duplicate',h,d0,'',''))
        else:
            E[k]={'head':h,'segs':segs,'doms':doms,'v24':[d0],'status':'v2.4','alts':set(),'inl':inl,'was':fixed_from}
    # cross-ref-only entries: pull target definition
    for k,e in E.items():
        txt=render(e['segs'])
        m=re.fullmatch(r'\(= ?([a-z .,\'-]+)\)',txt)
        if m:
            tg=[t.strip() for t in re.split(r',| - ',m.group(1)) if t.strip()]
            tg=[t for t in tg if t in E and t!=k and not re.fullmatch(r'\(=.*\)',render(E[t]['segs']))]
            if tg:
                t=E[tg[0]]
                e['segs']=[[None,None,'(= %s)'%tg[0]]]+[list(x) for x in t['segs']]
                e['doms']|=t['doms']; e['status']='improved'; st['xref_resolved']+=1
                log.append(('cross-reference-resolved',e['head'],txt,render(e['segs']),''))
    # expert rewrites of core entries
    for f in sorted(glob.glob(S+'/review/merged/out_*.tsv')):
        for l in open(f,encoding='utf-8'):
            p=l.rstrip('\n').split('\t')
            if len(p)!=2: st['rewrite_badline']+=1; continue
            h,df=p[0].strip().lower(),' '.join(fanorm.basic(p[1]).split())
            if h not in E or len(df)<2 or not re.search(r'[\u0600-\u06ff]',df): st['rewrite_badline']+=1; continue
            e=E[h]; old=render(e['segs'])
            if df==old: continue
            e['before']=old; e['segs']=[[None,None,df]]; e['status']='rewritten'; st['rewritten']+=1
            log.append(('definition-rewritten',e['head'],old,df,''))
    # additions
    add=[]
    for f in sorted(glob.glob(S+'/new/*.tsv')):
        src=os.path.basename(f)
        for l in open(f,encoding='utf-8'):
            p=l.rstrip('\n').split('\t')
            if len(p)!=3: st['add_badline']+=1; continue
            h,dm,df=p[0].strip().lower(),p[1].strip(),fanorm.basic(p[2].strip())
            if dm not in DOM or not h or not re.search(r'[؀-ۿ]',df): st['add_badline']+=1; continue
            add.append((h,dm,df,src))
    for h,dm,df,src in add:
        theme=src.startswith('theme')
        if h in E:
            e=E[h]
            if e['status']=='new':
                norm=lambda x:re.sub(r'\([^)]*\)|[\s\u200c\u0654]','',x)
                have={norm(x) for sg in e['segs'] for x in re.split(r'[،؛]',sg[2])}
                keep=[x.strip() for x in re.split(r'[،؛]',df) if norm(x) and norm(x) not in have]
                e['doms'].add(dm)
                if not keep or len(keep)*2<=len([x for x in re.split(r'[،؛]',df) if x.strip()]): continue
                e['segs'].append(['dom' if dm!='general' else None, dm if dm!='general' else None, '، '.join(keep)]); continue
            if not theme: st['gap_already_present']+=1; continue
            old=render(e['segs'])
            first=re.split(r'[،؛(]',re.sub(r'^\([^)]*\)\s*','',df))[0].strip()
            if e['status']=='rewritten':
                e['doms'].add(dm)
                if first and first in old: continue
                e['segs'].append(['dom' if dm!='general' else None, dm if dm!='general' else None, df]); st['sense_added']+=1
                log.append(('modern-sense-added',e['head'],old,df,dm)); continue
            if first and first.replace('\u200c','').replace(' ','') in old.replace('\u200c','').replace(' ',''):
                e['doms'].add(dm)
                if len(old)<30 and e['status']!='improved':
                    e.setdefault('before',old); e['segs']=[[None,None,df]]; e['status']='improved'; st['short_replaced']+=1
                    log.append(('definition-replaced',e['head'],old,df,dm))
                continue
            e.setdefault('before',old)
            e['segs'].insert(0,['dom' if dm!='general' else None, dm if dm!='general' else None, df])
            e['doms'].add(dm); e['status']='improved'; e['newsense']=True; st['sense_added']+=1
            log.append(('modern-sense-added',e['head'],old,df,dm))
        else:
            E[h]={'head':h,'segs':[['dom' if dm!='general' else None, dm if dm!='general' else None, df]],'doms':{dm},'v24':[],'status':'new','alts':set(),'inl':set(),'was':None}
            st['new_entry']+=1; log.append(('new-entry',h,'',df,dm))
    # v3.1 subject expansion: runs after the v3.0 inputs so their results are unchanged.
    # A new headword becomes a new entry; on an existing headword the subject sense is
    # appended (never prepended), keeping only the equivalents the entry does not have yet.
    norm=lambda x:re.sub(r'[\s\u200c\u0654\u064b-\u0652-]','',re.sub(r'\([^)]*\)|\[[^\]]*\]','',x)).replace('آ','ا').replace('أ','ا').replace('ة','ه').replace('ؤ','و')
    for f in sorted(glob.glob(S+'/new/v3.1/*.tsv')):
        for l in open(f,encoding='utf-8'):
            p=l.rstrip('\n').split('\t')
            if len(p)!=3: st['v31_badline']+=1; continue
            h,dm,df=p[0].strip().lower(),p[1].strip(),' '.join(fanorm.basic(p[2].strip()).split())
            if dm not in DOM or not h or not re.search(r'[؀-ۿ]',df): st['v31_badline']+=1; continue
            lab=['dom' if dm!='general' else None, dm if dm!='general' else None]
            if h not in E:
                E[h]={'head':h,'segs':[lab+[df]],'doms':{dm},'v24':[],'status':'new','alts':set(),'inl':set(),'was':None}
                st['v31_new_entry']+=1; log.append(('new-entry',h,'',df,dm)); continue
            e=E[h]
            if not e['doms']: e['doms']={'general'}  # what the end of the build would have given it
            e['doms'].add(dm)
            have={norm(x) for sg in e['segs'] for x in re.split(r'[،؛]',sg[2])}
            items=split_items(df)
            keep=[(x,sp) for x,sp in items if norm(x) and norm(x) not in have]
            if not keep or len(keep)*2<len(items): st['v31_already_present']+=1; continue
            txt=''.join(x+(sp+' ' if sp else '') for x,sp in keep).strip(' ،؛')
            if e['status']!='new': e.setdefault('before',render(e['segs']))
            old=render(e['segs'])
            e['segs'].append(lab+[txt])
            if e['status'] in ('v2.4',): e['status']='improved'
            st['v31_sense_added']+=1; log.append(('subject-sense-added',e['head'],old,txt,dm))
    # alternate lookup forms
    web={}
    for i,l in enumerate(open(S+'/ref/count_1w.txt')): web[l.split('\t')[0]]=i
    for k,e in E.items():
        h=e['head']
        m=re.fullmatch(r"([a-z'-]+)\(([a-z]+)\)",h)
        if m: e['alts']|={m.group(1),m.group(1)+m.group(2)}
        m=re.fullmatch(r"([a-z' -]+?)\s*\(([^)]*)\)",h)
        if m and ' ' in h and m.group(1).strip() not in E: e['alts'].add(m.group(1).strip())
        if h.startswith('to ') and len(h)>5: e['alts'].add(h[3:])
        if re.fullmatch(r'[a-z]{3,}',h):
            c=set()
            c|={h+'s',h+'es',h+'ed',h+'ing',h+'d',h+'ly',h+'er',h+'est'}
            if h.endswith('e'): c|={h[:-1]+'ing',h+'r',h+'st'}
            if h.endswith('y'): c|={h[:-1]+'ies',h[:-1]+'ied',h[:-1]+'ier',h[:-1]+'iest',h[:-1]+'ily'}
            if re.search(r'[^aeiou][aeiou][^aeiouwxy]$',h): c|={h+h[-1]+'ed',h+h[-1]+'ing',h+h[-1]+'er',h+h[-1]+'est'}
            e['alts']|={x for x in c if web.get(x,10**9)<200000}
        e['alts']={a for a in e['alts'] if a and a not in E and a!=k}
    # an alt form claimed by several entries is fine; count
    for k,e in E.items():
        e['def']=render(e['segs'])
        if not e['doms']: e['doms']={'general'}
        if e['status']=='v2.4':
            base=' '.join(fanorm.basic(e['v24'][0]).split())
            e['status']='unchanged' if e['def']==base else 'normalized'
    out=[{'head':e['head'],'def':e['def'],'doms':sorted(e['doms']),'inl':sorted(e['inl']-e['doms']),'status':e['status'],'was':e.get('was'),'before':e.get('before'),'alts':sorted(e['alts']),'v24':e['v24'],'segs':e['segs']} for e in E.values()]
    out.sort(key=lambda e:(re.sub(r'[^a-z0-9]','',e['head'].lower()),e['head']))
    json.dump(out,open(S+'/master.json','w',encoding='utf-8'),ensure_ascii=False)
    with open(S+'/changelog.tsv','w',encoding='utf-8') as f:
        f.write('change\theadword\tv2.4\t%s\tnote\n'%os.environ.get('DICT_VER','v3.0'))
        for r in log: f.write('\t'.join(x.replace('\t',' ') for x in r)+'\n')
    st['total']=len(out); st['alts']=sum(len(e['alts']) for e in out)
    st.update({'status_'+k:v for k,v in collections.Counter(e['status'] for e in out).items()})
    json.dump(st,open(S+'/stats_build.json','w'),indent=1)
    print(json.dumps(st,indent=1))
if __name__=='__main__': main()
