#!/usr/bin/env python3
"""
emoviz/method_comparison.py — LIKE-FOR-LIKE comparison of the two IMAGE readers.

The published comparison (similarity_v2.py, reported in RESULTS_describe_extract.md and the dossier as
"describe-then-extract 49.3% vs direct-CLIP 25.3% family agreement") is NOT like-for-like with the
main analysis (analysis_final.py):
  * its PROMPT reader is BART-MNLI zero-shot (describe_extract.jsonl 'prompt_emotions'), not GoEmotions;
  * its subset is the 608 records the OLD lexicon reader flagged as emotional, not the 607 GoEmotions
    non-neutral prompts;
  * its overlap formula (similarity_v2.soft_overlap: intersection / mean of the two sums) differs from
    analysis_final.soft(), which normalises EACH side's top-3 to 1 first.

This script redoes the comparison holding EVERYTHING constant except the image reader:
  prompt reader   GoEmotions 28->7 families, cached in outputs/prompt_emotions_goe.json (same as analysis_final.py)
  subset          analysed ids 14..1025 (pre-tests dropped) whose GoEmotions top-1 family != 'neutral'  -> 607
  metrics         sign() / va_sim / soft() / metrics() / with_null() copied VERBATIM from analysis_final.py
  null            300 random re-pairings, random.seed(7), called in the SAME ORDER as analysis_final.py so the
                  describe-then-extract numbers are the published ones to the digit and BOTH readers see the
                  identical 300 shuffles
  image reader A  describe-then-extract: describe_extract.jsonl 'image_emotions' (BLIP-VQA description -> NLI top-3)
  image reader B  direct-CLIP:           results_clip_v2_baseline.json rows[].img_scores (CLIP zero-shot over
                  7 labels; 'happiness' -> 'joy'; top-1 = img_basic, the unrounded argmax)

Each reader is scored on valence-sign agreement, family agreement, top-3 overlap and VA similarity between
the prompt reader and the image reader, each against its own random-pairing null with a z-score, on the
records both readers cover (all 607 — both files hold every analysed id).

Then a PAIRED test on per-record family hit/miss (and valence-sign hit/miss):
  * exact-binomial McNemar p (treats records as independent — OPTIMISTIC, because 249 of the 1,012
    analysed records repeat an earlier prompt, so repeated prompts are not independent evidence);
  * a CLUSTER-LEVEL SIGN-FLIP randomisation test — the McNemar statistic (b - c) recomputed after flipping
    the sign of each dedup_key cluster's hit-difference as a block — which respects the prompt clustering;
  * a clustered bootstrap 95% CI for the difference in agreement rates (resampling dedup_key clusters).

analysis_final.py executes on import (it re-runs the whole analysis and rewrites analysis_final.csv), so
nothing is imported from it: the constants and functions below are copied from it verbatim, and the
face/scene rule (is_face) likewise, so the face/scene counts (591/421; within emotional 402/205) reproduce
(one code COMMENT inside is_face is reworded for the project vocabulary; the code is unchanged).

Writes outputs/method_comparison.json. Never touches the frozen inputs.
Run:  .venv/bin/python method_comparison.py
"""
import json, os, math, random, statistics as st, re, time
from collections import defaultdict

T0 = time.time()
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
SEED, N_SHUFFLE = 7, 300
PRETEST_MAX_ID = 13                       # ids 1-13 = pre-festival developer tests (as analysis_final.py)
FAMILIES = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]

# ======== copied VERBATIM from analysis_final.py (lines 24-81) — do not edit here; edit there ========
CEN = {"joy": (0.8, 0.6), "sadness": (-0.75, 0.3), "anger": (-0.7, 0.8), "fear": (-0.65, 0.75),
       "surprise": (0.3, 0.8), "disgust": (-0.7, 0.6), "neutral": (0.0, 0.3)}   # emotion -> (valence,arousal)
POS, NEG = {"joy"}, {"sadness", "anger", "fear", "disgust"}
# vocabulary of readable facial-expression answers (a documented word list, not per-image tuning)
EXPRESSION_WORDS = {"smile", "smiling", "happy", "sad", "angry", "serious", "surprised", "surprise",
                    "calm", "excited", "crying", "laughing", "frowning", "scared", "shocked", "worried",
                    "concentration", "concentrating", "grin", "grinning", "neutral",
                    "confused", "determined", "pensive", "sleepy", "sleeping"}
