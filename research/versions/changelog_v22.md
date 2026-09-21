# Changelog v22 — the exact Z̄₃ closure of Λ(2), the marginal-q=4
# log-correction re-read, the tilted-variance profile family, and the
# n=5 L=8 rung

From v21.  All files NEW (never-overwrite honored).  No v21 number is
altered except where this round's audit CORRECTS it — every correction is
itself a result, machine-verified, and listed here.

## R.0 The deposit-integrity repair (the round's first finding)

The shared library `gap_utils.py` (the Weingarten channel W_{p,n} of
Eq. (Wpn) — the common dependency of the deposited v17/v18/v19 script
suites) was MISSING from the repository: the reproduction chain of
research/ v4–v7 was silently broken.  It is reconstructed exactly from
the manuscript's Eq. (Wpn), placed in `scripts/v22-exactZ3-n5L8/` and
copied into the three legacy script directories, and validated by
re-running the deposited batteries unmodified: `n3_annealed_validate_v1`
V1–V6 all PASS (Sec. 9 benchmarks exact at six decimals, Kaufman closed
form to 4e-11) and `n45_annealed_validate_v1` V1–V8 ALL OK (the n=5 pinv
channel, the p=1 closed form 1/14, the pinv property 3.2e-15).

## R.1 The exact Z̄₃ closure of Λ(2) (the user directive #2)

* **The identification is exact.**  The dyadic identity at n=3 requires
  the two-qubit Clifford group to reproduce the Haar twirl at three
  replicas.  Verified: the conjugation-channel average over the 11,520
  phase classes agrees with the Haar twirl to **1.6e-14** (n=2 control
  2.1e-14; n=4 deviates 0.578 — the negative control, the design
  property failing exactly at the replica number where d² ≥ n still
  holds), consistent with Zhu–Kraemer–Gross (qubit Clifford groups are
  unitary 3-designs), +1 bibitem.  So E_ω[2^{-2N_rand}] = Z̄₃ exactly.
* **The exact values** (t = 4L, the trajectory-ladder convention — the
  round's second finding: the production cells run t = 4L, not L/2; the
  ESS numbers 11.7/3.9/1.4 only reconcile at t = 4L):
  Λ(2) = −0.121924 / −0.123857 / −0.124526 at L=8/12/16 (p=0.16);
  −0.169613 / −0.172746 / −0.173901 at p=0.22.  The boundary-vector
  formula on the compressed bond space (c₁ = w̄^nb·1, the trace
  functional ∏d^{2c(τ_b)}, layer-parity invariance to 0.0) reproduces
  the deposited Z̄₂ anchors to 1e-14 — the conventions are validated.
* **The ESS-law exponent is CORRECTED:** Λ(2)−2Λ(1) = 0.0340 / 0.0349 /
  0.0353 (p=0.16; 0.0432/0.0438/0.0443 at p=0.22) — L-independent to
  4%, twice-to-seven-times the trajectory estimates 0.0159/0.0080/0.0049,
  which are biased LOW by the ESS collapse (the exact ESS/B = 2.7e-8 at
  L=8 against the within-sample 2.9e-4; even Ξ₁ is biased: −0.0804 vs
  −0.0780).  The v21 sentence quoting the trajectory exponents is
  superseded in prop:ess; the diagnosis (estimator difficulty, not
  physics) is unchanged and now quantified exactly.
* **Two independent confirmations:** (a) a well-conditioned β=2
  trajectory run at t=L/2 (B=4e6/2.4e6/1.6e6) estimates E[2^{-2N}]
  within 1.95e-3 (0.4σ, ESS(w²)=3.7e4) of the exact Z̄₃; (b) the Λ(1)
  column reproduces the v21 corrected anchors and gap closures
  0.0224/0.0226/0.0227 exactly.
* **The ladder:** λ₁⁽³⁾ by power iteration (dense-validated 1.9e-10):
  lnλ₁/(2L) = −0.124775/−0.125861/−0.126047 (p=0.16),
  −0.173595/−0.175609/−0.176101 (p=0.22); amplitudes A₃ =
  4.3048/10.068/22.5566 (7.6837/27.0572/90.5274) constant to six digits
  for t ≥ L.  L=24 (6¹²=2.2e9 labels) exceeds the 3 GB budget — scoped
  honestly (L=20 too, after two OOM kills).

## R.2 The marginal-q=4 log-correction analysis (directive #1c)

* **A caption error is corrected:** the q=4-Potts amplitude-ratio target
  is x_σ/x_ε = (1/8)/(1/2) = **1/4** — not the Ising 1/8 quoted in
  v18–v21 (which requires x_ε = 1; at q=4, 1/ν = 3/2 so x_ε = 1/2).
