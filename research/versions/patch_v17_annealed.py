"""v17 patch — the annealed three-replica critical point.

Base: manuscript_revised_v16_recovered.tex (the recovered-data v16).
Applies:
  * a new subsection 'The annealed three-replica critical point' at the end of
    Sec. II (exact sector-resolved spectra of C^{(3)}, L = 4..12, d = 2):
    p_c^{(3)} = 0.305(3), a continuous transition with the three-state-Potts
    amplitude ratio 1/6, slope exponent 1/nu_eff ~ 1.15, gap law ~ 1/L, the
    growth-rate chain, and the lambda_1 simplicity observation;
  * a new Table (crossings / ratio / gap) and the n=2 control row (the same
    code reproduces the deposited benchmark crossings at L = 16..32);
  * the corresponding rewrite of the Discussion open-problem sentence
    ('scaling-quality spectral data for the n>=3 operators do not yet exist');
  * an abstract clause and a pointer in the 'Two remarks' paragraph;
  * a new bibitem (Wu 1982, Potts-model review).

New version file only (versions/manuscript_revised_v17_annealed-n3.tex); the
v16 file is kept unmodified.  Every anchor is asserted before any write.
"""
import re, sys

SRC = "manuscript_revised_v16_recovered.tex"
DST = "manuscript_revised_v17_annealed-n3.tex"

src = open(SRC).read()
n0 = src.count("\n")

def rep(old, new, tag, count=1):
    global src
    assert src.count(old) == count, f"anchor {tag}: count={src.count(old)} (expected {count})"
    src = src.replace(old, new, count)
    print(f"  [ok] {tag}")

# ---------------------------------------------------------------- header
rep("% v16 (recovered-data version), built from the ORIGINAL deposited v13 of the",
    "% v17 (annealed three-replica critical point): new Sec.~\\ref{sec:n3annealed} with the\n"
    "% exact sector-resolved spectra of C^{(3)} at L=4..12 (d=2) — p_c^{(3)}=0.305(3), a\n"
    "% continuous transition with the three-state-Potts amplitude ratio and slope exponent,\n"
    "% the n=2 control reproducing the deposited benchmark crossings, the growth-rate\n"
    "% chain, and the lambda_1 simplicity observation; open-problems paragraph updated.\n"
    "% v16 (recovered-data version), built from the ORIGINAL deposited v13 of the",
    "header")

# ---------------------------------------------------------------- abstract clause
rep("This exact solution benchmarks the transfer-matrix chain; its complete nonzero spectrum is obtained in closed free-fermion form, fixing the finite-size amplitudes at the annealed point exactly; and the annealed point is distinct from the quenched, Born-weighted transition, whose critical point an independent purification locator with disjoint seeds confirms.",
    "This exact solution benchmarks the transfer-matrix chain; its complete nonzero spectrum is obtained in closed free-fermion form, fixing the finite-size amplitudes at the annealed point exactly; and the annealed point is distinct from the quenched, Born-weighted transition, whose critical point an independent purification locator with disjoint seeds confirms.  For three replicas the annealed critical point is located by exact sector-resolved transfer-matrix scaling at $p_c^{(3)}=0.305(3)$ ($d=2$): the transition is continuous, with the amplitude ratio and slope exponent of the three-state Potts class rather than the Ising class of $n=2$, so the annealed replica points move away from the quenched transition as the replica number grows.",
    "abstract-n3")

# ---------------------------------------------------------------- 'Two remarks' pointer
rep("A closed-form spectrum, and the existence of the $L\\to\\infty$ growth rate, remain open for $n\\ge3$ (the symmetry bound on the generic rank, Eq.~\\eqref{eq:rank3}, is known); an end-to-end check of the $n=3$ chain against brute-force record enumeration in a four-qubit Haar brickwork ($\\overline Z_3(t)=\\E_U\\sum_Rp_R^3$) agrees to within Monte-Carlo error.",
    "A closed-form spectrum, and a proof of the existence and regularity of the $L\\to\\infty$ growth rate, remain open for $n\\ge3$ (the symmetry bound on the generic rank, Eq.~\\eqref{eq:rank3}, is known); an end-to-end check of the $n=3$ chain against brute-force record enumeration in a four-qubit Haar brickwork ($\\overline Z_3(t)=\\E_U\\sum_Rp_R^3$) agrees to within Monte-Carlo error.  Sec.~\\ref{sec:n3annealed} below supplies what the exact route does not: sector-resolved scaling spectra of $\\Ccomp^{(3)}$ itself, which locate the annealed three-replica critical point numerically and find it continuous, with three-state-Potts scaling amplitudes.",
    "remarks-pointer")

