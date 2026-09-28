"""patch_v25_tjp.py -- the v25 Turkish Journal of Physics targeting pass.

Builds manuscript_revised_v25_tjp.tex from the DEPOSITED
manuscript_revised_v24.tex (preserved unmodified, like all predecessors).
User directive: referee-proofing for TJP -- referees must be convinced that
the exact results are correct, that the numerical evidence is compelling,
and that the advance is significant; the manuscript must be structured
clearly with a dedicated Conclusion section.

Edits (each asserted unique, count==1, before application):
  E1  source header comment replaced (v25 provenance);
  E2  \\label{conj:continuum} added to the conditional-continuum conjecture;
  E3  dedicated \\section{Conclusion} inserted before the Declarations
      (five paragraphs: exact mechanics; the annealed ladder and the
      three-size first-order test; Born-weighted and record objects;
      the exactness/verification layer (referee-facing); significance and
      outlook).  Every number verbatim from v24 and the deposited results;
      no new claims, no new "first"s beyond the ones v24 already makes;
  E4-E7  the Discussion's unresolved-questions mega-paragraph split at four
      sentence boundaries -- pure paragraph breaks, zero text changes;
  E8  the Introduction's logical-spine sentence now points to the Conclusion.

Output written ONLY to the new file; v21-v24 never touched.  Companion
supplement_v7.tex is unchanged by this pass.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VER = os.path.join(HERE, '..', '..', 'versions')
SRC = os.path.join(VER, 'manuscript_revised_v24.tex')
DST = os.path.join(VER, 'manuscript_revised_v25_tjp.tex')

OLD_HEADER = """% manuscript_revised_v24.tex -- editorial revision (patch_v24_editorial.py) of
% manuscript_revised_v23_rung.tex, which is preserved unmodified alongside its
% predecessors.  Scope of this pass: internal version/meta tokens purged from the
% source and visible text; two/three-size claims reconciled (the size-ladder table
% now carries the L=8 rung at n=3,4,5); abstract restructured; Introduction added
% to Sec. I; data-availability DOI note normalized.  Change log: changelog_v24.md.
% Companion: supplement_v7.tex (same pass).  Provenance ledger: certificate_sha256_v11.txt."""

NEW_HEADER = """% manuscript_revised_v25_tjp.tex -- Turkish Journal of Physics targeting pass
% (patch_v25_tjp.py) of manuscript_revised_v24.tex, preserved unmodified alongside
% its predecessors.  Scope of this pass: dedicated Conclusion section added before
% the Declarations; the Discussion's unresolved-questions paragraph split into five
% readable paragraphs; label added to the conditional-continuum conjecture; the
% Introduction's logical spine now points to the Conclusion.  No physics content
% changed; every number verbatim from v24 and the deposited results.  Companion:
% supplement_v7.tex (unchanged by this pass).  Change log: changelog_v25.md.
% Provenance ledger: certificate_sha256_v12.txt."""

CONCLUSION = r"""\section{Conclusion}
\label{sec:conclusion}

This paper set out to replace perturbative and purely numerical treatments of the replica objects behind measurement-induced entanglement transitions by exact finite-dimensional statements, and to push the associated spectral computation to replica numbers and system sizes at which universality questions can be answered with exact data.  The delivered results are as follows.  For the mechanics: the minimal invariant unital algebra of the one-wire feature space is determined and its fixed-basis leakage quantified (Eq.~\eqref{eq:leaknorm}); an independent layer of Haar-averaged two-site gates on a perfect matching closes the leaked directions exactly for every replica number through the explicit Weingarten bond channel (Eqs.~\eqref{eq:Bpmatrix} and~\eqref{eq:Wpn}); the one-period map is of the form $\mathsf A\mathsf A^\dagger$, so its nonzero spectrum is real, positive and semisimple and compresses exactly to bond-label space; and at $n=2$ the compressed operator is the row-to-row transfer matrix of the anisotropic triangular-lattice Ising model, so the annealed two-replica critical point $p_c^{(2)}=0.2338$ and the free-fermion spectrum are known in closed form.

For the annealed replica ladder: carrying the same computation through $n=3,4,5$ locates $p_c^{(3)}=0.305(3)$, $p_c^{(4)}\approx0.383$ and $p_c^{(5)}\approx0.47$--$0.48$ with the universality classes the $q=n$-Potts identification requires---three-state Potts at $n=3$, marginal $q=4$ logarithmic behaviour at $n=4$---and, at $n=5$, an exact three-size test ($L=4,6,8$) of the predicted first-order transition.  The test is enabled by a symmetry-reduced orbit basis of dimension $3{,}865$ that carries the $120^4=2.1\times10^8$ bond labels of the $n=5$, $L=8$ sector as an exactly assembled dense block.  Every measured quantity moves in the first-order direction (Table~\ref{tab:n5twosize}): the two-phase gap closing accelerates monotonically across replica number, with factors $1.81/1.94/2.12$ over $L=4\to6$ at $n=3/4/5$ that persist at the third size as $1.45/1.54/1.68$ over $L=6\to8$, while the scaled gap $L\,\mathrm{gap}_{12}$, which saturates on the continuous $n=3$ envelope ($6.53$ at $L=8$), falls to $3.85$ at $n=5$.  Two sizes alone cannot separate exponential from power-law closing; the three-size ladder does.

