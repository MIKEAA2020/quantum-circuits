"""Build manuscript v20 from v19: the alignment pass.  Fixes the six
stale pre-v19 numbers that survived into v19 (Scope p_c, abstract/three
sizes, the sec:n3annealed cross-reference, the tab:n4annealed caption,
the n=5 single-size trend chain, the Discussion replica-chain value),
updates the keywords for the v18/v19 content, adds section labels for a
logical-spine roadmap sentence in Sec. I, and adds two pedagogical
remarks requested by the author review: rem:whyqn (why the q=n-Potts
classes appear and why the annealed points recede from the quenched
transition) and rem:dichotomy (corners versus affine branches --- the
physical dichotomy of the no-freezing theorem).  Asserted-anchor editing
(never overwrite: writes manuscript_revised_v20_alignment.tex as a NEW
file).
"""
import sys

SRC = 'manuscript_revised_v19_twosize-nofreeze.tex'
DST = 'manuscript_revised_v20_alignment.tex'

text = open(SRC).read()


def rep(old, new, count=1):
    global text
    n = text.count(old)
    assert n == count, f"anchor x{n} (want {count}): {old[:90]!r}"
    text = text.replace(old, new, count)


# =========================================================================
# 1. Scope section: the stale pre-recentring p_c -> the adopted value
# =========================================================================
rep("): $p_c=0.1595(10)$, $\\nu=1.24(7)$,",
    "): $p_c=0.1597(8)$, $\\nu=1.24(7)$,")

# =========================================================================
# 2. Scope enumeration: add the v17-v19 computed results to the list of
#    what the work establishes, and add the logical-spine roadmap
# =========================================================================
rep("Born-normalization identities, the worst-case complexity of "
    "conditional trajectories, and the large-deviation definitions for "
    "the Born record.",
    "Born-normalization identities, the worst-case complexity of "
    "conditional trajectories, and the large-deviation definitions for "
    "the Born record, together with the computed annealed replica "
    "chain---$p_c^{(2)}=0.233810<p_c^{(3)}=0.305(3)<p_c^{(4)}\\approx"
    "0.383<p_c^{(5)}\\approx0.47$--$0.48$ with the two-size confirmation "
    "of the first-order prediction at $n=5$, the no-freezing theorem for "
    "finite-reachable processes, and the first sequential-Monte-Carlo "
    "measurement of the quenched record SCGF.")

rep("they are results of simulation, not theorems, and are quoted with "
    "systematic rather than statistical uncertainties.",
    "they are results of simulation, not theorems, and are quoted with "
    "systematic rather than statistical uncertainties.  The logical "
    "spine of the paper: Secs.~\\ref{sec:compression}--\\ref{sec:ising} "
    "establish the exact two-replica mechanics and its closed-form "
    "solution; Secs.~\\ref{sec:general-n}--\\ref{sec:n4n5} carry the "
    "spectral computation to $n=3,4,5$ and test the $q=n$-Potts "
    "prediction; Sec.~\\ref{sec:born} separates the Born-weighted "
    "objects and the complexity statements; Sec.~\\ref{sec:records} "
    "develops the record large deviations, proves the no-freezing "
    "theorem, and measures the first quenched record SCGFs; "
    "Sec.~\\ref{sec:aux} delimits what remains conditional.")

# labels for the two unlabelled sections the roadmap refers to
rep("\\section{Born normalization, replica data, and complexity}",
    "\\section{Born normalization, replica data, and complexity}\n"
    "\\label{sec:born}")
rep("\\section{Auxiliary fields: identities, not a microscopic "
    "derivation}",
    "\\section{Auxiliary fields: identities, not a microscopic "
    "derivation}\n\\label{sec:aux}")

