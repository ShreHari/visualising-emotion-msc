#!/usr/bin/env python3
"""
emoviz/error_taxonomy.py — qualitative error taxonomy of HIGH-CONFIDENCE DISAGREEMENTS between the
prompt reader (GoEmotions, 28 -> 7 families) and the image reader (BLIP-VQA -> description -> NLI).

Discussion-chapter material. The quantitative results say WHERE the two readers agree (faces more than
scenes, emotional prompts above the random-pairing null); this script asks WHY they disagree when both
are confident, by (1) selecting every emotional record whose prompt top-1 score >= 0.8 AND image top-1
score >= 0.8 AND whose two top-1 families differ, (2) auto-tagging each with cheap diagnostic flags, and
(3) recording ONE primary failure mode per record, assigned by a human looking at the actual drawing.

Selection and tagging are automatic and reproducible. The failure-mode assignments are human judgments
(the MANUAL_MODES table below); they are stored in the script so the JSON can be regenerated and so a
marker can open the same image_path and check each call.

Population note: at these thresholds the population is small (38 records, 37 distinct prompts), below
the target sample of 40, so the "sample" is a CENSUS of every high-confidence disagreement; the four
largest confusion cells are still identified and the per-cell breakdown is reported. The sampling code
clusters on dedup_key (prompt identity) in case a re-run with looser thresholds ever exceeds the target.

Inputs (read only): outputs/describe_extract.jsonl, outputs/prompt_emotions_goe.json.
Outputs: outputs/error_taxonomy.json, outputs/ERROR_TAXONOMY.md.
Run:  .venv/bin/python error_taxonomy.py
"""
import json, os, re, math, random, statistics as st
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
PRETEST_MAX_ID = 13          # ids 1-13 = pre-festival developer tests (same rule as analysis_final.py)
CONF = 0.8                   # both readers' top-1 score must be >= CONF
TARGET = 40                  # stratified sample size; population below this -> census
N_CELLS = 4                  # stratify across the N largest prompt-family x image-family cells
SEED = 7
FAMILIES = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]

# ---------------------------------------------------------------------------------------------
# Copied VERBATIM from analysis_final.py (that module runs its whole analysis on import, so it is not
# imported; the constants and functions below are duplicated here so the classification rules are
# identical: CEN, POS/NEG, G2F, EXPRESSION_WORDS, NUMWORDS, sign, n_people, is_face, va_point, va_sim,
# soft, metrics, with_null).
# ---------------------------------------------------------------------------------------------
CEN = {"joy": (0.8, 0.6), "sadness": (-0.75, 0.3), "anger": (-0.7, 0.8), "fear": (-0.65, 0.75),
       "surprise": (0.3, 0.8), "disgust": (-0.7, 0.6), "neutral": (0.0, 0.3)}   # emotion -> (valence,arousal)
POS, NEG = {"joy"}, {"sadness", "anger", "fear", "disgust"}
# GoEmotions 28 labels -> 7 Ekman families (standard grouping)
G2F = {**dict.fromkeys(["admiration","amusement","approval","caring","desire","excitement","gratitude","joy","love","optimism","pride","relief"], "joy"),
       **dict.fromkeys(["disappointment","embarrassment","grief","remorse","sadness"], "sadness"),
       **dict.fromkeys(["anger","annoyance","disapproval"], "anger"),
       **dict.fromkeys(["fear","nervousness"], "fear"),
       **dict.fromkeys(["surprise","realization","confusion","curiosity"], "surprise"),
       "disgust": "disgust", "neutral": "neutral"}
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
# ---------------------------------------------------------------------------------------------
# end of verbatim copy
# ---------------------------------------------------------------------------------------------

# ---- fixed failure-mode set (one PRIMARY mode per record) ----
MODES = {
    "a": "describer hallucinated a face/expression where none exists",
    "b": "describer read the expression wrongly",
    "c": "reader mis-inferred from a correct description",
    "d": "prompt is ambiguous or mixed",
    "e": "genuine generator failure - the drawing does not depict the prompt",
    "f": "prompt reader wrong",
}

