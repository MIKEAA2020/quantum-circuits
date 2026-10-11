# W3b ADJUNCTION ATLAS v0.1 — RESULTS LEDGER
fingerprint: W3b-ATLAS-2026-10-11
date: 2026-10-11 · engine: /home/user/w3b_atlas.py · report: /home/user/w3b_atlas_report.json · runtime 0.3 s
policy: FAILURES PUBLISHED FIRST (W3b standing rule). Paper-pending rows never guessed.

## ══ FAILURE ROW (published first) ══

### Row i — (J, K) split pair: J isometry, K retraction (KJ = I_a), a=3, b=8
VERDICT: **NO ADJUNCTION in the linear world** (obstruction certified, not narrated).
- Triangle-identity trap exposed: with η = I_a, ε = JK the triangle identities PASS (residuals 1.3e-14, 1.7e-15). Triangles are necessary, NOT sufficient — a candidate that passes triangles can still fail adjunction.
- Decisive test: adjunction would force JK = I_b; measured ‖JK − I₈‖ = 8.72, rank(JK) = 3 < 8. Rank bound makes it structurally impossible (rank(JK) ≤ a < b). Hom-dimension test (ab = ab) passes and is non-decisive — recorded as a trap class.
- Repair: canonical twin K# = Jᵀ gives the actual adjunction J ⊣ Jᵀ, a reflective inclusion; counit ε* = JJᵀ is the orthogonal projector (idempotent to 5.5e-16, symmetric exactly).
- Setting-flip: the same split data in an ordered (poset/rig) setting IS a Galois connection (fg ≤ id suffices). The adjunction question has no setting-free answer; ambient structure is an input, not a background.
- Registered expectation: met exactly (obstruction / repair-by-restriction / residual = reflection data).

## ══ POSITIVE ROWS (with quantified thresholds) ══

### Row ii — Weingarten = Gram pseudoinverse (certificate + rank audit)
- At d = 3, n = 3: Gram 6×6 full rank; Wg = G⁻¹ satisfies Moore–Penrose identities to 2.7e-14 / 3.4e-17; Wg central (conjugation defect 2.9e-17); n=2, d=2 spot-values equal known Weingarten numbers exactly (1/3, −1/6).
- Rank-audit table (n = 3): d=1 → rank 1/6 (σ_min = 0); d=2 → rank 5/6 (σ_min = 6.0e-16, i.e. zero); d=3 → rank 6/6.
- Turns the counit question into a sharp threshold: **counit-like inverse exists ⟺ d ≥ n**; below threshold only the pseudoinverse branch. Residual freedom: branch choice + basis gauge.
- Row kept POSITIVE with the threshold attached — positive rows are only kept with their quantified boundary.

### Row iii — S_n × S_n bimodule → tensor–hom
- Verdict: adjunction EXISTS at module level (tensor ⊣ hom, unconditional). Certificate: Peter–Weyl C[S₃] = ⊕λ Sλ ⊠ Sλ*, Σ dλ² = 6 = |S₃| ✓ (dims 1²+2²+1²).
- The user's "expected interesting failure" cannot live at module level; if it materializes it must be at the STRICT/monoidal level (Φ_n on G_n^⊗L, associator/compatibility). Strict test queued — definition-pending.
- Discipline note: reporting a positive where a failure was expected is itself a registered outcome (expectation postmortem: the failure intuition attached to the wrong level of structure).

## ══ PAPER-PENDING ROWS (never guessed) ══
B_even·B_odd period map adjunction; C_comp = K_eJ_oK_oJ_e; Φ_n strict level; Clifford-conjugation 3-design engine input — all **definition-pending: paper upload required**. Anti-GRU-pattern discipline applied to our own corpus row.

## ══ ATLAS-LEVEL FINDINGS ══
1. Triangle-identity trap class identified (Row i): any future adjunction candidate in this corpus must run the decisive identity test, not triangles alone. Promoted to a standing atlas check rule.
2. Every row produced either a numerical obstruction certificate or a numerical existence certificate; zero narrative verdicts. W3b standard met.
3. Ambient-structure dependence is an empirical axis (Row i flip): the atlas ledger now carries an `ambient` field by default.

---

