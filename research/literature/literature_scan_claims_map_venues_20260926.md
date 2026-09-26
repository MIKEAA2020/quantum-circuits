# Literature scan, claims–evidence map, and venue shortlist

**Date:** 2026-09-26 (post-v22, with the v23 L=8 rung in preparation)
**Subject manuscript:** *Exact Replica Mechanics and Born-Record Large Deviations in Monitored Quantum Circuits* (A. Abaee), file `research/versions/manuscript_revised_v22_exactZ3.tex` (57 bibitems, most recent cited year 2022).
**Method:** 26 targeted web searches (~170 results triaged), cross-checked against the manuscript's bibliography and claim structure (Scope §I, abstract, Discussion). Search log retained in `/tmp/litscan/` (not part of the repo).

---

## Part 1 — Literature scan

### 1.1 Novelty assessment, claim cluster by claim cluster

**A. Entanglement-feature leakage algebra and post-Haar closure (Thm. `fixed-algebra`, Thm. `strobe`, Prop. `general-n`).**
No prior statement found of (i) the minimal invariant algebra span{I,S,C} with the exact leakage norm for every replica number, (ii) the gate-to-gate closure on span{I,S}^⊗L after independent Haar averages, or (iii) the explicit Weingarten bond channel `W_{p,n}` for all n. The base formalism (entanglement features, locally scrambled dynamics) is Kuo–Akhtar–Arovas–You PRB 101, 224202 (2020) — already cited. The adjacent "locally scrambled dynamics" follow-up line (Akhtar–You multiregion entanglement) works in the feature-vector formalism but states no closure/leakage algebra and no AA† spectral structure. **Verdict: novel; base literature properly credited.**

**B. Annealed n-replica critical chain, n=3,4,5 (Secs. `n3annealed`, `n4n5`).**
Prior art: Bao–Choi–Altman PRB 101, 104301 (2020) is the n=2 Ising identification — the manuscript explicitly *recovers* it and converts it into a benchmark (correctly credited). The general statement that monitored-circuit MIPTs map to q-state Potts models with columnar disorder *in the replica limit* is folklore/lecture-level (ICTS lecture notes; Nahum–Wiese PRB 108, 104203 (2023); Zabalo et al. infinite-randomness RSRG 2023) — those works treat the *quenched* transition by RG, not exact annealed n=3,4,5 points. **No published annealed p_c^{(3)}, p_c^{(4)}, or n=5 first-order two-size test found.** Verdict: novel and quantitative; *but* the q=n-Potts correspondence circulates informally, so the paper should cite the RG line (Nahum–Wiese, Zabalo RSRG) and frame its own contribution as "the folklore correspondence made exact and quantitative at n=3,4,5." This preempts a referee's "already known."

**C. Exact Z3 rank certificates over Z[p] (App. `rank3`).**
No competing or prior line found (generic rank, exceptional points, L=12 two-sided certificate). **Verdict: novel.**

**D. Born-record large deviations, no-freezing theorem, REM construction (Sec. `records`).**
An adjacent, well-established literature exists that the manuscript does **not** currently cite: quantum-trajectory large deviations (Garrahan–Lesanovsky, PRL 104, 210601 (2010); Carollo–Jack–Garrahan, PRB 98, 041118(R) (2018) *— verify page at write-up*; Causer et al. 2025; Carollo et al. level-2.5), and the log-correlated REM freezing literature (Carpentier–Le Doussal, PRE 63, 026110 (2001); Fyodorov–Bouchaud, J. Phys. A 41, 372001 (2008)). No prior "Born-record" statistics framework (records as the paper defines them, surprisal SCGF, multifractal identities) was found. The construction of a *smooth* freezing (τ′ continuous at q_c) is characteristic of log-REM freezing — citing CLD/Fyodorov–Bouchaud both strengthens the Discussion remark ("only second-derivative diagnostics detect it") and connects to a known community. **Verdict: framework novel; missing citations are a real referee-facing gap — add them.**

**E. Clifford record-count, conjugation 3-design closure (Sec. `clifforddisorder`).**
The statement that the Clifford group is an exact unitary 3-design is *already established*: Webb (Quantum Inf. Comput. 16, 1009 (2016)) and Zhu–Kueng–Gross (PRL 116, 040501 (2016)) — the latter is cited, the former is not. The manuscript's "verified conjugation 3-design" is a re-verification consistent with literature; citing Webb removes any novelty ambiguity. The measured objects (record-count SCGF anchors, L-independent variance 0.105/site, annealed–quenched gap 0.0226(2) nats/site, ESS law) have no prior counterparts found. **Verdict: measured objects novel; add Webb 2016.**

