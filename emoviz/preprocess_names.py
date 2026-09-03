#!/usr/bin/env python3
"""
preprocess_names.py — the dataset's name-redaction pre-processing step.

SUPERVISOR DIRECTION (Dr Chaona Chen, 30 Jul 2026): redact real names; KEEP illness and
grief content — it is not identifying on its own and it is essential to the analysis;
document the procedure.

Three stages, all reproducible from this file alone:

  1. HIGH-RECALL DETECTION (`candidates`)
     Flags every token that is either a gazetteer first name, or capitalised mid-sentence
     and absent from an English dictionary, or preceded by a naming phrase ("called X",
     "my friend X"). Deliberately over-flags: 77% of the corpus is written entirely in
     lower case, so capitalisation alone would miss most real names.
     Resources: NLTK `names` (7,944 given names), NLTK `words` + the system dictionary
     (~236k English words).

  2. REVIEWED DECISION (`DECISIONS`)
     Every candidate the detector produced was reviewed once and recorded below with a
     reason. Only names of PRIVATE INDIVIDUALS are redacted. Places, brands, public
     figures, medical eponyms and detector artefacts are kept. This table is a documented
     editorial judgement over a fixed 1,025-record corpus, not a heuristic — re-run
     `candidates()` after any data change and any unreviewed candidate raises.

  3. APPLICATION (`redact`)
     Applied at the data loader, so every downstream surface — analysis, figures, the demo
     app — sees redacted text. The original dataset files are NEVER modified.

Run `python preprocess_names.py` for the audit report.
"""
from __future__ import annotations
import functools, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDER = "[name]"

# ---------------------------------------------------------------- lexical resources
@functools.lru_cache(maxsize=1)
def _lex():
    from nltk.corpus import names as _n, words as _w
    try:
        gaz = {n.lower() for n in _n.words()}
        eng = {w.lower() for w in _w.words()}
    except LookupError:                       # first run on a new machine
        import nltk
        nltk.download("names", quiet=True); nltk.download("words", quiet=True)
        gaz = {n.lower() for n in _n.words()}
        eng = {w.lower() for w in _w.words()}
    sysdict = "/usr/share/dict/words"
    if os.path.exists(sysdict):
        eng |= {w.strip().lower() for w in open(sysdict, encoding="utf-8", errors="ignore")}
    return gaz, eng

_REL = (r"friend|mate|partner|husband|wife|son|daughter|mum|mom|mother|dad|father|brother|"
        r"sister|nan|nana|gran|grandma|grandad|grandpa|boyfriend|girlfriend|dog|cat|pet|"
        r"baby|child|kid|colleague|boss|neighbour|neighbor|professor|doctor|teacher")
_CTX = [re.compile(r"\b(?:called|named)\s+([A-Za-z][a-z]+)", re.I),
        re.compile(rf"\b(?:my|our|his|her|their)\s+(?:{_REL})\s+([A-Za-z][a-z]+)", re.I)]

def candidates(text: str) -> dict[str, list[str]]:
    """token -> reasons it looks like a name. High recall by design."""
    gaz, eng = _lex()
    ctx = {m.group(1).lower() for c in _CTX for m in c.finditer(text)}
    out: dict[str, list[str]] = {}
    for m in re.finditer(r"[A-Za-z][A-Za-z'\-]*", text):
        w, pos = m.group(), m.start()
        lw = w.lower().strip("'")
        if len(lw) < 2:
            continue
        capmid = w[0].isupper() and pos > 0 and not text[:pos].rstrip().endswith((".", "!", "?"))
        why = []
        if lw in gaz and lw not in eng:                     why.append("gazetteer name, not an English word")
        if lw in gaz and lw in eng and (capmid or lw in ctx): why.append("gazetteer name + naming signal")
        if capmid and lw not in eng and lw not in gaz:      why.append("capitalised mid-sentence, not an English word")
        if lw in ctx:                                       why.append("follows a naming phrase")
        if why:
            out.setdefault(lw, []).extend(why)
    return out

