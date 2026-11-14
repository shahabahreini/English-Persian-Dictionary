"""Generate the project landing pages: docs/index.html (English) and docs/fa/index.html (Persian).

usage (from the repository root):  python3 pipeline/scripts/build_site.py

Inputs: pipeline/site/{site.css,site.js,jsonld-en.json,jsonld-fa.json,logos/*.svg}, file sizes from dist/ and data/.
The FAQ shown on each page is built from the FAQPage structured data so visible text and markup always match.
"""
import html, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = os.path.join(ROOT, 'pipeline', 'site')
BASE = 'https://shahabahreini.github.io/English-Persian-Dictionary/'
REPO = 'https://github.com/shahabahreini/English-Persian-Dictionary'
UPSTREAM = 'https://github.com/hossein1376/English-Persian-Kindle-Custom-Dictionary'
RAW = REPO + '/raw/main/'
E = html.escape

def read(*p):
    return open(os.path.join(*p), encoding='utf-8').read()

def logo(name, cls=''):
    s = read(SITE, 'logos', name + '.svg')
    s = re.sub(r'<title>.*?</title>', '', s)
    s = s.replace(' role="img"', '')
    if name == 'kobo':  # the wordmark only fills y 5.3..18.7 of its 24x24 box; crop to it so it renders at a useful size
        s = s.replace('viewBox="0 0 24 24"', 'viewBox="0 5.3 24 13.41"')
    return s.replace('<svg ', '<svg aria-hidden="true" focusable="false"' + (f' class="{cls}"' if cls else '') + ' ', 1)

ICON = {
 'reader': '<svg class="gen" viewBox="0 0 32 32" aria-hidden="true"><rect x="7" y="3" width="18" height="26" rx="2.5"/><path d="M11 9h10M11 14h10M11 19h6"/></svg>',
 'apps': '<svg class="gen" viewBox="0 0 32 32" aria-hidden="true"><rect x="3" y="6" width="26" height="19" rx="2.5"/><path d="M12 29h8M16 25v4"/></svg>',
 'data': '<svg class="gen" viewBox="0 0 32 32" aria-hidden="true"><rect x="5" y="4" width="22" height="24" rx="2.5"/><path d="M5 11h22M5 18h22M14 11v17"/></svg>',
 'dl': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>',
 'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v13M6 13l6 6 6-6"/></svg>',
}

PERSIAN_DIGITS = str.maketrans('0123456789,.', '۰۱۲۳۴۵۶۷۸۹٬٫')

def num(n, fa):
    s = f'{n:,}'
    return s.translate(PERSIAN_DIGITS) if fa else s

def size(rel, fa):
    mb = os.path.getsize(os.path.join(ROOT, rel)) / 1e6
    s = f'{mb:.1f}'
    return (s.translate(PERSIAN_DIGITS) + ' مگابایت') if fa else s + ' MB'

SECTIONS = [  # (English label, Persian label, v2.4, v3.1)
 ('Engineering', 'مهندسی', 6909, 7110), ('Computing', 'رایانه', 3632, 5399),
 ('Business & economics', 'بازرگانی و اقتصاد', 3161, 4335), ('Sports', 'ورزش', 3550, 4153), ('Chemistry', 'شیمی', 3688, 4010),
 ('Law', 'حقوق', 3713, 4003), ('Informal & slang', 'زبان محاوره', 79, 2456), ('Medicine', 'پزشکی', 654, 1633), ('Geography', 'جغرافیا', 15, 1210),
 ('Philosophy & logic', 'فلسفه و منطق', 0, 1181), ('Biology', 'زیست‌شناسی', 517, 996), ('Arts', 'هنر', 0, 865),
 ('Earth & environment', 'علوم زمین و محیط زیست', 0, 753), ('Transport & logistics', 'حمل‌ونقل', 0, 719), ('Mathematics', 'ریاضی', 136, 716),
 ('Agriculture & veterinary', 'کشاورزی و دامپزشکی', 0, 706), ('Psychology', 'روان‌شناسی', 13, 676), ('Linguistics', 'زبان‌شناسی', 63, 665),
 ('Music', 'موسیقی', 208, 631), ('Politics', 'سیاست', 0, 584), ('History & archaeology', 'تاریخ و باستان‌شناسی', 0, 542), ('Food', 'غذا', 0, 537),
 ('Sociology & anthropology', 'جامعه‌شناسی و مردم‌شناسی', 0, 525), ('Literature', 'ادبیات', 0, 520), ('Physics', 'فیزیک', 28, 514),
 ('Fashion & textiles', 'پوشاک و نساجی', 0, 497), ('Education', 'آموزش', 0, 485), ('Statistics', 'آمار', 0, 393),
 ('Media & communication', 'رسانه و ارتباطات', 0, 376), ('Abbreviations', 'اختصارات', 0, 275), ('Religion', 'دین', 0, 165),
]

