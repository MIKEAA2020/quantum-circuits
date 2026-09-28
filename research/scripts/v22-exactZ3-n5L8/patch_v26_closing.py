#!/usr/bin/env python3
"""patch_v26_closing.py -- build manuscript_revised_v26.tex + supplement_v8.tex
from the canonical v25 files (manuscript_revised_v25_tjp.tex + supplement_v7.tex,
both preserved unmodified; the parallel instance's coordination claim in the
worklog reserved v26 for the compute-extension promotion, which this pass
delivers).  Content: the dual effective closing rates of the two-phase gap
(the interface-tension extraction from the deposited size ladder) as a new
table + two paragraphs in Sec. II.G; one abstract clause; one last-digit
correction (6*0.806 = 4.836, "4.85" -> "4.84", two sites); two Conclusion
extension sentences; and two new Supplement paragraphs (the extraction
protocol; the d=3 local-dimension extension -- validation and the deposited
locator scans).  Every replacement is asserted to occur the stated number of
times.  No earlier version file is touched."""
import re
from pathlib import Path

V = Path('/home/z/my-project/quantum-circuits/research/versions')
MS_OLD = (V / 'manuscript_revised_v25_tjp.tex').read_text()
SM_OLD = (V / 'supplement_v7.tex').read_text()

MS_HEADER_OLD = """% manuscript_revised_v25_tjp.tex -- Turkish Journal of Physics targeting pass
% (patch_v25_tjp.py) of manuscript_revised_v24.tex, preserved unmodified alongside
% its predecessors.  Scope of this pass: dedicated Conclusion section added before
% the Declarations; the Discussion's unresolved-questions paragraph split into five
% readable paragraphs; label added to the conditional-continuum conjecture; the
% Introduction's logical spine now points to the Conclusion.  No physics content
% changed; every number verbatim from v24 and the deposited results.  Companion:
% supplement_v7.tex (unchanged by this pass).  Change log: changelog_v25.md.
% Provenance ledger: certificate_sha256_v12.txt.
"""

MS_HEADER_NEW = r"""% manuscript_revised_v26.tex -- closing-rate diagnostics pass (patch_v26_closing.py)
% of manuscript_revised_v25_tjp.tex, which is preserved unmodified alongside its
% predecessors (v25 = the TJP editorial pass by the parallel instance; v26 was
% reserved by the worklog coordination claim for the compute-extension promotion).
% Scope of this pass: the dual effective closing rates of the two-phase gap -- the
% interface-tension (sigma_eff) and power-law (alpha_eff) readings of the deposited
% size-ladder values -- as a new table and two paragraphs in Sec. II.G; one abstract
% clause; one last-digit correction (6*0.806 = 4.836, quoted "4.85" -> "4.84", two
% sites); two Conclusion extension sentences (the closing-rate table pointer; the
% deposited d=3 locator scans); Supplement v8 with the extraction protocol and the
% d=3 local-dimension extension.  Companion: supplement_v8.tex (same pass).
% Change log: changelog_v26.md.  Provenance ledger: certificate_sha256_v13.txt.
"""

SM_HEADER_NEW = r"""% supplement_v8.tex -- closing-rate diagnostics pass (patch_v26_closing.py) of
% supplement_v7.tex, which is preserved unmodified.  Same pass as the manuscript:
% two new paragraphs in Sec. S7 (the effective closing rates of the two-phase gap;
% the local-dimension extension at d=3 -- block-route validation and the deposited
% locator scans).  Provenance ledger: certificate_sha256_v13.txt.
"""

