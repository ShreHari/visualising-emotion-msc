# Chapter briefs

One brief per file to write. Each brief gives: the file, the target length, the sections and labels
(keep the labels exactly, other chapters reference them), what the chapter must contain (taken from
the old chapter, which you must also read for the full argument), which figures and tables to place,
which bibliography keys the chapter owns (each must be cited in it), and chapter-specific cautions.
The style contract is `STYLE_GUIDE.md`; the facts are `FACT_SHEET.md`; the macros are `MACROS.md`;
the keys are `BIBKEYS.md`. Old chapters live in `report/chapters/`.

General rules for every chapter
- Write the whole chapter in one go as valid LaTeX for the `book` class, starting with `\chapter{...}`
  and `\label{...}`, no preamble, no `\begin{document}`.
- Every statistic is a macro `\Name{}`. Tables are `\input{generated/tab_xxx}`. Figures use the
  file names and labels in FACT_SHEET section 8 (`\includegraphics[width=\textwidth]{fig1_face_vs_scene}`
  etc.; extension omitted). Placeholders use `\placeholderfigure{label}{caption}{instructions}`.
- Keep the old chapter's ARGUMENT and ORDER OF IDEAS, and all of its facts, but write every sentence
  fresh. Do not reuse its sentences, its openers, its closers or its metaphors. Where the old chapter
  had a memorable turn of phrase, do not keep it; state the point plainly instead.
- Before returning, run `python3 dissertation/build_notes/check_tex.py <your file>` and fix every
  phrase hit, every undefined macro, unknown cite key and undefined ref, and every uniform paragraph.
  Run it again until the phrase-hit list is empty (or every remaining hit is a false positive you can
  justify, e.g. "robustness check", "match" inside the sentence saying the project does not do
  matching, "alignment" describing other people's work, "convey" inside the fixed hypothesis string).
- Do not write a "summary" paragraph at the end of a section. Do not end a chapter with a
  one-sentence flourish. Chapter 4 ends with a numbered summary of findings because the old one did;
  that is a list of facts, not a flourish.

---------------------------------------------------------------------------------------------------

## abstract.tex  (target 320 to 380 words, one page)

Starts `\chapter*{\Large \center Abstract}`. Three paragraphs: (1) the setting and the question
(festival, \nTotal{} records, \nAnalysed{} analysed, no ground truth so two readers, describe-then-
extract, similarity not matching, four measures, every value against a random-pairing null, clustered
on prompt groups because \nRepeats{} records repeat a prompt); (2) the results with macros
(\FullEmoSignObs{} vs \FullEmoSignNull{}, z \FullEmoSignZ{}; family \FullEmoFamObs{} vs
\FullEmoFamNull{}; survive distinct-prompt re-run and Holm; face \FullFaceSignObs{} vs scene
\FullSceneSignObs{}, difference \DiffSignPp{} CI \DiffSignCi{} p \DiffSignP{}; neutral prompts at
chance; describe-then-extract \McDeFam{} vs direct CLIP \McClipFam{}; consistency \ConsFam{} vs
\ConsFamNull{}); (3) the audits and what they mean (describer names an expression for
\DescScenePeopleZeroExpr{} of \DescScenePeopleZero{} no-person scene drawings; copy rate
\DescCopyStrict{}; ablation: expression word removed collapses agreement, people-aware template leaves
faces unchanged and brings scenes to chance; findings are about a measurement chain; the single-coder
check and a human-rated study are the next step; contribution = corpus and question, null-referenced
ladder, consistency experiment, audited toolkit and demonstrator). No citations in the abstract.

## chapter1.tex  Introduction  (target 1,600 to 1,900 words)

Sections and labels: `\chapter{Introduction}\label{ch:intro}`; `\section{Context}\label{sec:intro-context}`;
`\section{The question}\label{sec:intro-question}`; `\section{Aims and objectives}\label{sec:intro-aims}`;
`\section{Contributions}\label{sec:intro-contributions}`; `\section{Overview of the report}\label{sec:intro-overview}`.

Must contain: the festival installation (September 2024, visitors typed how they felt, a
text-to-image model returned a black-and-white line drawing shown back to them; \nTotal{} records;
handed over with no labels, no metadata, no record of who typed what); the two properties that
shaped the work (short personal entries: median four words, a quarter single words, common words
happy/tired/excited, mixed feelings; monochrome: a line-art instruction was appended so colour, the
strongest carrier of affect in generated images per Alvarado \cite{alvarado2025texttoimage}, is
absent); the shape of the corpus (free text so a minority are not self-report: "pigs", pop culture,
questions; records not people; \nRepeats{} of \nAnalysed{} repeat a prompt; contributors at most
\nDistinct{}); Figure~\ref{fig:examples} (six records; 63 and 201 are the demonstrator examples;
21 is a mountain scene the describer called smiling). The question stated plainly, and why it is
narrow (no ground truth, nobody rated the drawings, two readers stand in, agreement not perception,
the human study is the next step). The similarity framing from the supervisor and why matching is
wrong for emotion (people disagree, models noisy, labels overlap; Cowen and Keltner
\cite{cowen2017self} 27 categories on gradients; Russell's circumplex \cite{russell1980circumplex,
posner2005circumplex}; a drawing read as excited for a prompt "happy" should not count as a total
miss); the ladder of four measures; the null (floor 0.41 for the loosest measure, random pairs
already about \FullNeuVaNull{}). Aim and the eight objectives (image reader without asking for an
emotion; ladder plus null; whole corpus and the two splits; formal test of face/scene and the
repeated-prompt robustness; like-for-like comparison with direct CLIP; consistency from repeated
prompts; audits: control, describer, taxonomy, ablation, single-coder check; reproducible toolkit
with pinned tests and a demonstrator). Contributions, honestly bounded: the toolkit is existing
models recombined; new are the object (unmediated mixed-affect public self-report as colour-free
line art; closest prior study Lomas and colleagues \cite{lomas2024improved} used a fixed ten-item
typology on a person or robot in colour), the question, the null-referenced ladder with clustered
inference and a formal test of the one designed contrast, the consistency experiment, and the audits
that show where the instrument is weak with numbers. Deliverables (code, result tables, demonstrator,
two-layer tests, audits; every statistic a generated macro). Overview of chapters.

