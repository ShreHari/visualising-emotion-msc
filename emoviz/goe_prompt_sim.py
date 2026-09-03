#!/usr/bin/env python3
"""
Refinement test: the prompt side of describe_extract used zero-shot NLI, which over-labels short
prompts as 'surprise' (333/1025). GoEmotions read first-person prompts well earlier, so here we
re-extract PROMPT emotion with GoEmotions (28 labels -> 7 Ekman families), keep the NLI IMAGE
emotion from the jsonl, and recompute the similarity ladder. Compares to the NLI-prompt version.
Text-only, fast, no images.
"""
import json, os, math, random, statistics as st
random.seed(7)
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")

CEN = {"joy": (0.8, 0.6), "sadness": (-0.75, 0.3), "anger": (-0.7, 0.8), "fear": (-0.65, 0.75),
       "surprise": (0.3, 0.8), "disgust": (-0.7, 0.6), "neutral": (0.0, 0.3)}
POS, NEG = {"joy"}, {"sadness", "anger", "fear", "disgust"}
def sign(l): return "+" if l in POS else "-" if l in NEG else "0"

# GoEmotions 28 -> 7 Ekman families
G2F = {**dict.fromkeys(["admiration","amusement","approval","caring","desire","excitement","gratitude","joy","love","optimism","pride","relief"], "joy"),
       **dict.fromkeys(["disappointment","embarrassment","grief","remorse","sadness"], "sadness"),
       **dict.fromkeys(["anger","annoyance","disapproval"], "anger"),
       **dict.fromkeys(["fear","nervousness"], "fear"),
       **dict.fromkeys(["surprise","realization","confusion","curiosity"], "surprise"),
       "disgust": "disgust", "neutral": "neutral"}

def va_point(t3):
    tot = sum(s for _, s in t3) or 1.0
    return (sum(CEN[l][0]*s for l, s in t3)/tot, sum(CEN[l][1]*s for l, s in t3)/tot)
def va_sim(p, q): return 1 - math.hypot(((p[0]+1)/2)-((q[0]+1)/2), p[1]-q[1]) / math.sqrt(2)
def soft(a, b):
    da = {l: s for l, s in a}; db = {l: s for l, s in b}
    inter = sum(min(da.get(l, 0), db.get(l, 0)) for l in set(da) | set(db))
    return inter / ((sum(da.values())+sum(db.values()))/2 or 1)
def metrics(pairs):
    return {"va": st.mean(va_sim(va_point(p), va_point(i)) for p, i in pairs),
            "vsign": sum(1 for p, i in pairs if sign(p[0][0]) != "0" and sign(p[0][0]) == sign(i[0][0]))/max(1, sum(1 for p, i in pairs if sign(p[0][0]) != "0")),
            "family": sum(1 for p, i in pairs if p[0][0] == i[0][0])/len(pairs),
            "overlap": st.mean(soft(p, i) for p, i in pairs)}
def with_null(pairs, N=300):
    t = metrics(pairs); ps = [p for p, _ in pairs]; im = [i for _, i in pairs]
    nl = {k: [] for k in t}
    for _ in range(N):
        sh = im[:]; random.shuffle(sh)
        for k, v in metrics(list(zip(ps, sh))).items(): nl[k].append(v)
    return t, {k: st.mean(v) for k, v in nl.items()}, {k: (st.pstdev(v) or 1e-9) for k, v in nl.items()}

# load records (pre-test ids 1-13 excluded per methodology)
rows = [r for r in (json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8"))
        if r["id"] > 13]

# GoEmotions on the prompts -> 7-family top-3
import torch
from transformers import pipeline
dev = "mps" if torch.backends.mps.is_available() else "cpu"
print("[GoEmotions on prompts ...]")
clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None, truncation=True, device=dev, batch_size=32)
texts = [r["text"] for r in rows]
preds = clf(texts)
def to_fam_top3(pred):
    fam = {}
    for d in pred:
        f = G2F.get(d["label"], "neutral"); fam[f] = fam.get(f, 0) + d["score"]
    top = sorted(fam.items(), key=lambda x: -x[1])[:3]
    return [[l, round(float(s), 4)] for l, s in top]
goe_prompt = {r["id"]: to_fam_top3(p) for r, p in zip(rows, preds)}

# distribution check
from collections import Counter
dist = Counter(goe_prompt[r["id"]][0][0] for r in rows)
print("GoEmotions prompt top-1 distribution:", dict(dist.most_common()))

# similarity: GoEmotions-prompt vs NLI-image
pairs = [(goe_prompt[r["id"]], r["image_emotions"]) for r in rows
         if goe_prompt[r["id"]][0][0] != "neutral" or r["image_emotions"][0][0] != "neutral"]
t, nm, ns = with_null(pairs)
print(f"\n=== GoEmotions-prompt  vs  NLI-image  ({len(pairs)} records) ===")
names = {"va": "Valence-Arousal similarity", "vsign": "Valence-sign agreement",
         "family": "Emotion-family agreement", "overlap": "Top-3 soft overlap"}
for k in ["va", "vsign", "family", "overlap"]:
    print(f"{names[k]:28s} {t[k]:6.1%} (null {nm[k]:5.1%}, z={ (t[k]-nm[k])/ns[k]:.1f})")

pos = [(p, i) for p, i in pairs if sign(p[0][0]) == "+"]
neg = [(p, i) for p, i in pairs if sign(p[0][0]) == "-"]
print(f"\nAsymmetry: positive(n={len(pos)}) VA {metrics(pos)['va']:.1%} vsign {metrics(pos)['vsign']:.1%}"
      f"  |  negative(n={len(neg)}) VA {metrics(neg)['va']:.1%} vsign {metrics(neg)['vsign']:.1%}")
