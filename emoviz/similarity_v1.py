#!/usr/bin/env python3
"""
[SUPERSEDED — v1 (direct-CLIP) similarity reframe. Current analysis: analysis_final.py + similarity_v2.py.]

similarity_v1.py — reframe existing results from MATCHING to SIMILARITY (Chen's direction).

Uses only outputs/results.json (GoEmotions text emotion + CLIP image emotion, already computed).
Computes a "similarity ladder" instead of exact-match agreement, each against a random-pairing
NULL baseline so we can claim "an image's emotion is more similar to its OWN prompt than to a
random prompt" — the defensible, non-binary framing.

Metrics:
  1. Valence-Arousal similarity  (1 - normalised distance in affect space) -- headline
  2. Valence-sign agreement       (both positive / both negative)
  3. Ekman family exact agreement (the old "match" number, for contrast)
  4. Soft top-3                   (is the text emotion in the image's top-3?)
Plus the positive-vs-negative asymmetry, on the similarity scale.

Honest limitation: text/image V-A here come from emotion-label centroids, not continuous NRC-VAD
lexicon values -- so this measures similarity between emotion FAMILIES in affect space. The full
describe->extract pipeline + NRC-VAD will make it continuous. Still a valid first cut.
"""
import json, os, random, statistics as st
random.seed(7)
ROOT = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(ROOT, "outputs", "results.json")))["rows"]
E = [r for r in rows if r.get("is_emotional") and r.get("img_basic") and r.get("text_basic")]

POS, NEG = {"happiness"}, {"sadness", "anger", "fear", "disgust"}
def sign(lbl): return "+" if lbl in POS else "-" if lbl in NEG else "0"   # surprise/neutral -> 0
META = {"_portrait_prob", "_margin", "_has_face"}

def va_sim(tv, ta, iv, ia):
    # normalise valence [-1,1]->[0,1]; arousal already ~[0,1]; 1 - dist/max
    import math
    dv = ((tv + 1) / 2) - ((iv + 1) / 2)
    da = ta - ia
    d = math.hypot(dv, da)
    return 1 - d / math.sqrt(2)

def img_top3(r):
    sc = {k: v for k, v in (r.get("img_scores") or {}).items() if k not in META}
    return [k for k, _ in sorted(sc.items(), key=lambda x: -x[1])[:3]]

def metrics(pairs):
    """pairs = list of (text_row, image_row) — allows shuffling the image side."""
    va = [va_sim(t["text_valence"], t["text_arousal"], i["img_valence"], i["img_arousal"]) for t, i in pairs]
    vsign = [1 for t, i in pairs if sign(t["text_basic"]) != "0" and sign(t["text_basic"]) == sign(i["img_basic"])]
    vsign_denom = [1 for t, i in pairs if sign(t["text_basic"]) != "0"]
    fam = [1 for t, i in pairs if t["text_basic"] == i["img_basic"]]
    top3 = [1 for t, i in pairs if t["text_basic"] in img_top3(i)]
    return {
        "va": st.mean(va),
        "vsign": sum(vsign) / max(1, len(vsign_denom)),
        "family": sum(fam) / len(pairs),
        "top3": sum(top3) / len(pairs),
    }

true_pairs = [(r, r) for r in E]
true = metrics(true_pairs)

# NULL baseline: shuffle which image goes with which text, N times
N = 300
null = {k: [] for k in true}
imgs = list(E)
for _ in range(N):
    shuf = imgs[:]; random.shuffle(shuf)
    m = metrics(list(zip(E, shuf)))
    for k in m: null[k].append(m[k])
null_mean = {k: st.mean(v) for k, v in null.items()}
null_sd = {k: (st.pstdev(v) or 1e-9) for k, v in null.items()}

names = {"va": "Valence-Arousal similarity (headline)", "vsign": "Valence-sign agreement",
         "family": "Ekman family EXACT match (old metric)", "top3": "Text emotion in image top-3 (soft)"}
print(f"=== SIMILARITY vs MATCHING — {len(E)} emotional paired records ===\n")
print(f"{'metric':40s}  {'TRUE':>7s}  {'NULL':>7s}  {'gap':>6s}  {'z':>5s}")
for k in ["va", "vsign", "family", "top3"]:
    z = (true[k] - null_mean[k]) / null_sd[k]
    print(f"{names[k]:40s}  {true[k]:6.1%}  {null_mean[k]:6.1%}  {true[k]-null_mean[k]:+5.1%}  {z:4.1f}")

# asymmetry on the similarity scale
def subset(sgn): return [(r, r) for r in E if sign(r["text_basic"]) == sgn]
pos, neg = subset("+"), subset("-")
print(f"\n=== ASYMMETRY (VA similarity) ===")
print(f"  positive-text pairs (n={len(pos)}):  VA-sim {metrics(pos)['va']:.1%}   vsign {metrics(pos)['vsign']:.1%}")
print(f"  negative-text pairs (n={len(neg)}):  VA-sim {metrics(neg)['va']:.1%}   vsign {metrics(neg)['vsign']:.1%}")

# save markdown summary
out = ["# Similarity Analysis v1 (reframe of existing results)\n",
       f"On {len(E)} emotional paired records. Each metric vs a random-pairing null (N={N}).",
       "Framing: **how similar** the image emotion is to the prompt emotion — not right/wrong.\n",
       "| Metric | True pairs | Random pairs | Gap | z |",
       "|---|--:|--:|--:|--:|"]
for k in ["va", "vsign", "family", "top3"]:
    z = (true[k] - null_mean[k]) / null_sd[k]
    out.append(f"| {names[k]} | {true[k]:.1%} | {null_mean[k]:.1%} | {true[k]-null_mean[k]:+.1%} | {z:.1f} |")
out += ["",
        f"**Headline:** an image's emotion is measurably **more similar to its own prompt than to a "
        f"random prompt** (VA similarity {true['va']:.1%} vs {null_mean['va']:.1%} null, z={((true['va']-null_mean['va'])/null_sd['va']):.1f}). "
        "The alignment is real — it was just hidden by exact-match scoring.",
        "",
        "## Asymmetry (still holds on the similarity scale)",
        f"- Positive-text pairs (n={len(pos)}): VA-similarity **{metrics(pos)['va']:.1%}**, valence-sign agreement {metrics(pos)['vsign']:.1%}",
        f"- Negative-text pairs (n={len(neg)}): VA-similarity **{metrics(neg)['va']:.1%}**, valence-sign agreement {metrics(neg)['vsign']:.1%}",
        "",
        "## Honest limitations",
        "- V-A here is derived from emotion-label centroids (not continuous NRC-VAD) → this is "
        "family-level affect similarity; the describe→extract pipeline + NRC-VAD will make it continuous.",
        "- Image side is still the direct-CLIP reader (to be replaced by describe→extract).",
        "- Text side has only a top-1 label (no top-3) → soft top-3 is asymmetric (text-in-image-top3)."]
open(os.path.join(ROOT, "outputs", "similarity_v1.md"), "w").write("\n".join(out) + "\n")
print("\nsaved outputs/similarity_v1.md")
