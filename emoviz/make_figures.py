#!/usr/bin/env python3
"""
make_figures.py — publication-quality figures for the technical report (and reusable in the
dissertation). All numbers come from the verified analyses (RESULTS_final.md /
analysis_final.py, similarity_v2.py, data_audit_consistency.py). Matplotlib only.
Outputs PDF (vector, for LaTeX) + PNG (for slides) into outputs/figures/.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "outputs", "figures")
os.makedirs(FIG, exist_ok=True)

# palette — restrained, print-safe
INK   = "#1d2227"
SOFT  = "#5a636c"
BLUE  = "#31708f"   # primary
GOLD  = "#b07d2b"   # secondary
GREY  = "#a8aeb6"   # null / reference
GREEN = "#3c7a4e"

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "axes.edgecolor": SOFT, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": SOFT, "ytick.color": SOFT,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150,
})

def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"), bbox_inches="tight",
                    facecolor="white")
    plt.close(fig)
    print(f"  saved {name}.pdf/.png")

# ---------------------------------------------------------------- fig 1: face vs scene
def fig_face_scene():
    metrics = ["Valence-sign\nagreement", "Emotion-family\nagreement", "Top-3 soft\noverlap"]
    face  = [74, 62, 53]
    scene = [43, 36, 45]
    null_face  = [53, 46, 40]   # exact null means (recomputed after audit fixes)
    null_scene = [30, 26, 38]
    x = range(len(metrics)); w = 0.35
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    b1 = ax.bar([i - w/2 for i in x], face, w, color=BLUE, label="Face images (n=402)")
    b2 = ax.bar([i + w/2 for i in x], scene, w, color=GOLD, label="Scene images (n=205)")
    # null markers
    for i in x:
        ax.plot([i - w, i], [null_face[i]]*2, color=INK, lw=1.4, ls=":")
        ax.plot([i, i + w], [null_scene[i]]*2, color=INK, lw=1.4, ls=":")
    ax.plot([], [], color=INK, lw=1.4, ls=":", label="Random-pairing null")
    for b in (*b1, *b2):
        ax.annotate(f"{b.get_height():.0f}%", (b.get_x() + b.get_width()/2, b.get_height() + 1.2),
                    ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(list(x)); ax.set_xticklabels(metrics)
    ax.set_ylabel("Agreement with prompt emotion (%)")
    ax.set_ylim(0, 85)
    ax.set_title("Drawings with a readable face convey the prompt's emotion far better than scenes",
                 fontsize=12, pad=12)
    ax.legend(frameon=False, loc="upper right")
    save(fig, "fig1_face_vs_scene")

# ---------------------------------------------------------------- fig 2: old vs new method
def fig_old_new():
    metrics = ["Emotion-family\nagreement", "Top-3 soft\noverlap", "Valence-Arousal\nsimilarity"]
    new = [49.3, 48.6, 83.7]
    old = [25.3, 22.8, 74.2]
    y = range(len(metrics)); h = 0.34
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.barh([i + h/2 for i in y], new, h, color=GREEN, label="New: describe → extract")
    ax.barh([i - h/2 for i in y], old, h, color=GREY, label="Old: direct CLIP")
    for i in y:
        ax.annotate(f"{new[i]:.0f}%", (new[i] + 1, i + h/2), va="center", fontweight="bold", color=GREEN)
        ax.annotate(f"{old[i]:.0f}%", (old[i] + 1, i - h/2), va="center", color=SOFT)
    ax.set_yticks(list(y)); ax.set_yticklabels(metrics)
    ax.set_xlabel("Alignment with prompt emotion (%)  ·  same 608 records")
    ax.set_xlim(0, 100)
    ax.set_title("The describe→extract method reads image emotion far better than direct CLIP",
                 fontsize=12, pad=12)
    ax.legend(frameon=False, loc="lower right")
    save(fig, "fig2_method_comparison")

# ---------------------------------------------------------------- fig 3: validity + significance
def fig_validity():
    groups = ["Emotional prompts\n(n=607)", "Non-emotional prompts\n(n=405)"]
    z = [12, 0.3]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    bars = ax.bar(groups, z, 0.5, color=[BLUE, GREY])
    ax.axhline(2, color=GOLD, lw=1.4, ls="--")
    ax.annotate("significance threshold (z≈2)", (0.52, 2.35), fontsize=9.5, color=GOLD)
    for b, v in zip(bars, z):
        ax.annotate(f"z = {v:g}", (b.get_x() + b.get_width()/2, v + 0.35),
                    ha="center", fontweight="bold")
    ax.set_ylabel("Alignment vs random pairing (z-score)")
    ax.set_ylim(0, 14.5)
    ax.set_title("Validity check: alignment appears only where there is a feeling to convey",
                 fontsize=12, pad=12)
    save(fig, "fig3_validity_check")

# ---------------------------------------------------------------- fig 4: consistency
def fig_consistency():
    # 'happy' x42 breakdown + overall consistency
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
    labels = ["joy", "neutral", "surprise"]; counts = [34, 7, 1]
    colors = [BLUE, GREY, GOLD]
    b = ax1.barh(labels[::-1], counts[::-1], 0.55, color=colors[::-1])
    for bb, c in zip(b, counts[::-1]):
        ax1.annotate(str(c), (c + 0.6, bb.get_y() + bb.get_height()/2), va="center", fontweight="bold")
    ax1.set_xlim(0, 40)
    ax1.set_title('The prompt "happy", drawn 42 times', fontsize=11.5)
    ax1.set_xlabel("Image emotion across the 42 drawings")

    cats = ["Same exact\nemotion", "Same\nvalence", "Fully\nconsistent"]
    vals = [69, 74, 32]  # 28/87 = 32%
    b2 = ax2.bar(cats, vals, 0.48, color=[BLUE, GREEN, GOLD])
    for bb, v in zip(b2, vals):
        ax2.annotate(f"{v}%", (bb.get_x() + bb.get_width()/2, v + 1.5), ha="center", fontweight="bold")
    ax2.set_ylim(0, 90)
    ax2.tick_params(axis="x", labelsize=9.5)
    ax2.set_title("Per-prompt agreement (87 repeated prompts)", fontsize=11)
    ax2.set_ylabel("Agreement (%)")
    fig.suptitle("Generative consistency: the same prompt yields a different feeling ≈⅓ of the time",
                 fontsize=12, y=1.04)
    save(fig, "fig4_consistency")

# ---------------------------------------------------------------- fig 5: dataset composition
def fig_dataset():
    fig, ax = plt.subplots(figsize=(7.4, 2.6))
    seg = [("Emotional · face", 402, BLUE), ("Emotional · scene", 205, "#6b9ab0"),
           ("Non-emotional", 405, GREY), ("Pre-test (excluded)", 13, "#d9d4c8")]
    left = 0
    for name, v, c in seg:
        ax.barh([0], [v], left=left, color=c, height=0.5)
        if v > 60:
            ax.annotate(f"{name}\n{v}", (left + v/2, 0), ha="center", va="center",
                        fontsize=9.5, color="white" if c != "#d9d4c8" else INK, fontweight="bold")
        left += v
    ax.annotate("Pre-test: 13", (left - 6, 0.42), ha="right", fontsize=8.5, color=SOFT)
    ax.set_xlim(0, 1025); ax.set_yticks([])
    ax.set_xlabel("1,025 text–image pairs (100% processed, 0 failures)")
    ax.set_title("Dataset composition and how every record is used", fontsize=12, pad=10)
    for s in ("left",): ax.spines[s].set_visible(False)
    save(fig, "fig5_dataset")

for f in (fig_face_scene, fig_old_new, fig_validity, fig_consistency, fig_dataset):
    f()
print("all figures done ->", FIG)
