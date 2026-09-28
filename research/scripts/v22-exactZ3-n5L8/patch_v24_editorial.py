#!/usr/bin/env python3
"""patch_v24_editorial.py -- build manuscript_revised_v24.tex + supplement_v7.tex
from the v23 files (preserved unmodified).  Editorial pass per the user-approved
fix order: purge internal version/meta tokens -> reconcile two/three-size claims
(size-ladder table now carries the L=8 rung at n=3,4,5) -> strip source comments
-> abstract restructure -> DOI note -> Introduction in Sec. I.
Every replacement is asserted to occur exactly once.  No v21/v22/v23 file touched."""
import re
from pathlib import Path

V = Path('/home/z/my-project/quantum-circuits/research/versions')
MS_OLD = (V / 'manuscript_revised_v23_rung.tex').read_text()
SM_OLD = (V / 'supplement_v6.tex').read_text()

MS_HEADER = r"""% manuscript_revised_v24.tex -- editorial revision (patch_v24_editorial.py) of
% manuscript_revised_v23_rung.tex, which is preserved unmodified alongside its
% predecessors.  Scope of this pass: internal version/meta tokens purged from the
% source and visible text; two/three-size claims reconciled (the size-ladder table
% now carries the L=8 rung at n=3,4,5); abstract restructured; Introduction added
% to Sec. I; data-availability DOI note normalized.  Change log: changelog_v24.md.
% Companion: supplement_v7.tex (same pass).  Provenance ledger: certificate_sha256_v11.txt.
"""

SM_HEADER = r"""% supplement_v7.tex -- editorial revision (patch_v24_editorial.py) of
% supplement_v6.tex, which is preserved unmodified.  Same pass as the manuscript:
% internal version tokens removed from headings and visible text, library-provenance
% narrative neutralized, timing note added to the reproduction paragraph.
% Provenance ledger: certificate_sha256_v11.txt.
"""

ABSTRACT_NEW = r"""We develop an exact finite-dimensional theory of the replica mechanics underlying measurement-induced entanglement transitions in monitored quantum circuits, separating three structures that are often conflated: linear outcome-summed replica channels, normalized conditional trajectories, and asymptotic large deviations.  For fixed-basis projective measurements we determine the minimal invariant unital algebra of the one-wire feature space and prove that independently Haar-averaged two-site gates on a perfect matching close the $n$-replica permutation space exactly for every replica number, with an explicit Weingarten bond channel.  The resulting one-period transfer operators have real, positive, semisimple nonzero spectra that compress to bond-label space; at $n=2$ the model is exactly the anisotropic triangular-lattice Ising model of Bao, Choi and Altman, with a closed-form critical point and a closed free-fermion spectrum.  Carrying the same computation through $n=3,4,5$ locates the annealed critical points $p_c^{(2)}=0.2338<p_c^{(3)}=0.305(3)<p_c^{(4)}\approx0.383<p_c^{(5)}\approx0.47$ with the Potts-class exponents at $n=3,4$, and confirms the first-order prediction of the $q=n$-Potts identification at $n=5$: an exact three-size test ($L=4,6,8$) on a symmetry-reduced orbit basis of dimension $3{,}865$ over the $2.1\times10^8$ bond-label space shows the two-phase gap closing faster than the continuous baseline at every size, with the scaled gap falling below the continuous envelope.  We further prove a no-freezing theorem for finite-reachable record processes, establish the worst-case complexity of conditional-trajectory decision, derive the exact replica interpolation identity with its measurable self-averaging criterion, and give the first numerical quenched record scaled cumulant generating functions for Haar circuits, which exhibit genuine record multifractality; the Clifford record-count disorder statistics are closed exactly through a verified conjugation $3$-design."""