# ---- HUMAN ASSIGNMENTS: id -> (mode, one-line justification), made by opening image_path for every
# record in the census and comparing the drawing with the prompt, the VQA answers, the description
# and the two readings. A record absent from this table is written with primary_mode = null.
# Tie-break rule used when more than one stage is at fault: a failure VISIBLE in the drawing itself
# (a face/expression reported where none is drawn; a drawn expression named wrongly; a drawing that shows
# a different feeling) is primary; (d) is used when the prompt lists several feelings or names none
# cleanly, so that no single-family reading could agree; (c) when the description is true to the
# drawing and the label is lost between description and family; (f) when the prompt is clear and
# single-feeling but its family is wrong. Secondary faults are recorded in the note.
MANUAL_MODES = {
    18:   ("a", "silhouette figures with no facial features in a rescue centre; describer reports 'happy' (5 people). "
                "Secondary: 'feeling emotional' is read as sadness 0.87, which a person would call ambiguous"),
    19:   ("a", "two hands on a keyboard, no face anywhere; describer reports 'angry', 2 people"),
    39:   ("b", "woman reading by the fire with a cat, eyes lowered, serene; describer calls the downcast reading face 'sad'"),
    65:   ("d", "prompt lists hopeful / slightly anxious / resigned / detached; drawing is nine labelled head profiles with "
                "no expressions, so 'angry' is also hallucinated, but no single family could agree with this list"),
    66:   ("d", "same mixed list as 65; drawing is a pensive woman with eyes closed and head bowed - 'sad' is a fair "
                "reading of the resigned/detached part; the joy reading comes from 'hopeful'"),
    89:   ("c", "'grateful' drawn as a meditating figure on a mountain; description 'calm, sitting' is true to the drawing; the "
                "reader maps calm to neutral because no family holds low-arousal positive states"),
    93:   ("d", "'celebratory anguish' is an oxymoron; drawing is a split face, one half frowning, one half crying, "
                "with balloons and confetti - it depicts the mix exactly; 'angry' is a partial mis-read of the frown"),
    107:  ("c", "'free from stress, hopeful' drawn as a silhouette rising from broken chains; description 'standing, "
                "calm' is true to the drawing but drops the chains, and calm is mapped to neutral"),
    137:  ("e", "'i am excited' drawn as a screaming face with bared teeth, furrowed brows and lightning; the describer's "
                "'angry' is what the drawing shows (people-count 0 is wrong but the expression is not)"),
    192:  ("b", "'happy and tired' drawn as a man lying back with a contented smile; describer answers action 'smiling' "
                "yet expression 'angry' - the description contradicts itself and the reader follows 'angry'"),
    202:  ("b", "'my tummy hurts' drawn as a figure bent over clutching its stomach; the pain grimace is called 'angry' "
                "(scene 'monkey' is also wrong); pain itself has no family on either side"),
    214:  ("d", "prompt lists happy / tired / sleepy / hungry; drawing is a grid of twelve yawning, dozing, coffee-clutching "
                "figures - the tired part is drawn, 'angry' is a fair read of the grumpy ones, joy is the prompt's 'happy'"),
    216:  ("d", "'in pain every day ... had enough of it' mixes pain (sadness) with exasperation (anger); drawing is an "
                "abstract circle of straining silhouettes with a brain; both readings sit inside the prompt's mix"),
    231:  ("c", "'happy heart' drawn as a heart with a smiling face; description says 'smiling' and 'smile' but also "
                "'a drawing of none'; the reader returns neutral 0.95 from a description that names a smile twice"),
    232:  ("c", "second run of the same prompt: heart with a smiling face; description names 'smiling' and 'smile'; "
                "reader returns neutral 0.82"),
    242:  ("a", "'love' drawn as leaves forming a heart shape on black, no face; describer reports 'sad' with action 'no person'"),
    287:  ("d", "'happy mixed emotions' drawn as a large face built from dozens of small faces, most of them frowning, with "
                "rain clouds and tears; the drawing shows the mix with a sad tilt and 'sad' is a fair read of it"),
    295:  ("b", "'energetic grateful and happy' drawn as a woman dancing with arms flung out and mouth open; the small "
                "open-mouthed face is called 'angry'"),
    363:  ("a", "'happy, relaxed, open minded' drawn as abstract circles and dot patterns, no figure; describer reports "
                "'surprised' with action 'no person'"),
    436:  ("f", "'an impressed baby in a bearsuit' drawn as a baby in a bear suit with wide eyes and an O-shaped mouth; "
                "describer's 'surprise' is right; the prompt reader's raw label is admiration 0.92, which the 28-to-7 "
                "mapping sends to joy, whereas a person would accept surprise for 'impressed'"),
    547:  ("d", "'confused' has no family: the raw label confusion 0.92 is mapped to surprise; drawing is scowling faces "
                "among question marks, so 'angry' has visible support; neither family is what a person would name"),
    594:  ("b", "'excited and happy' drawn as a crowd laughing with heads thrown back in falling snow; the laughing faces "
                "are called 'surprise'"),
    608:  ("b", "'excited' drawn as a concert crowd looking up with open mouths and raised arms; describer picks 'surprise' "
                "for faces a person would call excited or awed - excitement and surprise share the open-mouth pattern"),
    627:  ("a", "'I am confused' drawn as a landscape (palms beside a pine and a snowy peak), no people; describer reports "
                "'happy' and 'swimming' with people 0. Secondary: the drawing shows no feeling at all"),
    640:  ("b", "'tired and happy but excited' drawn as a shouting profile with geometric shapes bursting from the head; "
                "'angry' is a defensible read of the open mouth, so this is a soft call; the prompt is also mixed"),
    648:  ("d", "prompt lists tired / elated / hopeful / excited; drawing is a woman with head thrown back, eyes shut, fists "
                "clenched - the tired/exasperated part is drawn and 'angry' is a fair read of it"),
    677:  ("a", "'ecstatic about my new tattoo' drawn as a rat tattoo design with a name banner, no human face; describer "
                "reports 'surprised' with action 'no person'"),
    692:  ("c", "'calm but tired, happy it is the weekend' drawn as a man reclining in a deckchair by water; description "
                "'sunbathing, reclined, calm' is true to the drawing; calm is mapped to neutral"),
    726:  ("a", "'good' drawn as a mountain-and-lake landscape with no people; describer reports 'surfing' and 'calm' with "
                "people 0. Secondary: a one-word prompt gave the generator no feeling to draw, so neutral would follow anyway"),
    729:  ("b", "'excited to discover new things' drawn as a crowd with cameras and a magnifying glass, mouths open, brows "
                "raised; describer picks 'surprise' for faces that show discovery - the same excitement/surprise boundary as 608"),
    753:  ("d", "prompt lists tired / sleepy / chilled / slightly worried / enjoying / hungry; drawing is a man with hand on "
                "chin and thought bubbles labelled 'mild concerns' - the worried part is drawn; 'confused' is a fair read"),
    771:  ("e", "'excited to draw with the printer' drawn as a man with bared teeth, clenched fists and pencils exploding "
                "around him; the face reads as rage, and the describer's 'angry' is what is drawn"),
    820:  ("b", "'overcharged excitement' drawn as a shouting profile with shapes bursting outward; 'surprised' is the "
                "describer's word for an open-mouthed exclaiming face"),
    829:  ("a", "'good wierd' drawn as an abstract swirl with a single eye inside a circle, no face; describer reports 'sad' "
                "and 'sitting' with people 0"),
    970:  ("a", "'hope and care' drawn as two hands cradling a sprouting plant under a sun, no face; describer reports 'sad' "
                "with 'holding hands'"),
    988:  ("d", "prompt lists tired / proud / happy; drawing is the same man three times, twice frowning with a hand on his "
                "head and once smiling - the tired part dominates and 'angry' is a fair read of the frowns"),
    1011: ("d", "prompt lists proud / happy / tired; drawing is a sweat-soaked runner slumped with mouth open in a city - the "
                "tired part is drawn; 'surprised' is additionally a mis-read of a panting face"),
    1015: ("b", "'unhappy because I'm not getting my go on the VR machine' drawn as one figure in a headset with arms crossed "
                "and another sitting and crying loudly; the crying face is called 'angry' (the headset figure does look cross)"),
}

