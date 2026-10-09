#!/usr/bin/env python3
r"""patch_v29_layout_polish.py -- build manuscript_revised_v29.tex from the
canonical v28 file (manuscript_revised_v28.tex) AND supplement_v10.tex from
supplement_v9.tex (both sources preserved unmodified alongside their
predecessors).  Scope (author-directed layout-polish + metaphysics +
data-availability pass):

MANUSCRIPT (v28 -> v29):
(1) COLUMN-OVERFLOW REPAIR OF THE TABLES.  The author reported that
    TABLE IV (tab:n5twosize, overfull 62.75pt) and TABLE V
    (tab:closingrates, overfull 30.76pt) exceed the PDF column; the
    pre-flight scan of the same defect class found two more: TABLE VI
    (tab:smchaar, 94.98pt, its last columns ran past the page edge) and
    TABLE IX (tab:numerics, 46.36pt, its cells crossed into the
    neighbouring column's text).  All four are promoted from
    single-column floats to two-column-spanning floats (table*), the
    format already used by TABLE I; the tabular bodies are carried
    BYTE-IDENTICAL (asserted below), so no number, label, or caption
    changes and the table numbering is unaffected.
(2) CLIPPED DISPLAY EQUATIONS RE-SET.  In the closed-form-spectrum
    proposition the two displays eq:QRdef (overfull 163.42pt) and
    eq:spinor (overfull 207.00pt) overflowed so far that parts of their
    definitions (the whole R(k) definition; the U_k factor of the
    spinor factorization) fell outside the page box and were invisible
    in the rendered PDF.  Both are re-set as multi-line displays
    (aligned / gathered) with every token preserved verbatim
    (asserted below).  A third display (eq:dyadicmoments, overfull
    11.32pt) has its separator tightened (\qquad -> \!\\quad).
(3) ITEM-LABEL REPAIR.  The enumerate of Proposition 13 (prop:gap)
    began on the same paragraph line as the proposition header, so the
    item label "(i)" was typeset at the end of the header line and
    protruded 19pt into the margin.  A \\leavevmode now separates the
    header from the enumerate (the label starts the item line, the
    pattern every other enumerate of the paper already shows); no text
    changes.
(4) METAPHYSICS TERMINOLOGY (Sec. VII).  Per the author: "The standing
    metaphysics.  This section records the working assumption
    maintained with this project's research record and examines what
    it implies for the readings of quantum mechanics." -- the
    metaphysics is established once as the working assumption and
    thereafter referred to by its descriptive, ontological name.  All
    fourteen further occurrences of "assumption"/"assumption's" inside
    Sec. VII (and the introduction's spine entry describing Sec. VII)
    become "metaphysics" or an equivalent grammatical form; the
    mathematical uses of "assumption" elsewhere in the paper are
    untouched.
(5) DATA AVAILABILITY.  The deposit host changes from figshare to
    preprints.org, and the statement now records formally that the
    Supplementary Material includes the web simulation of the monitored
    circuits (the interactive stabilizer-tableau simulator with the
    finite-size-scaling benchmark, the annealed replica chain, and the
    record SCGF analyses).

SUPPLEMENT (v9 -> v10), same defect class:
(6) The SMC weight display (overfull 74.03pt, its w-bar term ran past
    the page edge) is split into two align lines, tokens preserved.
(7) The calibration table tabS:calib (overfull 91.53pt) is promoted to
    a two-column float; tabular body byte-identical.
(8) The reproduction command/purpose block (overfull 260.94/265.64pt,
    rendered ON TOP of the right column's text) is re-set as an
    itemized list with both commands and their purposes verbatim.
(9) Six literal label-name references (Remark rem:cliff3design,
    Prop. prop:z3closure x2, Table tab:z3exact, Table tab:n5twosize,
    Table tab:closingrates) and three label-style equation pointers
    (Eq. (rank3), Eq. (dyadicmoments), Eq. (Wpn) x2) are replaced by
    the explicit numbers of the main text (Remark 7, Proposition 13,
    Tables IV/V/VII, Eqs. (55)/(87)/(14)), the convention already used
    elsewhere in the supplement ("Theorem 8 of the main text", ...).
No earlier version file is touched.  Change log: changelog_v29.md.
Provenance ledger: certificate_sha256_v16.txt.
"""
import re
from collections import Counter
from pathlib import Path

