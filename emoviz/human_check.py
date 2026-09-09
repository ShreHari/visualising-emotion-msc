#!/usr/bin/env python3
"""
human_check.py — a single-coder reliability check for the image side of the pipeline.

Nothing in the pipeline has been compared with a human looking at the drawings: the
describer's people count, its facial-expression answer, and the emotion the reader infers
from the description are all machine-on-machine. This tool draws a fixed, stratified sample
of drawings, lays them out as numbered contact sheets WITHOUT any model output, and — once
the coder has filled in the CSV — scores the describer and the reader against the human
codes with Wilson 95% confidence intervals. It also re-runs the headline face/scene contrast
on the human-coded split, which breaks the circularity of the machine-defined split for
that sample.

The coder never sees the prompt, the description or the model's emotions while coding.

Usage
  .venv/bin/python human_check.py sample            # -> outputs/human_check/sheet_*.png + labels.csv
  # ... open the sheets, fill the four code columns in labels.csv (see the header) ...
  .venv/bin/python human_check.py score             # -> outputs/human_check/human_check.json

Codes (one row per drawing; leave a cell blank only if you truly cannot decide):
  person     y / n      is at least one person or face drawn?
  face       y / n      is there a face whose expression you can read? (n if no person)
  valence    + / - / 0  the feeling the drawing gives you: positive, negative, neither
  family     joy / sadness / anger / fear / surprise / disgust / neutral
"""
from __future__ import annotations
import argparse, csv, json, math, os, random, re, statistics as st
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "outputs")
HC = os.path.join(OUT, "human_check")
PRETEST_MAX_ID = 13
FAMILIES = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
POS, NEG = {"joy"}, {"sadness", "anger", "fear", "disgust"}

# --- copied verbatim from analysis_final.py (which executes on import, so cannot be imported) ---
EXPRESSION_WORDS = {"smile", "smiling", "happy", "sad", "angry", "serious", "surprised", "surprise",
                    "calm", "excited", "crying", "laughing", "frowning", "scared", "shocked", "worried",
                    "concentration", "concentrating", "grin", "grinning", "neutral",
                    "confused", "determined", "pensive", "sleepy", "sleeping"}
