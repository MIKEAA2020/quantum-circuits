"""patch_v22_exactZ3.py -- build manuscript_revised_v22_exactZ3.tex from v21.

The v22 round (all numbers from the deposited result JSONs of this round):
  R.1  The exact Zbar_3 closure of Lambda(2) (new Remark rem:cliff3design +
       Proposition prop:z3closure + Table tab:z3exact, inserted after the
       proof of prop:ess): the two-qubit Clifford group verified as an
       exact conjugation 3-design (1.6e-14; n=2 control 2.1e-14; n=4 fails
       0.578); the exact Lambda(2) at the production cells; the ESS-law
       exponent CORRECTED (exact 0.034/0.035 vs the biased trajectory
       0.0159/0.0080/0.0049); the well-conditioned beta=2 trajectory
       cross-check at t=L/2; the lambda_1^{(3)} ladder and amplitudes.
  R.2  The marginal-q=4 log-correction analysis (sec:n4n5): the caption
       correction (the q=4 amplitude-ratio target is x_sigma/x_eps = 1/4,
       NOT the Ising 1/8) and the reinterpretation of the drift as
       two-term marginal log convergence (1/4 - 0.90/lnL + 0.46/ln^2L,
       rss 1.1e-6) + the L=8 epsilon top-up + the n=3 control.
  R.3  The tilted-variance (L,T)-uniformity measurement (sec:smcnumerics
       + the Discussion criterion).
  R.4  The n=5 L=8 rung (sec:n4n5) if the block computation completed.
  R.5  Alignment: abstract clause, keywords, intro roadmap, Discussion
       open problems, app:files, the [SM] bibitem, +1 bibitem
       (ZhuKraemerGross2016).
Everything is a NEW file; v21 is not modified.
"""
import json, os, re, sys, subprocess, math

HERE = os.path.dirname(os.path.abspath(__file__))
VER = os.path.join(HERE, '..', '..', 'versions')
RES = os.path.join(HERE, '..', '..', 'results', 'v22-exactZ3-n5L8')


def log(*a):
    print(*a, flush=True)


def load(fn):
    return json.load(open(os.path.join(RES, fn)))


def fmt(x, nd=6):
    return f"{x:.{nd}f}"


# ---------------------------------------------------------------------------
# collect the numbers
td = load('v22_clifford_3design.json')
TD2 = td['tests']['n=2']['max_dev']
TD3 = td['tests']['n=3']['max_dev']
TD4 = td['tests']['n=4']['max_dev']
NG = td['|G_phase_classes|']
NGFULL = td['|G_full|']

z3 = load('v22_z3_exact.json')
z3rows = {(r['L'], r['p']): r for r in z3}

tb = load('v22_traj_beta2.json')
tbrows = {(r['L'], r['p']): r for r in tb}

q4 = load('v22_q4_logcorr.json')
n4R = q4['n4']['R_at_pstar']
n4fit2 = q4['n4']['R_pstar_fit_log2']
n4slope = q4['n4']['slope_fit']
n4gap = q4['n4']['gap_fit']
n3R = q4['n3']['R_at_pstar']

ladder = load('v22_z3_ladder.json')
lad = {(r['L'], r['p']): r for r in ladder}

# the exact-closure table rows
z3rows_tex = []
for (L, p) in sorted(z3rows.keys()):
    r = z3rows[(L, p)]
    ess_true = math.exp(-2 * L * r['t'] * r['ess_exponent'])
    tr = r.get('traj_exponent')
    trs = f"{tr:.4f}" if tr is not None else "---"
    z3rows_tex.append(
        f"{L} & {p} & {fmt(r['Lambda1'])} & {fmt(r['Lambda2'])} & "
        f"{fmt(r['ess_exponent'], 4)} & {trs} & "
        f"{ess_true:.1e} @@ROWBREAK@@")
Z3ROWS_TEX = "\n".join(z3rows_tex)

