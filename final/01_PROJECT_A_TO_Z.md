# The Project, A to Z

A complete, self-contained account of the dissertation. Each section gives a plain-English explanation first, then the technical one.

---

## 1. Project overview

**In simple English.** At the Festival of the Mind in Sheffield in 2024, members of the public typed a short line about how they were feeling, and an image generator turned each line into a black-and-white line drawing. This project takes those text-drawing pairs and asks a narrow, answerable question: if one automatic reader estimates the emotion of the typed words, and a second automatic reader estimates the emotion of the drawing, how similar are the two estimates — and is that similarity greater than you would get by pairing a drawing with somebody else's words?

**Technically.** The corpus is 1,025 text-image pairs; 13 are pre-festival developer tests identified from recovered C2PA signing timestamps, leaving 1,012 analysed records. Prompts are very short, with a median of about four words. A *prompt reader* (GoEmotions) and an *image reader* (BLIP-VQA description followed by BART-MNLI zero-shot inference) each produce a distribution over the same seven emotion families. Four graded similarity measures are computed between the two distributions, and every one of them is reported against a 300-shuffle random-pairing null baseline with seed 7. The unit of study is therefore **prompt-reader / image-reader agreement**, not human perception.

---

## 2. Problem statement

**In simple English.** There is no correct answer to "what emotion is this drawing." People disagree, models are noisy, and nobody recorded what the visitor intended beyond the words they typed. So scoring an image right or wrong against a single label is the wrong instrument. On top of that, the images are monochrome line art, which is not what emotion-recognition models are trained on.

**Technically.** Three problems compound. First, no ground truth exists: the corpus carries the visitor's own text but no independent affect annotation, so exact-label, right-or-wrong scoring imposes a precision the data cannot support and treats "happy" versus "excited" as a total failure. Second, the images are out of distribution for visual affect models: EmoSet- and ArtELingo-style recognisers are trained on photographs and colour artwork, and the corpus removes colour entirely. Third, the obvious architecture — asking a vision-language model directly for an emotion label — is a poor fit, because such models are trained on colour photographs and are strong on objects rather than affect. Manual inspection of the direct route found an arms-raised celebration read as anger at 0.73.

---

## 3. Why this problem matters

**In simple English.** Text-to-image systems are increasingly used to visualise feelings, but the standard ways of checking whether the output is any good only check whether the right *objects* appear. Nobody has a good way to check the emotional side, especially when colour — the strongest emotional channel — has been taken away.

**Technically.** Automatic text-to-image evaluation metrics (VQAScore, TIFA, GenEval, DSG) score object and attribute presence, not affect. Affect-conditioned generators such as EmoGen and EmotiCrafter are conditioned on a target emotion and produce full-colour output, so they do not address unmediated, mixed-affect user text. The colour literature (Alvarado 2025) is cited here only as motivation for why monochrome line art is a hard case, never as a result of this project: the corpus is monochrome throughout and there is no colour-control condition, so no claim about colour is made. A second practical concern is stability: a generator that returns emotionally divergent drawings for the same sentence is a different proposition for deployment than one that does not, and this corpus contains enough repeated prompts to look at that directly.

---

## 4. Research question and sub-questions

**In simple English.** The main question is how similar the two automatic readings are, and whether that similarity is real rather than an artefact of the metrics. Underneath it sit five smaller questions: does it hold for emotional prompts, does it differ between drawings with people and drawings without, is the image reader stable when the same words are drawn again, does describing-then-extracting beat asking the model directly, and does the whole thing correctly show nothing when there is nothing to show?

**Technically.**

- **Main RQ.** To what extent does the emotion distribution recovered from a line drawing agree with the distribution recovered from the prompt that produced it, relative to a random-pairing null?
- **SQ1.** Does agreement exceed the null on the emotional-prompt subset, across all four similarity measures?
- **SQ2.** Does agreement differ between face-classified and scene-classified images?
- **SQ3.** How consistent is the image reader's output across drawings generated from the same prompt?
- **SQ4.** Does the describe-then-extract architecture outperform the direct-CLIP route on the same records?
- **SQ5.** Specificity check: on prompts the prompt reader labels non-emotional, does agreement fall to the null?