* The missing L=8 λ_ε values are RECOMPUTED (p=0.39–0.41; the deposited
  p=0.38 value reproduced to 5.7e-16 first — the v18 "projected ε
  top-up" was never deposited).
* **The drift is convergence, not degradation:** R_L(p*=0.383) =
  0.1315/0.1829/0.2142/0.2378 (L=4..10) converges logarithmically to
  1/4: the two-term marginal form 1/4 − 0.90/lnL + 0.46/ln²L fits with
  residual ≤ 8e-4.  The n=3 control converges cleanly to 1/6 (0.1670 at
  L=10).  The slope exponent rises 1.00→1.38→1.57 through 3/2 with the
  1/lnL correction; gap·L converges to 2πx_σA = 1.256.

## R.3 The tilted-variance (L,T)-uniformity measurement (directive #1b)

The open self-averaging criterion of prop:replica-int is now MEASURED as
a family: exactly enumerated Haar p=1 collision partition functions
(k*=−1) over L=3–6 × T=2L–8L (6000 circuits/cell) plus fresh
well-conditioned Clifford disorder trajectories at t=L/2.  Part A
(Haar): the profile is flat and (L,T)-uniform — ρ = 1.02±0.03 across
the whole grid, v(0)/T T-independent within each L; Part B (Clifford
disorder): ρ ≈ 0.885 at L=8 (the v21 sub-Gaussian reading, now
confirmed on well-conditioned data), drifting lower with L.  The
t=4L production npz CANNOT carry this measurement (tilted ESS = 1 — the
same estimator difficulty as the β=2 moment); the stale within-sample
profiles are flagged in the JSON.

## R.4 The n=5 L=8 rung (directive #1a)

The full space (S₅)⁴ = 2.07e8 defeats iteration (memory + ~10 min per
ring matvec), so the rung is computed by the SYMMETRY-REDUCED DENSE
BLOCK: the mom0∩triv.triv sector = the orbits of (S₅×S₅)⋊Z₄, assembled
exactly (canonical forms = min over conjugators × shifts; the block
elements √(n_α/n_β)·Σ_{τ∈O_β}M[rep_α,τ] by chunked segment sums).
Validation: the deposited n=5 L=4 triv3 rows reproduced to 1.6e-14; the
L=6 blocks against fresh unrestricted Arnoldi.  [The p-grid run status
is recorded in v22_n5_L8_rung.json; the manuscript rung paragraph is
injected iff the JSON exists.]

## R.5 Files

* `manuscript_revised_v22_exactZ3.tex/.pdf` (38 pp, tectonic, compiled
  clean; content verified via pypdf — the new remark/proposition/table,
  the q=4 corrections, the Discussion/abstract/keywords/roadmap/app:files
  alignment, +1 bibitem ZhuKraemerGross2016).
* `supplement_v5.tex/.pdf` (11 pp): the new S7 subsection sm:v22closure
  (the gap_utils reconstruction + battery, the design test, the Z̄₃
  derivation and cells, the β=2 cross-check, the q=4 fits, the
  tilted-variance family, the block route) + the ledger-v9 note.
* Scripts (all in scripts/v22-exactZ3-n5L8/): gap_utils.py (the
  reconstruction; copies in the three legacy dirs), v22_clifford_3design_v1.py,
  v22_z3_exact_v1.py, v22_traj_beta2_v1.py, v22_n4_eps_topup_v1.py,
  v22_q4_logcorr_v1.py, v22_tiltvar_uniform_v1.py, v22_n5_L8_block_v1.py,
  patch_v22_exactZ3.py, patch_v22_supplement.py, run_chain.sh.
* Results (results/v22-exactZ3-n5L8/): v22_clifford_3design.json,
  v22_z3_validate.json, v22_z3_exact.json, v22_z3_ladder.json,
  v22_traj_beta2.json, v22_n4_eps_topup.json, v22_q4_logcorr.json,
  v22_tiltvar_haar_p1.json, v22_tiltvar_clifford.json,
  v22_n5_L8_rung.json (iff the run completed).
* Companions: this changelog, README_v22_exactZ3.md,
  mipt_numerical_report_v10.md, certificate_sha256_v9.txt.
* Web explorer (both copies, live + repo, byte-identical): the exact
  Λ(2)-closure card, the ESS-card correction (exact vs struck-through
  trajectory exponents), the replica-section q=4 re-read, the version
  trail → v22, the hero clause — see the worklog (Task 2-a).
