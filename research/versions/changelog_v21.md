# Changelog v21 — the Clifford record-count closure (the parallel v16_scgf
# line integrated with corrected framing; two proofs delegated to the
# supplement; supplement v4)

From v20.  All files NEW (never-overwrite honored).  No scientific
content of v20 is altered: every v20 number is reproduced unchanged.
This round integrates the record-SCGF theorem-closure line that ran in
parallel to v16_recovered→v20 (its manuscript is preserved verbatim as
`manuscript_revised_v16_scgf.tex`; its scripts and results were merged
in git as the local half of the parallel-lines merge), **with the
framing corrected to this paper's terminology** — the correction is
itself a scientific result of the audit:

## R.1 The framing correction (the important part)

The parallel line called its object "the quenched SCGF"
Ξ_L(β) = ln E_Born[2^{-βX_R}]/(2Lt).  In this paper's language it is
**the disorder-direction SCGF** Λ_L(β) (Def. 3 of the new Sec. IV.F):
the annealed record moment at fractional order q = 1+β, i.e. the
disorder average *inside* the logarithm.  The reconciliation rests on
Remark rem:clifford (v20): for a fixed Clifford realization ω the
unsigned stabilizer group evolves identically on every branch, so
P_ω(R) = 2^{-N_rand(ω)} for every positive-probability record, the
surprisal is ω-measurable, ψ_{L,ω} is exactly affine — **the trajectory
direction is trivial and Theorem no-freeze applies in its degenerate
zero-variance case**.  All nontrivial record statistics live in the
disorder direction, where the integer moments are exactly the annealed
replica partition functions: E_ω[2^{(1-n)N_rand}] = Z̄_n (n=2 is the
transfer-matrix cross-check of rem:clifford; n=3 is the v17 object).
Consequences applied throughout the new section:

- The parallel line's "freezing realization" (ESS collapse) is
  **reframed as estimator difficulty** in the sense of the SMC
  contract's clone-collapse clause — an exact law
  ESS/B = exp[−2Lt(Λ(2)−2Λ(1))] now carries it (Prop. ess), with no
  nonanalyticity of any τ and no contradiction with Theorem no-freeze;
  what it measures is extremal domination of the annealed endpoint by
  an atypical minority of circuits (tilted density 0.097 vs typical
  0.145 at L=8), the finite-size shadow of Theorem rem's mechanism.
- The parallel line's "disorder–replica interchange" proposition is
  **absorbed into Proposition replica-int**: the measured Jensen gap
  g = 0.0226(2) nats/site is exactly the r=1 interpolation remainder
  ∫₀¹(1−s)Var_s ds of Eq. (repint); the leading cumulant overshoots by
  13% (a decaying, sub-Gaussian tilted-variance profile) — the first
  measured data on the profile whose (L,T)-uniformity the Discussion
  flags as the open criterion.
- Two data-entry slips in the parallel line's ladder are corrected:
  the L=16 β=1 anchor is the finite-t value −0.079901 (not the λ₁
  asymptote −0.080867), giving gap 0.0227 (not 0.0217); the summary gap
  is 0.0226(2) (not 0.0222(5)); L=24 uses the amplitude-corrected
  anchor −0.080325 (A(24)≈21.4 extrapolated), gap ≈0.0229.

## R.2 The new section (Sec. IV.F, `sec:clifforddisorder`)

