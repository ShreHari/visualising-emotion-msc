#!/usr/bin/env python3
"""
emoviz/inference.py — inferential statistics for the prompt-reader / image-reader AGREEMENT results.

Pure Python (+ numpy for vectorised resampling sums); no models. Reads the frozen outputs
(describe_extract.jsonl, prompt_emotions_goe.json), reproduces the point estimates of analysis_final.py
exactly, and then adds what that script does not give:

  (1) CLUSTERED BOOTSTRAP 95% CIs — 10,000 draws, resampling dedup_key GROUPS (prompt identity), seed 7 —
      for every subset x metric. Subsets: emotional, face, scene, non-emotional, all-analysed, and the
      distinct-prompt versions of emotional / face / scene. Metrics: valence-arousal similarity (va),
      valence-sign agreement (vsign), family agreement (family), top-3 overlap agreement (overlap).
      Non-emotional reports va only: vsign and family are degenerate there by the subset's definition.
  (2) The REPEATED-PROMPT CONSISTENCY result, scripted for the first time: the modal-family fraction of
      the image reader across the 87 dedup_key groups with >=2 records, its clustered bootstrap CI over
      groups, and a permutation null (image top-1 shuffled across all 1,012 analysed records, regrouped,
      1,000 draws, seed 7) with mean, sd, z — plus the same null at 300 draws, which is where the published
      "59.1%, z+4.9" comes from, and its seed sensitivity.
  (3) COHEN'S KAPPA for family agreement on each subset, from the 7x7 prompt-family x image-family
      confusion matrix, with a clustered bootstrap CI — so the agreement is comparable with other studies.
  (4) HOLM-BONFERRONI across the full table of z-scores that analysis_final.py prints (48 printed;
      12 flagged degenerate; 36 tested). z -> two-sided p by the normal approximation.
  (5) The stability of the headline z (emotional valence-sign) under seeds 1..5.

Clustering matters because 249 of the 1,012 analysed records repeat an earlier prompt. dedup_key on each
record is prompt identity, so every resample and permutation here clusters on it.

Every string here uses "agreement" for the central quantity — the degree to which the prompt reader and
the image reader return the same reading. Nothing here says what a drawing shows a person.

Writes outputs/inference.json only. Run:  .venv/bin/python inference.py
"""
import json, os, math, random, statistics as st, re, time, datetime
from collections import defaultdict, Counter
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
T0 = time.time()
SEED, B_BOOT, N_PERM, N_NULL = 7, 10000, 1000, 300
FAMILIES = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
FIDX = {f: i for i, f in enumerate(FAMILIES)}

# =====================================================================================================
# Copied VERBATIM from analysis_final.py (its lines 23-81). That script executes its whole analysis on
# import and rewrites outputs/analysis_final.csv, so it must NOT be imported; the block below is a
# byte-for-byte copy so every point estimate here is the same function of the same data.
# =====================================================================================================
PRETEST_MAX_ID = 13                       # ids 1-13 = pre-festival developer tests (timestamps 26 Aug-18 Sep)
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
    # token-intersection match so multi-word answers ("man is smiling") count (audit fix)
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
# =====================================================================================================
# end of the verbatim copy
# =====================================================================================================

METRICS = ["va", "vsign", "family", "overlap"]
METRIC_NAME = {"va": "valence-arousal similarity", "vsign": "valence-sign agreement",
               "family": "family agreement", "overlap": "top-3 overlap agreement"}

def r4(x):
    if x is None: return None
    x = float(x)
    return None if math.isnan(x) else round(x, 4)
def pct_ci(v):
    v = np.asarray(v, dtype=float); v = v[~np.isnan(v)]
    lo, hi = np.percentile(v, [2.5, 97.5])
    return [r4(lo), r4(hi)], r4(v.mean()), r4(v.std())

