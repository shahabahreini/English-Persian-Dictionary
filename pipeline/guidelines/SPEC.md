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

---

# v3.1 subject expansion (addendum)

Files go in `new/v3.1/<code>.tsv`, same 3-field format as above. `build.py` reads them in a separate pass after
all v3.0 inputs, so v3.0 results do not change.

## Additional domain codes (v3.1)
| code | Persian section | covers |
|---|---|---|
| `philosophy` | فلسفه و منطق | logic, epistemology, metaphysics, ethics, aesthetics, philosophy of mind/science/language, political philosophy, schools and -isms, Islamic philosophy |
| `earth` | علوم زمین و محیط زیست | geology, mineralogy, volcanology, seismology, meteorology, climate, oceanography, hydrology, soils, ecology, conservation, pollution |
| `statistics` | آمار | descriptive statistics, probability distributions, inference, sampling, regression, experimental design |
| `arts` | هنر | painting, drawing, sculpture, printmaking, photography, art history and movements, theatre and stagecraft, film and cinema, dance, crafts |
| `literature` | ادبیات | genres, forms, prosody and metre, rhetoric and figures of speech, narrative theory, criticism, publishing of literature |
| `history` | تاریخ و باستان‌شناسی | historical periods, institutions and events as common nouns, historiography, archaeology, material culture |
| `sociology` | جامعه‌شناسی و مردم‌شناسی | social structure, stratification, institutions, kinship, culture, ritual, migration, demography, urban sociology |
| `education` | آموزش | teaching, pedagogy, curriculum, assessment, school and university systems, degrees, academic life |
| `agriculture` | کشاورزی و دامپزشکی | farming, crops, soils, irrigation, horticulture, livestock, poultry, apiculture, fisheries, veterinary medicine |
| `transport` | حمل‌ونقل | automotive (car parts, driving, traffic), rail, road, logistics, freight, shipping and customs (use `aviation`/`maritime` for those fields) |
| `media` | رسانه و ارتباطات | journalism, publishing, broadcasting, advertising, public relations, social media, communication studies |
| `fashion` | پوشاک و نساجی | clothing, garment parts, sewing and tailoring, fabrics and fibres, weaving, knitting, footwear, accessories, jewellery, cosmetics |

Existing codes keep their scope (`math`, `physics`, `astronomy`, `psychology`, `linguistics`, `music`, `architecture`, `civil`, `sports`, `aviation`, `maritime`, `slang`, `general`).

## Existing headwords
Check every headword against the current dictionary, `data/English-Persian.v3.1.tsv` (or run `python3 scripts/lint31.py <file>`).
- New headword: write the full entry, most common sense first.
- Existing headword: write **only the subject sense the entry lacks** (e.g. `fault	earth	گسل`). The build appends it
  after the current definition under the subject label and drops equivalents the entry already has. If the
  current entry already gives the subject sense, leave the word out.

## Terminology standard
- Use the term an Iranian university textbook or a specialist writing in Persian today would use:
  معرفت‌شناسی، هستی‌شناسی، پدیدارشناسی، وظیفه‌گرایی، سنگ رسوبی، زمین‌ساخت ورقه‌ای، آبخوان، بازهٔ اطمینان، میزانسن،
  تناوب زراعی، بارنامه. If two terms are both current, give both, the more common first.
- Academy (فرهنگستان) coinages only where they are actually used. Iranian Persian, not Dari or Tajik usage.
- Islamic-philosophical equivalents where they are the established ones (ماهیت، وجود، جوهر، عرض، علت فاعلی).
- Loan terms where those are what people say (امپرسیونیسم، کوبیسم، رئالیسم), with a Persian gloss if helpful.
- Multiword English terms are welcome and are often what is missing (`crop rotation`, `mise en scene`, `a priori`).

## Slang and informal English
- Give the Persian **colloquial** equivalent a speaker would really use, not a literal or dictionary gloss
  (`sus	slang	(عامیانه) مشکوک، مشکوکی، بودار`). Add a short gloss in parentheses when there is no close equivalent.
- Register label first: `(عامیانه)`, `(عامیانه، اینترنتی)`, `(رکیک)`, `(عامیانهٔ بریتانیایی)`, `(عامیانهٔ آمریکایی)`, `(قدیمی)`.
- Idioms and phrasal verbs that are not slang take `general` and no register label unless informal.
