#!/usr/bin/env python3
"""
significance.py — confidence intervals and a significance test for the face/scene difference.

Addresses the one inferential gap in the analysis: analysis_final.py reports each subset against its
own random-pairing null, but never tests whether the face and scene RATES DIFFER FROM EACH OTHER.

Two procedures, both clustered on prompt identity:
  * CLUSTERED BOOTSTRAP (10,000 draws) — resamples prompt GROUPS with replacement, giving a 95%
    confidence interval for each rate and for the difference.
  * CLUSTERED PERMUTATION TEST (10,000 draws) — shuffles the face/scene label across prompt groups
    and counts how often a difference at least as large as the observed one arises by chance.

Clustering matters: 249 of the 1,012 analysed records repeat an earlier prompt, so records are not
independent. Resampling individual records would understate the uncertainty.

WHAT THIS DOES AND DOES NOT SETTLE. It establishes that the face/scene gap is not sampling noise.
It does NOT remove the partial circularity: the split is derived from the same BLIP-VQA output whose
description the image reader reads, so a significant difference is evidence that the two groups
differ, not that faces inherently carry more emotional signal.

Run:  .venv/bin/python significance.py
"""

import json, re, random, statistics as st
from collections import defaultdict

CEN = {"joy":(0.8,0.6),"sadness":(-0.75,0.3),"anger":(-0.7,0.8),"fear":(-0.65,0.75),
       "surprise":(0.3,0.8),"disgust":(-0.7,0.6),"neutral":(0.0,0.3)}
POS, NEG = {"joy"}, {"sadness","anger","fear","disgust"}
sign = lambda l: "+" if l in POS else "-" if l in NEG else "0"

src = open("analysis_final.py").read()
EW = eval(re.search(r"EXPRESSION_WORDS\s*=\s*(\{[^}]*\})", src, re.S).group(1))
def n_people(a):
    a=(a or "").lower().strip()
    if a in {"0","none","no one","nobody","zero"}: return 0
    d=re.findall(r"\d+",a); return int(d[0]) if d else (1 if a else 0)
def is_face(v):
    w=set(re.findall(r"[a-z]+",(v.get("expression","") or "").lower()))
    return n_people(v.get("people",""))>=1 and bool(w & EW)

rows=[json.loads(l) for l in open("outputs/describe_extract.jsonl",encoding="utf-8")]
rows=[r for r in rows if r["id"]>13]
goe={int(k):v for k,v in json.load(open("outputs/prompt_emotions_goe.json")).items()}

recs=[]
for r in rows:
    pe, ie = goe[r["id"]], r["image_emotions"]
    recs.append({"key": r.get("dedup_key"), "p": pe[0][0], "i": ie[0][0],
                 "face": is_face(r.get("vqa",{}))})
emo=[r for r in recs if r["p"]!="neutral"]

def vsign_rate(sub):
    d=[r for r in sub if sign(r["p"])!="0"]
    return (sum(1 for r in d if sign(r["p"])==sign(r["i"]))/len(d), len(d)) if d else (float("nan"),0)
def family_rate(sub):
    return (sum(1 for r in sub if r["p"]==r["i"])/len(sub), len(sub)) if sub else (float("nan"),0)

face=[r for r in emo if r["face"]]; scene=[r for r in emo if not r["face"]]
print(f"emotional n={len(emo)}   face n={len(face)}   scene n={len(scene)}\n")

# ---- clustered bootstrap: resample PROMPT GROUPS, not records ----
groups=defaultdict(list)
for r in emo: groups[r["key"]].append(r)
keys=list(groups)
rng=random.Random(7); B=10000

def boot(metric):
    fa,sc,df=[],[],[]
    for _ in range(B):
        samp=[x for k in (rng.choice(keys) for _ in keys) for x in groups[k]]
        f=[r for r in samp if r["face"]]; s=[r for r in samp if not r["face"]]
        rf,_=metric(f); rs,_=metric(s)
        if rf==rf and rs==rs: fa.append(rf); sc.append(rs); df.append(rf-rs)
    q=lambda v,p: sorted(v)[int(p*(len(v)-1))]
    return fa,sc,df,q

for name,metric in [("valence-sign agreement",vsign_rate),("emotion-family agreement",family_rate)]:
    rf,nf=metric(face); rs,ns=metric(scene)
    fa,sc,df,q=boot(metric)
    print(f"=== {name} ===")
    print(f"  face   {rf:.1%}  95% CI [{q(fa,.025):.1%}, {q(fa,.975):.1%}]   (n={nf})")
    print(f"  scene  {rs:.1%}  95% CI [{q(sc,.025):.1%}, {q(sc,.975):.1%}]   (n={ns})")
    print(f"  difference  {rf-rs:+.1%}  95% CI [{q(df,.025):+.1%}, {q(df,.975):+.1%}]")
    # permutation test: shuffle the face/scene label ACROSS PROMPT GROUPS
    obs=rf-rs; cnt=0; P=10000
    glist=[groups[k] for k in keys]
    nface_groups=sum(1 for g in glist if sum(x["face"] for x in g)*2>=len(g))
    rng2=random.Random(11)
    for _ in range(P):
        lab=[True]*nface_groups+[False]*(len(glist)-nface_groups); rng2.shuffle(lab)
        f=[x for g,L in zip(glist,lab) if L for x in g]
        s=[x for g,L in zip(glist,lab) if not L for x in g]
        a,_=metric(f); b,_=metric(s)
        if a==a and b==b and abs(a-b)>=abs(obs): cnt+=1
    p=(cnt+1)/(P+1)
    print(f"  permutation test (labels shuffled across prompt groups, {P} draws): p = {p:.4f}"
          f"{'  -> significant at 0.05' if p<0.05 else ''}\n")
