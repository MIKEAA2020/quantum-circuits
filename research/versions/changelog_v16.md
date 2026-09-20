# Changelog — Section R (v16, recovered-data version)

## Section R — v16 (the original workspace recovered; every caveat resolved)

- **The fuller_workspace release contains the complete original workspace**
  (`workspace-phys2.zip`, 116 411 529 bytes, SHA-256 verified against the
  GitHub release digest): the raw I3 dataset (192 files, 475 600
  trajectories, L = 16–512), the purification dataset (270 files, 135 000
  trajectories), the original v13 manuscript (1218 lines) with all versions
  v5–v13, every script, result JSON and log. The v14/v15 reconstruction's
  operating assumption "the deposited workspace is lost / raw I3 data not
  recoverable" is therefore void.
- **Item 13 completed — the exact computation at which the deposited session
  stopped.** Three latent defects in the deposited transform script were
  located and fixed in a new version (`mipt_v14_transform_v2.py`; v1 kept):
  a stale final token-count assertion, an invalid `binds_old_1e-6`
  identifier, and a `rec`-rebinding crash in the floor-audit loop. The
  corrected transform generates the released `mipt_fss2_floorN.py` (1/N
  standard-error floors; the Nelder–Mead `xatol` intentionally untouched)
  and `mipt_final2_rerun.py`.
- **The 1/N-floor re-run on the recovered raw data proves the no-op
  bit-for-bit**: max |Δp_c| = 0, max |Δν| = 0, max |Δχ²| = 0 over all 24
  windowed collapses; the floor audit explains it (smallest in-window s.e.
  3.35e-3 bits vs the 1/N floor 2.5–5e-4; no window contains a floored
  point). The regenerated figure reproduces the deposited one.
- **Seed contract re-verified**: 44/44 test trajectories regenerate
  bit-exactly from `seed0 + k` (legacy MT19937), including the I3 ≡ 0
  saturated file at L = 384, p = 0.18.
- **Purification locator re-run**: zero differences against the deposited
  summary, bootstrap values included (τ=1, L≥64: 0.16011(9), 1.2499(14)).
- **Manuscript v16** (`versions/manuscript_revised_v16_recovered.tex/.pdf`,
  30 pp): the ORIGINAL deposited v13 with the full audit-3 v14 plan (E1–E9,
  N3, D6, N2; 21 asserted-anchor edits via `versions/patch_v16_recovered.py`),
  the v15 spinor factorisation inside the proof of the closed-form-spectrum
  Proposition, the authorised re-centring p_c = 0.1595(10) → 0.1597(8), and
  the recovery-verification sentences. v13, v14 and v15 kept unmodified.
- **Report v5** (`versions/mipt_numerical_report_v5.md`): Secs. 8–8.6
  document the recovery, the item-13 completion, the re-verifications and
  the file lists.
- **No numerical result of the manuscript changes**: p_c = 0.1597(8),
  ν = 1.24(7), α = 1.55(7), the purification locator, the exact annealed
  line, the benchmark, and the enclosures are as in v14/v15; v16 upgrades
  their provenance from "quoted from the deposit" to "recomputed from the
  recovered raw dataset".
- **Ledger v3** (`logs/certificate_sha256_v3.txt`): all v1/v2 entries plus
  the v16 artifacts; v1 and v2 kept.
