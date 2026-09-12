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

**In simple English.** The main question is how similar the two automatic readings are, and whether that similarity is real rather than an artefact of the metrics. Underneath it sit five smaller questions: does it hold for emotional prompts, does it differ between drawings with people and drawings without, is the image reader stable when the same words are drawn again, does describing-then-extracting agree with the prompt reader more closely than asking the model directly, and does the whole thing sit at chance when the text reader finds nothing?

**Technically.**

- **Main RQ.** To what extent does the emotion distribution recovered from a line drawing agree with the distribution recovered from the prompt that produced it, relative to a random-pairing null?
- **SQ1.** Does agreement exceed the null on the emotional-prompt subset, across all four similarity measures?
- **SQ2.** Does agreement differ between face-classified and scene-classified images?
- **SQ3.** How consistent is the image reader's output across drawings generated from the same prompt?
- **SQ4.** Does the describe-then-extract image reader agree with the prompt reader more closely than the direct-CLIP route, on the same records and with the same prompt reader?
- **SQ5.** Specificity check: on prompts the prompt reader labels neutral, does agreement sit at the null?

---

## 5. Research objectives

**In simple English.** Build a working pipeline that turns a drawing into words and then into an emotion; define measures that reward being close rather than exact; test every measure against chance; group the data the way the supervisor asked; compare against the obvious alternative approach; and be explicit about what the results do not show.

**Technically.** (i) Implement a describe-then-extract image reader so that both sides of the comparison are text. (ii) Implement a prompt reader appropriate to short first-person text. (iii) Define a graded similarity ladder spanning coarse to fine resolution. (iv) Compute a random-pairing null and a z-score for every measure on every subset. (v) Partition the corpus into emotional/non-emotional prompts and face/scene images and report all groups. (vi) Run a frozen direct-CLIP baseline for method comparison. (vii) Analyse repeated prompts against a permutation null. (viii) Put a clustered-bootstrap confidence interval on every reported rate and test the face/scene difference directly. (ix) Document rejected architectures with the evidence that rejected them, and state the limitations of every claim.

---

## 6. Literature review summary and the research gap

**In simple English.** I read and filtered a large body of work and found that the neighbouring research either scores objects rather than feelings, uses tidy template sentences rather than what real people type, generates in full colour towards a chosen target emotion, or uses models trained on photographs. Nothing sits where this project sits.

**Technically.** The curated library holds 73 papers retained as core evidence across eight themes, from 97 screened as surveys, position pieces or off-target, documented in a filtering log and an annotated bibliography; the BibTeX file holds 91 entries (the retained papers plus the method references). Four neighbours define the boundary. Automatic text-to-image metrics (VQAScore, TIFA, GenEval, DSG) evaluate semantic content, not affect. Lomas et al. (2024), the closest work, uses templated prompts rather than unmediated self-report. Affect-conditioned generators (EmoGen, EmotiCrafter) are target-conditioned and full-colour. Visual-emotion recognisers (EmoSet, ArtELingo) are trained on photographs and colour art, leaving monochrome line art out of distribution.

**The gap.** Within the 73-paper corpus reviewed here, no work measures prompt-reader / image-reader agreement for short, unmediated, mixed-affect first-person self-reports rendered as colour-free line art, nor the stability of the image reading under repeated identical prompts. The contribution is a corpus, a question framed as graded similarity, and a consistency experiment — not a new metric; the toolkit recombines existing models.

---

## 7. The proposed solution

**In simple English.** Two ideas. First, do not ask the vision model for an emotion; ask it plain factual questions about the picture, write the answers into a sentence, and read the emotion out of that sentence — so you are comparing text with text. Second, do not score right or wrong; ask how similar, so that neighbouring emotions count as close.

**Technically.** The supervisor, Dr Chaona Chen (30 July 2026), named the novel contribution herself: **similarity, not exact one-to-one scoring**. Her reasoning is reproduced as the project's own justification — emotion is subjective, there is no ground truth, humans disagree and models are noisy, so asking whether an image emotion is right or wrong against the text is too simplistic; "happy" and "excited" should count as similar, and emotions should be grouped into families. Her architectural instruction was equally specific: do not force CLIP to output emotion, because CLIP is trained on real colour photographs and is good at objects, not emotion. Instead, *describe* the image, then extract emotion from the description, so both sides are text and the comparison is text-to-text. She also specified the six-section dissertation structure: Abstract, Introduction, Literature Review, Methodology, Results, Discussion.