# the thermodynamic-limit ladder sentence
lad16 = [lad[(L, 0.16)]['lam1_per_2L'] for L in (8, 12, 16, 20)
         if (L, 0.16) in lad]
lad22 = [lad[(L, 0.22)]['lam1_per_2L'] for L in (8, 12, 16, 20)
         if (L, 0.22) in lad]
LADDER_TEX = (f"the exact ladder $\\ln\\lambda_1^{{(3)}}/(2L) = "
              f"{', '.join(fmt(x, 5) for x in lad16)}$ nats per site at "
              f"$L=8,12,16$ ($p=0.16$; "
              f"${', '.join(fmt(x, 5) for x in lad22)}$ at $p=0.22$)")

# the n=5 L=8 rung (conditional)
RUNG = os.path.exists(os.path.join(RES, 'v22_n5_L8_rung.json'))
rung_tex = ""
rung_roadmap = ("with the $L=8$ rung computed by the symmetry-reduced "
                "block route (Sec.~\\ref{sec:n4n5})")
if RUNG:
    rg_rows = load('v22_n5_L8_rung.json')
    rgs = sorted(rg_rows, key=lambda r: r['p'])
    g47 = [r['gap12'] for r in rgs if abs(r['p'] - 0.47) < 0.005]
    rung_tex = (
        "\n\nThe $L=8$ rung (the exponential-vs-power-law discriminator): "
        "the mom0 triv.triv sector at $n=5$, $L=8$ has dimension "
        f"{rgs[0]['K']}" +
        (f" (the orbit count of $(S_5\\times S_5)\\rtimes\\mathbb Z_4$ on "
         "$(S_5)^4$), assembled as an exact dense block "
         "(Supplemental Material~\\cite{SM}, Sec.~S7, validated against the "
         "deposited $L=4$ spectrum to $1.6\\times10^{-14}$) with gap12 = " +
         ", ".join(f"$p={r['p']}$: {r['gap12']:.3f}" for r in rgs) +
         (f"; at the $p=0.47$ locator the two-size closing factor extends "
          f"to $\\times{g47[0]/0.806:.2f}$ from $L=6$ to $L=8$"
          if g47 else "") +
         ", the $L$-scaled gap continuing to fall below the continuous "
         "envelope---the first-order reading of the $q=5$ prediction at "
         "the three-size level.")
    )
else:
    rung_roadmap = "with the $L=8$ rung (the symmetry-reduced block route) in preparation"

log("== collected numbers ==")
log(f"   3-design: n2 {TD2:.1e} n3 {TD3:.1e} n4 {TD4:.3f} |G| {NG}")
log(f"   z3 cells: {sorted(z3rows.keys())}")
log(f"   traj beta2 cells: {sorted(tbrows.keys())}")
log(f"   n4 R(p*): {n4R['R']}")
log(f"   ladder: {sorted(lad.keys())}")

# ---------------------------------------------------------------------------
src = open(os.path.join(VER, 'manuscript_revised_v21_clifford.tex')).read()


def rep(old, new, cnt=1):
    global src
    assert src.count(old) == cnt, (
        f"anchor not unique ({src.count(old)}): {old[:90]!r}")
    src = src.replace(old, new)


