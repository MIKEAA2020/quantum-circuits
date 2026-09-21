# Numerical report — v5

**Manuscript:** `versions/manuscript_revised_v16_scgf.tex` (v16; v15 kept
unmodified). This report supersedes v4; everything in v4 stands; the new
Sec. 11 documents the record-SCGF suite (the four theorem-level items closed
in v16) and Sec. 12 updates the provenance.

**Status box (unchanged from v3):** I3 locator $p_c = 0.1597(8)$, $\nu =
1.24(7)$, $\alpha = 1.55(7)$; purification locator $p_c^{\rm purif} =
0.1601$–$0.1604$, $\nu^{\rm purif} = 1.25(2)_{\rm stat}(6)_{\rm sys}$; exact
annealed line $p_c^{(2)}(2) = 0.233810$, $p_c^{(2)}(3) = 0.459688$,
$p_c^{(2)}(5) = 0.679004$.

## 7. Exact certificates (v4: 7.2 gap closed; 7.3 NEW)

### 7.1 N3 Collatz–Wielandt enclosures
Unchanged from v3 (five exact-rational two-sided enclosures of
$\lambda_1(\Ccomp)$, relative widths $2.2$–$7.3\times10^{-15}$, reproduced in
`scripts/mipt_audit3_cw_exact.py`).

### 7.2 Closed-form spectrum verification
As in v3 (`mipt_kaufman_lib.py` + `mipt_audit3_gauss_proof.py`: 108-config
dense-vs-closed agreement $\le 10^{-10}$ in $\ln\lambda$; kernel counts;
commutators; benchmark; Houtappel; $p_{\rm eff}$), **with the v3 caveat
removed**: the spinor factorisation lemma of the deposited proof route *has
now been re-derived and verified* — see 7.3.

### 7.3 The spinor factorisation (NEW in v4; closes the v3 gap)
`scripts/spinor_verify.py` (V1–V4; `logs/spinor_verify.log`,
`results/spinor_verify.json`).  The deposited identity

$$E = \cosh K_2\,\tilde Y + \sinh K_2\,z_m \tilde Y z_1,\qquad
\tilde Y = c\,e^{K_1 x_m} U_{m-1}\cdots U_1,\quad
U_k = e^{K_2 z_k z_{k+1}}\,c\,e^{K_1 x_k},\quad c = \sqrt{2\sinh 2K_1}$$

holds **exactly** for our diagonal transfer $E$ with the parameter map
recovered by structural discovery (Pauli-string decomposition + grid search
over conventions and Kramers–Wannier duals):

- $x_k = \sigma^x_k$, $z_k = \sigma^z_k$ — *plain Paulis*, the
  Schultz–Mattis–Lieb Ising-Clifford algebra (not string Majoranas; the v3
  parameter search tried string conventions and failed for that reason);
- $K_2 = K_d$, and $K_1 = \tfrac12 \operatorname{arsinh}(1/\sinh 2K_d)$ — the
  Kramers–Wannier dual ($\sinh 2K_1 \sinh 2K_d = 1$);
- overall normalisation $N = \sinh^m(2K_d)$ exactly:
  $E = \sinh^m(2K_d)\,[\cosh K_d\,\tilde Y + \sinh K_d\,z_m\tilde Y z_1]$.

**Verification (all PASS, machine precision):**
- V2/V2b: relative residual $\le 6\times10^{-16}$ over $m = 3$–$8$,
  $d \in \{2, 3, 5\}$, $p \in \{0.05, 0.16, 0.40, 0.60\}_{d=2} \cup
  \{0.20, 0.60\}_{d=3} \cup \{0.45\}_{d=5}$ — both branches of the weight
  trajectory; fitted $A^mB$ gives $A = \sinh 2K_d$ to 10 digits and
  $B = 1.0000000000$.
