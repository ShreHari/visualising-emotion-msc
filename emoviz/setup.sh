#!/bin/bash
# setup.sh — create the project environment for emoviz (one-time).
# Creates .venv and installs pinned dependencies; every documented command then uses .venv/bin/python.
set -e
cd "$(dirname "$0")"

echo "== creating virtual environment (.venv) =="
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q

echo "== installing pinned dependencies (requirements.txt) =="
.venv/bin/pip install -r requirements.txt

echo
echo "Done. Notes for first run:"
echo "  * Models download once from Hugging Face (~3.5 GB total, cached in ~/.cache/huggingface):"
echo "      Salesforce/blip-vqa-base  ·  facebook/bart-large-mnli  ·  SamLowe/roberta-base-go_emotions"
echo "      (+ open_clip ViT-B-32 weights if the v1 baseline is re-run)"
echo "  * Full pipeline over 1,025 images takes ~30-90 min depending on machine load."
echo
echo "Quick check :  .venv/bin/python analysis_final.py"
echo "Full test    :  bash test.sh"
