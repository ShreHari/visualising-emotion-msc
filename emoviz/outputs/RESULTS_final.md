# Final Results — Describe→Extract Pipeline (verified)

Consolidated analysis on the **complete corpus: 1,012 analysed records** (13 pre-festival developer
test images dropped from 1,025). Prompt emotion via **GoEmotions** (28 → 7 Ekman families); image
emotion via **zero-shot NLI reading a BLIP-VQA description**. The quantity reported throughout is
**agreement between the prompt reader and the image reader** — nothing here is a statement about
what a person would see in a drawing. **Every metric is reported against a random-pairing null with
a z-score, a clustered-bootstrap 95% CI, and a multiplicity check**; every headline is re-checked on
distinct prompts only.

**Audit trail.** Re-audited on 1 September and 9 September 2026; every correction is listed at the
end of this document. Every number below is produced by a script and written to a JSON file under
`outputs/` (`analysis_final.json`, `consistency.json`, `inference.json`, `method_comparison.json`,
`audits.json`, `error_taxonomy.json`, `ablation/summary.json`); `test_numeric.py` pins each headline
to its file and fails the build if any moves. Figures and the dissertation's tables are generated
from the same files.

**Rules (documented, not per-record tuning).** *Emotional prompt* = GoEmotions top-1 family ≠
neutral (607 emotional / 405 labelled neutral). *Face-classified image* = BLIP-VQA reports ≥ 1
person AND a readable expression word, token-matched (591 face / 421 scene across all analysed
records; 402 / 205 within the emotional prompts). Both splits are the readers' outputs, never a
human's; the face rule in particular is a property of the describer.

---

## Headline table — emotional prompts, full sample

Random-pairing null: 300 shuffles of the image side, seed 7. CI: clustered bootstrap, 10,000 draws,
resampling prompt groups (`dedup_key`), because 249 of the 1,012 records repeat an earlier prompt.
Valence-sign agreement is computed over prompts whose family has a sign (surprise and neutral have
none), so its denominator is smaller than n.

| Subset | n (signed) | Valence-sign agreement | Emotion-family agreement | Top-3 soft overlap | VA similarity |
|---|---|---|---|---|---|
| **All emotional** | 607 (530) | **64.0%** vs 45.6%, z +11.1, CI [58.6, 68.8] | **53.0%** (322/607) vs 38.8%, z +10.3, CI [47.3, 58.7] | 50.6% vs 39.4%, z +11.6, CI [46.5, 54.7] | 83.8% vs 77.3%, z +12.2, CI [82.0, 85.5] |
| Face-classified | 402 (360) | **73.9%** vs 53.5%, z +10.4, CI [68.3, 79.2] | **61.9%** vs 45.8%, z +10.3, CI [55.8, 68.1] | 53.4% vs 40.4%, z +11.6 | 84.2% vs 76.4%, z +11.2 |
| Scene-classified | 205 (170) | 42.9% vs 29.6%, z +5.8, CI [33.1, 51.1] | 35.6% vs 26.2%, z +4.4, CI [26.4, 44.1] | 44.9% vs 38.1%, z +4.9 | 82.9% vs 79.1%, z +6.0 |
| Labelled neutral | 405 (0) | degenerate null | degenerate null | 31.6% vs 31.6%, z +0.0 | 76.6% vs 76.6%, z +0.3 |

Cohen's κ on family agreement (7 × 7): all emotional **0.23** [0.18, 0.29]; face 0.30 [0.23, 0.37];
scene 0.13 [0.06, 0.19] — "fair", "fair" and "slight" on the Landis–Koch scale.

---

## Findings

### 1. Agreement between the two readers is real, on every measure

On the 607 emotional prompts, the emotion read from the drawing is closer to the emotion read from
its own prompt than to a random prompt's on all four measures (z +10.3 to +12.2). Holm–Bonferroni
across the 36 non-degenerate comparisons the analysis prints leaves 26 significant at family-wise
0.05; every full-sample emotional, face and scene cell survives. The z is an ordering statistic,
not a precise quantity: re-estimating the emotional valence-sign null under seeds 1–5 moves z
between +11.2 and +12.2 while the null mean stays within 45.5–45.6%.

### 2. Face-classified drawings agree far more than scene-classified ones

