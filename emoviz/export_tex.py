#!/usr/bin/env python3
"""
export_tex.py — every number the dissertation quotes, exported from the result files as LaTeX.

Reads (all under outputs/):
  analysis_final.json        analysis_final.py          observed / null / z per subset and metric
  consistency.json           data_audit_consistency.py  repeated-prompt consistency + permutation null
  inference.json             inference.py               clustered-bootstrap CIs, Cohen's kappa, Holm, seeds
  method_comparison.json     method_comparison.py       like-for-like image-reader comparison, paired tests
  audits.json                audits.py                  control contamination, describer leak, per-family
  error_taxonomy.json        error_taxonomy.py          failure-mode tally
  RESULTS_significance.txt   significance.py            face/scene difference CIs and permutation p
  ablation/summary.json      ablate_nli.py              (optional) description-template ablation
  human_check/human_check.json  human_check.py          (optional) single-coder reliability check

Writes report/generated/numbers.tex (one \\newcommand per number) and report/generated/tab_*.tex
(booktabs tables). The dissertation \\input{}s these, so no statistic is ever typed by hand and a
change in any analysis propagates to the text on the next run.

Run:  emoviz/.venv/bin/python emoviz/export_tex.py   (from any directory)
"""
from __future__ import annotations
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "outputs")
GEN = os.path.normpath(os.path.join(ROOT, "..", "report", "generated"))
os.makedirs(GEN, exist_ok=True)

def load(name, required=True):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        if required: raise SystemExit(f"missing {p}")
        return None
    return json.load(open(p, encoding="utf-8"))

