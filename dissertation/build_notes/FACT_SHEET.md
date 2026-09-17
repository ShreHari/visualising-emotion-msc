# Fact sheet: everything a chapter may state, and the words to state it with

Everything below is verified against the code, the result files (`emoviz/outputs/*.json`) and
the project notes on 12 September 2026. If a fact is not here and not in the old chapter you
were given, do not write it. Numbers marked with a macro must be written as that macro.

## 1. The project

- Registered title (fixed, do not paraphrase in the title page): *Visualising Emotion: A
  Similarity-Based Analysis of Emotional Fidelity in Text-to-Image Generation*.
- Degree: MSc in Artificial Intelligence, School of Computer Science, University of Sheffield,
  module COM6912. Student: Shre Hari Prem Anandh. Supervisor: Dr Chaona Chen (psychologist;
  facial expression and cross-cultural emotion perception, Jack/Schyns Glasgow tradition).
- The project specification (comapps project 3199) said: analyse a dataset "collected from a
  previous public engagement event, where participants entered prompts describing their current
  emotions", each prompt "used to generate a corresponding image using the DALL-E model"; two
  possible strands, text analysis of the prompts and image analysis of "how effectively these
  images represent the emotions"; "you'll have the flexibility to select the focus".
- Submission deadline: Wednesday 23 September 2026 (extended from 16 September). Length limit
  10,000 to 20,000 words excluding references and appendices. Presentation given Friday 4
  September 2026 (a live demonstration was part of it).
- Timeline (all 2026): 18 June first meeting (get to know the dataset, start reading, get the
  template). 9 July meeting (two strands; six-section structure; "cite the evidence"). 17 July:
  dataset structure worked out (filename patterns, timestamps, pre-tests, repeats). Late July
  (meeting on or about 30 July): supervisor's methodological direction, see section 2. Early
  August: describe-then-extract pipeline built and run over all 1,025 images. 15 August: the
  demonstrator (local web app). 20 August meeting: demonstrator shown; decision to write up the
  computational results and treat a human-rated study as the next step. 1 September: first audit
  and corrections (positive-vs-negative direction withdrawn; a label-space mismatch in the
  direct-CLIP overlap fixed; face rule changed to token matching). 4 September: presentation.
  9 September: second audit against the marking criteria: clustered confidence intervals, Cohen's
  kappa, Holm correction, scripted consistency null, like-for-like reader comparison, control
  audit, describer audit and copy rate, error taxonomy, description-template ablation, single-coder
  sample drawn. 10 September: supervision meeting. 12 September: this rewrite. The single-coder
  check had not been coded at the time of writing.

## 2. Supervisor's direction (late July; the design follows it)

1. Similarity, not matching. Emotion is subjective, people disagree, models are noisy, so
   scoring a drawing right/wrong against a label is too crude. Measure how similar the two
   readings are; group emotions into families; treat "happy" and "excited" as close. She asked
   for this to be stated as the novel element.
2. Describe the drawing first, then extract the emotion from the description with a separate
   text model. Do not ask CLIP for an emotion (trained on colour photographs, good at objects).
3. Consider sketch- or drawing-specific models. (Designed, not run: listed as further work.)
4. Faces versus scenes: expect faces to be easier; handle the split.
5. Group the prompts: emotional versus non-emotional, analysed separately.
6. Data pre-processing: redact real names of private individuals; keep illness and grief
   content (not identifying on its own, essential to the analysis). Do NOT use the words
   ethics/approval/consent anywhere.
7. Build in an evaluation: an ablation, a comparison with another method, or human feedback.
   (All three were done: template ablation, direct-CLIP comparison, single-coder check.)
8. Marking: amount of work, quality of products and processes, writing, evaluation, supervisor
   engagement, presentation.

## 3. The corpus

- \nTotal{} prompt--drawing records from the Festival of the Mind, Sheffield, September 2024.
  The installation invited visitors to type how they were feeling; the interface accepted any
  text; each entry produced one drawing shown back to the visitor. A style instruction
  producing black-and-white line art was appended by the installation software and is not in
  the data.
- Data as supplied: one JSON file, a flat dictionary of 1,025 bare strings keyed "1".."1025",
  no labels, no metadata, no participant ids; and 1,025 PNG images linked to the text by
  position only.
