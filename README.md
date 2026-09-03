# Visualising Emotion — MSc Artificial Intelligence dissertation

Measuring **agreement** between the emotion recovered from a person's written self-report and the
emotion recovered from the AI-generated line drawing produced from it.

University of Sheffield, School of Computer Science · Supervisor: Dr Chaona Chen

## What is here

| Path | Contents |
|---|---|
| `emoviz/` | the analysis pipeline, the live demo app, and the test suite (29 checks) |
| `emoviz/outputs/` | all analysis results, the per-record tables, and the report figures |
| `final/` | the A–Z project explanation, viva question bank, revision sheet, dissertation review |
| `deck/` | presentation source (pptxgenjs) |
| `report/` | the dissertation LaTeX source |
| `RESEARCH PAPERS/references.bib` | the 74-entry bibliography |

## What is deliberately NOT here

- **`02AI_drawing_data/`** — the source corpus. It contains festival visitors' own words, including
  records with real names that are redacted at *load* time rather than on disk. It is not uploaded.
- **`RESEARCH PAPERS/lit/`** — 97 copyrighted PDFs. The bibliography is tracked instead.
- **`emoviz/.venv/`** — regenerate with `bash emoviz/setup.sh`.

> **This repository must remain private.** `emoviz/preprocess_names.py` contains the reviewed
> redaction table, which by its nature names the tokens it redacts.

## Running it

```bash
bash emoviz/setup.sh          # one-time environment
bash emoviz/test.sh           # 29 checks
bash emoviz/run_interface.sh  # the demo app on :5050
```
The analysis scripts need `02AI_drawing_data/` present alongside this repository.
