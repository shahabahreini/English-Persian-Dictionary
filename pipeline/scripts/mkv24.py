"""raw.html (from unpack.py) -> v24.tsv: one 'headword<TAB>definition' row per entry.

v2.4 stores each Persian definition with its words in reverse (visual) order so that
Kindle pop-ups, which lay text out left to right, display it correctly. Restore reading order.
usage: python3 mkv24.py raw.html v24.tsv
"""
import re, sys
raw = open(sys.argv[1], encoding='utf-8').read()
n = 0
with open(sys.argv[2], 'w', encoding='utf-8') as out:
    for head, d in re.findall(r'<b>(.*?)</b><p>(.*?)</p>', raw, flags=re.S):
        out.write(head + '\t' + ' '.join(reversed(d.split(' '))) + '\n')
        n += 1
print(n, 'entries')
