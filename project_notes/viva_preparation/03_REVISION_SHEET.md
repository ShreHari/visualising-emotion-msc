# Revision sheet - read this in the ten minutes before you present

## The project in three sentences
Members of the public at Festival of the Mind 2024 typed how they were feeling, and DALL-E drew each entry as a monochrome line drawing - 1,025 records, contributors unknown. I built a pipeline that reads an emotion from the drawing and an emotion from the words, then measures how **similar** the two readings are - graded, never right-or-wrong. Every figure is reported against its own random-pairing null, with a clustered 95% interval.

## Research question - say it exactly
> To what extent does an automatic image-emotion reader **agree** with prompt-derived emotion labels for AI-generated monochrome drawings, and how does that agreement vary by visual content and by repeated prompts?

## The contribution - this is the line to land
The field reports **one-to-one accuracy**. I report **graded, chance-referenced similarity**. Emotion is subjective, there is no ground truth, humans disagree and models are noisy - so "does it match, right or wrong" is too simplistic. "Happy" and "excited" should count as close.

## Architecture - three stages
1. **Describe** - BLIP-VQA answers five factual questions (expression, action, posture, people, scene) into one neutral sentence. Never asked for an emotion.
2. **Read** - BART-MNLI zero-shot reads a feeling from that sentence; GoEmotions reads the prompt. Both land in the same seven families.
3. **Compare** - four measures, each against a 300-shuffle null.

## The four measures
valence-arousal distance - valence-sign agreement - emotion-family agreement - top-3 overlap.
**The null:** shuffle the images against the prompts 300 times; that is chance.

## Numbers worth memorising
| | value | null |
|---|---|---|
| Emotional prompts, valence-sign | **64.0%** | 45.6% (z+11.1) |
| Face-classified, valence-sign | **73.9%** | 53.5% (z+10.4) |
| Scene-classified, valence-sign | **42.9%** | 29.6% (z+5.8) |
| Non-emotional (specificity) | 76.6% | 76.6% (z+0.3) |
| Same prompt, same emotion | **68.8%** | 59.4% (z+4.5) |
| Describe-then-extract vs CLIP (like for like, family) | **53.0%** | vs 22.4% (+30.6 pp, p < 0.0001) |
| Face minus scene, valence-sign | **+30.9 pp** | CI +22.6 to +40.6, p = 0.0001 |
| Scene, people-aware template (ablation) | **4.7%** | 3.4% (z+1.6) — at chance |
| Expression sentence removed, family | **20.3%** | from 53.0% — the reading rests on one word |
| Valence-arousal metric | floor **41** | random pairs **76** |

Dataset: 1,025 collected - 13 pre-festival tests - **1,012 analysed**; 607 emotional / 405 labelled neutral; 591 face / 421 scene; 763 distinct prompts; 87 drawn more than once.

## Keywords to drop naturally
BLIP-VQA - zero-shot NLI - GoEmotions - Ekman families - describe-then-extract - random-pairing null - z-score - valence-sign agreement - specificity check - permutation null - out-of-distribution.

## Three sentences to say carefully
1. "This measures **agreement between two automatic readers**. It does not establish what a human perceives."
2. "The face/scene split is **produced by the same describer** whose output the emotion reader reads, so it is partly circular. The gap itself is significant - clustered permutation p = 0.0001, +22.6 to +40.6 points - but that does not remove the circularity. Describe the no-person drawings honestly and this reader finds nothing above chance in them: faces, and only faces."
3. "I make **no claim about colour**: the corpus is monochrome, but there is no colour-control condition."

## Conclusion
Prompt-reader and image-reader agreement is well above chance where the describer reports a face, and at chance where it reports none once the template stops inventing an expression; across repeated prompts the reader returns the same family for 68.8% of drawings in a group against 59.4% by chance - more consistent than chance but far from fixed. The contribution is the chance-referenced similarity measure, not a new classifier.

## Two-minute verbal recap - if asked "tell me about your project"
"At a science festival members of the public typed how they were feeling, and an AI drew each one as a black-and-white line drawing. My question is whether the emotion in the drawing agrees with the emotion in the words.

The hard part is that there is no correct answer - emotion is subjective, people disagree, models are noisy. So rather than scoring it right or wrong, I measure how *similar* the two readings are, on a four-level scale over emotion families, so that happy and excited count as close.

The pipeline never asks the image model what emotion it sees, because those models are trained on colour photographs and are good at objects, not feelings. Instead it asks five factual questions - expression, action, posture, how many people, what's in the picture - assembles the answers into a sentence, and a separate language model reads the feeling out of that sentence. The words go through a third model into the same seven families. Now both sides are text, and I compare text to text.

Everything is measured against chance: I shuffle the drawings against the prompts three hundred times to see what random pairing gives. Agreement is well above chance - sixty-four per cent on valence sign against a forty-six per cent null. It's much stronger when the drawing contains a person, seventy-four per cent, than when it's a scene, forty-three.

Two things I found that I didn't expect. The similarity scale doesn't start at zero - random pairs already score seventy-six - so a seventy-one looks like a pass and is actually below chance. And the same words do not reliably give the same reading: across repeated prompts the reader returns the same emotion for sixty-nine per cent of drawings in a group, against fifty-nine by chance.

What I can't claim is what a human sees. Both my readers are automatic and they disagree with each other. Human validation is the next study."
