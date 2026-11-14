"""Wrap the generated change report (an HTML fragment from report.py) into a complete,
indexable web page with a proper head: charset, viewport, canonical URL, description, Open Graph, Twitter card.

usage: python3 site.py <report-fragment.html> <out/report.html>
"""
import sys, html

BASE = 'https://shahabahreini.github.io/English-Persian-Dictionary/'
REPO = 'https://github.com/shahabahreini/English-Persian-Dictionary'
TITLE = 'Change report: English–Persian Dictionary v3.0 vs v2.4 (154,439 entries)'
DESC = ('Every new, rewritten and corrected entry in English–Persian Dictionary v3.0 next to its v2.4 text, '
        'with entry counts per subject section (computing, medicine, law, slang…), device compatibility and known limits.')

frag = open(sys.argv[1], encoding='utf-8').read()
cut = frag.index('</style>') + len('</style>')
head_part, body_part = frag[:cut], frag[cut:]
# the fragment's own <title> and tool-specific meta are replaced by the page head below
head_part = head_part[head_part.index('<link rel="stylesheet"'):]

e = html.escape
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{BASE}report.html">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="theme-color" content="#0b7f86">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="English–Persian Dictionary">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{BASE}report.html">
<meta property="og:image" content="{BASE}assets/og-image.png">
<meta property="og:image:alt" content="English–Persian Dictionary v3.0: 154,439 entries for Kindle, Kobo, KOReader and StarDict">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(TITLE)}">
<meta name="twitter:description" content="{e(DESC)}">
<meta name="twitter:image" content="{BASE}assets/og-image.png">
{head_part}
</head>
<body>
<nav style="font:14px/1.4 system-ui,sans-serif;padding:10px 16px;border-bottom:1px solid #d7dfe4"><a href="./">English–Persian Dictionary v3.0</a> · <a href="fa/" hreflang="fa" lang="fa">فارسی</a> · <a href="{REPO}">GitHub</a></nav>
'''
open(sys.argv[2], 'w', encoding='utf-8').write(head + body_part.strip() + '\n</body>\n</html>\n')
print('wrote', sys.argv[2])
