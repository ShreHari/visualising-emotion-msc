#!/usr/bin/env python3
"""
emoviz/ablate_nli.py — description-template ABLATION for the image reader.

Question: how much of the AGREEMENT between the prompt reader and the image reader reported in
analysis_final.py depends on each clause of the description that the BLIP-VQA answers are composed into?
In particular, how much of the face-vs-scene gap rests on the single facial-expression word?

Method (nothing upstream is re-run):
  * each record's five cached BLIP-VQA answers (outputs/describe_extract.jsonl, field "vqa") are
    re-composed into a description under an ablated template;
  * ONLY the zero-shot NLI step is re-run on that description
    (facebook/bart-large-mnli, hypothesis template exactly TEMPLATE below, the seven families as labels,
    top-3 kept, fp16 on mps) -> new image_emotions;
  * prompt_emotions are copied unchanged from the cached file; the analysis reads prompt emotions from
    the GoEmotions cache (outputs/prompt_emotions_goe.json), exactly as analysis_final.py does.

Baseline template (describe_extract.py, verbatim):
  "A drawing of {people} showing {scene}. The person is {action}, {posture}. The facial expression is {expression}."
Variants:
  drop_expression        omit the final sentence
  drop_action            "The person is {posture}."
  drop_posture           "The person is {action}."
  drop_people            "A drawing showing {scene}."
  drop_scene             "A drawing of {people}."
  fixed_expression       keep the sentence, but expression := "unclear" for EVERY record
  people_aware           records where the describer reports no person: "A drawing showing {scene}."
                         (no person, no action, no expression asserted); all other records unchanged
  people_aware_no_expression   as above but keeping action/posture: "A drawing showing {scene}. The scene
                         involves {action}, {posture}."; all other records unchanged
  control_full_template  (extra control, run last) the unmodified template re-run under the same fp16
                         conditions, so numerical noise can be separated from template effects.

Outputs (all under outputs/ablation/):
  <variant>.jsonl  one record per line, same schema as describe_extract.jsonl (id, text, dedup_key,
                   image_path, vqa, description, prompt_emotions, image_emotions, prompt_top1, image_top1);
                   appended incrementally, already-done ids are skipped on restart (crash-safe, resumable).
  summary.json     {variant: {subset: {metric: {obs, null, z, n}}}} for the emotional subset (n=607) and its
                   face/scene halves (plus positive/negative/non_emotional, and *_distinct robustness rows on
                   first-occurrence-per-dedup_key records, i.e. clustered on prompt identity exactly as
                   analysis_final.py does), each against a 300-shuffle random-pairing null, seed 7.
                   A "baseline" row is computed from the unmodified describe_extract.jsonl by the SAME code
                   and is checked against the published values BEFORE any model is loaded.
                   The key "_meta" is metadata (run settings, reference checks, top-1 distributions), not a variant.

The similarity code (CEN, POS/NEG, sign, va_point, va_sim, soft, metrics, with_null, is_face, n_people and
the word lists) is COPIED VERBATIM from analysis_final.py, which executes its whole analysis on import and
therefore cannot be imported. The ORDER of with_null calls also mirrors analysis_final.py (FULL block, then
DISTINCT block; emotional, face, scene, positive, negative, non-emotional) so that the seed-7 random stream
is identical and the baseline reproduces its numbers to the digit.

Run:  .venv/bin/python ablate_nli.py                                 # full, resumable (~7-15 min per variant)
      .venv/bin/python ablate_nli.py --analysis-only                 # recompute summary.json from existing files
      .venv/bin/python ablate_nli.py --limit 20 --out-dir /tmp/abl   # smoke test into a scratch directory
"""
from __future__ import annotations
import argparse, json, math, os, random, re, statistics as st, sys, time
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
SRC = os.path.join(OUT, "describe_extract.jsonl")
GOE = os.path.join(OUT, "prompt_emotions_goe.json")
ABL_DEFAULT = os.path.join(OUT, "ablation")