- Three filename patterns (records 1--199 `img_00001.PNG` zero-padded; 200--999 `img_200.PNG`
  unpadded; 1000--1025 `img_t1000.PNG` with a t prefix); two files (records 2 and 4) have a
  lower-case `.png` extension. A naive loader resolves 199 of 1,025 (under a fifth).
- Every PNG carries a C2PA provenance manifest (a `caBX` chunk): software agent "DALL·E" with
  no version, no seed, no rewritten prompt. The RFC-3161 signing time inside it gives a
  per-image timestamp. Records 1--13 were generated between 26 August and 18 September 2024,
  before the festival, on scattered days: developer tests, excluded (\nPretest{}). Records
  14--1024 fall on 19--29 September 2024 (no records on 23 September; busiest days 28 and 29
  September). Record 1025 carries a 20 October 2024 timestamp and is kept.
- Analysed: \nAnalysed{}. Images 1024 by 1024 pixels, all monochrome line art.
- Prompts: median 4 words, mean about 6, longest 107 words; 294 single-word prompts among the
  analysed records (counted after redaction: the two name-only records collapse to one token); about 78% typed entirely in lower case; all ASCII; a few in Italian,
  French or German. Common entries: "happy" (\nHappy{} times), "curious", "ok", "excited",
  "pigs", "good", "hungry". Mixed feelings are common ("tired but happy", "tired proud happy",
  "hopeful, slightly anxious, resigned"). A substantial minority are not self-report: objects
  ("pigs"), pop culture ("mickey mouse", "disney characters"), questions to the machine,
  place names.
- Repeats: \nDistinct{} distinct prompts (case-folded, whitespace-stripped, computed on the
  text BEFORE redaction); \nRepeats{} records repeat an earlier prompt; \nGroups{} prompts
  appear two or more times covering \nGroupRecords{} records; \nPairGroups{} of those groups
  are pairs. Contributors unknown, at most \nDistinct{}.
- Name redaction: 8 records contain names of private individuals (friend, relative, teacher);
  the name becomes "[name]"; two records consisted of a name alone and reduce to the bare
  placeholder (\CtrlNameOnly{}). Detection tuned for recall (most prompts are lower case):
  NLTK given-name gazetteer (7,944 names), mid-sentence capitalised tokens absent from a
  236,000-word English dictionary, and naming phrases ("called X", "my friend X"). Every
  candidate has a reviewed keep/redact decision with a reason, scoped to its record (this is
  what stops "Jack Frost" and "woolly mammoth" being treated as people); the audit fails on any
  unreviewed candidate. Applied at load time; files on disk untouched. Re-reading the redacted
  prompts moves no family probability by more than 0.012 and changes no top-1 family. The
  decision table travels with the dataset, not the code (it names the tokens).
- Prompt-group key computed before redaction, because two different names both become "[name]"
  and would otherwise merge two prompts into one group (this happened once in development and
  the accounting test caught it). The key is case-insensitive but the prompt reader saw the text
  as typed, so a few groups mix readings ("Ok" and "ok"); no count changes.

## 4. The pipeline and the design

- Prompt reader: RoBERTa fine-tuned on GoEmotions (`SamLowe/roberta-base-go_emotions`, about
  125 million parameters), 28 categories (27 emotions + neutral) summed into seven families by
  the dataset authors' grouping (Appendix B), normalised, top three kept. Emotional prompt =
  top-1 family not neutral: \nEmotional{} emotional, \nNonEmotional{} neutral-labelled. The
  label is the reader's judgement, never human-checked.
- Rejected on the prompt side: zero-shot NLI (BART-MNLI) over-read surprise on short prompts
  (about a third of prompts came back surprise; 333 of 1,025 in the first run); the first
  version's hand-built lexicon was transparent but could not represent a blended prompt.
- Describer: BLIP-VQA (`Salesforce/blip-vqa-base`, about 385 million parameters) answers five
  fixed questions in order: facial expression, what the person is doing, body posture, how many
  people, what is in the picture. The word "emotion" appears in none. Answers cached per record.
- Rejected describers: Qwen2.5-VL-3B (the intended describer) exhausted the laptop's 16 GB,
  swapped for 4 h 45 min with no completed record, abandoned. Florence-2 failed on
  Transformers 5.14 (a `forced_bos_token_id` incompatibility). BLIP's plain caption was too
  terse and the reader collapsed almost everything to one family (surprise). GoEmotions applied
  to descriptions collapsed to neutral above 0.95 (it needs first-person feeling words).