# ---------- load the frozen data, drop pre-test, attach the cached GoEmotions prompt reading ----------
rows = [json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8")]
rows = [r for r in rows if r["id"] > PRETEST_MAX_ID]
goe = {int(k): v for k, v in json.load(open(os.path.join(OUT, "prompt_emotions_goe.json"))).items()}
missing = [r["id"] for r in rows if r["id"] not in goe]
if missing: raise SystemExit(f"prompt-emotion cache missing ids {missing[:5]}")

recs = []
for r in rows:                                   # file order == id order, as in analysis_final.py
    pe = goe[r["id"]]; ie = r["image_emotions"]
    ptop, itop = pe[0][0], ie[0][0]
    recs.append({"id": r["id"], "key": r["dedup_key"], "pe": pe, "ie": ie, "ptop": ptop, "itop": itop,
                 "emotional": ptop != "neutral", "face": is_face(r.get("vqa", {})),
                 "va": va_sim(va_point(pe), va_point(ie)), "overlap": soft(pe, ie),
                 "vsd": sign(ptop) != "0", "vsagree": sign(ptop) != "0" and sign(ptop) == sign(itop),
                 "fam": ptop == itop})

# distinct prompts: first record per dedup_key, exactly as analysis_final.py builds them
seen = set(); distinct = []
for r in recs:
    if r["key"] not in seen: seen.add(r["key"]); distinct.append(r)

emo = [r for r in recs if r["emotional"]]; demo = [r for r in distinct if r["emotional"]]
SUBSETS = {
    "emotional":          emo,
    "face":               [r for r in emo if r["face"]],
    "scene":              [r for r in emo if not r["face"]],
    "non_emotional":      [r for r in recs if not r["emotional"]],
    "all_analysed":       recs,
    "distinct_emotional": demo,
    "distinct_face":      [r for r in demo if r["face"]],
    "distinct_scene":     [r for r in demo if not r["face"]],
}
SUBSET_NOTE = {
    "emotional": "analysed records whose GoEmotions top-1 family != neutral",
    "face": "emotional records where BLIP-VQA reports >=1 person AND an expression word",
    "scene": "emotional records not face-classified",
    "non_emotional": "analysed records whose GoEmotions top-1 family == neutral (va only; vsign and family are degenerate: every prompt sign is 0 and every prompt family is neutral, so neither can vary under resampling)",
    "all_analysed": "all 1,012 analysed records (ids 14..1025); vsign denominator = records with a signed prompt family",
    "distinct_emotional": "emotional, first record per dedup_key only",
    "distinct_face": "face, first record per dedup_key only",
    "distinct_scene": "scene, first record per dedup_key only",
}

# ---------- data facts (must reproduce, not re-derive) ----------
ids = [r["id"] for r in recs]
data = {"analysed": len(recs), "id_min": min(ids), "id_max": max(ids),
        "emotional": len(emo), "non_emotional": len(SUBSETS["non_emotional"]),
        "face_all": sum(r["face"] for r in recs), "scene_all": sum(not r["face"] for r in recs),
        "face_within_emotional": len(SUBSETS["face"]), "scene_within_emotional": len(SUBSETS["scene"]),
        "distinct_prompts": len(distinct), "records_repeating_an_earlier_prompt": len(recs) - len(distinct),
        "distinct_emotional": len(demo), "distinct_face": len(SUBSETS["distinct_face"]),
        "distinct_scene": len(SUBSETS["distinct_scene"])}
checks = []
def check(name, observed, expected, tol=0.0):
    ok = abs(observed - expected) <= tol if isinstance(expected, (int, float)) else observed == expected
    checks.append({"check": name, "observed": observed if isinstance(observed, int) else r4(observed),
                   "expected": expected, "ok": bool(ok)})
for k, v in [("analysed", 1012), ("id_min", 14), ("id_max", 1025), ("emotional", 607), ("non_emotional", 405),
             ("face_all", 591), ("scene_all", 421), ("face_within_emotional", 402), ("scene_within_emotional", 205),
             ("distinct_prompts", 763), ("records_repeating_an_earlier_prompt", 249)]:
    check(f"data.{k}", data[k], v)

# ---------- point estimates (metrics() on each subset) ----------
point = {name: metrics([(r["pe"], r["ie"]) for r in sub]) for name, sub in SUBSETS.items()}
REFERENCE_RATES = {("emotional", "vsign"): 0.640, ("emotional", "family"): 0.531, ("emotional", "va"): 0.838,
                   ("emotional", "overlap"): 0.506, ("face", "vsign"): 0.739, ("face", "family"): 0.619,
                   ("scene", "vsign"): 0.429, ("scene", "family"): 0.356, ("non_emotional", "va"): 0.766}
for (s, m), v in REFERENCE_RATES.items():
    check(f"point.{s}.{m}", point[s][m], v, tol=0.00101)   # references are quoted to 0.1 pp

# =====================================================================================================
# (1) CLUSTERED BOOTSTRAP CIs + (3) COHEN'S KAPPA — per subset, resampling dedup_key groups
# =====================================================================================================
def group_matrices(sub):
    groups = defaultdict(list)
    for r in sub: groups[r["key"]].append(r)
    keys = list(groups)
    S = np.zeros((len(keys), 6)); C = np.zeros((len(keys), 49))
    for gi, k in enumerate(keys):
        for r in groups[k]:
            S[gi] += [1.0, r["va"], float(r["vsd"]), float(r["vsagree"]), float(r["fam"]), r["overlap"]]
            C[gi, FIDX[r["ptop"]] * 7 + FIDX[r["itop"]]] += 1
    return keys, S, C

def stats_from(S, C):
    """S: (..., 6) per-draw sums; C: (..., 49) per-draw confusion. Same formulas as metrics()."""
    n = S[..., 0]
    va = S[..., 1] / n
    vsign = S[..., 3] / np.maximum(1.0, S[..., 2])
    fam = S[..., 4] / n
    ov = S[..., 5] / n
    m = C.reshape(C.shape[:-1] + (7, 7)); N = m.sum(axis=(-1, -2))
    po = np.trace(m, axis1=-2, axis2=-1) / N
    pe = (m.sum(-1) * m.sum(-2)).sum(-1) / N ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        kappa = np.where(1 - pe > 1e-12, (po - pe) / (1 - pe), np.nan)
    return {"va": va, "vsign": vsign, "family": fam, "overlap": ov, "kappa": kappa, "kappa_pe": pe}

bootstrap, kappa_out = {}, {}
for name, sub in SUBSETS.items():
    keys, S, C = group_matrices(sub)
    G = len(keys)
    obs = stats_from(S.sum(0), C.sum(0))
    # exact reproduction check: the vectorised sums must equal metrics() on the same pairs
    for m in METRICS: assert abs(float(obs[m]) - point[name][m]) < 1e-12, (name, m)
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, G, size=(B_BOOT, G))                    # G groups drawn with replacement
    W = np.stack([np.bincount(row, minlength=G) for row in idx]).astype(float)
    bs = stats_from(W @ S, W @ C)
    entry = {"n": len(sub), "groups": G, "draws": B_BOOT, "seed": SEED, "note": SUBSET_NOTE[name]}
    report = ["va"] if name == "non_emotional" else METRICS
    for m in report:
        ci, bm, bsd = pct_ci(bs[m])
        entry[m] = {"observed": r4(obs[m]), "ci95": ci, "boot_mean": bm, "boot_sd": bsd}
    if name == "non_emotional":
        entry["vsign"] = entry["family"] = "degenerate on this subset (prompt sign is 0 and prompt family is neutral for every record); not reported"
    bootstrap[name] = entry
    # kappa
    if name == "non_emotional":
        kappa_out[name] = {"n": len(sub), "kappa": 0.0, "note": "degenerate: every prompt family is neutral, so observed agreement equals chance agreement and kappa is 0 by construction; not a result"}
    else:
        ci, bm, bsd = pct_ci(bs["kappa"])
        kappa_out[name] = {"n": len(sub), "groups": G, "kappa": r4(obs["kappa"]),
                           "ci95": ci, "boot_mean": bm, "boot_sd": bsd,
                           "observed_agreement_po": r4(obs["family"]), "chance_agreement_pe": r4(obs["kappa_pe"]),
                           "confusion_7x7_prompt_rows_image_cols": C.sum(0).reshape(7, 7).astype(int).tolist()}