# ══ v0.2 — FOUR-DIRECTIVE ROUND (2026-10-11) ══
fingerprint: W3b-ATLAS-2026-10-11-v02
engine: /home/user/w3b_atlas_v02.py · report: w3b_atlas_v02_report.json · runtime 0.1 s · v0.1 record above STANDS unaltered.
directives: D1 strict-level row iii · D2 trap-class audit row ii · D3 two new rows (executed as three: Energy, Particles, Spin/statistics) · D4 trap class as standing check (every row now carries a trap_class block).

## FAILURE / TRAP-CLASS ROWS FIRST

### D2 — Row ii trap-class audit: row ii is a CONFIRMED trap-class instance below threshold
- At d=2: triangles PASS (MP identities, residuals 9.9e-17 / 9.6e-15) while the decisive identity test FAILS: ‖G·G⁺ − I₆‖ = 1.000 (Gram rank 5 < 6). At d=3: triangles 2.3e-16 / 4.1e-14, decisive 2.1e-15 — both pass.
- Verdict: v0.1's positive on row ii was saved by the DECISIVE test, not the triangles. The pseudoinverse pair (G, G⁺) is a reflection-like datum at d<n (idempotent counit) and an adjunction only at d≥n. The assessor's suspicion was correct and is now certified on both sides of the threshold.

### ROW iv — Energy (RP3 row verbatim: "Energy | Kinetic / Potential | mass, height, velocity | conservation | E (canonical template)")
- Adjunction species DENIED: no order/projection structure in the row.
- CONJUGACY species certified with exact boundary: L² = id ON-GRID exactly 0.0 on convex cosh (disclosed off-grid floor 9.5e-6 = O(f″h²/8) at half-step points — grid-resolution floor printed, not hidden); FAILS off-domain: nonconvex x⁴−2x² biconjugate deficit 1.000 on |x|<0.5 (L² = closed convex envelope, Fenchel–Moreau).
- Refines the v8 "yields nothing" verdict: no physics yield, but a sharp measurable species assignment. Species assignment is empirical, not rhetorical.

### ROW v — Particles ("Quantum field | Particle / Antiparticle | charge conjugation | CPT | E")
- Z₂-involution certified at the MODE-SWAP level, sign table MEASURED not assumed: C swaps +/− single-particle projectors exactly (0.0); operator squares measured C C* = T T* = Θ Θ* = −I in the 4D Dirac rep (pseudoreal/Kramers; convention-free content is the projector swap).
- Adjunction species DENIED (involutive-with-sign, not reflective).
- Rig-defect logged: the v0.2 first build hardcoded "C² = +1" in prose against a certificate measuring −1; caught by reading the JSON against prose. Prose must be generated from certificates (rule added to engine discipline), fix forward.

### ROW vi — Spin/statistics ("Matter-force structure | Fermion / Boson | spin number | statistics | E")
- Z₂-GRADING certified at algebra level: 3-mode CAR exact 0.0; parity conjugation P a P = −a exact 0.0; CCR [b,b†]=1 on N=7 truncation, interior residual 1.8e-15 with truncation boundary DISCLOSED (infinite-dim is not matrix-checkable); 2π-rotation at spin 1/2: R = −I residual 1.2e-16.
- Honesty clause printed in the row: the spin-statistics CONNECTION (locality + Lorentz) is a theorem, not matrix-derivable — the atlas certifies the graded algebras and the sign match, and says exactly what is not certified.
- Adjunction species DENIED (a grading, not a reflection).

## POSITIVE STRICT-LEVEL RESULT

### D1 — Row iii strict level PASSED at the atlas's registered strict definition
Registered definition (workable without the paper): adjunction must live at the BALANCED tensor over C[G₃] — composition relations (xa)⊗y = x⊗(ay), not the vector-space tensor — with tensor–hom dimension equality on regular bimodules.
Certificates (all exact):
- rank(balanced relations) = 30 ⇒ dim(X ⊗_A X) = 36 − 30 = 6 (=dim X); kernel-of-multiplication contains relations exactly (containment 0.0, dims equal ⇒ equality);
- dim End_bimod(X) = 3 (= number of conjugacy classes ✓); dim Hom_A(X,X) = 6; dim Hom_bimod(X, Hom_A(X,X)) = 3;
- adjunction dimension certificate 3 = 3.
- strict content printed: X ⊗_C X is 36-dim while X ⊗_A X is 6-dim — the vector-space tensor is the WRONG composition in the bimodule category; that dimensional split IS the strict-level content.
Expectation postmortem v2: the failure intuition is now excluded at TWO levels (vector-space, balanced-tensor). Remaining level — monoidal/Φ_n on G_n^⊗L — is the paper's definition: still pending upload, never guessed.

