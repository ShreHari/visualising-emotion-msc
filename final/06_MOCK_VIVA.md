# Mock viva — graded

27 questions an examiner is likely to ask, each with **a 2:1 answer**, why it only scores 60, and
**a distinction answer** written to be said out loud in 60-110 seconds. Then the follow-up.

**How to use this in the time you have.** Do not read it front to back. Read the *questions* first
and answer each out loud from memory. Only then read the distinction answer and see what you left
out. The gap between what you said and what is written is your revision list.

**The pattern every distinction answer follows:** give the number, concede the limitation *before*
being pushed, then bound the claim. Conceding first is what separates 80 from 60. A student who
volunteers the weakness reads as someone who understands their own work; a student who defends until
cornered reads as someone who does not.

---


# Statistics and inference

### Q. Your null is a random re-pairing of labels, three hundred times. Tell me what hypothesis that actually encodes — and why three hundred?

**A 2:1 answer (≈60%)** — "It's a chance baseline. I shuffle the image-side labels so that any agreement sitting above the null is above chance. Three hundred shuffles is enough for the mean to stabilise, and the observed rate is nowhere near it — 64.0 per cent against 45.6."

**Why it only scores 60** — it says "chance" without saying *whose* chance: the shuffle preserves both readers' skewed marginals, and that is the whole substantive point. It also defends three hundred on the stability of the mean when it is the standard deviation that carries the z.

**A distinction answer (≈80%)** — "It's a re-pairing null. I hold both label distributions fixed and shuffle which drawing goes with which prompt, three hundred times. So it encodes chance agreement *given the marginals* — GoEmotions' skew and BART-MNLI's skew are baked into the baseline, which is deliberate, because both readers are lopsided. Two limits I'll concede. Three hundred draws pins the null standard deviation only to a few per cent. And I shuffle records, not prompt groups, so with 249 repeats the null spread is too narrow. What I defend is the gap — 64.0 against 45.6 — not the exact z."

**If pushed further** — *"If the null is too narrow, every z in the thesis is inflated. By how much?"* — "I don't know the factor, and I won't guess it; what I did instead was re-do the one comparison I cared about with a clustered bootstrap and clustered permutation, which is why the face–scene difference carries an interval and the subset z's do not."

---

### Q. A z of plus eleven. What do you think that number means?

**A 2:1 answer (≈60%)** — "It means the result is highly significant — eleven standard deviations above the null mean, so p is far below 0.001. Emotional prompts agree at 64.0 per cent where chance re-pairing gives 45.6, and the same pattern holds for family agreement at 53.1 against 38.8."

**Why it only scores 60** — it converts a Monte Carlo distance into a normal-theory p-value it never computed, from a null estimated on only three hundred draws, and quotes significance where the examiner wants effect size.

**A distinction answer (≈80%)** — "It means the observed rate sits about eleven null standard deviations above the mean of three hundred shuffles. It does not mean a p-value with eleven digits. The standard deviation is itself estimated from three hundred draws, so eleven is really eleven give or take about half a point. And the shuffle ignores prompt clustering, which makes it optimistic rather than conservative. So I read z as ordering evidence between subsets, nothing finer. The numbers I'd defend are the eighteen-point gap, 64.0 against 45.6, and the clustered interval on the face–scene difference, plus 30.9 points, 22.6 to 40.6."

**If pushed further** — *"Then why report z at all?"* — "Because every subset needs a chance baseline on its own scale, and z is the compact way to say how far each sits above its own null; the confidence intervals carry the actual inference."

---

### Q. Two categorical readers, seven families, a thousand records. That is a textbook contingency table. Why is there no chi-square in this thesis, and no kappa either?

**A 2:1 answer (≈60%)** — "Chi-square tests independence, and I wanted agreement against chance rather than a test of association, so I used a shuffle null instead. It gives the same information in a form that suits the graded-similarity framing."

**Why it only scores 60** — it never names the assumption chi-square would actually violate here, and it asserts equivalence to a chance-corrected agreement statistic without having computed one.

**A distinction answer (≈80%)** — "Two reasons and one omission. Pearson's chi-square asks whether the two readers are independent. I already know they aren't, and I need how far above chance the agreement sits, not whether any association exists. It also assumes independent records, and 249 of the 1,012 repeat an earlier prompt, so the degrees of freedom would be wrong. The omission is Cohen's kappa. My shuffle null does the same job — it fixes both marginals and estimates the chance rate empirically — but kappa is the statistic you'd expect on the page, and I should have printed it alongside."

**If pushed further** — *"What would kappa have given you that the shuffle didn't?"* — "Comparability: my 53.1 per cent family agreement is chance-corrected only inside my own analysis, so nobody can put it next to another study's number."

---

### Q. How many z-scores are in this work? And how many corrections for multiplicity?

