# Addendum — the face/scene difference is statistically significant

Computed 4 September 2026 by `emoviz/significance.py`. This closes the one inferential gap in the
analysis: every subset was previously reported against its own random-pairing null, but the face and
scene rates had never been tested **against each other**.

## Results

| | face-classified | scene-classified | difference |
|---|---|---|---|
| **Valence-sign agreement** | 73.9%  [68.2, 79.2] | 42.9%  [33.3, 51.1] | **+30.9%  [+22.6, +40.6]** |
| **Emotion-family agreement** | 61.9%  [55.7, 68.0] | 35.6%  [26.7, 44.1] | **+26.3%  [+18.4, +35.3]** |

95% confidence intervals from a clustered bootstrap, 10,000 draws.
Clustered permutation test, 10,000 draws: **p = 0.0001** for both metrics.

`inference.py` (9 September), which resamples each subset within itself rather than splitting inside each draw, gives [68.3, 79.2] and [33.1, 51.1] for valence sign and [55.8, 68.1] and [26.4, 44.1] for family — the same intervals to within 0.3 points. Cohen's kappa for family agreement: face 0.30 [0.23, 0.37], scene 0.13 [0.06, 0.19].

## Why the resampling is clustered

249 of the 1,012 analysed records repeat an earlier prompt, so records are **not independent**. Both
procedures therefore resample and shuffle whole **prompt groups**, never individual records.
Resampling records would have understated the uncertainty and inflated significance.

## What this settles, and what it does not

**Settles:** the gap between face-classified and scene-classified drawings is not sampling noise.
Neither confidence interval for the difference comes close to zero.

**Does not settle:** the partial circularity. The face/scene split is derived from the same BLIP-VQA
output whose description the image reader then reads. A significant difference shows the two groups
differ; it does not show that faces inherently carry more emotional signal. That distinction must be
stated whenever the result is quoted.

Note also what actually drives the split: 414 of the 421 scene-classified records (98.3%) are ones
where the describer reported **no people present** — and 406 of those *do* contain an expression
word. The split is governed by the people-count answer, not by absent expression content.

## The sentence to use

> The difference is statistically significant — a clustered permutation test gives p = 0.0001, and the
> 95% confidence interval on the difference is +22.6 to +40.6 percentage points for valence-sign
> agreement. I clustered on prompt identity because 249 records repeat an earlier prompt. What that
> establishes is that the gap is not noise; it does not remove the circularity, because the split
> comes from the same describer output the emotion reader reads.

## Replaces

Wherever the documents or the deck said *"no formal significance test of the face–scene difference has
been run"*, that is superseded. The deck was presented on 4 September with the spoken correction; the
project documents have since been updated (9 September). The circularity caveat still stands.
