Create a 10-slide presentation, 16:9, one artboard per slide.

# What this is

The final assessed presentation for an MSc Artificial Intelligence dissertation at the **University of Sheffield, School of Computer Science**. It is delivered to academic markers in a viva setting on 4 September 2026. The speaker is Shre Hari Prem Anandh; the supervisor is Dr Chaona Chen.

This is a formal university assessment, not a product pitch. It must read as scholarly: sober, evidential, restrained. A marker should look at it and see research, not marketing. Ten minutes total — nine slides of speaking plus a 90-second live software demonstration at slide 9.

# Design direction

- Editorial and academic. A research journal or a university department, not a startup deck.
- One idea per slide, generous whitespace, nothing decorative.
- Serif headings, clean sans body. Body text no smaller than 12pt equivalent — assume a projector viewed from the back of a lecture room.
- A single restrained accent used sparingly, plus one contrasting colour reserved for the "not established" material on the final slide.
- Slides **1, 4, 7, 9 and 10** should be visually distinct from the rest — a darker or inverted ground works well. These are the emphasis beats: the title, the contribution, the rigour argument, the demonstration, and the conclusion.
- Every slide except the title carries a small uppercase section label above its heading (given below as EYEBROW).

# Avoid

- No icons, stock photography, gradients, or decorative shapes.
- No accent stripes or coloured bars along the edge of slides or cards.
- No centred body text — centre only titles.
- Do not turn the statistics into oversized decorative numerals. These are research findings and must be presented as evidence: tables, labelled rows, plain figures.

# Diagrams required

**Slide 5 — architecture.** Two rows of connected boxes.
Upper row: `Drawing` → `BLIP-VQA` → `BART-MNLI` → `Image reading`.
Lower row: `Prompt` → `GoEmotions` → (one long arrow) → `Prompt reading`.
Beneath both, a full-width bar labelled **Compare**, listing the four measures across it.
The two right-hand boxes are the outputs — give them slightly more emphasis.

**Slide 7 — a horizontal scale** from 41 to 100 with three marked points: **41** ("metric floor"), **76** ("random pairings"), **84** ("observed"). Shade the region below 76 to show it is below chance. This graphic carries the argument, so give it room.

**Slide 8 — a four-column results table.** Left-align every column, and align each header with its own data.

# Critical — do not rewrite the wording

Every claim below has been checked against the underlying statistics and the phrasing is deliberately precise. Reproduce the text as given. Specifically:

- Never change **"agreement"** to "alignment", "fidelity", "accuracy" or "matching".
- Never say a drawing **"conveys"** or **"carries"** an emotion. This study measures agreement between two automatic readers, not what a human perceives.
- Keep every **"vs null"** figure and every **z-score** attached to the number it belongs to.
- Keep the footnotes. They are not filler — they are what makes the claims defensible under examination.

---

# SLIDE 1 — Title

**Visualising Emotion**
*Measuring agreement between a written feeling and an AI-generated drawing*

Shre Hari Prem Anandh
MSc Artificial Intelligence · School of Computer Science
University of Sheffield · Supervisor: Dr Chaona Chen

4 September 2026

---

# SLIDE 2
EYEBROW: The problem
**Object prompts can be checked. Feelings cannot.**

Two side-by-side panels:

*"a red car"* — Is there a car? Is it red? The prompt names objects, so existing metrics can score it.

*"tired but happy"* — No object to find, no answer key, and the feeling is mixed. Existing metrics do not transfer.

Below, a highlighted block:

**Research question.** To what extent does an automatic image-emotion reader agree with prompt-derived emotion labels for AI-generated monochrome drawings, and how does that agreement vary by visual content and by repeated prompts?

Sub-questions: (i) does agreement exceed a random-pairing baseline? (ii) does it differ for face-classified and scene-classified drawings? (iii) how stable is the image reading when the same prompt is drawn again? (iv) does describe-then-extract agree more than reading emotion from the image directly?

FOOTNOTE: The question is deliberately narrower than "does the drawing convey the feeling" — see the closing slide.

---