AMBIG_RAW = {"curiosity", "realization", "confusion"}    # raw GoEmotions labels that flag an ambiguous prompt
MIXED_RE = re.compile(r"\b(but|although|though|yet)\b", re.I)
BARE_WORDS = EXPRESSION_WORDS | set(FAMILIES) | {"happiness"}   # single-token expression answers

# ---------- load, drop pre-test ----------
rows = [json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8")]
rows = [r for r in rows if r["id"] > PRETEST_MAX_ID]
goe = {int(k): v for k, v in json.load(open(os.path.join(OUT, "prompt_emotions_goe.json"))).items()}
missing = [r["id"] for r in rows if r["id"] not in goe]
if missing: raise SystemExit(f"prompt-emotion cache is stale ({len(missing)} ids missing)")

recs = []
for r in rows:
    pe = goe[r["id"]]; ie = r["image_emotions"]
    recs.append({"id": r["id"], "text": r["text"], "dedup_key": r.get("dedup_key", r["text"].strip().lower()),
                 "pe": pe, "ie": ie, "prompt_top": pe[0][0], "image_top": ie[0][0],
                 "emotional": pe[0][0] != "neutral", "face": is_face(r.get("vqa", {})),
                 "vqa": r.get("vqa", {}), "description": r.get("description", ""),
                 "image_path": r["image_path"]})

# ---------- VERIFICATION against the published reference values (analysis_final.py, seed 7) ----------
# analysis_final.py seeds random once and then calls with_null in the order ALL-emotional, face, scene,
# positive, negative, non-emotional. Replaying the same sequence reproduces its null means and z-scores.
def _check(name, got, ref, tol):
    ok = abs(got - ref) <= tol
    print(f"  {'ok ' if ok else 'XX '} {name:42s} got {got:.4f}  ref {ref:.4f}")
    return ok

print("=== verification vs published reference values ===")
emo = [r for r in recs if r["emotional"]]; non = [r for r in recs if not r["emotional"]]
face = [r for r in emo if r["face"]]; scene = [r for r in emo if not r["face"]]
checks = [
    _check("analysed records", len(recs), 1012, 0),
    _check("emotional prompts", len(emo), 607, 0), _check("non-emotional prompts", len(non), 405, 0),
    _check("face images (all)", sum(r["face"] for r in recs), 591, 0),
    _check("scene images (all)", sum(not r["face"] for r in recs), 421, 0),
    _check("face images within emotional", len(face), 402, 0),
    _check("scene images within emotional", len(scene), 205, 0),
]
random.seed(SEED)
def _z(t, nm, ns, k): return (t[k] - nm[k]) / ns[k]
t, nm, ns = with_null([(r["pe"], r["ie"]) for r in emo])
checks += [_check("emotional valence-sign agreement", t["vsign"], 0.640, 0.0005),
           _check("emotional valence-sign null", nm["vsign"], 0.456, 0.0005),
           _check("emotional valence-sign z", _z(t, nm, ns, "vsign"), 11.1, 0.05),
           # published as 53.1%; the exact rate is 322/607 = 53.05%, which rounds half-up to 53.1%
           _check("emotional family agreement (322/607)", t["family"], 322/607, 1e-9),
           _check("emotional family null", nm["family"], 0.388, 0.0005),
           _check("emotional family z", _z(t, nm, ns, "family"), 10.3, 0.05)]
tf, nmf, nsf = with_null([(r["pe"], r["ie"]) for r in face])
ts, nms, nss = with_null([(r["pe"], r["ie"]) for r in scene])
checks += [_check("face valence-sign agreement", tf["vsign"], 0.739, 0.0005),
           _check("face valence-sign null", nmf["vsign"], 0.535, 0.0005),
           _check("face valence-sign z", _z(tf, nmf, nsf, "vsign"), 10.4, 0.05),
           _check("face family agreement", tf["family"], 0.619, 0.0005),
           _check("scene valence-sign agreement", ts["vsign"], 0.429, 0.0005),
           _check("scene valence-sign null", nms["vsign"], 0.296, 0.0005),
           _check("scene valence-sign z", _z(ts, nms, nss, "vsign"), 5.8, 0.05),
           _check("scene family agreement", ts["family"], 0.356, 0.0005)]
with_null([(r["pe"], r["ie"]) for r in emo if sign(r["prompt_top"]) == "+"])   # replay positive
with_null([(r["pe"], r["ie"]) for r in emo if sign(r["prompt_top"]) == "-"])   # replay negative
tn, nmn, nsn = with_null([(r["pe"], r["ie"]) for r in non])
checks += [_check("non-emotional VA similarity", tn["va"], 0.766, 0.0005),
           _check("non-emotional VA null", nmn["va"], 0.766, 0.0005)]
if not all(checks): raise SystemExit("verification against reference values FAILED - see XX lines above")
print(f"  all {len(checks)} reference checks reproduced\n")

# ---------- population: high-confidence disagreements ----------
pop = [r for r in emo if r["pe"][0][1] >= CONF and r["ie"][0][1] >= CONF and r["prompt_top"] != r["image_top"]]
cells = Counter((r["prompt_top"], r["image_top"]) for r in pop)
top_cells = [c for c, _ in cells.most_common(N_CELLS)]
print(f"=== high-confidence disagreements (both top-1 scores >= {CONF}, families differ) ===")
print(f"  population {len(pop)} records, {len({r['dedup_key'] for r in pop})} distinct prompts, "
      f"out of {len(emo)} emotional records")
for (p, i), n in cells.most_common():
    print(f"    prompt {p:9s} -> image {i:9s} {n:3d}{'   (stratum)' if (p, i) in top_cells else ''}")

# ---------- stratified sample, clustered on dedup_key ----------
rng = random.Random(SEED)
census = len(pop) <= TARGET
if census:
    sample = sorted(pop, key=lambda r: r["id"])
    print(f"  population ({len(pop)}) <= target ({TARGET}): taking the whole population (census)")
else:
    # allocate TARGET across the N largest cells in proportion (largest remainder), then draw PROMPT
    # GROUPS without replacement inside each cell so a repeated prompt cannot enter twice.
    tot = sum(cells[c] for c in top_cells)
    quota = {c: int(TARGET * cells[c] / tot) for c in top_cells}
    for c in sorted(top_cells, key=lambda c: -(TARGET * cells[c] / tot - quota[c]))[:TARGET - sum(quota.values())]:
        quota[c] += 1
    sample = []
    for c in top_cells:
        groups = defaultdict(list)
        for r in pop:
            if (r["prompt_top"], r["image_top"]) == c: groups[r["dedup_key"]].append(r)
        keys = sorted(groups); rng.shuffle(keys)
        picked = []
        for k in keys:
            if len(picked) >= quota[c]: break
            picked.append(min(groups[k], key=lambda r: r["id"]))    # one record per prompt group
        sample += picked
    sample.sort(key=lambda r: r["id"])
    print(f"  stratified sample of {len(sample)} across {N_CELLS} largest cells, quotas {quota}")

# ---------- raw 28-label GoEmotions top label for the sampled prompts (not in the cache) ----------
print("\n[GoEmotions raw 28-label pass on the sampled prompts ...]")
import torch
from transformers import pipeline
dev = "mps" if torch.backends.mps.is_available() else "cpu"
clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None,
               truncation=True, device=dev, batch_size=32)