Keys owned: alvarado2025texttoimage, cowen2017self, russell1980circumplex, posner2005circumplex,
lomas2024improved.

Cautions: first person is natural here ("I was given", "I built"). Do not open with a grand
sentence about AI. Open with what happened at the festival. Vary paragraph length.

## chapter2.tex  Literature Review  (target 3,800 to 4,300 words)

Sections and labels: `\chapter{Literature Review}\label{ch:lit}`; `\section{Scope and method of the
review}\label{sec:lit-scope}`; `\section{Foundations: emotion theory and taxonomy}\label{sec:lit-theory}`;
`\section{Emotion from text}\label{sec:lit-text}`; `\section{Datasets, benchmarks and
lexicons}\label{sec:lit-data}`; `\section{Text-to-image generative models}\label{sec:lit-t2i}`;
`\section{Image evaluation: metrics and frameworks}\label{sec:lit-eval}`; `\section{The intersection:
emotion in generated images}\label{sec:lit-intersection}`; `\section{Emotion perception and human
judgement}\label{sec:lit-perception}`; `\section{Context}\label{sec:lit-context}`; `\section{The
gap}\label{sec:lit-gap}`.

Must contain (see FACT_SHEET section 10 and the old chapter for the per-paper claims): how the
review was done (97 read, scored on relevance and evidence strength, 24 excluded with reasons
logged, 73 kept, eight themes; foundations kept by exception; started from eight papers the
supervisor supplied and followed citations outward); the alignment/agreement wording note; every
paper's finding as the old chapter states it, in new words, with its citation. Each section should
end by saying what the theme meant for this project's decisions, but say it differently each time
(sometimes one sentence in the middle, sometimes a short paragraph, never a repeated formula).
The gap section must state the gap precisely and contrast it against each neighbour (compositional
metrics, Lomas, conditional generators, visual-emotion recognisers), then the two questions the
dissertation answers and the one it declines (what a person sees).

