# Numerical report — v4

**Manuscript:** `versions/manuscript_revised_v15_spinor.tex` (v15; v14 kept
unmodified). This report supersedes v3; everything in v3 stands except
Sec. 7.2's honest-gap paragraph, which is now resolved, and the file lists.
The changed/added material is rewritten in full below.

**Status box (unchanged from v3):** I3 locator $p_c = 0.1597(8)$, $\nu =
1.24(7)$, $\alpha = 1.55(7)$; purification locator $p_c^{\rm purif} =
0.1601$–$0.1604$, $\nu^{\rm purif} = 1.25(2)_{\rm stat}(6)_{\rm sys}$; exact
annealed line $p_c^{(2)}(2) = 0.233810$, $p_c^{(2)}(3) = 0.459688$,
$p_c^{(2)}(5) = 0.679004$.

## 7. Exact certificates (v4: 7.2 gap closed; 7.3 NEW)

### 7.1 N3 Collatz–Wielandt enclosures
Unchanged from v3 (five exact-rational two-sided enclosures of
$\lambda_1(\Ccomp)$, relative widths $2.2$–$7.3\times10^{-15}$, reproduced in
`scripts/mipt_audit3_cw_exact.py`).

### 7.2 Closed-form spectrum verification
As in v3 (`mipt_kaufman_lib.py` + `mipt_audit3_gauss_proof.py`: 108-config
dense-vs-closed agreement $\le 10^{-10}$ in $\ln\lambda$; kernel counts;
commutators; benchmark; Houtappel; $p_{\rm eff}$), **with the v3 caveat
removed**: the spinor factorisation lemma of the deposited proof route *has
now been re-derived and verified* — see 7.3.

### 7.3 The spinor factorisation (NEW in v4; closes the v3 gap)
`scripts/spinor_verify.py` (V1–V4; `logs/spinor_verify.log`,
`results/spinor_verify.json`).  The deposited identity

$$E = \cosh K_2\,\tilde Y + \sinh K_2\,z_m \tilde Y z_1,\qquad
\tilde Y = c\,e^{K_1 x_m} U_{m-1}\cdots U_1,\quad
U_k = e^{K_2 z_k z_{k+1}}\,c\,e^{K_1 x_k},\quad c = \sqrt{2\sinh 2K_1}$$

holds **exactly** for our diagonal transfer $E$ with the parameter map
recovered by structural discovery (Pauli-string decomposition + grid search
over conventions and Kramers–Wannier duals):

- $x_k = \sigma^x_k$, $z_k = \sigma^z_k$ — *plain Paulis*, the
  Schultz–Mattis–Lieb Ising-Clifford algebra (not string Majoranas; the v3
  parameter search tried string conventions and failed for that reason);
- $K_2 = K_d$, and $K_1 = \tfrac12 \operatorname{arsinh}(1/\sinh 2K_d)$ — the
  Kramers–Wannier dual ($\sinh 2K_1 \sinh 2K_d = 1$);
- overall normalisation $N = \sinh^m(2K_d)$ exactly:
  $E = \sinh^m(2K_d)\,[\cosh K_d\,\tilde Y + \sinh K_d\,z_m\tilde Y z_1]$.

**Verification (all PASS, machine precision):**
- V2/V2b: relative residual $\le 6\times10^{-16}$ over $m = 3$–$8$,
  $d \in \{2, 3, 5\}$, $p \in \{0.05, 0.16, 0.40, 0.60\}_{d=2} \cup
  \{0.20, 0.60\}_{d=3} \cup \{0.45\}_{d=5}$ — both branches of the weight
  trajectory; fitted $A^mB$ gives $A = \sinh 2K_d$ to 10 digits and
  $B = 1.0000000000$.
- V1: the end-term/boundary structure holds separately and exactly for $E$
  (wrap coupling $K_d$) and for $D_h$ (wrap coupling $K_h$):
  $E = \cosh K_d\,E_{\rm OBC} + \sinh K_d\,\sigma^z_m E_{\rm OBC}\sigma^z_1$
  (residual $\le 4\times10^{-16}$, $m = 3$–$7$, four $(d,p)$).  Element-wise
  proof: $(\sigma^z_m M \sigma^z_1)_{s's} = s'_m M_{s's} s_1$, so the bracket
  multiplies by $\cosh K + s'_m s_1 \sinh K = e^{K s'_m s_1}$, the wrap bond.
- V4: $D_{h,\rm OBC} = \prod_{k<m} e^{K_h \sigma^z_k\sigma^z_{k+1}}$ exactly
  (commuting bond exponentials).
- V3 (determinant structure, replacing the deposited square-lattice formula):
  every factor of $\tilde Y$ has unit determinant, so $\det\tilde Y =
  c^{m2^m}$; one flip sector of $E$ is *exactly singular* (the $k=\pi$
  kernel at the transfer level); the two flip sectors of $E_{\rm OBC}$ have
  *equal* determinants with the closed form
  $|\det E_{\rm OBC,\varepsilon}| = (2\sinh 2K_d)^{m2^{m-2}}$ (per-site scale
  $2\sinh 2K_d$, $m$-independent; verified $m = 3$–$6$, three $(d,p)$).
  The deposited formula $\rho_\varepsilon^2 = 1 + \varepsilon(-1)^m
  (\sinh 2K_2/\sinh 2K_1)^m$ (Kaufman's square-lattice determinant) does not
  hold for this triangular $E$ — it was evidently mis-transcribed in the
  deposited route; the verified statements above replace it in the manuscript
  (v15 states them after Eq. spinor and in the verification remark).

**Discovery record** (kept for reproducibility): `scripts/spinor_discover.py`
(Pauli-string content of $\log E$/$\log E_{\rm OBC}$/$\log D_h$; the OBC
string count is exactly $m(2m-1)+1$ — the Gaussian counting) and
`scripts/spinor_gridsearch.py` (conventions × parameter maps × targets; the
winning combination above is the unique machine-precision match).

## 8. Purification locator (unchanged from v3)
`scripts/mipt_purif_analysis.py`: $\tau = 1$ collapse $0.16009/1.2486$
($\chi^2 = 18.3/18$); $\tau = 0.5$: $0.16039/1.2506$; frozen-$\nu$
$\Delta\chi^2$ and bootstrap as in v3; all deposited numbers reproduced.

## 9. Files (v4)
`scripts/`: v3 list **plus** `spinor_verify.py` (the factorisation,
boundary, determinant verification), `spinor_discover.py`,
`spinor_gridsearch.py` (the discovery record).
`results/`: v3 list plus `spinor_verify.json`.
`logs/`: v3 list plus `spinor_verify.log`.
`versions/`: `manuscript_revised_v15_spinor.tex` / `.pdf` (v14 kept),
`mipt_numerical_report_v4.md` (v3 kept), `changelog_v15.md` (§Q; the v14
changelog kept), `certificate_sha256_v2.txt` (ledger v2; v1 kept).

## 10. Reconstruction provenance (v4 update)
As in v3, plus: the spinor factorisation — the one item the v3 reconstruction
could not reproduce — is now derived and verified from first principles
(Sec. 7.3), completing the proof-to-code chain of the manuscript's
Proposition: dense diagonalisation (S2), exact enclosures (S8), and now the
operator identity itself (V1–V4). The only deposited claims not reproduced
verbatim are (i) the raw I3 dataset (lost; rows quoted from the deposit, as
in v3) and (ii) the square-lattice Kaufman determinant formula, which is
replaced by the verified triangular-$E$ determinant structure of Sec. 7.3.
