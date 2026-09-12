# Viva / Marker Question Bank

**29 questions across eight areas, with sayable answers.** Every figure below is one the project actually reports. Where a question is hostile, the answer concedes first and bounds second — that is the pattern that earns marks.

### Ground rules for answering out loud

- Always name **both readers**: "prompt-reader / image-reader agreement". Never say the drawing *shows* or *communicates* an emotion — you have no human data.
- Reserve **"similarity"** for the valence-arousal metric, which is a graded distance. Say **"valence-sign agreement"**, never "mood direction".
- Never quote a raw percentage without its null. `68.8%` bare is the single most dangerous number in the project.
- When you don't have something — a human rating, a second coder — say "I have not done that" in the first six words, then say what you *do* have.

---

## 1. Research question & contribution

### Q1. "Tell me your research question in one sentence."

**Answer.** The project asks how far an automatic reading of a monochrome line drawing agrees with an automatic reading of the free-text feeling that produced it, and whether that agreement is best expressed as graded closeness rather than right-or-wrong. Concretely: across 1,012 public-festival prompts and their generated drawings, does a describe-then-extract image reader land in the same emotion family, the same valence sign, and the same neighbourhood of valence-arousal space as a prompt reader, more often than re-shuffled pairings of the same corpus would give? Everything is scored against a 300-shuffle null.

*If pressed further:* it is deliberately a question about two automatic readers, not about human perception — no human rated any drawing in this project.

---

### Q2. "What is genuinely novel here?"

**Answer.** Three things. First, the framing my supervisor named herself: "similarity, not matching". Emotion is subjective, there is no ground truth, humans disagree and models are noisy, so asking whether an image's emotion is *right* against a text is too simplistic — "happy" and "excited" should count as close. So I score graded closeness on four metrics across seven emotion families. Second, the architecture: I never ask a vision model for an emotion; I describe the image factually, then read emotion out of that description, so both sides are text. Third, the corpus: 1,012 real public prompts with monochrome line art.

*If pressed further:* the novelty is in the measurement design, not in a model — every component is off-the-shelf and frozen, and I claim no modelling contribution.

---

### Q3. "Isn't 'similarity not matching' just a softer scoring rule that inflates your numbers?"

**Answer.** It would be, if I reported the raw rate alone. I don't. Every graded metric is scored against a null built by re-shuffling prompt-image pairings 300 times *within the same subset*, so the loosening applies identically to the null and cancels. Family agreement on emotional prompts is 53.0% against a 38.8% null, z+10.3; valence-arousal similarity is 83.8% against a 77.3% null, z+12.2. The looser metric lifts both numbers; the claim is the gap. And on prompts the text reader labels neutral the gap disappears — 76.6% against a 76.6% null, z+0.3 — which a purely inflationary metric would not do.

---

## 2. Literature & gap

### Q4. "Where does this sit in the literature, and what is the gap?"

**Answer.** Affective image computing is dominated by photographs and paintings, where colour, texture and scene content do much of the work, and it is overwhelmingly evaluated as one-to-one label accuracy against curated ground truth. Sketch and line-art work, by contrast, is mostly recognition and retrieval, not affect. The gap sits at the intersection: minimal monochrome line art, generated from first-person mixed-affect self-reports rather than annotator labels, and evaluated by graded agreement rather than accuracy. Across the 73-paper library I built, almost nothing combines a self-report prompt side with a stripped-back visual side while refusing the ground-truth assumption.

*If pressed further:* the closest neighbours are text-to-image affect studies, but they typically score against curated emotion labels, which quietly reintroduces the ground truth my design argues does not exist for this material.

---

### Q5. "There is a large literature on colour and emotion, and your images have no colour. Doesn't that make your stimulus a special case?"

**Answer.** Yes, and deliberately so. That literature is precisely why line art is a hard case: remove hue and saturation and the drawing has to work through posture, facial line, composition and the number of figures. But I want to be exact about what I can claim. The corpus is monochrome throughout and there is **no colour-control condition**, so I make no claim whatsoever about colour's contribution. I cannot tell you that line art is harder than colour imagery; I can only tell you the material I have sits at the sparse end, and cite the colour literature as motivation for choosing it.

---

## 3. Methodology & architecture

### Q6. "Walk me through the pipeline."

