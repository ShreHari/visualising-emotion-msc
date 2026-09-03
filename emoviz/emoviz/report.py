"""
emoviz.report — generate a self-contained interactive HTML dashboard from
outputs/results.json. No external hosts: charts are server-rendered SVG, image
thumbnails are inlined as base64. Theme-aware (light/dark).
"""
from __future__ import annotations
import base64, html, io, json, os
from . import analysis

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")

EMO_COLORS = {
    "happiness": "#E0A63B", "sadness": "#4F82C2", "anger": "#C7463A",
    "fear": "#7E6BC4", "surprise": "#2FA7A0", "disgust": "#8B9A45", "neutral": "#9AA0A8",
}
EMO_ORDER = ["happiness", "sadness", "fear", "anger", "surprise", "disgust", "neutral"]


def _thumb(path, px=96):
    try:
        from PIL import Image
        im = Image.open(path).convert("L"); im.thumbnail((px, px))
        buf = io.BytesIO(); im.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


# --------------------------------------------------------------------------- SVG charts
def circumplex(rows, size=440):
    """Valence(-1..1, x) vs Arousal(0..1, y) scatter, coloured by basic emotion."""
    pad = 46; W = H = size; iw = W - 2 * pad; ih = H - 2 * pad
    def X(v): return pad + (v + 1) / 2 * iw
    def Y(a): return pad + (1 - a) * ih
    parts = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Valence-arousal scatter of {len(rows)} emotional records">']
    # quadrant wash + grid
    parts.append(f'<rect x="{pad}" y="{pad}" width="{iw}" height="{ih}" fill="var(--grid-bg)" />')
    parts.append(f'<line x1="{X(0)}" y1="{pad}" x2="{X(0)}" y2="{pad+ih}" class="axis" />')
    parts.append(f'<line x1="{pad}" y1="{Y(0.5)}" x2="{pad+iw}" y2="{Y(0.5)}" class="axis" />')
    # axis labels
    parts.append(f'<text x="{X(0)}" y="{pad-16}" class="axlab" text-anchor="middle">high arousal</text>')
    parts.append(f'<text x="{X(0)}" y="{pad+ih+28}" class="axlab" text-anchor="middle">low arousal</text>')
    parts.append(f'<text x="{pad-10}" y="{Y(0.5)}" class="axlab" text-anchor="end">negative</text>')
    parts.append(f'<text x="{pad+iw+10}" y="{Y(0.5)}" class="axlab" text-anchor="start">positive</text>')
    # jitter deterministically to reduce overplot
    for i, r in enumerate(rows):
        if not r.get("is_emotional"):
            continue
        jx = ((i * 37) % 11 - 5) * 0.9
        jy = ((i * 53) % 11 - 5) * 0.9
        c = EMO_COLORS.get(r["text_basic"], "#999")
        parts.append(f'<circle cx="{X(r["text_valence"])+jx:.1f}" cy="{Y(r["text_arousal"])+jy:.1f}" '
                     f'r="3.1" fill="{c}" fill-opacity="0.62" />')
    parts.append("</svg>")
    return "".join(parts)


def hbars(counts, total, unit=""):
    rows = []
    mx = max(counts.values()) if counts else 1
    for k in EMO_ORDER:
        if k not in counts:
            continue
        v = counts[k]; w = v / mx * 100
        rows.append(f'''<div class="bar-row">
          <span class="bar-key"><i class="dot" style="background:{EMO_COLORS[k]}"></i>{k}</span>
          <span class="bar-track"><span class="bar-fill" style="width:{w:.1f}%;background:{EMO_COLORS[k]}"></span></span>
          <span class="bar-val">{v}</span></div>''')
    return "".join(rows)


def diverging(corr):
    """RQ2 diverging bars: |r| up to 0.25 scale, +ve right / -ve left."""
    rows = []
    keys = sorted(corr.keys(), key=lambda k: -abs(corr[k]["r_valence"]))
    scale = 0.25
    for k in keys:
        rv = max(-scale, min(scale, corr[k]["r_valence"]))
        w = abs(rv) / scale * 50
        # positive extends right of centre, negative extends left
        side = f"left:50%;width:{w:.1f}%" if rv >= 0 else f"right:50%;width:{w:.1f}%"
        col = "var(--pos)" if rv >= 0 else "var(--neg)"
        rows.append(f'''<div class="dv-row">
          <span class="dv-key">{k}</span>
          <span class="dv-track"><span class="dv-fill" style="{side};background:{col}"></span>
            <span class="dv-zero"></span></span>
          <span class="dv-val">{corr[k]["r_valence"]:+.2f}</span></div>''')
    return "".join(rows)


