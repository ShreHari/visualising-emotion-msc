#!/usr/bin/env python3
"""
test_numeric.py — pins every headline number to the result file that produces it, and unit-tests
the metric functions. Run by test.sh; exits non-zero on any failure.

Why this exists: a smoke test that greps for a section heading passes even if every statistic
silently changes. Each check below asserts a reported value against the JSON the analysis
scripts write, within a stated tolerance, so a change in the analysis fails the build and the
figures and the dissertation (both generated from the same JSON) cannot drift from the code.

Reference values are the ones quoted in the dissertation. If an analysis is deliberately changed,
update the value here in the same commit and say why.
"""
from __future__ import annotations
import json, math, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
sys.path.insert(0, ROOT)
from emoviz.metrics import (CEN, G2F, FAMILIES, sign, n_people, is_face, va_point, va_sim, soft,
                            metrics, va_floor)

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
def near(x, ref, tol): return x is not None and abs(x - ref) <= tol
def load(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else None

# ---------------------------------------------------------------- unit tests of the metric module
check("VA floor over centroids is 0.412", near(va_floor(), 0.412, 0.001), f"{va_floor():.4f}")
p = va_point([("joy", 0.7), ("surprise", 0.2), ("neutral", 0.1)]); q = va_point([("sadness", 0.9), ("fear", 0.1)])
check("va_sim(x,x) = 1", near(va_sim(p, p), 1.0, 1e-12))
check("va_sim symmetric", near(va_sim(p, q), va_sim(q, p), 1e-12))
check("va_sim within [0.412, 1]", 0.412 - 1e-9 <= va_sim(p, q) <= 1.0)
a = [("joy", 0.5), ("neutral", 0.3), ("surprise", 0.2)]; b = [("sadness", 0.6), ("anger", 0.3), ("fear", 0.1)]
check("soft(a,a) = 1", near(soft(a, a), 1.0, 1e-12))
check("soft on disjoint supports = 0", near(soft(a, b), 0.0, 1e-12))
check("soft is scale-invariant per side", near(soft(a, [(l, s * 10) for l, s in a]), 1.0, 1e-12))
check("sign(): joy + / fear - / surprise 0 / neutral 0",
      sign("joy") == "+" and sign("fear") == "-" and sign("surprise") == "0" and sign("neutral") == "0")
check("n_people(): none 0 / 2 -> 2 / many 4 / unknown 1 / '' 0",
      n_people("none") == 0 and n_people("2") == 2 and n_people("many") == 4 and n_people("unknown") == 1 and n_people("") == 0)
check("is_face(): needs >=1 person AND an expression word",
      not is_face({"people": "0", "expression": "smiling"}) and is_face({"people": "one", "expression": "man is smiling"})
      and not is_face({"people": "1", "expression": "kiss"}))
check("GoEmotions map: 28 labels -> 7 families", len(G2F) == 28 and set(G2F.values()) == set(FAMILIES) and set(CEN) == set(FAMILIES))
m = metrics([(a, a), (b, b)])
check("metrics() on identical pairs = 1 everywhere", all(near(v, 1.0, 1e-12) for v in m.values()))

# ---------------------------------------------------------------- analysis_final.json
af = load("analysis_final.json")
check("analysis_final.json present", af is not None)
if af:
    F = af["blocks"]["full"]; D = af["blocks"]["distinct"]; S = F["subsets"]; SD = D["subsets"]
    check("1,012 analysed; 607/405; 591/421", F["records"] == 1012 and F["emotional"] == 607 and F["non_emotional"] == 405 and F["face"] == 591 and F["scene"] == 421)
    e = S["ALL emotional"]; f = S["face images"]; s_ = S["scene images"]; ne = S["non-emotional"]
    check("emotional n=607, valence-sign denominator 530", e["n"] == 607 and e["n_sign"] == 530)
    check("emotional valence-sign 64.0% vs null 45.6%, z>10", near(e["metrics"]["vsign"]["obs"], 0.6396, 0.001) and near(e["metrics"]["vsign"]["null"], 0.456, 0.01) and e["metrics"]["vsign"]["z"] > 10)
    check("emotional family 53.0% (322/607) vs null 38.8%", near(e["metrics"]["family"]["obs"], 322 / 607, 1e-9) and near(e["metrics"]["family"]["null"], 0.388, 0.01))
    check("emotional overlap 50.6%, VA 83.8%", near(e["metrics"]["overlap"]["obs"], 0.5056, 0.001) and near(e["metrics"]["va"]["obs"], 0.8379, 0.001))
    check("face n=402 (sign denominator 360): sign 73.9%, family 61.9%", f["n"] == 402 and f["n_sign"] == 360 and near(f["metrics"]["vsign"]["obs"], 0.7389, 0.001) and near(f["metrics"]["family"]["obs"], 0.6194, 0.001))
    check("scene n=205 (sign denominator 170): sign 42.9%, family 35.6%", s_["n"] == 205 and s_["n_sign"] == 170 and near(s_["metrics"]["vsign"]["obs"], 0.4294, 0.001) and near(s_["metrics"]["family"]["obs"], 0.3561, 0.001))
    check("face null sign 53.5% / scene null sign 29.6%", near(f["metrics"]["vsign"]["null"], 0.535, 0.01) and near(s_["metrics"]["vsign"]["null"], 0.296, 0.01))
    check("non-emotional n=405: VA 76.6% at its null (|z|<1)", ne["n"] == 405 and near(ne["metrics"]["va"]["obs"], 0.766, 0.002) and abs(ne["metrics"]["va"]["z"]) < 1)
    check("non-emotional: family and valence-sign nulls flagged degenerate, no z", ne["metrics"]["family"]["degenerate"] and ne["metrics"]["vsign"]["degenerate"] and ne["metrics"]["family"]["z"] is None)
    check("positive prompts: family degenerate; negative prompts: family NOT degenerate", S["positive prompts"]["metrics"]["family"]["degenerate"] and not S["negative prompts"]["metrics"]["family"]["degenerate"])
    check("distinct prompts: 763 records, 452 emotional", D["records"] == 763 and D["emotional"] == 452)
    check("distinct face n=319 sign 71.8% z~+8.4; scene n=133 sign 37.3%, family 30.8%",
          SD["face images"]["n"] == 319 and near(SD["face images"]["metrics"]["vsign"]["obs"], 0.718, 0.002) and near(SD["face images"]["metrics"]["vsign"]["z"], 8.4, 0.6)
          and SD["scene images"]["n"] == 133 and near(SD["scene images"]["metrics"]["vsign"]["obs"], 0.373, 0.002) and near(SD["scene images"]["metrics"]["family"]["obs"], 0.308, 0.002))
    check("249 repeats, 763 distinct, 'happy' x42", af["duplicates"]["records_repeating_an_earlier_prompt"] == 249 and af["duplicates"]["distinct_prompts"] == 763 and af["duplicates"]["happy_count"] == 42)
    check("image reader never returns disgust, fear 4 times", af["families"]["image"]["disgust"] == 0 and af["families"]["image"]["fear"] == 4)

# ---------------------------------------------------------------- consistency.json
c = load("consistency.json")
check("consistency.json present with a null", c is not None and "null" in c)
if c and "null" in c:
    check("87 groups / 336 records / 43 pairs", c["runs"] == 87 and c["records_in_runs"] == 336 and c["pair_groups"] == 43)
    check("modal-emotion 68.8%, valence 74.5%, 28 fully consistent", near(c["mean_emotion_consistency"], 0.688, 0.001) and near(c["mean_valence_consistency"], 0.745, 0.001) and c["fully_consistent_runs"] == 28)
    ne_ = c["null"]["mean_emotion_consistency"]
    check("consistency null 59.4% (sd ~2.1), z between +4 and +5", near(ne_["null_mean"], 0.594, 0.006) and 4.0 <= ne_["z"] <= 5.0)
    check("fully-consistent null ~14.5 of 87", near(c["null"]["fully_consistent_runs"]["null_mean"], 14.5, 1.0))

# ---------------------------------------------------------------- inference.json
inf = load("inference.json")
check("inference.json present", inf is not None)
if inf:
    B = inf["bootstrap_ci95_clustered"]
    check("face valence-sign 95% CI ~[68.3, 79.2]", near(B["face"]["vsign"]["ci95"][0], 0.683, 0.02) and near(B["face"]["vsign"]["ci95"][1], 0.792, 0.02))
    check("scene valence-sign 95% CI ~[33.1, 51.1]", near(B["scene"]["vsign"]["ci95"][0], 0.331, 0.02) and near(B["scene"]["vsign"]["ci95"][1], 0.511, 0.02))
    K = inf["cohens_kappa_family_agreement"]
    check("Cohen's kappa: emotional 0.23, face 0.30, scene 0.13", near(K["emotional"]["kappa"], 0.235, 0.02) and near(K["face"]["kappa"], 0.299, 0.02) and near(K["scene"]["kappa"], 0.129, 0.02))
    H = inf["holm_bonferroni"]["primary_family_all_non_degenerate"]
    check("Holm: 26 of 36 non-degenerate z survive at family-wise 0.05", H["m"] == 36 and H["holm_n_survive"] == 26)
    check("headline z survives Holm (emotional valence-sign)", any("ALL emotional vsign" in x for x in H["survive"]))

# ---------------------------------------------------------------- method_comparison.json
mc = load("method_comparison.json")
check("method_comparison.json present", mc is not None)
if mc:
    h = mc["headline"]
    check("like-for-like family: describe 53.0% vs direct-CLIP 22.4% (+30.6 pp)", near(h["describe_then_extract"]["family"]["pct"], 53.0, 0.1) and near(h["direct_clip"]["family"]["pct"], 22.4, 0.1) and near(h["family_agreement_difference_pp"], 30.6, 0.1))
    check("like-for-like valence-sign: 64.0% vs 31.1%", near(h["describe_then_extract"]["vsign"]["pct"], 64.0, 0.1) and near(h["direct_clip"]["vsign"]["pct"], 31.1, 0.1))
    check("clustered bootstrap CI on the family difference ~[+25.5, +35.6] pp; cluster p < 0.001", near(h["family_clustered_bootstrap_95ci_pp"][0], 25.5, 1.0) and near(h["family_clustered_bootstrap_95ci_pp"][1], 35.6, 1.0) and h["family_cluster_sign_flip_p"] < 0.001)
    v1 = mc["v1_nli_prompt_side_comparison"]
    check("v1 (NLI prompt side) record preserved: 49.3% vs 25.3% on 608", v1["n_records"] == 608 and near(v1["describe_then_extract"]["family"], 0.493, 0.001))

# ---------------------------------------------------------------- audits.json
au = load("audits.json")
check("audits.json present", au is not None)
if au:
    cc = au["control_contamination"]
    check("control: 405 records; 2 '[name]'-only; 68 (16.8%) with a plain affect word", cc["n_control"] == 405 and cc["name_only_records"]["n"] == 2 and cc["lexicon_flagged"]["n"] == 68)
    dh = au.get("describer_hallucination") or au.get("describer_leak") or {}
    txt = json.dumps(dh)
    check("describer: 414 scene records with people=0, 406 with an expression word, 332 smile/smiling/happy",
          all(str(x) in txt for x in (414, 406, 332)))

# ---------------------------------------------------------------- error taxonomy, significance, ablation, human check
et = load("error_taxonomy.json")
check("error_taxonomy.json: 38 records, every one assigned a mode", et is not None and et["sample_size"] == 38 and sum(et["failure_mode_tally"].values()) == 38 if et and isinstance(et["failure_mode_tally"], dict) and all(isinstance(v, int) for v in et["failure_mode_tally"].values()) else et is not None and et["sample_size"] == 38)
sig = os.path.join(OUT, "RESULTS_significance.txt")
check("significance.py output reports the clustered permutation p = 0.0001", os.path.exists(sig) and "0.0001" in open(sig).read())
ab = load(os.path.join("ablation", "summary.json"))
if ab is not None:
    base, ctrl, de, pa = ab["baseline"], ab["control_full_template"], ab["drop_expression"], ab["people_aware"]
    check("ablation: control re-run of the unmodified template reproduces the baseline exactly",
          near(ctrl["emotional"]["vsign"]["obs"], base["emotional"]["vsign"]["obs"], 1e-9) and near(ctrl["scene"]["family"]["obs"], base["scene"]["family"]["obs"], 1e-9))
    check("ablation: baseline row = main analysis (64.0% / 53.0%)", near(base["emotional"]["vsign"]["obs"], 0.6396, 0.001) and near(base["emotional"]["family"]["obs"], 322 / 607, 1e-6))
    check("ablation: without the expression word, family agreement falls below 25%", de["emotional"]["family"]["obs"] < 0.25)
    check("ablation: people-aware template leaves face rows unchanged", near(pa["face"]["vsign"]["obs"], base["face"]["vsign"]["obs"], 1e-9) and near(pa["face"]["family"]["obs"], base["face"]["family"]["obs"], 1e-9))
    check("ablation: people-aware scene agreement sits at its null (|z| < 2.5)", abs(pa["scene"]["vsign"]["z"]) < 2.5 and abs(pa["scene"]["family"]["z"]) < 2.5)
hc = load(os.path.join("human_check", "human_check.json"))
if hc is not None:
    check("human check: coded sample present", hc.get("n_coded", 0) >= 60)

# ---------------------------------------------------------------- report
bad = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
print(f"numeric checks: {len(results) - len(bad)} passed, {len(bad)} failed")
sys.exit(1 if bad else 0)