FILES = {
 'classic': 'dist/kindle/English-Persian.Dictionary.v3.1-classic.mobi',
 'rtl': 'dist/kindle/English-Persian.Dictionary.v3.1-rtl.mobi',
 'kobo': 'dist/kobo/dicthtml-en-fa.zip',
 'sd': 'dist/stardict/English-Persian-v3.1-stardict.zip',
 'sdp': 'dist/stardict/English-Persian-v3.1-stardict-plaintext.zip',
 'tsv': 'data/English-Persian.v3.1.tsv',
 'log': 'data/changelog.tsv',
}

L = {}
L['en'] = dict(
 lang='en', dir='ltr', up='', other_url='fa/', other_label='فارسی', other_lang='fa',
 title='English–Persian Dictionary v3.1 for Kindle, Kobo &amp; KOReader',
 desc='Free English-to-Persian (Farsi) dictionary with 164,524 entries for Kindle, Kobo, KOReader, Onyx Boox and StarDict apps. Download the Kindle .mobi, Kobo dicthtml or StarDict files.',
 og_desc='Free English-to-Persian (Farsi) dictionary with 164,524 entries for Kindle, Kobo, KOReader, Onyx Boox and StarDict apps.',
 tw_desc='Free English-to-Persian (Farsi) dictionary with 164,524 entries for e-readers. Kindle, Kobo, KOReader, StarDict.',
 og_locale='en_US', og_alt='fa_IR', canon=BASE,
 skip='Skip to content', nav_dl='Get it', nav_in="What's inside", nav_faq='FAQ', nav_rep='Report', gh='GitHub', gh_aria='English–Persian Dictionary on GitHub',
 eyebrow='Version 3.1 · Free · Offline · MIT licence',
 h1='English–Persian dictionary for Kindle, Kobo, KOReader and StarDict apps',
 lede='A free, offline English-to-Persian (Farsi) dictionary with <strong>164,524 entries</strong> for e-readers. A revision and expansion of v2.4 with 21,578 new entries, twelve new subject sections in v3.1, standardised Persian spelling and 31,189 inflected forms.',
 cta1='Choose your device', cta2='View on GitHub',
 works='<b>Kindle</b> · <b>Kobo</b> · <b>KOReader</b> · <b>Onyx Boox</b> · <b>StarDict apps</b>',
 spec='Sample entries',
 tag_comp='[رایانه]', tag_elec='[الکترونیک]', tag_v='[v.]',
 stats=[(164524, 'entries (v2.4 had 145,075)'), (21578, 'new entries'), (7016, 'core definitions rewritten'), (31189, 'inflected forms indexed')],
 dl_t='Get the dictionary', dl_p='Pick your device for the right file and the exact steps.',
 dev=[('kindle', 'Kindle', 'Amazon, .mobi'), ('kobo', 'Kobo', 'dicthtml zip'), ('koreader', 'KOReader', 'StarDict, any device'),
      ('stardict', 'Boox &amp; StarDict apps', 'GoldenDict, Moon+ Reader'), ('data', 'Raw data', 'TSV for your own tools')],
 copy='Copy', copied='Copied',
 verify='Built and checked by software; not yet verified screen by screen on every e-reader. <a href="' + REPO + '/issues/new?template=device-report.yml">Report a display problem</a>.',
 in_t="What's inside", in_p='Entries are grouped by subject. Grey is v2.4, teal is v3.1. An entry with senses in several subjects is counted in each.',
 leg_old='v2.4', leg_new='v3.1',
 general='General vocabulary is not charted: 103,231 entries in v2.4 and 101,466 in v3.1 (duplicates were merged, and some entries moved to a subject).',
 cl=[('10,085 new entries in v3.1', 'Twelve new sections (philosophy, earth sciences, statistics, arts, literature, history, sociology, education, agriculture, transport, media, fashion), much more slang, idioms and proverbs, and 3,589 subject senses on existing words.'),
     ('11,493 new entries in v3.0', 'Modern vocabulary (internet, smartphone, podcast), science, medicine, business, phrasal verbs, idioms and slang.'),
     ('7,016 words rewritten', 'The most frequent words: most common sense first, grouped by part of speech, wrong equivalents removed.'),
     ('106,983 entries respelled', 'Persian ی and ک, restored آ, half-spaces, tanvin and ezafe marks, quotation marks.'),
     ('3,120 headwords corrected', 'Misspellings such as illustrous → illustrious. 2,128 duplicates merged, 97 garbled headwords cleaned.'),
     ('31,189 inflected forms', 'Looking up walked opens walk. Plurals, past tenses and -ing forms are indexed.')],
 rep_link='See every change in the report',
 faq_t='Frequently asked questions',
 lim_t='Know before you rely on it',
 lim=['New and rewritten wording was produced by AI language models and has not been reviewed by a human Persian editor.',
      'About 107,000 specialised entries received mechanical repairs only and keep their 1990s wording.',
      'Built and checked by software, not screen by screen on every e-reader. The right-to-left Kindle build has not been tried on a device.'],
 lim_link='Found a mistake? Open a correction',
 cr_t='Credits',
 cr=['Built on <strong>English-Persian Dictionary v2.4</strong>, compiled by H. Yazdani and published by hossein1376 under the MIT licence. Its word list descends from the MHM Advance English-Persian Dictionary.',
     'Revision, new entries and builds by shahabahreini.'],
 cr_up='Original project', cr_this='This project',
 f_links=[('Change report', 'report.html'), ('Credits', REPO + '/blob/main/CREDITS.md'), ('Licence (MIT)', REPO + '/blob/main/LICENSE'), ('llms.txt', 'llms.txt'), ('Cite', REPO + '/blob/main/CITATION.cff')],
 tm='Kindle is a trademark of Amazon.com, Inc. or its affiliates. Kobo is a trademark of Rakuten Kobo Inc. KOReader, Onyx Boox, StarDict and GoldenDict are names or marks of their respective owners. They appear only to show which devices and apps each file is for. This project is not affiliated with or endorsed by any of them.',
)
L['fa'] = dict(
 lang='fa', dir='rtl', up='../', other_url='../', other_label='English', other_lang='en',
 title='دیکشنری انگلیسی به فارسی برای کیندل، کوبو و KOReader – نسخه ۳٫۱',
 desc='دیکشنری رایگان و آفلاین انگلیسی به فارسی با ۱۶۴٬۵۲۴ مدخل برای کتابخوان‌های کیندل، کوبو، KOReader، اونیکس بوکس و برنامه‌های StarDict. دانلود فایل mobi کیندل و آموزش نصب.',
 og_desc='دیکشنری رایگان و آفلاین انگلیسی به فارسی با ۱۶۴٬۵۲۴ مدخل برای کتابخوان‌های کیندل، کوبو، KOReader و StarDict.',
 tw_desc='دیکشنری رایگان و آفلاین انگلیسی به فارسی با ۱۶۴٬۵۲۴ مدخل برای کتابخوان‌ها.',
 og_locale='fa_IR', og_alt='en_US', canon=BASE + 'fa/',
 skip='رفتن به محتوا', nav_dl='دانلود', nav_in='محتوا', nav_faq='پرسش‌ها', nav_rep='گزارش', gh='GitHub', gh_aria='دیکشنری انگلیسی به فارسی در GitHub',
 eyebrow='نسخهٔ ۳٫۱ · رایگان · آفلاین · مجوز MIT',
 h1='دیکشنری انگلیسی به فارسی برای کیندل، کوبو، KOReader و برنامه‌های StarDict',
 lede='فرهنگ لغت رایگان و آفلاین انگلیسی به فارسی با <strong>۱۶۴٬۵۲۴ مدخل</strong> برای کتابخوان‌های الکترونیکی. بازنگری و گسترش نسخهٔ ۲٫۴ با ۲۱٬۵۷۸ مدخل تازه، دوازده بخش موضوعی تازه در نسخهٔ ۳٫۱، املای یکدست و ۳۱٬۱۸۹ شکل صرفی.',
 cta1='انتخاب دستگاه و دانلود', cta2='مشاهده در GitHub',
 works='<b>کیندل</b> · <b>کوبو</b> · <b>KOReader</b> · <b>اونیکس بوکس</b> · <b>برنامه‌های StarDict</b>',
 spec='نمونه مدخل‌ها',
 tag_comp='[رایانه]', tag_elec='[الکترونیک]', tag_v='[v.]',
 stats=[(164524, 'مدخل (نسخهٔ ۲٫۴: ۱۴۵٬۰۷۵)'), (21578, 'مدخل تازه'), (7016, 'واژهٔ پرکاربرد بازنویسی‌شده'), (31189, 'شکل صرفی قابل جست‌وجو')],
 dl_t='دانلود دیکشنری', dl_p='دستگاه خود را انتخاب کنید تا فایل درست و مراحل نصب را ببینید.',
 dev=[('kindle', 'کیندل', 'Amazon، فایل mobi'), ('kobo', 'کوبو', 'فایل zip قالب dicthtml'), ('koreader', 'KOReader', 'StarDict، روی هر دستگاه'),
      ('stardict', 'اونیکس بوکس و StarDict', 'GoldenDict، Moon+ Reader'), ('data', 'داده‌های خام', 'فایل TSV برای ابزار شما')],
 copy='کپی', copied='کپی شد',
 verify='فایل‌ها با نرم‌افزار ساخته و بررسی شده‌اند، اما روی هر مدل کتابخوان صفحه‌به‌صفحه آزمایش نشده‌اند. <a href="' + REPO + '/issues/new?template=device-report.yml" lang="en" dir="ltr">گزارش مشکل نمایش</a>.',
 in_t='درون دیکشنری', in_p='مدخل‌ها بر اساس موضوع دسته‌بندی شده‌اند. خاکستری نسخهٔ ۲٫۴ و فیروزه‌ای نسخهٔ ۳٫۱ است. مدخلی که در چند موضوع معنی دارد، در هرکدام شمرده می‌شود.',
 leg_old='نسخهٔ ۲٫۴', leg_new='نسخهٔ ۳٫۱',
 general='بخش عمومی در نمودار نیست: ۱۰۳٬۲۳۱ مدخل در نسخهٔ ۲٫۴ و ۱۰۱٬۴۶۶ مدخل در نسخهٔ ۳٫۱ (مدخل‌های تکراری ادغام شدند و برخی مدخل‌ها به بخش موضوعی رفتند).',
 cl=[('۱۰٬۰۸۵ مدخل تازه در نسخهٔ ۳٫۱', 'دوازده بخش تازه (فلسفه، علوم زمین، آمار، هنر، ادبیات، تاریخ، جامعه‌شناسی، آموزش، کشاورزی، حمل‌ونقل، رسانه، پوشاک)، زبان محاوره، اصطلاح و ضرب‌المثل بسیار بیشتر و ۳٬۵۸۹ معنای تخصصی برای واژه‌های موجود.'),
     ('۱۱٬۴۹۳ مدخل تازه در نسخهٔ ۳٫۰', 'واژه‌های نو (اینترنت، گوشی هوشمند، پادکست)، علوم، پزشکی، بازرگانی، فعل‌های عبارتی، اصطلاح و زبان محاوره.'),
     ('۷٬۰۱۶ واژه بازنویسی‌شده', 'پرکاربردترین واژه‌ها: معنی رایج‌تر در ابتدا، گروه‌بندی بر اساس نقش دستوری، حذف معادل‌های نادرست.'),
     ('۱۰۶٬۹۸۳ مدخل با املای اصلاح‌شده', '«ی» و «ک» فارسی، «آ»، نیم‌فاصله، تنوین و کسره، گیومه.'),
     ('۳٬۱۲۰ سرواژهٔ اصلاح‌شده', 'غلط‌هایی مانند illustrous ← illustrious. ۲٬۱۲۸ مدخل تکراری ادغام و ۹۷ سرواژهٔ خراب پاک‌سازی شد.'),
     ('۳۱٬۱۸۹ شکل صرفی', 'جست‌وجوی walked به walk می‌رسد. جمع‌ها، گذشته‌ها و شکل‌های ing ثبت شده‌اند.')],
 rep_link='همهٔ تغییرها را در گزارش ببینید',
 faq_t='پرسش‌های متداول',
 lim_t='پیش از اتکا به آن بدانید',
 lim=['معنی‌های تازه و بازنویسی‌شده را مدل‌های هوش مصنوعی نوشته‌اند و ویراستار فارسی‌زبان انسانی آن‌ها را بررسی نکرده است.',
      'حدود ۱۰۷ هزار مدخل تخصصی فقط اصلاح ظاهری شده‌اند و همان متن دههٔ ۷۰ را دارند.',
      'فایل‌ها با نرم‌افزار ساخته و بررسی شده‌اند، نه روی هر کتابخوان. نسخهٔ RTL کیندل هنوز روی دستگاه آزمایش نشده است.'],
 lim_link='ایرادی دیدید؟ اصلاحیه بفرستید',
 cr_t='منابع و سپاس',
 cr=['بر پایهٔ <strong>دیکشنری انگلیسی به فارسی نسخهٔ ۲٫۴</strong> که ح. یزدانی گردآورده و hossein1376 با مجوز MIT منتشر کرده است. فهرست واژه‌های آن از «MHM Advance English-Persian Dictionary» گرفته شده است.',
     'بازنگری، مدخل‌های تازه و ساخت فایل‌ها: shahabahreini.'],
 cr_up='پروژهٔ اصلی', cr_this='این پروژه',
 f_links=[('گزارش تغییرات', '../report.html'), ('منابع', REPO + '/blob/main/CREDITS.md'), ('مجوز MIT', REPO + '/blob/main/LICENSE'), ('llms.txt', '../llms.txt'), ('ارجاع', REPO + '/blob/main/CITATION.cff')],
 tm='Kindle نشان تجاری Amazon.com, Inc. یا شرکت‌های وابسته به آن است. Kobo نشان تجاری Rakuten Kobo Inc. است. KOReader، Onyx Boox، StarDict و GoldenDict نام یا نشان صاحبان خود هستند. این نشان‌ها فقط برای نشان‌دادن دستگاه یا برنامهٔ مناسب هر فایل آمده‌اند. این پروژه وابسته به هیچ‌یک از آن‌ها نیست و از طرف آن‌ها تأیید نشده است.',
)

