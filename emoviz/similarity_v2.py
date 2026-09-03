#!/usr/bin/env python3
"""
emoviz/similarity_v2.py — Stage-3 similarity ladder for the NEW describe->extract pipeline,
plus the OLD-vs-NEW baseline comparison (Chen's evaluation: does describe->extract beat direct-CLIP?).

Reads:
  outputs/describe_extract.jsonl  (NEW: prompt & image emotions, both via zero-shot NLI, top-3)
  outputs/results.json            (OLD: direct-CLIP image emotion, for the baseline comparison)

Reports, each against a random-pairing NULL baseline (so "similar" means "more similar to its OWN
prompt than to a random prompt"):
  1. Valence-Arousal similarity   (weighted top-3 centroid; headline)
  2. Valence-sign agreement
  3. Emotion-family agreement (top-1)
  4. Top-3 soft overlap           (both sides now have top-3 — a real set comparison)
Plus positive-vs-negative asymmetry, and NEW (describe->extract) vs OLD (direct-CLIP) side by side.
"""
import json, os, math, random, statistics as st
random.seed(7)
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "outputs")

# label -> (valence in [-1,1], arousal in [0,1]) centroids; happiness==joy
CEN = {"joy": (0.8, 0.6), "happiness": (0.8, 0.6), "sadness": (-0.75, 0.3), "anger": (-0.7, 0.8),
       "fear": (-0.65, 0.75), "surprise": (0.3, 0.8), "disgust": (-0.7, 0.6), "neutral": (0.0, 0.3)}
POS = {"joy", "happiness"}
NEG = {"sadness", "anger", "fear", "disgust"}
def sign(l): return "+" if l in POS else "-" if l in NEG else "0"
def fam(l): return "joy" if l in POS else l  # collapse joy/happiness


def va_point(top3):
    """weighted average of top-3 emotion centroids -> one continuous (v,a) point."""
    tot = sum(s for _, s in top3) or 1.0
    v = sum(CEN[l][0] * s for l, s in top3) / tot
    a = sum(CEN[l][1] * s for l, s in top3) / tot
    return v, a


def va_sim(p, q):
    dv = ((p[0] + 1) / 2) - ((q[0] + 1) / 2)
    da = p[1] - q[1]
    return 1 - math.hypot(dv, da) / math.sqrt(2)


def soft_overlap(a3, b3):
    """probability-weighted overlap of two top-3 label lists (0..1)."""
    da = {l: s for l, s in a3}; db = {l: s for l, s in b3}
    inter = sum(min(da.get(l, 0), db.get(l, 0)) for l in set(da) | set(db))
    denom = (sum(da.values()) + sum(db.values())) / 2 or 1.0
    return inter / denom


def metrics(pairs):
    va = [va_sim(va_point(p), va_point(i)) for p, i in pairs]
    vs = [1 for p, i in pairs if sign(p[0][0]) != "0" and sign(p[0][0]) == sign(i[0][0])]
    vsd = [1 for p, i in pairs if sign(p[0][0]) != "0"]
    famhit = [1 for p, i in pairs if fam(p[0][0]) == fam(i[0][0])]
    ov = [soft_overlap(p, i) for p, i in pairs]
    return {"va": st.mean(va), "vsign": sum(vs) / max(1, len(vsd)),
            "family": sum(famhit) / len(pairs), "overlap": st.mean(ov)}


def with_null(pairs, N=300):
    true = metrics(pairs)
    prompts = [p for p, _ in pairs]; imgs = [i for _, i in pairs]
    null = {k: [] for k in true}
    for _ in range(N):
        sh = imgs[:]; random.shuffle(sh)
        m = metrics(list(zip(prompts, sh)))
        for k in m: null[k].append(m[k])
    return true, {k: st.mean(v) for k, v in null.items()}, {k: (st.pstdev(v) or 1e-9) for k, v in null.items()}