Keys owned (all must be cited in this chapter): ekman1992argument, russell1980circumplex,
posner2005circumplex, cowen2017self, jack2012facial, jack2014dynamic, chen2018distinct,
chen2018reverse, chen2020building, chen2024cultural, demszky2020goemotions, harutyunyan2026fine,
yang2023context, liu2023emotion, bhat2024emotion, buechel2017emobank, mohammad2018obtaining,
mohammad2025nrc, mohammad2013crowdsourcing, tausczik2010psychological, zanwar2022improving,
niu2025contrastive, parkington2025human, grootendorst2022bertopic, yin2019benchmarking,
lewis2020bart, williams2018broad, raffel2020exploring, chung2022scaling, wolf2020transformers,
yang2023emoset, machajdik2010affective, marchewka2014nencki, kosti2020context, achlioptas2021artemis,
mohamed2022artelingo, mohammad2018wikiart, saravia2018carer, mohammad2018semeval,
muhammad2025semeval, kirstain2023pick, wu2023human, xu2023imagereward, ramesh2021zero,
ramesh2022hierarchical, betker2023improving, rombach2022high, podell2023sdxl,
saharia2022photorealistic, radford2021learning, li2022blip, li2023blip, ilharco2021openclip,
hessel2021clipscore, hu2023tifa, cho2024davidsonian, ghosh2023geneval, lin2024evaluating,
li2024evaluating, koo2026evaluating, anderson2016spice, vedantam2015cider, heusel2017gans,
lee2023holistic, zhang2025rethinking, chang2023prompt, oppenlaender2024artworks, carrasco2024level,
horton2023bias, millet2023defending, bhattacharyya2025evaluating, gao2025eemo, yang2024emogen,
lin2024make, dang2025emoticrafter, mehta2024generating, zhou2025analyzing, alvarado2025texttoimage,
lomas2024improved, yang2018weakly, ragot2020ai.

Cautions: "alignment" is allowed here ONLY for other people's work; this project's word is
"agreement". Do not add any paper or finding not in the old chapter. Numbers about other people's
studies may be typed (they are in the old chapter). Keep section lengths uneven. A literature review
by a student often has a slightly list-like rhythm when going through resources; that is fine, but
vary sentence length inside it.

## chapter3.tex  Methodology  (target 4,100 to 4,600 words)

