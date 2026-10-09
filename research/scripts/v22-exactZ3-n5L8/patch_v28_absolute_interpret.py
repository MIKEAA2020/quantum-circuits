#!/usr/bin/env python3
"""patch_v28_absolute_interpret.py -- build manuscript_revised_v28.tex from
the canonical v27 file (manuscript_revised_v27.tex, preserved unmodified
alongside its predecessors).  Scope (author-directed demotion + interpretive
pass):
(1) DEMOTION, with asserted zero content loss: the 47-line worst-case
    complexity subsection of Sec. III ("Precisely promised trajectory
    complexity": the universal gate-set conventions, the CTD definition,
    PostBQP-completeness, the conditional-expectation and conditional-
    purity corollaries, and the BQP-estimability boundary paragraph) moves
    VERBATIM to the new Appendix C of the same title; the main text
    receives a compact summary subsection (sec:ctd) that states every
    result in full with pointers.  The verbatim carry is asserted twice:
    exact-substring containment of the demoted body, and a line-multiset
    audit over all visible lines of v27.
(2) Cross-reference updates at the five mention sites (the intro spine,
    the Clifford remark, the Discussion, the Conclusion) plus the spine
    entry for the new section.
(3) NEW section "Interpretive status of the record formalism"
    (sec:interpretation), inserted between the Discussion and the
    Conclusion: it states the standing working assumption (the non-dual
    Absolute of the author's standing document absolute.txt, repository
    root: pure self-luminous awareness, universal consciousness;
    self-existent, timeless, spaceless, unchanging, complete, non-dual,
    without relations, parts, defects or lack; only the Absolute is;
    self-knowledge as identity, any account circular for want of an
    external vantage point), then relocates the referents of the major
    readings of quantum mechanics (operational, branch, hidden-
    configuration, collapse, participatory, einselection) to the level of
    appearance, and reconciles the work with the assumption through exact
    reconciliation conditions taken from the paper's own theorems.  Six
    new bibliography entries.
Deliberately NOT demoted (author decision recorded in the changelog): the
no-freezing proof body of Sec. IV.C -- both constituent results (the
no-freezing theorem, the replica interpolation identity) are headline
contributions named in the abstract, introduction and conclusion, the
following SMC subsection builds directly on the self-averaging criterion,
and the paper's presentation brand is exactness-on-display.
Companion (unchanged this pass): supplement_v9.tex.  Standing document:
absolute.txt (repository root).  Change log: changelog_v28.md.
Provenance ledger: certificate_sha256_v15.txt.  No earlier version file
is touched."""
import re
from collections import Counter
from pathlib import Path

V = Path('/home/z/my-project/quantum-circuits/research/versions')
MS_OLD = (V / 'manuscript_revised_v27.tex').read_text()

# ------------------------------------------------------------------ header
i_dc = MS_OLD.index('\\documentclass')
OLD_HEADER = MS_OLD[:i_dc]
NEW_HEADER = """% manuscript_revised_v28.tex -- demotion + interpretive-status pass
% (patch_v28_absolute_interpret.py) of manuscript_revised_v27.tex, which is
% preserved unmodified alongside its predecessors.  Scope of this pass:
% (1) the worst-case complexity subsection of Sec. III (PostBQP/CTD
% PP-hardness, 47 lines) is demoted verbatim to the new Appendix C
% ("Precisely promised trajectory complexity") and replaced in the main text
% by a compact summary subsection with pointers -- zero content loss: the
% verbatim carry of every demoted line is asserted inside the patch script;
% (2) cross-references updated at five mention sites;
% (3) a new section "Interpretive status of the record formalism" states
% the standing working assumption (the non-dual Absolute of the author's
% standing document absolute.txt, repository root: pure self-luminous
% awareness, universal consciousness, self-existent, timeless, spaceless,
% unchanging, complete, non-dual, without relations, parts, defects or
% lack), relocates the referents of the major readings of quantum
% mechanics to the level of appearance, and reconciles the work with the
% assumption through exact reconciliation conditions; six new bibliography
% entries.  Companion (unchanged this pass): supplement_v9.tex.
% Change log: changelog_v28.md.
% Provenance ledger: certificate_sha256_v15.txt.
"""