- Template: "A drawing of {people} showing {scene}. The person is {action}, {posture}. The
  facial expression is {expression}." Applied to EVERY record, including those where people is
  "0" or "none". Written in the first week; its consequence only measured in September.
- Image reader: BART fine-tuned on MultiNLI (`facebook/bart-large-mnli`, about 407 million
  parameters), zero-shot by entailment, hypothesis "This scene conveys {family}", top three kept.
- Face-classified record = describer reports at least one person AND its expression answer
  contains a word from the fixed list (Appendix B), matched by token. Everything else is
  scene-classified. \nFaceAll{} face / \nSceneAll{} scene over all analysed records;
  \nFaceEmo{} / \nSceneEmo{} within the emotional prompts. Partly circular by construction: the
  class is defined from the same description the image reader reads.
- Run: all \nTotal{} images processed with no unhandled error (a robustness statement, not a
  correctness one), between about 1 and 12 seconds a record (slowing under memory pressure),
  crash-safe and resumable (JSONL checkpoint). Apple silicon, float16, Python 3.12, PyTorch
  2.13, Transformers 5.14; about 3.5 GB of model downloads. Direct-CLIP baseline: OpenCLIP
  ViT-B/32, LAION-2B weights, prompted with the seven families, output frozen in a file.
- The four measures (definitions in the old chapter 3, keep the equations and labels eq:va,
  eq:overlap, eq:family, eq:sign): valence--arousal similarity (score-weighted centroid
  distance on the circumplex; hand-placed centroids; floor 0.412 for joy vs sadness; random
  pairs already average about \FullNeuVaNull{}); top-3 soft overlap (sum of per-family minima
  after normalising each side); family agreement (top-1 match rate); valence-sign agreement
  (+ joy; - sadness/anger/fear/disgust; 0 surprise/neutral; denominator excludes unsigned
  prompts: \FullEmoNSign{} of \FullEmoN{}).
- Random-pairing null: \nullShuffles{} random re-pairings of the image readings with the
  prompts, seed \nullSeed{}; z = (observed - null mean)/null sd (eq:z). z is an ordering
  statistic: across seeds 1--5 the headline valence-sign z moves between \ZSeedMin{} and
  \ZSeedMax{} while the null mean stays within a tenth of a point. Degenerate null = sd 0 (every
  prompt in the subset shares one label); detected from the null's own spread; no z printed.
- Inference: clustered bootstrap over prompt groups, \DiffDraws{} draws, 95% percentile
  intervals; clustered permutation test of the face/scene difference (labels permuted across
  groups, p = (k+1)/(P+1), smallest reportable 0.0001; eq:permp); Cohen's kappa with
  Landis--Koch bands (eq:kappa); Holm--Bonferroni over the \HolmM{} non-degenerate z (the
  normal approximation is nominal for the largest z and affects no decision); McNemar exact test
  (unclustered, optimistic) plus a cluster sign-flip test with \McClusterDraws{} draws for the
  two-reader comparison; Wilson intervals for the single-coder proportions.
- Consistency: for each repeat group, the share of its drawings that receive the group's modal
  image family; mean over the \nGroups{} groups; read against a permutation null that shuffles
  image families over all analysed records and re-cuts the same groups (\ConsDraws{} draws).
  Bounds the whole prompt-to-image-to-reader chain; cannot isolate the generator (no seed, no
  rewritten prompt); cannot separate one visitor typing twice from two visitors.
- One module (`emoviz/metrics.py`) holds the only definition of every measure, constant, split
  rule and the null; every script imports it. Before it existed two scripts carried slightly
  different overlap formulas.
- Tests: a shell smoke suite (environment, corpus integrity, cached outputs, redaction audit,
  every analysis script to a clean exit, a live three-image pipeline run on fresh images, the
  figure build; exits non-zero on failure) plus `test_numeric.py`, which pins every headline
  number in this document to the JSON file that produces it within a tolerance and unit-tests
  the measures (the 0.412 floor, symmetry, overlap bounds and scale invariance, the sign map,
  the face rule). Do not quote a count of checks. Figures (`make_figures.py`) and every number
  and table in this document (`export_tex.py`) are generated from the same JSON files.
