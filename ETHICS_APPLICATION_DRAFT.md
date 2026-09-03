# Ethics Application — DRAFT (for review before submission)

> **STATUS (20 Aug 2026): DESIGNED, NOT SUBMITTED — decision taken after supervision.**
> The human-rating study was never a supervisor requirement; it came from the research-gap
> analysis. With ~4 weeks to submission and the dissertation unwritten, it was dropped so the
> writing could proceed. Approval alone would have taken ~2 weeks.
>
> **This document is not waste — use it twice:**
> 1. **Limitations chapter** — it defines precisely what the computational results do NOT
>    establish: that the automatic readers perceive emotion as a person does.
> 2. **Future work / appendix** — a fully specified, ready-to-run validation study
>    (design, participant information sheet, consent form, recruitment text, instrument).
>
> The ethics content that DOES belong in the dissertation is the secondary-data handling:
> the dataset review, the name-redaction procedure, keeping illness/grief content per the
> supervisor's judgement, and the demo's privacy design (nothing stored, no request log,
> sensitive records withheld among decoys so the flagged set cannot be recovered by probing).


**Project:** Visualising Emotion: Text and Image Analysis of Human Feelings
**Student:** Shre Hari Prem Anandh · MSc Artificial Intelligence · School of Computer Science, University of Sheffield
**Supervisor:** Dr Chaona Chen
**System:** ethics.ris.shef.ac.uk (University Research Ethics — PGT dissertation)

> This is a **draft you review, edit, and submit yourself** — it is administrative, not part of your
> assessed dissertation. Everything in **[BRACKETS]** is something you must confirm or fill in.
> The application has two components: (1) reuse of an existing dataset, (2) a new human-rating study.

---

## ✅ Before you can submit — the gate (do first, ~40 min)
Complete these three mandatory online courses (they unlock the ethics form):
- [ ] Information Management (~20 min)
- [ ] Data Protection (~10 min)
- [ ] Protecting Research Data (~10 min)

## ⚠️ The one thing to confirm with Chen
- [ ] **Consent for secondary use:** was the Festival-of-the-Mind dataset collected with consent for its
  use in *research*? You need to be able to answer this. If yes, note where that consent is documented.

---

# PART A — Application form answers (paste into the online form)

**A1. Project aims / summary**
> This project investigates how faithfully a text-to-image AI model (DALL·E) conveys human emotion.
> It analyses an existing dataset of ~1,000 short, anonymous emotional self-descriptions collected at a
> public engagement event, each of which was turned into a black-and-white line drawing by DALL·E. Using
> natural-language processing and computer-vision methods, the project measures the *similarity* between
> the emotion expressed in each text and the emotion conveyed by its drawing. To validate these automated
> measures, a small anonymous online study will ask adult volunteers to rate how well a sample of drawings
> convey the feelings in their prompts.

**A2. Does the project involve human participants?** Yes — for the validation rating study (Part C).
**A3. Does it use secondary data (data collected by others)?** Yes — the drawing dataset (Part B).
**A4. Does it involve vulnerable groups / children / patients?** No — adults (18+) only.
**A5. Deception?** No. **A6. Physical/psychological intervention?** No.
**A7. Risk level:** **Low risk** — anonymous adult volunteers, a short non-sensitive judgement task, no
personal data collected, voluntary with the right to withdraw.

---

# PART B — Secondary data (the existing drawing dataset)

**B1. Source.** ~1,025 text–image pairs from a public engagement event [Festival of the Mind, Sheffield,
2024]. Members of the public typed a short description of how they felt; each was rendered as a
black-and-white line drawing by the DALL·E model. Provided to the student by the supervisor.

**B2. Consent basis.** [CONFIRM WITH SUPERVISOR — the data were collected at a public event; state the
consent basis for research reuse here.]

**B3. Personal data & re-identification risk — and how it is mitigated.**
The text entries are short and generally non-identifying, but a small number contain first names or
personal disclosures. To ensure findings cannot lead to re-identification:
- A **pre-processing step redacts personal names** (automated detection with manual confirmation),
  replacing them with a neutral token, while preserving emotional content.
- Records containing sensitive personal disclosures **will not be reproduced verbatim or paired with
  their image as identifiable figures** in the dissertation.
- Only **aggregate / anonymised** results are reported; no attempt is made to identify any contributor.

**B4. Data management (GDPR).** The dataset is stored only on **University-managed systems** (University
OneDrive / encrypted local storage), accessed only by the student and supervisor, not shared externally,
and handled per the University Research Data Management policy. No new personal data are added to it.

---

# PART C — The human-rating validation study

**C1. Purpose.** To check whether the project's automated emotion measures agree with human judgement —
i.e. do people rate the drawings' emotional fit the same way the pipeline scores it.

**C2. Participants.** [~30–50] adult volunteers (18+), fluent in English. Recruited via
[student networks / social media / Prolific]. No vulnerable groups.

**C3. What participants do.** An anonymous online survey (~[15] minutes). For each of ~[60–80] text–drawing
pairs (a stratified sample), the participant:
- reads the short text, views its drawing, and rates **"How well does the drawing convey the feeling in
  the text?"** on a 0–10 scale; and
- selects **which emotion the drawing best shows** from a fixed list.
No right/wrong answers; participants may skip any item and stop at any time.