NLI_ID = "facebook/bart-large-mnli"
LABELS = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]   # describe_extract.py order
TEMPLATE = "This scene conveys {}."          # hypothesis template fixed by describe_extract.py (verbatim)
VARIANTS = ["drop_expression", "drop_action", "drop_posture", "drop_people", "drop_scene", "fixed_expression",
            "people_aware", "people_aware_no_expression"]
CONTROL = "control_full_template"
N_SHUFFLES, SEED = 300, 7

# ---- data facts from analysis_final.py — asserted on every file, never re-derived ----
EXPECT = dict(records=1012, emotional=607, non_emotional=405, face=591, scene=421,
              emo_face=402, emo_scene=205, duplicates=249, distinct=763)
# ---- published values the baseline row must reproduce (analysis_final.py, seed 7, 300 shuffles) ----
REFERENCE = [  # (subset, metric, obs, null, z-or-None), all as printed to 1 decimal in percent
    ("emotional", "vsign", 64.0, 45.6, 11.1), ("emotional", "family", 53.1, 38.8, 10.3),
    ("face", "vsign", 73.9, 53.5, None), ("scene", "vsign", 42.9, 29.6, None),
    ("non_emotional", "va", 76.6, 76.6, None)]

# =====================================================================================================
# COPIED VERBATIM from analysis_final.py (lines 23-81). analysis_final.py runs its whole analysis on
# import, so it cannot be imported; only the is_face comment is reworded.
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
    # token intersection so multi-word answers ("man is smiling") count (audit fix)
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


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------------------------------------------------------------- description templates ----------
def build_description(a: dict, variant: str) -> str:
    """Re-compose the cached BLIP-VQA answers `a` under the ablated template.
    Defaults are those of describe_extract.py; any variant name not handled (e.g. CONTROL) yields the
    unmodified baseline template."""
    people, scene = a.get("people", "a"), a.get("scene", "a scene")
    action, posture = a.get("action", "present"), a.get("posture", "")
    # people-aware variants: where the describer reports NO person, do not assert one. This is the
    # sensitivity check for the template defect (the baseline names a person and an expression for
    # all 414 no-people drawings). Records with >=1 person keep the full baseline template.
    if variant in ("people_aware", "people_aware_no_expression") and n_people(people) == 0:
        if variant == "people_aware":
            return f"A drawing showing {scene}."
        return f"A drawing showing {scene}. The scene involves {action}, {posture}."
    expression = "unclear" if variant == "fixed_expression" else a.get("expression", "unclear")
    s1 = {"drop_people": f"A drawing showing {scene}.",
          "drop_scene": f"A drawing of {people}."}.get(variant, f"A drawing of {people} showing {scene}.")
    s2 = {"drop_action": f"The person is {posture}.",
          "drop_posture": f"The person is {action}."}.get(variant, f"The person is {action}, {posture}.")
    s3 = "" if variant == "drop_expression" else f" The facial expression is {expression}."
    return f"{s1} {s2}{s3}"


# ---------------------------------------------------------------- NLI re-run ----------------------
def load_nli():
    import torch
    from transformers import pipeline
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float16 if dev != "cpu" else torch.float32
    log(f"device={dev} dtype={dtype}; loading NLI ({NLI_ID}) ...")
    zs = pipeline("zero-shot-classification", model=NLI_ID, device=dev, dtype=dtype)
    log("model ready")
    return zs, dev, str(dtype)


def top3(z):   # same rounding/shape as describe_extract.nli_top3
    return [[l, round(float(s), 4)] for l, s in list(zip(z["labels"], z["scores"]))[:3]]


def done_ids(path):   # copied from describe_extract.py
    ids = set()
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            try:
                ids.add(json.loads(line)["id"])
            except Exception:
                pass
    return ids