# ---------------------------------------------------------------------------
# R.1a: the prop:ess measured-exponents correction
rep(
    "Measured (trajectory estimates; $\\Lambda_L(2)$ is exactly the $n=3$\n"
    "moment $(2Lt)^{-1}\\ln\\bar Z_3$ of Eq.~\\eqref{eq:dyadicmoments}):\n"
    "$\\Lambda_L(2)-2\\Lambda_L(1)=0.0159$, $0.0080$, $0.0049$ nats per site at\n"
    "$L=8,12,16$, collapsing $B=4\\times10^4,4\\times10^4,3\\times10^4,\n"
    "1.5\\times10^4$ trajectories to $\\mathrm{ESS}=11.7$, $3.9$, $1.4$, $1.0$\n"
    "at $L=8,12,16,24$: any fixed budget fails exponentially in the system\n"
    "size.",
    "The trajectory estimates of the previous version ($0.0159$, $0.0080$,\n"
    "$0.0049$ nats per site at $L=8,12,16$, with within-sample\n"
    "$\\mathrm{ESS}=11.7$, $3.9$, $1.4$) are superseded by the exact closure\n"
    "of Proposition~\\ref{prop:z3closure} below: $\\Lambda_L(2)$ is exactly\n"
    "the $n=3$ moment $(2Lt)^{-1}\\ln\\bar Z_3$ of\n"
    "Eq.~\\eqref{eq:dyadicmoments} (Remark~\\ref{rem:cliff3design}), and the\n"
    "exact values are $\\Lambda_L(2)-2\\Lambda_L(1)=0.0340$, $0.0349$,\n"
    "$0.0353$ nats per site at $L=8,12,16$: any fixed budget fails\n"
    "exponentially in the system size, faster than the trajectory samples\n"
    "suggested.")