---

## 5. Research objectives

**In simple English.** Build a working pipeline that turns a drawing into words and then into an emotion; define measures that reward being close rather than exact; test every measure against chance; group the data the way the supervisor asked; compare against the obvious alternative approach; and be explicit about what the results do not show.

**Technically.** (i) Implement a describe-then-extract image reader so that both sides of the comparison are text. (ii) Implement a prompt reader appropriate to short first-person text. (iii) Define a graded similarity ladder spanning coarse to fine resolution. (iv) Compute a random-pairing null and a z-score for every measure on every subset. (v) Partition the corpus into emotional/non-emotional prompts and face/scene images and report all groups. (vi) Run a frozen direct-CLIP baseline for method comparison. (vii) Analyse repeated prompts against a permutation null. (viii) Document rejected architectures with the evidence that rejected them, and state the limitations of every claim.

---

## 6. Literature review summary and the research gap

**In simple English.** I read and filtered a large body of work and found that the neighbouring research either scores objects rather than feelings, uses tidy template sentences rather than what real people type, generates in full colour towards a chosen target emotion, or uses models trained on photographs. Nothing sits where this project sits.

**Technically.** The curated library holds 74 retained papers across twelve themes, with 23 excluded as surveys, position pieces or off-target, documented in a filtering log and an annotated bibliography with a 74-entry BibTeX file. Four neighbours define the boundary. Automatic text-to-image metrics (VQAScore, TIFA, GenEval, DSG) evaluate semantic content, not affect. Lomas et al. (2024), the closest work, uses templated prompts rather than unmediated self-report. Affect-conditioned generators (EmoGen, EmotiCrafter) are target-conditioned and full-colour. Visual-emotion recognisers (EmoSet, ArtELingo) are trained on photographs and colour art, leaving monochrome line art out of distribution.

**The gap.** No existing work measures prompt-reader / image-reader agreement for short, unmediated, mixed-affect first-person self-reports rendered as colour-free line art, nor the stability of the image reading under repeated identical prompts. The contribution is a corpus, a question framed as graded similarity, and a consistency experiment — not a new metric; the toolkit recombines existing models.

---

## 7. The proposed solution

**In simple English.** Two ideas. First, do not ask the vision model for an emotion; ask it plain factual questions about the picture, write the answers into a sentence, and read the emotion out of that sentence — so you are comparing text with text. Second, do not score right or wrong; ask how similar, so that neighbouring emotions count as close.

**Technically.** The supervisor, Dr Chaona Chen (30 July 2026), named the novel contribution herself: **similarity, not exact one-to-one scoring**. Her reasoning is reproduced as the project's own justification — emotion is subjective, there is no ground truth, humans disagree and models are noisy, so asking whether an image emotion is right or wrong against the text is too simplistic; "happy" and "excited" should count as similar, and emotions should be grouped into families. Her architectural instruction was equally specific: do not force CLIP to output emotion, because CLIP is trained on real colour photographs and is good at objects, not emotion. Instead, *describe* the image, then extract emotion from the description, so both sides are text and the comparison is text-to-text. She also specified the six-section dissertation structure: Abstract, Introduction, Literature Review, Methodology, Results, Discussion.

---

## 8. Methodology

**In simple English.** Every drawing is turned into a short factual sentence, and that sentence is read for emotion. Every prompt is read for emotion separately. The two readings are compared four different ways, from coarse to fine. Each comparison is repeated 300 times with the drawings shuffled against the wrong prompts, to see what the score would be by chance.

**Technically.** The image reader poses five factual questions to BLIP-VQA — *What is the facial expression? What is the person doing? What is the body posture? How many people are there? What is in the picture?* — none of which mentions emotion. The answers are assembled into a single neutral sentence, which is read by zero-shot NLI (`facebook/bart-large-mnli`) over the seven emotion families with the hypothesis template `"This scene conveys {}."`. The prompt reader is `SamLowe/roberta-base-go_emotions`, whose 28 labels are collapsed to the same seven families by a standard grouping. Both sides yield a top-3 distribution in a shared label space.

