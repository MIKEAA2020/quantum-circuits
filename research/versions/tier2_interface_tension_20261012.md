# Tier-2 interface-tension round — which of the suggested computations
# can be executed, and what they return

**Date:** 2026-10-12 · **Round:** research v23 (deposits:
`research/scripts/v22-exactZ3-n5L8/tier2_interface_tension_v1.py`,
`research/results/tier2_interface_tension_v1.json`; ledger v22 —
corrected in place the same day per the author's call: ledger v23).
**Manuscript of record:** `manuscript_revised_v32.tex` — **not edited;
no new version needed** (the v32 registered conditional stands; this
deposit quantifies its completion test. The proposed v33 sentence was
corrected per the author's call — §6, same day — and withdrawn as a
version-triggering edit: the corrected conditional is already the v32
body's own statement. Script and JSON deposits unchanged; only this
note's presentation corrected — ledger v23.)

The question this round answers: of the three-tier strengthening
program for the n=5 first-order test (extend to L=10; extract the
interface tension by fitting σ_eff(L); extend to L=12), **which parts
are computable — and what do the computable parts return?**

---

## 1. What is computable, tier by tier

| suggestion | verdict | where |
|---|---|---|
| **Tier 1** — L=10 at n=5 (the eigen-solve) | **not on this sandbox; days on adequate hardware via the deposited design** | v21 method round (`tier1_L10_design_20261011.md`): exact sector dimension 346,177 (validated vs the 3,865 anchor); dense block 1.7 TiB ×2; streaming assembly 8.6×10¹⁶ MACs/p-point = 40 days at the measured 2.5×10¹⁰ MAC/s; streaming matvec → Lanczos(60) ≈ 3.3 years; full-space iterative needs 185 GB of Krylov vectors. Two viable routes specified: (A) distributed streaming / distributed full-space iterative (pure engineering on the deposited code, ~10³ cores → hours-to-days per p-point) and (B′) the CG-coupled colour basis (resting on the machine-precision-validated W-channel factorization). |
| **Tier 2** — the σ_eff(L) = Σ − A/L fits | **computed this round, from the deposits of record** (no new eigen-solves; two already-deposited ladder cells newly used) | below, §2–§4 |
| **Tier 3** — L=12 at n=5 | **no** — cluster-scale; and this round's discriminator analysis (§4) shows the fifth size, not the fourth, is where the exponential/power-law decision plausibly lands | §4 |
| n=3 baseline at the **asymptotic** envelope | **computed this round** (5-point extrapolation incl. the L=12 cell; three fit forms; out-of-sample check) | §5 |
| p_c⁽⁵⁾ locator extrapolation | computable in principle, **deliberately not applied** — v32's plausibility-range label over the monotone-decreasing 0.48/0.47/0.465 sequence stands (three points, no size extrapolation at n=5); revisits when L=10 lands | v32 item 3 |
| abstract/body verb alignment + registered conditional | **already shipped** as v32 items 1–7 | `changelog_v32.md` |

## 2. The extended ladder (every cell re-extracted and validated)

Two ladder cells were **already deposited but never used** in the
manuscript's tables — both confirmed here and folded in:

- **n=3, L=12** (gap₁₂ = 0.4995 at p=0.30, `n3_annealed_scan_block12.json`,
  dim_k0 = 7,826 = the manuscript's own anchor): gives the **fourth**
  σ_eff interval at n=3. This is the "matched fourth n=3 point likely
  already in the deposited data" — it was.
- **n=4, L=10** (gap₁₂ = 0.4661 at p=0.38, `n4_L10_scan_v2.json`):
  gives the **third** σ_eff interval at n=4.

Full ladder (gap₁₂ at the coexistence locators; published cells
reproduce the v32 tables to ≤ 6×10⁻⁴):

| L | n=3 (p=0.30) | n=4 (p=0.38) | n=5 (p=0.47/0.465) |
|---|---|---|---|
| 4 | 2.1472 | 1.9187 | 1.7114 |
| 6 | 1.1853 | 0.9896 | 0.8057 |
| 8 | 0.8165 | 0.6445 | 0.4797 |
| 10 | 0.6209 | **0.4661** | — |
| 12 | **0.4995** | — | — |

σ_eff (ΔL=2, interval midpoints): n=3: 0.297, 0.186, 0.137, **0.109**;
n=4: 0.331, 0.214, **0.162**; n=5: 0.377, 0.259. The new cells preserve
the two signatures the manuscript prints: at every matched interval
the rates rise monotonically with n, and at n=3 they decay with size.

## 3. The Σ − A/L fits (the Tier-2 computation proper)

Finite-size ansatz σ_eff(L̄) = Σ − A/L̄ (L̄ = interval midpoint;
geometric-midpoint refits shift Σ by < 0.01):

- **n=3 (4 points, dof 2): Σ = −0.055 ± 0.012**, A = −1.74
  (leave-one-out: −0.028 … −0.068, spread 0.040).
- **n=4 (3 points, dof 1): Σ = −0.055 ± 0.016**, A = −1.92.
- **n=5:** two points — no fit; the registered discriminator below.

**The honest reading.** Both controls return the *same* small negative
Σ. A negative interface tension is unphysical: the sign is the
misspecification signature of the first-order ansatz at crossover
sizes (L̄ ≤ 11), not a measurement. What the fits deliver is the
**exclusion**: at this order, no positive interface tension is
extractable at n=3 *or* n=4 — the continuous and marginal controls are
indistinguishable under this ansatz at accessible sizes, exactly as
the manuscript's "the accessible sizes sit in the crossover region"
predicts. The discriminating signatures at these sizes remain the ones
the manuscript already prints: the level ordering at matched
intervals and the L·gap₁₂ envelope.

This *sharpens* Tier 1's role rather than replacing it: the Σ-fit
machinery is now validated end-to-end on the controls (null behavior
characterized, error bars and leave-one-out spread on record), so the
L=10 point at n=5 drops into a ready, quantitative test.

## 4. The registered quantitative discriminator for L=10 (n=5)

From the two n=5 intervals: σ_eff·L̄ = 1.883, 1.815 (spread 0.068).

- **Power-law continuation** (Σ = 0, σ_eff = c/L̄ with c = 1.849 ±
  0.034): predicts σ_eff(8→10) ≈ **0.206**, i.e. gap₁₂(L=10) ≈ 0.318
  and α_eff(8→10) ≈ 1.84.
- **Flip threshold**: the 3-point Σ-fit turns positive at
  σ_eff(8→10) ≳ **0.213** (gap₁₂(L=10) ≲ 0.313, α_eff ≳ 1.91).

The two readings sit ~0.007 apart in σ_eff (~3% of the value).
Consequences, stated plainly:

1. A single L=10 point *at the threshold* is ambiguous on its own;
   the decisive observable is the **trend** of σ_eff across intervals
   (does it break the c/L̄ decay?) — and, per Tier 3, the fifth size.
2. The v32 registered conditional ("stabilizing at a positive
   interface tension" vs "continue to decay") now carries numbers —
   with the single-point limit stated up front: the two branches sit
   ~0.007 apart in σ_eff at the fourth size, so the numbers quantify
   the completion test without making one L=10 point decisive. The
   power-law branch reads σ_eff(8→10) ≈ 0.205 (gap₁₂(L=10) ≈ 0.318,
   α_eff ≈ 1.84); the first-order branch needs σ_eff(8→10) ≳ 0.213
   (gap₁₂(L=10) ≲ 0.313, α_eff ≳ 1.91) for the 3-point Σ-fit to turn
   positive — and at exactly that threshold the first-order reading
   degenerates to the power law (Σ = 0 is c/L̄), so the branches
   separate only at the next interval: the power-law continuation
   gives σ_eff(10→12) ≈ c/L̄ ≈ 0.17, while a genuine positive Σ keeps
   σ_eff at its level (≳ 0.2). The controls sit at 0.137 (n=3) and
   0.162 (n=4) at the same L̄ = 9 — below both n=5 branches, a level
   separation that carries no branch information (n=5's decay
   constant is simply larger). *[Corrected 2026-10-12, author's call —
   the original text here read "stabilization means σ_eff(8→10)
   holding at ≳ 0.21 while the controls' extrapolated σ_eff at the
   same L̄ is ≈ 0.10–0.13; decay means following the controls toward
   ≈ 0.20 and below": the 0.10–0.13 figure is the controls'
   next-interval level (0.109 measured, ≈ 0.12 extrapolated, at
   L̄ = 11), not their L̄ = 9 value; and the decay branch is n=5's own
   c/L̄ continuation, not the controls'.]*
3. α_eff gives the same test in the dual reading: the n=3 α_eff
   asymptote is **0.951 ± 0.028 ≈ 1** (the saturating-envelope value,
   validating the manuscript's "drifts down toward the value a
   saturating envelope implies"); n=4's is 1.21 ± 0.05 (above 1, as
   the marginal q=4 with log corrections requires); the n=5 two-point
   power-law reading would sit at α ≈ 1.67 — a value no continuous or
   marginal Potts class realizes, which is precisely the
   super-continuous level the manuscript reports.

## 5. The n=3 envelope, extrapolated (the asymptotic comparison)

With the L=12 cell the n=3 L·gap₁₂ sequence is
8.589 → 7.112 → 6.532 → 6.209 → **5.994**. Fits on all five points:

| form | asymptote â ± s | out-of-sample (fit L≤10, predict L=12) |
|---|---|---|
| a + b/L | 4.63 ± 0.11 | 5.88 vs deposited 5.99 (−0.12) |
| a + b/L² | 5.76 ± 0.05 | 6.13 vs 5.99 (+0.13) |
| a + b·ln L/L | 2.0 ± 0.7 | 5.55 vs 5.99 (−0.45) |

The form bracket is **[4.6, 5.8]**; the q=3 Potts thermal dimension
x_ε = 4/5 gives 2πx_ε = 5.03, inside the bracket (consistency
observation; the two-phase thermal splitting makes the ε operator the
natural identification). The n=4 envelope is form-unstable (1/L → 2.6,
1/L² → 4.2) — expected for the marginal class with log corrections;
not extrapolated.

**The strengthened comparison:** n=5's L·gap₁₂ = 3.84 at L=8 falls
below the *entire* asymptotic bracket (by 0.8–1.9), not merely below
the finite-size value 6.53 — "falls below the continuous envelope" now
holds against every fitted asymptotic reading of the n=3 chain.
(Systematic caveat: the ladder sits at p=0.30, on the edge of the
deposited p_c⁽³⁾ = 0.305(3) bracket; the CFT consistency supports the
critical reading at these sizes.)

## 6. The v33 proposal — corrected per the author's call; no new
## version

**Author's call (2026-10-12):** correct the Tier-2 sentence; **no new
manuscript version is needed** — v32 remains the manuscript of record.
The corrected conditional is already the v32 body's own statement, so
the proposal is withdrawn as a version-triggering edit and retained
here as the corrected record for the round that eventually extends
Table tab:closingrates (e.g., alongside a Tier-1 L=10 result).

**The defect corrected.** The originally proposed sentence closed with
"if the n=5 closing is genuinely exponential, σ_eff(8→10) will hold at
or above ≈ 0.21 (gap₁₂(L=10) ≲ 0.31), and if it is a slowly decaying
power law it will follow the controls' c/L̄ decay toward ≈ 0.21 and
below" — two branches that overlap almost entirely at the fourth size
(0.205 vs 0.213, ~3% apart), presented as a discriminator. That
framing contradicted §4's own point 1 (a single L=10 point at the
threshold is ambiguous) and the manuscript's honest register ("the
current data cannot distinguish these outcomes").

**The appropriate conditional (author-supplied, verbatim):**

> The three-size trend is consistent with first-order, but does not
> yet establish it. If the trend is genuinely first-order, a fourth
> size (L = 10) will show the effective closing rate σ_eff saturating
> at a positive interface tension Σ; if the asymptotic is a
> slowly-decaying power law, σ_eff will continue to decay. The current
> data cannot distinguish these.

**Abstract/body alignment, verified this round (no edit required).**
The v32 abstract (line 90) carries the compressed form — "supports, at
the three-size level, the first-order prediction … a directional
trend, with the registered conditional that completes it: if the
closing is genuinely exponential, a fourth size (L=10) will show the
effective closing rate stabilizing at a positive interface tension,
and if the asymptotic is a slowly decaying power law, that rate will
continue to decay"; the body (line 890) carries the full conditional
with the closing clause "the current data cannot distinguish these
outcomes, and the registered conditional—not a performed
discrimination—is the claim"; the conclusion (line 1773) carries the
same conditional in the summary register ("the separation is
registered as a prediction rather than claimed as performed"). All
three sites state the same claim at the same strength: **aligned**.

**What survives quantitatively** (for the future edit that ships with
a Tier-1 run, not now): the controls' exclusion finding (no positive
interface tension at accessible sizes under the standard finite-size
ansatz — Σ = −0.055 ± 0.012 at n=3 over four intervals, −0.055 ±
0.016 at n=4 over three, the crossover-limit signature); the
extrapolated continuous envelope (L·gap₁₂ → 4.6–5.8 across fit forms,
bracketing 2πx_ε = 5.03 at x_ε = 4/5) lying entirely above the n=5
value 3.84; and the registered readings for the L=10 point (power-law
continuation σ_eff ≈ 0.205 / gap₁₂ ≈ 0.318; flip threshold σ_eff ≳
0.213 / gap₁₂ ≲ 0.313), stated as the completion test of the
conditional — with the fifth size, not the fourth, as the plausible
decision point (the power-law continuation predicts σ_eff(10→12) ≈
0.17; a genuine positive Σ keeps it at its level).

The Table tab:closingrates extension (two new cells) remains available
unchanged:

```
σ_eff, L=8→10   & 0.137 & 0.162 & --- \\   →  n=4 cell filled: 0.162
σ_eff, L=10→12  & 0.109 & ---   & --- \\   →  new row
α_eff, L=8→10   & 1.227 & 1.452 & --- \\
α_eff, L=10→12  & 1.193 & ---   & --- \\
```

## 7. What was deliberately not done

- No manuscript edit (v32 stands; §6 corrected per the author's call
  and withdrawn as a version trigger — no v33 minted; the abstract /
  body / conclusion alignment on the conditional verified unchanged).
- No p_c⁽⁵⁾ extrapolation (v32's plausibility-range label stands).
- No Tier-1/Tier-3 compute (the v21 verdict and design note stand).
- The two new ladder cells are *used deposits*, not new
  eigen-solves — no new claim of computation is made beyond the fits.
