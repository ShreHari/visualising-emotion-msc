# Supervision Briefing — 17 July 2026

**Project 3199:** *Visualising Emotion: Text and Image Analysis of Human Feelings*
**Student:** Shre Hari Prem Anandh · **Supervisor:** Chaona Chen · MSc Artificial Intelligence (COM6912)

**Clock:** Presentation **Fri 4 Sep** (49 days). Dissertation **Wed 16 Sep, 15:00** (61 days). Length **10,000–20,000 words** excl. references. Presentation + dissertation = **100% of the mark**.
*(Verified verbatim from Lecture_1_ProjectOutline_PGT.pptx, slides 10, 12, 13.)*

---

## 1. The dataset — verified structure

`data.json` is a **flat object of 1,025 bare strings**, keys `"1"`–`"1025"`, contiguous, no gaps.
`all(isinstance(v, str)) == True`. There are no fields, no nesting.

**Therefore: no emotion labels, no taxonomy, no participant IDs, no demographics, no consent flags, no timestamps, no model metadata, no image filenames** — the structure has nowhere to put them.

**Linkage is positional only:** key *N* ↔ image numbered *N*. Clean bijection — 1,025 records, 1,025 files, zero gaps, zero orphans.

### Two silent data bugs — fix before any analysis

**Filenames use three incompatible patterns:**

| Records | Pattern | Count |
|---|---|---|
| 1–199 | `img_00001.PNG` (5-digit zero-padded) | 199 |
| 200–999 | `img_200.PNG` (unpadded) | 800 |
| 1000–1025 | `img_t1000.PNG` (`t` prefix) | 26 |

A naive `f'img_{i:05d}.PNG'` loader resolves **199 of 1,025 — under 20%**.

**Two files are lowercase `.png`** (records 2 and 4). This Mac's volume is case-insensitive, so `os.path.exists` masks it; `glob` does not — `glob('img_*.PNG')` returns 1,023. **This bug only appears on Colab/Linux/Docker.** Record 2 is one of the richest texts in the corpus.

### Text characteristics

- **Short:** median **4 words**, mean 6.0, max 107. **28.6% are a single word** (293 records).
- **100% pure ASCII.** No encoding repair needed (the French is unaccented).
- **Mixed affect is the norm:** `happy` 191×, `tired` 83×, `excited` 72×, `love` 21×, `sad` 18×, `anxious` 11×, `angry` 7×. "Tired but happy" recurs. **Single-label classification would destroy the corpus's most characteristic feature.**
- **Not all emotional:** bare nouns (`pigs` ×8), pop culture (`mickey mouse`), cars (`Nissan GTR Skyline R33`), questions to the AI (`what does god look like`), trolling. A filtering/coding step is mandatory — or "how the public actually uses an emotion installation" becomes a finding in its own right.
- **785 unique texts / 1,025 records.**

### Hidden metadata in the PNGs — recovered, not in the JSON

Every image carries a **C2PA/JUMBF provenance manifest** in a `caBX` chunk (14,823 bytes):
- `softwareAgent = "DALL·E"` · `claim_generator = "OpenAI-API c2pa-rs/0.31.3"` · `digitalSourceType = trainedAlgorithmicMedia`
- The manifest says **"DALL·E", not "DALL·E 3"** — the version is inference, not asserted.
- **No seed, no rewritten prompt.** Exact regeneration is impossible — state as a limitation.

**Per-record generation timestamps are recoverable** from the RFC-3161 signing time (ASN.1 GeneralizedTime). This is a free time variable the JSON lacks. Extracted for all 1,025:

- **Records 1–13 = pre-event test block** — scattered 26 Aug–18 Sep, non-monotonic, before the festival.
- **Records 14–1024 = the event proper:** 19 Sep (62), 20 Sep (44), 21 Sep (86), 22 Sep (91), **23 Sep absent**, 24 Sep (82), 25 Sep (143), 26 Sep (83), 27 Sep (91), 28 Sep (170), 29 Sep (159).
- **Record 1025 = lone 20 Oct outlier.**

The exclusion rule is simply **"drop 1–13."**

All images are 1024×1024 RGB, **uniformly monochrome line art** — so a style instruction was appended to every prompt by the installation software and **is not in `data.json`**. Records 473 and 771 explain why: outputs were plotted by a pen-drawing machine.

### The built-in natural experiment