Groupings are rule-based and documented, never per-record: a prompt is *emotional* when the prompt reader's top-1 family is not neutral (607 emotional / 405 non-emotional); an image is *face-classified* when the describer reports at least one person **and** a readable expression word (591 face / 421 scene; within emotional prompts, 402 face / 205 scene). Splits are groupings, not exclusions — all groups are reported.

Every measure is reported against a random-pairing null of 300 shuffles at seed 7, with a z-score. Null degeneracy is a hand-passed flag, not auto-detected: single-valence subsets and the non-emotional subset are degenerate for the sign and family measures, because the shuffled pairing cannot change a quantity that is constant within the subset.

Several architectures were tried and rejected, and the evidence belongs in the Methodology: GoEmotions applied to image descriptions collapses to neutral above 0.95, because it needs first-person feeling words; a single terse BLIP caption fed to the reader collapses to "surprise"; BART-MNLI on the prompt side over-reads surprise (333 of 1,025 prompts); Qwen2.5-VL-3B as describer exceeded 16 GB of RAM and produced no progress in 4h45m; Florence-2 was incompatible with transformers 5.14; and asking CLIP directly for emotion was beaten in the method comparison.

---

## 9. System architecture

**In simple English.** Data goes in one end, gets cleaned, splits into two parallel paths — one for the words, one for the picture — and the two paths meet at a comparison step that produces the numbers.

**Technically.** A loader reads the corpus and applies pre-processing (pre-test exclusion, name redaction, duplicate keying) so that every downstream surface sees the same cleaned text. From there the flow forks:

- **Prompt path:** redacted text -> GoEmotions -> 28 labels -> collapse to 7 families -> top-3 distribution, cached to `outputs/prompt_emotions_goe.json`.
- **Image path:** image -> BLIP-VQA x 5 questions -> composed description sentence -> BART-MNLI zero-shot over 7 families -> top-3 distribution, checkpointed line by line to `outputs/describe_extract.jsonl`.
- **Comparison:** the two distributions -> four similarity measures -> subset grouping -> 300-shuffle null and z-score -> `outputs/analysis_final.csv` and the results document.
- **Frozen baseline:** a separate OpenCLIP ViT-B/32 (LAION-2B) run stored as an immutable results file so the main pipeline cannot overwrite it.
- **Demonstrator:** a Flask application exposes the live pipeline for a single record or an uploaded image.

---

## 10. Technologies, models and tools

**In simple English.** Three small neural models, all run locally on a laptop, plus Python for the analysis and a small web app for demonstrations.

**Technically.**

| Role | Model | Size |
| --- | --- | --- |
| Describer | `Salesforce/blip-vqa-base` | ~385M |
| Image emotion reader | `facebook/bart-large-mnli` | ~407M |
| Prompt emotion reader | `SamLowe/roberta-base-go_emotions` | ~125M |
| Frozen comparison baseline | OpenCLIP ViT-B/32 (LAION-2B) | — |

Supporting stack: Python with PyTorch and Hugging Face `transformers`, NumPy, Matplotlib for figures, NLTK gazetteers for the redaction pass, Flask for the demonstrator, and a pinned `requirements.txt` with a `setup.sh` that builds an isolated virtual environment. All models run locally with fp16 and lazy per-model loading; the hardware ceiling is real and shaped the model choices — 16 GB of RAM admits only small native describers, which is why the 3B-parameter option was abandoned.

---

## 11. Implementation, step by step

**In simple English.** Load and clean the data; run the describer over every image, saving as you go so a crash costs nothing; read emotions from both sides; compute the numbers; compare with the alternative method; and check the whole thing with a smoke-test script.

**Technically.**

