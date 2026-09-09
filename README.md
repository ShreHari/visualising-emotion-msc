# Visualising Emotion — MSc Artificial Intelligence dissertation

Measuring **agreement** between the emotion recovered from a person's written self-report and the
emotion recovered from the AI-generated line drawing produced from it.

University of Sheffield, School of Computer Science · Supervisor: Dr Chaona Chen

## What is here

| Path | Contents |
|---|---|
| `emoviz/` | the analysis pipeline, the live demo app, the audits and ablation, and the two-layer test suite (38 checks + 54 pinned numbers) |
| `emoviz/outputs/` | all analysis results, the per-record tables, and the report figures |
| `final/` | the A–Z project explanation, viva question bank, revision sheet, dissertation review |
| `deck/` | presentation source (pptxgenjs) |
| `report/` | the dissertation LaTeX source |
| `RESEARCH PAPERS/references.bib` | the 91-entry bibliography (73 retained papers + method references) |

## What is deliberately NOT here

- **`02AI_drawing_data/`** — the source corpus. It contains festival visitors' own words, including
  records with real names that are redacted at *load* time rather than on disk. It is not uploaded.
- **`RESEARCH PAPERS/lit/`** — the 97 screened PDFs (89 under `lit/`, 8 at the folder root). They are copyrighted; the bibliography is tracked instead.
- **`emoviz/.venv/`** — regenerate with `bash emoviz/setup.sh`.

- **`emoviz/private/`** — the reviewed name-redaction decision table. It names the tokens it
  redacts, so it travels with the dataset, never with the repository. `preprocess_names.py`
  loads it at run time and stops with a clear message if it is absent.

> **This repository stays private.** Its history predates the move of the decision table out of
> the source, and the corpus is personal data from a public-engagement event.

## Running it

```bash
bash emoviz/setup.sh          # one-time environment
bash emoviz/test.sh           # 38 checks + 54 pinned numbers
bash emoviz/run_interface.sh  # the demo app on :5050
```
The analysis scripts need `02AI_drawing_data/` present alongside this repository.
