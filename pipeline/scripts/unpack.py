import sys
from calibre.ebooks.mobi.reader.mobi6 import MobiReader
from calibre.utils.logging import default_log
src, out = sys.argv[1], sys.argv[2]
mr = MobiReader(src, default_log)
mr.extract_text()
raw = mr.mobi_html
open(out, 'wb').write(raw)
h = mr.book_header
print('len', len(raw), 'codec', h.codec, 'compression', h.compression_type, 'title', h.title)
print('records', len(mr.sections), 'first_image', getattr(h,'first_image_index',None))
eh = h.exth
print('exth', {k: getattr(eh, k) for k in dir(eh) if not k.startswith('_') and k in ('mi','start_offset','kf8_header')} if eh else None)
try:
    print(eh.mi)
except Exception as e: print(e)
