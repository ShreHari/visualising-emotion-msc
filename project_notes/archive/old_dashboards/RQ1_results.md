> **SUPERSEDED (15 Aug 2026).** Direct-CLIP-era analysis. The κ/matching framing and the positive-collapse direction claim were retracted after the describe→extract reader disagreed in the opposite direction (reader bias, see RESULTS_final.md — only the human study can adjudicate). Kept for the project history / methods chapter.

# RQ1 Results — Text→Image Emotional Fidelity

**Pipeline (v2):** GoEmotions (RoBERTa) text emotion ↔ CLIP ViT-B/32 zero-shot image
emotion (prompt-ensembled, calibrated temperature, content gate), both mapped to
Ekman-6 + neutral. 1,012 non-test records, ~90 s on Apple-Silicon MPS.
Reproduce: `.venv/bin/python run.py --text-backend goemotions --image-backend clip`.

## Step 0 — we MEASURED the image reader before trusting it

`validate.py` drew a stratified sample (4 per predicted emotion = 28 images), rendered a
contact-sheet, and scored the reader against hand labels (`outputs/validation/`).

| Model predicts | Precision | Reality |
|---|--:|---|
| **happiness** | **75%** | reliable |
| **sadness** | **75%** | reliable |
| anger | 25% | mostly scenes / fear |
| fear | 0% | actually *happiness* |
| surprise | 0% | scenes + happiness |
| disgust | 0% | all scenes — a busy-texture artifact |

- **Overall exact-match accuracy 25%**; on confident predictions (margin ≥ 0.10) **50%**.
- **The face-gate does NOT help** (face 20% vs scene 28%): in this corpus, emotion is carried
  by whole *scenes* (a lone figure in mist = sadness), not just close-up faces. Gate kept only
  as a diagnostic flag, not a filter.
- **~Half the sampled corpus has no readable emotion** — hearts, a gaping mouth, spilled milk,
  landscapes, a DNA helix, decorative patterns, animals. (Finding in its own right: much public
  input was not an emotion at all.)

**Conclusion:** CLIP zero-shot is trustworthy for **happiness / sadness** on line-art and
unreliable for anger/fear/surprise/disgust. Report on the axis it can read.

## RQ1 on three axes

| Axis | n | agreement | Cohen's κ | reading |
|---|--:|--:|--:|---|
| (a) Full 7-way Ekman | 608 | 21.5% | **0.10** | contaminated — lower bound |
| (b) Valence (pos/neg/neutral) | 608 | 29.8% | **0.13** | defensible headline |
| (c) Trustworthy subset¹ | 70 | 91.4% | **0.80** | where the image is confidently happy/sad |

¹ image prediction is a *confident* (margin ≥ 0.10) happiness or sadness — the regime measured
at ~75% precision above.

## The headline finding — positive affect collapses without colour

Valence confusion (text valence → image valence):

| Text is… | → image positive | → image **neutral** | → image negative |
|---|--:|--:|--:|
| **positive** (n=454) | 18% | **57%** | 25% |
| **negative** (n=129) | 2% | 34% | **64%** |

- **When the text is happy, the line-art reads as emotionally *neutral* 57% of the time and
  positive only 18%.** When the text is negative, the image reads negative 64% of the time.
- This **asymmetry is the result**: negative affect survives the translation into monochrome
  line-art (carried by dark tone, jagged line, slumped posture); **positive affect largely does
  not** — it flattens to neutral. That is exactly what the colour-emotion literature predicts
  (Alvarado 2025: lightness/chroma, not hue, carry affect; positive emotions lean on warm/bright
  colour), and it echoes Lomas et al. (2024) that alignment varies sharply by emotion.
- **It is not random noise:** on the subset where the image confidently conveys a clear emotion,
  text–image valence agrees **91% (κ=0.80)**. So the low overall fidelity is driven by DALL·E
  *flattening* happy prompts to neutral imagery, not by mismatched emotions.

## What to put in the dissertation

1. **Primary claim:** text→image emotional fidelity in monochrome line-art is weak overall
   (valence κ≈0.13) and **strongly asymmetric — negative affect transfers, positive affect
   collapses to neutral** — consistent with colour being the missing positive-affect channel.
2. **Method contribution:** a measured reliability profile of CLIP zero-shot on line-art
   (happiness/sadness 75%, other Ekman classes unusable) — justifies reporting on the valence axis.
3. **Corpus finding:** a large share of public prompts produced non-emotional / symbolic images.

## Caveats & next steps (do not over-claim)

- Ground truth for the reliability table is **one expert annotator (me), 28 images**. For the
  dissertation this needs **multiple human raters** on a larger sample with inter-rater agreement
  (Krippendorff's α) — and ideally the Lomas 0–10 alignment protocol.
- Both readers are imperfect: GoEmotions on ultra-short first-person text is weak (Demszky 2020;
  Yang 2023); CLIP on line-art is out-of-distribution. κ is bounded by both.
- The valence collapse hides *within-negative* confusions (fear/anger/disgust) — fine for the
  valence claim, not for per-emotion claims.
- No seed / rewritten prompt stored → cannot decompose DALL·E variance (RESEARCH_GAP.md §6).