**Answer.** Two independent readers. On the prompt side, GoEmotions — roberta-base, about 125M parameters — labels the visitor's typed text across 28 labels, collapsed to seven emotion families. On the image side, BLIP-VQA, about 385M, is asked five fixed factual questions: what is the facial expression, what is the person doing, what is the body posture, how many people are there, what is in the picture. The answers are assembled into one neutral sentence, which goes to BART-large-MNLI, about 407M, as zero-shot classification over the same seven families. The two family distributions are then compared on four metrics. Nothing is fine-tuned.

---

### Q7. "Why describe-then-extract? Why not ask a vision-language model for the emotion directly?"

**Answer.** Two reasons. My supervisor's: don't force CLIP to output emotion — it is trained on real colour photographs and is good at objects, not affect. And a design reason: describing the image first makes both sides of the comparison text, so I compare like with like instead of crossing a modality gap inside one embedding space. I tested the alternative like for like: same GoEmotions prompt reader, same 607 emotional records, same measures, only the image reader varied. Describe-then-extract reaches 53.0% family agreement against direct CLIP's 22.4% — a difference of 30.6 points, clustered 95% interval +25.5 to +35.6, cluster-level p below 0.0001 — and 64.0% valence-sign agreement against 31.1%. Manual inspection found CLIP reading an arms-raised celebration as anger at 0.73.

---

### Q8. "Why five fixed questions? Why not simply caption the image?"

**Answer.** I tried a single BLIP caption first and it failed: the captions were too terse and the emotion reader collapsed almost everything to surprise. The five questions are chosen to be factual and answerable rather than affective — expression, action, posture, people count, scene content — so the describer commits to the specific visual facts the emotion reader needs. Holding the same five constant across all 1,012 records makes the description stage an instrument rather than a per-image judgement. I present it as a designed instrument, and I accept that a different question set would produce different descriptions.

*If pressed further:* the question set was fixed for the whole corpus and never tuned per subset. An ablation of the description template — each answer dropped in turn, the expression word fixed, and a people-aware template — was run by re-composing the cached answers and re-running only the NLI stage. It shows the reading rests on one word: removing the expression sentence collapses family agreement from 53.0% to 20.3%, while removing action, posture or scene moves it by one to three points. In effect the pipeline asks the describer for the facial expression and maps that word to a family.

---

### Q9. "You use different readers on the two sides. Isn't that an uncontrolled asymmetry?"

**Answer.** It is a deliberate asymmetry with an empirical reason. The two sides are different registers: prompts are first-person feeling statements with a median of about four words; descriptions are third-person scene sentences. Run GoEmotions on the image descriptions and it collapses to neutral above 0.95 — it needs first-person feeling language. Run BART-MNLI on the prompt side and it over-reads surprise, on 333 of the 1,025 prompts. So each reader is used where it works. The cost is that the two sides have different label priors, and the shuffle null absorbs that, because it uses exactly the same two readers.

---

### Q10. "Why did you not use a model designed for sketches?"

**Answer.** I should have explored them further — my supervisor suggested exactly that, and it sits openly on my not-done list. The practical constraint was capacity: I tried two larger describers and both failed outright. Qwen2.5-VL-3B exceeded 16GB of RAM and ran four hours forty-five minutes with zero progress; Florence-2 was incompatible with transformers 5.14. Architecturally, sketch-specific models are mostly recognition and retrieval models trained on stroke data, so they would replace the *describer*, not the emotion reader, and the description stage would still be needed. It is the most obvious next experiment.

---

## 4. Evaluation & statistics

### Q11. "Explain your null. Why is shuffling the right comparison?"

**Answer.** For each subset I randomly re-pair prompts with images 300 times at seed 7 and recompute every metric. Shuffling destroys the pairing while preserving both marginal label distributions, so the null keeps the same class imbalance, the same reader biases and the same metric compression as the real data. The reported z is the observed value's position in that shuffle distribution. It is the right comparison because a uniform-chance baseline would flatter me badly: the valence-arousal metric would appear to beat 0% when its true random level is about 76%.

*If pressed further:* this is also what makes the claim falsifiable. If shuffled pairings had produced the same rates as true pairings, there would be nothing here — which is exactly what happens on the non-emotional subset at z+0.3.

---

### Q12. "Your similarity score of 84% — what does that actually mean if random pairs score 76%?"

