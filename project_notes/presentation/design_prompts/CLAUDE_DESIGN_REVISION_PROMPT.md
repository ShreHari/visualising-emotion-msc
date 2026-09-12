Revise the existing 11-artboard deck. Do not rebuild it — the typography, the Broadsheet treatment, the dark emphasis slides and the running foot are all working. Keep them.

The audience is a technical professor marking an MSc Artificial Intelligence dissertation. The changes below all serve one goal: **make the argument land faster for someone who reads figures more fluently than prose.**

---

# 1. The global rule — apply to every slide

Move to an assertion–evidence structure. Garner & Alley (2013, *IJEE* 29(6)) randomised 110 engineering students across two slide designs with identical narration: a sentence-assertion heading supported by a graphic, averaging **21 words of body text per slide**, beat the bullet-based design averaging 41 words — on comprehension (d = 0.81), on recall a week later (d = 0.89), and on *lower* reported mental effort.

So, on every slide:

- **Cut body text by roughly a third.** Target ~20–25 words of body text per slide, excluding the heading, the footnote and any figure labels. Slides 6 and 8 are the densest — start there.
- **Raise the type floor.** Body text no smaller than 20pt equivalent; captions, eyebrows and footnotes no smaller than 16pt. Nothing below that anywhere.
- **The honesty footnotes must come up out of small grey type.** They are the caveats that make the claims defensible under examination — a marker who cannot read them cannot credit them.
- What you cut from the slide is not lost; the speaker says it. Slides carry evidence, not script.

---

# 2. Six diagrams to add or rebuild

Follow Rougier et al., *Ten Simple Rules for Better Figures* (PLOS Comp Biol, 2014) for all of them: thicker lines, larger text, strong contrast, no vertical text, no reliance on colour alone, and message over beauty. Reveal each figure whole — no progressive build-up.

## 2.1 — Slide 4: draw the similarity ladder *(highest value)*

The "four-level similarity ladder" is named as the novel contribution three times in this deck and drawn nowhere. The marker is being asked to accept the contribution as a noun phrase.

Draw a **vertical scale with four labelled rungs**, coarsest at the bottom:
- top rung: **same emotion family**
- then: **adjacent family**
- then: **same valence sign**
- bottom rung: **valence–arousal distance**

Plot the worked pair **"happy" / "excited"** on it twice, side by side:
- left, under the **conventional one-to-one rule** — scored as a miss, marked with a cross
- right, on **this ladder** — scored high, near the top

Draw a horizontal **chance line** across the ladder.

Replace the pull-quote with this figure. The quote's point is already made by the slide title; the figure is what the marker cannot get from the title.

## 2.2 — Slide 8: replace the table with a dot-and-null chart *(highest value for the evidence)*

The table currently asks the marker to perform twelve mental subtractions to see the finding. Draw it instead.

**Two small panels side by side** — one for valence-sign agreement, one for emotion-family agreement. In each:
- one horizontal axis, 0–100% agreement
- one row per subset: emotional prompts, face-classified, scene-classified, non-emotional
- a **hollow marker** for the null, a **filled marker** for the observed value, and a **connecting rule between them whose length is the effect**
- the **z value printed at the end of each row**

Two things this must show that the table hides: the face-versus-scene gap becomes a *visible distance*, and the non-emotional row sits exactly on its own null, which proves the specificity check graphically.

Nest the face and scene rows under the emotional row so that 402 + 205 = 607 is structurally obvious.

Lift the caveat "the prompt reader here is BART-MNLI, not the GoEmotions reader used above" onto its own line — it currently hides mid-sentence and it is the honest disclosure that protects the comparison.

## 2.3 — Slide 3: replace the four prose rows with a coverage matrix

The title promises "the space between them" and the layout never shows a space.

Draw a **2 × 2 matrix**. Rows: *emotion in text* / *emotion in image*. Columns: *generate* / *evaluate*. Fill three cells with a solid tint and a paper count. Leave the fourth cell — **evaluate emotion recovered from a generated line drawing** — as an empty outlined cell, and place this project's marker inside it.

