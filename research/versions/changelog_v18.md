# Changelog v18 — n=4 full S₄ colour resolution, n≥5 first-order test,
# and the Haar SMC record-multifractality run (Target C)

From v17a.  All files NEW (never-overwrite honored).

## S.1 What changed

1. **Sec. sec:n4n5 (new)** — the annealed four-replica point with FULL
   S₄ colour resolution at L=4,6,8 (Table tab:n4annealed): p_c^{(4)} =
   0.40(2) (crossings 0.35820 → 0.37899, bracket 0.385–0.415),
   1/ν_eff = 1.28 rising toward the q=4 Potts 3/2, ξ/L of order unity
   (continuous), σ multiplet 9-fold in std⊗std, ordering
   triv > std > two > std⊗sgn > sgn, λ₁ simple.  The amplitude ratio
   DRIFTS (0.128 → 0.203) — honestly reported as the marginal-class
   degradation of the one clean n=2,3 diagnostic (log corrections,
   ε–marginal mixing; Cardy1986 added).
2. **n=5 first-order diagnostics (in sec:n4n5)** — the pinv Weingarten
   channel (Gram rank 119/120) validated by the exact p=1 closed form
   (per-bond 1/14); L=4 21-point scan: two-phase gap12 tightens
   2.15 → 1.92 → 1.71 (n=3→4→5 at own p_c), sharpness steepens
   5.4 → 6.2 → 7.2, gap12-minimum locator calibrates p_c^{(5)} ≈ 0.48–0.50.
   The decisive two-size test (L=6) is implemented and validated but
   exceeds the sandbox budget — stated as such.
3. **Sec. sec:smcnumerics (new) + Table tab:smchaar** — the FIRST
   numerical quenched record SCGFs for Haar circuits (grok's Target C,
   qwen's theorem target 2, the open problem of the v1 assessment):
   ψ(k) curves at 16 (L,p) points, τ(q), D(q) — genuine record
   multifractality (D-spread up to 1.96 nats/period at L=8, p=0.4),
   per-site entropy rate L-independent to 5%, NO finite-q freezing up to
   q=3 (min |τ″| = 0.24), annealed-quenched gap measured, ESS reliability
   protocol with an N=1536 top-up.
4. **Abstract** — two new clauses (the n=4/n=5 results; the SMC run).
5. **Open problems (Discussion)** — rewritten: n≥3 spectral data now exist
   at n=3,4; remaining targets are the n=5 two-size confirmation, the
   growth-rate regularity, the q=n-Potts conjecture; the record-LD item
   now carries the first numerical freezing bounds.
6. **Bibliography** — Cardy1986 added (q=4 log corrections).

## S.2 What did NOT change

All prior sections and their numbering; the deposited data and v17a
results; every previously stated theorem/proof (the new sections are
strictly additive); the never-overwrite convention (v18 files are new).

## S.3 Validation summary

Annealed route: n=2 vs Kaufman 3·10⁻¹⁵ (L=8); n=3 vs deposited scan 10⁻¹⁵
(L=6); n=4 vs dense 3.6·10⁻¹⁵ (L=4); 25-block completeness/idempotency
2.5·10⁻¹⁶; p=1 closed form exact for n=2..5 (pinv check); pinv identity
3·10⁻¹⁵; momentum content 1.00 at every record.  SMC route: brute-force
unbiasedness (L=4, 4 decades of Z, 2σ); p=1 exact Markov chain (1.4σ up
to Z ~ 4·10¹⁰); deposited-surprisal agreement (z=0.86); ψ(0)=0; internal
curvature identity 0.428 vs 0.427; ESS protocol + N=1536 top-up (z ≤ 1.4).

Two implementation bugs were caught and fixed by the validation chain:
(1) a broadcast bug in the batched measurement (X[:, :, 1-keep, :] mixed
particle rows — silent state corruption at N>1, caught by the brute-force
unbiasedness check Vb); (2) a ring-translation bug (np.roll value-shift
vs axis permutation — caught by the n=3 deposited-spectrum comparison V2).
Also a character-table typo (S₅ sgn at cycle type (3,2)) caught by the
convolution-idempotency check.

## S.4 Files

Scripts (workspace root): n45_annealed_lib_v1.py (library),
n45_annealed_validate_v1.py (V1–V8), n4_annealed_scan_v1.py (scan/blocks/
growth), n4_eps_L8_v1.py + n4_eps_fast_v1.py (λ_ε top-ups),
n5_annealed_scan_v1.py (scan/blocks), n45_analyze_v1.py (master analysis),
haar_smc_lib_v1.py (SMC core), haar_smc_v1.py (validate/produce/analyze),
haar_smc_topup_v1.py (N=1536 top-up), make_cert_v5.py.
Results: mipt_results/n4_annealed_scan_{L4,L6,L8,}_v1.json,
n4_colour_table_v1.json, n4_growth_v1.json, n4_eps_L{4,6}_v1.json,
n4_eps_L8_fast_v1.json, n5_annealed_scan_v1.json, n45_final_v1.json,
haar_smc_L{6,8,10,12}_p{...}_v1.json (16 files),
haar_smc_topup_L{8,10,12}_p{...}_v1.json (6 files),
haar_smc_summary_v1.json.  Manuscript:
versions/manuscript_revised_v18_n4n5-smc.tex/.pdf (33 pp), built by
versions/patch_v18_n4n5smc.py from v17a with asserted anchors; compiled
with tectonic; content verified with pypdf.  Report:
versions/mipt_numerical_report_v7.md (Secs. 12, 12a, 13).
Certificates: versions/certificate_sha256_v5.txt.

## S.5 Scope and honest limits

n=4: exact finite-size data, L ≤ 8, systematic extrapolation; the
amplitude-ratio diagnostic is NOT clean at n=4 (marginal class) — reported
as such.  n=5: single-size diagnostics only (L=6 out of budget); the
first-order claim is supported, not established.  SMC: statistical
estimates, T = 2L (not the long-time limit), no population extrapolation
beyond ESS; the freezing statement is a finite-size bound.  The n=5 L=6
and n=6 routes are implemented, validated, and ready for a larger machine.