1. **Load.** Parse the corpus, resolving filename patterns and record identifiers.
2. **Pre-process.** Apply name redaction at the loader and flag the 13 pre-test records; key duplicate prompts from the original text.
3. **Describe.** Run BLIP-VQA's five questions over all 1,025 images, appending one JSON line per record. The run is crash-safe and resumable: completed ids are skipped on restart.
4. **Compose.** Assemble the five answers into one neutral description sentence per image.
5. **Extract image emotion.** Run BART-MNLI zero-shot over the seven families for each description, storing the full top-3.
6. **Extract prompt emotion.** Run GoEmotions over each redacted prompt, collapse 28 labels to 7 families, cache the result.
7. **Group.** Apply the emotional/non-emotional and face/scene rules from the stored describer answers.
8. **Measure.** Compute the four similarity measures per record, then per subset.
9. **Null.** For each subset, shuffle the image side 300 times at seed 7, recompute, and report mean null and z.
10. **Compare methods.** Run the same similarity code over the frozen direct-CLIP baseline on the records both pipelines cover.
11. **Consistency.** Group records by identical prompt and measure how often the image reader returns the same family within a group, against a permutation null.
12. **Verify and report.** Run the 29-assertion smoke-test script, regenerate the five figures, and write the results.

The full 1,025-record describe-then-extract run completed with **0 failures**, which means zero unhandled exceptions. It is a robustness statement, not an accuracy one. Likewise, the 29 assertions are smoke checks — none of them asserts a numeric result.

---

## 12. Data pre-processing

**In simple English.** Before any analysis, the data is cleaned in three ways: the developer's own test entries are set aside, real people's names are replaced with a placeholder, and repeated prompts are given a shared key so they can be grouped later. The original files are never edited.

**Technically.**

**Pre-test exclusion.** Thirteen records were written before the festival opened, identified from recovered C2PA signing timestamps on the generated images. They are still processed by the pipeline — so that record accounting is complete — but excluded from analysis, leaving 1,012.

**Name redaction.** A three-stage, reproducible procedure implemented in a single module:

1. *High-recall detection.* Flags any token that is a gazetteer given name (NLTK `names`, 7,944 entries), or capitalised mid-sentence and absent from an English dictionary (NLTK `words` plus the system dictionary, ~236k entries), or preceded by a naming phrase such as "called X" or "my friend X". It deliberately over-flags, because most of the corpus is written entirely in lower case and capitalisation alone would miss most real names.
2. *Reviewed decision.* Every candidate was reviewed once and recorded with a reason in a fixed decision table. Only names of private individuals are replaced with `[name]`; places, brands, public figures, medical eponyms and detector artefacts are kept. Re-running detection after any data change raises on an unreviewed candidate.
3. *Application.* Redaction is applied at the loader, so analysis, figures and the demonstrator all see the redacted text. The original dataset files are never modified. Illness and bereavement content is retained: it is not identifying on its own and it is material to the analysis.

**Duplicate keying.** The corpus holds 763 distinct prompts; 249 records repeat an earlier prompt, and 87 prompts drawn two or more times cover 336 records. Each record carries a key derived from its original text, enabling both the distinct-prompt robustness analysis and the consistency experiment.

---

## 13. Experiments conducted

**In simple English.** Five experiments: the main one on emotional prompts, one splitting drawings by whether a person appears, one on prompts that carry no emotion (a check that the method can return nothing), one on repeated prompts, and one comparing the two architectures head to head.

**Technically.**

- **E1 — Main.** All four measures on the 607 emotional-prompt records against the null.
- **E2 — Face vs scene.** The same measures on 402 face-classified and 205 scene-classified emotional records, each against its own null.
- **E3 — Specificity.** The 405 non-emotional records. Only the valence-arousal measure is informative here; the sign and family measures are degenerate on this subset by the subset's own definition and are not presented as a passing control.
- **E4 — Robustness to duplicates.** All measures recomputed on the 763 distinct prompts.
- **E5 — Consistency.** Within-group agreement of the image reader across the 87 repeated prompts, against a permutation null.
- **E6 — Method comparison.** Describe-then-extract versus direct-CLIP on the 608 records both pipelines cover.

---

## 14. Evaluation metrics

Each measure is stated in plain words first.

**Valence-sign agreement.** *Do both readers land on the same side — positive or negative?* Formally, the proportion of records for which the sign of the prompt reader's top-1 family equals the sign of the image reader's top-1 family, over records whose prompt sign is non-zero. Note the wording: **valence-sign agreement**, never "mood direction".

**Family agreement.** *Do both readers pick the same emotion family?* The proportion of records where the two top-1 families are identical, in the shared seven-family space.