PANELS = {
 'en': {
  'kindle': dict(t='Kindle', sub='For E Ink Kindles that already showed Persian in v2.4.',
    files=[('classic', 'English-Persian.Dictionary.v3.1-classic.mobi', 'Recommended. Same display style as v2.4.', True),
           ('rtl', 'English-Persian.Dictionary.v3.1-rtl.mobi', 'Only if sentences look reversed. For Kindle apps and firmware that handle right-to-left text.', False)],
    steps=['Connect the Kindle to your computer with a USB cable.',
           ('Copy the file into', 'documents/dictionaries/'),
           'Eject the Kindle. In a book, long-press a word, tap the dictionary name in the pop-up and choose <em>English-Persian Dictionary v3.1</em>. Or go to Settings › Language &amp; Dictionaries › Dictionaries › English.'],
    note='Still have v2.4 installed? Both appear in the list. Delete the old one once you are happy with v3.1.'),
  'kobo': dict(t='Kobo', sub='All models with firmware 4.24 or later.',
    files=[('kobo', 'dicthtml-en-fa.zip', 'Copy it as it is. Do not unzip.', True)],
    steps=['Connect the Kobo to your computer with a USB cable.',
           ('Copy the zip into', '.kobo/custom-dict/', '(create the folder if it is missing).'),
           'Eject, then choose it under Settings › Language and dictionaries.'], note=None),
  'koreader': dict(t='KOReader', sub='Runs on Kindle, Kobo, PocketBook, Onyx Boox, reMarkable and Android.',
    files=[('sd', 'English-Persian-v3.1-stardict.zip', 'StarDict format with an index for inflected forms.', True)],
    steps=['Unzip the file. You get a folder called <code>English-Persian-v3.1</code>.',
           ('Copy that folder into', 'koreader/data/dict/'),
           'In KOReader, long-press a word. If the dictionary does not appear, enable it in the search menu › Dictionary settings › Manage dictionaries.'], note=None),
  'stardict': dict(t='Onyx Boox and other StarDict apps', sub='Boox built-in reader, GoldenDict, Moon+ Reader, AlReader and other StarDict apps.',
    files=[('sd', 'English-Persian-v3.1-stardict.zip', 'Recommended.', True),
           ('sdp', 'English-Persian-v3.1-stardict-plaintext.zip', 'Same content as plain text, for readers that print HTML tags as text (CoolReader, early PocketBook and Onyx firmware).', False)],
    steps=['Unzip the file.',
           ('Copy the folder into the app\'s dictionary folder', 'dicts/', '(Onyx Boox).'),
           'Select it in the app\'s dictionary settings, then look up a word.'], note=None),
  'data': dict(t='Raw data', sub='For your own tools, analysis or another format.',
    files=[('tsv', 'English-Persian.v3.1.tsv', 'All 164,524 entries: headword, definition, sections, status, alternate forms.', True),
           ('log', 'changelog.tsv', 'Every change, with the v2.4 text beside the v3.1 text.', False)],
    steps=['Download the TSV. It is UTF-8 and tab-separated.',
           'Open it in a spreadsheet or read it with a script.',
           'To rebuild or edit it, see the <a href="' + REPO + '/blob/main/pipeline/README.md">pipeline guide</a>.'], note=None),
 },
 'fa': {
  'kindle': dict(t='کیندل', sub='برای کیندل‌های E Ink که در نسخهٔ ۲٫۴ هم فارسی را درست نشان می‌دادند.',
    files=[('classic', 'English-Persian.Dictionary.v3.1-classic.mobi', 'پیشنهادی. شیوهٔ نمایش مثل نسخهٔ ۲٫۴.', True),
           ('rtl', 'English-Persian.Dictionary.v3.1-rtl.mobi', 'فقط اگر جمله‌ها وارونه دیده شد. برای برنامه‌ها و فریم‌ورهای کیندل که متن راست‌به‌چپ را خودشان درست نشان می‌دهند.', False)],
    steps=['کیندل را با کابل USB به رایانه وصل کنید.',
           ('فایل را در این پوشه کپی کنید:', 'documents/dictionaries/'),
           'کیندل را جدا کنید. داخل کتاب روی یک واژه انگشت بگذارید، نام واژه‌نامه را در پنجرهٔ معنی لمس کنید و <em class="ltr">English-Persian Dictionary v3.1</em> را انتخاب کنید. یا از <span class="ltr">Settings › Language &amp; Dictionaries › Dictionaries › English</span> تنظیم کنید.'],
    note='نسخهٔ ۲٫۴ هنوز روی دستگاه است؟ هر دو در فهرست دیده می‌شوند. وقتی از نسخهٔ ۳٫۱ راضی بودید، قدیمی را پاک کنید.'),
  'kobo': dict(t='کوبو', sub='همهٔ مدل‌ها با فریم‌ور ۴٫۲۴ یا بالاتر.',
    files=[('kobo', 'dicthtml-en-fa.zip', 'همان‌طور که هست کپی کنید. باز نکنید.', True)],
    steps=['کوبو را با کابل USB به رایانه وصل کنید.',
           ('فایل zip را در این پوشه کپی کنید:', '.kobo/custom-dict/', '(اگر نبود، پوشه را بسازید).'),
           'کوبو را جدا کنید و از <span class="ltr">Settings › Language and dictionaries</span> انتخابش کنید.'], note=None),
  'koreader': dict(t='KOReader', sub='روی کیندل، کوبو، پاکت‌بوک، اونیکس بوکس، ریمارکبل و اندروید کار می‌کند.',
    files=[('sd', 'English-Persian-v3.1-stardict.zip', 'قالب StarDict همراه با نمایهٔ شکل‌های صرفی.', True)],
    steps=['فایل را باز کنید. پوشه‌ای به نام <code>English-Persian-v3.1</code> به دست می‌آید.',
           ('این پوشه را در این مسیر دستگاه کپی کنید:', 'koreader/data/dict/'),
           'در KOReader روی یک واژه انگشت بگذارید. اگر واژه‌نامه دیده نشد، از منوی جست‌وجو و سپس <span class="ltr">Dictionary settings › Manage dictionaries</span> فعالش کنید.'], note=None),
  'stardict': dict(t='اونیکس بوکس و برنامه‌های StarDict', sub='کتاب‌خوان داخلی Boox، GoldenDict، Moon+ Reader، AlReader و دیگر برنامه‌های StarDict.',
    files=[('sd', 'English-Persian-v3.1-stardict.zip', 'پیشنهادی.', True),
           ('sdp', 'English-Persian-v3.1-stardict-plaintext.zip', 'همان محتوا به صورت متن ساده، برای کتابخوان‌هایی که تگ HTML را به شکل متن نشان می‌دهند (CoolReader و فریم‌ورهای قدیمی پاکت‌بوک و اونیکس).', False)],
    steps=['فایل را باز کنید.',
           ('پوشه را در پوشهٔ واژه‌نامهٔ برنامه کپی کنید', 'dicts/', '(در اونیکس بوکس).'),
           'در تنظیمات واژه‌نامهٔ برنامه آن را انتخاب کنید و یک واژه را جست‌وجو کنید.'], note=None),
  'data': dict(t='داده‌های خام', sub='برای ابزار خودتان، تحلیل یا ساخت قالبی دیگر.',
    files=[('tsv', 'English-Persian.v3.1.tsv', 'همهٔ ۱۶۴٬۵۲۴ مدخل: سرواژه، تعریف، بخش‌ها، وضعیت، شکل‌های دیگر.', True),
           ('log', 'changelog.tsv', 'هر تغییر، با متن نسخهٔ ۲٫۴ کنار متن نسخهٔ ۳٫۱.', False)],
    steps=['فایل TSV را دانلود کنید. با UTF-8 و جداکنندهٔ تب است.',
           'آن را در صفحه‌گسترده باز کنید یا با اسکریپت بخوانید.',
           'برای ساخت دوباره یا ویرایش، <a href="' + REPO + '/blob/main/pipeline/README.md" lang="en" dir="ltr">راهنمای pipeline</a> را ببینید.'], note=None),
 },
}


