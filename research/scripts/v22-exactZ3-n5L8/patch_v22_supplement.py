"""patch_v22_supplement.py -- build supplement_v5.tex from supplement_v4.

Adds the v22 exact-closure suite to Sec. S7 (sm:cliffordruns):
  * the gap_utils reconstruction (the deposit-integrity repair) and its
    validation battery;
  * the conjugation-design test protocol (Remark rem:cliff3design);
  * the exact Zbar_3 boundary-vector derivation, production cells, and
    the lambda_1^{(3)} ladder;
  * the beta=2 identification cross-check at t = L/2;
  * the marginal q=4 log-correction fits with the L=8 epsilon top-up;
  * the tilted-variance profile family;
  * the symmetry-reduced n=5 L=8 block assembler (validation + rung);
plus the scope sentence, the ledger note (certificate_sha256_v9.txt), and
reproduction commands.
All numbers are read from the round's result JSONs.  NEW file; v4 intact.
"""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
VER = os.path.join(HERE, '..', '..', 'versions')
RES = os.path.join(HERE, '..', '..', 'results', 'v22-exactZ3-n5L8')


def log(*a):
    print(*a, flush=True)


def load(fn):
    return json.load(open(os.path.join(RES, fn)))


# ---------------------------------------------------------------------------
src = open(os.path.join(VER, 'supplement_v4.tex')).read()


def rep(old, new, cnt=1):
    global src
    assert src.count(old) == cnt, (
        f"anchor not unique ({src.count(old)}): {old[:90]!r}")
    src = src.replace(old, new)


# scope sentence
rep("and the Clifford record-count runs behind the main-text Sec.~IV.F (Sec.~\\ref{sm:cliffordruns}).",
    "the Clifford record-count runs behind the main-text Sec.~IV.F (Sec.~\\ref{sm:cliffordruns}), and the v22 exact-closure suite of that section (the reconstructed gap\\_utils library with its validation battery, the conjugation-design test, the exact $\\bar Z_3$ cells and ladder, the $\\beta=2$ identification cross-check, the marginal $q=4$ log-correction fits, the tilted-variance profile family, and the symmetry-reduced $n=5$ $L=8$ block route; Sec.~\\ref{sm:v22closure}).")

# ledger note
rep("and \\texttt{certificate\\_sha256\\_v8.txt} (the v21 round: the manuscript and supplement of this round together with the Clifford record-count suite whose runs are tabulated in Sec.~\\ref{sm:cliffordruns}; the parallel-line ledger of that suite is \\texttt{certificate\\_sha256\\_v3\\_scgf.txt}), each self-verifying in the same way.",
    "\\texttt{certificate\\_sha256\\_v8.txt} (the v21 round: the manuscript and supplement of that round together with the Clifford record-count suite whose runs are tabulated in Sec.~\\ref{sm:cliffordruns}; the parallel-line ledger of that suite is \\texttt{certificate\\_sha256\\_v3\\_scgf.txt}), and \\texttt{certificate\\_sha256\\_v9.txt} (the v22 round: the exact-closure suite of Sec.~\\ref{sm:v22closure} together with the gap\\_utils copies that repair the reproduction chain of the v17--v19 scripts), each self-verifying in the same way.")

