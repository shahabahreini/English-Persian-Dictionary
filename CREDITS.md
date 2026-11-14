# Credits and provenance

## Upstream dictionary
This project would not exist without the work below.

- **[hossein1376/English-Persian-Kindle-Custom-Dictionary](https://github.com/hossein1376/English-Persian-Kindle-Custom-Dictionary)** (MIT, © 2022 hossein1376). The v2.4 Kindle dictionary (March 2022) is the starting point for every entry here: about 145,000 words and phrases, with inflection data and the idea of storing Persian in visual order for Kindle pop-ups, credited upstream to Mohammad-Ali Afshar. Thank you for publishing it freely together with its source files and a guide.
- **H. Yazdani**, the compiler credited in the v2.4 file's metadata.
- **MHM Advance English-Persian Dictionary**: according to the upstream README, the original database of v2.4 comes from this freely available dictionary. Its own licence terms are not known to this project. If you hold rights to it and want something changed, please open an issue.

## What this revision adds
Revision, expansion and packaging by [shahabahreini](https://github.com/shahabahreini): the new and rewritten entries, Persian orthography normalisation, headword repairs, extra sections, the StarDict, Kobo and Kindle builds, and the change report. The new and rewritten wording was produced with AI language models (Claude, by Anthropic) acting as lexicographers under the written guidelines in [`pipeline/guidelines`](pipeline/guidelines), and has not been reviewed by a human Persian editor.

## Reference data used while building
Used as lookup references only and **not redistributed** here:

- [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords): English and Persian word-frequency lists, used to decide which missing words to add, and as a lexicon for restoring Persian letters and half-spaces.
- Peter Norvig's [English word counts](https://norvig.com/ngrams/) (`count_1w.txt`): used to recognise real inflected forms.

## Tools
[calibre](https://calibre-ebook.com) (reading the original MOBI), [pyglossary](https://github.com/ilius/pyglossary) (StarDict and Kobo writers), [marisa-trie](https://github.com/pytries/marisa-trie), and Amazon's `kindlegen` from Kindle Previewer (Kindle `.mobi` compilation).

## Licence
Everything in this repository is released under the [MIT licence](LICENSE), which carries forward the upstream copyright notice.
