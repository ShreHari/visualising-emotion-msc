"""
emoviz.image_features — real, dependency-light structural descriptors of the
monochrome line-art (numpy + PIL only, no torch).

These are NOT emotion labels — they are objective image statistics. Their value:
(1) they run today over all 1025 images in seconds, and (2) the dissertation can
test whether any of them correlate with the *text* valence/arousal (a legitimate
preliminary signal about whether affect survives colour removal — RQ2). For
defensible image-EMOTION classification, use image_emotion.CLIPBackend.

Descriptors per image (all in [0,1] unless noted):
  ink_density     fraction of dark (drawn) pixels
  brightness      mean luminance / 255  (higher = more white space)
  contrast        std of luminance / 128
  edge_density    fraction of high-gradient pixels (line/detail busyness)
  entropy         Shannon entropy of the luminance histogram / 8  (visual complexity)
  v_center        vertical centre-of-mass of ink (0 top .. 1 bottom)
  h_spread        horizontal spread of ink (std of x, normalised)
  symmetry        left-right mirror similarity of the ink mask
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import Optional
import numpy as np
from PIL import Image

INK_THRESHOLD = 100  # luminance below this counts as "ink"

@dataclass
class Features:
    ink_density: float
    brightness: float
    contrast: float
    edge_density: float
    entropy: float
    v_center: float
    h_spread: float
    symmetry: float

    def to_dict(self):
        return {k: round(v, 4) for k, v in asdict(self).items()}


def _load_gray(path: str, size: int = 256) -> np.ndarray:
    im = Image.open(path).convert("L")
    im.thumbnail((size, size))
    return np.asarray(im, dtype=np.float32)


def extract(path: str, size: int = 256) -> Optional[Features]:
    try:
        g = _load_gray(path, size)
    except Exception:
        return None
    h, w = g.shape
    tot = float(h * w)

    ink = g < INK_THRESHOLD
    ink_density = float(ink.sum()) / tot
    brightness = float(g.mean()) / 255.0
    contrast = float(g.std()) / 128.0

    # gradient magnitude (Sobel-ish via finite differences)
    gx = np.abs(np.diff(g, axis=1))
    gy = np.abs(np.diff(g, axis=0))
    edge_density = float((gx > 30).sum() + (gy > 30).sum()) / (2 * tot)

    # histogram entropy (visual complexity)
    hist, _ = np.histogram(g, bins=32, range=(0, 255))
    p = hist / max(hist.sum(), 1)
    p = p[p > 0]
    entropy = float(-(p * np.log2(p)).sum()) / 5.0  # /log2(32)

    # ink composition
    ys, xs = np.nonzero(ink)
    if len(ys):
        v_center = float(ys.mean()) / h
        h_spread = float(xs.std()) / w
    else:
        v_center, h_spread = 0.5, 0.0

    # left-right symmetry of the ink mask
    left = ink[:, : w // 2].astype(np.float32)
    right = np.fliplr(ink[:, w - w // 2:]).astype(np.float32)
    m = min(left.shape[1], right.shape[1])
    if m:
        agree = (left[:, :m] == right[:, :m]).mean()
        symmetry = float(agree)
    else:
        symmetry = 0.0

    return Features(ink_density, brightness, contrast, edge_density,
                    entropy, v_center, h_spread, symmetry)


if __name__ == "__main__":
    from . import data
    recs = data.load(with_timestamps=False)
    for r in recs[:5]:
        f = extract(r.image_path)
        print(f"#{r.id:<4} {r.text[:32]!r:34s} {f.to_dict() if f else 'FAIL'}")
