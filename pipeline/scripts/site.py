"""Wrap the generated change report (an HTML fragment from report.py) into a complete,
indexable web page with a proper head: charset, viewport, canonical URL, description, Open Graph, Twitter card.

usage: python3 site.py <report-fragment.html> <out/report.html>
"""
import sys, html

BASE = 'https://shahabahreini.github.io/English-Persian-Dictionary/'
REPO = 'https://github.com/shahabahreini/English-Persian-Dictionary'
TITLE = 'Change report: English–Persian Dictionary v3.1 vs v2.4 (164,524 entries)'
DESC = ('Every new, rewritten and corrected entry in English–Persian Dictionary v3.1 next to its v2.4 text, '
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
<meta property="og:image:alt" content="English–Persian Dictionary v3.1: 164,524 entries for Kindle, Kobo, KOReader and StarDict">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(TITLE)}">
<meta name="twitter:description" content="{e(DESC)}">
<meta name="twitter:image" content="{BASE}assets/og-image.png">
{head_part}
<style>
.sitebar{{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:16px;justify-content:space-between;padding:0 24px;min-height:64px;background:rgba(246,244,238,.92);backdrop-filter:blur(10px);border-bottom:1px solid #d9dcd5;font:400 .93rem/1.2 "IBM Plex Sans",system-ui,sans-serif}}
.sb-brand{{color:#14212b;text-decoration:none;font:600 1.15rem/1 Newsreader,Georgia,serif;letter-spacing:-.01em;white-space:nowrap}}
.sb-brand small{{font:500 .68rem/1 "IBM Plex Mono",monospace;color:#0b7f86;letter-spacing:.1em;margin-left:8px}}
.sb-links{{display:flex;align-items:center;gap:6px}}
.sb-links a{{color:#566570;text-decoration:none;padding:8px 12px;border-radius:6px;white-space:nowrap}}
.sb-links a:hover{{background:#e2efec;color:#14212b}}
.sb-links .sb-gh{{display:inline-flex;align-items:center;gap:8px;border:1px solid #c3c8c0;color:#14212b;background:#fcfbf7;font-weight:500}}
.sb-links .sb-gh svg{{flex:none}}
@media (max-width:560px){{.sb-gh span{{display:none}}}}
</style>
</head>
<body>
<header class="sitebar"><a class="sb-brand" href="./">English–Persian <small>v3.1</small></a><span class="sb-links"><a href="./#download">Download</a><a href="fa/" hreflang="fa" lang="fa">فارسی</a><a class="sb-gh" href="{REPO}" aria-label="English–Persian Dictionary on GitHub"><svg viewBox="0 0 24 24" aria-hidden="true" width="19" height="19" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg><span>GitHub</span></a></span></header>
'''
open(sys.argv[2], 'w', encoding='utf-8').write(head + body_part.strip() + '\n</body>\n</html>\n')
print('wrote', sys.argv[2])