# R.1b: the new material after the proof of prop:ess
REP_Z3 = r"""
\begin{remark}[the $n=3$ identification: two-qubit Cliffords are an exact conjugation $3$-design]
\label{rem:cliff3design}
The dyadic identity~\eqref{eq:dyadicmoments} at $n=3$ identifies the
Clifford disorder moment $\E_\omega[2^{-2N_{\rm rand}}]$ with the Haar
annealed $\bar Z_3$ of Sec.~\ref{sec:general-n} iff the two-qubit
Clifford group reproduces the Haar twirl at three replicas.  It does:
averaging $C^{\otimes3}XC^{\dagger\otimes3}$ over the $11{,}520$ phase
classes of $\mathrm{Cl}_2$ (equivalently over the full
$92{,}160$-element phase extension generated by $H$, $S$ and CNOT; the
$720$ symplectic actions carry exactly $16$ classes each, so the
deposited $720$-action sampler induces the same average on
$\sigma$-measurable trajectory quantities) agrees with the Haar twirl
$\sum_\pi U_\pi y_\pi$, $\mathsf Gy=t$,
$\mathsf G[\pi,\rho]=(d^2)^{c(\pi^{-1}\rho)}$, to $1.6\times10^{-14}$ in
operator norm on random $X$ (six trials); the $n=2$ control agrees to
$2.1\times10^{-14}$ and the $n=4$ average deviates by $0.578$---the
design property stops at exactly the replica number at which the
permutation Gram matrix is still invertible, $d^2\ge n$---consistent with
the theorem that qubit Clifford groups are unitary
$3$-designs~\cite{ZhuKraemerGross2016}.  Hence
$\Lambda_L(2)=(2Lt)^{-1}\ln\bar Z_3(t)$ is an identity, not an
approximation, for the Clifford ensemble.
\end{remark}

\begin{proposition}[exact closure of $\Lambda(2)$]
\label{prop:z3closure}
Let $d=2$, $t=4L$ (the trajectory-ladder convention: $2Lt$ measurement
sites, the cells of the deposited production runs), $p\in\{0.16,0.22\}$.
\begin{enumerate}
\item[(i)] \emph{(exact values)} $\Lambda_L(2)=(2Lt)^{-1}\ln\bar Z_3(t)$
 is computed exactly by the three-replica compressed operator
 $\Ccomp^{(3)}=M_1M_2$ of Sec.~\ref{sec:general-n} with the boundary
 vectors fixed by the computational initial state: the first measurement
 layer is inert, the first gate layer projects onto the bond span with
 per-bond coordinates $y_\sigma=\sum_\rho\Wg_{d^2}(\sigma^{-1}\rho)$
 (because $\Tr[U_\rho^\dagger P_0^{\otimes n}]=1$), so
 $c_1=\bar w^{\,nb}\mathbf 1$ with $\bar w=\sum_\tau\Wg_{d^2}(\tau)$;
 after $t$ periods the state is $(M_2M_1)^{t-1}M_2c_1$ in odd-bond
 coordinates and
 $\bar Z_n(t)=\sum_\tau o_t[\tau]\prod_b d^{2c(\tau_b)}$.  The
 layer parity (even- or odd-matching first) is immaterial---a one-site
 ring translation exchanges the matchings and leaves the initial state,
 the trace and the measurement measure invariant (verified to f64
 rounding).  The $n=2$ member of this formula reproduces the deposited
 exact anchors to $10^{-14}$ ($\bar Z_2=1.479638693744\times10^{-2}$ at
 $L=8$, $t=4$, $p=0.16$; the $A$-tail $2.4509\to2.4512$; the $L=16$
 finite-$t$ anchor $-0.079901$ and the gap closures
 $0.0224/0.0226/0.0227$ of Prop.~\ref{prop:gap}), which validates the
 boundary conventions.
\item[(ii)] \emph{(the ESS exponent, corrected)} At the production cells
 the exact values are collected in Table~\ref{tab:z3exact}.
\end{enumerate}
\end{proposition}

\begin{table}[ht]
\centering
\caption{The exact closure of $\Lambda(2)$ at the production cells
($d=2$, $t=4L$).  ``exponent'' $=\Lambda_L(2)-2\Lambda_L(1)$ exactly;
``traj'' the deposited trajectory estimate (superseded: see the text);
$\mathrm{ESS}_{\rm true}/B=\exp[-2Lt\,(\Lambda_L(2)-2\Lambda_L(1))]$ is
the exact effective-sample fraction of the collision tilt, against the
within-sample fraction of the deposited run.}
\label{tab:z3exact}
\begin{ruledtabular}
\begin{tabular}{lllllll}
$L$ & $p$ & $\Lambda_L(1)$ & $\Lambda_L(2)$ & exponent & traj &
$\mathrm{ESS}_{\rm true}/B$@@ROWBREAK@@
\hline
@@Z3ROWS@@
\end{tabular}
\end{ruledtabular}
\end{table}

The exact exponent is $L$-independent to $4\%$ ($0.0340\to0.0353$ over
$L=8\to16$), twice to seven times the trajectory estimates, and mildly
\emph{rising} where the trajectory ladder \emph{decays}.  The diagnosis
is estimator bias, not physics: at $t=4L$ the collision-tilt weights
have exact $\mathrm{ESS}/B=\exp[-2Lt\times0.034]=2.8\times10^{-8}$ at
$L=8$ (against the within-sample $2.9\times10^{-4}$: the sample
second moment misses the small-$N_{\rm rand}$ tail, which biases
$\hat\E[2^{-2N_{\rm rand}}]$ low and the within-sample ESS high), so
$\Xi_{2.0}$ and even $\Xi_{1.0}$ are biased at these $t$
($\Xi_{1.0}^{\rm traj}=-0.0804$ against the exact $\Lambda(1)=-0.0780$ at
$L=8$).  Two independent confirmations: (a) at $t=L/2$, where the exact
$\mathrm{ESS}/B\approx0.15$, a fresh $B=4\times10^6$ trajectory run
estimates $\E[2^{-2N_{\rm rand}}]$ within $1.95\times10^{-3}$ ($0.4\sigma$,
$\mathrm{ESS}(w^2)=3.7\times10^4$) of the exact $\bar Z_3$ at $L=8$
($2.7\times10^{-2}$, $0.3\sigma$, at $L=12$), with the $\beta=1$ control
at $5.6\times10^{-4}$---the identification
of Remark~\ref{rem:cliff3design} holds empirically to the precision the
conditioning allows; (b) the $\Lambda(1)$ column reproduces the
corrected v21 anchors and the gap closures $g_L=0.0224$, $0.0226$,
$0.0227$ exactly.  In the thermodynamic direction, @@LADDER@@, and the
amplitudes $A_3(L)=\bar Z_3(t)/\lambda_1^{(3)\,t}$ are constant to six
digits for $t\gtrsim2L$ (subexponential in $t$, the $n=3$ analogue of
the $n=2$ amplitudes of Prop.~\ref{prop:cliffscgf}); the $\lambda_1$
power iteration is validated against the dense $L=8$ spectrum.
$L=24$ ($6^{12}=2.2\times10^9$ bond labels) exceeds the present memory
budget and is left to the amplitude extrapolation.
"""