- Demonstrator: a local Flask web app (`app.py` + `web/index.html`, port 5050) that runs the
  real models on any analysed record or an uploaded image; shows the five answers, the composed
  description, both readings, and the four measures against the same null the analysis uses
  (computed at start-up from the result files). The valence--arousal axis starts at its floor
  and shades the middle half of random pairings; the verdict leads with valence sign and family;
  a degenerate chance level is stated as such. Nothing typed or uploaded is stored; the request
  log is suppressed. Models pre-warm in float16 (about 1.8 GB); first request about 40 s cold,
  about 9 s warm. Used in the 20 August supervision and the 4 September presentation. Not a
  data-collection instrument.
- Single-coder check: 120 drawings, stratified on the describer's output (40 face-classified,
  40 scene-classified with no people reported, every record with a vague or word-only people
  answer, topped up equally from the first two strata), fixed by seed, laid out on six numbered
  contact sheets showing nothing but the drawings; coder (the author) fills person y/n, readable
  face y/n, valence +/-/0, family; blind to prompt, description and readings. Scoring gives the
  describer's people-count accuracy, the face rule's precision and recall, what lies behind the
  "smiling" answers, the image reader's valence against the coder, and the face/scene contrast
  recomputed on the coder's split (the one estimate that breaks the circularity). NOT CODED at
  the time of writing: the results section must say so and be written so the numbers can be
  dropped in (the generated table `tab_humancheck` renders a pending note until then).

## 5. Results (write every number as its macro; the values are for your understanding only)

Overall, emotional prompts (n = \FullEmoN{}): valence sign \FullEmoSignObs{} vs null
\FullEmoSignNull{} (z \FullEmoSignZ{}, CI \FullEmoSignCi{}, denominator \FullEmoNSign{});
family \FullEmoFamObs{} vs \FullEmoFamNull{} (z \FullEmoFamZ{}, CI \FullEmoFamCi{}); overlap
\FullEmoOvlpObs{} vs \FullEmoOvlpNull{} (z \FullEmoOvlpZ{}); VA \FullEmoVaObs{} vs
\FullEmoVaNull{} (z \FullEmoVaZ{}). The loosest measure has the largest z and the smallest gap
in points (its null is high and tight because of the floor).

Face vs scene (within emotional): face (n \FullFaceN{}) sign \FullFaceSignObs{} vs
\FullFaceSignNull{} (z \FullFaceSignZ{}, CI \FullFaceSignCi{}), family \FullFaceFamObs{} vs
\FullFaceFamNull{} (z \FullFaceFamZ{}); scene (n \FullSceneN{}) sign \FullSceneSignObs{} vs
\FullSceneSignNull{} (z \FullSceneSignZ{}, CI \FullSceneSignCi{}), family \FullSceneFamObs{} vs
\FullSceneFamNull{} (z \FullSceneFamZ{}). Difference face minus scene: \DiffSignPp{} (CI
\DiffSignCi{}) on sign, \DiffFamPp{} (CI \DiffFamCi{}) on family, clustered permutation
p = \DiffSignP{} on both. VA similarity does not separate the classes (\FullFaceVaObs{} vs
\FullSceneVaObs{}).

Distinct prompts only (\nDistinct{} records, \nDistinctEmo{} emotional): face (n \DistFaceN{})
sign \DistFaceSignObs{} (z \DistFaceSignZ{}), family \DistFaceFamObs{} (z \DistFaceFamZ{});
scene (n \DistSceneN{}) sign \DistSceneSignObs{} (z \DistSceneSignZ{}), family
\DistSceneFamObs{} (z \DistSceneFamZ{}, does NOT survive Holm; suggestive only).

Holm: \HolmM{} non-degenerate z tested, \HolmSurvive{} survive at family-wise 0.05, \HolmFail{}
do not (the control cells, the single-valence VA/overlap cells, the distinct-prompt scene family).

Specificity check, neutral-labelled prompts (n \CtrlN{}): only VA is informative:
\CtrlVaObs{} vs \CtrlVaNull{} (record-level z \CtrlVaZ{}; clustered z \CtrlVaZClustered{});
family equals its null exactly (\CtrlFamObs{}) because every prompt shares the label; sign has a
zero denominator. Control audit: \CtrlFlagged{} of \CtrlN{} (\CtrlFlaggedPct{}) contain one of
\CtrlLexicon{} plain affect words (most often \CtrlTopWords{}); \CtrlNameOnly{} are the bare
placeholder; cleaned control n \CtrlCleanN{}: \CtrlCleanVaObs{} vs \CtrlCleanVaNull{} (z
\CtrlCleanVaZ{}). The null's spread here is tiny (\CtrlVaSd{}) so observed and expected are
bound to coincide: a weak check, passed.

