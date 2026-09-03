> **SUPERSEDED (15 Aug 2026).** Direct-CLIP-era analysis. The κ/matching framing and the positive-collapse direction claim were retracted after the describe→extract reader disagreed in the opposite direction (reader bias, see RESULTS_final.md — only the human study can adjudicate). Kept for the project history / methods chapter.

# Similarity Analysis v1 (reframe of existing results)

On 608 emotional paired records. Each metric vs a random-pairing null (N=300).
Framing: **how similar** the image emotion is to the prompt emotion — not right/wrong.

| Metric | True pairs | Random pairs | Gap | z |
|---|--:|--:|--:|--:|
| Valence-Arousal similarity (headline) | 70.0% | 65.1% | +4.9% | 9.6 |
| Valence-sign agreement | 28.3% | 18.3% | +10.0% | 9.1 |
| Ekman family EXACT match (old metric) | 21.5% | 12.8% | +8.8% | 10.2 |
| Text emotion in image top-3 (soft) | 41.0% | 29.6% | +11.4% | 8.7 |

**Headline:** an image's emotion is measurably **more similar to its own prompt than to a random prompt** (VA similarity 70.0% vs 65.1% null, z=9.6). The alignment is real — it was just hidden by exact-match scoring.

## Asymmetry (still holds on the similarity scale)
- Positive-text pairs (n=454): VA-similarity **67.1%**, valence-sign agreement 18.1%
- Negative-text pairs (n=129): VA-similarity **80.4%**, valence-sign agreement 64.3%

## Honest limitations
- V-A here is derived from emotion-label centroids (not continuous NRC-VAD) → this is family-level affect similarity; the describe→extract pipeline + NRC-VAD will make it continuous.
- Image side is still the direct-CLIP reader (to be replaced by describe→extract).
- Text side has only a top-1 label (no top-3) → soft top-3 is asymmetric (text-in-image-top3).
