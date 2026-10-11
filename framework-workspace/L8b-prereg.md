# L-8d — FORMAL PRE-REGISTRATION
## Temporal spectral dimension of 4D CDT's de Sitter phase via projected two-walker meeting probability

**Status:** PRE-REGISTERED — frozen artifact. **Registration date:** 2026-10-11. **Program anchor:** pov-circle fw·KR·11 (L-8), protocol layer L-8b (v10.5), data context L-8c (v10.7), this artifact = L-8d (v10.8). **Read-out horizon:** 2029-10-10 (unchanged, binding). **Rule:** this document may only change through a new registration round, never by amendment-in-place.

> One-line scope: *measure whether the foliation-direction ("temporal") spectral dimension d_t of CDT de Sitter-phase geometries flows with diffusion scale — before knowing which direction is "predicted," and with the kills named in advance.*

---

## SR0 — Why this artifact exists

All protocol content below existed at text level in the program since v10.5 (L-8b). What did not exist: a standalone, frozen, blinding-disciplined document — the only form a test takes to data, or to a collaborator's inbox. The adjudication that forced it (`before-running-eval.md`, A1) recorded the split: **text-level registered since v10.5; artifact-level missing until now.**

Lineage warnings carried into the artifact, not beside it:
- *(Trap-inheritance)* Under any Lifshitz-type dispersion the time-part of the diffusion kernel is the ordinary 1D heat kernel, so d_t ≡ 1 analytically. **The null-expectation of this test, by construction-sensitive argument, is "no flow." See SR6-R.**
- *(Confabulation-record)* The one datum that previously "matched" this test's desired headline ("spine d_s = 1.019 ± 0.015", author-less, venue-less) failed three independent citation checks and is banned for/against (L-8c). **Hence SR8 (blinding).**

## SR1 — Data

- **Ensemble:** CDT configurations in the extended de Sitter phase (phase C_dS), dimension D = 3+1, fixed N4 with the full foliation-time assignment by construction (standard CDT convention).
- **Size:** N ≥ 100 configurations per bare-parameter point; at least one point at/near the canonical point (κ0 = 2.2, Δ = 0.6), plus ≥1 additional point if available.
- **Inclusion rule (binding):** every configuration of an acquired ensemble is analyzed; no subset selection by outcome, drift, or volume-profile outlier rejection beyond a *pre-declared* burn-in cut. Post-hoc exclusions require a new registration round.
- **Availability check (registered with truth value UNKNOWN as of 2026-10-11):** no public 4D C_dS ensemble with foliation data is confirmed to exist. Public tooling is 2D CDT (JorenB/2d-cdt; guide: arXiv:2310.16744). See SR9.

## SR2 — Diffusion kernel (frozen at protocol level)

- Lazy random walk on the dual graph of the triangulation, time-consistent adjacency (per-slice + inter-slice links as the configuration gives them), absorbing at the t = 0 endcap; diffusion time σ in integer steps, ensemble-averaged return probabilities; even/odd-σ smoothing per Kommu (arXiv:1110.6875) to remove bipartite oscillation.
- **Convention C1 (re-affirmed, binding):** the SAME kernel, SAME ensemble, SAME σ supports both d_s-slice and d_t extractions; σ-windows shared.

## SR3 — Observables and estimators (frozen)

1. **Slice spectral dimension d_s(σ; t0):** return probability of walks restricted to a spatial slice at fixed foliation time t0 (max-volume slice and volume-averaged variant; both reported), Benedetti–Henson lineage (PRD 80, 124036). d_s = −2 ∂ln P_ret/∂ln σ, finite-difference with the even/odd merge.
2. **Projected meeting probability (Eichhorn–Mizera lineage, foliation projection):** P_meet^(t)(σ) = ∫dt [∫ d^3x P(x, t, σ)]²; implementation: two independent walks from the same seed, projected spatial-marginals per time step; meeting = equal projected position; d_t(σ) = −2 ∂ln P_meet^(t)/∂ln σ.
3. **Adaptation-check (prerequisite, not optional):** the E&M estimator was developed for causal sets. Before Gate C0b, the projected-meeting construction is validated on the CDT dual graph: (i) on a fixed slice sequence the marginal projection is well-defined; (ii) in the flat control it reproduces the 1D heat-kernel scaling (Gate C0a target). This check is a C0a-precursor, not a separate deliverable.

## SR4 — Calibration gates (must pass before any ensemble run; methodology published either way)

- **GATE C0a — flat control:** 4D Minkowski spacetime discretized on a CDT-like foliated lattice. Targets (mid-σ window, away from discreteness onset and finite-size turn-over): d_t = 1 ± 0.05, d_s = 4 ± 0.05. If not met → protocol has a bug or E&M does not adapt to CDT as expected → fix required, full re-freeze, new hash, methodology note published either way.
- **GATE C0b — analytic control:** 2D CDT, where spectral quantities are known analytically (Durhuus–Jonsson–Wheater line). The extraction pipeline (code, unchanged) run on 2D configurations must reproduce the analytic d_s structure within quoted precision. If not → same consequence chain as C0a.
- **Gate discipline:** gates are pass-before-ensemble; a failing gate is itself a reportable finding about the estimator's CDT-adaptability (feeds K2, theory-choice tier).

