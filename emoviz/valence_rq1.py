#!/usr/bin/env python3
"""
[SUPERSEDED — v1 (direct-CLIP) analysis. Current analysis: analysis_final.py.]

Post-hoc RQ1 on the axis CLIP can actually read.

Validation (outputs/validation) showed CLIP zero-shot reads happiness & sadness from
line-art at ~75% precision but is unreliable on anger/fear/surprise/disgust. So report
RQ1 three ways and let the reader see the trade-off:
  (a) full 7-way Ekman agreement (contaminated, lower bound);
  (b) VALENCE 3-way (positive / negative / neutral) — errors within the negative
      bucket (fear<->disgust<->anger) collapse away;
  (c) TRUSTWORTHY subset — only confident (margin>=0.10) happiness/sadness image
      predictions, i.e. where CLIP was measured to be right ~75% of the time.
Reads outputs/results.json (must be a v2 CLIP run). No new deps.
"""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(ROOT, "outputs", "results.json")))["rows"]

POS, NEG, NEU = {"happiness"}, {"sadness", "anger", "fear", "disgust"}, {"neutral", "surprise"}
def val(lbl):
    return "+" if lbl in POS else "-" if lbl in NEG else "0"

def kappa(pairs):
    labs = sorted({x for p in pairs for x in p})
    idx = {l: i for i, l in enumerate(labs)}; k = len(labs); n = len(pairs)
    m = [[0]*k for _ in range(k)]
    for a, b in pairs: m[idx[a]][idx[b]] += 1
    po = sum(m[i][i] for i in range(k))/n
    r = [sum(m[i])/n for i in range(k)]; c = [sum(m[i][j] for i in range(k))/n for j in range(k)]
    pe = sum(r[i]*c[i] for i in range(k))
    return (po-pe)/(1-pe) if pe < 1 else 1.0, po, n

emo = [r for r in rows if r.get("is_emotional") and r.get("img_basic") and r.get("text_basic")]

# (a) full 7-way
full = [(r["text_basic"], r["img_basic"]) for r in emo]
ka, poa, na = kappa(full)

# (b) valence 3-way (drop pairs where either side is neutral/surprise->'0'? keep all 3 classes)
valp = [(val(r["text_basic"]), val(r["img_basic"])) for r in emo]
kb, pob, nb = kappa(valp)

# (c) trustworthy subset: image pred is confident happiness/sadness
def margin(r): return (r.get("img_scores") or {}).get("_margin", 0.0)
trust = [r for r in emo if r["img_basic"] in ("happiness", "sadness") and margin(r) >= 0.10]
tv = [(val(r["text_basic"]), val(r["img_basic"])) for r in trust]
kc, poc, nc = kappa(tv) if tv else (float("nan"), float("nan"), 0)

print("=== RQ1 on multiple axes (v2 CLIP reader) ===\n")
print(f"(a) Full 7-way Ekman     n={na:4d}  agreement={poa:.1%}  kappa={ka:.3f}   [contaminated - lower bound]")
print(f"(b) Valence pos/neg/neu  n={nb:4d}  agreement={pob:.1%}  kappa={kb:.3f}   [defensible]")
print(f"(c) Trustworthy subset   n={nc:4d}  agreement={poc:.1%}  kappa={kc:.3f}   [confident happy/sad img preds]")

# valence confusion
from collections import Counter
print("\nValence confusion (text -> image):")
for tv_ in ["+", "-", "0"]:
    c = Counter(iv for t, iv in valp if t == tv_)
    print(f"  text {tv_}: {dict(c)}")