def run_variant(zs, rows, variant, abl_dir, batch_size):
    path = os.path.join(abl_dir, f"{variant}.jsonl")
    already = done_ids(path)
    todo = [r for r in rows if r["id"] not in already]
    log(f"[{variant}] {len(rows)} records in scope; {len(already)} done; {len(todo)} to process -> {path}")
    if not todo:
        return path, 0.0
    t0 = time.time(); n = 0
    with open(path, "a", encoding="utf-8") as fh:
        for b, i in enumerate(range(0, len(todo), batch_size)):
            chunk = todo[i:i + batch_size]
            descs = [build_description(r["vqa"], variant) for r in chunk]
            outs = zs(descs, LABELS, hypothesis_template=TEMPLATE, batch_size=batch_size)
            if isinstance(outs, dict):
                outs = [outs]
            for r, d, z in zip(chunk, descs, outs):
                ie = top3(z)
                rec = {"id": r["id"], "text": r["text"], "dedup_key": r.get("dedup_key"),
                       "image_path": r["image_path"], "vqa": r["vqa"], "description": d,
                       "prompt_emotions": r["prompt_emotions"], "image_emotions": ie,
                       "prompt_top1": r["prompt_top1"], "image_top1": ie[0][0]}
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush(); n += len(chunk)          # one flushed batch = the resumable unit
            if b % 4 == 0 or n == len(todo):
                rate = (time.time() - t0) / n
                log(f"  [{variant}] {n}/{len(todo)}  {rate:.2f}s/rec  ETA {rate*(len(todo)-n)/60:.1f}m")
    dt = time.time() - t0
    log(f"[{variant}] done: {n} records in {dt/60:.1f} min")
    return path, dt