Difference face − scene: **+30.9 pp on valence sign** [+22.6, +40.6] and **+26.3 pp on family**
[+18.4, +35.3]; clustered permutation test (10,000 draws, prompt groups as units) p = 0.0001 on both
(`significance.py`). On distinct prompts only the gap holds: face 71.8% (z +8.4) vs scene 37.3%
(z +3.5).

**What the split is.** It is the describer's output, not a human judgement, and the same
description feeds the image reader — so the contrast is partly circular. The earlier explanation
("scene descriptions lack expression content") was wrong: **414 of the 421 scene-classified records
are drawings for which the describer reports no person, yet 406 of them still include an expression
word, and 332 answer "smile", "smiling" or "happy"** (80% of the 414). The description template
asserts a person and an expression that are not there, and the image reader reads that assertion.
The split is governed by the people-count answer. Two consequences follow: the scene-side reading is
largely noise from a hallucinated clause, and the face-side reading depends heavily on one word —
which the ablation (2b) quantifies.

### 2b. Ablation — what the image reading rests on

Each record's five cached BLIP-VQA answers were re-composed under an altered description template
and **only the NLI stage re-run** (`ablate_nli.py`; a control re-run of the unmodified template
reproduces every baseline number exactly — 0 of 1,012 top-1 readings change — so every difference
below is a template effect, not numerical noise). Emotional prompts, full sample; each cell is
observed vs its own 300-shuffle null.

| Description template | All emotional: valence sign | All emotional: family | Face-classified: sign | Face: family | Scene-classified: sign | Scene: family |
|---|---|---|---|---|---|---|
| **Baseline** (as published) | 64.0% / 45.6% (z +11.1) | 53.0% / 38.8% (z +10.3) | 73.9% / 53.5% (z +10.4) | 61.9% / 45.8% (z +10.3) | 42.9% / 29.6% (z +5.8) | 35.6% / 26.2% (z +4.4) |
| Expression sentence removed | 15.3% / 11.4% (z +5.1) | 20.3% / 16.6% (z +3.8) | 18.9% / 14.7% (z +3.8) | 25.9% / 20.5% (z +3.8) | 7.6% / 4.7% (z +2.7) | 9.3% / 6.4% (z +2.2) |
| Expression fixed to "unclear" | 15.1% / 10.8% (z +5.9) | 21.3% / 17.5% (z +3.9) | 17.5% / 12.8% (z +4.4) | 25.1% / 19.7% (z +4.0) | 10.0% / 6.6% (z +2.8) | 13.7% / 11.2% (z +1.5) |
| Action clause removed | 61.9% / 43.9% (z +11.0) | 50.6% / 36.7% (z +10.3) | 72.5% / 52.2% (z +10.4) | 60.7% / 44.5% (z +10.4) | 39.4% / 26.8% (z +5.6) | 30.7% / 21.9% (z +4.6) |
| Posture clause removed | 62.3% / 44.5% (z +10.7) | 51.4% / 37.9% (z +9.7) | 73.1% / 53.1% (z +10.0) | 61.4% / 45.6% (z +10.1) | 39.4% / 26.8% (z +5.6) | 31.7% / 24.0% (z +3.6) |
| Scene phrase removed | 64.2% / 46.0% (z +10.7) | 53.4% / 39.2% (z +9.8) | 74.4% / 53.8% (z +10.4) | 62.4% / 46.1% (z +10.1) | 42.4% / 29.9% (z +5.6) | 35.6% / 26.8% (z +3.9) |
| People count removed | 68.5% / 50.7% (z +10.8) | 57.8% / 43.7% (z +9.9) | 70.8% / 50.7% (z +10.4) | 59.7% / 43.6% (z +10.3) | 63.5% / 50.9% (z +5.0) | 54.1% / 44.5% (z +3.8) |
| **People-aware**: "A drawing showing {scene}." where no person is reported; otherwise baseline | 51.7% / 36.9% (z +10.1) | 47.1% / 34.5% (z +8.8) | 73.9% / 53.5% (z +10.4) | 61.9% / 45.8% (z +10.3) | **4.7% / 3.4% (z +1.6)** | **18.0% / 17.3% (z +0.6)** |
| People-aware, keeping action and posture | 55.3% / 39.5% (z +10.5) | 48.1% / 35.0% (z +9.6) | 73.9% / 53.5% (z +10.4) | 61.9% / 45.8% (z +10.3) | 15.9% / 11.6% (z +2.7) | 21.0% / 16.8% (z +2.2) |

**Readings.**

