# research/ — the academic manuscript work (v14)

This directory completes the academic work that the deposited session logs
(`../previous chat.txt`, `../previous turns.txt`) left unfinished at the
v14 plan: the computations, the joint audit points, and the manuscript.

## What was reconstructed and verified

The deposited workspace (original machine, `/home/user`) is lost; the repo
carried only the two chat logs. The exact mathematics was rebuilt from first
principles and verified against **every** deposited exact number:

| item | status |
|---|---|
| Two-replica compression to the triangular-Ising transfer | rebuilt (per-site algebra {e0,e+,e-}; dense quantum transfer reproduces the Ising spectrum to 1e-10) |
| Closed-form weights (a,b,c,W0)(theta,d), both branches | **new closed form** (Eqs. wordered/wdisordered in the manuscript); reproduces the five exact enclosures, the benchmark, p_eff |
| Closed-form spectrum (Prop. spectrum, D6/Q2-b) | verified: dense vs closed over 108 configs, kernel/rank, commutators, benchmark crossings (8/8 to 5e-6), ratio row, amplitudes, gapless double zero |
| N3 Collatz–Wielandt enclosures | reproduced in exact rational arithmetic (C_comp = M1^2 tau); every bracket contains the deposited interval and the closed form |
| p_c^{(2)}(d) = (d-theta_c)/(d-1) | exact for d=2,3,5 |
| p_eff tilt mechanism (E1) | bulk + p_c^{(2)} values for d=2,3,5 match the deposit to 8 digits |
| N2 purification analysis | full re-analysis of the deposited dataset (recovered verbatim): all deposited numbers reproduced (0.16009/1.2486 etc.) |
| floorN released module (item 13) | corrected transform (Nelder-Mead 1e-6 intentionally untouched — the bug that stopped the previous session); provable no-op |
| I3 FSS rows | **quoted from the deposit** (raw I3 data not recoverable); audit-3 root-cause conclusions independently confirmed by the recovered parts |

## Layout

- `versions/` — `manuscript_revised_v14_audit3.tex/.pdf` (11 pp; the v14
  manuscript implementing the full audit-3 plan), `mipt_numerical_report_v3.md`,
  `changelog.md` (§P), the sha256 ledger in `../logs/`.
- `scripts/` — the computation scripts (see the report §9).
- `results/` — JSON outputs. `logs/` — run logs + `certificate_sha256.txt`.

## Reproduce

```bash
cd scripts
python3 mipt_audit3_gauss_proof.py     # the verification suite (S1–S11)
python3 mipt_audit3_cw_exact.py        # exact-rational CW enclosures (N3)
python3 mipt_purif_analysis.py         # the purification locator (N2)
python3 mipt_fss2_floorN.py            # the 1/N floor demonstration
cd ../versions && tectonic manuscript_revised_v14_audit3.tex
```

Versioning policy: revisions are always new version files (v13 -> v14,
report v2 -> v3); nothing is overwritten.

## v16 (record SCGF): the four theorem-level items closed  *(parallel line, merged)*

> The v16 lineage had two parallel rounds (both preserved, nothing
> overwritten): `manuscript_revised_v16_recovered.*` (the recovered-data
> round) and `manuscript_revised_v16_scgf.*` (the record-SCGF round below).
> The canonical chain continues v16_recovered -> v17 -> v18 -> v19 -> v20;
> the v16_scgf theorem closures are integrated by v21.

- `versions/manuscript_revised_v16_scgf.tex/.pdf` — v15 + new Sec. 7 (the
  record SCGF: thermodynamic limit, freezing realization, disorder–replica
  interchange, Born-average hardness) + App. C; the tilt-chain time
  convention fixed (t = L/2 periods).
- `scripts/mipt_scgf_exact.py` — exact two-replica algebra evolution (3^L
  basis); reproduces the deposited tilt chain to its rounding (Z_2 =
  1.4796e-2, S~_2 = 2.155 at L=8/t=4; S~_2 = 3.128 at L=12/t=6).
- `scripts/mipt_born_scgf.py` — vectorised tableau simulator tracking the
  record information X_R (P(R) = 2^{-X_R} exactly); cross-validated against
  the exact Z_2 at three sizes and against the deposited quenched chain.
- Headline numbers: Xi(1) → (ln W0 + f_H)/2 = −0.08101 nats/site (p=0.16);
  xbar → 0.1489 bits/site; Var(X)/(2Lt) = 0.105 L-independent; the tilt ESS
  collapses to O(1)–O(10) records; the Jensen gap g = 0.0222(5) nats/site is
  L-independent (the annealed–quenched free-energy gap persists).
- `versions/changelog_v16.md` (§R), `versions/mipt_numerical_report_v5.md`
  (§11–12), `logs/certificate_sha256_v3.txt` (ledger v3).

## v18 addendum (this release): research/versions/README_v18_n4n5-smc.md

The v18 round (n=4 full S₄ colour resolution at L=4,6,8; the n=5
first-order diagnostics; the Haar SMC record-multifractality run — grok's
Target C) lives in `scripts/v18-n4n5-smc/`, `results/v18-n4n5-smc/`,
`logs/v18-n4n5-smc/`, and `versions/` (manuscript v18, report v7,
changelog v18, certificate v5).  See
`versions/README_v18_n4n5-smc.md` for the summary and
`versions/changelog_v18.md` for the full record.  Main results:
p_c^{(2)}=0.233810 < p_c^{(3)}=0.305(3) < p_c^{(4)}=0.40(2) <
p_c^{(5)}≈0.48–0.50 vs quenched 0.1597(8); 1/ν_eff 1.15 → 1.28 (rising
toward the q=4 Potts 3/2); Haar record multifractality measured for the
first time (D(q) nonconstant), freezing bounded away for q ≤ 3 at L ≤ 12.

## v21 (Clifford record-count closure): the parallel line integrated

The v16_scgf theorem-closure line (preserved as
`versions/manuscript_revised_v16_scgf.tex` and merged from the parallel
git line) is integrated into the canonical chain by
`versions/manuscript_revised_v21_clifford.tex` — with the framing
corrected: its "quenched SCGF" is the **disorder-direction SCGF**
(annealed record moment at fractional order q=1+β; for fixed Clifford ω
the record surprisal is ω-measurable, so the trajectory direction is
trivial and all nontrivial record statistics are disorder statistics,
with E_ω[2^{(1-n)N_rand}] = Z̄_n at integer order).  New Sec. IV.F:
exact β=1 anchors with the Houtappel closure −0.08101 nats/site;
self-averaging Var/(2Lt)=0.105 (the measurable criterion, verified);
the L-independent annealed–quenched gap **g = 0.0226(2) nats/site**
(the r=1 interpolation remainder; sub-Gaussian 13%); the collision-tilt
ESS law ESS/B = exp[−2Lt(Λ(2)−2Λ(1))] (estimator difficulty, not a
transition — consistent with Theorem no-freeze); the
Gottesman–Knill/2-design/Haar complexity trichotomy.  Supplement v4
gains the deferred proofs (Theorem rem, Prop. SMC) and the
record-count runs (Sec. S7: calibration with the t=L/2 convention fix,
anchors, ladder, reproduction).  Companion docs: changelog_v21.md,
README_v21_clifford.md, mipt_numerical_report_v9.md (Secs. 16–20, the
framing-correction record and the corrected ladder), ledger
certificate_sha256_v8.txt.
