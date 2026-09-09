---
title: "Supervision Meeting — Thursday 10 September 2026"
subtitle: "Visualising Emotion · Shre Hari Prem Anandh · Supervisor: Dr Chaona Chen"
date: "Submission: Wednesday 16 September, 15:00 (6 days)"
---

## 0. Open (30 seconds)

> "Thank you for the presentation feedback, it went well. Since the fourth I've done one thing: I audited the whole project against the marking criteria as if I were the marker, and fixed everything I found. That produced five new analyses and one finding that changes how I describe the main result. I'd like to show you that finding first, then the human check I'm about to run, and I have three questions."

Then go straight to Section 2. Do not list everything in Section 1 unless she asks what changed.

---

## 1. What is new since 4 September (say it as a list only if asked)

| Added | What it gives |
|---|---|
| Confidence intervals on every rate (clustered on prompt groups), Cohen's kappa, Holm–Bonferroni across all 36 comparisons | Every number now has an interval; 26 of 36 comparisons survive correction; every headline does |
| Consistency null, scripted | 68.8% within-group agreement vs 59.4% by chance (z +4.5) — the old 59.1 / +4.9 was an unscripted estimate |
| Like-for-like method comparison with a paired test | Describe-then-extract 53.0% family agreement vs direct CLIP 22.4%, +30.6 pp, clustered p < 0.001 |
| Control audit | 68 of the 405 "neutral" prompts contain a plain affect word; on the cleaned 335 the check still sits at chance (z +0.04) |
| Describer audit and copy rate | 414 of 421 scene records report no person; 406 still name an expression; 332 say "smile". Where the expression word names an emotion, the reader copies it 99.8% of the time |
| Error taxonomy | 38 confident disagreements, every drawing inspected: 19 describer, 5 reader, 12 prompt side, 2 generator |
| Template ablation | Section 2 — the finding to lead with |
| Human check | 120-drawing blind sample drawn, contact sheets made; I code it this week (Section 3) |
| Engineering | One shared definition of every measure; 54 pinned numeric tests; every figure and table generated from the result files |

---

## 2. The finding to lead with: the description-template ablation

**Say it in plain words first:**

> "You asked me in July to describe first and extract second, so the vision model is never asked for an emotion. I've now tested how much that separation actually buys, and the honest answer is: less than it sounds.
>
> The description I feed to the language model has five parts — expression, action, posture, how many people, what's in the picture. I rebuilt every description with one part removed at a time and re-ran only the last step. Taking out action, posture or scene changes the result by one to three points. Taking out the facial-expression sentence removes almost all of the agreement: family agreement drops from 53% to 20%. So the reading rests on one word — what the describer says the face is doing.
>
> The second half is about scenes. The template always says 'the person is doing X, the facial expression is Y', even when the describer has just said there are no people. For 414 of the 421 scene drawings it reported no person and still named an expression, usually 'smile'. When I describe those drawings honestly — just 'a drawing showing mountains' — the face results don't move at all, and the scene results fall to chance: 4.7% valence-sign agreement against 3.4% by chance.
>
> So the result I presented as 'faces agree much more than scenes' is really 'faces, and only faces, for this reader'. The scene number in my table was agreement with an expression the describer invented."

**Why this is good news, if she looks worried:**

> "It's a sharper and more defensible result than the one I had. It survives every test, it explains the circularity you and I discussed instead of just flagging it, and it tells me exactly what the next experiment has to be: either a person looks at the scene drawings, or the describer has to read affect from composition rather than from a face."

**The numbers (only if she asks):**

| Template | All emotional: sign | family | Face: sign | Scene: sign | Scene: family |
|---|---|---|---|---|---|
| Baseline (as presented) | 64.0 / 45.6 (z +11.1) | 53.0 / 38.8 (z +10.3) | 73.9 / 53.5 | 42.9 / 29.6 (z +5.8) | 35.6 / 26.2 (z +4.4) |
| Expression sentence removed | 15.3 / 11.4 (z +5.1) | 20.3 / 16.6 (z +3.8) | 18.9 / 14.7 | 7.6 / 4.7 | 9.3 / 6.4 |
| Expression fixed to "unclear" | 15.1 / 10.8 | 21.3 / 17.5 | 17.5 / 12.8 | 10.0 / 6.6 | 13.7 / 11.2 |
| Action / posture / scene removed | 62–64 | 50.6 / 51.4 / 53.4 | ~73 | ~40 | ~31–36 |
| **People-aware** ("A drawing showing {scene}." when no person) | 51.7 / 36.9 (z +10.1) | 47.1 / 34.5 (z +8.8) | **73.9 (unchanged)** | **4.7 / 3.4 (z +1.6)** | **18.0 / 17.3 (z +0.6)** |

Each cell is observed / chance. A control re-run of the unchanged template reproduced every baseline number exactly (0 of 1,012 readings changed), so these are template effects, not noise.

---

## 3. The human check (what I do this week)

> "Everything in the project so far is one model agreeing with another model. This is the first point where a person looks at a drawing.
>
> I've drawn 120 drawings, stratified on what the describer said: 40 where it read a face, 40 where it reported no person, and every drawing where its people answer was vague. They're laid out on six numbered sheets with nothing else on them — no prompt, no description, no model output. I code each one for four things: is a person drawn, can I read an expression, is the feeling positive, negative or neither, and which family.
>
> Scoring gives me the describer's people-count accuracy, how many of its 'smiling' answers have a real smile behind them, the reader's valence agreement with me, and — the point of it — the face-versus-scene contrast on **my** split instead of the describer's, which is the one estimate that breaks the circularity."