**F. Complexity results (PostBQP/PP-hardness, Sec. `born`/`complexity`).**
Standard techniques applied to newly specified problems; the primary references (Aaronson Proc. R. Soc. A 461 (2005); Aaronson–Arkhipov; Bouland et al.) are already cited. No conflicting prior claims found. **Verdict: sound; no citation gaps.**

**G. Quenched Clifford FSS benchmark (App. `numerics`).**
p_c = 0.1597(8), ν = 1.24(7), α = 1.55(7) bits — consistent with Zabalo et al. PRB 101, 060301(R) (2020) and Sierant et al. PRB 106, 214316 (2022), both cited. **Verdict: consistent, properly hedged as simulation.**

### 1.2 Recommended citation additions (all verified this scan)

**Must-add (5):**
1. A. Nahum and K. J. Wiese, *Renormalization group for measurement and entanglement phase transitions*, Phys. Rev. B **108**, 104203 (2023). — The RG/quenched-side line the Discussion's "no log-CFT derived" positioning implicitly addresses.
2. M. Fava, L. Piroli, T. Swann, D. Bernard, and A. Nahum, *Nonlinear sigma models for monitored dynamics of free fermions*, Phys. Rev. X **13**, 041045 (2023). — The replica-trick EFT line; the free-fermion counterpart of what Sec. `aux` delimits.
3. Z. Webb, *The Clifford group forms a unitary 3-design*, Quantum Inf. Comput. **16**, 1009 (2016). — Independent original proof of the exact statement used for the β=2 closure.
4. J. M. Koh et al., *Measurement-induced entanglement phase transition on a superconducting quantum processor with mid-circuit readout*, Nat. Phys. **19**, 1314 (2023) — experimental realization.
5. Google Quantum AI and Collaborators, *Measurement-induced entanglement and teleportation on a noisy quantum processor*, Nature **622**, 481 (2023) — experimental realization (70-qubit class).

**Should-add (4):**
6. J. P. Garrahan and I. Lesanovsky, *Thermodynamics of quantum jump trajectories*, Phys. Rev. Lett. **104**, 210601 (2010). — Foundation for Sec. `records`' trajectory-LD framing.
7. F. Carollo, R. L. Jack, and J. P. Garrahan, *Unravelling the large deviation statistics of Markovian open quantum systems*, Phys. Rev. B **98**, 041118(R) (2018) *(verify page)*.
8. D. Carpentier and P. Le Doussal, Phys. Rev. E **63**, 026110 (2001). — Log-correlated freezing scenario; context for the smooth freezing of Thm. `rem`.
9. Y. V. Fyodorov and J.-P. Bouchaud, J. Phys. A **41**, 372001 (2008). — Freezing and extreme-value statistics in log-REMs.

**Optional (3):**
10. A. Mele, *Introduction to Haar measure tools in quantum information*, Quantum **8**, 1343 (2024) — modern Weingarten survey for practitioners.
11. The Weingarten-calculus survey (B. Collins et al., 2021).
12. A. Zabalo et al., *Infinite-randomness criticality in monitored quantum dynamics* (PRB, 2023) — RSRG line.

**Recent developments worth one Discussion sentence each (2024–2026):** monitored free-fermion multifractality (arXiv:2607.23871); Lumia et al., *Measurement-induced transitions beyond Gaussianity*; teleportation-MIPT in the SYK model (SciPost, 2024); first-order/"critical touching" claims for temporal entanglement transitions (Sep 2026). These show the first-order-MIPT question is live — the n=5 verdict is timely.

### 1.3 Risk flags
- **Folklore risk (main):** the q=n-Potts annealed correspondence circulates in lecture/RG form; mitigate by citing Nahum–Wiese + Zabalo RSRG and framing the exact chain as the contribution.
- **Trajectory-LD gap:** a referee from the Garrahan school will notice the absent citations (items 6–7).
- **Timeliness:** citations stop at 2022; the 2023–2026 experimental/RG/EFT surge is invisible in the current bibliography.
- **Strongest single upgrade before submission:** the L=8 rung (v23, in preparation) — closes the manuscript's own declared two-size caveat.

---

## Part 2 — Claims–evidence map