NUMWORDS = {"no": 0, "none": 0, "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "several": 3, "many": 4, "crowd": 5, "group": 3, "lots": 4}

def sign(l): return "+" if l in POS else "-" if l in NEG else "0"

def n_people(ans):
    a = (ans or "").lower().strip()
    m = re.search(r"\d+", a)
    if m: return int(m.group())
    for w, n in NUMWORDS.items():
        if re.search(rf"\b{w}\b", a): return n   # word-boundary (avoids 'no' inside 'unknown')
    return 1 if a else 0                          # a non-empty non-numeric answer implies a subject present

def is_face(vqa):
    # token-intersection so multi-word answers ("man is smiling") count (audit fix; comment reworded here)
    words = set(re.findall(r"[a-z]+", vqa.get("expression", "").lower()))
    return n_people(vqa.get("people", "")) >= 1 and bool(words & EXPRESSION_WORDS)

# ---- similarity metrics (weighted top-3 centroid; soft overlap) ----
def va_point(t3):
    tot = sum(s for _, s in t3) or 1.0
    return (sum(CEN[l][0]*s for l, s in t3)/tot, sum(CEN[l][1]*s for l, s in t3)/tot)
def va_sim(p, q): return 1 - math.hypot(((p[0]+1)/2)-((q[0]+1)/2), p[1]-q[1]) / math.sqrt(2)
def soft(a, b):
    # normalise EACH side's top-3 to sum 1 first, so prompt (multi-label) and image (softmax) scales
    # are comparable; then overlap = sum of per-label minima (a proper distribution overlap in [0,1]).
    sa = sum(s for _, s in a) or 1.0; sb = sum(s for _, s in b) or 1.0
    da = {l: s/sa for l, s in a}; db = {l: s/sb for l, s in b}
    return sum(min(da.get(l, 0), db.get(l, 0)) for l in set(da) | set(db))
def metrics(pairs):
    vsd = [1 for p, i in pairs if sign(p[0][0]) != "0"]
    return {"va": st.mean(va_sim(va_point(p), va_point(i)) for p, i in pairs),
            "vsign": sum(1 for p, i in pairs if sign(p[0][0]) != "0" and sign(p[0][0]) == sign(i[0][0]))/max(1, len(vsd)),
            "family": sum(1 for p, i in pairs if p[0][0] == i[0][0])/len(pairs),
            "overlap": st.mean(soft(p, i) for p, i in pairs)}
def with_null(pairs, N=300):
    if len(pairs) < 5: return metrics(pairs), None, None
    t = metrics(pairs); ps = [p for p, _ in pairs]; im = [i for _, i in pairs]
    nl = {k: [] for k in t}
    for _ in range(N):
        sh = im[:]; random.shuffle(sh)
        for k, v in metrics(list(zip(ps, sh))).items(): nl[k].append(v)
    return t, {k: st.mean(v) for k, v in nl.items()}, {k: (st.pstdev(v) or 1e-9) for k, v in nl.items()}
# ======== end of verbatim copy ========

# ---------- direct-CLIP label space -> the seven families ----------
CLIP2FAM = {"happiness": "joy", "sadness": "sadness", "anger": "anger", "fear": "fear",
            "surprise": "surprise", "disgust": "disgust", "neutral": "neutral"}
def clip_top3(row):
    """Top-3 [family, score] from the CLIP softmax over 7 labels. Scores in the file are rounded to 3 dp;
    img_basic is the argmax of the UNROUNDED softmax, so it is placed first (this breaks the two
    three-decimal ties, ids 24 and 256), then the rest are ordered by score."""
    sc = {CLIP2FAM[k]: float(v) for k, v in row["img_scores"].items() if not k.startswith("_")}
    top1 = CLIP2FAM[row["img_basic"]]
    order = sorted(sc, key=lambda l: (l != top1, -sc[l]))
    return [[l, sc[l]] for l in order[:3]]

# ---------- load the frozen inputs (read-only) ----------
rows = [json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8")]
rows = [r for r in rows if r["id"] > PRETEST_MAX_ID]
goe = {int(k): v for k, v in json.load(open(os.path.join(OUT, "prompt_emotions_goe.json"))).items()}
clip = {r["id"]: r for r in json.load(open(os.path.join(OUT, "results_clip_v2_baseline.json")))["rows"]}
missing_goe = [r["id"] for r in rows if r["id"] not in goe]
if missing_goe: raise SystemExit(f"prompt_emotions_goe.json lacks {len(missing_goe)} ids, e.g. {missing_goe[:5]}")

recs = []
for r in rows:
    pe = goe[r["id"]]
    rec = {"id": r["id"], "key": r.get("dedup_key"), "pe": pe, "prompt_top": pe[0][0],
           "emotional": pe[0][0] != "neutral", "face": is_face(r.get("vqa", {})),
           "ie_describe": r["image_emotions"]}
    c = clip.get(r["id"])
    rec["ie_clip"] = clip_top3(c) if c and c.get("img_scores") and c.get("img_basic") else None
    recs.append(rec)

n_analysed = len(recs)
n_keys = len({r["key"] for r in recs}); n_repeat = n_analysed - n_keys
emo_all = [r for r in recs if r["emotional"]]
both = [r for r in emo_all if r["ie_clip"] is not None]          # records both readers cover
nonemo_both = [r for r in recs if not r["emotional"] and r["ie_clip"] is not None]
tie_ids = [i for i, c in clip.items() if c["img_basic"] != max((k for k in c["img_scores"] if not k.startswith("_")), key=c["img_scores"].get)]

print(f"analysed {n_analysed} (ids {min(r['id'] for r in recs)}..{max(r['id'] for r in recs)}); "
      f"distinct dedup_keys {n_keys}; records repeating an earlier prompt {n_repeat}")
print(f"emotional {len(emo_all)} / non-emotional {n_analysed-len(emo_all)}; "
      f"face {sum(r['face'] for r in recs)} / scene {sum(not r['face'] for r in recs)}; "
      f"within emotional face {sum(r['face'] for r in emo_all)} / scene {sum(not r['face'] for r in emo_all)}")
print(f"records both readers cover (emotional): {len(both)} of {len(emo_all)}; "
      f"direct-CLIP rounded-score ties resolved by img_basic: ids {sorted(tie_ids)}")

# ---------- subsets (all prompt- or record-defined, hence identical for both readers) ----------
SUBSETS = [  # same ORDER as analysis_final.block() so the RNG sequence after seed(7) is identical
    ("all_emotional",      both,                                              False),
    ("face_images",        [r for r in both if r["face"]],                    False),
    ("scene_images",       [r for r in both if not r["face"]],                False),
    ("positive_prompts",   [r for r in both if sign(r["prompt_top"]) == "+"], True),
    ("negative_prompts",   [r for r in both if sign(r["prompt_top"]) == "-"], True),
    ("non_emotional",      nonemo_both,                                       False),
]
READERS = [("describe_then_extract", "ie_describe"), ("direct_clip", "ie_clip")]

def score_reader(field):
    random.seed(SEED)                     # same seed, same call order -> identical shuffles for both readers
    out = {}
    for name, subset, degenerate in SUBSETS:
        pairs = [(r["pe"], r[field]) for r in subset]
        t, nm, ns = with_null(pairs, N_SHUFFLE)
        d = {"n": len(pairs), "n_sign_defined": sum(1 for r in subset if sign(r["prompt_top"]) != "0")}
        for k in ["vsign", "family", "overlap", "va"]:
            d[k] = {"value": round(t[k], 4), "null_mean": round(nm[k], 4), "null_sd": round(ns[k], 4),
                    "z": round((t[k] - nm[k]) / ns[k], 3)}
        if degenerate:
            d["note"] = ("single-sign subset: every prompt shares one sign, so the sign/family nulls are "
                         "degenerate (z=0 by construction); only VA and overlap are interpretable here")
        out[name] = d
    return out

METRIC_NAMES = {"vsign": "valence-sign agreement", "family": "family agreement",
                "overlap": "top-3 soft overlap", "va": "VA similarity"}
results = {rname: score_reader(field) for rname, field in READERS}

print("\n=== LIKE-FOR-LIKE: prompt reader = GoEmotions, same 607, same soft(), same 300 shuffles (seed 7) ===")
for sname, _, degenerate in SUBSETS:
    n = results["describe_then_extract"][sname]["n"]
    print(f"\n--- {sname} (n={n}){'  [single-sign: sign/family z degenerate]' if degenerate else ''}")
    print(f"  {'metric':24s} {'describe->extract':>32s} {'direct-CLIP':>32s}")
    for k in ["vsign", "family", "overlap", "va"]:
        a = results["describe_then_extract"][sname][k]; b = results["direct_clip"][sname][k]
        print(f"  {METRIC_NAMES[k]:24s} {a['value']:6.1%} vs null {a['null_mean']:6.1%} [z{a['z']:+5.1f}]"
              f"   {b['value']:6.1%} vs null {b['null_mean']:6.1%} [z{b['z']:+5.1f}]")

# ---------- reference check: describe-then-extract must reproduce analysis_final.py to the digit ----------
REFERENCE = {  # (subset, metric) -> (value %, null %, z or None) from analysis_final.py / rerun_af.log
    ("all_emotional", "vsign"):  (64.0, 45.6, 11.1),
    ("all_emotional", "family"): (53.1, 38.8, 10.3),   # brief says 53.1; 322/607 = 53.05% sits on the 1-dp boundary (published: "53%")
    ("face_images",   "vsign"):  (73.9, 53.5, None),
    ("scene_images",  "vsign"):  (42.9, 29.6, None),
    ("non_emotional", "va"):     (76.6, 76.6, None),
}
ref_rows = []; ref_ok = True
for (sname, k), (v, nm, z) in REFERENCE.items():
    got = results["describe_then_extract"][sname][k]
    TOL = 0.051   # pp; a rate of h/607 can land exactly on a 1-dp rounding boundary (322/607 = 53.05%)
    ok = (abs(got["value"]*100 - v) <= TOL) and (abs(got["null_mean"]*100 - nm) <= TOL) and (z is None or abs(got["z"] - z) <= 0.051)
    ref_ok &= ok
    ref_rows.append({"subset": sname, "metric": k, "expected": {"value_pct": v, "null_pct": nm, "z": z},
                     "got": {"value_pct": round(got["value"]*100, 2), "null_pct": round(got["null_mean"]*100, 2), "z": round(got["z"], 2)},
                     "ok": ok})
COUNT_REF = {"n_analysed": (n_analysed, 1012), "n_emotional": (len(emo_all), 607), "n_non_emotional": (n_analysed-len(emo_all), 405),
             "n_face": (sum(r["face"] for r in recs), 591), "n_scene": (sum(not r["face"] for r in recs), 421),
             "n_face_emotional": (sum(r["face"] for r in emo_all), 402), "n_scene_emotional": (sum(not r["face"] for r in emo_all), 205),
             "n_repeat_prompts": (n_repeat, 249)}
count_ok = all(g == e for g, e in COUNT_REF.values())
print(f"\nREFERENCE CHECK vs analysis_final.py: metrics {'PASS' if ref_ok else 'FAIL'}; counts {'PASS' if count_ok else 'FAIL'}")
for rr in ref_rows:
    print(f"  {rr['subset']:14s} {rr['metric']:7s} expected {rr['expected']}  got {rr['got']}  {'ok' if rr['ok'] else 'DIFFERS'}")

# ---------- PAIRED tests on per-record hit/miss ----------
def fam_hit(r, field):  return r["prompt_top"] == r[field][0][0]
def sign_hit(r, field): return sign(r["prompt_top"]) == sign(r[field][0][0])

def exact_mcnemar(b, c):
    """Two-sided exact binomial McNemar on the discordant counts (b = A-only hits, c = B-only hits)."""
    n = b + c
    if n == 0: return 1.0
    lo = min(b, c)
    p = 2 * sum(math.comb(n, k) for k in range(lo + 1)) / 2**n
    return min(1.0, p)

def paired_block(subset, hit, label):
    A = [hit(r, "ie_describe") for r in subset]; B = [hit(r, "ie_clip") for r in subset]
    n = len(subset)
    bb = sum(1 for a, b in zip(A, B) if a and not b); cc = sum(1 for a, b in zip(A, B) if b and not a)
    both_hit = sum(1 for a, b in zip(A, B) if a and b); both_miss = n - bb - cc - both_hit
    p_unclustered = exact_mcnemar(bb, cc)
    # cluster-level sign-flip randomisation: per-cluster sum of (hitA - hitB); flip whole clusters
    csum = defaultdict(int)
    for r, a, b in zip(subset, A, B): csum[r["key"]] += int(a) - int(b)
    diffs = [v for v in csum.values()]; n_clusters = len(diffs); n_informative = sum(1 for v in diffs if v != 0)
    obs = sum(diffs)                        # == bb - cc, the McNemar numerator
    rng = random.Random(SEED); DRAWS = 20000; cnt = 0
    for _ in range(DRAWS):
        t = sum(v if rng.random() < 0.5 else -v for v in diffs)
        if abs(t) >= abs(obs): cnt += 1
    p_cluster = (cnt + 1) / (DRAWS + 1)
    # clustered bootstrap CI for the difference in agreement rates (resample dedup_key clusters)
    groups = defaultdict(list)
    for r, a, b in zip(subset, A, B): groups[r["key"]].append((a, b))
    keys = list(groups); rng2 = random.Random(11); B_DRAWS = 10000; dd = []
    for _ in range(B_DRAWS):
        samp = [x for k in (rng2.choice(keys) for _ in keys) for x in groups[k]]
        dd.append(sum(a for a, _ in samp)/len(samp) - sum(b for _, b in samp)/len(samp))
    dd.sort(); q = lambda p: dd[int(p*(len(dd)-1))]
    out = {"n": n, "n_clusters_dedup_key": n_clusters, "n_clusters_with_nonzero_difference": n_informative,
           "describe_then_extract_hits": sum(A), "direct_clip_hits": sum(B),
           "describe_then_extract_rate": round(sum(A)/n, 4), "direct_clip_rate": round(sum(B)/n, 4),
           "difference_pp": round(100*(sum(A)-sum(B))/n, 1),
           "both_hit": both_hit, "both_miss": both_miss, "describe_only_hit_b": bb, "direct_clip_only_hit_c": cc,
           "mcnemar_exact_binomial_p_unclustered": p_unclustered,
           "cluster_sign_flip_p": round(p_cluster, 5), "cluster_sign_flip_draws": DRAWS,
           "clustered_bootstrap_95ci_difference_pp": [round(100*q(.025), 1), round(100*q(.975), 1)],
           "clustered_bootstrap_draws": B_DRAWS,
           "notes": [
               "hit = prompt-reader top-1 equals image-reader top-1 (" + label + ")",
               "the exact-binomial McNemar treats the discordant records as independent; it is OPTIMISTIC because "
               f"{n - n_clusters} of these {n} records repeat an earlier prompt (dedup_key), and repeats of one prompt "
               "are not independent evidence about the readers",
               "cluster_sign_flip_p: the McNemar statistic (b - c) under a randomisation that flips the sign of each "
               "dedup_key cluster's summed hit-difference as a block (readers exchangeable within a record => the "
               "cluster sum is symmetric about 0 under H0); this is the clustered version of the McNemar/sign test; "
               "two-sided; Monte-Carlo with seed 7",
               "clustered bootstrap: dedup_key clusters resampled with replacement, seed 11; CI on the "
               "describe-minus-CLIP difference in agreement rate"]}
    return out

paired = {"family_agreement": paired_block(both, fam_hit, "family"),
          "valence_sign_agreement": paired_block([r for r in both if sign(r["prompt_top"]) != "0"], sign_hit,
                                                 "valence sign; records whose prompt top-1 is surprise are excluded because sign(surprise)=0")}
print("\n=== PAIRED tests (describe-then-extract vs direct-CLIP, same records) ===")
for k, d in paired.items():
    print(f"  {k}: n={d['n']} ({d['n_clusters_dedup_key']} prompt clusters)  "
          f"describe {d['describe_then_extract_rate']:.1%} vs CLIP {d['direct_clip_rate']:.1%}  diff {d['difference_pp']:+.1f} pp  "
          f"b={d['describe_only_hit_b']} c={d['direct_clip_only_hit_c']}  "
          f"McNemar exact p={d['mcnemar_exact_binomial_p_unclustered']:.2e} (unclustered, optimistic)  "
          f"cluster sign-flip p={d['cluster_sign_flip_p']:.5f}  "
          f"clustered bootstrap 95% CI [{d['clustered_bootstrap_95ci_difference_pp'][0]:+.1f}, {d['clustered_bootstrap_95ci_difference_pp'][1]:+.1f}] pp")

# ---------- how often the two image readers agree with EACH OTHER ----------
def reader_vs_reader(subset):
    n = len(subset); same = sum(1 for r in subset if r["ie_describe"][0][0] == r["ie_clip"][0][0])
    conf = {f: {g: 0 for g in FAMILIES} for f in FAMILIES}
    for r in subset: conf[r["ie_describe"][0][0]][r["ie_clip"][0][0]] += 1
    return {"n": n, "top1_agreement": round(same/n, 4),
            "describe_top1_counts": {f: sum(1 for r in subset if r["ie_describe"][0][0] == f) for f in FAMILIES},
            "direct_clip_top1_counts": {f: sum(1 for r in subset if r["ie_clip"][0][0] == f) for f in FAMILIES},
            "confusion_describe_rows_clip_cols": conf}
rvr = {"emotional_607": reader_vs_reader(both),
       "all_analysed_1012": reader_vs_reader([r for r in recs if r["ie_clip"] is not None])}
print(f"\nimage reader vs image reader top-1 agreement: emotional {rvr['emotional_607']['top1_agreement']:.1%}, "
      f"all analysed {rvr['all_analysed_1012']['top1_agreement']:.1%}")

# ---------- the published v1 comparison, kept as-is and labelled ----------
v1 = {
    "label": "v1 (NLI prompt side) comparison",
    "source": "similarity_v2.py (printout preserved in outputs/rerun_s2.log; quoted in outputs/RESULTS_describe_extract.md, "
              "outputs/RESULTS_final.md, outputs/report_src/project_dossier.tex and make_figures.py fig2)",
    "status": "left untouched — it is NOT superseded as a record of what was published, but it is not like-for-like "
              "with analysis_final.py; use like_for_like above when comparing against the main analysis",
    "n_records": 608,
    "describe_then_extract": {"family": 0.493, "family_z": 11.2, "overlap": 0.486, "overlap_z": 14.0, "va": 0.837, "va_z": 14.2},
    "direct_clip":           {"family": 0.253, "family_z": 10.2, "overlap": 0.228, "overlap_z": 12.1, "va": 0.742, "va_z": 12.3},
    "why_not_like_for_like": [
        "prompt reader = BART-MNLI zero-shot (describe_extract.jsonl 'prompt_emotions'), whereas analysis_final.py uses GoEmotions",
        "subset = the 608 records the OLD lexicon prompt reader flagged is_emotional (results_clip_v2_baseline.json), not the 607 GoEmotions non-neutral prompts (606 ids in common)",
        "overlap = similarity_v2.soft_overlap (intersection / mean of the two raw sums), not analysis_final.soft() (each side normalised to 1 first)",
        "valence-sign agreement was not reported in the v1 comparison table"]}

# ---------- assemble & write ----------
def pct(x): return round(100*x, 1)
lfl = results["describe_then_extract"]["all_emotional"]; lfc = results["direct_clip"]["all_emotional"]
headline = {
    "n_records_both_readers_cover": len(both),
    "describe_then_extract": {k: {"pct": pct(lfl[k]["value"]), "null_pct": pct(lfl[k]["null_mean"]), "z": lfl[k]["z"]} for k in ["vsign", "family", "overlap", "va"]},
    "direct_clip":           {k: {"pct": pct(lfc[k]["value"]), "null_pct": pct(lfc[k]["null_mean"]), "z": lfc[k]["z"]} for k in ["vsign", "family", "overlap", "va"]},
    "family_agreement_difference_pp": paired["family_agreement"]["difference_pp"],
    "family_mcnemar_exact_p_unclustered": paired["family_agreement"]["mcnemar_exact_binomial_p_unclustered"],
    "family_cluster_sign_flip_p": paired["family_agreement"]["cluster_sign_flip_p"],
    "family_clustered_bootstrap_95ci_pp": paired["family_agreement"]["clustered_bootstrap_95ci_difference_pp"],
}
out = {
    "meta": {
        "script": "method_comparison.py",
        "purpose": "like-for-like comparison of the two image readers (describe-then-extract vs direct-CLIP) against the "
                   "SAME prompt reader, subset, overlap formula and null as analysis_final.py; the central quantity is "
                   "agreement between the prompt reader and the image reader",
        "prompt_reader": "GoEmotions (SamLowe/roberta-base-go_emotions) 28 -> 7 Ekman families, cached in outputs/prompt_emotions_goe.json",
        "analysed_ids": f"{min(r['id'] for r in recs)}..{max(r['id'] for r in recs)} (pre-test ids 1-{PRETEST_MAX_ID} dropped)",
        "n_analysed": n_analysed, "n_emotional": len(emo_all), "n_non_emotional": n_analysed - len(emo_all),
        "emotional_rule": "GoEmotions top-1 family != 'neutral'",
        "face_rule": "BLIP-VQA people-count >= 1 AND an EXPRESSION_WORDS token in the expression answer (analysis_final.is_face)",
        "n_face": sum(r["face"] for r in recs), "n_scene": sum(not r["face"] for r in recs),
        "n_face_emotional": sum(r["face"] for r in emo_all), "n_scene_emotional": sum(not r["face"] for r in emo_all),
        "n_distinct_dedup_keys": n_keys, "n_records_repeating_an_earlier_prompt": n_repeat,
        "null": f"{N_SHUFFLE} random re-pairings of images to prompts; random.seed({SEED}) set once per reader, subsets scored in "
                "analysis_final.py's order (all, face, scene, positive, negative, non-emotional) so both readers see identical shuffles "
                "and the describe-then-extract figures equal the published ones",
        "families": FAMILIES,
        "sign_rule": "joy=+ ; sadness/anger/fear/disgust=- ; surprise/neutral=0 (records with prompt sign 0 are excluded from valence-sign)",
        "metric_functions": "sign, va_point, va_sim, soft, metrics, with_null, is_face copied verbatim from analysis_final.py",
        "image_readers": {
            "describe_then_extract": "outputs/describe_extract.jsonl 'image_emotions' (BLIP-VQA description -> BART-MNLI zero-shot, top-3 of 7 families)",
            "direct_clip": "outputs/results_clip_v2_baseline.json rows[].img_scores (CLIP zero-shot softmax over 7 labels, rounded to 3 dp); "
                           "label map " + json.dumps(CLIP2FAM) + "; top-1 = img_basic (unrounded argmax; resolves 3-dp ties at ids " + str(sorted(tie_ids)) + "); "
                           "keys starting with '_' (_portrait_prob, _margin, _has_face) are diagnostics, not labels, and are dropped"},
        "coverage": {"describe_then_extract": n_analysed, "direct_clip": sum(1 for r in recs if r["ie_clip"] is not None),
                     "emotional_records_both_cover": len(both)},
    },
    "headline": headline,
    "like_for_like": {rname: results[rname] for rname, _ in READERS},
    "paired_tests": paired,
    "reader_vs_reader": rvr,
    "v1_nli_prompt_side_comparison": v1,
    "reference_check": {"passed": bool(ref_ok and count_ok),
                        "tolerance": "values compared within 0.051 pp / 0.051 z of the reference; needed only because 322/607 = 53.05% "
                                     "family agreement sits on the 1-dp rounding boundary (the brief quotes 53.1%, analysis_final.py prints 53%)",
                        "metrics": ref_rows,
                        "counts": {k: {"got": g, "expected": e, "ok": g == e} for k, (g, e) in COUNT_REF.items()}},
    "runtime_s": round(time.time() - T0, 1),
}
path = os.path.join(OUT, "method_comparison.json")
json.dump(out, open(path, "w"), indent=1)
print(f"\nsaved {os.path.relpath(path, ROOT)}  ({out['runtime_s']} s)")
