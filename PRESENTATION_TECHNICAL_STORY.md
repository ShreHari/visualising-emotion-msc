# What was built — the technical story (for the 4 Sep presentation)

## 1. The problem
You can check whether an AI drew "a red car" — look for a car, check it's red.
You cannot do that with "tired but happy". There is no object to find.
**So there was no way to check whether a drawing carried a feeling. That is what this builds.**

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
| Qwen 2.5-VL (3B) | 7 GB fp16 exceeded a 16 GB laptop; **4h45m, zero progress** |
| Florence-2 | Incompatible with transformers 5.14 |
| **BLIP-VQA (chosen)** | 0.4B, ~1.5 s/image; its "facial expression" answer is exactly the cue needed |

## 6. How the numbers are kept honest (the strongest section)
- **Null baselines** — every metric compared against 300 shuffles that pair each drawing with a
  random stranger's sentence.
- **A negative control** — ~400 prompts contain no feeling ("pigs", "mickey mouse").
  The method scores **exactly chance** on them. It only finds emotion where emotion exists.
- **Duplicate robustness** — 249 prompts repeat; re-run on unique prompts only, findings hold.
- **Baseline comparison** — measured against the old CLIP method on the same records.

## 7. Chance is not zero (the discovery that changed the reporting)
- The similarity measure **cannot fall below 41%** — that is its mathematical floor.
- Two **randomly paired** items already score about **76%**.
- So a score of 71% looks like a pass but is **worse than luck**.
- That measure gives ~84% for faces *and* scenes, so it cannot tell them apart.
→ Mood-direction and emotion-family agreement became the headline; the raw score is now
  always shown against its measured chance line.
**Slide idea:** one bar marked 41 (floor) · 76 (chance) · 84 (result).

## 8. The four findings
1. **Faces carry emotion, scenes barely do** — 74% mood agreement with a readable face,
   43% for scenes. Both beat chance; gap survives every check.
2. **Validity check passes** — non-emotional prompts land at chance.
3. **The generator is inconsistent** — identical words redrawn give the same emotion only ~69%
   of the time; only 32% of repeated prompts are fully consistent.
4. **The supervisor's architecture wins** — 49% emotion-family agreement vs 25% for direct CLIP.

## 9. Built beyond the analysis
- **Live demo app** — runs the real pipeline in a browser; every number shown against chance.
- **Documented name redaction** — 77% of prompts are lowercase, so detection needed a dictionary,
  a name gazetteer and phrase patterns, not capitals. 8 records held real names → `[name]`.
  Illness and grief content kept (supervisor direction). **Proved analytically inert:
  zero emotion readings changed.**
- **28 automated tests**, all passing.

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
- The face/scene split is partly circular: the split is defined by whether the model reported an
  expression, and the emotion is read from that same description.
- No positive-vs-negative direction is claimed — the evidence conflicts, so it was retracted.
