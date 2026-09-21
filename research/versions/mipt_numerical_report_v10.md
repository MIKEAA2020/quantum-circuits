# MIPT numerical report v10 — the v22 exact-closure round

Sections 21–25.  All numbers are machine-produced by the round's scripts
(scripts/v22-exactZ3-n5L8/, results/v22-exactZ3-n5L8/, logs mirrored);
every validation listed passed before the corresponding production run.

## 21. The deposit-integrity repair: gap_utils.py

Finding: the shared Weingarten-channel library `gap_utils.py`, imported
by every deposited v17/v18/v19 annealed script, was absent from the
repository — the reproduction chain of research/ v4–v7 was broken (the
runs had happened in a scratch directory that was never deposited).

Repair: reconstructed exactly from Eq. (Wpn)
(W_{p,n}(π|μ,ν) = Σ_σ Wg_{d²}(π⁻¹σ)[(1−p)d^{c(σ⁻¹μ)}+pd][(1−p)d^{c(σ⁻¹ν)}+pd],
Wg = inverse/pinv of the Gram D^{c(σ⁻¹τ)}), signature-compatible
(returns (P, idx, W); `weingarten(n, D) → (P, Wg)`; `bond_ops`,
`build_M`), and copied into v17-annealed-n3/, v18-n4n5-smc/,
v19-n5L6-nofreeze/.

Validation (the deposited batteries, unmodified):
- n3_annealed_validate_v1: V1 PASS (all five Sec. 9 benchmark spectra,
  max|err| = 0.00e+00 at six decimals), V2 PASS (eigs(C)=σ(S)² to
  1.7e-16), V6 PASS (product rows exact), V4 PASS (momentum-block union
  to 1.3e-16), V5 PASS (colour sectors to 2e-6), V3 PASS (Kaufman
  closed form to 4.4e-11; crossings 0.19907/0.22261/0.22881 → 0.23381).
- n45_annealed_validate_v1: V1–V8 ALL OK (n=2 iterative vs Kaufman
  5.2e-15; n=3 vs the deposited scan 2.9e-15; n=4 vs dense 3.6e-15; the
  25-block S₄ completeness 2.5e-16; the p=1 closed forms 0.4/0.2/8/70
  and the n=5 pinv value 1/14 exact; the pinv property 3.2e-15).

## 22. The exact Z̄₃ closure of Λ(2)

### 22a. The conjugation-design test (v22_clifford_3design_v1.py)

|G| = 92,160 (the BFS closure from H,S,CNOT = the phase extension
{e^{ikπ/4}}·Cl₂); phase classes (key U⊗Ū) = 11,520; unsigned-Pauli
actions = 720 with class sizes exactly 16 each.  The design test
(max ‖T_Cl − T_Haar‖/‖T_Haar‖ over random X):

  n=2: 2.085e-14  PASS (the known 2-design, the control)
  n=3: 1.617e-14  PASS (the identification under test)
  n=4: 5.784e-01  FAIL (the negative control)

Hence E_ω[2^{−2N_rand}] = Z̄₃ EXACTLY for the deposited 720-action
Clifford sampler (each action carries 16 phase classes — equal weights).

### 22b. The boundary-vector formula and its validation (v22_z3_exact_v1.py)

Z̄_n(t) = Σ_τ o_t[τ]·∏_b d^{2c(τ_b)},  o_t = (M₂M₁)^{t−1}M₂c₁,
c₁ = w̄^{nb}·1 (w̄ = Σ_τ Wg_{d²}(τ)).  Validation: the deposited Z₂
anchors reproduce to 2.6e-15 / 2.2e-14 / 1.7e-15; the A-tail
2.4508841805/2.4511989714/2.4512049553 to 1.1e-14; the layer-parity
invariance (A-first vs B-first) to 0.00e+00.

### 22c. The production cells (t = 4L — the convention finding)

The deposited trajectory ladder runs t = 4L (nsite = 2Lt = 512/1152/
2048/4608); the ESS values 11.7/3.9/1.4 only reconcile with the quoted
exponents at t = 4L (ln(4e4/11.7)/512 = 0.0159 ✓).  The exact closure
therefore runs at t = 4L:

  L= 8 p=0.16: Z̄₃ = 7.745437985134e-28  Λ(1) = −0.077984  Λ(2) = −0.121924
                exponent = 0.034043   (traj 0.015888; ESS_true/B = 2.7e-8)
  L=12 p=0.16: Z̄₃ = 1.080456618559e-62  Λ(1) = −0.079362  Λ(2) = −0.123857
                exponent = 0.034868   (traj 0.008010; 3.6e-18)
  L=16 p=0.16: Z̄₃ = 1.748391658473e-111 Λ(1) = −0.079901  Λ(2) = −0.124526
                exponent = 0.035277   (traj 0.004867; 4.2e-32)
  L= 8 p=0.22: Λ(1) = −0.106382  Λ(2) = −0.169613  exponent = 0.043189
  L=12 p=0.22: Λ(1) = −0.108278  Λ(2) = −0.172746  exponent = 0.043810
  L=16 p=0.22: Λ(1) = −0.109095  Λ(2) = −0.173901  exponent = 0.044288

The Λ(1) column reproduces the v21 corrected finite-t anchors
(−0.079901 at L=16) and the gap closures 0.0224/0.0226/0.0227.  The
exact exponent is L-independent to 4% and mildly RISING where the
trajectory ladder decays: the trajectory moments are biased low (the
sample second moment misses the small-N tail; even Ξ₁ is biased:
−0.0804 vs −0.0780 at L=8).

### 22d. The β=2 identification cross-check (v22_traj_beta2_v1.py)

