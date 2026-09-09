# What was built — the technical story (for the 4 Sep presentation)

## 1. The problem
You can check whether an AI drew "a red car" — look for a car, check it's red.
You cannot do that with "tired but happy". There is no object to find.
**So there was no way to check how far the emotion read from a drawing agrees with the emotion read from the words. That is what this builds.**

## 2. The data was messy (real engineering, worth a slide)
1,025 drawings. Three problems had to be solved before any analysis:
- **Three filename systems** in one folder (`img_00001.PNG`, `img_200.PNG`, `img_t1000.PNG`),
  plus two lowercase `.png`. A naive loader resolves **under 20%** of files; the robust one 100%.
- **Hidden C2PA metadata** inside every PNG gave a creation timestamp → revealed that
  **records 1–13 were made before the festival** (developer tests). Excluded from results,
  still processed, so nothing is silently dropped.
- **87 prompts were drawn more than once.** Looked like a nuisance; became a finding.

## 3. The first attempt failed — and catching it mattered
Asked CLIP directly "which emotion is this drawing?".
- Everything returned **neutral** — the prompts described the medium ("black and white line
  drawing"), which handed 'neutral' an unfair advantage.
- Fixed the wording, re-ran, got answers — then **looked at the actual images**:
  arms-up celebration → "anger 73%"; hands on a keyboard → "disgust 82%".
- **Threw the result away rather than reporting it.**

## 4. The redesign — describe first, then read
| Stage | What happens |
|---|---|
| Describe | 5 plain questions to the image: expression, action, posture, how many people, scene |
| Read | One model infers a feeling from that description; a different model reads the words |
| Compare | Four measures of closeness, strict to loose |

The vision model is **never** asked for an emotion.

## 5. Four approaches tried and rejected (evidence, not opinion)
| Tried | Why it failed |
|---|---|
| GoEmotions on image descriptions | Collapses to "neutral" 95%+ — it needs first-person feeling words |
| Single caption → emotion | Captions too short ("a man with hands in the air") → collapses to "surprise" |
| Qwen 2.5-VL (3B) | 7 GB fp16 exceeded a 16 GB laptop; **4 h 45 min, zero progress** |
| Florence-2 | Incompatible with transformers 5.14 |
| **BLIP-VQA (chosen)** | 0.4B, ~1.5 s/image; its "facial expression" answer is exactly the cue needed |

## 6. How the numbers are kept honest (the strongest section)
- **Null baselines** — every metric compared against 300 shuffles that pair each drawing with a
  random stranger's sentence.
- **A specificity check** — 405 prompts are labelled neutral by the text reader ("pigs", "mickey mouse").
  On them valence–arousal agreement is 76.6% against a chance level of 76.6% (z +0.3) — indistinguishable
  from chance. Sign and family are degenerate there, so the check rests on one measure.
- **Duplicate robustness** — 249 records repeat an earlier prompt; re-run on the 763 distinct prompts,
  the overall and face results hold and the scene result weakens (z +3.5).
- **Baseline comparison** — measured against the old CLIP method like for like: same prompt reader, same 607 records,
  with a paired test clustered on prompt identity.
- **Confidence intervals** on every rate (clustered bootstrap), and a clustered permutation test of the face/scene
  difference: +30.9 pp [+22.6, +40.6], p = 0.0001.

## 7. Chance is not zero (the discovery that changed the reporting)
- The similarity measure **cannot fall below 41%** — that is its mathematical floor.
- Two **randomly paired** items already score about **76%**.
- So a score of 71% looks like a pass but is **worse than luck**.
- That measure gives ~84% for faces *and* scenes, so it cannot tell them apart.
→ Valence-sign and emotion-family agreement became the headline; the raw score is now
  always shown against its measured chance line.
**Slide idea:** one bar marked 41 (floor) · 76 (chance) · 84 (result).

## 8. The four findings
1. **Agreement is much higher where the describer reports a face** — 73.9% valence-sign agreement
   for face-classified drawings, 42.9% for scene-classified. Both above chance; the difference is +30.9 pp
   [+22.6, +40.6], p = 0.0001; the split is the describer's own, and under a people-aware template the scene reading
   falls to its null (4.7% vs 3.4%, z +1.6): faces, and only faces, for this reader.
2. **Specificity check passes** — prompts the text reader labels neutral sit at chance (one measure informative).
3. **The same words do not reliably give the same reading** — across repeated prompts the reader returns the
   same family for 68.8% of drawings in a group, against 59.4% by chance (z +4.5); 28 of 87 groups fully
   consistent against 14.5 by chance. More consistent than chance, far from fixed.
4. **Describe-then-extract agrees far more closely with the prompt reader than direct CLIP** — 53.0% vs 22.4%
   emotion-family agreement, like for like (+30.6 pp, p < 0.0001).
5. **The reading rests on one word** — removing the describer's expression sentence collapses family agreement
   from 53.0% to 20.3%; the other clauses move it 1–3 pp (template ablation, NLI stage only re-run).

## 9. Built beyond the analysis
- **Live demo app** — runs the real pipeline in a browser; every number shown against chance.
- **Documented name redaction** — about 78% of prompts are lowercase, so detection needed a dictionary,
  a name gazetteer and phrase patterns, not capitals. 8 records held real names → `[name]`.
  Illness and grief content kept (supervisor direction). **Redaction changed no top-1 prompt
  family (largest probability shift 0.012).**
- **An automated self-test**, including a numeric layer that pins every headline value to the result file
  that produces it; figures are generated from the same files.

## Suggested 15-minute running order
1. The problem (red car vs "tired but happy")
2. The data and its three traps
3. The first attempt failed — and how it was caught
4. The architecture — one diagram
5. Rejected approaches — one table
6. **How it is kept honest — the "pigs" control**
7. **Chance is not zero — the 41/76/84 bar**
8. The four findings
9. Live demo (2 min)
10. Limits and the next study

Spend the most time on **6 and 7** — that is where it reads as research rather than as running code.

## Limits to state yourself, before you are asked
- Both readers are automatic and they **disagree with each other** (one skews negative on line
  art; the other reads 57% of readable faces as happy). Only human ratings can settle it.
- The face/scene split is partly circular: it is governed by the describer's people-count answer, and the
  emotion is read from the same description — which asserted an expression even for drawings with no person.
  Described honestly, those drawings give nothing above chance for this reader.
- No positive-vs-negative direction is claimed — the evidence conflicts, so it was retracted.
