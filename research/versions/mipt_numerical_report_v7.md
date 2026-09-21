# Numerical report v7 — n=4 with full S₄ colour resolution, the n=5
# first-order diagnostics, and the Haar SMC record-multifractality run
(v18; continues report v6 Secs. 11/11a.  All eigenvalues exact unless
stated; SMC estimates carry the stated statistical errors.)

## 12. The annealed four-replica point (n=4, d=2) with full S₄ colour
## resolution at L=4,6,8

**Machinery (new, validated).**  General-n library
(n45_annealed_lib_v1.py): central (isotypic) idempotents of S_n from the
hardcoded character tables (n=2..5) give the 25 (λ,μ) blocks of the global
S₄×S₄ replica symmetry, applied in O(N·n!²) BLAS through the (key, member)
bijections of the free left/right regular orbits (left key σ₁⁻¹σ_k, right
key σ_kσ₁⁻¹; free orbits of size n!); the ring transfer M1M2 is applied as
a boundary-carry contraction with a π₀ block loop (validated exact against
the deposited dense bond_ops to 2·10⁻¹⁶ at n=2,3, nb=2..4); all leading
eigenvalues live at ring momentum k=0 (imposed by axis-permutation shift
averaging; mom content 1.00 at every record); the spectrum is extracted by
Arnoldi ('LR') with colour classification of eigenvectors (the deposited
block-12 pattern generalized), plus colour-restricted projected solves for
λ_ε (the 2nd trivial eigenvalue sits below the 9+4+9+1-fold spin multiplets
in the plain top-k list).

**Validation chain (n45_annealed_validate_v1.py, ALL OK).**  V1 n=2 vs the
Kaufman closed form at L=8: 3·10⁻¹⁵.  V2 n=3 vs the deposited
n3_annealed_scan_dense at L=6 (p=0.25, 0.30): λ₁, λ_σ, λ_ε to 10⁻¹⁵
(blocks std.std ✓).  V3 n=4 vs dense at L=4: value-set 3.6·10⁻¹⁵ (λ₁
identical to 8 digits; ARPACK undercounts only the multiplicities of the
9-fold std.std multiplet — the values match).  V4/V5 the 25 S₄ projectors
sum to the identity and are idempotent to 2.5·10⁻¹⁶.  V6 at p=1 the
rank-one eigenvalue equals [d²Γ(d²)Γ(n+1)/Γ(d²+n)]^{2nb} EXACTLY for
n=2,3,4,5 (per-bond values 0.4, 0.2, 8/70, 1/14) — the n=5 entry checks the
pseudo-inverse Weingarten channel itself.  V7 G·Wg·G=G at n=5 (rank 119/120,
3·10⁻¹⁵).  V8 timing: n=4 L=8 matvec 0.9–2.6 s.

**Results (n45_final_v1.json, Table tab:n4annealed).**
- Crossings of X_L = L·log(λ₁/λ_σ): (4,6) = 0.35820, (6,8) = 0.37899 —
  converging upward; linear extrapolation 0.400, Aitken-style 0.386 →
  **p_c^{(4)} = 0.40(2)** (bracket 0.385–0.415).  The replica trend
  continues away from the quenched point:
  0.233810 < 0.305(3) < 0.40 vs quenched 0.1597(8).
- Slope exponent: |dX_L/dp| at the crossing = 5.63/9.07/13.48 (L=4/6/8) →
  1/ν_eff = 1.18 (4,6), 1.38 (6,8) — rising toward the q=4 Potts 3/2
  (n=3 measured 1.15 vs 6/5; Ising 1).
- Continuous: gap at crossings (larger size) 0.146 → 0.131, ξ/L = 1.14,
  0.95 — order unity; no two-phase degeneracy (gap12 stays ≈ 1.98 at L=4
  with its minimum exactly at the crossing region).
- Amplitude ratio R = log(λ₁/λ_σ)/log(λ₁/λ_ε) at the crossings:
  0.128 → 0.176 → 0.203 — starts at the q=4 value 1/8 at L=4 and DRIFTS
  UPWARD, past 1/6.  The one clean diagnostic of n=2,3 degrades exactly
  where the borderline q=4 class predicts (multiplicative log corrections;
  ε–marginal mixing).  The absolute check is likewise inconclusive
  (L·log(λ₁/λ_ε) = 5.2 at the L=8 crossing vs 2πx_ε = 6.28 under the
  σ-side lattice-amplitude factor 1.3).  Honest verdict: the ratio
  diagnostic is NOT clean at n=4 at these sizes.
- Colour content (full S₄ resolution): the σ multiplet is 9-fold,
  (dim std)²; ordering triv > std > two > std⊗sgn > sgn at every (L,p);
  at L=8, p=0.36 the leading spectrum reads λ₁ (triv, 1), λ_σ (std.std,
  9), two.two (4), stdsgn.stdsgn (9), sgn.sgn (1), with λ_ε below all
  spin multiplets — the q=4 analogue of the deposited 1+4+1 pattern.
- λ₁ simple at every (L,p) tested; growth chain λ₁^{1/L} monotone in L
  (0.9190 → 0.9157 at p=0.05; 0.2180 → 0.2170 at p=0.75).

## 12a. The n=5 first-order diagnostics (L=4)

Bond space 120^{L/2}; the L=4 space (14400) via the same iterative
machinery with the pinv Weingarten channel (n=5 > D^{1/2}: Gram rank
119/120).  21-point scan, full colour classification + colour-trivial
projected solves (n5_annealed_scan_v1.json).

