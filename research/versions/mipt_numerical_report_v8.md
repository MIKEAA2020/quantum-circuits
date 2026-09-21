# Numerical report v8 — the n=5 two-size test (first-order confirmed),
# the n=4 L=10 third crossing, and the no-freezing theorem verification
(v19; continues report v7 Secs. 12/12a/13.  All eigenvalues exact unless
stated; the n=5 L=6 sweep is float32 with float64 spot-checks as stated.)

## 14. The n=5 two-size test: the budget barrier overcome, the
## first-order confirmation

**The budget diagnosis (measured, not asserted).**  The v18 statement
"exceeds the present computational budget" was an implementation
artifact, not a resource limit:

* Peak RSS of the n=5, L=6 iterative transfer: **942 MB** against
  2.3 GB available — memory was never binding.
* The v1 numpy ring_M2 cost 60 s per M2 at nb=3 (121 s per C = M1M2).
  Profiling: the contraction itself is only ~2·120⁵ = 5·10¹⁰ MACs, but
  v1 performs ~4 cache-hostile strided 110 MB transpose-copies per
  carry-chunk, and its final contraction feeds BLAS a strided W-panel
  view that knocks numpy off the GEMM fast path (measured 1.6 GFLOPS on
  that stage vs 64 GFLOPS contiguous).

**ring_gemm_v2.py (the production kernel).**  Same mathematical
operation as n45_annealed_lib_v1.ring_M2, restructured: the lift
broadcasts directly into the step-1 layout (no copy at nb=3); each step
GEMM batches over (b, π_{k+1}) leading axes so its output is consumed
by the next stage without relayout; the final contraction uses
explicitly contiguous W-panels.  Validated to **4·10⁻¹⁶** against the
numpy reference at n=2 (nb=2), n=3 (nb=3,4,5 — multi-step chains), n=4
(nb=4); one numba route (ring_nb_v3.py, also validated to 1.4·10⁻¹⁵)
is kept for the record.  Speed at n=5 nb=3: **5.4 s (f64) / 2.9 s
(f32) per M2** — an 11–21× speedup on the same 2 cores.

**The L=4 anchor (n5_L6_scan_v2.py validate).**  The full 21-point
L=4 grid re-solved with this machinery: λ₁, λ₂ (triv.triv k=3) and λ_σ
(std.std k=1) reproduce the deposited v18 scan values with max relative
deviation **5.5·10⁻¹⁵ (f64)** and **4.3·10⁻⁶ (f32)** — the float32
systematic error is thereby calibrated empirically at the 10⁻⁶ level,
negligible for every diagnostic below.

**The L=6 production sweep.**  21 points p = 0.32..0.52 (the L=4 grid),
colour-restricted Arnoldi (triv.triv k=3, std.std k=1), warm starts,
checkpointed; 4–13 min per point; float64 spot-checks at
p = 0.32, 0.44, 0.46, 0.48, 0.50, 0.52 confirm every f32 value to 5+
significant figures (gap12 identical to 5 decimals at all six).

**Results (n5_analyze_L6_v2.py).**

| diagnostic | L=4 | L=6 | reading |
|---|---|---|---|
| gap12 at coexistence (p≈0.47) | 1.711 | 0.806 | closes ×2.12 |
| gap12 minimum locator | 0.48 | 0.47 | stable → p_c^{(5)}≈0.47–0.48 |
| gap12·L at p=0.47 | 6.85 | 4.85 | falls below the continuous envelope |
| plateau width (+1% band) | 0.060 | 0.040 | narrows by 4/6 = fixed ξ |
| X_L = L log(λ₁/λ_σ) crossing | — | X₄=X₆ at p=0.449 | FSS locator |
| max \|dX/dp\| | 8.95 | 19.49 | ratio 2.18 |

The cross-replica comparison at matched sizes and locators
(the decisive table):

| | n=3 (p=0.30, continuous) | n=4 (p=0.38, marginal) | n=5 (p=0.47) |
|---|---|---|---|
| gap12(L=4) | 2.147 | 1.919 | 1.711 |
| gap12(L=6) | 1.185 | 0.990 | 0.806 |
| **closing factor** | **1.81** | **1.94** | **2.12** |
| 4·gap12 → 6·gap12 | 8.59→7.11 | 7.67→5.94 | 6.85→4.85 |

plus the n=3 saturation chain 8.59→7.11→6.53→6.21 (L=4,6,8,10; the
energy-operator amplitude 2πx_ε of a continuous transition) against
n=5's drop below that envelope; the n=3 \|dX/dp\| baseline
7.49→12.68→19.18→26.52 (ratio 1.69 ≈ (6/4)^1.15, continuous scaling)
against n=5's 2.18; and the plateau narrowing 0.67 = 4/6 (fixed ξ)
against the ≈1.1 a continuous 1/ν=1.15 scaling gives.

**Verdict.**  Every measured quantity moves in the first-order
direction, and the closing factor is monotone across replica number
(1.81 → 1.94 → 2.12).  The v18 single-size prediction is thereby
**confirmed at the two-size level**, with the honest caveats: two
sizes cannot yet separate an exponential from a power-law closing; the
q=5 Potts transition is weakly first order (finite ξ), so L=4,6 are
crossover-dominated; L=8 (120⁴ = 2.1·10⁸ labels, ~40 s per f32
transfer application with the present kernel, ~15–25 h for the sweep)
is the natural next rung.

## 14a. The n=4 L=10 third crossing

