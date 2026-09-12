# Meeting with Dr Chen — Thursday 20 August 2026

**Live demo:** http://127.0.0.1:5050 (running — models warm up ~30s after start)
**Clock:** presentation in **15 days** (4 Sep) · submission in **27 days** (16 Sep)

---

## 1. Open (30 seconds — say it once, don't dwell)

> "Quick context on the last few days — I had an exam on Monday, so most of last week went
> into revising for that. Since then I've been back on the project full time, and what I've
> been building is the analysis dashboard and the technical documentation. I'd like to show
> you the dashboard, then talk about ethics, because there's a timing decision I need your
> steer on."

Then move on. Don't apologise twice.

---

## 2. The dashboard (show it — 4–5 minutes)

Open the browser and drive it while you talk.

> "This runs the actual pipeline live — it's not a mock-up. It's the architecture you asked
> for: describe first, then extract the emotion, then compare by similarity."

**Click an example, then Compare, and narrate as it goes:**

> "So it picks a drawing from the festival dataset. The image model answers five plain
> questions — expression, action, posture, how many people, what's in the picture. It is
> never asked 'what emotion is this'. Then a separate language model reads a feeling out of
> those answers. And the words are read by a third model. Then I compare the two."

**Point at the paired reading:**

> "This is the part I'd most like your opinion on. Each row is one feeling. The filled dot is
> the words, the ring is the drawing, and the bar between them is the distance. So you see
> the similarity directly, rather than reading two separate charts."

**Point at the verdict:**

> "And this is the thing I fixed this week, which I think is the most important change.
> The similarity score can't start at zero. If you take a drawing and a sentence completely
> at random from the dataset, they already score about 76% — because most feelings sit close
> together on the map. So a score of 71 looks like a pass but is actually *below* chance.
> Every number here is now shown against that chance line, and it tells you what percentage
> of random pairings this pair beats."

**If she looks interested, this is your strongest line:**

> "It also changed what I lead with. Valence–arousal similarity can't tell a face apart from
> a scene — it's about 84% for both. The signal is in valence-sign and emotion-family
> agreement, so those are now the headline and the raw number is secondary."

---

## 3. What the results say (2 minutes — only if she asks, or if there's time)

- **Faces carry emotion, scenes don't.** Drawings with a readable face agree with the prompt's
  mood direction **74%** of the time; scene-only drawings **43%**. Both beat chance; the gap
  is large and survives every robustness check.
- **The method passes its own validity test.** For prompts with no feeling in them
  ("pigs", "mickey mouse") the alignment drops to exactly chance. It only finds emotion
  where emotion exists.
- **The generator is unstable.** 87 prompts were drawn more than once. Given identical words,
  the AI conveys the same emotion only about **69%** of the time.
- **Your architecture is measurably better.** Describe-then-extract gets **49%** emotion-family
  agreement; asking CLIP for the emotion directly gets **25%**.

**Be honest about the limit — she will respect this more than a clean claim:**

> "The one thing I can't settle is whether a *person* sees the same feeling. My two automatic
> readers disagree in opposite directions — CLIP skews negative on line art, and the
> description model reads 57% of the faces it can read as happy. Only human ratings can
> adjudicate that. Which brings me to ethics."

---

## 4. Ethics — the decision you need from her (the real agenda item)

**State the position plainly:**

> "The ethics application is drafted — the form answers, the participant information sheet,
> the consent form, the recruitment text and the rating survey are all written. It is not
> submitted yet. Before I can submit I need to finish three short online courses, which is
> about forty minutes, and I need one answer from you."

**The question you must ask her:**

> "Was the Festival of the Mind dataset collected with consent that covers this kind of
> secondary use? I need to state that on the form, and I don't want to guess."

**Then put the timing decision to her — do not decide this alone:**

> "The timing is the problem. Approval takes about two weeks. If I submit in the next day or
> two, that's approval around the 3rd of September. Submission is the 16th. So running the
> human study, analysing it and writing it up would all have to happen in under two weeks,
> on top of the write-up.
>
> So I'd like your view: do I push to get a small human study done in that window, or do we
> treat it as the clear next step and I write the dissertation on the computational results
> as they stand?"

**Have your own recommendation ready if she asks what you think:**

> "My instinct is to submit the ethics application anyway — it costs me a day and it means
> the option stays open — but to write the dissertation assuming no human data, so the
> writing isn't blocked on it."

---

## 5. Technical documentation — mention, don't present

