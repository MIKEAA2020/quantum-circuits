# RP11b ENGINE v0.1 — CALIBRATION LEDGER C1–C5
fingerprint: R11b-CAL-2026-10-11
date: 2026-10-11 · engine: /home/user/rp11b_engine.py · report: /home/user/rp11b_cal_report.json · runtime 12.4 s
mode: exact-probe (independent enumeration of two invariants + identity test). No theorem-prover scope. No yield scored. Publish-either-way.

## registered expectations vs outcomes

| case | registered expectation | outcome | match |
|---|---|---|---|
| C1 Ising KW, planar 3×3 grid | completion t = t̃ (tanh K = e^{−2K̃}); K* = 0.4406867935; residual = prefactor + b.c. | map recovered exactly; K* = 0.440686793510 ✓; residual printed as registered; **verdict label "OBSTRUCTION"** | MATH ✓ / LABEL ✗ → F1 |
| C2 q=3 Potts RC, primal 3×3 grid vs dual (5-vertex multigraph) | v·ṽ = 3; v* = √3; unique over 6-map library | unique hit: ('vt = q/v', a=12, b=−4), i.e. Z_G = v^{E} q^{−(V*−1)} Z_{G*}(q, q/v); v* = √3 = 1.732051 ✓ | ✓ |
| C3 Ising 3×3 torus | OBSTRUCTION (homology); residual = 4 spin-structure sectors | four (wx,wy) sector polynomials enumerated and all distinct; no single-map completion; residual = 2×2 sector basis | ✓ |
| C4 S-duality structure | S²=−I, (ST)³=S²; coroot(B₃)=roots(C₃); residual = center/level | all four checks true; residual printed as registered | ✓ |
| C5 particle-vortex Poisson chain | numeric identity to 1e−11; residual = winding sectors | certified over 25 random (a, φ) at 1e−11; a ↔ 1/a coupling inversion recovered; residual = winding integers | ✓ |

SCORE: 5/5 substantive matches; 1 rig-level defect (F1). Assumption-debt ledger H1–H5 printed verbatim in the JSON report.

## finding F1 — verdict-taxonomy asymmetry (calibration-flaw class: rig, not math)

C1 tested **bare** polynomial equality H_G(t) == H_G*(t̃); C2 tested equality **up to monomial prefactor** v^a q^b.
Both cases are duality-with-prefactor in reality, so the rig classified C1 "OBSTRUCTION" while C2 (same logical form) was classified "FORCED COMPLETION". The registered C1 expectation (a completion) is the correct physics — the flaw is in v0.1's labeling rule, not in the enumeration.

**Rule for v0.1.1 (forward-only, no re-scoring of v0.1):** all verdicts must be issued on prefactor-normalized comparisons; the prefactor itself moves to the residual-freedom field. Applied v0.1 results *as run* would re-label C1 → FORCED COMPLETION; v0.1 printed record above stands unaltered (amendment rule).

## what calibration establishes about engine behavior

1. Map-library discipline works: unknown-prefactor identities are found by exact expand-sweep, not assumed (C2 prefactor (12, −4) was *recovered from data*, matching the standard planar identity).
2. Obstruction classification works: C3 separates local completion (map exists) from global obstruction (topology) — the engine's core design claim is exercised and confirmed.
3. Residual-freedom field is never empty in any non-trivial case (H1–H5 ledger active every case) — debt-tracking is the engine's default, as designed.
4. F1 is the first calibration-found rig defect of the framework; logged per publish-either-way.

## pending rows (never guessed; discipline item)

Paper-specific cases (period map B_even·B_odd, compressed operator C_comp, bond channel W_{p,n} counit test, n-replica map Φ_n on G_n^⊗L, Clifford 3-design conjugation) are **definition-pending: paper upload required**. W3-v10 benchmark (pre-cutoff, blinded, externally scored): registered, unrun.