**66 consecutive runs of identical text cover 215 records.** `Happy` at 614–624 (**11 in a row**), `pigs` at 258–265 (8), `Excited for the cold and Christmas` at 780–787 (8). Within a run: different MD5s, timestamps seconds apart. **These are independent DALL·E samples of one identical prompt** — *if* they were batch calls rather than one person hitting regenerate. That distinction matters enormously (see Q6).

---

## 2. What the project is

**Stated verbatim** (project spec page, `comapps.shef.ac.uk/projects/projects/3199`): dataset "collected from a previous public engagement event, where participants entered prompts describing their current emotions"; "Each prompt was then used to generate a corresponding image using the DALL-E model." Task authorises two strands — text analysis ("sentiment analysis, thematic coding, or NLP") and image analysis ("how effectively these images represent the emotions"). "You'll have the flexibility to select the focus." Flagged **"May require ethics approval."**

**Inferred, well-supported:** the event is **Festival of the Mind 2024, Sheffield** — participants name it (record 221: "festival of the mind in Sheffield, UK"), and timestamps cluster 19–29 Sep 2024 to match. The on-screen prompt was probably "How are you feeling?" — record 58 is someone typing the question back. **This is inference, not documented.**

**Reconstructed research question:** *When members of the public describe how they feel in free text, what do they say, and how faithfully does a text-to-image model render that feeling?*

The monochrome constraint is a **gift**: colour is stripped as a confound, forcing affect through composition, line energy and posture alone.

---

## 3. Against the June action items

| Item (18 Jun) | Status |
|---|---|
| "Get familiar with the previous datasets" | **Done, and then some** — the C2PA/timestamp recovery and the duplicate-run experiment are findings, not familiarity |
| "Start literature review (e.g. text-to-image)" | **Partly** — 8 papers downloaded 9 Jul; no review prose written; `mybibliography.bib` still holds 3 stubs |
| "Get the template" | **Acquired, unused** — only figure is the placeholder |

From 9 Jul ("Emotions extracted from text analysis; image analysis") — **neither has begun. There is no code in the folder.**

---

## 4. The literature, organised

**Theme A — Short-text emotion (the text half; 1 paper)**
`s41599-023-01816-6.pdf` — Liu, "Emotion classification for short texts: an improved multi-label method" (*Humanities and Social Sciences Communications*, 2023). **The most important paper here for this project.** Targets exactly the two properties the data has: short texts (median 4 words) and multi-label affect ("tired but happy").

**Theme B — Emotional alignment of AI and humans (the bridge; 1 paper)**
`2405.18510v1.pdf` — Lomas et al., "Improved Emotional Alignment of AI and Humans" (arXiv 2024, TU Delft). Closest to this dissertation's actual question. 240 images, SD v1 / DALL-E 2 / DALL-E 3, 10 emotions, 24 Prolific raters, 0–10 scale. Model effect huge (η²_G = 0.62; DALL-E 3 *M* = 7.04 vs DALL-E 2 5.79 vs SD v1 2.13); emotion effect small (η²_G = 0.07), *resentment* worst. Supplies a validated rating protocol.

**Theme C — Perception bias when judging AI images (1 paper)**
`3334480.3382892.pdf` — Ragot, Martin & Cojean, CHI 2020 LBW, N = 565. Identical artworks rated lower when merely *labelled* AI-made (*p* < .001, small: *d* = 0.05–0.13). **Lesson: blind raters to provenance or counterbalance the label.** Supplies a 4-item 7-point instrument and a mixed model with **participant *and* stimulus as random factors** — right for 1,025 items of varying quality.

**Theme D — Automatic alignment metrics (4 papers, the bulk)**
- `2404.01291v2.pdf` — the primary **VQAScore** paper. Unread; it is the origin of the metric the others benchmark against.
- `Li_..._CVPRW_2024` — **GenAI-Bench** (1,600 prompts, 80,000+ human ratings). **VQAScore dominates: Pearson 46.0 vs CLIPScore 19.3.** Best-of-N ranking lifts alignment (+0.22 DALL-E 3 at N=9) with **no training**. Documented failure: VQAScore overlooks fine-grained detail — a live threat for sparse line drawings.
- `2506.08480v1.pdf` — Zhang & Wan, "Re-Thinking the Automatic Evaluation of Image-Text Alignment". **The scepticism paper.** CLIPScore and DSGScore **reverse model rankings when the seed changes**; a **+1-pixel perturbation** shifts scores by up to 10.36 / 7.30 / 50.00 (VQAScore / CLIPScore / DSGScore). Their N = 1,000 ≈ this corpus — pre-empts "more data will fix it."
- `NeurIPS-2023-geneval` — **GenEval**, object-detector-based. Unread. **Transfer to monochrome line art is genuinely doubtful** — test before committing.

