#!/usr/bin/env python3
r"""
copy_check.py: finds runs of words that a new chapter shares verbatim with the old draft, the
project notes, or the result documents. A shared run of N words (default 8) is reported with both
locations. Use it to make sure no sentence was lifted from the earlier draft or from any note.

Usage: python3 copy_check.py dissertation/chapters/chapter3.tex [--n 8]
"""
import re, sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
SOURCES = glob.glob(os.path.join(PROJ, "report", "chapters", "*.tex")) + \
          glob.glob(os.path.join(PROJ, "project_notes", "**", "*.md"), recursive=True) + \
          glob.glob(os.path.join(PROJ, "emoviz", "outputs", "*.md")) + \
          [os.path.join(PROJ, "emoviz", "README.md"), os.path.join(PROJ, "README.md"), os.path.join(PROJ, "HANDOFF.md")]
def words(text):
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = re.sub(r"\\[A-Za-z]+\*?(\[[^\]]*\])?(\{[^}]*\})*", " ", text)
    return re.findall(r"[a-z0-9']+", text.lower())
def shingles(ws, n):
    return {" ".join(ws[i:i+n]): i for i in range(max(0, len(ws)-n+1))}
def main():
    n = 8
    if "--n" in sys.argv: n = int(sys.argv[sys.argv.index("--n")+1])
    targets = [a for a in sys.argv[1:] if a.endswith(".tex")]
    src_sh = {}
    for f in SOURCES:
        if not os.path.exists(f): continue
        for sh in shingles(words(open(f, encoding="utf8", errors="ignore").read()), n):
            src_sh.setdefault(sh, os.path.relpath(f, PROJ))
    for t in targets:
        ws = words(open(t, encoding="utf8").read())
        hits = [(sh, i, src_sh[sh]) for sh, i in shingles(ws, n).items() if sh in src_sh]
        # merge consecutive shingles into runs
        hits.sort(key=lambda h: h[1]); runs = []
        for sh, i, src in hits:
            if runs and i <= runs[-1][1] + 1 and runs[-1][2] == src:
                runs[-1] = (runs[-1][0], i, src)
            else:
                runs.append((i, i, src))
        print(f"=== {os.path.relpath(t, PROJ)}: {len(runs)} shared runs of >= {n} words ===")
        for a, b, src in runs:
            print(f"  [{src}] ... {' '.join(ws[a:b+n])} ...")
        print()
if __name__ == "__main__": main()
