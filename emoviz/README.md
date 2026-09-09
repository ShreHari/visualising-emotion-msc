# EmoViz — measuring agreement between a prompt's emotion and its AI drawing's emotion

Analysis toolkit for the MSc dissertation *"Visualising Emotion: A Similarity-Based Analysis of
Emotional Fidelity in Text-to-Image Generation"* (University of Sheffield, supervisor Dr Chaona
Chen). Corpus: **1,025 prompt–drawing records** collected at Festival of the Mind 2024 (visitors
typed free text, mostly how they felt; DALL·E drew each as a black-and-white line drawing).
Question: **how far does the emotion a text model reads from the words agree with the emotion a
second model reads from the drawing?** — measured as **similarity against chance, not exact
matching**. Nothing here is a statement about what a person would see in a drawing: that is the
next study, and a single-coder check is built in (below).

## The pipeline

```
PROMPT ── GoEmotions (28 → 7 Ekman families) ──────────────► top-3 families ┐
                                                                            ├─► FOUR MEASURES, each vs a
IMAGE ── BLIP-VQA answers 5 factual questions ── zero-shot NLI ─► top-3     ┘   random-pairing null → z
         (expression / action / posture /        reads the one-
          people / scene — emotion never asked)  sentence description
```

* **Describe, then extract.** The vision model is asked only factual questions; a separate text
  model infers the emotion from the description. (The separation is weaker than it sounds: where
  the expression answer is itself an affect word — 41% of records — the reader relays it 99.8% of
  the time. That is measured, not assumed: `audits.py`, `ablate_nli.py`.)
* **Similarity, not matching.** Four measures at increasing strictness (valence–arousal proximity,
  valence sign, Ekman family, top-3 soft overlap). **Every number is read against a random-pairing
  null**: the valence–arousal measure cannot fall below 0.412 and randomly paired records already
  average 76%, so a bare score means nothing; the z against the null does.
* **One definition of everything.** `emoviz/metrics.py` holds every constant and measure; the
  analysis, the significance test, the demo app, the audits and the numeric tests import it.

## Quick start

```bash
bash setup.sh                          # one-time: creates .venv, installs pinned requirements.txt
bash test.sh                           # full self-test: environment, data, every analysis, a live
                                       #   pipeline run, redaction, numeric regression, figures
.venv/bin/python analysis_final.py     # the final analysis (seconds — uses cached outputs)
```

First run downloads ~3.5 GB of models from Hugging Face (cached afterwards):
`Salesforce/blip-vqa-base` · `facebook/bart-large-mnli` · `SamLowe/roberta-base-go_emotions`.

## Key results (all verified; details and caveats in `outputs/RESULTS_final.md`)

Every figure below is agreement between the prompt reader and the image reader on the 607 records
whose prompt the text reader labels emotional, against a 300-shuffle random-pairing null (seed 7),
with clustered-bootstrap 95% CIs (10,000 draws, clustered on prompt identity).

| | valence-sign agreement | emotion-family agreement |
|---|---|---|
| all emotional (n=607) | 64.0% vs 45.6% null, z +11.1, CI [58.6, 68.8] | 53.0% vs 38.8%, z +10.3, CI [47.3, 58.7] |
| face-classified (n=402) | 73.9% vs 53.5%, z +10.4, CI [68.3, 79.2] | 61.9% vs 45.8%, z +10.3, CI [55.8, 68.1] |
| scene-classified (n=205) | 42.9% vs 29.6%, z +5.8, CI [33.1, 51.1] | 35.6% vs 26.2%, z +4.4, CI [26.4, 44.1] |

1. **Agreement is real** on every measure and survives Holm–Bonferroni across the 36 non-degenerate
   comparisons the analysis prints (26 survive; the ten that do not are the control cells, the
   single-valence cells and the distinct-prompt scene family, z +2.6).
2. **Face-classified drawings agree far more than scene-classified ones**: difference +30.9 pp
   [+22.6, +40.6] on valence sign, +26.3 pp [+18.4, +35.3] on family, clustered permutation
   p = 0.0001. The split is the describer's, not a human's, and 414 of the 421 scene-classified
   records are drawings in which the describer reports no person yet still names an expression
   (332 of them "smile"/"smiling"/"happy") — the template asserts a face that is not there. The
   description-template ablation (`ablate_nli.py`) shows what this rests on: with a people-aware
   description, face rows are unchanged and **scene agreement falls to its null** (valence sign
   4.7% vs 3.4%, z +1.6); and removing the expression word alone drops family agreement from 53.0%
   to 20.3%. This reader reads faces, and only faces.