kappa_out["_families"] = FAMILIES
kappa_out["_note"] = ("Cohen's kappa on the 7x7 prompt-family x image-family confusion matrix. pe is chance "
                      "agreement from the two readers' marginals — the quantity the 300-shuffle random-pairing "
                      "null estimates for the family metric — so kappa ~= (observed - null) / (1 - null). "
                      "CIs are percentile intervals from the same clustered bootstrap as section (1).")

# cross-check with significance.py's published CIs (it resamples EMOTIONAL groups and then splits face/scene,
# so its intervals let the face/scene sizes vary; here each subset is resampled within itself)
PUBLISHED_SIG = {("face", "vsign"): [0.682, 0.792], ("scene", "vsign"): [0.333, 0.511],
                 ("face", "family"): [0.557, 0.680], ("scene", "family"): [0.267, 0.441]}
sig_compare = [{"subset": s, "metric": m, "this_ci95": bootstrap[s][m]["ci95"], "significance_py_ci95": v,
                "max_abs_diff_pp": r4(100 * max(abs(a - b) for a, b in zip(bootstrap[s][m]["ci95"], v)))}
               for (s, m), v in PUBLISHED_SIG.items()]

# =====================================================================================================
# (2) REPEATED-PROMPT CONSISTENCY — modal-family fraction across dedup_key groups with >=2 records
# =====================================================================================================
groups_all = defaultdict(list)
for pos, r in enumerate(recs): groups_all[r["key"]].append(pos)
runs = {k: p for k, p in groups_all.items() if len(p) >= 2}
run_pos = list(runs.values())
labels = [r["itop"] for r in recs]
vlabels = [sign(l) for l in labels]
def modal_frac(labs):  return Counter(labs).most_common(1)[0][1] / len(labs)
def mean_modal(labs):  return st.mean(modal_frac([labs[p] for p in ps]) for ps in run_pos)
cons_fam = [modal_frac([labels[p] for p in ps]) for ps in run_pos]
obs_fam, obs_val = st.mean(cons_fam), mean_modal(vlabels)
n_in_runs = sum(len(p) for p in run_pos)
check("consistency.groups_ge2", len(runs), 87); check("consistency.records_in_groups", n_in_runs, 336)
check("consistency.modal_family_fraction", obs_fam, 0.688, tol=0.0005)
check("consistency.modal_valence_fraction", obs_val, 0.745, tol=0.0005)