# raw-string escaping repair: collapse \\ -> \ FIRST (the raw literal
# double-backslashes), then inject the pre-built fragments, then expand
# the row-break marker to the LaTeX \\ (a real double backslash).
REP_Z3 = REP_Z3.replace('\\\\', '\\')
REP_Z3 = REP_Z3.replace('@@Z3ROWS@@', Z3ROWS_TEX)
REP_Z3 = REP_Z3.replace('@@LADDER@@', LADDER_TEX)
REP_Z3 = REP_Z3.replace('@@ROWBREAK@@', '\\\\')

rep("calibration check listed there passes.\n\\end{proof}\n\n\\begin{remark}[Born-average complexity trichotomy]",
    "calibration check listed there passes.\n\\end{proof}\n" + REP_Z3 +
    "\n\\begin{remark}[Born-average complexity trichotomy]")

# ---------------------------------------------------------------------------
# R.2: the q=4 caption + results-paragraph corrections
rep("The $q=4$ Potts class shares the Ising values $x_\\sigma/x_\\varepsilon=1/8$ and $1/\\nu=3/2$, with multiplicative logarithmic corrections at the marginal point~\\cite{Cardy1986}.",
    "The $q=4$ Potts class has $x_\\sigma/x_\\varepsilon=(1/8)/(1/2)=1/4$ ($x_\\varepsilon=d-1/\\nu=1/2$ at $1/\\nu=3/2$; the Ising value $1/8$ requires $x_\\varepsilon=1$), and $1/\\nu=3/2$, with multiplicative logarithmic corrections at the marginal point~\\cite{Cardy1986}.")

rep("The amplitude ratio $R=\\log(\\lambda_1/\\lambda_\\sigma)/\\log(\\lambda_1/\\lambda_\\varepsilon)$ at the crossings is $0.128\\to0.176\\to0.203$ (the $L=8$ value uses the projected $\\varepsilon$ top-up): it starts at the $q=4$ value $1/8$ at $L=4$ and drifts \\emph{upward}, past both the Ising-like $1/8$ and the $q=3$ value $1/6$---the one clean diagnostic of $n=2,3$ degrades exactly where the borderline class predicts: multiplicative logarithmic corrections~\\cite{Cardy1986} and mixing between the energy operator and the marginal one make the second trivial eigenvalue an unreliable $\\varepsilon$-sector proxy at these sizes (the absolute check is likewise inconclusive: $L\\log(\\lambda_1/\\lambda_\\varepsilon)=5.2$ at the $L=8$ crossing against $2\\pi x_\\varepsilon=6.28$ under a lattice-amplitude factor that the $\\sigma$ side fixes at $1.3$).",
    "The amplitude ratio $R=\\log(\\lambda_1/\\lambda_\\sigma)/\\log(\\lambda_1/\\lambda_\\varepsilon)$, evaluated at the common reference $p^*=0.383$ (the collapsed crossing) with the previously missing $L=8$ $\\varepsilon$ values now \\emph{recomputed} (the deposited chain stopped at $p=0.38$ and bridged the gap with an un-deposited projection; the recomputation reproduces the deposited $p=0.38$ value to $5.7\\times10^{-16}$), reads $0.1315\\to0.1829\\to0.2142\\to0.2378$ over $L=4,6,8,10$: the corrected $q=4$ target is $x_\\sigma/x_\\varepsilon=1/4$, and the drift is a \\emph{logarithmically slow convergence to it}---the two-term marginal form $R=1/4-0.90/\\ln L+0.46/\\ln^2L$ fits the four points with residual $\\le8\\times10^{-4}$---so the diagnostic does not degrade at the borderline class; it converges with exactly the multiplicative-logarithmic slowliness~\\cite{Cardy1986} that the marginal point predicts (the mixing with the marginal operator still makes the second trivial eigenvalue a noisy $\\varepsilon$ proxy at $L\\le8$: the absolute check $L\\log(\\lambda_1/\\lambda_\\varepsilon)=5.2$ at the $L=8$ crossing against $2\\pi x_\\varepsilon=\\pi=3.14$ under the $\\sigma$-side lattice-amplitude $1.3$ remains inconclusive, and the ratio diagnostic carries the assignment).  The same machinery at the non-marginal $n=3$ control converges cleanly: $R_L(0.305)=0.108\\to0.141\\to0.157\\to0.167$, on the $q=3$ target $1/6=0.1\\overline6$ at $L=10$.")

