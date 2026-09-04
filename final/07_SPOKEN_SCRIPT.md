# Spoken script — 10 minutes

Written to be **said**, not read. Roughly 1,400 words: about nine minutes of speech at a normal pace,
leaving a minute of slack. Timings are cumulative.

**On the title.** The registered title is *Visualising Emotion: A Similarity-Based Analysis of
Emotional Fidelity in Text-to-Image Generation*. Say it as written — it is the formal title. Note that
it describes the **topic** ("emotional fidelity") and the **approach** ("a similarity-based analysis"),
which is exactly right. Inside the talk, keep saying *agreement*: the title names what is being
studied; the body says what was measured. If an examiner presses on the word, the answer is on the
last page of this script.

**One correction carried into this script:** the face–scene difference **has** now been tested. Do not
say that no test has been run.

---

## Slide 1 — Title  ·  0:00–0:30

Good morning. I'm Shre Hari Prem Anandh. This is my MSc Artificial Intelligence dissertation,
supervised by Dr Chaona Chen: *Visualising Emotion — A Similarity-Based Analysis of Emotional
Fidelity in Text-to-Image Generation*.

The project measures whether an AI-generated drawing agrees emotionally with the words that produced
it. The drawing on the right is real — it came from the prompt "tired but happy", one of 1,025
collected at the Festival of the Mind.

---

## Slide 2 — The problem  ·  0:30–1:20

If someone prompts an image generator with "a red car", checking the output is easy. Look for a car.
Check it's red. That is essentially what text-to-image evaluation does today.

Now take "tired but happy". There is no object to look for. There is no answer key. And the feeling
is mixed. None of the existing metrics transfer.

So my research question is deliberately precise: **to what extent does an automatic image-emotion
reader agree with prompt-derived emotion labels for AI-generated monochrome drawings, and how does
that agreement vary by visual content and by repeated prompts?**

Four sub-questions follow, and each one becomes a result later.

---

## Slide 3 — The gap  ·  1:20–2:10

Four areas are each well established on their own.

Reading emotion from text — GoEmotions gives a taxonomy and a classifier, though short first-person
self-report is the hardest register for it.

Generating emotional images — systems exist that condition on a target emotion, and the literature
reports colour as the principal carrier of affect.

Evaluating text-to-image output — but for objects, not feelings.

And reading emotion back out of an image, which is known to be weak and positively biased.

The gap sits between them. No work in the corpus I reviewed measures whether the emotion in a
person's own unedited self-report is recoverable from the drawing generated from it — in monochrome
line art, where the colour channel the literature relies on is simply absent.

I should be explicit: I cite the colour work as motivation for why line art is a hard case. I have no
colour condition, so I make no claim about colour.

---

## Slide 4 — Contribution  ·  2:10–3:00

This is the contribution, and my supervisor named it.

Emotion is subjective. There is no ground truth. Humans disagree with each other and the models are
noisy. So asking whether the image emotion *matches* the text — right or wrong — is too simplistic.

Instead I measure how **similar** the two readings are, on a four-level ladder over emotion families,
so that "happy" and "excited" count as close rather than as a miss.

You can see it on the left: under a conventional one-to-one rule, that pair scores as a failure.
On my ladder it scores near the top.

That is the novel element. The field reports one-to-one accuracy; this study reports graded,
chance-referenced similarity.

---

## Slide 5 — Method  ·  3:00–4:00

My supervisor's instruction was: don't force CLIP to output an emotion. CLIP is trained on real
colour photographs and is good at objects, not affect.

So the image is **described** first. BLIP-VQA answers five fixed factual questions — expression,
action, posture, how many people, what's in the picture — and those answers are assembled into one
neutral sentence. A separate model, BART-MNLI, reads a feeling out of that sentence.

The prompt goes through GoEmotions into the same seven emotion families.

Now both sides are text, and I compare text to text on four measures — every one of them against a
300-shuffle random-pairing null.

One honest caveat, which is on the slide: asking "what is the facial expression" often returns a
feeling word. So the separation between describing and reading is weaker than it first appears, and
I report that.

---

## Slide 6 — Data  ·  4:00–4:45

1,025 drawings. Three things had to be solved before any analysis was possible.

Three incompatible filename schemes in one folder — a naive loader resolves under a fifth of the
corpus. Hidden C2PA signing timestamps inside each PNG, which let me identify thirteen images
generated *before* the festival: developer tests, excluded. And a pre-processing step — eight records
contained real names, replaced with a placeholder, and I verified that redaction changed no emotion
label at all.

