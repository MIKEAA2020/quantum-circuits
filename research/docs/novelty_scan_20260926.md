# Novelty / Literature Scan — 2026-09-26

Manuscript: `manuscript_revised_v22_exactZ3.tex` — "Exact Replica Mechanics and Born-Record Large Deviations in Monitored Quantum Circuits" (A. Abaee). Context: the n=5 L=8 rung (three-size first-order test) is in progress (grid ~49.5% at scan time).

Method: 10 targeted web searches (z-ai web_search, 2026-09-26; raw results archived in `scripts/litscan/s*.json`, not pushed) + nearest-neighbor triage. Items marked **[to-verify]** need the exact bibliographic record resolved before citation. Search-hit titles/venues are quoted as returned by the search engine.

---

## A. Replica mechanics of monitored circuits (the core line)

Nearest neighbors found:

- Gullans & Huse, "Dynamical purification phase transition induced by quantum measurements" (PRX 2020) [cited: Gullans2020] — the replica-limit/locator lineage the paper's purification locator follows.
- Choi, Bao, Qi, Altman (PRX 2020) [cited: Choi2020] and Bao, Choi, Altman (PRB 2020) [cited: Bao2020] — replica statistical mechanics of monitored circuits; source of the 2-replica Ising identification that the paper converts into a closed-form benchmark.
- Jian et al., monitored Brownian SYK chains [cited: Jian2020] — continuum replica field theory (approximate, not exact spectra).
- Delmonte et al., "Measurement-induced phase transitions in monitored infinite-…" **Phys. Rev. Research 7, 023082 (2025)** — the closest recent replica-numerics line found by this scan (postselection-free replica diagnostics for monitored circuits).
- Suzuki, "Quantum complexity phase transitions in monitored random circuits," **Quantum 9, 1627 (2025)** — complexity-side monitored-circuit transitions.
- Moghaddam et al., "Exponential shortcut to measurement-induced entanglement…," **PRL 131, 020401 (2023)** — rare-event-flavored MIPT numerics.
- "Measurement-induced phase transition in space…," arXiv:2607.12386 (Jul 2026) **[to-verify]** — very recent MIPT characterization work.

**Verdict.** The paper's niche — EXACT finite-n annealed replica transfer operators with proven structure (period map = AA†, real positive semisimple spectrum strictly inside the unit disk, S_n×S_n symmetry, bond-space compression, exact rank over Z[p] with algebraic exceptional points) plus a measured annealed ladder p_c^(2)=0.233810 < p_c^(3)=0.305(3) < p_c^(4)≈0.383 < p_c^(5)≈0.47–0.48 with q=n Potts universality (2: closed-form Ising; 3: continuous q=3; 4: marginal q=4 with measured 1/ln L corrections; 5: first-order two-size test) — is **not occupied** by any hit found. The 2025–2026 replica works are approximate/numerical or continuum; none computes exact finite-n spectra or rank certificates. Differentiation is clean. **Action:** cite Delmonte (2025) and Suzuki (2025) in the intro/related-work to pre-empt "how does this relate to current replica numerics" referee questions; optionally Moghaddam PRL 2023.

## B. n=2 exact Ising benchmark

Houtappel (1950), Kaufman (1949), Bao–Choi–Altman (2020) all already cited. The paper's contribution here (closed form p_c^(2)(d)=(d−θ_c)/(d−1), θ_c=β_d+√(β_d²+1), β_d=(d²−1)/(d²+1); closed free-fermion nonzero spectrum fixing finite-size amplitudes; conversion of the Ising identification into a proof-to-computation benchmark, reproduced to 3×10⁻¹⁵) is exact re-derivation + benchmarking, correctly framed, not a new-universality claim. No action.

## C. q=n Potts identification (rem:whyqn)

