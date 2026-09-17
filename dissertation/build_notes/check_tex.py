#!/usr/bin/env python3
r"""
check_tex.py: mechanical checks on a dissertation chapter (.tex).

Reports, for the prose of the file:
  * sentence-length statistics (mean, sd, min, max, share under 12 and over 30 words) overall and
    per paragraph, and paragraphs whose sentence lengths are too uniform (sd < 6 words)
  * hits on the banned-construction and banned-vocabulary lists from STYLE_GUIDE.md, with line numbers
  * em/en dashes in prose, 'not X but Y' shapes, forced-triad shapes, repeated sentence openers
  * macros used that are not defined in generated/numbers.tex, \cite keys not in the .bib,
    \ref labels not defined anywhere in dissertation/ (chapters, generated tables, main.tex)
  * digits typed in prose that look like statistics (percentages, z-scores, CIs) outside macros
  * approximate word count

Usage:  python3 check_tex.py dissertation/chapters/chapter3.tex [--json]
Exit code is always 0; read the report.
"""
import re, sys, os, json, statistics, glob

HERE = os.path.dirname(os.path.abspath(__file__))
DISS = os.path.dirname(HERE)

BANNED_PHRASES = [
    # staging / contrast / closers / performed candour
    r"\bnot (?:just|only|merely|simply) \w+[^.]{0,80}\bbut\b", r"\bit is not \w+[^.]{0,60}, it is\b",
    r"\bis not (?:a |an |the )?\w+[^.]{0,40}\b(?:but|so much as) (?:a |an |the )?\w+", r"\bless \w+ than \w+\b",
    r"\brather than\b", r"\bwhich is (?:why|what|exactly|where|how)\b", r"\bThat is the \w+ behind\b",
    r"\bthe reasoning behind\b", r"\bturns? out\b", r"\bin any room\b", r"\bin the end\b", r"\bin effect\b",
    r"\bI want to be careful\b", r"\bhas to be (?:said|stated)\b", r"\bsaid plainly\b", r"\bto be honest\b",
    r"\bthe honest (?:answer|version)\b", r"\bthe right form of words\b", r"\bI would defend\b",
    r"\bThis is not to say\b", r"\bOne might (?:object|argue|think)\b", r"\bIt would be tempting\b",
    r"\bit is worth (?:noting|stating|saying|mentioning)\b", r"\bit should be noted\b", r"\bimportantly\b",
    r"\bnotably\b", r"\barguably\b", r"\bin essence\b", r"\bat its core\b", r"\bfundamentally\b",
    r"\bultimately\b", r"\bserves as\b", r"\bstands as\b", r"\brepresents an? \b", r"\balign(?:s|ed)? with\b",
    r"\binterplay\b", r"\benduring\b", r"\bgarner", r"\bbolster", r"\benhanc(?:e|es|ed|ing)\b",
    r"\bin terms of\b", r"\bin order to\b", r"\bdue to the fact\b", r"\bmoreover\b", r"\bfurthermore\b",
    r"\bin today's\b", r"\ba range of\b", r"\ba variety of\b",
    # vocabulary
    r"\bdelv", r"\bcrucial", r"\bpivotal", r"\bleverag", r"\blandscape\b", r"\btapestry\b", r"\bunderscor",
    r"\bhighlight(?:s|ed|ing)?\b", r"\bshowcas", r"\btestament\b", r"\bvibrant\b", r"\bfoster", r"\bnavigat",
    r"\brealm\b", r"\bintricate\b", r"\bmeticulous", r"\bnuanced?\b", r"\bmultifaceted\b", r"\bholistic\b",
    r"\bseamless", r"\bgroundbreaking\b", r"\bcomprehensive\b", r"\bkey (?:role|part|factor|point|question|finding|result|insight)\b",
    r"\brobust(?:ly)?\b(?! check)(?!ness)",
    # project-specific
    r"\bconvey(?:s|ed|ing)?\b(?!\s*\\?\{)", r"\bcarr(?:y|ies|ied|ying) (?:the |an? |its |their )?(?:emotion|feeling|affect)",
    r"\baccura(?:cy|te|tely)\b", r"\balignment\b", r"\bfidelity\b", r"\bmatch(?:es|ed|ing)?\b", r"\bmood\b",
    r"\bperceiv", r"\bperception\b", r"\bethic", r"\bapproval\b", r"\bconsent\b", r"\bsignificant(?:ly)?\b",
    r"\bprove[sdn]?\b", r"\bdemonstrates?\b", r"\bground truth\b", r"\bhallucinat", r"\bbaseline\b",
]
DASHES = r"(?<![-\w])(?:—|–|--)(?![-\w])"
TRIAD = r"\b\w+, \w+,? and \w+\b"