**A 2:1 answer (≈60%)** — "There are quite a few — four measures reported across the subsets. I didn't apply a correction, but the effects are so large that it wouldn't change any conclusion."

**Why it only scores 60** — "wouldn't change anything" is asserted rather than shown, no corrected threshold is named, and it quietly ignores the weakest results, which are exactly the ones a correction bites.

**A distinction answer (≈80%)** — "Four measures across six subsets, so on the order of twenty-four z-values, and no correction anywhere. That's a genuine fault and I'll take it. What I can do is say what a correction would do. Bonferroni at twenty-four puts the threshold near z of three point one. Plus 11.1, 10.3, 10.4, 5.8 and 4.9 all clear it comfortably. The distinct-prompt scene result at plus 3.5 clears it only barely, so I'd stop describing that one as solid. The face–scene difference has its own permutation test — one comparison — so it isn't affected."

**If pushed further** — *"Bonferroni assumes independent tests. Yours overlap heavily."* — "It does, which makes it conservative here, since the subsets nest and the four measures correlate; I'm treating it as a worst case, and the large z's survive the worst case."

---

### Q. Your non-emotional control returns 76.6 per cent against a null of 76.6 per cent. Explain to me how that could ever have come out any other way.

**A 2:1 answer (≈60%)** — "That's the specificity check. Where the prompt carries no emotion, the effect disappears — 76.6 against 76.6, z of plus 0.3 — which is what you'd want to see if the signal in the emotional subset is real."

**Why it only scores 60** — it presents as an empirical finding something the arithmetic forces. A subset that cannot produce a positive z is not evidence of anything.

**A distinction answer (≈80%)** — "It couldn't have, and I should say that before you ask. On those 405 records the prompt reader returns neutral for every one, so the prompt side is constant. Shuffling the image side just re-pairs identical prompts, so the null mean has to equal the observed value. Sign and family are worse than degenerate — they have no varying denominator at all. So plus 0.3 is arithmetic, not specificity. What it does establish is a sanity check on the code path. Real specificity needs a subset where the prompt labels vary and agreement still collapses. I did not run that."

**If pushed further** — *"So delete it from the thesis?"* — "No — keep it, relabel it a degeneracy check with the z suppressed, which the script already flags, and stop calling it a control."

---

### Q. Your scene interval runs from 33.3 to 51.1 per cent. That's eighteen points wide. What are you actually claiming about scenes?

**A 2:1 answer (≈60%)** — "That scene drawings agree much less than face drawings — 42.9 per cent against 73.9 on valence-sign — and that the difference is significant, with a permutation p of 0.0001 on both measures."

**Why it only scores 60** — it recites the point estimates and the p-value and never engages with the width. It doesn't say what an n of 205 can and cannot support.

**A distinction answer (≈80%)** — "Only that scene agreement is lower, and lower by a lot. The point estimate is 42.9 per cent, but the clustered interval runs 33.3 to 51.1 — eighteen points, because n is 205 and clustering on prompt groups costs me further precision. So I won't claim scenes sit at chance, and I won't rank two scene conditions against each other. The precision is in the difference: plus 30.9 points, 22.6 to 40.6, and plus 26.3 on family, 18.4 to 35.3. That difference is the claim. The scene rate alone is an estimate, not a measurement."

**If pushed further** — *"How many scene records would you need to halve that interval?"* — "Roughly four times as many, around eight hundred emotional scene records against my 205, and I ran no prospective power calculation because the corpus was fixed at 1,012 before any analysis began."

---

### Q. Is a permutation test even the right instrument here? You didn't randomise anything.

**A 2:1 answer (≈60%)** — "It's the right choice because it makes no distributional assumption and it respects the dependence — I shuffle the face/scene label across prompt groups rather than across records, ten thousand draws, and I get p equals 0.0001 on both valence-sign and family."

**Why it only scores 60** — the mechanics are right but the inference isn't bounded: a design-based test is being read as though the label had been assigned. And 0.0001 is quoted as a value when it is the floor of the resolution.

**A distinction answer (≈80%)** — "It's the right test for the question I asked and the wrong one for the question it looks like it answers. Nothing was randomised, so it tests exchangeability only — is the face/scene label swappable across prompt groups. It is not evidence that faces inherently produce more readable drawings. Two caveats. Zero of ten thousand draws reached the observed gap, so the honest statement is p below 0.0001, not equal to it. And the label comes from the same BLIP-VQA output that the description reader then reads, so significance cannot touch the partial circularity — it rules out sampling noise, nothing else."

**If pushed further** — *"Then what would break the circularity?"* — "Human coding of a sample of drawings for people-present and expression, then re-running the split on those labels; I did not do it, and it's the first thing I'd fix, because 414 of the 421 scene records are simply ones where the describer reported no people."

