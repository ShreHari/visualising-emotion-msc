"""
emoviz/metrics.py — the ONE definition of every quantity the project reports.

analysis_final.py, significance.py, app.py, test_numeric.py and the new analysis scripts all
import from here, so "valence-sign agreement", "family agreement", "top-3 overlap", the
valence–arousal similarity, the face rule and the random-pairing null cannot drift apart
between the analysis, the figures, the demo and the tests.

Vocabulary: the central quantity is *agreement* between the prompt reader (GoEmotions on the
self-report) and the image reader (zero-shot NLI on the BLIP-VQA description). Nothing here is
a statement about what a person would see in a drawing.

The random state is the caller's: analysis_final.py seeds `random` once (seed 7) and calls
with_null() in a fixed order, which is what makes every published null reproducible.
"""
from __future__ import annotations
import math, random, re, statistics as st

# ---- documented constants -------------------------------------------------------------------
PRETEST_MAX_ID = 13                       # ids 1-13 = pre-festival developer tests (timestamps 26 Aug-18 Sep)
FAMILIES = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
# emotion family -> (valence, arousal) centroid on the circumplex (Russell 1980; Posner et al. 2005).
# Hand-set from the standard placement of the basic emotions; NRC-VAD per-family means are a
# documented alternative (Mohammad 2018) and a stated further-work item.
CEN = {"joy": (0.8, 0.6), "sadness": (-0.75, 0.3), "anger": (-0.7, 0.8), "fear": (-0.65, 0.75),
       "surprise": (0.3, 0.8), "disgust": (-0.7, 0.6), "neutral": (0.0, 0.3)}
POS, NEG = {"joy"}, {"sadness", "anger", "fear", "disgust"}
# GoEmotions 28 labels -> 7 Ekman families (the grouping proposed with the dataset; Demszky et al. 2020)
G2F = {**dict.fromkeys(["admiration","amusement","approval","caring","desire","excitement","gratitude","joy","love","optimism","pride","relief"], "joy"),
       **dict.fromkeys(["disappointment","embarrassment","grief","remorse","sadness"], "sadness"),
       **dict.fromkeys(["anger","annoyance","disapproval"], "anger"),
       **dict.fromkeys(["fear","nervousness"], "fear"),
       **dict.fromkeys(["surprise","realization","confusion","curiosity"], "surprise"),
       "disgust": "disgust", "neutral": "neutral"}
# vocabulary of readable facial-expression answers (a documented word list, not per-image tuning)
EXPRESSION_WORDS = {"smile", "smiling", "happy", "sad", "angry", "serious", "surprised", "surprise",
                    "calm", "excited", "crying", "laughing", "frowning", "scared", "shocked", "worried",
                    "concentration", "concentrating", "grin", "grinning", "neutral",
                    "confused", "determined", "pensive", "sleepy", "sleeping"}
NUMWORDS = {"no": 0, "none": 0, "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "several": 3, "many": 4, "crowd": 5, "group": 3, "lots": 4}

# ---- splits ---------------------------------------------------------------------------------
def sign(l): return "+" if l in POS else "-" if l in NEG else "0"

def n_people(ans):
    """Integer read of the describer's 'How many people are there?' answer."""
    a = (ans or "").lower().strip()
    m = re.search(r"\d+", a)
    if m: return int(m.group())
    for w, n in NUMWORDS.items():
        if re.search(rf"\b{w}\b", a): return n   # word-boundary (avoids 'no' inside 'unknown')
    return 1 if a else 0                          # a non-empty non-numeric answer implies a subject present

def is_face(vqa):
    """Face-classified = the describer reports >=1 person AND a readable expression word.
    Token-intersection match so multi-word answers ("man is smiling") count."""
    words = set(re.findall(r"[a-z]+", vqa.get("expression", "").lower()))
    return n_people(vqa.get("people", "")) >= 1 and bool(words & EXPRESSION_WORDS)

# ---- the four similarity measures -----------------------------------------------------------
def va_point(t3):
    """Score-weighted centroid of a top-3 list [(family, score), ...] in valence–arousal space."""
    tot = sum(s for _, s in t3) or 1.0
    return (sum(CEN[l][0]*s for l, s in t3)/tot, sum(CEN[l][1]*s for l, s in t3)/tot)

def va_sim(p, q):
    """1 - normalised Euclidean distance between two VA points (valence rescaled to [0,1]).
    Its floor over the centroids is 0.412 (joy vs sadness): randomly paired records already
    average ~0.76, which is why every value is read against a null."""
    return 1 - math.hypot(((p[0]+1)/2)-((q[0]+1)/2), p[1]-q[1]) / math.sqrt(2)

def soft(a, b):
    """Top-3 soft overlap: normalise EACH side's top-3 to sum 1 first, so prompt (multi-label)
    and image (softmax) scales are comparable; then sum the per-label minima — a proper
    distribution overlap in [0, 1], equal to 1 only when the two distributions coincide."""
    sa = sum(s for _, s in a) or 1.0; sb = sum(s for _, s in b) or 1.0
    da = {l: s/sa for l, s in a}; db = {l: s/sb for l, s in b}
    return sum(min(da.get(l, 0), db.get(l, 0)) for l in set(da) | set(db))

def metrics(pairs):
    """The four agreement measures over a list of (prompt_top3, image_top3) pairs.
    vsign is computed over records whose prompt family has a valence sign (surprise and
    neutral have none) — report that denominator alongside n."""
    vsd = [1 for p, i in pairs if sign(p[0][0]) != "0"]
    return {"va": st.mean(va_sim(va_point(p), va_point(i)) for p, i in pairs),
            "vsign": sum(1 for p, i in pairs if sign(p[0][0]) != "0" and sign(p[0][0]) == sign(i[0][0]))/max(1, len(vsd)),
            "family": sum(1 for p, i in pairs if p[0][0] == i[0][0])/len(pairs),
            "overlap": st.mean(soft(p, i) for p, i in pairs)}

def with_null(pairs, N=300):
    """Observed metrics, plus the mean and sd of each metric over N random re-pairings of the
    image readings (the random-pairing null). Uses the module-level `random` state."""
    if len(pairs) < 5: return metrics(pairs), None, None
    t = metrics(pairs); ps = [p for p, _ in pairs]; im = [i for _, i in pairs]
    nl = {k: [] for k in t}
    for _ in range(N):
        sh = im[:]; random.shuffle(sh)
        for k, v in metrics(list(zip(ps, sh))).items(): nl[k].append(v)
    return t, {k: st.mean(v) for k, v in nl.items()}, {k: (st.pstdev(v) or 1e-9) for k, v in nl.items()}

def degenerate(ns):
    """Metrics whose random-pairing null has zero spread: permutation cannot change the score, so
    a z would be meaningless. This happens when every prompt in the subset shares one top-1 label
    (family) or one valence sign (sign) — detected from the null itself, not by hand."""
    return {k for k, sd in ns.items() if sd <= 1e-9}

def va_floor():
    """The smallest value va_sim can take between two family centroids."""
    pts = [CEN[f] for f in FAMILIES]
    return min(va_sim(p, q) for p in pts for q in pts)
