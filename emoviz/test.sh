#!/bin/bash
# test.sh — full local test of the emoviz tech. Run:  bash test.sh
cd "$(dirname "$0")" || exit 1
PY=.venv/bin/python
pass=0; fail=0
ok(){ echo "  ✅ PASS  $1"; pass=$((pass+1)); }
no(){ echo "  ❌ FAIL  $1"; fail=$((fail+1)); }
check(){ if eval "$2" >/dev/null 2>&1; then ok "$1"; else no "$1"; fi; }

echo "════════ EMOVIZ TECH TEST ════════"

echo; echo "[1] Environment"
check "venv python works"              "$PY --version"
check "torch + transformers + open_clip import" "$PY -c 'import torch,transformers,open_clip'"
DEV=$($PY -c 'import torch;print("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")')
ok "compute device detected: $DEV"

echo; echo "[2] Data integrity"
check "dataset = 1025 images"           "[ \$(ls ../02AI_drawing_data/imgs/*.[Pp][Nn][Gg] 2>/dev/null | wc -l) -eq 1025 ]"
check "describe_extract.jsonl = 1025 records" "[ \$($PY -c 'print(sum(1 for _ in open(\"outputs/describe_extract.jsonl\")))') -eq 1025 ]"
check "results.json valid"             "$PY -c 'import json;json.load(open(\"outputs/results.json\"))'"
check "no processing failures"         "[ ! -f outputs/describe_extract.failures.log ]"

echo; echo "[3] Analysis scripts run & produce expected findings"
$PY analysis_final.py > /tmp/af.log 2>&1
check "  final analysis runs"          "grep -q 'FINAL ANALYSIS' /tmp/af.log"
check "  face>scene finding present"   "grep -q 'face images' /tmp/af.log"
check "  validity check present"       "grep -q 'non-emotional' /tmp/af.log"
check "  dedup robustness present"     "grep -q 'DISTINCT PROMPTS' /tmp/af.log"
$PY similarity_v2.py > /tmp/s2.log 2>&1
check "  old-vs-new comparison runs"   "grep -q 'BASELINE COMPARISON' /tmp/s2.log"
$PY data_audit_consistency.py > /tmp/ca.log 2>&1
check "  significance test exits 0"   "$PY significance.py"
check "  consistency analysis exits 0" "$PY data_audit_consistency.py"
check "  consistency analysis runs"    "grep -q 'CONSISTENCY' /tmp/ca.log"
check "  consistency null is scripted"  "$PY -c 'import json;d=json.load(open(\"outputs/consistency.json\"));assert d[\"null\"][\"draws\"]>=1000'"
check "  data accounting = 1025"       "grep -q '1025' /tmp/ca.log"
check "  analysis_final.json written"  "[ -f outputs/analysis_final.json ]"
check "  inference (CIs, kappa, Holm) exits 0"      "$PY inference.py"
check "  like-for-like method comparison exits 0"  "$PY method_comparison.py"
check "  control + describer audits exit 0"        "$PY audits.py"

echo; echo "[3b] Numeric regression — every headline number pinned to the result file that produces it"
NL=$(mktemp -t emoviz_num); $PY test_numeric.py > "$NL" 2>&1
check "  test_numeric.py: all pinned values reproduce"  "grep -q ', 0 failed' \"$NL\""
check "  metric module is the single definition (analysis, significance, app import it)" "grep -q 'from emoviz.metrics import' analysis_final.py && grep -q 'from emoviz.metrics import' significance.py && grep -q 'from emoviz.metrics import' app.py"

echo; echo "[4] Live pipeline (BLIP-VQA + NLI) on 3 fresh images"
PT=$(mktemp -t emoviz_pipe).jsonl; rm -f "$PT"      # unique per run: concurrent runs must not collide
$PY describe_extract.py --limit 3 --out "$PT" > /tmp/pipe.log 2>&1
check "  pipeline completes 3/3"       "grep -q 'ok=3 fail=0' /tmp/pipe.log"
check "  produces valid records"       "[ \$(wc -l < "$PT") -eq 3 ]"
check "  each record has description+emotions" "$PY -c 'import json;[[r[\"description\"],r[\"prompt_emotions\"],r[\"image_emotions\"]] for r in map(json.loads,open(\""$PT"\"))]'"

echo; echo "[4b] Name redaction (supervisor direction: redact names, keep illness content)"
$PY preprocess_names.py > /tmp/redact.log 2>&1
check "  redaction audit passes"       "grep -q 'every detector candidate has a recorded decision' /tmp/redact.log"
check "  no unreviewed candidates"     "grep -q 'unreviewed candidates      : 0' /tmp/redact.log"
check "  no stale REDACT entries"      "grep -q 'stale REDACT entries       : 0' /tmp/redact.log"
check "  loader redacts by default"    "$PY -c 'import sys;sys.path.insert(0,\".\");from emoviz import data;rs=data.load(with_timestamps=False);assert all(\"[name]\" in r.text for r in rs if r.id in (750,751,1020))'"
check "  no redacted name in outputs"  "$PY -c 'import sys,json,csv;sys.path.insert(0,\".\");import preprocess_names as p;rows={r[\"id\"]:r[\"text\"] for r in map(json.loads,open(\"outputs/describe_extract.jsonl\"))};rows.update({int(r[\"id\"]):r[\"text\"] for r in csv.DictReader(open(\"outputs/analysis_final.csv\"))});bad=[(t,i) for t,(ids,_) in p.REDACT.items() for i in ids if i in rows and t in rows[i].lower()];assert not bad,bad'"
check "  illness content KEPT"         "$PY -c 'import sys;sys.path.insert(0,\".\");from emoviz import data;rs={r.id:r.text for r in data.load(with_timestamps=False)};assert \"Parkinson\" in rs[302] and \"Alzheimer\" in rs[532]'"
check "  non-person names preserved"   "$PY -c 'import sys;sys.path.insert(0,\".\");from emoviz import data;rs={r.id:r.text for r in data.load(with_timestamps=False)};assert \"mammoth\" in rs[463].lower() and \"frost\" in rs[41].lower()'"
check "  demo pool = all 1012"         "[ \$($PY -c 'import app;print(len(app.records()))') -eq 1012 ]"

echo; echo "[5] All scripts compile"
tot=0; c=0
for f in *.py; do tot=$((tot+1)); $PY -c "import ast;ast.parse(open('$f').read())" 2>/dev/null && c=$((c+1)); done
[ "$c" -eq "$tot" ] && ok "all $tot scripts compile" || no "only $c/$tot scripts compile"

echo; echo "[6] Figures regenerate"
$PY make_figures.py > /tmp/figs.log 2>&1
check "  make_figures.py runs in venv"  "grep -q 'all figures done' /tmp/figs.log"
check "  at least 7 figure PDFs present" "[ \$(ls outputs/figures/*.pdf 2>/dev/null | wc -l) -ge 7 ]"
check "  figures carry no typed result lists (read JSON)" "! grep -qE '\\[ *[0-9]+(\\.[0-9]+)? *, *[0-9]+(\\.[0-9]+)? *, *[0-9]+' make_figures.py"

echo; echo "════════ RESULT: $pass passed, $fail failed ════════"
[ "$fail" -eq 0 ] && echo "🟢 ALL TESTS PASSED — tech side is working." || echo "🔴 $fail test(s) failed — see above."
exit "$fail"
