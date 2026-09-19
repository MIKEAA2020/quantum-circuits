# Numerical report — v3

**Manuscript:** `versions/manuscript_revised_v14_audit3.tex` (v14, audit-3 plan
implemented; v13 kept in the deposit history). This report supersedes v2; the
sections carried over unchanged are summarised, the changed sections are
rewritten in full.

**Status box (updated):** I3 locator $p_c = 0.1597(8)$ (v13: $0.1595(10)$ — the
audit-3 recenter, Sec. 3.5 below), $\nu = 1.24(7)$, $\alpha = 1.55(7)$;
purification locator $p_c^{\rm purif} = 0.1601$–$0.1604$, $\nu^{\rm purif} =
1.25(2)_{\rm stat}(6)_{\rm sys}$; exact annealed line $p_c^{(2)}(2) =
0.233810$, $p_c^{(2)}(3) = 0.459688$, $p_c^{(2)}(5) = 0.679004$.

## 1. Ensemble
Random two-qudit Clifford brickwork on a ring of $L = 2m$ qudits (dimension
$d = 2$ for the quenched runs), two gate layers per period, each followed by
independent computational-basis measurements at rate $p$; $475{,}600$ quenched
trajectories (I3/entropy locators) and $135{,}000$ purification trajectories
(disjoint seeds). Annealed $n = 2$: exact (the two-replica compression of the
manuscript, Sec. 2).

## 2. Dataset
Quenched: $L = 16$–$512$, $p = 0.14$–$0.18$, $t = 2L, 4L$, $N = 800$–$4000$
per cell, MT19937 seed contract $\mathit{seed0}(L,p)+k$ (bit-exact
regeneration checked for 23 trajectories spanning $L = 16$–$512$, including
the $I_3 \equiv 0$ file). Purification: $L = 16$–$256$, 9 $p$-points, $\tau =
t/L \in \{0.25, 0.5, 1, 2, 4\}$, $N = 2000$–$4000$ per point, 270 files.

## 3. Critical point
### 3.1 Crossings
PCHIP crossings of $I_3(L)$ vs $I_3(2L)$; weighted plateau of the $L \ge 96$
crossings $0.1599(3)$; ladder $p_\times = p_c + aL^{-\omega}$: $0.1600(4)$–
$0.1602(6)$ with $\omega_{\rm eff} = 1.6(4)$–$2.5(8)$ depending on $L_{\min}$
(label corrected: this $\omega_{\rm eff}$ is the ladder's own effective
exponent, not a universal correction exponent; **c_eff label fix** — the
$v2$ discussion of a central-charge conversion is here labelled as the
$\alpha \leftrightarrow \tilde c \ln 2$ identification only, and no central
charge is quoted).
### 3.2 Windowed collapse
$I_3 = F((p-p_c)L^{1/\nu})$, quartic $F$, $|x| \le 0.6, 1, 1.5$, $L_{\min} =
48/64/96$: $\nu = 1.18$–$1.27$, $\chi^2/\mathrm{dof} = 0.7$–$2.6$; for
$L \ge 64$ windows the $\chi^2$ $p$-values are $0.2$–$0.9$.
### 3.3 Logarithmic entanglement
Straight-line $\alpha$ at the adopted $p_c$: $1.56$–$1.64$ (see 3.6).
### 3.4 Corrections to scaling (NEW in v3)
With the saturated tail handled (3.5), a power-law correction $AL^{-\omega}$
is preferred only when $L = 48$ is retained ($\Delta\mathrm{AIC} = -7$ to
$-14$), neutral at $L \ge 64$ ($-6.6$ to $+0.1$), disfavoured at $L \ge 96$
($+3.6$ to $+3.9$); $\omega$ undetermined ($0.3$–$4$); it raises $\nu$ by
$0.02$–$0.04$. The windowed quartic collapses remain the conservative
backbone.
### 3.5 Weighting defect and fix; the $p_c$ center shift (NEW in v3)
The legacy fixed-set fits floored standard errors at $10^{-4}$ (and $10^{-6}$
in the collapse cost). The point $(L{=}384, p{=}0.18, t{=}2L)$ has $I_3 = 0$
in all 800 trajectories (s.e. $= 0 \to 10^{-4} \to$ weight $10^{8}$), i.e.
98% of one fit's total weight. A sextic polynomial forced through the
area-law tail (mean $I_3 > -0.01$ bits, s.e. $0.001$–$0.003$) tilts the
collapse core and pushes $\nu$ to $1.30$–$1.35$: a model artefact. With the
floor at $1/N_{\rm traj}$ and the tail either excluded or described by a
spline scaling function (K = 6), all tail-safe variants agree to $\le 0.01$
and centre at $p_c = 0.1597$–$0.1598$, $\nu = 1.21$–$1.29$; the deposited
$\tau = 2$ purification collapse ($\chi^2/\mathrm{dof} = 82.8/18$) shows the
same tail pathology and is not used. The legacy floors are replaced by $1/N$
in the released analysis code (`scripts/mipt_fss2_floorN.py`, a new file; the
Nelder–Mead `xatol = 10^{-6}` is an optimiser tolerance and is intentionally
untouched — the transform that the previous session left broken). The re-run
confirms the windowed numbers do not move (no point with s.e. below either
floor enters any window; on the recovered purification dataset the change is
provably a no-op: $\max_p (1/N)/\mathrm{s.e.} = 1.000$, zero points touched).
**The headline moves $0.1595(10) \to 0.1597(8)$**: the corrected tail-safe
analyses centre at $0.1597$–$0.1598$ and every independent estimator lies at
or above $0.1597$ within its errors (plateau $0.1599(3)$, ladder
$0.1600(4)$–$0.1602(6)$, joint entropy $0.1598$–$0.1601$, $\Delta S$
crossings $0.159$–$0.161$, Sierant $0.15995(10)$, Gullans–Huse $0.1593(5)$);
keeping $0.1595$ while claiming the defect is addressed would repeat the same
inconsistency the audit rejected for $\nu$.
### 3.6 $\alpha$ rows at the recentered $p_c$
$\mathrm{d}\alpha/\mathrm{d}p \approx -110$, so the straight-line rows move by
${\approx} -0.02$ from the $p_c = 0.1595$ evaluation — within the stated
errors; the rows are quoted at the adopted $0.1597$. A power-law correction
$s_1 L^{-y}$ ($y = 0.5, 1, 2$) is never preferred and moves $\alpha$ by
$< 0.05$.