raw_preds = clf([r["text"] for r in sample])
raw_top = {}
for r, pred in zip(sample, raw_preds):
    best = max(pred, key=lambda d: d["score"])
    raw_top[r["id"]] = (best["label"], round(float(best["score"]), 4))
    # consistency: aggregating these raw scores by family must reproduce the frozen cache's top-1 family
    fam = {}
    for d in pred: fam[G2F.get(d["label"], "neutral")] = fam.get(G2F.get(d["label"], "neutral"), 0) + d["score"]
    tot = sum(fam.values()) or 1.0
    top_fam, top_s = max(fam.items(), key=lambda x: x[1])
    if top_fam != r["prompt_top"] or abs(top_s / tot - r["pe"][0][1]) > 0.01:
        raise SystemExit(f"raw GoEmotions re-run disagrees with the frozen cache for id {r['id']}: "
                         f"{top_fam} {top_s/tot:.4f} vs {r['pe'][0]}")
print(f"  raw labels for {len(raw_top)} prompts; family aggregation reproduces the frozen cache for all")

# ---------- auto-tags ----------
def bare_emotion_word(expr):
    toks = re.findall(r"[a-z]+", (expr or "").lower())
    return len(toks) == 1 and toks[0] in BARE_WORDS

def tags_for(r):
    return {
        "people_zero": n_people(r["vqa"].get("people", "")) == 0,
        "bare_expression_word": bare_emotion_word(r["vqa"].get("expression", "")),
        "mixed_feeling_connective": bool(MIXED_RE.search(r["text"])),
        "ambiguous_raw_label": raw_top[r["id"]][0] in AMBIG_RAW,
        "short_prompt": len(r["text"].split()) <= 2,
    }