# Method and architecture

### Q. You had CLIP. CLIP puts images and text in one space in a single step. Instead you bolted a five-question describer onto a text classifier. Why did you add a failure point?

**A 2:1 answer (≈60%)** — "CLIP is trained on photographs and it does badly on line art. Our own comparison shows it: on 608 shared records, describe-then-extract gets 49.3% family agreement and direct CLIP gets 25.3%. That's nearly double. The describe route also gives us a readable intermediate sentence, so we can see why the model said what it said. So BLIP-VQA was the better choice on both counts."

**Why it only scores 60** — it sells that comparison as clean when it is not: the prompt side of the 49.3-vs-25.3 contrast uses BART-MNLI, not the GoEmotions reader used everywhere else in the thesis, so the two routes are not being held to the same standard.

**A distinction answer (≈80%)** — "Two reasons, one strong, one weaker. The strong one is interpretability. The intermediate sentence is the point where a human could inspect or intervene. The weaker one is the number. On 608 shared records describe-then-extract gives 49.3% family agreement, direct CLIP 25.3%. But that contrast is not clean. The prompt side there is BART-MNLI, not GoEmotions, so it is not the comparison I run elsewhere. And CLIP's negative skew on line art could be a prompt-template artefact I never tuned away. So: BLIP for interpretability, and 49.3 against 25.3 is supporting, not decisive."

**If pushed further** — *"So you cannot claim CLIP is the worse architecture?"* — "Correct. I can say it agreed less on this corpus with the templates I gave it; I did not tune those templates, so the claim stops at this setup."

---

### Q. Why five questions? Why not three? Why not fifteen? Where did the number five come from?

**A 2:1 answer (≈60%)** — "The five cover the main channels through which a drawing shows emotion — expression, action, posture, people, scene. Three would drop posture and scene, which matter for the drawings with no faces in them. Much more than five and the assembled sentence gets long and BART-MNLI starts losing the signal. Five was the balance, and it worked: 53.1% family agreement on the 607 emotional prompts against a 38.8% null."

**Why it only scores 60** — the claim that more questions would degrade the sentence is asserted, not shown; nothing was run that could distinguish five from three, so a design decision is being dressed up as an empirical finding.

**A distinction answer (≈80%)** — "Honestly, five was a design decision, not an empirical result. I picked expression, action, posture, people and scene because they cover both the face drawings and the ones with no people. I did not run three, or seven, or any other set, so I cannot tell you what the marginal question buys. What I can tell you is that one of the five dominates the structure: 414 of the 421 scene records, 98.3%, are records where the describer reported no people. So the people-count answer governs the split, and that much I can evidence."

**If pushed further** — *"If one question governs it, are the other four doing anything?"* — "I do not know — whether expression, action, posture and scene move the emotion read at all is precisely the ablation I did not run."

---

### Q. You have a five-part instrument and you never removed a part. That is a day of compute. Why is there no ablation in this thesis?

**A 2:1 answer (≈60%)** — "It came down to time. The pipeline was finalised late and the significance work took priority — the clustered bootstrap and permutation test were only computed on the 4th of September. The ablation is flagged in future work. The five questions were fixed in advance, so there was no configuration search to declare, and the headline numbers stand on their own."

**Why it only scores 60** — "no time" is honest but it answers a different question; and "the numbers stand on their own" dodges the real cost, which is that a reader cannot tell whether this is a five-question result or a one-question result.

**A distinction answer (≈80%)** — "I did not run it, and it is the biggest hole in the method chapter. It was a scheduling failure — the clustered significance work landed on the 4th, the ablation did not. What it would have told me is whether the face-scene difference survives dropping a question. I can bound what I do have: that difference is +30.9 points on valence-sign, interval +22.6 to +40.6, clustered permutation p equals 0.0001. So it is robust to resampling prompt groups. It is not robust to a question I never removed. Those are different claims, and I only make the first."

**If pushed further** — *"Which question would you drop first?"* — "People-count, because it is the one I can show governs the split — 414 of 421 — so removing it is the sharpest test of whether the rest of the instrument does any work."

---

### Q. Ekman's basic emotions have been under sustained attack for twenty years. Barrett is not a fringe position. Why is your entire label space a theory the field is still arguing about?

**A 2:1 answer (≈60%)** — "Six basic emotions plus neutral is the standard taxonomy in affective computing, so it makes the work comparable to prior studies. GoEmotions has 27 labels, which is far too fine for 1,012 records — you get sparse cells everywhere. Collapsing to seven families gives usable counts per family and lets both readers speak the same language. It is a pragmatic, conventional choice."

**Why it only scores 60** — "it is what the field uses" is an appeal to convention that never engages the critique, and it treats the taxonomy as neutral plumbing in a project whose whole premise is that emotion labels are contested.

