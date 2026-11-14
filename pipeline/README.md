# Pipeline

Scripts and editorial data used to turn v2.4 into v3.0. Use this to audit how an entry was produced, to rebuild after you edit the inputs, or to produce another format.

Rebuilding `master.json`, `changelog.tsv` and both Kindle sources (`content.html`) from these inputs was tested and gives output identical to what ships in `dist/` and `data/`.

## What is here

| Path | Contents |
|---|---|
| `scripts/unpack.py`, `scripts/mkv24.py` | Read the original v2.4 `.mobi` and turn it into `unpacked/v24.tsv` (headword, definition in reading order) |
| `scripts/fanorm.py` | Persian orthography normalisation (letters, آ, half-spaces, tanvin, numbers, quotes) |
| `scripts/build.py` | Applies typo fixes, merges duplicates, resolves cross-references, applies rewrites and additions, indexes inflected forms. Writes `master.json`, `changelog.tsv` |
| `scripts/export.py` | Writes the tab files and the Kindle sources (classic and RTL) |
| `scripts/glos.py` | StarDict and Kobo writers (via pyglossary) |
| `scripts/verify.py`, `scripts/chk_mobi.py` | Read-back checks. `verify.py` expects the author's output layout (`<dest>/StarDict/English-Persian-v3.0/`, `<dest>/Kobo/`) and needs `idzip`; `chk_mobi.py` (run with `calibre-debug scripts/chk_mobi.py -- file.mobi`) counts headwords in a compiled `.mobi` |
| `scripts/report.py` | Generates the change report (`docs/index.html`) |
| `scripts/gap.py`, `typocand.py`, `slices.py`, `revprep.py`, `salvage.py` | Helpers that found missing words and typo candidates and prepared and merged the AI-written batches |
| `new/` | New entries (`gap_*`, `manual_a`) and modern senses added to existing entries (`theme_*`) |
| `review/merged/` | Rewritten definitions for the 7,016 most frequent words |
| `typo/` | Headword spelling fixes (`fix_*.tsv`) and the candidate lists they came from |
| `report/` | Report template and the static text (device table, limits) |
| `guidelines/` | The written specs given to the AI writers (`SPEC.md` for new entries, `REVIEW.md` for rewrites) |

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
DICT_REF="$PWD/ref" python3 scripts/build.py "$PWD"                  # master.json, changelog.tsv

# 4. Export
python3 scripts/export.py "$PWD" "$PWD/out" 3.0                     # tab files + Kindle sources
```

### StarDict and Kobo
```bash
pip install pyglossary marisa-trie
python3 scripts/glos.py out/en-fa.html.tabfile.txt out/sd/English-Persian-v3.0.ifo Stardict          # HTML definitions
python3 scripts/glos.py out/en-fa.tabfile.txt out/sd-plain/English-Persian-v3.0-plaintext.ifo StardictPlain
python3 scripts/glos.py out/en-fa.kobo.tabfile.txt out/dicthtml-en-fa.zip Kobo
```
Use `en-fa.kobo.tabfile.txt` for Kobo: it lists alternate forms with a different first two letters as separate entries, which the Kobo writer otherwise turns into look-ups that cannot be found.

### Compile the Kindle dictionary
```bash
cd out/kindle-classic-src      # or kindle-rtl-src
kindlegen dict.opf -c1 -dont_append_source -o English-Persian.Dictionary.v3.0.mobi
```
`kindlegen` is inside Kindle Previewer, for example `/Applications/Kindle Previewer 4.app/Contents/Resources/KFXGen/bin/kindlegen` on macOS. Exit code 1 with "built with WARNINGS" (no cover image) is normal.

## Editing entries
- To change a rewritten word, edit its line in `review/merged/out_*.tsv`. To change an added entry, edit `new/*.tsv`. A headword spelling fix goes in `typo/fix_*.tsv`. Then re-run steps 3 and 4.
- Persian text is stored in reading order everywhere except the classic Kindle source, which `export.py` converts to visual order.
- Keep subject labels in the form the existing files use; `build.py` maps them to Persian section names.

## Note on third-party data
`ref/` and `unpacked/` are git-ignored. The original v2.4 file and the frequency lists belong to their authors and are not redistributed here; see [CREDITS.md](../CREDITS.md).