---

## 8. Methodology

**In simple English.** Every drawing is turned into a short factual sentence, and that sentence is read for emotion. Every prompt is read for emotion separately. The two readings are compared four different ways, from coarse to fine. Each comparison is repeated 300 times with the drawings shuffled against the wrong prompts, to see what the score would be by chance.

**Technically.** The image reader poses five factual questions to BLIP-VQA — *What is the facial expression? What is the person doing? What is the body posture? How many people are there? What is in the picture?* — none of which mentions emotion. The answers are assembled into a single neutral sentence, which is read by zero-shot NLI (`facebook/bart-large-mnli`) over the seven emotion families with the hypothesis template `"This scene conveys {}."`. The prompt reader is `SamLowe/roberta-base-go_emotions`, whose 28 labels are collapsed to the same seven families by a standard grouping. Both sides yield a top-3 distribution in a shared label space.

Groupings are rule-based and documented, never per-record: a prompt is *emotional* when the prompt reader's top-1 family is not neutral (607 emotional / 405 labelled neutral by the text reader); an image is *face-classified* when the describer reports at least one person **and** a readable expression word (591 face / 421 scene; within emotional prompts, 402 face / 205 scene). Splits are groupings, not exclusions — all groups are reported.

Every measure is reported against a random-pairing null of 300 shuffles at seed 7, with a z-score, and every rate carries a 95% confidence interval from a clustered bootstrap (10,000 draws, resampling prompt groups). Null degeneracy is detected automatically from the null's own spread: where every prompt in a subset shares one label, shuffling cannot change the score, the null has zero standard deviation, and no z is printed. This affects the sign measure on the single-valence subsets, the family measure on the positive-prompt subset, and both on the neutral-labelled subset; the negative-prompt family null is not degenerate.

Several architectures were tried and rejected, and the evidence belongs in the Methodology: GoEmotions applied to image descriptions collapses to neutral above 0.95, because it needs first-person feeling words; a single terse BLIP caption fed to the reader collapses to "surprise"; BART-MNLI on the prompt side over-reads surprise (333 of 1,025 prompts); Qwen2.5-VL-3B as describer exceeded 16 GB of RAM and produced no progress in 4 h 45 min; Florence-2 was incompatible with transformers 5.14; and asking CLIP directly for emotion agreed far less with the prompt reader in the like-for-like comparison.

---

## 9. System architecture

**In simple English.** Data goes in one end, gets cleaned, splits into two parallel paths — one for the words, one for the picture — and the two paths meet at a comparison step that produces the numbers.

**Technically.** A loader reads the corpus and applies pre-processing (pre-test exclusion, name redaction, duplicate keying) so that every downstream surface sees the same cleaned text. From there the flow forks:

- **Prompt path:** redacted text -> GoEmotions -> 28 labels -> collapse to 7 families -> top-3 distribution, cached to `outputs/prompt_emotions_goe.json`.
- **Image path:** image -> BLIP-VQA x 5 questions -> composed description sentence -> BART-MNLI zero-shot over 7 families -> top-3 distribution, checkpointed line by line to `outputs/describe_extract.jsonl`.
- **Comparison:** the two distributions -> four similarity measures -> subset grouping -> 300-shuffle null and z-score -> `outputs/analysis_final.csv`, `outputs/analysis_final.json` (every printed number, machine-readable) and the results document. One definition of every measure lives in `emoviz/metrics.py`, imported by the analysis, the significance test, the demonstrator and the tests.
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
10. **Compare methods.** Run the same similarity code over the frozen direct-CLIP baseline with the same GoEmotions prompt reader on the same 607 emotional records, with a paired test clustered on prompt identity (`method_comparison.py`).
11. **Consistency.** Group records by identical prompt and measure how often the image reader returns the same family within a group, against a permutation null.
12. **Verify and report.** Run the automated self-test (`test.sh`, which now includes `test_numeric.py`, pinning every headline value to the result file it comes from), regenerate the figures from those result files, and write the results.

