# Changelog

## Section P — v14 (audit round 3 implemented)

- **1b (D2 recenter).** Headline p_c 0.1595(10) -> 0.1597(8) (abstract,
  Sec. 5 adopted sentence, Sec. 7 conclusion, the alpha-row caption note;
  cause: corrected tail-safe fits centre at 0.1597-0.1598 and all
  independent estimators lie at/above 0.1597; report v3 Sec. 3.5).
- **E1.** "(Jensen)" removed; the annealed-vs-quenched paragraph rewritten
  with the exact tilt mechanism (p_eff = p + p(1-p) dlog(lambda1)/dp /(2L);
  0.1049/0.1011/0.0920 at p=0.16 for L=8/12/infty; the L=8 40,000-trajectory
  chain, ESS 5935; L=12 exact values only; no annealing<->quenching mapping
  claimed). One mechanism clause added in Sec. 5 (main text).
- **E2.** Exponent paragraph: fixed-set Delta-chi^2 profile (52-334 / 0.2-11
  / 0.1-2.6 / 0-9.9 / 3.0-36.5 / 12.5-89 for nu = 1 / 1.20 / 1.24 / 1.28 /
  4/3 / 1.40; sextic tail-out: Delta-chi^2(nu=1) >= 72); corrections to
  scaling sentence; weighting disclosure (1/N floors, saturated-tail
  exclusion / spline F); slope method as consistency check; GATE-4
  shared-trajectory sentence.
- **E3.** omega -> omega_eff = 1.6(4)-2.5(8) depending on L_min; chi^2
  p-values added (>= 0.2 for L >= 64 windows).
- **E4.** alpha at p_c = 0.1597 (rows shift ~ -0.02, dalpha/dp ~ -110);
  s1 L^{-y} clause (never preferred, |dalpha| < 0.05).
- **E5.** "(sampled as the 720 symplectic actions, under which every recorded
  quantity is invariant)".
- **E6.** Gullans-Huse p_c = 0.1593(5), nu = 1.28(2); c~ = alpha/ln2 note;
  the N2 purification paragraph (independent observable, Eq. purif).
- **E7.** Abstract/conclusion: no numerical change beyond the recenter; the
  "systematic rather than statistical uncertainties" sentence stays.
- **E8.** Report v3 (Secs. 3.4, 3.5, 5.4, 6, 7 rewritten; c_eff label fix;
  Sec. 10 provenance); changelog (this section); ledger updated.
- **E9.** Reproducibility sentence (MT19937 seed0+k contract; bit-exact for
  23 trajectories across L = 16-512).
- **N3.** Appendix A, new subsection "Collatz-Wielandt enclosures of the
  two-replica Perron eigenvalue" (five exact-rational certificates; the
  certified sentence at the benchmark).
- **D6 (Q2 -> (b)).** Proposition (closed-form spectrum) with proof after
  the Houtappel proof + numerical-verification remark; new bibitems
  Kaufman1949, Newell1950, Schultz1964.
- **N2 (Q3 -> yes).** Purification paragraph: independent observable,
  disjoint seeds, mixed initial state; p_c^purif = 0.1601-0.1604,
  nu = 1.25(2); quoted separately.
- **Item 13 (released code).** mipt_fss2_floorN.py: 1/N standard-error
  floors (the legacy 1e-4/1e-6 floors replaced; the second 1e-6 is the
  Nelder-Mead xatol and is intentionally NOT transformed - the bug that
  stopped the previous session); re-run check: the windowed numbers do not
  move (no point with s.e. below either floor enters any window; provable
  no-op on the recovered purification dataset).
- **Table caption.** tab:numerics caption: alpha rows at p_c = 0.1597 with
  the shift note; bootstrap resamples and the 1/N s.e. floor disclosed.