Sections and labels: `\chapter{Methodology}\label{ch:method}`; `\section{Overview and design
principles}\label{sec:method-overview}`; `\section{The corpus}\label{sec:method-corpus}`;
`\section{Data pre-processing}\label{sec:method-preprocessing}` with subsections Loading and
pre-test removal / Prompt groups / Name redaction; `\section{The pipeline}\label{sec:method-pipeline}`
with subsections Prompt reader / Describer / Description template and image reader / Face and scene
classes; `\section{The similarity ladder}\label{sec:method-measures}` (the four equations with labels
eq:va, eq:overlap, eq:family, eq:sign; copy the mathematics from the old chapter exactly, the prose
around it fresh); `\section{The random-pairing null}\label{sec:method-null}` (eq:z);
`\section{Inference}\label{sec:method-inference}` (clustered bootstrap, clustered permutation test
eq:permp, Cohen's kappa eq:kappa, Holm, McNemar and cluster sign-flip, Wilson);
`\section{Analyses}\label{sec:method-analyses}` (splits and main table; face/scene difference;
specificity check; method comparison; consistency with its definition and null; control audit;
describer audit and copy rate; error taxonomy and its fixed six modes and tie-break; template
ablation variants; single-coder check); `\section{The demonstrator}\label{sec:method-demo}`;
`\section{Reproducibility and testing}\label{sec:method-repro}`.

Figures and placements: fig:pipeline (`\resizebox{\textwidth}{!}{\input{figures/pipeline}}`) in the
overview; fig:promptlength and fig:dataset in the corpus section; fig:timeline in the loading /
pre-test subsection; the optional placeholder fig:installation at the end of the corpus section
(caption: a photograph of the installation at the festival; instructions: optional, delete the
line if no photograph is available, credit the source in the caption); fig:codingsheet in the
single-coder paragraph; placeholder fig:demo in the demonstrator section (caption: the demonstrator
after running record 63, "super tired": the drawing, the five answers, the two readings and the
verdict against the chance band; instructions: run `bash emoviz/run_interface.sh`, choose record 63,
press Compare, screenshot the result panel, save as figures/demo_screenshot.png).

Must contain everything in the old chapter 3 and FACT_SHEET sections 3 and 4, including: the three
design principles and where each came from (supervision, or the data, with the story of noticing the
0.71-looks-like-a-pass problem while building the demonstrator); the corpus facts; the loader and
the naive-loader failure; the timestamps and the pre-test rule; prompt groups computed before
redaction and why; the redaction procedure with its three stages and the 0.012 check; the rejected
alternatives on both sides with the concrete reasons (NLI surprise artefact; lexicon brittle;
Qwen 3B and the 16 GB laptop, 4 h 45 min; Florence-2 and Transformers 5.14; the terse caption;
GoEmotions on descriptions collapsing to neutral); the template and the plain statement that it
asserts a person and an expression for every drawing, written in the first week, consequence
measured in September; the face rule and its partial circularity; the measures with equations; the
null and its two cautions (z as ordering statistic with the seed range; degenerate nulls, detected
from the spread, replacing a hand flag that missed a subset); the inference procedures with their
citations; the analyses in the order the results chapter reports them; the demonstrator's three
design choices and that nothing is stored; the pinned environment, the single metrics module and
the two-layer tests, and the plain statement of what the tests do not do.

Keys owned (must be cited here): demszky2020goemotions, li2022blip, lewis2020bart,
williams2018broad, yin2019benchmarking, russell1980circumplex, mohammad2018obtaining,
good2005permutation, cameron2008bootstrap, efron1993introduction, north2002note,
cohen1960coefficient, landis1977measurement, holm1979simple, mcnemar1947note, wilson1927probable,
radford2021learning, ilharco2021openclip, bird2009natural, betker2023improving.

Cautions: this is the chapter where the first-person process voice matters most. Say what was tried
first, what failed, how long it took, and what was done instead. Passive voice for procedure is fine.
Do not describe the analyses as if they were planned from the start when the old chapter says they
came from the September audit (the intervals, kappa, Holm, the scripted consistency null, the
like-for-like comparison, the audits and the ablation were added after the presentation; say so).

## chapter4.tex  Results  (target 2,500 to 2,900 words; the supervisor asked for a short results chapter)

Sections and labels: `\chapter{Results}\label{ch:results}`; `\section{Overall
agreement}\label{sec:results-overall}`; `\section{Face-classified versus scene-classified
drawings}\label{sec:results-face-scene}`; `\section{Robustness to repeated prompts and multiple
comparisons}\label{sec:results-robustness}`; `\section{Specificity check: prompts the text reader
labels neutral}\label{sec:results-control}`; `\section{Two image readers, like for
like}\label{sec:results-method}`; `\section{Consistency across repeated
prompts}\label{sec:results-consistency}`; `\section{Per-family agreement}\label{sec:results-families}`;
`\section{The describer}\label{sec:results-describer}`; `\section{Error
taxonomy}\label{sec:results-taxonomy}`; `\section{Description-template
ablation}\label{sec:results-ablation}`; `\section{Single-coder reliability check}\label{sec:results-human}`;
`\section{Summary of findings}\label{sec:results-summary}`.

Figures and tables in order: opening paragraph states the conventions (every value a macro, every
rate against its null with \nullShuffles{} re-pairings and seed \nullSeed{}, every interval a
clustered bootstrap with \DiffDraws{} draws). Overall: tab_headline, fig:zgroup. Face/scene:
fig:facescene, tab_difference. Robustness: tab_distinct, tab_holm. Control: tab_control. Method:
fig:method, tab_method, tab_methodvone (kept as a record, not quoted as a result). Consistency:
fig:consistency, fig:happygrid, tab_consistency. Families: fig:confusion, tab_confusion, tab_kappa,
tab_families. Describer: tab_describer, fig:noperson. Taxonomy: fig:taxonomy, tab_taxonomy. Ablation:
fig:ablation, tab_ablation. Human check: `\input{generated/tab_humancheck}` and a paragraph that
says the sample is drawn, the sheets exist, the coding was not complete at the time of writing, and
what the scored table will report; add a LaTeX comment `% TODO once labels.csv is coded ...` so the
student can swap the paragraph. Summary: a numbered list of five findings tied to the objectives,
then one short paragraph on what the audits do to them.

Must contain every number the old chapter 4 reports, as macros, and the two "details that need
saying" about the method comparison (CLIP's higher z with a lower rate; the two readers agree with
each other on only \McReaderAgree{}). Interpretation stays out of this chapter (it goes in
Chapter 5); each paragraph says what a table or figure shows and stops.