LATEX_WHITELIST = set("""chapter section subsection subsubsection paragraph label ref cite input include includegraphics
caption centering begin end item textbf textit emph texttt textsc footnote url newcommand renewcommand
resizebox textwidth linewidth vspace hspace noindent par small footnotesize scriptsize large Large huge
setlength itemsep placeholderfigure placeholder mathbb mathcal operatorname frac sqrt sum min max left right
Bigl Bigr bigl bigr tfrac cdot times le ge neq wedge in dots ldots quad qquad text mathrm hat sigma mu pi kappa
alpha beta ell ell_i tilde top sub sup limits parbox fbox hfill newline bibliography bibliographystyle
tableofcontents listoffigures listoftables appendix appendices mainmatter frontmatter addcontentsline
toprule midrule bottomrule multicolumn hline cline rule textbackslash ttfamily sloppypar nocite clearpage
newpage pagebreak enumerate itemize description ttfamily emph SI num percent dag ddag S P copyright
subfigure subcaption figure table equation align tikzpicture center quote quotation verbatim
tcolorbox tcbset cref Cref labelcref eqref pageref autoref""".split())

def load_macros():
    p = os.path.join(DISS, "generated", "numbers.tex")
    return set(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}", open(p, encoding="utf8").read()))

def load_bibkeys():
    p = os.path.join(DISS, "mybibliography.bib")
    return set(re.findall(r"@\w+\{([^,\s]+),", open(p, encoding="utf8").read()))

NEW_LABELS = {"fig:timeline", "fig:promptlength", "fig:installation", "fig:demo", "fig:happygrid",
              "fig:noperson", "fig:testsuite", "app:supervision"}

def load_labels():
    labels = set(NEW_LABELS)
    old = os.path.join(HERE, "labels_old.json")
    if os.path.exists(old):
        labels |= set(json.load(open(old))["labels"])
    for f in glob.glob(os.path.join(DISS, "chapters", "*.tex")) + glob.glob(os.path.join(DISS, "generated", "*.tex")) \
             + glob.glob(os.path.join(DISS, "figures", "*.tex")) + [os.path.join(DISS, "main.tex")]:
        if os.path.exists(f):
            labels |= set(re.findall(r"\\label\{([^}]+)\}", open(f, encoding="utf8").read()))
    return labels

def strip_comments(src):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in src.splitlines())

def prose_of(src):
    """Turn LaTeX into rough prose for rhythm analysis: drop math, commands, keep macro tokens as 'N'."""
    s = strip_comments(src)
    s = re.sub(r"\\begin\{(equation|align|tikzpicture|tabular|table|figure)\*?\}.*?\\end\{\1\*?\}", " ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " N ", s)
    s = re.sub(r"\\(?:input|include|includegraphics|label|ref|cite|placeholderfigure|placeholder)\*?(?:\[[^\]]*\])?\{[^}]*\}(\{[^}]*\})*", " ", s)
    s = re.sub(r"\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}", r"\n\n\1.\n\n", s)
    s = re.sub(r"\\[A-Za-z]+\{\}", " N ", s)            # number macros
    s = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", s)  # other commands
    s = s.replace("{", " ").replace("}", " ").replace("~", " ").replace("``", '"').replace("''", '"')
    return s

def sentences(par):
    par = re.sub(r"\s+", " ", par).strip()
    if not par: return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"(])", par)
    return [p for p in parts if len(p.split()) >= 2]

