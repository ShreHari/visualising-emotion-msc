#!/usr/bin/env python3
"""
emoviz/audits.py — three pure-counting audits of the describe->extract results -> outputs/audits.json.
Read-only on every other file.

The central quantity throughout is AGREEMENT between the prompt reader (GoEmotions top-1 family on the
visitor's text) and the image reader (zero-shot NLI top-1 family on the BLIP-VQA description).

  (1) CONTROL CONTAMINATION — the 405 'non-emotional' prompts are defined by GoEmotions top-1 = neutral
      and were never human-checked. A fixed English affect-word lexicon (LEXICON below) counts how many
      contain a plain emotion word; records whose text is exactly "[name]" after redaction are flagged as
      empty, not non-emotional. The specificity check (VA similarity observed vs a 300-shuffle
      random-pairing null, seed 7) is then re-run on the CLEANED control.
  (2) DESCRIBER LEAK — BLIP-VQA answers "What is the facial expression?" even when it reports no people.
      The 2x2 people-count x expression-word table, the scene-classified breakdown, the rate at which the
      expression answer is itself a bare emotion word, and the rate at which the image reader's top-1
      family equals the family implied by that word (copy rate).
  (3) PER-FAMILY BREAKDOWN — 7x7 confusion (prompt family x image family) on the 607 emotional records,
      per-family recall with clustered bootstrap CIs, and the image reader's family marginals.

Clustering: dedup_key on each record is prompt identity (249 of 1,012 records repeat an earlier prompt),
so every bootstrap resamples prompt GROUPS and the clustered null permutes prompts ACROSS groups. The
record-level null of analysis_final.py is reproduced as well (same call order, same seed) so the auditor
can see the reference numbers come out of this script unchanged before the cleaned-control re-run.

Run:  .venv/bin/python audits.py
"""
import json, os, math, random, statistics as st, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
N_SHUFFLES, SEED, B_BOOT = 300, 7, 10000
FAMS = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]

# =====================================================================================================
# COPIED VERBATIM from analysis_final.py (lines 23-81). That script executes its whole analysis on
# import, so it cannot be imported; the constants and functions below are copied unchanged (code
# identical; two comments lightly reworded for this project's vocabulary).
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
    # token-intersection so multi-word answers ("man is smiling") count (audit fix)
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
# ===================================== end of verbatim copy ==========================================

# ---- (1) fixed English affect-word lexicon: exact word forms, word-boundary search, case-insensitive.
#      No stemming, no misspellings ("ecited", "curios", "thrillled"), no non-English words — so the
#      contamination count is a LOWER bound.
LEXICON = ["happy", "sad", "excited", "tired", "angry", "worried", "hopeful", "content", "ecstatic",
           "delighted", "lonely", "anxious", "scared", "afraid", "nervous", "calm", "relaxed", "peaceful",
           "joyful", "jovial", "cheerful", "glad", "proud", "grateful", "bored", "stressed", "stress",
           "frustrated", "upset", "depressed", "miserable", "gloomy", "morose", "grumpy", "moody",
           "jealous", "impatient", "love", "hate", "fear", "joy", "anger", "sadness", "happiness",
           "excitement", "amazement", "curious", "confused", "surprised", "amazed", "thrilled",
           "disgusted", "annoyed", "furious", "exhausted", "sleepy", "overwhelmed", "hopeless",
           "optimistic", "nostalgic", "melancholy", "inspired", "interested", "anticipation",
           "bemused", "intrigued"]
assert len(LEXICON) == len(set(LEXICON))
LEX_RE = {w: re.compile(rf"\b{re.escape(w)}\b") for w in LEXICON}

# ---- (2) expression answer -> family it implies (a priori mapping; 'confused' follows G2F confusion->surprise)
EXPRESSION_FAMILY = {
    "smile": "joy", "smiling": "joy", "happy": "joy", "laughing": "joy", "excited": "joy", "grin": "joy", "grinning": "joy",
    "sad": "sadness", "crying": "sadness", "frowning": "sadness",
    "angry": "anger", "anger": "anger",
    "scared": "fear", "worried": "fear",
    "surprised": "surprise", "surprise": "surprise", "shocked": "surprise", "confused": "surprise",
    "disgusted": "disgust",
    "neutral": "neutral", "calm": "neutral", "serious": "neutral", "concentration": "neutral",
    "concentrating": "neutral", "determined": "neutral", "pensive": "neutral", "sleepy": "neutral", "sleeping": "neutral"}
