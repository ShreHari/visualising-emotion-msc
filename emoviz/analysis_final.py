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
Writes outputs/analysis_final.csv (per record) and outputs/analysis_final.json (every printed number:
observed, null mean, null sd, z, denominators, degenerate flags) — make_figures.py and test_numeric.py
read the JSON, so no number is ever typed by hand downstream. Degenerate nulls are detected from the
null's own spread and no z is printed for them.
"""
import json, os, math, random, statistics as st, re, csv
random.seed(7)
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")

# ---- every constant and metric comes from ONE place: emoviz/metrics.py (shared with significance.py,
#      app.py, test_numeric.py and the audit scripts, so the definitions cannot drift) ----
import sys; sys.path.insert(0, ROOT)
from emoviz.metrics import (PRETEST_MAX_ID, CEN, POS, NEG, G2F, EXPRESSION_WORDS, NUMWORDS,
                            sign, n_people, is_face, va_point, va_sim, soft, metrics, with_null, degenerate)

def zline(name, t, nm, ns):
    if nm is None: return f"  {name:24s} n<5, no null"
    deg = degenerate(ns)
    def cell(k, lab):
        if k in deg: return f"{lab} {t[k]:.0%}/{nm[k]:.0%}[z n/a]"
        return f"{lab} {t[k]:.0%}/{nm[k]:.0%}[z{(t[k]-nm[k])/ns[k]:+.1f}]"
    # observed/null for EVERY metric, with its z vs the random-pairing null; 'z n/a' = degenerate null
    line = f"  {name:24s} " + " ".join(cell(k, l) for k, l in (("va", "VA"), ("vsign", "sign"), ("family", "fam"), ("overlap", "ovlp")))
    if deg: line += f"  (degenerate null for {', '.join(sorted(deg))}: every prompt shares one label — no z reported)"
    return line

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

RESULTS = {"seed": 7, "null_shuffles": 300, "blocks": {}}
def sub_analysis(title, subset, store=None):
    pairs = [(r["pe"], r["ie"]) for r in subset]
    if not pairs: print(f"  {title}: (empty)"); return
    t, nm, ns = with_null(pairs)
    print(zline(f"{title} (n={len(pairs)})", t, nm, ns))
    if store is not None and nm is not None:
        deg = degenerate(ns)
        store[title] = {"n": len(pairs),
                        "n_sign": sum(1 for p, _ in pairs if sign(p[0][0]) != "0"),   # valence-sign denominator
                        "face": sum(r["face"] for r in subset),
                        "metrics": {k: {"obs": t[k], "null": nm[k], "sd": ns[k],
                                        "z": None if k in deg else (t[k]-nm[k])/ns[k],
                                        "degenerate": k in deg} for k in t}}

def block(recs_in, header, key):
    print(f"\n########## {header} — {len(recs_in)} records ##########")
    print(f"emotional: {sum(r['emotional'] for r in recs_in)}  non-emotional: {sum(not r['emotional'] for r in recs_in)}"
          f"  |  face: {sum(r['face'] for r in recs_in)}  scene: {sum(not r['face'] for r in recs_in)}")
    store = RESULTS["blocks"][key] = {"records": len(recs_in),
                                      "emotional": sum(r["emotional"] for r in recs_in),
                                      "non_emotional": sum(not r["emotional"] for r in recs_in),
                                      "face": sum(r["face"] for r in recs_in),
                                      "scene": sum(not r["face"] for r in recs_in), "subsets": {}}
    S = store["subsets"]
    emo = [r for r in recs_in if r["emotional"]]
    print("--- emotional prompts, and the face/scene split (each vs its own random-pairing null) ---")
    sub_analysis("ALL emotional", emo, S)
    sub_analysis("face images", [r for r in emo if r["face"]], S)
    sub_analysis("scene images", [r for r in emo if not r["face"]], S)
    print("--- positive vs negative (VA is the only non-degenerate metric here) ---")
    sub_analysis("positive prompts", [r for r in emo if sign(r["prompt_top"]) == "+"], S)
    sub_analysis("negative prompts", [r for r in emo if sign(r["prompt_top"]) == "-"], S)
    print("--- prompts the text reader labels neutral (specificity check: expect z~0) ---")
    sub_analysis("non-emotional", [r for r in recs_in if not r["emotional"]], S)

print(f"=== FINAL ANALYSIS — {len(recs)} records (pre-tests dropped) ===")
block(recs, "FULL SAMPLE", "full")

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
block(distinct, "DISTINCT PROMPTS ONLY (robustness)", "distinct")

# ---------- write CSV ----------
with open(os.path.join(OUT, "analysis_final.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "text", "prompt_emotion", "image_emotion", "emotional", "face"])
    for r in recs:
        w.writerow([r["id"], r["text"], r["prompt_top"], r["image_top"], int(r["emotional"]), int(r["face"])])
print(f"\nsaved outputs/analysis_final.csv ({len(recs)} rows)")
RESULTS["duplicates"] = {"records_repeating_an_earlier_prompt": n_dup, "distinct_prompts": len(distinct),
                         "happy_count": sum(1 for r in recs if r["text"].strip().lower() == "happy")}
RESULTS["families"] = {"prompt": {f: sum(1 for r in recs if r["prompt_top"] == f) for f in CEN},
                       "image": {f: sum(1 for r in recs if r["image_top"] == f) for f in CEN}}
with open(os.path.join(OUT, "analysis_final.json"), "w") as f:
    json.dump(RESULTS, f, indent=1)
print("saved outputs/analysis_final.json (every number above, machine-readable: figures and tests read this)")
