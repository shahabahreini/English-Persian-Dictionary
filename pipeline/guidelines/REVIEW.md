# Reviewing existing entries of the English→Persian dictionary (v3.0 revision)

Input file: TAB-separated `headword<TAB>current definition`. These are the most frequently looked-up
English words. The current definitions come from an old dictionary: they are long unordered synonym dumps,
often open with a rare or technical sense, contain glued words (`دورازمحور`, `سحراسا`), dated spellings,
occasional wrong or truncated equivalents, and lack modern senses. ` ▪ ` separates sense groups; labels in
square brackets are either a part of speech (`[n.]`, `[vt.]`) or a subject field (`[رایانه]`, `[حقوق]`, `[ورزش]` …);
labels in parentheses such as `(پزشکی)` or `(حقوق)` mark the field of the equivalent that follows.

## Your job: rewrite EVERY entry as a professional lexicographer would
Output file: one line per input line, same order, exactly `headword<TAB>new definition`.

Rules for the new definition:
1. Put the most common, core meanings FIRST (an e-reader popup shows only the first line or two).
2. Group by part of speech when the word has more than one, using labels `[n.]`, `[v.]`, `[adj.]`, `[adv.]`,
   `[prep.]`, `[conj.]`, `[pron.]`, `[interj.]`, `[det.]`, and separate the groups with ` ▪ ` (space, U+25AA, space).
   Within a group separate equivalents with `، ` and clearly distinct senses with `؛ `.
3. KEEP every valid equivalent and every specialised/technical sense from the current entry — do not lose
   information — but delete duplicates, near-duplicate spelling variants, garbage and wrong equivalents, and fix
   truncated ones. Keep specialised senses after the general ones, each introduced by its field label in
   parentheses, e.g. `(حقوق) …`, `(رایانه) …`, `(ورزش) …`, `(نظامی) …`, `(پزشکی) …`.
4. ADD important meanings that are missing, especially the main everyday sense and modern senses.
5. Modern standard Persian orthography: ی/ک (never ي ى ك), آ where required, correct ZWNJ (می‌شود، خانه‌ای،
   بی‌نظیر، کتاب‌ها), separate glued words, `هٔ` for the ezafe after silent ه only where it helps. No Latin
   transliteration; an English cross-reference such as `(= colour)` may stay.
6. No TAB inside the definition; one line per entry; no commentary.
7. For irregular inflected forms (e.g. `went`, `children`) start with e.g. `(گذشتهٔ go)` or `(جمعِ child)`.

Example
  in : `tension	قوره کشش، زور، کشش، امتداد، تمدد، قوه انبساط، سفتی، بحران، تحت فشار قرار دادن، تنش، کشمکش، قدرت`
  out: `tension	[n.] تنش، کشش، فشار؛ کشمکش، بحران، تشنج (در روابط)؛ اضطراب، فشار عصبی؛ سفتی، کشیدگی؛ (فیزیک) نیروی کشش؛ (برق) ولتاژ ▪ [v.] کشیدن، تحت کشش یا فشار قرار دادن`