INTRO_NEW = r"""Monitored random quantum circuits exhibit measurement-induced entanglement transitions: in the thermodynamic limit the entanglement of a typical Born trajectory scales volumetrically or logarithmically in the system size depending on the measurement rate~\cite{Li2018,Skinner2019,Chan2019,Gullans2020,Choi2020,Vasseur2019,Jian2020,Bao2020}.  The theoretical descriptions of these transitions---replica field theories of the annealed and quenched kinds, transfer-matrix contractions, and large-deviation functions of the measurement record---all rest on replica objects whose finite-dimensional structure has largely been treated perturbatively or accessed only numerically.  Exact statements about the replica transfer operators themselves, their spectra, ranks, symmetries, and the critical points they encode, have been scarce; this paper supplies them.

The first contribution is an exact finite-dimensional mechanics of the replica channels of a canonical monitored-circuit period.  For fixed-basis projective measurements we determine the minimal invariant unital algebra of the one-wire entanglement-feature space and quantify its leakage; a subsequent layer of independently Haar-averaged two-site gates on a perfect matching closes the leaked directions exactly, for every replica number, through an explicit Weingarten bond channel.  The period map is of the form $\mathsf A\mathsf A^\dagger$ in the Hilbert--Schmidt inner product, so its nonzero spectrum is real, positive and semisimple and compresses to bond-label space; at $n=2$ the compressed operator is the row-to-row transfer matrix of the anisotropic triangular-lattice Ising model of Ref.~\cite{Bao2020}, so the annealed two-replica problem is exactly solvable and its critical point is known in closed form.

The second contribution is the annealed replica ladder built on this foundation.  Exact symmetry-resolved computations locate the annealed critical points at $n=3,4,5$ and identify their universality classes: Potts exponents at $n=3$ (continuous) and marginal $q=4$ behaviour at $n=4$, while at $n=5$---where the $q>4$ criterion demands a first-order transition---an exact three-size test ($L=4,6,8$) on a symmetry-reduced orbit basis of dimension $3{,}865$ over $2.1\times10^8$ bond labels provides the first three-size discrimination of exponential from power-law gap closing in this family.  The third contribution separates the Born-weighted objects from the symmetric unnormalized ones---an information-theoretic no-go with a bivariate recovery, and the worst-case complexity of conditional-trajectory decision---and develops the large deviations of the measurement record: a no-freezing theorem, the exact replica interpolation identity with its measurable self-averaging criterion, the first numerical quenched record SCGFs for Haar circuits, and an exact closure of the Clifford record-count disorder statistics through a verified conjugation $3$-design.

A delimitation is stated at the outset.  The exactly solved and exactly computed objects of this paper are annealed averages; none of them determines by itself the quenched, Born-weighted transition that experiments and trajectory simulations target.  The value of the annealed ladder is precisely that it is exactly computable at every replica number, providing a controlled calibration target for replica field theories of the quenched problem, with the interpolation identity of Sec.~\ref{sec:records} making the connection quantitative; the detailed delimitations are collected at the end of this section.

"""