RATES_TABLE = r"""\begin{table}[t]
\caption{Effective closing rates of the two-phase gap at the coexistence locators, computed from the size-ladder values of Table~\ref{tab:n5twosize} (the $n=3$ $L=10$ rate from the deposited envelope value $10\,\mathrm{gap}_{12}=6.21$).  $\sigma_{\rm eff}=\tfrac{1}{\Delta L}\log[\mathrm{gap}_{12}(L)/\mathrm{gap}_{12}(L{+}\Delta L)]$ is the exponential (interface-tension) reading; $\alpha_{\rm eff}=\log[\mathrm{gap}_{12}(L)/\mathrm{gap}_{12}(L{+}\Delta L)]/\log[(L{+}\Delta L)/L]$ the power-law reading, per consecutive-size pair ($\Delta L=2$).  At matched intervals both rates rise monotonically with $n$; at $n=3$ they decay with size as a continuous transition requires, at $n=4$ they sit at the marginal level, and at $n=5$ they stay above it.  Extraction script and cross-checks: Supplemental Material~\cite{SM}, Sec.~S7.}
\label{tab:closingrates}
\begin{ruledtabular}
\begin{tabular}{lccc}
 & $n=3$ ($p=0.30$) & $n=4$ ($p=0.38$) & $n=5$ ($p=0.47$) \\
\colrule
$\sigma_{\rm eff}$, $L{=}4\to6$ & $0.297$ & $0.331$ & $0.376$ \\
$\sigma_{\rm eff}$, $L{=}6\to8$ & $0.187$ & $0.214$ & $0.258$ \\
$\sigma_{\rm eff}$, $L{=}8\to10$ & $0.137$ & --- & --- \\
$\alpha_{\rm eff}$, $L{=}4\to6$ & $1.466$ & $1.632$ & $1.857$ \\
$\alpha_{\rm eff}$, $L{=}6\to8$ & $1.297$ & $1.489$ & $1.794$ \\
$\alpha_{\rm eff}$, $L{=}8\to10$ & $1.224$ & --- & --- \\
\end{tabular}
\end{ruledtabular}
\end{table}

The same three sizes admit a dual reading as effective rates (Table~\ref{tab:closingrates}).  If the closing were asymptotically exponential---the tunnelling picture of Remark~\ref{rem:whyqn}---then $\sigma_{\rm eff}$ would converge to the interface tension in units of the ring length; if it were a power law, $\alpha_{\rm eff}$ would converge to its exponent.  At matched sizes both readings rise monotonically across replica number, and the $n=3$ control behaves as a continuous transition must: $\sigma_{\rm eff}$ decays toward zero with size while $L\,\mathrm{gap}_{12}$ saturates, so $\alpha_{\rm eff}$ drifts down toward the value a saturating envelope implies.  At $n=4$ the closing sits at the marginal level over $L=6\to8$ ($\alpha_{\rm eff}=1.489$), and at $n=5$ it is above it at every measured interval.

Three sizes do not yet separate the two asymptotics at $n=5$, and the honest statement is directional: every matched-size rate is super-continuous and $n$-monotone, the level ordering continuous $<$ marginal $<$ first-order persists in both readings, and the accessible sizes sit in the crossover region that $q>4$ Potts systems also display before their asymptotic exponential regime.  The rates add to the size-ladder test a second, model-free summary of the same deposits, and they are the quantities a finite-size extraction of the interface tension would converge to if the asymptotic regime were reached.
"""

MS_EDITS = [
    # --- abstract: add the closing-rates clause to the first-order sentence ---
    (r"with the scaled gap falling below the continuous envelope.  We further prove",
     r"with the scaled gap falling below the continuous envelope and dual effective closing rates that separate the continuous, marginal and first-order behaviours at matched sizes.  We further prove",
     1),
    # --- last-digit correction: 6*0.806 = 4.836 -> "4.84" (prose + table, 2 sites) ---
    (r"6.85\to4.85", r"6.85\to4.84", 2),
    # --- Sec. II.G: closing-rates table + two paragraphs before the Scope note ---
    (r"""prediction at the three-size level.
\emph{Scope.}""",
     r"""prediction at the three-size level.

""" + RATES_TABLE + r"""
\emph{Scope.}""",
     1),
    # --- Conclusion: the closing-rate pointer after the ladder sentence ---
    (r"Two sizes alone cannot separate exponential from power-law closing; the three-size ladder does.",
     r"Two sizes alone cannot separate exponential from power-law closing; the three-size ladder does.  Table~\ref{tab:closingrates} makes the same deposits a dual reading---effective interface-tension and power-law rates that separate the continuous, marginal and first-order behaviours at every matched interval.",
     1),
    # --- Conclusion: the deposited d=3 locator status after the extensions sentence ---
    (r"and interface-tension and latent-heat extraction from the deposited eigensystems.",
     r"and interface-tension and latent-heat extraction from the deposited eigensystems.  The interface-tension reading of the deposited size ladder is delivered in Table~\ref{tab:closingrates}, and the $d=3$ locator scans at $L=4$ and $L=6$ are deposited: the gap minimum sits at $p\approx0.85$ at both sizes, and the two-size closing factor is $2.39$ against $2.12$ at $d=2$---the first-order direction strengthens with local dimension (Supplemental Material~\cite{SM}, Sec.~S7).",
     1),
]