**A distinction answer (≈80%)** — "It is a compromise, and I will defend it as one, not as a commitment to basic emotion theory. Seven families are a shared register both readers can be mapped into; GoEmotions' 27 labels are too sparse across 1,012 records. And the study's own logic cuts against reifying them — everything is graded similarity referenced to chance, precisely because there is no ground truth and people disagree. That is nearer Barrett than Ekman. But the label space is Ekman's, so every family-level number inherits that theory. That is why I report valence-sign alongside family throughout."

**If pushed further** — *"Would the result survive a different taxonomy?"* — "I ran one taxonomy, so I cannot say; that valence-sign and family move together — 73.9 and 61.9 on faces, 42.9 and 35.6 on scenes — is suggestive that the effect is not purely an artefact of the seven-way carve-up, but it is not a test of it."

---

### Q. You use two different readers — GoEmotions on the prompt, BART-MNLI on the description. Why not the same model on both sides? Are you not simply measuring two classifiers disagreeing with each other?

**A 2:1 answer (≈60%)** — "Each side gets the appropriate model. GoEmotions is trained on short first-person text, which is exactly what the self-reports are. BART-MNLI is zero-shot, which suits the description side because those assembled sentences are third-person and factual — out of distribution for any trained emotion classifier. Both outputs map into the same seven families, so the comparison is like for like."

**Why it only scores 60** — "like for like" is the over-claim: the mapping equalises the output space, not the readers' biases, and the student has not conceded that a shared prior on either side would inflate the agreement figure.

**A distinction answer (≈80%)** — "Yes — every number here is agreement between two automatic readers, and neither is validated against human coding. I say that plainly. The reason they differ is fit: GoEmotions is trained on short first-person text, which the reports are; BART-MNLI is zero-shot, which the assembled description needs, because a third-person factual sentence is out of distribution for a trained classifier. Different readers at least means their errors are not identical by construction. What I lack is a human-coded subset to anchor either. So the claim is: two automatic readers agree above chance, 53.1% against 38.8%. Not that either is right."

**If pushed further** — *"Two readers can be wrong the same way."* — "They can, and I have one direct sign of it: the describer reports a happy or smiling expression for 57% of the faces it can read, so if the prompts skew positive too, part of that 64.0% valence-sign agreement is a shared prior rather than a shared reading."

---

### Q. The valence-arousal coordinates. Did you fit those, or did you make them up?

**A 2:1 answer (≈60%)** — "They are set from standard circumplex positions — each of the seven families sits at conventional valence and arousal coordinates, and the measure scores the distance between the two readers' points. It is graded rather than right-or-wrong, which fits the similarity framing. There is a mathematical floor at 41 and random pairings average 76, so the scale has a proper reference point."

**Why it only scores 60** — it calls the coordinates "standard" without a source, and it quotes the 76 baseline without noticing what that baseline does to the measure: there is almost no headroom above chance left.

**A distinction answer (≈80%)** — "I placed them by hand, from circumplex convention. They were not fitted to the data and not checked by raters, so they are an assumption, not a measurement. The consequence shows up in the numbers: the floor is 41 and random pairings already average 76. That is very little room above chance. It is also why the non-emotional control comes out at 76.6 against a 76.6 null, z plus 0.3. So I treat valence-arousal as the weakest of the four measures and I hang no claim on it. Valence-sign and family carry the argument."

**If pushed further** — *"Then why report it at all?"* — "Because it is the only one of the four that is computable on the non-emotional subset — sign and family are degenerate there by definition — so it is what makes the specificity check possible at all."

---

### Q. Three hundred shuffles. Why three hundred? And your test suite is 29 smoke assertions with not one number in it. Why should I believe any figure in this thesis is reproducible?

**A 2:1 answer (≈60%)** — "300 gives a stable null — the null distribution settles well before that, and the z-scores are large enough, plus 11.1 on valence-sign, that more shuffles would not change a single conclusion. The pipeline is seeded and the scripts are in the repository, so anyone can rerun it end to end. The tests confirm the pipeline runs, which is what smoke tests are for."

**Why it only scores 60** — the claim that the null distribution settles is asserted with no convergence check, and "the tests confirm it runs" concedes the examiner's actual point: nothing in the suite would catch a number silently changing.

**A distinction answer (≈80%)** — "Both criticisms land. 300 was chosen for compute, not from a convergence check I can show you. And the suite is 29 smoke assertions — not one pins a numeric result, so a refactor could move 53.1 to 50 and the tests would still pass. What I did do is stop leaning on the shuffle null for the headline. The significance script runs a clustered bootstrap and a clustered permutation, resampling prompt groups rather than records, because 249 of the 1,012 records repeat an earlier prompt. That gives face minus scene at +30.9, interval +22.6 to +40.6, p equals 0.0001. That is the number I defend."