The full 1,025-record describe-then-extract run completed with **no unhandled errors**. It is a robustness statement, not an accuracy one: the describer returns an expression answer even where it reports no people present (§17). The self-test has two layers: smoke checks that each stage runs, and `test_numeric.py`, which asserts every reported figure against the result file that produces it; `make_figures.py` reads the same files, so a change in the analysis fails the build instead of drifting silently.

---

## 12. Data pre-processing

**In simple English.** Before any analysis, the data is cleaned in three ways: the developer's own test entries are set aside, real people's names are replaced with a placeholder, and repeated prompts are given a shared key so they can be grouped later. The original files are never edited.

**Technically.**

**Pre-test exclusion.** Thirteen records were written before the festival opened, identified from recovered C2PA signing timestamps on the generated images. They are still processed by the pipeline — so that record accounting is complete — but excluded from analysis, leaving 1,012.

**Name redaction.** A three-stage, reproducible procedure implemented in a single module:

1. *High-recall detection.* Flags any token that is a gazetteer given name (NLTK `names`, 7,944 entries), or capitalised mid-sentence and absent from an English dictionary (NLTK `words` plus the system dictionary, ~236k entries), or preceded by a naming phrase such as "called X" or "my friend X". It deliberately over-flags, because most of the corpus is written entirely in lower case and capitalisation alone would miss most real names.
2. *Reviewed decision.* Every candidate was reviewed once and recorded with a reason in a fixed decision table. Only names of private individuals are replaced with `[name]`; places, brands, public figures, medical eponyms and detector artefacts are kept. Re-running detection after any data change raises on an unreviewed candidate.
3. *Application.* Redaction is applied at the loader, so analysis, figures and the demonstrator all see the redacted text. The original dataset files are never modified. Illness and bereavement content is retained: it is not identifying on its own and it is material to the analysis.

**Duplicate keying.** The corpus holds 763 distinct prompts; 249 records repeat an earlier prompt, and 87 prompts drawn two or more times cover 336 records (43 of the groups are pairs). Each record carries a key derived from its original text, enabling both the distinct-prompt robustness analysis and the consistency experiment.

---

## 13. Experiments conducted

**In simple English.** Six experiments: the main one on emotional prompts, one splitting drawings by whether the describer reports a person, one on prompts the text reader labels neutral (a check that the method can sit at chance), one re-run on distinct prompts only, one on repeated prompts, and one comparing the two architectures head to head. Five further analyses were added on 9 September: confidence intervals and a multiplicity correction, an audit of the control set and the describer, a like-for-like method comparison, an error taxonomy of the high-confidence disagreements, and an ablation of the description template.

**Technically.**

- **E1 — Main.** All four measures on the 607 emotional-prompt records against the null.
- **E2 — Face vs scene.** The same measures on 402 face-classified and 205 scene-classified emotional records, each against its own null.
- **E3 — Specificity.** The 405 records the text reader labels neutral. Only the valence-arousal measure is informative here; the sign and family measures are degenerate on this subset by the subset's own definition and are not presented as a passing control.
- **E4 — Robustness to duplicates.** All measures recomputed on the 763 distinct prompts.
- **E5 — Consistency.** Within-group agreement of the image reader across the 87 repeated prompts, against a permutation null.
- **E6 — Method comparison.** Describe-then-extract versus direct-CLIP on the same 607 emotional records with the same GoEmotions prompt reader and the same measures, with a paired test clustered on prompt identity (`method_comparison.py`). The earlier 608-record comparison with the NLI prompt reader is kept only as the historical v1 record.
- **E7 — Inference.** Clustered-bootstrap 95% intervals on every rate, Cohen's kappa for family agreement, and a Holm–Bonferroni correction across all 36 non-degenerate z-scores (`inference.py`).
- **E8 — Audits.** Contamination of the neutral-labelled control set, the describer's expression answers on drawings with no person, the copy rate from expression word to image family, and the per-family confusion matrix (`audits.py`).
- **E9 — Error taxonomy.** Every high-confidence disagreement (both readers ≥ 0.8, families differ: 38 records) examined against the drawing and assigned a primary failure mode (`error_taxonomy.py`).
- **E10 — Template ablation.** The NLI stage re-run on descriptions with each answer dropped in turn, with the expression word fixed, and under a people-aware template that omits the person and expression clauses wherever the describer reports no person — without re-running the describer (`ablate_nli.py`; results in §15).
- **E11 — Human check.** A 120-drawing blind single-coder sample drawn and laid out for coding (`human_check.py`); coding pending.