rng = np.random.default_rng(SEED)
cons_arr = np.array(cons_fam)
idx = rng.integers(0, len(cons_arr), size=(B_BOOT, len(cons_arr)))
cons_ci, cons_bm, cons_bsd = pct_ci(cons_arr[idx].mean(1))

def perm_null(pool_positions, n_draws, seed):
    """Shuffle image top-1 across the given record positions, regroup on dedup_key, recompute."""
    rng = random.Random(seed); out = []
    base = labels[:]
    pool_labels = [labels[p] for p in pool_positions]
    for _ in range(n_draws):
        sh = pool_labels[:]; rng.shuffle(sh)
        for p, l in zip(pool_positions, sh): base[p] = l
        out.append(mean_modal(base))
    return out
null_all = perm_null(list(range(len(recs))), N_PERM, SEED)             # across all 1,012 (the specified null)
null_336 = perm_null([p for ps in run_pos for p in ps], N_PERM, SEED)   # within the 336 grouped records only
null_300 = perm_null(list(range(len(recs))), N_NULL, SEED)                 # the 300-shuffle convention of analysis_final.py
cons_seed_rows = []                                                        # seed sensitivity of the consistency z
for s_ in range(1, 6):
    nul = perm_null(list(range(len(recs))), N_PERM, s_); mu_, sd_ = st.mean(nul), st.pstdev(nul)
    cons_seed_rows.append({"seed": s_, "draws": N_PERM, "null_mean": r4(mu_), "null_sd": r4(sd_), "z": round((obs_fam - mu_) / sd_, 2)})
def summarise_null(null, obs):
    mu, sd = st.mean(null), st.pstdev(null)
    return {"draws": len(null), "mean": r4(mu), "sd": r4(sd), "z": r4((obs - mu) / sd),
            "mean_as_quoted": f"{mu:.1%}", "z_as_quoted": f"{(obs - mu) / sd:+.1f}",   # from the raw values
            "p_perm_one_sided": r4((sum(1 for v in null if v >= obs) + 1) / (len(null) + 1)),
            "null_min": r4(min(null)), "null_max": r4(max(null))}
# valence version of the same test, for the record
vnull = []
rng_v = random.Random(SEED); pool = vlabels[:]
for _ in range(N_PERM):
    sh = pool[:]; rng_v.shuffle(sh); vnull.append(mean_modal(sh))