# ---------------------------------------------------------------- new subsection (before Sec. III)
rep("The exact closure has a precise scope: it applies to the linear outcome-correlated replica channel and independently Haar-averaged gates (or exact 2-designs).  It does not apply to a fixed gate realization, a terminal post-measurement strobe, or normalized conditioned trajectories.\n\n\\section{Born normalization, replica data, and complexity}",
    "The exact closure has a precise scope: it applies to the linear outcome-correlated replica channel and independently Haar-averaged gates (or exact 2-designs).  It does not apply to a fixed gate realization, a terminal post-measurement strobe, or normalized conditioned trajectories.\n\n"
    "\\subsection{The annealed three-replica critical point}\n"
    "\\label{sec:n3annealed}\n\n"
    "For $n=3$ there is no Ising equivalence and no closed form, and the open-problem list has since its first version carried the item that scaling-quality spectral data for the $n\\ge3$ operators do not exist.  This subsection supplies them for $n=3$, $d=2$: exact, sector-resolved spectra of $\\Ccomp^{(3)}=M_1M_2$ on the same lattice, sizes $L=4$--$12$, every number a finite transfer-matrix eigenvalue with no statistical error.\n\n"
    "\\emph{Method.}  The bond channel is Eq.~\\eqref{eq:Wpn} at $D=d^2=4$; the Gram similarity $\\Ccomp\\sim\\mathsf S\\mathsf S^{\\mathsf T}$, $\\mathsf S=\\mathsf G^{1/2}M_1\\mathsf G^{-1/2}$ (Theorem~\\ref{thm:general-n}(i)), makes every restricted spectrum a symmetric problem.  The spectra are resolved by the symmetry of item (iv): at every size and rate tested, the three gaps that scale are carried by the momentum-zero sector---$\\lambda_1$ (colour-trivial, the Perron value), $\\lambda_\\sigma$ (the leading colour-nontrivial value, in the $\\mathrm{std}\\otimes\\mathrm{std}$, inversion-even block, fourfold degenerate as $(\\dim\\mathrm{std})^2=4$), and $\\lambda_\\varepsilon$ (the second colour-trivial value).  Sizes $L\\le10$ are dense ($6^{L/2}\\le7776$); at $L=12$ the momentum-zero block (dimension $7826$) is assembled exactly from product rows of $M_1$ and $M_2$ over shift orbits and diagonalized by Lanczos with colour-restricted iterations.  The validation chain is the same as for the $n=2$ benchmark: the deposited small-size spectra of Sec.~\\ref{sec:general-n} reproduce to the last digit, and the identical code at $n=2$ reproduces the Kaufman closed form to $10^{-11}$ and, run at $L=16$--$32$ through the same momentum-block route, the crossings of Table~\\ref{tab:benchmark} themselves: $0.23319$, $0.23347$, $0.23361$ against the deposited $0.23319$, $0.23348$, $0.23361$ (and $0.23368$ for $(28,32)$), i.e.\\ agreement to $10^{-5}$ at sizes beyond the $n=3$ chain.\n\n"
    "\\begin{table}[t]\n"
    "\\caption{Annealed three-replica critical point ($n=3$, $d=2$), from exact spectra of $\\Ccomp^{(3)}$.  Top: crossings of $X_L=L\\log(\\lambda_1/\\lambda_\\sigma)$ for consecutive sizes.  Middle: the amplitude ratio $\\log(\\lambda_1/\\lambda_\\sigma)/\\log(\\lambda_1/\\lambda_\\varepsilon)$ at the crossing (value of the larger size).  Bottom: the raw gap $\\log(\\lambda_1/\\lambda_\\sigma)$ at the crossing (larger size).  The three-state Potts values are $x_\\sigma/x_\\varepsilon=1/6$ and $\\nu=5/6$~\\cite{Wu1982}; the Ising values of the $n=2$ row of Table~\\ref{tab:benchmark} are $1/8$ and $\\nu=1$.}\n"
    "\\label{tab:n3annealed}\n"
    "\\begin{ruledtabular}\n"
    "\\begin{tabular}{lccccc}\n"
    " & $(4,6)$ & $(6,8)$ & $(8,10)$ & $(10,12)$ & limit \\\\\n"
    "\\colrule\n"
    "$p^*$ & $0.27114$ & $0.29678$ & $0.30244$ & $0.30403$ & $0.305(3)$ \\\\\n"
    "ratio & $0.107$ & $0.144$ & $0.161$ & $0.171$ & $\\to1/6=0.167$ \\\\\n"
    "gap & $0.126$ & $0.118$ & $0.100$ & $0.085$ & $\\propto1/L$ \\\\\n"
    "\\end{tabular}\n"
    "\\end{ruledtabular}\n"
    "\\end{table}\n\n"
    "\\emph{Results} (Table~\\ref{tab:n3annealed}).  The crossings of $X_L=L\\log(\\lambda_1/\\lambda_\\sigma)$ converge from below; power-law, geometric-deceleration and Aitken extrapolations of the four crossings bracket $p_c^{(3)}=0.305(3)$ at $d=2$.  Three independent diagnostics, each the exact analogue of a column of the $n=2$ benchmark, fix the order and the universality class.  (i) \\emph{Continuous:} the raw gap at the crossings decays as $0.126\\to0.118\\to0.100\\to0.085$ over $L=6\\to12$, with $\\xi/L=1/1.32,\\,1/1.06,\\,1/1.00,\\,1/0.98$---a first-order point would saturate the gap and freeze $\\xi/L$, and the two-phase degeneracy signature (an avoided crossing inside the colour-trivial sector) is absent at every size.  (ii) \\emph{Amplitude ratio:} $\\log(\\lambda_1/\\lambda_\\sigma)/\\log(\\lambda_1/\\lambda_\\varepsilon)$ at the crossings is $0.107\\to0.144\\to0.161\\to0.171$, approaching the three-state Potts value $x_\\sigma/x_\\varepsilon=(2/15)/(4/5)=1/6$~\\cite{Wu1982} and excluding the Ising $1/8$ already at $L=10$; the residual overshoot at $L=12$ ($+2.5\\%$) is of the same magnitude as the $n=2$ control's deviation from $1/8$ at comparable sizes ($0.118$ at $L=10$, $0.1243$ at $L=32$).  The identification of the $\\varepsilon$-sector is checked absolutely: at $L=12$ and the crossing, $L\\log(\\lambda_1/\\lambda_\\varepsilon)=6.0$, which tracks $2\\pi x_\\varepsilon=5.03$ under the same lattice-amplitude factor that rescales the $\\sigma$ gap $2\\pi x_\\sigma=0.838\\to1.03$; a two-$\\sigma$ composite ($2x_\\sigma$, ratio $1/2$) or a subleading trivial operator would miss both numbers.  (iii) \\emph{Slope exponent:} $\\mathrm{d}X_L/\\mathrm{d}p$ at $p_c$ grows as $L^{1.15}$, i.e.\\ $1/\\nu_{\\rm eff}=1.15(10)$, against the Potts $6/5=1.2$ and the Ising $1$.  The operator content matches the assignment: the spin excitation lives in the $\\mathrm{std}\\otimes\\mathrm{std}$ block (the two-dimensional standard representation of $S_3$ is the Potts spin), the leading symmetric excitation in the trivial block (the Potts energy), and the $\\sigma$ multiplet is fourfold, $(\\dim\\mathrm{std})^2$, as the $S_3\\times S_3$ symmetry requires.  Two further records: the growth-rate chain $\\lambda_1(L,p)^{1/L}$ is monotone in $L$ at every $p$ and its Richardson extrapolation gives a smooth $\\lambda_\\infty^{(3)}(p)$ ($0.926$ at $p=0.05$ falling to $0.313$ at $p=0.75$), consistent with a single nonanalytic point at $p_c^{(3)}$; and $\\lambda_1$ remained simple, with the $p\\to0$ multiplet splitting $\\mathrm{triv}>\\mathrm{std}>\\mathrm{sgn}$, at every $(L,p)$ tested ($165$ of $165$), extending the simplicity observation of Sec.~\\ref{sec:general-n} below the entrywise-positivity threshold.\n\n"
    "\\emph{Interpretation and scope.}  All three diagnostics land on the three-state-Potts values rather than the Ising ones.  Together with the exact $n=2$ identification this suggests the annealed critical points of this circuit family follow the $q=n$-state Potts universality classes at $n=2,3$; the criterion $q>4$ would then predict the annealed $n\\ge5$ points to be first order, a sharply falsifiable target for the same computation at $n\\ge4$ (the $n=4$ bond space, $24^{L/2}$, is reachable to $L=6$ with the present machinery).  The replica trend also quantifies the annealed--quenched distinction of Sec.~\\ref{sec:ising} at the next replica number: $p_c^{(2)}=0.233810<p_c^{(3)}=0.305(3)$ against the quenched $p_c=0.1597(8)$, i.e.\\ the annealed points move \\emph{away} from the quenched transition as $n$ grows, so no sequence of annealed $n$-replica points converges to the Born-weighted transition from above.  Scope: exact finite-size data with a systematic (not statistical) extrapolation, sizes $L\\le12$, $d=2$; the universality assignment rests on the ratio, the slope exponent and the gap law, not on a proof; and the $\\lambda_\\infty^{(3)}$ curve is an extrapolated record, not a theorem of existence.\n\n"
    "\\section{Born normalization, replica data, and complexity}",
    "new-subsection")