- V1: the end-term/boundary structure holds separately and exactly for $E$
  (wrap coupling $K_d$) and for $D_h$ (wrap coupling $K_h$):
  $E = \cosh K_d\,E_{\rm OBC} + \sinh K_d\,\sigma^z_m E_{\rm OBC}\sigma^z_1$
  (residual $\le 4\times10^{-16}$, $m = 3$–$7$, four $(d,p)$).  Element-wise
  proof: $(\sigma^z_m M \sigma^z_1)_{s's} = s'_m M_{s's} s_1$, so the bracket
  multiplies by $\cosh K + s'_m s_1 \sinh K = e^{K s'_m s_1}$, the wrap bond.
- V4: $D_{h,\rm OBC} = \prod_{k<m} e^{K_h \sigma^z_k\sigma^z_{k+1}}$ exactly
  (commuting bond exponentials).
- V3 (determinant structure, replacing the deposited square-lattice formula):
  every factor of $\tilde Y$ has unit determinant, so $\det\tilde Y =
  c^{m2^m}$; one flip sector of $E$ is *exactly singular* (the $k=\pi$
  kernel at the transfer level); the two flip sectors of $E_{\rm OBC}$ have
  *equal* determinants with the closed form
  $|\det E_{\rm OBC,\varepsilon}| = (2\sinh 2K_d)^{m2^{m-2}}$ (per-site scale
  $2\sinh 2K_d$, $m$-independent; verified $m = 3$–$6$, three $(d,p)$).
  The deposited formula $\rho_\varepsilon^2 = 1 + \varepsilon(-1)^m
  (\sinh 2K_2/\sinh 2K_1)^m$ (Kaufman's square-lattice determinant) does not
  hold for this triangular $E$ — it was evidently mis-transcribed in the
  deposited route; the verified statements above replace it in the manuscript
  (v15 states them after Eq. spinor and in the verification remark).

**Discovery record** (kept for reproducibility): `scripts/spinor_discover.py`
(Pauli-string content of $\log E$/$\log E_{\rm OBC}$/$\log D_h$; the OBC
string count is exactly $m(2m-1)+1$ — the Gaussian counting) and
`scripts/spinor_gridsearch.py` (conventions × parameter maps × targets; the
winning combination above is the unique machine-precision match).

## 8. Purification locator (unchanged from v3)
`scripts/mipt_purif_analysis.py`: $\tau = 1$ collapse $0.16009/1.2486$
($\chi^2 = 18.3/18$); $\tau = 0.5$: $0.16039/1.2506$; frozen-$\nu$
$\Delta\chi^2$ and bootstrap as in v3; all deposited numbers reproduced.

## 9. Files (v4)
`scripts/`: v3 list **plus** `spinor_verify.py` (the factorisation,
boundary, determinant verification), `spinor_discover.py`,
`spinor_gridsearch.py` (the discovery record).
`results/`: v3 list plus `spinor_verify.json`.
`logs/`: v3 list plus `spinor_verify.log`.
`versions/`: `manuscript_revised_v15_spinor.tex` / `.pdf` (v14 kept),
`mipt_numerical_report_v4.md` (v3 kept), `changelog_v15.md` (§Q; the v14
changelog kept), `certificate_sha256_v2.txt` (ledger v2; v1 kept).

## 10. Reconstruction provenance (v4 update)
As in v3, plus: the spinor factorisation — the one item the v3 reconstruction
could not reproduce — is now derived and verified from first principles
(Sec. 7.3), completing the proof-to-code chain of the manuscript's
Proposition: dense diagonalisation (S2), exact enclosures (S8), and now the
operator identity itself (V1–V4). The only deposited claims not reproduced
verbatim are (i) the raw I3 dataset (lost; rows quoted from the deposit, as
in v3) and (ii) the square-lattice Kaufman determinant formula, which is
replaced by the verified triangular-$E$ determinant structure of Sec. 7.3.

## 11. The record SCGF suite (NEW in v5; closes the four theorem-level items)

Manuscript v16 Sec. 7 / App. C. Two new scripts, both verified against the
deposit and against each other.

### 11.1 Exact side (mipt_scgf_exact.py)

Two-replica state evolved on the 3^L per-site algebra basis {e0,e+,e-}^L:
bond twirl (factorised, exact on products) alpha = (4 t_i t_j - s_i s_j)/60,
beta = (4 s_i s_j - t_i t_j)/60 with per-site (t,s) = (2,2),(1,1),(1,-1);
measurement layer diagonal e_pm -> (1-p) e_pm (ONE factor: the measure/no-
measure decision is a single event shared by both replicas — this was the
subtle point; a (1-p)^2 damping is wrong and was caught by the deposit
calibration); initial state after [inert M]+first A layer =
otimes_even[(AA+BB)/10] with trace exactly 1. Observables: Z2 = sum c_a
prod t_a; P_{2,A} = sum c_a prod t_a prod_{k in A} eps_a (the algebraic form
of the replica swap S_A).

Calibration (the deposited audit3_tiltchain.json targets):
- L=8, t=4 periods, p=0.16: Z2 = 1.479639e-2 (deposit 1.4796e-2), S~2 =
  2.1547 (deposit 2.155). PASS to the rounding.
- L=12, t=6 periods, p=0.16: S~2 = 3.1281 (deposit 3.128). PASS.
This also FIXES the deposited chain's time convention: t = L/2 periods, not
the "t = 4L" reading recorded in the logs (at t = 4L = 32 one gets
Z2 = 4.5666e-18, twenty-nine orders away). The v15 manuscript's App. B
sentence "t = 4L" is corrected in v16.

Compressibility: Z2(t)/lambda_1^t -> A(L) constant to six digits for
t >= 3L: A = 2.4512 (L=8, p=0.16), 4.235 (L=12), 7.229 (L=16), 3.279 / 6.833 (L=8/12, p=0.22); the L=16 run (3^16 configurations) gives Z_2 = 8.574e-72, S~2 = 4.1291 at t=64.
The exact beta=1 SCGF anchors: Xi(1; L, t=4L) = -0.077984 (L=8), -0.079362
(L=12) nats/site; lambda_1 ladder (t->inf): -0.07974, -0.08062, -0.08087,
-0.08099, -0.08101 for L = 8..32 at p=0.16 (Houtappel bulk -0.08101);
-0.10870 -> -0.11082 at p=0.22. Saturated tilted entropies
S~2(inf) = 2.2243 (L=8), 3.2496 (L=12), 1.9262 / 2.6004 (p=0.22).

### 11.2 Trajectory side (mipt_born_scgf.py)

Vectorised phase-free F2 tableau (B trajectories simultaneously; uint64
x/z-word rows; the 720 Sp(4,2) gates as 16-entry LUTs; M-A-M-B period order
matching the deposited simulator). Tracks X_R (random-outcome count; P(R) =
2^{-X_R} exactly) and S_{L/2}. New seed contract: numpy PCG64,
seed = 20260529 + cell index (v16 data, not the deposit's MT19937).

Validation: E[2^{-X}] vs the exact Z2 — 0.12929(8) vs 0.12886 (L=4, t=4);
1.4689e-2 vs 1.4796e-2 (L=8, t=4; the deposit's own sampled value was
1.4942e-2); 3.8399e-5 vs 3.8173e-5 (L=12, t=6). E[S] = 2.015(4) vs the
deposit's 2.019(4) and ESS 6339 vs 5935 at (L=8, t=4). The L=12 deposited
quenched entropy 2.394(5) matches neither t=4 (ours 2.497(7)) nor t=6
(2.632(5)) — a convention ambiguity of the deposited L=12 chain (their
exact values DO match at t=6); recorded, not silently smoothed over.

Production (t = 4L; p = 0.16 and 0.22; L = 8, 12, 16, 24; B = 4e4, 4e4,
3e4, 1.5e4; raw arrays in results/scgf_born_raw_*.npz):

| L | xbar (bits/site) | Xi(0.25) | Xi(1) traj | Xi(1) exact | ESS (tilt) | Var(X)/2Lt | E[S] |
|---|---|---|---|---|---|---|---|
| 8  | 0.14479 | -0.0236 | -0.0804 | -0.07798 | 12 | 0.1055 | 2.036 |
| 12 | 0.14703 | -0.0239 | -0.0835 | -0.07936 | 3.9 | 0.1044 | 2.675 |
| 16 | 0.14803 | -0.0241 | -0.0875 | (-0.08087 lambda1) | 1.4 | 0.1058 | 3.116 |
| 24 | 0.14890 | -0.0243 | -0.0917 | (-0.08099 lambda1) | 1.0 | 0.1048 | 3.732 |

### 11.3 The four theorem-level items (as stated in the manuscript)

1. SCGF thermodynamic limit — Prop. scgf: exact beta=1 endpoint = Z2;
   Xi(1) -> (ln W0 + f_H)/2; xbar -> 0.1489 bits/site; Var(X)/(2Lt) =
   0.104–0.106 L-independent (the LDP backbone).
2. Freezing realization — Prop. freeze: exact tilted-entropy gap grows
   (0.19 -> 0.57 bits, L=8 -> 12); the tilt ESS collapses to O(1)–O(10)
   records; the beta=1 estimator becomes edge-dominated at L >= 16.
3. Born-average hardness — Remark hardness: the GK / 2-design /
   average-case trichotomy (new bibliography).
4. Disorder–replica interchange — Prop. replica: the finite-L identity is
   exact; the cumulant expansion reproduces Xi(0.25) to <1% at every L;
   the Jensen gap g = Xi(1) + ln2 xbar = 0.0224 / 0.0226 / 0.0227
   nats/site (L = 8, 12, 16 — exact finite-t anchors; ~0.0228 at L = 24 with
   the A-corrected lambda_1 anchor; p = 0.16) is L-INDEPENDENT — the annealed-minus-
   quenched free-energy gap persists (0.026–0.027 at p = 0.22); the leading
   cumulant 0.0252 overestimates g by ~13% (sub-Gaussian tails).

### 11.4 Files

scripts/mipt_scgf_exact.py, scripts/mipt_born_scgf.py;
results/scgf_exact.json, scgf_exact_addendum.json, scgf_born.json,
scgf_born_raw_L{8,12,16,24}_p{16,22}.npz; logs/mipt_scgf_exact.log,
logs/mipt_born_scgf.log. Ledger v3 (certificate_sha256_v3.txt).

## 12. Reconstruction provenance (v5 update)

As in v4, plus: the record-SCGF layer is entirely reconstructed and verified
(the exact algebra evolution calibrated against the deposited tilt chain to
its rounding; the trajectory simulator cross-validated against the exact Z2
at three sizes). New findings recorded honestly: (i) the deposited chain's
time convention is t = L/2 periods (the logs' "t=4L" reading is a
mis-transcription — fixed in v16); (ii) the deposited L=12 quenched entropy
2.394(5) is not reproduced at either t=4 or t=6 (their exact values are);
(iii) the L=16 exact evolution (3^16 = 43M configs) completed (Z_2 = 8.574e-72,
S~2 = 4.1291 at t = 64; A = 7.229), so the exact finite-t beta=1 anchors
cover L <= 16; beyond that the certified lambda_1 closed form with the
A(L) tail constant carries the anchor.