consistency = {
    "definition": ("within-group agreement of the image reader across repeated prompts: for each dedup_key group "
                   "with >=2 analysed records, the fraction of records sharing the group's modal image family; "
                   "reported as the mean over groups (each group weighted once, as data_audit_consistency.py does)"),
    "groups_ge2": len(runs), "records_in_groups": n_in_runs, "analysed": len(recs),
    "modal_family_fraction": r4(obs_fam),
    "fully_consistent_groups": sum(1 for c in cons_fam if c == 1.0),
    "bootstrap_ci95_over_groups": {"draws": B_BOOT, "seed": SEED, "ci95": cons_ci, "boot_mean": cons_bm, "boot_sd": cons_bsd},
    "permutation_null_shuffle_all_1012": {**summarise_null(null_all, obs_fam), "seed": SEED,
        "procedure": "image top-1 family shuffled across all 1,012 analysed records (random.Random(7).shuffle), records regrouped on their fixed dedup_key, mean modal-family fraction over the same 87 groups recomputed"},
    "permutation_null_shuffle_within_336": {**summarise_null(null_336, obs_fam), "seed": SEED,
        "procedure": "same, but the shuffle is restricted to the 336 records inside the 87 groups (secondary check)"},
    "permutation_null_shuffle_all_1012_300_draws": {**summarise_null(null_300, obs_fam), "seed": SEED,
        "procedure": "identical to the 1,000-draw null but with the 300-shuffle convention of analysis_final.py — this is the procedure behind the published 59.1% / z+4.9"},
    "permutation_null_seed_sensitivity_1000_draws": cons_seed_rows,
    "modal_valence_fraction": r4(obs_val),
    "valence_permutation_null_shuffle_all_1012": {**summarise_null(vnull, obs_val), "seed": SEED},
    "published_value_to_reconcile": {"null": 0.591, "z": 4.9, "where": "final/01_PROJECT_A_TO_Z.md §15-16, 02_VIVA_QUESTIONS.md, 03_REVISION_SHEET.md, 06_MOCK_VIVA.md — no script in the repository produced it"},
}
pn = consistency["permutation_null_shuffle_all_1012"]; p300 = consistency["permutation_null_shuffle_all_1012_300_draws"]
cz = [x["z"] for x in cons_seed_rows]
published_reproduced = p300["mean_as_quoted"] == "59.1%" and p300["z_as_quoted"] == "+4.9"
consistency["published_pair_reproduced_at_300_draws_seed_7"] = published_reproduced
consistency["reconciliation"] = (
    f"The published pair (null 59.1%, z+4.9) is {'reproduced exactly' if published_reproduced else 'NOT reproduced'} by the same "
    f"procedure at 300 draws, seed 7: null mean {p300['mean_as_quoted']} ({p300['mean']:.4f}), sd {p300['sd']:.4f}, z{p300['z_as_quoted']} ({p300['z']:+.2f}). "
    f"At the 1,000 draws specified for this script the null mean is {pn['mean']:.4f} (sd {pn['sd']:.4f}) and z{pn['z']:+.2f}; "
    f"across seeds 1..5 at 1,000 draws z ranges {min(cz):+.2f} to {max(cz):+.2f}. The null MEAN is stable; the published "
    f"z+4.9 sits at the top of the seed range because the 300-draw estimate of the null sd happened to be low "
    f"({p300['sd']:.4f} vs {pn['sd']:.4f}). Quote: modal-family fraction {obs_fam:.1%} against a permutation null of "
    f"{pn['mean']:.1%} (1,000 draws), z{pn['z']:+.1f}, permutation p = {pn['p_perm_one_sided']}, clustered bootstrap CI "
    f"[{cons_ci[0]:.1%}, {cons_ci[1]:.1%}], which excludes the null mean.")

# =====================================================================================================
# (4) the z-table analysis_final.py prints, reproduced exactly, then HOLM-BONFERRONI
# =====================================================================================================
# The frozen script seeds the module-level random with 7 once, then calls with_null() on these twelve
# subsets in this order (FULL block then DISTINCT block). Replaying the same calls on the same global
# random reproduces every printed z to the digit.
def block_subsets(base):
    e = [r for r in base if r["emotional"]]
    return [("ALL emotional", e), ("face images", [r for r in e if r["face"]]),
            ("scene images", [r for r in e if not r["face"]]),
            ("positive prompts", [r for r in e if sign(r["ptop"]) == "+"]),
            ("negative prompts", [r for r in e if sign(r["ptop"]) == "-"]),
            ("non-emotional", [r for r in base if not r["emotional"]])]
# what rerun_af.log shows (seed 7, 300 shuffles) — the published z-table, one decimal
PRINTED = {
 ("FULL", "ALL emotional"): (12.2, 11.1, 10.3, 11.6), ("FULL", "face images"): (11.2, 10.4, 10.3, 11.6),
 ("FULL", "scene images"): (6.0, 5.8, 4.4, 4.9),      ("FULL", "positive prompts"): (3.9, 0.0, 0.0, 2.3),
 ("FULL", "negative prompts"): (2.1, 0.0, 2.1, 3.0),  ("FULL", "non-emotional"): (0.3, 0.0, 0.0, 0.0),
 ("DISTINCT", "ALL emotional"): (10.6, 9.9, 9.3, 10.8), ("DISTINCT", "face images"): (9.7, 8.4, 8.1, 9.7),
 ("DISTINCT", "scene images"): (3.6, 3.5, 2.6, 3.1),  ("DISTINCT", "positive prompts"): (3.3, 0.0, 0.0, 1.9),
 ("DISTINCT", "negative prompts"): (1.6, 0.0, 2.1, 2.7), ("DISTINCT", "non-emotional"): (1.1, 0.0, 0.0, 0.8)}
DEGENERATE = {"positive prompts": {"vsign", "family"}, "negative prompts": {"vsign", "family"},
              "non-emotional": {"vsign", "family"}}