# strict tier: the answer NAMES an affective state (as opposed to a facial action such as 'smiling')
NAMED_EMOTION_WORDS = {"happy", "sad", "angry", "anger", "excited", "scared", "worried", "surprised",
                       "surprise", "shocked", "confused", "disgusted", "calm", "neutral"}

def bare_answer(vqa):
    """The expression answer as a single lower-case token if it is one word in EXPRESSION_FAMILY, else None."""
    a = (vqa.get("expression", "") or "").lower().strip()
    return a if (" " not in a and a in EXPRESSION_FAMILY) else None

def has_expression_word(vqa):
    return bool(set(re.findall(r"[a-z]+", (vqa.get("expression", "") or "").lower())) & EXPRESSION_WORDS)

# ---------- load (same rules as analysis_final.py) ----------
rows = [json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8")]
rows = [r for r in rows if r["id"] > PRETEST_MAX_ID]
goe = {int(k): v for k, v in json.load(open(os.path.join(OUT, "prompt_emotions_goe.json"))).items()}
recs = []
for r in rows:
    pe = goe[r["id"]]; ie = r["image_emotions"]
    recs.append({"id": r["id"], "text": r["text"], "key": r["dedup_key"], "pe": pe, "ie": ie,
                 "p": pe[0][0], "i": ie[0][0], "emotional": pe[0][0] != "neutral",
                 "face": is_face(r.get("vqa", {})), "vqa": r.get("vqa", {})})
emo = [r for r in recs if r["emotional"]]; non = [r for r in recs if not r["emotional"]]
face_emo = [r for r in emo if r["face"]]; scene_emo = [r for r in emo if not r["face"]]
groups_all = defaultdict(list)
for r in recs: groups_all[r["key"]].append(r)
# dedup_key is computed from the ORIGINAL text case-insensitively, but GoEmotions ran on the
# case-preserved text, so a few groups hold slightly different prompt distributions ('happy' vs 'Happy').
# Counted and reported below; the clustered null represents each group by its first record's distribution.
groups_pe_differ = sorted(k for k, g in groups_all.items() if any(x["pe"] != g[0]["pe"] for x in g))
groups_top1_differ = {str(k): {"records": [{"id": x["id"], "text": x["text"], "prompt_top1": x["p"],
                                            "emotional": x["emotional"]} for x in g]}
                      for k, g in groups_all.items() if len({x["p"] for x in g}) > 1}

def pct(x): return None if x is None else round(100 * x, 1)
def z(t, nm, ns, k): return round((t[k] - nm[k]) / ns[k], 2)
def null_block(t, nm, ns):
    return {m: {"observed_pct": pct(t[m]), "null_mean_pct": pct(nm[m]), "null_sd_pct": round(100 * ns[m], 2),
                "z": z(t, nm, ns, m)} for m in ["va", "vsign", "family", "overlap"]}
METRIC_NAMES = {"va": "va_similarity", "vsign": "valence_sign_agreement", "family": "family_agreement",
                "overlap": "top3_overlap"}
def rename(b): return {METRIC_NAMES[k]: v for k, v in b.items()}

def with_null_clustered(subset, N=N_SHUFFLES, seed=SEED):
    """Random-pairing null clustered on prompt identity: the prompt distributions are permuted ACROSS
    dedup groups (each group receives another group's prompt; records sharing a prompt move together);
    images stay with their own record. Uses a private RNG so it does not disturb the record-level null."""
    groups = defaultdict(list)
    for r in subset: groups[r["key"]].append(r)
    keys = list(groups)
    if len(keys) < 5: return None
    t = metrics([(r["pe"], r["ie"]) for r in subset])
    gp = [groups[k][0]["pe"] for k in keys]
    rng = random.Random(seed); nl = {k: [] for k in t}
    for _ in range(N):
        sh = gp[:]; rng.shuffle(sh)
        pairs = [(p, r["ie"]) for k, p in zip(keys, sh) for r in groups[k]]
        for m, v in metrics(pairs).items(): nl[m].append(v)
    return t, {k: st.mean(v) for k, v in nl.items()}, {k: (st.pstdev(v) or 1e-9) for k, v in nl.items()}, len(keys)

def specificity(subset, label):
    """VA similarity (and the other three metrics) observed vs the 300-shuffle random-pairing null,
    seed 7, both record-level (analysis_final.py procedure, fresh seed) and clustered on dedup_key."""
    pairs = [(r["pe"], r["ie"]) for r in subset]
    random.seed(SEED); t, nm, ns = with_null(pairs, N_SHUFFLES)
    out = {"label": label, "n": len(subset), "n_prompt_groups": len({r["key"] for r in subset}),
           "record_level_null": rename(null_block(t, nm, ns))}
    cl = with_null_clustered(subset)
    if cl: out["clustered_null"] = rename(null_block(cl[0], cl[1], cl[2]))
    out["va_sits_at_null"] = abs(out["record_level_null"]["va_similarity"]["z"]) < 2 and \
                             ("clustered_null" not in out or abs(out["clustered_null"]["va_similarity"]["z"]) < 2)
    return out

# =====================================================================================================
# REFERENCE CHECK — reproduce analysis_final.py's record-level numbers: same seed, same call order
# =====================================================================================================
random.seed(SEED)
ref = {}
for name, sub in [("emotional", emo), ("face", face_emo), ("scene", scene_emo),
                  ("positive", [r for r in emo if sign(r["p"]) == "+"]),
                  ("negative", [r for r in emo if sign(r["p"]) == "-"]), ("non_emotional", non)]:
    t, nm, ns = with_null([(r["pe"], r["ie"]) for r in sub], N_SHUFFLES)
    ref[name] = {"n": len(sub), **rename(null_block(t, nm, ns))}
n_repeats = len(recs) - len(groups_all)
runs = {k: g for k, g in groups_all.items() if len(g) >= 2}
counts = {"analysed": len(recs), "id_min": min(r["id"] for r in recs), "id_max": max(r["id"] for r in recs),
          "emotional": len(emo), "non_emotional": len(non),
          "face_all": sum(r["face"] for r in recs), "scene_all": sum(not r["face"] for r in recs),
          "face_within_emotional": len(face_emo), "scene_within_emotional": len(scene_emo),
          "distinct_prompts": len(groups_all), "records_repeating_an_earlier_prompt": n_repeats,
          "prompts_drawn_2plus": len(runs), "records_in_2plus_runs": sum(len(g) for g in runs.values())}
expected = {"analysed": 1012, "id_min": 14, "id_max": 1025, "emotional": 607, "non_emotional": 405,
            "face_all": 591, "scene_all": 421, "face_within_emotional": 402, "scene_within_emotional": 205,
            "distinct_prompts": 763, "records_repeating_an_earlier_prompt": 249,
            "prompts_drawn_2plus": 87, "records_in_2plus_runs": 336}
ref_expected = {("emotional", "valence_sign_agreement", "observed_pct"): 64.0,
                ("emotional", "valence_sign_agreement", "null_mean_pct"): 45.6,
                ("emotional", "valence_sign_agreement", "z"): 11.1,
                ("emotional", "family_agreement", "observed_pct"): 53.1,
                ("emotional", "family_agreement", "null_mean_pct"): 38.8,
                ("emotional", "family_agreement", "z"): 10.3,
                ("face", "valence_sign_agreement", "observed_pct"): 73.9,
                ("face", "valence_sign_agreement", "null_mean_pct"): 53.5,
                ("scene", "valence_sign_agreement", "observed_pct"): 42.9,
                ("scene", "valence_sign_agreement", "null_mean_pct"): 29.6,
                ("non_emotional", "va_similarity", "observed_pct"): 76.6,
                ("non_emotional", "va_similarity", "null_mean_pct"): 76.6}
# tolerance 0.1 (one unit in the last quoted decimal): family agreement is 322/607 = 53.048%, which is
# 53.0% at 1 dp although the reference quotes 53.1% (analysis_final.py itself prints 53%).
ref_mismatch = {f"{a}.{b}.{c}": (ref[a][b][c], v) for (a, b, c), v in ref_expected.items()
                if abs(ref[a][b][c] - v) > 0.1 + 1e-9}
def frac(sub, cond, denom_cond=lambda r: True):
    d = [r for r in sub if denom_cond(r)]; k = sum(1 for r in d if cond(r))
    return {"numerator": k, "denominator": len(d), "pct_exact": round(100 * k / len(d), 3) if d else None}
exact_fractions = {
    "emotional_valence_sign_agreement": frac(emo, lambda r: sign(r["p"]) == sign(r["i"]), lambda r: sign(r["p"]) != "0"),
    "emotional_family_agreement": frac(emo, lambda r: r["p"] == r["i"]),
    "face_valence_sign_agreement": frac(face_emo, lambda r: sign(r["p"]) == sign(r["i"]), lambda r: sign(r["p"]) != "0"),
    "scene_valence_sign_agreement": frac(scene_emo, lambda r: sign(r["p"]) == sign(r["i"]), lambda r: sign(r["p"]) != "0"),
    "face_family_agreement": frac(face_emo, lambda r: r["p"] == r["i"]),
    "scene_family_agreement": frac(scene_emo, lambda r: r["p"] == r["i"])}
count_mismatch = {k: (counts[k], v) for k, v in expected.items() if counts[k] != v}
case_variants = {"groups_with_differing_prompt_distribution": len(groups_pe_differ), "group_keys": groups_pe_differ,
                 "groups_with_differing_top1": groups_top1_differ,
                 "note": "dedup_key is case-insensitive prompt identity; GoEmotions read the case-preserved text, so "
                         "'Ok' x2 (joy 0.52) sit in the emotional set while 'ok' x6 (neutral 0.92) sit in the control, "
                         "and 'Hopeful' (id 379, neutral) sits in the control while 'hopeful' x3 (joy) are emotional. "
                         "A prompt-reader case artefact; reported, not changed."}
reference_check = {"counts": counts, "counts_expected": expected, "count_mismatches": count_mismatch,
                   "dedup_group_case_variants": case_variants,
                   "record_level_null_reproduced": ref, "exact_fractions": exact_fractions,
                   "reference_value_mismatches": ref_mismatch,
                   "passed": not count_mismatch and not ref_mismatch,
                   "note": "seed 7, 300 shuffles, with_null called in the same order as analysis_final.py "
                           "(emotional, face, scene, positive, negative, non-emotional) so the null means "
                           "are bit-identical; values compared to the quoted reference within 0.1. "
                           "Family agreement on the 607 is exactly 322/607 = 53.048% (53.0% at 1 dp; the "
                           "reference's 53.1% is a rounding slip, analysis_final.py prints 53%)."}

# =====================================================================================================
# (1) CONTROL CONTAMINATION
# =====================================================================================================
name_only = [r for r in non if r["text"].strip() == "[name]"]
name_only_ids = [r["id"] for r in name_only]
flagged = {}
word_hits = Counter()
for r in non:
    t = r["text"].lower()
    ws = [w for w, p in LEX_RE.items() if p.search(t)]
    if ws:
        flagged[r["id"]] = ws
        for w in set(ws): word_hits[w] += 1
flagged_ids = sorted(flagged)
overlap_ids = sorted(set(flagged_ids) & set(name_only_ids))
removed = set(flagged_ids) | set(name_only_ids)
cleaned = [r for r in non if r["id"] not in removed]
flagged_recs = [r for r in non if r["id"] in flagged]

control = {
    "definition": "non-emotional = GoEmotions top-1 family == 'neutral' (never human-checked)",
    "n_control": len(non),
    "lexicon_size": len(LEXICON), "lexicon": LEXICON,
    "lexicon_rule": "exact word forms, case-insensitive, word-boundary search on the redacted prompt text; "
                    "no stemming, no misspellings, no non-English words -> a LOWER bound on contamination",
    "name_only_records": {"ids": name_only_ids, "n": len(name_only_ids),
                          "note": "text is exactly '[name]' after redaction: empty prompts, not non-emotional"},
    "lexicon_flagged": {"n": len(flagged_ids), "pct_of_control": pct(len(flagged_ids) / len(non)),
                        "distinct_words_hit": len(word_hits),
                        "top20_words": [{"word": w, "records": c} for w, c in word_hits.most_common(20)],
                        "records": [{"id": i, "text": next(r["text"] for r in non if r["id"] == i), "words": flagged[i]}
                                    for i in flagged_ids]},
    "overlap_name_only_and_flagged": overlap_ids,
    "n_removed": len(removed), "n_cleaned": len(cleaned),
    "notes": ["'content' hits (8) were checked by eye: all use the affective sense ('content', 'stuffed full with "
              "pancakes but content', 'content calm meditative').",
              "Non-English affect prompts exist in the control (French 'stress ... joie' x6 — caught only via the "
              "English word 'stress'; Italian 'ansiosa', 'preoccupato'; German 'neugierig') and misspelt English "
              "affect words ('ecited', 'curios', 'thrillled', 'comfused') — not counted by the lexicon.",
              "Contamination changes what the 405 are, not the pipeline's result on them: agreement is at its "
              "null before and after cleaning (see specificity)."],
    "specificity": {
        "full_control_405": specificity(non, "all 405 non-emotional prompts (reference procedure, fresh seed 7)"),
        "cleaned_control": specificity(cleaned, "cleaned control: minus '[name]' records and lexicon-flagged records"),
        "flagged_subset": specificity(flagged_recs, "the lexicon-flagged records alone (do they show agreement?)")}}

# =====================================================================================================
# (2) DESCRIBER LEAK
# =====================================================================================================
two_by_two = Counter()
for r in recs:
    two_by_two[("people_ge1" if n_people(r["vqa"].get("people", "")) >= 1 else "people_0",
                "expression_word_present" if has_expression_word(r["vqa"]) else "expression_word_absent")] += 1
scene_all = [r for r in recs if not r["face"]]
scene_p0 = [r for r in scene_all if n_people(r["vqa"].get("people", "")) == 0]
scene_p0_expr = [r for r in scene_p0 if has_expression_word(r["vqa"])]
scene_p0_smile = [r for r in scene_p0 if (r["vqa"].get("expression", "") or "").lower().strip() in {"smile", "smiling", "happy"}]
scene_p_ge1 = [r for r in scene_all if n_people(r["vqa"].get("people", "")) >= 1]
p0_answers = Counter((r["vqa"].get("expression", "") or "").lower().strip() for r in scene_p0)

bare = [(r, bare_answer(r["vqa"])) for r in recs]
bare = [(r, a) for r, a in bare if a]
named = [(r, a) for r, a in bare if a in NAMED_EMOTION_WORDS]
def copy_stats(pairs):
    n = len(pairs); c = sum(1 for r, a in pairs if r["i"] == EXPRESSION_FAMILY[a])
    by_fam = defaultdict(lambda: [0, 0])
    for r, a in pairs:
        f = EXPRESSION_FAMILY[a]; by_fam[f][0] += 1; by_fam[f][1] += (r["i"] == f)
    return {"n": n, "copied": c, "copy_rate_pct": pct(c / n) if n else None,
            "by_implied_family": {f: {"n": v[0], "copied": v[1], "copy_rate_pct": pct(v[1] / v[0])}
                                  for f, v in sorted(by_fam.items(), key=lambda x: -x[1][0])}}
image_marg_all = Counter(r["i"] for r in recs)
per_answer = []
for a, n in Counter((r["vqa"].get("expression", "") or "").lower().strip() for r in recs).most_common():
    sub = [r for r in recs if (r["vqa"].get("expression", "") or "").lower().strip() == a]
    fam = EXPRESSION_FAMILY.get(a) if " " not in a else None
    per_answer.append({"answer": a, "n": n, "implied_family": fam,
                       "image_top1": dict(Counter(r["i"] for r in sub).most_common()),
                       "copy_rate_pct": pct(sum(1 for r in sub if r["i"] == fam) / n) if fam else None})
not_bare = [r for r in recs if not bare_answer(r["vqa"])]
SMILE = {"smile", "smiling", "happy"}
def smile_share(sub):
    k = sum(1 for r in sub if (r["vqa"].get("expression", "") or "").lower().strip() in SMILE)
    return {"smile_smiling_happy": k, "n": len(sub), "pct": pct(k / len(sub)) if sub else None}
face_all = [r for r in recs if r["face"]]
people_ge1 = [r for r in recs if n_people(r["vqa"].get("people", "")) >= 1]
describer = {
    "definition": "people-count via n_people() and expression word via EXPRESSION_WORDS, both copied from analysis_final.py; "
                  "face = people>=1 AND expression word; scene = everything else",
    "two_by_two_all_1012": {f"{a}|{b}": two_by_two[(a, b)] for a in ["people_ge1", "people_0"]
                            for b in ["expression_word_present", "expression_word_absent"]},
    "scene_classified": {
        "n": len(scene_all),
        "people_0": len(scene_p0),
        "people_0_with_expression_word": len(scene_p0_expr),
        "people_0_answer_smile_smiling_happy": len(scene_p0_smile),
        "people_0_answer_smile_smiling_happy_pct_of_people_0": pct(len(scene_p0_smile) / len(scene_p0)),
        "people_0_expression_answers": dict(p0_answers.most_common()),
        "people_ge1_but_no_expression_word": [{"id": r["id"], "people": r["vqa"].get("people"),
                                              "expression": r["vqa"].get("expression")} for r in scene_p_ge1],
        "note": "ids 46 and 50 answer 'anger' with 1 person: 'anger' is not in EXPRESSION_WORDS (only 'angry'), "
                "so the frozen rule files them as scene. Reported, not changed."},
    "bare_expression_word_corpus_wide": {
        "definition_broad": "expression answer is a single token in EXPRESSION_FAMILY (facial actions such as 'smile' included)",
        "definition_strict": "expression answer is a single token in NAMED_EMOTION_WORDS (names an affective state)",
        "expression_family_map": EXPRESSION_FAMILY, "named_emotion_words": sorted(NAMED_EMOTION_WORDS),
        "broad": {"n": len(bare), "rate_pct": pct(len(bare) / len(recs))},
        "strict": {"n": len(named), "rate_pct": pct(len(named) / len(recs))}},
    "copy_rate": {
        "definition": "share of records where the image reader's top-1 family == the family implied by the bare expression word",
        "broad": copy_stats(bare), "strict": copy_stats(named),
        "broad_within_people_0": copy_stats([(r, a) for r, a in bare if n_people(r["vqa"].get("people", "")) == 0]),
        "broad_within_people_ge1": copy_stats([(r, a) for r, a in bare if n_people(r["vqa"].get("people", "")) >= 1]),
        "broad_affect_families_only": copy_stats([(r, a) for r, a in bare if EXPRESSION_FAMILY[a] != "neutral"]),
        "context_image_top1_marginal_all_1012_pct": {f: pct(image_marg_all[f] / len(recs)) for f in FAMS},
        "context_records_without_bare_word": {"n": len(not_bare),
                                              "image_top1": dict(Counter(r["i"] for r in not_bare).most_common())}},
    "per_answer_table": per_answer,
    "smile_share": {"all_1012": smile_share(recs), "face_classified_591": smile_share(face_all),
                    "people_ge1_598": smile_share(people_ge1), "scene_people_0_414": smile_share(scene_p0),
                    "note": "RESULTS_final.md says BLIP-VQA 'reads ~66% of faces as smiling': 66% is the corpus-wide "
                            "share of smile/smiling/happy answers over all 1,012 records (people or not); within the "
                            "591 face-classified records the share is lower (see face_classified_591)."},
    "notes": ["Strict tier: whenever BLIP-VQA names an affective state (happy, sad, angry, surprised, calm, ...), the "
              "image reader's top-1 family is that state in 417 of 418 records — the NLI stage reproduces the "
              "describer's word rather than adding a reading of its own.",
              "'serious' (103 answers) is mapped a priori to neutral, but the reader returns sadness 71 / anger 15 / "
              "neutral 8 / surprise 5 / fear 4 — it reads 'serious' as negative valence. Counted as non-copy here; "
              "under a 'serious -> sadness' mapping the broad copy rate would be higher, not lower.",
              "Facial-action words ('smile' 299, 'smiling' 165) are read as joy only ~53% of the time, and only 37.7% "
              "when the description also says there are no people ('A drawing of none ...'); the remainder go to "
              "neutral or surprise. This is the leak into the scene group: 332 of the 414 people=0 scene records "
              "still say smile/smiling/happy, and the reader returns joy for 125 of them."]}

# =====================================================================================================
# (3) PER-FAMILY BREAKDOWN on the 607 emotional records
# =====================================================================================================
cm = Counter((r["p"], r["i"]) for r in emo)
confusion = {p: {i: cm[(p, i)] for i in FAMS} for p in FAMS}
row_tot = {p: sum(confusion[p].values()) for p in FAMS}
col_tot = {i: sum(confusion[p][i] for p in FAMS) for i in FAMS}
assert sum(row_tot.values()) == len(emo) == 607
groups_emo = defaultdict(list)
for r in emo: groups_emo[r["key"]].append(r)
keys_emo = list(groups_emo); rng = random.Random(SEED)
draws = {f: [] for f in FAMS}
for _ in range(B_BOOT):
    samp = [x for k in (rng.choice(keys_emo) for _ in keys_emo) for x in groups_emo[k]]
    cnt = Counter(); hit = Counter()
    for r in samp:
        cnt[r["p"]] += 1; hit[r["p"]] += (r["p"] == r["i"])
    for f in FAMS:
        if cnt[f]: draws[f].append(hit[f] / cnt[f])
def q(v, p): return sorted(v)[int(p * (len(v) - 1))]
recall = {}
for f in FAMS:
    n = row_tot[f]
    recall[f] = {"n_prompts": n, "agreed": confusion[f][f],
                 "recall_pct": pct(confusion[f][f] / n) if n else None,
                 "ci95_pct": [pct(q(draws[f], .025)), pct(q(draws[f], .975))] if draws[f] else None,
                 "bootstrap_draws_with_family_present": len(draws[f])}
image_marg_emo = Counter(r["i"] for r in emo)
per_family = {
    "n": len(emo),
    "confusion_prompt_family_x_image_family": confusion,
    "row_totals_prompt_family": row_tot, "column_totals_image_family": col_tot,
    "trace": sum(confusion[f][f] for f in FAMS),
    "family_agreement_pct": pct(sum(confusion[f][f] for f in FAMS) / len(emo)),
    "recall_by_prompt_family": recall,
    "bootstrap": f"clustered on dedup_key: {len(keys_emo)} prompt groups resampled with replacement, "
                 f"B={B_BOOT}, seed {SEED}; percentile 95% CI (same convention as significance.py)",
    "image_reader_marginals": {
        "all_1012": {f: image_marg_all[f] for f in FAMS},
        "emotional_607": {f: image_marg_emo[f] for f in FAMS},
        "never_or_almost_never_returned": {f: image_marg_all[f] for f in FAMS if image_marg_all[f] <= 10}},
    "prompt_reader_marginals_all_1012": {f: Counter(r["p"] for r in recs)[f] for f in FAMS},
    "notes": ["the 'neutral' row is empty by construction (emotional = prompt top-1 != neutral).",
              "fear (16 prompts) and disgust (1 prompt) have 0 agreed records; the image reader returns "
              "fear 4 times and disgust 0 times across all 1,012 records, so those families cannot agree."]}

# =====================================================================================================
out = {"meta": {"script": "audits.py", "inputs": ["outputs/describe_extract.jsonl", "outputs/prompt_emotions_goe.json"],
                "analysed_ids": f"{counts['id_min']}..{counts['id_max']} ({counts['analysed']} records; pre-test ids 1-13 dropped)",
                "seed": SEED, "null_shuffles": N_SHUFFLES, "bootstrap_draws": B_BOOT,
                "central_quantity": "agreement between the prompt reader (GoEmotions) and the image reader (NLI over the BLIP-VQA description)"},
       "reference_check": reference_check, "control_contamination": control,
       "describer_leak": describer, "per_family": per_family}
json.dump(out, open(os.path.join(OUT, "audits.json"), "w"), indent=1, ensure_ascii=False)

# ---------- printed summary ----------
print(f"=== AUDITS — {len(recs)} analysed records (ids {counts['id_min']}..{counts['id_max']}) ===")
print(f"reference check: {'PASS' if reference_check['passed'] else 'FAIL'}  count mismatches={count_mismatch}  value mismatches={ref_mismatch}")
r = ref["emotional"]
print(f"  emotional n={r['n']}: sign {r['valence_sign_agreement']['observed_pct']}% vs null {r['valence_sign_agreement']['null_mean_pct']}% z{r['valence_sign_agreement']['z']:+}; "
      f"family {r['family_agreement']['observed_pct']}% vs {r['family_agreement']['null_mean_pct']}% z{r['family_agreement']['z']:+}")
print(f"  face sign {ref['face']['valence_sign_agreement']['observed_pct']}%/{ref['face']['valence_sign_agreement']['null_mean_pct']}%  "
      f"scene {ref['scene']['valence_sign_agreement']['observed_pct']}%/{ref['scene']['valence_sign_agreement']['null_mean_pct']}%  "
      f"non-emotional VA {ref['non_emotional']['va_similarity']['observed_pct']}%/{ref['non_emotional']['va_similarity']['null_mean_pct']}%")

print(f"\n(1) CONTROL CONTAMINATION — {len(non)} non-emotional prompts, lexicon of {len(LEXICON)} words")
print(f"  '[name]'-only records: {name_only_ids}")
print(f"  lexicon-flagged: {len(flagged_ids)} ({pct(len(flagged_ids)/len(non))}%), {len(word_hits)} distinct words hit")
print("  top words: " + ", ".join(f"{w} x{c}" for w, c in word_hits.most_common(20)))
print(f"  cleaned control: {len(cleaned)} = {len(non)} - {len(name_only_ids)} - {len(flagged_ids)} (overlap {overlap_ids})")
for k in ["full_control_405", "cleaned_control", "flagged_subset"]:
    s = control["specificity"][k]; a = s["record_level_null"]["va_similarity"]; c = s.get("clustered_null", {}).get("va_similarity")
    print(f"  {k:18s} n={s['n']:3d} groups={s['n_prompt_groups']:3d}  VA {a['observed_pct']}% vs null {a['null_mean_pct']}% z{a['z']:+}"
          + (f"  | clustered null {c['null_mean_pct']}% z{c['z']:+}" if c else "") + f"  -> at null: {s['va_sits_at_null']}")
    fa = s["record_level_null"]["family_agreement"]; print(f"  {'':18s} family {fa['observed_pct']}% vs null {fa['null_mean_pct']}% z{fa['z']:+}")

print(f"\n(2) DESCRIBER LEAK")
print(f"  2x2 (all {len(recs)}): " + "  ".join(f"{k}={v}" for k, v in describer['two_by_two_all_1012'].items()))
sc = describer["scene_classified"]
print(f"  scene-classified {sc['n']}: people=0 {sc['people_0']}; of those with an expression word {sc['people_0_with_expression_word']}; "
      f"answering smile/smiling/happy {sc['people_0_answer_smile_smiling_happy']}; people>=1 without expression word {len(sc['people_ge1_but_no_expression_word'])}")
bw = describer["bare_expression_word_corpus_wide"]; cr = describer["copy_rate"]
print(f"  bare expression word: broad {bw['broad']['n']}/{len(recs)} = {bw['broad']['rate_pct']}%; strict (named emotion) {bw['strict']['n']}/{len(recs)} = {bw['strict']['rate_pct']}%")
print(f"  copy rate (image top-1 == implied family): broad {cr['broad']['copied']}/{cr['broad']['n']} = {cr['broad']['copy_rate_pct']}%; "
      f"strict {cr['strict']['copied']}/{cr['strict']['n']} = {cr['strict']['copy_rate_pct']}%; "
      f"people=0 only {cr['broad_within_people_0']['copied']}/{cr['broad_within_people_0']['n']} = {cr['broad_within_people_0']['copy_rate_pct']}%")
print("  by implied family (broad): " + ", ".join(f"{f} {v['copied']}/{v['n']}={v['copy_rate_pct']}%" for f, v in cr['broad']['by_implied_family'].items()))

print(f"\n(3) PER-FAMILY — {len(emo)} emotional records, rows = prompt family, cols = {FAMS}")
for f in FAMS: print(f"  {f:9s} {[confusion[f][i] for i in FAMS]}  n={row_tot[f]:3d}  recall {recall[f]['recall_pct']}%  CI95 {recall[f]['ci95_pct']}")
print(f"  column totals (image family): {col_tot}")
print(f"  image reader marginals, all 1012: {per_family['image_reader_marginals']['all_1012']}")
print(f"\nsaved outputs/audits.json")
