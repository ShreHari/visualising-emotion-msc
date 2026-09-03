"""
emoviz.data — robust loader for the '02AI_drawing_data' corpus.

Bakes in the dataset quirks established during exploration:
  * data.json is a flat dict {"1".."1025"} of bare strings (no metadata).
  * image N links to text N *positionally*.
  * THREE incompatible filename patterns:
        1-199    img_00001.PNG   (5-digit zero-padded)
        200-999  img_200.PNG     (unpadded)
        1000+    img_t1000.PNG   ('t' prefix)
  * two images are lowercase '.png' (records 2, 4) -> breaks glob('*.PNG') on Linux.
  * every PNG carries a C2PA/JUMBF manifest (caBX chunk) with an RFC-3161
    signing timestamp we can recover  ->  per-image generation time.
  * records 1-13 are pre-event developer tests (drop them).
  * long runs of identical consecutive text = independent DALL-E samples of one
    prompt (a natural experiment on generative consistency).

Pure standard-library + (optional) nothing else. No pandas/torch needed.
"""
from __future__ import annotations
import json, os, re, struct
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional

# ----------------------------------------------------------------------------- paths
def default_root() -> str:
    # emoviz/ lives inside the dissertation folder; data is a sibling.
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(os.path.dirname(here), "02AI_drawing_data")

PRETEST_MAX = 13  # records 1..13 are pre-event tests

# ----------------------------------------------------------------------------- record
@dataclass
class Record:
    id: int
    text: str
    image_path: Optional[str]
    timestamp: Optional[str] = None      # ISO8601, from C2PA signing time
    is_pretest: bool = False
    run_id: Optional[int] = None         # groups consecutive identical-text runs
    run_size: int = 1                    # how many records share this run
    word_count: int = 0
    is_ascii: bool = True
    dedup_key: Optional[int] = None      # identity group computed from the ORIGINAL text

    def to_dict(self):
        return asdict(self)

# ----------------------------------------------------------------------------- image resolver
def resolve_image(root: str, n: int) -> Optional[str]:
    """Return the on-disk path for record n across all known naming patterns/cases."""
    imgs = os.path.join(root, "imgs")
    candidates = [
        f"img_{n:05d}.PNG", f"img_{n:05d}.png",   # 1-199 zero-padded
        f"img_{n}.PNG",     f"img_{n}.png",        # 200-999 unpadded
        f"img_t{n}.PNG",    f"img_t{n}.png",       # 1000+ 't' prefix
    ]
    for c in candidates:
        p = os.path.join(imgs, c)
        if os.path.exists(p):
            return p
    return None

# ----------------------------------------------------------------------------- C2PA timestamp
_GENTIME = re.compile(rb"20[0-9]{12}Z")  # ASN.1 GeneralizedTime yyyymmddHHMMSSZ

def _cabx_blob(path: str) -> bytes:
    """Extract the caBX (C2PA/JUMBF) chunk bytes from a PNG, up to first IDAT."""
    try:
        with open(path, "rb") as fh:
            d = fh.read()
    except OSError:
        return b""
    i, out = 8, b""
    while i + 8 <= len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        typ = d[i + 4:i + 8]
        if typ == b"caBX":
            out += d[i + 8:i + 8 + ln]
        if typ == b"IDAT":
            break
        i += 8 + ln + 4
    return out

def image_timestamp(path: Optional[str]) -> Optional[str]:
    """Recover the DALL-E generation time from the C2PA signing timestamp."""
    if not path:
        return None
    blob = _cabx_blob(path)
    stamps = sorted(set(m.group().decode() for m in _GENTIME.finditer(blob)))
    if not stamps:
        return None
    s = stamps[0]  # the signing time (earliest gentime in the manifest)
    try:
        dt = datetime.strptime(s, "%Y%m%d%H%M%S%f" if len(s) > 15 else "%Y%m%d%H%M%SZ")
        return dt.replace(tzinfo=timezone.utc).isoformat()
    except ValueError:
        # s like '20240919092541Z'
        try:
            dt = datetime.strptime(s, "%Y%m%d%H%M%SZ")
            return dt.replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            return None

