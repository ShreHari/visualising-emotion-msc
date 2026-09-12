# Visualising Emotion — MSc Artificial Intelligence dissertation

*Visualising Emotion: A Similarity-Based Analysis of Emotional Fidelity in Text-to-Image Generation*
Shre Hari Prem Anandh · University of Sheffield, School of Computer Science · Supervisor: Dr Chaona Chen

Measuring **agreement** between the emotion recovered from a person's written self-report and the
emotion recovered from the AI-generated line drawing made from it, always against chance.

## Folder layout

| Folder | What it is |
|---|---|
| **`report/`** | **The dissertation.** LaTeX source (`myReport.tex`, `chapters/`), generated tables and numbers (`generated/`), and the built `myReport.pdf` |
| **`emoviz/`** | **The code.** Pipeline, analyses, audits, tests, demonstrator, and every result file and figure the dissertation uses (`emoviz/outputs/`) |
| `02AI_drawing_data/` | The dataset. The code reads it from here. Never uploaded (see below) |
| `university_guidelines/` | The rules: marking criteria, project specification, dissertation template, lecture slides, university guidance |
| `project_notes/` | Everything else: supervision meetings, the 4 September presentation, viva preparation, plain-English explainers, the literature library, dated drafts, and an archive of superseded files |

Inside `project_notes/`:

| Subfolder | Contents |
|---|---|
| `meetings/` | Supervision briefs and notes (17 Jul, 29 Jul, 20 Aug, 10 Sep) |
| `presentation/` | The presented deck, earlier versions, the spoken script, the deck's source code and design prompts |
| `viva_preparation/` | Project A–Z, viva question bank, revision sheet, self-review, significance addendum, mock viva |
| `explainers/` | `PROJECT_EXPLAINED.pdf`, the technical report, and their LaTeX sources |
| `literature/` | The screened library: 97 read, 73 retained, 8 themes; annotated bibliography, filtering log, research gap, `references.bib` |
| `drafts/` | Dated snapshots (9 Sep dissertation draft; an ethics application that was not submitted) |
| `archive/` | Superseded dashboards, v1-era outputs, old run logs, and pre-redaction backups (never tracked) |

## Running it

```bash
bash emoviz/setup.sh          # one-time environment
bash emoviz/test.sh           # 38 smoke checks + 54 pinned numbers
bash emoviz/run_interface.sh  # the demonstrator on :5050
```

Building the dissertation (from `report/`):

```bash
../emoviz/.venv/bin/python ../emoviz/export_tex.py      # numbers and tables from the result files
../emoviz/.venv/bin/python ../emoviz/make_figures.py    # figures
pdflatex myReport && bibtex myReport && pdflatex myReport && pdflatex myReport
```

## What is deliberately NOT in the repository

- **`02AI_drawing_data/`** — festival visitors' own words, including records with real names that
  are redacted at load time rather than on disk.
- **`project_notes/literature/` PDFs** — copyrighted; the bibliography and notes are tracked instead.
- **`emoviz/private/`** — the reviewed name-redaction decision table. It names the tokens it redacts,
  so it travels with the dataset, never with the repository.
- **`emoviz/.venv/`** — regenerate with `bash emoviz/setup.sh`.

> **This repository stays private.** Its history predates the move of the decision table out of the
> source, and the corpus is personal data from a public-engagement event.