# =========================================================================
# 3. Abstract: "three sizes" -> "four sizes" (the L=10 third crossing
#    needs L=4,6,8,10; the same clause already cites the L=10 crossing)
# =========================================================================
rep("now resolved with full $S_4$ colour resolution at three sizes, "
    "continues the trend at $p_c^{(4)}\\approx0.383$",
    "now resolved with full $S_4$ colour resolution at four sizes, "
    "continues the trend at $p_c^{(4)}\\approx0.383$")

# =========================================================================
# 4. Keywords: register the v18/v19 content (Potts chain, SMC)
# =========================================================================
rep("\\keywords{monitored quantum circuits; measurement-induced "
    "transitions; replica transfer matrices; Weingarten calculus; "
    "triangular-lattice Ising model; exact rank certificates; "
    "Born-record large deviations; multifractality}",
    "\\keywords{monitored quantum circuits; measurement-induced "
    "transitions; replica transfer matrices; Weingarten calculus; "
    "triangular-lattice Ising model; exact rank certificates; Potts "
    "universality classes; Born-record large deviations; "
    "multifractality; sequential Monte Carlo}")

# =========================================================================
# 5. sec:n3annealed: the stale v18 cross-reference to sec:n4n5
# =========================================================================
rep("(the $n=4$ bond space, $24^{L/2}$, is reachable to $L=6$ with the "
    "present machinery).  Sec.~\\ref{sec:n4n5} completes the $n=4$ "
    "computation with full $S_4$ colour resolution at three sizes "
    "($L=4,6,8$): $p_c^{(4)}=0.40$, on the continuing trend "
    "$p_c^{(2)}=0.2338<p_c^{(3)}=0.305<p_c^{(4)}=0.40$, and it adds the "
    "first $n=5$ diagnostics.",
    "(the $n=4$ bond space, $24^{L/2}$, is reachable to $L=10$ with the "
    "present machinery).  Sec.~\\ref{sec:n4n5} completes the $n=4$ "
    "computation with full $S_4$ colour resolution at four sizes "
    "($L=4,6,8,10$): $p_c^{(4)}\\approx0.383$, on the continuing trend "
    "$p_c^{(2)}=0.2338<p_c^{(3)}=0.305<p_c^{(4)}\\approx0.383$, and it "
    "adds the $n=5$ diagnostics together with the two-size test that "
    "confirms the first-order prediction.")

# =========================================================================
# 6. tab:n4annealed caption: the table carries the (8,10) crossing
# =========================================================================
rep("with full $S_4$ colour resolution at $L=4,6,8$.  Rows as in "
    "Table~\\ref{tab:n3annealed}",
    "with full $S_4$ colour resolution at $L=4,6,8,10$.  Rows as in "
    "Table~\\ref{tab:n3annealed}")

# =========================================================================
# 7. sec:n4n5, n=5 diagnostics: the stale v18 single-size trend chain
# =========================================================================
rep("while at $n=4$ the same minimum sits at the crossing region "
    "($0.38$ against the extrapolated $0.40$), which calibrates the "
    "$n=5$ annealed point to $p_c^{(5)}\\approx0.48$--$0.50$---on the "
    "continuing trend $0.2338<0.305<0.40<0.49$ away from the quenched "
    "$0.1597(8)$.",
    "while at $n=4$ the same minimum sits at the crossing region "
    "($0.38$ against the extrapolated $0.383$), which calibrates the "
    "$n=5$ annealed point to $p_c^{(5)}\\approx0.48$--$0.50$ from the "
    "single size---on the continuing trend $0.2338<0.305<0.383<0.47$ "
    "away from the quenched $0.1597(8)$, refined by the two-size test "
    "below to $p_c^{(5)}\\approx0.47$--$0.48$.")