SM_EDITS = [
    # --- two new paragraphs at the end of Sec. S7 ---
    (r"""certificate\_sha256\_v10.txt}.

\begin{thebibliography}{9}""",
     r"""certificate\_sha256\_v10.txt}.

\paragraph{Effective closing rates of the two-phase gap.}
\texttt{v25\_sigma\_extract.py} turns the size-ladder values of the
main-text table (Table tab:n5twosize) into the dual effective closing
rates quoted in the main text (Table tab:closingrates): per
consecutive-size pair $L\to L+\Delta L$ ($\Delta L=2$),
$\sigma_{\rm eff}=\Delta L^{-1}\log[\mathrm{gap}_{12}(L)/\mathrm{gap}_{12}(L+\Delta L)]$
(the exponential reading: $\mathrm{gap}_{12}\sim e^{-\sigma L}$ gives
$\sigma_{\rm eff}\to\sigma$, the interface tension in units of the ring
length) and
$\alpha_{\rm eff}=\log[\mathrm{gap}_{12}(L)/\mathrm{gap}_{12}(L+\Delta L)]/\log[(L+\Delta L)/L]$
(the power-law reading: $\mathrm{gap}_{12}\sim L^{-\alpha}$ gives
$\alpha_{\rm eff}\to\alpha$).  The script re-derives every quoted
closing factor and scaled gap from the table values (all cross-checks
pass to rounding) and emits the rate rows; no new computation enters.
The $n=3$ $L=10$ rate uses the envelope value
$10\,\mathrm{gap}_{12}=6.21$ of the deposited $n=3$ chain.

\paragraph{The local-dimension extension ($d=3$).}
The orbit table of the block route is $d$-independent (the symmetry
group acts on bond labels, not on local states), so the same deposited
machinery serves $d=3$: only the per-bond channel $W_{p,n}$ changes,
through the Gram $D=d^2=9$ (generic and invertible at $n=5$).
\texttt{v25\_n5\_L8\_ext\_v1.py} validates the $d=3$ block route
against the unrestricted iterative route at $L=4$ (agreement
$8\times10^{-15}$ at two interior points) and against the exact $p=1$
rank-one anchors $(1/143)^{2\mathrm{nb}}$ at $L=4$ and $L=6$ (relative
error $1.3\times10^{-14}$ and $1.6\times10^{-14}$), then scans the
$\log(\lambda_1/\lambda_2)$ locator at $d=3$ with the same block route
(deposited as \texttt{v25\_n5\_d3\_locator.json}, hashed in
\texttt{certificate\_sha256\_v13.txt}): the interior minimum sits at
$p\approx0.85$ at both $L=4$ (gap $1.482$) and $L=6$ (gap $0.621$), so
the two-phase gap closes by a factor $2.39$ between the first two sizes
at $d=3$---against $2.12$ at $d=2$ at the corresponding locators---and
$6\,\mathrm{gap}_{12}=3.73$ at $L=6$ falls below the $d=2$ value
$4.84$: the first-order direction strengthens with local dimension.
The $L=8$ rung at $d=3$ and a finer $d=2$ locator grid follow the same
chunk-checkpointed block assembly and the same driving protocol as the
deposited rung.

\begin{thebibliography}{9}""",
     1),
]


def apply(text, edits, tag):
    for old, new, count in edits:
        n = text.count(old)
        assert n == count, (
            f"[{tag}] anchor count {n} != {count} for: {old[:90]!r}")
        text = text.replace(old, new)
    return text


def residual_report(text, tag):
    print(f"--- residual-token report [{tag}] (visible lines only) ---")
    hits = 0
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("%"):
            continue
        for pat in [r"\bprevious version\b", r"\bprevious implementation\b",
                    r"\bprevious bracket\b", r"\bis now done\b",
                    r"\bnow supplies\b", r"\bnow computed\b",
                    r"\bnow resolved\b", r"\bnow exists?\b", r"\bnow proves\b",
                    r"\bnow extends\b", r"\bnow measured\b",
                    r"\bnow an exact\b", r"\bnow three-size\b",
                    r"corrected v21", r"v17--v19", r"mis-transcription",
                    r"present revision", r"recovered dataset",
                    r"present memory", r"no longer a prediction",
                    r"placeholder DOI", r"XXXXXXX"]:
            for m in re.finditer(pat, line):
                hits += 1
                print(f"  line {ln}: {pat}: ...{line[max(0,m.start()-40):m.end()+40]}...")
    print(f"  forbidden-token hits: {hits}")
    now_hits = [(ln, line.strip()[:110]) for ln, line in enumerate(text.splitlines(), 1)
                if not line.lstrip().startswith("%") and re.search(r"\bnow\b", line)]
    print(f"  remaining '\\bnow\\b' occurrences (review for benignity): {len(now_hits)}")
    for ln, ctx in now_hits:
        print(f"    line {ln}: {ctx}")


assert MS_OLD.count(MS_HEADER_OLD) == 1
ms = MS_OLD.replace(MS_HEADER_OLD, MS_HEADER_NEW)
sm = SM_OLD.replace(SM_OLD[:SM_OLD.index("\\documentclass")], SM_HEADER_NEW)
ms = apply(ms, MS_EDITS, "MS")
sm = apply(sm, SM_EDITS, "SM")

# structural assertions on the outputs
assert ms.count(r"\section{Conclusion}") == 1
assert ms.count(r"\label{tab:closingrates}") == 1
assert ms.count(r"6.85\to4.84") == 2 and ms.count(r"6.85\to4.85") == 0
secs = re.findall(r"\\section\{([^}]*)\}", ms)
print(f"MS sections ({len(secs)}): {secs}")
sm_paras = re.findall(r"\\paragraph\{([^}]*)\}", sm)
print(f"SM paragraphs: {len(sm_paras)} (last three: {sm_paras[-3:]})")

(V / "manuscript_revised_v26.tex").write_text(ms)
(V / "supplement_v8.tex").write_text(sm)
print(f"written: manuscript_revised_v26.tex ({len(ms)} chars), "
      f"supplement_v8.tex ({len(sm)} chars)")
residual_report(ms, "MS v26")
residual_report(sm, "SM v8")
print("PATCH OK")