**If pushed further** — *"What is the first thing you would add?"* — "A regression test asserting the face and scene valence-sign figures to one decimal, 73.9 and 42.9, on the fixed seed, so any pipeline change has to declare itself."

---

Relevant file, if the examiner asks where the clustered bootstrap and permutation test live: `/Users/shrehari/Desktop/FINAL YR DISSERTATION/emoviz/significance.py`

# Limitations and validity

### Q. Your headline is that face drawings agree better than scene drawings. But you cut the face/scene split out of the describer's own output, and then fed that same output to the emotion reader. What stops the whole finding being an artefact of the split?

**A 2:1 answer (≈60%)** — "The split is a content variable, it isn't part of the emotion reading. Face records reach 73.9% valence-sign agreement against a 53.5% null, scene records 42.9% against 29.6%. Both clear chance comfortably. And the clustered bootstrap puts the difference at +30.9%, permutation p = 0.0001, so the gap is real and not sampling noise."

**Why it only scores 60** — it treats the split as an independent variable when it is a downstream product of the same BLIP-VQA pass, so the significance test is computed *inside* the circularity and cannot rescue it.

**A distinction answer (≈80%)** — "It is partly circular and I say so before you push. The split comes from the same BLIP-VQA pass the emotion reader then reads. What actually drives it is one answer, the people-count: 414 of the 421 scene records, 98.3%, are ones where the describer reported no people. So face versus scene is really people versus no-people as the describer sees it. The numbers themselves hold — 73.9% against a 53.5% null, 42.9% against 29.6%, difference +30.9%, CI +22.6 to +40.6, p = 0.0001. But that licenses a claim about describer-reported content, not about human-visible content."

**If pushed further** — *"So what would break the circularity?"* Hand-code a subset for people-present and re-run the split on the human labels; I did not do that, so face-versus-scene stays an internal variable of the describer.

---

### Q. Walk me through what your image side actually measures. Because as far as I can see, BART-MNLI is reading BLIP-VQA, and nobody at any point is reading the drawing.

**A 2:1 answer (≈60%)** — "BLIP-VQA is a well-established visual question answering model and the five questions are deliberately factual — expression, action, posture, people, scene — so the sentence stays neutral and the emotion reading comes from the content of the drawing. Family agreement is 53.1% on the 607 emotional prompts against a 38.8% null, z +10.3."

**Why it only scores 60** — it silently substitutes the describer's text for the image, and "well-established" is a claim about photographs, not about monochrome line art, which is the domain in question.

**A distinction answer (≈80%)** — "You are right, and it is the structural weakness of the design. Every image-side number is a reading of BLIP-VQA's text, never of the drawing, and never checked against human coding. So the honest statement is that a description reader and a prompt reader agree well above chance — 53.1% family against 38.8%, z +10.3, and 64.0% valence-sign against 45.6%. That is agreement between two automatic readers in series. It bounds nothing about what a person would read off the drawing. I also ran no ablation of the five questions, so I cannot tell you which one carries the agreement."

**If pushed further** — *"Then why insert a describer at all rather than read the image directly?"* Because the direct route is worse here — describe-then-extract gets 49.3% family agreement on the 608 shared records against direct-CLIP's 25.3% — though that only ranks two automatic readers, it validates neither.

---

### Q. Three hundred and thirty-two of your four hundred and twenty-one scene records report a smile in a picture the same model says contains no people. Why is anything downstream of that salvageable?

**A 2:1 answer (≈60%)** — "That's a known forced-choice behaviour in VQA models — they answer the question rather than decline it. It adds noise, and you can see the noise landing where you'd expect: the scene condition is the weakest, 42.9% against a 29.6% null, z +5.8, well below the face condition. So the effect degrades gracefully."

**Why it only scores 60** — "adds noise" is the wrong frame. A default word is a systematic bias, and it may be *producing* the face/scene gap rather than merely degrading one side of it.

**A distinction answer (≈80%)** — "It is a forced-choice artefact and it is the worst thing in the project. The describer emits an expression word whether or not it reports a person: 406 of the 414 no-people scene records still carry one, and 332 of the 421 say smile, smiling or happy. So the scene condition's 42.9% against a 29.6% null is partly agreement with a default word rather than with the drawing. I would report scene as a floor on describer noise, not as a content result. And the face/scene difference is then partly a difference in describer reliability, not only in visual content."

**If pushed further** — *"Is the face condition contaminated the same way?"* Very likely in the same direction — the describer calls 57% of the faces it can read happy or smiling — and I never separated a positive describer default from a genuinely positive corpus.

---

### Q. Your specificity check. n = 405, z +0.3. Tell me why that counts as a control.