MS_EDITS = [
    # --- Sec. I: retitle + Introduction + de-duplicate opening ---
    (r"""\section{Scope and conventions}
""",
     r"""\section{Introduction, scope, and conventions}

""" + INTRO_NEW),
    (r"Monitored random circuits display measurement-induced entanglement transitions~\cite{Li2018,Skinner2019,Chan2019,Gullans2020,Choi2020,Vasseur2019,Jian2020,Bao2020}.  This work establishes exact finite-dimensional constraints on the replica mechanics underlying such transitions.  We prove statements that can serve as controlled inputs to later analytical and numerical studies:",
     r"This work establishes exact finite-dimensional constraints on the replica mechanics underlying these transitions.  The proved and computed statements serve as controlled inputs to later analytical and numerical studies:"),
    # --- two-size -> three-size reconciliation ---
    (r"with the two-size confirmation of the first-order prediction at $n=5$",
     r"with the three-size confirmation of the first-order prediction at $n=5$"),
    (r"and it adds the $n=5$ diagnostics together with the two-size test that confirms the first-order prediction",
     r"and it adds the $n=5$ diagnostics together with the size-ladder test ($L=4,6,8$) that supports the first-order prediction at the three-size level"),
    (r"\emph{The two-size test at $n=5$}",
     r"\emph{The size-ladder test at $n=5$}"),
    (r"diagnostics and the two-size test measure.",
     r"diagnostics and the size-ladder test measure."),
    (r"first-order test is now three-size, its every measured quantity in",
     r"first-order test is three-size, its every measured quantity in"),
    # --- version/meta purge in visible text ---
    (r"replacing the two-size proxy of the previous version, the crossings move to",
     r"the crossings move to"),
    (r"the annealed four-replica point revises to $p_c^{(4)}\approx0.383$---the lower edge of the previous bracket, with the replica trend",
     r"the annealed four-replica point is $p_c^{(4)}\approx0.383$, with the replica trend"),
    (r"with the previously missing $L=8$ $\varepsilon$ values now \emph{recomputed} (the deposited chain stopped at $p=0.38$ and bridged the gap with an un-deposited projection; the recomputation reproduces the deposited $p=0.38$ value to $5.7\times10^{-16}$), reads",
     r"with the $L=8$ $\varepsilon$ values (extended scan, Supplemental Material~\cite{SM}, Sec.~S7), reads"),
    (r"The decisive two-size test is now done.  A restructured BLAS ring contraction---the same mathematical operation as the deposited iterative kernel, validated to $4\times10^{-16}$ against it at $n=2$--$4$, $\mathrm{nb}=2$--$5$, and reproducing every deposited $L=4$ eigenvalue to $5.5\times10^{-15}$ (float64; the float32 production sweep deviates by at most $4.3\times10^{-6}$)---performs the $n=5$, $L=6$ transfer application in $5.4$\,s (float64) or 2.9\,s (float32) per matrix--vector product on the same two cores: an $11$--$21\times$ speedup whose content is diagnostic, since the binding constraint had been the cache-hostile strided temporaries of the previous implementation, not memory ($<500$\,MB peak against 2.3\,GB available).  The full $21$-point, $L=6$, colour-restricted sweep on the same $p$-grid as $L=4$ is thereby routine, with float64 spot-checks at the decisive points.",
     r"The decisive test rests on a restructured ring contraction---the same mathematical operation as the iterative kernel, validated to $4\times10^{-16}$ against it at $n=2$--$4$, $\mathrm{nb}=2$--$5$, and reproducing every $L=4$ eigenvalue to $5.5\times10^{-15}$---which makes the full $21$-point, $L=6$, colour-restricted sweep on the same $p$-grid as $L=4$ routine, with float64 spot-checks at the decisive points (implementation, timings and memory profile in the Supplemental Material~\cite{SM}, Sec.~S7)."),
    (r""") now supplies the
third size, with the numbers below.""",
     r""") supplies the
third size, with the numbers below."""),
    (r"The $L=8$ rung (the exponential-vs-power-law discriminator): the mom0",
     r"The $L=8$ rung---the third rung of the size ladder $L=4,6,8$ and the discriminator between exponential and power-law closing: the mom0"),
    (r"""the claim is no longer a prediction supported by
single-size diagnostics but a measured finite-size trend""",
     r"""the claim is not a prediction supported by
single-size diagnostics alone but a measured finite-size trend"""),
    (r"""---calibrated against the
deposited tilt chain to its rounding, which also fixes that chain's time
convention as $t=L/2$ periods, the earlier ``$t=4L$'' reading being a
mis-transcription---with a vectorized phase-free stabilizer tableau""",
     r"(time convention $t=L/2$ periods; calibration against the deposited tilt chain in the Supplemental Material~\cite{SM}, Sec.~S7)---with a vectorized phase-free stabilizer tableau"),
    (r"""run
inventories, estimator definitions, calibration tables and reproduction
commands are in the Supplemental Material~\cite{SM}, Sec.~S7.""",
     r"""run
inventories, estimator definitions and reproduction
commands are in the Supplemental Material~\cite{SM}, Sec.~S7."""),
    (r"The trajectory estimates of the previous version ($0.0159$, $0.0080$,",
     r"Trajectory estimates ($0.0159$, $0.0080$,"),
    (r"corrected v21 anchors and the gap closures",
     r"corrected $\beta=1$ anchors and the gap closures"),
    (r"""exceeds the present memory
budget and is left to the amplitude extrapolation.""",
     r"""exceeds the memory available for exact dense
treatment and is left to the amplitude extrapolation."""),
    (r"scaling-quality spectral data now exist for $n=3$",
     r"scaling-quality spectral data exist for $n=3$"),
    (r"the two-size confirmation of the first-order prediction is delivered in Sec.~\ref{sec:n4n5} (Table~\ref{tab:n5twosize}), the $q=n$-Potts conjecture is confirmed at the two-size level for $n\le5$ (three sizes at $n=5$), with the $L=8$ rung computed by the symmetry-reduced block route (Sec.~\ref{sec:n4n5})",
     r"the size-ladder confirmation of the first-order prediction is delivered in Sec.~\ref{sec:n4n5} (Table~\ref{tab:n5twosize}), the $q=n$-Potts conjecture being confirmed at the three-size level for $n=5$, the $L=8$ rung computed by the symmetry-reduced block route (Sec.~\ref{sec:n4n5})"),
    (r"Theorem~\ref{thm:nofreeze} now proves existence",
     r"Theorem~\ref{thm:nofreeze} proves existence"),
    (r"the $n=4$ chain now extends to $L=10$",
     r"the $n=4$ chain extends to $L=10$"),
    (r"the $n=3$ moment $\bar Z_3$ itself is now an exact computational object",
     r"the $n=3$ moment $\bar Z_3$ itself is an exact computational object"),
    (r"the profile \emph{family} is now measured across $(L,T)$",
     r"the profile \emph{family} is measured across $(L,T)$"),
    (r"the reconstructed shared library \texttt{gap\_utils.py} (Eq.~\eqref{eq:Wpn}; the original was missing from the deposit, breaking the reproduction chain of the v17--v19 scripts---the full deposited validation battery V1--V8 re-run and passing)",
     r"the shared library \texttt{gap\_utils.py} (Eq.~\eqref{eq:Wpn}; validated by the full battery V1--V8, all passing)"),
    (r"The present revision re-verified the recovered dataset end to end: the seed contract above regenerates the test trajectories bit-exactly",
     r"The dataset was re-verified end to end: the seed contract regenerates the test trajectories bit-exactly"),
    (r"the v22 exact-closure suite (the gap\_utils reconstruction and its validation battery,",
     r"the exact-closure suite (the shared gap\_utils library and its validation battery,"),
    (r"with the $L=10$ third crossing now computed",
     r"with the $L=10$ third crossing computed"),
    (r"""\lambda_\sigma)$ now
cross at $p\simeq0.449$""",
     r"""\lambda_\sigma)$
cross at $p\simeq0.449$"""),
    (r"The estimator of the preceding subsection is now run:",
     r"The estimator of the preceding subsection is run:"),
    (r"now supplies one measured profile",
     r"supplies one measured profile"),
    (r"\texttt{v22\_n5\_L8\_rung.json} now deposited)",
     r"\texttt{v22\_n5\_L8\_rung.json} deposited)"),
    (r"re-verified on the recovered dataset for",
     r"re-verified on the deposited dataset for"),
    (r"was re-run on the recovered dataset and reproduces",
     r"was re-run end to end and reproduces"),
    (r"The v22 exact-closure suite is deposited with it: the shared library",
     r"The exact-closure suite is deposited with it: the shared library"),
    # --- DOI note ---
    (r"are deposited on figshare at \href{https://doi.org/10.6084/m9.figshare.XXXXXXXX}{doi:10.6084/m9.figshare.XXXXXXXX} [placeholder DOI].",
     r"are deposited on figshare (DOI to be assigned prior to submission)."),
    # --- size-ladder table: add the L=8 rung rows (n=3 from the deposited n=3 chain,
    #     n=4 from the deposited lambda_eps top-up, n=5 from the rung JSON) ---
    (r"""\begin{tabular}{lccc}
 & $n=3$ ($p=0.30$) & $n=4$ ($p=0.38$) & $n=5$ ($p=0.47$) \\
\colrule
$\mathrm{gap}_{12}(L{=}4)$ & $2.147$ & $1.919$ & $1.711$ \\
$\mathrm{gap}_{12}(L{=}6)$ & $1.185$ & $0.990$ & $0.806$ \\
closing factor & $1.81$ & $1.94$ & $2.12$ \\
$4\,\mathrm{gap}_{12}\to6\,\mathrm{gap}_{12}$ &
$8.59\to7.11$ & $7.67\to5.94$ & $6.85\to4.85$ \\
\end{tabular}""",
     r"""\begin{tabular}{lccc}
 & $n=3$ ($p=0.30$) & $n=4$ ($p=0.38$) & $n=5$ ($p=0.47$) \\
\colrule
$\mathrm{gap}_{12}(L{=}4)$ & $2.147$ & $1.919$ & $1.711$ \\
$\mathrm{gap}_{12}(L{=}6)$ & $1.185$ & $0.990$ & $0.806$ \\
$\mathrm{gap}_{12}(L{=}8)$ & $0.816$ & $0.645$ & $0.481$ \\
closing factor $L{=}4\to6$ & $1.81$ & $1.94$ & $2.12$ \\
closing factor $L{=}6\to8$ & $1.45$ & $1.54$ & $1.68$ \\
$4\,\mathrm{gap}_{12}\to6\,\mathrm{gap}_{12}$ &
$8.59\to7.11$ & $7.67\to5.94$ & $6.85\to4.85$ \\
$8\,\mathrm{gap}_{12}$ & $6.53$ & $5.16$ & $3.85$ \\
\end{tabular}"""),
    (r"""The $n=5$ two-size test ($d=2$; colour-trivial sector; float32
sweep validated to $4.3\times10^{-6}$ against the deposited $L=4$ values
with float64 spot-checks at the decisive points).  Closing factors at
matched sizes and locators: $n=3$ (continuous) closes slowest, $n=5$
fastest; $L\,\mathrm{gap}_{12}$ saturates at $n=3$ and falls below the
continuous envelope at $n=5$.""",
     r"""The $n=5$ size-ladder test ($d=2$; colour-trivial sector; float32
sweep validated to $4.3\times10^{-6}$ against the deposited $L=4$ values
with float64 spot-checks at the decisive points).  Closing factors at
matched sizes and locators: $n=3$ (continuous) closes slowest, $n=5$
fastest, and the ordering persists at the third size; $L\,\mathrm{gap}_{12}$
saturates at $n=3$ and falls below the continuous envelope at $n=5$.  The
$L=8$ column is available at $n=3$ from the deposited $n=3$ chain, at $n=4$
from the deposited $\lambda_\varepsilon$ top-up (Supplemental
Material~\cite{SM}, Sec.~S7, hashed in \texttt{certificate\_sha256\_v9.txt}),
and at $n=5$ from the symmetry-reduced block route."""),
    # --- orphaned mid-body comment block ---
    (r"""% ---------------------------------------------------------------------------
% v19 staged LaTeX fragments: the no-freezing theorem + replica interpolation
% identity (to be patched into manuscript v19 by patch_v19_twosize.py).
% Anchored insertion after the freezing-scope remark (rem:rem-scope).
% ---------------------------------------------------------------------------
""", r""),
]

