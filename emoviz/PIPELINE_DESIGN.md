> **AS BUILT (final, 15 Aug 2026).** This is the design-space record. The built pipeline differs from the
> "recommended default" below after empirical testing: **describer = BLIP-VQA** (`Salesforce/blip-vqa-base`)
> — Qwen2.5-VL-3B was rejected (RAM-thrash on 16 GB), Florence-2 rejected (transformers-5.x break);
> **image emotion = zero-shot NLI** (`facebook/bart-large-mnli`) on the description; **prompt emotion =
> GoEmotions** (28→7 families). NRC-VAD / Presidio / sentence-transformers remain future upgrades.
> See `outputs/RESULTS_describe_extract.md` ("Rejected approaches") and `README.md`.

# Pipeline Redesign — Chen's "Describe → Extract → Similarity" Architecture

Redesign of the emoviz pipeline following Chaona Chen's direction (see memory `supervisor-direction`).
Core shift: **don't force a vision model to output emotion; describe the image as text, then extract
emotion from that text, then compare prompt-emotion vs image-emotion by SIMILARITY (not right/wrong).**
Every option below is free/open and runs on the existing laptop (Apple-Silicon MPS, torch+transformers+open_clip already installed).

```
 PROMPT (text) ─────────────┐                         DRAWING (image)
                            │                               │
                            │              STAGE 1: DESCRIBE (objects/scene, NO emotion)
                            │                               │  Qwen2.5-VL-3B  (+ BLIP baseline)
                            │                          description (text)
                            ▼                               ▼
        STAGE 2: emotion-from-text  ◄──── same code ────►  STAGE 2: emotion-from-text
        GoEmotions top-3  +  NRC-VAD (valence/arousal)     GoEmotions top-3  +  NRC-VAD
                            │                               │
                            └──────────► STAGE 3: SIMILARITY LADDER ◄────────┘
                                (1) Ekman-6 family agreement
                                (2) valence-arousal distance   ← headline
                                (3) top-3 soft overlap  (+ null baseline)

 STAGE 0 (upstream): split prompts emotional vs non-emotional · split images face vs scene
 PRE-PROC: redact names → [NAME] (keep emotion words like Joy/Hope/Grace + all illness/grief)
```

---

## The recommended default build (one clear path — start here)

| Stage | Pick | Why |
|---|---|---|
| **0A · prompt split** | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` (zero-shot) + existing lexicon baseline | emotional vs non-emotional; handles the French/Italian prompts; no new install |
| **0B · face split** | CLIP presence probe (open_clip, installed) + BLIP-caption keyword cross-check | face vs scene; CLIP degrades gracefully on drawings; reuses the caption |
| **Pre-proc · names** | Presidio + GLiNER → `[NAME]`, with emotion-word allow-list + 30-min manual confirm of flagged rows | reliable, preserves emotion; guards Joy/Hope/Grace |
| **1 · describe** | **`Qwen/Qwen2.5-VL-3B-Instruct`** (primary) + `Salesforce/blip-image-captioning-large` (baseline) | native in transformers 5.14, follows "describe objects, no emotion", laptop-friendly; two describers = hallucination check. Optional aux: `kmewhort/beit-sketch-classifier` shape tags |
| **2 · emotion from text** (both sides) | **GoEmotions** `SamLowe/roberta-base-go_emotions` (top-3, 28-dim) + **NRC-VAD v2.1** (valence-arousal) | categorical mixed-affect + continuous affect; GoEmotions ships the Ekman family map |
| **3 · similarity** | ladder: (1) Ekman-6 family agreement · (2) **VAD distance = headline** · (3) top-3 soft overlap; + sentence-transformers `all-mpnet-base-v2` cosine sanity check; + **permutation null + bootstrap CIs** | "similar not identical" made rigorous; null proves true pairs beat random |

**Install (all free, CPU/MPS):**
```
.venv/bin/pip install qwen-vl-utils sentence-transformers "presidio-analyzer[gliner]" \
    krippendorff simpledorff statsmodels pingouin scikit-posthocs