**Answer.** Fair challenge, and the absolute number is the least informative thing about it. Valence-arousal similarity is a bounded distance in a two-dimensional space where the seven families occupy a limited region, so it has a mathematical floor of 41% — it cannot reach zero — and random pairings average about 76%. So 83.8% must never be read as "84% correct". The claim is the 6.5-point gap over that subset's own 77.3% null, at z+12.2. The evidence that the metric is not simply saturated is the non-emotional subset: 76.6% against a 76.6% null, z+0.3.

*If pressed further:* in future I would report this metric only as a standardised gap, never as a percentage, because the percentage invites precisely the misreading you are pointing at.

---

### Q13. "Why should I believe 49% beats 25% when you changed the prompt reader between the two?"

**Answer.** That 49.3-against-25.3 figure is the historical v1 comparison, and I no longer lead with it, for exactly the reason in the question: it held the prompt side at BART-MNLI on a 608-record subset from an older lexicon rule. The like-for-like re-run holds the GoEmotions prompt reader, the 607 emotional records and the same overlap formula constant and varies only the image reader: 53.0% against 22.4% family agreement, +30.6 points, clustered 95% interval +25.5 to +35.6, cluster-level p below 0.0001. Neither reader has ground truth, so what this shows is that the two image readers disagree, with describe-then-extract far closer to the text reader — not that it is more accurate.

---

### Q14. "Your non-emotional control set is defined by the same classifier you are testing. Isn't that circular?"

**Answer.** Yes, in the sense that matters, and I say so in the write-up. The split is the prompt reader's own output — top-1 label not equal to neutral — and no human ever validated it. So the control is not "prompts a person would call unemotional"; it is "prompts GoEmotions calls neutral" — 68 of the 405 contain a plain affect word such as calm, content or tired, and two consist of a name alone. What it can still do is bound the *metric*: if valence-arousal similarity were returning a high number regardless of input, it would return one here too, and it does not — 76.6% against a 76.6% null, z+0.3, and z+0.04 on the 335 records left after removing the affect-word and name-only prompts. It is a specificity check on the instrument, not an independent human-defined control condition.

*If pressed further:* only the valence-arousal metric is informative on that subset. Valence-sign and family agreement are degenerate there by the subset's own definition, since almost everything is neutral, so I do not present them as a passing control.

---

### Q15. "Is the face-versus-scene difference statistically significant?"

**Answer.** Yes. Face-classified records, n=402, reach 73.9% valence-sign agreement against a 53.5% null, z+10.4, and 61.9% family agreement against 45.8%, z+10.3. Scene-classified records, n=205, reach 42.9% against 29.6%, z+5.8, and 35.6% against 26.2%, z+4.4. The difference is +30.9 points for valence sign, 95% interval +22.6 to +40.6, and +26.3 points for family, interval +18.4 to +35.3; a clustered permutation test gives p = 0.0001 for both. I clustered on prompt identity because 249 records repeat an earlier prompt, so records are not independent. What that establishes is that the gap is not sampling noise. It does not remove the circularity: the split is the describer's own classification. And the template ablation changes what the contrast means: under a people-aware description — no person or expression clause where the describer reports no person — the scene rows fall to their null, valence sign 4.7% against 3.4%, z +1.6. So for this reader it is faces, and only faces, not faces more than scenes.

*If pressed further:* the scene result is the fragile one — on distinct prompts its family z falls to +2.6 and does not survive a Holm correction across the 36 non-degenerate tests.

---

### Q16. "You report z-scores everywhere. Where are the confidence intervals?"

**Answer.** I do report them — every rate carries a clustered-bootstrap 95% interval, 10,000 draws resampling prompt groups because 249 records repeat an earlier prompt. Emotional valence-sign 64.0% [58.6, 68.8]; face 73.9% [68.3, 79.2]; scene 42.9% [33.1, 51.1]. The scene interval is the widest, as expected at n=205. The z is something different: a position within a 300-shuffle null distribution, which says how far the observed value sits from re-paired chance, not how precisely the rate is estimated. Across seeds 1 to 5 the headline z moves between +11.2 and +12.2, so I treat it as an ordering statistic; the intervals carry the inference about the rate.

---

### Q17. "How do you know your nulls are meaningful in every subset you report?"

