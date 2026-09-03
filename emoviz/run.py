#!/usr/bin/env python3
"""
[BASELINE v1 — SUPERSEDED by describe_extract.py + analysis_final.py. Kept: it produced the frozen direct-CLIP baseline compared in similarity_v2.py. Running it overwrites outputs/results.json.]

EmoViz CLI — run the text->image emotional-fidelity pipeline and build the dashboard.

Examples:
  python3 run.py                          # full run, lexicon text + structural features
  python3 run.py --limit 200              # quick sample
  python3 run.py --image-backend clip     # add CLIP image-emotion (needs setup.sh)
  python3 run.py --text-backend goemotions --image-backend clip   # full ML pipeline
  python3 run.py --report-only            # rebuild dashboard from cached results.json
"""
import argparse, sys
from emoviz import pipeline, report


def main():
    ap = argparse.ArgumentParser(description="EmoViz emotional-fidelity pipeline")
    ap.add_argument("--root", help="path to 02AI_drawing_data (default: sibling of emoviz/)")
    ap.add_argument("--text-backend", default="lexicon", choices=["lexicon", "goemotions"])
    ap.add_argument("--image-backend", default=None, choices=[None, "clip"],
                    help="add CLIP zero-shot image emotion (needs setup.sh)")
    ap.add_argument("--limit", type=int, help="only process the first N records")
    ap.add_argument("--keep-pretest", action="store_true", help="keep records 1-13")
    ap.add_argument("--image-size", type=int, default=256)
    ap.add_argument("--report-only", action="store_true", help="just rebuild the dashboard")
    args = ap.parse_args()

    if args.report_only:
        report.write()
        return

    try:
        pipeline.run(
            root=args.root, text_backend=args.text_backend, image_backend=args.image_backend,
            drop_pretest=not args.keep_pretest, limit=args.limit, image_size=args.image_size,
        )
    except ImportError as e:
        print(f"\n[!] {e}\n", file=sys.stderr)
        sys.exit(2)
    report.write()
    print("\nOpen outputs/dashboard.html in a browser.")


if __name__ == "__main__":
    main()