# ---------------------------------------------------------------- open problems rewrite
rep("a closed-form spectrum, a proof that the leading eigenvalue is simple at small $p$, the generic rank for general $L$ (the symmetry bound~\\eqref{eq:rank3} is attained for $L\\le10$ but not at $L=12$), and the existence and regularity of the $L\\to\\infty$ growth rate are open; scaling-quality spectral data for the $n\\ge3$ operators, beyond the exact rank certificates and the small-size spectra quoted in Sec.~\\ref{sec:general-n}, do not yet exist.",
    "A closed-form spectrum, a proof that the leading eigenvalue is simple at small $p$, the generic rank for general $L$ (the symmetry bound~\\eqref{eq:rank3} is attained for $L\\le10$ but not at $L=12$), and a proof of the existence and regularity of the $L\\to\\infty$ growth rate are open; scaling-quality spectral data now exist for $n=3$ (Sec.~\\ref{sec:n3annealed}): $p_c^{(3)}=0.305(3)$ at $d=2$, a continuous transition with the three-state-Potts amplitude ratio $1/6$ and slope exponent $1/\\nu_{\\rm eff}=1.15(10)$, with $\\lambda_1$ simple at every tested size and rate—so the remaining $n\\ge3$ targets are the $n\\ge4$ annealed points, the growth-rate regularity as a theorem, and the $q=n$-Potts universality conjecture that the $n=2$ (exact) and $n=3$ (numerical) data suggest, including its first-order prediction for $n\\ge5$.",
    "open-problems")