**C4. Informed consent.** Before starting, participants read the **Participant Information Sheet** (Part D)
and give consent via tick-boxes on an online **Consent Form** (Part E). No data are recorded before consent.

**C5. Anonymity & data collected.** **No identifying information is collected.** Responses are anonymous.
Optionally collected for context only: age range and whether English is a first language. Responses cannot
be linked to any individual.

**C6. Risks and mitigation.** Minimal. The task is a low-stakes judgement of drawings. **A small number of
drawings depict themes such as sadness, illness or grief**; participants are warned of this in the
information sheet and told they may skip any item or withdraw at any time with no consequence.

**C7. Payment / incentives.** [None — voluntary.  OR: Prolific participants paid at the standard rate
(~£9/hour equivalent).]

**C8. Data management.** Responses are collected via [Google Forms / University Qualtrics], exported and
stored on **University OneDrive**, analysed in anonymised/aggregate form, and retained/destroyed per
University policy at the end of the project. No personal data leave University systems.

**C9. Right to withdraw.** Participants may stop at any point. Because responses are anonymous, once a
completed survey is submitted it cannot be individually identified for later withdrawal — this is stated
clearly on the information sheet.

---

# PART D — Participant Information Sheet (attach to application)

**Study title:** How well do AI-generated drawings convey emotion?
**Researcher:** Shre Hari Prem Anandh, MSc Artificial Intelligence, University of Sheffield
**Supervisor:** Dr Chaona Chen ([supervisor email])

**What is this study about?**
An AI drew pictures based on short descriptions of how people felt. We want to know how well those
drawings capture the feeling in the words. You'll be shown some text–drawing pairs and asked for your
opinion. There are no right or wrong answers — we're interested in what *you* think.

**Do I have to take part?** No. Taking part is completely voluntary. You can stop at any time, and you can
skip any item you don't want to answer.

**What will I do?** You'll view about [60–80] short text-and-drawing pairs and, for each, rate how well the
drawing conveys the feeling (0–10) and pick the emotion you think it shows. It takes about [15] minutes.

**Are there any risks?** The task is low-stakes. **Please note: a few of the drawings depict themes such as
sadness, illness or grief.** If you'd prefer not to see a particular image, you can skip it, and you can
stop the study at any time.

**Will my data be anonymous?** Yes. We do **not** collect your name or any identifying information. We may
ask your age range and whether English is your first language, only to describe our participants as a
group. Your responses cannot be traced back to you.

**What happens to my answers?** Anonymous responses are stored securely on University of Sheffield systems,
analysed together with everyone else's, and used only for this MSc dissertation. They will be
retained and destroyed in line with University policy.

**Can I withdraw?** You can stop at any time. Because responses are anonymous, once you submit a completed
survey we cannot identify it to remove it later.

**Questions or concerns?** Contact [student email]. If you have a concern about how the study was
conducted, contact [the School's Ethics contact / Registrar & Secretary's Office, per University guidance].

---

# PART E — Consent Form (attach to application)

**Study:** How well do AI-generated drawings convey emotion?

Please confirm you agree with each statement (tick to proceed):
- [ ] I have read and understood the Participant Information Sheet.
- [ ] I understand my participation is voluntary and I may stop at any time and skip any item.
- [ ] I understand that some drawings may depict themes such as sadness, illness or grief.
- [ ] I understand my responses are anonymous and cannot be traced back to me.
- [ ] I understand that, because responses are anonymous, I cannot withdraw my data after submitting.
- [ ] I am 18 years of age or older.
- [ ] I agree to take part in this study.

*(Online: the survey does not begin until all boxes are ticked.)*

---

# PART F — Recruitment text (email / social post)

> **Help with an MSc study — 15 minutes, anonymous.**
> Can an AI draw a feeling? I'm studying how well AI-generated drawings capture the emotions people
> described. I'm looking for adults (18+) to rate some text-and-drawing pairs — no right answers, just
> your opinion. It's anonymous and takes about 15 minutes. [link] Thank you!
> *(Note: a few drawings depict themes such as sadness or grief; you can skip any image.)*

---

# PART G — The rating survey (the instrument)

For each of ~[60–80] pairs, shown one at a time:

> **Text someone wrote:** *"[the prompt]"*
> **The AI's drawing:** [image]
>
> **Q1.** How well does the drawing convey the feeling in the text?
> `0 — not at all  …………………  10 — perfectly`
>
> **Q2.** Which emotion does the drawing show? (pick one)
> ☐ Happy ☐ Sad ☐ Angry ☐ Afraid ☐ Surprised ☐ Disgusted ☐ No clear emotion ☐ Other: ___

Sample of ~[60–80] chosen to cover: emotional vs non-emotional prompts · face vs scene drawings ·
positive vs negative feelings · a few repeated-prompt cases. Each pair rated by [3–5] participants.

**Analysis (what earns the marks):** inter-rater agreement (Krippendorff's α); and the correlation
between participants' 0–10 ratings and the pipeline's similarity scores — validating the automated method.

---

## Submission checklist
- [ ] Three online courses completed
- [ ] Consent-for-secondary-use question confirmed with Chen (Part B2)
- [ ] Fill every [BRACKET] (participant numbers, recruitment method, tool, payment, emails)
- [ ] Attach: this application + Participant Information Sheet (D) + Consent Form (E)
- [ ] Supervisor (Chen) reviews and classifies risk before it goes for approval
- [ ] If uncertain, email the School ethics contact **and CC Chen**