L=10 → nb=5, N = 24⁵ = 7,962,624 bond labels; a dense transfer matrix
would need N² = 6.3·10¹³ entries (~500 TB) — the "dense matrices"
barrier — while the iterative ring route runs at <1.8 GB peak RSS.
Machinery identical to Sec. 14 (L=8 anchor: λ₁ and λ_σ reproduce the
deposited v18 L=8 scan to 1.8·10⁻¹⁴ at p = 0.34, 0.40, 0.44).  A
genuine memory hazard was found and fixed en route: the colour
projector's bijection assertion materialises an ~1.5 GB tuple-set at
this N — FastColourLite (chunked construction, subsampled bijection
check, byte-identical output on the validated sizes: rel err 0.0 on
both tested blocks) removes it; the 8M-element warm-start vectors are
checkpointed to a compact side .npz (the first JSON attempt produced a
431 MB row).

**Results (n4_analyze_L10_v2.py; 11 points, p = 0.32..0.42, f32).**

| | (4,6) | (6,8) | (8,10) |
|---|---|---|---|
| X-crossing p* | 0.35820 | 0.37899 | **0.3823** |

The crossing drift COLLAPSES: successive drifts 0.0208 → 0.0033 (ratio
0.158, far below the 0.68 a 1/ν = 1.28 power-law drift would give) —
the crossing sequence has essentially converged, and the annealed
four-replica point revises from the v18 extrapolation 0.40(2) to
**p_c^{(4)} ≈ 0.383** (the lower edge of the v18 bracket; the
marginal-q=4 logarithmic corrections presumably explain the
faster-than-power-law convergence).  The replica trend survives and
tightens: 0.233810 < 0.305(3) < 0.383 < 0.47–0.48 away from the
quenched 0.1597(8).  The L=10 curve steepens further
(max|dX₁₀/dp| = 30.6 at the grid edge vs 25.8 for X₈), and the
colour-trivial gap12 at p = 0.38 continues the continuous/marginal
trend (L·gap12: 7.67 → 5.94 → 5.75 → 4.66 at L = 4, 6, 8, 10) —
consistent with v18's continuous assignment at n = 4.

## 15. The no-freezing theorem and the replica interpolation identity
## (numerical verification; no_freeze_theory_v1.py, 8/8 PASS)

**Theorem thm:nofreeze (manuscript v19).**  No finite-q freezing in any
allowable finite-reachable monitored process — deterministic,
i.i.d.-random, or reducible:  ψ exists a.s., is deterministic and equals
the top Lyapunov exponent (Furstenberg–Kesten + the positivity
identification); k ↦ γ(k) is real-analytic on ℝ (Le Page 1974 / Ruelle
1979 / Peres 1992); hence τ = −γ(1−q) is analytic — an affine segment
on an interval would force global affinity (identity theorem),
contradicting strict convexity at 0.  Reducible chains give ψ = max γ_i
with corners (τ′ jumps — a quenched dynamical phase transition) but
still no affine branch.  Freezing requires an unbounded reachable set
(the REM sequence of thm:rem).  **Corollary cor:p1closure:** the p=1
Haar-refreshed family (a.s. entrywise strictly positive tilted
matrices = allowable) has its analyticity closed unconditionally —
removing the v18 "remains conditional" flag.

**Proposition prop:replica-int (manuscript v19).**  For X > 0:
g(r) − r·E log X = ∫₀ʳ (r−s)·Var_s(log X) ds EXACTLY; r ↦ g(r)/r
nondecreasing with limits E log X (r↓0, quadratically) and
log ess-sup X (r→∞); ∂_r E X^r|₀ = E log X.  Applied to X = Z_{q,ω}(T):
the annealed replica free energies form a monotone ladder squeezed
between the quenched value and the extremal value; the m→∞ replica
limit OVERSHOOTS (not an interchange); the T→∞ interchange reduces to
the tilted-variance profile — the measurable self-averaging criterion
sup_T Var(T⁻¹ log Z_T) < ∞.

**Verification (all checks pass):**
* A1 deterministic positive tilted chain: ψ = log ρ(M(k)) smooth,
  strictly convex, τ with no affine segment.
* A2 i.i.d. allowable random chains (CRN, 240 draws, T=192, correct
  power-iteration Lyapunov estimator): no affine segment (longest run
  of |τ″| below 5% of median: a single grid point).
* A3 reducible two-block chain: corner with slope jump 0.57, both
  branches curved (vs the REM's exact 0).
* A4 REM benchmark: closed form φ(s) = a+s²/2 (s ≤ s_c), s·s_c
  (s ≥ s_c): junction continuous, φ′ continuous at s_c = √(2 log 2),
  |φ″| above s_c ≤ 9·10⁻¹⁶ vs 10⁻⁴ below — the terminal affine branch,
  the exact freezing signature, side by side with A1–A3.
* A5 p=1 Haar-refreshed family (L=4, 12 sweeps, 400 exact
  enumerations): ψ smooth, strictly convex over k ∈ [−2.5, 2.5]
  (Corollary cor:p1closure empirically).
* B1 synthetic exact: the interpolation identity to 4·10⁻⁸ relative
  (quadrature-limited).
* B2 Lyapunov monotonicity exact on a 400-point m-grid; f(m→0⁺)
  matches E log X + m·Var/2 to 4·10⁻⁵; f(m→∞) matches
  log ess-sup + (log p_max)/m (the finite-m correction) to <10⁻³.
* B3 **the real object**: 6000 exactly-enumerated p=1 Haar record
  partition functions Z (L=4, 6 sweeps, k=0.5): E log Z = 13.256,
  Var log Z = 0.037 — the identity holds to 6·10⁻⁷ relative at m=1,2;
  the quadratic small-m rate (f_m − E log Z)/(m·Var/2) measures
  0.994–0.998 at m = 0.125, 0.25, 0.5; the replica derivative matches
  to 1.2%; the f₈ = 13.390 < log max Z = 13.869 extremal overshoot is
  exhibited; monotonicity exact.