---

## 14. Evaluation metrics

Each measure is stated in plain words first.

**Valence-sign agreement.** *Do both readers land on the same side — positive or negative?* Formally, the proportion of records for which the sign of the prompt reader's top-1 family equals the sign of the image reader's top-1 family, over records whose prompt sign is non-zero. Note the wording: **valence-sign agreement**, never "mood direction".

**Family agreement.** *Do both readers pick the same emotion family?* The proportion of records where the two top-1 families are identical, in the shared seven-family space.

**Top-3 overlap.** *How much do the two readers' three best guesses overlap, weighted by confidence?* Each side's top-3 is normalised to sum to one — so the prompt reader's multi-label scores and the image reader's softmax are on a comparable scale — and the overlap is the sum of per-label minima, a distribution overlap bounded in [0, 1].

**Valence-arousal similarity.** *How close are the two readings on a two-dimensional emotion map?* This is the only quantity the project calls **similarity**, because it is a graded distance rather than a yes/no agreement. Each top-3 is mapped to a confidence-weighted centroid in valence-arousal space using fixed per-family coordinates, and similarity is one minus the normalised Euclidean distance. It has a mathematical floor of about 41% — it cannot reach zero — and random pairings average about 76%, so only movement above that band is meaningful.

**Random-pairing null and z.** For each subset, the image side is shuffled against the prompt side 300 times at seed 7 and every measure recomputed, giving a null mean and a standard deviation from which a z-score is taken. Degeneracy is detected from the null's spread and no z is printed for a degenerate measure. Every rate also carries a clustered-bootstrap 95% interval (10,000 draws resampling prompt groups, seed 7).

**Consistency (permutation null).** For each prompt drawn two or more times, the fraction of its drawings sharing the group's modal image family, averaged over groups; compared against a permutation null that shuffles the image readings across all 1,012 analysed records and re-cuts them into the same groups (10,000 draws, seed 7). Half the groups are pairs, so the measure cannot fall below 50%.

---

## 15. Results and analysis

**In simple English.** On prompts the text reader labels emotional, the two readers agree well above chance on every measure. Where the describer reports a face, the two readers agree far above chance; where it reports no person, an honest description of the drawing gives nothing above chance — the scene figure in the table comes from an expression the describer invented. On prompts the text reader labels neutral, agreement sits at chance, which is what it should do. The image reader is more consistent than chance across redraws of the same words, but far from fixed, and describing-then-extracting agrees with the prompt reader far more closely than asking the model directly.

**Technically.** All figures below are against the 300-shuffle random-pairing null, seed 7.

| Subset | Measure | Observed | Null | z |
| --- | --- | --- | --- | --- |
| Emotional, n=607 | valence-sign | 64.0% | 45.6% | +11.1 |
| Emotional, n=607 | family | 53.0% | 38.8% | +10.3 |
| Emotional, n=607 | top-3 overlap | 50.6% | 39.4% | +11.6 |
| Emotional, n=607 | valence-arousal | 83.8% | 77.3% | +12.2 |
| Face, n=402 | valence-sign | 73.9% | 53.5% | +10.4 |
| Face, n=402 | family | 61.9% | 45.8% | +10.3 |
| Scene, n=205 | valence-sign | 42.9% | 29.6% | +5.8 |
| Scene, n=205 | family | 35.6% | 26.2% | +4.4 |
| Neutral-labelled, n=405 | valence-arousal | 76.6% | 76.6% | +0.3 |

95% confidence intervals (clustered bootstrap, 10,000 draws, seed 7): emotional valence-sign [58.6, 68.8] and family [47.3, 58.7]; face valence-sign [68.3, 79.2] and family [55.8, 68.1]; scene valence-sign [33.1, 51.1] and family [26.4, 44.1]. Cohen's kappa for family agreement: emotional 0.23 [0.18, 0.29], face 0.30 [0.23, 0.37], scene 0.13 [0.06, 0.19] — fair, fair and slight on the Landis and Koch scale. Valence-sign denominators are the records whose prompt family has a sign: 530 of 607, 360 of 402, 170 of 205.