V = Path('/home/z/my-project/quantum-circuits/research/versions')
MS = (V / 'manuscript_revised_v28.tex').read_text()
SM = (V / 'supplement_v9.tex').read_text()

# =====================================================================
# MANUSCRIPT: header
# =====================================================================
i_dc = MS.index('\\documentclass')
NEW_HEADER = """% manuscript_revised_v29.tex -- layout-polish + metaphysics + data-availability
% pass (patch_v29_layout_polish.py) of manuscript_revised_v28.tex, which is
% preserved unmodified alongside its predecessors.  Scope of this pass:
% (1) the four column-overflowing tables (IV tab:n5twosize, V
% tab:closingrates, VI tab:smchaar, IX tab:numerics) are promoted from
% single-column floats to two-column-spanning floats (table*), the
% format already used by TABLE I -- tabular bodies byte-identical,
% asserted in the patch script, numbering unaffected;
% (2) the two clipped displays of the closed-form-spectrum proposition
% (eq:QRdef, eq:spinor: parts of their definitions fell outside the
% page box in the v28 rendering) are re-set as multi-line displays with
% every token preserved; the eq:dyadicmoments display is tightened;
% (3) the enumerate of Proposition 13 is detached from the proposition
% header with \\leavevmode (the "(i)" label previously protruded into
% the margin);
% (4) Sec. VII refers to the standing metaphysics as metaphysics
% throughout, established once as the working assumption (author's
% wording), including the introduction's spine entry;
% (5) the data availability statement names preprints.org and states
% formally that the Supplementary Material includes the web simulation.
% Companion this pass: supplement_v10.tex (same-class layout repairs:
% the SMC weight display split, the calibration table promoted to a
% two-column float, the reproduction block re-set as a list, six
% literal label-name references replaced by explicit main-text numbers).
% Change log: changelog_v29.md.
% Provenance ledger: certificate_sha256_v16.txt.
"""
ms = NEW_HEADER + MS[i_dc:]

# =====================================================================
# MANUSCRIPT (1): promote the four overflowing tables to table*
# =====================================================================
def promote(text, label, opener='\\begin{table}[t]'):
    li = text.index(f'\\label{{{label}}}')
    bi = text.rindex(opener, 0, li)
    between = text[bi:li]
    assert '\\end{table}' not in between, f'unbalanced float before {label}'
    text = (text[:bi] + opener.replace('table', 'table*') + text[bi + len(opener):])
    li = text.index(f'\\label{{{label}}}')
    ei = text.index('\\end{table}', li)
    text = text[:ei] + '\\end{table*}' + text[ei + len('\\end{table}'):]
    return text

for lab in ('tab:n5twosize', 'tab:closingrates', 'tab:smchaar', 'tab:numerics'):
    ms = promote(ms, lab)
assert ms.count('\\begin{table*}[t]') == 5      # TABLE I + the four promoted
assert ms.count('\\end{table*}') == 5

# byte-identical tabular bodies: extract each table's tabular block
def tabular_of(text, label):
    li = text.index(f'\\label{{{label}}}')
    i0 = text.index('\\begin{tabular}', li)
    i1 = text.index('\\end{tabular}', li) + len('\\end{tabular}')
    return text[i0:i1]

for lab in ('tab:n5twosize', 'tab:closingrates', 'tab:smchaar', 'tab:numerics'):
    assert tabular_of(ms, lab) == tabular_of(MS, lab), f'tabular changed: {lab}'

# =====================================================================
# MANUSCRIPT (2): re-set the clipped display equations
# =====================================================================
oldQ = """\\begin{equation}
 Q(k)=\\cosh^2\\!2K_d\\,\\cosh 2K_h+\\sinh^2\\!2K_d\\,\\sinh 2K_h-\\sinh 2K_h\\,\\cos k,\\qquad
 R(k)=2\\sinh 2K_d\\,\\cos\\tfrac{k}{2},
 \\label{eq:QRdef}
\\end{equation}"""
newQ = """\\begin{equation}
\\begin{aligned}
 Q(k)&=\\cosh^2\\!2K_d\\,\\cosh 2K_h+\\sinh^2\\!2K_d\\,\\sinh 2K_h\\\\
 &\\quad-\\sinh 2K_h\\,\\cos k,\\\\
 R(k)&=2\\sinh 2K_d\\,\\cos\\tfrac{k}{2},
\\end{aligned}
 \\label{eq:QRdef}
\\end{equation}"""
assert ms.count(oldQ) == 1
ms = ms.replace(oldQ, newQ)

