# Pipeline

Scripts and editorial data used to turn v2.4 into v3.0, and v3.0 into v3.1. Use this to audit how an entry was produced, to rebuild after you edit the inputs, or to produce another format.

Rebuilding `master.json`, `changelog.tsv`, the master TSV and both Kindle sources from these inputs was tested and gives output identical to what ships in `data/` and `dist/`. The v3.1 data fix corrected 122 malformed lines in `new/theme_everyday.tsv`, a v3.0 input, so v3.0 itself is reproduced from its own commit (`0015027`); the build reports any subject code left in a definition field as `def_code_prefix`, which should be absent (zero).

## What is here

| Path | Contents |
|---|---|
| `scripts/unpack.py`, `scripts/mkv24.py` | Read the original v2.4 `.mobi` and turn it into `unpacked/v24.tsv` (headword, definition in reading order) |
| `scripts/fanorm.py` | Persian orthography normalisation (letters, آ, half-spaces, tanvin, numbers, quotes) |
| `scripts/build.py` | Applies typo fixes, merges duplicates, resolves cross-references, applies rewrites and additions, indexes inflected forms. Writes `master.json`, `changelog.tsv` |
| `scripts/export.py` | Writes the tab files and the Kindle sources (classic and RTL) |
| `scripts/glos.py` | StarDict and Kobo writers (via pyglossary) |
| `scripts/verify.py`, `scripts/chk_mobi.py` | Read-back checks. `verify.py` expects the author's output layout (`<dest>/StarDict/English-Persian-v<version>/`, `<dest>/Kobo/`) and takes the version as a second argument (`verify.py <dest> 3.1`) and uses `idzip` if installed, otherwise plain gzip; `chk_mobi.py` (run with `calibre-debug scripts/chk_mobi.py -- file.mobi`) counts headwords in a compiled `.mobi` |
| `scripts/report.py`, `scripts/site.py`, `scripts/build_site.py` | Generate the change report, wrap it as `docs/report.html`, and build the English and Persian landing pages |
| `scripts/gap.py`, `typocand.py`, `slices.py`, `revprep.py`, `salvage.py` | Helpers that found missing words and typo candidates and prepared and merged the AI-written batches |
| `new/` | New entries (`gap_*`, `manual_a`) and modern senses added to existing entries (`theme_*`) for v3.0 |
| `new/v3.1/` | v3.1 subject glossaries, one file per subject (`philosophy.tsv`, `earth.tsv`, `slang.tsv`, `general_a.tsv` …). Read in a separate pass after everything else, so v3.0 results do not change |
| `scripts/lint31.py` | Checks the v3.1 files (format, domain codes, ی/ک, half-spaces, separators, duplicates) and reports whether each line is a new entry, adds a sense, or repeats what the entry already has |
| `review/merged/` | Rewritten definitions for the 7,016 most frequent words |
| `typo/` | Headword spelling fixes (`fix_*.tsv`) and the candidate lists they came from |
| `report/` | Report template and the static text (device table, limits) |
| `site/` | Project site: stylesheet, script, structured data, logos and the social preview image source |
| `guidelines/` | The written specs given to the AI writers (`SPEC.md` for new entries, with the v3.1 addendum at the end; `REVIEW.md` for rewrites) |

## Rebuild