3. **Specificity check passes weakly**: on the 405 prompts the text reader labels neutral, only the
   valence–arousal measure is informative (76.6% vs 76.6%, z +0.3; the other nulls are degenerate by
   construction). 68 of those prompts contain a plain affect word; on the cleaned 335 the z is +0.04.
4. **Like-for-like image-reader comparison**: same prompt reader, same 607 records — describe-then-
   extract agrees with the text reader on 53.0% of families against 22.4% for direct CLIP
   (+30.6 pp, CI [+25.5, +35.6], cluster sign-flip p < 0.0001). Neither reader has ground truth, so
   this shows the two readers disagree, with describe-then-extract far closer to the text reader.
5. **Repeated prompts**: across 87 prompts drawn 2+ times, the reader returns the same family for
   68.8% of drawings within a group against a permutation null of 59.4% (z +4.5) — more consistent
   than chance, far from fixed. Half the groups are pairs (floor 50%). This bounds the whole
   prompt→image→reader chain, not the generator alone.
6. **Not claimed**: a positive-vs-negative direction (single-valence nulls are degenerate and the
   two readers point opposite ways); anything about fear, disgust or surprise (n ≤ 16, or a class
   made largely of curiosity-mapped prompts; the reader never returns disgust); human validity.

## Interactive interface (pipeline tester)

```bash
bash run_interface.sh          # starts the app and opens http://127.0.0.1:5050
```

A local web app that runs the **real** pipeline live: pick a drawing (random, by id, or upload your
own), watch BLIP-VQA answer the five questions, see the emotion NLI infers from that description
and the emotion GoEmotions reads from the words, and get the four measures **against chance** —
`/api/baselines` computes the same null the analysis uses, and the interface starts the
valence–arousal axis at its true floor, shades the middle half of random pairings, reports the
percentile, and leads with valence sign and family. Degenerate chance figures are suppressed.

Host-ready: models pre-warm in the background (float16, ~1.8 GB); an inference lock queues
concurrent visitors; uploads are size-capped; nothing a visitor types or uploads is stored; the
request log is suppressed. All 1,012 analysed records are served, names redacted. Port 5050.
Same Wi-Fi: `HOST=0.0.0.0 .venv/bin/python app.py`; beyond it, a tunnel (`cloudflared`, ngrok).

## Name redaction (data pre-processing)

```bash
.venv/bin/python preprocess_names.py            # audit report (dry run)
.venv/bin/python preprocess_names.py --apply    # also scrub derived artifacts (.prename backups kept)
```

Per supervisor direction (30 Jul 2026): redact real names of private individuals; keep illness
and grief content, which is not identifying on its own and is essential to the analysis. Three
documented stages — **detect** (high recall by design: about 78% of the corpus is lower-case, so
capitalisation alone would miss most names; candidates come from an NLTK given-name gazetteer,
mid-sentence capitalisation against a ~236k-word dictionary, and naming phrases), **review**
(every candidate carries a recorded REDACT/KEEP decision with a reason; the audit fails on any
unreviewed candidate or stale entry), **apply** (scoped to the specific record each name was
reviewed in, which is what stops "Jack Frost" and "woolly mammoth" being scrubbed as people).
Redaction is applied at load time by `emoviz/data.py`; the files on disk are never modified.

**8 records** contain names of private individuals; those names become `[name]`. Two records
consisted of a name alone and reduce to `[name]`; they are counted in the neutral-labelled group
and the control audit shows removing them changes nothing. Redaction changes no top-1 family and
moves no GoEmotions probability by more than 0.012. **The reviewed decision table is not in the
repository** — by its nature it names the tokens it redacts — it lives at
`private/redaction_decisions.json` (git-ignored) and travels with the dataset. Everything that
reads only `outputs/` works without it.

## Regenerating everything from scratch (order matters)