oldS = """\\begin{equation}
 E=\\sinh^m(2K_d)\\,\\bigl[\\cosh K_d\\,\\tilde Y+\\sinh K_d\\,z_m\\tilde Yz_1\\bigr],\\qquad
 \\tilde Y=c\\,e^{K_1x_m}U_{m-1}\\cdots U_1,\\qquad
 U_k=e^{K_dz_kz_{k+1}}\\,c\\,e^{K_1x_k},
 \\label{eq:spinor}
\\end{equation}"""
newS = """\\begin{equation}
\\begin{gathered}
 E=\\sinh^m(2K_d)\\,\\bigl[\\cosh K_d\\,\\tilde Y+\\sinh K_d\\,z_m\\tilde Yz_1\\bigr],\\\\
 \\tilde Y=c\\,e^{K_1x_m}U_{m-1}\\cdots U_1,\\qquad
 U_k=e^{K_dz_kz_{k+1}}\\,c\\,e^{K_1x_k},
\\end{gathered}
 \\label{eq:spinor}
\\end{equation}"""
assert ms.count(oldS) == 1
ms = ms.replace(oldS, newS)

oldD = """ =\\E_\\omega Z_{n,\\omega}(T)=\\bar Z_n(t),\\qquad n=1,2,\\ldots,
 \\label{eq:dyadicmoments}"""
newD = """ =\\E_\\omega Z_{n,\\omega}(T)=\\bar Z_n(t),\\!\\quad n=1,2,\\ldots,
 \\label{eq:dyadicmoments}"""
assert ms.count(oldD) == 1
ms = ms.replace(oldD, newD)

# token-preservation audit for the three equations (every math token of
# the old body occurs in the new body)
for old, new, name in ((oldQ, newQ, 'eq:QRdef'), (oldS, newS, 'eq:spinor')):
    otk = re.findall(r'[A-Za-z\\][A-Za-z@]*|_', old.replace('\\qquad', ''))
    for tk in set(ot for ot in otk if len(ot) > 1):
        assert tk in new, f'token lost from {name}: {tk!r}'

# =====================================================================
# MANUSCRIPT (3): separate the prop:gap enumerate from its header
# =====================================================================
oldE = """\\begin{proposition}[the annealed--quenched record gap]
\\label{prop:gap}
\\begin{enumerate}"""
newE = """\\begin{proposition}[the annealed--quenched record gap]
\\label{prop:gap}
\\leavevmode
\\begin{enumerate}"""
assert ms.count(oldE) == 1
ms = ms.replace(oldE, newE)