**Top-3 overlap.** *How much do the two readers' three best guesses overlap, weighted by confidence?* Each side's top-3 is normalised to sum to one — so the prompt reader's multi-label scores and the image reader's softmax are on a comparable scale — and the overlap is the sum of per-label minima, a distribution overlap bounded in [0, 1].

**Valence-arousal similarity.** *How close are the two readings on a two-dimensional emotion map?* This is the only quantity the project calls **similarity**, because it is a graded distance rather than a yes/no agreement. Each top-3 is mapped to a confidence-weighted centroid in valence-arousal space using fixed per-family coordinates, and similarity is one minus the normalised Euclidean distance. It has a mathematical floor of about 41% — it cannot reach zero — and random pairings average about 76%, so only movement above that band is meaningful.

**Random-pairing null and z.** For each subset, the image side is shuffled against the prompt side 300 times at seed 7 and every measure recomputed, giving a null mean and a standard deviation from which a z-score is taken. A measure is only reported as informative where the null is non-degenerate.

**Consistency (permutation null).** For repeated prompts, the proportion of within-group record pairs on which the image reader returns the same family, compared against a permutation null that reshuffles group membership.

---

## 15. Results and analysis

**In simple English.** On prompts that carry emotion, the two readers agree well above chance on every measure. Drawings with a face agree far better than drawings without. On prompts with no emotion, agreement drops exactly to chance, which is what it should do. The image reader is fairly stable across redraws of the same words, and describing-then-extracting roughly doubles agreement over asking the model directly.

**Technically.** All figures below are against the 300-shuffle random-pairing null, seed 7.

| Subset | Measure | Observed | Null | z |
| --- | --- | --- | --- | --- |
| Emotional, n=607 | valence-sign | 64.0% | 45.6% | +11.1 |
| Emotional, n=607 | family | 53.1% | 38.8% | +10.3 |
| Emotional, n=607 | top-3 overlap | 50.6% | 39.4% | +11.6 |
| Emotional, n=607 | valence-arousal | 83.8% | 77.3% | +12.2 |
| Face, n=402 | valence-sign | 73.9% | 53.5% | +10.4 |
| Face, n=402 | family | 61.9% | 45.8% | +10.3 |
| Scene, n=205 | valence-sign | 42.9% | 29.6% | +5.8 |
| Scene, n=205 | family | 35.6% | 26.2% | +4.4 |
| Non-emotional, n=405 | valence-arousal | 76.6% | 76.6% | +0.3 |

**Specificity.** The non-emotional subset returns 76.6% against a null of 76.6%, z +0.3 — indistinguishable from chance, and the sole informative measure on that subset.

**Robustness to duplicate prompts.** On the 763 distinct prompts all emotional-subset measures remain at z +9 to +11, and face-classified valence-sign agreement stands at 71.8% (z ~ +9). The scene result, however, **weakens substantially** to 37.3% (z +3.5). The headlines do not all hold equally under deduplication, and the scene finding is the one that softens.

**Consistency.** Across repeated prompts, the image reader returns the same emotion family for 68.8% of drawings within a group, against a permutation null of 59.1%, z +4.9. The 68.8% figure is meaningless without its null and must never be quoted bare.

**Method comparison.** On the 608 records both pipelines cover, describe-then-extract reaches 49.3% family agreement against direct-CLIP's 25.3%, and 48.6% top-3 overlap against 22.8%. Two qualifications are material: this comparison holds the prompt reader constant as BART-MNLI, which is *not* the GoEmotions reader used in the main analysis, and the 608-record intersection derives from a v1 lexicon rule.

**On face versus scene.** Both rates are reported against their own nulls and both clear them. No statistical test of the *difference* between them has been performed, so no ratio claim such as "1.7 times better" is made; a formal test is outstanding.

---

## 16. Key findings

**In simple English.** Agreement between the two readers is real and well above chance on emotional prompts; it is much stronger when a person's face is present; it disappears exactly where it should; the drawings are moderately stable under repetition; and the describe-then-extract design is the better architecture.

**Technically.**

