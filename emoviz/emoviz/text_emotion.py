"""
emoviz.text_emotion — extract emotion from the free-text self-reports.

Pluggable backends behind a common interface:

  * LexiconBackend  (default, zero-dependency)  — a curated valence-arousal +
      basic-emotion affect lexicon. Runs today, no model download. Honest about
      being a baseline; good enough to demonstrate the pipeline end-to-end.
  * GoEmotionsBackend (optional) — HuggingFace transformer fine-tuned on the
      27-category GoEmotions taxonomy (Demszky et al. 2020). Needs `transformers`
      + `torch` (see setup.sh). Drop-in: same .predict() contract.

Interface:  backend.predict(text) -> Prediction
  Prediction(valence[-1..1], arousal[0..1], basic, scores{}, matched, is_emotional)

Valence/arousal follow Russell's (1980) circumplex; basic emotions use Ekman's
six + 'neutral'. Swap in the full NRC-VAD lexicon (Mohammad 2018) for the
dissertation proper — see load_nrc_vad().
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional

# ------------------------------------------------------------------ curated lexicon
# word -> (valence[-1..1], arousal[0..1], ekman_basic)
# Compact, weighted toward affect words actually frequent in this corpus.
LEXICON: dict[str, tuple[float, float, str]] = {
    # --- happiness / positive ---
    "happy": (0.85, 0.55, "happiness"), "happier": (0.8, 0.55, "happiness"),
    "happiness": (0.85, 0.55, "happiness"), "joy": (0.9, 0.65, "happiness"),
    "joyful": (0.9, 0.65, "happiness"), "glad": (0.7, 0.45, "happiness"),
    "cheerful": (0.8, 0.6, "happiness"), "delighted": (0.9, 0.7, "happiness"),
    "excited": (0.7, 0.85, "happiness"), "excitement": (0.7, 0.85, "happiness"),
    "thrilled": (0.85, 0.9, "happiness"), "elated": (0.9, 0.8, "happiness"),
    "content": (0.6, 0.3, "happiness"), "satisfied": (0.65, 0.35, "happiness"),
    "satisfaction": (0.65, 0.35, "happiness"), "grateful": (0.75, 0.4, "happiness"),
    "hopeful": (0.6, 0.5, "happiness"), "optimistic": (0.65, 0.5, "happiness"),
    "proud": (0.7, 0.6, "happiness"), "love": (0.9, 0.6, "happiness"),
    "loved": (0.85, 0.55, "happiness"), "loving": (0.85, 0.55, "happiness"),
    "peaceful": (0.6, 0.2, "happiness"), "calm": (0.5, 0.15, "happiness"),
    "relaxed": (0.55, 0.2, "happiness"), "comfortable": (0.5, 0.25, "happiness"),
    "amused": (0.7, 0.55, "happiness"), "fun": (0.75, 0.7, "happiness"),
    "blessed": (0.75, 0.45, "happiness"), "confident": (0.6, 0.55, "happiness"),
    "energetic": (0.6, 0.85, "happiness"), "inspired": (0.7, 0.65, "happiness"),
    "motivated": (0.6, 0.65, "happiness"), "curious": (0.4, 0.55, "happiness"),
    "interested": (0.45, 0.5, "happiness"),
    # --- sadness / low ---
    "sad": (-0.8, 0.3, "sadness"), "sadness": (-0.8, 0.3, "sadness"),
    "unhappy": (-0.75, 0.35, "sadness"), "depressed": (-0.85, 0.25, "sadness"),
    "depression": (-0.85, 0.25, "sadness"), "down": (-0.6, 0.3, "sadness"),
    "lonely": (-0.7, 0.3, "sadness"), "alone": (-0.55, 0.35, "sadness"),
    "lost": (-0.6, 0.4, "sadness"), "empty": (-0.7, 0.25, "sadness"),
    "hopeless": (-0.85, 0.35, "sadness"), "miserable": (-0.85, 0.4, "sadness"),
    "grief": (-0.85, 0.45, "sadness"), "heartbroken": (-0.9, 0.5, "sadness"),
    "disappointed": (-0.6, 0.4, "sadness"), "gloomy": (-0.65, 0.3, "sadness"),
    "melancholy": (-0.6, 0.3, "sadness"), "tired": (-0.35, 0.25, "sadness"),
    "exhausted": (-0.45, 0.3, "sadness"), "drained": (-0.5, 0.3, "sadness"),
    "numb": (-0.5, 0.2, "sadness"), "hurt": (-0.7, 0.45, "sadness"),
    "crying": (-0.75, 0.55, "sadness"), "regret": (-0.6, 0.4, "sadness"),
    "guilty": (-0.6, 0.45, "sadness"), "ashamed": (-0.65, 0.45, "sadness"),
    "homesick": (-0.55, 0.4, "sadness"), "nostalgic": (-0.1, 0.4, "sadness"),
    # --- anger ---
    "angry": (-0.7, 0.8, "anger"), "anger": (-0.7, 0.8, "anger"),
    "mad": (-0.65, 0.8, "anger"), "furious": (-0.8, 0.9, "anger"),
    "rage": (-0.85, 0.95, "anger"), "annoyed": (-0.5, 0.6, "anger"),
    "irritated": (-0.5, 0.6, "anger"), "frustrated": (-0.6, 0.65, "anger"),
    "frustration": (-0.6, 0.65, "anger"), "resentful": (-0.65, 0.6, "anger"),
    "hate": (-0.85, 0.8, "anger"), "disgusted": (-0.7, 0.65, "disgust"),
    "disgust": (-0.7, 0.65, "disgust"), "sick": (-0.5, 0.45, "disgust"),
    "fed": (-0.5, 0.6, "anger"),  # "fed up"
    # --- fear / anxiety ---
    "afraid": (-0.7, 0.75, "fear"), "scared": (-0.7, 0.8, "fear"),
    "fear": (-0.7, 0.8, "fear"), "fearful": (-0.7, 0.8, "fear"),
    "anxious": (-0.6, 0.7, "fear"), "anxiety": (-0.6, 0.7, "fear"),
    "nervous": (-0.5, 0.7, "fear"), "worried": (-0.55, 0.6, "fear"),
    "stressed": (-0.6, 0.75, "fear"), "stress": (-0.6, 0.75, "fear"),
    "overwhelmed": (-0.55, 0.75, "fear"), "panic": (-0.75, 0.9, "fear"),
    "terrified": (-0.85, 0.9, "fear"), "uneasy": (-0.45, 0.55, "fear"),
    "insecure": (-0.55, 0.55, "fear"), "tense": (-0.5, 0.7, "fear"),
    "desperate": (-0.75, 0.7, "fear"), "confused": (-0.3, 0.5, "fear"),
    # --- surprise ---
    "surprised": (0.3, 0.8, "surprise"), "surprise": (0.3, 0.8, "surprise"),
    "shocked": (-0.1, 0.85, "surprise"), "amazed": (0.6, 0.8, "surprise"),
    "astonished": (0.5, 0.8, "surprise"), "stunned": (0.0, 0.8, "surprise"),
    # --- neutral / low-signal ---
    "bored": (-0.3, 0.15, "sadness"), "boredom": (-0.3, 0.15, "sadness"),
    "okay": (0.1, 0.3, "neutral"), "fine": (0.2, 0.3, "neutral"),
    "neutral": (0.0, 0.3, "neutral"), "meh": (-0.1, 0.2, "neutral"),
}

NEGATORS = {"not", "no", "never", "n't", "without", "hardly", "barely"}
_WORD = re.compile(r"[a-zA-Z']+")
FEEL_PATTERN = re.compile(r"\b(i\s*(am|'m|feel|felt|am feeling)|i'm|feeling|makes me)\b", re.I)

EKMAN = ["happiness", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]


@dataclass
class Prediction:
    valence: float          # -1..1
    arousal: float          # 0..1
    basic: str              # dominant Ekman category (or 'neutral')
    scores: dict            # basic -> weight
    matched: list           # matched (word, valence, arousal, basic)
    is_emotional: bool
    n_words: int = 0

    def quadrant(self) -> str:
        v, a = self.valence, self.arousal
        hi = a >= 0.5
        if v >= 0:
            return "excited-positive" if hi else "calm-positive"
        return "tense-negative" if hi else "low-negative"


class LexiconBackend:
    name = "lexicon-v1"

    def __init__(self, lexicon: Optional[dict] = None):
        self.lex = lexicon or LEXICON

    def predict(self, text: str) -> Prediction:
        tokens = [t.lower() for t in _WORD.findall(text or "")]
        matched, vs, as_, scores = [], [], [], {}
        for i, tok in enumerate(tokens):
            if tok in self.lex:
                v, a, basic = self.lex[tok]
                # simple negation: flip valence if a negator is within 2 tokens before
                window = tokens[max(0, i - 2):i]
                if any(w in NEGATORS for w in window):
                    v = -v * 0.6
                    basic = "neutral" if abs(v) < 0.25 else basic
                matched.append((tok, round(v, 2), round(a, 2), basic))
                vs.append(v); as_.append(a)
                scores[basic] = scores.get(basic, 0.0) + abs(v) + 0.3
        if matched:
            valence = sum(vs) / len(vs)
            arousal = sum(as_) / len(as_)
            basic = max(scores, key=scores.get)
            is_emo = True
        else:
            valence, arousal, basic = 0.0, 0.3, "neutral"
            is_emo = bool(FEEL_PATTERN.search(text or ""))
        return Prediction(round(valence, 3), round(arousal, 3), basic,
                          {k: round(v, 2) for k, v in scores.items()},
                          matched, is_emo, n_words=len(tokens))

    def predict_batch(self, texts):
        return [self.predict(t) for t in texts]


class GoEmotionsBackend:
    """Optional transformer backend (Demszky et al. 2020 taxonomy). Needs torch+transformers."""
    name = "goemotions-bert"
    # map the 27 GoEmotions labels onto Ekman-6 + neutral for a shared axis
    _MAP = {
        "admiration": "happiness", "amusement": "happiness", "approval": "happiness",
        "caring": "happiness", "desire": "happiness", "excitement": "happiness",
        "gratitude": "happiness", "joy": "happiness", "love": "happiness",
        "optimism": "happiness", "pride": "happiness", "relief": "happiness",
        "sadness": "sadness", "disappointment": "sadness", "grief": "sadness",
        "remorse": "sadness", "embarrassment": "sadness",
        "anger": "anger", "annoyance": "anger", "disapproval": "anger",
        "disgust": "disgust", "fear": "fear", "nervousness": "fear",
        "surprise": "surprise", "realization": "surprise", "confusion": "surprise",
        "curiosity": "happiness", "neutral": "neutral",
    }

    def __init__(self, model="SamLowe/roberta-base-go_emotions", device=None):
        try:
            import torch
            from transformers import pipeline  # noqa
        except ImportError as e:
            raise ImportError(
                "GoEmotionsBackend needs transformers+torch. Run emoviz/setup.sh, "
                "or use LexiconBackend (default)."
            ) from e
        import torch
        from transformers import pipeline
        if device is None:
            device = ("mps" if torch.backends.mps.is_available()
                      else 0 if torch.cuda.is_available() else -1)
        self.clf = pipeline("text-classification", model=model, top_k=None,
                            truncation=True, device=device, batch_size=32)

    def predict(self, text: str) -> Prediction:
        out = self.clf(text or "")[0]  # list of {label, score}
        scores = {}
        for d in out:
            b = self._MAP.get(d["label"], "neutral")
            scores[b] = scores.get(b, 0.0) + d["score"]
        basic = max(scores, key=scores.get)
        # rough valence/arousal from Ekman category centroids in the lexicon
        cents = {"happiness": (0.8, 0.6), "sadness": (-0.75, 0.3), "anger": (-0.7, 0.8),
                 "fear": (-0.65, 0.75), "surprise": (0.3, 0.8), "disgust": (-0.7, 0.6),
                 "neutral": (0.0, 0.3)}
        v, a = cents[basic]
        return Prediction(v, a, basic, {k: round(val, 3) for k, val in scores.items()},
                          [], basic != "neutral", n_words=len((text or "").split()))

    def predict_batch(self, texts):
        return [self.predict(t) for t in texts]


def load_nrc_vad(path: str) -> dict:
    """Build a lexicon dict from the NRC-VAD tsv (word\\tvalence\\tarousal\\tdominance).
    Maps NRC's 0..1 valence to -1..1 and keeps arousal 0..1; basic emotion left 'neutral'
    (combine with NRC-EmoLex for categories). For the dissertation proper."""
    lex = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            w = parts[0]
            try:
                v = float(parts[1]) * 2 - 1
                a = float(parts[2])
            except ValueError:
                continue
            lex[w.lower()] = (v, a, "neutral")
    return lex


def get_backend(name: str = "lexicon"):
    if name in ("lexicon", "lexicon-v1"):
        return LexiconBackend()
    if name in ("goemotions", "bert"):
        return GoEmotionsBackend()
    raise ValueError(f"unknown text backend: {name}")


if __name__ == "__main__":
    b = LexiconBackend()
    for t in ["I am sad.", "tired but happy", "I feel depressed and lost",
              "I am not happy", "pigs", "excited for christmas", "A drawing depicting anger"]:
        p = b.predict(t)
        print(f"{t!r:42s} -> v={p.valence:+.2f} a={p.arousal:.2f} {p.basic:9s} "
              f"[{p.quadrant()}] emo={p.is_emotional}")