# ---------------------------------------------------------------- stage 2: reviewed decisions
# REDACT — names of private individuals, SCOPED TO THE RECORD they were reviewed in.
# Scoping matters: a bare token list redacted "Jack Frost" (id 41, folklore) and "woolly
# mammoth" (id 463) because those strings also occur innocently elsewhere. Each entry is a
# specific reviewed edit to a specific record, which is also what makes the log auditable.
REDACT: dict[str, tuple[set[int], str]] = {
    "marilyn":  ({20},   "private individual being visited"),
    "jack":     ({453},  "private individual, 'a person called Jack Woolley'"),
    "woolley":  ({453},  "surname of the same individual"),
    "timmy":    ({739},  "private individual"),
    "karena":   ({750},  "private individual, full name given"),
    "cheung":   ({750},  "surname of the same individual"),
    "thomas":   ({751},  "private individual, full name given"),
    "chung":    ({751},  "surname of the same individual"),
    "laurie":   ({894},  "private individual"),
    "ellis":    ({894},  "private individual"),
    "matteo":   ({985},  "private individual, 'my friend Matteo'"),
    "vanessa":  ({1020}, "named individual, 'professor vanessa'"),
}
# KEEP — reviewed and judged not personal data. Grouped by why.
KEEP = {
    **dict.fromkeys(["sheffield", "yorkshire", "dale", "uk", "oslo", "london", "france",
                     "millenium", "morocco", "mexican", "scottish"], "place name"),
    **dict.fromkeys(["pinterest", "nissan", "gtr", "skyline", "essenza", "scv", "panionios",
                     "chihuahua", "lamborghini"], "brand / club / product"),
    **dict.fromkeys(["sandro", "botticelli", "noah", "kahan", "ryan", "adams", "orwell",
                     "jesus", "mohammad", "star", "born"], "public or cultural figure — not personal data"),
    **dict.fromkeys(["parkinson", "parkinson's", "alzheimer", "alzheimer's", "mri"],
                    "medical term — supervisor directed that illness content is kept"),
    **dict.fromkeys(["whiskers"], "pet name, not a person"),
    **dict.fromkeys(["cat", "dog", "pet", "baby", "gran", "mum", "nan"],
                    "relationship word captured by the naming regex, not a name"),
    **dict.fromkeys(["justin", "bieber", "frost", "woolly", "wooley", "elvis", "santa"],
                    "public or folklore figure — not personal data"),
    **dict.fromkeys(["christmas", "festival", "monday", "gallery", "jackets", "isde", "groundd",
                     "playing", "having", "has", "improved", "years", "grandchildren", "sleeping",
                     "named", "and", "on", "in", "just", "who", "is", "i'm", "i've", "i'll",
                     "the", "but", "not", "then", "some", "how", "draw", "looking", "following",
                     "feeling", "happy", "sad", "light", "stuck"],
                    "detector artefact — ALL-CAPS text, contraction or ordinary word"),
}

def redact(text: str, record_id: int | None = None) -> str:
    """Replace reviewed private-individual names with a placeholder. Idempotent.

    A redaction only fires on the record it was reviewed in — passing no record_id redacts
    nothing, so an unscoped call can never silently scrub unrelated text.
    """
    if not text or record_id is None:
        return text
    def swap(m):
        tok = m.group(0).lower().strip("'")
        ids = REDACT.get(tok, (set(), ""))[0]
        return PLACEHOLDER if record_id in ids else m.group(0)
    out = re.sub(r"[A-Za-z][A-Za-z'\-]*", swap, text)
    out = re.sub(rf"(?:{re.escape(PLACEHOLDER)}[\s,]+)+{re.escape(PLACEHOLDER)}", PLACEHOLDER, out)
    return out

def unreviewed(texts) -> dict[str, list[str]]:
    """Candidates the detector raises that no one has ruled on — must be empty."""
    seen: dict[str, list[str]] = {}
    for t in texts:
        for tok, why in candidates(t or "").items():
            if tok not in REDACT and tok not in KEEP:
                seen.setdefault(tok, []).extend(why)
    return seen

# ---------------------------------------------------------------- derived-artifact scrub
# describe_extract.py loads through emoviz.data, so any FUTURE run is redacted automatically.
# Artifacts generated before redaction existed still carry names, so they are scrubbed once here.
SCRUB_TARGETS = ["describe_extract.jsonl", "analysis_final.csv", "records.csv",
                 "results.json", "results_clip_v2_baseline.json"]