## SR5 — [reserved] extraction runs (post-gate)

Pipeline frozen by SR8(i) runs on all SR1 configurations; per-configuration d_t(σ) and d_s(σ; ·) reported; ensemble averages with bootstrap errors; flows binned in the pre-declared σ-windows (W_ir, W_cp, W_uv) fixed at Gate C0a pass-time from the flat-control's window locations, rescaled by the relative lattice spacing.

## SR6 — Predictions (tiered; the tiering is itself registered)

- **P0 — PRIMARY, sole registered prediction:** **direction-of-flow.** d_t(σ) is non-constant with negative slope: d_t(W_uv) < d_t(W_ir) with the gap exceeding 2σ_boot (bootstrap over configurations, all included).
- **P1 — CONDITIONAL SECONDARY (tested only if P0 confirms):** consonance of the two extracted flows with a z-parametrized (Hořava-form) account, with d_t(U V) ≈ 1/z printed as *hypothesis-window, derivation-obligation* (the 3-independent-UV-numbers scatter, L-8c item (iii), is the reason this is not a primary quantity). Any d_s+d_t sum-form is permanently out of scope (sum-invariance withdrawn, v10.5/H1).
- **SR6-R — REGISTERED NULL-EXPECTATION (binding on all reporting):** under any Lifshitz-type diffusion the time-part kernel is the 1D heat kernel ⇒ d_t ≡ 1 for all z. **A P0-confirm is therefore a double finding: (a) directional co-variation exists and (b) CDT deviates from the Lifshitz picture in the foliation direction.** Reports must print both halves or none.

## SR7 — Kills (three, double-gate: kill consumes only on pre-registered criteria)

- **K1 (lab-tier, decisive):** d_t ≡ 1 ± 0.1 at all scales, with blinding intact and gates passed. → bridge dies in CDT; registered kill-event (kill-log asset at program level only).
- **K2 (theory-choice-tier):** principled ill-definition — the projected-meeting estimator cannot be made well-defined on CDT dual graphs (adaptation-check fails in a way no re-freeze fixes within convention C1).
- **K3 (redirect):** d_t flows but not in any z-parametrized form (P0 confirms, P1 fails) → claim redirects: direction yes, z-structure no.
- No fourth kill is added after registration without a new round.

## SR8 — Blinding and anti-confabulation (binding)

(i) **Code-before-data:** analysis code frozen and hash-committed (SHA-256 printed here at freeze time: `________________________`) **before** any access to any SR1 configuration; the hash is the artifact. (ii) **Analyst blinding:** the pipeline reports flows before any comparison to P0's direction; the comparison step is run last, after pipeline freeze; analyst's state-of-knowledge at each step logged. (iii) **Whole-ensemble:** SR1 inclusion rule; no subsets. (iv) **Windows pre-declared:** W_ir/W_cp/W_uv fixed at gate time, not outcome time. (v) **External review:** one CDT-experienced reviewer external to the program reviews code + gates before scoring. (vi) **No re-windowing:** any adjustment to windows, cuts, or estimators after data access = new registration round with the round's full audit.

## SR9 — Resource routes (priority order, registered)

1. **R1 — running-group collaboration (highest probability):** this artifact is the outreach payload; the framework supplies the question and the blinding discipline; the collaborating group supplies ensembles + reviewer. Targets: the Ambjørn–Jurkiewicz–Loll line (Nijmegen/IMAPP + collaborator groups).
2. **R2 — 4D port/extension:** extend a 2D framework (JorenB/2d-cdt-class) to 4D + gate C0b/C0a. Multi-month; requires CDT-experienced implementer.
3. **R3 — snapshot re-analysis:** downgraded pending the SR1 availability check; currently no confirmed public 4D C_dS ensemble with foliation data.

## SR10 — Scoring → program disposition (frozen mapping)

| Outcome | Disposition |
|---|---|
| P0 confirms (gates passed, blinding intact, external review clean) | First display-level check registered; **double-finding flag mandatory** (SR6-R); P1 testing opens |
| K1 | Kill-event; L-8 dies in CDT; kill-log entry; Lakatos date 2027-10-10 unchanged |
| K2 | Theory-choice-tier kill of the estimator-route; redirect options reviewed in a new round |
| K3 | Redirect: direction-of-flow stands, z-structure dies; L-8 re-scoped in a new round |
| Infeasible (no R-route opens in 36 months) | **Retirement-as-inapplicable**: E5-tier boundary event — not a result, not a framework failure; the registered-stake ledger (L-8) keeps its stake-line with this event attached |

## SR11 — Schedule (binding)

- Pre-registration (this artifact): **2026-10-11** ✓
- Execution window: 36 months from an opened R-route; status check-ins each registration round.
- **Read-out horizon: 2029-10-10** (inherited, unchanged).
- Amendment rule: none; new registration rounds only.

---

**Standing risk line (carried from the program, unamended):** throughput zero; benchmark unrun; contraction/Lakatos 2027-10-10 binding; read-outs under 2029-10-10; registrations are not results.

**Fingerprint:** L-8d-PR-2026-10-11 — frozen.