**Theme E — Distributional metrics (1 paper)**
`Koo_..._WACV_2026` — Conditional Fréchet Distance. Unread. Conditions on the prompt, unlike vanilla FID. Relevant for comparing the 11 `happy` draws as a **distribution**.

### Reusable metrics

| Tool | Use for | Caution |
|---|---|---|
| **VQAScore** | Primary automatic alignment metric | Weak on fine detail; max Δ 10.36 under perturbation |
| **CLIPScore** | Baseline/contrast only | Bag-of-words; Pearson 19.3; ranking-unstable — don't default to it |
| **GenEval** | Compositional check | Detector-based; unproven on line art |
| **Conditional FD** | Distribution across the 66 duplicate runs | Unread; needs per-condition sample sizes |
| **Dominance ratio** (per-item win rate) | Report beside every mean and *p* | From Zhang & Wan — exposes meaningless significance |
| **Lomas 0–10 scale** / **Ragot 4×7 items** | Human rating instrument | Ragot's "I perceive the meaning" → "I perceive the emotion" |
| **Krippendorff's α**; participant + stimulus as random factors | Agreement and mixed models | Chen will expect both |

**The gap — and the dissertation's opening:** none of the seven T2I papers is about emotion. Li et al.'s aspects are objects, counting, negation. **Emotional fidelity ≠ compositional alignment.** Lomas et al. evaluate emotional alignment but on *prompted templates*, not unmediated public self-report.

---

## 5. Ethics — the top risk

This is **secondary data**, which routes to the **self-declaration** questionnaire rather than a full application. But self-declaration requires **all five** answers to land correctly, and two are not obviously available:

1. *"Has consent been obtained from the original data subjects for the secondary use of their data for research purposes?"* → must be **Yes**. **Nobody knows. There is no consent log in the folder.**
2. *"Could your analysis and reporting lead to re-identification...?"* → must be **No**. **Not a reflexive No.** The corpus contains apparent **real names** — record 750 `[name]`, 751 `[name]`, 1020 `[name]` — and **sensitive disclosures**: 300 `missing my son. 30 long years`; 302 Parkinson's; 216 lifelong chronic pain; 532 Alzheimer's caregiving; 858 `I am desparate and alone and in need of love`; 982 dying pet. If quoted verbatim or paired with images, the data provider (who holds the original mapping) can re-identify contributors.

**The hidden third trigger:** the moment this project asks humans to rate whether an image conveys an emotion, it is **research with human participants**. The ethics deck closes every escape hatch in advance — anonymous Google Forms, non-identifiable feedback, MTurk annotators, and testing on yourself are all explicitly **not** exemptions.

**Hard facts:**
- Applications **take two weeks**, longer if amended. **Work requiring approval cannot begin before approval** — doing it first *is* the breach.
- Two weeks from today ≈ **31 July**, leaving ~6 weeks of protected working time. Not yet a crisis; **there is no second two-week window.**
- **Three online courses gate the application:** Information Management (~20 min), Data Protection (~10 min), Protecting Research Data (~10 min). **~40 minutes total — do these today.**
- System: `https://ethics.ris.shef.ac.uk/`. Route: student drafts → supervisor checks → classifies low/high risk → if low, supervisor is lead reviewer → admin check → approved.

---

## 6. A structural conflict to resolve today

The supplied LaTeX template ships with **Introduction, Literature Survey, Analysis, Planning, Conclusions** — five chapters, no Methodology/Results/Discussion.

Lecture 1 slide 12's **Experimental** column is **Introduction, Literature Review, Approach, Experiments, Results and Discussion, Conclusions** — six, and it matches this project.

Slide 12 says *"structure depends on the type of project, discuss with your supervisor."* **Following the template literally produces the wrong structure.**

---

## 7. Questions for Chaona

1. **Ethics route — self-declaration or full application, and can we answer the consent question?** Does the Festival of the Mind 2024 consent wording cover research reuse, and is there documentation anywhere? Given the two-week window and 16 September, this is the one thing I can't start without.

