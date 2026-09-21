# Changelog — v16 (record SCGF: theorem-level items closed)

Section R. All changes are NEW VERSION FILES; v15 (spinor) is kept unmodified.

## R.1 Purpose

Close the four remaining theorem-level items of the research programme:

1. **Quenched SCGF thermodynamic limit** — Prop. `scgf` (new Sec. 7).
2. **Freezing realization** — Prop. `freeze` (new Sec. 7).
3. **Born-average hardness** — Remark `hardness` (new Sec. 7).
4. **Disorder–replica interchange** — Prop. `replica` (new Sec. 7).

## R.2 New mathematics and computations (all verified in this workspace)

### R.2.1 The record SCGF (Sec. 7, Eqs. dyadic/scgfdef/beta1exact)

- `P(R) = 2^{-X_R}` exactly, `X_R` = the number of random measurement outcomes
  (Gottesman–Knill; stabilizer measurement outcomes are uniform on their
  fibres). The record SCGF `Xi_L(beta) = ln E_Born[2^{-beta X_R}]/(2Lt)`.
- **Exact beta=1 endpoint**: `E_Born[2^{-X_R}] = E_omega[Sum_R p_R^2] = Z_2(t)` —
  the two-replica partition function, i.e. the transfer matrix of the paper
  computes the SCGF's beta=1 point exactly for every (L, p, t).
- `Z_2(t) = A(L) lambda_1^t` with `A` subexponential: A = 2.4512 (L=8, p=0.16),
  4.235 (L=12), 7.229 (L=16), 3.279 / 6.833 (L=8/12, p=0.22) — constant to 6
  digits for t >~ 3L; the L=16 evolution (3^16 = 43M configurations) gives
  Z_2 = 8.574e-72 and S~2 = 4.1291 at t=64.
  Hence `Xi(1) -> (ln W0 + f_H)/2` (the Houtappel free energy per measurement
  site): -0.08101 nats/site at p=0.16 (closed-form ladder L=8..32:
  -0.07974, -0.08062, -0.08087, -0.08099, -0.08101); -0.11082 at p=0.22.
- Quenched information density converges: xbar = 0.1448(1), 0.1470(1),
  0.1480(1), 0.1489(1) bits/site (L = 8, 12, 16, 24; tau = 4; p = 0.16).
- **Self-averaging**: Var(X_R)/(2Lt) = 0.104–0.106 (p=0.16) and 0.124–0.125
  (p=0.22), L-independent for L = 8–24 -> Var(xbar) = O(1/(Lt)) -> 0 (LDP).

### R.2.2 Freezing realization (Prop. freeze)

- Exact side: the tilted-vs-quenched entropy gap GROWS:
  S~2(inf) - E[S] = 0.19 bits (L=8) -> 0.57 bits (L=12), both sides exact
  (saturated tilted values S~2(inf) = 2.2243, 3.2496).
- Trajectory side: the collision-tilt ESS collapses to O(1)–O(10) records
  (12/40000, 3.9/40000, 1.4/30000, 1.0/15000 at L = 8, 12, 16, 24; tau=4);
  the naive E[P(R)] estimator degrades from 0.7% (L=8) to edge-dominated
  (L >= 16). REM-flavored interpretation (Derrida 1981), honestly scoped:
  the freezing point of the multifractal tau(q) is NOT claimed.

### R.2.3 Disorder–replica interchange (Prop. replica)

- Finite-L replica identity is exact (no interchange needed):
  E[ln P] = d/dbeta|_0 ln E[P^beta].
- The thermodynamic limit commutes with the replica derivative on beta in
  [0,1) (Gartner–Ellis under the verified LDP): the two-term cumulant
  expansion reproduces the measured Xi(0.25) to <1% at every L (e.g.
  -0.02351 predicted vs -0.0236(2) measured at L=8).