- q=3 (continuous): amplitude ratio → 1/6, slope 1.15 — consistent with three-state Potts (Wu 1982 cited).
- q=4 (marginal): Cardy 1986 (cited) is the canonical log-correction reference; additional literature confirms the anomalously slow finite-size convergence at q=4 (Berche et al. 2004 **[to-verify ID]**; Chatelain's conformal-space work; equivalent-neighbor q=4 studies). The paper's two-term marginal fit R=1/4−0.90/ln L+0.46/ln²L (residual ≤8×10⁻⁴ over L=4,6,8,10) is a measurement, not a theory claim — safe as stated.
- q≥5 (first-order): textbook (Wu 1982; Baxter 1982 cited).

**Verdict.** The identification remains empirical, exactly as rem:whyqn states ("no Temperley–Lieb or free-fermion equivalence is exhibited for n≥3"). Keep that scoping sentence; optionally add one modern q=4 log-correction study beyond Cardy1986.

## D. First-order transitions in monitored dynamics (context for n=5)

Found: discontinuous/first-order transitions in driven monitored systems (shaking-driven, arXiv Aug 2026 **[to-verify]**), dissipative first-order transitions (Rossini et al. 2021), first-order localization via imaginary zeros (Tong et al. 2024), and the continuous-measurement-driven first-order entanglement-transition line in 1D hybrid circuits (search hit; exact reference **[to-verify]**). **None concerns the annealed finite-n replica sector of projective monitored circuits.** The paper's n=5 evidence (two-phase gap closing factor 2.12 from L=4→6 vs 1.94 (n=4) and 1.81 (n=3) at matched sizes/locators; scaled gap L·gap12 falling below the continuous envelope 6.85→4.85 vs saturation at n=3; coexistence plateau narrowing by the full size ratio 0.060→0.040 = 4/6 at fixed ξ; slope-ratio excess 2.18 vs 1.69) has no identified competitor. The pre-registered L=8 decision rule (closing factor ≥~2.1 → three-size confirmation of first-order; ~1.8–1.9 with saturation → downgrade to power-law closing) is the right discriminator and is exactly the kind of pre-registration referees reward.

## E. Exact rank certificates over Z[p]

No prior art found for exact integer rank certificates with a finite algebraic exceptional set in replica transfer matrices, or in the MIPT literature generally (generic rank = symmetry bound for L≤10 but 70 below it at L=12, identically for every local dimension computed; all exceptional points found for L≤8; two-sided L=12 certificate). Standard exact-algebra references already in bib (StewartSun1990, HornJohnson2013, Flanders1951). **Appears novel** as a computer-assisted-mathematics contribution.

## F. Record SCGF, no-freezing theorem, SMC estimation

- SMC/cloning for large deviations: Del Moral 2004 (cited), Giardinà–Kurchan–Peliti PRL 96, 120603 (2006) (cited), Tailleur–Kurchan 2009 (cited). Recommended addition: Brewer & Clark, "Efficient characterisation of large deviations using population dynamics" (2017) **[to-verify]** — the modern cloning-diagnostics reference matching the paper's finite-N population contract.
- Freezing: Derrida 1981 (cited) is present, but the systematic freezing literature is missing: Fyodorov, "Multifractality and freezing phenomena in random energy models," Physica A 389, 4229 (2010); Fyodorov & Le Doussal, "Freezing transitions and extreme values: random matrix theory, and disordered landscapes" (2014). The thm:rem construction (linear τ branch beyond q_c=√(2 ln 2) with τ′ continuous, so only second-derivative/interval-linearity diagnostics detect it) is exactly the phenomenology those works systematized — **citing them strengthens the theorem's placement**. Must add.
- First numerical quenched record SCGFs for Haar circuits with genuine record multifractality (D(q) nonconstant) and no-freezing bounds for q≤3 at L≤12: **no prior hit found** — appears first.

## G. Clifford record statistics and unitary designs

- Clifford 2-design / Gottesman–Knill: cited (Gottesman1998, plus the v21 pass added Gottesman98/AaronsonArkhipov13/Bouland19).
- Clifford 3-design: Zhu–Krämmer–Gross 2016 already in bib (ZhuKraemerGross2016); the general multiqubit statement is Webb, "Multiqubit Clifford groups are unitary 3-designs" **[to-verify: arXiv:1608.06445]** — recommended addition alongside. The paper's contribution is not the group theory but its verified two-qubit conjugation-3-design use to close Λ(2) exactly (correcting the ESS-law exponent) and the measured L-independent annealed–quenched gap 0.0226(2) nats/site with self-averaging variance 0.105/site.
- Clifford/stabilizer MIPT numerics: search niche is thin (Clifford-generator papers dominate); the trajectory-trivial / disorder-nontrivial separation for Clifford records appears **unclaimed elsewhere**.

## H. Complexity

PostBQP=PP lineage present (Shi2003, Aharonov2003, Fenner1994, Aaronson2005, AaronsonArkhipov2013, Bouland2019). The precise promise families (conditional-trajectory decision; conditional purity decision; the Born-average entropy sitting outside the BQP-estimable M(j,k) family) appear new in this framing. No action.

## I. Quenched finite-size-scaling benchmark (Appendix)

p_c=0.1597(8), ν=1.24(7), half-chain entropy slope α=1.55(7) bits — consistent with cited Li2019/Zabalo2020/Sierant2022; independent purification locator with disjoint seeds returns 0.1601–0.1604, ν=1.25(2). Recommended addition: the experimental MIPT line — Hoke et al., "Measurement-induced entanglement and teleportation on a noisy quantum processor," Nature 622, 481 (2023) **[to-verify details]** — and the postselection-barrier mitigation literature (e.g. arXiv:2410.05394 **[to-verify]**) to connect the benchmark to experimental reality.

---

## Overall verdict

**No scoop.** Every load-bearing exact result (finite-n replica mechanics and its structural theorems, the Z[p] rank certificates, the annealed p_c ladder with q=n Potts diagnostics, the no-freezing theorem, the Clifford disorder SCGF closure) is unoccupied as of 2026-09-26. The nearest active competition (Delmonte PRR 2025; Suzuki Quantum 2025) is approximate/numerical and differentiable by exactness. Required actions before submission:

1. Add the flagged references: Delmonte 2025; Suzuki 2025; Moghaddam 2023; Brewer–Clark 2017; Fyodorov 2010 + Fyodorov–Le Doussal 2014; Webb 2016 (multiqubit 3-design); experimental MIPT (Hoke et al. 2023).
2. Resolve the figshare placeholder DOI in Declarations (reviewers and editors check this first).
3. Complete the L=8 rung so the three-size first-order verdict is in the manuscript — currently the only claim resting on two sizes.

## Search log (raw results in scripts/litscan/, not pushed)

| file | query |
|---|---|
| s1_replica_mipt.json | measurement-induced phase transition replica transfer matrix monitored quantum circuits exact |
| s2_clifford_mipt.json | Clifford circuit measurement-induced entanglement phase transition stabilizer |
| s3_annealed_quenched.json | annealed quenched replica averaging measurement-induced entanglement transition |
| s4_firstorder_mipt.json | first-order measurement-induced entanglement transition discontinuous |
| s5_clifford_3design.json | two-qubit Clifford group unitary 3-design |
| s6_potts_q4.json | Potts model q=4 logarithmic corrections marginal universality |
| s7_freezing.json | freezing transition multifractality random energy model tau q linear branch |
| s8_cloning.json | cloning algorithm population dynamics large deviation function Giardina Kurchan |
| s9_postbqp.json | PostBQP PP hardness quantum trajectory conditional dynamics decision problem |
| s10_purification.json | purification transition monitored random circuits Gullans Huse locator |
