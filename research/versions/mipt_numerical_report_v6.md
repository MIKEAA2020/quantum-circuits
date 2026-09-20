# Numerical report v6 — the annealed three-replica critical point

New in v6 (only addition to v5; every earlier section stands):
Sec. 11 — the sector-resolved spectra of the n=3 compressed operator and the
annealed three-replica transition.

## 11. The annealed three-replica critical point (n=3, d=2)

**Object.** C_comp^{(3)} = M1 M2 on the 6^{L/2} bond-label space, bond channel
Eq. (Wpn) at D = d^2 = 4, Gram similarity eigs(C) = sigma(S)^2 with
S = G^{1/2} M1 G^{-1/2} (Theorem general-n(i)).

**Method.**
- L = 4,6,8,10: dense S (N <= 7776), sector-restricted eigsh with the deposited
  S_3 group-algebra colour idempotents; deflation for the second triv value.
- L = 12: the exact momentum-zero block (dim 7826) assembled from product rows of
  M1, M2 over shift orbits; sector-restricted Lanczos (k=4 in the triv sector —
  k=2 provably returns a spurious Ritz value; the bug was caught against the
  global top-k list and fixed).
- All three scaling gaps live at momentum k = 0 at every (L, p) tested;
  lambda_sigma is always the std.std,i+ (4-fold) leading value.

**Validation (all pass, scripts deposited).**
- V1: n=3 spectra == the deposited gap_proofs Sec. 9 benchmarks EXACTLY
  (L=4,6,8; d=2,3; 0.00e+00 on all 5 cases).
- V2: eigs(M1 M2) == sigma(S)^2 to 1.7e-16.
- V3: n=2 dense == the Kaufman closed form (1e-11..1e-15); n=2 crossing control
  (dense L=4..10): 0.19907/0.22261/0.22881 -> 0.23381 as in the deposited table.
- V4: momentum-block union == the full spectrum to 1.7e-16 (n=3, nb=3).
- V5: colour sectors reproduce the deposited 1+4+1 pattern (0.836807/0.834268/0.831750).
- V6: product rows == dense rows exactly.
- CONTROL (new, the strongest): the same momentum-block code at n=2, L=16..32,
  fine grid (45 points, step 5e-4) reproduces the deposited benchmark crossings:
  0.23319/0.23347/0.23361/0.23368 vs deposited 0.23319/0.23348/0.23361/0.23368
  (max diff 1e-5) — at sizes beyond the n=3 chain.

**Results (d=2, exact eigenvalues, no statistical error).**
- Crossings of X_L = L log(l1/l_sigma), consecutive sizes:
  (4,6): 0.27114  (6,8): 0.29678  (8,10): 0.30244  (10,12): 0.30403
  Extrapolations (power-law b in 0.5..8: 0.30525; geometric deceleration: 0.30465;
  Aitken: 0.30341; 3-param power fit: 0.3070(9)) — adopted p_c^{(3)} = 0.305(3).
- Continuous: gap at crossings 0.1265 -> 0.1176 -> 0.1001 -> 0.0854 (L=6..12),
  xi/L = 1/1.32, 1/1.06, 1/1.00, 1/0.98; no two-phase avoided crossing in the
  colour-trivial sector at any size.
- Amplitude ratio log(l1/l_sig)/log(l1/l_eps) at the crossings:
  0.107 -> 0.144 -> 0.161 -> 0.171 -> 1/6 (three-state Potts x_sig/x_eps;
  Ising 1/8 excluded at L=10). Absolute check at L=12: L log(l1/l_eps) = 6.0
  vs 2 pi x_eps = 5.03 under the same lattice-amplitude factor that rescales
  the sigma gap 0.838 -> 1.03 (a 2-sigma composite would give ratio 1/2).
- Slope exponent: dX_L/dp at p_c ~ L^{1.15} => 1/nu_eff = 1.15(10)
  (Potts 6/5 = 1.2; Ising 1; first order 2).
- Growth-rate chain l1^{1/L} monotone in L at every p; Richardson-extrapolated
  l_inf^{(3)}(p): 0.926 (p=0.05) ... 0.613 (p=0.30) ... 0.313 (p=0.75),
  consistent with a single nonanalytic point at p_c^{(3)}.
- lambda_1 simplicity: triv > std > sgn splitting at every (L, p) tested
  (165/165) — extends the simplicity observation below the entrywise-positivity
  threshold (p >= 0.31 at L=4, 0.43 at L=6 in the manuscript's remark).

**Interpretation.** All three diagnostics land on the three-state-Potts values
(ratio 1/6, 1/nu 6/5, continuous with gap ~ 1/L); the operator content matches
(spin in std (2-dim) = the Potts spin; energy in triv; sigma multiplet 4-fold =
(dim std)^2). Conjecture: the annealed n-replica points of this circuit follow
q=n-state Potts universality (n=2 exact Ising = q=2; n=3 numerics q=3);
q > 4 then predicts first order for n >= 5 — falsifiable with the present
machinery at n=4 (bond space 24^{L/2}, reachable to L=6).
The replica trend quantifies the annealed-quenched distinction:
p_c^{(2)} = 0.233810 < p_c^{(3)} = 0.305(3) vs quenched 0.1597(8) — the annealed
points move AWAY from the quenched transition as n grows.

**Scope.** Exact finite-size data, systematic (not statistical) extrapolation,
L <= 12, d=2; universality from three finite-size diagnostics, not a proof.

**Files.** scripts: n3_annealed_lib.py, n3_annealed_validate_v1.py,
n3_annealed_runall_v1.py, n3_annealed_analysis_v1.py (workspace root);
results: mipt_results/n3_annealed_{validation,scan_dense,scan_block12,final}.json,
mipt_results/n2_control_{blocks,crossings}.json; logs: logs/n3_annealed_*.log;
manuscript: versions/manuscript_revised_v17_annealed-n3.tex/.pdf (new Sec.
sec:n3annealed + Table tab:n3annealed + open-problems rewrite), built by
versions/patch_v17_annealed.py from v16 (anchors asserted).

## 11a. Addendum — exploratory n=4 datum (v17a)
The same momentum-block machinery at n=4 (bond dim 24, Weingarten D=4>=n
invertible), L=4,6, with the second momentum-zero eigenvalue as the sigma proxy
(colour resolution of S_4 not implemented): the (4,6) crossing of
X_L = L log(l1/l2) lies at 0.35726 (14-point grid, step 0.025).  With the n=3
small-L bias ((4,6) crossing 0.27114 = p_c - 0.034), this indicates
p_c^{(4)} ~ 0.36-0.39 — the replica trend continues:
0.233810 (n=2) < 0.305(3) (n=3) < ~0.37 (n=4) vs quenched 0.1597(8).
Files: mipt_results/n4_annealed_exploratory.json.  Manuscript v17a records the
datum (versions/manuscript_revised_v17a_annealed-n3.tex/.pdf).