Keys owned: none required (results chapter). Cite nothing unless the old chapter did.

Cautions: results prose is naturally denser with numbers; still vary sentence length (a short
sentence stating what a table shows, then a long one with the values). Say "the describer reports"
and "the image reader returns", never "the drawing conveys". The people-aware ablation result must
be stated exactly: face rows identical by construction, scene rows fall to their nulls.

## chapter5.tex  Discussion  (target 2,200 to 2,500 words)

Sections and labels: `\chapter{Discussion}\label{ch:discussion}`; `\section{What the results
establish}\label{sec:disc-establish}`; `\section{The describer is the weak link}\label{sec:disc-describer}`;
`\section{Circularity of the face/scene split}\label{sec:disc-circularity}`; `\section{What is not
claimed}\label{sec:disc-not-claimed}`; `\section{Relation to prior work}\label{sec:disc-prior}`;
`\section{Limitations}\label{sec:disc-limitations}` (a numbered list of the ten limitations from the old
chapter, each one or two sentences); `\section{Threats to validity}\label{sec:disc-threats}`
(construct, internal, external, statistical).

Must contain: the three things established (agreement above chance on every rung, surviving
clustering, the distinct re-run and Holm; agreement concentrated in describer-reported faces, with
the ablation removing the scene result; the instrument behaves on its checks: control at chance,
describe-then-extract closer to the prompt reader than direct CLIP, framed as disagreement between
readers, not correctness) and the fourth thing not claimed (perception). The describer as weak link
with the numbers (\DescScenePeopleZero{}, \DescScenePeopleZeroExpr{}, \DescSceneSmile{},
\DescBareStrictPct{}, \DescCopyStrict{}; ablation drop to \AblDropExpressionEmoFamObs{} and
\AblFixedExpressionEmoFamObs{}; "the entailment model works as an expensive lookup table" may be
said in plain words once); the consequence for the method comparison (advantage may be BLIP-VQA
reading drawn faces better than CLIP, not the architecture; the expression-word ablation that would
separate them is further work); the taxonomy (describer \TaxDescriber{}, reader \TaxReader{}, prompt
\TaxPrompt{}, generator \TaxGenerator{}) and its fit with the positive bias and expressed/evoked
confusion reported for vision-language models \cite{bhattacharyya2025evaluating, gao2025eemo}. The
circularity section with the corrected mechanism (split driven by the people count; the same
description read by the reader; statistically real; what it does and does not establish; the
single-coder check as the only estimate that breaks it). The non-claims (FACT_SHEET section 9) each
with its reason, including the story of the two builds pointing opposite ways. Relation to prior
work: Lomas (person vs robot direction; consistent, neither validates the other); Cowen and Keltner
(near misses carry information; the loose measures far above null where family agreement is only
\FullEmoFamObs{}); the prompt reader's weakness on this register \cite{demszky2020goemotions,
yang2023context} and kappa \KappaEmo{} in the \KappaEmoBand{} band being the kind of figure human
annotators reach on fine-grained text emotion; Carrasco \cite{carrasco2024level} agreement rising when
collapsed to positive/negative mirrored by the sign vs family gap; reading every value against a
null following Zhang and Wan \cite{zhang2025rethinking} and Lee and colleagues \cite{lee2023holistic};
direct CLIP as the right baseline for the reason CLIPScore \cite{hessel2021clipscore} is the default,
failing for the reason VQAScore's authors \cite{lin2024evaluating} prefer a question-answering judge;
the describer as a VQAScore-style judge pointed at expression; WikiArt Emotions'
\cite{mohammad2018wikiart} faces-give-consistent-judgements reproduced as the face/scene contrast with
the caveat that the consistency is a machine's; Alvarado \cite{alvarado2025texttoimage} for the
colour non-claim. Limitations and threats as in the old chapter.

