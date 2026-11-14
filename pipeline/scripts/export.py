# Export master.json to every target format's source.
import sys,re,os,json,html
S,OUT,VER=sys.argv[1],sys.argv[2],sys.argv[3]
m=json.load(open(S+'/master.json',encoding='utf-8'))
TITLE='English-Persian Dictionary v%s'%VER
LAT=re.compile(r"^[\(\[«\"']*[A-Za-z0-9][A-Za-z0-9.,:;/+\-='&%]*[\)\]»\"'،]*$")
def legacy(t):
    """v2.4 convention: visual order for renderers that place words left-to-right."""
    t=t.replace('‌',' ').replace('ٔ','').replace('ً','').replace('«','"').replace('»','"').replace(' ▪ ',' | ').replace('؛',' ؛')
    t=re.sub(r'\s*،\s*',' ، ',t)
    toks=t.split()
    groups=[]; run=[]
    for k in toks:
        if LAT.match(k) and not re.search(r'[؀-ۿ]',k): run.append(k)
        else:
            if run: groups.append(' '.join(run)); run=[]
            groups.append(k)
    if run: groups.append(' '.join(run))
    return ' '.join(reversed(groups))
def h_modern(t):
    parts=[html.escape(x,quote=False) for x in t.split(' ▪ ')]
    parts=[re.sub(r'^\[([^\]]+)\]',r'<i>[\1]</i>',x) for x in parts]
    return '<br/>'.join(parts)
os.makedirs(OUT,exist_ok=True)
# 1. plain tab-delimited (logical order) + alternates  -> pyglossary input & universal source
with open(OUT+'/en-fa.tabfile.txt','w',encoding='utf-8') as f, open(OUT+'/en-fa.html.tabfile.txt','w',encoding='utf-8') as g:
    f.write('##name\t%s\n##sourceLang\tEnglish\n##targetLang\tPersian\n'%TITLE)
    g.write('##name\t%s\n##sourceLang\tEnglish\n##targetLang\tPersian\n'%TITLE)
    for e in m:
        key='|'.join([e['head'].replace('|','/')]+e['alts'])
        f.write(key+'\t'+e['def'].replace(' ▪ ',' | ')+'\n')
        g.write(key+'\t<div dir="rtl" style="text-align:right">'+h_modern(e['def'])+'</div>\n')
import unicodedata
def kprefix(w):
    wo=w[:2].strip().lower()
    if not wo or any(not unicodedata.category(c).startswith('L') for c in wo): return '11'
    return wo
with open(OUT+'/en-fa.kobo.tabfile.txt','w',encoding='utf-8') as g:
    g.write('##name\t%s\n##sourceLang\tEnglish\n##targetLang\tPersian\n'%TITLE)
    for e in m:
        body='<div dir="rtl" style="text-align:right">'+h_modern(e['def'])+'</div>'
        hp=kprefix(e['head']); same=[a for a in e['alts'] if kprefix(a)==hp]; other=[a for a in e['alts'] if kprefix(a)!=hp]
        g.write('|'.join([e['head'].replace('|','/')]+same)+'\t'+body+'\n')
        for a in other:
            g.write(a+'\t<div><i>→ '+html.escape(e['head'],quote=False)+'</i></div>'+body+'\n')
# 2. Kindle sources
OPF='''<?xml version="1.0" encoding="utf-8"?>
<package unique-identifier="uid" xmlns="http://www.idpf.org/2007/opf" version="2.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>%s</dc:title><dc:language>en-us</dc:language><dc:creator>H.Yazdani</dc:creator>
<dc:contributor>v3.0 revision and expansion</dc:contributor>
<dc:identifier id="uid">%s</dc:identifier>
<x-metadata><DictionaryInLanguage>en-us</DictionaryInLanguage><DictionaryOutLanguage>fa</DictionaryOutLanguage><DefaultLookupIndex>default</DefaultLookupIndex></x-metadata>
</metadata>
<manifest><item id="c" href="content.html" media-type="application/xhtml+xml"/></manifest>
<spine><itemref idref="c"/></spine>
</package>'''
HEAD='<html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg" xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><body><mbp:frameset>\n'
def kindle(name,title,fn):
    d=OUT+'/'+name; os.makedirs(d,exist_ok=True)
    open(d+'/dict.opf','w',encoding='utf-8').write(OPF%(title,name))
    with open(d+'/content.html','w',encoding='utf-8') as f:
        f.write(HEAD)
        for e in m:
            hw=html.escape(e['head'],quote=True)
            infl=''.join('<idx:iform value="%s"/>'%html.escape(a,quote=True) for a in e['alts'])
            if infl: infl='<idx:infl>'+infl+'</idx:infl>'
            f.write('<idx:entry name="default" scriptable="yes" spell="yes"><idx:short><idx:orth value="%s"><b>%s</b>%s</idx:orth>%s</idx:short></idx:entry>\n'%(hw,hw,infl,fn(e['def'])))
        f.write('</mbp:frameset></body></html>')
kindle('kindle-classic-src',TITLE,lambda t:'<p>'+html.escape(legacy(t),quote=False)+'</p>')
kindle('kindle-rtl-src',TITLE+' (RTL)',lambda t:'<p dir="rtl">'+h_modern(t)+'</p>')  # no align="right": the full source must stay under kindlegen's ~40 MB limit
print('exported',len(m))
import random; random.seed(5)
for e in random.sample(m,6): print(e['head'],'\n  M:',e['def'],'\n  L:',legacy(e['def']))