2. **Do I need to redact before I can answer the re-identification question "No"?** Records 750/751/1020 contain apparent real names; 216/300/302/532/858/982 are genuinely sensitive. Should I commit now to redacting names and excluding those records from figures — and does that make "No" defensible?

3. **What was the full prompt actually sent to DALL·E?** Every image is monochrome line art, so the installation appended a style instruction, but `data.json` has only the participant's raw words. Do you or the developer still have the generation script? Without it my independent variable is only partly known. (Relatedly: the C2PA manifests say only "DALL·E", not "DALL·E 3" — can API logs settle the version?)

4. **Is the annotation scheme mine to design, or do you have one in mind?** No labels of any kind exist, and mixed affect is the norm — single-label would destroy the data's signature feature. The Liu (2023) multi-label short-text paper is the only one on the list addressing the text half. Is that the steer, or do you want dimensional valence/arousal?

5. **How do we handle the non-emotional fraction?** `pigs` ×8, `mickey mouse`, `Nissan GTR Skyline R33`, plus trolling. Filtering could halve *N*; alternatively "how the public actually uses an emotion installation" is a finding. Also — do you agree records 1–13 should be dropped as pre-event tests? Their C2PA timestamps are 26 Aug–18 Sep, before the festival.

6. **Are the 66 duplicate-prompt runs a natural experiment or a system artefact?** 215 records sit in consecutive identical-text runs — `Happy` 11 in a row — with byte-distinct images and timestamps seconds apart. If those are automated batch calls, they're independent samples and "how stable is DALL·E's rendering of *happy* across 11 draws" is a self-contained chapter. If it's one person hitting regenerate, **records 614–624 are one participant, not eleven** — which breaks independence for every per-record statistic. Do you know which?

7. **Does this project need a human rating study, and must it be in the same ethics application?** Ragot et al. show that merely labelling an image AI-made depresses ratings. If a rating study is in scope, it needs a PIS and consent form **now**, not in August.

8. **Which structure do I follow** — the template's five chapters, or slide 12's six-chapter Experimental structure?

9. **Is VQAScore the right primary metric given the stimuli are sparse line drawings?** Li et al. show it dominates CLIPScore (46.0 vs 19.3), but document that it overlooks fine-grained detail, and Zhang & Wan found a 1-pixel perturbation moves it by up to 10.36. GenEval is detector-based — I doubt it transfers to line art. Should I validate on a hand-rated subset first?

---

## 8. Proposed next two weeks (17–31 July)

**Today** — the three online ethics courses (~40 min; they gate everything). Cross-check deadlines on Blackboard ("COM PGT Dissertation Project (2025~26)").

**Week 1 (18–24 Jul) — ethics + infrastructure**
- **Draft the ethics self-declaration, to Chaona within 3 days.** Submit by ~24 July so the two-week window closes with ~6 weeks in hand. If uncertain after her review, email `com-ethics@` **and CC Chaona** (the deck marks the CC as required).
- **Fix the loader once, properly:** resolve all three filename patterns and both cases; assert `len(index) == 1025` and fail loudly. **Test on Linux/Colab, not just this Mac.**
- **Build the table the JSON should have shipped:** `record_id | text | image_path | c2pa_timestamp | is_pretest | run_id | word_count | language`. One day's work.
- Set up Overleaf from the template, commit to git, replace the 3 stub `.bib` entries with the 8 real papers.

**Week 2 (25–31 Jul) — literature + first prose**
- **Read, in this order:** Liu (2023) short-text multi-label → primary VQAScore paper (`2404.01291v2`) → GenEval → Koo. Use Keshav's three-pass method (Lecture 2).
- **Write 1,500–2,000 words of Lit Review + Introduction.** The gap statement writes itself: *seven papers evaluate compositional alignment; none evaluates emotional fidelity; Lomas et al. evaluate emotional alignment but on prompted templates, not unmediated public self-report.*
- **Hand-code a 100-record pilot** in whichever scheme Chaona specifies, recording ambiguity. Validates the scheme cheaply before committing to 1,025.
- **1-page written progress note before the next meeting** (~31 Jul).

**Explicitly deferred until ethics approval:** all model-running, metric computation, and any human rating study. That is the deck's rule, not a preference.

**Flag for the *next* plan:** the **4 September presentation** is a separate, earlier, mark-bearing deliverable. Working back from 16 Sep 15:00 and a 10,000-word floor, **first full draft by ~1 September.**