# ---------------------------------------------------------------- analysis -----------------------
def load_rows(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")]


def assemble(rows, goe, name):
    """Records with classifications, exactly as analysis_final.py builds them (pre-tests dropped,
    prompt emotions from the GoEmotions cache, image emotions from the file's NLI labels)."""
    rows = [r for r in rows if r["id"] > PRETEST_MAX_ID]
    missing = [r["id"] for r in rows if r["id"] not in goe]
    if missing:
        raise SystemExit(f"[{name}] prompt-emotion cache lacks {len(missing)} ids, e.g. {missing[:5]}")
    recs = []
    for r in rows:
        pe = goe[r["id"]]; ie = r["image_emotions"]
        recs.append({"id": r["id"], "text": r["text"], "dedup_key": r.get("dedup_key"), "pe": pe, "ie": ie,
                     "prompt_top": pe[0][0], "image_top": ie[0][0],
                     "emotional": pe[0][0] != "neutral", "face": is_face(r.get("vqa", {}))})
    return recs


def distinct_recs(recs):
    # copied from analysis_final.py: first occurrence per dedup_key (prompt identity), text as fallback
    seen = set(); distinct = []
    for r in recs:
        k = r.get("dedup_key", r["text"].strip().lower())
        if k not in seen:
            seen.add(k); distinct.append(r)
    return distinct


def check_counts(recs, name):
    emo = [r for r in recs if r["emotional"]]
    got = dict(records=len(recs), emotional=len(emo), non_emotional=len(recs) - len(emo),
               face=sum(r["face"] for r in recs), scene=sum(not r["face"] for r in recs),
               emo_face=sum(r["face"] for r in emo), emo_scene=sum(not r["face"] for r in emo))
    got["distinct"] = len(distinct_recs(recs)); got["duplicates"] = len(recs) - got["distinct"]
    bad = {k: (got[k], EXPECT[k]) for k in EXPECT if got[k] != EXPECT[k]}
    if bad:
        raise SystemExit(f"[{name}] data facts differ from analysis_final.py (got, expected): {bad}")
    return got


def analyse(recs):
    """Same subsets and the same ORDER of with_null calls as analysis_final.py (FULL block, then the
    DISTINCT-prompt block), so the seed-7 random stream is identical to the published run."""
    random.seed(SEED)
    out = {}

    def sub(name, subset):
        pairs = [(r["pe"], r["ie"]) for r in subset]
        if not pairs:
            return
        t, nm, ns = with_null(pairs, N_SHUFFLES)
        n_signed = sum(1 for p, _ in pairs if sign(p[0][0]) != "0")
        out[name] = {}
        for k in t:
            row = {"obs": t[k], "null": None if nm is None else nm[k],
                   "z": None if nm is None else (t[k] - nm[k]) / ns[k], "n": len(pairs)}
            if k == "vsign":
                row["n_signed"] = n_signed   # vsign's denominator: prompts whose top-1 family has a sign
            out[name][k] = row

    def block(recs_in, suffix):
        emo = [r for r in recs_in if r["emotional"]]
        sub("emotional" + suffix, emo)
        sub("face" + suffix, [r for r in emo if r["face"]])
        sub("scene" + suffix, [r for r in emo if not r["face"]])
        sub("positive" + suffix, [r for r in emo if sign(r["prompt_top"]) == "+"])
        sub("negative" + suffix, [r for r in emo if sign(r["prompt_top"]) == "-"])
        sub("non_emotional" + suffix, [r for r in recs_in if not r["emotional"]])

    block(recs, "")
    block(distinct_recs(recs), "_distinct")
    return out


TOL = 0.055   # published figures carry 1 decimal (half-unit 0.05); 0.055 also admits a figure rounded twice
              # (emotional family agreement is exactly 322/607 = 53.048%, published as 53.1 via 53.05)

def verify_baseline(row):
    """The baseline row must reproduce the published values at their published precision."""
    checks, ok = [], True
    for subset, metric, obs, null, z in REFERENCE:
        c = row[subset][metric]
        for what, got, exp in (("obs", c["obs"] * 100, obs), ("null", c["null"] * 100, null),
                               ("z", c["z"], z)):
            if exp is None:
                continue
            good = abs(got - exp) <= TOL          # within the published precision
            exact = round(got, 1) == exp           # rounds to the published figure
            ok &= good
            checks.append({"subset": subset, "metric": metric, "field": what, "got": round(got, 4),
                           "published": exp, "pass": good, "rounds_to_published": exact})
            flag = "PASS" if exact else ("PASS*" if good else "FAIL")
            print(f"  {flag:5s} baseline {subset:14s}{metric:7s}{what:5s} got {got:8.3f}   published {exp}"
                  + ("" if exact else f"   (* exact value rounds to {round(got, 1)}; within {TOL} of published)"))
    return ok, checks


def meta_for(recs, base_top):
    dist = Counter(r["image_top"] for r in recs)
    return {"n": len(recs),
            "image_top1_distribution": {l: dist.get(l, 0) for l in LABELS},
            "image_top1_changed_vs_baseline": sum(1 for r in recs if base_top[r["id"]] != r["image_top"])}


def print_table(summary, suffix, title):
    print(f"\n=== {title} ===")
    print(f"{'variant':22s} {'subset':10s} {'n':>4s} | {'valence-sign agreement':>24s} | {'family agreement':>24s}")
    print(f"{'':22s} {'':10s} {'':>4s} | {'obs':>7s} {'null':>7s} {'z':>7s} | {'obs':>7s} {'null':>7s} {'z':>7s}")
    for variant, rows in summary.items():
        if variant.startswith("_"):
            continue
        for subset in ("emotional", "face", "scene"):
            c = rows.get(subset + suffix)
            if not c:
                continue
            v, f = c["vsign"], c["family"]
            print(f"{variant:22s} {subset:10s} {v['n']:4d} | {v['obs']:6.1%} {v['null']:6.1%} {v['z']:+7.1f} "
                  f"| {f['obs']:6.1%} {f['null']:6.1%} {f['z']:+7.1f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variants", nargs="*", default=VARIANTS + [CONTROL],
                    help=f"subset of {VARIANTS + [CONTROL]} (default: all six, then the control)")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None, help="process only the first N records (smoke test)")
    ap.add_argument("--out-dir", default=ABL_DEFAULT, help="where the variant files and summary.json go")
    ap.add_argument("--analysis-only", action="store_true", help="skip the NLI re-run; summarise existing files")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    # ---- source data ----
    rows = load_rows(SRC)
    goe = {int(k): v for k, v in json.load(open(GOE)).items()}
    mism = [r["id"] for r in rows if build_description(r["vqa"], CONTROL) != r["description"]]
    if mism:
        raise SystemExit(f"template rebuild differs from the cached description for {len(mism)} ids, e.g. {mism[:5]}")
    log(f"{len(rows)} cached records; the baseline template rebuilds every cached description exactly")

    # ---- baseline row by the SAME code, checked against the published values before any model loads ----
    log("baseline (unmodified describe_extract.jsonl) ...")
    base = assemble(rows, goe, "baseline")
    counts = check_counts(base, "baseline")
    log(f"counts reproduce analysis_final.py: {counts}")
    summary = {"_meta": {}, "baseline": analyse(base)}
    ok, checks = verify_baseline(summary["baseline"])
    if not ok:
        raise SystemExit("baseline does NOT reproduce the published values — fix the analysis code first")
    log("baseline reproduces every published reference value")
    base_top = {r["id"]: r["image_top"] for r in base}
    meta = {"nli_model": NLI_ID, "hypothesis_template": TEMPLATE, "labels": LABELS, "top_k": 3,
            "prompt_emotions_for_analysis": os.path.relpath(GOE, ROOT), "source": os.path.relpath(SRC, ROOT),
            "seed": SEED, "n_shuffles": N_SHUFFLES, "counts": counts,
            "subsets": "emotional = GoEmotions top-1 family != neutral; face = BLIP-VQA people >= 1 and an "
                       "EXPRESSION_WORDS token; *_distinct = first record per dedup_key (prompt identity)",
            "reference_checks": checks, "variants": {}, "per_variant": {"baseline": meta_for(base, base_top)}}
    summary["_meta"] = meta

    # ---- NLI re-run per variant (resumable) ----
    if not a.analysis_only:
        scope = rows[:a.limit] if a.limit else rows
        zs, dev, dtype = load_nli()
        meta.update({"device": dev, "dtype": dtype, "batch_size": a.batch_size})
        for v in a.variants:
            path, dt = run_variant(zs, scope, v, a.out_dir, a.batch_size)
            meta["variants"][v] = {"file": os.path.relpath(path, ROOT), "seconds_this_run": round(dt, 1),
                                   "example_description": build_description(rows[0]["vqa"], v)}
    if a.limit:
        log("--limit given: variant files are partial, so no variant summary is computed"); return

    # ---- summarise every complete variant file ----
    for v in a.variants:
        path = os.path.join(a.out_dir, f"{v}.jsonl")
        if not os.path.exists(path):
            log(f"[{v}] no file, skipped"); continue
        recs = assemble(load_rows(path), goe, v)
        check_counts(recs, v)
        summary[v] = analyse(recs)
        meta["per_variant"][v] = meta_for(recs, base_top)
        meta["variants"].setdefault(v, {})["example_description"] = build_description(rows[0]["vqa"], v)
        log(f"[{v}] summarised; image top-1 changed vs baseline on "
            f"{meta['per_variant'][v]['image_top1_changed_vs_baseline']}/{len(recs)} records")

    out_path = os.path.join(a.out_dir, "summary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    print_table(summary, "", "emotional prompts (n=607) and the face/scene split, vs 300-shuffle null")
    print_table(summary, "_distinct", "robustness: first record per dedup_key only (n=452)")
    print("\n=== image top-1 distribution (analysed 1,012 records) ===")
    print(f"{'variant':22s} " + " ".join(f"{l:>8s}" for l in LABELS) + f" {'changed':>8s}")
    for v, m in meta["per_variant"].items():
        d = m["image_top1_distribution"]
        print(f"{v:22s} " + " ".join(f"{d[l]:8d}" for l in LABELS) + f" {m['image_top1_changed_vs_baseline']:8d}")
    log(f"saved {out_path}")


if __name__ == "__main__":
    main()