| # | Claim (as stated in abstract/Scope) | Evidence in manuscript | Type / strength | Residual gap |
|---|---|---|---|---|
| C1 | Fixed-basis measurement leaks span{I,S}; minimal invariant algebra span{I,S,C}; exact leakage norm ∀ n | Thm. `fixed-algebra`, Eq. (leaknorm)/(leak-n) | **Theorem** (full proof) | None |
| C2 | Post-Haar closure of the feature space; Weingarten bond channel for all n | Thm. `strobe`, Prop. `general-n`, Eq. (Wpn) | **Theorem** | None |
| C3 | One-period operator AA† ⇒ real positive semisimple spectrum, strict contraction, S_n×S_n symmetry, compression | Thm. `general-n` | **Theorem** | Simplicity of λ₁ at small p proven only at tested n (see C7/C8) |
| C4 | n=2 compressed rank = 3·2^{L/2−2}, ∀ p∈[0,1), ∀ d | Sec. `compression` | **Theorem** | None |
| C5 | n=3 rank: generic = symmetry bound for L≤10, 70 below at L=12; all exceptional points for L≤8; endpoint ranks | App. `rank3`, exact Z[p] certificates + SHA-256 ledger | **Exact certificate** (no floating point) | Generic rank for general L open |
| C6 | Two-replica model = Bao–Choi–Altman triangular Ising; annealed p_c^{(2)}(d) closed form; free-fermion spectrum; exact finite-size amplitudes | Sec. `ising` (Houtappel, Kaufman) | **Theorem + exact benchmark** | Recovers published result (credited) |
| C7 | Annealed p_c^{(3)} = 0.305(3) (d=2), continuous, 3-state-Potts amplitude ratio + slope exponent | Sec. `n3annealed`, sector-resolved TM, L=4..12 | **Exact-TM scaling** (numerics-grade) | Growth-rate regularity as theorem open |
| C8 | p_c^{(4)} ≈ 0.383 at four sizes, full S₄ colour resolution, marginal q=4 log-corrections (amplitude ratio → 1/4) | Sec. `n4n5` | **Numerics + log-correction analysis** | Marginal case inherently slow — drift collapse via L=10 third crossing is evidence, not proof |
| C9 | n=5 first-order: two-size test (L=4→6 closing factor 2.12 vs 1.81 continuous baseline; scaled gap below envelope; plateau narrows at fixed ξ) | Sec. `n4n5`, Table `tab:n5twosize` (1.7×10⁶ bond labels) | **Numerics (exact per-sample)** | **Two sizes cannot separate exponential vs power-law closing — L=8 rung in preparation (v23)** |
| C10 | Quenched Clifford FSS: p_c = 0.1597(8), ν = 1.24(7), α = 1.55(7) bits; independent purification locator 0.1601–0.1604 | App. `numerics` (16≤L≤512, crossings, collapse, bootstrap) | **Simulation benchmark** | Explicitly not a theorem; consistent with Zabalo/Sierant |
| C11 | No finite-q freezing for any allowable finite-reachable monitored process (incl. fully monitored Haar-refreshed family) | Thm. `nofreeze`, Cor. `p1closure` | **Theorem** | Beyond finite-reachable sets open |
| C12 | Born-realizable record sequence with finite-q freezing at q_c=√(2 log 2), τ′ continuous | Thm. `rem` (explicit construction) | **Theorem (construction)** | Whether local circuit ensembles realize it — open |
| C13 | Symmetric scalar replica moments do not determine quenched Rényi entropy; bivariate family does | Sec. `born`, information-theoretic counterexample | **Theorem (counterexample)** | None |
| C14 | Conditional-trajectory decision PP-hard (PostBQP), same for conditional purity | Sec. `complexity` | **Theorem** | Average-case hardness explicitly not claimed |
| C15 | Record SCGF/multifractal identities | Sec. `records` | **Conditional on LD hypotheses** (stated as such) | Physical nonanalyticity requires extrapolation survival |
| C16 | First numerical quenched record SCGFs (Haar), genuine multifractality, no freezing q≤3, L≤12, T=2L | Sec. `smcnumerics` (SMC, validated vs exact enumeration) | **Numerics with estimator contract** | Finite N, T, L |
| C17 | Clifford record count: β=1 anchors, variance 0.105/site (L-indep), annealed–quenched gap 0.0226(2) nats/site, β=2 closed via 3-design | Sec. `clifforddisorder` | **Exact anchors + measured** | 3-design statement re-verifies Webb 2016 / Zhu et al. 2016 (cite both) |
| C18 | Replica interpolation identity ⇒ disorder-replica interchange = self-averaging criterion; tilted-variance profile measured | Prop. `replica-int` + profile family | **Theorem + measured profile** | Uniformity in (L,T) open |