Two image readers, like for like (same prompt reader, same \McN{} records, same measures and
re-pairings): family \McDeFam{} vs \McClipFam{} (difference \McDiffFamPp{}, CI \McDiffFamCi{},
cluster sign-flip p \McClusterFamP{}, unclustered McNemar p = \McMcNemarFamP{}); sign \McDeSign{}
vs \McClipSign{} (\McDiffSignPp{}, CI \McDiffSignCi{}); overlap \McDeOvlp{} vs \McClipOvlp{}; VA
\McDeVa{} vs \McClipVa{}. Of \McN{}: \McFamB{} only describe-then-extract agrees on, \McFamC{} only
CLIP, \McFamBoth{} both, \McFamNeither{} neither. CLIP's family z (\McClipFamZ{}) exceeds
describe-then-extract's (\McDeFamZ{}) although its rate is far lower, because its null is lower
and tighter (it reads \McClipNeutral{} of the \McN{} images as neutral). The two image readers
agree with each other on only \McReaderAgree{} of top-1 families. Neither has ground truth: the
comparison shows two readers disagree and one sits closer to the prompt reader, not that one is
more correct. The v1 comparison (\McVOneN{} records, NLI prompt side, different overlap formula:
\McVOneDeFam{} vs \McVOneClipFam{}) is a historical record only (Table tab:methodvone), not
quoted as a result.

Consistency (\nGroups{} groups, \nGroupRecords{} records, \nPairGroups{} pairs): same family
\ConsFam{} (CI over groups \ConsFamCi{}) vs null \ConsFamNull{} (sd \ConsFamNullSd{}), z
\ConsFamZ{}, p \ConsFamP{}; same valence \ConsVal{} vs \ConsValNull{} (z \ConsValZ{}); fully
consistent groups \ConsFull{} of \nGroups{} (\ConsFullPct{}) vs \ConsFullNull{} expected (z
\ConsFullZ{}). "happy" drawn \ConsHappyN{} times: joy \ConsHappyJoy{}, neutral
\ConsHappyNeutral{}, surprise \ConsHappySurprise{}. Pairs have a 50% floor.

Per family (emotional records): prompt side joy \RecJoyN{}, sadness \RecSadnessN{}, surprise
\RecSurpriseN{}, fear \RecFearN{}, anger \RecAngerN{}, disgust \RecDisgustN{}. Recall by prompt
family: joy \RecJoy{} (CI \RecJoyCi{}), sadness \RecSadness{} (CI \RecSadnessCi{}), anger
\RecAnger{} (n \RecAngerN{}), surprise \RecSurprise{} (CI \RecSurpriseCi{}), fear \RecFear{}.
Image reader never returns disgust; returns fear \famImageFear{} times in \nAnalysed{}. Kappa:
emotional \KappaEmo{} (CI \KappaEmoCi{}, \KappaEmoBand{}), face \KappaFace{} (\KappaFaceBand{}),
scene \KappaScene{} (\KappaSceneBand{}). In practice a three-family ladder (joy, sadness,
neutral) with anger a distant fourth. Surprise is largely curiosity-mapped prompts.

Describer audit (all analysed): people count crossed with expression word: \DescPeopleExpr{} /
\DescPeopleNoExpr{} / \DescNoPeopleExpr{} / \DescNoPeopleNoExpr{}. Of \DescSceneN{}
scene-classified, \DescScenePeopleZero{} report no people; \DescScenePeopleZeroExpr{} of those
still carry an expression word; \DescSceneSmile{} answer smile/smiling/happy (\DescSceneSmilePct{}
of the no-people records). Smile rate \DescSmileFace{} of the \nFaceAll{} face-classified,
\DescSmileAll{} of all analysed (always give the denominator). Copy rate: where the expression
answer names an emotion outright (\DescBareStrictN{} records, \DescBareStrictPct{} of the corpus)
the image reader's top-1 equals that word's family \DescCopyStrict{} of the time; broad
definition (facial actions like smile/crying, \DescBareBroadN{} records) \DescCopyBroad{}:
\DescCopyBroadPeople{} where a person is reported, \DescCopyBroadPeopleZero{} where none (the
"0 people" token pulls readings towards neutral).

