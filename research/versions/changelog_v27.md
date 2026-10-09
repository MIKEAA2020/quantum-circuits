# Changelog — v27 (extension-integration pass)

Date: 2026-10-09 (build 2026-10-09 11:24 UTC). Script:
`research/scripts/v22-exactZ3-n5L8/patch_v27_extL8.py`.
Sources preserved unmodified: `manuscript_revised_v26.tex`,
`supplement_v8.tex` (and all earlier versions). New files:
`manuscript_revised_v27.tex/.pdf`, `supplement_v9.tex/.pdf`, this changelog,
`README_v27.md`, `certificate_sha256_v14.txt`.

Provenance note: the extension campaign whose results this pass integrates
was declared complete on 2026-10-09 (all queue points computed, merged, and
verified 0/0 with origin; see the v25-ext-watch worklog entries). This is
the manuscript-integration pass that the v26 README's outlook section
anticipated.

## 1. What was integrated

The two completed extension deposits:

- **The d=3 L=8 rung** (`v25_n5_L8_rung_d3.json`): p=0.82/0.84/0.86 →
  gap12 = 0.948/0.453/0.519, interior minimum 0.45316 at p=0.84 — the
  d=3 three-size ladder is complete (1.482 → 0.621 → 0.453 at its locators).
- **The finer d=2 locator grid at L=8** (`v25_n5_L8_finegrid.json`):
  p=0.455/0.465/0.475/0.485 → gap12 = 0.484/0.480/0.485/0.501, minimum
  0.47965 at p=0.465 (against 0.481 at both p=0.46 and 0.47 on the rung
  grid).

## 2. Main-text changes (Sec. II.G and front/back matter)

- **Table `tab:n5twosize`**: the n=5 L=8 cell 0.481 → 0.480 (the
  fine-grid minimum), with caption provenance added; the scaled-gap row
  8·gap12: 3.85 → 3.84.
- **Table `tab:closingrates`**: σ_eff(6→8) n=5: 0.258 → 0.259;
  α_eff(6→8) n=5: 1.794 → 1.802 — same table-value convention as the
  deposited `v25_sigma_extract.py` (rates derived from the quoted cells),
  re-derived and asserted inside the patch script.
- **The L=8 rung paragraph**: the rung grid values are followed by the
  finer locator grid; the closing factor ×1.68 is re-anchored at the
  refined p=0.465 locator; a new block presents the d=3 ladder (level
  ordering below d=2 at every size, 8·gap12 = 3.62 vs 3.84, interval
  closings ×2.39 then ×1.37) with the crossover-region caveat.
- **Locator sentence**: 0.48/0.47 at L=4/6 → 0.48/0.47/0.465 at
  L=4/6/8 (the last on the finer grid).
- **Scope note**: the d=3 local-dimension extension through L=8 is
  recorded.
- **Abstract**: one clause appended ("...and at local dimension d=3 the
  same three-size test keeps the gap level below the d=2 values at every
  size").
- **Conclusion**: last-digit 3.85 → 3.84; the extensions paragraph
  restated from promissory ("follow the same ... protocol") to deposited
  (fine-grid locator, d=3 ladder, level-ordering reading, crossover-region
  deceleration at both dimensions); latent-heat extraction remains the one
  open extension.

Physics reading (honest, directional): the d=3 gap LEVEL sits below the
d=2 value at every size and 8·gap12 = 3.62 below the d=2 value 3.84 and
the continuous envelope 6.53 — the level ordering carries the first-order
direction with local dimension. The interval closing factors at d=3 read
×2.39 then ×1.37 (against ×2.12, ×1.68 at d=2): the rates decelerate at
both dimensions, the crossover-region behaviour the main text already
records for d=2. The former two-size phrase "the first-order direction
strengthens with local dimension" is retired in favour of this level/
rate split.

## 3. Supplement changes (v8 → v9, Sec. S7)

- **The local-dimension extension paragraph**: the promissory closing
  sentence ("The L=8 rung at d=3 and a finer d=2 locator grid follow the
  same ... protocol as the deposited rung") is replaced by the completed
  deposits — both JSONs named and hashed in
  `certificate_sha256_v14.txt`, the bounded-window restart-safe execution
  note, the fine-grid readings and the resulting last-digit cell moves,
  and the d=3 three-size ladder with its dual rate readings
  (σ_eff = 0.435 → 0.158; α_eff = 2.145 → 1.096).
- **The reproduction chain**: `v25_n5_L8_ext_v1.py` appended (validates
  the d=3 route, scans the locators, computes the extension points; JSON
  and log locations noted).
- **Formal-prose fix**: the reproduction block's "The files of this round
  are hashed in certificate_sha256_v8.txt (round files)" — compute-round
  language — reworded to "The files of this computational suite are
  hashed in certificate_sha256_v8.txt".

## 4. Conventions and verification

- All rates/closings re-derived inside `patch_v27_extL8.py` from the
  quoted table values with assertions (same convention as
  `v25_sigma_extract.py`); the level ordering gap(d=3) < gap(d=2) at
  every size is asserted.
- The residual-token report (visible lines only) reports **zero**
  forbidden tokens — including the retired "strengthens with local
  dimension" phrasing and compute-infrastructure vocabulary — and zero
  remaining "now" occurrences in both outputs.
- Structural assertions: 9 sections, both table labels unique, all
  edit anchors matched exactly once.
- PDFs built with tectonic (revtex4-2): 585.70 KiB (manuscript, 39 pp
  class) and 216.38 KiB (supplement).