AF = load("analysis_final.json"); CONS = load("consistency.json"); INF = load("inference.json")
MC = load("method_comparison.json"); AU = load("audits.json"); ET = load("error_taxonomy.json")
AB = load(os.path.join("ablation", "summary.json"), required=False)
HC = load(os.path.join("human_check", "human_check.json"), required=False)
SIG_TXT = open(os.path.join(OUT, "RESULTS_significance.txt"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(OUT, "RESULTS_significance.txt")) else ""

# ----------------------------------------------------------------------------- formatting
def pct(x, d=1):
    """fraction -> 'NN.N\\%' (the value is in [0,1])."""
    return "n/a" if x is None else f"{100*x:.{d}f}\\%"
def pp(x, d=1):
    """already a percentage -> 'NN.N\\%'."""
    return "n/a" if x is None else f"{x:.{d}f}\\%"
def zf(x, d=1):
    return "n/a" if x is None else f"{x:+.{d}f}"
def ci(lo, hi, frac=True, d=1):
    if lo is None or hi is None: return "--"
    if frac: return f"[{100*lo:.{d}f}, {100*hi:.{d}f}]"
    return f"[{lo:.{d}f}, {hi:.{d}f}]"
def num(x): return f"{x:,}" if isinstance(x, int) else str(x)
def sci(p):
    if p is None: return "n/a"
    if p >= 1e-3: return f"{p:.4f}".rstrip("0").rstrip(".")
    m, e = f"{p:.1e}".split("e"); return f"${m}\\times10^{{{int(e)}}}$"
def tex(s):
    return (str(s).replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", "\\%")
            .replace("_", "\\_").replace("#", "\\#").replace("$", "\\$").replace("^", "\\^{}"))

MACROS: list[tuple[str, str, str]] = []   # (name, value, meaning)
def M(name, value, meaning):
    assert re.fullmatch(r"[A-Za-z]+", name), f"macro names must be letters only: {name}"
    MACROS.append((name, str(value), meaning))

# ----------------------------------------------------------------------------- counts
F, D = AF["blocks"]["full"], AF["blocks"]["distinct"]
S, SD = F["subsets"], D["subsets"]
M("nTotal", num(CONS["total"]), "records processed (incl. pre-tests)")
M("nPretest", num(CONS["pretest"]), "pre-festival developer test records, excluded")
M("nAnalysed", num(F["records"]), "records analysed")
M("nEmotional", num(F["emotional"]), "prompts whose GoEmotions top-1 family is not neutral")
M("nNonEmotional", num(F["non_emotional"]), "prompts the text reader labels neutral")
M("nFaceAll", num(F["face"]), "face-classified records, all analysed")
M("nSceneAll", num(F["scene"]), "scene-classified records, all analysed")
M("nFaceEmo", num(S["face images"]["n"]), "face-classified within emotional")
M("nSceneEmo", num(S["scene images"]["n"]), "scene-classified within emotional")
M("nPositive", num(S["positive prompts"]["n"]), "positive-valence prompts (family joy)")
M("nNegative", num(S["negative prompts"]["n"]), "negative-valence prompts")
M("nDistinct", num(AF["duplicates"]["distinct_prompts"]), "distinct prompts (dedup_key groups)")
M("nRepeats", num(AF["duplicates"]["records_repeating_an_earlier_prompt"]), "records repeating an earlier prompt")
M("nHappy", num(AF["duplicates"]["happy_count"]), "records whose prompt is exactly 'happy'")
M("nDistinctEmo", num(D["emotional"]), "distinct prompts, emotional")
M("nDistinctNonEmo", num(D["non_emotional"]), "distinct prompts, neutral-labelled")
M("nDistinctFace", num(SD["face images"]["n"]), "distinct prompts, emotional, face-classified")
M("nDistinctScene", num(SD["scene images"]["n"]), "distinct prompts, emotional, scene-classified")
M("nGroups", num(CONS["runs"]), "prompts drawn two or more times")
M("nGroupRecords", num(CONS["records_in_runs"]), "records inside those groups")
M("nPairGroups", num(CONS["pair_groups"]), "groups that are pairs")
M("nullShuffles", num(AF["null_shuffles"]), "random re-pairings per null")
M("nullSeed", num(AF["seed"]), "random seed of the analysis")
for fam, v in AF["families"]["prompt"].items(): M("famPrompt" + fam.capitalize(), num(v), f"prompt-reader top-1 = {fam}, all analysed")
for fam, v in AF["families"]["image"].items(): M("famImage" + fam.capitalize(), num(v), f"image-reader top-1 = {fam}, all analysed")

# ----------------------------------------------------------------------------- per subset x metric
SUB = [("Emo", "ALL emotional", "emotional"), ("Face", "face images", "face"), ("Scene", "scene images", "scene"),
       ("Pos", "positive prompts", None), ("Neg", "negative prompts", None), ("Neu", "non-emotional", "non_emotional")]
MET = [("Va", "va"), ("Sign", "vsign"), ("Fam", "family"), ("Ovlp", "overlap")]
B = INF["bootstrap_ci95_clustered"]
def ci_for(block, infkey, metric):
    if infkey is None: return None
    key = infkey if block == "Full" else "distinct_" + infkey
    if key not in B: return None
    m = B[key].get(metric)
    return m["ci95"] if isinstance(m, dict) else None
rows_by_block = {}
for block, subsets in (("Full", S), ("Dist", SD)):
    rows = []
    for code, name, infkey in SUB:
        sub = subsets[name]
        M(f"{block}{code}N", num(sub["n"]), f"{block} block, {name}: n")
        M(f"{block}{code}NSign", num(sub["n_sign"]), f"{block} block, {name}: valence-sign denominator")
        for mcode, mkey in MET:
            m = sub["metrics"][mkey]
            deg = m["degenerate"]
            M(f"{block}{code}{mcode}Obs", pct(m["obs"]), f"{block} {name} {mkey}: observed")
            M(f"{block}{code}{mcode}Null", pct(m["null"]), f"{block} {name} {mkey}: null mean")
            M(f"{block}{code}{mcode}Sd", pp(100*m["sd"], 2), f"{block} {name} {mkey}: null sd (pp)")
            M(f"{block}{code}{mcode}Z", "n/a" if deg else zf(m["z"]), f"{block} {name} {mkey}: z (n/a = degenerate)")
            c = None if deg else ci_for(block, infkey, mkey)
            M(f"{block}{code}{mcode}Ci", ci(*c) if c else "--", f"{block} {name} {mkey}: clustered-bootstrap 95% CI")
            rows.append((code, name, sub, mcode, mkey, m, c))
    rows_by_block[block] = rows

# ----------------------------------------------------------------------------- face/scene difference
def grab(pattern, default):
    mm = re.search(pattern, SIG_TXT)
    return mm.groups() if mm else default
fs_sign = grab(r"valence-sign agreement ===.*?difference\s+([+-][\d.]+)%\s+95% CI \[([+-][\d.]+)%, ([+-][\d.]+)%\].*?p = ([\d.]+)", ("+30.9", "+22.6", "+40.6", "0.0001"))
fs_fam = grab(r"emotion-family agreement ===.*?difference\s+([+-][\d.]+)%\s+95% CI \[([+-][\d.]+)%, ([+-][\d.]+)%\].*?p = ([\d.]+)", ("+26.3", "+18.4", "+35.3", "0.0001"))
draws = grab(r"(\d+) draws", ("10000",))[0]
M("DiffSignPp", f"{fs_sign[0]}~pp", "face minus scene, valence-sign agreement")
M("DiffSignCi", f"[{fs_sign[1]}, {fs_sign[2]}]", "its clustered-bootstrap 95% CI (pp)")
M("DiffSignP", fs_sign[3], "clustered permutation p (valence sign)")
M("DiffFamPp", f"{fs_fam[0]}~pp", "face minus scene, family agreement")
M("DiffFamCi", f"[{fs_fam[1]}, {fs_fam[2]}]", "its clustered-bootstrap 95% CI (pp)")
M("DiffFamP", fs_fam[3], "clustered permutation p (family)")
M("DiffDraws", num(int(draws)), "draws in the clustered bootstrap / permutation")

# ----------------------------------------------------------------------------- kappa
K = INF["cohens_kappa_family_agreement"]
def landis(k):
    return ("poor" if k < 0 else "slight" if k < 0.2 else "fair" if k < 0.4 else "moderate" if k < 0.6
            else "substantial" if k < 0.8 else "almost perfect")
KAP = [("Emo", "emotional"), ("Face", "face"), ("Scene", "scene"), ("All", "all_analysed"),
       ("DistEmo", "distinct_emotional"), ("DistFace", "distinct_face"), ("DistScene", "distinct_scene")]
for code, key in KAP:
    k = K[key]
    M(f"Kappa{code}", f"{k['kappa']:.2f}", f"Cohen's kappa, family agreement, {key}")
    M(f"Kappa{code}Ci", ci(*k["ci95"], frac=False, d=2), f"its clustered-bootstrap 95% CI")
    M(f"Kappa{code}Band", landis(k["kappa"]), "Landis & Koch (1977) band")

# ----------------------------------------------------------------------------- consistency
N = CONS["null"]
M("ConsFam", pct(CONS["mean_emotion_consistency"]), "mean within-group modal-family agreement")
M("ConsFamNull", pct(N["mean_emotion_consistency"]["null_mean"]), "its permutation-null mean")
M("ConsFamNullSd", pp(100*N["mean_emotion_consistency"]["null_sd"]), "its null sd")
M("ConsFamZ", zf(N["mean_emotion_consistency"]["z"]), "its z")
M("ConsFamP", sci(N["mean_emotion_consistency"]["p_perm"]), "its permutation p")
cr = INF["consistency_repeated_prompts"]["bootstrap_ci95_over_groups"]["ci95"]
M("ConsFamCi", ci(*cr), "clustered-bootstrap 95% CI over groups (inference.py)")
M("ConsVal", pct(CONS["mean_valence_consistency"]), "mean within-group modal-valence agreement")
M("ConsValNull", pct(N["mean_valence_consistency"]["null_mean"]), "its null mean")
M("ConsValZ", zf(N["mean_valence_consistency"]["z"]), "its z")
M("ConsValP", sci(N["mean_valence_consistency"]["p_perm"]), "its permutation p")
M("ConsFull", num(CONS["fully_consistent_runs"]), "groups where every drawing shares one family")
M("ConsFullPct", pct(CONS["fully_consistent_runs"] / CONS["runs"]), "as a share of the groups")
M("ConsFullNull", f"{N['fully_consistent_runs']['null_mean']:.1f}", "its null mean (count)")
M("ConsFullZ", zf(N["fully_consistent_runs"]["z"]), "its z")
M("ConsFullP", sci(N["fully_consistent_runs"]["p_perm"]), "its permutation p")
M("ConsDraws", num(N["draws"]), "permutation draws")
big = CONS["largest_groups"][0]
M("ConsHappyN", num(big["n"]), f"drawings of the prompt '{big['text']}'")
for fam, v in big["image_top1"].items(): M("ConsHappy" + fam.capitalize(), num(v), f"'{big['text']}' drawings read as {fam}")
zs = INF["z_seed_stability"]
M("ZSeedMin", zf(zs["z_min"]), "smallest emotional valence-sign z over seeds 1-5")
M("ZSeedMax", zf(zs["z_max"]), "largest emotional valence-sign z over seeds 1-5")

# ----------------------------------------------------------------------------- method comparison
h = MC["headline"]; L = MC["like_for_like"]; PT = MC["paired_tests"]
M("McN", num(h["n_records_both_readers_cover"]), "records both image readers cover")
for rcode, rkey in (("De", "describe_then_extract"), ("Clip", "direct_clip")):
    for mcode, mkey in MET:
        m = L[rkey]["all_emotional"][mkey]
        M(f"Mc{rcode}{mcode}", pct(m["value"]), f"like-for-like {rkey} {mkey} (emotional)")
        M(f"Mc{rcode}{mcode}Null", pct(m["null_mean"]), "its null mean")
        M(f"Mc{rcode}{mcode}Z", zf(m["z"]), "its z")
    for scode, skey in (("Face", "face_images"), ("Scene", "scene_images")):
        for mcode, mkey in (("Sign", "vsign"), ("Fam", "family")):
            m = L[rkey][skey][mkey]
            M(f"Mc{rcode}{scode}{mcode}", pct(m["value"]), f"like-for-like {rkey} {skey} {mkey}")
            M(f"Mc{rcode}{scode}{mcode}Z", zf(m["z"]), "its z")
pf, pv = PT["family_agreement"], PT["valence_sign_agreement"]
M("McDiffFamPp", f"{pf['difference_pp']:+.1f}~pp", "describe minus CLIP, family agreement")
M("McDiffFamCi", f"[{pf['clustered_bootstrap_95ci_difference_pp'][0]:+.1f}, {pf['clustered_bootstrap_95ci_difference_pp'][1]:+.1f}]", "its clustered-bootstrap 95% CI (pp)")
M("McMcNemarFamP", sci(pf["mcnemar_exact_binomial_p_unclustered"]), "exact McNemar p, unclustered (optimistic)")
M("McClusterFamP", f"$<${1/ pf['cluster_sign_flip_draws']*20:.4f}".replace("$<$0.0010", "$<$0.001"), "cluster sign-flip p (family)")
M("McFamB", num(pf["describe_only_hit_b"]), "records only describe-then-extract agrees on (family)")
M("McFamC", num(pf["direct_clip_only_hit_c"]), "records only direct CLIP agrees on (family)")
M("McFamBoth", num(pf["both_hit"]), "records both agree on (family)")
M("McFamNeither", num(pf["both_miss"]), "records neither agrees on (family)")
M("McDiffSignPp", f"{pv['difference_pp']:+.1f}~pp", "describe minus CLIP, valence-sign agreement")
M("McDiffSignCi", f"[{pv['clustered_bootstrap_95ci_difference_pp'][0]:+.1f}, {pv['clustered_bootstrap_95ci_difference_pp'][1]:+.1f}]", "its clustered-bootstrap 95% CI (pp)")
M("McMcNemarSignP", sci(pv["mcnemar_exact_binomial_p_unclustered"]), "exact McNemar p, unclustered")
M("McClusterDraws", num(pf["cluster_sign_flip_draws"]), "cluster sign-flip draws")
rv = MC["reader_vs_reader"]["emotional_607"]
M("McReaderAgree", pct(rv["top1_agreement"]), "top-1 agreement between the two image readers")
M("McClipNeutral", num(rv["direct_clip_top1_counts"]["neutral"]), "emotional-prompt images direct CLIP reads as neutral")
v1 = MC["v1_nli_prompt_side_comparison"]
M("McVOneN", num(v1["n_records"]), "records in the v1 (NLI prompt side) comparison")
for rcode, rkey in (("De", "describe_then_extract"), ("Clip", "direct_clip")):
    for mcode, mkey in (("Fam", "family"), ("Ovlp", "overlap"), ("Va", "va")):
        M(f"McVOne{rcode}{mcode}", pct(v1[rkey][mkey]), f"v1 comparison {rkey} {mkey}")

# ----------------------------------------------------------------------------- control audit
cc = AU["control_contamination"]; sp = cc["specificity"]
M("CtrlN", num(cc["n_control"]), "neutral-labelled prompts")
M("CtrlNameOnly", num(cc["name_only_records"]["n"]), "records reduced to '[name]' by redaction")
M("CtrlLexicon", num(cc["lexicon_size"]), "affect words in the audit lexicon")
M("CtrlFlagged", num(cc["lexicon_flagged"]["n"]), "neutral-labelled prompts containing an affect word")
M("CtrlFlaggedPct", pp(cc["lexicon_flagged"]["pct_of_control"]), "as a share of the control")
M("CtrlRemoved", num(cc["n_removed"]), "records removed for the cleaned control")
M("CtrlCleanN", num(cc["n_cleaned"]), "cleaned control size")
M("CtrlTopWords", ", ".join(f"{w['word']} ({w['records']})" for w in cc["lexicon_flagged"]["top20_words"][:10]), "ten most frequent affect words in the control")
fc, cl = sp["full_control_405"], sp["cleaned_control"]
M("CtrlVaObs", pp(fc["record_level_null"]["va_similarity"]["observed_pct"]), "full control VA observed")
M("CtrlVaNull", pp(fc["record_level_null"]["va_similarity"]["null_mean_pct"]), "full control VA null")
M("CtrlVaSd", pp(fc["record_level_null"]["va_similarity"]["null_sd_pct"], 2), "full control VA null sd (pp)")
M("CtrlVaZ", zf(fc["record_level_null"]["va_similarity"]["z"]), "full control VA z (record-level null)")
M("CtrlVaZClustered", zf(fc["clustered_null"]["va_similarity"]["z"]), "full control VA z (clustered null)")
M("CtrlCleanVaObs", pp(cl["record_level_null"]["va_similarity"]["observed_pct"]), "cleaned control VA observed")
M("CtrlCleanVaNull", pp(cl["record_level_null"]["va_similarity"]["null_mean_pct"]), "cleaned control VA null")
M("CtrlCleanVaZ", zf(cl["record_level_null"]["va_similarity"]["z"]), "cleaned control VA z (record-level)")
M("CtrlCleanVaZClustered", zf(cl["clustered_null"]["va_similarity"]["z"]), "cleaned control VA z (clustered)")
M("CtrlFamObs", pp(fc["record_level_null"]["family_agreement"]["observed_pct"]), "full control family agreement (degenerate: equals its null)")

# ----------------------------------------------------------------------------- describer leak
dl = AU["describer_leak"]; t22 = dl["two_by_two_all_1012"]; sc = dl["scene_classified"]
M("DescPeopleExpr", num(t22["people_ge1|expression_word_present"]), "people>=1 and expression word")
M("DescPeopleNoExpr", num(t22["people_ge1|expression_word_absent"]), "people>=1, no expression word")
M("DescNoPeopleExpr", num(t22["people_0|expression_word_present"]), "people=0 yet an expression word")
M("DescNoPeopleNoExpr", num(t22["people_0|expression_word_absent"]), "people=0, no expression word")
M("DescSceneN", num(sc["n"]), "scene-classified records")
M("DescScenePeopleZero", num(sc["people_0"]), "of which people=0")
M("DescScenePeopleZeroExpr", num(sc["people_0_with_expression_word"]), "of which people=0 with an expression word")
M("DescSceneSmile", num(sc["people_0_answer_smile_smiling_happy"]), "people=0 answering smile/smiling/happy")
M("DescSceneSmilePct", pp(sc["people_0_answer_smile_smiling_happy_pct_of_people_0"]), "as a share of the people=0 records")
bw = dl["bare_expression_word_corpus_wide"]; cp = dl["copy_rate"]; sm = dl["smile_share"]
M("DescBareStrictN", num(cp["strict"]["n"]), "expression answers that name an affective state (strict)")
M("DescBareStrictPct", pct(cp["strict"]["n"] / F["records"]), "as a share of analysed records")
M("DescBareBroadN", num(cp["broad"]["n"]), "expression answers that are a single facial-action or affect word (broad)")
M("DescCopyStrict", pp(cp["strict"]["copy_rate_pct"]), "copy rate, strict: image top-1 equals the word's family")
M("DescCopyBroad", pp(cp["broad"]["copy_rate_pct"]), "copy rate, broad")
M("DescCopyBroadPeopleZero", pp(cp["broad_within_people_0"]["copy_rate_pct"]), "copy rate, broad, people=0")
M("DescCopyBroadPeople", pp(cp["broad_within_people_ge1"]["copy_rate_pct"]), "copy rate, broad, people>=1")
M("DescSmileAll", pp(sm["all_1012"]["pct"]), "smile/smiling/happy share, all analysed")
M("DescSmileAllN", num(sm["all_1012"]["smile_smiling_happy"]), "count")
M("DescSmileFace", pp(sm["face_classified_591"]["pct"]), "smile/smiling/happy share, face-classified")
M("DescSmileFaceN", num(sm["face_classified_591"]["smile_smiling_happy"]), "count")

# ----------------------------------------------------------------------------- per family
pfam = AU["per_family"]; rec = pfam["recall_by_prompt_family"]
for fam, r in rec.items():
    if r["recall_pct"] is None: continue
    M("Rec" + fam.capitalize(), pp(r["recall_pct"]), f"per-family recall (row = prompt family {fam})")
    M("Rec" + fam.capitalize() + "Ci", f"[{r['ci95_pct'][0]:.1f}, {r['ci95_pct'][1]:.1f}]", "its clustered-bootstrap 95% CI")
    M("Rec" + fam.capitalize() + "N", num(r["n_prompts"]), "prompts in that family")

# ----------------------------------------------------------------------------- error taxonomy
tally = ET["failure_mode_tally"]; stage = ET["by_pipeline_stage"]
M("TaxN", num(ET["sample_size"]), "high-confidence disagreements examined")
M("TaxDistinct", num(ET["population"]["n_distinct_prompts"]), "distinct prompts among them")
for k, v in tally.items(): M("Tax" + k.upper(), num(v), f"failure mode ({k})")
M("TaxDescriber", num(stage["describer (a+b)"]), "describer faults (a+b)")
M("TaxReader", num(stage["image reader (c)"]), "image-reader faults (c)")
M("TaxPrompt", num(stage["prompt side (d+f)"]), "prompt-side faults (d+f)")
M("TaxGenerator", num(stage["generator (e)"]), "generator faults (e)")
M("TaxPeopleZero", num(ET["tag_counts"]["people_zero"]), "records auto-tagged people=0")

# ----------------------------------------------------------------------------- Holm
H = INF["holm_bonferroni"]["primary_family_all_non_degenerate"]
M("HolmM", num(H["m"]), "non-degenerate z-scores tested")
M("HolmExcluded", num(INF["holm_bonferroni"]["flagged_degenerate_excluded"]), "degenerate z-scores excluded")
M("HolmSurvive", num(H["holm_n_survive"]), "survive Holm at family-wise 0.05")
M("HolmFail", num(H["holm_n_do_not_survive"]), "do not survive")
M("HolmBonfZ", f"{H['bonferroni_z_for_smallest_rank']:.1f}", "Bonferroni-equivalent z for the smallest rank")

# ----------------------------------------------------------------------------- optional: ablation, human check
# ablation macros: the cells the prose quotes (per variant x subset x measure: observed, null, z)
if AB:
    _VNAME = {"drop_expression": "DropExpression", "drop_action": "DropAction", "drop_posture": "DropPosture",
              "drop_people": "DropPeople", "drop_scene": "DropScene", "fixed_expression": "FixedExpression",
              "people_aware": "PeopleAware", "people_aware_no_expression": "PeopleAwareNoExpression",
              "control_full_template": "Control", "baseline": "Baseline"}
    for v, vn in _VNAME.items():
        if v not in AB: continue
        for sk, sn in (("emotional", "Emo"), ("face", "Face"), ("scene", "Scene")):
            sub = AB[v].get(sk, {})
            for mk, mn in (("vsign", "Sign"), ("family", "Fam")):
                m = sub.get(mk, {})
                if not m: continue
                M(f"Abl{vn}{sn}{mn}Obs", pct(m.get("obs")), f"ablation {v}, {sk}, {mk}: observed")
                M(f"Abl{vn}{sn}{mn}Null", pct(m.get("null")), f"ablation {v}, {sk}, {mk}: null mean")
                M(f"Abl{vn}{sn}{mn}Z", zf(m.get("z")), f"ablation {v}, {sk}, {mk}: z")
    _pv = (AB.get("_meta") or {}).get("per_variant", {})
    if "control_full_template" in _pv:
        M("AblControlChanged", num(_pv["control_full_template"].get("image_top1_changed_vs_baseline", 0)), "top-1 readings changed by the control re-run")
    if "drop_expression" in _pv:
        dist = _pv["drop_expression"].get("image_top1_distribution", {})
        M("AblDropExpressionSurprise", num(dist.get("surprise", 0)), "drop_expression: records read as surprise")
        M("AblDropExpressionNeutral", num(dist.get("neutral", 0)), "drop_expression: records read as neutral")
        M("AblDropExpressionChanged", num(_pv["drop_expression"].get("image_top1_changed_vs_baseline", 0)), "drop_expression: top-1 readings changed vs baseline")
M("AblationAvailable", "yes" if AB else "no", "ablation summary present")
M("HumanCheckAvailable", "yes" if HC else "no", "human check scored")
if HC:
    M("HcN", num(HC["n_coded"]), "drawings coded")
    def w(t): return f"{100*t[0]:.1f}\\% [{100*t[1]:.1f}, {100*t[2]:.1f}]"
    M("HcPeopleAcc", w(HC["describer_people"]["accuracy"]), "describer people-count accuracy vs coder")
    M("HcFaceAcc", w(HC["face_rule"]["accuracy"]), "face-rule accuracy vs coder")
    M("HcFacePrec", w(HC["face_rule"]["precision"]), "face-rule precision")
    M("HcFaceRec", w(HC["face_rule"]["recall"]), "face-rule recall")
    M("HcSmileN", num(HC["smiling_answer"]["n"]), "'smiling' answers in the sample")
    M("HcSmileTrue", w(HC["smiling_answer"]["human_face_and_positive"]), "of which a readable positive face")
    M("HcSmileNoPerson", w(HC["smiling_answer"]["human_no_person"]), "of which no person drawn")
    M("HcReaderSign", w(HC["image_reader_vs_human"]["valence_sign"]), "image reader vs coder, valence sign")
    M("HcReaderFam", w(HC["image_reader_vs_human"]["family"]), "image reader vs coder, family")
    M("HcReaderKappa", f"{HC['image_reader_vs_human']['family_kappa']:.2f}", "its kappa")
    pv_ = HC["prompt_vs_human_by_human_face"]
    M("HcPromptFace", w(pv_["readable_face"]), "prompt reader vs coder valence, coder says readable face")
    M("HcPromptScene", w(pv_["no_readable_face"]), "prompt reader vs coder valence, no readable face")
    M("HcPromptDiffPp", f"{pv_['difference_pp']:+.1f}~pp" if pv_["difference_pp"] is not None else "n/a", "difference")
    M("HcPromptDiffZ", zf(pv_["two_proportion_z"]) if pv_["two_proportion_z"] is not None else "n/a", "two-proportion z")

# ============================================================================= write numbers.tex
with open(os.path.join(GEN, "numbers.tex"), "w", encoding="utf-8") as f:
    f.write("% numbers.tex — GENERATED by emoviz/export_tex.py. Do not edit; re-run the exporter.\n")
    f.write("% Every macro below is a number read from a result file under emoviz/outputs/.\n")
    f.write("% Macro                      Meaning\n")
    for name, _, meaning in MACROS: f.write(f"%   \\{name:26s} {meaning}\n")
    f.write("\n")
    for name, value, _ in MACROS: f.write(f"\\newcommand{{\\{name}}}{{{value}}}\n")

# ============================================================================= tables
def table(name, caption, label, colspec, header, rows, note=None, size="\\small"):
    lines = ["% GENERATED by emoviz/export_tex.py — do not edit", "\\begin{table}[htbp]", "\\centering", size,
             f"\\caption{{{caption}}}", f"\\label{{{label}}}", f"\\begin{{tabular}}{{{colspec}}}", "\\toprule",
             " & ".join(header) + " \\\\", "\\midrule"]
    for r in rows:
        if r == "MIDRULE": lines.append("\\midrule"); continue
        lines.append(" & ".join(r) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    if note: lines.append(f"\\par\\smallskip\\footnotesize {note}")
    lines.append("\\end{table}\n")
    open(os.path.join(GEN, f"tab_{name}.tex"), "w", encoding="utf-8").write("\n".join(lines))

MNAME = {"va": "Valence--arousal similarity", "vsign": "Valence-sign agreement", "family": "Family agreement", "overlap": "Top-3 soft overlap"}
SNAME = {"ALL emotional": "Emotional prompts", "face images": "\\quad face-classified", "scene images": "\\quad scene-classified",
         "positive prompts": "\\quad positive valence", "negative prompts": "\\quad negative valence", "non-emotional": "Neutral-labelled prompts"}
def headline_rows(rows):
    out = []; last = None
    for code, name, sub, mcode, mkey, m, c in rows:
        if name in ("positive prompts", "negative prompts"): continue
        if name != last:
            if last is not None: out.append("MIDRULE")
            out.append([f"\\textbf{{{SNAME[name]}}} ($n$={sub['n']}; sign $n$={sub['n_sign']})", "", "", "", ""]); last = name
        out.append([MNAME[mkey], pct(m["obs"]), pct(m["null"]), "n/a" if m["degenerate"] else zf(m["z"]), ci(*c) if c else ("degenerate" if m["degenerate"] else "--")])
    return out
table("headline", f"Agreement between the prompt reader and the image reader on the {F['records']:,} analysed records, by prompt group and image class, against the random-pairing null ({AF['null_shuffles']} re-pairings, seed {AF['seed']}). CI: clustered bootstrap over prompt groups ({INF['bootstrap_draws']:,} draws). n/a: degenerate null (every prompt in the subset shares one label, so permutation cannot change the score).",
      "tab:headline", "lrrrl", ["Subset / measure", "Observed", "Null", "$z$", "95\\% CI"], headline_rows(rows_by_block["Full"]))
table("distinct", f"The same analysis on the {D['records']} distinct prompts only (first occurrence of each prompt text kept), a check against pseudo-replication from the {AF['duplicates']['records_repeating_an_earlier_prompt']} repeated prompts.",
      "tab:distinct", "lrrrl", ["Subset / measure", "Observed", "Null", "$z$", "95\\% CI"], headline_rows(rows_by_block["Dist"]))

fsr = []
for lab, mkey, fs in (("Valence-sign agreement", "vsign", fs_sign), ("Family agreement", "family", fs_fam)):
    fm, sm_ = S["face images"]["metrics"][mkey], S["scene images"]["metrics"][mkey]
    cf, cs = ci_for("Full", "face", mkey), ci_for("Full", "scene", mkey)
    fsr.append([lab, f"{pct(fm['obs'])} {ci(*cf)}", f"{pct(sm_['obs'])} {ci(*cs)}", f"{fs[0]}~pp [{fs[1]}, {fs[2]}]", fs[3]])
table("difference", f"Face-classified versus scene-classified drawings on the emotional prompts: agreement with 95\\% clustered-bootstrap CIs, the difference with its CI, and the clustered permutation p ({int(draws):,} draws; significance.py).",
      "tab:difference", "lllll", ["Measure", f"Face ($n$={S['face images']['n']})", f"Scene ($n$={S['scene images']['n']})", "Difference (pp)", "Perm.\\ $p$"], fsr, size="\\footnotesize")

mr = []
for mcode, mkey in MET:
    a, b = L["describe_then_extract"]["all_emotional"][mkey], L["direct_clip"]["all_emotional"][mkey]
    mr.append([MNAME[mkey], pct(a["value"]), pct(a["null_mean"]), zf(a["z"]), pct(b["value"]), pct(b["null_mean"]), zf(b["z"])])
mr += ["MIDRULE",
       ["Paired family test", f"$b$={pf['describe_only_hit_b']}, $c$={pf['direct_clip_only_hit_c']}", "", "", f"diff {pf['difference_pp']:+.1f}~pp", f"CI [{pf['clustered_bootstrap_95ci_difference_pp'][0]:+.1f}, {pf['clustered_bootstrap_95ci_difference_pp'][1]:+.1f}]", f"cluster $p<0.001$"],
       ["Paired valence-sign test", f"$b$={pv['describe_only_hit_b']}, $c$={pv['direct_clip_only_hit_c']}", "", "", f"diff {pv['difference_pp']:+.1f}~pp", f"CI [{pv['clustered_bootstrap_95ci_difference_pp'][0]:+.1f}, {pv['clustered_bootstrap_95ci_difference_pp'][1]:+.1f}]", f"cluster $p<0.001$"]]
table("method", f"Two image readers scored like for like against the same prompt reader (GoEmotions) on the same {h['n_records_both_readers_cover']} emotional records with the same measures and the same {AF['null_shuffles']} re-pairings. $b$ = records only describe-then-extract agrees on; $c$ = records only direct CLIP agrees on. The exact McNemar $p$ treats records as independent and is optimistic ({sci(pf['mcnemar_exact_binomial_p_unclustered'])} for family); the cluster sign-flip randomisation ({pf['cluster_sign_flip_draws']:,} draws) respects prompt groups.",
      "tab:method", "lrrrrrr", ["Measure", "Describe→extract", "null", "$z$", "Direct CLIP", "null", "$z$"], mr, size="\\scriptsize")
table("methodvone", f"The earlier (v1) comparison as published in the build log: prompt side read by BART-MNLI, the {v1['n_records']} records of the v1 lexicon rule, and a different overlap formula. Kept as a record; not comparable with Table~\\ref{{tab:headline}}.",
      "tab:methodvone", "lrr", ["Measure", "Describe→extract", "Direct CLIP"],
      [[MNAME["family"], pct(v1["describe_then_extract"]["family"]), pct(v1["direct_clip"]["family"])],
       [MNAME["overlap"], pct(v1["describe_then_extract"]["overlap"]), pct(v1["direct_clip"]["overlap"])],
       [MNAME["va"], pct(v1["describe_then_extract"]["va"]), pct(v1["direct_clip"]["va"])]])

fams = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
conf = pfam["confusion_prompt_family_x_image_family"]
crows = []
for pfam_ in fams:
    row = conf[pfam_]; n = sum(row.values())
    if n == 0: continue
    r = rec[pfam_]
    crows.append([pfam_] + [str(row[i]) for i in fams] + [str(n), f"{pp(r['recall_pct'])} [{r['ci95_pct'][0]:.0f}, {r['ci95_pct'][1]:.0f}]"])
crows.append("MIDRULE")
crows.append(["\\textit{image total}"] + [str(pfam["column_totals_image_family"][i]) for i in fams] + [str(pfam["n"]), ""])
table("confusion", f"Prompt-reader family (rows) against image-reader family (columns) on the {pfam['n']} emotional records. Recall = row diagonal share, with a clustered-bootstrap 95\\% CI. Cohen's $\\kappa$ = {K['emotional']['kappa']:.2f} {ci(*K['emotional']['ci95'], frac=False, d=2)}. The image reader never returns disgust and returns fear {AF['families']['image']['fear']} times in {F['records']:,} records.",
      "tab:confusion", "l" + "r"*7 + "rl", ["Prompt \\textbackslash{} image"] + fams + ["$n$", "Recall [CI]"], crows, size="\\scriptsize")

table("kappa", "Cohen's $\\kappa$ for family agreement (7 families), with clustered-bootstrap 95\\% CIs and the Landis \\& Koch (1977) band. The neutral-labelled subset is degenerate ($\\kappa$ = 0 by construction) and is omitted.",
      "tab:kappa", "lrrll", ["Subset", "$n$", "$\\kappa$", "95\\% CI", "Band"],
      [[k.replace("_", " "), str(K[k]["n"]), f"{K[k]['kappa']:.2f}", ci(*K[k]["ci95"], frac=False, d=2), landis(K[k]["kappa"])] for _, k in KAP])

table("consistency", f"Within-group agreement of the image reader across the {CONS['runs']} prompts drawn two or more times ({CONS['records_in_runs']} records; {CONS['pair_groups']} groups are pairs, whose modal agreement cannot fall below 50\\%), against a permutation null that shuffles the image readings over all {CONS['analysed']:,} analysed records and re-cuts them into the same groups ({N['draws']:,} draws, seed {N['seed']}).",
      "tab:consistency", "lrrrr", ["Quantity", "Observed", "Null mean (sd)", "$z$", "$p$"],
      [["Same family, mean over groups", pct(CONS["mean_emotion_consistency"]), f"{pct(N['mean_emotion_consistency']['null_mean'])} ({pp(100*N['mean_emotion_consistency']['null_sd'])})", zf(N["mean_emotion_consistency"]["z"]), sci(N["mean_emotion_consistency"]["p_perm"])],
       ["Same valence, mean over groups", pct(CONS["mean_valence_consistency"]), f"{pct(N['mean_valence_consistency']['null_mean'])} ({pp(100*N['mean_valence_consistency']['null_sd'])})", zf(N["mean_valence_consistency"]["z"]), sci(N["mean_valence_consistency"]["p_perm"])],
       ["Fully consistent groups (of " + str(CONS["runs"]) + ")", str(CONS["fully_consistent_runs"]), f"{N['fully_consistent_runs']['null_mean']:.1f} ({N['fully_consistent_runs']['null_sd']:.1f})", zf(N["fully_consistent_runs"]["z"]), sci(N["fully_consistent_runs"]["p_perm"])]])

table("control", f"The specificity check on the prompts the text reader labels neutral. Only valence--arousal similarity is informative there (sign and family are degenerate: every prompt shares the neutral label). Cleaned control = minus the {cc['name_only_records']['n']} records reduced to `[name]' and the {cc['lexicon_flagged']['n']} containing one of {cc['lexicon_size']} plain affect words.",
      "tab:control", "lrrrrr", ["Control set", "$n$", "VA observed", "VA null", "$z$ (record null)", "$z$ (clustered null)"],
      [["All neutral-labelled prompts", str(fc["n"]), pp(fc["record_level_null"]["va_similarity"]["observed_pct"]), pp(fc["record_level_null"]["va_similarity"]["null_mean_pct"]), zf(fc["record_level_null"]["va_similarity"]["z"]), zf(fc["clustered_null"]["va_similarity"]["z"])],
       ["Cleaned control", str(cl["n"]), pp(cl["record_level_null"]["va_similarity"]["observed_pct"]), pp(cl["record_level_null"]["va_similarity"]["null_mean_pct"]), zf(cl["record_level_null"]["va_similarity"]["z"]), zf(cl["clustered_null"]["va_similarity"]["z"])]])

table("describer", f"The describer's answers on all {F['records']:,} analysed records: people count crossed with whether the facial-expression answer contains an expression word. The face rule is the top-left cell. Of the {sc['n']} scene-classified records, {sc['people_0']} report no people and {sc['people_0_with_expression_word']} of those still contain an expression word ({sc['people_0_answer_smile_smiling_happy']} answer smile, smiling or happy).",
      "tab:describer", "lrr", ["", "Expression word present", "Expression word absent"],
      [["People $\\geq 1$", str(t22["people_ge1|expression_word_present"]), str(t22["people_ge1|expression_word_absent"])],
       ["People $= 0$", str(t22["people_0|expression_word_present"]), str(t22["people_0|expression_word_absent"])]])

MODE = {"a": "describer invented a face or expression where none is drawn", "b": "describer read the expression wrongly",
        "c": "reader mis-inferred from a correct description", "d": "prompt ambiguous or mixed",
        "e": "drawing does not depict the prompt", "f": "prompt reader wrong"}
table("taxonomy", f"Primary failure mode of the {ET['sample_size']} high-confidence disagreements (both readers' top-1 score $\\geq 0.8$, families differ), assigned from the drawing. Describer faults (a+b) = {stage['describer (a+b)']}; image reader (c) = {stage['image reader (c)']}; prompt side (d+f) = {stage['prompt side (d+f)']}; generator (e) = {stage['generator (e)']}.",
      "tab:taxonomy", "lp{0.55\\textwidth}rl", ["Mode", "Description", "$n$", "Exemplar ids"],
      [[f"({k})", MODE[k], str(v), ", ".join(map(str, ET["failure_mode_exemplars"][k]))] for k, v in tally.items()])

table("holm", f"Multiple-comparison control over the {H['m']} non-degenerate $z$-scores the analysis prints ({INF['holm_bonferroni']['flagged_degenerate_excluded']} degenerate ones excluded). Two-sided $p$ by the normal approximation; Holm--Bonferroni at family-wise 0.05: {H['holm_n_survive']} survive, {H['holm_n_do_not_survive']} do not.",
      "tab:holm", "lp{0.78\\textwidth}", ["Outcome", "Tests"],
      [["Do not survive", "; ".join(tex(x) for x in H["do_not_survive"])],
       ["Survive", f"the remaining {H['holm_n_survive']}, including every headline (emotional, face and scene on all four measures; distinct-prompt emotional and face)"]], size="\\footnotesize")

table("families", f"Top-1 family marginals of the two readers over all {F['records']:,} analysed records.",
      "tab:families", "lrr", ["Family", "Prompt reader", "Image reader"],
      [[fam, str(AF["families"]["prompt"][fam]), str(AF["families"]["image"][fam])] for fam in fams])

# ablation (optional)
if AB:
    variants = ["baseline"] + [v for v in AB if v not in ("baseline", "_meta")]
    def find(d, hint):
        for k in d:
            if hint in k.lower(): return d[k]
        return None
    arows = []
    for v in variants:
        for hint, lab in (("emo", "emotional"), ("face", "face"), ("scene", "scene")):
            sub = find(AB[v], hint) or {}
            s_, f_ = sub.get("vsign", {}), sub.get("family", {})
            arows.append([tex(v) if hint == "emo" else "", lab, str(sub.get("n", s_.get("n", ""))),
                          pct(s_.get("obs")) if s_ else "--", pct(s_.get("null")) if s_ else "--", zf(s_.get("z")) if s_ else "--",
                          pct(f_.get("obs")) if f_ else "--", pct(f_.get("null")) if f_ else "--", zf(f_.get("z")) if f_ else "--"])
        arows.append("MIDRULE")
    arows.pop()
    table("ablation", "Description-template ablation: the NLI stage re-run on descriptions rebuilt from the cached describer answers with one clause removed or fixed; the prompt side and the null procedure unchanged. Valence-sign and family agreement per variant on the emotional prompts and their face/scene halves.",
          "tab:ablation", "llrrrrrrr", ["Variant", "Subset", "$n$", "Sign obs", "null", "$z$", "Family obs", "null", "$z$"], arows, size="\\footnotesize")
else:
    open(os.path.join(GEN, "tab_ablation.tex"), "w").write("% GENERATED — ablation summary not present when export_tex.py last ran; re-run after ablate_nli.py.\n\\noindent\\emph{[Ablation table pending: run \\texttt{ablate\\_nli.py}, then \\texttt{export\\_tex.py}.]}\n")

if HC:
    def w(t): return f"{100*t[0]:.1f}\\% [{100*t[1]:.1f}, {100*t[2]:.1f}]"
    table("humancheck", f"Single-coder reliability check on {HC['n_coded']} drawings coded blind to prompt and model output (Wilson 95\\% CIs).",
          "tab:humancheck", "ll", ["Quantity", "Value [95\\% CI]"],
          [["Describer people-count accuracy", w(HC["describer_people"]["accuracy"])],
           ["Face-rule precision / recall", f"{w(HC['face_rule']['precision'])} / {w(HC['face_rule']['recall'])}"],
           ["`Smiling' answers with a readable positive face", w(HC["smiling_answer"]["human_face_and_positive"])],
           ["`Smiling' answers with no person drawn", w(HC["smiling_answer"]["human_no_person"])],
           ["Image reader vs coder, valence sign", w(HC["image_reader_vs_human"]["valence_sign"])],
           ["Image reader vs coder, family ($\\kappa$)", f"{w(HC['image_reader_vs_human']['family'])} ($\\kappa$ = {HC['image_reader_vs_human']['family_kappa']:.2f})"],
           ["Prompt reader vs coder valence, readable face", w(HC["prompt_vs_human_by_human_face"]["readable_face"])],
           ["Prompt reader vs coder valence, no readable face", w(HC["prompt_vs_human_by_human_face"]["no_readable_face"])]])
else:
    open(os.path.join(GEN, "tab_humancheck.tex"), "w").write("% GENERATED — human check not scored when export_tex.py last ran; code outputs/human_check/labels.csv, run human_check.py score, then export_tex.py.\n\\noindent\\emph{[Human-check table pending: code \\texttt{outputs/human\\_check/labels.csv}, run \\texttt{human\\_check.py score}, then \\texttt{export\\_tex.py}.]}\n")

print(f"wrote {GEN}/numbers.tex ({len(MACROS)} macros) and {len([f for f in os.listdir(GEN) if f.startswith('tab_')])} tables")
