# README — v27 (extension-integration pass)

**Deliverable (current submission candidate):** `manuscript_revised_v27.tex/.pdf`
+ `supplement_v9.tex/.pdf`, built by `research/scripts/v22-exactZ3-n5L8/patch_v27_extL8.py`
from the canonical v26 (`manuscript_revised_v26.tex`, the closing-rate
diagnostics pass) with `supplement_v8.tex`. All earlier versions preserved
unmodified. Changelog: `changelog_v27.md`; ledger:
`certificate_sha256_v14.txt`.

## Version map (this round)

- **v26** (previous): the closing-rate diagnostics pass — σ_eff/α_eff
  table, one abstract clause, the last-digit fix, Supplement v8 (the
  extraction protocol + the d=3 local-dimension extension at the
  two-size level).
- **v27** (this pass): the extension-integration pass — the completed
  extension campaign's two deposits (the d=3 L=8 rung closing the d=3
  three-size ladder; the finer d=2 locator grid refining the L=8
  minimum to 0.4797 at p=0.465) integrated into the tables, the L=8
  rung paragraph, the locator sentence, the Scope note, one abstract
  clause, the Conclusion, and Supplement S7.

## The v25 extension campaign (complete)

- **All queue points computed and merged** (verified 7/7 against
  `v25_ext_config.json`; repo 0/0 with origin):
  - d=3 locator scans (L=4: 19 pts; L=6: 7 pts) —
    `v25_n5_d3_locator.json`: interior minimum at p≈0.85 at both sizes
    (gaps 1.482 / 0.621), hashed in `certificate_sha256_v13.txt`.
  - d=3 L=8 rung — `v25_n5_L8_rung_d3.json`: 0.948 / 0.453 / 0.519 at
    p=0.82/0.84/0.86, interior minimum at p=0.84.
  - d=2 finer L=8 grid — `v25_n5_L8_finegrid.json`: 0.484 / 0.480 /
    0.485 / 0.501 at p=0.455/0.465/0.475/0.485, minimum at p=0.465.
  - Both new JSONs hashed in `certificate_sha256_v14.txt`, together
    with the per-point run logs and the patch script.
- **Three-size readings at d=3**: gap level below the d=2 value at every
  size; 8·gap12 = 3.62 (vs 3.84 at d=2, envelope 6.53); interval
  closings ×2.39 then ×1.37 (vs ×2.12, ×1.68 at d=2) — level ordering
  first-order with local dimension, interval rates in the crossover
  region at both dimensions.

## Turkish Journal of Physics — submission checklist

- Abstract ≤ 250 words ✓; keywords ✓; numbered references ✓;
  declarations block (competing interests, funding, AI declaration,
  data availability, ethics) ✓; ORCID ✓; dedicated Conclusion ✓;
  39 pp + 11 pp supplement.
- The source is revtex4-2 (aps,prx): transcode to the TJP template
  (DergiPark) at submission — the content is already structured for it.
- **Open author actions:** mint the figshare DOI (the Declarations carry
  the "DOI to be assigned prior to submission" note); optionally sharpen
  the title toward the replica-ladder headline before submission; update
  the figshare bundle to include the v14 ledger and the two extension
  JSONs.

## Editorial review notes (recorded 2026-10-09, not executed)

A journal-readiness scan of v27 + supplement v9 was recorded in the
worklog (Task ID v25-ext-watch, 2026-10-09): zero informal-artifact
tokens in visible text; the demotion candidates identified there
(the PostBQP/CTD appendix material and the appendix-numerics simulation
block, both already appendix-resident) were judged to require an
author decision before any restructuring, and none was executed by the
integration pass.
