# Handoff — Visualising Emotion (MSc AI dissertation)

Read this first in a new session. It is the state of the project on **12 September 2026**.

## 1. The project in one paragraph

**Registered title (do not change):** *Visualising Emotion: A Similarity-Based Analysis of Emotional Fidelity in Text-to-Image Generation*
Student: Shre Hari Prem Anandh · MSc Artificial Intelligence (COM6912), University of Sheffield · Supervisor: Dr Chaona Chen.

At the Festival of the Mind 2024 (Sheffield), visitors typed how they felt and DALL·E drew each entry as a monochrome line drawing: **1,025 records, 1,012 analysed** (13 pre-festival tests dropped). The project measures **agreement** between the emotion a text model reads from the words (GoEmotions, 28 labels → 7 families) and the emotion a second reader gets from the drawing (BLIP-VQA answers five factual questions → one sentence → BART-MNLI zero-shot). Agreement is scored as **similarity, not matching**, on four measures (valence–arousal similarity, valence-sign agreement, family agreement, top-3 overlap), and **every value is read against a random-pairing null** (300 shuffles, seed 7), with clustered bootstrap CIs and clustered permutation tests because 249 records repeat a prompt.

## 2. Deadline and what is left

**Submission: Wednesday 16 September 2026, 15:00.** Check the hand-in route on Blackboard / COM Projects.

| # | Task | How |
|---|---|---|
| 1 | **Code the 120 drawings** for the human check (0/120 done) | Open `emoviz/outputs/human_check/sheet_01.png` … `sheet_06.png`; fill `emoviz/outputs/human_check/labels.csv` (person y/n, face y/n, valence +/-/0, family). Then `cd emoviz && .venv/bin/python human_check.py score` |
| 2 | Refresh numbers and tables after step 1 | `cd emoviz && .venv/bin/python export_tex.py`, then rebuild the report (section 5). Replace the "coding not complete" paragraph in `report/chapters/chapter4.tex` (section "Single-coder reliability check") with the scored numbers |
| 3 | Fill two image placeholders | `report/chapters/chapter3.tex`: `\placeholder{PHOTOGRAPH OF THE FESTIVAL INSTALLATION}` (optional, delete if none) and `\placeholder{SCREENSHOT OF THE DEMONSTRATOR}` (run `bash emoviz/run_interface.sh`, pick record 63, press Compare, screenshot, put in `report/figures/`, swap the placeholder for `\includegraphics`) |
| 4 | Revise the prose in the student's own voice | The full draft is written (15,366 words; limit 10,000–20,000 excl. references and appendices). The student wants to edit and rephrase it freely, with AI help, before submission |
| 5 | Final checks | `bash emoviz/test.sh` (expect 38/38), rebuild the report, fill the Declaration page (name, signature, date), submit |

The supervision brief for 10 September is in `project_notes/meetings/MEETING_BRIEF_10Sep2026.md`. The outcome of that meeting is **not recorded** here; ask the student what Dr Chen said.

**Working with the student:** the student has said their supervisor is fine with AI assistance. Help freely with drafting, rewriting, editing and tone of the dissertation. Answer in simple English when they ask for explanations; they prefer direct answers over long tool runs.

## 3. Folder layout

| Folder | Contents |
|---|---|
| `report/` | **The dissertation.** `myReport.tex`, `chapters/` (abstract, glossary, ch1–6, appendix A–B), `generated/` (numbers + tables, never edit by hand), `figures/`, `myReport.pdf` (75 pages) |
| `emoviz/` | **The code.** Pipeline, analyses, audits, tests, demonstrator; results and figures in `emoviz/outputs/` |
| `02AI_drawing_data/` | The dataset. Code reads it from here. Never upload it |
| `university_guidelines/` | Marking criteria (html + txt), project spec, template, lectures, university guidance |
| `project_notes/` | `meetings/`, `presentation/`, `viva_preparation/`, `explainers/`, `literature/` (97 read, 73 retained, 8 themes, `references.bib`), `drafts/`, `archive/` |

GitHub: `github.com/ShreHari/visualising-emotion-msc` — **must stay private.** Never commit `02AI_drawing_data/`, `emoviz/private/` (redaction decision table, names real people), `*.prename` / `*.nodedup` backups (in `project_notes/archive/redaction_backups/`, contain real names), or the literature PDFs. `.gitignore` already covers all of these.

## 4. Numbers — the only values to quote

All come from JSON files in `emoviz/outputs/`; `emoviz/test_numeric.py` pins them. In LaTeX, **never type a number** — use the macros in `report/generated/numbers.tex` (e.g. `\FullEmoSignObs`).

