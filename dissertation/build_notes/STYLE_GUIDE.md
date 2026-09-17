# Style guide for the dissertation rewrite

This is the contract for anyone (person or agent) writing or editing a chapter of
`dissertation/`. Read it in full before writing a word. The old draft in `report/chapters/`
is the SOURCE OF CONTENT (facts, argument, order of ideas). It is NOT a source of sentences.
The old draft was flagged as machine-written. The job is a fresh draft that carries the same
facts and the same argument in the voice described below, and that would read as the work of
the student who did the project.

## 1. Who is writing, and how they sound

The author is Shre Hari Prem Anandh, an MSc Artificial Intelligence student at the University
of Sheffield, writing up a four-month project supervised by Dr Chaona Chen, a psychologist who
studies facial expressions. English is not his first language but he writes it fluently and
plainly. He did the engineering himself on a 16 GB laptop, ran the analyses, audited his own
numbers twice, and presented the work on 4 September 2026.

The voice to aim for:

- Plain, direct, specific. A competent student explaining what they did and what they found,
  to an examiner who will check the numbers.
- First person singular is normal for decisions and process ("I chose", "I tried", "I could not
  get", "I then re-ran"). Passive voice is normal for procedure ("the answers are cached").
  Mix them the way a real methods chapter does. "We" is never used (single author).
- Concrete rather than clever. Say what happened, with the real detail (which model, how long
  it took, what broke, which meeting the idea came from), instead of characterising it.
- Slightly conversational connectives are fine and expected: "so", "then", "at first", "in
  practice", "as it turned out", "for that reason", "the problem with this was".
- It is fine to admit uncertainty in plain words: "I am not sure how much of this is", "this is
  the part I would most like to check with a second coder".
- Ordinary academic signposting is fine and human: "This chapter describes...", "Section 3.4
  defines...", "Two things follow from this.", "There are three reasons.", "First, ... Second, ...".
  (Numbered enumeration is human; the *forced* rhetorical triad is not, see section 3.)
- Hedge once, not three times: "may", "suggests", "appears to". Never "could potentially
  possibly".

What it must NOT sound like: an essayist, a columnist, a keynote speaker, or a chatbot. No
aphorisms, no punchlines, no rhetorical staging, no "let me be careful here".

## 2. Rhythm (the thing detectors key on most)

Machine prose settles into a narrow band of sentence lengths with the same subject-verb-object
opening every time. Human prose is uneven. Every paragraph you write must pass these checks:

- At least one sentence under 12 words AND at least one over 30 words, in most paragraphs.
- Sentence-length standard deviation inside a paragraph of at least 8 words (aim for 10 to 14).
- No three consecutive sentences opening the same way (same first word, or all
  noun-phrase-subject openings). Open some sentences with a subordinate clause ("Because the
  prompts are short, ..."), some with a prepositional phrase ("On the 607 emotional prompts, ..."),
  some with the object or the result, some with "I".
- Long sentences are allowed to be genuinely long (35 to 50 words) with two or three clauses,
  the way a student writes when explaining a procedure. Do not chop everything into 15-word units.
- Paragraph lengths must vary: some 3 sentences, some 8. Sections must vary in depth: one may
  be two paragraphs and the next six. Do not give every section the same shape.
- Do not end every paragraph with a neat summarising sentence. End on the last fact.
- Semicolons: at most one per 300 words. Colons introducing a reveal ("The answer: ..."): never.

## 3. Constructions that are banned (they are the tells that got the old draft flagged)

Search your draft for each of these before returning it. If you find one, rewrite the sentence.

Staging and contrast
- "not X but Y", "not just/only/merely X but (also) Y", "it is not X, it is Y", "X rather than Y"
  used as a rhetorical flourish, "less X than Y", "X, not Y" as a clipped tail, and the same
  contrast split across two sentences ("This does not mean X. It means Y."). Keep a contrast only
  when the negative half corrects a belief the examiner would actually hold, and even then
  prefer to state the positive claim on its own.
- One-line closers and aphorisms: "That is the finding.", "The ladder is the result.", "Faces,
  and only faces.", "X is the Y of Z". No sentence whose only job is to make the previous
  sentence sound important.
- Announcing enumerations for effect: "Three things, and I want to be careful not to claim a
  fourth." "Two cautions attach to z." Say the things.
- Performed candour: "I want to be careful about", "it has to be said plainly", "to be honest",
  "the honest answer is", "the right form of words is", "in any room", "I would defend".
  Just make the claim with its qualification.
- Arguing with no one: "This is not to say", "One might object", "It would be tempting to",
  "The obvious way ... Neither survives".
- "which is why", "which is what", "which is exactly", "That is the ... behind", "The reasoning
  behind X comes from", "turns out", "as it happens", "in effect" (more than once), "in the end".
- Rhetorical questions in the Results and Discussion chapters. (One genuine question in the
  Introduction that states the research question is fine.)

Rhythm by rule
- Forced triads: three parallel items or three parallel examples for the sound of it. Two items
  or four are fine when that is what the content has. A list of the four measures is four.
- Anaphora and parallel paragraph closers ("For this project the lesson is ..." at the end of
  every literature section). Vary or drop.
- Em dashes and en dashes in prose: none. (The only allowed en dash is inside a numeric range or
  a hyphenated compound like "valence--arousal" and "text-to-image", which are terms.)
- Stacked short fragments for drama.

Vocabulary (do not use, in any form)
delve, crucial, pivotal, robust (except "robustness check", a technical term used sparingly),
leverage, landscape (abstract), tapestry, underscore (verb), highlight (verb), showcase,
testament, vibrant, foster, navigate (figurative), realm, intricate, meticulous, nuanced,
multifaceted, holistic, seamless, groundbreaking, comprehensive (abstract), key (adjective),
notably, importantly, arguably, "it is worth noting", "it should be noted", "in essence",
"at its core", "fundamentally", "ultimately", "in today's world", "serves as", "stands as",
"represents a" (as a copula), "align with", "interplay", "enduring", "garner", "bolster",
"enhance", "emphasise" (as a rider), "reflecting/highlighting/underscoring ..." as a trailing
-ing phrase, "a range of", "a variety of", "in terms of", "in order to" (use "to"),
"due to the fact that", "moreover" and "furthermore" (use "also", "in addition", or nothing;
at most one "Additionally" per page), "In summary" (except once in the Conclusions),
"Overall," as a paragraph opener more than once per chapter.

Project-specific banned words (they mis-state what was measured)
- convey, carry, express, transmit, communicate, show (as in "the drawing shows joy"), portray,
  capture (an emotion). A drawing does not convey anything in this dissertation. The readers
  return readings.
- accuracy, accurate, correct, right, wrong, error rate, performance (for the central quantity).
  The central quantity is AGREEMENT between two readers, never accuracy, because there is no
  ground truth. ("Error taxonomy" and "failure mode" are the fixed names of the audit; keep them.)
- alignment (for this project's quantity). Use "alignment" only when describing other people's
  work in their words (VQAScore, Lomas et al., CLIPScore).
- fidelity: only inside the registered title, never in the body.
- matching / match: only in the sentence that says this project does NOT do matching.
- mood, mood direction: use "valence-sign agreement".
- perceive, perception, see, sees (for a machine reader). Machines read; people perceive. The
  only perception in the project is the single-coder check and the future human study.
- ethics, ethical, approval, consent: do not appear. Name removal is "data pre-processing".
- significant/significantly: only with a named test and its statistic beside it.
- prove, proves, proven, demonstrates (for results). Use "shows", "finds", "gives".
- "ground truth": only in "there is no ground truth".
- baseline: only for the direct-CLIP reader. The chance reference is "the random-pairing null"
  or "chance level".
- hallucinate/hallucination: prefer "invented" (a face or expression the describer reported
  that is not drawn) because the audit uses that word; "hallucination" may appear once in the
  literature review when quoting the field's term.

## 4. Terminology: one name per thing, used every time

record (one prompt + one drawing) · prompt (the visitor's words) · drawing (the image) ·
prompt reader (GoEmotions, RoBERTa) · describer (BLIP-VQA) · image reader (BART-MNLI over the
description) · describe-then-extract (the image pipeline) · direct CLIP (the baseline reader) ·
category (one of the 28 GoEmotions labels) · family (one of seven: joy, sadness, anger, fear,
surprise, disgust, neutral) · agreement (the central quantity) · the four measures / the ladder:
valence--arousal similarity, valence-sign agreement, family agreement, top-3 soft overlap ·
random-pairing null · z · degenerate null · prompt group (dedup key) · clustered bootstrap ·
clustered permutation test · face-classified / scene-classified (the describer's split) ·
emotional prompt / neutral-labelled prompt (the prompt reader's split) · specificity check ·
copy rate · consistency (repeated prompts) · repeat group · people-aware template · the
single-coder check · the demonstrator · Dr Chen or "my supervisor" (never "Chen" alone in prose).

Never pair a person-word with a record count. "1,025 records", never "1,025 visitors". The
number of contributors is unknown and at most 763.

## 5. Numbers, macros, citations, LaTeX

- Every statistic that comes from the analysis is a macro from `generated/numbers.tex`, written
  as `\MacroName{}` in the prose (the empty braces stop LaTeX eating the following space). The
  list is in `build_notes/MACROS.md`. Never type one of those numbers by hand, even when the
  macro renders the same digits. If a number you want is not a macro, and it is in the
  hand-typed allow-list in `FACT_SHEET.md` section 6, type it; otherwise leave it out.
- Tables are `\input{generated/tab_xxx}` and are never edited. Refer to them by
  `Table~\ref{tab:xxx}`. Figures use the labels in `FACT_SHEET.md` section 8.
- Citations: `\cite{key}` with keys from `build_notes/BIBKEYS.md` only. Multiple keys in one
  `\cite{a, b}`. Author names in prose the way a student writes them: "Lomas and colleagues
  \cite{lomas2024improved}", "Cowen and Keltner \cite{cowen2017self}", "Zhang and Wan
  \cite{zhang2025rethinking}". Every key in BIBKEYS.md must be cited somewhere in the finished
  dissertation, and the chapter briefs say which chapter owns which keys.
- Cross-references: `Chapter~\ref{ch:method}`, `Section~\ref{sec:method-null}`,
  `Figure~\ref{fig:facescene}`, `Table~\ref{tab:headline}`, `Equation~\ref{eq:va}`. The tilde
  is required. Use the label names from FACT_SHEET section 8 exactly; do not invent new labels
  unless the brief tells you to.
- British spelling (analyse, colour, behaviour, -ise). "Dr Chen". "DALL$\cdot$E" in LaTeX.
- Quotation marks in LaTeX: ``like this''. Visitor prompts are quoted in double quotes exactly
  as typed (lower case and all), except that records in the forbidden list are never quoted.
- Headings: sentence case ("Data pre-processing", not "Data Pre-Processing").
- Lists: use `\begin{enumerate}` / `itemize` only where the old draft had a list or where a
  procedure genuinely has steps. No bold lead-ins on list items.
- No `\textbf` in body prose. `\emph` only for a term being defined at first use or a quoted
  visitor word.

## 6. Plagiarism and originality

- Do not copy any sentence, or any run of more than about six consecutive words, from the old
  draft, from the project notes, or from any cited paper. Read the source, close it, write.
- Describe other people's findings in your own words with the citation. Direct quotation only
  when the exact words matter (e.g. the hypothesis template "This scene conveys {family}", which
  is a fixed string and is allowed).
- Never invent a fact, number, date, quotation, or reference. If the fact sheet does not have
  it, leave it out.
- Never quote or describe the content of records 216, 300, 302, 532, 750, 751, 858, 982, 1020,
  or any record whose text contains "[name]" or a real name. The safe examples are listed in
  FACT_SHEET section 7.

## 7. Two short examples of the target voice (tone only; do not paste them)

Target (methodology register):
"At first I used the NLI model on both sides, because it seemed cleaner to have one reader for
the prompts and one for the descriptions. On two-word prompts it did something odd. About a third
of them came back with surprise as the top family, and when I looked at the cases it was clearly
the hypothesis wording reacting to short inputs rather than anything in the words. GoEmotions
did not have this problem. It was trained on first-person Reddit comments, which are the closest
thing to a festival entry I could find, and swapping it in removed the surprise artefact without
changing any of the headline results. So the prompt side uses GoEmotions and the image side
uses NLI."

Target (discussion register):
"The face/scene result needs a caveat that I did not appreciate until September. The split comes
from the describer's own answers, and the image reader then reads those same answers. So when I
say face-classified drawings agree more, what I have really shown is that when BLIP-VQA reports a
person and an expression, the family the reader returns tends to track the prompt. That is a
smaller claim than 'faces carry emotion better than scenes'. It still survives every test I ran,
including the permutation test at p = \DiffSignP{}. But it is a claim about the instrument."

Note what these do: mixed sentence lengths (4 to 40 words), a first-person decision, a real
detail (Reddit; September), one hedge, no closer, no triad, no contrast-for-effect.