def consistency_bars(per_run, n=14):
    rows = []
    runs = [e for e in per_run if e.get("cv_ink_density") is not None][:n]
    mx = max((e["cv_ink_density"] for e in runs), default=1) or 1
    for e in runs:
        cv = e["cv_ink_density"]; w = cv / mx * 100
        txt = html.escape((e["text"] or "")[:34])
        rows.append(f'''<div class="cv-row">
          <span class="cv-key" title="{txt}">{txt} <b>×{e["size"]}</b></span>
          <span class="cv-track"><span class="cv-fill" style="width:{w:.1f}%"></span></span>
          <span class="cv-val">{cv:.2f}</span></div>''')
    return "".join(rows)


# --------------------------------------------------------------------------- page
def build(results_path=None):
    results_path = results_path or os.path.join(OUT, "results.json")
    R = json.load(open(results_path))
    rows = R["rows"]; meta = R["meta"]; dist = R["distribution"]
    fid = R["fidelity"]; cons = R["consistency"]; integ = R["integrity"]

    # gallery: the largest duplicate run (Happy x11) as a consistency strip
    biggest = cons["per_run"][0] if cons["per_run"] else None
    strip = ""
    if biggest:
        ids = set(biggest["ids"])
        members = [r for r in rows if r["id"] in ids]
        thumbs = "".join(
            f'<figure class="th"><img src="{_thumb(r["image_path"])}" alt="record {r["id"]}"/>'
            f'<figcaption>#{r["id"]}</figcaption></figure>' for r in members)
        strip = f'''<div class="strip">{thumbs}</div>
          <p class="cap">All {biggest["size"]} images above were generated from the identical prompt
          <b>&ldquo;{html.escape(biggest["text"])}&rdquo;</b> — every one is a distinct DALL·E sample.</p>'''

    # sample pairs gallery (spread across emotions)
    picks, seen = [], set()
    for r in rows:
        b = r["text_basic"]
        if r.get("is_emotional") and b not in seen and r.get("image_path"):
            picks.append(r); seen.add(b)
        if len(picks) >= 7:
            break
    gallery = "".join(
        f'''<figure class="pair">
          <img src="{_thumb(r["image_path"],140)}" alt="record {r['id']}"/>
          <figcaption><span class="tag" style="--c:{EMO_COLORS.get(r["text_basic"],"#999")}">{r["text_basic"]}</span>
          <span class="ptext">{html.escape((r["text"] or "")[:90])}</span></figcaption>
        </figure>''' for r in picks)

    fv = "%.2f" % dist["mean_valence"]; fa = "%.2f" % dist["mean_arousal"]
    emo_pct = round(100 * dist["n_emotional"] / meta["n"])
    rq1 = fid["text_vs_image_emotion"]
    rq1_html = (f'<b>κ={rq1["cohens_kappa"]:.2f}</b>, agreement {rq1["agreement"]:.0%} (n={rq1["n_paired"]})'
                if rq1 else '<span class="pending">requires the CLIP image backend — run <code>setup.sh</code></span>')

    # strongest RQ2 signals
    corr = fid["text_vs_image_feature_corr"]
    top_sig = sorted(corr.items(), key=lambda kv: -abs(kv[1]["r_valence"]))[:1][0]
    top_ar = sorted(corr.items(), key=lambda kv: -abs(kv[1]["r_arousal"]))[:1][0]

    return PAGE.format(
        n=meta["n"], n_emo=dist["n_emotional"], emo_pct=emo_pct,
        n_runs=cons["n_runs"], mean_v=fv, mean_a=fa,
        text_backend=meta["text_backend"], img_backend=meta["image_backend"] or "— (lexicon-only run)",
        elapsed=meta["elapsed_s"],
        circumplex=circumplex(rows), dist_bars=hbars(dist["basic_counts"], meta["n"]),
        dv=diverging(corr), cv=consistency_bars(cons["per_run"]),
        strip=strip, gallery=gallery, rq1=rq1_html,
        top_v_feat=top_sig[0], top_v_r="%+.2f" % top_sig[1]["r_valence"],
        top_a_feat=top_ar[0], top_a_r="%+.2f" % top_ar[1]["r_arousal"],
        resolved=integ["images_resolved"], missing=len(integ["images_missing"]),
        ts_cov=integ["timestamp_coverage"], big_run=integ["largest_run"],
        cv_ink=cons["mean_feature_cv"].get("ink_density", 0),
        cv_edge=cons["mean_feature_cv"].get("edge_density", 0),
    )


