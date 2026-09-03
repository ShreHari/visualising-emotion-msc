"""
emoviz.image_emotion — classify the emotion an image conveys.

CLIPBackend: zero-shot classification with CLIP (Radford et al. 2021). For each
Ekman emotion we score the image against an *ensemble* of natural-language prompts
(text embeddings averaged per emotion) and softmax across emotions. This is the
standard, defensible approach for image-emotion on out-of-distribution stimuli like
line-art (no labelled line-art training set exists — see RESEARCH_GAP.md). Needs
`torch` + `open_clip_torch`: run emoviz/setup.sh.

A manual re-check (2026-07-19) found plain CLIP zero-shot is unreliable here: it
forces confident emotions onto faceless *scene* images and confuses open-mouth joy
with anger. This version adds, per that finding:
  1. prompt ENSEMBLE (mean text embedding per label) instead of max-pool of one prompt;
  2. a calibrated temperature (0.05, not 0.01) so scores are not falsely peaked;
  3. a CONTENT GATE (portrait/face vs scene) so callers can restrict facial-emotion
     claims to images that actually show a readable face;
  4. disambiguated prompts (anger=scowl/furrowed brow; happiness=laughing/celebrating).
It also returns a confidence MARGIN (top1-top2) so low-confidence guesses can abstain.

Contract matches text_emotion: backend.predict_path(path) -> Prediction. Richer
detail (portrait_prob, margin) is available via predict_detail(path).
"""
from __future__ import annotations
from typing import Optional
from .text_emotion import Prediction, EKMAN

# Emotion prompt bank — parallel, expression-focused, never naming the medium.
# anger emphasises scowl/brow (not "shouting", which collides with open-mouth joy);
# happiness includes laughing/celebrating so triumphant open-mouth faces read as joy.
_PROMPTS = {
    "happiness": ["a happy smiling person", "a person laughing joyfully with a big smile",
                  "someone celebrating, delighted and cheerful", "a joyful person with arms raised in triumph"],
    "sadness":   ["a sad unhappy person", "someone crying with tears", "a downcast, gloomy, sorrowful figure",
                  "a lonely person looking dejected"],
    "anger":     ["an angry person scowling with furrowed brows", "a furious face with gritted teeth",
                  "someone frowning in rage, hostile and aggressive", "a person glaring with a clenched jaw"],
    "fear":      ["a scared, frightened person", "a terrified face with wide eyes",
                  "an anxious, tense person recoiling", "someone panicking in fear"],
    "surprise":  ["a surprised person with raised eyebrows", "an astonished face with an open mouth and wide eyes",
                  "someone startled and amazed"],
    "disgust":   ["a disgusted person wrinkling their nose", "a grossed-out, sneering face",
                  "someone recoiling from something revolting"],
    "neutral":   ["a calm person with a neutral, expressionless face", "an ordinary everyday moment with no strong emotion",
                  "a plain, emotionally flat scene"],
}
# Content gate: is there a single readable face, or is it a scene/object/crowd?
_GATE = {
    "face":   ["a close-up portrait of one person's face", "a single human face with a clear expression",
               "a headshot showing someone's facial expression"],
    "noface": ["a wide scene with objects, scenery or buildings", "a crowd of many small distant people",
               "a diagram, text, symbols or an abstract pattern", "hands, body parts or objects with no visible face"],
}
_CENTROID = {"happiness": (0.8, 0.6), "sadness": (-0.75, 0.3), "anger": (-0.7, 0.8),
             "fear": (-0.65, 0.75), "surprise": (0.3, 0.8), "disgust": (-0.7, 0.6),
             "neutral": (0.0, 0.3)}
_TEMP = 0.05           # calibrated softmax temperature (was 0.01 — falsely peaked)
_MARGIN_MIN = 0.10     # top1-top2 below this => low confidence (abstain-eligible)
_PORTRAIT_MIN = 0.55   # portrait_prob below this => treat as scene (no facial emotion)


