# Handoff — Visualising Emotion (MSc AI dissertation)

Read this first in a new session. State of the project on **21 September 2026**.

**SUBMITTED on Monday 21 September 2026**, before the extended deadline (15:00, Wednesday
23 September). Route "as is": Submission Link A (Turnitin, the dissertation PDF), Link C (the
submission form, 18:14) and Link D (the code zip, 18:16); Links B1/B2 were not needed. Blackboard
tags the submissions "(Late)" because it still shows the original 16 September due date; the
extension removes the penalty.

**Submission proof** (receipts, the exact files submitted, screenshots, and a README with SHA-256
checksums) is in `~/Desktop/COM6912_Submission_Proof/`, outside the repository on purpose because
it holds personal correspondence. On 21 September the one item still to add was the Link A
Turnitin digital receipt.

---

## 1. The project in one paragraph

**Registered title (do not change):** *Visualising Emotion: A Similarity-Based Analysis of Emotional
Fidelity in Text-to-Image Generation*
Student: Shre Hari Prem Anandh · MSc Artificial Intelligence (COM6912), University of Sheffield ·
Supervisor: Dr Chaona Chen.

At the Festival of the Mind 2024 (Sheffield), visitors typed how they felt and DALL·E drew each
entry as a monochrome line drawing: **1,025 records, 1,012 analysed** (13 pre-festival developer
tests dropped, found via the C2PA signing timestamps inside the PNGs). The project measures
**agreement** between the emotion a text model reads from the words (GoEmotions, 28 labels → 7
families) and the emotion a second reader gets from the drawing (BLIP-VQA answers five factual
questions → one sentence → BART-MNLI zero-shot). Agreement is scored as **similarity, not
matching**, on four measures (valence–arousal similarity, valence-sign agreement, family agreement,
top-3 overlap), and **every value is read against a random-pairing null** (300 shuffles, seed 7),
with clustered bootstrap CIs and clustered permutation tests because 249 records repeat a prompt.

---

## 2. THE DISSERTATION IS FINISHED AND SUBMITTED

`dissertation/main.pdf` — **81 pages, A4, 0 errors, 0 undefined references, 0 placeholders,
0 TODOs.** All eight objectives met. It builds clean from scratch.

### The signature is kept out of the repository

The Declaration is dated 21 September 2026 and was signed for submission. LaTeX places the
signature from `dissertation/images/signature.png`, which is git-ignored, and `main.tex` leaves the
line blank when that file is absent. **The committed `main.pdf` is unsigned on purpose**; its text is
identical to the submitted PDF. The signed PDF that was submitted is
`PremAnandh_ShreHari_COM6912_Dissertation.pdf` (SHA-256 `2c45fddd…`), kept at the repo root
(git-ignored) and in the proof folder. A local rebuild with the signature file present makes a
signed `main.pdf` again: **do not commit that one.**

Never sign with macOS Preview. Re-saving through Preview garbled the PDF text layer at the ff/fi/ffl
ligatures ("di#erence", "She!eld"), which Turnitin would flag as replaced characters.

Nothing is left to do. Do not go looking for more work unless the student asks.

### Do not re-do these — they are done and verified

- Single-coder check: **120 of 120 drawings coded**, scored, written into §4.11 with Table 4.15
- Both screenshots placed: Figure 3.6 (demonstrator verdict) and Figure A.1 (38/38 test run)
- All 91 references verified against arXiv / Crossref / Zenodo (see §6)
- Formatting brought to the School spec (see §5)
- First person converted: 107 → 1 (the Declaration boilerplate, which must stay)
- Similarity check: **11%**, 0 missing citations, nothing above 3% from one source
- Final audit, 21 September: every citation re-read against its source; four mis-stated claims
  (references [39], [47], [65], [90]) and one overstatement (Alvarado, on colour) corrected in seven
  sentences. Running heads added to the Declaration, Abstract and Appendices pages, Table 4.6
  padding fixed, Figures 3.6 and A.1 referenced in the text

---

## 3. Folder layout