- Two-phase degeneracy gap12 = log(λ₁/λ₂-triv) at each n's own estimated
  transition: 2.15 (n=3) → 1.92 (n=4) → 1.71 (n=5) — tightening in the
  first-order direction.
- Crossing sharpness |dX₄/dp| at own p_c: 5.4 → 6.2 → 7.2 — steepening.
- Single-size locator: the gap12(p) curve has an interior minimum at
  p = 0.480 (n=5); at n=4 the same minimum sits at 0.380 against the
  extrapolated p_c = 0.400 — calibrating p_c^{(5)} ≈ 0.48–0.50, on the
  trend 0.234 < 0.305 < 0.40 < 0.49.
- Colour content: σ in std⊗std, 16-fold = (dim std)² — the S₅ analogue of
  the n ≤ 4 pattern; X₄(p) over the full grid recorded for the future
  two-size test.
- The decisive two-size test (gap saturation, ξ/L → 0) needs L=6
  (120³ = 1.7·10⁶ labels, ~5·10¹⁰ flops/transfer application): implemented
  and validated, but a full Arnoldi solve (~100 iterations × ~170 s/matvec)
  exceeds the 3 GB / 2-core sandbox budget.  The n=5 first-order claim
  remains a prediction SUPPORTED by (not established by) these data.

## 13. The Haar SMC record-multifractality run (Target C)

The manuscript's open problem "Haar record multifractality stays open" is
now supplied with its first numerical data: the quenched record SCGF
ψ_{L,p}(k) for Haar circuits, estimated by the specified particle filter
(haar_smc_lib_v1.py + haar_smc_v1.py): N=384 particles, one brickwork
period per block (T = 2L), systematic resampling, stabilized log c_t, on
the deposited Haar protocol; L = 6–12, p ∈ {0.10, 0.1597, 0.2338, 0.4},
k ∈ [−2, 2] half-unit, 8 circuits/point (6 at L=12); k = +2 top-up at
N=1536.

**Validation (all pass).**  Va: ψ̂(0)=0 exactly; particle surprisal
statistics vs the deposited haar npz at (L=8, p=0.2338, t=16): 2.295±0.009
vs 2.287±0.005 (z = 0.86).  Vb: brute-force enumeration of ALL records of
a fixed L=4 circuit — E[Ẑ_T] over 600 runs matches the exact
Z_T(k) = Σ_{Y:P>0} P^{1−k} within 2σ at every k ∈ {−1.5,−0.5,0.5,1.5}
(unbiasedness verified across 4 decades of Z).  Vc: at p=1 the exact
basis-state Markov chain — agreement within 1.4σ up to Z ~ 4·10¹⁰.  Plus
the internal identity ψ″(0) = Var(A_T)/T: central difference 0.428 vs
direct 0.427 at (L=8, p=0.2338).

**Results (haar_smc_summary_v1.json, Table tab:smchaar).**
- Genuine record multifractality: D(q) = τ(q)/(q−1) is NOT constant —
  spread over q ∈ [−1,3]: L=8: 0.20 (p=0.10) → 0.32 → 0.85 → 1.96 (p=0.4);
  at L=12, p=0.2338: 1.34 nats/period.  (Clifford: D exactly constant.)
  First measurement of the object the manuscript defines.
- Entropy rate: ψ′(0) = A_T/T per period rises with p (1.02, 1.50, 2.36,
  3.62 nats at L=8) and sub-extensively with L: per-site rate
  A_T/(TL) = 0.287/0.295/0.288 (L=6/8/10, p=0.2338) — L-independent to 5%.
- No finite-q freezing: over q ≤ 3 and all (L,p), min |τ″| = 0.24 nats/
  period — τ strictly convex; no linear branch.  First finite-size bounds
  on the freezing question (T = 2L, L ≤ 12 — far from asymptopia).
- Annealed vs quenched: (1/T)log E_ω Z exceeds E_ω log Z/T everywhere
  (e.g. +0.48 at L=12, p=0.2338, k=1) — the distinction the manuscript
  insists on, measured.
- Reliability: ESS_min flags k=+2 at p ≥ 0.2338 (as low as 1–6); the
  N=1536 top-up confirms those entries (z ≤ 1.4; the small upward shift is
  the expected Jensen-bias reduction).

**Files.**  Scripts: n45_annealed_lib_v1.py, n45_annealed_validate_v1.py,
n4_annealed_scan_v1.py, n4_eps_L8_v1.py (and n4_eps_fast_v1.py inline),
n5_annealed_scan_v1.py, n45_analyze_v1.py, haar_smc_lib_v1.py,
haar_smc_v1.py, haar_smc_topup_v1.py, make_cert_v5.py.  Results:
mipt_results/n4_annealed_scan_L{4,6,8}_v1.json, n4_colour_table_v1.json,
n4_growth_v1.json, n4_eps_L{4,6}_v1.json + n4_eps_L8_fast_v1.json,
n5_annealed_scan_v1.json, n45_final_v1.json, haar_smc_L*_p*_v1.json (16),
haar_smc_topup_*_v1.json (6), haar_smc_summary_v1.json.  Logs:
logs/n45_annealed_validate_v1.log, n4_scan_v1.log, n5_scan_v1.log,
haar_smc_v1.log, haar_smc_topup_v1.log.  Manuscript:
versions/manuscript_revised_v18_n4n5-smc.tex/.pdf (33 pp; Sec. sec:n4n5 +
Tables tab:n4annealed, tab:smchaar + Sec. sec:smcnumerics + abstract +
open-problems rewrite + bibitem Cardy1986), built by
versions/patch_v18_n4n5smc.py from v17a (anchors asserted).