Requirements: Python 3.9+, [calibre](https://calibre-ebook.com) (for `calibre-debug`, only to unpack the original), and for StarDict/Kobo: `pip install pyglossary marisa-trie`.

Run everything from this `pipeline/` directory (the scripts take it as their working directory).

```bash
# 1. Get the inputs that are not redistributed here
#    - the original v2.4 .mobi from the upstream repo:
#      https://github.com/hossein1376/English-Persian-Kindle-Custom-Dictionary
#    - Persian word frequencies (fa_full.txt) from hermitdave/FrequencyWords
#    - English word counts (count_1w.txt) from https://norvig.com/ngrams/
mkdir -p ref unpacked
cp /path/to/fa_full.txt /path/to/count_1w.txt ref/

# 2. Unpack v2.4
calibre-debug scripts/unpack.py -- "English-Persian Dictionary v2.4.mobi" unpacked/raw.html
python3 scripts/mkv24.py unpacked/raw.html unpacked/v24.tsv        # 145075 entries

# 3. Build the master data
DICT_VER=v3.1 DICT_REF="$PWD/ref" python3 scripts/build.py "$PWD"     # master.json, changelog.tsv (DICT_VER labels the changelog column)

# 4. Export
python3 scripts/export.py "$PWD" "$PWD/out" 3.1                     # master TSV, tab files, Kindle sources
```

### StarDict and Kobo
```bash
pip install pyglossary marisa-trie python-idzip   # python-idzip gives the .dict.dz compression
mkdir -p out/sd/English-Persian-v3.1 out/sd-plain/English-Persian-v3.1-plaintext
python3 scripts/glos.py out/en-fa.html.tabfile.txt out/sd/English-Persian-v3.1/English-Persian-v3.1.ifo Stardict          # HTML definitions
python3 scripts/glos.py out/en-fa.tabfile.txt out/sd-plain/English-Persian-v3.1-plaintext/English-Persian-v3.1-plaintext.ifo StardictPlain
python3 scripts/glos.py out/en-fa.kobo.tabfile.txt out/dicthtml-en-fa.zip Kobo
```
Use `en-fa.kobo.tabfile.txt` for Kobo: it lists alternate forms with a different first two letters as separate entries, which the Kobo writer otherwise turns into look-ups that cannot be found.

### Change report and site
```bash
python3 scripts/report.py "$PWD"                                     # report fragment: report/dictionary-v3-report.html
python3 scripts/site.py report/dictionary-v3-report.html ../docs/report.html   # wrap it as a complete, indexable page
```
The landing pages (`docs/index.html`, `docs/fa/index.html`) are generated, not hand-edited: run `python3 pipeline/scripts/build_site.py` from the repository root. Copy lives in that script (English and Persian side by side), styling in `site/site.css`, behaviour in `site/site.js`, structured data in `site/jsonld-*.json`, and file sizes are read from `dist/` and `data/`, so rebuild after changing any of them. The FAQ on each page is built from its `FAQPage` JSON-LD so the visible text and the markup cannot drift apart. Logo sources and licences are in `site/logos/README.md`. `site/og-image.html` is the source of the social preview images: `docs/assets/github-social-preview.png` (1280×640, uploaded by hand under the repo's Settings › Social preview) and `docs/assets/og-image.png` (1200×630, used by the pages' Open Graph tags). Render it at those sizes with a headless browser, e.g. Chrome with `--window-size=1280,640 --virtual-time-budget=8000 --screenshot=…` so the web fonts finish loading.

### Compile the Kindle dictionary
```bash
cd out/kindle-classic-src      # or kindle-rtl-src
kindlegen dict.opf -c1 -dont_append_source -o English-Persian.Dictionary.v3.1.mobi
```
`kindlegen` is inside Kindle Previewer, for example `/Applications/Kindle Previewer 4.app/Contents/Resources/KFXGen/bin/kindlegen` on macOS. Exit code 1 with "built with WARNINGS" (no cover image) is normal.

**Size limit:** kindlegen stalls at 0% CPU, with no error, when a single source HTML file is much over about 40 MB (a 42.8 MB test file never got past "Parsing files"). `export.py` therefore writes the Kindle sources as several files of 40,000 entries each (`content0.html` …), listed in `dict.opf`; v3.1 compiles in about 35 seconds per build and keeps all headwords. It also writes `<p dir="rtl">` only, without `align="right"`, to keep the sources small.

## Editing entries
- To change a v3.1 subject entry, edit its line in `new/v3.1/<subject>.tsv`, run `python3 scripts/lint31.py new/v3.1/*.tsv` (it must report 0 errors), then re-run steps 3 and 4.
- To change a rewritten word, edit its line in `review/merged/out_*.tsv`. To change an added entry, edit `new/*.tsv`. A headword spelling fix goes in `typo/fix_*.tsv`. Then re-run steps 3 and 4.
- Persian text is stored in reading order everywhere except the classic Kindle source, which `export.py` converts to visual order.
- Keep subject labels in the form the existing files use; `build.py` maps them to Persian section names.

## Note on third-party data
`ref/` and `unpacked/` are git-ignored. The original v2.4 file and the frequency lists belong to their authors and are not redistributed here; see [CREDITS.md](../CREDITS.md).