| Folder | Contents |
|---|---|
| `dissertation/` | **The live dissertation.** Self-contained Overleaf project. `main.tex`, `chapters/`, `generated/`, `figures/`, `images/`, `mybibliography.bib`, `main.pdf` |
| `emoviz/` | **The code.** Pipeline, analyses, audits, tests, demonstrator; results and figures in `emoviz/outputs/` |
| `02AI_drawing_data/` | The dataset. Code reads it from here. **Never upload it** |
| `report/` | Superseded 9 September draft, kept for reference. **But `report/generated/` is where `export_tex.py` actually writes** — `sync_generated.sh` copies from there into `dissertation/generated/`. Do not delete it |
| `university_guidelines/` | Marking criteria, project spec, template, lectures |
| `project_notes/` | `meetings/`, `presentation/`, `viva_preparation/`, `explainers/`, `literature/`, `drafts/`, `archive/` |

Local-only files at the repo root, all git-ignored: the two files as submitted
(`PremAnandh_ShreHari_COM6912_Dissertation.pdf`, signed, and `PremAnandh_ShreHari_COM6912_Code.zip`),
`LinkC_title_and_abstract.txt` (the title and abstract entered in Link C), a copy of university
correspondence, and the duplicates `dissertation copy/`, `dissertation copy.zip` and
`dissertation_overleaf.zip` (the Overleaf zip holds the signature). The Overleaf upload zip is
regenerated on demand (§4).

GitHub: `github.com/ShreHari/visualising-emotion-msc` — **must stay private until after results.**
Never commit `02AI_drawing_data/`, `emoviz/private/` (redaction decision table, names real people),
`*.prename` / `*.nodedup` backups, the literature PDFs, the signature image, a signed `main.pdf`, or
the local-only files above. `.gitignore` covers all of these except a signed `main.pdf`, which is a
tracked file and has to be checked by hand.

---

## 4. How to build and run

```bash
# the dissertation (from dissertation/)
pdflatex main && bibtex main && pdflatex main && pdflatex main

# refresh numbers and tables after any analysis change
bash dissertation/sync_generated.sh

# the code (from emoviz/)
bash setup.sh              # one-time environment, Python 3.12, pinned requirements
bash test.sh               # 38 smoke checks + test_numeric.py; currently 38/38 PASSING
bash run_interface.sh      # demonstrator at http://127.0.0.1:5050
```

### Overleaf zip

```bash
cd dissertation && zip -rq ../dissertation_overleaf.zip . -x '.DS_Store' '*/.DS_Store' '*__pycache__*'
```

Zip the **contents**, not the folder, so `main.tex` lands at the zip root. Overleaf: New Project →
Upload Project → compiler pdfLaTeX → defaults. The zip picks up `images/signature.png` when it is
present, so keep it private.

> **Known environment quirk:** `grep -c` silently returns nothing in this shell. It once reported
> exit 1 for a string on line 1 of a file, which produced two wrong status reports. **Count things
> with Python, not grep.**

---

## 5. Formatting — brought to the School spec on 17–18 September

All of this is done. Verified against the COM Programme Information 2026/27 style rules.

| Rule | State |
|---|---|
| Line spacing | `\setstretch{1.1}` |
| Font size | 11pt, Computer Modern, `\texttt` for code |
| Margins | **37 mm left / 25 mm right** (binding spec), A4, via `geometry` |
| Font encoding | `[T1]{fontenc}` — fixes braces in typewriter text and accented names |
| Headers | `fancyhdr`, centred, on **every** page including chapter/appendix openings. "Chapter 4. Results", "Appendix D. Glossary" |
| Page numbers | Centred footer, roman front matter, arabic from Chapter 1, appendices included |
| Glossary | Moved from front matter to **Appendix D** |
| Headings | Three levels + unnumbered `\paragraph` |
| Acronyms | Defined at first use: C2PA, BERT, LIWC, FID, VQA, NLI, CI, CLIP, BLIP |
| Figures/tables | Chapter-numbered, referenced by number, no "figure below" |
| Word count | ~18,600 (limit 10,000–20,000) |

**Deliberate exception:** the abstract keeps `BLIP-VQA` and `BART-MNLI` unexpanded. They are
checkpoint names functioning as proper nouns; expanding them mid-abstract clutters it. They are
defined where the models are introduced in the body.

---

## 6. References — all 91 verified, nothing fabricated

Verified live: 39 by exact arXiv ID, 30 by DOI through Crossref, 17 by Crossref title search,
13 classics checked to volume and page, 2 URLs, 1 Zenodo record comparison.
**Every entry is real and every entry is cited. No gaps, none uncited.**

Six metadata corrections were applied on 18 September, each confirmed against the publisher record
**before** editing — never trust a suggested correction without checking it:

| Key | Correction |
|---|---|
| `chen2024cultural` | pages `213--223` → `213--223.e5` (Cell style) |
| `koo2026evaluating` | pages `2052--2059` → `2052--2062`, DOI added |
| `ilharco2021openclip` | Zenodo `5143773` → `7301701` — 5143773 lists 11 creators, our 13-author list matches 7301701 |
| `dang2025emoticrafter` | arXiv → ICCV 2025, pp. 15218–15228 |
| `lin2024make` | arXiv → ICCV 2025, pp. 16367–16376 |
| `harutyunyan2026fine` | "submitted to Elsevier" → arXiv:2601.18162, January 2026 |

**`lomas2024improved` was deliberately NOT switched to its journal version.** The published paper
exists (*"Evaluating the alignment of AI with human emotions"*, Advanced Design Research 2(2):88–97,
DOI 10.1016/j.ijadr.2024.10.002) but carries a **different title**, and the dissertation makes
specific claims about that study's design (24 raters, 240 images, person vs robot) that were
verified against the **preprint**. The preprint is cited and the journal version is named in the
note. Do not "fix" this without checking the journal version contains those claims.

---

## 7. Numbers — the only values to quote

All come from JSON files in `emoviz/outputs/`; `emoviz/test_numeric.py` pins them. In LaTeX,
**never type a number** — use the macros in `dissertation/generated/numbers.tex` (e.g.
`\FullEmoSignObs`). `sync_generated.sh` regenerates them.

| Result | Value |
|---|---|
| Emotional prompts (n=607), valence-sign | 64.0% vs null 45.6%, z +11.1, CI [58.6, 68.8] — **denominator 530**, state it |
| Emotional prompts, family | **53.0%** (322/607; never 53.1) vs 38.8%, z +10.3 |
| Face (n=402) / scene (n=205), valence-sign | 73.9% vs 53.5% / 42.9% vs 29.6% |
| Face − scene difference | +30.9 pp [+22.6, +40.6] sign; +26.3 pp family; clustered permutation p = 0.0001 |
| Distinct prompts (763) | face sign 71.8% z +8.4; scene family 30.8% z +2.6 (**fails Holm**) |
| Holm–Bonferroni | 26 of 36 non-degenerate z survive |
| Neutral-labelled (n=405) | VA 76.6% vs 76.6%, z +0.3; 68 contain an affect word; cleaned 335 z +0.04 |
| Like-for-like readers | describe-then-extract 53.0% vs direct CLIP 22.4% family, +30.6 pp, cluster p < 0.001 |
| Repeated prompts (87 groups) | 68.8% same family vs null 59.4%, z +4.5; 28/87 fully consistent vs 14.5 |
| Cohen's kappa (family) | emotional 0.23, face 0.30, scene 0.13 |
| Describer | 414/421 scene records report no person; 406 still name an expression; 332 say smile/smiling/happy |
| Copy rate | 99.8% where the expression answer is an emotion word (41% of records) |
| Ablation | expression sentence removed: family 53.0% → 20.3%; **people-aware template: face unchanged, scene falls to null** (sign 4.7% vs 3.4%, z +1.6) |
| Error taxonomy (38 confident disagreements) | describer 19, reader 5, prompt side 12, generator 2 |

### The single-coder check — completed 17 September

120 drawings, coded blind from contact sheets by the student, scored by `human_check.py score`.
Results in `emoviz/outputs/human_check/human_check.json`, written up in §4.11.

| Quantity | Value |
|---|---|
| Describer people-count accuracy | 87.5% [80.4, 92.3] |
| **Face-rule precision** | **42.2%** [30.9, 54.4] — 37 false positives vs 27 true |
| Face-rule recall | 77.1% [61.0, 87.9] |
| "Smiling" answers with a readable positive face | 18.2% [11.2, 28.2] |
| "Smiling" answers with **nobody drawn** | 50.6% [39.7, 61.5] |
| Image reader vs coder, valence sign | 71.0% (44/62) |
| Image reader vs coder, family | 40.8% (49/120), κ 0.21 |
| Face/scene contrast on the **coder's** split | +13.6 pp, z +1.8 — not significant |

**What it means:** the check *confirms* the weakness the ablation already found. It passes on the
people count, fails on the face rule, and is too small to settle the contrast. Written up honestly;
do not oversell it.

**The main finding, correctly stated:** for this reader, drawings where the describer reads a face
agree far above chance; scene drawings show nothing above chance once the invented expression is
removed — **"faces, and only faces, for this reader"**.

---

## 8. Writing conventions — keep these