Error taxonomy: \TaxN{} emotional records with both readers' top-1 at 0.8 or above and
different families (\TaxDistinct{} distinct prompts; below the intended sample of 40 so all
examined). Primary mode from the drawing: describer \TaxDescriber{} (\TaxA{} invented a face or
expression, \TaxB{} misread one), image reader \TaxReader{}, prompt side \TaxPrompt{} (\TaxD{}
mixed/ambiguous, \TaxF{} prompt reader wrong), generator \TaxGenerator{}. \TaxPeopleZero{}
carry the people=0 tag; 7 of the \TaxA{} invented-expression records do. Joy-to-neutral cell is
one mechanism: low-arousal positive prompts ("grateful", "calm but tired") have no family in the
seven, the describer answers "calm" or "smile", the reader returns neutral. The mixed-prompt
detector looked for connectives (but/although) and caught none of the 11 mixed prompts because
visitors list feelings without connectives ("tired proud happy"); a list detector would do better.

Ablation (NLI stage only re-run; control re-run of the unmodified template changes
\AblControlChanged{} top-1 readings, so differences are template effects): drop the expression
sentence: family \FullEmoFamObs{} to \AblDropExpressionEmoFamObs{} (null
\AblDropExpressionEmoFamNull{}, z \AblDropExpressionEmoFamZ{}), sign \FullEmoSignObs{} to
\AblDropExpressionEmoSignObs{} (null \AblDropExpressionEmoSignNull{}, z
\AblDropExpressionEmoSignZ{}), face sign to \AblDropExpressionFaceSignObs{}; the reader's output
falls to surprise for \AblDropExpressionSurprise{} and neutral for \AblDropExpressionNeutral{}
of \nAnalysed{} records. Expression fixed to "unclear": family \AblFixedExpressionEmoFamObs{}
(z \AblFixedExpressionEmoFamZ{}). Drop action / posture / scene: family
\AblDropActionEmoFamObs{} / \AblDropPostureEmoFamObs{} / \AblDropSceneEmoFamObs{} (one to three
points). Drop the people count: rates and nulls rise together (scene sign
\AblDropPeopleSceneSignObs{} vs \AblDropPeopleSceneSignNull{}, z \AblDropPeopleSceneSignZ{}).
People-aware template ("A drawing showing {scene}." wherever no person is reported; everything
else unchanged): face rows identical by construction (\AblPeopleAwareFaceSignObs{},
\AblPeopleAwareFaceFamObs{}); scene falls to its null: sign \AblPeopleAwareSceneSignObs{} vs
\AblPeopleAwareSceneSignNull{} (z \AblPeopleAwareSceneSignZ{}), family
\AblPeopleAwareSceneFamObs{} vs \AblPeopleAwareSceneFamNull{} (z \AblPeopleAwareSceneFamZ{});
restoring action and posture: \AblPeopleAwareNoExpressionSceneSignObs{} vs
\AblPeopleAwareNoExpressionSceneSignNull{} (z \AblPeopleAwareNoExpressionSceneSignZ{}) and
\AblPeopleAwareNoExpressionSceneFamObs{} vs \AblPeopleAwareNoExpressionSceneFamNull{} (z
\AblPeopleAwareNoExpressionSceneFamZ{}); all emotional under people-aware: sign
\AblPeopleAwareEmoSignObs{} (z \AblPeopleAwareEmoSignZ{}), family \AblPeopleAwareEmoFamObs{}
(z \AblPeopleAwareEmoFamZ{}).

The main finding, stated correctly: for this reader, drawings where the describer reads a face
agree far above chance; scene drawings show nothing above chance once the invented expression
is removed from their description. "Faces, and only faces, for this reader" is the short form
(use it at most once, and not as a closer). It is a finding about a measurement chain, not about
what a person would see.

## 6. Hand-typed numbers that are allowed (everything else is a macro)