TAG_NAMES = ["people_zero", "bare_expression_word", "mixed_feeling_connective", "ambiguous_raw_label", "short_prompt"]
out_sample = []
for r in sample:
    tg = tags_for(r)
    m = MANUAL_MODES.get(r["id"])
    out_sample.append({
        "id": r["id"], "dedup_key": r["dedup_key"],
        "cell": f"{r['prompt_top']}->{r['image_top']}", "in_stratum": (r["prompt_top"], r["image_top"]) in top_cells,
        "prompt": r["text"], "prompt_words": len(r["text"].split()),
        "prompt_reading": r["pe"], "prompt_raw_goemotions_top": list(raw_top[r["id"]]),
        "image_reading": r["ie"], "face_classified": r["face"],
        "vqa": r["vqa"], "description": r["description"], "image_path": r["image_path"],
        "tags": tg,
        "primary_mode": m[0] if m else None,
        "primary_mode_label": MODES[m[0]] if m else None,
        "note": m[1] if m else None,
    })

tag_counts = {t: sum(s["tags"][t] for s in out_sample) for t in TAG_NAMES}
print("\n=== auto-tag counts over the sample ===")
for t, n in tag_counts.items(): print(f"  {t:28s} {n:3d} / {len(out_sample)}")

# ---------- failure-mode tally (human assignments) ----------
tally = {m: sum(1 for s in out_sample if s["primary_mode"] == m) for m in MODES}
unassigned = [s["id"] for s in out_sample if s["primary_mode"] is None]
exemplars = {m: [s["id"] for s in out_sample if s["primary_mode"] == m][:3] for m in MODES}
tally_by_cell = defaultdict(Counter)
for s in out_sample:
    if s["primary_mode"]: tally_by_cell[s["cell"]][s["primary_mode"]] += 1