# SLIDE 3
EYEBROW: Literature
**Four established areas, and the space between them**

Four labelled rows:

**Emotion in text** — Well established. GoEmotions supplies a 27-category taxonomy and a classifier; but short first-person self-report is the hardest register.

**Emotional image generation** — Well established. Systems generate images to carry a chosen emotion, and colour is reported as the principal carrier of affect.

**Text-to-image evaluation** — Well established for OBJECTS. CLIPScore and VQAScore measure whether the picture contains what the prompt named.

**Reading emotion from an image** — Weak. Vision-language models are positively biased and order-sensitive readers of affect.

Highlighted block beneath:
**The gap:** no study has measured whether the emotion in a person's own unedited self-report is recoverable from the drawing generated from it — in monochrome line art, where the reported colour channel is absent.

FOOTNOTE: 97 papers screened; 73 retained as core evidence across eight themes. Colour is cited as motivation only — this study has no colour-control condition.

---

# SLIDE 4 — emphasis slide
EYEBROW: Contribution
**Similarity, not matching**

Pull quote, given prominence:
*"Asking whether the image emotion matches the text — right or wrong — is too simplistic. Emotion is subjective, there is no ground truth, humans disagree and models are noisy. Ask how similar the two emotions are."*
— Supervisory direction, 30 July 2026

Two contrasting panels:

**Conventional** — One-to-one match. The predicted label is right or wrong; accuracy is reported against an assumed ground truth.

**This project** — A four-level similarity ladder over emotion families. "Happy" and "excited" are counted as close, not as a miss — and every level is referenced to chance.

Closing line, given weight:
**This is the novel element: the field reports one-to-one accuracy; this study reports graded, chance-referenced similarity.**

---

# SLIDE 5
EYEBROW: Methodology
**Describe the image, then read the feeling from the description**

[architecture diagram as specified above]

Box contents:
- **Drawing** — 1,025 monochrome line drawings
- **BLIP-VQA** — five factual questions → one neutral sentence
- **BART-MNLI** — zero-shot over seven emotion families
- **Image reading** — top-3 emotions
- **Prompt** — the visitor's own words
- **GoEmotions** — 28 labels collapsed to the same seven families
- **Prompt reading** — top-3 emotions

Compare bar: **Compare → four-level similarity ladder, every level against a 300-shuffle random-pairing null**
Listing: valence-arousal distance · valence-sign agreement · emotion-family agreement · top-3 overlap

FOOTNOTE: The image model is asked only factual questions. Caveat stated in the write-up: "what is the facial expression?" often returns a feeling word, so the separation is weaker than it appears.

---

# SLIDE 6
EYEBROW: Data
**1,025 real self-reports, and what it took to use them**

Four figures across the top:
- **1,012** — analysed records (13 pre-festival tests excluded)
- **607 / 405** — prompts the text reader labels emotional versus neutral — the specificity set
- **591 / 421** — face-classified versus scene-classified drawings
- **87** — prompts drawn more than once, covering 336 records

Two panels beneath:

**Data engineering**
- Three incompatible filename schemes in one folder — a naive loader resolves under 20%.
- C2PA signing timestamps recovered from inside each PNG identified 13 pre-festival developer tests.
- Ran to completion on all 1,025 images with no unhandled errors — a robustness statement, not an accuracy one.

**Data pre-processing**
- Eight records contained names of private individuals; these were replaced with a placeholder.
- Detection combined a 7,944-name gazetteer, a 236,000-word dictionary and naming phrases — about 78% of the corpus is lower case, so capitalisation alone would miss most names.
- Verified inert: re-running the prompt reader changed no emotion label.

---

# SLIDE 7 — emphasis slide
EYEBROW: Evaluation design
**Two checks that decide whether any number means anything**

Two panels:

**1 · A random-pairing null** — Within each subset the image side is shuffled and re-paired against the untouched prompts, 300 times, with a fixed seed. Every figure I report is quoted against its own null, so a result counts only insofar as it exceeds chance.