# =========================================================================
# 8. sec:n4n5 Scope paragraph: L<=10 at n=4 (the "extended below" was a
#    v19 editing leftover; the L=10 results appear above it), then the
#    pedagogical remark rem:whyqn
# =========================================================================
rep("\\emph{Scope.}  Exact finite-size data with systematic "
    "extrapolation,\n$d=2$, $L\\le8$ at $n=4$ (extended to $L=10$ "
    "below) and $L\\le6$ at\n$n=5$; the universality assignments rest "
    "on the ratio, slope and gap law,\nnot on a proof; the $n=5$ "
    "first-order test is now two-size, its every\nmeasured quantity in "
    "the first-order direction.",
    "\\emph{Scope.}  Exact finite-size data with systematic "
    "extrapolation,\n$d=2$, $L\\le10$ at $n=4$ and $L\\le6$ at $n=5$; "
    "the universality\nassignments rest on the ratio, slope and gap "
    "law, not on a proof; the\n$n=5$ first-order test is now two-size, "
    "its every measured quantity in\nthe first-order direction.\n\n"
    + r"""\begin{remark}[Why $q=n$, and why the annealed points recede from the quenched one]
\label{rem:whyqn}
Two structural facts organize the whole chain.  (i)~\emph{Why the Potts
classes appear.}  The site channel $T_p(\sigma,\tau)=(1-p)d^{c(\sigma^{-1}\tau)}+pd$
is central in $\mathbb Q[S_n]$, because the cycle count $c$ is a class
function; the transfer problem therefore decomposes over the irreducible
representations of $S_n$, in the same way as the $q$-state Potts
transfer matrix decomposes over its representation sectors, and at
$n=2,3$ the measured amplitude ratios and slope exponents land on the
$q=n$ values.  The replica permutations play the role of the Potts spin
algebra: the standard representation of $S_n$ has dimension $n-1=q-1$,
the number of Potts spin components, and the $\sigma$ excitation lives
in $\mathrm{std}\otimes\mathrm{std}$ with multiplicity $(n-1)^2$, while
the leading symmetric excitation sits in the trivial sector---the
energy--spin hierarchy of the Potts spectrum.  The identification
remains empirical (no Temperley--Lieb or free-fermion equivalence is
exhibited for $n\ge3$), but every measured number supports it, and the
$q>4$ first-order criterion then predicts, correctly, what the $n=5$
diagnostics and the two-size test measure.  (ii)~\emph{Why the annealed
points move away from the quenched transition as $n$ grows.}  The
annealed average $\E_\omega Z_{q,\omega}^n$ is the disorder law tilted
toward high-$Z$ realizations, and the tilt sharpens with $n$;
Proposition~\ref{prop:replica-int} makes this exact through the monotone
ladder $g(r)/r$ and the tilted variance.  For this circuit family,
high-$Z$ disorder means measurement-poor records---the $p_R^2$
record-collision weight of Sec.~\ref{sec:ising} is the $n=2$ instance,
and its effective density shift $p\to p_{\rm eff}<p$ (Appendix~\ref{app:numerics})
is the mechanism in microcosm---so the annealed singularity sits at a
higher monitoring rate than the quenched one and recedes further as the
tilt strengthens: the chain
$0.1597(8)<0.2338<0.305<0.383<0.47$ is the $n$-axis trace of that
single mechanism.  At a first-order point the same picture identifies
the gap $\log(\lambda_1/\lambda_2)$: the two leading colour-trivial
eigenvalues are the free energies of the two coexisting phases, and the
gap is their tunnelling splitting---exponentially small in $L$ through
an interface whose tension the latent heat sets, against the power-law
gap of a continuous transition.  That is why the closing-factor and
$L\,\mathrm{gap}_{12}$ diagnostics of Table~\ref{tab:n5twosize}
separate the two behaviours, and why the coexistence plateau narrows at
fixed $\xi$.
\end{remark}""")

# =========================================================================
# 9. Discussion: the stale v18 replica-chain value
# =========================================================================
rep("$p_c^{(3)}=0.305(3)$ and $p_c^{(4)}=0.40$ at $d=2$, both "
    "continuous",
    "$p_c^{(3)}=0.305(3)$ and $p_c^{(4)}\\approx0.383$ at $d=2$, both "
    "continuous")

