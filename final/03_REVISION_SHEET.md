# Revision sheet - read this in the ten minutes before you present

## The project in three sentences
About a thousand members of the public at Festival of the Mind 2024 typed how they were feeling, and DALL-E drew each entry as a monochrome line drawing. I built a pipeline that reads an emotion from the drawing and an emotion from the words, then measures how **similar** the two readings are - graded, never right-or-wrong. Every figure is reported against a random-pairing baseline, so a result counts only insofar as it beats chance.

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
| Same prompt, same emotion | **68.8%** | 59.1% (z+4.9) |
| Describe-then-extract vs CLIP | **49.3%** | vs 25.3% |
| Valence-arousal metric | floor **41** | random pairs **76** |

Dataset: 1,025 collected - 13 pre-festival tests - **1,012 analysed**; 607 emotional / 405 not; 591 face / 421 scene; 763 distinct prompts; 87 drawn more than once.

## Keywords to drop naturally
BLIP-VQA - zero-shot NLI - GoEmotions - Ekman families - describe-then-extract - random-pairing null - z-score - valence-sign agreement - specificity check - permutation null - out-of-distribution.

## Three sentences to say carefully
1. "This measures **agreement between two automatic readers**. It does not establish what a human perceives."
2. "The face/scene split is **produced by the same describer** whose output the emotion reader reads, so it is partly circular - and no formal significance test of the gap has been run."
3. "I make **no claim about colour**: the corpus is monochrome, but there is no colour-control condition."

## Conclusion
Prompt-reader and image-reader agreement is well above chance and substantially stronger for drawings containing a person; the generator is not stable in what emotion it conveys for the same words. The contribution is the chance-referenced similarity measure, not a new classifier.

## Two-minute verbal recap - if asked "tell me about your project"
"At a science festival about a thousand people typed how they were feeling, and an AI drew each one as a black-and-white line drawing. My question is whether the emotion in the drawing agrees with the emotion in the words.

The hard part is that there is no correct answer - emotion is subjective, people disagree, models are noisy. So rather than scoring it right or wrong, I measure how *similar* the two readings are, on a four-level scale over emotion families, so that happy and excited count as close.

The pipeline never asks the image model what emotion it sees, because those models are trained on colour photographs and are good at objects, not feelings. Instead it asks five factual questions - expression, action, posture, how many people, what's in the picture - assembles the answers into a sentence, and a separate language model reads the feeling out of that sentence. The words go through a third model into the same seven families. Now both sides are text, and I compare text to text.

Everything is measured against chance: I shuffle the drawings against the prompts three hundred times to see what random pairing gives. Agreement is well above chance - sixty-four per cent on valence sign against a forty-six per cent null. It's much stronger when the drawing contains a person, seventy-four per cent, than when it's a scene, forty-three.

Two things I found that I didn't expect. The similarity scale doesn't start at zero - random pairs already score seventy-six - so a seventy-one looks like a pass and is actually below chance. And the generator is inconsistent with itself: give it the same words again and the same emotion comes back only sixty-nine per cent of the time.

What I can't claim is what a human sees. Both my readers are automatic and they disagree with each other. Human validation is the next study."