# =====================================================================
# MANUSCRIPT (4): metaphysics terminology in Sec. VII + intro spine
# =====================================================================
EDITS = [
 # --- the opening paragraph, author's exact wording ---
 ("\\emph{The standing assumption.}  This section records the working "
  "assumption---the standing metaphysics maintained with this project's "
  "research record---and examines what it implies for the readings of "
  "quantum mechanics.",
  "\\emph{The standing metaphysics.}  This section records the working "
  "assumption maintained with this project's research record and examines "
  "what it implies for the readings of quantum mechanics."),
 ("and the assumption is open to revision by evidence, not by preference."
  "  The assumption is that reality is",
  "and the metaphysics is open to revision by evidence, not by preference."
  "  The metaphysics is that reality is"),
 # --- what it does to the interpretations ---
 ("\\emph{What the assumption does to the interpretations.}",
  "\\emph{What the metaphysics does to the interpretations.}"),
 ("structure that the assumption assigns to appearance",
  "structure that the metaphysics assigns to appearance"),
 ("Under the assumption none of these is a rival ultimate ontology:",
  "Under the metaphysics none of these is a rival ultimate ontology:"),
 ("what the assumption adds is the strict non-duality",
  "what the metaphysics adds is the strict non-duality"),
 # --- non-eliminable division ---
 ("The assumption denies division ultimately;",
  "The metaphysics denies division ultimately;"),
 ("The parallel with the assumption's absence of an external vantage "
  "point is exact in form and modest in claim",
  "The parallel with the metaphysics having no external vantage point "
  "is exact in form and modest in claim"),
 ("The theorem does not prove the assumption; it marks, inside physics, "
  "the same boundary that the assumption draws absolutely.",
  "The theorem does not prove the metaphysics; it marks, inside physics, "
  "the same boundary that the metaphysics draws absolutely."),
 # --- the one and the many ---
 ("the assumption takes it as one appearing as many",
  "the metaphysics takes it as one appearing as many"),
 # --- virtuous circularity ---
 ("The assumption's circularity thesis---any account of the Absolute is "
  "self-referential because there is no external vantage point---has a "
  "methodological echo in this paper's exactness program.",
  "The circularity thesis of the metaphysics---any account of the "
  "Absolute is self-referential because there is no external vantage "
  "point---has a methodological echo in this paper's exactness program."),
 ("That is the quantitative form of the assumption's circularity: not a "
  "loop of dependence, but self-consistency made checkable.",
  "That is the quantitative form of that circularity: not a loop of "
  "dependence, but self-consistency made checkable."),
 # --- reconciliation ---
 ("The work and the assumption do not compete.  The assumption locates "
  "the referent",
  "The work and the metaphysics do not compete.  The metaphysics locates "
  "the referent"),
 ("nothing in the assumption contradicts an exact phenomenal grammar",
  "nothing in the metaphysics contradicts an exact phenomenal grammar"),
 ("The assumption frames the work; the theorems carry it;",
  "The metaphysics frames the work; the theorems carry it;"),
 # --- the introduction's spine entry describing Sec. VII ---
 ("Sec.~\\ref{sec:interpretation} states the standing interpretive "
  "assumption and its reconciliation conditions;",
  "Sec.~\\ref{sec:interpretation} states the standing metaphysics and "
  "its reconciliation conditions;"),
]
for old, new in EDITS:
    assert ms.count(old) == 1, f'edit anchor not unique: {old[:70]!r}'
    ms = ms.replace(old, new)

# Sec. VII audit: exactly ONE 'assumption' survives (the working
# assumption of the opening sentence)
i7 = ms.index('\\section{Interpretive status of the record formalism}')
i8 = ms.index('\\section{Conclusion}')
sec7 = ms[i7:i8]
n_assump = len(re.findall(r'assumption', sec7))
n_metaph = len(re.findall(r'metaphysics', sec7))
assert n_assump == 1, f'Sec. VII must keep exactly 1 "assumption", has {n_assump}'
assert n_metaph == 17, f'Sec. VII expected 17 "metaphysics", has {n_metaph}'
assert "The standing metaphysics.}  This section records the working assumption maintained" in sec7
# outside Sec. VII, the only visible 'assumption's left are the
# mathematical ones (self-averaging assumption): v28 had 2 visible
# occurrences outside Sec. VII (the intro spine entry + the
# mathematical one); v29 has exactly the mathematical one.
outside_vis = [l for l in (ms[:i7] + ms[i8:]).splitlines()
               if l.strip() and not l.lstrip().startswith('%')]
n_out = sum('assumption' in l for l in outside_vis)
assert n_out == 1, f'visible "assumption" outside Sec. VII expected 1, got {n_out}'
assert any('self-averaging assumption' in l for l in outside_vis)

# =====================================================================
# MANUSCRIPT (5): data availability statement
# =====================================================================
oldDA = ("are deposited on figshare (DOI to be assigned prior to "
         "submission).")
newDA = ("are deposited on preprints.org (DOI to be assigned prior to "
         "submission).  The Supplementary Material includes the web "
         "simulation of the monitored circuits: an interactive "
         "stabilizer-tableau simulator of the Clifford dynamics of "
         "Appendix~\\ref{app:numerics}, with the finite-size-scaling "
         "benchmark, the annealed replica chain, and the record SCGF "
         "analyses of the paper presented in interactive form.")
assert ms.count(oldDA) == 1
ms = ms.replace(oldDA, newDA)
assert ms.count('figshare') == 0
assert 'preprints.org' in ms and 'web simulation' in ms
# the deposited-artifact list is preserved verbatim:
for keep in ('release\\_checksums.sha256', 'certificate\\_sha256.txt',
             'npz', 'app:rank3', 'app:numerics'):
    assert keep in ms

# =====================================================================
# MANUSCRIPT: line-multiset no-content-loss audit (house protocol).
# Float-environment lines are structural (verified separately by the
# byte-identical tabular checks) and are excluded from the audit.
STRUCTURAL = {'\\begin{table}[t]', '\\begin{table*}[t]',
              '\\begin{table}[ht]', '\\end{table}', '\\end{table*}'}

