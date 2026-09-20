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
