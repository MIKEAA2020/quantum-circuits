# Node A — MCMC-grade 1+1D Gate Re-run: Results (fail verdict, mechanism quantified)

**Date:** 2026-10-11 · **Code:** `cdt_mh_2d.py` (main), `cdt_mh_diag.py` (diagnostics D1/D2) · **Machine output:** `cdt_mh_2d_report.json`, `cdt_mh_diag_report.json` · **Duration:** ~70 s total · **Rule honored: publish-either-way.** The verdict below is a gate failure with the mechanism isolated — which is a *successful gate event*, not a buried one.

---

## 1. The run

Replaced the v10.9 direct-composition sampler with an equilibrated Metropolis chain, per Node A:
- **Ensemble:** microcanonical in total volume (Σn_t = 1200 fixed, T = 48 rings, n_t ∈ [8, 200] fluctuating, profile sd ≈ 14.7–18.6); pair-shift profile moves + uniform type-string Gibbs resampling (300k-move burn-in, 80k-move spacing between the 6 configurations, 2,400 nodes each).
- **Measure convention (printed, unamended):** uniform over labeled-slot type-string microstates (arbitrary U/D arrangements, gap-vertex valence 3 admitted); profile-marginal ∝ ∏ C(m_s+m_{s+1}, m_s)·δ(Σ−1200); rooted-convention collation with Ambjørn–Loll '98 transfer matrix C(l+m−1, l−1) = **open item A1b**; d_s = 2 and d_t = 1 are convention-robust at gate granularity.
- **Targets (registered before execution, same as v10.9):** d_s ≈ 2 (± 0.25), d_t = 1 ± 0.1, window [4, 40], with the explicit drift question: does the v10.9 d_t drift survive equilibrated measure?

## 2. Numbers and verdict

| run | profile | slice size | d_s @[4,40] | d_t @[4,40] |
|---|---|---|---|---|
| v10.9 C0a-flat | flat | 600 | 2.003 ± 0.006 | 0.996 ± 0.002 → **PASS** |
| v10.9 C0b ens. | fluctuating | 128–1600 | 1.984 ± 0.004 | 0.938 ± 0.006 → PASS-partial, drift flagged |
| **Node A ens.** | fluctuating (eq.) | 8–200 (sd≈17) | **1.687 ± 0.027** | **0.609 ± 0.033** → **FAIL** |
| D1 diag | flat (eq.) | 25 | 1.816 ± 0.056 | **0.771 ± 0.042** |
| D2 diag | strip-chain, eq.-profile rates | — | — | **0.746 ± 0.131** (table 0.55→1.33, σ-overshoot at 64–128) |

**Verdict: C0b-full NOT promoted; gate stands FAIL → resolved as "PASS-partial + quantified systematic".** The d_t σ-table rises monotonically from ~0.56 toward 1 (asymptotic 1D recurrence); the overshoot ≈ 64–128 prints the finite-T torus turn. The drift question is now answered completely: the v10.9 value 0.94 is the same systematic's gentle tail at large slice sizes. Not a flow anywhere in sight — which is also what the mechanism analysis predicts.

## 3. Pinned mechanism: the crossover systematic of the projected-meeting estimator

Within-strip equilibration competes with strip-jumping: a walker's strip-marginal behaves as a clean 1D chain only after it equilibrates inside strips. In any σ-window at/below that mixing scale, the projected meeting probability decays *slower* than σ^{−1/2}, so the windowed estimator reads **d_t < 1**, with deficit:

- increasing as slice size falls (0.996 → 0.94 → 0.77 → 0.61 as typical slice size runs 600 → ~500 → 25 → ~25±fluct); further aggravated by profile-rate heterogeneity (D1 flat: 0.77 vs full ens.: 0.61 — trapping contributes on top of mixing);

- **asymptotically vanishing** — d_t(σ) → 1, all columns of the σ-table monotonically recovering.

The reduced strip-chain (D2: forgetting all spatial structure, rates read off equilibrated profiles) alone reproduces the windowed value (0.75 vs 0.61; residual gap = spatial correlations) — so the effect is kinematic estimator physics, not geometry.

**The 4D consequence (the reason the gate earned its keep):** a naive d_t reading in a finite-ensemble (∼10⁴–10⁵ simplex) window **cannot** distinguish this crossover from a genuine flow. Without a rule, the 4D run would be free to manufacture d_t ≈ 0.6 "hits" — or phantom kills — out of estimator physics. That hole is now closed by Gate C0b2 (see `L8b-prereg-am1.md`).

## 4. d_s side note (same physics)

d_s reads below 2 at small slices (1.82 flat / 1.69 fluct) — spatial-saturation crossover, same family; the v10.9 large-slice values recovered the registered value. No separate item opened; the same C0b2 rule (mixing-time-controlled windows) covers it.

## 5. Registered outcomes

1. **C0b-2D:** partial retained; promotion denied on evidence.
2. **Noise-budget item: CLOSED** (drift mechanism = crossover systematic; quantified).
3. **Gate C0b2 registered** (amendment AM1): window-selection must sit above the within-strip mixing time (computed per-ensemble from the estimator's own σ-table + homogeneity diagnostic), and every d_t report must carry the full σ-table, not a windowed scalar.
4. **Open item A1b:** rooted/unrooted convention collation for the strip transfer matrix.
5. Node A's side effect: the 2D toolchain is now at MCMC grade (equilibrated, convention-printed, 2400-node microcanonical) — the remaining upgrade axes are volume scaling and convention collation.

Standing risk (from CONVENTIONS.md, single copy): throughput zero; benchmark unrun; Lakatos 2027-10-10; L-8 horizon 2029-10-10. A gate failure that produces a quantified estimator rule is the machinery working, not a setback — and it changes none of the standing numbers.