1. **The reading rests on one word.** Removing the expression sentence, or fixing it to "unclear",
   removes nearly all agreement (family 53.0% → 20.3% / 21.3%; the residual z +3.8 comes from the
   action and scene words), and the reader's output collapses to surprise/neutral (514/368 of
   1,012). The other three clauses contribute 1–3 pp each. In effect the pipeline is "ask the
   describer for the facial expression and map that word to a family" — the same conclusion as the
   99.8% copy rate (finding 7), reached independently.
2. **The scene result was an artefact of the template.** Under the people-aware description, face
   rows are unchanged by construction and **scene agreement falls to its null**: valence sign 4.7%
   vs 3.4% (z +1.6), family 18.0% vs 17.3% (z +0.6); restoring action and posture gives 15.9% vs
   11.6% (z +2.7) and 21.0% vs 16.8% (z +2.2). The scene z +5.8 in the headline table is agreement
   between the prompt and an *invented* expression — which agrees with the prompt because most
   prompts (66% joy) and most invented expressions (80% smile) are positive.
3. **The people-count token matters in the other direction too.** Deleting "A drawing of 0" from
   every description raises raw rates and nulls together (scene sign 63.5% vs 50.9%, z +5.0): the
   "0" pulls scene readings toward neutral. Raw rates move; z barely does — one more reason to read
   every number against its null.
4. **Corrected statement of finding 2.** For drawings the describer can read a face in, agreement
   is far above chance; for drawings it cannot, this reader finds nothing above chance once the
   invented clause is removed. The contrast is not "faces more than scenes" but "faces, and only
   faces, for this reader". Whether scene drawings hold a feeling a *person* can read is precisely
   what the human check tests; the design of a scene-capable describer is the main item of further
   work.


### 3. The specificity check passes, but it is a weak check

