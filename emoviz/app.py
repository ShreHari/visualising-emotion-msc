#!/usr/bin/env python3
"""
emoviz/app.py — EmoViz demo app: the describe→extract→similarity pipeline as a hostable web app.

Product-grade behaviours (beyond the earlier tester):
  * /api/status + /api/warmup — the UI shows model state honestly and pre-loads in the background.
  * A global inference LOCK — concurrent visitors queue instead of loading models twice / thrashing RAM.
  * NAME REDACTION — every prompt is loaded through emoviz.data, which applies the reviewed
    redaction in preprocess_names.py, so no private individual's name can reach any surface.
    Illness and grief content is kept, per supervisor direction.
  * Featured examples — computed from the analysis CSV at startup (one clear example per emotion
    family), never hard-coded ids.
  * Upload guard (size/type), env-configurable HOST/PORT for LAN hosting, threaded server.
  * Stores nothing: no logs of text, no uploaded images kept.

Run:   .venv/bin/python app.py                     → http://127.0.0.1:5050
Host on your network:  HOST=0.0.0.0 .venv/bin/python app.py   (share http://<your-ip>:5050)

Science parity: the pipeline pieces (questions, description template, NLI hypothesis, GoEmotions
family mapping, similarity ladder) are IDENTICAL to describe_extract.py / analysis_final.py.
"""
from __future__ import annotations
import base64, csv, io, json, math, os, threading

from flask import Flask, jsonify, render_template, request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "outputs")

app = Flask(__name__, template_folder=os.path.join(ROOT, "web"), static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024   # 8 MB upload cap
# Jinja caches templates in memory when debug is off, so edits to web/index.html would silently not
# appear until a restart — a trap when iterating on the interface. Cost is one stat() per request.
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ---------------------------------------------------------------- science config (parity with analysis)
# every constant and measure comes from emoviz/metrics.py — the same module analysis_final.py,
# significance.py and test_numeric.py import — so the demo cannot drift from the analysis
import sys; sys.path.insert(0, ROOT)
from emoviz.metrics import (FAMILIES as LABELS, CEN, POS, NEG, G2F, sign, va_point, va_sim, soft)
QUESTIONS = [("expression", "What is the facial expression?"), ("action", "What is the person doing?"),
             ("posture", "What is the body posture?"), ("people", "How many people are there?"),
             ("scene", "What is in the picture?")]

# Nothing is withheld any more. Names are redacted at load time by preprocess_names.py, and the
# supervisor directed that illness and grief content is KEPT — it is not identifying on its own
# and it is essential to the analysis. Redacting rather than withholding is also the stronger
# privacy position: with no hidden set, there is nothing for id-probing to recover, which is why
# the decoy records this app used to serve are gone too.
# Escape hatch: put ids here to withhold them again; the 404 text stays deliberately uninformative.
WITHHELD_IDS: set[int] = set()

# ---------------------------------------------------------------- models: lazy, fp16, lock-guarded
_M: dict = {}
_LOCK = threading.Lock()          # one inference at a time — protects a small-RAM host
_WARMING = {"active": False}

def _device():
    import torch
    if "dev" not in _M:
        _M["torch"] = torch
        _M["dev"] = ("mps" if torch.backends.mps.is_available()
                     else "cuda" if torch.cuda.is_available() else "cpu")
    return _M["dev"]

def vqa_model():
    if "vqa" not in _M:
        from transformers import BlipProcessor, BlipForQuestionAnswering
        dev = _device()
        app.logger.info("loading BLIP-VQA (fp16) ...")
        _M["vqa_proc"] = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        _M["vqa"] = BlipForQuestionAnswering.from_pretrained(
            "Salesforce/blip-vqa-base", dtype=_M["torch"].float16).to(dev).eval()
    return _M["vqa_proc"], _M["vqa"]

def nli_model():
    if "nli" not in _M:
        from transformers import pipeline
        app.logger.info("loading NLI (fp16) ...")
        _M["nli"] = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",
                             device=_device(), dtype=_M["torch"].float16)
    return _M["nli"]

def goe_model():
    if "goe" not in _M:
        from transformers import pipeline
        app.logger.info("loading GoEmotions (fp16) ...")
        _M["goe"] = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions",
                             top_k=None, truncation=True, device=_device(),
                             dtype=_M["torch"].float16)
    return _M["goe"]

_GOE_CACHE = None
def goe_cache():
    global _GOE_CACHE
    if _GOE_CACHE is None:
        p = os.path.join(OUT, "prompt_emotions_goe.json")
        _GOE_CACHE = {int(k): v for k, v in json.load(open(p)).items()} if os.path.exists(p) else {}
    return _GOE_CACHE