**A 2:1 answer (≈60%)** — "Those are the prompts the emotion reader classified as non-emotional. If the pipeline manufactured agreement out of nothing, it would show up there too, and it doesn't: valence-arousal is 76.6% against a 76.6% null, z +0.3. Flat. That is the specificity evidence — the effect appears only where there is emotion in the prompt."

**Why it only scores 60** — the set's membership is one classifier's own top-1 output, never checked, and the answer also fails to say that two of the three metrics are degenerate there, so the whole check rests on a single measure.

**A distinction answer (≈80%)** — "It is a weak control and I would not lean on it. Membership is GoEmotions' own top-1 label, never human-checked, and on inspection at least 15% contains an explicit emotion word — ecstatic, content, hopeful. So it is not a clean neutral set. Second, only one metric can speak there: sign and family are degenerate on that subset by its own definition, so the check rests entirely on valence-arousal, 76.6% against a 76.6% null, z +0.3. I read that as no evidence of a spurious effect on a contaminated set with one metric. I do not read it as demonstrated specificity."

**If pushed further** — *"What would a real control have been?"* Hand-screened neutral prompts, or the same prompts with the emotion word stripped and the scene kept, through an identical pipeline — I did neither.

---

### Q. There is not one human judgement anywhere in this thesis. Why should we award a degree for two models agreeing with each other?

**A 2:1 answer (≈60%)** — "Human coding of 1,012 drawings wasn't feasible in a summer project, and the design compensates by referencing every measure to chance: a 300-shuffle random-pairing null throughout, plus a clustered bootstrap and a permutation test at p = 0.0001. The agreement is far above chance on every emotional subset, so it isn't an artefact of the metric."

**Why it only scores 60** — it answers a validity question with a chance question. Nulls show the agreement is not random; they say nothing about whether either reader is right. And it leads with scope rather than with what was established.

**A distinction answer (≈80%)** — "I have no human validation, and no null substitutes for it. Nulls rule out chance, not error. What I established is this: face 73.9% against a 53.5% null, family 61.9% against 45.8%, clustered CIs excluding zero, permutation p = 0.0001, and a face-scene difference of +30.9%, +22.6 to +40.6, stable when I resample prompt groups rather than records — which matters, because 249 of the 1,012 repeat an earlier prompt. So: the two readers agree far more than random pairing allows. Whether either agrees with a person is untested, and that is the next study."

**If pushed further** — *"Design it for me."* A stratified hand-coded subset with more than one coder, reporting human-human agreement first as the ceiling, then each reader against the humans — so a model-model number finally has something to be compared to.

---

### Q. You report your method beating CLIP, 49.3 to 25.3. What does that comparison actually establish?

**A 2:1 answer (≈60%)** — "That describe-then-extract is the better route for this material. CLIP is trained on photographs and skews negative on sparse monochrome line art, whereas going through a neutral factual sentence first avoids that. Nearly double the family agreement on the 608 shared records — 49.3% against 25.3%."

**Why it only scores 60** — "better" quietly promotes the prompt-side label to truth, and the answer omits the confound: the prompt side in that comparison is BART-MNLI, not the GoEmotions reader used for every other number in the thesis.

**A distinction answer (≈80%)** — "It ranks two image readers against a third model's labels, and no more than that. On the 608 shared records the description route gets 49.3% family agreement, direct CLIP 25.3%. Two things I have to flag. The prompt side there is held constant with BART-MNLI, not the GoEmotions reader used elsewhere, so it does not sit alongside my headline numbers. And 'better' means only 'closer to a third automatic reader' — if that reader is biased, the ranking inherits the bias. CLIP skewing negative on line art is consistent with what I saw, but I did not test it directly."

**If pushed further** — *"Could both your readers be wrong in the same direction and you would never see it?"* Yes — shared training-data bias is completely invisible to this design, and only human coding would surface it.

---

### Q. Last one. Give me the bound. What does a reader get to conclude from this, and what would be over-claiming?

**A 2:1 answer (≈60%)** — "That an automatic image-emotion reader agrees with prompt-derived labels well above chance, most strongly for drawings containing faces, and that repeated prompts get read consistently — 68.8% against a 59.1% null. It's a working similarity framework for AI-generated line art, in line with the supervisor's framing of similarity rather than matching."

**Why it only scores 60** — that is a summary, not a bound. "Drawings containing faces" restates the circular split as though it were a validated content finding, and the answer never names a single thing the study cannot support.

**A distinction answer (≈80%)** — "What it licenses: on this corpus, two automatic readers agree above a random-pairing null — 64.0% valence-sign against 45.6% on the 607 emotional prompts — and agreement is higher where the describer reports people, 73.9% against 53.5%, difference +30.9%, p = 0.0001. Repeated prompts get the same reading 68.8% of the time against a 59.1% permutation null. What it does not license: anything about human reading, anything about colour — the corpus is monochrome with no colour condition — and any positive-versus-negative direction claim, which I withdrew because the nulls went degenerate and the readers disagreed."

