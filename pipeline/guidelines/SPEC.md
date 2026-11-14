# English→Persian dictionary: entry-writing spec (v3.0 expansion)

You are writing entries for a serious English→Persian (Farsi) dictionary used on e-readers.
Quality bar: a professional bilingual lexicographer. Accuracy matters more than volume, but be thorough.

## Output file format (strict)
UTF-8 text, one entry per line, exactly 3 TAB-separated fields, no header, no blank lines, no quotes:

    headword<TAB>domain<TAB>definition

- headword: lowercase English (even proper nouns and acronyms, e.g. `usb`, `france`), no trailing punctuation.
- domain: exactly one code from this list:
  general, computing, electronics, engineering, medicine, biology, chemistry, physics, math, law,
  business, military, aviation, maritime, architecture, civil, sports, botany, zoology, astronomy,
  anatomy, psychology, music, geography, politics, religion, linguistics, food, slang, abbr
  (use `business` for economics/finance/commerce; `geography` for countries, nationalities, cities, regions;
  `abbr` for abbreviations/acronyms that have no better domain; `slang` for informal/colloquial/vulgar words.)
- definition: Persian equivalents separated by `، ` (Persian comma + space), most common/current first,
  typically 1–5 equivalents. Where a bare equivalent would be unclear, add a short explanatory gloss in
  parentheses. For abbreviations give the English expansion first, then the Persian, e.g.
  `usb	computing	Universal Serial Bus؛ یواس‌بی، درگاه همه‌گذر سریال`.
  For words with clearly different senses, separate senses with `؛ `.
  For slang/vulgar words add a register label like `(عامیانه)` or `(رکیک)`.
  For irregular inflected forms (e.g. `women`, `taken`, `went`) write e.g. `(جمعِ woman) زنان` or
  `(اسم مفعولِ take) گرفته، برده`.

## Persian orthography (mandatory)
- Persian letters only: ی and ک (never Arabic ي ى ك).
- Write آ where required (آب، آزمایش، درآمد).
- Use ZWNJ (U+200C, نیم‌فاصله) properly: می‌شود، کتاب‌ها، خانه‌ای، بی‌سیم، نرم‌افزار.
- Use the equivalents actually used by educated Iranian speakers today. Give the established loanword
  when that is what people say (اینترنت، ایمیل، وبلاگ) and also the Academy (فرهنگستان) coinage when it has
  real currency (رایانامه، تارنما، رایانه). Do not invent coinages.
- No Latin transliteration of Persian, no pronunciation guides, no TAB characters inside fields.

## What NOT to include
- Personal first names and surnames, company/brand/product names (exception: a brand name that has become
  a generic word or is essential tech vocabulary), random web junk, misspellings, non-English words,
  porn-site jargon. Ordinary slang and common vulgar words ARE allowed with a register label.
- Regular inflections (plain plurals, -ed, -ing forms) whose base form is an ordinary word.