def _warm():
    try:
        with _LOCK:
            vqa_model(); nli_model()
    finally:
        _WARMING["active"] = False

# ---------------------------------------------------------------- pipeline (identical semantics)
def describe_image(pil_img):
    proc, vqa = vqa_model()
    dev = _device()
    ans = {}
    for key, q in QUESTIONS:
        inp = proc(pil_img, q, return_tensors="pt").to(dev, _M["torch"].float16)
        with _M["torch"].no_grad():
            o = vqa.generate(**inp, max_new_tokens=15)
        ans[key] = proc.decode(o[0], skip_special_tokens=True).strip()
    desc = (f"A drawing of {ans.get('people','a')} showing {ans.get('scene','a scene')}. "
            f"The person is {ans.get('action','present')}, {ans.get('posture','')}. "
            f"The facial expression is {ans.get('expression','unclear')}.")
    return desc, ans

def emotion_from_description(desc):
    z = nli_model()(desc, LABELS, hypothesis_template="This scene conveys {}.")
    return [[l, round(float(s), 4)] for l, s in list(zip(z["labels"], z["scores"]))[:3]]

def emotion_from_prompt(text, record_id=None):
    if not text.strip():
        return [["neutral", 1.0]]
    if record_id is not None:
        cached = goe_cache().get(int(record_id))
        r = records().get(int(record_id))
        if cached and r and r.text.strip()[:500] == text.strip():   # text arrives truncated
            return cached
    preds = goe_model()(text)[0]
    f = {}
    for d in preds:
        fam = G2F.get(d["label"], "neutral")
        f[fam] = f.get(fam, 0) + d["score"]
    tot = sum(f.values()) or 1.0
    f = {k: v / tot for k, v in f.items()}
    return [[l, round(float(s), 4)] for l, s in sorted(f.items(), key=lambda x: -x[1])[:3]]

def similarity(pe, ie):
    p, q = va_point(pe), va_point(ie)
    va = va_sim(p, q); overlap = soft(pe, ie)          # the analysis's own functions, unchanged
    return {"va": round(va, 3), "overlap": round(overlap, 3),
            "family_match": pe[0][0] == ie[0][0],
            "valence_match": sign(pe[0][0]) != "0" and sign(pe[0][0]) == sign(ie[0][0]),
            "prompt_valence": sign(pe[0][0]), "image_valence": sign(ie[0][0]),
            # The TOP FAMILY, not the valence sign, is what the analysis splits on ("emotional
            # prompt" = GoEmotions top-1 != neutral). sign() collapses surprise to "0" alongside
            # neutral, so anything routing on valence alone mis-classifies surprise-led prompts.
            "prompt_top": pe[0][0], "image_top": ie[0][0],
            # display-only: the two valence-arousal points the VA number is the distance between.
            # Returned (not recomputed in JS) so the figure cannot drift from the science.
            "p_point": [round(p[0], 3), round(p[1], 3)],
            "i_point": [round(q[0], 3), round(q[1], 3)]}

# ---------------------------------------------------------------- chance baselines (computed, not hard-coded)
_BASE, _BASE_LOCK = None, threading.Lock()