**Limits to say before she does:** one coder; I know the project, so I am not naive; 120 is a pilot for the rated study, not the study.

---

## 4. Corrected headline numbers (cheat sheet)

| | Observed | Chance | z | 95% CI |
|---|---|---|---|---|
| Emotional prompts (n=607), valence sign | 64.0% | 45.6% | +11.1 | [58.6, 68.8] |
| Emotional prompts, family | 53.0% (322/607) | 38.8% | +10.3 | [47.3, 58.7] |
| Face-classified (n=402), valence sign | 73.9% | 53.5% | +10.4 | [68.3, 79.2] |
| Scene-classified (n=205), valence sign | 42.9% | 29.6% | +5.8 | [33.1, 51.1] |
| Face − scene difference, valence sign | +30.9 pp | | p = 0.0001 | [+22.6, +40.6] |
| Neutral-labelled prompts (n=405), VA | 76.6% | 76.6% | +0.3 | (only informative measure) |
| Describe-then-extract vs direct CLIP, family | 53.0% vs 22.4% | | p < 0.001 | [+25.5, +35.6] |
| Repeated prompts (87 groups), same family | 68.8% | 59.4% | +4.5 | [63.8, 73.9] |
| Cohen's kappa, emotional / face / scene | 0.23 / 0.30 / 0.13 | | | fair / fair / slight |

Distinct prompts only (763): face sign 71.8% (z +8.4); scene sign 37.3% (z +3.5), scene family 30.8% (z +2.6, does **not** survive Holm).

**Wording to keep:** "agreement between the prompt reader and the image reader", never "accuracy"; "valence-sign agreement", never "mood direction"; "53.0%", not 53.1; "more consistent than chance but far from fixed", never "unstable".

---

## 5. What I still cannot claim (say these before she finds them)

1. **Anything about what a person sees.** Every number is two readers agreeing. The human check is the first step; the rated study is the real one.
2. **A positive-versus-negative direction.** Inside a single-valence subset the chance level is degenerate, and my two image readers point in opposite directions.
3. **Anything about colour.** No colour condition exists; the colour literature is motivation only.
4. **Anything about the generator alone.** The consistency result bounds the whole prompt-to-image-to-reader chain; I have no reliability estimate for the reader.
5. **Fear, anger, disgust.** n = 16, 12 and 1 on the prompt side; the reader never returns disgust. The seven-family ladder is really joy / sadness / neutral.

---

## 6. Questions for her (pick three)

1. **Framing.** "Is 'faces, and only faces, for this reader' the right way to state the main result, or would you rather I keep 'faces agree far more than scenes' as the headline and present the ablation as the qualification?"
2. **Second coder.** "The human check is one coder. Would you be willing to code the same 120 drawings, or suggest someone? A second coder gives me an inter-rater figure, which is the number a psychologist will ask for."
3. **People-aware template.** "The honest template changes the scene numbers but not the face numbers. Should it become the default and I re-run everything, or stay as the sensitivity analysis next to the main table? My instinct is to keep it as the sensitivity analysis, because the main table is what I presented and the ablation is the controlled comparison."
4. **Further work.** "For the scene drawings the next instrument is either a person or a describer that reads composition and posture rather than a face. You suggested sketch-specific models in July; I designed that and didn't run it. Is that the further-work item you'd want stated first?"
5. **Presentation feedback.** "Was there anything from the second marker I should act on before the 16th?"
6. **Contact.** "Can I email you once between now and the 16th if something in the human check surprises me?"

---

## 7. If she asks technical questions

- **"How do you know the ablation isn't noise?"** A control variant re-runs the unmodified template under identical conditions and reproduces every baseline number exactly; 0 of 1,012 top-1 readings change.
- **"Why not just fix the template and re-run?"** The demonstrator and the analysis must stay in parity, and the main table is what was presented; the ablation *is* the fixed template, run as a controlled comparison against the original, which is more informative than a single re-run.
- **"What is the copy rate?"** Where the describer's expression answer is itself an emotion word (41% of records), the reader's top family equals that word's family 99.8% of the time. The entailment stage relays the word.
- **"So is the two-stage architecture pointless?"** No: it still agrees with the prompt reader far more than direct CLIP does, like for like. But the advantage may lie in BLIP-VQA reading drawn faces well rather than in the architecture. An ablation that strips the emotion word from the expression answer before extraction would separate the two; that is further work.
- **"What does kappa 0.23 mean?"** Fair on the Landis–Koch scale. It is the same band human annotators reach on fine-grained emotion labelling of text; two models separated by a generator and a drawing were not going to beat the annotators of their own training data.
- **"Why Holm?"** I print 36 non-degenerate comparisons. Holm controls the family-wise error rate step-down; 26 survive at 0.05, and the ten that fail are the control cells, the single-valence VA cells and the distinct-prompt scene family, exactly the ones that should.
- **"What is a degenerate null?"** When every prompt in a subset shares one label, shuffling the drawings cannot change the score, so the chance spread is zero and there is nothing to test. The analysis now detects this from the null's own spread and prints no z.

---

## 8. Plan to submission (technical side)

| When | What |
|---|---|
| Thu 10 – Fri 11 Sep | Code the 120 drawings (about an hour), run the scorer, add the second coder if she agrees |
| Sat 12 Sep | Freeze all result files; final full test run; regenerate every figure and table |
| Sun 13 – Tue 15 Sep | Final checks and polish |
| Wed 16 Sep, before 15:00 | Submit |

## 9. Close

> "So the plan is: code the human check tomorrow, get the second coder in if you're willing, freeze the numbers by the weekend. Does that match what you'd expect at this point?"