# ---------------------------------------------------------------- bibitem
rep("\\bibitem{Zabalo2020} A.~Zabalo, M.~J.~Gullans, J.~H.~Wilson, S.~Gopalakrishnan, D.~A.~Huse, and J.~H.~Pixley, Phys. Rev. B \\textbf{101}, 060301(R) (2020).",
    "\\bibitem{Zabalo2020} A.~Zabalo, M.~J.~Gullans, J.~H.~Wilson, S.~Gopalakrishnan, D.~A.~Huse, and J.~H.~Pixley, Phys. Rev. B \\textbf{101}, 060301(R) (2020).\n"
    "\\bibitem{Wu1982} F.~Y.~Wu, Rev. Mod. Phys. \\textbf{54}, 235 (1982); the exact $q=3$ exponents are $\\nu=5/6$, $x_\\sigma=2/15$, $x_\\varepsilon=4/5$.",
    "bibitem-Wu1982")

# ---------------------------------------------------------------- write + lint
assert src.count("\\subsection{The annealed three-replica critical point}") == 1
assert src.count("Wu1982") == 3  # caption + text + bibitem
open(DST, "w").write(src)
print(f"written versions/{DST}: {n0} -> {src.count(chr(10))} lines")
# lint: balanced braces (rough), no stray control chars
assert src.count("{") == src.count("}")
import re as _re
assert not _re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", src)
print("lint ok")