Keys owned: lomas2024improved, cowen2017self, demszky2020goemotions, yang2023context,
carrasco2024level, zhang2025rethinking, lee2023holistic, hessel2021clipscore, lin2024evaluating,
bhattacharyya2025evaluating, gao2025eemo, mohammad2018wikiart, alvarado2025texttoimage.

Cautions: this is the chapter most likely to drift into essay rhetoric. No "Three things, and not a
fourth." No "I would defend in any room." No "faces, and only faces" as a closer (once, mid-paragraph,
as the short form of the finding, is allowed). Keep the argument, drop the performance. A student
would write "I think the honest reading of this is..." at most once in the whole chapter.

## chapter6.tex  Conclusions and Further Work  (target 800 to 1,000 words)

Sections and labels: `\chapter{Conclusions and Further Work}\label{ch:conclusion}`;
`\section{Conclusions}\label{sec:conc}`; `\section{Further work}\label{sec:further}`.

Must contain: the answer to the question, bounded as the discussion bounds it; each of the eight
objectives ticked off with its macro result; what the dissertation contributes (corpus and question,
a way of asking it that gives every value its chance level, the consistency experiment, an audited
account of an instrument that ended up more modest than its architecture promised; the plain
statement that the two-stage reader is, for most records, a facial-expression question with a lookup
table, and that a study of what a drawing shows needs either a person or a describer that can read a
scene). Further work in priority order, each tied to a result: the human-rated study (blind to
provenance given \cite{ragot2020ai, horton2023bias, millet2023defending}; adapt Lomas's protocol
\cite{lomas2024improved}; the single-coder check as its pilot); the people-aware template as the
default, re-running the main table and keeping the demonstrator in parity; the expression-word
ablation on face-classified records; a scene-capable (sketch- or drawing-specific) describer,
designed but not run; a second describer and test-retest for both readers; NRC per-family means
\cite{mohammad2018obtaining} or a richer scheme such as the 27 categories \cite{cowen2017self} so
low-arousal positive states stop falling to neutral; a second coder with an agreement statistic.

Keys owned: ragot2020ai, horton2023bias, millet2023defending, lomas2024improved,
mohammad2018obtaining, cowen2017self.

Cautions: conclusions are allowed one "In summary" or "To conclude". Do not end on an aphorism. End on
the most concrete next step.
