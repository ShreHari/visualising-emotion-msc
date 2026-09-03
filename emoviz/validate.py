#!/usr/bin/env python3
"""
[BASELINE-ERA tool — validated the direct-CLIP reader (v1). The current pipeline is describe_extract.py; kept as the scaffold for the human-rating study.]

emoviz/validate.py — measure how well the image-emotion reader actually works.

Plain CLIP zero-shot was found to mislabel line-art (faceless scenes -> confident
"disgust"; open-mouth joy -> "anger"). This harness quantifies reliability instead
of trusting it:

  1) sample   : draw a stratified sample (n per predicted emotion), run the v2 reader,
                save sample.json, and render a numbered contact-sheet montage.png so a
                human (or an expert eyeball) can judge many images in one view.
  2) score    : given ground-truth labels (labels.json = {idx: emotion}), compute
                precision per predicted class, overall accuracy, a confusion matrix,
                and whether the gate (has_face) / margin (confident) flags predict
                correctness. Compares against the plain-CLIP labels if provided.

Usage:
  .venv/bin/python validate.py sample --n-per-class 4 --seed 7
  # ...view outputs/validation/montage.png, write outputs/validation/labels.json...
  .venv/bin/python validate.py score
"""
from __future__ import annotations
import argparse, json, os, random
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "outputs", "validation")
os.makedirs(OUT, exist_ok=True)
EMOS = ["happiness", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]


def _load_records():
    import sys; sys.path.insert(0, ROOT)
    from emoviz import data
    return list(data.load(with_timestamps=False))


def cmd_sample(args):
    from emoviz.image_emotion import CLIPBackend
    recs = _load_records()
    be = CLIPBackend()
    rng = random.Random(args.seed)
    # predict all (fast on MPS), then stratify by predicted label
    rng.shuffle(recs)
    bucket = defaultdict(list)
    preds = {}
    print(f"scanning {len(recs)} images for a stratified sample...")
    for r in recs:
        d = be.predict_detail(r.image_path)
        if d is None:
            continue
        preds[r.id] = d
        if len(bucket[d["basic"]]) < args.n_per_class:
            bucket[d["basic"]].append(r)
        if all(len(bucket[e]) >= args.n_per_class for e in EMOS):
            break
    sample = []
    for e in EMOS:
        for r in bucket[e]:
            d = preds[r.id]
            sample.append({"id": r.id, "path": r.image_path, "text": r.text,
                           "pred": d["basic"], "margin": d["margin"],
                           "portrait_prob": d["portrait_prob"], "has_face": d["has_face"],
                           "scores": d["scores"]})
    for i, s in enumerate(sample):
        s["idx"] = i
    json.dump(sample, open(os.path.join(OUT, "sample.json"), "w"), indent=1)
    _montage(sample, cols=args.cols, thumb=args.thumb)
    # write a blank labels template
    tmpl = {str(s["idx"]): "" for s in sample}
    p = os.path.join(OUT, "labels_template.json")
    json.dump(tmpl, open(p, "w"), indent=1)
    print(f"wrote {len(sample)} -> {OUT}/sample.json + montage.png")
    print(f"label each idx in {p} with one of {EMOS} (or 'scene' if no readable emotion),")
    print("save as labels.json, then: validate.py score")


