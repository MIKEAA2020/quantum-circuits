# v21 — the Clifford record-count closure

This round integrates the parallel v16_scgf theorem-closure line into
the canonical chain (v16_recovered → … → v20), with the framing
corrected to the paper's own terminology, and delegates two proofs plus
the verification appendix to Supplement v4.

## 1. What the parallel line had, and what it actually is

The parallel manuscript (`manuscript_revised_v16_scgf.tex`, preserved
verbatim) closed four theorem-level items under the name "quenched
SCGF".  The v20 audit of this round establishes what that object is in
this paper's language:

| parallel-line name | v21 identity |
|---|---|
| "quenched record SCGF" Ξ_L(β) | the **disorder-direction SCGF** Λ_L(β) = (2Lt)^{-1} ln E_ω[2^{-βN_rand}] — the annealed record moment at fractional order q=1+β (Def. 3, Sec. IV.F) |
| "freezing realization" (ESS collapse) | **estimator difficulty**: the exact law ESS/B = exp[−2Lt(Λ(2)−2Λ(1))] (Prop. ess); consistent with Theorem no-freeze (the degenerate zero-variance case), the finite-size shadow of Theorem rem's extremal-domination mechanism |
| "disorder–replica interchange" | absorbed into **Prop. replica-int**: the measured gap g is the r=1 interpolation remainder; sub-Gaussian profile (13% cumulant overshoot) |
| "Born-average hardness" | the **complexity trichotomy** remark (Gottesman–Knill / 2-design / Haar average-case), complementing the worst-case PostBQP completeness |

The keystone is Remark rem:clifford's mechanism (the unsigned
stabilizer group is branch-independent): the trajectory direction is
trivial, every integer disorder moment is an annealed replica partition
function E_ω[2^{(1-n)N_rand}] = Z̄_n, and the disorder LDP is the
nontrivial content — Λ_L is its scaled cumulant generating function.

## 2. Headline results (all machine-verified in the workspace)

- **Exact β=1 anchors**: Λ_L(1) = (2Lt)^{-1} ln Z̄_2(t) — the transfer
  matrix, for every (L,p,t); Z̄_2(t) = A(L)λ₁^t with A(L) =
  2.4512/4.2354/7.2288 (L=8/12/16, p=0.16) subexponential in t
  (constant to 6 digits for t ≳ 3L); the closed-form Houtappel limit
  Λ(1) → ½(log W₀ + f_H) = **−0.08101 nats/site** (p=0.16; −0.11082 at
  p=0.22).
- **Self-averaging verified**: Var_ω(N_rand)/(2Lt) = 0.104–0.106
  (p=0.16) and 0.124–0.125 (p=0.22), L-independent for L=8–24 — the
  measurable criterion of Prop. replica-int, directly verified.
- **The annealed–quenched record gap persists**: g = Λ(1)+log2·x̄ =
  0.0224/0.0226/0.0227 at L=8/12/16 (exact anchors), ≈0.0229 at L=24
  (amplitude-corrected), ≈0.027 at p=0.22 — **0.0226(2) nats/site,
  L-independent**; the record analogue of the p_c^{(2)}-vs-p_c
  separation.  (Two data-entry slips of the parallel line corrected:
  the L=16 anchor and the summary value; see changelog R.1.)
- **The ESS law**: ESS/B = exp[−2Lt(Λ(2)−2Λ(1))], exponents
  0.0159/0.0080/0.0049 nats/site (L=8/12/16), ESS 11.7/3.9/1.4/1.0 —
  any fixed budget fails exponentially; Λ(2) is exactly Z̄₃ (the v17
  object).
- **Conventions fixed**: the deposited tilt chain runs at t = L/2
  periods (the "t=4L" reading was a mis-transcription; the calibration
  table is Supplement S7); the deposited L=12 quenched entropy 2.394(5)
  is flagged as a provenance exception (not reproduced at either
  convention; nothing depends on it).

## 3. The audit answers (this round's remit)

1. *Simulation/web*: yes — both web-explorer copies now carry the
   replica-ladder (v19/v20) and the record-SCGF sections, the latter
   reframed to this round's statements with the corrected ladder; QA
   green (0 console errors, mobile 390px clean).
2. *Title/keywords/abstract/sections/supplementary*: audited against
   v21 — abstract clause, keyword, intro roadmap, Discussion
   parenthesis, app:files list, [SM] promise all updated; title
   unchanged (still covers both pillars).
3. *Delegation*: Theorem rem's proof and Prop. SMC's proof moved to
   Supplement S5/S6; the verification appendix → S7; App. B assessed
   and deliberately kept (see changelog R.4).
4. *Supplement completeness*: v4 now covers the certificates (S1–S4),
   the two delegated proofs (S5–S6), and the record-count runs (S7)
   with hashes and reproduction commands — matching the updated [SM]
   promise exactly.

## 4. Files

`manuscript_revised_v21_clifford.tex/.pdf` (36 pp) ·
`supplement_v4.tex/.pdf` (10 pp) · `changelog_v21.md` ·
`mipt_numerical_report_v9.md` · `certificate_sha256_v8.txt` · the
parallel-line artifacts preserved (`manuscript_revised_v16_scgf.*`,
`changelog_v16_scgf.md`, `mipt_numerical_report_v5_scgf.md`,
`certificate_sha256_v3_scgf.txt`).
