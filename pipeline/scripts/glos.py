import sys
from pyglossary.glossary_v2 import Glossary, ConvertArgs
Glossary.init()
src,dst,fmt=sys.argv[1],sys.argv[2],sys.argv[3]
g=Glossary()
kw={}
if fmt=='Stardict': kw=dict(writeOptions={'sametypesequence':'h','dictzip':True})
if fmt=='StardictPlain': fmt='Stardict'; kw=dict(writeOptions={'sametypesequence':'m','dictzip':True})
r=g.convert(ConvertArgs(inputFilename=src,outputFilename=dst,inputFormat='Tabfile',outputFormat=fmt,**kw))
print('->',r)
