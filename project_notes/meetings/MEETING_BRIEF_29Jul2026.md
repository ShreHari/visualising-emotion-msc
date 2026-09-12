# Supervision Meeting — Script & Brief (29 July 2026)
**With:** Chaona Chen · **Project:** Visualising Emotion: Text and Image Analysis of Human Feelings
**Show her:** the dashboard → https://claude.ai/code/artifact/b06477ce-4905-49b4-b549-06153dab9171

---

## 0. The 30-second opener (say this first)
"Since we last met I've done three things: I've gone deep into the dataset and found some things
that aren't obvious, I've been reading into the relevant literature and worked out where the
research gap is, and I've got a working analysis pipeline giving preliminary answers to all three
research questions. I've put it together in a dashboard so I can show you visually — can I share
my screen?"

---

## 1. What I've done — progress (say it as a list)
- **Understood the dataset fully** — all 1,025 text–image pairs, including hidden structure nobody set up for me.
- **Been reading into the relevant literature** — text-to-image and emotion — and I've worked out the research gap the project fills.
- **Built the analysis framework ("emoviz")** — it reads emotion from the text, reads emotion from the image, and compares them.
- **Validated the method** — I checked how far the AI image-reader can actually be trusted before reporting anything.
- **Produced preliminary results for all three research questions.**

---

## 2. What I've studied about the dataset (this proves you know the data)
Say these — they show real familiarity:
- "It's **1,025 prompts** people typed at **Festival of the Mind 2024**, each turned into a
  **black-and-white line drawing by DALL·E**. The text and image are linked only by position."
- "The prompts are **short — median 4 words** — and often **mixed feelings** like 'tired but happy'.
  About **60% express an emotion**; the rest are objects, jokes, or questions."
- "I recovered **hidden timestamps** from inside the image files, which let me spot that
  **records 1–13 are pre-event test runs**, so I drop them — leaving 1,012."
- "There are **65 cases where the same prompt was drawn 2–11 times** — that's a built-in
  experiment on how consistent the model is."
- "Two things I want to flag: some records contain **real names and sensitive personal disclosures**
  (illness, grief), which matters for ethics; and the images are **monochrome**, which means a
  style instruction was added that isn't in the data I was given."

---

## 3. The findings — in plain language (the exciting part)
**RQ1 — Does the drawing feel like the text?** "Overall, only weakly — but the interesting part is
it's *asymmetric*."

**The headline:** "**Negative feelings survive the drawing; positive feelings collapse to neutral.**
When someone writes something happy, the image only reads as positive **18%** of the time — most go
flat. When someone writes something negative, the image stays negative **64%** of the time. My
reading is that this is because **colour normally carries positive feeling, and colour has been
stripped out** — which lines up with the literature (Alvarado 2025; Lomas et al. 2024)."

**RQ2 — Which emotions survive?** "Anger 77%, sadness 64%, fear 62% — but happiness only 18%. The
one positive emotion is the worst-preserved."

**RQ3 — Same prompt, same feeling?** "No — the model is unstable. Given the word 'Happy' eleven
times it drew **7 happy, 3 neutral, 1 surprise**. Across all 65 repeat-runs, only 21 were fully
consistent."

**Honesty line (say this — supervisors respect it):** "These are **preliminary** — they come from
automatic AI readers, not yet human raters. And I **measured my image-reader first**: it's reliable
for happy/sad (75%) but not for the rarer emotions, so I honestly report on the **positive/negative
axis** where it works, and flag the rest as a lower bound."

---

## 4. Timeline (say: "here's my plan to submission")
- **Now (29 Jul):** pipeline, results, and literature gap — done. ✓
- **Late July:** submit ethics; agree the emotion scheme and scope with you.
- **Early August:** run a small **human-rater validation study** — the key step that turns my
  numbers into defended ones.
- **Mid August:** final analysis + all figures.
- **Late August:** write the dissertation (Intro + Lit Review already scaffolded) → **first full
  draft to you ~1 Sep**.
- **4 Sep:** presentation.
- **4–15 Sep:** revise on your feedback + polish.
- **16 Sep, 15:00:** submit.

---

## 5. Questions to ask her (this is what the meeting is *for*)
1. **Emotion scheme:** happy with me reporting on the **valence axis** (positive/negative), since the
   image-reader is only reliable there? Or push for full categories despite the noise?
2. **Human validation study:** is a small rating study in scope? If yes, it needs to go into the
   **ethics application now**, not in August.
3. **Non-emotional prompts:** ~40% aren't feelings. Filter them out, or treat "how the public used
   the tool" as a finding in itself?
4. **The repeat-runs:** do you know if the 65 duplicate prompts were **automatic batch calls** or
   **one person hitting regenerate**? It changes whether they count as independent samples.
5. **Ethics route:** given the real names / sensitive disclosures — self-declaration, and should I
   commit to redacting names and excluding those records from any figures?

---

## 6. One-line summary of the whole project (if she asks "so what's the point?")
"AI can now draw what we say we feel — I'm measuring whether the drawing *actually* feels that way,
using real public self-reports rendered as colour-free line art, to find where machine-visualised
emotion works and where it breaks."