DEGEN_WHY = {"positive prompts": "single-sign subset: analysis_final.py flags sign/family nulls DEGENERATE (every prompt sign is +; every prompt family is joy)",
             "negative prompts": "single-sign subset: analysis_final.py flags sign/family nulls DEGENERATE (every prompt sign is -)",
             "non-emotional": "every prompt sign is 0 and every prompt family is neutral: sign and family cannot vary under shuffling (z is 0 by construction)"}
MAIN_TABLE = {"ALL emotional", "face images", "scene images"}

def p_two_sided(z): return math.erfc(abs(z) / math.sqrt(2))   # normal approximation

random.seed(SEED)
ztable = []; z_ref = None
for blk, base in [("FULL", recs), ("DISTINCT", distinct)]:
    for title, sub in block_subsets(base):
        t, nm, ns = with_null([(r["pe"], r["ie"]) for r in sub])
        for mi, m in enumerate(METRICS):
            z = (t[m] - nm[m]) / ns[m]
            printed = PRINTED[(blk, title)][mi]
            degenerate = m in DEGENERATE.get(title, set())
            ztable.append({"block": blk, "subset": title, "n": len(sub), "metric": m, "metric_name": METRIC_NAME[m],
                           "observed": r4(t[m]), "null_mean": r4(nm[m]), "null_sd": r4(ns[m]),
                           "z": round(z, 3), "z_printed_by_analysis_final": printed,
                           "reproduced_to_printed_digit": f"{z:+.1f}" == f"{printed:+.1f}",
                           "p_two_sided_normal": float(f"{p_two_sided(z):.3e}"),
                           "degenerate": degenerate, "degenerate_reason": DEGEN_WHY[title] if degenerate else None,
                           "in_main_table": title in MAIN_TABLE})
        if blk == "FULL" and title == "ALL emotional":
            z_ref = {"z_vsign": (t["vsign"] - nm["vsign"]) / ns["vsign"], "null_mean": nm["vsign"], "null_sd": ns["vsign"]}
            check("null.emotional.vsign.null_mean", nm["vsign"], 0.456, tol=0.00101)
            check("null.emotional.family.null_mean", nm["family"], 0.388, tol=0.00101)
            check("null.emotional.overlap.null_mean", nm["overlap"], 0.394, tol=0.00101)
            check("null.emotional.va.null_mean", nm["va"], 0.773, tol=0.00101)
        if blk == "FULL" and title == "face images":
            check("null.face.vsign.null_mean", nm["vsign"], 0.535, tol=0.00101); check("null.face.family.null_mean", nm["family"], 0.458, tol=0.00101)
        if blk == "FULL" and title == "scene images":
            check("null.scene.vsign.null_mean", nm["vsign"], 0.296, tol=0.00101); check("null.scene.family.null_mean", nm["family"], 0.262, tol=0.00101)
        if blk == "FULL" and title == "non-emotional": check("null.non_emotional.va.null_mean", nm["va"], 0.766, tol=0.00101)
n_repro = sum(e["reproduced_to_printed_digit"] for e in ztable)
check("ztable.printed_z_reproduced_of_48", n_repro, 48)

def holm(entries, alpha=0.05):
    order = sorted(entries, key=lambda e: e["p_two_sided_normal"])
    m = len(order); alive = True; out = []
    for rank, e in enumerate(order, 1):
        thr = alpha / (m - rank + 1)
        if e["p_two_sided_normal"] > thr: alive = False
        out.append({"rank": rank, "block": e["block"], "subset": e["subset"], "metric": e["metric"], "z": e["z"],
                    "p": e["p_two_sided_normal"], "holm_threshold": float(f"{thr:.3e}"),
                    "holm_threshold_as_z": round(math.sqrt(2) * _erfcinv(thr), 2), "survives": alive,
                    "bonferroni_survives": e["p_two_sided_normal"] <= alpha / m})
    return out
def _erfcinv(p):
    # two-sided normal quantile for a p-value: |z| such that erfc(|z|/sqrt2) = p; bisection is plenty here
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if math.erfc(mid) > p: lo = mid
        else: hi = mid
    return (lo + hi) / 2

tested = [e for e in ztable if not e["degenerate"]]
main = [e for e in tested if e["in_main_table"]]
holm_all, holm_main = holm(tested), holm(main)
def survivors(h, yes, key="survives"): return [f"{x['block']} {x['subset']} {x['metric']} z{x['z']:+.1f}" for x in h if x[key] == yes]
def family_summary(h, m):
    return {"m": m, "bonferroni_z_for_smallest_rank": round(math.sqrt(2) * _erfcinv(0.05 / m), 2),
            "holm_n_survive": sum(x["survives"] for x in h), "holm_n_do_not_survive": sum(not x["survives"] for x in h),
            "survive": survivors(h, True), "do_not_survive": survivors(h, False),
            "bonferroni_n_survive": sum(x["bonferroni_survives"] for x in h),
            "bonferroni_do_not_survive": survivors(h, False, "bonferroni_survives"), "table": h}