def wbr(name):
    s = E(name)
    for tok in ('-', 'Persian.', 'Dictionary.'):
        s = s.replace(tok, tok + '<wbr>')
    return s


def panel_html(c, lang, key, spec):
    fa = lang == 'fa'
    files = ''
    for fk, name, desc, main in spec['files']:
        href = RAW + FILES[fk]
        files += (f'<a class="file{" main" if main else ""}" href="{href}" download>{ICON["dl"]}'
                  f'<span><span class="n">{wbr(name)}</span><span class="d">{desc}</span></span>'
                  f'<span class="s">{size(FILES[fk], fa)}</span></a>')
    steps = ''
    for s in spec['steps']:
        if isinstance(s, tuple):
            pre, path = s[0], s[1]
            post = s[2] if len(s) > 2 else ''
            steps += (f'<li><span>{pre} <code>{E(path)}</code> {post} '
                      f'<button class="copy" type="button" hidden data-copy="{E(path)}" data-done="{c["copied"]}">{c["copy"]}</button></span></li>')
        else:
            steps += f'<li><span>{s}</span></li>'
    note = f'<p class="note">{spec["note"]}</p>' if spec['note'] else ''
    return (f'<div class="panel" role="tabpanel" id="{key}" aria-labelledby="tab-{key}" tabindex="0">'
            f'<div><h3>{spec["t"]}</h3><p class="sub">{spec["sub"]}</p><div class="dl">{files}</div></div>'
            f'<div><ol class="steps">{steps}</ol>{note}</div></div>')