That leaves 1,012 analysed: 607 prompts carrying a feeling, 405 not; 591 with a readable face, 421
scenes.

---

## Slide 7 — Evaluation design  ·  4:45–6:00

This is the slide I would most like you to take away.

Two checks decide whether any of my numbers mean anything.

First, a random-pairing null. Within each subset I shuffle the drawings against the prompts, three
hundred times with a fixed seed, and see what chance alone produces. Every figure I report is quoted
against its own null.

Second, a specificity check. Four hundred and five prompts carry no feeling — "pigs", "mickey mouse".
On those, valence–arousal similarity returns 76.6% against a null of 76.6%. The pipeline reports
agreement only where the prompt reader finds an emotion. I should add that on that subset the sign
and family measures are degenerate by the subset's own definition, so only the valence–arousal figure
is informative there.

And third — the scale does not start at zero. This measure has a mathematical floor of 41, and
randomly paired items already score 76. So a score of 71 reads as a pass and is actually below
chance. That is why I lead with valence-sign and family agreement rather than this number.

---

## Slide 8 — Results  ·  6:00–7:15

Agreement is well above chance overall: 64% valence-sign against a null of 46, z over eleven.

It is strongest for face-classified drawings — 73.9% against a null of 53.5 — and weaker, though
still above chance, for scenes at 42.9%.

I have tested that difference. A clustered permutation test gives **p equals 0.0001**, and the 95%
confidence interval on the difference is **plus 22.6 to plus 40.6 percentage points**. I clustered on
prompt identity, because 249 of the records repeat an earlier prompt and are therefore not
independent.

Three further results. Repeated prompts: given the same words, the image reader recovers the same
emotion 68.8% of the time against a null of 59.1%. The method comparison favours describe-then-extract,
49.3% against 25.3% for reading emotion from the image directly — though I should note the prompt
side is held constant with BART-MNLI in that comparison, not the GoEmotions reader used elsewhere.
And on distinct prompts only, the face result holds while the scene result weakens substantially,
to 37.3%.

---

## Slide 9 — Demonstration  ·  7:15–8:45  (LIVE)

*Switch to the browser. Pick "super tired".*

Here are the five factual answers the image model gave — expression sad, posture bent, one person.
I never asked it what emotion the picture shows.

*Click Compare.*

A second model read sadness out of that description, at 93%. A third model read the person's own
words and also said sadness. And here is the score — 89, against the chance line at 76, on an axis
that starts at 41.

*Now pick "disney characters".*

This one has no feeling in the words. The pipeline doesn't invent one — it lands below chance. That
is the specificity check, running live.

One example illustrates the method; it isn't evidence. The evidence is the 1,012 records on the
previous slide.

*Return to the slides.*

---

## Slide 10 — Conclusion  ·  8:45–9:45

To close.

Established: prompt-reader and image-reader agreement is well above chance on every metric;
significantly higher for drawings containing a person; the same prompt does not reliably yield the
same recovered emotion; and describe-then-extract agrees more than reading emotion directly.

Not established, and I want to say these before you ask. What a *human* perceives — both my readers
are automatic and they disagree with each other. Anything about colour. And any positive-versus-
negative direction, which I withdrew when the evidence didn't support it.

One limitation I'll name directly: the face/scene split is derived from the same describer output
that the emotion reader then reads, so it is partly circular. The difference is statistically real,
but that does not make it independent evidence.

My contribution is not a new emotion classifier. It is a reproducible methodology for evaluating
emotional agreement between prompts and AI-generated monochrome drawings, using graded similarity
against a random-pairing baseline, in a setting where no human ground truth exists.

Thank you — I'm happy to take questions.


---

# If an examiner asks about the word "fidelity" in your title

They may. Have this ready — it takes fifteen seconds and it turns the question into a strength.

> "The title names the phenomenon I set out to study — emotional fidelity — and it names the approach,
> a similarity-based analysis. What I actually measure is agreement between two automatic readers,
> which is a narrower thing, and I'm careful to say so throughout. I chose a similarity-based analysis
> precisely because fidelity implies a correct answer, and this dataset has no human ground truth to
> be faithful to. So the title states the target; the thesis states what could actually be established
> about it."

That answer shows you understand the distinction rather than having missed it.

# Last thing before you walk in

Say the number, concede the limitation before you are pushed, then bound the claim. That sequence
works for every question you will be asked.
