# L-8d Pre-Registration — AMENDMENT AM1 (registration round 2)
**Date:** 2026-10-11 · **Amends:** `L8b-prereg.md` (frozen, fingerprint L-8d-PR-2026-10-11) · **Basis:** Node A gate run + diagnostics (`cdt-2d-mcmc-results.md`, `cdt_mh_2d_report.json`, `cdt_mh_diag_report.json`) · **Scope:** estimator-discipline only; no prediction, kill, or schedule item touched.

## AM1-1 — Gate C0b promotion status

C0b-full **denied**, on evidence. The v10.9 PASS-partial stands, upgraded in status to: **PASS-partial with quantified systematic**. The upturned noise-budget item (d_t drift) is closed: mechanism identified as the estimator crossover below.

## AM1-2 — New Gate C0b2: the crossover rule (binding on any d_t report, 2D or 4D)

**Pinned systematic.** The projected two-walker meeting estimator exhibits a finite-mixing-time crossover: whenever the σ-window sits at/below the within-strip/slice equilibration timescale, P_meet^(t)(σ) decays slower than the asymptotic σ^{−1/2}, and the windowed estimator reads **d_t < 1**, with the deficit scaling with slice size and rate heterogeneity, and with d_t(σ) → 1 asymptotically (1D recurrence). Evidence: ensemble d_t = 0.609 ± 0.033 (small-slice, fluctuating), 0.771 ± 0.042 (small-slice, flat), 0.938 ± 0.006 (large-slice), 0.996 ± 0.002 (largest-slice control) — monotone in slice scale; the reduced strip-chain with measured profile rates reproduces the windowed value (0.75); no flow is required anywhere to explain it.

**Therefore, for every d_t measurement:**

1. **Full σ-table mandatory.** No scalar/windowed d_t may be reported without its per-σ table. (Finite-T overshoot structure — a rise above 1 followed by turn-down, as observed at σ ≈ 64–128 in 2D — is a finite-torus signature and must be labeled as such when present.)
2. **Window-above-mixing rule.** The accepted reading window must begin *above* the within-slice mixing time of the ensemble under study, estimated per-ensemble (from the estimator's own short-σ slope-break and a slice-homogeneity diagnostic), and the estimate must be printed. A window chosen inside the crossover region invalidates the reading for scoring purposes.
3. **Crossover diagnostic in every report.** Each d_t report carries: (i) the within-slice mixing-time estimate, (ii) the slice-size/heterogeneity summary, (iii) the explicit statement that the observed σ-shape is or is not crossover-consistent before any flow language is used.
4. **No rescoring.** Anything previously read without this rule (nothing exists outside gate runs) would be rescored; the rule applies forward from 2026-10-11.

## AM1-3 — What this amendment knowingly protects

Under Lifshitz-type expectations d_t ≡ 1 *asymptotically*; the crossover shows an estimator that reads *below* 1 in-window independent of the truth. Without C0b2, the 4D run could manufacture (i) a false kill (reading crossover as kill-1-free "flow"), or (ii) a false hit (reading crossover-consistent d_t < 1 as P0-confirming direction-of-flow). Both paths ran live in this gate round and were caught. The double-finding discipline of SR6-R is unchanged; C0b2 is its estimator-level precondition.

**Fingerprint:** L-8d-PR-2026-10-11-AM1. The base artifact and this amendment travel together; the base text is unaltered.
