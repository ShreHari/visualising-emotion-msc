# dissertation/ — the write-up (self-contained Overleaf project)

This folder is the dissertation. Everything it needs is inside it, so it can be zipped and
uploaded to Overleaf as one project.

```
main.tex                the document (School template, extra packages, the placeholder command)
chapters/               abstract, glossary, chapters 1–6, appendices A–C
generated/              numbers.tex (673 macros) and tab_*.tex tables, GENERATED, never edited by hand
figures/                every figure (PDF/PNG) plus the TikZ pipeline diagram
images/                 the University logo for the title page
mybibliography.bib      the 91 references
sync_generated.sh       refreshes generated/ and figures/ from the analysis (run after any analysis change)
FIGURES_TO_ADD.md       the images still to be captured by hand, with instructions
build_notes/            the writing contract and the checkers used to produce the text (not part of the PDF)
```

## Building

Overleaf: New Project, Upload Project, choose a zip of this folder, set `main.tex` as the main
document, compiler pdfLaTeX. It compiles with the defaults (three passes and BibTeX happen
automatically).

Locally (TeX Live):

```bash
cd dissertation
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Refreshing the numbers

Every statistic in the text is a macro from `generated/numbers.tex`; every table is a file in
`generated/`. Both are produced by `emoviz/export_tex.py` from the JSON result files. After any
change to the analysis (for example after scoring the single-coder check), run

```bash
bash dissertation/sync_generated.sh
```

and rebuild. The text does not need editing, except the pending paragraph in the single-coder
section of Chapter 4 once that check is scored.

## Checks used while writing

`build_notes/check_tex.py <chapter.tex>` reports sentence-rhythm statistics, banned phrases,
undefined macros, unknown citation keys, undefined references and hand-typed numbers.
`build_notes/copy_check.py <chapter.tex>` reports runs of eight or more words shared verbatim with
the earlier draft or any project note. Both were run on every chapter before the text was accepted.
