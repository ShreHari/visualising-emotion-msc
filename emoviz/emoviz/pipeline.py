"""
emoviz.pipeline — run the whole thing end-to-end and cache results.

  load corpus -> text emotion -> image features -> (optional) image emotion
              -> fidelity + consistency + distribution -> outputs/results.json

Designed to run TODAY with zero heavy deps (lexicon text + numpy/PIL features).
Add --image-backend clip once setup.sh has installed torch/open_clip.
"""
from __future__ import annotations
import csv, json, os, time
from . import data, image_features, analysis
from .text_emotion import get_backend as get_text_backend

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")


def run(root=None, *, text_backend="lexicon", image_backend=None,
        drop_pretest=True, limit=None, image_size=256, progress=True):
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()

    records = data.load(root, with_timestamps=True, drop_pretest=drop_pretest)
    if limit:
        records = records[:limit]
    integ = data.integrity(records)

    tb = get_text_backend(text_backend)
    ib = None
    if image_backend:
        from .image_emotion import get_backend as get_img_backend
        ib = get_img_backend(image_backend)  # raises with install hint if torch missing

    rows = []
    n = len(records)
    for i, r in enumerate(records):
        tp = tb.predict(r.text)
        feats = image_features.extract(r.image_path, size=image_size)
        row = {
            "id": r.id, "text": r.text, "image_path": r.image_path,
            "timestamp": r.timestamp, "run_id": r.run_id, "run_size": r.run_size,
            "word_count": r.word_count, "is_ascii": r.is_ascii,
            "text_valence": tp.valence, "text_arousal": tp.arousal,
            "text_basic": tp.basic, "text_quadrant": tp.quadrant(),
            "is_emotional": tp.is_emotional,
            "features": feats.to_dict() if feats else None,
        }
        if ib:
            ip = ib.predict_path(r.image_path)
            if ip:
                row.update(img_basic=ip.basic, img_valence=ip.valence,
                           img_arousal=ip.arousal, img_scores=ip.scores)
        rows.append(row)
        if progress and (i + 1) % 100 == 0:
            print(f"  {i+1}/{n}  ({(i+1)/(time.time()-t0):.0f}/s)")

    result = {
        "meta": {
            "n": len(rows), "text_backend": tb.name,
            "image_backend": ib.name if ib else None,
            "dropped_pretest": drop_pretest, "elapsed_s": round(time.time() - t0, 1),
        },
        "integrity": integ,
        "distribution": analysis.distribution(rows),
        "fidelity": analysis.fidelity(rows),
        "consistency": analysis.consistency(rows),
    }

    # persist
    with open(os.path.join(OUT, "results.json"), "w") as fh:
        json.dump({**result, "rows": rows}, fh, indent=1)
    _write_csv(rows)
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(result, fh, indent=1)
    print(f"\nDone in {result['meta']['elapsed_s']}s -> {OUT}/results.json")
    return result, rows


def _write_csv(rows):
    keys = ["id", "text", "timestamp", "run_id", "run_size", "word_count",
            "text_valence", "text_arousal", "text_basic", "text_quadrant", "is_emotional",
            *[f"feat_{k}" for k in analysis.FEATURE_KEYS],
            "img_basic", "img_valence"]
    with open(os.path.join(OUT, "records.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(keys)
        for r in rows:
            feats = r.get("features") or {}
            w.writerow([
                r["id"], r["text"].replace("\n", " ")[:200], r.get("timestamp"),
                r["run_id"], r["run_size"], r["word_count"],
                r["text_valence"], r["text_arousal"], r["text_basic"],
                r["text_quadrant"], r["is_emotional"],
                *[feats.get(k, "") for k in analysis.FEATURE_KEYS],
                r.get("img_basic", ""), r.get("img_valence", ""),
            ])


if __name__ == "__main__":
    run()
