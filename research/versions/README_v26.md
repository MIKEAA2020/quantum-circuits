# README — v26 (closing-rate diagnostics pass)

**Deliverable (current submission candidate):** `manuscript_revised_v26.tex/.pdf`
+ `supplement_v8.tex/.pdf`, built by `research/scripts/v22-exactZ3-n5L8/patch_v26_closing.py`
from the canonical v25 (`manuscript_revised_v25_tjp.tex`, the TJP editorial
pass by the parallel dispatch) with `supplement_v7.tex`. All earlier
versions preserved unmodified. Changelog: `changelog_v26.md`; ledger:
`certificate_sha256_v13.txt`.

## Version map (this round)

- **v25** (`manuscript_revised_v25_tjp.*`, commit 2b14c43): the TJP
  editorial pass — dedicated Conclusion, Discussion splits, exactness
  summary, conjecture label, spine pointer.
- **v26** (this pass): the compute-extension promotion reserved by the
  worklog coordination claim — the interface-tension extraction from the
  deposited size ladder (new Table `tab:closingrates`: σ_eff/α_eff), one
  abstract clause, the last-digit fix (4.85→4.84), two Conclusion
  continuation sentences, Supplement v8 (the extraction protocol + the
  d=3 local-dimension extension).

## Turkish Journal of Physics — submission checklist

- Abstract ≤ 250 words ✓; keywords ✓; numbered references ✓; declarations
  block (competing interests, funding, AI declaration, data availability,
  ethics) ✓; ORCID ✓; dedicated Conclusion ✓; 39 pp + 11 pp supplement.
- The source is revtex4-2 (aps,prx): transcode to the TJP template
  (DergiPark) at submission — the content is already structured for it.
- **Open author actions:** mint the figshare DOI (the Declarations carry
  the "DOI to be assigned prior to submission" note); optionally sharpen
  the title toward the replica-ladder headline before submission.

## The v25 extension campaign (in flight)

- **Done:** d=3 block-route validation (vs the unrestricted iterative
  route to 8×10⁻¹⁵; exact p=1 anchors (1/143)^{2nb} to 1.3–1.6×10⁻¹⁴) and
  the d=3 locator scans at L=4 (19 points) and L=6 (7 points) —
  `results/v22-exactZ3-n5L8/v25_n5_d3_locator.json`: interior minimum at
  p≈0.85 at both sizes (gaps 1.482 / 0.621), two-size closing factor
  2.39 vs 2.12 at d=2, 6·gap12 = 3.73 below the d=2 value 4.84.
- **Queue** (`v25_ext_config.json`): the d=3 L=8 rung grid
  {0.84, 0.82, 0.86} and the d=2 finer locator grid
  {0.465, 0.475, 0.455, 0.485}, driven in bounded chunk-checkpointed
  windows (`drive_v25_ext.sh`, one python segment at a time — the
  OOM-safe single-point profile; the sandbox reaps background processes,
  so long-lived supervisors are not viable). Each L=8 point costs ~17 h
  of compute driven through ~520 s windows; the queue is priority-ordered
  (d3@0.84 first) and append-safe.
- **Watch:** a 30-min cron drives up to two windows per firing, commits
  completed result rows, and stands down when `/home/z/.v25_ext_done`
  exists. Results land in `v25_n5_L8_rung_d3.json` /
  `v25_n5_L8_finegrid.json`.
- **v27 outlook:** integrate the L=8 d=3 rung (completing the d=3
  three-size ladder) and the fine grid (the locator refinement +
  latent-heat-adjacent plateau reading) as a new version pass.