- **The gap persists**: g = Xi(1) + ln2*xbar = 0.0224, 0.0226, 0.0227
  nats/site at L = 8, 12, 16 (exact finite-t anchors; ~0.0228 at L = 24 with
  the A(L)-corrected lambda_1 anchor) — L-INDEPENDENT within errors
  (0.026–0.027 at p=0.22). The leading cumulant (ln2)^2 sigma^2/2
  = 0.0252 overestimates g by ~13% (sub-Gaussian record tails).

### R.2.4 Born-average hardness (Remark hardness)

The Gottesman–Knill / 2-design / average-case-hardness trichotomy with new
bibliography (Gottesman 1998; Aaronson–Arkhipov 2013; Bouland et al. 2018;
Derrida 1981; Dembo–Zeitouni 1998).

## R.3 Bug fix discovered by the new calibration (manuscript-level)

The deposited tilt chain (audit3_tiltchain.json) is at **t = L/2 periods**
(t = 4 at L=8, t = 6 at L=12), NOT "t = 4L" as the v15 text says in one
place (App. B paragraph; Sec. 5.2 already said "t=4"). Evidence: the exact
algebra evolution reproduces Z_2 = 1.4796e-2 and S~2 = 2.155 at (L=8, t=4)
and S~2 = 3.128 at (L=12, t=6) — to the deposited rounding; at t = 4L the
same quantities are 4.57e-18 and 2.2243. v16 fixes the App. B sentence and
records the convention in App. C. (The deposited L=12 quenched entropy
2.394(5) corresponds to a shorter chain than its exact values: our chain
gives 2.497(7) at t=4 and 2.632(5) at t=6; the exact annealed quantities
match at t=6.)

## R.4 New scripts, logs, results

- `scripts/mipt_scgf_exact.py` — the exact two-replica algebra evolution
  (3^L basis; factorised bond twirl alpha/beta table; diagonal measurement
  layer; M-A-M-B period order; observables Z_2 and P_{2,A} as linear
  functionals). Reproduces the deposited tilt chain exactly at both sizes.
- `scripts/mipt_born_scgf.py` — the vectorised phase-free F2 tableau
  simulator (B trajectories in parallel, uint64 row packing, 720 Sp(4,2)
  LUTs), tracking X_R and S_{L/2}; the SCGF/freezing statistics with
  bootstrap errors. New PCG64 seed contract (seed0 = 20260529 + cell).
- `results/scgf_exact.json`, `results/scgf_exact_addendum.json`,
  `results/scgf_born.json`, `results/scgf_born_raw_L{8,12,16,24}_p{16,22}.npz`
  (raw per-trajectory X and S arrays).
- `logs/mipt_scgf_exact.log`, `logs/mipt_born_scgf.log`.

## R.5 Files

- NEW: `versions/manuscript_revised_v16_scgf.tex/.pdf` (15 pp; v15 kept).
- NEW: `versions/mipt_numerical_report_v5.md` (Sec. 11: the record SCGF).
- NEW: `versions/changelog_v16.md` (this file).
- UPDATED (new version): `logs/certificate_sha256_v3.txt` (ledger v3).
- UPDATED (append-only): `research/README.md`.

## R.6 Verification summary

- Algebra evolution vs deposit: Z_2 (L=8, t=4): 1.479639e-2 vs 1.4796e-2;
  S~2: 2.1547 vs 2.155; (L=12, t=6): S~2 3.1281 vs 3.128. PASS.
- Tableau vs algebra (independent implementations): E[2^{-X}] = 0.12929(8)
  vs exact Z_2 = 0.12886 at (L=4, t=4); 1.4689e-2 vs 1.4796e-2 and
  3.8399e-5 vs 3.8173e-5 at (L=8, t=4) / (L=12, t=6) (0.3–0.7%, consistent
  with the Monte-Carlo error). PASS.
- Tableau vs deposit (distribution level, L=8): E[S] = 2.015(4) vs 2.019(4);
  ESS 6339 vs 5935. PASS.
- Z_2/lambda_1^t -> A(L) constant to 6 digits (t >= 3L). PASS.
- tectonic: v16 compiles (15 pages); all new propositions render.