# + download NRC-VAD lexicon; opencv-python + lbpcascade_animeface optional for face split
```

---

## Full menu (every option, per stage)

### Stage 1 — image → description (captioning / VLM)
- **Qwen2.5-VL-3B-Instruct** ⭐ primary — native, promptable, best OOD on line-art. (2B variant if slow.)
- **BLIP-large** — baseline/agreement check, trivial, fast, standard citation.
- **Florence-2-large** — excellent detailed captions but `trust_remote_code` breaks on transformers 5.x (pin env). Optional.
- **moondream2** — small + promptable, same pin caveat.
- **BLIP-2 / LLaVA-7B** — heavier, no gain here on a laptop.
- **GIT / ViT-GPT2** — weak COCO captioners; keep only as a "floor baseline" to show the OOD gap.
- **CLIP-Interrogator** — tag-salad, injects style tokens, clashes with open_clip 3.3. Avoid.

### Stage 1b — sketch/drawing-specific models (Chen's "shape-focus" idea)
- **kmewhort/beit-sketch-classifier** — use as an **auxiliary top-3 object tag only**, not the describer.
- QuickDraw ViT finetunes — equivalent swap-in (pick one).
- Sketch_LVM / Sketch-CLIP — principled open-vocab version; research-grade, stretch goal.
- Sketch-a-Net, DoodleNet, ImageNet-Sketch — avoid (dated / off-stack / not a describer).
- **Honest finding to report:** these read line-art *style* well but collapse a multi-object scene into one doodle word → they can't describe scenes. That negative result is itself a finding.

### Stage 2 — emotion from text (prompt AND description, identical code)
- **GoEmotions RoBERTa** ⭐ — 28 multi-label, top-3 easy, ships Ekman family map.
- **Ekman-7 DistilRoBERTa** (j-hartmann) — cheap cross-check already at family granularity.
- **NRC-VAD v2.1** ⭐ — continuous valence-arousal; the psychology-standard similarity basis.
- CardiffNLP Twitter-emotion — only if you want Plutchik labels (trust/anticipation/love).
- NRC EmoLex — transparent word-level appendix signal (too sparse on 4-word prompts alone).
- Local LLM (Ollama Qwen2.5-7B / Llama-3.1-8B) — optional validator on disagreement cases only.

### Stage 3 — similarity (not matching)
- **Ekman-6 family agreement** — rate + confusion matrix.
- **Valence-arousal distance** ⭐ headline — makes "tired but happy" ≈ "content" score high; plots as a 2D scatter.
- **Top-3 soft/probability-weighted overlap** — implements Chen's "top-3 per side"; EMD over the 28-dim distribution for full partial credit.
- sentence-transformers cosine — taxonomy-free corroboration, not headline.
- **Permutation null + bootstrap CIs** — essential: proves image emotion is more similar to its own prompt than to random prompts.
- Plutchik-wheel adjacency — optional robustness check.

### Stage 0 — data splitting
- **(A) prompt emotional vs non-emotional:** mDeBERTa zero-shot NLI (primary) + lexicon baseline; optional Ollama LLM on low-confidence cases (also returns top-3). Hand-label ~50 for precision/recall.
- **(B) face vs scene:** CLIP presence probe (primary) + BLIP-caption keyword; OWL-ViT for boxes if needed; lbpcascade_animeface as cheap CPU complement. Every detector is OOD on DALL·E line-art → validate on ~50-100 hand-labelled images.

### Pre-processing — name redaction
- **Presidio + GLiNER** ⭐ → map PERSON → `[NAME]`.
- GLiNER standalone (person-only) — lightest.
- HF NER (dslim/bert-base-NER-uncased) — classical fallback.
- Regex + name lists — second pass only (over-redacts Joy/Hope/Grace).
- **Guard:** emotion-word allow-list; manual confirm of flagged rows (~30 min). Illness/grief words are not name entities → untouched.

### Evaluation (its own marked section)
- **P1 now (no ethics):** shuffled-pair null control · baseline old-CLIP-direct vs new describe-then-extract · bootstrap/data-halving CIs · per-family similarity distributions (Kruskal-Wallis).
- **P2 mark-maker (ethics now):** human study — 60-100 stratified items, 3-5 raters, Lomas 0-10 + top-3 pick, Krippendorff α; **headline = Spearman(pipeline similarity, human alignment)** → validates the metric. `validate.py` is already ~80% of this harness.
- **P3 if time:** captioner-swap ablation (also probes line-art reading).

---

## What this unlocks — research directions you can proceed with

1. **RQ1 · text→image emotional *similarity*** (the core, reframed): how similar is the drawing's emotion (describe→extract) to the prompt's, on the similarity ladder? The positive-affect-collapse finding becomes a *similarity distribution*, not an accuracy number.
2. **RQ2 · which emotions stay similar vs drift** — per-family similarity.
3. **RQ3 · generative consistency** — across the 65 duplicate-prompt runs, how similar are the emotions across repeats.
4. **Methodological contribution + evaluation** — describe-then-extract vs direct-CLIP (Chen's redirection, proven empirically).
5. **Face vs scene** — does emotional similarity differ when a face is present?
6. **Emotional vs non-emotional prompts** — the split, and what the non-emotional ones generate.
7. **The novel framing** — *similarity, not matching* — Chen's highlighted contribution: flexible partial-credit alignment instead of one-to-one accuracy.
