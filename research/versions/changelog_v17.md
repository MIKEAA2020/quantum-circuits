# Changelog — Section S (v17): the annealed three-replica critical point

Base: v16 (manuscript_revised_v16_recovered.tex, the recovered-data version).
New version files only; nothing overwritten.

## S.1  What was asked
The user asked for (1) remaining points from the audits / joint assessments
worth addressing and (2) highly-merited, non-decorative, novel computational
work.  Audit status at v16: audit3_joint_assessment v2 (the 13-item v14 plan)
fully closed; audit_adjudication (four audits) closed in v5-v13; the REM
adjudication closed (v11); gap_proofs P1-P3 closed (v12/v13); the qwen
"physics gap open" Theorems 1-2 were refuted by qwen_open_verification.md
(Thm 1 Step 3 false; all-L sharpness settled negatively at L=12).  The
manuscript's own open-problems paragraph then carried the item: "scaling-quality
spectral data for the n>=3 operators do not yet exist" — the highest-merit
remaining computation.  This round executes it.

## S.2  What was computed
The annealed THREE-REPLICA transition of the monitored Haar circuit (d=2):
sector-resolved exact spectra of C_comp^{(3)} at L = 4,6,8,10 (dense) and
L = 12 (exact momentum-zero block, dim 7826, product-row construction).
- p_c^{(3)} = 0.305(3): crossings of X_L = L log(l1/l_sigma) for consecutive
  sizes 0.27114 / 0.29678 / 0.30244 / 0.30403, four extrapolation methods.
- Continuous (not first order): the gap at the crossings decays
  0.126 -> 0.085 over L = 6 -> 12 (xi/L -> 0.98); no two-phase avoided crossing.
- Three-state Potts universality: amplitude ratio at the crossings
  0.107 -> 0.144 -> 0.161 -> 0.171 -> 1/6 (x_sigma/x_epsilon; the Ising 1/8 of
  the n=2 row is excluded at L=10); absolute epsilon-sector check
  L log(l1/l_eps) = 6.0 vs 2 pi x_eps = 5.03 under the same lattice-amplitude
  factor (a 2-sigma composite would give 1/2); slope exponent 1/nu_eff = 1.15(10)
  (Potts 6/5; Ising 1; first order 2); the sigma sector is std (x) std (4-fold,
  (dim std)^2) — the Potts spin representation.
- Growth-rate chain l1^{1/L} and the Richardson-extrapolated l_inf^{(3)}(p)
  (0.926 at p=0.05 to 0.313 at p=0.75), consistent with one nonanalytic point.
- lambda_1 simplicity observation: triv > std > sgn at every (L, p) tested
  (165/165) — extends the manuscript's simplicity remark below the
  entrywise-positivity threshold.
- The replica trend: p_c^{(2)} = 0.233810 < p_c^{(3)} = 0.305(3) vs quenched
  0.1597(8): the annealed points move away from the quenched transition.
- Conjecture recorded: annealed n-replica points follow q = n-state Potts
  universality (n=2 exact, n=3 numerics); q > 4 predicts first order for
  n >= 5 — falsifiable at n=4 with the present machinery.

## S.3  Validation
V1 spectra == deposited Sec. 9 benchmarks (0.00e+00, five cases); V2 Gram
similarity 1.7e-16; V3 n=2 dense == Kaufman closed form (1e-11..1e-15) with the
crossing control reproducing the deposited convergence pattern; V4
momentum-block union == full spectrum (1.7e-16); V5 colour sectors == deposited
1+4+1 pattern; V6 product rows exact; NEW CONTROL: the same momentum-block code
at n=2, L = 16..32 reproduces the deposited benchmark crossings
0.23319/0.23347/0.23361/0.23368 to 1e-5 (the (28,32) pair to 0.00000) — at
sizes beyond the n=3 chain.  Two implementation bugs were caught and fixed by
this validation chain: a lambda_1-squaring deflation error (ghost eigenvalue
lambda_1 (1 - lambda_1), caught against the closed form) and an ARPACK k=2
spurious second Ritz value (caught against the global top-k list; k=4 used).

## S.4  Files
Scripts (workspace root): n3_annealed_lib.py (library: W tensor, dense
S-construction, colour projectors from the deposited idempotents, momentum
blocks, product rows), n3_annealed_validate_v1.py (V1-V6),
n3_annealed_runall_v1.py (dense scan + block12 + the n=2 control, daemon-safe),
n3_annealed_analysis_v1.py (crossings/extrapolations/ratio/slope/growth).
Results: mipt_results/n3_annealed_validation.json, n3_annealed_scan_dense.json,
n3_annealed_scan_block12.json, n3_annealed_final.json, n2_control_blocks.json,
n2_control_crossings.json.  Logs: logs/n3_annealed_*.log.
Manuscript: versions/patch_v17_annealed.py (anchors asserted) ->
versions/manuscript_revised_v17_annealed-n3.tex/.pdf (31 pp; new subsection
sec:n3annealed + Table tab:n3annealed + abstract clause + open-problems rewrite
+ bibitem Wu1982).  Report: versions/mipt_numerical_report_v6.md (Sec. 11).

## S.5  Addendum (v17a): the exploratory n=4 datum
The same machinery run at n=4 (L=4,6; bond dim 24; sigma proxy = the second
momentum-zero eigenvalue): the (4,6) crossing is 0.35726, i.e.
p_c^{(4)} ~ 0.36-0.39 after the n=3-calibrated small-L bias — the replica
trend continues away from the quenched point, as the q=n-Potts conjecture and
the annealed-quenched distinction require.  New files: v17a manuscript
(versions/manuscript_revised_v17a_annealed-n3.tex/.pdf), report Sec. 11a,
mipt_results/n4_annealed_exploratory.json.