NUMWORDS = {"no": 0, "none": 0, "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "several": 3, "many": 4, "crowd": 5, "group": 3, "lots": 4}
VAGUE = {"several", "many", "crowd", "group", "lots"}

def sign(l): return "+" if l in POS else "-" if l in NEG else "0"

def n_people(ans):
    a = (ans or "").lower().strip()
    m = re.search(r"\d+", a)
    if m: return int(m.group())
    for w, n in NUMWORDS.items():
        if re.search(rf"\b{w}\b", a): return n
    return 1 if a else 0

def is_face(vqa):
    words = set(re.findall(r"[a-z]+", vqa.get("expression", "").lower()))
    return n_people(vqa.get("people", "")) >= 1 and bool(words & EXPRESSION_WORDS)
# --- end copy ---

def wilson(k, n, z=1.96):
    """Wilson score interval for a binomial proportion (Wilson 1927)."""
    if n == 0: return (float("nan"), float("nan"), float("nan"))
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (p, c - h, c + h)

def load_records():
    rows = [json.loads(l) for l in open(os.path.join(OUT, "describe_extract.jsonl"), encoding="utf-8")]
    rows = [r for r in rows if r["id"] > PRETEST_MAX_ID]
    goe = {int(k): v for k, v in json.load(open(os.path.join(OUT, "prompt_emotions_goe.json"))).items()}
    for r in rows:
        r["pe"] = goe[r["id"]]; r["ie"] = r["image_emotions"]
        r["prompt_top"] = r["pe"][0][0]; r["image_top"] = r["ie"][0][0]
        r["emotional"] = r["prompt_top"] != "neutral"
        r["face"] = is_face(r.get("vqa", {}))
        r["n_people"] = n_people(r.get("vqa", {}).get("people", ""))
    return rows

def stratum(r):
    """Three describer-output strata, so every kind of describer answer is checked."""
    people_ans = (r["vqa"].get("people") or "").lower().strip()
    vague = (not re.search(r"\d", people_ans)) and (people_ans == "" or any(w in people_ans for w in VAGUE)
                                                   or people_ans not in NUMWORDS)
    if r["face"] and not vague: return "face"
    if (not r["face"]) and r["n_people"] == 0 and not vague: return "scene"
    return "ambiguous"   # vague / word-only people answers, or a person reported without a readable expression

# ----------------------------------------------------------------------------- sample
def cmd_sample(a):
    os.makedirs(HC, exist_ok=True)
    from PIL import Image, ImageDraw, ImageFont
    rows = load_records()
    rng = random.Random(a.seed)
    by = defaultdict(list)
    for r in rows: by[stratum(r)].append(r)
    print("stratum sizes in the analysed set:", {k: len(v) for k, v in by.items()})
    want = {"face": a.n // 3, "scene": a.n // 3, "ambiguous": a.n - 2 * (a.n // 3)}
    chosen = []
    short = 0
    for k, n in want.items():
        pool = sorted(by[k], key=lambda r: r["id"]); rng.shuffle(pool)
        take = pool[:n]; short += n - len(take); chosen += take
    if short:   # an under-sized stratum is topped up from face and scene equally
        for k in ("face", "scene"):
            pool = [r for r in by[k] if r not in chosen]; rng.shuffle(pool)
            chosen += pool[:short // 2 + (short % 2 if k == "face" else 0)]
    rng.shuffle(chosen)                      # coding order is random, not by stratum
    sample = [{"idx": i + 1, "id": r["id"], "image_path": r["image_path"], "stratum": stratum(r)}
              for i, r in enumerate(chosen)]
    json.dump(sample, open(os.path.join(HC, "sample.json"), "w"), indent=1)
    # labels CSV: only idx and id are visible to the coder — no prompt, no model output
    with open(os.path.join(HC, "labels.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["idx", "id", "person(y/n)", "face(y/n)", "valence(+/-/0)", "family(joy/sadness/anger/fear/surprise/disgust/neutral)"])
        for s in sample: w.writerow([s["idx"], s["id"], "", "", "", ""])
    # contact sheets: 20 per sheet, tile 300 px, index printed large in the corner
    per, cols, tile, pad = 20, 5, 300, 12
    try: font = ImageFont.load_default(size=34)
    except TypeError: font = ImageFont.load_default()
    for s0 in range(0, len(sample), per):
        chunk = sample[s0:s0 + per]; rows_n = math.ceil(len(chunk) / cols)
        sheet = Image.new("RGB", (cols * (tile + pad) + pad, rows_n * (tile + pad + 40) + pad), "white")
        d = ImageDraw.Draw(sheet)
        for j, s in enumerate(chunk):
            im = Image.open(s["image_path"]).convert("RGB"); im.thumbnail((tile, tile))
            x = pad + (j % cols) * (tile + pad); y = pad + (j // cols) * (tile + pad + 40)
            sheet.paste(im, (x + (tile - im.width) // 2, y + 40 + (tile - im.height) // 2))
            d.rectangle([x, y, x + tile, y + 36], fill="#1d2227")
            d.text((x + 10, y + 2), f"#{s['idx']}", fill="white", font=font)
        n = s0 // per + 1
        sheet.save(os.path.join(HC, f"sheet_{n:02d}.png"))
    print(f"sample of {len(sample)} drawings -> {HC}/sheet_01..{n:02d}.png, labels.csv, sample.json")
    print("coder instructions are in the module docstring; code from the sheets only.")

# ----------------------------------------------------------------------------- score
def agree_rate(pairs):
    k = sum(1 for a, b in pairs if a == b); return wilson(k, len(pairs)) + (k, len(pairs))

def kappa(pairs, labels):
    n = len(pairs)
    if n == 0: return float("nan")
    po = sum(1 for a, b in pairs if a == b) / n
    ca = Counter(a for a, _ in pairs); cb = Counter(b for _, b in pairs)
    pe = sum(ca[l] * cb[l] for l in labels) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")

def two_prop_z(k1, n1, k2, n2):
    p = (k1 + k2) / (n1 + n2); se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2)) or 1e-9
    return (k1 / n1 - k2 / n2) / se

def cmd_score(a):
    rows = {r["id"]: r for r in load_records()}
    labels = []
    with open(a.labels, newline="") as f:
        rd = csv.reader(f); hdr = next(rd)
        for row in rd:
            if len(row) < 6 or not row[0].strip(): continue
            idx, rid, person, face, val, fam = [c.strip().lower() for c in row[:6]]
            if not (person and face and val and fam): continue
            if fam not in FAMILIES or val not in {"+", "-", "0"} or person not in "yn" or face not in "yn":
                raise SystemExit(f"row idx={idx}: bad code {row}")
            labels.append({"id": int(rid), "person": person == "y", "face": face == "y", "val": val, "fam": fam})
    if not labels: raise SystemExit("no completed rows in labels.csv")
    out = {"n_coded": len(labels), "coder": "single coder (the author), blind to prompt and model output",
           "ci": "Wilson 95%"}
    R = [(l, rows[l["id"]]) for l in labels]

    # 1. describer: people count and face rule vs the human
    pp = [(r["n_people"] >= 1, l["person"]) for l, r in R]
    tp = sum(1 for m, h in pp if m and h); fp = sum(1 for m, h in pp if m and not h)
    fn = sum(1 for m, h in pp if not m and h); tn = sum(1 for m, h in pp if not m and not h)
    out["describer_people"] = {"accuracy": wilson(tp + tn, len(pp)), "precision": wilson(tp, tp + fp),
                               "recall": wilson(tp, tp + fn), "tp": tp, "fp": fp, "fn": fn, "tn": tn}
    ff = [(r["face"], l["face"]) for l, r in R]
    tp = sum(1 for m, h in ff if m and h); fp = sum(1 for m, h in ff if m and not h)
    fn = sum(1 for m, h in ff if not m and h); tn = sum(1 for m, h in ff if not m and not h)
    out["face_rule"] = {"accuracy": wilson(tp + tn, len(ff)), "precision": wilson(tp, tp + fp),
                        "recall": wilson(tp, tp + fn), "tp": tp, "fp": fp, "fn": fn, "tn": tn}
    # 2. the 'smiling' answer: how often is there a readable positive face behind it?
    sm = [(l, r) for l, r in R if set(re.findall(r"[a-z]+", r["vqa"].get("expression", "").lower())) & {"smile", "smiling", "happy"}]
    out["smiling_answer"] = {"n": len(sm),
                             "human_face_and_positive": wilson(sum(1 for l, r in sm if l["face"] and l["val"] == "+"), len(sm)),
                             "human_no_person": wilson(sum(1 for l, r in sm if not l["person"]), len(sm))}
    # 3. the image reader vs the human (valence sign on non-neutral human codes; family; kappa)
    vs = [(sign(r["image_top"]), l["val"]) for l, r in R if l["val"] != "0"]
    out["image_reader_vs_human"] = {
        "valence_sign": agree_rate(vs),
        "family": agree_rate([(r["image_top"], l["fam"]) for l, r in R]),
        "family_kappa": kappa([(r["image_top"], l["fam"]) for l, r in R], FAMILIES),
        "by_human_face": {
            "readable_face": agree_rate([(sign(r["image_top"]), l["val"]) for l, r in R if l["val"] != "0" and l["face"]]),
            "no_readable_face": agree_rate([(sign(r["image_top"]), l["val"]) for l, r in R if l["val"] != "0" and not l["face"]])}}
    # 4. the headline, human-anchored: prompt reader vs the HUMAN's reading of the drawing,
    #    split by the HUMAN's face code (emotional prompts only, as in the main analysis)
    def ph(sub): return [(sign(r["prompt_top"]), l["val"]) for l, r in sub if r["emotional"] and sign(r["prompt_top"]) != "0" and l["val"] != "0"]
    hf = ph([(l, r) for l, r in R if l["face"]]); hs = ph([(l, r) for l, r in R if not l["face"]])
    af, as_ = agree_rate(hf), agree_rate(hs)
    out["prompt_vs_human_by_human_face"] = {
        "readable_face": af, "no_readable_face": as_,
        "difference_pp": (af[0] - as_[0]) * 100 if hf and hs else None,
        "two_proportion_z": two_prop_z(af[3], af[4], as_[3], as_[4]) if hf and hs else None,
        "note": "valence-sign agreement between the prompt reader and the human's valence code; the split is the human's face code, not the describer's"}
    # 5. the same contrast on the machine split, on this sample only, for direct comparison
    mf = ph([(l, r) for l, r in R if r["face"]]); ms = ph([(l, r) for l, r in R if not r["face"]])
    out["prompt_vs_human_by_machine_face"] = {"face_classified": agree_rate(mf), "scene_classified": agree_rate(ms)}
    out["stratum_counts"] = dict(Counter(stratum(r) for _, r in R))
    json.dump(out, open(os.path.join(HC, "human_check.json"), "w"), indent=1)

    def pct(t): return f"{t[0]*100:5.1f}% [{t[1]*100:.1f}, {t[2]*100:.1f}]" + (f"  ({t[3]}/{t[4]})" if len(t) > 3 else "")
    print(f"=== HUMAN CHECK — {len(labels)} drawings coded by one coder, blind ===")
    print(f"describer people-count  accuracy {pct(out['describer_people']['accuracy'])}  precision {pct(out['describer_people']['precision'])}  recall {pct(out['describer_people']['recall'])}")
    print(f"face rule               accuracy {pct(out['face_rule']['accuracy'])}  precision {pct(out['face_rule']['precision'])}  recall {pct(out['face_rule']['recall'])}")
    print(f"'smiling' answers (n={len(sm)}): readable positive face behind it {pct(out['smiling_answer']['human_face_and_positive'])}; no person drawn {pct(out['smiling_answer']['human_no_person'])}")
    ir = out["image_reader_vs_human"]
    print(f"image reader vs human   valence-sign {pct(ir['valence_sign'])}  family {pct(ir['family'])}  kappa {ir['family_kappa']:.2f}")
    print(f"   by human face code   readable {pct(ir['by_human_face']['readable_face'])}  none {pct(ir['by_human_face']['no_readable_face'])}")
    pv = out["prompt_vs_human_by_human_face"]
    print(f"prompt reader vs HUMAN  readable face {pct(pv['readable_face'])}  no readable face {pct(pv['no_readable_face'])}"
          + (f"  diff {pv['difference_pp']:+.1f} pp, z {pv['two_proportion_z']:+.1f}" if pv["difference_pp"] is not None else ""))
    print(f"saved {HC}/human_check.json")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("sample"); s.add_argument("--n", type=int, default=120); s.add_argument("--seed", type=int, default=7)
    s.set_defaults(fn=cmd_sample)
    c = sp.add_parser("score"); c.add_argument("--labels", default=os.path.join(HC, "labels.csv"))
    c.set_defaults(fn=cmd_score)
    a = ap.parse_args(); a.fn(a)