# ----------------------------------------------------------------------------- redaction
def _redactor():
    """The reviewed name-redaction step. Imported lazily so the loader keeps working (loudly)
    if the pre-processing module or its lexical resources are ever missing."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from preprocess_names import redact
    return redact

# ----------------------------------------------------------------------------- loader
def load(root: Optional[str] = None, *, with_timestamps: bool = True,
         drop_pretest: bool = False, redact_names: bool = True) -> list[Record]:
    """Load the corpus as a list[Record], validated to a clean 1:1 mapping.

    Names of private individuals are redacted BY DEFAULT (supervisor direction, 30 Jul 2026).
    Redaction happens here, at the single point every downstream surface loads through, so the
    analysis, the figures and the demo app cannot diverge. Illness and grief content is kept —
    it is not identifying on its own and it is essential to the analysis.
    Pass redact_names=False only to audit the procedure (see preprocess_names.py).
    The dataset files on disk are never modified.
    """
    root = root or default_root()
    data_path = os.path.join(root, "json", "data.json")
    with open(data_path, encoding="utf-8") as fh:
        raw = json.load(fh)

    ids = sorted(int(k) for k in raw.keys())
    records: list[Record] = []
    # Duplicate identity MUST be decided on the original text. Redaction can collapse two
    # genuinely different prompts into the same string: two records holding two DIFFERENT people's
    # names both become "[name]", which would otherwise be counted as one prompt drawn twice. The key is a
    # bare group index: it carries no information about the name it replaced.
    _key, _seen = {}, {}
    for n in ids:
        norm = raw[str(n)].strip().lower()
        _key[n] = _seen.setdefault(norm, len(_seen))

    scrub = _redactor() if redact_names else (lambda t, n=None: t)
    for n in ids:
        text = scrub(raw[str(n)], n)
        rec = Record(
            id=n,
            text=text,
            image_path=resolve_image(root, n),
            is_pretest=(n <= PRETEST_MAX),
            word_count=len(text.split()),
            is_ascii=text.isascii(),
            dedup_key=_key[n],
        )
        records.append(rec)

    # --- duplicate-run grouping (consecutive identical text) ---
    run_id = 0
    i = 0
    while i < len(records):
        j = i
        while j + 1 < len(records) and records[j + 1].text.strip() == records[i].text.strip():
            j += 1
        size = j - i + 1
        for k in range(i, j + 1):
            records[k].run_id = run_id
            records[k].run_size = size
        run_id += 1
        i = j + 1

    # --- timestamps (optional; ~2s for all 1025) ---
    if with_timestamps:
        for rec in records:
            rec.timestamp = image_timestamp(rec.image_path)

    if drop_pretest:
        records = [r for r in records if not r.is_pretest]
    return records

# ----------------------------------------------------------------------------- integrity report
def integrity(records: list[Record]) -> dict:
    n = len(records)
    missing = [r.id for r in records if r.image_path is None]
    lowercase = [r.id for r in records if r.image_path and r.image_path.endswith(".png")]
    dup_runs = {}
    for r in records:
        if r.run_size > 1:
            dup_runs.setdefault(r.run_id, []).append(r.id)
    ts = [r.timestamp for r in records if r.timestamp]
    return {
        "n_records": n,
        "images_missing": missing,
        "images_resolved": n - len(missing),
        "lowercase_png_ids": lowercase,
        "pretest_ids": [r.id for r in records if r.is_pretest],
        "n_duplicate_runs": len(dup_runs),
        "records_in_runs": sum(len(v) for v in dup_runs.values()),
        "largest_run": max((len(v) for v in dup_runs.values()), default=0),
        "timestamp_coverage": len(ts),
        "timestamp_range": [min(ts), max(ts)] if ts else None,
    }

if __name__ == "__main__":
    recs = load()
    import pprint
    pprint.pp(integrity(recs))
