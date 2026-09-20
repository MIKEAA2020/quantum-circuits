# Changelog — Section Q (v15, spinor verification completed)

## Section Q — v15 (the v14 proof-route gap closed)

- **S5/S6 resolved.** The one item the v14 reconstruction left open — the
  spinor factorisation of the diagonal transfer quoted from the deposited
  route — is derived and machine-verified (`scripts/spinor_verify.py`,
  checks V1–V4; `results/spinor_verify.json`, `logs/spinor_verify.log`):
  with $x_k = \sigma^x_k$, $z_k = \sigma^z_k$ (the SML Ising-Clifford
  algebra), $K_1 = \tfrac12\operatorname{arsinh}(1/\sinh 2K_d)$
  (Kramers–Wannier dual), $K_2 = K_d$ and $c = \sqrt{2\sinh 2K_1}$,
  $$E = \sinh^m(2K_d)\,[\cosh K_d\,\tilde Y + \sinh K_d\,z_m\tilde Y z_1],
  \quad \tilde Y = c\,e^{K_1x_m}\prod_{k=m-1}^{1}
  \big[e^{K_d z_kz_{k+1}}\,c\,e^{K_1x_k}\big],$$
  relative residual $\le 6\times10^{-16}$ ($m = 3$–$8$, $d\in\{2,3,5\}$,
  both branches); normalisation exactly $\sinh^m(2K_d)$ (fitted
  $A = \sinh 2K_d$ to 10 digits, $B = 1$).
- **Boundary/end-term identities (V1).** $E = \cosh K_d E_{\rm OBC} +
  \sinh K_d\,\sigma^z_m E_{\rm OBC}\sigma^z_1$ and the analogous $D_h$
  identity (wrap coupling $K_h$), element-wise proof, residual
  $\le 4\times10^{-16}$ — the verified content of "the periodic boundary
  contributes only through the end term".
- **Determinant structure (V3).** $\det\tilde Y = c^{m2^m}$; one flip sector
  of $E$ exactly singular (the $k=\pi$ kernel at the transfer level);
  $|\det E_{\rm OBC,\varepsilon}| = (2\sinh 2K_d)^{m2^{m-2}}$ with equal
  sectors. The deposited square-lattice formula
  $\rho_\varepsilon^2 = 1+\varepsilon(-1)^m(\sinh2K_2/\sinh2K_1)^m$ does not
  hold for this triangular $E$ and is replaced by these verified statements
  (manuscript v15, Remark rem:verification).
- **Manuscript v15** (`versions/manuscript_revised_v15_spinor.tex/.pdf`):
  proof step (a) of the Proposition now states the reproduced factorisation
  with the closed-form parameter map; the final verification paragraph and
  the numerical-verification remark updated; the App. A file list extended.
  v14 kept unmodified (versioning policy: new version files only).
- **Report v4** (`versions/mipt_numerical_report_v4.md`): Sec. 7.3 (new),
  Sec. 7.2 caveat removed, file lists and provenance updated; v3 kept.
- **Ledger v2** (`logs/certificate_sha256_v2.txt`): all v1 entries plus the
  v15 artifacts; v1 kept.
- **Discovery record** (for reproducibility): `scripts/spinor_discover.py`
  (Pauli-string structure of $\log E$ / $\log E_{\rm OBC}$; the OBC string
  count equals the Gaussian counting $m(2m-1)+1$ exactly) and
  `scripts/spinor_gridsearch.py` (the convention/parameter search that
  identified the unique machine-precision match).
- **No numerical result of the manuscript changes**: $p_c = 0.1597(8)$,
  $\nu = 1.24(7)$, $\alpha = 1.55(7)$, the purification locator, the exact
  annealed line, the benchmark, and the enclosures are untouched; v15
  strengthens the proof chain only.
