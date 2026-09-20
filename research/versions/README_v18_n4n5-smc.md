# README v18 — n=4 full S₄ colour resolution, n≥5 first-order test, Haar SMC (Target C)

This release (v18) closes three items from the v17a open list:

1. **n=4 with full S₄ colour resolution at larger L** — the previous
   datum was a 2-size exploratory run with a σ proxy; now: three sizes
   (L=4,6,8), the true σ sector (std⊗std, 9-fold), the complete 25-block
   colour resolution, crossings 0.35820/0.37899 → p_c^{(4)} = 0.40(2),
   1/ν_eff rising toward the q=4 Potts 3/2, ξ/L order unity (continuous),
   and an honest report that the amplitude-ratio diagnostic degrades at
   the marginal class (drifts 0.128 → 0.203; log corrections).
2. **The n≥5 first-order test** — n=5 at L=4 with the pseudo-inverse
   Weingarten channel (validated exactly at p=1, per-bond 1/14):
   two-phase gap12 tightens 2.15 → 1.92 → 1.71 (n=3→4→5), sharpness
   steepens 5.4 → 6.2 → 7.2, and the gap12-minimum locator calibrates
   p_c^{(5)} ≈ 0.48–0.50.  The decisive two-size test (L=6) is implemented
   and validated but exceeds the 3 GB/2-core sandbox budget — stated as
   such in the manuscript.
3. **The Haar SMC record-multifractality run (Target C)** — the first
   numerical quenched record SCGFs for Haar circuits: ψ(k) at 16 (L,p)
   points (L=6..12), τ(q), D(q) — genuine record multifractality
   (D nonconstant; spread up to 1.96 nats/period), per-site record
   entropy rate L-independent to 5%, NO finite-q freezing up to q=3,
   annealed-vs-quenched gap measured, ESS reliability protocol with an
   N=1536 top-up.  Validated by brute-force record enumeration (L=4),
   the exact p=1 Markov chain, and the deposited Born-sampling data.

Key files: versions/manuscript_revised_v18_n4n5-smc.tex/.pdf (33 pp),
versions/mipt_numerical_report_v7.md, versions/changelog_v18.md,
versions/certificate_sha256_v5.txt; scripts and results listed in the
changelog Sec. S.4.  Everything is NEW (never-overwrite honored); v17a
and all earlier versions remain untouched.

Main results at a glance:
- p_c^{(2)} = 0.233810 < p_c^{(3)} = 0.305(3) < p_c^{(4)} = 0.40(2) <
  p_c^{(5)} ≈ 0.48–0.50 (single-size locator), against the quenched
  0.1597(8) — the annealed points move away from the quenched transition.
- 1/ν_eff: 1.15 (n=3) → 1.28 (n=4, rising toward 3/2) — the q=n-Potts
  slope-exponent sequence.
- Record multifractality of Haar circuits: MEASURED (first time);
  freezing: bounded away for q ≤ 3 at L ≤ 12.
