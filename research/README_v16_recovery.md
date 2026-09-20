# research/ — the v16 recovered-data round

This file documents the v16 round; `README.md` (v1, unmodified) documents
the v14/v15 reconstruction rounds.

## What changed

The **fuller_workspace release**
(`https://github.com/MIKEAA2020/quantum-circuits/releases/tag/fuller_workspace`,
`workspace-phys2.zip`, 116 411 529 bytes, SHA-256
`15ec3a0e76b2e39fb9d152b7925db062189b7eccca0231b6f0892fdd310948d9`)
contains the **complete original working workspace** — the raw I3 dataset
(192 files, 475 600 trajectories, L = 16–512), the purification dataset
(270 files, 135 000 trajectories), the original v13 manuscript, all versions
v5–v13, every script, result and log. The v14/v15 reconstruction's premise
"the deposited workspace is lost / raw I3 data not recoverable" is void.

## What was done (all new files; nothing overwritten)

| item | status |
|---|---|
| Item 13 — the $1/N$-floor re-run (the exact point the deposited session died) | **completed**: three latent defects in the deposited transform fixed in `scripts/v16-recovery/mipt_v14_transform_v2.py`; the released pipeline re-run on the raw data gives max \|Δp_c\| = max \|Δν\| = max \|Δχ²\| = **0** over all 24 windows; the floor audit *explains* the no-op (smallest in-window s.e. 3.35e-3 vs the 1/N floor 2.5–5e-4; 0/24 windows bind) |
| Seed contract (R6/E9) | re-verified: **44/44** trajectories regenerate bit-exactly from `seed0 + k`, including the I3 ≡ 0 file (L=384, p=0.18) |
| Purification locator (N2) | re-run on the recovered 270-file dataset: **zero differences** vs the deposit, bootstraps included |
| Manuscript | **`versions/manuscript_revised_v16_recovered.tex/.pdf`** (30 pp): the ORIGINAL deposited v13 + the full audit-3 v14 plan (E1–E9, N3, D6, N2; 21 asserted-anchor edits, `versions/patch_v16_recovered.py`) + the v15 spinor factorisation in the Proposition proof + the authorised re-centring p_c = 0.1595(10) → 0.1597(8) + recovery-verification sentences |
| Report / changelog / ledger | `versions/mipt_numerical_report_v5.md`, `versions/changelog_v16.md` (§R), `logs/certificate_sha256_v3.txt` |

## Reproduce (against the extracted fuller_workspace)

```bash
python3 mipt_v14_transform_v2.py        # generates mipt_fss2_floorN.py + mipt_final2_rerun.py
python3 mipt_final2_rerun.py            # ~5 min: the no-op proof + Secs. 8-9
python3 mipt_seed_recheck.py            # seconds: 44/44 bit-exact
python3 mipt_purif_analysis_rerun.py 100  # seconds: zero differences
cd versions && tectonic manuscript_revised_v16_recovered.tex
```

Versioning policy: unchanged — revisions are always new version files
(v13 → v14 → v15 → v16; report v2 → v3 → v4 → v5); nothing is overwritten.