**2 · A specificity check** — 405 prompts are labelled neutral by the text reader — "pigs", "mickey mouse". On these the valence-arousal metric returns 76.6% against a null of 76.6%, z = +0.3. The pipeline reports agreement only where the prompt reader finds an emotion.

Then, with a heading **"And the scale does not start at zero"**, the 41 / 76 / 84 scale graphic described above.

FOOTNOTE: Consequence: a valence-arousal score of 71 reads as a pass but is below chance. Reporting therefore leads with valence-sign and family agreement, which the metric cannot substitute for.

---

# SLIDE 8
EYEBROW: Results
**Agreement is above chance, and strongest for face-classified drawings**

Table — four columns: Subset | Valence-sign agreement | Emotion-family agreement | Verdict

| Emotional prompts (n=607) | 64.0% vs null 45.6% z +11.1 | 53.0% vs null 38.8% z +10.3 | Well above chance |
| Face-classified (n=402) | 73.9% vs null 53.5% z +10.4 | 61.9% vs null 45.8% z +10.3 | Strongest |
| Scene-classified (n=205) | 42.9% vs null 29.6% z +5.8 | 35.6% vs null 26.2% z +4.4 | Above chance, weaker |
| Neutral-labelled (n=405) | — degenerate by definition | — degenerate by definition | Specificity check |

Three labelled rows beneath:

**Repeated prompts** — Given the same prompt text, the image reader returns the same emotion for 68.8% of drawings within a group, against a permutation null of 59.4% (z +4.5). More consistent than chance but far from fixed; this measures the whole prompt→image→reader chain, and the reading is not deterministic in what the reader recovers.

**Method comparison** — Like for like (same GoEmotions prompt reader, same 607 records, only the image reader varied): describe-then-extract 53.0% family agreement against direct-CLIP 22.4%, +30.6 pp, clustered 95% CI +25.5 to +35.6, p < 0.0001. The earlier 49.3% vs 25.3% figure (608 records) used BART-MNLI on the prompt side, not the GoEmotions reader used above.

**Robustness** — Re-run on the 763 distinct prompts, the overall and face results hold (z +8.4 to +10.8). The scene result weakens substantially, to 37.3% (z +3.5; family z +2.6).

FOOTNOTE: The face–scene difference is significant: clustered permutation p = 0.0001; 95% CI on the difference +22.6 to +40.6 pp (valence sign). Both rates are also reported against their own nulls.

---

# SLIDE 9 — emphasis slide
EYEBROW: Demonstration
**The pipeline, running live**

Three numbered steps:
1. **Choose a drawing** — from the festival dataset, or upload an image
2. **Watch it described** — the five factual answers, then the emotion read from them
3. **Compare** — both readings, and the score against the chance line

Closing line: Every figure the interface shows is referenced to the measured chance line, and nothing a visitor types is stored.

Leave this slide uncluttered — the speaker switches to live software here for 90 seconds.

---

# SLIDE 10 — emphasis slide
EYEBROW: Conclusion
**What this establishes, and what it does not**

Two contrasting panels — the first affirmative, the second in the reserved contrasting colour:

**Established**
- Prompt-reader and image-reader agreement is well above chance on every metric.
- Agreement is substantially higher for face-classified than scene-classified drawings.
- The same prompt does not reliably yield the same recovered emotion (69% vs 59% null).
- Describe-then-extract agrees more than reading emotion from the image directly.

**Not established**
- What a human viewer perceives — both readers are automatic, and they disagree with each other.
- That the face–scene split reflects faces as such — the gap is significant (p = 0.0001), but the split is the describer's own classification.
- That scene-classified drawings hold a feeling this reader can find: under a people-aware description their agreement sits at chance (z +1.6).
- Any effect of colour — the corpus is monochrome but there is no colour condition.
- Any positive-versus-negative direction; that claim was withdrawn.

Beneath: **Future work:** human validation of both readers · sketch-trained describers · a formal test and confidence intervals for the face–scene difference

Final line, given weight:
**The contribution is a chance-referenced similarity measure for emotional agreement — not a new classifier.**

Then, quietly: *Thank you — questions welcome*
