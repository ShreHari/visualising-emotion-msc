# EmoViz — measuring whether AI drawings convey the feeling in their prompts

Analysis toolkit for the MSc dissertation *"Visualising Emotion"* (University of Sheffield,
supervisor Dr Chaona Chen). Dataset: **1,025 short public self-reports of emotion**, each rendered
as a black-and-white line drawing by DALL·E at Festival of the Mind 2024. Question: **does the
drawing convey the feeling in the words?** — measured by **similarity, not exact matching**.

## The pipeline (final architecture)

```
PROMPT ── GoEmotions (28 → 7 Ekman families) ──────────────► top-3 emotion ┐
                                                                           ├─► SIMILARITY LADDER
IMAGE ── BLIP-VQA describes it ── zero-shot NLI reads the ─► top-3 emotion ┘    (each metric vs a
         (expression / action /    description               random-pairing null → z-score)
          posture / scene —
          emotion never asked)
```

* **Describe, don't ask** — the vision model is never asked for an emotion (supervisor's design);
  emotion is inferred from its factual description by a separate text model.
* **Similarity, not matching** — four metrics at increasing strictness (valence–arousal proximity,
  valence sign, Ekman family, probability-weighted top-3 overlap); every number is referenced to a
  random-pairing null, so alignment means *beats chance*, not "exact match".

## Quick start

```bash
bash setup.sh                          # one-time: creates .venv, installs pinned requirements.txt
bash test.sh                           # full self-test (env, data, analyses, live pipeline, figures)
.venv/bin/python analysis_final.py     # the final analysis (instant — uses cached outputs)
```

First run downloads ~3.5 GB of models from Hugging Face (cached afterwards):
`Salesforce/blip-vqa-base` · `facebook/bart-large-mnli` · `SamLowe/roberta-base-go_emotions`.

## Interactive interface (pipeline tester)

```bash
bash run_interface.sh          # starts the app and opens http://127.0.0.1:5050
```

A small local web app that runs the **real** pipeline live — useful for testing, for showing the
supervisor, and as a demo in the presentation:

* pick a drawing (random from the dataset, by id, or **upload your own image**),
* watch BLIP-VQA describe it (expression / action / posture / scene — emotion never asked),
* see the emotion NLI infers from that description, and the emotion GoEmotions reads from the text,
* get the **similarity verdict** on the same ladder the analysis uses.

**Every number is shown against chance.** `/api/baselines` computes the random-pairing null at
startup from `describe_extract.jsonl` + `prompt_emotions_goe.json`, using the *identical* procedure as
`analysis_final.py` (300 shuffles), and the interface renders it. This matters: the valence–arousal
metric **cannot fall below 0.412** and randomly paired text/images already average **76%**, so a bare
0–100 score reads as a pass when it is in fact below chance. The interface therefore
(a) starts that axis at the metric's real floor, (b) shades the middle half of random pairings,
(c) reports the percentile (*"closer than N% of random pairings"*), and (d) leads the verdict with
valence-sign and family agreement — the two measures `RESULTS_final.md` identifies as carrying the
finding, VA being unable to separate faces from scenes.

The app is **host-ready**: models pre-warm in the background (float16, ~1.8 GB); an inference lock
queues concurrent visitors safely; uploads are size-capped; nothing a visitor types or uploads is
stored and the request log is suppressed (no visitor IPs). Port **5050** (macOS AirPlay occupies 5000).

**Name redaction, not withholding.** Per supervisor direction (30 Jul 2026): *redact real names;
keep illness and grief content — it is not identifying on its own and it is essential to the
analysis; document the procedure.* `preprocess_names.py` implements exactly that, and
`emoviz/data.py` applies it at load time, so the analysis, the figures and the demo cannot diverge.
All **1,012 records are served** — nothing is hidden, so there is no hidden set for id-probing to
recover. The dataset files on disk are never modified.

**Sharing it:**
- *Same Wi-Fi:* `HOST=0.0.0.0 .venv/bin/python app.py` → share `http://<your-ip>:5050`.
- *Beyond your network:* a quick tunnel (`cloudflared tunnel --url http://localhost:5050` or ngrok),
  or a small always-on machine. GitHub Pages **cannot** host it (it needs a Python server + models).
- *Ethics note:* fine to share as a **demo** (it collects nothing). The moment you ask testers to
  **rate** things and keep their answers, that is the human study — ethics approval first.

## Name redaction (pre-processing)

```bash
.venv/bin/python preprocess_names.py            # audit report (dry run)
.venv/bin/python preprocess_names.py --apply    # also scrub derived artifacts (.prename backups kept)
```