The gap stops being a sentence the marker must trust and becomes a literal hole in a grid.

## 2.4 — Slide 7: promote the ruler, and show the permutation

(a) **Move the 41/76/84 ruler into the top half of the slide at roughly double its current size.** It is the best graphic in the deck sitting in the worst position. Tint the 76–100 band as the admissible region. Add a **ghost tick at 71** labelled *"passes a naive threshold, fails against chance."* Keep 84 as a heavy filled marker.

(b) **Replace box 1's prose with a two-frame schematic of the permutation.** Frame one: a column of prompts beside a column of drawings, joined by straight parallel rules — the true pairing. Frame two: the same two columns with the drawing column shifted by one, so the rules cross — a shuffled pairing. Caption it *"× 300, fixed seed."* That is the whole method in one picture.

## 2.5 — Slide 6: one corpus partition figure instead of four loose statistics

Draw a single **horizontal bar of width 1,025** with 13 pre-festival tests sliced off one end. Beneath it, **two parallel partition bars over the same 1,012**: cut A, emotional 607 / non-emotional 405; cut B, face-classified 591 / scene-classified 421. Add a bracket spanning both marking **87 repeated prompts covering 336 records**.

One picture shows what four separate numbers currently do not: these are two *independent* partitions of the same corpus, not four unrelated counts.

## 2.6 — Slide 11 (the hidden demo-fallback slide): make it echo slide 5

Rebuild it as **slide 5's pipeline skeleton at small scale with real values dropped in**: drawing → the five answers → the generated sentence → image distribution; prompt → prompt distribution; both converging on one compare node showing **84 against 76 on the same mini-ruler used on slide 7**.

If the live demo fails, the audience then watches the method run rather than reading a screenshot.

---

# 3. Smaller fixes

- **Slide 1** — put one specimen line drawing beside the title with its prompt underneath. This is a deck about drawings and shows none until slide 2. Also close the dead band in the middle third, and drop the registration marks at the four edge midpoints (they read as dust at projection distance; the corner crop marks are fine).
- **Slide 2** — the research question is the most important sentence in the deck and is currently set at body size inside a grey box while the illustrative panels shout louder. Invert that. Set the four sub-questions as four short labelled lines, not inline (i)–(iv) prose. Make the two panels equal height. Delete the cross-reference "see the closing slide".
- **Slide 4** — the dark slides silently drop the running foot while the light slides carry it. Carry it on every slide.
- **Slide 9** — either crop the interface screenshot to one legible region and run it at double size, or drop it and give the three steps the full width at a readable size. A shrunken full screenshot communicates nothing from the back of a room.
- **Slide 10** — shorten each bullet to a headline; the qualifier is spoken. Keep the two-column established / not-established ledger exactly as it is — that structure is right.
- **Terminology on slide 11** — the interface screenshot shows the app's labels at the time, "Same direction of mood" and "feeling similarity" (the interface has since been relabelled "Same valence sign"), which contradict the deck's controlled vocabulary ("valence-sign agreement", "valence–arousal distance"). If a screenshot remains, add one small caption noting that the interface uses lay wording for public visitors.

---

# 4. Unchanged — the wording lock still applies

Every claim was checked against the underlying statistics. Do not reword any of it.

- Never change **"agreement"** to "alignment", "accuracy", "fidelity" or "matching".
- Never say a drawing **"conveys"** or **"carries"** an emotion. This measures agreement between two automatic readers, not human perception. Quoting what the project does *not* claim is legitimate and should be kept.
- Keep every **"vs null"** figure and every **z-score** attached to its number.
- Keep all five footnotes.

The previous build reproduced all of this correctly. Preserve it.

---

# 5. If time is short, do these three

1. **2.1** — the similarity ladder on slide 4. Your contribution is currently invisible.
2. **2.2** — the dot-and-null chart on slide 8. This is the marking evidence.
3. **Section 1** — the word cut and the type floor across all slides.

Everything else is improvement. Those three are the difference.
