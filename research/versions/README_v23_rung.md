# README_v23_rung.md — v23: the n=5 L=8 rung completion (2026-09-28T15:49:14Z)

**What landed.** The background chain (`run_chain.sh`) completed the
symmetry-reduced block computation at n=5, L=8 — the
exponential-vs-power-law discriminator of the two-size first-order test.
K = 3865 orbits; gap12 at the grid: $p=0.44$: 0.505, $p=0.46$: 0.481, $p=0.47$: 0.481, $p=0.48$: 0.492, $p=0.50$: 0.545; p=0.47 locator: closing
factor x1.68 from L=6 to L=8, L*gap12 = 3.85 (n=3 envelope 6.53).

**Files (all new; v21/v22 untouched).**
- `versions/manuscript_revised_v23_rung.tex/.pdf` — the rung paragraph +
  Scope/Discussion/abstract/app:files alignment (patch_v23_rung.py, all
  anchors asserted against the committed v22).
- `versions/supplement_v6.tex/.pdf` — the rung-deposit note + ledger
  pointer.
- `versions/mipt_numerical_report_v11.md` — report v10 + Sec. 26.
- `versions/changelog_v23.md`, this file.
- `versions/certificate_sha256_v10.txt` — ledger v10 (make_cert_v10.py).
- `results/v22-exactZ3-n5L8/v22_n5_L8_rung.json` — the rung rows
  (p, L, n, K, triv6, lam1, lam2, gap12, growth, secs).
- `results/v22-exactZ3-n5L8/tmp_n5L8block/reps_nb4.npy`,
  `counts_nb4.npy` — the orbit table (the 830 MB canonical-id array is
  NOT deposited: GitHub's 100 MB limit; regenerate with
  `python3 v22_n5_L8_block_v1.py ids`).
- `logs/v22-exactZ3-n5L8/v22_n5_L8_block_ids.log`,
  `v22_n5_L8_block_run.log`, `chain.log` (CHAIN_DONE).

**Reproduce.**
```
cd research/scripts/v22-exactZ3-n5L8
python3 v22_n5_L8_block_v1.py validate   # nb=2 vs deposited, nb=3 vs Arnoldi
python3 v22_n5_L8_block_v1.py ids        # ~830 MB canonical-id array
python3 v22_n5_L8_block_v1.py run --pgrid 0.44,0.46,0.47,0.48,0.50
python3 patch_v23_rung.py                # rebuild the v23 files
```

**Closing-factor convention.** tab:n5twosize: factor = previous gap / new
gap (2.12 = 1.711/0.806, L=4 -> L=6); hence L=6 -> L=8 is
0.806/gap12(L=8, p=0.47).  (The dormant RUNG branch of
patch_v22_exactZ3.py had the ratio inverted; v23 uses the table's
convention.)
