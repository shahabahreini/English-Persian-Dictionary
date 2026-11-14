import sys,struct,gzip,zipfile,re,io
import xml.etree.ElementTree as ET
try: from idzip import IdzipFile
except ImportError:  # .dict.dz is gzip-compatible; read it whole when idzip is not installed
    class IdzipFile(io.BytesIO):
        def __init__(self,p): super().__init__(gzip.open(p).read())
D=sys.argv[1]; V=sys.argv[2] if len(sys.argv)>2 else '3.1'
# StarDict: parse idx/syn, decode via .dict.dz
base=D+'/StarDict/English-Persian-v%s/English-Persian-v%s'%(V,V)
ifo=dict(l.strip().split('=',1) for l in open(base+'.ifo',encoding='utf-8') if '=' in l)
idx=open(base+'.idx','rb').read(); words=[]; p=0
while p<len(idx):
    e=idx.index(b'\0',p); w=idx[p:e].decode(); off,sz=struct.unpack('>II',idx[e+1:e+9]); words.append((w,off,sz)); p=e+9
syn=open(base+'.syn','rb').read(); syns={}; p=0
while p<len(syn):
    e=syn.index(b'\0',p); syns[syn[p:e].decode()]=struct.unpack('>I',syn[e+1:e+5])[0]; p=e+5
print('stardict: ifo wordcount',ifo['wordcount'],'parsed',len(words),'syn',len(syns),ifo['synwordcount'])
# sorted check (StarDict requires g_ascii_strcasecmp order)
def k(w): return (w.encode().lower(), w.encode())
print('  idx sorted:', all(k(words[i][0])<=k(words[i+1][0]) for i in range(len(words)-1)))
dz=IdzipFile(base+'.dict.dz'); W={w:(o,s) for w,o,s in words}
def look(w):
    if w in W: o,s=W[w]
    elif w in syns: o,s=words[syns[w]][1:]; w=w+' → '+words[syns[w]][0]
    else: return w+' : NOT FOUND'
    dz.seek(o); return w+' : '+dz.read(s).decode()[:140]
for w in ['internet','walked','theurgical','set','smartphone','went','figure out','illustrious','leukaemia','epistemology','a priori','sus','crop rotation','mise en scene','haute couture','freight forwarder','chiaroscuro','gaslighting','chill out','lol']: print('  ',look(w))
# Kobo
z=zipfile.ZipFile(D+'/Kobo/dicthtml-en-fa.zip'); names=z.namelist()
print('kobo: files',len(names),names[:6])
html=[n for n in names if n.endswith('.html')]
blob=z.read(html[len(html)//2]); 
try: txt=gzip.decompress(blob).decode()
except Exception: txt=blob.decode('utf-8','replace')
print('  sample',txt[:300].replace('\n',' '))
# Kindle sources well-formed
import glob
for v in ['source-classic','source-rtl']:
    n=0
    for f in sorted(glob.glob(D+'/Kindle/'+v+'/content*.html')):
        try:
            root=ET.parse(f).getroot(); ns='{https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf}'
            n+=sum(1 for _ in root.iter(ns+'entry'))
        except ET.ParseError as e: print('kindle',v,f,'PARSE ERROR',e)
    print('kindle',v,'well-formed XML, entries',n)
    ET.parse(D+'/Kindle/'+v+'/dict.opf')