For the Born-weighted and record objects: the normalized conditional-trajectory quantities are separated from the symmetric unnormalized ones by an information-theoretic no-go with an explicit bivariate recovery; the worst-case conditional-trajectory and conditional-purity decision problems are established PP-hard; the no-freezing theorem (Theorem~\ref{thm:nofreeze}) proves existence, determinism and real-analyticity of the quenched record SCGF and rules out finite-$q$ freezing for every allowable finite-reachable process; the exact replica interpolation identity (Proposition~\ref{prop:replica-int}) reduces the annealed-to-quenched passage to a measurable self-averaging criterion; the first numerical quenched record SCGFs for Haar circuits are measured and exhibit genuine record multifractality; and the Clifford record-count disorder statistics are closed exactly through a verified conjugation $3$-design.

A word on what ``exact'' means here, since the computational claims rest on it.  Every proved statement is free of floating-point computation: the three-replica rank certificates of Appendix~\ref{app:rank3} are exact integer-matrix statements with rational interval certificates, certified through $L=12$, and the Collatz--Wielandt enclosures of Appendix~\ref{app:enclosures} certify the two-replica Perron eigenvalue exactly at rational points.  Every computed eigenvalue quoted in this paper is anchored in four independent ways: the operating code reproduces the closed-form Kaufman/Ising answer to $3\times10^{-15}$ at $n=2$; the $p=1$ rank-one anchor matches its closed-form value exactly for every $n=2,\dots,5$, checking the pseudo-inverse Weingarten channel itself at $n=5$; the compressed and full-space routes agree to $4\times10^{-16}$ where both are available, the $L=8$ assembler reproduces the deposited $L=4$ spectrum to $1.6\times10^{-14}$, the $L=6$ blocks match unrestricted colour-restricted Arnoldi solves, and two-seed full-space Arnoldi cross-checks leave residuals below $2\times10^{-15}$; and all deposited artifacts carry checksum ledgers, so every number in this paper is regenerable from the deposit.  The residual numerical error is floating-point roundoff in eigenvalue evaluation only, bounded by the cross-route agreement above and, at the decisive $n=5$ points, by float64 spot-checks on the float32 sweep validated to $4.3\times10^{-6}$.

The significance of the annealed ladder is that it is exactly computable at every replica number, and therefore a controlled calibration target for replica field theories of the quenched transition---with the annealed points receding from the quenched one ($0.2338\to0.305\to0.383\to0.47$ against the Clifford quenched benchmark $0.1597(8)$ of Appendix~\ref{app:numerics}), so that no sequence of annealed points converges to the Born-weighted transition from above.  Three extensions follow immediately from the machinery as deposited: the $d=3$ rung at $L=8$ on the same orbit basis, a finer $p$-grid resolving the $n=5$ locator, and interface-tension and latent-heat extraction from the deposited eigensystems.  The deeper open problems---growth-rate regularity for $n\ge3$, the uniformity of the tilted variance in $(L,T)$, and the conditional continuum program of Conjecture~\ref{conj:continuum}---are collected in the Discussion.

"""

edits = [
    # E1 -- provenance header
    (OLD_HEADER, NEW_HEADER),
    # E2 -- label the conditional-continuum conjecture
    ("\\begin{conjecture}[Conditional continuum program]",
     "\\begin{conjecture}[Conditional continuum program]\n\\label{conj:continuum}"),
    # E3 -- the dedicated Conclusion, inserted before the Declarations
    ("\\section*{Declarations}",
     CONCLUSION + "\\section*{Declarations}"),
    # E4..E7 -- split the unresolved-questions mega-paragraph (pure breaks)
    ("(Prop.~\\ref{prop:z3closure}).  For complexity, the Born average",
     "(Prop.~\\ref{prop:z3closure}).\n\nFor complexity, the Born average"),
    ("neither its hardness nor an average-case Haar statement is known.  For record large deviations, Theorem~\\ref{thm:nofreeze}",
     "neither its hardness nor an average-case Haar statement is known.\n\nFor record large deviations, Theorem~\\ref{thm:nofreeze}"),
    ("no linear $\\tau$ branch up to $q=3$ at $L\\le12$, $T=2L$.  The disorder-replica interchange is reduced",
     "no linear $\\tau$ branch up to $q=3$ at $L\\le12$, $T=2L$.\n\nThe disorder-replica interchange is reduced"),
    ("Supplemental Material~\\cite{SM}, Sec.~S7.)  Finally, the exact integer-$q$ lattice functional",
     "Supplemental Material~\\cite{SM}, Sec.~S7.)\n\nFinally, the exact integer-$q$ lattice functional"),
    # E8 -- the Introduction spine points to the Conclusion
    ("Sec.~\\ref{sec:aux} delimits what remains conditional.",
     "Sec.~\\ref{sec:aux} delimits what remains conditional; Sec.~\\ref{sec:conclusion} concludes."),
]


def main():
    with open(SRC, encoding='utf-8') as f:
        text = f.read()
    for i, (old, new) in enumerate(edits, 1):
        n = text.count(old)
        assert n == 1, f"edit E{i}: anchor count {n} != 1 -- ABORT, nothing written"
        text = text.replace(old, new)
    with open(DST, 'w', encoding='utf-8') as f:
        f.write(text)
    # residual-token report (visible-text meta talk must stay at zero)
    forbidden = ["previous version", "previous implementation", "previous bracket",
                 "mis-transcription", "superseded", "recomputed from",
                 "recovered dataset", "RAM", "cores", "GB of"]
    low = text
    hits = {p: low.count(p) for p in forbidden if low.count(p)}
    print(f"written {DST} ({len(text)} chars)")
    print("residual-token report:", hits if hits else "0 forbidden phrases")
    for tag in ["\\section{Conclusion}", "\\label{sec:conclusion}",
                "\\label{conj:continuum}", "Sec.~\\ref{sec:conclusion} concludes"]:
        assert text.count(tag) == 1, f"post-check failed for {tag}"
    print("post-checks: Conclusion + label + spine pointer all present exactly once")


if __name__ == '__main__':
    main()