Three documented stages. **Detect** — high recall by design, because 77% of the corpus is written
entirely in lower case, so capitalisation alone would miss most names; candidates come from an NLTK
given-name gazetteer, mid-sentence capitalisation against a ~236k-word English dictionary, and
naming phrases ("called X", "my friend X"). **Review** — every candidate carries a recorded
REDACT/KEEP decision with a reason; the audit **fails** if any candidate is unreviewed or if a
REDACT entry matches nothing. **Apply** — scoped to the specific record each name was reviewed in,
which is what stops "Jack Frost" and "woolly mammoth" being scrubbed as people.

**8 records** contain names of private individuals; those names become `[name]`. Places, brands,
public figures (Orwell, Botticelli), medical eponyms (Parkinson's, Alzheimer's) and detector
artefacts are kept. **Redaction is analytically inert:** re-running GoEmotions on the redacted
prompts moves each probability by ≤0.012 and changes **zero** top-1 emotion families.

## Regenerating everything from scratch (order matters)

```bash
.venv/bin/python describe_extract.py               # 1. full pipeline over all 1,025 images
                                                   #    (~30-90 min; crash-safe/resumable JSONL)
.venv/bin/python analysis_final.py                 # 2. final analysis: splits, similarity, nulls, dedup
.venv/bin/python data_audit_consistency.py         # 3. data accounting + repeated-prompt consistency
.venv/bin/python similarity_v2.py                  # 4. old-vs-new method comparison
                                                   #    (reads outputs/results_clip_v2_baseline.json —
                                                   #     the FROZEN direct-CLIP baseline)
.venv/bin/python make_figures.py                   # 5. all report figures -> outputs/figures/
```

Demo without touching real outputs: `.venv/bin/python describe_extract.py --limit 5 --out /tmp/demo.jsonl`

## Key results (verified; details in `outputs/RESULTS_final.md`)

1. **Faces carry emotion, scenes far less** — valence-sign agreement 74% (z≈+11) vs 43% (z≈+6);
   robust on deduplicated prompts.
2. **Validity check passes** — non-emotional prompts ("pigs") align at chance (z≈0).
3. **Generative emotion is unstable** — identical prompts re-drawn agree on the emotion only ~69%.
4. **Method comparison** — describe→extract beats direct-CLIP (family agreement roughly doubled).
5. **Not claimed:** a positive-vs-negative direction (reader biases conflict; awaiting the
   human-rating study).

## File map

| File | Role |
|---|---|
| `preprocess_names.py` | **Name redaction** (detect → reviewed decision → apply; `--apply` scrubs derived artifacts) |
| `describe_extract.py` | **The pipeline** (BLIP-VQA + NLI; crash-safe, resumable) |
| `analysis_final.py` | **The final analysis** (splits · similarity ladder · nulls · dedup) |
| `data_audit_consistency.py` | Data accounting + repeated-prompt consistency |
| `similarity_v2.py` | Old-vs-new baseline comparison |
| `make_figures.py` | Report figures (PDF + PNG) |
| `test.sh` / `setup.sh` / `requirements.txt` | Self-test · environment setup · pinned deps |
| `app.py` + `web/index.html` + `run_interface.sh` | **Interactive pipeline tester** (local web app) |
| `emoviz/` | Core package — `data.py` (robust loader, used by everything) + v1 baseline reader |
| `run.py`, `validate.py`, `similarity_v1.py`, `valence_rq1.py` | **v1 baseline era (superseded** — banners inside; `run.py` overwrites `outputs/results.json`) |
| `outputs/RESULTS_final.md` | **The verified findings** |
| `outputs/RESULTS_describe_extract.md` | Method build log (incl. rejected approaches) |
| `outputs/describe_extract.jsonl` | Per-record pipeline output (all 1,025) |
| `outputs/analysis_final.csv` | Per-record analysis table (1,012 analysed) |
| `outputs/results_clip_v2_baseline.json` | Frozen direct-CLIP baseline for the comparison |
| `outputs/archive/` | Superseded dashboards/write-ups (banners inside; do not cite) |
| `PIPELINE_DESIGN.md` | Design-space record (options considered; see AS-BUILT banner) |

## Notes for a new machine
* Paths in `describe_extract.jsonl` are absolute to the authoring machine; regenerate or remap if moving.
* Runtime auto-selects `mps` (Apple) / `cuda` / `cpu`. Keep RAM free: models >1B parameters were
  found to thrash on a 16 GB laptop (see "Rejected approaches" in the method build log).
