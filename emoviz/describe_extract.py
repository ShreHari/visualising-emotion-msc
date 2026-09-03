#!/usr/bin/env python3
"""
emoviz/describe_extract.py — Chen's "describe -> extract -> compare by similarity" pipeline.

Per record:
  IMAGE  -> BLIP-VQA answers visual questions (facial expression, action, posture, scene)  [NO emotion asked]
         -> the answers are composed into a description
         -> zero-shot NLI infers emotion from that description   (top-3)
  PROMPT -> zero-shot NLI infers emotion from the text           (top-3)
Both sides land on the SAME 7-label space, so Stage 3 compares them by SIMILARITY.

Why this exact shape (each link was TESTED before building):
  * GoEmotions collapses object-descriptions to 'neutral' -> use NLI, which INFERS emotion from cues.
  * A single terse caption is too sparse for NLI (collapses to 'surprise').
  * Qwen2.5-VL-3B (the "ideal" describer) THRASHED this laptop's RAM into swap (7GB, no progress) and
    Florence-2 breaks on transformers 5.14 -> both rejected.
  * BLIP-VQA is small (~0.4B, runs fine here) and its "facial expression?" answer ('smiling'/'sad')
    gives NLI the affective cue it needs. Faithful to Chen: describe the visible expression, extract
    emotion separately. (Grounding emotion in the depicted face suits a facial-expression supervisor.)

CRASH-SAFE / RESUMABLE: one JSON line per record appended to outputs/describe_extract.jsonl;
already-done ids are skipped on restart.

Run:  .venv/bin/python describe_extract.py --limit 30     # test
      .venv/bin/python describe_extract.py                # full (resumable)
"""
from __future__ import annotations
import argparse, json, os, sys, time, traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "outputs")
JSONL = os.path.join(OUT, "describe_extract.jsonl")
FAILLOG = os.path.join(OUT, "describe_extract.failures.log")

VQA_ID = "Salesforce/blip-vqa-base"
NLI_ID = "facebook/bart-large-mnli"
LABELS = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
QUESTIONS = [
    ("expression", "What is the facial expression?"),
    ("action", "What is the person doing?"),
    ("posture", "What is the body posture?"),
    ("people", "How many people are there?"),
    ("scene", "What is in the picture?"),
]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_models():
    import torch
    from transformers import BlipProcessor, BlipForQuestionAnswering, pipeline
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    log(f"device={dev}; loading BLIP-VQA ({VQA_ID}) ...")
    proc = BlipProcessor.from_pretrained(VQA_ID)
    vqa = BlipForQuestionAnswering.from_pretrained(VQA_ID).to(dev).eval()
    log(f"loading NLI ({NLI_ID}) ...")
    zs = pipeline("zero-shot-classification", model=NLI_ID, device=dev)
    log("models ready")
    return torch, proc, vqa, zs, dev


def describe(torch, proc, vqa, dev, path):
    from PIL import Image
    img = Image.open(path).convert("RGB")
    ans = {}
    for key, q in QUESTIONS:
        inp = proc(img, q, return_tensors="pt").to(dev)
        with torch.no_grad():
            o = vqa.generate(**inp, max_new_tokens=15)
        ans[key] = proc.decode(o[0], skip_special_tokens=True).strip()
    desc = (f"A drawing of {ans.get('people','a')} showing {ans.get('scene','a scene')}. "
            f"The person is {ans.get('action','present')}, {ans.get('posture','')}. "
            f"The facial expression is {ans.get('expression','unclear')}.")
    return desc, ans


def nli_top3(zs, text, tmpl):
    if not text or not text.strip():
        return [["neutral", 1.0]]
    z = zs(text, LABELS, hypothesis_template=tmpl)
    return [[l, round(float(s), 4)] for l, s in list(zip(z["labels"], z["scores"]))[:3]]


def done_ids(path=JSONL):
    ids = set()
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            try:
                ids.add(json.loads(line)["id"])
            except Exception:
                pass
    return ids


def run(limit=None, out=None):
    os.makedirs(OUT, exist_ok=True)
    jsonl_path = out or JSONL          # --out lets you demo to a scratch file, keeping real results safe
    sys.path.insert(0, ROOT)
    from emoviz import data
    # NOTE: pre-test ids 1-13 are deliberately KEPT here — the pipeline processes 100% of the
    # dataset for full data accounting; they are excluded downstream (analysis_final.py PRETEST_MAX_ID).
    recs = list(data.load(with_timestamps=False))
    if limit:
        recs = recs[:limit]
    already = done_ids(jsonl_path)
    todo = [r for r in recs if r.id not in already]
    log(f"{len(recs)} records in scope; {len(already)} done; {len(todo)} to process")
    if not todo:
        log("nothing to do"); return

    torch, proc, vqa, zs, dev = load_models()
    t0 = time.time(); ok = fail = 0
    with open(jsonl_path, "a", encoding="utf-8") as fh:
        for n, r in enumerate(todo, 1):
            try:
                desc, ans = describe(torch, proc, vqa, dev, r.image_path)
                pe = nli_top3(zs, r.text, "This person feels {}.")
                de = nli_top3(zs, desc, "This scene conveys {}.")
                rec = {"id": r.id, "text": r.text.strip(), "dedup_key": r.dedup_key,
                       "image_path": r.image_path,
                       "vqa": ans, "description": desc,
                       "prompt_emotions": pe, "image_emotions": de,
                       "prompt_top1": pe[0][0], "image_top1": de[0][0]}
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); fh.flush()
                ok += 1
            except Exception as e:
                fail += 1
                with open(FAILLOG, "a", encoding="utf-8") as fl:
                    fl.write(f"id={r.id} {type(e).__name__}: {e}\n{traceback.format_exc()}\n")
                log(f"  ! failed id={r.id}: {type(e).__name__}: {e}")
            if n % 50 == 0 or n == len(todo):
                rate = (time.time() - t0) / n
                log(f"  {n}/{len(todo)}  ok={ok} fail={fail}  {rate:.1f}s/rec  ETA {rate*(len(todo)-n)/60:.0f}m")
    log(f"DONE. ok={ok} fail={fail}. Output: {jsonl_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="process only first N records")
    ap.add_argument("--out", default=None, help="write to a scratch file instead of the real results")
    a = ap.parse_args()
    run(limit=a.limit, out=a.out)