def _walk(obj):
    """Yield every dict that carries both a record id and a text field."""
    if isinstance(obj, dict):
        if "text" in obj and any(k in obj for k in ("id", "record_id")):
            yield obj
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)

def scrub_outputs(out_dir: str, apply: bool = False) -> list[tuple[str, int]]:
    """Apply the reviewed redaction to derived artifacts. Writes a .prename backup first."""
    import csv as _csv, shutil
    results = []
    for name in SCRUB_TARGETS:
        path = os.path.join(out_dir, name)
        if not os.path.exists(path):
            continue
        n = 0
        if name.endswith(".jsonl"):
            rows = [json.loads(l) for l in open(path, encoding="utf-8")]
            for r in rows:
                new = redact(r.get("text", ""), r.get("id"))
                if new != r.get("text"): r["text"] = new; n += 1
            if apply and n:
                shutil.copy2(path, path + ".prename")
                with open(path, "w", encoding="utf-8") as fh:
                    for r in rows: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        elif name.endswith(".csv"):
            with open(path, newline="", encoding="utf-8") as fh:
                rd = list(_csv.DictReader(fh)); cols = rd[0].keys() if rd else []
            for r in rd:
                if "text" not in r or "id" not in r: continue
                new = redact(r["text"], int(r["id"]))
                if new != r["text"]: r["text"] = new; n += 1
            if apply and n:
                shutil.copy2(path, path + ".prename")
                with open(path, "w", newline="", encoding="utf-8") as fh:
                    w = _csv.DictWriter(fh, fieldnames=list(cols)); w.writeheader(); w.writerows(rd)
        else:
            obj = json.load(open(path, encoding="utf-8"))
            for d in _walk(obj):
                rid = d.get("id", d.get("record_id"))
                try: rid = int(rid)
                except (TypeError, ValueError): continue
                new = redact(d.get("text", ""), rid)
                if new != d.get("text"): d["text"] = new; n += 1
            if apply and n:
                shutil.copy2(path, path + ".prename")
                json.dump(obj, open(path, "w", encoding="utf-8"), ensure_ascii=False)
        results.append((name, n))
    return results

# ---------------------------------------------------------------- audit report
if __name__ == "__main__":
    import sys
    sys.path.insert(0, ROOT)
    from emoviz import data
    recs = data.load(with_timestamps=False, redact_names=False)
    texts = [r.text for r in recs]

    missing = unreviewed(texts)
    changed = [(r.id, r.text, redact(r.text, r.id)) for r in recs if redact(r.text, r.id) != r.text]
    # every reviewed name must actually fire on its record — catches typos in the table
    stale = [tok for tok, (ids, _) in REDACT.items()
             if not any(re.search(rf"\b{re.escape(tok)}\b", (r.text or "").lower())
                        for r in recs if r.id in ids)]

    print(f"records scanned            : {len(recs)}")
    print(f"records redacted           : {len(changed)}")
    print(f"distinct names redacted    : {len(REDACT)}")
    print(f"unreviewed candidates      : {len(missing)}  <- must be 0")
    print(f"stale REDACT entries       : {len(stale)}  <- must be 0 {stale if stale else ''}")
    for tok, why in sorted(missing.items()):
        print(f"    ! {tok}: {sorted(set(why))}")
    print("\nRedactions applied:")
    for rid, before, after in sorted(changed):
        print(f"  id {rid:4d}  {after}")
    if missing or stale:
        raise SystemExit("\nFAIL: unreviewed candidates, or REDACT entries that match nothing.")
    print("\nDerived artifacts:")
    dry = "--apply" not in sys.argv
    for name, n in scrub_outputs(os.path.join(ROOT, "outputs"), apply=not dry):
        print(f"  {name:34s} {n:3d} text field(s) {'left to scrub (dry run)' if dry and n else 'scrubbed' if n else 'clean'}")
    if dry:
        print("\n  (dry run — re-run with --apply to write; a .prename backup is kept)")
    print("\nOK — every detector candidate has a recorded decision.")
