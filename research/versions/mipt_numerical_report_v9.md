# Numerical report v9 — the Clifford record-count closure: the disorder
# SCGF measured, the framing correction, and the corrected ladder
(v21; continues report v8 Secs. 14/14a/15.  All β=1 anchors exact; the
trajectory statistics carry bootstrap s.e. (200 resamples) as stated.
The runs themselves are the parallel-line suite (v16_scgf round,
scripts `mipt_scgf_exact.py` / `mipt_born_scgf.py`, results
`scgf_exact.json` / `scgf_exact_addendum.json` / `scgf_born.json`);
this report re-reads them under the v21 framing and records the
corrections.)

## 16. The framing correction (what the "quenched SCGF" actually is)

The v16_scgf round defined Ξ_L(β) = (2Lt)^{-1} ln E_Born[2^{-βX_R}]
and called it the quenched record SCGF.  The v20/v21 audit establishes
the correct identity of this object:

* For a fixed Clifford realization ω the unsigned stabilizer group
  evolves identically on every branch (rem:clifford), so
  P_ω(R) = 2^{-N_rand(ω)} for **every** positive-probability record:
  X_R is ω-measurable, the trajectory variance is identically zero,
  and ψ_{L,ω}(k) = k N_rand(ω) ln 2 / T is exactly affine.
* E_Born averages over disorder and trajectories jointly, and since
  2^{-βX} is ω-measurable the trajectory average is inert:
  E_Born[2^{-βX}] = E_ω[2^{-βN_rand}] — the **annealed** record moment
  at fractional order q = 1+β.  In v21 notation: Λ_L(β).
* Integer order: E_ω[2^{(1-n)N_rand}] = E_ω Z_{n,ω} = Z̄_n.  n=2 is the
  transfer matrix (the free cross-check of rem:clifford, verified at
  L=16/p=0.16/t=2 to 4 digits in App. B and here at L=8/12, t=4L, to
  0.6–0.7%); n=3 is the v17 three-replica object — so the trajectory
  estimate of Λ(2) is an estimate of Z̄₃.
* Consequence for "freezing": the ESS collapse is an estimator
  statement (the clone-collapse clause of the SMC contract), not a
  thermodynamic transition; Theorem no-freeze classifies the family as
  its degenerate zero-variance case.  The exact law
  ESS/B = exp[−2Lt(Λ(2)−2Λ(1))] carries the collapse.

Checks performed this round: (i) Var_ω(X) recomputed from the raw npz
ladder — 0.10547/0.10441/0.10581/0.10481 per site (L=8–24, p=0.16),
confirming the L-independence; (ii) the ESS law verified against the
measured ESS at every L ≤ 16 (11.7/11.73, 3.9/3.93, 1.4/1.41, 18.2/18.23,
2.7/2.74, 1.1/1.07 — the within-sample ratios); (iii) the tilted
density m̃(1) = 0.0974 at L=8 re-read against the Gaussian prediction
x̄ − ln2·σ² = 0.0717 (the tilt shifts 65% of the Gaussian prediction —
sub-Gaussian).

## 17. The corrected ladder (two data-entry slips fixed)

The v16_scgf ladder mixed finite-t anchors and λ₁-asymptotes.  Corrected
values (finite-t 3^L evolution at L ≤ 16; amplitude-corrected λ₁ at
L=24 with A(24) ≈ 21.4 extrapolated from log A(L) ≈ 0.135 L):

| L | p | Λ_L(1) anchor | x̄ (bits/site) | g = Λ(1)+ln2·x̄ |
|---|---|---|---|---|
| 8 | 0.16 | −0.077984 (finite t=32) | 0.14479 | 0.02238 |
| 12 | 0.16 | −0.079362 (finite t=48) | 0.14703 | 0.02255 |
| 16 | 0.16 | **−0.079901** (finite t=64; was mis-entered as −0.080867, the λ₁ asymptote) | 0.14803 | **0.02270** (was 0.0217) |
| 24 | 0.16 | −0.080325 (A-corrected) | 0.14890 | 0.02288 |
| 8 | 0.22 | −0.106382 (finite t=32) | 0.19280 | 0.02726 |
| 12 | 0.22 | −0.108278 (finite t=48) | 0.19512 | 0.02697 |

Summary: **g = 0.0226(2) nats/site, L-independent** (the parallel
line's 0.0222(5) was the stale summary; the four corrected values are
0.02238/0.02255/0.02270/0.02288).  At p=0.22: g ≈ 0.027.  The
leading-cumulant estimate (ln2)²σ²/2 = 0.0252 overshoots by ≈13% — the
tilted-variance profile decays (sub-Gaussian), the first measured data
on the profile whose uniformity the Discussion flags as open.

## 18. The interpolation-identity reading of the gap

g·(2Lt) = ln E_ω[2^{-N}] − E_ω[ln 2^{-N}] is exactly the r=1 remainder
of Prop. replica-int applied to X = 2^{-N_rand}:
g = (2Lt)^{-1} ∫₀¹ (1−s) Var_s(ln X) ds.  The v19 verification of that
identity (no_freeze_theory_v1.py: 4×10⁻⁸ relative on an exact synthetic
law; the quadratic small-m rate 0.994–0.998) and this measurement are
mutually consistent: the r=1 remainder is L-independent per site, and
the quadratic (leading-cumulant) approximation of it overshoots by 13%,
i.e. Var_s decays in s faster than the untilted variance would suggest.

## 19. Anchors, amplitudes, and the Houtappel closure (unchanged,
## re-verified)

A(L) = 2.4512/4.2354/7.2288 at L=8/12/16 (p=0.16), constant to six
digits for t ≳ 3L (z2_tail in scgf_exact.json: 2.45088…2.45120 at
t=8…32, L=8); log λ₁/(2L) = −0.07974/−0.08062/−0.08087/−0.08099/
−0.08101 for L=8/12/16/24/32 → the closed form ½(log W₀+f_H) =
−0.08101 nats/site.  The L=16 exact evolution (3^16 configurations)
gives Z₂ = 8.574×10⁻⁷² and S̃₂ = 4.1291 at t=64, consistent with the
λ₁ scaling and the A(L) sequence.  Deposit calibration unchanged:
Z₂ = 1.479639×10⁻² (deposit 1.4796×10⁻²), S̃₂ = 2.1547 (2.155) at
L=8/t=4; S̃₂ = 3.1281 (3.128) at L=12/t=6 — fixing the deposited
chain's convention at t = L/2 periods (at t=4L=32 one gets
Z₂ = 4.57×10⁻¹⁸, 29 orders away).  The deposited L=12 quenched entropy
2.394(5) remains a provenance exception (2.497(7) at t=4, 2.632(5) at
t=6 in our chains) — flagged in the main text and Supplement S7;
nothing depends on it.

## 20. Files and reproduction

Unchanged from the v16_scgf round (scripts
`research/scripts/mipt_scgf_exact.py`, `research/scripts/mipt_born_scgf.py`;
results `research/results/scgf_exact.json`,
`scgf_exact_addendum.json`, `scgf_born.json`, and the eight raw npz
arrays; logs `research/logs/mipt_scgf_exact.log`,
`mipt_born_scgf.log`).  Hashes: ledger v8
(`research/versions/certificate_sha256_v8.txt`) for the round files and
the suite; the parallel-line ledger
(`research/logs/certificate_sha256_v3_scgf.txt`) remains valid for the
suite as deposited.