EDITED_MARKERS = [
    ' Q(k)=\\cosh^2\\!2K_d',                       # eq:QRdef re-set (l.1)
    ' R(k)=2\\sinh 2K_d\\,\\cos\\tfrac{k}{2},',       # eq:QRdef re-set (l.2)
    ' E=\\sinh^m(2K_d)',                           # eq:spinor re-set
    '=\\E_\\omega Z_{n,\\omega}(T)=\\bar Z_n(t),\\qquad n=1,2,\\ldots,',  # dyadic
    'The standing assumption',                    # Sec. VII opening (l.1711)
    'What the assumption does to the interpretations',            # l.1713
    'The assumption denies division',             # l.1715
    'the assumption takes it as one appearing as many',          # l.1719
    "The assumption's circularity thesis",       # l.1721
    'The work and the assumption do not compete',                # l.1723
    'states the standing interpretive assumption',               # intro spine
    'deposited on figshare',                      # data availability
]


def visible(text):
    return [l for l in text.splitlines()
            if l.strip() and not l.lstrip().startswith('%')
            and l.strip() not in STRUCTURAL]


c28, c29 = Counter(visible(MS)), Counter(visible(ms))
removed = Counter()
for m in EDITED_MARKERS:
    hits = [l for l in c28 if m in l]
    assert len(hits) == 1, f'edited marker not unique: {m[:60]!r}'
    removed[hits[0]] = c28[hits[0]]
lost = {l: n for l, n in (c28 - removed).items() if c29[l] < n}
assert not lost, f'CONTENT LOSS: {list(lost)[:3]}'
print(f"manuscript line-multiset audit PASS: {sum(c28.values())} visible "
      f"v28 lines, {sum(removed.values())} deliberately edited, "
      f"{sum(c29.values())} visible v29 lines")

# =====================================================================
# SUPPLEMENT: header
# =====================================================================
i_dc_s = SM.index('\\documentclass')
NEW_S_HEADER = """% supplement_v10.tex -- layout-repair pass
% (patch_v29_layout_polish.py) of supplement_v9.tex, which is preserved
% unmodified.  Same pass as the manuscript v29: (1) the SMC weight
% display of Sec. S6 is split into two align lines (its last term fell
% outside the page box in the v9 rendering; every token preserved);
% (2) the calibration table (tabS:calib) is promoted to a
% two-column-spanning float (tabular byte-identical); (3) the
% reproduction command/purpose block of Sec. S6 is re-set as an
% itemized list (the centered tabular previously rendered on top of
% the neighbouring column's text); (4) six literal label-name
% references are replaced by the explicit numbers of the main text
% (Remark 7, Proposition 13, Tables IV/V/VII, Eqs. (55)/(87)/(14)),
% following the convention already used elsewhere in this supplement.
% Provenance ledger: certificate_sha256_v16.txt.
"""
sm = NEW_S_HEADER + SM[i_dc_s:]

# =====================================================================
# SUPPLEMENT (6): split the SMC weight display
# =====================================================================
oldSMC = """\\begin{align}
 m_t&=\\max_i\\ell_t^i,\\qquad
 \\log c_t=m_t+\\log\\Bigl(\\frac1N\\sum_i e^{\\ell_t^i-m_t}\\Bigr),\\qquad
 \\bar w_t^i=\\frac{e^{\\ell_t^i-m_t}}{\\sum_j e^{\\ell_t^j-m_t}},\\nonumber
\\end{align}"""
newSMC = """\\begin{align}
 m_t&=\\max_i\\ell_t^i,\\qquad
 \\log c_t=m_t+\\log\\Bigl(\\frac1N\\sum_i e^{\\ell_t^i-m_t}\\Bigr),\\nonumber\\\\
 \\bar w_t^i&=\\frac{e^{\\ell_t^i-m_t}}{\\sum_j e^{\\ell_t^j-m_t}},\\nonumber
\\end{align}"""
assert sm.count(oldSMC) == 1
sm = sm.replace(oldSMC, newSMC)
for tk in ('\\max_i\\ell_t^i', '\\log c_t=m_t+\\log\\Bigl(\\frac1N\\sum_i '
           'e^{\\ell_t^i-m_t}\\Bigr)', '\\bar w_t^i=\\frac{e^{\\ell_t^i-m_t}}'
           '{\\sum_j e^{\\ell_t^j-m_t}}'):
    assert (tk.replace(' ', '').replace('&', '')
            in sm.replace(' ', '').replace('&', '')), f'SMC token lost: {tk!r}'