# cross-tab: which auto-tags co-occur with which human mode (helps say whether the cheap tags predict the mode)
tag_by_mode = {m: {t: sum(1 for s in out_sample if s["primary_mode"] == m and s["tags"][t]) for t in TAG_NAMES} for m in MODES}
# where in the pipeline the disagreement arises: describer (a,b) / reader (c) / prompt side (d,f) / generator (e)
stage = {"describer (a+b)": tally["a"] + tally["b"], "image reader (c)": tally["c"],
         "prompt side (d+f)": tally["d"] + tally["f"], "generator (e)": tally["e"]}

print("\n=== primary failure mode (one per record, assigned from the drawing) ===")
for m, lab in MODES.items(): print(f"  ({m}) {lab:66s} {tally[m]:3d}   exemplars {exemplars[m]}")
if unassigned: print(f"  UNASSIGNED: {len(unassigned)} records {unassigned}")
print(f"  by pipeline stage: {stage}")

# ---------- observations for the Discussion chapter (every number computed above) ----------
n = len(out_sample)
pz_a = tag_by_mode["a"]["people_zero"]; pz_rest = tag_counts["people_zero"] - pz_a
neutral_cell = tally_by_cell.get("joy->neutral", Counter())
mixed_d = tag_by_mode["d"]["mixed_feeling_connective"]
# describer answer-vocabulary check over the whole analysed set: identical five-answer dicts across records
_byv = defaultdict(list)
for r in recs: _byv[json.dumps(r["vqa"], sort_keys=True)].append(r["id"])
_shared = [ids for ids in _byv.values() if len(ids) > 1]
n_shared = sum(len(ids) for ids in _shared)
observations = [
    f"The describer, not the generator, is where most high-confidence disagreements arise: modes (a)+(b) cover "
    f"{stage['describer (a+b)']} of {n}; the drawing shows a feeling other than the prompt's in only {tally['e']} of {n} (mode e).",
    f"people_zero is a usable predictor of mode (a): {pz_a} of {tally['a']} records tagged (a) have a people-count of 0, "
    f"against {pz_rest} of {n - tally['a']} in every other mode. When BLIP-VQA reports no people yet names an expression, "
    f"the expression is being invented.",
    f"The joy->neutral cell is a single mechanism: {neutral_cell.get('c', 0)} of {cells[('joy', 'neutral')]} are mode (c), and "
    f"in every one the describer answered 'calm' or 'smile' and the reader returned neutral. Low-arousal positive states "
    f"(grateful, at peace, relaxed) have no family in the 7-way scheme, so 'calm' falls to neutral by construction; and the "
    f"reader returned neutral for the two 'happy heart' records although the description names a smile twice.",
    f"bare_expression_word fires on {tag_counts['bare_expression_word']} of {n}: in this population it adds no information, "
    f"because an image top-1 score >= {CONF} is only reached when the describer gives a one-word expression answer.",
    f"mixed_feeling_connective (but/although/though/yet) catches {mixed_d} of the {tally['d']} mode-(d) records; its "
    f"{tag_counts['mixed_feeling_connective']} hits fall in other modes. Visitors list feelings without connectives "
    f"('tired proud happy', 'hopeful, slightly anxious, resigned'), so a list detector (3+ feeling words separated by "
    f"commas or spaces) would serve better than a connective detector.",
    f"Across all {len(recs)} analysed records, {n_shared} share a byte-identical five-answer VQA dict with at least one other "
    f"record ({len(_shared)} groups); ids 93 and 216 in this census are one such pair with visibly different drawings. "
    f"The describer's answer vocabulary is coarse, and identical descriptions produce identical image readings.",
]
print("\n=== observations ===")
for o in observations: print("  - " + o)