1,025 / 13 / 1,012 may be typed ONLY inside the title page or captions where a macro cannot be
used; in prose use \nTotal{}, \nPretest{}, \nAnalysed{}. Allowed by hand: median 4 words; mean
about 6; 107 words (longest); 294 single-word prompts (after redaction); about 78% lower case; 8 redacted records;
7,944 names; 236,000-word dictionary; 0.012 probability shift; 1024 by 1024 pixels; 19--29
September 2024; 26 August to 18 September 2024; 20 October 2024; 16 GB; 4 h 45 min; 3 billion
parameters (Qwen); about 125 / 385 / 407 million parameters; about 3.5 GB; 1 to 12 seconds a
record; about 40 s cold / 9 s warm; 1.8 GB; port 5050; 0.412 (the floor; also the macro-free
constant in eq:va); 0.8 (the taxonomy confidence threshold); 40 (intended taxonomy sample);
120 drawings; 40 / 40 strata; six contact sheets; seven families; 28 categories; five questions;
four measures; the 300 shuffles and seed 7 ONLY via \nullShuffles{} and \nullSeed{}; 97 papers
read, 24 excluded, 73 retained, eight themes; 91 references in the bibliography; 0.05
family-wise level; 95% intervals; 1989 etc. inside other people's findings as in the old text
(e.g. GoEmotions 58,000 comments, macro-F1 0.46; Cowen and Keltner 27 categories; Lomas 24
raters, 240 images, ten emotions, 0--10 scale; EmoSet 118,000 images; ArtEmis 439,000
utterances; NRC 20,000 and 55,000 words; CLIP 400 million pairs; Ragot 565 participants; Chang
et al. 'line art'/'black and white' keywords; Millet/Horton ten experiments). Do not add any
other number.

## 7. Records that may be quoted (prompt text exactly as typed) and their readings

Safe: 14 "very excited to be here", 31 "optimistic happy", 35 "disney characters", 36 "mickey
mouse", 45 "absolutely fantastic", 50 "inspired and overwhelmed in equal measure", 58 "How are
you feeling?", 59 "happy, creative, emotional", 63 "super tired" (face-classified; describer:
expression sad, sitting, bent, 1 person, "woman drinking"; image reader sadness; prompt reader
sadness; the demonstrator example), 64 "intrigued optomistic tired hazy", 65 "hopeful slightly
anxious resigned detached appreciating", 68 "how can a circle be squared", 73 "I don't know",
79 "sunny day with friends", 89 "grateful" (describer: calm, sitting, 1 person, "man sitting on
mountain"; reader neutral; prompt joy), 93 "celebratory anguish", 100 "i like football", 102
"stressed tired", 109 "neutral, relaxed, exploring stuff ,curious, peaceful", 126 "i am deep in
thought.", 129 "chilled out", 132 "I feel bored", 137 "i am excited" (scene-classified because
the describer reported 0 people; answers: angry, yelling, mouth, 0, "face"; reader anger; the
drawing is a screaming face; in the taxonomy as a generator failure), 201 "tired but happy"
(face-classified; three faces, smile; reader joy; prompt joy; the title-slide drawing), 21
"che bello essere qui! ma fa freddo" (Italian; scene of mountains; describer said 0 people
and expression "smiling"; reader joy), 258 "pigs" (drawing of pigs; describer 0 people,
expression "smiling"; reader joy; prompt reader neutral/disgust-ish, treat as neutral-labelled),
242 "love" (drawing of an apple; describer 0 people, "no person", expression "sad"; reader
sadness; prompt joy), 594 "excited and happy" (crowd singing; describer expression "surprise";
reader surprise; prompt joy), 692 "calm but tired. Happy that it is the weekend", 988 "tired
proud happy", 1011 "proud happy tired", 436 "an impressed baby in a bearsuit", 547 "confused",
608 "excited", 726 "good", 829 "good wierd", 970 "hope and care", 39 (long "feeling at peace as
a women, sitting by the fire place reading a novel ..." prompt; describer read the expression
as sad; reader sadness; prompt joy). "pigs" appears 8 times, "curious" 12 times, "excited for
the cold and christmas" 8 times, "tired happy proud" 6 times, "hungry" 6 times.
FORBIDDEN (never quote, describe, or show): 216, 300, 302, 532, 750, 751, 858, 982, 1020, any
record containing "[name]", and records 1--13.

## 8. Figures and tables: file names, labels, and what each shows

Figures (all in `figures/`; include with `\includegraphics[width=...]{name}` without extension;
PDF preferred where both exist):
- `examples` (PNG) label fig:examples: six records (63, 201, 594 face-classified; 21, 258, 137
  scene-classified) with prompt, class and the two readings. Chapter 1.
- `pipeline` (TikZ, `\input{figures/pipeline}` inside `\resizebox{\textwidth}{!}{...}`) label
  fig:pipeline: the describe-then-extract pipeline and the ladder and null. Chapter 3.
- `fig5_dataset` label fig:dataset: composition bar (402 / 205 / 405 / 13). Chapter 3.
- `fig_timeline` (NEW) label fig:timeline: records per day from the recovered timestamps, the
  13 pre-festival tests shown apart. Chapter 3, pre-processing.