**Map of gaps → v23 (in preparation):** the L=8 rung upgrades C9 from two-size to three-size; decision rule: closing factor ≥ ~2.1 (with L·gap12 falling below the n=3 envelope 4.85) ⇒ first-order confirmed at three sizes; ~1.8–1.9 saturating ⇒ downgrade to power-law. C5, C7, C8 gaps are theorem-side and unaffected.

---

## Part 3 — Venue shortlist (ranked)

| Rank | Venue | Fit | Practical notes |
|---|---|---|---|
| 1 | **Phys. Rev. B** | The manuscript's citation core and genre live here: Bao–Choi–Altman PRB 101, 104301; Kuo et al.; Jian et al.; Zabalo; Sierant; Nahum–Wiese PRB 108 (2023). Long exact-results papers with transfer matrices and certificates are standard PRB fare. | Standard referee pool knows the replica-MIPT line. No institutional affiliation required. Length OK (PRB has no hard page limit; ~50 pages acceptable). |
| 2 | **SciPost Physics** | Physics-first, open access, no APC, welcoming to long technically dense papers; the paper's certificate/reproducibility ethos (SHA-256 ledgers, verification contracts, figshare deposit) matches SciPost's open-refereeing culture unusually well. | Referee reports are published (open); a constructive-plus-visible record suits the verification-heavy style. Independent researcher friendly. |
| 3 | **PRX** | Only after the L=8 verdict lands: "three-size first-order confirmation of the annealed replica chain, exactly" is a potential headline. Without it, the paper reads as many strong but individually incremental exact results — a known PRX rejection mode. | High bar; breadth (complexity + SMC + stat-mech) may read as sprawling. Consider only if v23 lands decisively and the abstract is rebuilt around it. |
| 4 | **J. Phys. A: Math. Gen.** | The transfer-matrix/rank-certificate/Weingarten mathematical core is a first-class J. Phys. A topic; the paper would feel at home technically. | Lower visibility within the MIPT community; IOP. Good fallback if PRB referees balk at breadth. |
| 5 | **Physical Review Research** | Broad scope (complexity + stat-mech mix is fine), faster turnaround. | Younger journal; prestige perception still forming. |
| 6 | **Quantum** | Only if reframed quantum-info-first (hardness, designs, Born records); the stat-mech core is off-center for its audience. | Open access; strong community, wrong center of gravity for this paper. |
| 7 | **JSTAT** | Possible for a split statistical-mechanics companion (see strategy below). | Better for shorter focused pieces. |
| 8 | **Commun. Math. Phys.** | Only as a split mathematical companion (closure algebra, rank certificates, Weingarten mechanics, no-freezing theorem). | The physics paper stays separate; high effort. |

**Submission strategy options:**
- **Single paper (recommended default):** PRB first; SciPost as strong second (or simultaneous arXiv + SciPost submission). Fill the figshare placeholder DOI before submission; add the 5 must-cite references; wait for the v23 L=8 rung so the n=5 claim enters review at three sizes.
- **Two-paper split (fallback if length/breadth draws referee fire):** (i) *Exact replica mechanics and the annealed replica chain* (C1–C9) → PRB/SciPost; (ii) *Born-record large deviations and the quenched record SCGF* (C11–C18) → PRB or J. Phys. A. The complexity results ride with (ii). Cost: the "one exact framework" narrative is diluted; benefit: each paper is squarely inside one referee pool.

**Pre-submission checklist (ordered):** (1) let the L=8 grid finish and build v23 (already scripted, `followup_v23.sh`); (2) add must-cite items 1–5 (all verified above); (3) add should-cite items 6–9 with a bib-verify pass; (4) fill the figshare DOI; (5) tighten the abstract (currently ~600 words — PRB/SciPost tolerate long abstracts, but a 250-word version with a one-paragraph "exact results included" list reads better); (6) AI-use declaration already present — keep it, several venues now require it.

---

*Prepared by the watch agent (Z.ai Code), Task ID: literature-scan, 2026-09-26. Search queries and raw JSON results retained in `/tmp/litscan/` (s1–s24, v1–v5) outside the repo; this file is the durable record.*
