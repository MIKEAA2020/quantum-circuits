"""Seed-contract re-verification on the RECOVERED raw I3 dataset (fuller_workspace release).

Audit point R6/E9: trajectory k of data file (L, p) must regenerate bit-for-bit from
    run_sample(L, p, rec, SP4, seed0 + k)
with seed0 stored in the file (legacy MT19937 global stream, np.random.seed).
The deposited session verified 23 trajectories across 5 files (L = 16-512, including
the I3 == 0 file at L = 384, p = 0.18).  This script re-verifies on the recovered
data: one file per system size plus the saturated file, 4 k-values each.

New file (nothing overwritten).  Output: mipt_results/seed_recheck.json,
log: logs/mipt_seed_recheck.log.
"""
import numpy as np, glob, json, time
from mipt_clifford_sim import run_sample, SP4

CASES = [
    ("mipt_data/L16_p0.1600.npz",   [0, 1, 1999, 3999]),
    ("mipt_data/L24_p0.1550.npz",   [0, 1, 2000, 3999]),
    ("mipt_data/L32_p0.1500.npz",   [0, 1, 2000, 3999]),
    ("mipt_data/L48_p0.1650.npz",   [0, 1, 2000, 3999]),
    ("mipt_data/L64_p0.1700.npz",   [0, 1, 2000, 3999]),
    ("mipt_data/L96_p0.1500.npz",   [0, 1, 1499, 2999]),
    ("mipt_data/L128_p0.1600.npz",  [0, 1, 1499, 2999]),
    ("mipt_data/L192_p0.1450.npz",  [0, 1, 999, 1999]),
    ("mipt_data/L256_p0.1550.npz",  [0, 1, 999, 1999]),
    ("mipt_data/L384_p0.1800.npz",  [0, 1, 400, 799]),   # the I3 == 0 saturated file
    ("mipt_data/L512_p0.1600.npz",  [0, 1, 200, 399]),
]

t0 = time.time()
rows, n_ok, n_bad = [], 0, 0
for fn, ks in CASES:
    z = np.load(fn)
    L, p, seed0 = int(z["L"]), float(z["p"]), int(z["seed0"])
    rec, data = z["rec"], z["data"]
    N = data.shape[0]
    for k in ks:
        if k >= N:
            continue
        regen = run_sample(L, p, rec, SP4, seed0 + k)
        ok = bool(np.array_equal(regen, data[k].astype(np.int64).astype(float)) or
                  np.array_equal(regen.astype(data.dtype), data[k]))
        rows.append(dict(file=fn, L=L, p=p, k=k, seed=seed0 + k, bitexact=ok))
        n_ok += ok; n_bad += (not ok)
        print(f"{fn} k={k:5d} seed={seed0+k:12d}: {'BIT-EXACT' if ok else 'MISMATCH'}", flush=True)

out = dict(cases=len(rows), bitexact=n_ok, mismatches=n_bad, elapsed_s=time.time() - t0,
           contract="run_sample(L, p, rec, SP4, seed0 + k), legacy MT19937 (np.random.seed)", rows=rows)
json.dump(out, open("mipt_results/seed_recheck.json", "w"), indent=1)
print(f"\n{N and ''}{n_ok}/{len(rows)} trajectories regenerate bit-exactly ({time.time()-t0:.0f} s)")
print("verdict:", "SEED CONTRACT VERIFIED" if n_bad == 0 else "CONTRACT VIOLATED")
json.dump(out, open("mipt_results/seed_recheck.json", "w"), indent=1)