- **Agreement**, not alignment / accuracy / fidelity / matching, for the central quantity. A drawing
  does not "convey" or "carry" an emotion; a reader *returns* or *reads* a family. Exceptions: the
  registered title, the NLI hypothesis template ("This scene conveys {}"), and describing other
  people's work in their own words.
- **No Ethics section.** Do not use the words "ethics" or "approval" anywhere in the dissertation.
  Name removal is described as **data pre-processing** (8 records redacted; illness and grief content
  kept, per supervisor). The 20 August calendar note mentions ethics — it stays out of Appendix C.
- **Third person.** The conversion is done. Only the Declaration boilerplate keeps "I".
- Never claim anything about what a person sees beyond the single-coder check, about colour (no
  colour condition), about a positive-vs-negative direction (degenerate nulls), or about the
  generator alone.
- Records are not people: contributors unknown, at most 763.
- References: only the 91 entries in `dissertation/mybibliography.bib`.

---

## 9. Supervision

Supervision record is Appendix C. It matches the student's **calendar record**: 18 Jun, 9 Jul,
31 Jul, 20 Aug, plus the 4 September presentation.

A 17 July brief and a 10 September brief exist in `project_notes/meetings/` but **no calendar
meeting corresponds to either**. The 17 July content was merged into the 9 July row; the 10 September
row was removed rather than claim a meeting that may not have happened. Do not re-add either without
the student confirming.

**17 September:** the student waited in the Google Meet lobby; Dr Chen had not received a
confirmation reply and the meeting did not happen. She replied graciously and said an email update
was not required. The student sent the draft by email that evening.

**Supervisor's standing directions:** similarity not matching is the novel contribution · describe
the image then extract the emotion (do not ask CLIP for emotion) · handle faces vs scenes · group
emotional vs non-emotional prompts · redact names, keep illness content · include an evaluation
(ablation, method comparison, human feedback — all done).

---

## 10. Plagiarism / AI-detection status — resolved, do not re-open

The student ran a **Turnitin Draft Coach** check via a friend's Sheffield Hallam account on
17 September. Result: **11% overall, 0 missing quotations, 0 missing citations**, highest single
source 3% (arxiv.org), everything else under 1%. The matches are the reference list and stock
academic phrasing.

**Draft Coach does not store submissions in the Turnitin repository.** This was confirmed two ways:
by the tool's design, and empirically — a second upload of the identical file 2h23m later came back
at 11% again with no self-match. **There is no stored copy and no false-match risk on submission.**

Rules until results are published: keep the GitHub repo private, do not submit to any other Turnitin
assignment that stores papers, do not post the text anywhere public.

---

## 11. Working with the student

- The supervisor is fine with AI assistance. Help freely with drafting, rewriting and editing.
- **Answer in simple English.** They prefer direct answers over long tool runs.
- They care a great deal that the prose stays in **their** voice and that similarity stays low.
  Make minimal, targeted edits. Do not bulk-rewrite prose.
- **Verify before acting on external review.** Two rounds of ChatGPT review produced genuinely
  correct findings, but every bibliography claim was checked against the publisher record before
  anything was changed. Keep doing that.
- Do not code the single-coder check, or any other human judgement, on the student's behalf. The
  validity of §4.11 depends on it being a person's blind judgement. (The student dictated their own
  codings; transcribing those was fine.)

---

## 12. Useful files

- `emoviz/outputs/RESULTS_final.md` — every result with its caveats and a corrections log
- `emoviz/outputs/human_check/human_check.json` — the scored single-coder check
- `emoviz/emoviz/metrics.py` — the one definition of every measure, constant, split rule and null
- `project_notes/viva_preparation/` — A-to-Z explainer, viva question bank, mock viva, revision sheet
- `project_notes/explainers/PROJECT_EXPLAINED.pdf` — plain-English account of the whole project
- `dissertation/build_notes/` — the writing contract and the checkers (`check_tex.py`, `copy_check.py`)
- `university_guidelines/Marking_criteria_PGT_2025-26.txt` — the marking bands

---

## 13. If something needs changing

1. Edit the **LaTeX source**, never the PDF.
2. If a *number* changes, re-run the analysis, then `bash dissertation/sync_generated.sh`, then
   rebuild. Never type a result by hand.
3. Rebuild with the full four-pass run.
4. Check with Python, not grep: errors, undefined references, missing files, overfull boxes.
5. Re-zip for Overleaf (§4).
