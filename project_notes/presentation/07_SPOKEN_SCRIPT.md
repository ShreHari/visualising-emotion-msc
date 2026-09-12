# Spoken script — 10 minutes

Checked against the actual deck on 4 September. **The slide numbers below match your deck.**
Roughly 1,450 words: about nine and a half minutes including the live demonstration.

## Your deck, as it actually runs

Checked against `Visualising_Emotion_viva_deck.pptx` — **11 slides, speaker notes on every one.**
Present from this file, not the PDF: the PDF is a shorter 10-slide export with no notes.

| # | Section | |
|---|---|---|
| 1 | Title | |
| 2 | The problem — **your research question is on this slide** | |
| 3 | Literature — the 2x2 coverage matrix | |
| 4 | Contribution — similarity, not matching | |
| 5 | Methodology — the pipeline diagram | |
| 6 | Data | |
| 7 | Evaluation design — the two checks and the scale | |
| 8 | Results — the dot-and-null chart | |
| 9 | Demonstration | **live, 90 seconds** |
| 10 | Conclusion | |
| 11 | Backup | **skip unless the demo stalls** |

## Two spoken corrections

**Slide 8** still carries the footnote *"No formal significance test of the face-scene difference has
been run."* That is now out of date — you ran one. Say the real figure aloud; the wording is in the
script below.

**Slide 3** says *"23 excluded, 74 retained across twelve themes."* The correct figures from your own
filtering log are **97 screened, 24 excluded, 73 retained across eight themes**. Nobody is likely to raise
it; if they do, give the right numbers and move on.

## Post-presentation note (9 September)

The results slide said scenes are *"weaker, though still above chance"*. The template ablation run after
the presentation shows that scene figure was an artefact: the description template asserted a person
and an expression for drawings with none. Under a people-aware template the scene reading falls to its
null (valence sign 4.7% vs 3.4%, z +1.6) while the face rows are unchanged. If the viva returns to slide
8, say: **faces, and only faces, for this reader** — not faces more than scenes.

## On the title

The registered title is *Visualising Emotion: A Similarity-Based Analysis of Emotional Fidelity in
Text-to-Image Generation*. Say it as written. It names the **topic** and the **approach**, which is
correct. Inside the talk keep saying *agreement* — the title names the target, the body says what was
established.

## Slide 1 — Title · 0:00–0:35

Good morning. I'm Shre Hari Prem Anandh. This is my MSc Artificial Intelligence dissertation,
supervised by Dr Chaona Chen: *Visualising Emotion — A Similarity-Based Analysis of Emotional
Fidelity in Text-to-Image Generation*.

The drawing on this slide is real. Someone at the Festival of the Mind typed "tired but happy", and
that is what the AI produced. One of 1,025.

---

## Slide 2 — The problem · 0:35–1:25

If you prompt an image generator with "a red car", checking the output is easy — look for a car,
check it's red. That is essentially what text-to-image evaluation does today.

Now take "tired but happy". There is no object to look for. There is no answer key. And the feeling
is mixed. None of the existing metrics transfer.

So my research question is deliberately precise, and it is on the slide: **to what extent does an
automatic image-emotion reader agree with prompt-derived emotion labels for AI-generated monochrome
drawings — and how does that agreement vary by visual content and by repeated prompts?**

Four sub-questions follow from it, and each one becomes a result later in the talk.

---

## Slide 3 — Literature · 1:25–2:15

Four areas are each well established on their own, and this matrix shows where they sit.

Generating images from text — well established. Evaluating that output — well established, but for
**objects**: CLIPScore and VQAScore ask whether the picture contains what the prompt named.

Generating images towards a chosen **emotion** — also well established, and the literature reports
colour as the principal carrier of affect.

And then the fourth cell, which is empty. Evaluating the emotion recovered from a generated line
drawing. That is where this project sits.

Reading emotion back out of an image is known to be weak — vision-language models are positively
biased and order-sensitive readers of affect.

One thing I want to be explicit about: I cite the colour work as motivation for why monochrome line
art is a hard case. I have no colour-control condition, so I make no claim about colour.

---

## Slide 4 — Contribution · 2:15–3:10

This is the contribution, and my supervisor named it.

Emotion is subjective. There is no ground truth. Humans disagree with each other and the models are
noisy. So asking whether the image emotion *matches* the text — right or wrong — is too simplistic.

Instead I measure how **similar** the two readings are, on a four-level ladder over emotion families,
so that "happy" and "excited" count as close rather than as a miss.

You can see it here. Under a conventional one-to-one rule, that pair scores as a failure. On my
ladder it sits near the top.

That is the novel element. The field reports one-to-one accuracy; this study reports graded,
chance-referenced similarity.

---

## Slide 5 — Methodology · 3:10–4:05

My supervisor's instruction was: don't force CLIP to output an emotion. CLIP is trained on real
colour photographs and is good at objects, not affect.

So the image is **described** first. BLIP-VQA answers five fixed factual questions — expression,
action, posture, how many people, what's in the picture — and those answers are assembled into one
neutral sentence. A separate model, BART-MNLI, reads a feeling out of that sentence.

The prompt goes through GoEmotions into the same seven emotion families.

