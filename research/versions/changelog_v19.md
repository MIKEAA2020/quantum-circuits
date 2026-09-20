# Changelog v19 — the n=5 two-size test (first-order confirmed), the
# n=4 L=10 third crossing, the no-freezing theorem, and the replica
# interpolation identity

From v18.  All files NEW (never-overwrite honored).

## S.1 What changed

1. **Sec. sec:nofreeze (new)** — Theorem thm:nofreeze: no finite-q
   freezing in any *allowable finite-reachable* monitored process —
   deterministic, i.i.d.-random, or reducible.  Assembly: (i)
   Furstenberg–Kesten + the positivity identification (matrix element =
   norm exponent via Hilbert-metric cone contraction); (ii) Le
   Page/Ruelle/Peres real-analyticity of the top Lyapunov exponent in k;
   (iii) the identity-theorem corollary: an analytic ψ affine on an
   interval is affine everywhere, contradicting strict convexity at 0 —
   so τ has no affine segment on ANY interval; reducible chains give
   ψ = max γ_i with corners (τ′ jumps) but still no affine branch.
   Freezing requires an unbounded reachable set (the REM sequence).
   Corollary cor:p1closure: the p=1 Haar-refreshed family (a.s.
   entrywise strictly positive tilted matrices = allowable) has its
   v18-flagged analyticity conditionality removed unconditionally.
2. **Proposition prop:replica-int (new)** — the exact replica
   interpolation identity g(r) − r·E log X = ∫₀ʳ (r−s)Var_s(log X)ds,
   Lyapunov monotonicity of the replica free energies, the quadratic
   small-m rate, the replica-derivative identity, and the two one-sided
   limits (m↓0 recovers the quenched value; m→∞ overshoots to the
   extremal value — the naive replica limit is not an interchange).
   The disorder-replica interchange question is thereby reduced to the
   tilted-variance profile (the measurable self-averaging criterion).
3. **Sec. sec:n4n5 (extended)** — the decisive n=5 two-size test,
   previously "beyond the computational budget", executed and POSITIVE
   (Table tab:n5twosize): gap12 at the coexistence locator closes
   1.711 → 0.806 (×2.12) from L=4 to L=6, against ×1.94 at n=4 and
   ×1.81 at n=3 (continuous baseline) at matched sizes and locators —
   the closing factor is MONOTONE across replica number; the scaled gap
   L·gap12 falls below the continuous envelope (n=3 saturates at its
   energy-operator amplitude 8.59→7.11→6.53→6.21; n=5 drops
   6.85→4.85); the coexistence plateau narrows by the full size ratio
   (fixed ξ); X-curves cross at p≃0.449 with slope ratio 2.18 vs the
   n=3 continuous 1.69; the locator is stable → p_c^{(5)} ≈ 0.47–0.48.
   The first-order claim is upgraded from "prediction supported by" to
   "measured finite-size trend confirming" (with the two-sizes caveat).
4. **n=4 L=10 third crossing (in sec:n4n5)** — the N = 24⁵ = 7,962,624
   bond-label space (a dense matrix would need 6.3·10¹³ entries ≈ 500
   TB) computed by the iterative ring route at <1.8 GB peak RSS.
   [NUMBERS IN THE REPORT §14a AND THE L=10 TABLE COLUMN.]
5. **The budget-barrier diagnosis (report §14)** — the v18 "exceeds the
   3 GB / 2-core budget" was an implementation artifact: peak RSS 942 MB
   (memory never binding); the 121 s/matvec came from cache-hostile
   strided 110 MB transpose-copies and a strided-W BLAS slow path
   (measured 1.6 GFLOPS vs 64 GFLOPS contiguous).  ring_gemm_v2.py (the
   identical contraction, validated to 4·10⁻¹⁶) runs 5.4 s (f64) / 2.9 s
   (f32) per M2 — an 11–21× speedup on the same two cores.  The L=4
   anchor: all 21 points reproduce the deposited v18 values to
   5.5·10⁻¹⁵ (f64) / 4.3·10⁻⁶ (f32); six f64 spot-checks confirm the
   L=6 f32 sweep to 5 decimals.
6. **Open problems (rewritten)** — the freezing question localized to
   local ensembles with unbounded reachable sets; the disorder-replica
   interchange reduced to the self-averaging criterion with the
   m→∞ direction closed negatively; the n≥3 targets updated (the
   two-size confirmation delivered; the n=5 L=8 rung and the
   growth-rate regularity remain).

## S.2 New and changed files (all new)

* scripts (research/scripts/v19-n5L6-nofreeze/): ring_gemm_v1.py,
  ring_gemm_v2.py (the production kernel), ring_nb_v1/v2/v3.py (the
  numba route, validated, kept for the record), budget_bench_v1.py
  (the budget diagnosis), n5_L6_scan_v2.py (the L=6 two-size sweep:
  validate/scan/f64spot; includes FastColourLite for N > 2·10⁶),
  n4_L10_scan_v2.py (the L=10 third crossing), n5_analyze_L6_v2.py
  (the two-size battery), no_freeze_theory_v1.py (8/8 PASS).
* results (research/results/v19-n5L6-nofreeze/): n5_L6_validate_f64.json,
  n5_L6_validate_f32.json, n5_L6_scan_v2.json (+ _v0.npz),
  n5_L6_f64spot_v2.json, n4_L10_scan_v2.json (+ _v0.npz),
  n4_L10_f64spot_v2.json, no_freeze_theory_v1.log.
* versions (research/versions/): manuscript_revised_v19_twosize-
  nofreeze.tex/.pdf (35 pp), v19_staged_nofreeze.tex (the staged
  theorem text), patch_v19_twosize.py, mipt_numerical_report_v8.md
  (Secs. 14, 14a, 15), changelog_v19.md (this file),
  certificate_sha256_v6.txt, README_v19_twosize-nofreeze.md.
* logs (research/logs/v19-n5L6-nofreeze/): budget_bench_v1.log,
  n5_L6_validate_v2.log, n5_L6_scan_v2.log, n5_L6_f64spot_v2.log,
  n5_analyze_L6_v2.log, n4_L10_scan_v2.log, no_freeze_theory_v1.log.

## S.3 Validation chain

1. ring_gemm_v2 == n45_annealed_lib_v1.ring_M2 to 4·10⁻¹⁶ at n=2
   (nb=2), n=3 (nb=3,4,5), n=4 (nb=4); the numba route to 1.4·10⁻¹⁵.
2. [C, P_colour] = 0 verified numerically (1.1·10⁻¹⁴) — the
   colour-restricted Arnoldi semantics are the v1 semantics.
3. L=4 anchor (21 points): λ₁, λ₂, λ_σ vs the deposited v18 scan —
   5.5·10⁻¹⁵ (f64), 4.3·10⁻⁶ (f32).
4. L=8 anchor for the n=4 machinery: 1.8·10⁻¹⁴ at p = 0.34, 0.40, 0.44.
5. f64 spot-checks: 6/6 decisive L=6 points confirm the f32 sweep
   (gap12 identical to 5 decimals).
6. FastColourLite == FastColour byte-identical (rel err 0.0) on both
   tested blocks at n=4 nb=4; bijection subsample-checked at N > 2·10⁶.
7. no_freeze_theory_v1.py: A1–A5, B1–B3 all PASS (the interpolation
   identity to 6·10⁻⁷ relative on 6000 exactly-enumerated p=1 Haar
   record partition functions).