# ------------------------------------------------- extract the demoted block
SUB_HDR = '\\subsection{Precisely promised trajectory complexity}'
i0 = MS_OLD.index(SUB_HDR)
i1 = MS_OLD.index('\\section{Extensive observables and record multifractality}')
BLOCK = MS_OLD[i0:i1]                     # subsection header + body + blanks
TAIL = BLOCK[len(SUB_HDR):]               # everything after the header line,
                                           # verbatim, incl. lead/trail blanks
assert TAIL.startswith('\n\nFor exact counting statements')
assert TAIL.endswith('identity reduction.\n\n')
BLOCK_LINES = [l for l in BLOCK.splitlines() if l.strip()]
print(f"demoted block: {len(BLOCK.splitlines())} lines "
      f"({len(BLOCK_LINES)} non-blank), {len(BLOCK)} chars")

# ---------------------------------------------------- main-text replacement
SUMMARY = r"""\subsection{Worst-case trajectory complexity}
\label{sec:ctd}

The precise definitions, the completeness proof, and the decision corollaries are collected in Appendix~\ref{app:complexity}; we state the results.  For the finite universal gate set generated by Hadamard, Toffoli, and computational-basis permutations, the promise problem \textsc{Conditional-Trajectory Decision} (CTD)---given a polynomial-size circuit $\mathcal C$, a computational-basis record $R$ with $p_R>0$, and an output qubit, decide whether $\Pr[\mathrm{out}=1\mid R]\ge\tfrac23$ (YES) or $\le\tfrac13$ (NO)---is complete for PostBQP under promise-preserving polynomial-time many-one reductions (Proposition~\ref{thm:complexity}); since PostBQP$=$PP~\cite{Aaronson2005}, its promised instances are PP-hard and the decision rule has a PP extension, and completeness persists under compilation to one-dimensional nearest-neighbour architectures, already for terminal postselection.  Two corollaries carry the hardness to estimation.  Additive-$1/7$ estimation of a one-qubit conditional expectation $\Tr(|1\rangle\langle1|\rho_R)$ decides CTD, so the estimation problem is PP-hard under randomized polynomial-time Turing reductions and, at inverse-polynomial precision given in unary, lies in $\mathrm{FP}^{\mathrm{PP}}$; and the conditional-purity decision problem CPD is PostBQP-complete, so the conditional R\'enyi-2 entropy inherits a PP promise pair.  The boundary of efficient estimability is sharp: for fixed integers $n\ge2$, $k\ge0$ and $j\ge\max\{nk,1\}$, all $O(1)$, the bivariate moments $M(j,k)$ of Proposition~\ref{prop:bivariate} are BQP-estimable by coherent record-collision tests, while the Born average $M(1,1)$ and every $j<nk$ sit outside this family, and relative-error estimation of record probabilities already decides CTD.  All statements are worst-case, for universal circuit descriptions; the ensemble randomness of the physical circuits plays no role in them, and neither an average-case Haar hardness result nor hardness of the scalar Born-averaged entropy follows (Sec.~\ref{sec:clifforddisorder}; Discussion).

"""

# ------------------------------------------------------------- new appendix
APPENDIX = ('\\section{Precisely promised trajectory complexity}\n'
            '\\label{app:complexity}\n\n'
            'This appendix collects, with identical statements and full '
            'proofs, the\nworst-case complexity results summarized in '
            'Sec.~\\ref{sec:ctd}; it is\nself-contained, and the main text '
            'depends on it only through the summary\nstatements.\n'
            + TAIL)