`manuscript_revised_v21_clifford.tex` (36 pp): the dichotomy paragraph
+ Eq. (dyadicmoments) + Def. (disorder SCGF) + Prop. cliffscgf (exact
β=1 anchors with A(L)=2.4512/4.2354/7.2288 subexponential in t; the
Houtappel-closed thermodynamic limit ½(log W₀+f_H) = −0.08101
nats/site at p=0.16, −0.11082 at p=0.22; the quenched density ladder
x̄→0.1489 bits/site; Var/(2Lt) = 0.104–0.106 L-independent — the
measurable self-averaging criterion, verified; two-term cumulant <1%)
+ Prop. gap (finite-L derivative exact; the r=1 interpolation
remainder 0.0224/0.0226/0.0227 at L=8/12/16, ≈0.0229 at L=24,
≈0.027 at p=0.22 — L-independent, the record analogue of the
p_c^{(2)}-vs-p_c separation; sub-Gaussian 13%) + Prop. ess (the ESS
law; exponents 0.0159/0.0080/0.0049 nats/site at L=8/12/16; ESS
11.7/3.9/1.4/1.0; Λ(2)=Z̄₃ noted) + Remark trichotomy (Gottesman–Knill
/ exact 2-design / Haar average-case, +3 bibitems) + the t=L/2
convention-fix sentence + the L=12 provenance caveat.

## R.3 Alignment edits (the audit answers)

- Abstract: "note that Clifford circuits have trivial record
  statistics" → "trajectory-trivial … while their disorder statistics
  are not trivial — we measure the Clifford record-count SCGF with
  exact β=1 anchors, an L-independent self-averaging variance of 0.105
  per site, and an L-independent annealed–quenched gap of 0.0226(2)
  nats per site".  Keywords + "self-averaging".  Intro roadmap +
  "…and closes the Clifford record-count disorder statistics with exact
  anchors, self-averaging, and the annealed–quenched gap".  Discussion
  open-problems: the tilted-variance-profile parenthesis.  Title:
  unchanged (the new material lives under both declared pillars).
- app:files: the record-count suite (mipt_scgf_exact.py,
  mipt_born_scgf.py, scgf_exact.json, scgf_exact_addendum.json,
  scgf_born.json, the npz arrays) added to the deposit list.

## R.4 Delegation to the supplement (never the reverse)

- Theorem rem's proof (the Borel–Cantelli/TIS-concentration/truncation
  estimates, 30 lines) → Supplement Sec. S5, restated with S-numbered
  equations; main text keeps the statement + a scope summary pointer.
- Proposition SMC's proof (the Del Moral induction) → Supplement
  Sec. S6, restated with the estimator definition and Eqs. (S-FK),
  (S-SMC), (S-RN).
- The parallel line's verification appendix (the 3^L evolution, the
  deposit calibration table, the anchors, the production ladder, the
  estimator/error model, reproduction commands) → Supplement Sec. S7
  (new; would otherwise have bloated the main text).
- Assessment for a future round: App. B (the FSS benchmark) is the
  remaining main-text delegation candidate; it is kept in main because
  the Scope and Discussion benchmark statements anchor to it directly.

## R.5 Supplement v4

`supplement_v4.tex` (10 pp): scope sentence extended; Secs. S5/S6/S7 as
above; the S4 ledger note records certificate_sha256_v8.txt (this
round) and the parallel-line ledger certificate_sha256_v3_scgf.txt; a
bibliography (BLM2013, Rockafellar1970, DemboZeitouni1998,
DelMoral2004) is added for the proofs.

## R.6 Files

- `manuscript_revised_v21_clifford.tex/.pdf` (36 pp, tectonic,
  revtex4-2; compiled and content-verified via pypdf: all new
  propositions, the ESS law, the trichotomy, the caveat render).
- `supplement_v4.tex/.pdf` (10 pp, tectonic; S5 p.3, S7 p.6 verified).
- `changelog_v21.md` (this file), `README_v21_clifford.md`,
  `mipt_numerical_report_v9.md` (Sec. 15: the runs behind Sec. IV.F,
  the framing-correction record, the corrected ladder),
  `certificate_sha256_v8.txt` (ledger v8: the round files + the
  record-count suite).
- Web explorer (both copies, live + repo): the record-scgf section
  reframed to match this round (dichotomy, ESS law, corrected ladder)
  and the replica-ladder section merged in — see the worklog.