# ---------- write JSON ----------
result = {
    "method": {
        "selection": f"emotional records (GoEmotions top-1 family != neutral) with prompt top-1 score >= {CONF} "
                     f"AND image top-1 score >= {CONF} AND differing top-1 families; pre-test ids 1-{PRETEST_MAX_ID} dropped",
        "sampling": ("census - the whole population is below the target sample size" if census else
                     f"stratified sample of {TARGET} across the {N_CELLS} largest cells, one record per prompt group (dedup_key)"),
        "target_sample": TARGET, "n_strata": N_CELLS, "seed": SEED,
        "auto_tags": {
            "people_zero": "BLIP-VQA people-count answer parses to 0 (n_people from analysis_final.py)",
            "bare_expression_word": "BLIP-VQA expression answer is a single token in EXPRESSION_WORDS or a family name",
            "mixed_feeling_connective": "prompt contains but / although / though / yet (mixed feeling)",
            "ambiguous_raw_label": "raw 28-label GoEmotions top label is curiosity, realization or confusion",
            "short_prompt": "prompt is <= 2 words",
        },
        "failure_modes": MODES,
        "assignment": "one primary mode per record, assigned by a human after opening image_path and comparing the "
                      "drawing with the prompt, the VQA answers, the description and the two readings; stored in "
                      "MANUAL_MODES inside error_taxonomy.py",
    },
    "population": {
        "n_emotional": len(emo), "n_high_confidence_disagreements": len(pop),
        "n_distinct_prompts": len({r["dedup_key"] for r in pop}),
        "cells": {f"{p}->{i}": n for (p, i), n in cells.most_common()},
        "strata": [f"{p}->{i}" for p, i in top_cells],
        "n_in_strata": sum(cells[c] for c in top_cells),
    },
    "sample_size": len(out_sample),
    "tag_counts": tag_counts,
    "failure_mode_tally": tally,
    "failure_mode_exemplars": exemplars,
    "failure_mode_by_cell": {c: dict(v) for c, v in tally_by_cell.items()},
    "tags_by_mode": tag_by_mode,
    "by_pipeline_stage": stage,
    "unassigned_ids": unassigned,
    "observations": observations,
    "sample": out_sample,
}
json.dump(result, open(os.path.join(OUT, "error_taxonomy.json"), "w"), indent=1, ensure_ascii=False)
print(f"\nsaved outputs/error_taxonomy.json ({len(out_sample)} records)")