def build(lang):
    c = L[lang]; fa = lang == 'fa'; up = c['up']
    jl = json.dumps(json.load(open(os.path.join(SITE, f'jsonld-{lang}.json'), encoding='utf-8')), ensure_ascii=False, indent=1)
    faq_items = [x for g in json.loads(jl)['@graph'] if g['@type'] == 'FAQPage' for x in g['mainEntity']]
    faq = ''.join(f'<details><summary>{E(q["name"])}</summary><p>{E(q["acceptedAnswer"]["text"])}</p></details>' for q in faq_items)

    dev_logo = {'kindle': ICON['reader'], 'kobo': '<span class="wm">' + logo('kobo', 'wm') + '</span>', 'koreader': logo('koreader'),
                'stardict': ICON['apps'], 'data': ICON['data']}
    devs = ''.join(f'<a class="dev" role="tab" id="tab-{k}" data-panel="{k}" href="#{k}" aria-controls="{k}" aria-selected="false">'
                   f'<span class="logo">{dev_logo[k]}</span><span><strong>{n}</strong><small>{s}</small></span></a>'
                   for k, n, s in c['dev'])
    panels = ''.join(panel_html(c, lang, k, PANELS[lang][k]) for k, _, _ in c['dev'])

    stats = ''.join(f'<div class="stat"><b>{num(n, fa)}</b><span>{lab}</span></div>' for n, lab in c['stats'])
    mx = max(s[3] for s in SECTIONS)
    rows = ''
    for en, fl, a, b in SECTIONS:
        old = f'<span class="o" style="--w2:{a / mx * 100:.2f}%"></span>' if a else ''
        label = fl if fa else E(en)
        nums = (f'{num(a, fa)} → <b>{num(b, fa)}</b>' if a else f'<b>{num(b, fa)}</b>')
        rows += (f'<div class="row"><div class="k">{label}</div><div class="b">{old}<span class="v" style="--w3:{b / mx * 100:.2f}%"></span></div>'
                 f'<div class="nn">{nums}</div></div>')
    cl = ''.join(f'<div><b>{h}</b><span>{p}</span></div>' for h, p in c['cl'])
    lims = ''.join(f'<li>{x}</li>' for x in c['lim'])
    cr = ''.join(f'<p>{x}</p>' for x in c['cr'])
    flinks = ''.join(f'<a href="{u}">{E(n)}</a>' for n, u in c['f_links'])
    gh = logo('github')
    ent = (f'<div class="ent"><div class="hw"><span>internet</span><span class="tag">{c["tag_comp"]}</span></div><div class="fa">اینترنت، شبکهٔ جهانی</div></div>'
           f'<div class="ent"><div class="hw"><span>smartphone</span><span class="tag">{c["tag_elec"]}</span></div><div class="fa">گوشی هوشمند، تلفن هوشمند</div></div>'
           f'<div class="ent"><div class="hw"><span>walked</span><span class="ar">→</span><span>walk</span><span class="tag m">{c["tag_v"]}</span></div><div class="fa">راه رفتن، قدم زدن، گام زدن</div></div>')
    img = BASE + 'assets/og-image.png'
    alt = 'English–Persian Dictionary v3.1: 164,524 entries for Kindle, Kobo, KOReader and StarDict'
    css = read(SITE, 'site.css'); js = read(SITE, 'site.js')
    other = c['other_url']

    return f'''<!doctype html>
<html lang="{lang}" dir="{c['dir']}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{c['title']}</title>
<meta name="description" content="{E(c['desc'])}">
<link rel="canonical" href="{c['canon']}">
<link rel="alternate" hreflang="en" href="{BASE}">
<link rel="alternate" hreflang="fa" href="{BASE}fa/">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="theme-color" content="#f6f4ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0e171c" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<meta name="author" content="shahabahreini">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{'دیکشنری انگلیسی به فارسی' if fa else 'English–Persian Dictionary'}">
<meta property="og:locale" content="{c['og_locale']}">
<meta property="og:locale:alternate" content="{c['og_alt']}">
<meta property="og:title" content="{c['title']}">
<meta property="og:description" content="{E(c['og_desc'])}">
<meta property="og:url" content="{c['canon']}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{c['title']}">
<meta name="twitter:description" content="{E(c['tw_desc'])}">
<meta name="twitter:image" content="{img}">
<link rel="alternate" type="text/markdown" href="{up}llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Vazirmatn:wght@400;500;700&display=swap">
<style>
{css}
</style>
<script type="application/ld+json">
{jl}
</script>
</head>
<body>
<a class="skip" href="#main">{c['skip']}</a>
<header class="site-header"><div class="wrap bar">
  <a class="brand" href="./" aria-label="{E(c['title'].replace('&amp;', '&'))}">{'دیکشنری انگلیسی به فارسی' if fa else 'English–Persian'} <small>v3.1</small></a>
  <nav class="nav" aria-label="{'منوی اصلی' if fa else 'Main'}">
    <a class="opt" href="#download">{c['nav_dl']}</a><a class="opt" href="#inside">{c['nav_in']}</a><a class="opt" href="#faq">{c['nav_faq']}</a><a class="opt" href="{up}report.html">{c['nav_rep']}</a>
    <a class="lang" href="{other}" hreflang="{c['other_lang']}" lang="{c['other_lang']}">{c['other_label']}</a>
    <a class="gh" href="{REPO}" aria-label="{E(c['gh_aria'])}" lang="en" dir="ltr">{gh}<span>{c['gh']}</span></a>
  </nav>
</div></header>

<main id="main" class="wrap">
<div class="hero">
  <div>
    <p class="eyebrow">{c['eyebrow']}</p>
    <h1>{c['h1']}</h1>
    <p class="lede">{c['lede']}</p>
    <div class="cta"><a class="btn primary" href="#download">{c['cta1']} {ICON['arrow']}</a><a class="btn ghost" href="{REPO}">{gh}{c['cta2']}</a></div>
    <p class="works">{c['works']}</p>
  </div>
  <aside class="specimen" aria-label="{c['spec']}"><h2>{c['spec']}</h2>{ent}</aside>
</div>

<div class="stats">{stats}</div>

<section id="download">
  <div class="head"><h2 class="t">{c['dl_t']}</h2><p>{c['dl_p']}</p></div>
  <div class="devs" role="tablist" aria-label="{c['dl_t']}">{devs}</div>
  {panels}
  <p class="fine">{c['verify']}</p>
</section>

<section id="inside">
  <div class="head"><h2 class="t">{c['in_t']}</h2><p>{c['in_p']}</p></div>
  <div class="legend"><span><i style="background:var(--rule-strong)"></i>{c['leg_old']}</span><span><i style="background:var(--accent)"></i>{c['leg_new']}</span></div>
  <div class="bars">{rows}</div>
  <p class="gen-note">{c['general']}</p>
  <div class="cl">{cl}</div>
  <p class="fine"><a href="{up}report.html">{c['rep_link']} →</a></p>
</section>

<section id="faq">
  <div class="head"><h2 class="t">{c['faq_t']}</h2></div>
  <div class="faq">{faq}</div>
</section>

<section>
  <div class="two">
    <div class="card warn"><h3>{c['lim_t']}</h3><ul>{lims}</ul><p style="margin-top:14px"><a href="{REPO}/issues/new/choose">{c['lim_link']}</a></p></div>
    <div class="card"><h3>{c['cr_t']}</h3>{cr}<p><a class="ghlink" href="{UPSTREAM}" lang="en" dir="ltr">{gh}hossein1376/English-Persian-Kindle-Custom-Dictionary</a></p><p><a class="ghlink" href="{REPO}" lang="en" dir="ltr">{gh}shahabahreini/English-Persian-Dictionary</a></p></div>
  </div>
</section>
</main>

<footer><div class="wrap">
  <div class="links">{flinks}<a href="{REPO}" lang="en" dir="ltr">GitHub</a></div>
  <p class="tm">{c['tm']}</p>
</div></footer>
<script>
{js}
</script>
</body>
</html>
'''


if __name__ == '__main__':
    for lang, path in (('en', 'docs/index.html'), ('fa', 'docs/fa/index.html')):
        out = os.path.join(ROOT, path)
        open(out, 'w', encoding='utf-8').write(build(lang))
        print('wrote', path, os.path.getsize(out), 'bytes')