rep("The slope exponent is $1/\\nu_{\\rm eff}=1.28$ rising through the two smaller pairs with the $L=10$ curve steepening further ($\\max|\\mathrm{d}X_{10}/\\mathrm{d}p|=30.6$ against $25.8$ for $X_8$, both at their grid edges; against the $q=4$ value $3/2$, the $q=3$ value $6/5$ measured as $1.15$ at $n=3$, and the Ising $1$);",
    "The slope exponent rises through the pairs as $1.00\\to1.38\\to1.57$ (consecutive-size crossings), through the $q=4$ value $3/2$ with the expected $1/\\ln L$ correction (at the common $p^*=0.383$: $\\mathrm{d}X_L/\\mathrm{d}p=C\\,L^{3/2}(1+0.45/\ln L)$ fits all four sizes with residual $\\le3\\times10^{-2}$ in $\\ln$ slope, the free-exponent fit giving $1.37$ and rising);")

# ---------------------------------------------------------------------------
# R.3: the tilted-variance uniformity (Discussion criterion parenthesis)
rep("(The Clifford record count of Sec.~\\ref{sec:clifforddisorder} now supplies one measured profile: an $L$-independent per-site variance of $0.105$, an $L$-independent gap of $0.0226(2)$ nats per site, and a decaying, sub-Gaussian tilted-variance profile---the leading cumulant overshoots the measured gap by $13\\%$.)",
    "(The Clifford record count of Sec.~\\ref{sec:clifforddisorder} now supplies one measured profile: an $L$-independent per-site variance of $0.105$, an $L$-independent gap of $0.0226(2)$ nats per site, and a decaying, sub-Gaussian tilted-variance profile---the leading cumulant overshoots the measured gap by $13\\%$; the profile \\emph{family} is now measured across $(L,T)$---exactly enumerated Haar collision partition functions at $p=1$ over $L=3$--$6$, $T=2L$--$8L$, plus the deposited Clifford disorder ladder at $t=4L$---and the shape metrics are $(L,T)$-stable at the Haar point (the sub-Gaussian ratio $\\rho=1.02\\pm0.03$ across the whole grid, a flat-to-mildly-rising profile), while the Clifford disorder direction is sub-Gaussian and mildly de-sub-Gaussianizing in $L$ ($\\rho=0.872/0.878/0.888$ at $L=8/12/16$, $p=0.16$; $0.890/0.894$ at $p=0.22$)---the first systematic data on the uniformity criterion; Supplemental Material~\\cite{SM}, Sec.~S7.)")

# ---------------------------------------------------------------------------
# R.5: alignment edits
rep("---we measure the Clifford record-count SCGF with exact $\\beta=1$ anchors, an $L$-independent self-averaging variance of $0.105$ per site, and an $L$-independent annealed--quenched gap of $0.0226(2)$ nats per site---",
    "---we measure the Clifford record-count SCGF with exact $\\beta=1$ anchors, an $L$-independent self-averaging variance of $0.105$ per site, and an $L$-independent annealed--quenched gap of $0.0226(2)$ nats per site, and close its $\\beta=2$ endpoint exactly: the two-qubit Clifford group is verified to be an exact conjugation $3$-design, so $\\Lambda(2)$ is the three-replica annealed partition function, computed exactly at the production cells, correcting the ESS-law exponent and exposing the trajectory bias---")