1. **Agreement above the null is robust on emotional prompts.** All four measures clear their nulls at z +10 to +12 on n=607, and survive deduplication to 763 distinct prompts at z +9 to +11.
2. **Face-classified images show much higher agreement than scene-classified images** (valence-sign 73.9% vs 42.9%; family 61.9% vs 35.6%), each above its own null — though the scene result weakens substantially on distinct prompts and no test of the difference has been run.
3. **The specificity check passes.** Where the prompt reader finds no emotion, valence-arousal similarity sits at the null exactly (z +0.3), indicating the measures are not manufacturing agreement out of the metric's own structure.
4. **The image reader is moderately consistent under repeated prompts** (68.8% within-group same-family, permutation null 59.1%, z +4.9) — better than chance, far from deterministic.
5. **Describe-then-extract substantially outperforms asking the model directly** (family 49.3% vs 25.3%; top-3 overlap 48.6% vs 22.8%), which empirically supports the supervisor's architectural redirection, subject to the two qualifications above.
6. **Graded similarity recovers structure that exact-label scoring hides.** The ladder from valence-arousal down to family agreement shows agreement is partial rather than absent, which is precisely the point of the similarity framing.

---

## 17. Limitations

**In simple English.** The single most important thing to say is that this project measures whether two computer programs agree with each other. It does not establish what a human being sees in these drawings.

**Technically.**

1. **Two automatic readers, not human perception.** Every result is prompt-reader / image-reader agreement. Nothing here establishes what a human perceives. This is the governing limitation and it qualifies every number above.
2. **Circularity in the face/scene split.** The split is not an expression detector. Of the 421 scene records, 414 (98.3%) are ones where the describer answered that no people are present, and 406 of those *do* contain an expression word. The split is driven by the people-count answer. The circularity is real, and its mechanism is specific: the same describer output supplies both the split variable and the text the emotion reader reads.
3. **No test of the face/scene difference.** Both rates beat their own nulls; the gap between them is untested.
4. **Degeneracy is hand-flagged.** The analysis script does not auto-detect degenerate nulls. Single-valence subsets and the non-emotional subset are degenerate for the sign and family measures, because those quantities cannot vary under shuffling within such a subset.
5. **The non-emotional control is unvalidated.** It is defined by a classifier's own output and was never checked by a human. Only the valence-arousal measure is informative on it.
6. **The method comparison is not like-for-like.** Its prompt reader is BART-MNLI, not GoEmotions, and its record set comes from a v1 lexicon rule.
7. **"0 failures" is a robustness claim.** It means zero unhandled exceptions across 1,025 records, nothing about accuracy.
8. **The test suite is 29 smoke assertions.** None asserts a numeric result.
9. **No colour claim.** The corpus is monochrome and there is no colour-control condition; the colour literature is motivation only.
10. **No positive-versus-negative claim.** It was withdrawn: those subsets have degenerate nulls and the two readers disagreed on the direction.
11. **No confidence intervals** are reported on any figure; the z-scores against the shuffle null are the only inferential quantity.

---

## 18. Future work

**In simple English.** Four things would materially strengthen this: ask humans what they see, use models actually built for drawings, test the face/scene gap properly, and put error bars on everything.

**Technically.**

- **Human validation.** The decisive next step, and the one that converts a reader-agreement result into a perception result. A rater study over a stratified sample would also supply the missing check on the non-emotional control set, which is currently defined by a classifier's own output.
- **Drawing- and sketch-specific models.** The supervisor suggested exploring these; it was not done. Both the describer and the image emotion reader are trained on photographic and general-web data, and a sketch-domain describer is the most likely single source of improvement on scene-classified images.
- **A formal significance test of the face/scene gap,** with an explicit test statistic, so the comparison can be stated as a result rather than as two separately-nulled rates.
- **Confidence intervals** on every reported figure, by bootstrap over records, replacing point estimates with ranges.
- **Breaking the circularity** in the face/scene split by deriving the split variable from a source independent of the text the emotion reader reads.
- **A like-for-like method comparison,** re-running the direct-CLIP baseline with GoEmotions on the prompt side and the current record-selection rule, so the two architectures differ only in the image path.
- **Numeric assertions in the test suite,** pinning the headline figures so that a regression in any model or dependency is caught automatically rather than by inspection.