## 4. Exponent $\nu$
Adopted $\nu = 1.24(7)$: the interval covers the full tail-safe envelope
$1.21$–$1.29$ (including the correction-term variants), the bootstrap errors
($0.015$–$0.04$), and the windowed values; the two $t = 4L$ small-window
values $1.10$–$1.12(7)$ are within $2\sigma$. Fixed-set frozen-$\nu$
$\Delta\chi^2$ profiles (spline $F$, tail in, $L \ge 64$, eight variants):
$\nu = 1$: $52$–$334$; $1.20$: $0.2$–$11$; $1.24$: $0.1$–$2.6$; $1.28$: $0$–
$9.9$; $4/3$: $3.0$–$36.5$; $1.40$: $12.5$–$89$. Sextic, tail out:
$\Delta\chi^2(\nu = 1) \ge 72$.

## 5. Estimators
### 5.4 I(A:C) crossings (discounted in v3)
The $I(A{:}C)$ crossings are dominated by noise (their scatter exceeds the
inter-size differences); they are reported but discounted as a locator —
consistent with the audit finding.
### 5.5 Bootstrap
Trajectory bootstrap: $200$ resamples (crossings/collapse), $100$
(purification).

## 6. Annealed versus quenched (rewritten in v3)
The excess of the annealed quasi-entropy $\tilde S_2$ over the quenched
$\E S$ is a **density effect**, not a convexity (Jensen) effect: the
record-collision weight $p_R^2$ of the annealed channel favours records with
fewer measurements, lowering the effective monitoring rate to
$p_{\rm eff} = p + \frac{p(1-p)}{2L}\partial_p \ln\lambda_1$ ($0.1049$ at
$L = 8$, $0.1011$ at $L = 12$, $0.0920$ at $L \to \infty$ for $p = 0.16$;
$0.1493$ at $p_c^{(2)}(2)$; the closed form confirms the transfer-matrix
values to five digits). The $L = 8$ Born chain (40,000 trajectories, ESS
5935): $\tilde S_2 = 2.155$, $\E S = 2.019(4)$, $S(p_{\rm eff}) = 2.339(4)$,
tilted sample $2.429$ — the density shift accounts for ${\approx}80\%$ of the
tilt gap. At $L = 12$ (exact): $\tilde S_2 = 3.128$, $\E S = 2.394(5)$,
$S(p_{\rm eff}) = 2.941(4)$; the sampled tilt average (ESS 454) is not used.
No mapping between the annealed and quenched transitions is claimed (the
bare $p$ with $p_{\rm eff} = 0.1595$ is $0.2446$, a numerical coincidence
with $p_c^{(2)}(2) = 0.2338$).