**Specificity.** Prompts the text reader labels neutral (n=405) return 76.6% against a null of 76.6%, z +0.3 — indistinguishable from chance, and the sole informative measure on that subset. Two caveats: 68 of the 405 (16.8%) contain a plain affect word (calm, content, tired, relaxed, stress), and two consist of a name alone; on the cleaned 335 the z is +0.04, still at the null. The set is therefore better described as prompts the text reader could not read affect from than as prompts with no feeling.

**Robustness to duplicate prompts.** On the 763 distinct prompts (452 emotional) all emotional-subset measures remain at z +9.3 to +10.8, and face-classified valence-sign agreement stands at 71.8% (n=319, z +8.4). The scene result **weakens substantially**: valence-sign 37.3% (n=133, z +3.5) and family 30.8% (z +2.6), and the latter does not survive a Holm–Bonferroni correction across the 36 non-degenerate z-scores (26 of 36 survive at family-wise 0.05; the ten that do not are the control cells, the single-valence valence-arousal and overlap cells, and distinct-prompt scene family). The headlines do not all hold equally under deduplication, and the scene finding is the one that softens.

**Consistency.** Across the 87 prompts drawn two or more times, the image reader returns the same emotion family for 68.8% of drawings within a group, against a permutation null of 59.4% (sd 2.1; 10,000 draws, seed 7), z +4.5, p = 0.0001; the same valence sign for 74.5% against 63.7%, z +5.0; and 28 of 87 groups are fully consistent against a null of 14.5, z +4.2. Half the groups are pairs, whose modal agreement cannot fall below 50%. The 68.8% figure is meaningless without its null and must never be quoted bare, and it measures the whole prompt→image→reader chain, not the generator alone.

**Method comparison.** Like for like — same GoEmotions prompt reader, same 607 emotional records, same measures, varying only the image reader — describe-then-extract reaches 53.0% family agreement against direct CLIP's 22.4% (+30.6 pp; clustered bootstrap 95% CI [+25.5, +35.6]; cluster-level sign-flip p < 0.0001; unclustered McNemar p = 3e-35), 64.0% valence-sign agreement against 31.1%, 50.6% top-3 overlap against 26.4%, and 83.8% valence-arousal similarity against 73.3%. Direct CLIP reads 283 of the 607 drawings as neutral. Neither reader has ground truth, so this ranks two image readers against a third model's labels: the two disagree, with describe-then-extract far closer to the text reader. The earlier figure of 49.3% against 25.3% (608 records, BART-MNLI on the prompt side, a v1 lexicon rule for the subset) is kept only as the historical v1 record. Note that direct CLIP's family z (+11.1) is higher than describe-then-extract's (+10.3) because its null is lower and tighter: z is distance from chance, not level of agreement.

**On face versus scene.** Both rates are reported against their own nulls and both clear them, and the difference has been tested (`significance.py`, 4 September): face minus scene is +30.9 pp [+22.6, +40.6] for valence-sign agreement and +26.3 pp [+18.4, +35.3] for family agreement, clustered permutation p = 0.0001 (10,000 draws, clustered on prompt identity). No ratio such as "1.7 times better" is quoted, because the two nulls differ; the difference with its interval is the statement.

**Template ablation (`ablate_nli.py`).** Each record's five cached describer answers were re-composed under an altered description template and only the NLI stage re-run; a control re-run of the unmodified template reproduces every baseline number exactly (0 of 1,012 top-1 readings change), so every difference is a template effect. Removing the expression sentence collapses agreement — all-emotional family 53.0% → 20.3% (null 16.6%, z +3.8), valence sign 64.0% → 15.3% (11.4%, z +5.1); fixing the expression word to "unclear" gives the same collapse (family 21.3%, z +3.9), and the reader's output falls to surprise or neutral (514 and 368 of 1,012). Removing the action, posture or scene clause moves the rates by 1–3 pp (family 50.6 / 51.4 / 53.4). Removing the people count raises rates and nulls together (scene valence sign 63.5% vs 50.9%, z +5.0): the "0" token pulls scene readings toward neutral, and z barely moves. Under a **people-aware template** — "A drawing showing {scene}." wherever the describer reports no person, every other record unchanged — the face rows are unchanged by construction (73.9% / 61.9%) and **scene agreement falls to its null**: valence sign 4.7% vs 3.4% (z +1.6), family 18.0% vs 17.3% (z +0.6); keeping the action and posture clauses gives 15.9% vs 11.6% (z +2.7) and 21.0% vs 16.8% (z +2.2). All-emotional under the people-aware template: sign 51.7% vs 36.9% (z +10.1), family 47.1% vs 34.5% (z +8.8).

