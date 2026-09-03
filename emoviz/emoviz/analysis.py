"""
emoviz.analysis — the two headline analyses from RESEARCH_GAP.md.

  consistency()  RQ3 : across the 66 duplicate-prompt runs, how stable is the
                       rendering under an identical prompt? Uses image FEATURES
                       (always available) and, if present, image-emotion labels.
  fidelity()     RQ1 : does the emotion in the image match the emotion in the
                       text? If a CLIP image-emotion backend has run, compares
                       basic labels + valence. Otherwise reports the honest
                       preliminary signal: correlation between text valence/arousal
                       and image structural features (RQ2).

Pure numpy; no sklearn/scipy required (Pearson r and simple stats hand-rolled).
"""
from __future__ import annotations
import numpy as np

FEATURE_KEYS = ["ink_density", "brightness", "contrast", "edge_density",
                "entropy", "v_center", "h_spread", "symmetry"]


def _pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3 or x.std() == 0 or y.std() == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def _cohens_kappa(a, b):
    """Categorical agreement between two label lists."""
    labels = sorted(set(a) | set(b))
    idx = {l: i for i, l in enumerate(labels)}
    n = len(a); k = len(labels)
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = np.zeros(k); pb = np.zeros(k)
    for x in a: pa[idx[x]] += 1
    for y in b: pb[idx[y]] += 1
    pa /= n; pb /= n
    exp = float((pa * pb).sum())
    return float((obs - exp) / (1 - exp)) if exp < 1 else 1.0, obs


# --------------------------------------------------------------------------- RQ3
def consistency(rows: list[dict]) -> dict:
    """rows: dicts with id, run_id, run_size, features{}, [img_basic].
    Measures within-run variability of identical prompts."""
    runs = {}
    for r in rows:
        if r.get("run_size", 1) > 1:
            runs.setdefault(r["run_id"], []).append(r)

    per_run = []
    feat_cv = {k: [] for k in FEATURE_KEYS}          # coefficient of variation
    label_agreements = []
    for rid, members in runs.items():
        if len(members) < 2:
            continue
        entry = {"run_id": rid, "size": len(members),
                 "text": members[0].get("text", ""),
                 "ids": [m["id"] for m in members]}
        # feature variability
        for k in FEATURE_KEYS:
            vals = [m["features"][k] for m in members if m.get("features")]
            if len(vals) >= 2:
                mu = np.mean(vals); sd = np.std(vals)
                cv = sd / abs(mu) if mu else 0.0
                entry[f"cv_{k}"] = round(cv, 3)
                feat_cv[k].append(cv)
        # emotion-label consistency within the run (if image emotion present)
        labs = [m["img_basic"] for m in members if m.get("img_basic")]
        if labs:
            top = max(set(labs), key=labs.count)
            agr = labs.count(top) / len(labs)
            entry["label_mode"] = top
            entry["label_agreement"] = round(agr, 3)
            label_agreements.append(agr)
        per_run.append(entry)

    return {
        "n_runs": len(per_run),
        "mean_feature_cv": {k: round(float(np.mean(v)), 3) for k, v in feat_cv.items() if v},
        "mean_label_agreement": round(float(np.mean(label_agreements)), 3) if label_agreements else None,
        "per_run": sorted(per_run, key=lambda e: -e["size"]),
    }


# --------------------------------------------------------------------------- RQ1 / RQ2
def fidelity(rows: list[dict]) -> dict:
    """rows: dicts with text_valence, text_arousal, text_basic, is_emotional,
    features{}, and optionally img_basic, img_valence."""
    emo = [r for r in rows if r.get("is_emotional")]

    out = {"n_total": len(rows), "n_emotional": len(emo)}

    # --- RQ2: text affect vs image structural features (always available) ---
    tv = [r["text_valence"] for r in emo if r.get("features")]
    ta = [r["text_arousal"] for r in emo if r.get("features")]
    feat_corr = {}
    for k in FEATURE_KEYS:
        fv = [r["features"][k] for r in emo if r.get("features")]
        feat_corr[k] = {"r_valence": round(_pearson(tv, fv), 3),
                        "r_arousal": round(_pearson(ta, fv), 3)}
    out["text_vs_image_feature_corr"] = feat_corr

    # --- RQ1: text emotion vs image emotion (only if CLIP ran) ---
    paired = [r for r in emo if r.get("img_basic") and r.get("text_basic")]
    if paired:
        k, obs = _cohens_kappa([r["text_basic"] for r in paired],
                               [r["img_basic"] for r in paired])
        out["text_vs_image_emotion"] = {
            "n_paired": len(paired),
            "agreement": round(obs, 3),
            "cohens_kappa": round(k, 3),
            "valence_r": round(_pearson([r["text_valence"] for r in paired],
                                        [r.get("img_valence", 0) for r in paired]), 3),
        }
    else:
        out["text_vs_image_emotion"] = None  # needs CLIP backend
    return out


def distribution(rows: list[dict]) -> dict:
    """Corpus-level emotion + affect distribution (text side)."""
    from collections import Counter
    basics = Counter(r["text_basic"] for r in rows if r.get("is_emotional"))
    quadrants = Counter(r.get("text_quadrant") for r in rows if r.get("is_emotional"))
    return {
        "basic_counts": dict(basics.most_common()),
        "quadrant_counts": dict(quadrants),
        "n_emotional": sum(1 for r in rows if r.get("is_emotional")),
        "n_non_emotional": sum(1 for r in rows if not r.get("is_emotional")),
        "mean_valence": round(float(np.mean([r["text_valence"] for r in rows if r.get("is_emotional")])), 3),
        "mean_arousal": round(float(np.mean([r["text_arousal"] for r in rows if r.get("is_emotional")])), 3),
    }