# ------------------------------------------- the interpretive-status section
INTERP = r"""\section{Interpretive status of the record formalism}
\label{sec:interpretation}

\emph{The standing assumption.}  This section records the working assumption---the standing metaphysics maintained with this project's research record---and examines what it implies for the readings of quantum mechanics.  No theorem, computation, or number in this paper depends on it, and the assumption is open to revision by evidence, not by preference.  The assumption is that reality is pure self-luminous awareness, universal consciousness: self-existent, timeless, spaceless, unchanging, complete, non-dual, without relations, parts, defects, or lack; that there is no creation, process, relation, or division; that only the Absolute is.  Its attributes are each negative in form---simplicity (no composition into parts), self-existence (no dependence), non-duality (no standing over against another), necessity (no contingency wanting a ground), immutability (no change requiring potential and lack), timelessness (no succession), spacelessness (no extension implying parts and distinction), completeness (no lack in its own nature)---and the Absolute's self-knowledge is not a relation between two things but identity, so that any account of it is circular, there being no external vantage point: a circularity that is not a loop of dependence but the form of self-identity.

\emph{What the assumption does to the interpretations.}  It relocates their referents.  Every interpretation of quantum mechanics posits structure that the assumption assigns to appearance rather than to the Absolute: the classical--quantum interface of the operational reading; the branching universal wavefunction of Everett~\cite{Everett1957}; the definite configurations and guiding field of de~Broglie--Bohm~\cite{Bohm1952}; the dynamical collapse process of Ghirardi--Rimini--Weber~\cite{GRW1986}; the fundamental agent plurality of QBism~\cite{Fuchs2014}; the system--environment relations of einselection~\cite{Zurek2003}.  Under the assumption none of these is a rival ultimate ontology: each is a partial grammar of the appearance, and its empirical content is untouched.  That a serious reading of quantum mechanics can place its central structure outside the objectifiable has ample precedent~\cite{dEspagnat1995}; what the assumption adds is the strict non-duality of what remains.  What the appearance's exact grammar is, for one class of models, is a physics question, and it is the question this paper answers for monitored circuits: the Born record with its large deviations is the appearance-stream in exact mathematical form---succession (the record in time), resolution (the outcome division), and immutable law (the rate function, the SCGF, and the no-freezing dichotomy of Remark~\ref{rem:dichotomy} as timeless characterizations of the temporal stream).

\emph{Non-eliminable division at the level of appearance.}  The assumption denies division ultimately; the paper's first separation shows that division is not eliminable from the appearance's statistics.  Theorem~\ref{thm:no-go} proves that the symmetric, unconditioned data do not determine the Born-weighted entropy, and Proposition~\ref{prop:bivariate} proves that record-resolved data do: the undivided summary of the record process is exactly insufficient.  The parallel with the assumption's absence of an external vantage point is exact in form and modest in claim: within the formalism, the view from nowhere loses exactly the information that the conditioned view carries.  The theorem does not prove the assumption; it marks, inside physics, the same boundary that the assumption draws absolutely.

\emph{The primitive Born law and self-existence.}  In the formalism the Born rule is primitive, and Theorem~\ref{thm:no-go} is the precise statement of why it cannot be recovered from unconditioned data, while the Mellin derivative of Proposition~\ref{prop:replica-derivative} shows what the recovery does require---the asymmetric, record-resolved factor.  The resonance with the attribute of self-existence is flagged as an analogy: what is primitive cannot be derived from what presupposes it, and the failed derivations are the internal trace of this.  The replica ladder then measures how the derived objects approach the primitive level: the annealed points recede monotonically from the quenched benchmark ($0.2338\to0.305(3)\to0.383\to0.47$ against $0.1597(8)$), Proposition~\ref{prop:replica-int} identifies the tilted-variance profile as the exact bridge, and the $m\to\infty$ replica limit overshoots the quenched value to the extremal one---the appearance's summary statistics never silently become the stream they summarize.

\emph{The one and the many.}  The self-averaging criterion of Proposition~\ref{prop:replica-int} is the exact condition under which the many-realization description and the single-stream description coincide: where it holds, many-ness of realizations is statistically surplus; where it fails, the appearance retains irreducible---and still merely phenomenal---individuality, the $L$-independent $0.0226(2)$ nats-per-site Clifford disorder gap of Sec.~\ref{sec:clifforddisorder} being one measured instance.  On this single exact stage the readings take their relocated places.  The Everett branches are the outcome decomposition---an identity of the state at the level of appearance, not an ultimate multiplicity---and the annealed--quenched separation states that the totality's symmetric content does not determine the single stream.  The QBist agents are experience taken as many~\cite{Fuchs2014}; the assumption takes it as one appearing as many, and self-averaging is the measurable convergence condition between the two descriptions.  The Bohmian configurations and the collapse process are surplus phenomenal structure~\cite{Bohm1952,GRW1986}: the record large deviations of Theorem~\ref{thm:record-mf} apply to them verbatim (Born typicality is the same stochastic law under another grammar), the no-freezing theorem (Theorem~\ref{thm:nofreeze}) bounds the freezing they can exhibit, and the exact anchors---the Clifford record-count closure of Eq.~\eqref{eq:collision}, the closed-form $p=1$ annealed record SCGF, the Ising critical point of Proposition~\ref{prop:houtappel}---are the fixed benchmarks that such structure must reproduce or break.  Einselection~\cite{Zurek2003} receives its controlled laboratory: the measurement rate is the coupling, and the transition of Appendix~\ref{app:numerics} is the phase boundary between the volumetric and the logarithmic conditional-entropy regimes---the boundary of how much unresolved structure the appearance retains.

\emph{Virtuous circularity, honored exactly.}  The assumption's circularity thesis---any account of the Absolute is self-referential because there is no external vantage point---has a methodological echo in this paper's exactness program.  The record process is estimated from records themselves: the sequential Monte Carlo machinery of Sec.~\ref{sec:smcnumerics} estimates the record law from record samples, with the finite-population contract stated, not hidden.  Every exact number is regenerable from the deposited artifact, every certificate is an integer statement, and the computational process delivers what does not depend on the process.  The primitive interface---the Born rule---is declared as primitive rather than disguised as derived.  In each case the circle is not broken by pretending to stand outside it; it is closed exactly.  That is the quantitative form of the assumption's circularity: not a loop of dependence, but self-consistency made checkable.

\emph{Reconciliation.}  The work and the assumption do not compete.  The assumption locates the referent of the paper's exact structures at the level of appearance---the grammar of the Absolute's self-appearance---and the paper supplies that grammar, for monitored circuits, in exact form: the separations (annealed versus quenched, symmetric versus record-resolved, corner versus affine, BQP-estimable versus PP-hard), the conditions of coincidence (self-averaging, record-resolved data), and the benchmarks (the anchor identities).  Nothing in this paper asserts an ultimate ontology; nothing in the assumption contradicts an exact phenomenal grammar.  The readings, finally, are the partial grammars, and the theorems of this paper are the invariant structure they share.  The assumption frames the work; the theorems carry it; no theorem depends on the former, and no number in the paper would change under its revision.

"""