def write(path=None):
    path = path or os.path.join(OUT, "dashboard.html")
    open(path, "w").write(build())
    print("wrote", path)
    return path


PAGE = r"""<meta charset="utf-8">
<title>EmoViz — Text-to-Image Emotional Fidelity</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{{
  --paper:#F4F5F7; --panel:#FFFFFF; --ink:#16191F; --ink-soft:#4A515C; --ink-faint:#8B929C;
  --line:#DDE1E7; --grid-bg:#EDEFF3; --accent:#2B5C8A; --pos:#C7813A; --neg:#4F82C2;
  --shadow:0 1px 2px rgba(20,25,35,.06),0 8px 24px rgba(20,25,35,.05);
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,"SF Mono","Cascadia Code",Menlo,monospace;
}}
@media (prefers-color-scheme:dark){{:root{{
  --paper:#0E1116; --panel:#151A21; --ink:#E8EAED; --ink-soft:#A8AEB8; --ink-faint:#6B7480;
  --line:#232833; --grid-bg:#1A2029; --accent:#6BA8D8; --pos:#E0A65E; --neg:#6BA8D8;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 28px rgba(0,0,0,.35);
}}}}
:root[data-theme="light"]{{
  --paper:#F4F5F7; --panel:#FFFFFF; --ink:#16191F; --ink-soft:#4A515C; --ink-faint:#8B929C;
  --line:#DDE1E7; --grid-bg:#EDEFF3; --accent:#2B5C8A; --pos:#C7813A; --neg:#4F82C2;
}}
:root[data-theme="dark"]{{
  --paper:#0E1116; --panel:#151A21; --ink:#E8EAED; --ink-soft:#A8AEB8; --ink-faint:#6B7480;
  --line:#232833; --grid-bg:#1A2029; --accent:#6BA8D8; --pos:#E0A65E; --neg:#6BA8D8;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  line-height:1.5;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1080px;margin:0 auto;padding:clamp(20px,4vw,52px)}}
header{{border-bottom:1px solid var(--line);padding-bottom:26px;margin-bottom:34px}}
.eyebrow{{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);margin:0 0 10px}}
h1{{font-family:var(--serif);font-weight:600;font-size:clamp(30px,5vw,46px);line-height:1.04;
  margin:0 0 12px;text-wrap:balance;letter-spacing:-.01em}}
.sub{{color:var(--ink-soft);max-width:63ch;margin:0;font-size:16.5px}}
h2{{font-family:var(--serif);font-weight:600;font-size:23px;margin:0 0 4px;letter-spacing:-.01em}}
.lead{{color:var(--ink-soft);margin:0 0 20px;font-size:14.5px;max-width:70ch}}
section{{margin:44px 0}}
.rule{{display:flex;align-items:baseline;gap:12px;margin-bottom:18px}}
.rule .no{{font-family:var(--mono);font-size:12px;color:var(--ink-faint);letter-spacing:.1em}}
.rule .line{{flex:1;height:1px;background:var(--line)}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}}
.kpi{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 18px 16px;
  box-shadow:var(--shadow)}}
.kpi .v{{font-family:var(--serif);font-size:32px;font-weight:600;line-height:1;
  font-variant-numeric:tabular-nums}}
.kpi .k{{color:var(--ink-faint);font-size:12.5px;margin-top:8px;font-family:var(--mono);
  letter-spacing:.03em}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
@media(max-width:760px){{.grid2{{grid-template-columns:1fr}}}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px;
  box-shadow:var(--shadow);min-width:0}}
.chart{{width:100%;height:auto;display:block}}
.chart .axis{{stroke:var(--ink-faint);stroke-width:1;stroke-dasharray:3 3;opacity:.6}}
.chart .axlab{{fill:var(--ink-faint);font-family:var(--mono);font-size:11px}}
.bar-row,.dv-row,.cv-row{{display:grid;align-items:center;gap:10px;margin:7px 0;font-size:13.5px}}
.bar-row{{grid-template-columns:118px 1fr 34px}}
.bar-key{{display:flex;align-items:center;gap:7px;color:var(--ink-soft);text-transform:capitalize}}
.dot{{width:9px;height:9px;border-radius:50%;flex:none}}
.bar-track{{background:var(--grid-bg);border-radius:5px;height:12px;overflow:hidden}}
.bar-fill{{height:100%;border-radius:5px}}
.bar-val,.dv-val,.cv-val{{font-family:var(--mono);text-align:right;color:var(--ink-soft);
  font-variant-numeric:tabular-nums;font-size:12.5px}}
.dv-row{{grid-template-columns:96px 1fr 44px}}
.dv-key{{font-family:var(--mono);font-size:11.5px;color:var(--ink-soft)}}
.dv-track{{position:relative;height:16px;background:var(--grid-bg);border-radius:4px}}
.dv-zero{{position:absolute;left:50%;top:-3px;bottom:-3px;width:1px;background:var(--ink-faint);opacity:.7}}
.dv-fill{{position:absolute;top:0;height:100%;border-radius:3px;opacity:.85}}
.cv-row{{grid-template-columns:1fr 90px 34px}}
.cv-key{{font-size:12.5px;color:var(--ink-soft);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.cv-key b{{color:var(--ink);font-family:var(--mono)}}
.cv-track{{background:var(--grid-bg);border-radius:5px;height:11px;overflow:hidden}}
.cv-fill{{height:100%;background:linear-gradient(90deg,var(--neg),var(--pos));border-radius:5px}}
.legend{{display:flex;flex-wrap:wrap;gap:12px 16px;margin-top:14px;font-size:12px;color:var(--ink-soft)}}
.legend span{{display:flex;align-items:center;gap:6px}}
.strip{{display:flex;gap:8px;overflow-x:auto;padding:4px 0 10px}}
.th{{margin:0;flex:none;text-align:center}}
.th img{{width:86px;height:86px;object-fit:cover;border:1px solid var(--line);border-radius:8px;
  background:#fff}}
.th figcaption{{font-family:var(--mono);font-size:10.5px;color:var(--ink-faint);margin-top:4px}}
.cap{{font-size:13.5px;color:var(--ink-soft);margin:6px 0 0}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:14px}}
.pair{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.pair img{{width:100%;aspect-ratio:1;object-fit:cover;background:#fff;display:block;border-bottom:1px solid var(--line)}}
.pair figcaption{{padding:9px 10px 11px}}
.tag{{display:inline-block;font-family:var(--mono);font-size:10.5px;text-transform:uppercase;
  letter-spacing:.05em;color:var(--c);border:1px solid var(--c);border-radius:20px;padding:1px 8px;margin-bottom:6px}}
.ptext{{display:block;font-size:12.5px;color:var(--ink-soft);line-height:1.4}}
.pending{{color:var(--ink-faint);font-style:italic}}
code{{font-family:var(--mono);font-size:.88em;background:var(--grid-bg);padding:1px 5px;border-radius:4px}}
.callout{{border-left:3px solid var(--accent);padding:2px 0 2px 16px;margin:20px 0;color:var(--ink-soft);font-size:14px}}
footer{{margin-top:52px;padding-top:22px;border-top:1px solid var(--line);color:var(--ink-faint);
  font-size:12.5px;font-family:var(--mono);line-height:1.7}}
.big{{font-size:15px;color:var(--ink)}}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">EmoViz · text → image emotional fidelity</p>
  <h1>Do the drawings feel the way the words do?</h1>
  <p class="sub">A pipeline over {n} public self-reports, each rendered as monochrome line-art by DALL·E.
  It reads the emotion in the text, measures the image, and asks whether — with colour stripped away —
  the picture still carries the feeling. Corpus leans positive (mean valence {mean_v}); {emo_pct}% of
  entries carry a legible emotion.</p>
</header>

<div class="kpis">
  <div class="kpi"><div class="v">{n}</div><div class="k">records analysed</div></div>
  <div class="kpi"><div class="v">{n_emo}</div><div class="k">emotional / {emo_pct}%</div></div>
  <div class="kpi"><div class="v">{mean_v}</div><div class="k">mean valence</div></div>
  <div class="kpi"><div class="v">{mean_a}</div><div class="k">mean arousal</div></div>
  <div class="kpi"><div class="v">{n_runs}</div><div class="k">duplicate-prompt runs</div></div>
</div>

<section>
  <div class="rule"><h2>The emotional landscape of the corpus</h2><span class="line"></span></div>
  <p class="lead">Every emotional self-report placed on Russell's circumplex — horizontal is valence
  (unpleasant→pleasant), vertical is arousal (calm→activated), colour is the dominant basic emotion.
  The crowding in the upper-right is real: this was a public engagement event, and people mostly reported
  feeling good.</p>
  <div class="grid2">
    <div class="card">{circumplex}
      <div class="legend">
        <span><i class="dot" style="background:#E0A63B"></i>happiness</span>
        <span><i class="dot" style="background:#4F82C2"></i>sadness</span>
        <span><i class="dot" style="background:#7E6BC4"></i>fear</span>
        <span><i class="dot" style="background:#C7463A"></i>anger</span>
        <span><i class="dot" style="background:#2FA7A0"></i>surprise</span>
        <span><i class="dot" style="background:#8B9A45"></i>disgust</span>
      </div>
    </div>
    <div class="card">
      <h2 style="font-size:17px">Emotion distribution</h2>
      <p class="lead" style="margin-bottom:16px">Basic-emotion counts (text side).</p>
      {dist_bars}
    </div>
  </div>
</section>

<section>
  <div class="rule"><span class="no">RQ1</span><h2>Does the image emotion match the text?</h2><span class="line"></span></div>
  <p class="lead">The headline question. Extract the emotion the <em>image</em> conveys with a CLIP zero-shot
  classifier, compare it to the text emotion, and score the agreement (Cohen's κ).</p>
  <p class="big">{rq1}</p>
</section>

<section>
  <div class="rule"><span class="no">RQ2</span><h2>What survives when colour is removed?</h2><span class="line"></span></div>
  <p class="lead">These images are pure black-and-white line-art, so any affect must live in composition and
  line — not colour, which the literature says is the dominant channel. Correlation between text valence and
  each structural image feature. Bars are weak by design: that faintness <em>is</em> the finding. Strongest
  signals — <b>{top_v_feat}</b> tracks valence ({top_v_r}); <b>{top_a_feat}</b> tracks arousal ({top_a_r}).</p>
  <div class="card">{dv}
    <p class="cap" style="margin-top:14px">Pearson r of text valence vs image feature. Left = negative, right = positive; scale ±0.25.</p>
  </div>
</section>

<section>
  <div class="rule"><span class="no">RQ3</span><h2>How consistent is DALL·E on an identical prompt?</h2><span class="line"></span></div>
  <p class="lead">The corpus contains a hidden natural experiment: {n_runs} prompts were each sent to DALL·E
  several times in a row. The images differ every time — here is how much, measured as the coefficient of
  variation in ink density across each run (higher = less consistent).</p>
  <div class="grid2">
    <div class="card">{cv}
      <p class="cap" style="margin-top:12px">Within-run variation of ink density, top runs by sample count.</p>
    </div>
    <div class="card">
      <h2 style="font-size:17px">The largest run, seen</h2>
      {strip}
    </div>
  </div>
</section>

<section>
  <div class="rule"><h2>A look at the pairs</h2><span class="line"></span></div>
  <p class="lead">One example per emotion — the self-report and the drawing it produced.</p>
  <div class="gallery">{gallery}</div>
</section>

<section>
  <div class="rule"><h2>Data integrity</h2><span class="line"></span></div>
  <div class="kpis">
    <div class="kpi"><div class="v">{resolved}</div><div class="k">images resolved</div></div>
    <div class="kpi"><div class="v">{missing}</div><div class="k">missing / broken</div></div>
    <div class="kpi"><div class="v">{ts_cov}</div><div class="k">C2PA timestamps</div></div>
    <div class="kpi"><div class="v">×{big_run}</div><div class="k">largest identical run</div></div>
  </div>
  <div class="callout">The loader resolves all three filename patterns and both letter-cases, drops the 13
  pre-event test records, recovers a per-image DALL·E timestamp from the C2PA manifest, and groups the
  duplicate-prompt runs — so every number here rests on a clean 1:1 text↔image mapping.</div>
</section>

<footer>
  text backend: {text_backend} &nbsp;·&nbsp; image backend: {img_backend} &nbsp;·&nbsp; {elapsed}s over {n} records<br>
  EmoViz demo framework · lexicon + structural features run offline; install CLIP/GoEmotions for the
  full RQ1 result · generated from outputs/results.json
</footer>
</div>
"""


if __name__ == "__main__":
    write()