Fresh well-conditioned runs at t = L/2 (B = 4e6/2.4e6/1.6e6):

  L= 8 p=0.16: β=1 rel 5.6e-4 (0.5σ; ESS 605,529);
               β=2 rel 1.95e-3 (0.4σ; ESS(w²) 36,987)
  L=12 p=0.16: β=1 rel 3.9e-3 (0.6σ); β=2 rel 2.7e-2 (0.3σ; ESS(w²) 88)
  (the p=0.22 cells analogous; see v22_traj_beta2.json)

The identification holds empirically to the precision the conditioning
allows.

### 22e. The λ₁⁽³⁾ ladder and amplitudes (v22_z3_ladder.json)

λ₁⁽³⁾ by power iteration, dense-validated at L=8 (1.94e-10):

  p=0.16: lnλ₁/(2L) = −0.124775 / −0.125861 / −0.126047  (L=8/12/16)
  p=0.22: lnλ₁/(2L) = −0.173595 / −0.175609 / −0.176101
  A₃(L) = 4.3048 / 10.068 / 22.5566  (p=0.16; 7.6837/27.0572/90.5274
  at p=0.22) — constant to six digits for t ≥ L, subexponential in t.

L=20 and L=24 exceed the 3 GB memory budget (two OOM kills at nb=10;
6¹⁰ = 6.0e7 and 6¹² = 2.2e9 bond labels) — scoped honestly.

## 23. The marginal-q=4 log-correction analysis

### 23a. The L=8 ε top-up (v22_n4_eps_topup_v1.py)

triv3 at L=8: p=0.38 → [0.00218531, 0.00114715, 0.00043129] — the
deposited fast-file λ_ε reproduced to 5.67e-16; new points p=0.39/0.40/
0.41 deposited (λ_ε = 0.00096580/0.00081027/0.00067728).

### 23b. The re-read (v22_q4_logcorr_v1.py)

R_L(p*=0.383) = 0.1315 / 0.1829 / 0.2142 / 0.2378 (L=4/6/8/10) → the
CORRECTED q=4 target x_σ/x_ε = 1/4 (x_ε = d − 1/ν = 1/2 at 1/ν = 3/2;
the v18–v21 caption's Ising 1/8 requires x_ε = 1).  Two-term marginal
fit 1/4 − 0.902/lnL + 0.461/ln²L, rss 1.1e-6 (residuals ≤ 8e-4).  The
n=3 control: R_L(0.305) = 0.108/0.141/0.157/0.167 → 1/6 cleanly.
Slopes at p*: dX/dp = C·L^{3/2}(1 + 0.454/lnL), rss 2.0e-3 (free
exponent 1.366, rising); gap·L → 1.256 (= 2πx_σ·A_lat).  Crossings
recomputed with the top-up: 0.3582/0.3790/0.3823; 1/ν_eff =
1.003/1.376/1.571.

## 24. The tilted-variance (L,T)-uniformity family

Part A (Haar p=1, exactly enumerated collision Z at k*=−1, 6000
circuits/cell): ρ = 1.02 ± 0.03 across L=3–6 × T=2L–8L (flat-to-mildly-
rising profile, (L,T)-uniform in shape); v(0)/T T-independent within
each L to 3% (0.051–0.058/0.096–0.103/0.101–0.104/0.152–0.159 at
L=3/4/5/6); the interpolation identity per cell ≤ 2.5e-6; tilted ESS
flags the largest (L,T) cells (down to 4–29 effective samples — the
honest conditioning boundary).

Part B (Clifford disorder, fresh t=L/2 trajectories, B=4e6/2.4e6/1.6e6):
  L= 8 p=0.16: v0 = 0.0458  ρ = 0.872(0.000)  κ = 0.429  ESSmin = 141,542
  L=12 p=0.16: v0 = 0.0477  ρ = 0.878(0.002)  κ = 0.402  ESSmin = 1,251
  L=16 p=0.16: v0 = 0.0485  ρ = 0.888(0.006)  κ = 0.365  ESSmin = 23
  L= 8 p=0.22: v0 = 0.0563  ρ = 0.890(0.001)  κ = 0.361  ESSmin = 42,498
  L=12 p=0.22: v0 = 0.0577  ρ = 0.894(0.002)  κ = 0.340  ESSmin = 364
  L=16 p=0.22: v0 = 0.0584  ρ = 0.897(0.008)  κ = 0.327  ESSmin = 16
— the v21 sub-Gaussian reading CONFIRMED on well-conditioned data (the
leading cumulant overshoot 1/ρ ≈ 13–15%) and mildly de-sub-Gaussianizing
in L (0.872 → 0.888 at p=0.16); the per-site untilted variance rate
v0 = Var/(2Lt) ≈ 0.046–0.049 (p=0.16) / 0.056–0.058 (p=0.22),
L-stable.  The t=4L production npz cannot carry this
measurement (tilted ESS = 1); the stale within-sample profiles are kept
in the JSON, flagged.

## 25. The n=5 L=8 block route (v22_n5_L8_block_v1.py)

The mom0∩triv.triv sector at nb=4 = the orbits of (S₅×S₅)⋊Z₄ on (S₅)⁴;
the canonical-id pass is p-independent (memmapped).  Validation: the
deposited n=5 L=4 triv3 rows reproduced to 1.6e-14 (p=0.44 and 0.32);
the L=6 blocks (K=57 orbits) against fresh unrestricted
colour-restricted Arnoldi.  The L=8 rung p-grid (0.44–0.50) is
checkpointed in v22_n5_L8_rung.json (see the file for the completed
points; the assembly is ~1.2 h per p-point on this 3 GB machine).