Now both sides are text, and I compare text to text on four measures — every one against a
300-shuffle random-pairing null.

One honest caveat, which is on the slide: asking "what is the facial expression" often returns a
feeling word. So the separation between describing and reading is weaker than it first appears, and
I report that.

---

## Slide 6 — Data · 4:05–4:45

1,025 drawings. Three things had to be solved before any analysis was possible.

Three incompatible filename schemes in one folder — a naive loader resolves under a fifth of the
corpus. Hidden C2PA signing timestamps inside each PNG, which let me identify thirteen images
generated *before* the festival: developer tests, excluded. And a pre-processing step — eight records
contained real names, replaced with a placeholder, and I verified that redaction changed no top-1
prompt label at all.

That leaves 1,012 analysed: 607 prompts the text reader labels emotional, 405 neutral; 591 the
describer classifies as a readable face, 421 as scenes.

---

## Slide 7 — Evaluation design · 4:45–5:55

This is the slide I would most like you to take away.

Two checks decide whether any of my numbers mean anything.

First, a random-pairing null. Within each subset I shuffle the drawings against the prompts, three
hundred times with a fixed seed, and see what chance alone produces. Every figure I report is quoted
against its own null.

Second, a specificity check. Four hundred and five prompts are labelled neutral by the text reader —
"pigs", "mickey mouse". On those, valence–arousal similarity returns 76.6% against a null of 76.6%.
The pipeline sits at chance where the prompt reader finds no emotion. I should add that on that subset the sign
and family measures are degenerate by the subset's own definition, so only the valence–arousal figure
is informative there.

And third — the scale does not start at zero. This measure has a mathematical floor of 41, and
randomly paired items already score 76. So a score of 71 reads as a pass and is actually below
chance. That is why I lead with valence-sign and family agreement rather than that number.

---

## Slide 8 — Results · 5:55–7:05

Agreement is well above chance overall: 64% valence-sign against a null of 46, z over eleven.

It is strongest for face-classified drawings — 73.9% against a null of 53.5 — and weaker, though
still above chance, for scenes at 42.9%.

**I have tested that difference.** A clustered permutation test gives **p equals 0.0001**, and the 95%
confidence interval on the difference is **plus 22.6 to plus 40.6 percentage points**. I clustered on
prompt identity because 249 records repeat an earlier prompt and are therefore not independent.
*(The footnote on this slide predates that test — take the spoken figure.)*

Three further results. Repeated prompts: given the same words, the image reader recovers the same
emotion 68.8% of the time against a null of 59.4% — more consistent than chance, far from fixed. The
method comparison, like for like, favours describe-then-extract: 53.0% family agreement against 22.4%
for direct CLIP, a difference of thirty points with a clustered interval of plus 25.5 to plus 35.6.
And on distinct prompts, the face result holds while the scene result weakens substantially, to 37.3%.

---

## Slide 9 — Demonstration · 7:05–8:35 · LIVE

*Switch to the browser. Click "super tired".*

Here are the five factual answers the image model gave — expression sad, posture bent, one person.
I never asked it what emotion the picture shows.

*Click Compare.*

A second model read sadness out of that description, at 93%. A third model read the person's own
words and also said sadness. And the score is 89, against the chance line at 76, on an axis starting
at 41.

*Now click "disney characters".*

This one has no feeling in the words. The pipeline doesn't invent one — it lands below chance. That
is the specificity check, running live.

One example illustrates the method; it isn't evidence. The evidence is the 1,012 records on the
previous slide.

*Return to the slides.*

---

## Slide 10 — Conclusion · 8:35–9:35

To close.

Established: prompt-reader and image-reader agreement is well above chance on every metric;
significantly higher where the describer reports a person; the same prompt does not reliably yield
the same recovered emotion; and describe-then-extract agrees far more closely with the prompt reader
than reading emotion directly.

Not established, and I want to say these before you ask. What a *human* perceives — both my readers
are automatic and they disagree with each other. Anything about colour. And any positive-versus-
negative direction, which I withdrew when the evidence didn't support it.

One limitation I'll name directly: the face/scene split is derived from the same describer output the
emotion reader then reads, so it is partly circular. The difference is statistically real, but that
does not make it independent evidence.

My contribution is not a new emotion classifier. It is a reproducible methodology for evaluating
emotional agreement between prompts and AI-generated monochrome drawings, using graded similarity
against a random-pairing baseline, where no human ground truth exists.

Thank you — I'm happy to take questions.

---

## Slide 11 — Backup

Do not go to this slide unless the demonstration fails. If it does: *"I'll show you the numbers
instead"* — then walk through record 63 ("super tired") exactly as you would have walked through the
live run; record 201 ("tired but happy") is the second backup.

---

# If an examiner asks about "fidelity" in your title

> "The title names the phenomenon I set out to study — emotional fidelity — and the approach, a
> similarity-based analysis. What I actually measure is agreement between two automatic readers,
> which is narrower, and I say so throughout. I chose a similarity-based analysis precisely *because*
> fidelity implies a correct answer, and this dataset has no human ground truth to be faithful to.
> The title states the target; the thesis states what could be established about it."

# The habit that carries every answer

Say the number. Concede the limitation before you are pushed. Then bound the claim.