- `fig_prompt_length` (NEW) label fig:promptlength: histogram of prompt word counts. Chapter 3,
  corpus.
- `coding_sheet` (PNG) label fig:codingsheet: the first contact sheet. Chapter 3, single-coder
  check.
- PLACEHOLDER label fig:installation: photograph of the installation (optional). Chapter 3,
  corpus. Use `\placeholderfigure{...}` as defined in main.tex.
- PLACEHOLDER label fig:demo: screenshot of the demonstrator after running record 63. Chapter 3,
  demonstrator section.
- `fig3_z_by_prompt_group` label fig:zgroup: z by prompt group and measure. Chapter 4, overall.
- `fig1_face_vs_scene` label fig:facescene: face vs scene bars with CIs and nulls. Chapter 4.
- `fig2_method_comparison` label fig:method: two readers like for like. Chapter 4.
- `fig4_consistency` label fig:consistency: "happy" x42 and within-group agreement vs null.
  Chapter 4.
- `fig_happy_grid` (NEW) label fig:happygrid: twelve of the 42 drawings of "happy" with the
  image reader's family under each. Chapter 4, consistency.
- `fig6_confusion` label fig:confusion: prompt family vs image family heat map. Chapter 4.
- `fig_no_person_expression` (NEW) label fig:noperson: four scene-classified drawings where the
  describer reported no person yet named an expression, with its five answers. Chapter 4,
  describer section.
- `fig7_error_taxonomy` label fig:taxonomy: failure-mode counts. Chapter 4.
- `fig8_ablation` label fig:ablation: the template ablation bars. Chapter 4.
- PLACEHOLDER label fig:testsuite: terminal screenshot of `bash emoviz/test.sh` passing.
  Appendix A.

Tables (all `\input{generated/tab_xxx}`): tab_headline (tab:headline, main table), tab_difference
(tab:difference), tab_distinct (tab:distinct), tab_holm (tab:holm), tab_control (tab:control),
tab_method (tab:method), tab_methodvone (tab:methodvone), tab_consistency (tab:consistency),
tab_confusion (tab:confusion), tab_kappa (tab:kappa), tab_families (tab:families), tab_describer
(tab:describer), tab_taxonomy (tab:taxonomy), tab_ablation (tab:ablation), tab_humancheck
(tab:humancheck, renders a pending note until coded).

Equations keep their old labels: eq:va, eq:overlap, eq:family, eq:sign, eq:z, eq:permp, eq:kappa.
Chapter and section labels: keep exactly the old ones (listed in `labels_old.json`), so that
cross-references written by different agents resolve.

## 9. Non-claims (must appear, in the author's words, in the Discussion and be respected everywhere)

- No claim about what a person sees. Every number is agreement between two machine readers.
- No positive-versus-negative direction (single-valence nulls are degenerate; the two image
  readers point opposite ways; the first build said negative survives, the second said positive
  aligns best, both withdrawn).
- No claim about colour (no colour condition; the colour literature is motivation only, and
  Alvarado 2025 models colour features only and is silent about line).
- No claim about the generator alone from the consistency result.
- No family-level claim for fear, anger, disgust (too rare on the prompt side; the reader never
  returns disgust); surprise is largely curiosity-mapped prompts.
- Records are not people.

## 10. Literature (chapter 2) facts to preserve

97 papers read, scored on relevance and evidence strength, 24 excluded (surveys, position
pieces, off-target), 73 retained in eight themes, plus seminal foundations kept by exception
(Ekman 1992, Russell 1980); 18 methodological references added on 9 September for the models and
statistics; 91 entries in total. Eight themes: emotion theory and taxonomy; emotion from text;
datasets, benchmarks and lexicons; text-to-image generative models; image evaluation metrics and
frameworks; emotion in generated images (the intersection); emotion perception and human
judgement (incl. the supervisor's work); context (public reception of AI art). The gap: no work
measures agreement between the emotion recoverable from a short, unmediated, mixed-affect
first-person self-report and the emotion recoverable from a colour-free line drawing made from
it, nor how stable that reading is when the same words are drawn again. Contribution = corpus +
question + null-referenced similarity ladder + consistency experiment + audited toolkit; NOT a
new metric or a new classifier. The word for other people's prompt/image correspondence is
"alignment"; this project's word is "agreement".