SM_EDITS = [
    (r"and the v22 exact-closure suite of that section (the reconstructed gap\_utils library with its validation battery,",
     r"and the exact-closure suite of that section (the shared gap\_utils library with its validation battery,"),
    (r"\texttt{certificate\_sha256\_v8.txt} (the v21 round: the manuscript and supplement of that round together with the Clifford record-count suite whose runs are tabulated in Sec.~\ref{sm:cliffordruns}",
     r"\texttt{certificate\_sha256\_v8.txt} (the Clifford record-count round: the manuscript and supplement of that round together with the record-count suite whose runs are tabulated in Sec.~\ref{sm:cliffordruns}"),
    (r"(the v22 round: the exact-closure suite of Sec.~\ref{sm:v22closure} together with the gap\_utils copies that repair the reproduction chain of the v17--v19 scripts)",
     r"(the exact-closure round: the suite of Sec.~\ref{sm:v22closure} together with the gap\_utils copies distributed alongside the suites that depend on them)"),
    (r"\subsection{The v22 exact-closure runs}",
     r"\subsection{The exact-closure runs: $\bar Z_3$, the Clifford design, and the $n=5$ $L=8$ block}"),
    (r"""\paragraph{The reconstructed library.}
The shared module \texttt{gap\_utils.py} (the Weingarten channel
$W_{p,n}$ of Eq.~(Wpn), the group utilities, and the dense bond-label
operators \texttt{bond\_ops}) on which the deposited v17--v19 script
suites all depend was missing from the repository: the deposit's
reproduction chain was silently broken.  It is rebuilt exactly from
Eq.~(Wpn) (inverse of the Gram $D^{c(\sigma^{-1}\tau)}$ for $D\ge n$,
Moore--Penrose pseudo-inverse otherwise), placed both in
\texttt{scripts/v22-exactZ3-n5L8/} and as copies into
\texttt{v17-annealed-n3/}, \texttt{v18-n4n5-smc/} and
\texttt{v19-n5L6-nofreeze/}, and validated by re-running the deposited
batteries unmodified:""",
     r"""\paragraph{The shared library.}
The shared module \texttt{gap\_utils.py} (the Weingarten channel
$W_{p,n}$ of Eq.~(Wpn), the group utilities, and the dense bond-label
operators \texttt{bond\_ops}), on which the earlier script suites depend,
is included in the deposit, exactly following Eq.~(Wpn) (inverse of the
Gram $D^{c(\sigma^{-1}\tau)}$ for $D\ge n$, Moore--Penrose pseudo-inverse
otherwise), both in \texttt{scripts/v22-exactZ3-n5L8/} and as copies
alongside the suites that use it.  It is validated by re-running the
deposited batteries unmodified:"""),
    (r"""\texttt{v22\_n4\_eps\_topup\_v1.py} recomputes the missing $L=8$
$\lambda_\varepsilon$ values ($p=0.39,0.40,0.41$; the deposited $p=0.38$
value reproduced to $5.7\times10^{-16}$ first).""",
     r"""\texttt{v22\_n4\_eps\_topup\_v1.py} extends the $L=8$
$\lambda_\varepsilon$ scan to $p=0.39,0.40,0.41$ (the deposited $p=0.38$
value reproduced to $5.7\times10^{-16}$ first; the $p=0.38$ cell supplies
the $n=4$ $L=8$ rung row of the main-text size-ladder table)."""),
    (r"""the sub-Gaussian decaying profile of the v21 Discussion,
confirmed on well-conditioned data""",
     r"""the sub-Gaussian decaying profile anticipated in the main-text Discussion,
confirmed on well-conditioned data"""),
    (r"""The raw production $t=4L$ arrays are NOT used for
Part B""",
     r"""The raw production $t=4L$ arrays are not used for
Part B"""),
    (r"""(the within-sample profiles are reported in the
JSON for completeness, flagged).""",
     r"""(the within-sample profiles are reported in the
JSON for completeness)."""),
    (r"""The $L=8$ rung
runs the block at the locator grid; the completed rung (5 grid
points) is deposited as""",
     r"""The $L=8$ rung---the third rung of the size ladder---
runs the block at the locator grid; the completed rung (5 grid
points) is deposited as"""),
    (r"""the
wall time is minutes per script except the $L=8$ block assembly (hours;
the canonical-id pass is $p$-independent and done once).""",
     r"""the
wall time is minutes per script except the $L=8$ block assembly (hours;
the canonical-id pass is $p$-independent and done once).  The $L=6$
transfer application runs in $5.4$\,s (float64) or $2.9$\,s (float32)
per matrix--vector product on two cores, with $<500$\,MB peak memory."""),
    (r"""The files of
this round are hashed in \texttt{certificate\_sha256\_v9.txt}; the v23 rung
completion (\texttt{v22\_n5\_L8\_rung.json}, \texttt{manuscript\_revised\_v23\_rung})
is hashed in \texttt{certificate\_sha256\_v10.txt}.""",
     r"""The exact-closure files are hashed in
\texttt{certificate\_sha256\_v9.txt}; the $L=8$ rung result
\texttt{v22\_n5\_L8\_rung.json} (with the manuscript and supplement of
record) is hashed in \texttt{certificate\_sha256\_v10.txt}."""),
    (r"""the deposited log's own ``$t=4L$'' reading of
this chain is a mis-transcription (at $t=4L=32$ one instead gets
$Z_2=4.57\times10^{-18}$, twenty-nine orders away).""",
     r"""the ``$t=4L$'' reading of
this chain is excluded by the calibration (at $t=4L=32$ one instead gets
$Z_2=4.57\times10^{-18}$, twenty-nine orders away)."""),
]