def analyse(path):
    src = open(path, encoding="utf8").read()
    lines = src.splitlines()
    rep = {"file": os.path.relpath(path, DISS)}
    prose = prose_of(src)
    paras = [p for p in re.split(r"\n\s*\n", prose) if len(p.split()) >= 25]
    all_lens, uniform, no_short, no_long = [], [], [], []
    for i, p in enumerate(paras):
        ls = [len(s.split()) for s in sentences(p)]
        if len(ls) < 3: continue
        all_lens += ls
        sd = statistics.pstdev(ls)
        if sd < 6: uniform.append((i, round(sd, 1), ls))
        if min(ls) >= 12: no_short.append((i, ls))
        if max(ls) <= 30: no_long.append((i, ls))
    if all_lens:
        rep["sentences"] = len(all_lens)
        rep["words_in_prose"] = sum(all_lens)
        rep["mean_len"] = round(statistics.mean(all_lens), 1)
        rep["sd_len"] = round(statistics.pstdev(all_lens), 1)
        rep["min_len"], rep["max_len"] = min(all_lens), max(all_lens)
        rep["share_under_12"] = round(sum(l < 12 for l in all_lens) / len(all_lens), 2)
        rep["share_over_30"] = round(sum(l > 30 for l in all_lens) / len(all_lens), 2)
    rep["paragraphs_analysed"] = len(paras)
    rep["uniform_paragraphs(sd<6)"] = [(i, sd) for i, sd, _ in uniform]
    rep["paragraphs_without_short_sentence"] = [i for i, _ in no_short]
    rep["paragraphs_without_long_sentence"] = [i for i, _ in no_long]
    # repeated openers
    openers = []
    for p in paras:
        ss = sentences(p)
        firsts = [re.sub(r"[^A-Za-z]", "", s.split()[0]).lower() for s in ss if s.split()]
        for k in range(len(firsts) - 2):
            if firsts[k] and firsts[k] == firsts[k + 1] == firsts[k + 2]:
                openers.append(firsts[k])
    rep["three_same_openers_in_a_row"] = openers
    # phrase hits with line numbers (search the raw source minus comments, case-insensitive)
    hits = []
    for n, ln in enumerate(lines, 1):
        clean = re.sub(r"(?<!\\)%.*$", "", ln)
        if re.match(r"\s*\\(?:label|ref|cite|input|includegraphics|caption)", clean.strip()): pass
        for pat in BANNED_PHRASES:
            for m in re.finditer(pat, clean, flags=re.I):
                ctx = clean[max(0, m.start() - 30): m.end() + 30].strip()
                hits.append({"line": n, "pattern": pat, "context": ctx})
        for m in re.finditer(DASHES, clean):
            hits.append({"line": n, "pattern": "DASH", "context": clean[max(0, m.start() - 30): m.end() + 30].strip()})
    rep["phrase_hits"] = hits
    rep["triad_shapes"] = len(re.findall(TRIAD, prose))
    # macros, cites, refs
    macros = load_macros(); bib = load_bibkeys(); labels = load_labels()
    used = set(re.findall(r"\\([A-Za-z]+)\{\}", strip_comments(src)))
    rep["undefined_macros"] = sorted(m for m in used if m not in macros and m not in LATEX_WHITELIST)
    cites = set(k.strip() for c in re.findall(r"\\cite\{([^}]+)\}", src) for k in c.split(","))
    rep["unknown_cite_keys"] = sorted(cites - bib)
    rep["cite_keys_used"] = sorted(cites)
    refs = set(re.findall(r"\\(?:ref|cref|Cref|eqref)\{([^}]+)\}", src))
    rep["undefined_refs"] = sorted(refs - labels)
    # hand-typed statistics in prose
    body = strip_comments(src)
    body = re.sub(r"\\(?:cite|ref|label|input|includegraphics)\{[^}]*\}", "", body)
    typed = re.findall(r"(?<![\\\w])(?:\d{1,3}(?:,\d{3})+|\d+\.\d+\\?%|\b\d{1,2}\.\d%|\bz\s*=\s*[+-]?\d|\[\s*[+-]?\d+\.\d,\s*[+-]?\d+\.\d\s*\]|\b\d+\\%)", body)
    rep["hand_typed_number_like_tokens"] = typed[:60]
    rep["approx_words"] = len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", prose))
    return rep

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    for path in args:
        rep = analyse(path)
        if as_json:
            print(json.dumps(rep, indent=1)); continue
        print(f"=== {rep['file']} ===")
        for k in ("approx_words", "sentences", "mean_len", "sd_len", "min_len", "max_len", "share_under_12", "share_over_30",
                  "paragraphs_analysed", "uniform_paragraphs(sd<6)", "paragraphs_without_short_sentence",
                  "paragraphs_without_long_sentence", "three_same_openers_in_a_row", "triad_shapes",
                  "undefined_macros", "unknown_cite_keys", "undefined_refs", "hand_typed_number_like_tokens"):
            if k in rep: print(f"{k}: {rep[k]}")
        print(f"phrase_hits: {len(rep['phrase_hits'])}")
        for h in rep["phrase_hits"]:
            print(f"  L{h['line']:>4}  [{h['pattern']}]  ...{h['context']}...")
        print()

if __name__ == "__main__":
    main()