def _montage(sample, cols=4, thumb=256):
    from PIL import Image, ImageDraw, ImageFont
    rows = (len(sample) + cols - 1) // cols
    pad, header = 6, 22
    cw, ch = thumb + 2 * pad, thumb + header + 2 * pad
    canvas = Image.new("RGB", (cols * cw, rows * ch), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    for s in sample:
        i = s["idx"]; r, c = divmod(i, cols)
        x0, y0 = c * cw, r * ch
        draw.text((x0 + pad, y0 + 3), f"[{i}]  {s['text'][:26]}", fill="black", font=font)
        try:
            im = Image.open(s["path"]).convert("RGB")
            im.thumbnail((thumb, thumb))
            canvas.paste(im, (x0 + pad, y0 + header + pad))
        except Exception:
            draw.text((x0 + pad, y0 + header + pad), "??", fill="red", font=font)
    canvas.save(os.path.join(OUT, "montage.png"))


def _kappa(a, b, labels):
    idx = {l: i for i, l in enumerate(labels)}
    n = len(a); k = len(labels)
    m = [[0] * k for _ in range(k)]
    for x, y in zip(a, b):
        m[idx[x]][idx[y]] += 1
    po = sum(m[i][i] for i in range(k)) / n
    rows = [sum(m[i]) / n for i in range(k)]
    cols = [sum(m[i][j] for i in range(k)) / n for j in range(k)]
    pe = sum(rows[i] * cols[i] for i in range(k))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po


def cmd_score(args):
    sample = json.load(open(os.path.join(OUT, "sample.json")))
    lp = os.path.join(OUT, "labels.json")
    if not os.path.exists(lp):
        print(f"no {lp} — label the images first (see labels_template.json)"); return
    labels = json.load(open(lp))
    by = {s["idx"]: s for s in sample}
    rows = []
    for k, truth in labels.items():
        s = by.get(int(k))
        if not s or not truth:
            continue
        rows.append((s, truth.strip().lower()))
    n = len(rows)
    print(f"=== VALIDATION on {n} labelled images (reader = v2 CLIP zero-shot) ===\n")

    # treat 'scene'/'none'/'unclear' truths as no-readable-emotion
    NOEMO = {"scene", "none", "unclear", "neutral"}
    # overall exact-match accuracy (model basic vs truth), all images
    correct = sum(1 for s, t in rows if s["pred"] == t)
    print(f"Overall exact-match accuracy (all):        {correct}/{n} = {correct/n:.0%}")

    # accuracy on images the annotator judged to HAVE a readable emotion
    emo_rows = [(s, t) for s, t in rows if t not in NOEMO]
    if emo_rows:
        c = sum(1 for s, t in emo_rows if s["pred"] == t)
        print(f"Accuracy on readable-emotion images:       {c}/{len(emo_rows)} = {c/len(emo_rows):.0%}")

    # does the gate help? accuracy on has_face vs scene
    for flag, name in [(True, "has_face=True "), (False, "has_face=False")]:
        sub = [(s, t) for s, t in rows if s["has_face"] == flag]
        if sub:
            c = sum(1 for s, t in sub if s["pred"] == t)
            print(f"  {name}: {c}/{len(sub)} = {c/len(sub):.0%}")
    # does margin (confidence) help?
    conf = [(s, t) for s, t in rows if s["margin"] >= 0.10]
    if conf:
        c = sum(1 for s, t in conf if s["pred"] == t)
        print(f"  confident (margin>=0.10): {c}/{len(conf)} = {c/len(conf):.0%}")

    # precision per predicted class
    print("\nPrecision per predicted class (when model says X, truth is X):")
    bypred = defaultdict(list)
    for s, t in rows:
        bypred[s["pred"]].append(t)
    for e in EMOS:
        ts = bypred.get(e, [])
        if ts:
            c = sum(1 for t in ts if t == e)
            print(f"  pred={e:9s} n={len(ts):2d}  precision={c/len(ts):.0%}  truths={dict(Counter(ts))}")

    # confusion (pred -> truth)
    print("\nConfusion (pred -> most common truths):")
    for e in EMOS:
        ts = bypred.get(e, [])
        if ts:
            print(f"  {e:9s}: {dict(Counter(ts).most_common())}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("sample"); sp.add_argument("--n-per-class", type=int, default=4)
    sp.add_argument("--seed", type=int, default=7); sp.add_argument("--cols", type=int, default=4)
    sp.add_argument("--thumb", type=int, default=256)
    sub.add_parser("score")
    args = ap.parse_args()
    {"sample": cmd_sample, "score": cmd_score}[args.cmd](args)