Four readings follow. (1) The image reading rests on one word — the describer's expression answer — which is the same conclusion the 99.8% copy rate reaches independently; in effect the pipeline is "ask the describer for the facial expression and map that word to a family". (2) The scene result in the headline table (z +5.8) was an artefact of the template asserting a person and an expression for drawings with none; under an honest description this reader finds nothing above chance in scene-classified drawings. (3) The face/scene contrast is therefore "faces, and only faces, for this reader", not "faces more than scenes". (4) Whether scene drawings hold a feeling a person can read is exactly what the human check tests; a scene-capable describer is the main further-work item.

---

## 16. Key findings

**In simple English.** Agreement between the two readers is real and well above chance on emotional prompts; it is much stronger when a person's face is present; it sits at chance where the text reader finds nothing; the readings are more consistent than chance under repetition but far from fixed; and describe-then-extract agrees with the prompt reader far more closely than direct CLIP.

**Technically.**

1. **Agreement above the null is robust on emotional prompts.** All four measures clear their nulls at z +10 to +12 on n=607, and survive deduplication to 763 distinct prompts at z +9.3 to +10.8.
2. **Face-classified images show much higher agreement than scene-classified images** (valence-sign 73.9% vs 42.9%; family 61.9% vs 35.6%), each above its own null; the difference is +30.9 pp [+22.6, +40.6] on valence sign, clustered permutation p = 0.0001 — though the scene result weakens substantially on distinct prompts, and the split is the describer's own classification, not a human's. The template ablation sharpens this: under a people-aware description the scene rows fall to their null (valence sign 4.7% vs 3.4%, z +1.6), so for this reader the contrast is faces, and only faces — not faces more than scenes.
3. **The specificity check passes.** Where the prompt reader finds no emotion, valence-arousal similarity sits at the null (z +0.3), indicating the measures are not manufacturing agreement out of the metric's own structure.
4. **The image reader is more consistent than chance under repeated prompts, but far from fixed** (68.8% within-group same-family, permutation null 59.4%, z +4.5; 28 of 87 groups fully consistent against 14.5). This measures the whole prompt→image→reader chain, not the generator alone.
5. **Describe-then-extract agrees with the prompt reader far more closely than asking the model directly** (like for like: family 53.0% vs 22.4%, +30.6 pp [+25.5, +35.6], cluster-level p < 0.0001), which supports the supervisor's architectural redirection. Neither reader has ground truth, so this shows the two image readers disagree, with describe-then-extract closer to the text reader — not that either is more accurate.
6. **Graded similarity recovers structure that exact-label scoring hides.** The ladder from valence-arousal down to family agreement shows agreement is partial rather than absent, which is precisely the point of the similarity framing.

---

## 17. Limitations

**In simple English.** The single most important thing to say is that this project measures whether two computer programs agree with each other. It does not establish what a human being sees in these drawings.

**Technically.**

