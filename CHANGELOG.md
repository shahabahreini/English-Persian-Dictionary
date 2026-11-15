# Changelog

## 3.1.0 (2026-11-14)
[Release v3.1.0](https://github.com/shahabahreini/English-Persian-Dictionary/releases/tag/v3.1.0). Subject expansion. See [docs/report.html](docs/report.html) for the report and [data/changelog.tsv](data/changelog.tsv) for the per-entry changes (entries marked `subject-sense-added` or `new-entry` with a v3.1 section).

- 164,524 entries (v3.0: 154,439): 10,085 new entries and 3,589 subject senses added to existing entries.
- Twelve new subject sections: Philosophy & logic, Earth & environmental sciences, Statistics, Arts, Literature, History & archaeology, Sociology & anthropology, Education, Agriculture & veterinary science, Transport & logistics, Media & communication, Fashion & textiles.
- Deeper coverage in Informal & slang (1,045 → 2,514), Mathematics, Physics, Astronomy, Psychology, Linguistics, Music, Architecture, Civil engineering and Sports, plus about 1,800 everyday compounds, idioms, phrasal verbs and proverbs.
- On an existing word the subject sense is appended after the current definition; no v3.0 definition was removed or reworded.
- Pipeline: v3.1 inputs live in `pipeline/new/v3.1/` and are read in a separate pass after the v3.0 inputs; `scripts/lint31.py` checks them; the Kindle sources are split into several content files so kindlegen does not stall on the larger dictionary; `export.py` now also writes the master TSV.
- Fixed 94 entries where a subject code such as `slang|` or `psychology|` was printed at the start of a sense (e.g. *gaslighting*, *chill out*, *lol*). The code came from 122 malformed lines in a v3.0 input (`pipeline/new/theme_everyday.tsv`); it is now the entry's section label. `build.py` counts any recurrence as `def_code_prefix` and `lint31.py` rejects it.
- Kindle metadata now reads "Revision and expansion of v2.4" instead of naming v3.0.
- Files renamed from `v3.0` to `v3.1`.

## 3.0.0
Revision and expansion of English-Persian Dictionary v2.4. See [docs/report.html](docs/report.html) for the full before/after report and [data/changelog.tsv](data/changelog.tsv) for the per-entry changes.

- 154,439 entries (v2.4: 145,075); 11,493 new entries; 31,227 inflected forms indexed.
- 7,016 high-frequency definitions rewritten; 2,571 more improved or extended; 2,224 modern senses added.
- Persian orthography normalised in 106,983 entries; 3,120 misspelled headwords corrected; 2,128 duplicates merged; 97 garbled headwords cleaned.
- New subject sections: Politics, Food, Abbreviations, Religion. Large growth in Computing, Business, Medicine, Geography and Informal & slang.
- New builds: Kindle `.mobi` (classic and right-to-left), Kobo `dicthtml`, StarDict (HTML and plain text).
- Project site (English and Persian landing pages), change report, `llms.txt`, `CITATION.cff` and issue templates.

## 2.4
Upstream release by hossein1376 (March 2022). Not part of this repository.