def find_row(h, blk, sub, m): return next(x for x in h if x["block"] == blk and x["subset"] == sub and x["metric"] == m)
holm_out = {
    "assumption": ("Each z is converted to a two-sided p by the normal approximation p = erfc(|z|/sqrt(2)), i.e. the "
                   "300-shuffle null is treated as normal with its sample sd taken as known. For z above ~5 the p is "
                   "nominal (the sd is estimated from 300 draws), but the ordering, and the Holm decisions, do not depend on it."),
    "printed_z_values": 48, "flagged_degenerate_excluded": len(ztable) - len(tested), "tested": len(tested),
    "degenerate_excluded_list": [f"{e['block']} {e['subset']} {e['metric']} (z{e['z']:+.1f}; {e['degenerate_reason']})" for e in ztable if e["degenerate"]],
    "family_wise_alpha": 0.05,
    "primary_family_all_non_degenerate": family_summary(holm_all, len(tested)),
    "secondary_family_main_table_only": {"definition": "emotional / face / scene x four metrics x FULL and DISTINCT blocks",
                                         **family_summary(holm_main, len(main))},
    "z_table": ztable,
}
dsf_all, dsf_main = find_row(holm_all, "DISTINCT", "scene images", "family"), find_row(holm_main, "DISTINCT", "scene images", "family")
holm_out["distinct_scene_family"] = {
    "z": dsf_all["z"], "p_two_sided": dsf_all["p"],
    "holm_all_36_survives": dsf_all["survives"], "bonferroni_all_36_survives": dsf_all["bonferroni_survives"],
    "holm_main_24_survives": dsf_main["survives"], "bonferroni_main_24_survives": dsf_main["bonferroni_survives"],
    "reading": ("the weakest of the main-table z-values; it fails Holm over all 36 tested z (the step-down stops at DISTINCT "
                "negative-prompt overlap z+2.7 before reaching it) and fails plain Bonferroni in both families; it survives only "
                "Holm restricted to the 24 main-table tests, where as the last-ranked test it faces the uncorrected 0.05 "
                "threshold — report it as not robust to multiplicity")}

# =====================================================================================================
# (5) stability of the headline z (emotional valence-sign) across seeds 1..5
# =====================================================================================================
epairs = [(r["pe"], r["ie"]) for r in emo]
seed_rows = []
for s in range(1, 6):
    random.seed(s); t, nm, ns = with_null(epairs)
    seed_rows.append({"seed": s, "shuffles": N_NULL, "observed_vsign": r4(t["vsign"]), "null_mean": r4(nm["vsign"]),
                      "null_sd": r4(ns["vsign"]), "z": round((t["vsign"] - nm["vsign"]) / ns["vsign"], 2)})
zs = [x["z"] for x in seed_rows]
seed_out = {"metric": "valence-sign agreement, emotional prompts (n=607), 300 shuffles per seed",
            "seed_7_first_call_reference": {"z": round(z_ref["z_vsign"], 2), "null_mean": r4(z_ref["null_mean"]), "null_sd": r4(z_ref["null_sd"])},
            "seeds_1_to_5": seed_rows, "z_min": min(zs), "z_max": max(zs), "z_range_width": round(max(zs) - min(zs), 2),
            "null_mean_min": min(x["null_mean"] for x in seed_rows), "null_mean_max": max(x["null_mean"] for x in seed_rows),
            "null_sd_min": min(x["null_sd"] for x in seed_rows), "null_sd_max": max(x["null_sd"] for x in seed_rows),
            "reading": "the null MEAN is stable to a fraction of a point across seeds; the z moves with the 300-draw estimate of the null sd, so z is an ordering statistic here, not a precise quantity"}

# =====================================================================================================
# write
# =====================================================================================================
failed = [c for c in checks if not c["ok"]]
if failed:
    for c in failed: print("REFERENCE MISMATCH:", c)
    raise SystemExit("reference cross-check failed; outputs/inference.json NOT written")

