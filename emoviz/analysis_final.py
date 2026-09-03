#!/usr/bin/env python3
"""
emoviz/analysis_final.py — the consolidated, final analysis of the describe->extract results.

Applies the improvements agreed for the dissertation, each with a documented (not hard-coded) rule:
  * DROP pre-test records (ids 1-13) — developer test runs before the festival (per recovered timestamps).
  * PROMPT emotion via GoEmotions (28->7 Ekman families) — cleaner than NLI on short first-person text.
  * IMAGE emotion via the NLI-from-description labels already in describe_extract.jsonl.
  * SPLIT the data two ways Chen asked for:
      - emotional vs non-emotional PROMPTS   (rule: GoEmotions top-1 family != 'neutral')
      - face vs scene IMAGES                 (rule: BLIP-VQA reports >=1 person AND a readable expression)
  * Every metric reported against a random-pairing NULL baseline (so "similar" = more similar to its OWN
    prompt than to a random one), with a z-score.

Caches GoEmotions prompt emotions to outputs/prompt_emotions_goe.json so re-runs are instant.
Writes outputs/analysis_final.csv (RESULTS_final.md is the hand-written findings doc).
"""
import json, os, math, random, statistics as st, re, csv
random.seed(7)
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")

# ---- documented constants (rationale in the docstring; not per-record hard-coding) ----
PRETEST_MAX_ID = 13                       # ids 1-13 = pre-festival developer tests (timestamps 26 Aug-18 Sep)
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
def zline(name, t, nm, ns):
    if nm is None: return f"  {name:24s} n<5, no null"
    def z(k): return (t[k]-nm[k])/ns[k]
    # show BOTH the value and its z vs the random-pairing null, for EVERY metric (not just VA)
    return (f"  {name:24s} "
            f"VA {t['va']:.0%}[z{z('va'):+.1f}] "
            f"sign {t['vsign']:.0%}[z{z('vsign'):+.1f}] "
            f"fam {t['family']:.0%}[z{z('family'):+.1f}] "
            f"ovlp {t['overlap']:.0%}[z{z('overlap'):+.1f}]")

# ---------- load describe->extract, drop pre-test ----------
rows = [json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8")]
rows = [r for r in rows if r["id"] > PRETEST_MAX_ID]

# ---------- GoEmotions prompt emotions (cached) ----------
cache = os.path.join(OUT, "prompt_emotions_goe.json")
if os.path.exists(cache):
    goe = {int(k): v for k, v in json.load(open(cache)).items()}
    missing = [r["id"] for r in rows if r["id"] not in goe]
    if missing:
        raise SystemExit(f"prompt-emotion cache is stale ({len(missing)} ids missing, e.g. {missing[:5]}). "
                         f"Delete {cache} and re-run.")
else:
    import torch
    from transformers import pipeline
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    print("[GoEmotions on prompts (one-time, caching) ...]")
    clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None, truncation=True, device=dev, batch_size=32)
    preds = clf([r["text"] for r in rows])
    def fam_top3(pred):
        f = {}
        for d in pred:
            fam = G2F.get(d["label"], "neutral"); f[fam] = f.get(fam, 0) + d["score"]
        tot = sum(f.values()) or 1.0            # normalise to a distribution (audit fix;
        f = {k: v / tot for k, v in f.items()}  #  ordering unchanged, results identical)
        return [[l, round(float(s), 4)] for l, s in sorted(f.items(), key=lambda x: -x[1])[:3]]
    goe = {r["id"]: fam_top3(p) for r, p in zip(rows, preds)}
    json.dump({str(k): v for k, v in goe.items()}, open(cache, "w"))
    print(f"[cached {len(goe)} prompt emotions]")

# ---------- assemble records with classifications ----------
recs = []
for r in rows:
    pe = goe[r["id"]]; ie = r["image_emotions"]
    recs.append({"id": r["id"], "text": r["text"], "dedup_key": r.get("dedup_key"), "pe": pe, "ie": ie,
                 "prompt_top": pe[0][0], "image_top": ie[0][0],
                 "emotional": pe[0][0] != "neutral",
                 "face": is_face(r.get("vqa", {})), "vqa": r.get("vqa", {})})

def sub_analysis(title, subset, degenerate=False):
    pairs = [(r["pe"], r["ie"]) for r in subset]
    if not pairs: print(f"  {title}: (empty)"); return
    t, nm, ns = with_null(pairs)
    tag = "  (single-sign subset: sign/fam nulls DEGENERATE, ignore their z)" if degenerate else ""
    print(zline(f"{title} (n={len(pairs)})", t, nm, ns) + tag)

def block(recs_in, header):
    print(f"\n########## {header} — {len(recs_in)} records ##########")
    print(f"emotional: {sum(r['emotional'] for r in recs_in)}  non-emotional: {sum(not r['emotional'] for r in recs_in)}"
          f"  |  face: {sum(r['face'] for r in recs_in)}  scene: {sum(not r['face'] for r in recs_in)}")
    emo = [r for r in recs_in if r["emotional"]]
    print("--- emotional prompts, and the face/scene split (each vs its own random-pairing null) ---")
    sub_analysis("ALL emotional", emo)
    sub_analysis("face images", [r for r in emo if r["face"]])
    sub_analysis("scene images", [r for r in emo if not r["face"]])
    print("--- positive vs negative (VA is the only non-degenerate metric here) ---")
    sub_analysis("positive prompts", [r for r in emo if sign(r["prompt_top"]) == "+"], degenerate=True)
    sub_analysis("negative prompts", [r for r in emo if sign(r["prompt_top"]) == "-"], degenerate=True)
    print("--- non-emotional prompts (validity check: expect z~0, no feeling to convey) ---")
    sub_analysis("non-emotional", [r for r in recs_in if not r["emotional"]])

print(f"=== FINAL ANALYSIS — {len(recs)} records (pre-tests dropped) ===")
block(recs, "FULL SAMPLE")

# ---- ROBUSTNESS: duplicate prompts (~25% are repeats -> pseudo-replication). Re-run on distinct texts. ----
# group on dedup_key (identity from the ORIGINAL text) so redaction cannot merge two different
# prompts into one; fall back to text for any record predating the key.
seen = set(); distinct = []
for r in recs:
    k = r.get("dedup_key", r["text"].strip().lower())
    if k not in seen:
        seen.add(k); distinct.append(r)
n_dup = len(recs) - len(distinct)
print(f"\n[duplicate-prompt check: {n_dup} of {len(recs)} records repeat an earlier prompt "
      f"(e.g. 'happy' x{sum(1 for r in recs if r['text'].strip().lower()=='happy')}); "
      f"re-running on {len(distinct)} DISTINCT prompts]")
block(distinct, "DISTINCT PROMPTS ONLY (robustness)")

# ---------- write CSV ----------
with open(os.path.join(OUT, "analysis_final.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "text", "prompt_emotion", "image_emotion", "emotional", "face"])
    for r in recs:
        w.writerow([r["id"], r["text"], r["prompt_top"], r["image_top"], int(r["emotional"]), int(r["face"])])
print(f"\nsaved outputs/analysis_final.csv ({len(recs)} rows)")
