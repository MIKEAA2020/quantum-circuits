# changelog_v23.md — v23: the L=8 rung completion (2026-09-28T15:49:14Z)

v23 = v22 + the n=5 L=8 rung (the exponential-vs-power-law discriminator),
delivered by the background chain after the v22 commit.  All files are NEW;
v21/v22 are untouched.

## Manuscript (manuscript_revised_v23_rung.tex, built from v22 by patch_v23_rung.py)
- NEW rung paragraph before the Scope block (sec:n4n5): the mom0 triv.triv
  sector at n=5, L=8 — dimension K = 3865 (orbits of (S5 x S5) |x Z4 on
  (S5)^4), assembled as an exact dense block; gap12 = log(l1/l2) at the
  locator grid: $p=0.44$: 0.505, $p=0.46$: 0.481, $p=0.47$: 0.481, $p=0.48$: 0.492, $p=0.50$: 0.545; closing factor x1.68
  from L=6 to L=8 at the p=0.47 locator (against x2.12 from L=4 to L=6);
  L*gap12 = 3.85 vs the n=3 envelope 6.53 at L=8.
- Pre-table paragraph: the "honest caveat / natural next rung" sentence
  delivered (two sizes cannot separate exponential from power-law; the
  L=8 rung supplies the third size).
- Scope: "$L\le10$ at $n=4$ and $L\le8$ at $n=5$"; "now three-size".
- Discussion: the roadmap clause "with the L=8 rung ... in preparation" ->
  "computed by the symmetry-reduced block route (Sec. sec:n4n5)"; the
  q=n-Potts confirmation annotated "(three sizes at n=5)".
- Abstract: one clause appended (the L=8 rung extends the closing to three
  sizes).
- app:files: the rung result v22_n5_L8_rung.json noted as deposited.
- CONVENTION FIX relative to the never-executed RUNG branch of
  patch_v22_exactZ3.py: the closing factor is 0.806/gap12(L=8) (the
  tab:n5twosize convention: previous gap / new gap), not the inverse.

## Supplement (supplement_v6.tex, from v5)
- The block-route paragraph: the completed rung deposited
  (v22_n5_L8_rung.json) and hashed in certificate_sha256_v10.txt.
- The files-of-this-round sentence extended with the v10 ledger pointer.

## Companions
- mipt_numerical_report_v11.md = report v10 + Sec. 26 (the rung numbers).
- certificate_sha256_v10.txt (make_cert_v10.py): v23 files + the rung JSON
  + the ids/run logs + reps_nb4/counts_nb4.
- Results: results/v22-exactZ3-n5L8/v22_n5_L8_rung.json; logs:
  v22_n5_L8_block_ids.log, v22_n5_L8_block_run.log, chain.log (CHAIN_DONE).