## 7. Exact certificates (NEW in v3)
### 7.1 N3 Collatz–Wielandt enclosures
Five exact-rational two-sided enclosures of $\lambda_1(\Ccomp)$ (relative
widths $2.2$–$7.3 \times 10^{-15}$), reproduced in
`scripts/mipt_audit3_cw_exact.py` with brackets of comparable width
($3$–$5 \times 10^{-16}$) that contain both the deposited intervals and the
closed form (60-digit cross-check).
### 7.2 Closed-form spectrum verification
`scripts/mipt_kaufman_lib.py` + `scripts/mipt_audit3_gauss_proof.py`: the
nonzero spectrum of the dense $\Ccomp$ matches the closed form to
$\le 10^{-10}$ in $\ln\lambda$ over 108 configurations ($m = 4$–$9$, $d \in
\{2,3,5\}$, twelve $p$ values including $p_c^{(2)} \pm 2\times10^{-4}$);
kernel count $2^{m-2}$ everywhere; commutators $[\Ccomp, F]$, $[\Ccomp,
\tau]$ vanish to $10^{-15}$; the benchmark table reproduces to its rounding
(crossings $\le 5\times10^{-6}$, ratio row to four decimals);
$\lambda_1(28)^{1/28} = 0.683844946$ (the $0.6838449$ quote) and the bulk
$0.683844659$ (Houtappel); $p_{\rm eff}$ at $p_c^{(2)}$ for $d = 2, 3, 5$
matches the deposited values to 8 digits. The weights themselves were
re-derived in closed form from the quantum two-replica transfer (both
branches), and reproduce the five enclosures, the benchmark, and every
deposited exact number quoted above. The spinor factorisation lemma of the
deposited proof route ($E = \cosh K_2 \tilde Y + \sinh K_2 z_m \tilde Y z_1$,
residual $5\times10^{-15}$ in the deposit) was not re-derived in this
reconstruction (parameter candidates tried and documented); the Proposition
is certified by dense diagonalisation and the exact enclosures instead.

## 8. Purification locator (N2, verified in v3)
`scripts/mipt_purif_analysis.py` on the deposited dataset
(`scripts/mipt_purif_data.py`): $\tau = 1$ collapse $0.16009/1.2486$
($\chi^2 = 18.3/18$); $\tau = 0.5$: $0.16039/1.2506$ ($15.5/18$); $\tau = 2$:
$0.16027/1.310$ ($82.6/18$, saturated — not used); $\tau = 0.25$:
$0.16191/1.2808$ ($48.1/18$); frozen-$\nu$ $\Delta\chi^2$ ($\tau = 1$):
$544/16.8/0.5/6.6/45.7/138.5$ for $\nu = 1/1.2/1.24/1.28/4{\cdot}3^{-1}/1.4$;
bootstrap ($B = 100$): $0.16009(1)$, $1.249(13)$. All deposited numbers
reproduced (the bootstrap central value differs by $2\times10^{-5}$, within
the resampling scatter).

## 9. Files
`scripts/`: `mipt_kaufman_lib.py`, `mipt_audit3_gauss_proof.py`,
`mipt_audit3_cw_exact.py`, `mipt_purif_data.py`, `mipt_purif_analysis.py`,
`mipt_fss2_floorN.py`, plus the reverse-engineering notebooks
(`solve_couplings.py` … `final_verify.py`, kept for the record).
`results/`: `audit3_gauss_proof.json`, `audit3_cw_exact.json`,
`purif_summary.json`. `logs/`: the corresponding `.log` files.
`versions/`: `manuscript_revised_v14_audit3.tex` / `.pdf` (11 pp), this
report, the changelog, the ledger.

## 10. Reconstruction provenance (honest disclosure)
The deposited workspace (`/home/user`, scripts + raw `mipt_data` /
`mipt_data_purif` files) was lost with the original machine; the repository
carries only the two chat logs. This reconstruction rebuilds: (i) the exact
mathematics from first principles (the two-replica algebra, the closed-form
weights, the spectrum, the enclosures) — verified against every deposited
exact number; (ii) the purification analysis on the deposited dataset
(recovered verbatim from the logs); (iii) the released floorN module with
the corrected transform. The raw I3 dataset was not recoverable, so the I3
FSS rows (crossings, windowed collapses, $\alpha$ rows, joint fit) are quoted
from the deposited analysis (final2_summary.json et al., as quoted in the
logs) and are labelled as such; the audit-3 root-cause analysis (weighting
defect, tail pathology, recenter) is likewise quoted from the deposited
assessment, whose conclusions the recovered parts independently confirm.