result = {
    "script": "inference.py", "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    "seed": SEED, "bootstrap_draws": B_BOOT, "permutation_draws": N_PERM, "null_shuffles": N_NULL,
    "runtime_s": None,
    "quantity": ("agreement between the prompt reader (GoEmotions on the self-report) and the image reader "
                 "(zero-shot NLI on the BLIP-VQA description) — nothing here is a statement about what a person would see"),
    "clustering": "every resample and permutation clusters on dedup_key (prompt identity): 249 of the 1,012 analysed records repeat an earlier prompt",
    "data": data,
    "reference_cross_checks": checks,
    "published_rounding_discrepancies": [
        {"quantity": "emotional prompts (n=607), family agreement", "exact": r4(point["emotional"]["family"]),
         "count": f"{sum(r['fam'] for r in emo)}/{len(emo)}", "prints_as": f"{point['emotional']['family']:.1%}",
         "published_as": "53.1%", "where": "final/01_PROJECT_A_TO_Z.md, 02_VIVA_QUESTIONS.md, 06_MOCK_VIVA.md, CLAUDE_DESIGN_PROMPT.md",
         "note": "0.05 pp rounding slip; rerun_af.log and the earlier analysis_final.log both print 53% / 53.0%. Every other published rate and null mean matches to the quoted digit."}],
    "bootstrap_ci95_clustered": bootstrap,
    "bootstrap_vs_significance_py": {"note": "significance.py resamples emotional prompt groups and splits face/scene inside each draw; here each subset is resampled within itself. Intervals agree to within the stated pp.", "rows": sig_compare},
    "consistency_repeated_prompts": consistency,
    "cohens_kappa_family_agreement": kappa_out,
    "holm_bonferroni": holm_out,
    "z_seed_stability": seed_out,
}
result["runtime_s"] = round(time.time() - T0, 1)
json.dump(result, open(os.path.join(OUT, "inference.json"), "w"), indent=1)

# ---------- console summary ----------
print(f"=== inference.py — {len(recs)} analysed records, seed {SEED} ===")
print(f"reference cross-checks: {sum(c['ok'] for c in checks)}/{len(checks)} ok; printed z reproduced {n_repro}/48")
print("\n(1) clustered bootstrap 95% CIs (10,000 draws over dedup_key groups)")
for name, e in bootstrap.items():
    parts = [f"{m} {e[m]['observed']:.1%} [{e[m]['ci95'][0]:.1%}, {e[m]['ci95'][1]:.1%}]" for m in METRICS if isinstance(e.get(m), dict)]
    print(f"  {name:20s} n={e['n']:4d} G={e['groups']:3d}  " + "  ".join(parts))
print("\n(2) repeated-prompt consistency")
print(f"  modal-family fraction {obs_fam:.1%} over {len(runs)} groups / {n_in_runs} records; bootstrap CI [{cons_ci[0]:.1%}, {cons_ci[1]:.1%}]")
print(f"  permutation null (shuffle all 1,012): mean {pn['mean']:.1%} sd {pn['sd']:.1%} z{pn['z']:+.1f} p={pn['p_perm_one_sided']}")
p3 = consistency["permutation_null_shuffle_within_336"]
print(f"  permutation null (shuffle within 336): mean {p3['mean']:.1%} sd {p3['sd']:.1%} z{p3['z']:+.1f}")
print(f"  permutation null at 300 draws (published convention): mean {p300['mean_as_quoted']} sd {p300['sd']:.1%} z{p300['z_as_quoted']}")
print(f"  reconciliation: {consistency['reconciliation']}")
print("\n(3) Cohen's kappa (family agreement)")
for name, e in kappa_out.items():
    if name.startswith("_"): continue
    if "ci95" in e: print(f"  {name:20s} kappa {e['kappa']:+.3f} [{e['ci95'][0]:+.3f}, {e['ci95'][1]:+.3f}]  po {e['observed_agreement_po']:.3f} pe {e['chance_agreement_pe']:.3f}")
    else: print(f"  {name:20s} {e['note']}")
print(f"\n(4) Holm-Bonferroni over {len(tested)} non-degenerate z (of 48 printed); smallest-rank z threshold {holm_out['primary_family_all_non_degenerate']['bonferroni_z_for_smallest_rank']}")
print("  do NOT survive Holm:", *holm_out["primary_family_all_non_degenerate"]["do_not_survive"], sep="\n    ")
print(f"  main-table family (m={len(main)}): Holm survivors {holm_out['secondary_family_main_table_only']['holm_n_survive']}/{len(main)}; "
      f"Bonferroni failures: {holm_out['secondary_family_main_table_only']['bonferroni_do_not_survive']}")
print(f"  distinct scene family: {holm_out['distinct_scene_family']}")
print("\n(5) emotional valence-sign z across seeds 1..5:", zs, f"(seed 7 reference {seed_out['seed_7_first_call_reference']['z']:+.2f})")
print(f"\nsaved outputs/inference.json  ({result['runtime_s']} s)")