On the 405 prompts the text reader labels neutral, only the valence–arousal measure is informative:
**76.6% vs a null of 76.6%, z +0.3** (clustered null z −0.1). Valence-sign and family agreement are
degenerate there — every prompt shares the neutral label, so permutation cannot change them and
their z is identically zero by construction, not by measurement (the analysis now detects this from
the null's own spread and prints no z). Two further caveats (`audits.py`): the set is better
described as "prompts the text reader could not read affect from" than "prompts with no feeling" —
**68 of 405 (16.8%) contain a plain English affect word** (calm ×10, content ×8, tired ×7,
relaxed ×6, stress ×6 …) and 2 consist of a redacted name alone; on the **cleaned 335** the VA z is
+0.04, still at its null. The prompt-side VA points are nearly constant on this subset (sd 0.11 vs
0.51 on the emotional subset), so observed ≈ null is expected here; the check rules out a gross
artefact, no more.

### 4. Two image readers, scored like for like

Same prompt reader (GoEmotions), same 607 emotional records, same four measures and the same
shuffles, varying only the image reader (`method_comparison.py`):

| Image reader | Valence sign | Family | Top-3 overlap | VA |
|---|---|---|---|---|
| Describe-then-extract (BLIP-VQA → NLI) | 64.0% vs 45.6% (z +11.1) | **53.0%** vs 38.8% (z +10.3) | 50.6% vs 39.4% (z +11.6) | 83.8% vs 77.3% (z +12.2) |
| Direct CLIP zero-shot | 31.1% vs 18.6% (z +9.9) | **22.4%** vs 12.2% (z +11.1) | 26.4% vs 20.2% (z +11.2) | 73.3% vs 70.1% (z +10.2) |

Family-agreement difference **+30.6 pp**, clustered bootstrap 95% CI [+25.5, +35.6]; cluster-level
sign-flip test p < 0.0001 (unclustered exact McNemar p = 3 × 10⁻³⁵, optimistic because repeats are
not independent). The two readers agree with each other on only 32% of top-1 families; direct CLIP
calls 283 of the 607 images neutral. **Reading.** Neither reader has ground truth, so this shows the
two readers disagree, with describe-then-extract far closer to the text reader — not that it is
more accurate. Note that CLIP's family z (+11.1) is *higher* than describe-then-extract's (+10.3)
because CLIP's null is lower and tighter: z measures distance from chance, not level of agreement;
the paired tests on the rates are the right comparison. The earlier published figures (49.3% vs
25.3% family on 608 records, NLI on the prompt side, v1 overlap formula) are kept in
`method_comparison.json` as the historical v1 record and are not comparable with the table above.

### 5. Repeated prompts: more consistent than chance, far from fixed

87 prompts were drawn two or more times (336 records, 33% of the data; largest "happy" ×42; 43 of
the 87 groups are pairs). These pool the same text typed by different visitors and re-submissions
by one; generation parameters were never recorded. Question: given the same prompt text, how stable
is the emotion the pipeline reads from the drawings? (`data_audit_consistency.py`)

| | observed | permutation null (10,000 draws, seed 7) | z | p |
|---|---|---|---|---|
| same family within a group (mean over groups) | **68.8%** (CI [63.8, 73.9]) | 59.4% (sd 2.1) | +4.5 | 0.0001 |
| same valence within a group | 74.5% | 63.7% (sd 2.2) | +5.0 | 0.0001 |
| groups fully consistent | 28 of 87 | 14.5 (sd 3.2) | +4.2 | 0.0002 |

Half the groups are pairs, whose modal agreement cannot fall below 50% — a bare "69%" overstates
the instability. This measures the stability of the whole prompt → image → reader chain, not the
generator alone: with no reliability estimate for the reader, an unknown share of the variation is
measurement noise. e.g. "happy" ×42 → 34 joy / 7 neutral / 1 surprise; "curious" ×12 → 5 neutral /
4 joy / 2 surprise / 1 anger.

### 6. Per family, the ladder is three families in practice

Prompt families on the 607 emotional records: joy 402, sadness 99, surprise 77, fear 16, anger 12,
disgust 1. Image-reader recall by prompt family: joy 64.9% [58.7, 70.3], sadness 40.4% [30.9, 51.2],
anger 50.0% (n = 12), surprise 19.5% [11.4, 28.1], fear 0% (n = 16), disgust 0% (n = 1). Across all
1,012 records the image reader **never returns disgust and returns fear 4 times**. The "surprise"
family is largely curiosity-mapped prompts under the standard GoEmotions → Ekman map. Strong claims
are therefore confined to overall agreement and the face/scene contrast.

### 7. The describer is the weak link — measured, not assumed

* **Hallucinated faces.** The describer answers the expression question for every image; for the 414
  no-people drawings it names an expression in 406 and "smile/smiling/happy" in 332.
* **Positivity.** It reports a smiling or happy expression for **57% of the 591 face-classified
  records** (337/591) and for 66% of all expression answers corpus-wide (669/1,012). State the
  denominator whenever this is quoted.
* **Copy rate.** "Describe, don't ask" is a weaker separation than it sounds: where the expression
  answer itself names an affective state (happy, sad, angry, surprised, calm … — **41% of records**),
  the image reader's top-1 equals the family that word implies **99.8% of the time** (417/418); over
  all expression answers, 68.6%. The NLI stage largely relays the expression word; the advantage
  over direct CLIP may lie in BLIP-VQA being a better affective reader of line art rather than in
  the two-stage architecture.
* **Error taxonomy** (`error_taxonomy.py`; `ERROR_TAXONOMY.md`). Of the 38 high-confidence
  disagreements (both readers ≥ 0.8, families differ — a census, every drawing inspected), the
  describer accounts for 19 (9 invented a face or expression, 10 misread one), the image reader for
  5, the prompt side for 12 (11 mixed or ambiguous prompts, 1 prompt-reader error), and the drawing
  genuinely not depicting the prompt for 2. A people-count of 0 predicts the "invented face" mode
  (7 of 9). Visitors list feelings without connectives ("tired proud happy"), so mixed-feeling
  prompts are a prompt-side limitation of any single-label reader.

---

## Robustness

* **Distinct prompts (763; 452 emotional).** All-emotional measures hold (valence sign 62.2%, z +9.9;
  family 51.3%, z +9.3). Face holds (71.8%, z +8.4; family 59.9%, z +8.1). **Scene weakens**: valence
  sign 37.3% (z +3.5), family 30.8% (z +2.6, n 205 → 133) — the family cell does **not** survive
  Holm–Bonferroni and should be treated as suggestive. The single-valence subsets have degenerate
  sign nulls and are not re-testable; the negative-prompt family null is not degenerate (z +2.1).
* **Ten comparisons fail Holm at family-wise 0.05**, all expected: the two control cells, the
  single-valence VA/overlap cells, and distinct-prompt scene family.
* **Seeds.** Null means are stable to a fraction of a point across seeds; z moves with the 300-draw
  estimate of the null sd (emotional valence sign: +11.2 to +12.2 over seeds 1–5).
* **Redaction is inert on the prompt side**: no top-1 family changes and no GoEmotions probability
  moves by more than 0.012. Its effect on the downstream measures was not separately verified; the
  two records that reduce to "[name]" were shown not to affect the control (finding 3).
* **Letter case.** Prompt identity (`dedup_key`) is case-insensitive but GoEmotions read the text as
  typed, so 12 groups hold slightly different prompt distributions and two straddle the emotional /
  neutral split ("Ok" ×2 emotional vs "ok" ×6 neutral; "Hopeful" neutral vs "hopeful" ×3 emotional).
  This does not change any count above but means the split is not invariant to case.

## What is NOT claimed

* **A positive-versus-negative direction.** Within a single-valence subset the sign null is
  degenerate; the raw VA gap is a base-rate effect; the direct-CLIP reader points the opposite way.
  The two readers cannot settle it — that is what the human-rating study is for.
* **Anything about fear, disgust or surprise** (n ≤ 16, a class largely of curiosity-mapped prompts;
  the reader never returns disgust). With no colour condition, none of this can be attributed to the
  absence of colour.
* **Human validity.** No component of the pipeline has yet been compared with a person looking at the
  drawings. `human_check.py` draws a 120-drawing sample stratified on the describer's output and
  scores the describer's people count, its expression word and the reader's valence against a
  blind single coder with Wilson 95% CIs, and re-runs the face/scene contrast on the human split.
  The sample and sheets exist; the coding is the outstanding step and its result will be reported
  here when done.
* **Anything about the generator alone** (finding 5 bounds the whole chain).

## Data accounting — nothing left out

All 1,025 images were processed with no unhandled error — a robustness statement, not an accuracy
one (see finding 7). 13 pre-festival developer tests are excluded from analysis, still processed.
Every analysed record is in exactly one emotional / neutral-labelled group (607 / 405) and one
face / scene group (591 / 421), and all groups are reported. Records are not people: 249 repeat an
earlier prompt, so the number of contributors is unknown and no greater than 763; the installation
accepted free text, and a substantial minority of entries are object or scene requests.

## Reproducibility and testing

`bash test.sh` runs the environment, data, redaction, every analysis script, a live three-image
pipeline run, the numeric regression (`test_numeric.py`: 49 pinned values and unit tests of the
metric module) and the figures, and exits non-zero on any failure. Every constant and measure has
one definition, `emoviz/metrics.py`, imported by the analysis, the significance test, the demo app
and the tests. Degenerate nulls are detected automatically from the null's zero spread.

## Corrections log

* **1 Sep 2026.** Positive-vs-negative direction withdrawn (degenerate null). A label-space mismatch
  that deflated the direct-CLIP top-3 overlap fixed (15% → 23%). Face rule changed to token
  matching. Literature counts corrected to 97 screened / 24 excluded / 73 retained / 8 themes.
* **9 Sep 2026.** Family agreement quoted as 53.0% (322/607), not 53.1%. Consistency null scripted:
  68.8% vs 59.4%, z +4.5 (the earlier 59.1% / z +4.9 was an unscripted 300-draw estimate). The
  face/scene mechanism rewritten (template asserts a face; 414/406/332). Smiling rate given with
  its denominator (57% of face-classified; 66% corpus-wide). Like-for-like reader comparison
  replaces the v1 figure as the primary comparison (53.0% vs 22.4%, not 49.3% vs 25.3%). Distinct-
  prompt face z corrected to +8.4; scene family z +2.6 flagged as failing Holm. Degenerate-null
  detection made automatic. Figures regenerated from JSON with descriptive titles. Redaction
  decision table moved out of the repository. "Independently reviewed" replaced by this log.

## Files
- `analysis_final.py` → `analysis_final.{csv,json}`; `significance.py` → `RESULTS_significance.txt`;
  `data_audit_consistency.py` → `consistency.json`; `inference.py` → `inference.json`;
  `method_comparison.py` → `method_comparison.json`; `audits.py` → `audits.json`;
  `error_taxonomy.py` → `error_taxonomy.json`, `ERROR_TAXONOMY.md`; `ablate_nli.py` →
  `ablation/summary.json`; `human_check.py` → `human_check/`; `make_figures.py` → `figures/`.
- `describe_extract.jsonl` — full pipeline output (1,025 records incl. pre-tests).
- `RESULTS_describe_extract.md` — the method build, incl. rejected approaches.