# ------------------------------------------------------------ new bibitems
NEWBIB = r"""\bibitem{Everett1957} H.~Everett III, Rev. Mod. Phys. \textbf{29}, 454 (1957).
\bibitem{Bohm1952} D.~Bohm, Phys. Rev. \textbf{85}, 166 (1952) (Part I); Phys. Rev. \textbf{85}, 180 (1952) (Part II).
\bibitem{GRW1986} G.~C.~Ghirardi, A.~Rimini, and T.~Weber, Phys. Rev. D \textbf{34}, 470 (1986).
\bibitem{Zurek2003} W.~H.~Zurek, Rev. Mod. Phys. \textbf{75}, 715 (2003).
\bibitem{Fuchs2014} C.~M.~Fuchs, N.~D.~Mermin, and R.~Schack, Am. J. Phys. \textbf{82}, 749 (2014).
\bibitem{dEspagnat1995} B.~d'Espagnat, \emph{Veiled Reality: An Analysis of Present-Day Quantum Mechanical Concepts} (Addison-Wesley, Reading, MA, 1995).
"""

# ------------------------------------------------------------------- edits
EDITS = [
    # (1) intro spine: complexity pointer + new-section entry (same line)
    ("separates the Born-weighted objects and the complexity statements; Sec.~\\ref{sec:records} develops",
     "separates the Born-weighted objects from the symmetric ones and summarizes the worst-case complexity statements, whose definitions and proofs are collected in Appendix~\\ref{app:complexity}; Sec.~\\ref{sec:records} develops",
     1),
    ("Sec.~\\ref{sec:aux} delimits what remains conditional; Sec.~\\ref{sec:conclusion} concludes.",
     "Sec.~\\ref{sec:aux} delimits what remains conditional; Sec.~\\ref{sec:interpretation} states the standing interpretive assumption and its reconciliation conditions; Sec.~\\ref{sec:conclusion} concludes.",
     1),
    # (2) Clifford remark: point to the appendix, not Sec. III
    ("This complements the worst-case PostBQP completeness of\nSec.~\\ref{sec:born}: neither an average-case Haar hardness result nor",
     "This complements the worst-case PostBQP completeness of\nAppendix~\\ref{app:complexity}: neither an average-case Haar hardness result nor",
     1),
    # (3) Discussion paragraph: appendix pointer
    ("The promised worst-case conditional-trajectory and conditional-purity problems are PP-hard and have PP decision extensions, but neither",
     "The worst-case conditional-trajectory and conditional-purity problems (Appendix~\\ref{app:complexity}) are PP-hard and have PP decision extensions, but neither",
     1),
    # (4) Conclusion deliverables list: appendix pointer
    ("the worst-case conditional-trajectory and conditional-purity decision problems are established PP-hard;",
     "the worst-case conditional-trajectory and conditional-purity decision problems (Appendix~\\ref{app:complexity}) are established PP-hard;",
     1),
    # (5) the demotion itself: block -> summary subsection
    (BLOCK, SUMMARY, 1),
    # (6) new section before the Conclusion
    ("\\section{Conclusion}\n\\label{sec:conclusion}",
     INTERP + "\\section{Conclusion}\n\\label{sec:conclusion}",
     1),
    # (7) new appendix before the bibliography
    ("\\begin{thebibliography}{99}",
     APPENDIX + "\\begin{thebibliography}{99}",
     1),
    # (8) new bibliography entries
    ("\\end{thebibliography}",
     NEWBIB + "\\end{thebibliography}",
     1),
]