```bash
.venv/bin/python describe_extract.py          # 1. the pipeline over all 1,025 images (30–90 min; resumable)
.venv/bin/python analysis_final.py            # 2. splits · four measures · nulls · dedup -> analysis_final.json
.venv/bin/python data_audit_consistency.py    # 3. data accounting + repeated-prompt consistency with its null
.venv/bin/python significance.py              # 4. clustered bootstrap CIs + clustered permutation test (face vs scene)
.venv/bin/python inference.py                 # 5. CIs on every subset, Cohen's kappa, Holm–Bonferroni, z stability
.venv/bin/python method_comparison.py         # 6. like-for-like image-reader comparison + paired tests
.venv/bin/python audits.py                    # 7. control contamination · describer leak / copy rate · per family
.venv/bin/python error_taxonomy.py            # 8. failure modes of the 38 high-confidence disagreements
.venv/bin/python ablate_nli.py                # 9. description-template ablation (NLI only re-run; ~30 min)
.venv/bin/python make_figures.py              # 10. every figure, generated from the JSON above
.venv/bin/python export_tex.py                # 11. LaTeX macros + tables for the dissertation (report/generated/)
.venv/bin/python test_numeric.py              # pins every headline number to its result file
```
Steps 2–8 and 10–11 read cached outputs and take seconds. `similarity_v2.py` is the historical v1
comparison (NLI prompt side, 608 records; superseded by step 6 but kept as a record).

### The human check (single coder, blind)

```bash
.venv/bin/python human_check.py sample      # 120 drawings, stratified on the describer's output ->
                                            #   outputs/human_check/sheet_01..06.png + labels.csv
# ... code each drawing from the sheets only (person? readable face? valence? family?) ...
.venv/bin/python human_check.py score       # describer and reader vs the human, Wilson 95% CIs; the
                                            #   face/scene contrast re-run on the HUMAN split
```

## File map

| File | Role |
|---|---|
| `emoviz/metrics.py` | **The single definition** of every constant, measure, split rule and the null |
| `emoviz/data.py` | Robust loader (three filename schemes, timestamps, dedup_key, redaction at load) |
| `preprocess_names.py` | Name redaction (detect → reviewed decision → apply; decision table in `private/`) |
| `describe_extract.py` | **The pipeline** (BLIP-VQA + NLI; crash-safe, resumable) |
| `analysis_final.py` | **The final analysis** → `outputs/analysis_final.{csv,json}` |
| `data_audit_consistency.py` | Data accounting + repeated-prompt consistency with permutation null |
| `significance.py` | Clustered bootstrap + clustered permutation test of the face/scene difference |
| `inference.py` | CIs on every subset · Cohen's κ · Holm–Bonferroni · z stability over seeds |
| `method_comparison.py` | Like-for-like describe-then-extract vs direct-CLIP, McNemar + cluster sign-flip |
| `audits.py` | Control contamination · describer leak and copy rate · per-family recall |
| `error_taxonomy.py` | Failure-mode census of high-confidence disagreements (+ `outputs/ERROR_TAXONOMY.md`) |
| `ablate_nli.py` | Description-template ablation (drop-one, fixed expression, people-aware) |
| `human_check.py` | Blind single-coder sample, contact sheets, scoring with Wilson CIs |
| `make_figures.py` | Report figures, entirely from the JSON result files |
| `export_tex.py` | LaTeX macros and tables for `report/` from the same JSON |
| `test.sh` / `test_numeric.py` / `setup.sh` / `requirements.txt` | Self-test · numeric regression · environment · pinned deps |
| `app.py` + `web/index.html` + `run_interface.sh` | **Interactive pipeline tester** (local web app) |
| `outputs/RESULTS_final.md` | **The verified findings**, with every caveat |
| `outputs/RESULTS_describe_extract.md` | Method build log (incl. rejected approaches) |
| `outputs/describe_extract.jsonl` | Per-record pipeline output (all 1,025) |
| `outputs/results_clip_v2_baseline.json` | Frozen direct-CLIP baseline for the comparison |
| `outputs/archive/` | Superseded dashboards/write-ups (banners inside; do not cite) |
| `run.py`, `validate.py`, `similarity_v1.py`, `valence_rq1.py` | v1 baseline era (superseded; banners inside) |
| `PIPELINE_DESIGN.md` | Design-space record (options considered; AS-BUILT banner) |

## Notes for a new machine
* Paths in `describe_extract.jsonl` are absolute to the authoring machine; regenerate or remap if moving.
* Runtime auto-selects `mps` (Apple) / `cuda` / `cpu`. Keep RAM free: models >1B parameters were
  found to thrash on a 16 GB laptop (see "Rejected approaches" in the method build log).
* The analysis scripts (steps 2–11) need only `outputs/`; the pipeline, the demo and the human
  check need `../02AI_drawing_data/` and `private/redaction_decisions.json`.
