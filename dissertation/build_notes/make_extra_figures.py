#!/usr/bin/env python3
"""
make_extra_figures.py: four additional figures for dissertation/figures/, generated from the
dataset, the recovered timestamps and the cached pipeline output. Palette and typography match
emoviz/make_figures.py so the figures read as one set.

  fig_timeline            records per day from the C2PA signing timestamps (pre-tests apart)
  fig_prompt_length       histogram of prompt word counts, analysed records
  fig_happy_grid          twelve of the drawings of the prompt "happy", image-reader family under each
  fig_no_person_expression four scene-classified drawings where the describer reported no person
                          yet named an expression, with its five answers

Run from anywhere:  emoviz/.venv/bin/python dissertation/build_notes/make_extra_figures.py
"""
import json, os, sys, collections, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, "emoviz"))
from emoviz import data as D                     # noqa: E402
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                   # noqa: E402
from PIL import Image, ImageDraw, ImageFont      # noqa: E402

FIG = os.path.join(PROJ, "dissertation", "figures")
os.makedirs(FIG, exist_ok=True)
INK, SOFT, BLUE, GOLD, GREY, GREEN = "#1d2227", "#5a636c", "#31708f", "#b07d2b", "#a8aeb6", "#3c7a4e"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 11, "axes.edgecolor": SOFT,
                     "axes.labelcolor": INK, "text.color": INK, "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
SENSITIVE = {216, 300, 302, 532, 750, 751, 858, 982, 1020}

def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"), bbox_inches="tight", facecolor="white")
    plt.close(fig); print("  saved", name)

recs = D.load(with_timestamps=True, drop_pretest=False)
byid = {r.id: r for r in recs}
pipe = {}
for line in open(os.path.join(PROJ, "emoviz", "outputs", "describe_extract.jsonl")):
    r = json.loads(line); pipe[int(r["id"])] = r

# ------------------------------------------------------------------ fig_timeline
def fig_timeline():
    days = collections.Counter(); pre = collections.Counter()
    for r in recs:
        if not r.timestamp: continue
        d = datetime.date.fromisoformat(r.timestamp[:10])
        (pre if r.is_pretest else days)[d] += 1
    fest = [d for d in sorted(days) if datetime.date(2024, 9, 19) <= d <= datetime.date(2024, 9, 29)]
    late = {d: n for d, n in days.items() if d > datetime.date(2024, 9, 29)}
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    xs = list(range(len(fest)))
    ax.bar(xs, [days[d] for d in fest], 0.7, color=BLUE, label="Festival days (19 to 29 September 2024)")
    for x, d in zip(xs, fest):
        ax.annotate(str(days[d]), (x, days[d] + 3), ha="center", fontsize=9)
    # pre-tests as a single grey bar to the left, later records to the right
    ax.bar([-1.6], [sum(pre.values())], 0.7, color=GREY, label=f"Pre-festival developer tests, 26 Aug to 18 Sep ({sum(pre.values())}, excluded)")
    ax.annotate(str(sum(pre.values())), (-1.6, sum(pre.values()) + 3), ha="center", fontsize=9)
    if late:
        ax.bar([len(fest) + 0.6], [sum(late.values())], 0.7, color=GREY, hatch="//", edgecolor=SOFT,
               label=f"After the festival, 20 Oct ({sum(late.values())}, kept)")
        ax.annotate(str(sum(late.values())), (len(fest) + 0.6, sum(late.values()) + 3), ha="center", fontsize=9)
    ax.set_xticks([-1.6] + xs + ([len(fest) + 0.6] if late else []))
    ax.set_xticklabels(["tests"] + [d.strftime("%-d Sep") for d in fest] + (["20 Oct"] if late else []), fontsize=8.5, rotation=30, ha="right")
    ax.set_ylabel("Records generated"); ax.set_ylim(0, max(days.values()) * 1.25)
    ax.set_title("Records per day, from the signing timestamps recovered inside each PNG", fontsize=11, pad=10)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    save(fig, "fig_timeline")

