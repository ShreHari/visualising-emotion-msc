#!/usr/bin/env python3
"""
make_figures.py — report figures, generated ENTIRELY from the result files the analysis scripts
write (no number is typed here):

  outputs/analysis_final.json      analysis_final.py          observed / null / z per subset and metric
  outputs/inference.json           inference.py               clustered-bootstrap CIs, kappa, confusion
  outputs/consistency.json         data_audit_consistency.py  repeated-prompt consistency + permutation null
  outputs/method_comparison.json   method_comparison.py       like-for-like image-reader comparison
  outputs/error_taxonomy.json      error_taxonomy.py          failure-mode tally
  outputs/ablation/summary.json    ablate_nli.py              description-template ablation (optional)

Titles are descriptive, not conclusory: every figure shows agreement between the prompt reader
and the image reader against its random-pairing null. Matplotlib only. PDF (vector) + PNG.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "outputs")
FIG = os.path.join(OUT, "figures"); os.makedirs(FIG, exist_ok=True)

def load(name, required=True):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        if required: raise SystemExit(f"missing {p} — run the analysis scripts first (see README)")
        return None
    return json.load(open(p))

AF = load("analysis_final.json"); INF = load("inference.json"); CONS = load("consistency.json")
MC = load("method_comparison.json"); ET = load("error_taxonomy.json", required=False)
AB = load(os.path.join("ablation", "summary.json"), required=False)

INK, SOFT, BLUE, GOLD, GREY, GREEN = "#1d2227", "#5a636c", "#31708f", "#b07d2b", "#a8aeb6", "#3c7a4e"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 11, "axes.edgecolor": SOFT,
                     "axes.labelcolor": INK, "text.color": INK, "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})

def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"), bbox_inches="tight", facecolor="white")
    plt.close(fig); print(f"  saved {name}.pdf/.png")

def pct(x): return 100 * x
S = AF["blocks"]["full"]["subsets"]
METRICS = [("vsign", "Valence-sign\nagreement"), ("family", "Emotion-family\nagreement"), ("overlap", "Top-3 soft\noverlap")]

# ------------------------------------------------------------------ fig 1: face vs scene (+ CIs)
def fig_face_scene():
    face, scene = S["face images"], S["scene images"]
    B = INF["bootstrap_ci95_clustered"]
    x = range(len(METRICS)); w = 0.35
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    for off, sub, key, col, lab in ((-w/2, face, "face", BLUE, "Face-classified"), (w/2, scene, "scene", GOLD, "Scene-classified")):
        vals = [pct(sub["metrics"][k]["obs"]) for k, _ in METRICS]
        ci = [B[key][k]["ci95"] for k, _ in METRICS]
        err = [[v - pct(c[0]) for v, c in zip(vals, ci)], [pct(c[1]) - v for v, c in zip(vals, ci)]]
        bars = ax.bar([i + off for i in x], vals, w, color=col, label=f"{lab} (n={sub['n']})", yerr=err,
                      error_kw={"ecolor": INK, "capsize": 3, "lw": 1})
        for i, (k, _) in enumerate(METRICS):
            nv = pct(sub["metrics"][k]["null"])
            ax.plot([i + off - w/2, i + off + w/2], [nv, nv], color=INK, lw=1.4, ls=":")
        for bar, v in zip(bars, vals):
            ax.annotate(f"{v:.0f}%", (bar.get_x() + bar.get_width()/2, 2), ha="center", fontsize=9.5, color="white", fontweight="bold")
    ax.plot([], [], color=INK, lw=1.4, ls=":", label="Random-pairing null (mean)")
    ax.set_xticks(list(x)); ax.set_xticklabels([l for _, l in METRICS])
    ax.set_ylabel("Agreement with the prompt reader (%)"); ax.set_ylim(0, 90)
    ax.set_title("Prompt-reader / image-reader agreement by describer-defined image class,\nemotional prompts, with clustered-bootstrap 95% CIs and the random-pairing null", fontsize=11, pad=10)
    ax.legend(frameon=False, loc="upper right", fontsize=9.5)
    save(fig, "fig1_face_vs_scene")

# ------------------------------------------------------------------ fig 2: image readers, like for like
def fig_method():
    L = MC["like_for_like"]; n = MC["headline"]["n_records_both_readers_cover"]
    keys = [("vsign", "Valence-sign\nagreement"), ("family", "Emotion-family\nagreement"), ("overlap", "Top-3 soft\noverlap"), ("va", "Valence–arousal\nsimilarity")]
    y = range(len(keys)); h = 0.34
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    for off, reader, col, lab in ((h/2, "describe_then_extract", GREEN, "Describe-then-extract (BLIP-VQA → NLI)"), (-h/2, "direct_clip", GREY, "Direct CLIP zero-shot")):
        vals = [pct(L[reader]["all_emotional"][k]["value"]) for k, _ in keys]
        nulls = [pct(L[reader]["all_emotional"][k]["null_mean"]) for k, _ in keys]
        ax.barh([i + off for i in y], vals, h, color=col, label=lab)
        for i, (v, nv) in enumerate(zip(vals, nulls)):
            ax.plot([nv, nv], [i + off - h/2, i + off + h/2], color=INK, lw=1.4, ls=":")
            ax.annotate(f"{v:.0f}%", (v + 1, i + off), va="center", fontsize=9.5, color=INK)
    ax.plot([], [], color=INK, lw=1.4, ls=":", label="Each reader's own random-pairing null")
    ax.set_yticks(list(y)); ax.set_yticklabels([l for _, l in keys])
    ax.set_xlabel(f"Agreement with the same prompt reader (GoEmotions), same {n} emotional records (%)"); ax.set_xlim(0, 100)
    d = MC["headline"]
    ax.set_title(f"Two image readers scored like for like. Family-agreement difference "
                 f"{d['family_agreement_difference_pp']:+.1f} pp, 95% CI [{d['family_clustered_bootstrap_95ci_pp'][0]:+.1f}, {d['family_clustered_bootstrap_95ci_pp'][1]:+.1f}]", fontsize=10.5, pad=10)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3, fontsize=8.5)
    save(fig, "fig2_method_comparison")

# ------------------------------------------------------------------ fig 3: z by prompt group
def fig_z_by_group():
    e, ne = S["ALL emotional"], S["non-emotional"]
    keys = [("va", "Valence–arousal"), ("overlap", "Top-3 overlap"), ("vsign", "Valence sign"), ("family", "Family")]
    x = range(len(keys)); w = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for off, sub, col, lab in ((-w/2, e, BLUE, f"Emotional prompts (n={e['n']})"), (w/2, ne, GREY, f"Prompts the text reader labels neutral (n={ne['n']})")):
        for i, (k, _) in enumerate(keys):
            m = sub["metrics"][k]
            if m["degenerate"]:
                ax.annotate("null\ndegenerate", (i + off, 0.4), ha="center", fontsize=8, color=SOFT)
            else:
                ax.bar([i + off], [m["z"]], w, color=col, label=lab if i == 0 else None)
                ax.annotate(f"{m['z']:+.1f}", (i + off, m["z"] + 0.3), ha="center", fontsize=9.5, fontweight="bold")
    ax.axhline(2, color=GOLD, lw=1.2, ls="--"); ax.annotate("z = 2", (len(keys) - 0.6, 2.3), fontsize=9, color=GOLD)
    ax.set_xticks(list(x)); ax.set_xticklabels([l for _, l in keys])
    ax.set_ylabel("Distance from the random-pairing null (z)"); ax.set_ylim(0, max(15, e["metrics"]["va"]["z"] + 2))
    ax.set_title("Agreement z-score by prompt group and metric\n(the specificity check: prompts without a readable feeling should sit at their null)", fontsize=11, pad=10)
    ax.legend(frameon=False, loc="upper right", fontsize=9.5)
    save(fig, "fig3_z_by_prompt_group")

# ------------------------------------------------------------------ fig 4: consistency vs permutation null
def fig_consistency():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.8), gridspec_kw={"width_ratios": [1, 1.15], "wspace": 0.35})
    big = CONS["largest_groups"][0]
    labels = list(big["image_top1"].keys()); counts = list(big["image_top1"].values())
    b = ax1.barh(labels[::-1], counts[::-1], 0.55, color=[BLUE, GREY, GOLD, GREEN][:len(labels)][::-1])
    for bb, cnt in zip(b, counts[::-1]):
        ax1.annotate(str(cnt), (cnt + 0.6, bb.get_y() + bb.get_height()/2), va="center", fontweight="bold")
    ax1.set_xlim(0, max(counts) * 1.2); ax1.set_title(f'The prompt "{big["text"]}", drawn {big["n"]} times', fontsize=11)
    ax1.set_xlabel("Image-reader family across the drawings")
    N = CONS["null"]; runs = CONS["runs"]
    cats = ["Same family\n(mean over groups)", "Same valence\n(mean over groups)", "Fully\nconsistent groups"]
    obs = [pct(CONS["mean_emotion_consistency"]), pct(CONS["mean_valence_consistency"]), 100 * CONS["fully_consistent_runs"] / runs]
    nul = [pct(N["mean_emotion_consistency"]["null_mean"]), pct(N["mean_valence_consistency"]["null_mean"]), 100 * N["fully_consistent_runs"]["null_mean"] / runs]
    zs = [N["mean_emotion_consistency"]["z"], N["mean_valence_consistency"]["z"], N["fully_consistent_runs"]["z"]]
    bars = ax2.bar(cats, obs, 0.5, color=[BLUE, GREEN, GOLD])
    for i, (bb, v, nv, z) in enumerate(zip(bars, obs, nul, zs)):
        ax2.plot([bb.get_x(), bb.get_x() + bb.get_width()], [nv, nv], color=INK, lw=1.4, ls=":")
        ax2.annotate(f"{v:.0f}%\n(z {z:+.1f})", (bb.get_x() + bb.get_width()/2, v + 1.5), ha="center", fontsize=9, fontweight="bold")
    ax2.plot([], [], color=INK, lw=1.4, ls=":", label=f"Permutation null ({N['draws']:,} draws)")
    ax2.set_ylim(0, 95); ax2.tick_params(axis="x", labelsize=8); ax2.set_xticks(range(3)); ax2.set_xticklabels(cats, fontsize=8); ax2.set_ylabel("Within-group agreement (%)")
    ax2.set_title(f"{runs} prompts drawn 2+ times ({CONS['pair_groups']} are pairs; floor 50%)", fontsize=10.5)
    ax2.legend(frameon=False, loc="upper right", fontsize=8.5)
    fig.suptitle("Repeated prompts: how often the image reader returns the same family within a group, against a permutation null", fontsize=11, y=1.03)
    save(fig, "fig4_consistency")

# ------------------------------------------------------------------ fig 5: dataset composition
def fig_dataset():
    F = AF["blocks"]["full"]; pre = CONS["pretest"]; total = CONS["total"]
    ef = S["face images"]["n"]; es = S["scene images"]["n"]
    fig, ax = plt.subplots(figsize=(7.6, 2.6))
    seg = [("Emotional\nface-classified", ef, BLUE), ("Emotional\nscene-classified", es, "#6b9ab0"),
           ("Labelled neutral\nby the text reader", F["non_emotional"], GREY), ("Pre-festival tests (excluded)", pre, "#d9d4c8")]
    left = 0
    for name, v, c in seg:
        ax.barh([0], [v], left=left, color=c, height=0.5)
        if v > 60:
            ax.annotate(f"{name}\n{v}", (left + v/2, 0), ha="center", va="center", fontsize=8, color="white", fontweight="bold")
        left += v
    ax.annotate(f"Pre-test: {pre}", (left - 6, 0.42), ha="right", fontsize=8.5, color=SOFT)
    ax.set_xlim(0, total); ax.set_yticks([])
    ax.set_xlabel(f"{total:,} prompt–drawing records processed without an unhandled error; {F['records']:,} analysed")
    ax.set_title("Dataset composition: every analysed record is in one prompt group and one image class", fontsize=11, pad=10)
    ax.spines["left"].set_visible(False)
    save(fig, "fig5_dataset")

# ------------------------------------------------------------------ fig 6: confusion matrix
def fig_confusion():
    K = INF["cohens_kappa_family_agreement"]["emotional"]
    M = K["confusion_7x7_prompt_rows_image_cols"]; fams = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
    rows = [i for i in range(7) if sum(M[i]) > 0]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    data = [[M[i][j] / (sum(M[i]) or 1) for j in range(7)] for i in rows]
    im = ax.imshow(data, cmap="Blues", vmin=0, vmax=1)
    for r, i in enumerate(rows):
        for j in range(7):
            v = M[i][j]
            ax.text(j, r, str(v), ha="center", va="center", fontsize=9, color="white" if data[r][j] > 0.55 else INK)
    ax.set_xticks(range(7)); ax.set_xticklabels(fams, rotation=30, ha="right"); ax.set_yticks(range(len(rows))); ax.set_yticklabels([f"{fams[i]} (n={sum(M[i])})" for i in rows])
    ax.set_xlabel("Image-reader family"); ax.set_ylabel("Prompt-reader family")
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02); cb.set_label("Row fraction (recall)")
    ax.set_title(f"Prompt family versus image family, {K['n']} emotional records\n(Cohen's κ = {K['kappa']:.2f}, 95% CI [{K['ci95'][0]:.2f}, {K['ci95'][1]:.2f}]; the reader never returns disgust)", fontsize=10.5, pad=10)
    save(fig, "fig6_confusion")

# ------------------------------------------------------------------ fig 7: error taxonomy
def fig_taxonomy():
    if not ET: return
    tally = ET["failure_mode_tally"]
    desc = {"a": "Describer invented a face\nor expression", "b": "Describer read the\nexpression wrongly", "c": "Reader mis-inferred from\na correct description",
            "d": "Prompt ambiguous\nor mixed", "e": "Drawing does not\ndepict the prompt", "f": "Prompt reader\nwrong"}
    def key(k): return k.strip("()").lower()[0]
    items = sorted(tally.items(), key=lambda kv: key(kv[0]))
    labels = [desc.get(key(k), k) for k, _ in items]; vals = [(v["n"] if isinstance(v, dict) else v) for _, v in items]
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    cols = [GOLD, GOLD, BLUE, GREY, GREEN, GREY]
    bars = ax.bar(range(len(vals)), vals, 0.6, color=cols[:len(vals)])
    for b, v in zip(bars, vals): ax.annotate(str(v), (b.get_x() + b.get_width()/2, v + 0.3), ha="center", fontweight="bold")
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylabel("Records"); ax.set_ylim(0, max(vals) + 3)
    ax.set_title(f"Primary failure mode of the {ET['sample_size']} high-confidence disagreements (both readers ≥ 0.8, families differ)", fontsize=10.5, pad=10)
    save(fig, "fig7_error_taxonomy")

# ------------------------------------------------------------------ fig 8: ablation (optional)
def fig_ablation():
    if not AB: print("  (ablation summary not present — fig8 skipped)"); return
    variants = ["baseline"] + [v for v in AB if v not in ("baseline", "_meta", "control_full_template")]
    short = {"baseline": "baseline", "drop_expression": "no expression\nsentence", "drop_action": "no action", "drop_posture": "no posture", "drop_people": "no people\ncount", "drop_scene": "no scene\nphrase", "fixed_expression": "expression\n= unclear", "people_aware": "people-aware", "people_aware_no_expression": "people-aware\n+ action"}
    def find(d, subset_hint):
        for k in d:
            if subset_hint in k.lower(): return d[k]
        return None
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8), sharey=True)
    for ax, metric, lab in zip(axes, ("vsign", "family"), ("Valence-sign agreement", "Emotion-family agreement")):
        for j, (hint, col, name) in enumerate((("face", BLUE, "Face-classified"), ("scene", GOLD, "Scene-classified"))):
            vals, nulls = [], []
            for v in variants:
                sub = find(AB[v], hint) or {}
                m = sub.get(metric, {}); vals.append(pct(m.get("obs", float("nan")))); nulls.append(pct(m.get("null", float("nan"))))
            xs = [i + (j - 0.5) * 0.36 for i in range(len(variants))]
            ax.bar(xs, vals, 0.36, color=col, label=name)
            for x_, nv in zip(xs, nulls): ax.plot([x_ - 0.18, x_ + 0.18], [nv, nv], color=INK, lw=1.2, ls=":")
        ax.set_xticks(range(len(variants))); ax.set_xticklabels([short.get(v, v).replace("\n", " ") for v in variants], fontsize=8, rotation=30, ha="right")
        ax.set_title(lab, fontsize=10.5)
    axes[0].set_ylabel("Agreement with the prompt reader (%)")
    h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=9, loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    fig.suptitle("Description-template ablation (NLI re-run only): which describer answers the image reading rests on. Dotted = each cell's own null", fontsize=10.5, y=1.02)
    save(fig, "fig8_ablation")

for f in (fig_face_scene, fig_method, fig_z_by_group, fig_consistency, fig_dataset, fig_confusion, fig_taxonomy, fig_ablation):
    f()
print("all figures done ->", FIG)