# ---------- write short markdown ----------
def _row(s): return f"| {s['id']} | {s['cell']} | {s['primary_mode'] or '-'} | {s['prompt'][:70].replace('|', '/')} |"
md = []
md.append("# Error taxonomy of high-confidence disagreements\n")
md.append(f"Generated by `error_taxonomy.py`. Population: emotional records (n={len(emo)}) where the prompt reader "
          f"and the image reader both give a top-1 score >= {CONF} and their top-1 families differ: "
          f"**{len(pop)} records** ({len({r['dedup_key'] for r in pop})} distinct prompts). "
          + ("This is below the target sample of 40, so every record was examined (census). " if census else "")
          + f"The {N_CELLS} largest confusion cells hold {sum(cells[c] for c in top_cells)} of them.\n")
md.append("## Confusion cells (prompt family -> image family)\n")
md.append("| cell | n | stratum |\n|---|---|---|")
for (p, i), n in cells.most_common(): md.append(f"| {p} -> {i} | {n} | {'yes' if (p, i) in top_cells else ''} |")
md.append("\n## Auto-tags\n")
md.append("| tag | n |\n|---|---|")
for t, n in tag_counts.items(): md.append(f"| {t} | {n} |")
md.append("\n## Primary failure mode (one per record, assigned from the drawing)\n")
md.append("| mode | description | n | exemplar ids |\n|---|---|---|---|")
for m, lab in MODES.items(): md.append(f"| ({m}) | {lab} | {tally[m]} | {', '.join(map(str, exemplars[m])) or '-'} |")
if unassigned: md.append(f"\n**{len(unassigned)} records not yet assigned:** {unassigned}\n")
md.append(f"\nBy pipeline stage: " + "; ".join(f"{k} = {v}" for k, v in stage.items()) + ".\n")
md.append("\n## Reading of the tally\n")
for o in observations: md.append(f"- {o}")
md.append("\nTie-break rule for records with more than one fault: a failure visible in the drawing itself is primary; "
          "(d) is used when the prompt lists several feelings or names none cleanly; (c) when the description is true to "
          "the drawing and the label is lost between description and family; (f) when a clear single-feeling prompt lands "
          "in the wrong family. Secondary faults are in the per-record `note` field of the JSON.\n")
md.append("\n## Mode by confusion cell\n")
md.append("| cell | " + " | ".join(f"({m})" for m in MODES) + " |\n|---|" + "---|" * len(MODES))
for c in [f"{p}->{i}" for (p, i), _ in cells.most_common()]:
    md.append(f"| {c} | " + " | ".join(str(tally_by_cell[c].get(m, 0)) for m in MODES) + " |")
md.append("\n## Auto-tag hits within each mode\n")
md.append("| mode | " + " | ".join(TAG_NAMES) + " |\n|---|" + "---|" * len(TAG_NAMES))
for m in MODES: md.append(f"| ({m}) n={tally[m]} | " + " | ".join(str(tag_by_mode[m][t]) for t in TAG_NAMES) + " |")
md.append("\n## Every record\n")
md.append("| id | cell | mode | prompt |\n|---|---|---|---|")
for s in out_sample: md.append(_row(s))
md.append("\nPer-record notes, VQA answers, descriptions, both readings and image paths are in `outputs/error_taxonomy.json`.\n")
open(os.path.join(OUT, "ERROR_TAXONOMY.md"), "w", encoding="utf-8").write("\n".join(md))
print("saved outputs/ERROR_TAXONOMY.md")