def baselines(N=300):
    """Random-pairing null for every similarity metric, computed from this project's own outputs
    with the IDENTICAL procedure as analysis_final.py (shuffle the image side N times, average).

    The UI needs these because the metrics do NOT start at zero: two *randomly paired* text/image
    records already score ~76% on valence-arousal similarity. A bare "71%" therefore reads as a
    pass when it is in fact below chance. Serving the measured null lets the interface mark it.
    """
    global _BASE
    with _BASE_LOCK:
        if _BASE is not None:
            return _BASE
        import random as _r, statistics as _st
        jl = os.path.join(OUT, "describe_extract.jsonl")
        gc = os.path.join(OUT, "prompt_emotions_goe.json")
        if not (os.path.exists(jl) and os.path.exists(gc)):
            _BASE = {"available": False, "centroids": CEN}
            return _BASE

        rows = [json.loads(l) for l in open(jl, encoding="utf-8")]
        rows = [r for r in rows if r["id"] > 13]                 # drop pre-test ids, as the analysis does
        goe = {int(k): v for k, v in json.load(open(gc)).items()}
        recs = [(goe[r["id"]], r["image_emotions"]) for r in rows if r["id"] in goe]

        def mtr(pairs):
            nsign = sum(1 for p, _ in pairs if sign(p[0][0]) != "0") or 1
            sims = [similarity(p, i) for p, i in pairs]           # one pass — 300 shuffles is hot
            return {"va": _st.mean(s["va"] for s in sims),
                    "vsign": sum(1 for s in sims if s["valence_match"]) / nsign,
                    "family": sum(1 for s in sims if s["family_match"]) / len(sims),
                    "overlap": _st.mean(s["overlap"] for s in sims)}

        def pcts(vals):
            """101 percentile points (p0..p100) — a compact stand-in for the whole distribution."""
            s = sorted(vals)
            return [round(s[min(len(s) - 1, int(round(q / 100 * (len(s) - 1))))], 4) for q in range(101)]

        def null_for(pairs, PD=N):
            if len(pairs) < 5:
                return None
            obs, ps, im = mtr(pairs), [p for p, _ in pairs], [i for _, i in pairs]
            acc = {k: [] for k in obs}
            per = {"va": [], "overlap": []}      # PER-PAIR null values, not per-shuffle averages
            rng = _r.Random(20260816)            # fixed seed → a stable, citable line
            for t in range(N):
                sh = im[:]; rng.shuffle(sh)
                shuffled = list(zip(ps, sh))
                for k, v in mtr(shuffled).items():
                    acc[k].append(v)
                if t < PD:                       # a single comparison must be judged against the
                    for p, i in shuffled:        # spread of individual random pairs, not against
                        s = similarity(p, i)     # the mean of subset means
                        per["va"].append(s["va"]); per["overlap"].append(s["overlap"])
            # A null whose spread is zero is DEGENERATE: shuffling cannot change the metric (e.g.
            # every prompt in the subset shares one label), so its "chance" figure is an identity,
            # not a baseline. Flagged so the interface can refuse to draw a chance line for it.
            sd = {k: _st.pstdev(v) for k, v in acc.items()}
            mu = {k: _st.mean(v) for k, v in acc.items()}
            # Only what the interface actually draws is served. `observed` and `z` are deliberately
            # withheld: this shuffle uses its own seed, so its z would differ in the first decimal
            # from the dissertation's and there is no way for a reader to know which is authoritative.
            return {"n": len(pairs),
                    "null": {k: round(mu[k], 4) for k in acc},
                    "degenerate": sorted(k for k in acc if sd[k] < 1e-6),
                    "pair_pct": {k: pcts(v) for k, v in per.items()}}

        # The VA metric cannot reach 0: it is a normalised distance between points in a fixed
        # 7-centroid space, so the most distant possible pair still scores this. Computed, not
        # assumed — it becomes the floor of the UI's axis so no dead ink is drawn.
        floor = min(similarity([[a, 1.0]], [[b, 1.0]])["va"] for a in CEN for b in CEN)

        # The three blocks the dissertation actually reports. A prompt is "emotional" when its top
        # family is not neutral — the same rule as analysis_final.py, so the chance line a visitor
        # sees is the one published for their case.
        _BASE = {"available": True, "shuffles": N, "centroids": CEN, "va_floor": round(floor, 4),
                 "all": null_for(recs),
                 "emotional": null_for([(p, i) for p, i in recs if p[0][0] != "neutral"]),
                 "non_emotional": null_for([(p, i) for p, i in recs if p[0][0] == "neutral"])}
        return _BASE

# ---------------------------------------------------------------- dataset (safe pool only)
_RECORDS = None
def records():
    """Analysed records (ids 14+) minus the withheld set — the ONLY pool this app serves.

    data.load() applies the reviewed name redaction, so every text this app can display has
    already had private individuals' names replaced with a placeholder.
    """
    global _RECORDS
    if _RECORDS is None:
        import sys
        sys.path.insert(0, ROOT)
        from emoviz import data
        _RECORDS = {r.id: r for r in data.load(with_timestamps=False)
                    if r.id > 13 and r.id not in WITHHELD_IDS}
    return _RECORDS

def thumb_b64(path, size=520, q=82):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((size, size))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

# featured examples: one per family, computed from the analysis CSV (no hard-coded ids)
_FEATURED = None
def featured():
    global _FEATURED
    if _FEATURED is not None:
        return _FEATURED
    want = [("joy", "a happy one"), ("sadness", "a sad one"), ("anger", "an angry one"),
            ("fear", "a fearful one"), ("surprise", "a surprised one"), ("neutral", "not a feeling")]
    rows = []
    p = os.path.join(OUT, "analysis_final.csv")
    if os.path.exists(p):
        rows = list(csv.DictReader(open(p)))
    out = []
    recs = records()
    for fam, label in want:
        for r in rows:
            rid = int(r["id"])
            if (r["prompt_emotion"] == fam and rid in recs and r["face"] == "1"
                    and 3 <= len(r["text"]) <= 60):
                rec = recs[rid]
                out.append({"id": rid, "label": label, "text": rec.text.strip(),
                            "thumb": thumb_b64(rec.image_path, size=140, q=70)})
                break
    _FEATURED = out
    return out