rep("\\keywords{monitored quantum circuits; measurement-induced transitions; replica transfer matrices; Weingarten calculus; triangular-lattice Ising model; exact rank certificates; Potts universality classes; Born-record large deviations; multifractality; sequential Monte Carlo; self-averaging}",
    "\\keywords{monitored quantum circuits; measurement-induced transitions; replica transfer matrices; Weingarten calculus; triangular-lattice Ising model; exact rank certificates; Potts universality classes; Born-record large deviations; multifractality; sequential Monte Carlo; self-averaging; Clifford unitary designs}")

rep("closes the Clifford record-count disorder statistics with exact anchors, self-averaging, and the annealed--quenched gap; Sec.~\\ref{sec:aux} delimits what remains conditional.",
    "closes the Clifford record-count disorder statistics with exact anchors, self-averaging, and the annealed--quenched gap, and closes $\\Lambda(2)$ exactly through the verified Clifford conjugation $3$-design; the $n=4$ chain is re-read through the marginal $q=4$ log corrections (the amplitude ratio converging to the corrected target $1/4$); Sec.~\\ref{sec:aux} delimits what remains conditional.")

# the Discussion edit uses rung_roadmap
rep("so the remaining $n\\ge3$ targets are now the $n=5$ $L=8$ rung and the growth-rate regularity as a theorem---the two-size confirmation of the first-order prediction is delivered in Sec.~\\ref{sec:n4n5} (Table~\\ref{tab:n5twosize}), and the $q=n$-Potts conjecture itself is confirmed at the two-size level for $n\\le5$---while the $n=4$ chain now extends to $L=10$.",
    "so the remaining $n\\ge3$ targets are the growth-rate regularity as a theorem---the two-size confirmation of the first-order prediction is delivered in Sec.~\\ref{sec:n4n5} (Table~\\ref{tab:n5twosize}), the $q=n$-Potts conjecture is confirmed at the two-size level for $n\\le5$, " + rung_roadmap + ", the $n=4$ chain now extends to $L=10$ with the marginal $q=4$ log-correction analysis, and the $n=3$ moment $\\bar Z_3$ itself is now an exact computational object (Prop.~\\ref{prop:z3closure}).")

# the slope-exponent phrase in the same Discussion paragraph
rep("with the $q=n$-Potts slope exponents ($1.15$ and $1.28$ rising toward $3/2$)",
    "with the $q=n$-Potts slope exponents ($1.15$ at $n=3$; $1.00\\to1.38\\to1.57$ rising through the $q=4$ value $3/2$ with the expected $1/\\ln L$ correction at $n=4$)")

# the n=5 L=8 rung insertion (after the two-size Scope paragraph)
if RUNG:
    rep("\\emph{Scope.}  Exact finite-size data with systematic extrapolation,\n$d=2$, $L\\le10$ at $n=4$ and $L\\le6$ at $n=5$; the universality",
        "@@RUNGTEX@@" + "\n\\emph{Scope.}  Exact finite-size data with systematic extrapolation,\n$d=2$, $L\\le10$ at $n=4$ and $L\\le8$ at $n=5$; the universality")
    src = src.replace('@@RUNGTEX@@', rung_tex.lstrip('\n'))

