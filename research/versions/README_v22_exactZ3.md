# README v22 — the exact Z̄₃ closure (Λ(2)), the q=4 log-correction
# re-read, the tilted-variance family, and the n=5 L=8 rung

This release (v22) delivers the four computational directives of the
round, each machine-verified:

1. **The exact Z̄₃ computation via the v17 operator closes Λ(2)
   exactly.**  The identification rests on a verified fact: the
   two-qubit Clifford group is an exact conjugation 3-design (1.6e-14
   against the Haar twirl; n=2 control 2.1e-14; n=4 fails 0.578 — the
   negative control).  The exact values at the production cells
   (t = 4L): Λ(2) = −0.1219/−0.1239/−0.1245 at L=8/12/16 (p=0.16).  The
   ESS-law exponent is corrected to 0.0340/0.0349/0.0353 nats/site
   (L-independent) — the v21 trajectory estimates (0.0159/0.0080/0.0049)
   were biased low by the ESS collapse, quantified exactly
   (ESS_true/B = 2.7e-8 at L=8).  Cross-checked by a well-conditioned
   β=2 trajectory run (rel 1.95e-3 at 0.4σ).  λ₁⁽³⁾ ladder +
   subexponential amplitudes A₃ deposited.
2. **The marginal-q=4 log-correction analysis corrects the target and
   the reading.**  The q=4-Potts amplitude ratio is x_σ/x_ε = 1/4 (not
   the Ising 1/8); the measured drift 0.1315→0.2378 (L=4..10) is
   logarithmically slow CONVERGENCE to 1/4 (two-term marginal fit,
   residual ≤ 8e-4), not degradation — with the n=3 control converging
   cleanly to 1/6 and the slope exponent rising through 3/2 with the
   1/lnL correction.  The missing L=8 λ_ε values are recomputed
   (validated to 5.7e-16 against the deposit).
3. **The tilted-variance (L,T)-uniformity measurement** — the open
   self-averaging criterion — is delivered as a measured family: Haar
   p=1 exactly-enumerated collision partition functions (flat profile,
   ρ = 1.02±0.03, (L,T)-uniform) vs the Clifford disorder direction
   (sub-Gaussian, ρ ≈ 0.885 at L=8), with the production-t=4L arrays
   flagged unusable (tilted ESS = 1).
4. **The n=5 L=8 rung** is computed by the symmetry-reduced dense block
   (the mom0∩triv.triv orbit basis of (S₅×S₅)⋊Z₄), validated against
   the deposited L=4 spectrum to 1.6e-14; see v22_n5_L8_rung.json for
   the completed p-grid.

Plus the deposit-integrity repair: `gap_utils.py` (the Weingarten
channel library underpinning the whole v17–v19 suite) was missing from
the repository and is reconstructed and re-validated (the full deposited
V1–V8 batteries pass).

Key files: versions/manuscript_revised_v22_exactZ3.tex/.pdf (38 pp),
versions/supplement_v5.tex/.pdf (11 pp), versions/changelog_v22.md,
versions/mipt_numerical_report_v10.md,
versions/certificate_sha256_v9.txt; scripts and results in
scripts/v22-exactZ3-n5L8/ and results/v22-exactZ3-n5L8/.  Everything is
NEW (never-overwrite honored); v21 and all earlier versions remain
untouched.

Headline corrections carried into the manuscript:
- prop:ess exponents 0.0159/0.0080/0.0049 → exact 0.0340/0.0349/0.0353
  (the trajectory values are within-sample ratios, biased by the
  collapsed estimator).
- The q=4 caption target 1/8 → 1/4; "degrades at the marginal class" →
  "converges logarithmically to 1/4".