# =========================================================================
# 10. sec:nofreeze: the pedagogical remark rem:dichotomy, placed after
#     the numerical-verification paragraph, before the SMC contract
# =========================================================================
rep("\\subsection{Sequential Monte Carlo contract}",
    r"""\begin{remark}[Corners versus affine branches---the physical dichotomy]
\label{rem:dichotomy}
Theorem~\ref{thm:nofreeze} separates two mechanisms that a glance at a
plotted $\tau(q)$ can conflate.  A \emph{corner}---a jump of
$\tau'$---is phase competition: the tilted process has (at least) two
invariant sectors with distinct growth rates, and the dominant one
exchanges as $k$ varies; the quenched free energy is then a maximum of
analytic branches, exactly as at a first-order thermodynamic transition,
and the reducible allowable chains realize it with conserved sectors.
An \emph{affine branch}---$\tau$ linear over an interval of $q$---is
extremal domination: a single unbounded configuration class controls
the growth rate throughout the interval, as in the random-energy
sequence of Theorem~\ref{thm:rem}, where beyond $q_c=\sqrt{2\log2}$ the
maximum energy alone fixes the free energy while $\tau'$ stays
continuous.  Finite-reachable allowable processes can produce the first
behaviour but never the second: within a finite set the extremal
configuration is bounded and the process mixes (the Hilbert-metric
contraction), so the growth mode is unique and analytic in $k$---there
is no ladder of ever-more-extreme configurations for the tilt to climb.
Freezing is thus a statement about the \emph{reachable-set geometry},
not about the record observable itself: it requires unbounded extremes,
which is precisely the point on which the theorem's hypothesis and its
counterexample meet.  The numerical verification above displays the
dichotomy side by side: corners with curved branches in the reducible
chains, an affine terminal branch only in the random-energy benchmark.
\end{remark}

\subsection{Sequential Monte Carlo contract}""")

# =========================================================================
# 11. Version header comment
# =========================================================================
rep("% v17a: adds the exploratory n=4 (4,6) crossing 0.357 to Sec. n3annealed.",
    "% v20 (alignment pass): the six stale pre-v19 numbers fixed (Scope\n"
    "% p_c 0.1595(10)->0.1597(8); abstract and sec:n3annealed\n"
    "% \"three sizes\"->four sizes L=4,6,8,10; tab:n4annealed caption; the\n"
    "% n=5 single-size trend chain 0.40<0.49 -> 0.383<0.47; Discussion\n"
    "% p_c^{(4)}); keywords extended (Potts universality classes,\n"
    "% sequential Monte Carlo); Sec. I gains the logical-spine roadmap;\n"
    "% new pedagogical remarks rem:whyqn and rem:dichotomy.\n"
    "% v17a: adds the exploratory n=4 (4,6) crossing 0.357 to Sec. n3annealed.")

open(DST, 'w').write(text)
print(f"wrote {DST} ({len(text)} chars)")

# quick self-check: no stale strings remain in the BODY (the header
# comment legitimately documents the historical re-centring 0.1595(10))
body = text[text.index(r"\begin{document}"):]
for stale in ["): $p_c=0.1595(10)$", "three sizes ($L=4,6,8$)",
              "0.2338<0.305<0.40<0.49", "$p_c^{(4)}=0.40$",
              "colour resolution at $L=4,6,8$.  Rows",
              "reachable to $L=6$ with the present machinery"]:
    assert stale not in body, f"stale string survived: {stale!r}"
for fresh in ["rem:whyqn", "rem:dichotomy", "sec:born", "sec:aux",
              "four sizes", "0.383<0.47", "Potts universality classes; "]:
    assert fresh in text, f"new string missing: {fresh!r}"
print("self-check: all stale strings removed, all new strings present")
