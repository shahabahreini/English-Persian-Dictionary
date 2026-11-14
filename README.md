# English–Persian Dictionary v3.0

A revised and expanded English→Persian dictionary for e-readers: **154,439 entries**, built for Kindle, Kobo, KOReader, Onyx Boox, PocketBook (via KOReader) and any StarDict app.

It is a derivative of the freely distributed **English-Persian Dictionary v2.4** by H. Yazdani, as published by [hossein1376/English-Persian-Kindle-Custom-Dictionary](https://github.com/hossein1376/English-Persian-Kindle-Custom-Dictionary). Full credit and licence details are in [CREDITS.md](CREDITS.md).

📊 **[Open the change report](docs/index.html)** (also served at the repo's GitHub Pages site if enabled). It lists every new, rewritten and corrected entry with the v2.4 text beside the new one, entry counts per subject section, and a search box.

[فارسی ↓](#فارسی)

---

## Download

| Your device | File | Install |
|---|---|---|
| **Kindle** (E Ink, all generations that showed Persian in v2.4) | [`dist/kindle/English-Persian.Dictionary.v3.0-classic.mobi`](dist/kindle/English-Persian.Dictionary.v3.0-classic.mobi) | Copy to the Kindle's `documents/dictionaries/` folder. In a book, long-press a word, tap the dictionary name, choose *English-Persian Dictionary v3.0*. Or set it in *Settings › Language & Dictionaries › Dictionaries › English*. |
| **Kobo** (firmware 4.24+) | [`dist/kobo/dicthtml-en-fa.zip`](dist/kobo/dicthtml-en-fa.zip) | Copy to `.kobo/custom-dict/` (create the folder if needed), eject, then pick it under *Settings › Language and dictionaries*. |
| **KOReader** (Kindle, Kobo, PocketBook, Boox, reMarkable, Android), **Onyx Boox**, GoldenDict, Moon+ Reader, other StarDict apps | [`dist/stardict/English-Persian-v3.0-stardict.zip`](dist/stardict/English-Persian-v3.0-stardict.zip) | Unzip into `koreader/data/dict/` (KOReader) or the app's dictionary folder (Boox: `dicts/`). |
| Readers that print HTML tags as text (CoolReader, early PocketBook / Onyx firmware) | [`dist/stardict/English-Persian-v3.0-stardict-plaintext.zip`](dist/stardict/English-Persian-v3.0-stardict-plaintext.zip) | Same as above. |
| Your own tools | [`data/English-Persian.v3.0.tsv`](data/English-Persian.v3.0.tsv) | Tab-separated: headword, definition, sections, status, alternate forms. |

### Why the Kindle build stores Persian "backwards"
Kindle dictionary pop-ups on E Ink devices lay text out left to right and do not reorder right-to-left scripts. Following v2.4, the classic build stores each definition with its words in reverse order so it *displays* correctly. The StarDict, Kobo and source TSV files use normal reading order.

If a Kindle app or newer firmware shows sentences reversed with the classic build, it handles right-to-left text itself and needs the RTL variant. No compiled RTL `.mobi` is included yet: the pipeline generates its source, but Amazon's `kindlegen` had not finished compiling it when this was published. See [Building the Kindle files](#building-the-kindle-files).

> **Kindle tip:** if the old v2.4 dictionary is still installed, the two appear side by side. You can delete v2.4 once you are happy with v3.0.

## What changed from v2.4

| | |
|---|---|
| Entries | 145,075 → **154,439** |
| New entries | **11,493**, covering modern vocabulary (internet, smartphone, podcast…), science, medicine, business, everyday phrasal verbs, idioms and slang |
| Core definitions rewritten | **7,016** of the most frequent words: most common sense first, senses grouped by part of speech, wrong equivalents removed |
| Existing definitions improved or extended | **2,571** entries. Along the way, 2,224 modern senses were added and 535 very short definitions replaced |
| Orthography normalised | **106,983** entries: Persian ی/ک, restored آ, half-spaces (می‌, ‌ها, ‌ترین), tanvin, ezafe marks, quotation marks |
| Misspelled headwords corrected | 3,120 headwords (4,081 fixes), e.g. *illustrous → illustrious* |
| Duplicates merged | 2,128 |
| Garbled headwords cleaned | 97 |
| Cross-references resolved | 85 |
| Inflected forms indexed | 31,227, so looking up *walked* opens *walk* |
| Corrupted numbers fixed | e.g. «¹¹6» → 600 |
| Unchanged | 26,376 |

### Entries by subject section

| Section | v2.4 | v3.0 |
|---|---:|---:|
| General | 103,231 | 102,405 |
| Engineering | 6,909 | 7,110 |
| Computing | 3,632 | 5,395 |
| Business & economics | 3,161 | 4,327 |
| Chemistry | 3,688 | 4,010 |
| Law | 3,713 | 4,000 |
| Medicine | 654 | 1,616 |
| Geography | 15 | 1,210 |
| Informal & slang | 79 | 1,045 |
| Biology | 517 | 996 |
| Politics *(new)* | – | 580 |
| Food *(new)* | – | 537 |
| Abbreviations *(new)* | – | 275 |
| Religion *(new)* | – | 165 |

An entry with senses in several sections is counted in each. The [report](docs/index.html) has the full table, including smaller sections.

## Entry format
- `[n.]`, `[v.]`, `[adj.]` … part of speech.
- `[رایانه]`, `[پزشکی]`, `[حقوق]` … subject section.
- `▪` separates sense groups (plain-text builds use `|`), `،` separates equivalents, `؛` separates distinct senses.
- `(= colour)` is a cross-reference; `(گذشتهٔ go)`, `(جمعِ child)` mark irregular forms.

## Known limits
Please read these before relying on the dictionary for anything important.

- **Not verified on every device.** Both builds are checked by software: the Kindle `.mobi` was compiled with Amazon's kindlegen and read back to confirm all 154,439 headwords; StarDict and Kobo look-ups were resolved programmatically. Nothing has been checked screen by screen on each e-reader generation. Please [open an issue](../../issues) if something displays wrongly, with the device model and firmware.
- **No human Persian editor has reviewed the new wording.** The 7,016 rewrites and the 11,493 new entries were written by AI language models following the guidelines in [`pipeline/guidelines`](pipeline/guidelines). A few newly coined terms (for example *mansplaining*) have descriptive glosses rather than an established Persian equivalent.
- **About 107,000 specialised entries received mechanical repairs only.** Their wording is still the 1990s original, including some run-together words such as «دورازمحور», which cannot be split safely by rule.
- **Typo correction was limited** to headwords within one edit of a known English word. Further-off misspellings and wrong words that are valid English remain.
- **No PocketBook `.dic` build.** Use KOReader with the StarDict files on PocketBook.

## Building the Kindle files
The compiled classic `.mobi` is in `dist/kindle`. To rebuild it, or to try the right-to-left variant (`kindle-rtl-src`, untested on devices), generate the Kindle sources with the pipeline (see [pipeline/README.md](pipeline/README.md)), then compile with Amazon's `kindlegen`, which ships inside [Kindle Previewer](https://kdp.amazon.com/en_US/help/topic/G202131170):

```bash
kindlegen dict.opf -c1 -dont_append_source -o English-Persian.Dictionary.v3.0.mobi
```

## Repository layout

```
dist/       ready-to-install files: Kindle, Kobo, StarDict
data/       master TSV (every entry) and changelog.tsv (v2.4 vs v3.0 for each change)
docs/       change report (index.html)
pipeline/   scripts and editorial data used to produce this revision
```

## Contributing
Corrections are welcome. For a wrong or awkward translation, open an issue with the headword, the current definition and your suggested one. Fixes that follow the conventions above can be sent as pull requests against `data/English-Persian.v3.0.tsv` (the pipeline's inputs live under `pipeline/`).

## Licence
[MIT](LICENSE), the same licence as the upstream project. The copyright notice of the original project is retained.
See [CREDITS.md](CREDITS.md) for the provenance of the word list.

---

## فارسی

**فرهنگ لغت انگلیسی به فارسی، نسخهٔ ۳٫۰ — ۱۵۴٬۴۳۹ مدخل** برای کیندل، کوبو، KOReader، اونیکس بوکس، پاکت‌بوک (با KOReader) و همهٔ برنامه‌های StarDict.

این پروژه بازنگری و گسترش **نسخهٔ ۲٫۴ فرهنگ انگلیسی به فارسی** (ح. یزدانی) است که [hossein1376 در گیت‌هاب](https://github.com/hossein1376/English-Persian-Kindle-Custom-Dictionary) منتشر کرده است. سپاس ویژه از ایشان.

### نصب
- **کیندل:** فایل `dist/kindle/English-Persian.Dictionary.v3.0-classic.mobi` را در پوشهٔ `documents/dictionaries/` کیندل بریزید. در تنظیمات، بخش «زبان و لغت‌نامه»، آن را به عنوان واژه‌نامهٔ انگلیسی انتخاب کنید.
- **کوبو:** فایل `dist/kobo/dicthtml-en-fa.zip` را در `.kobo/custom-dict/` بریزید.
- **KOReader و بقیهٔ برنامه‌ها:** فایل `English-Persian-v3.0-stardict.zip` را در پوشهٔ واژه‌نامه‌ها (`koreader/data/dict/`) باز کنید.

### چه چیزی تغییر کرده
- حدود **۱۱٬۵۰۰ مدخل تازه**: اینترنت، گوشی هوشمند، پادکست، فعل‌های عبارتی، اصطلاحات و واژه‌های علمی و پزشکی جدید
- بازنویسی **۷٬۰۱۶ واژهٔ پرکاربرد** با ترتیب معنای رایج‌تر در ابتدا
- یکدست‌سازی املا: «ی» و «ک» فارسی، «آ»، نیم‌فاصله‌ها، تنوین
- اصلاح **۳٬۱۲۰ غلط املایی** در سرواژه‌ها، ادغام ۲٬۱۲۸ مدخل تکراری
- جست‌وجوی شکل‌های صرفی (مثلاً *walked* به *walk* می‌رسد)

### محدودیت‌ها
معنی‌های تازه و بازنویسی‌شده را مدل‌های هوش مصنوعی نوشته‌اند و هنوز ویراستار انسانی آن‌ها را بررسی نکرده است. حدود ۱۰۷ هزار مدخل تخصصی فقط اصلاح ظاهری شده‌اند و متن اصلی دههٔ ۷۰ را دارند. اگر مشکل یا ترجمهٔ بهتری دیدید، لطفاً [یک issue باز کنید](../../issues).