## v0.2 ATLAS-LEVEL FINDINGS
1. Trap-class confirmed ON the atlas itself (row ii) — the check is load-bearing, and D4 makes it a mandatory block on every row.
2. Species taxonomy now empirically populated: adjunction NONE of rows iv–vi survived (consistent with W3b's register: adjunction only where actually claimed); conjugacy (iv), Z₂-involution-with-sign (v), Z₂-grading (vi). P4's three species now carry matrix-certified instances.
3. Level-ladder discipline validated: iii passed at two levels; the pending level is definition-blocked, not conviction-blocked.
4. Corpus picture: i FAILED (adjunction), ii positive⟹decisive-saved, iii positive at both computed levels, iv–vi species-resolved negatives for adjunction. Failure rate for the adjunction species across E-rows: high — data for P4/H8's inversion-rule bookkeeping, as the assessor flagged ("if most rows fail, the claim is narrower").

---

# ══ v0.3 — POSITIVE-DIRECTION STRESS ROUND (2026-10-11) ══
fingerprint: W3b-ATLAS-2026-10-11-v03
engine: /home/user/w3b_atlas_v03.py · report: w3b_atlas_v03_report.json · runtime 3.3 s · v0.1/v0.2 records STAND.
directives: D5 stress the adjunction rate on the assessor-named likely-positive rows; D6 FT1 narrowing (folded document-side in v10.14).
REGISTERED EXPECTATION (assessor, pre-run): vii and viii are "the rows where adjunction is most likely to apply … a stress test of the 2/6 rate in the opposite direction." Computation decided, not the expectation.

## RIG-PROCESS LOG FIRST (this round had no row failures; it had one evaluator failure)

**Evaluator-order bug, row viii (caught by the certificate, not by eye).** First build's word evaluator accumulated left-multiplication, reading words right-to-left: the hom-property certificate measured FALSE on all 216+36 assignments while the prose hardcoded "verified" against it — the already-registered defect class (prose must be certificate-generated) caught it instantly. Evaluator fixed to left-to-right accumulation; the verdict string now branches on the measured flag. Second live instance of the prose-vs-certificate rule biting; the rule has demonstrated value twice and stays.

## ROW vii — Universal constructions ("Diagram | Limit / Colimit | universal property | adjunction | math")
- ADJUNCTION CERTIFIED on both sides at decisive level: Δ ⊣ Π and ⊔ ⊣ Δ on the finite fragment: **72/72 exact hom-count identities**, diagonal-map naturality brute-forced over all maps on the small grid = TRUE, triangle identities TRUE at component level.
- The corpus row names "adjunction" as its invariant — the atlas certifies rather than trusts.

## ROW viii — Group theory ("Group | Element / Inverse | operation | identity | math")
- Rendering (a) — the row's NAMED polarity: anti-involution species CERTIFIED exactly (integer Cayley arithmetic): i² = id and i(gh) = i(h)i(g) on S₃ (order 6), Z₆, S₄ (order 24).
- Rendering (b) — the genuine adjunction: Free ⊣ Forgetful: decisive certificate **Hom_Grp(F_n, S₃) ≅ (S₃)ⁿ by eval-at-generators**: n=2 (36 assignments) and n=3 (216) — every assignment extends to a homomorphism with the hom property verified exactly on 3,600 sampled word pairs per assignment; triangles at component level.
- **New row-level finding (viii): one corpus row can house two renderings in two species.** The named polarity (element/inverse) is anti-involution; the row's adjunction instance is free/forgetful. Species labels must record WHICH rendering is meant — ledger rule absorbed.

## MEASURED RATE AFTER v0.3
- Adjunction-positive: ii (d ≥ n only), iii (balanced tensor), vii, viii-b → **4/8 row-tests.** Denied/mismatched: i (registered failure), iv (conjugacy), v (Z₂+Kramers), vi (Z₂-grading).
- Directional read: positives live exactly where universal properties exist (vii) or freeness exists (viii-b); the physical E-rows (iv–vi) remain adjunction-negative. The rate is rendering-dependent: the data supports P4's species clause, not a single formalization center.
