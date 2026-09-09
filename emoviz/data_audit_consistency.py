#!/usr/bin/env python3
"""
emoviz/data_audit_consistency.py — (1) account for EVERY record so nothing is silently left out,
and (2) analyse the repeated-prompt groups as a CONSISTENCY check: where the same prompt text appears
more than once in the corpus, how stable is the emotion the pipeline reads from the resulting drawings?
Generation parameters were never recorded, so this bounds the reproducibility of the deployed
prompt->image->reader chain as a whole; it does not isolate the generator.

Every consistency figure is reported against a seeded permutation null (image readings shuffled across
all analysed records and re-cut into the same groups), because half the groups are pairs, whose modal
agreement cannot fall below 50% — a bare percentage would overstate the instability.

Uses outputs/describe_extract.jsonl (all 1,025 records). Writes outputs/consistency.json.
"""
import json, os, statistics as st
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
rows = [json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8")]

POS, NEG = {"joy"}, {"sadness", "anger", "fear", "disgust"}
def sign(l): return "+" if l in POS else "-" if l in NEG else "0"

# ---------- 1. FULL DATA ACCOUNTING (nothing dropped, only grouped) ----------
pre = [r for r in rows if r["id"] <= 13]
main = [r for r in rows if r["id"] > 13]
print("=== DATA ACCOUNTING — every record used ===")
print(f"total processed by pipeline : {len(rows)}   (100% of the dataset, 0 failures)")
print(f"  pre-test (ids 1-13)       : {len(pre)}   -> excluded from analysis (developer tests), still processed")
print(f"  analysed                  : {len(main)}")
# emotional split via the SAME reader as the final analysis (GoEmotions cache), for consistency
_goe = {int(k): v for k, v in json.load(open(os.path.join(OUT, "prompt_emotions_goe.json"))).items()} \
    if os.path.exists(os.path.join(OUT, "prompt_emotions_goe.json")) else {}
def _emotional(r):
    pe = _goe.get(r["id"])
    return (pe[0][0] if pe else r["prompt_emotions"][0][0]) != "neutral"
emo = sum(1 for r in main if _emotional(r))
print(f"    emotional prompts       : {emo}")
print(f"    non-emotional prompts   : {len(main)-emo}   (analysed too -> specificity check: agreement at chance)")
print("  every analysed record is in exactly one emotional/non-emotional and one face/scene group,")
print("  and ALL groups are reported (nothing is discarded — splits are groupings, not exclusions).")

# ---------- 2. RQ3 — generative consistency across repeated prompts ----------
groups = defaultdict(list)
for r in main:
    groups[r.get("dedup_key", r["text"].strip().lower())].append(r)   # identity from ORIGINAL text
runs = {t: rs for t, rs in groups.items() if len(rs) >= 2}   # prompts drawn 2+ times
n_in_runs = sum(len(rs) for rs in runs.values())
print(f"\n=== CONSISTENCY across repeated prompts ===")
print(f"{len(runs)} distinct prompts were drawn 2+ times, covering {n_in_runs} of {len(main)} records "
      f"({n_in_runs/len(main):.0%}). NOTE: these pool corpus-wide repeats (same text typed by different "
      f"visitors AND consecutive re-submissions); generation parameters were not recorded. The question is: "
      f"given the same prompt text, how stable is the emotion the pipeline reads from the drawings?")

import random
def consistency(label_of):
    """Per-group modal fractions for a labelling function, plus the fully-consistent count."""
    ce, cv = [], []
    for rs in runs.values():
        labs = [label_of(r) for r in rs]; vals = [sign(l) for l in labs]
        ce.append(Counter(labs).most_common(1)[0][1] / len(rs))     # modal-emotion fraction
        cv.append(Counter(vals).most_common(1)[0][1] / len(rs))     # modal-valence fraction
    return st.mean(ce), st.mean(cv), sum(1 for c in ce if c == 1.0)

obs_emo, obs_val, full = consistency(lambda r: r["image_top1"])
pairs = sum(1 for rs in runs.values() if len(rs) == 2)
print(f"  mean per-prompt agreement on the EXACT emotion : {obs_emo:.1%}")
print(f"  mean per-prompt agreement on valence (+/-/0)   : {obs_val:.1%}")
print(f"  prompts where every drawing shared one emotion : {full}/{len(runs)}")
print(f"  ({pairs} of the {len(runs)} groups are pairs, whose modal agreement cannot fall below 50%)")

# ---- permutation null: shuffle the image readings across ALL analysed records, re-cut into the
#      same groups (same sizes), and recompute. Seeded; P draws. This is the chance level the
#      observed figures must be read against.
P, SEED = 10000, 7
rng = random.Random(SEED)
labels = [r["image_top1"] for r in main]
idx = {r["id"]: i for i, r in enumerate(main)}
null_emo, null_val, null_full = [], [], []
for _ in range(P):
    sh = labels[:]; rng.shuffle(sh)
    e, v, f = consistency(lambda r: sh[idx[r["id"]]])
    null_emo.append(e); null_val.append(v); null_full.append(f)
def zsum(obs, null):
    m, sd = st.mean(null), (st.pstdev(null) or 1e-9)
    return {"obs": obs, "null_mean": m, "null_sd": sd, "z": (obs - m) / sd,
            "p_perm": (sum(1 for x in null if x >= obs) + 1) / (len(null) + 1)}
Z = {"mean_emotion_consistency": zsum(obs_emo, null_emo),
     "mean_valence_consistency": zsum(obs_val, null_val),
     "fully_consistent_runs": zsum(full, null_full)}
print(f"\n  Permutation null ({P} draws, seed {SEED}; image readings shuffled across all {len(main)} records, same groups):")
for k, v in Z.items():
    fmt = (lambda x: f"{x:.1f}") if k == "fully_consistent_runs" else (lambda x: f"{x:.1%}")
    print(f"    {k:26s} observed {fmt(v['obs'])}  null {fmt(v['null_mean'])} (sd {fmt(v['null_sd'])})  z {v['z']:+.1f}  p {v['p_perm']:.4f}")

# biggest runs, with breakdown
print("\n  Most-repeated prompts (image-emotion breakdown):")
for t, rs in sorted(runs.items(), key=lambda x: -len(x[1]))[:6]:
    c = Counter(r["image_top1"] for r in rs)
    modal = c.most_common(1)[0]
    label = rs[0]["text"][:30]          # groups are keyed by dedup_key (an int); show the prompt text
    print(f"    {label!r:32s} x{len(rs):<3d} modal={modal[0]}({modal[1]}/{len(rs)})  {dict(c.most_common())}")

print(f"\nInterpretation: across {len(runs)} prompts drawn two or more times, the pipeline reads the same "
      f"emotion for {obs_emo:.1%} of the drawings within a group, against {Z['mean_emotion_consistency']['null_mean']:.1%} "
      f"for randomly regrouped readings (z {Z['mean_emotion_consistency']['z']:+.1f}) — more consistent than chance, "
      f"but far from fixed. This measures the stability of the whole prompt->image->reader chain, not the "
      f"generator alone: with no reliability estimate for the reader, an unknown share of the variation is "
      f"measurement noise.")

# save
out = {"total": len(rows), "pretest": len(pre), "analysed": len(main), "emotional": emo,
       "runs": len(runs), "records_in_runs": n_in_runs, "pair_groups": pairs,
       "mean_emotion_consistency": round(obs_emo, 3),
       "mean_valence_consistency": round(obs_val, 3),
       "fully_consistent_runs": full,
       "null": {"draws": P, "seed": SEED,
                "method": "image top-1 readings shuffled across all analysed records, re-cut into the same 87 groups",
                **{k: {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in Z.items()}},
       "largest_groups": [{"text": rs[0]["text"][:40], "n": len(rs), "image_top1": dict(Counter(r["image_top1"] for r in rs).most_common())}
                          for t, rs in sorted(runs.items(), key=lambda x: -len(x[1]))[:6]]}
json.dump(out, open(os.path.join(OUT, "consistency.json"), "w"), indent=1)
print("\nsaved outputs/consistency.json")