> "There's a technical report covering the whole build — the architecture, the approaches
> I tried and rejected and why, all the findings with their statistics, and an automated
> test suite that currently passes 20 out of 20. I can send it over if it's useful."

If she asks about privacy in the demo:

> "Nothing a visitor types or uploads is stored, and there's no request log. Records with
> real names or personal disclosures are withheld — and I withhold a set of decoys as well,
> so nobody can work out which records were flagged just by seeing which ones are missing."

---

## 6. Questions to ask her (pick 2–3, don't fire all of them)

1. **Consent for secondary use — yes or no?** (blocks the ethics submission)
2. **Human study: go, or write it up as future work?** (the big call)
3. **Is the dashboard something you want in the presentation on the 4th?**
4. **For the write-up — how much of the method-development story does she want?**
   (the rejected approaches: Qwen too big for the laptop, GoEmotions collapsing on
   descriptions, the CLIP baseline)
5. **Has the project title been confirmed?**

---

## 7. Close

> "So my plan for the next week: finish the ethics courses and submit, and start writing the
> literature review and introduction. Does that match what you'd expect at this point?"

---

## Cheat sheet — numbers, if you get asked

| | |
|---|---|
| Dataset | 1,025 drawings · 1,012 analysed (13 are pre-festival tests) |
| Emotional vs not | 607 carry a feeling · 405 don't (those are the control) |
| Face vs scene | 74% vs 43% mood-direction agreement |
| Chance line | random pairings already score ~76% |
| Repeat consistency | same emotion only ~69% of the time |
| vs CLIP baseline | 49% vs 25% family agreement |
| Demo pool | all 1,012 records served (names redacted, nothing withheld) |
| Tests | 28/28 passing |

---

# APPENDIX — the tech side, in detail

## The 90-second version (say this first)

> "The pipeline is finished and it's the architecture you specified. The vision model is never
> asked what emotion a drawing shows — it answers five factual questions: expression, action,
> posture, how many people, what's in the picture. A separate language model reads a feeling
> out of that description. The words go through a third model. Then I compare the two by
> similarity, not by matching.
>
> Everything is measured against a random-pairing baseline, so a result only counts if it beats
> chance. It runs over all 1,025 drawings, and there's a test suite that checks the whole thing
> end to end — currently 20 out of 20."

## Her four directives (30 July) and what you did with each

| She asked for | What to say |
|---|---|
| Similarity, not matching | Four measures at increasing strictness: valence–arousal closeness, mood direction, emotion family, probability overlap. |
| Image → description → emotion | Built exactly that. The alternatives were tested first and failed — a finding in itself. |
| Group the data | Face vs scene, and emotional vs non-emotional. Both groups reported, nothing dropped. |
| Redact names | Done in the demo — sensitive records withheld, plus decoys so the withheld set can't be identified. |

## The new thing this week (lead with this)

> "The most important fix was realising the similarity score can't start at zero. Pair a drawing
> with a random sentence from the dataset and it already scores about 76% — because most emotions
> sit close together on the map. So a score of 71 looks like a pass but is below chance. Every
> number in the dashboard is now shown against that measured chance line.
>
> It also changed what I report. Valence–arousal similarity is about 84% for faces *and* scenes —
> it can't tell them apart. The real signal is in mood direction and emotion family, so those are
> now the headline."

## If she asks "how do you know it's working?"

1. **Validity check** — non-emotional prompts ("pigs", "mickey mouse") align at exactly chance.
   It only finds emotion where emotion exists.
2. **Null-referenced** — every metric compared against 300 shuffled pairings; z-scores, not raw %.
3. **Deduplication** — 249 prompts are duplicates; findings hold on distinct prompts only.

## If she asks what didn't work (volunteer this — it reads as rigour)

> "Three things failed first. GoEmotions collapsed to 'neutral' on image descriptions because it
> needs first-person feeling words. A single caption was too terse and the reader collapsed to
> 'surprise'. And Qwen 3B exhausted my laptop's memory — four and a half hours, zero progress.
> So the final design is constrained by what works on the hardware, and I documented all of it."

## The limits — say them before she finds them

> "The face/scene split has partial circularity I should flag: the split is defined by whether the
> model reported an expression, and the emotion is read from that same description. The gap is
> large and survives every check, but it's entangled with the definition, and I say so.
>
> And what I genuinely can't settle is whether a *person* sees the same feeling. My two automatic
> readers disagree in opposite directions. Only human ratings resolve that."

→ that last line is your transition into the ethics conversation.
