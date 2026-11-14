import sys, re, io
from calibre.ebooks.mobi.reader.mobi6 import MobiReader
from calibre.utils.logging import default_log
from calibre.ebooks.mobi.reader.headers import MetadataHeader
p = sys.argv[1]
mr = MobiReader(p, default_log)
mr.extract_text()
t = mr.mobi_html.decode('utf-8','replace') if isinstance(mr.mobi_html, bytes) else mr.mobi_html
print('title:', mr.book_header.title, '| codec:', mr.book_header.codec, '| mobi ver:', mr.book_header.mobi_version)
print('html bytes:', len(t), '| <b> heads:', len(re.findall(r'<b>', t)))
for w in ['internet', 'walk', 'smartphone']:
    m = re.search(r'<b>%s</b>(.{0,200})' % w, t)
    print(w, '->', m.group(1)[:160] if m else None)