1. **Two automatic readers, not human perception.** Every result is prompt-reader / image-reader agreement. Nothing here establishes what a human perceives. This is the governing limitation and it qualifies every number above.
2. **Circularity in the face/scene split.** The split is not an expression detector. Of the 421 scene records, 414 (98.3%) are ones where the describer answered that no people are present, and 406 of those *do* contain an expression word. The split is driven by the people-count answer. The circularity is real, and its mechanism is specific: the same describer output supplies both the split variable and the text the emotion reader reads.
3. **Serial dependency on the describer.** Every image-side number is a reading of BLIP-VQA's output, not of the drawing itself. Its answers have not yet been validated against human coding, and it returns a confident facial-expression word even for records where it simultaneously reports that no people are present: of the 421 scene-classified records, 414 report no people, 406 of those still carry an expression word, and 332 answer "smile", "smiling" or "happy". Where the expression answer names an affective state (41% of records), the image reader's top-1 family follows it 99.8% of the time, so the "describe, don't ask" separation is weaker than it sounds: the extraction stage largely relays the expression word. The template ablation confirms it: removing the expression sentence collapses family agreement from 53.0% to 20.3% while removing any other clause moves it by 1–3 pp, and under a people-aware template the scene rows fall to their null — the headline scene result (z +5.8) was agreement with an invented expression. Describer error therefore propagates into every downstream measure, and it is the principal source of error in the pipeline. The error taxonomy confirms it: of the 38 high-confidence disagreements, 19 trace to the describer, 5 to the image reader, 12 to the prompt side and 2 to the drawing not depicting the prompt.
4. **The neutral-labelled control is the text reader's own output.** It was never checked by a human; 68 of its 405 prompts contain a plain affect word and two consist of a name alone. Only the valence-arousal measure is informative on it, and its z on the cleaned 335 is +0.04.
5. **"No unhandled errors" is a robustness claim.** It says nothing about accuracy; there is no ground truth to be accurate against.
6. **No colour claim.** The corpus is monochrome and there is no colour-control condition; the colour literature is motivation only.
7. **No positive-versus-negative claim.** It was withdrawn: those subsets have degenerate nulls and the two readers disagreed on the direction.
8. **Three families are too rare for family-level claims.** On the emotional prompts fear has n=16, anger n=12 and disgust n=1, and the image reader never returns disgust and returns fear four times across all 1,012 records; the surprise family is largely curiosity-mapped prompts. Claims are restricted to overall agreement and the face/scene contrast.
9. **A single generator, with unrecorded generation parameters.** The repeated-prompt groups pool text typed by different visitors and re-submissions by one; model version, seed and any system prompt are unknown, so the consistency result bounds the deployed system as a whole.
10. **Rounding and multiplicity.** The z is a standardised distance from a 300-shuffle null, not a p-value; across seeds 1–5 the headline valence-sign z ranges from +11.2 to +12.2. After a Holm–Bonferroni correction, 26 of the 36 non-degenerate z-scores survive; the distinct-prompt scene family result (z +2.6) does not.

Limitations addressed since the 4 September presentation and no longer listed: confidence intervals (now on every rate), a test of the face/scene difference (done, p = 0.0001), the consistency null (now scripted), degenerate-null detection (now automatic), hard-coded figures (now generated from the result files), the method comparison not being like for like (re-run), and the absence of numeric tests (`test_numeric.py`).

## 18. Future work

**In simple English.** Three things would materially strengthen this: ask humans what they see, use models actually built for drawings, and stop the describer inventing a face where there is none.

**Technically.**

- **Human validation.** The decisive next step, and the one that converts a reader-agreement result into a perception result. A 120-drawing blind single-coder sample has been drawn and laid out for coding (`human_check.py`: person present, readable face, valence, family); scoring it gives the describer's people-count and face-rule precision and recall, the reader's valence and family agreement with a human, and the face/scene contrast on a human-coded split. The full study — a stratified sample rated by several raters with inter-rater agreement reported first — would also supply the missing check on the neutral-labelled control set.
- **A scene-capable describer.** The people-aware template has been run as an ablation: once the invented person and expression clauses are removed, this reader finds nothing above chance in scene-classified drawings. Whether those drawings hold a feeling a person can read is what the human check tests; if they do, the main further-work item is a describer that reads affect from composition, posture and setting rather than from a facial-expression word — the candidates in `PIPELINE_DESIGN.md`, fed through the people-aware template as the default.
- **Drawing- and sketch-specific models.** The supervisor suggested exploring these; it was designed but not executed. Candidates are listed in `PIPELINE_DESIGN.md`; a sketch-domain describer is the most likely single source of improvement on scene-classified images, and it would feed the same template.
- **Breaking the circularity** in the face/scene split by deriving the split variable from a source independent of the text the emotion reader reads — a face detector run on the image, or the human codes above.
- **Continuous valence–arousal coordinates** from NRC-VAD per-family means in place of the hand-set centroids.
