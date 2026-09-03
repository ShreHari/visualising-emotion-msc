# Final Results — Describe→Extract Pipeline (verified)

Consolidated analysis (`analysis_final.py`) on the **complete dataset, 1,012 records** (13 pre-test
developer images dropped). Prompt emotion via **GoEmotions** (28→7 Ekman families); image emotion via
**zero-shot NLI reading a BLIP-VQA description**. **Every metric is reported against a random-pairing
NULL with a z-score**, and every headline is re-checked on **distinct prompts only** (see robustness).
Independently reviewed for statistical validity; over-claims corrected.

Rules (documented, not per-record tuning): *emotional prompt* = GoEmotions top-1 ≠ neutral (607 emo /
405 non-emo); *face image* = BLIP-VQA reports ≥1 person AND a readable expression word — token-matched so multi-word answers count (591 / 421 across all analysed records; audit-refined rule).

---

## Headline findings

### 1. Faces carry the emotion; scenes carry it far more weakly (Chen's prediction — confirmed)
Metric values with their z vs the null (full sample):

| Image type (emotional prompts only; 402+205=607) | Valence-sign agreement | Family agreement | Top-3 overlap |
|---|--:|--:|--:|
| **Face** (n=402) | **74%** (z+10.4) | **62%** (z+10.3) | 53% (z+11.6) |
| Scene (n=205) | 43% (z+5.8) | 36% (z+4.4) | 45% (z+4.9) |

(The 591/421 face/scene counts above cover the whole analysed set; this table is the emotional-prompt
subset.) Both are *above chance* — but faces align roughly **1.7× better on valence and family**. On
distinct prompts only, the gap holds: face 72% (z+8.4) vs scene 37% (z+3.5). (Valence-Arousal similarity is ~84%
for both and is **not** where the difference lives — the signal is in sign/family, so report those.)
**Honest caveat — partial circularity:** the face/scene split is defined by whether BLIP-VQA reported
an expression, and the image emotion is read from that same description; scene descriptions lack
expression content, which mechanically lowers their scores. The effect is real (survives the null and
dedup) but is entangled with the definition — state this.

### 2. Non-emotional prompts align at chance — a validity check the pipeline passes
Non-emotional prompts (n=405, e.g. "pigs", "mickey mouse"): **z ≈ 0 on every metric** (VA 77% vs
77% null). No feeling in the prompt → no alignment found. If the pipeline had "found" emotion here it
would be untrustworthy; it doesn't. (Valence-sign shows 0% only because these are neutral-signed by
definition — that cell is a definitional artifact, not a result.)

### 3. Emotional alignment is real and strong
All emotional prompts (n=607): valence-sign 64% (**z+11.1**), family 53% (**z+10.3**), top-3 overlap 51%
(**z+11.6**), VA 84% (**z+12.2**). Holds on distinct prompts (z+9 to +11). An image's emotion is
significantly more similar to its own prompt than to a random prompt, on every measure.

### 4. New method beats the old one (the evaluation)
Describe→extract vs direct-CLIP on the same 608 records (608 = the old pipeline's emotional subset;
the final prompt reader gives 607): family agreement **49% vs 25%** (doubled), top-3 overlap
**49% vs 23%** (roughly doubled — corrected in audit: an earlier label-space mismatch had deflated
the old method's overlap to 15%), VA similarity 84% vs 74%. Chen's redirection is empirically justified.

---

## What we CANNOT claim (corrected after review)

- **"Positive emotions align better than negative" — NOT supported.** Within a single-valence subset
  the sign/family null is *degenerate* (every prompt shares one label → z = 0), and the raw "87% vs
  76%" is a base-rate/affect-space compression effect, not alignment. The direct-CLIP reader said the
  *opposite* (positive collapses). **The two readers diverge and neither can settle it — this is
  precisely what the human-rating study is for.** Do not state a direction.
- **fear / disgust / surprise** are poorly captured by both readers → restrict strong claims to the
  positive/negative (valence) axis and the face/scene split.

## Robustness & honesty notes
- **Duplicate prompts disclosed:** 249 of 1,012 records repeat an earlier prompt ("happy" ×42, etc.);
  the permutation test treats them as independent. Re-running on the **763 distinct prompts** keeps the
  face finding strong (z+9) and the validity check intact; scene weakens (z+3) and negative drops to
  non-significant — all reported, none hidden.
- **BLIP-VQA positivity bias:** reads ~66% of faces as smiling — inflates positive/face results; another
  reason the positive claim can't stand and the human study is needed.
- **Possible face↔positive confound:** happy prompts tend to yield smiling faces, so the face and
  positive effects partly overlap; the valence-sign gap (74% vs 43%) is large enough that the face
  effect is likely genuine, but state the confound.
- Valence-Arousal uses emotion-label centroids, not continuous NRC-VAD — a next upgrade.

## Data accounting — nothing left out
All **1,025 images were processed** (100%, 0 failures). Of these, 13 are pre-festival developer tests
(dropped from analysis, still processed) → **1,012 analysed**. Every analysed record is placed in exactly
one emotional/non-emotional group (607 / 405) **and** one face/scene group (591 / 421), and **all groups
are reported** — the splits are groupings for analysis, not exclusions. The duplicate-prompt structure is
used both as a robustness check (dedup) and as its own analysis (below). (`data_audit_consistency.py`)

## Extra finding — generative consistency (uses the repeated-prompt data)
87 distinct prompts were drawn **2+ times** (336 records, 33% of the data). These pool corpus-wide
repeats — the same text typed by different visitors *and* consecutive re-generations — but the prompt
text, the generator's only input, is identical within each group, so the question stands: *given the
same prompt, does DALL·E draw the same feeling?*
- Mean per-prompt agreement on the **exact emotion: 69%**; on **valence: 74%**.
- Only **28 of 87** repeated prompts drew one consistent emotion every time.
- (Earlier documents count 65 *consecutive* identical-submission runs, largest "Happy" ×11 — a stricter
  same-session definition; the corpus-wide grouping used here is the broader, clearly-labelled one.)
- e.g. "happy" ×42 → 34 joy / 7 neutral / 1 surprise;  "curious" ×12 → 5 neutral / 4 joy / 2 surprise / 1 anger.

**→ Generative emotion is unstable:** given the *same* prompt, the model conveys a *different* feeling
roughly a third of the time. This is a finding distinct from fidelity, and it draws directly on the
repeated-prompt structure of the dataset. (`outputs/consistency.json`)

## Files
- `analysis_final.py` — this analysis (re-runnable; caches prompt emotions; prints full-sample + distinct-prompt blocks)
- `outputs/analysis_final.csv` — per record: id, text, prompt emotion, image emotion, emotional?, face?
- `outputs/describe_extract.jsonl` — full pipeline output (1,025 records incl. pre-tests)
- `outputs/RESULTS_describe_extract.md` — the method build + baseline comparison + rejected approaches