class CLIPBackend:
    name = "clip-zeroshot-v2"

    def __init__(self, model="ViT-B-32", pretrained="laion2b_s34b_b79k", device=None):
        try:
            import torch, open_clip  # noqa
        except ImportError as e:
            raise ImportError(
                "CLIPBackend needs torch + open_clip_torch. Run emoviz/setup.sh, "
                "then re-run with --image-backend clip."
            ) from e
        import torch, open_clip
        self.torch = torch
        self.device = device or ("mps" if torch.backends.mps.is_available()
                                 else "cuda" if torch.cuda.is_available() else "cpu")
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model, pretrained=pretrained)
        self.model = self.model.to(self.device).eval()
        tok = open_clip.get_tokenizer(model)
        self.labels = list(_PROMPTS.keys())
        # ENSEMBLE: one averaged, re-normalised prototype embedding per label.
        self._proto = self._prototypes(tok, [_PROMPTS[l] for l in self.labels])
        # content gate prototypes: [face, noface]
        self._gate = self._prototypes(tok, [_GATE["face"], _GATE["noface"]])

    def _prototypes(self, tok, groups):
        torch = self.torch
        protos = []
        with torch.no_grad():
            for templates in groups:
                e = self.model.encode_text(tok(templates).to(self.device))
                e = e / e.norm(dim=-1, keepdim=True)
                m = e.mean(dim=0)
                m = m / m.norm()
                protos.append(m)
        return torch.stack(protos)  # [n_groups, d]

    def _encode(self, path):
        from PIL import Image
        torch = self.torch
        img = self.preprocess(Image.open(path).convert("RGB")).unsqueeze(0).to(self.device)
        with torch.no_grad():
            f = self.model.encode_image(img)
            f = f / f.norm(dim=-1, keepdim=True)
        return f

    def predict_detail(self, path: str) -> Optional[dict]:
        """Full detail: emotion scores + portrait_prob + margin + flags."""
        import numpy as np
        torch = self.torch
        try:
            f = self._encode(path)
        except Exception:
            return None
        with torch.no_grad():
            emo = (f @ self._proto.T).squeeze(0).detach().cpu().numpy()
            gate = (f @ self._gate.T).squeeze(0).detach().cpu().numpy()
        # emotion softmax (calibrated temperature)
        ex = np.exp((emo - emo.max()) / _TEMP); probs = ex / ex.sum()
        order = probs.argsort()[::-1]
        basic = self.labels[int(order[0])]
        margin = float(probs[order[0]] - probs[order[1]])
        # content gate softmax
        gx = np.exp((gate - gate.max()) / _TEMP); gp = gx / gx.sum()
        portrait_prob = float(gp[0])
        return {
            "scores": {l: round(float(p), 3) for l, p in zip(self.labels, probs)},
            "basic": basic,
            "margin": round(margin, 3),
            "portrait_prob": round(portrait_prob, 3),
            "has_face": portrait_prob >= _PORTRAIT_MIN,
            "confident": margin >= _MARGIN_MIN,
        }

    def predict_path(self, path: str) -> Optional[Prediction]:
        d = self.predict_detail(path)
        if d is None:
            return None
        basic = d["basic"]
        v, a = _CENTROID[basic]
        sc = dict(d["scores"])
        # stash gate/confidence in the scores dict under reserved keys (non-label)
        sc["_portrait_prob"] = d["portrait_prob"]
        sc["_margin"] = d["margin"]
        sc["_has_face"] = 1.0 if d["has_face"] else 0.0
        return Prediction(v, a, basic, sc, [], basic != "neutral")

    def predict_paths(self, paths):
        return [self.predict_path(p) for p in paths]


def get_backend(name: str = "clip"):
    if name in ("clip", "clip-zeroshot", "clip-zeroshot-v2"):
        return CLIPBackend()
    raise ValueError(f"unknown image backend: {name}")