**Answer.** The code checks it. A null is degenerate when shuffling cannot change the score — every prompt in the subset shares one label — and the analysis detects that from the null's own spread: zero standard deviation means no z is printed. Two families of subset trip it for the valence-sign and family metrics: the single-valence subsets, where re-pairing cannot move the sign, and the neutral-labelled subset, where every prompt family is neutral. The negative-prompt family null is not degenerate, and the code correctly leaves it in. In the degenerate cases I report only the valence-arousal metric or withdraw the claim.

---

## 5. Results

### Q18. "Give me your headline result."

**Answer.** On the 607 emotional prompts, prompt-reader / image-reader agreement is clearly above the shuffle null on all four metrics: valence-sign 64.0% against a 45.6% null, z+11.1; family 53.0% against 38.8%, z+10.3; top-3 overlap 50.6% against 39.4%, z+11.6; valence-arousal similarity 83.8% against 77.3%, z+12.2. The effect concentrates where a figure is drawn: face-classified records reach 73.9% valence-sign agreement against a 53.5% null, z+10.4. On the 405 prompts the text reader labels neutral the valence-arousal metric sits flat on its null, z+0.3. That is a consistent, well-above-chance agreement between two automatic readers.

---

### Q19. "Your face/scene split is circular, isn't it?"

**Answer.** Yes, and the mechanism is worse than it first appears, so let me state it exactly. The split is **not** an expression detector. 414 of the 421 scene-classified records — 98.3% — are ones where the describer answered that no people are present, so it is the people-count answer that drives the label. And 406 of those 414 descriptions still contain an expression word. The real circularity is that the same describer output supplies both the split variable and the text the emotion reader then reads — and where the expression answer names an affective state, the reader's top-1 family follows it 99.8% of the time. So face-versus-scene is a property of the describer's output, not an independent visual category. The ablation makes the cost concrete: the scene result in the headline table was agreement between the prompt and an expression the describer invented for a drawing with no person; describe those drawings honestly and this reader finds nothing above chance in them.

*If pressed further:* the honest fix is to derive the split from outside the pipeline — a face detector run on the image, or human labels — and re-run. A 120-drawing blind coding sample is drawn for exactly that; the full re-run is not done.

---

### Q20. "Do your headline results survive removing repeated prompts?"

**Answer.** Partly, and I will not claim they all hold equally. On the 763 distinct prompts, every all-emotional metric stays strongly above its null, z+9.3 to +10.8, and face-classified valence-sign agreement holds at 71.8%, z+8.4. The scene result does not hold: it weakens substantially, to 37.3% at z+3.5 on valence sign and 30.8% at z+2.6 on family, and that family result does not survive a Holm correction. That is the honest picture — the face effect survives de-duplication, the scene effect is much thinner and depends partly on repeated prompts. I report the weakening explicitly rather than the pooled figure, because the pooled scene number would overstate what is there.

---

### Q21. "You have 87 prompts drawn more than once. What does that tell you?"

**Answer.** It gives a stability check on the generator-plus-reader chain. Across the 336 records in those groups, the image reader returns the same emotion family for 68.8% of drawings within a group, against a permutation null of 59.4%, z+4.5, p = 0.0001; 28 of the 87 groups are fully consistent against 14.5 by chance. I quote both numbers together deliberately: 68.8% on its own looks like a reliability coefficient, and it is not — half the groups are pairs, whose modal agreement cannot fall below 50%, and the family priors are skewed. What it shows is that the same prompt tends to yield drawings the reader reads alike, above what re-shuffling group membership gives. It says nothing about correctness.

---

## 6. Limitations

### Q22. "You say the drawing conveys the emotion. How do you know? You never asked a human."

**Answer.** I don't know, and that is not a sentence I make. What this project measures is **agreement between two automatic readers** — a text reader on the prompt and a describe-then-extract reader on the image. That is the single most important limitation of the work, and it is the first line of my limitations section. No human rated any drawing, so I have no evidence about what a viewer perceives. What I can defend is that the two readers agree far above re-paired chance, most strongly where a figure is drawn. Whether either reader tracks human perception is a separate, untested question.

*If pressed further:* even the zero-shot hypothesis template is literally the string "This scene conveys {}." — that is a template the NLI model requires, not a perceptual claim, and I am careful not to let its wording leak into my conclusions.

---

### Q23. "Why didn't you validate with human ratings?"