**If pushed further** — *"And your test suite stands behind those numbers?"* No — it is 29 smoke assertions and not one of them asserts a numeric result, so reproducibility rests on re-running the scripts, not on the tests.

# Contribution and positioning

### Q. Strip the framing away for a moment. You downloaded BLIP-VQA, BART-MNLI and GoEmotions and reported some percentages. Where exactly is the research contribution?

**A 2:1 answer (≈60%)** — "The novelty is the pipeline. Nobody has combined BLIP-VQA, BART-MNLI and GoEmotions on AI-generated monochrome line drawings before, and the results are strongly significant — 64.0% valence-sign agreement against a 45.6% null, z+11.1. So it's a new combination of tools applied to a new dataset, and the face-versus-scene difference is a genuine finding on top of that."

**Why it only scores 60** — it locates the contribution in the choice of models, which is the one part that genuinely is off the shelf, and states the face/scene difference without the circularity that governs it.

**A distinction answer (≈80%)** — "Agreed, the components are off the shelf. The contribution is the measurement design. Every number sits against a matched null: 64.0% against 45.6% from 300 shuffled pairings. The null is clustered on prompt groups, because 249 of 1,012 records repeat an earlier prompt. And the split by visual content is the finding — face 73.9%, scene 42.9%, difference +30.9%, interval +22.6 to +40.6, p = 0.0001. I should say the split is partly circular; it comes from the same describer. So the claim is bounded: excess agreement between two automatic readers, on this corpus."

**If pushed further** — *"So your contribution is a null model?"* — "It is a null-referenced, group-clustered comparison rather than a raw score: the face–scene gap of +30.9% survives resampling whole prompt groups at p = 0.0001, whereas the bare 64.0% I would not defend on its own.

---

### Q. TIFA and VQAScore already decompose an image into questions and score it against the text. What have you added beyond re-running TIFA with an emotion label on the end?

**A 2:1 answer (≈60%)** — "TIFA and VQAScore check whether the image contains what the prompt asked for. Mine reads emotion instead, which is a harder problem because emotion is subjective. And I show the describe-then-extract route works better than reading the image directly — 49.3% family agreement against 25.3% for CLIP, which is close to my headline 53.1%."

**Why it only scores 60** — it puts 49.3% next to the headline 53.1% as though they were the same measurement; the CLIP comparison holds the prompt side at BART-MNLI, so that number is internal to the comparison and cannot be read across.

**A distinction answer (≈80%)** — "They score whether stated content is present. That is a checkable fact with a right answer. I have none: the prompt is a free-text self-report of feeling. So my five questions stay factual, the emotion reading happens one step later on the sentence, and the score is graded against chance rather than marked correct. I did not run TIFA or VQAScore as a baseline — that is a gap. What I ran was direct CLIP: 49.3% family against 25.3% on 608 shared records, with the prompt side held at BART-MNLI, so that figure lives inside that comparison only."

**If pushed further** — *"Your first question asks about facial expression. Is that not already an emotion question?"* — "It is the closest to one and it dominates — the describer reports a happy or smiling expression for 57% of the faces it can read — and I did not run the five-question ablation, so I cannot yet say how much of the agreement rests on that single answer."

---

### Q. EmoGen and EmotiCrafter condition generation on emotion and evaluate the result. You generated nothing. Is your work not simply their evaluation step, minus the interesting half?

**A 2:1 answer (≈60%)** — "They generate emotional images, I evaluate images that already exist, so it's a different task. They also work in colour, whereas my corpus is monochrome line art, which is much harder for an emotion reader and makes my result more impressive at 53.1% against a 38.8% null."

**Why it only scores 60** — "harder" is asserted with nothing behind it; no colour-control condition was run, so no comparative colour claim is available at all.

**A distinction answer (≈80%)** — "Those systems condition generation on a label the researcher picks, then evaluate with classifiers trained on colour photographs and paintings. Nothing in my corpus is label-conditioned. It is 1,012 public self-reports, free text, mixed affect, rendered as monochrome line drawings. No researcher-chosen label, no colour channel. I make no colour claim, because I ran no colour-control condition — monochrome is a property of the corpus, not a manipulated variable. What I can say is that on this material excess agreement is real but modest: family 53.1% against 38.8%, z+10.3, falling to 35.6% where the describer reports no people."

**If pushed further** — *"Then your thesis says nothing about generation at all."* — "Almost nothing: the one generation-side result is the repeated prompts, where the image reader returns the same family for 68.8% of drawings within a prompt group against a 59.1% permutation null, z+4.9."

---