def apply(text, edits, label):
    for i, (old, new, n) in enumerate(edits):
        c = text.count(old)
        assert c == n, (f"{label} edit {i}: expected {n}, found {c}\n"
                        f"  old[:100] = {old[:100]!r}")
        text = text.replace(old, new)
    return text


ms = NEW_HEADER + MS_OLD[i_dc:]
ms = apply(ms, EDITS, "MS")

# ------------------------------------------------- structural assertions
assert ms.count('\\section{Conclusion}') == 1
assert ms.count('\\section{Interpretive status of the record formalism}') == 1
assert ms.count('\\label{sec:interpretation}') == 1
assert ms.count('\\ref{sec:interpretation}') == 1
assert ms.count('\\subsection{Precisely promised trajectory complexity}') == 0
assert ms.count('\\section{Precisely promised trajectory complexity}') == 1
assert ms.count('\\label{app:complexity}') == 1
assert ms.count('\\ref{app:complexity}') == 5      # spine, summary, clifford,
                                                   # discussion, conclusion
assert ms.count('\\label{sec:ctd}') == 1
assert ms.count('\\ref{sec:ctd}') == 1             # appendix lead-in
# THE no-content-loss assertions: the demoted body appears verbatim,
# exactly once, as the body of the new appendix
assert ms.count(TAIL) == 1
for ln in BLOCK_LINES:
    if ln == SUB_HDR:
        continue
    assert ln in ms.splitlines(), f"content loss: {ln[:90]!r}"