# =====================================================================
# SUPPLEMENT (7): promote the calibration table
# =====================================================================
sm = promote(sm, 'tabS:calib')
assert sm.count('\\begin{table*}[t]') == 7          # six existing + one new
assert tabular_of(sm, 'tabS:calib') == tabular_of(SM, 'tabS:calib')

# =====================================================================
# SUPPLEMENT (8): reproduction block as an itemized list
# =====================================================================
oldRP = """Reproduction (from the \\texttt{research/scripts/} directory):
\\begin{center}
\\begin{tabular}{ll}
command & purpose\\\\
\\hline
\\texttt{python3 mipt\\_scgf\\_exact.py} & the $3^L$ evolution: calibration,
anchors, $A(L)$ tails (Table~\\ref{tabS:calib},~\\ref{tabS:anchors})\\\\
\\texttt{python3 mipt\\_born\\_scgf.py} & the trajectory suite: validation,
production ladder, ESS, tilted densities
(Table~\\ref{tabS:ladder})\\\\
\\end{tabular}
\\end{center}"""
newRP = """Reproduction (from the \\texttt{research/scripts/} directory):
\\begin{itemize}
\\item \\texttt{python3 mipt\\_scgf\\_exact.py} --- the $3^L$ evolution:
calibration, anchors, $A(L)$ tails
(Table~\\ref{tabS:calib},~\\ref{tabS:anchors});
\\item \\texttt{python3 mipt\\_born\\_scgf.py} --- the trajectory suite:
validation, production ladder, ESS, tilted densities
(Table~\\ref{tabS:ladder}).
\\end{itemize}"""
assert sm.count(oldRP) == 1
sm = sm.replace(oldRP, newRP)
assert '\\begin{center}' not in sm
for tk in ('python3 mipt\\_scgf\\_exact.py', 'python3 mipt\\_born\\_scgf.py',
           'calibration,', 'anchors, $A(L)$ tails', 'production ladder, ESS, '
           'tilted densities'):
    assert tk in newRP

# =====================================================================
# SUPPLEMENT (9): literal label references -> explicit main-text numbers
# =====================================================================
REFS = [
 ("(the identification of Remark rem:cliff3design),",
  "(the identification of Remark~7 of the main text),"),
 ("Prop.~prop:z3closure on the compressed bond space",
  "Proposition~13 of the main text on the compressed bond space"),
 ("cells ($t=4L$): Table tab:z3exact of the main text.",
  "cells ($t=4L$): Table~VII of the main text."),
 ("The results are quoted in the main text (Prop.~prop:z3closure).",
  "The results are quoted in the main text (Proposition~13)."),
 ("main-text table (Table tab:n5twosize) into the dual effective closing",
  "main-text table (Table~IV) into the dual effective closing"),
 ("rates quoted in the main text (Table tab:closingrates): per",
  "rates quoted in the main text (Table~V): per"),
 ("closed form of the Burnside deficit, Eq.~(rank3)",
  "closed form of the Burnside deficit, Eq.~(55) of the main text"),
 ("the main-text Eq.~(dyadicmoments) and is in",
  "the main-text Eq.~(87) and is in"),
 ("$W_{p,n}$ of Eq.~(Wpn), the group utilities,",
  "$W_{p,n}$ of Eq.~(14) of the main text, the group utilities,"),
 ("is included in the deposit, exactly following Eq.~(Wpn) (inverse of the",
  "is included in the deposit, exactly following Eq.~(14) of the main "
  "text (inverse of the"),
]
for old, new in REFS:
    assert sm.count(old) == 1, f'supplement ref anchor not unique: {old[:60]!r}'
    sm = sm.replace(old, new)

# no literal label names remain outside \ref/\label/\eqref (Eq.~(A1) and
# the S-numbered internal refs are legitimate):
lit = [ln for ln in sm.splitlines()
       if not ln.lstrip().startswith('%')
       and re.search(r'(?<!\\ref{)(?<!\\eqref{)(?<!\\label{)\b'
                     r'(tab|prop|rem|eq|app|sec|thm|fig|sm):[A-Za-z0-9_]+',
                     ln)]