# ---------------------------------------------------------------------------
# the new S7 subsection, inserted before the bibliography
ADD = r"""
\subsection{The v22 exact-closure runs}
\label{sm:v22closure}

\paragraph{The reconstructed library.}
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
batteries unmodified: \texttt{n3\_annealed\_validate\_v1.py} V1--V6 all
PASS (the Sec.~9 benchmarks to $0.0\times10^{0}$ at six decimals, the
Gram similarity $1.7\times10^{-16}$, the Kaufman closed form to
$4\times10^{-11}$, the momentum-block union $1.3\times10^{-16}$, the
colour sectors to $2\times10^{-6}$, the product rows exact) and
\texttt{n45\_annealed\_validate\_v1.py} V1--V8 ALL OK (including the
$n=5$ $p=1$ bond eigenvalue $1/14$ through the pseudo-inverse channel and
the pinv property $G\,\mathrm{Wg}\,G=G$ to $3\times10^{-15}$).

\paragraph{The conjugation-design test.}
\texttt{v22\_clifford\_3design\_v1.py} enumerates the two-qubit Clifford
group by BFS closure from $\{H\otimes I, I\otimes H, S\otimes I,
I\otimes S, \mathrm{CNOT}_{01}, \mathrm{CNOT}_{10}\}$: $92{,}160$
unitaries, the phase extension $\{e^{ik\pi/4}\}\times\mathrm{Cl}_2$;
phase classes are deduplicated by the injective phase-invariant key
$U\mapsto U\otimes\bar U$ ($11{,}520$ classes), and the census of the
unsigned-Pauli actions gives exactly the $720$ symplectic classes with
$16$ elements each.  The test averages $C^{\otimes n}XC^{\dagger\otimes
n}$ over the classes and compares with the Haar twirl
$\sum_\pi U_\pi y_\pi$, $\mathsf Gy=t$,
$\mathsf G[\pi,\rho]=(d^2)^{c(\pi^{-1}\rho)}$, on six random $X$ at each
$n$: $n=2$ deviates $2.1\times10^{-14}$, $n=3$ deviates
$1.6\times10^{-14}$ (the identification of Remark rem:cliff3design),
$n=4$ deviates $0.578$ (the negative control).

\paragraph{The exact $\bar Z_3$ cells and ladder.}
\texttt{v22\_z3\_exact\_v1.py} implements the boundary-vector formula of
Prop.~prop:z3closure on the compressed bond space with the
\texttt{ring\_gemm\_v2} kernels.  Validation: the $n=2$ anchors of
\texttt{scgf\_exact.json} to $2.6\times10^{-15}$, the $A$-tail
$2.4509\to2.4512$, the layer-parity invariance to $0.0$.  Production
cells ($t=4L$): Table tab:z3exact of the main text.  The ladder:
$\lambda_1^{(3)}$ by power iteration (validated against the dense $L=8$
spectrum to $1.9\times10^{-10}$), with amplitudes $A_3(L)$ constant to
six digits for $t\ge L$ and subexponential in $t$.

\paragraph{The $\beta=2$ identification cross-check.}
\texttt{v22\_traj\\_beta2\\_v1.py} runs the deposited tableau simulator at
$t=L/2$ with $B=4\times10^6/2.4\times10^6/1.6\times10^6$ trajectories at
$L=8/12/16$ (fresh PCG64 seeds, recorded): $\hat\E[2^{-2N_{\rm rand}}]$
against the exact $\bar Z_3(t)$ and $\hat\E[2^{-N_{\rm rand}}]$ against
$\bar Z_2(t)$, with bootstrap standard errors and the empirical tilted
ESS.  The results are quoted in the main text (Prop.~prop:z3closure).

\paragraph{The marginal $q=4$ log-correction fits.}
\texttt{v22\_n4\\_eps\\_topup\\_v1.py} recomputes the missing $L=8$
$\lambda_\varepsilon$ values ($p=0.39,0.40,0.41$; the deposited $p=0.38$
value reproduced to $5.7\times10^{-16}$ first).
\texttt{v22\_q4\\_logcorr\\_v1.py} then evaluates $R_L$, the slopes and
the gaps at the common reference $p^*=0.383$, and fits the marginal
forms: $R_L=1/4-0.90/\ln L+0.46/\ln^2L$ (residual $\le8\times10^{-4}$,
against the corrected $q=4$ target $x_\sigma/x_\varepsilon=1/4$);
$\mathrm{d}X_L/\mathrm{d}p=C\,L^{3/2}(1+0.45/\ln L)$; the $n=3$ control
converging cleanly to $1/6$.  The crossing table is recomputed with the
top-up ($p_c$ crossings $0.3582/0.3790/0.3823$; $1/\nu_{\rm eff}$
$1.00\to1.38\to1.57$).

\paragraph{The tilted-variance profile family.}
\texttt{v22\_tiltvar\\_uniform\\_v1.py} measures
$\mathrm{Var}_s(\log X)$ on $s\in[0,1.5]$ (61 points, tilted empirically, 200
bootstrap resamples): Part A, exactly enumerated Haar $p=1$ collision
partition functions ($k^\ast=-1$) over the grid $L=3$--$6$,
$T=2L,4L,8L$, $6000$ circuits per cell; Part B, fresh Clifford disorder
trajectories at $t=L/2$ (the same well-conditioned cells as the
$\beta=2$ cross-check).  Metrics per cell: the per-period variance rate
$v(0)=\mathrm{Var}_0/T$ (T-independent within each $L$ to $3\%$), the
sub-Gaussian profile ratio $\rho=2\int_0^1(1-s)v(s)\,\mathrm
ds/v(0)$, the initial decay rate $\kappa$, and the interpolation identity
as a per-cell validation ($\le2.5\times10^{-6}$).  Part A:
$\rho=1.02\pm0.03$ across the whole grid (a flat-to-mildly-rising
profile, $(L,T)$-uniform in shape); Part B (Clifford disorder):
$\rho=0.872/0.878/0.888$ at $L=8/12/16$, $p=0.16$ ($0.890/0.894/0.897$
at $p=0.22$): the sub-Gaussian decaying profile of the v21 Discussion,
confirmed on well-conditioned data and mildly de-sub-Gaussianizing with
$L$.  The raw production $t=4L$ arrays are NOT used for
Part B: their tilted ESS collapses to $1$, the same estimator difficulty
as the $\beta=2$ moment (the within-sample profiles are reported in the
JSON for completeness, flagged).

\paragraph{The symmetry-reduced $n=5$ $L=8$ block route.}
\texttt{v22\_n5\\_L8\\_block\\_v1.py} assembles the momentum-zero
colour-trivial block of $\Ccomp^{(5)}$ at $L=8$ exactly: the orbit basis
of the symmetry group $(S_5\times S_5)\rtimes\mathbb Z_4$ on
$(S_5)^4$ (canonical forms $=$ the minimum over conjugators and shifts of
the encoded lkey tuple; the orbit table is $p$-independent and
memmapped), the block elements
$B[\alpha,\beta]=\sqrt{n_\alpha/n_\beta}\sum_{\tau\in O_\beta}
M[\mathrm{rep}_\alpha,\tau]$ by a chunked pass (segment sums over
orbit-sorted chunks), and $C_{\rm block}=B_{M_1}B_{M_2}$.  Validation:
the deposited $n=5$ $L=4$ \texttt{triv3} rows reproduced to
$1.6\times10^{-14}$ ($p=0.44$ and $0.32$), and the $L=6$ blocks against
fresh unrestricted colour-restricted Arnoldi solves.  The $L=8$ rung
runs the block at the locator grid.

Reproduction: run the scripts in this order (each writes its JSON to
\texttt{results/v22-exactZ3-n5L8/} and its log to
\texttt{logs/v22-exactZ3-n5L8/}): \texttt{v22\_clifford\\_3design\\_v1.py},
\texttt{v22\_z3\_exact\\_v1.py all},
\texttt{v22\_traj\\_beta2\\_v1.py},
\texttt{v22\_n4\\_eps\\_topup\\_v1.py},
\texttt{v22\_q4\\_logcorr\\_v1.py},
\texttt{v22\_tiltvar\\_uniform\\_v1.py},
\texttt{v22\_n5\\_L8\\_block\\_v1.py validate},
\texttt{v22\_n5\\_L8\\_block\\_v1.py ids},
\texttt{v22\_n5\\_L8\\_block\\_v1.py run --pgrid 0.44,0.46,0.47,0.48,0.50}.
Dependencies: \texttt{numpy}, \texttt{scipy} (dense eigensolvers); the
wall time is minutes per script except the $L=8$ block assembly (hours;
the canonical-id pass is $p$-independent and done once).  The files of
this round are hashed in \texttt{certificate\_sha256\_v9.txt}.
"""

# raw-string escaping repair: collapse \\ -> \ (the ADD literal has no
# tabular row-breaks, so the blanket collapse is safe)
ADD = ADD.replace('\\\\', '\\')

rep("\\begin{thebibliography}{9}", ADD + "\n\\begin{thebibliography}{9}")

out = os.path.join(VER, 'supplement_v5.tex')
open(out, 'w').write(src)
log(f"written {out} ({len(src)} chars)")