### Q. Two automatic models agreeing with each other tells me nothing about human beings. Why is this question worth asking?

**A 2:1 answer (≈60%)** — "It matters because generative image tools are being used in public engagement settings like the Festival of the Mind, and we should know whether the emotion someone reported survives into the picture they were given. My results show it partly does — 53.1% family agreement against a 38.8% null, well above chance."

**Why it only scores 60** — it slides from agreement between two automatic readers to a claim about what survives into the picture, and there is no human validation anywhere in the work to license that step.

**A distinction answer (≈80%)** — "Fair. There is no human validation, so I cannot say these readings resemble how a person would read the drawing. The claim is about the instrument, not the drawings. Automatic emotion readers are increasingly used to evaluate generative systems, and mine shows the reader is not uniform: 73.9% excess agreement on face-classified records, 42.9% on scene, and flat on the non-emotional control — 76.6% against a 76.6% null, z+0.3. That control is itself weak. It came from a classifier's own top-1 and at least 15% of it contains an explicit emotion word."

**If pushed further** — *"If the control is that contaminated, what does the specificity check actually buy you?"* — "Only a negative: the pipeline does not manufacture excess agreement on prompts it should read as flat, which rules out a trivial artefact but licenses nothing positive."

---

### Q. "Similarity, not matching" is a convenient thing to say when your numbers are in the fifties. Convince me it is a methodological position and not a hedge.

**A 2:1 answer (≈60%)** — "Emotion is subjective, there's no ground truth and humans disagree with each other, so grading similarity against chance is more honest than scoring right or wrong. That's my supervisor's framing, and the nulls support it — 53.1% against 38.8% is a real excess even though 53% sounds low."

**Why it only scores 60** — it recites the framing as a belief rather than demonstrating that it constrains anything; no instance is given where the framing cost a result rather than rescued one.

**A fair challenge, and the test is whether the framing can cost me something. It does. The valence-arousal measure has a mathematical floor of 41 and random pairings average 76, so the 76.6% on the non-emotional set is chance and I report it as chance, not as a strong score. And I withdrew the positive-versus-negative direction claim entirely — degenerate nulls, and the two readers disagreed. Grading against chance is not a lower bar than right-or-wrong. On this data it removed two results I would otherwise have been able to report."** *(distinction answer, ≈80%)*

**If pushed further** — *"Name a result the framing let you keep that a stricter test would have killed."* — "None I would defend on those grounds: family agreement at 53.1% is the weakest survivor, and it survives because 38.8% is the honest chance level, not because a threshold moved."

---

### Q. Another six months and a working supervisor. What do you do first — and do not say "more data".

**A 2:1 answer (≈60%)** — "I'd add human validation, run the pipeline on more images, try newer or sketch-trained describers as my supervisor suggested, and possibly extend it to colour images so I could compare line art against photographs."

**Why it only scores 60** — it is an unordered wish list; nothing states which specific defect in the current work each item repairs, so it reads as scope rather than diagnosis.

**A distinction answer (≈80%)** — "Human coding first. A stratified sample across face and scene, several coders, emotion family. That is the load-bearing gap — every image-side number is a reading of the describer's output that no person has checked. Second, break the circularity in the split, because it is really the people-count answer: 414 of 421 scene records report no people, and 332 of those still answer smile, smiling or happy. That needs detection outside the describer. Third, the five-question ablation, which I did not run, and numeric assertions in the test suite — it is 29 smoke assertions and none pins a result."

**If pushed further** — *"Suppose the human coders agree with your describer only 40% of the time. Is the thesis dead?"* — "The agreement percentages become uninterpretable, but the comparative structure stands or falls on its own terms — I would then report the face–scene gap as a property of the describer rather than of the drawings, which is closer to what I can actually defend."


---

# The three sentences to have word-perfect

**Contribution.**
> My contribution is not a new emotion classifier. It is a reproducible methodology for evaluating
> emotional agreement between prompts and AI-generated monochrome drawings, using graded similarity
> against a random-pairing baseline, in a setting where no human ground truth exists.

**Biggest limitation.**
> This measures agreement between two automatic readers, not human perception, because the dataset
> carries no human emotion annotations.

**Strongest finding.**
> Agreement is consistently above the random-pairing baseline, it is significantly stronger for
> drawings the describer classifies as containing a person - plus 30.9 points, confidence interval
> 22.6 to 40.6, permutation p of 0.0001 - and prompts classified as non-emotional fall back to the
> baseline.

# If your mind goes blank

Say: *"Let me give you the number first."* Then the number. Then the caveat. That sequence works for
almost every question in this document, and it buys you three seconds to think.

# What not to do

Do not bluff a statistic. If you did not test it, say so and immediately say what you *did* establish
instead. Every distinction answer above does exactly that, and it is why they score 80.