# ---------- load NEW (describe->extract) ----------
newd = {}
p = os.path.join(OUT, "describe_extract.jsonl")
if os.path.exists(p):
    for line in open(p, encoding="utf-8"):
        try:
            r = json.loads(line)
            if r["id"] <= 13:          # pre-test developer records — excluded per methodology
                continue
            newd[r["id"]] = (r["prompt_emotions"], r["image_emotions"], r.get("description", ""))
        except Exception:
            pass

# ---------- load OLD (direct-CLIP) ----------
oldd = {}
_base = os.path.join(OUT, "results_clip_v2_baseline.json")   # frozen direct-CLIP baseline (run.py would overwrite results.json)
rj = json.load(open(_base if os.path.exists(_base) else os.path.join(OUT, "results.json")))["rows"]
for r in rj:
    if r.get("is_emotional") and r.get("img_basic") and r.get("text_basic"):
        oldd[r["id"]] = r

# ---------- NEW pipeline similarity ----------
new_pairs = [(newd[i][0], newd[i][1]) for i in newd
             if newd[i][0][0][0] != "neutral" or newd[i][1][0][0] != "neutral"]  # keep if either side emotional
print(f"=== NEW describe->extract pipeline — {len(new_pairs)} records ===")
if new_pairs:
    t, nm, ns = with_null(new_pairs)
    names = {"va": "Valence-Arousal similarity", "vsign": "Valence-sign agreement",
             "family": "Emotion-family agreement", "overlap": "Top-3 soft overlap"}
    print(f"{'metric':28s} {'TRUE':>7s} {'NULL':>7s} {'gap':>6s} {'z':>5s}")
    for k in ["va", "vsign", "family", "overlap"]:
        z = (t[k] - nm[k]) / ns[k]
        print(f"{names[k]:28s} {t[k]:6.1%} {nm[k]:6.1%} {t[k]-nm[k]:+5.1%} {z:4.1f}")

    # asymmetry
    def sub(sg): return [(pe, ie) for pe, ie in new_pairs if sign(pe[0][0]) == sg]
    pos, neg = sub("+"), sub("-")
    print(f"\nAsymmetry (VA similarity):")
    if pos: print(f"  positive prompts (n={len(pos)}): {metrics(pos)['va']:.1%}  vsign {metrics(pos)['vsign']:.1%}")
    if neg: print(f"  negative prompts (n={len(neg)}): {metrics(neg)['va']:.1%}  vsign {metrics(neg)['vsign']:.1%}")

# ---------- OLD vs NEW baseline comparison (same prompt basis) ----------
both = [i for i in newd if i in oldd]
print(f"\n=== BASELINE COMPARISON (image-emotion method) — {len(both)} records in both ===")
if both:
    # hold prompt side constant = NLI prompt emotion; vary image method.
    # canonicalise 'happiness' (old CLIP label space) -> 'joy' (new label space) so the
    # soft-overlap metric compares like with like (audit fix: without this, all
    # joy<->happiness mass counted as zero overlap, deflating the OLD method's score).
    def img_old_top3(r):
        sc = {k: v for k, v in (r.get("img_scores") or {}).items() if not k.startswith("_")}
        return [["joy" if k == "happiness" else k, float(v)]
                for k, v in sorted(sc.items(), key=lambda x: -x[1])[:3]]
    new_pp = [(newd[i][0], newd[i][1]) for i in both]           # prompt NLI vs image describe-NLI
    old_pp = [(newd[i][0], img_old_top3(oldd[i])) for i in both]  # prompt NLI vs image direct-CLIP
    tn, nmn, nsn = with_null(new_pp)
    to, nmo, nso = with_null(old_pp)
    print(f"{'':28s} {'NEW(describe)':>14s} {'OLD(directCLIP)':>16s}")
    for k in ["va", "family", "overlap"]:
        zn = (tn[k] - nmn[k]) / nsn[k]; zo = (to[k] - nmo[k]) / nso[k]
        print(f"{k:28s} {tn[k]:6.1%} (z={zn:4.1f}) {to[k]:6.1%} (z={zo:4.1f})")
    print("Higher true-vs-null gap (z) = the image-emotion method that aligns better with the prompt.")