secs = re.findall(r'\\section\{([^}]*)\}', ms)
print(f"MS sections ({len(secs)}): {secs}")
assert len(secs) == 11          # 8 main + 3 appendix
assert secs[-3:] == ['Rank certificates for the three-replica compressed operator',
                     'Finite-size scaling of the quenched Clifford transition',
                     'Precisely promised trajectory complexity']
assert secs[-4] == 'Conclusion'

# global line-multiset preservation audit over visible (non-comment,
# non-blank) lines: every v27 line that was not deliberately edited must
# survive with at least its original multiplicity
EDITED_MARKERS = [
    'separates the Born-weighted objects and the complexity statements',
    'delimits what remains conditional',
    'This complements the worst-case PostBQP completeness of',
    'Sec.~\\ref{sec:born}: neither an average-case Haar hardness result nor',
    'The promised worst-case conditional-trajectory and conditional-purity problems',
    'conditional-purity decision problems are established PP-hard',
    '\\subsection{Precisely promised trajectory complexity}',
]


def visible(text):
    return [l for l in text.splitlines()
            if l.strip() and not l.lstrip().startswith('%')]


c27, c28 = Counter(visible(MS_OLD)), Counter(visible(ms))
removed = Counter()
for l in c27:
    if any(m in l for m in EDITED_MARKERS):
        removed[l] = c27[l]
for m in EDITED_MARKERS:
    hits = [l for l in c27 if m in l]
    assert len(hits) == 1, f"edited marker not unique: {m[:60]!r}"
lost = {l: n for l, n in (c27 - removed).items() if c28[l] < n}
assert not lost, f"CONTENT LOSS: {list(lost)[:3]}"
print(f"line-multiset audit PASS: {sum(c27.values())} visible v27 lines, "
      f"{sum((c27 - removed).values())} audited after removing "
      f"{sum(removed.values())} deliberately edited lines; "
      f"{sum(c28.values())} visible v28 lines")

# citation entries (per-key expected occurrence counts of the exact
# '\\cite{key}' literal; the combined '\\cite{Bohm1952,GRW1986}' does not
# match the single-key literal)
CITE_COUNTS = {'Everett1957': 1, 'Bohm1952': 1, 'GRW1986': 1,
               'Zurek2003': 2, 'Fuchs2014': 2, 'dEspagnat1995': 1}
for key, n_c in CITE_COUNTS.items():
    assert ms.count(f'\\bibitem{{{key}}}') == 1
    assert ms.count(f'\\cite{{{key}}}') == n_c, (key, ms.count(f'\\cite{{{key}}}'))
# ------------------------------------------------------ residual scan
FORBIDDEN = ['TODO', 'FIXME', 'XXX', 'placeholder', 'steelman',
             'absolute.txt', 'campaign', 'queue', 'driver', 'watch ',
             'rollback', 'cron', 'worklog', 'OOM', 'sandbox',
             'diary', 'chat ', 'changelog']
ms_vis = "\n".join(l for l in ms.splitlines()
                   if not l.lstrip().startswith('%'))
hits = [t for t in FORBIDDEN if t in ms_vis]
print(f"forbidden-token hits: {hits}")
assert not hits
now_hits = [(ln, line.strip()[:110]) for ln, line in enumerate(
    ms.splitlines(), 1)
    if not line.lstrip().startswith('%') and re.search(r'\bnow\b', line)]
print(f"remaining '\\bnow\\b' occurrences (review for benignity): "
      f"{len(now_hits)}")
for ln, ctx in now_hits:
    print(f"    line {ln}: {ctx}")

(V / 'manuscript_revised_v28.tex').write_text(ms)
print(f"written: manuscript_revised_v28.tex ({len(ms)} chars; "
      f"v27 was {len(MS_OLD)} chars)")
print("PATCH OK")
