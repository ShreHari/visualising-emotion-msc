#!/usr/bin/env bash
# Refresh the generated numbers and tables from the analysis result files, then copy them here.
# Run after any analysis change (for example after scoring the single-coder check).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="$(dirname "$HERE")"
"$PROJ/emoviz/.venv/bin/python" "$PROJ/emoviz/export_tex.py"
"$PROJ/emoviz/.venv/bin/python" "$PROJ/emoviz/make_figures.py"
"$PROJ/emoviz/.venv/bin/python" "$HERE/build_notes/make_extra_figures.py"
cp "$PROJ/report/generated/"*.tex "$HERE/generated/"
cp "$PROJ/emoviz/outputs/figures/"*.pdf "$PROJ/emoviz/outputs/figures/"*.png "$HERE/figures/"
echo "generated/ and figures/ refreshed; now rebuild: cd $HERE && pdflatex main && bibtex main && pdflatex main && pdflatex main"