# ------------------------------------------------------------------ fig_prompt_length
def fig_prompt_length():
    wc = [r.word_count for r in recs if not r.is_pretest]
    cap = 20
    counts = collections.Counter(min(w, cap) for w in wc)
    xs = list(range(1, cap + 1))
    fig, ax = plt.subplots(figsize=(8.2, 3.4))
    ax.bar(xs, [counts.get(x, 0) for x in xs], 0.75, color=BLUE)
    for x in xs[:6]:
        ax.annotate(str(counts.get(x, 0)), (x, counts.get(x, 0) + 4), ha="center", fontsize=9)
    ax.set_xticks(xs); ax.set_xticklabels([str(x) if x < cap else f"{cap}+" for x in xs])
    ax.set_xlabel("Words in the prompt"); ax.set_ylabel("Records")
    import statistics
    ax.set_title(f"Prompt length over the {len(wc):,} analysed records (median {int(statistics.median(wc))} words; "
                 f"{counts.get(1,0)} single-word prompts; longest {max(wc)} words)", fontsize=10.5, pad=10)
    save(fig, "fig_prompt_length")

# ------------------------------------------------------------------ image grids (PIL)
def _font(size):
    for p in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial.ttf"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except OSError: pass
    return ImageFont.load_default()

def grid(ids, captions, name, cols, tile=300, cap_h=None, title=None):
    cap_h = cap_h or (48 if all(len(c) <= 2 for c in captions) else 26 * max(len(c) for c in captions) + 10)
    rows = (len(ids) + cols - 1) // cols
    pad = 16; th = 44 if title else 0
    W = cols * tile + (cols + 1) * pad; H = th + rows * (tile + cap_h) + (rows + 1) * pad
    im = Image.new("RGB", (W, H), "white"); dr = ImageDraw.Draw(im)
    f_big, f_small, f_title = _font(20), _font(17), _font(22)
    if title: dr.text((pad, 12), title, fill=INK, font=f_title)
    for k, (i, cap) in enumerate(zip(ids, captions)):
        r, c = divmod(k, cols)
        x = pad + c * (tile + pad); y = th + pad + r * (tile + cap_h + pad)
        img = Image.open(byid[i].image_path).convert("RGB").resize((tile, tile), Image.LANCZOS)
        im.paste(img, (x, y)); dr.rectangle([x, y, x + tile, y + tile], outline="#d9d4c8", width=1)
        yy = y + tile + 6
        for j, line in enumerate(cap):
            dr.text((x, yy), line, fill=INK if j == 0 else SOFT, font=f_big if j == 0 else f_small); yy += 24
    im.save(os.path.join(FIG, f"{name}.png"), dpi=(150, 150)); print("  saved", name)

def fig_happy_grid():
    ids = [r.id for r in recs if not r.is_pretest and r.text.strip().lower() == "happy" and r.id not in SENSITIVE][:12]
    caps = [[f"#{i}  read as {pipe[i]['image_top1']}", f"describer: {pipe[i]['vqa']['expression']}, people {pipe[i]['vqa']['people']}"] for i in ids]
    grid(ids, caps, "fig_happy_grid", cols=4, tile=260, cap_h=58,
         title='Twelve of the 42 drawings made from the single word "happy", with the image reader\'s top family')

def fig_no_person_expression():
    want = [21, 258, 242]
    # a fourth: a no-person record whose scene is plainly face-free, with a smiling answer
    FACEFREE = ("mountain", "landscape", "city", "tree", "flower", "building", "house", "car", "sky", "ocean",
                "beach", "forest", "book", "coffee", "cup", "road", "bridge", "plant", "garden", "river", "lake",
                "sun", "cloud", "boat", "train", "bicycle", "food", "cake")
    for i in sorted(pipe):
        v = pipe[i]["vqa"]
        if i > 13 and i not in SENSITIVE and i not in want and "[name]" not in byid[i].text \
           and v["people"] in ("0", "none") and v["expression"] in ("smiling", "smile", "happy") \
           and any(k in v["scene"] for k in FACEFREE) and len(byid[i].text.split()) <= 4:
            want.append(i); break
    caps = []
    for i in want:
        v = pipe[i]["vqa"]; t = byid[i].text.strip()
        short = t if len(t) <= 24 else t[:22] + "..."
        caps.append([f'#{i}  "{short}"', f"people: {v['people']}  scene: {v['scene'][:18]}",
                     f"expression: {v['expression']}",
                     f"image reader: {pipe[i]['image_top1']}"])
    grid(want, caps, "fig_no_person_expression", cols=4, tile=300, cap_h=108,
         title="Scene-classified drawings: the describer reports no person, then names a facial expression anyway")

for f in (fig_timeline, fig_prompt_length, fig_happy_grid, fig_no_person_expression):
    f()
print("done ->", FIG)