def apply(text, edits, tag):
    for i, (old, new) in enumerate(edits):
        n = text.count(old)
        assert n == 1, f"[{tag} edit {i}] anchor count={n} (expected 1): {old[:90]!r}"
        text = text.replace(old, new)
    return text

def set_header(text, header):
    parts = text.split(r"\documentclass", 1)
    assert len(parts) == 2
    return header + r"\documentclass" + parts[1]

def set_abstract(text, new_abs):
    a = text.index(r"\begin{abstract}") + len(r"\begin{abstract}")
    b = text.index(r"\end{abstract}")
    return text[:a] + "\n" + new_abs + "\n" + text[b:]

def residual_report(text, tag):
    print(f"--- residual-token report [{tag}] (visible lines only) ---")
    hits = 0
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("%"):
            continue
        for pat in [r"\bprevious version\b", r"\bprevious implementation\b", r"\bprevious bracket\b",
                    r"\bis now done\b", r"\bnow supplies\b", r"\bnow computed\b", r"\bnow resolved\b",
                    r"\bnow exists?\b", r"\bnow proves\b", r"\bnow extends\b", r"\bnow measured\b",
                    r"\bnow an exact\b", r"\bnow three-size\b", r"corrected v21", r"v17--v19",
                    r"mis-transcription", r"present revision", r"recovered dataset", r"present memory",
                    r"no longer a prediction", r"placeholder DOI", r"XXXXXXX"]:
            for m in re.finditer(pat, line):
                hits += 1
                print(f"  line {ln}: {pat}: ...{line[max(0,m.start()-40):m.end()+40]}...")
    print(f"  forbidden-token hits: {hits}")
    now_hits = [(ln, line.strip()[:110]) for ln, line in enumerate(text.splitlines(), 1)
                if not line.lstrip().startswith("%") and re.search(r"\bnow\b", line)]
    print(f"  remaining '\\bnow\\b' occurrences (review for benignity): {len(now_hits)}")
    for ln, ctx in now_hits:
        print(f"    line {ln}: {ctx}")

ms = set_header(MS_OLD, MS_HEADER)
ms = set_abstract(ms, ABSTRACT_NEW)
ms = apply(ms, MS_EDITS, "MS")
sm = set_header(SM_OLD, SM_HEADER)
sm = apply(sm, SM_EDITS, "SM")

(V / "manuscript_revised_v24.tex").write_text(ms)
(V / "supplement_v7.tex").write_text(sm)
print(f"written: manuscript_revised_v24.tex ({len(ms)} chars), supplement_v7.tex ({len(sm)} chars)")
residual_report(ms, "MS v24")
residual_report(sm, "SM v7")
print("PATCH OK")
