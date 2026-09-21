# v19 — the n=5 two-size test (first-order confirmed), the n=4 L=10
# third crossing, the no-freezing theorem, and the replica interpolation
# identity

This round answers two standing questions with executed work:

## 1. The 3 GB / 2-core budget barrier (overcome, and diagnosed)

The v18 statement that the n=5 L=6 two-size test and the L≥10 dense
matrices "exceed the present computational budget" was an implementation
artifact:

* **Memory was never binding.**  Peak RSS of the n=5 L=6 iterative
  transfer: 942 MB against 2.3 GB available.
* **The 121 s/matvec was a numpy pathology**, not a flop limit: the ring
  contraction is only ~2·120⁵ = 5·10¹⁰ MACs, but the v1 implementation
  performs ~4 cache-hostile strided 110 MB transpose-copies per
  carry-chunk, and its final contraction hands BLAS a strided W-panel
  view that falls off the GEMM fast path (measured 1.6 GFLOPS on that
  stage vs 64 GFLOPS contiguous on this machine).
* **ring_gemm_v2.py** performs the identical contraction (validated to
  4·10⁻¹⁶ against the deposited kernel at n=2..4, nb=2..5) in
  **5.4 s (float64) / 2.9 s (float32) per M2** — an 11–21× speedup on
  the same two cores.
* The L=4 anchor: all 21 points reproduce the deposited v18 eigenvalues
  to 5.5·10⁻¹⁵ (f64) / 4.3·10⁻⁶ (f32); six f64 spot-checks confirm the
  L=6 f32 sweep to 5 decimals.
* The n=4 L=10 space (N = 24⁵ = 7,962,624; a dense matrix would need
  6.3·10¹³ entries ≈ 500 TB) runs at <1.8 GB peak RSS.  (A 1.5 GB
  tuple-set assertion inside the colour projector — not the physics —
  was the actual L=10 memory hazard; FastColourLite fixes it and is
  byte-identical on the validated sizes.)

## 2. The theorem-level items (the most feasible ones closed/reduced)

* **Theorem thm:nofreeze (freezing realization — closed for a defined
  class):** no finite-q freezing in any *allowable finite-reachable*
  monitored process — deterministic, i.i.d.-random, or reducible.  ψ
  exists a.s., is deterministic (Furstenberg–Kesten + the positivity
  identification), real-analytic in k (Le Page/Ruelle/Peres), hence τ
  analytic: an affine segment would force global affinity (identity
  theorem).  Reducible chains give corners, not affine branches.
  **Freezing requires an unbounded reachable set.**
* **Corollary cor:p1closure (quenched SCGF analyticity):** the fully
  monitored p=1 Haar-refreshed family — the v18 "analyticity remains
  conditional" case — is allowable (a.s. entrywise strictly positive
  tilted matrices), so its conditionality is removed unconditionally.
* **Proposition prop:replica-int (disorder-replica interchange —
  reduced):** the exact interpolation identity
  g(r) − r·E log X = ∫₀ʳ (r−s)Var_s(log X)ds; the monotone replica
  ladder; the quadratic m↓0 rate; the m→∞ overshoot to the extremal
  value (the naive replica limit is *not* an interchange); the
  T→∞ interchange reduced to the measurable self-averaging criterion.
* **Born-average hardness** remains open — genuinely the least feasible
  (needs average-case complexity machinery that does not currently
  exist for this object).
* **Numerical verification: 8/8 PASS** (no_freeze_theory_v1.py),
  including the interpolation identity to 6·10⁻⁷ relative on 6000
  exactly-enumerated p=1 Haar record partition functions.

## The n=5 two-size verdict (the headline)

At the coexistence locator p≈0.47: gap12 closes 1.711 → 0.806 (×2.12)
from L=4 to L=6, against ×1.94 (n=4) and ×1.81 (n=3, continuous
baseline) at matched sizes — the closing factor is monotone across
replica number; L·gap12 falls below the continuous envelope (n=3
saturates at its energy-operator amplitude); the plateau narrows by the
full size ratio (fixed ξ); X-slope ratio 2.18 vs the continuous 1.69;
locator stable at 0.47–0.48.  **The q=n-Potts first-order prediction is
confirmed at the two-size level** (caveat: two sizes, weak-first-order
crossover regime, L=8 the next rung).

## Files

* `manuscript_revised_v19_twosize-nofreeze.tex/.pdf` (35 pp) — new
  Sec. sec:nofreeze (Theorem + Corollary + Proposition + verification),
  the two-size results + Table tab:n5twosize, the updated open problems,
  abstract, and the L=10 additions; built by `patch_v19_twosize.py`
  (asserted anchors) from v18; compiled with tectonic.
* `mipt_numerical_report_v8.md` — Secs. 14 (budget + two-size), 14a
  (L=10), 15 (theorem verification).
* `changelog_v19.md`, `certificate_sha256_v6.txt`.
* scripts: `ring_gemm_v1/v2.py`, `ring_nb_v1/v2/v3.py`,
  `budget_bench_v1.py`, `n5_L6_scan_v2.py`, `n4_L10_scan_v2.py`,
  `n5_analyze_L6_v2.py`, `n4_analyze_L10_v2.py`,
  `no_freeze_theory_v1.py`.
* results: `n5_L6_{validate_f64,validate_f32,scan_v2,f64spot_v2}.json`,
  `n4_L10_{scan_v2,f64spot_v2}.json`, the analysis logs.
