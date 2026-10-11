# 1+1D Calibration Run — Results Report (task twenty; v10.9 round, gate-level)

**Date:** 2026-10-11 · **Code:** `cdt_cal_2d.py` (hash-reproducible, seed 20261011) · **Output:** `cdt_cal_2d_report.json` · **Runtime:** 213.9 s (2-core sandbox, numpy) · **Round:** task twenty ("evaluate, verify, complete the search") with the standing execution challenge accepted: *the 2D gate was buildable rounds ago — now it is built and run.*

> **Scope line (binding):** this is a **pipeline validation under the L-8d pre-registration's gate machinery** — the 2D analog of Gate C0a (flat control) and Gate C0b-partial (solvable-case control). It is **not** the L-8 test, **not** a bridge datum, and it moves no yield column: throughput (bridge-artifact deliveries) remains **zero**. Registrations are not results; gate passes are not results either.

---

## 1. What was run

- **Kernel (Convention C1, frozen for the run):** lazy random walk on the 3-regular dual graph: stay w.p. 1/2, else uniform over the 3 neighbors (1/6 each). Same kernel, same σ-grid for both d_s and d_t on every control — C1 held operationally, not just declared.
- **Estimators:** full return probability P_ret(σ) via exact distribution propagation from 48 seeded walker-packets per configuration; projected two-walker meeting probability on the time-marginal M(σ) = Σ_strips P_strip(σ)² (Eichhorn–Mizera projected lineage); d(σ) = −2·dlnP/dlnσ by local log-window fits.
- **Controls:**
  - **FLAT 2D:** 60 strips × 600 ring, regular zigzag (composition c_i ≡ 1), time-periodic torus. N = 72,000 nodes.
  - **CDT-LIKE 2D ENSEMBLE:** 6 configurations, T = 48 strips, fluctuating profiles (n_0 = 700, diffusion ±90 per strip, clamp [128, 1600]), inter-strip fibrations by uniform positive compositions; N = 36,152–98,968 nodes. **Measure caveat (printed):** uniform-on-compositions × arbitrary fibration phase; not the Haar/Regge-weighted 2D CDT measure. MCMC upgrade exists publicly (dyntri-cdt2d).
  - **SLICE:** RW confined to one spatial ring (analytic target d = 1).

## 2. Numbers

| Control | observable | σ = 8 | 16 | 32 | 64 | 128 | 256 | window [16–128] | target | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Flat 2D | d_s | 1.993 | 2.032 | 2.006 | 2.001 | 2.000 | 2.000 | **2.003 ± 0.006** | 2 ± 0.1 | **PASS** |
| Flat 2D | d_t | 0.995 | 0.990 | 0.993 | 0.996 | 0.998 | 0.999 | **0.996 ± 0.002** | 1 ± 0.1 | **PASS** |
| Slice ring | d_slice | — | 1.000 | — | — | — | — | **1.000 ± 0.000** | 1 | exact |
| CDT-en. 2D | d_s | 1.959 | 1.998 | 1.986 | 1.984 | 1.979 | 1.979 | **1.984 ± 0.004** | ≈2 (±0.25) | **PASS-partial** |
| CDT-en. 2D | d_t | 0.952 | 0.950 | 0.946 | 0.938 | 0.929 | 0.915 | **0.938 ± 0.006** | 1 ± 0.1 | **PASS (just); drift noted** |

## 3. Verdicts

- **GATE C0a-2D-flat: PASS.** Both targets inside tolerance across the whole σ-table (d_s within 3‰ of 2 at σ ≥ 32; d_t within 1% of 1 at σ ≥ 8). The estimator reproduces exact analytic values on a control with no free parameters. This is the strongest possible *negative* gate result: the pipeline does not manufacture structure.
- **GATE C0b-2D (partial): PASS-partial.** d_s ensemble ≈ 1.984 — consistent with the exact 1+1D CDT result d_s = 2 (Durhuus–Jonsson–Wheater), which lends confidence that the composition-fibration sampler reproduces the correct observable behavior in its window ("partial" = measure caveat above). d_t ≈ 0.94: inside tolerance, **with a mild downward drift across σ (0.952 → 0.915) that is hereby NOT claimed as flow**: for the C1 kernel the strip-move probability per step is construction-fixed at 1/6, so the time-marginal is a 1D chain and d_t = 1 *by kernel construction*; the residual σ-dependence tracks strip-width mixing in the meeting marginal plus finite-T torus effects at large σ relative to T = 48. If a future MCMC-grade (dyntri-cdt2d) re-run shows the same drift after thermalization, this becomes a noise-budget item to quantify — flagged, not scored.
- **What the run operationalized (the round's genuine structural gain):** the **trap-inheritance warning, made mechanical**. In 1+1D the registered C1 kernel *cannot* return anything but d_t ≈ 1 — which is exactly why (i) the 2D gate validates the pipeline, not the claim, and (ii) only the 4D-ensemble run under L-8d is decisional. The isotropic-control print from v10.5 is now accompanied by a live numerical control.
- **What it did not do:** it did not touch the resource gap (no 4D de Sitter ensembles), did not score any framework yield, and did not alter the L-8 kill context. It raised the L-8b pipeline from *paper-registered* to *numerically behaved on controls* — a machine check, not a result.

## 4. Next gate items (registered)

1. MCMC-grade re-run: dyntri-cdt2d thermalized 2D ensemble (measure caveat removal), noise-budget quantification of the d_t drift item.
2. 4D chain: L-8d route R1 (collaboration with the Nijmegen/minimalist-line groups) remains highest-probability; R2 (build) now has a verified engineering base — dyntri-rs (generic N-D structures public; dimension-specific MCMC generators public for 2D only) and CDT-plusplus (archival scope: spherical 2+1D, 4D explicitly unsupported).
3. The emitter *not* to use as gate data: any dataset of the GRU/spine lineage (see `search-eval.md`, adjudication B4) — provenance-unverified data in a gate is a blinding-protocol breach by construction.

**Standing risk, restated:** throughput zero; benchmark unrun; contraction/Lakatos 2027-10-10 binding; L-8 read-outs under 2029-10-10. A gate pass is pipeline hygiene — registered as exactly that, no more.