| Result | Value |
|---|---|
| Emotional prompts (n=607), valence-sign | 64.0% vs null 45.6%, z +11.1, CI [58.6, 68.8] (denominator 530) |
| Emotional prompts, family | **53.0%** (322/607; never 53.1) vs 38.8%, z +10.3, CI [47.3, 58.7] |
| Face-classified (n=402) / scene-classified (n=205), valence-sign | 73.9% vs 53.5% / 42.9% vs 29.6% |
| Face − scene difference | +30.9 pp [+22.6, +40.6] sign; +26.3 pp [+18.4, +35.3] family; clustered permutation p = 0.0001 |
| Distinct prompts (763) | face sign 71.8% z +8.4; scene sign 37.3% z +3.5; scene family 30.8% z +2.6 (**fails Holm**) |
| Holm–Bonferroni | 26 of 36 non-degenerate z survive |
| Neutral-labelled prompts (n=405) | VA 76.6% vs 76.6%, z +0.3 (only informative measure); 68 contain an affect word; cleaned 335 z +0.04 |
| Like-for-like reader comparison | describe-then-extract 53.0% vs direct CLIP 22.4% family, +30.6 pp [+25.5, +35.6], cluster p < 0.001 (old 49.3 vs 25.3 is a historical v1 figure only) |
| Repeated prompts (87 groups, 336 records, 43 pairs) | 68.8% same family vs null 59.4%, z +4.5; 28/87 fully consistent vs 14.5 |
| Cohen's kappa (family) | emotional 0.23, face 0.30, scene 0.13 (fair, fair, slight) |
| Describer | 414/421 scene records report no person; 406 still name an expression; 332 say smile/smiling/happy; smiling = 57% of face-classified, 66% corpus-wide |
| Copy rate | 99.8% where the expression answer is an emotion word (41% of records) |
| Ablation | expression sentence removed: family 53.0% → 20.3%; **people-aware template: face unchanged, scene falls to null** (sign 4.7% vs 3.4%, z +1.6) |
| Error taxonomy (38 confident disagreements) | describer 19, reader 5, prompt side 12, generator 2 |

**The main finding, correctly stated:** for this reader, drawings where the describer reads a face agree far above chance; scene drawings show nothing above chance once the invented expression is removed ("faces, and only faces, for this reader").

## 5. How to run and build

```bash
cd emoviz
bash setup.sh                     # one-time environment (Python 3.12, pinned requirements)
bash test.sh                      # 38 smoke checks + test_numeric.py (54 pinned values); exits non-zero on failure
bash run_interface.sh             # demonstrator at http://127.0.0.1:5050
.venv/bin/python export_tex.py    # report/generated/ numbers + tables from the JSON
.venv/bin/python make_figures.py  # every figure, from the JSON

cd ../report
pdflatex myReport && bibtex myReport && pdflatex myReport && pdflatex myReport
```

Analysis scripts (all seeded, read cached outputs, run in seconds): `analysis_final.py`, `significance.py`, `inference.py`, `method_comparison.py`, `data_audit_consistency.py`, `audits.py`, `error_taxonomy.py`, `ablate_nli.py` (~30 min, NLI only), `human_check.py`. One definition of every measure: `emoviz/emoviz/metrics.py`.

## 6. Writing conventions for the dissertation

- **Agreement**, not alignment / accuracy / fidelity / matching, for the central quantity. A drawing does not "convey" or "carry" an emotion. "Valence-sign agreement", never "mood direction". Exceptions: the registered title, the NLI hypothesis template ("This scene conveys {}"), and describing other people's work in their own words.
- **No Ethics section**; do not use the words "ethics" or "approval" in the dissertation. Name removal is described as **data pre-processing** (8 records redacted; illness and grief content kept, per supervisor).
- Structure (supervisor): Abstract, Introduction, Literature Review, Methodology, Results (shorter), Discussion; plus Conclusions and Further Work.
- Never claim anything about what a person sees (agreement is between two machine readers), about colour (no colour condition), about a positive-vs-negative direction (degenerate nulls), or about the generator alone.
- Records are not people: contributors unknown, at most 763.
- References: only the 91 entries in `report/mybibliography.bib` (all evidence-based, all currently cited).

## 7. Supervisor's directions (still apply)

Similarity not matching is the novel contribution · describe the image then extract the emotion (do not ask CLIP for emotion) · handle faces vs scenes · group emotional vs non-emotional prompts · redact names, keep illness content · include an evaluation (ablation, method comparison, human feedback — all done) · marking covers amount of work, quality of products and processes, writing, evaluation, supervisor engagement, and the presentation (4 Sep, went well).

## 8. Other useful files

- `emoviz/outputs/RESULTS_final.md` — every result with its caveats and a corrections log.
- `project_notes/viva_preparation/` — A-to-Z explainer, viva question bank, mock viva, revision sheet.
- `project_notes/explainers/PROJECT_EXPLAINED.pdf` — plain-English account of the whole project.
- `university_guidelines/Marking_criteria_PGT_2025-26.txt` — the marking bands.