assert not lit, f'literal label names remain: {lit[:3]}'

# =====================================================================
# SUPPLEMENT: line-multiset no-content-loss audit (structural lines --
# float environments, \hline, list/tabular delimiters -- are excluded;
# they are verified by the byte-level checks above)
# =====================================================================
SM_STRUCTURAL = {'\\begin{table}[t]', '\\begin{table*}[t]',
                 '\\begin{table}[h]', '\\end{table}', '\\end{table*}',
                 '\\hline', '\\begin{center}', '\\end{center}',
                 '\\begin{tabular}{ll}', '\\begin{tabular}{lllll}',
                 '\\end{tabular}', '\\begin{itemize}', '\\end{itemize}'}


def visible_s(text):
    return [l for l in text.splitlines()
            if l.strip() and not l.lstrip().startswith('%')
            and l.strip() not in SM_STRUCTURAL]


SM_EDITED = [
    ' \\log c_t=m_t+\\log\\Bigl(\\frac1N\\sum_i e^{\\ell_t^i-m_t}\\Bigr),\\qquad',
    ' \\bar w_t^i=\\frac{e^{\\ell_t^i-m_t}}{\\sum_j e^{\\ell_t^j-m_t}},\\nonumber',
    'command & purpose',                            # replaced header row
    '\\texttt{python3 mipt\\_scgf\\_exact.py} & the $3^L$ evolution',
    '\\texttt{python3 mipt\\_born\\_scgf.py} & the trajectory suite',
    'production ladder, ESS, tilted densities',     # rewrapped
    'anchors, $A(L)$ tails (Table~\\ref{tabS:calib}',
    '(Table~\\ref{tabS:ladder})',                   # rewrapped
    '$1.6\\times10^{-14}$ (the identification of Remark rem:cliff3design)',
    'Prop.~prop:z3closure on the compressed bond space',
    'cells ($t=4L$): Table tab:z3exact of the main text.',
    'The results are quoted in the main text (Prop.~prop:z3closure).',
    'main-text table (Table tab:n5twosize) into the dual effective closing',
    'rates quoted in the main text (Table tab:closingrates): per',
    'closed form of the Burnside deficit, Eq.~(rank3)',
    'the main-text Eq.~(dyadicmoments) and is in',
    '$W_{p,n}$ of Eq.~(Wpn), the group utilities,',
    'is included in the deposit, exactly following Eq.~(Wpn) (inverse of the',
]
c9, c10 = Counter(visible_s(SM)), Counter(visible_s(sm))
removed = Counter()
for m in SM_EDITED:
    hits = [l for l in c9 if m in l]
    assert len(hits) == 1, f'supplement edited marker not unique: {m[:60]!r}'
    removed[hits[0]] = c9[hits[0]]
lost = {l: n for l, n in (c9 - removed).items() if c10[l] < n}
assert not lost, f'SUPPLEMENT CONTENT LOSS: {list(lost)[:3]}'
print(f"supplement line-multiset audit PASS: {sum(c9.values())} visible "
      f"v9 lines, {sum(removed.values())} deliberately edited, "
      f"{sum(c10.values())} visible v10 lines")

# =====================================================================
# final submission-cleanliness scan (house protocol)
# =====================================================================
FORBIDDEN = ['TODO', 'FIXME', 'XXX', 'placeholder', 'absolute.txt',
             'campaign', 'queue', 'driver', 'watch ', 'rollback', 'cron',
             'worklog', 'OOM', 'sandbox', 'diary', 'chat ', 'changelog',
             'figshare']
for name, text in (('manuscript', ms), ('supplement', sm)):
    tvis = "\n".join(l for l in text.splitlines()
                     if not l.lstrip().startswith('%'))
    hits = [t for t in FORBIDDEN if t in tvis]
    assert not hits, f'{name} forbidden tokens: {hits}'
print("forbidden-token scan PASS (manuscript + supplement)")

(V / 'manuscript_revised_v29.tex').write_text(ms)
(V / 'supplement_v10.tex').write_text(sm)
print(f"written: manuscript_revised_v29.tex ({len(ms)} chars; "
      f"v28 was {len(MS)} chars)")
print(f"written: supplement_v10.tex ({len(sm)} chars; "
      f"v9 was {len(SM)} chars)")
print("PATCH OK")