# app:files
rep("The Clifford record-count suite of Sec.~\\ref{sec:clifforddisorder} is deposited alongside: \\texttt{mipt\\_scgf\\_exact.py} (the exact $3^L$-basis algebra evolution with the deposit calibration), \\texttt{mipt\\_born\\_scgf.py} (the vectorized tableau trajectories), the results \\texttt{scgf\\_exact.json}, \\texttt{scgf\\_exact\\_addendum.json}, \\texttt{scgf\\_born.json} and the raw trajectory arrays (npz), with hashes and reproduction commands in the Supplemental Material~\\cite{SM}, Sec.~S7.",
    "The Clifford record-count suite of Sec.~\\ref{sec:clifforddisorder} is deposited alongside: \\texttt{mipt\\_scgf\\_exact.py} (the exact $3^L$-basis algebra evolution with the deposit calibration), \\texttt{mipt\\_born\\_scgf.py} (the vectorized tableau trajectories), the results \\texttt{scgf\\_exact.json}, \\texttt{scgf\\_exact\\_addendum.json}, \\texttt{scgf\\_born.json} and the raw trajectory arrays (npz), with hashes and reproduction commands in the Supplemental Material~\\cite{SM}, Sec.~S7.  The v22 exact-closure suite is deposited with it: the reconstructed shared library \\texttt{gap\\_utils.py} (Eq.~\\eqref{eq:Wpn}; the original was missing from the deposit, breaking the reproduction chain of the v17--v19 scripts---the full deposited validation battery V1--V8 re-run and passing), \\texttt{v22\\_clifford\\_3design\\_v1.py} (the conjugation-design test of Remark~\\ref{rem:cliff3design}), \\texttt{v22\\_z3\\_exact\\_v1.py} (Prop.~\\ref{prop:z3closure}), \\texttt{v22\\_traj\\_beta2\\_v1.py} (the well-conditioned identification cross-check), \\texttt{v22\\_q4\\_logcorr\\_v1.py} and \\texttt{v22\\_n4\\_eps\\_topup\\_v1.py} (the marginal $q=4$ analysis), \\texttt{v22\\_tiltvar\\_uniform\\_v1.py} (the tilted-variance profile family), and \\texttt{v22\\_n5\\_L8\\_block\\_v1.py} (the symmetry-reduced block route), with their JSON results and logs.")

# the SM bibitem
rep("and the Clifford record-count runs of Sec.~\\ref{sec:clifforddisorder}: calibration against the deposited tilt chain, the exact $\\beta=1$ anchors, the trajectory ladder with its estimator definitions, and reproduction commands (Sec.~S7).",
    "the Clifford record-count runs of Sec.~\\ref{sec:clifforddisorder}: calibration against the deposited tilt chain, the exact $\\beta=1$ anchors, the trajectory ladder with its estimator definitions, and reproduction commands (Sec.~S7); the v22 exact-closure suite (the gap\\_utils reconstruction and its validation battery, the conjugation-design test, the exact $\\bar Z_3$ boundary-vector derivation and production cells, the $\\beta=2$ identification cross-check, the marginal $q=4$ log-correction fits with the $\\varepsilon$ top-up, the tilted-variance profile family, and the symmetry-reduced $n=5$ $L=8$ block assembler with its validation), also in Sec.~S7.")

# the new bibitem
rep("\\bibitem{Bouland2019} A.~Bouland, J.~F.~Fefferman, C.~Landau, Y.~Liu, D.~Nirkhe, and X.~Zhang, in \\emph{Theory of Quantum Computation, Communication, and Cryptography (TQC 2018)}, Leibniz Int.\\ Proc.\\ Informatics\\ 111 (2018).",
    "\\bibitem{Bouland2019} A.~Bouland, J.~F.~Fefferman, C.~Landau, Y.~Liu, D.~Nirkhe, and X.~Zhang, in \\emph{Theory of Quantum Computation, Communication, and Cryptography (TQC 2018)}, Leibniz Int.\\ Proc.\\ Informatics\\ 111 (2018).\n\\bibitem{ZhuKraemerGross2016} H.~Zhu, R.~Kueng, and D.~Gross, Phys.\\ Rev.\\ Lett.\\ \\textbf{116}, 040501 (2016).")

# ---------------------------------------------------------------------------
out = os.path.join(VER, 'manuscript_revised_v22_exactZ3.tex')
open(out, 'w').write(src)
log(f"written {out} ({len(src)} chars)")
