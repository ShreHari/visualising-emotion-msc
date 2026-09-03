> **METHOD-BUILD LOG (8 Aug) — read with RESULTS_final.md.** This documents the pipeline build and its
> first (interim) numbers, which used the NLI prompt-reader. **Corrections since:** (1) Headline 3's
> "positive aligns best" direction was **withdrawn** — the positive/negative split has a degenerate null
> (see RESULTS_final.md "What we CANNOT claim"); the readers' opposite biases mean only the human study
> can adjudicate. (2) An audit found a label-space mismatch that deflated the OLD method's top-3 overlap:
> corrected 15%→23%, so "tripled" is **roughly doubled**. (3) Numbers below now exclude the 13 pre-test
> records (n=984, was 997). The definitive, verified findings are in **RESULTS_final.md**.

# Results — Describe→Extract Pipeline (Chen's architecture)

Built and run overnight per [supervisor direction #1–#2]. Pipeline: **BLIP-VQA describes the image's
facial expression / posture / scene (no emotion asked) → zero-shot NLI infers emotion from that
description → compare prompt-emotion vs image-emotion by SIMILARITY.** 1,025 records, 0 failures.
Code: `describe_extract.py` (crash-safe/resumable) · `similarity_v2.py`.

---

## Headline (what to tell Chen)

1. **The describe→extract method aligns with the prompt far better than the old direct-CLIP reader** —
   empirically justifies her redirection.
2. **Emotional similarity is real and highly significant** (z ≈ 10–16 vs a random-pairing null).
3. **The two automatic readers disagree systematically and in *opposite* directions** — direct-CLIP said
   *positive emotion collapses*; describe→extract says *positive aligns best*. Neither is ground truth.
   **This divergence is itself the key finding, and the strongest possible case for a human-rating study.**

---

## Result 1 — New method beats the baseline (the evaluation, 608 records, same prompt basis)

Holding the prompt side constant and varying only *how the image's emotion is read*:

| Metric | NEW describe→extract | OLD direct-CLIP |
|---|--:|--:|
| Valence-Arousal similarity | **83.7%** (z=14.2) | 74.2% (z=12.3) |
| Emotion-family agreement | **49.3%** (z=11.2) | 25.3% (z=10.2) |
| Top-3 soft overlap | **48.6%** (z=14.0) | 22.8% (z=12.1) — *corrected; label-space audit fix* |

Family agreement **doubled**, top-3 overlap **roughly doubled** (corrected). Describing the image then extracting emotion
captures the depicted feeling much better than forcing CLIP to output an emotion label directly.

## Result 2 — Similarity, not matching (984 records with a non-neutral side, pre-tests excluded; vs random-pairing null, N=300)

| Metric | True pairs | Random | gap | z |
|---|--:|--:|--:|--:|
| Valence-Arousal similarity | 81.3% | 75.7% | +5.7% | **15.7** |
| Valence-sign agreement | 61.5% | 38.8% | +22.8% | **13.0** |
| Emotion-family agreement | 35.8% | 24.9% | +10.9% | 9.6 |
| Top-3 soft overlap | 41.4% | 30.6% | +10.8% | **16.0** |

An image's emotion is **significantly more similar to its own prompt than to a random prompt** on every
metric. The signal is unmistakable once you score by similarity instead of exact match.

## Result 3 — The two readers disagree (the honest, important finding)

Per-emotion (prompt → image, top-1):

| Prompt emotion | n | aligns | notes |
|---|--:|--:|---|
| joy | 388 | **66%** | positive genuinely transfers |
| anger | 29 | **59%** | |
| sadness | 104 | 36% | a third leak to "joy" (smile bias) |
| neutral | 97 | 29% | |
| surprise | 333 | 15% | scattered (see NLI note) |
| fear | 44 | **0%** | never recovered → mostly read as sadness |
| disgust | 30 | **0%** | → joy / anger |

**And the asymmetry reversed vs the old pipeline:**
- Old (direct-CLIP): negative aligned better than positive → "positive collapses."
- New (describe→extract): **positive aligns better** (VA-sim 87% vs 76%; valence-sign 66% vs 53%).

Why the reversal? Because the readers have **opposite biases**:
- **CLIP** on monochrome line-art skews toward neutral/negative (validated earlier: 0–25% on rare emotions).
- **BLIP-VQA** skews positive — it reads **66% of all faces as smiling/happy** (676/1,025 expression
  answers). Some of this is real (DALL·E does draw many smiles) and some is bias.

**The truth lies between them, and no automatic reader can settle it — which is exactly why the
human-rating study is essential.** This is a strong methodological contribution: *the measured
emotional fidelity of AI line-art depends heavily on which automatic reader you use, and the two
leading options are biased in opposite directions.*

---

## Honest limitations (carry these into the write-up)

- **BLIP-VQA positivity bias** (66% smiling) inflates positive alignment. Report it explicitly; validate against humans.
- **NLI over-reads "surprise" on the prompts** (333/1,025 prompt top-1 = surprise) — a bart-MNLI artifact on
  short text. *Fix worth trying:* use GoEmotions for the prompt side (it read first-person prompts well
  earlier) and NLI only for the descriptions; reconcile the two label spaces.
- **Fear / disgust / surprise are poorly captured by both methods** — likely genuinely hard in colour-free
  line-art plus reader noise. Restrict strong claims to the positive/negative axis.
- The V-A values are emotion-label centroids (not continuous NRC-VAD yet) — an easy next upgrade.
- Run slowed to ~12 s/record late on (laptop memory pressure) but completed with zero failures thanks to
  resumable checkpointing.

## Robustness cross-check — prompt extractor (added, tested)

The "surprise on prompts" artifact is fixable: re-extracting prompt emotion with **GoEmotions**
(28→7 Ekman families) instead of NLI drops surprise from 333→77 prompt-labels, and **the finding
holds** — similarity still significant (n=896 after pre-test exclusion: VA 80.0% z=11.0; valence-sign 64.0%
z=10.8; family 35.9% z=5.2; overlap 38.8% z=8.8), same positive-leaning asymmetry (positive VA 86.6%
vs negative 75.9%) — though per the banner, no direction is claimed. So the result is
**robust to how the prompt emotion is extracted** — it isn't an NLI quirk. (`goe_prompt_sim.py`.)
Recommended final config: **GoEmotions for prompts** (cleaner) + **NLI for image-descriptions**.

## What's next
1. **Human-rating study** — the adjudicator between the two biased readers (needs the ethics application).
2. **Prompt side → GoEmotions** to remove the surprise artifact.
3. **NRC-VAD** for continuous valence-arousal.
4. Optionally a second describer (a small captioner) to triangulate the BLIP-VQA bias.

## Rejected approaches (tested, learned — good for the methods chapter)
- **GoEmotions on descriptions** → collapses to neutral (needs first-person feeling words).
- **BLIP plain caption → NLI** → too terse, collapses to "surprise".
- **Qwen2.5-VL-3B** (the "ideal" describer) → thrashed the laptop's RAM into swap (7 GB), no progress in 4.5 h.
- **Florence-2** → incompatible with transformers 5.14 (`forced_bos_token_id`).
- **Winner: BLIP-VQA** (~0.4 B, native, ~1.5–12 s/record) — its "facial expression?" answer gives NLI the cue.
