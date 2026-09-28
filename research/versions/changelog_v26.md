# Changelog — v26 (closing-rate diagnostics pass)

Date: 2026-09-29 (build 2026-09-28 20:32 UTC). Script: `patch_v26_closing.py`.
Sources preserved unmodified: `manuscript_revised_v25_tjp.tex`,
`supplement_v7.tex` (and all earlier versions). New files:
`manuscript_revised_v26.tex/.pdf`, `supplement_v8.tex/.pdf`, this changelog,
`README_v26.md`, `certificate_sha256_v13.txt`.

Provenance note: two dispatches executed the user's two-part request
concurrently (the worklog carries both coordination entries). The parallel
instance claimed and pushed v25 (the TJP editorial pass, 2b14c43) and
explicitly reserved v26 for the compute-extension promotion; this pass is
that promotion, built on the canonical v25 as base.

## 1. Effective closing rates (Sec. II.G)

New table `tab:closingrates` + two paragraphs between the L=8 rung paragraph
and the Scope note. Definitions per consecutive-size pair (ΔL = 2):
σ_eff = ΔL⁻¹ log[gap12(L)/gap12(L+ΔL)] (the exponential / interface-tension
reading) and α_eff = log[gap12(L)/gap12(L+ΔL)] / log[(L+ΔL)/L] (the
power-law reading). Values (computed by `v25_sigma_extract.py`, all
cross-checks against the quoted closings and scaled gaps PASS):

- σ_eff: n=3: 0.297/0.187/0.137 (L=4→6/6→8/8→10); n=4: 0.331/0.214;
  n=5: 0.376/0.258.
- α_eff: n=3: 1.466/1.297/1.224; n=4: 1.632/1.489; n=5: 1.857/1.794.

Reading (honest, directional): at matched sizes both rates rise
monotonically with n; at n=3 they decay with size as a continuous
transition requires (L·gap12 saturates); at n=4 the closing sits at the
marginal level over L=6→8 (α_eff = 1.489); at n=5 it is above it at every
measured interval. Three sizes do not yet separate the asymptotics at n=5 —
the crossover statement is kept explicit.

The abstract gained one clause ("...and dual effective closing rates that
separate the continuous, marginal and first-order behaviours at matched
sizes"); the Conclusion's ladder paragraph gained the table pointer; the
Conclusion's extensions sentence gained the deposited-status continuation
(the d=3 locator scans: minimum at p≈0.85 at both L=4 and L=6, two-size
closing factor 2.39 vs 2.12 at d=2).

## 2. Last-digit correction

6·gap12 = 6×0.806 = 4.836 at n=5, L=6 was quoted "4.85" in two places (the
size-ladder prose and the table row); corrected to "4.84" in both.

## 3. Supplement (v8)

Two new paragraphs at the end of Sec. S7:
- **Effective closing rates of the two-phase gap:** the extraction script,
  definitions, and cross-check protocol (pure arithmetic on the main-text
  table values; the n=3 L=10 rate from the deposited envelope 6.21).
- **The local-dimension extension (d=3):** the orbit table is
  d-independent, so the deposited ids array serves d=3; the block-route
  validation at d=3 (vs the unrestricted iterative route to 8×10⁻¹⁵ at
  L=4; the exact p=1 anchors (1/143)^{2nb} to 1.3–1.6×10⁻¹⁴ at L=4,6);
  the deposited locator scans (`v25_n5_d3_locator.json`): interior minimum
  at p≈0.85 at both L=4 (gap 1.482) and L=6 (gap 0.621), closing factor
  2.39 vs 2.12 at d=2, 6·gap12 = 3.73 below the d=2 value 4.84 — the
  first-order direction strengthens with local dimension. The L=8 d=3
  rung and the finer d=2 grid follow the same route (in flight; no
  numbers cited in the text).

## Verification

- Every patch anchor asserted to occur the stated number of times
  (5 manuscript edits + 1 supplement edit + header replacements).
- Residual-token report on both outputs (visible lines only): forbidden
  phrases = 0; stray "now" = 0.
- tectonic: both PDFs built (583.73 KiB / 214.43 KiB); warnings unchanged
  from the v23/v24/v25 baseline.
- pdftotext confirms: the closing-rates table renders with the exact
  values; the abstract clause; "6.85→4.84" at both sites; the two new
  Supplement paragraphs; 39 pages.
- The d=3 numbers are verbatim from `v25_n5_d3_locator.json` /
  `validate_d3.log` (hashed in `certificate_sha256_v13.txt`).