# ---------------------------------------------------------------- routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    return jsonify({"vqa": "vqa" in _M, "nli": "nli" in _M, "goe": "goe" in _M,
                    "warming": _WARMING["active"],
                    "ready": ("vqa" in _M and "nli" in _M)})

@app.route("/api/warmup", methods=["POST"])
def api_warmup():
    if not _WARMING["active"] and not ("vqa" in _M and "nli" in _M):
        _WARMING["active"] = True
        threading.Thread(target=_warm, daemon=True).start()
    return jsonify({"started": True})

@app.route("/api/baselines")
def api_baselines():
    """Chance lines + emotion centroids, so the UI never hard-codes a number the science owns."""
    return jsonify(baselines())

@app.route("/api/featured")
def api_featured():
    return jsonify(featured())

@app.route("/api/random")
def api_random():
    import random as _r
    recs = records()
    rid = _r.choice(list(recs.keys()))
    r = recs[rid]
    return jsonify({"id": r.id, "text": r.text.strip(), "image": thumb_b64(r.image_path)})

@app.route("/api/record/<int:rid>")
def api_record(rid):
    r = records().get(rid)
    if not r:
        # Deliberately does NOT say *why* an in-range id is missing. Distinguishing "withheld" from
        # "invalid" would let anyone walk 14–1025 and recover the exact list of records flagged as
        # containing real names or sensitive disclosures — which is the thing withholding protects.
        why = ("ids 1–13 are pre-test images" if rid <= 13
               else "valid ids are 14–1025" if rid > 1025
               else "it isn't part of the demo pool")   # stays vague: see WITHHELD_IDS
        return jsonify({"error": f"Record {rid} isn't available — {why}."}), 404
    return jsonify({"id": r.id, "text": r.text.strip(), "image": thumb_b64(r.image_path)})

@app.route("/api/record/<path:rid>")
def api_record_bad(rid):
    """Non-integer ids would otherwise hit Flask's HTML 404 and the UI would misreport it as a
    network failure. Answer in the same JSON shape as the real route."""
    return jsonify({"error": f"“{rid}” isn't a drawing number — use a whole number from 14 to 1025."}), 404

@app.route("/api/analyse", methods=["POST"])
def api_analyse():
    from PIL import Image
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "That request wasn't valid JSON."}), 400
    raw = (payload.get("text") or "").strip()
    text = raw[:500]
    result = {"text": text}
    if len(raw) > len(text):                 # tell the UI rather than silently dropping words
        result["truncated"] = len(raw)

    img = None
    if payload.get("record_id"):
        rid = int(payload["record_id"])
        r = records().get(rid)
        if r:
            img = Image.open(r.image_path).convert("RGB")
        else:
            result["warning"] = f"Record {rid} isn't available in the demo."
    elif payload.get("image_b64"):
        try:
            raw = base64.b64decode(payload["image_b64"].split(",")[-1])
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            img.thumbnail((1024, 1024))
        except Exception:
            return jsonify({"error": "That file couldn't be read as an image."}), 400

    with _LOCK:   # one visitor at a time through the models
        if img is not None:
            desc, vqa = describe_image(img)
            ie = emotion_from_description(desc)
            result.update({"vqa": vqa, "description": desc, "image_emotions": ie})
        else:
            ie = None
        pe = emotion_from_prompt(text, payload.get("record_id")) if text else None

    if pe:
        result["prompt_emotions"] = pe
    if pe and ie:
        result["similarity"] = similarity(pe, ie)
    return jsonify(result)

if __name__ == "__main__":
    # No request log. The default werkzeug access log records every visitor's IP address and the
    # ids they viewed; for a demo shared publicly on an ethics-sensitive dataset that is data we
    # have no reason to hold. Errors and tracebacks still reach stderr.
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    # Chance lines are pure-Python and take a few seconds; compute them off the request path so the
    # first visitor doesn't wait. Harmless if it finishes after the page loads (the UI re-fetches).
    threading.Thread(target=baselines, daemon=True).start()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5050"))
    print(f"\n  EmoViz  →  http://{host if host != '0.0.0.0' else '<your-ip>'}:{port}")
    print("  (models load in the background on first visit; ~1.8 GB in float16)\n")
    app.run(host=host, port=port, debug=False, threaded=True)