**Answer.** Time and scope, and I will not dress it up — it is the single largest item on the not-done list. It is also the highest-value missing piece, so I have specified it rather than just naming it, and drawn a 120-drawing blind single-coder sample as the first step: a sample of drawings stratified by face/scene and by emotion family, rated on valence and arousal by multiple raters, with inter-rater agreement reported *first*, because if humans disagree with one another then their disagreement sets the ceiling on any automatic reader. That design also demonstrates my supervisor's point — human disagreement is exactly why graded similarity is the right frame rather than a correctness score.

---

### Q24. "You dropped a positive-versus-negative analysis. Why shouldn't I read that as cherry-picking?"

**Answer.** Because I am telling you it existed and why it went. Splitting emotional prompts by valence produces subsets that are single-valence by construction, so the shuffle null becomes degenerate: re-pairing within a subset where nearly everything shares a sign cannot move the sign metric, and the null collapses toward the observed rate. On top of that, the two readers disagreed on those subsets. A result standing on a degenerate null is not a result, so I withdrew the claim rather than report an impressive-looking number I could not defend under exactly this question.

---

## 7. Technical implementation

### Q25. "You report no failures across 1,025 records. Isn't that suspiciously good?"

**Answer.** It would be, if it meant accuracy. It does not. "No unhandled errors" means exactly that: every record passed through the describer, both readers and the metric code without crashing or emitting a malformed output. It is a robustness statement about the pipeline, not a correctness statement about emotions. I make no accuracy claim at all, because there is no ground truth to be accurate against — that is the premise of the whole design. I flag this explicitly in the write-up precisely because it is the phrase a reader is most likely to over-interpret — the describer returns an expression answer for 406 of the 414 drawings in which it reports no people, and none of that counts as a failure.

---

### Q26. "Tell me about your test suite."

**Answer.** Two layers. A shell self-test checks the environment, the data counts, the redaction audit, a live three-image run of the pipeline and that every analysis script runs. A numeric layer, `test_numeric.py`, pins each headline figure to the result file that produces it — family agreement 53.0% on the 607, the consistency null, the like-for-like difference — and unit-tests the metric functions, including the 0.412 floor of the valence-arousal measure. The figures read the same result files. So a change in the analysis fails the build rather than drifting silently. That protects reproducibility; it is not evidence that any figure is *correct*, because there is no ground truth to be correct against.

---

### Q27. "Could I re-run this and get your numbers?"

**Answer.** Yes. Every model is off-the-shelf and frozen at a pinned version — BLIP-VQA base, BART-large-MNLI, GoEmotions roberta-base, and OpenCLIP ViT-B/32 on LAION-2B for the comparison — nothing is fine-tuned, so there are no trained weights of mine to reproduce. All nulls use 300 shuffles at seed 7. The corpus is 1,025 records, of which 13 are pre-festival developer tests, identified from recovered C2PA signing timestamps and excluded, leaving 1,012 analysed. Prompts are name-redacted as a data pre-processing step before any reader sees them. The pipeline runs from the raw records.

---

## 8. Future work

### Q28. "What is the single next study you would run, and what would you do with six more months?"

**Answer.** Human ratings first, because everything else is bounded by their absence: a stratified sample rated on valence and arousal by multiple raters, reporting inter-rater agreement before placing either automatic reader against the human distribution. Second, a scene-capable describer: the people-aware ablation shows this reader finds nothing above chance in scene-classified drawings once the invented expression clause is removed, so whether those drawings hold a readable feeling — which the human check tests — needs a describer that reads affect from composition, posture and setting rather than from a facial-expression word. Third, replace the describer with a sketch-trained or drawing-specific model, since the describer is the component every result rests on, and derive the face/scene split from outside the pipeline so it stops being circular.

---

### Q29. "Suppose all this holds. What is it actually for?"

**Answer.** Two things. Methodologically it is a reusable instrument: a frozen describe-then-extract pipeline with a shuffle null that can be pointed at any image-text corpus to ask how far two automatic readers agree, with no annotated ground truth required — which is the situation most affective corpora are genuinely in. Substantively it speaks to generative tools in participatory settings: the Festival of the Mind installation turned a member of the public's typed feeling into a drawing in front of them, and it is worth knowing whether the output stands in any measurable relation to the input. My answer is a bounded yes — between two machine readers, strongest when a figure is drawn.
