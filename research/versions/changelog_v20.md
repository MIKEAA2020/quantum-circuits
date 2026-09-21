# Changelog v20 — the alignment pass (title/abstract/keywords/sections/
# supplementary audited against the v19 findings; two pedagogical
# remarks added)

From v19.  All files NEW (never-overwrite honored).  No scientific
content of v19 is altered: every number in v19's results sections is
reproduced unchanged; this round fixes *internal cross-references* that
still carried pre-v19 values, and adds expository material requested in
the author review.

## S.1 The alignment audit (question 1 of the review)

Audited: title, abstract, keywords, every section, both appendices, and
the Supplemental Material, against the v19 findings (v17: p_c^(3);
v18: n=4 S_4 colour resolution, n=5 diagnostics, Haar SMC; v19: n=5
two-size test, p_c^(4)→0.383, no-freeze theorem, interpolation
identity).

**Aligned, no change needed:**
- *Title* — "Exact Replica Mechanics and Born-Record Large Deviations
  in Monitored Quantum Circuits": the v17–v19 additions all live under
  the two declared pillars (replica mechanics: the n=3,4,5 chain;
  Born-record large deviations: the no-freeze theorem, the SMC run).
- *Sections II A–E, III, IV A–C, V, both appendices* — verified line
  by line against the deposited results; no stale numbers found (the
  tab:n5twosize, tab:n4annealed, tab:smchaar, tab:n3annealed tables
  and the no-freeze/SMC sections match the result JSONs to the quoted
  precision).
- *Supplementary content* — the [SM] reference in the main text
  promises exactly the n=3 rank-certificate data that supplement v2
  delivers; no misalignment.  (A suspected `\begin{table}]` bracket
  defect in the supplement turned out to be a display artifact of the
  review tooling — the actual source is `\begin{table}[h]`, verified
  by hexdump; the asserted-anchor patch correctly refused the
  non-existent anchor.)

**Misalignments found and fixed in v20 (six stale strings, all
pre-v19 leftovers that the v19 patch had not reached):**
1. Sec. I (Scope) quoted the pre-re-centring quenched point
   `p_c=0.1595(10)`; the appendix, Sec. II.E remark and Discussion all
   say 0.1597(8).  → fixed to 0.1597(8).
2. The abstract said "full S_4 colour resolution at three sizes" in
   the same clause that cites "the L=10 third crossing" (which needs
   L=4,6,8,10).  → "four sizes".
3. Sec. II.G (sec:n3annealed) cross-reference: "completes the n=4
   computation … at three sizes (L=4,6,8): p_c^(4)=0.40 … and it adds
   the first n=5 diagnostics", plus "reachable to L=6 with the present
   machinery" — the v18 text.  → four sizes (L=4,6,8,10),
   p_c^(4)≈0.383, the two-size test, reachable to L=10.
4. Table tab:n4annealed caption: "at L=4,6,8" while the table itself
   carries the (8,10) crossing 0.3823.  → "L=4,6,8,10".
5. Sec. II.H (n=5 diagnostics): the single-size calibration trend
   "0.2338<0.305<0.40<0.49" contradicted the manuscript's own final
   values.  → "0.2338<0.305<0.383<0.47", with the single-size
   calibration 0.48–0.50 explicitly refined by the two-size test to
   0.47–0.48 (and "extrapolated 0.40" → 0.383).
6. Discussion: "p_c^(3)=0.305(3) and p_c^(4)=0.40" → "≈0.383".

**Keywords** extended for the v18/v19 content: added "Potts
universality classes" and "sequential Monte Carlo" (the previous list
predates the annealed-chain and SMC results).

**Supplement** v2 → v3: content unchanged; the file-ledger section now
records the versioned extension ledgers certificate_sha256_v5.txt
(v18 round) and _v6.txt (v19 round), which extend — never alter — the
base ledger the supplement verifies against.

## S.2 Pedagogical / expository additions (question 2 of the review)

The review asked whether the work merits *non-decorative* pedagogical
or physical-intuition additions.  Answer: yes, in three targeted
places; all are physics content, none is decoration:

1. **Remark rem:whyqn** (end of Sec. II.H) — "Why q=n, and why the
   annealed points recede from the quenched one."  Organizes the whole
   replica chain under two mechanisms: (i) the site channel T_p is
   central in Q[S_n] (the cycle count is a class function), so the
   transfer problem decomposes over S_n irreps exactly as the q-state
   Potts transfer matrix does over its representation sectors, with
   the standard representation of dimension n−1 = q−1 (the Potts spin
   components) carrying the σ excitation at multiplicity (n−1)², the
   energy–spin hierarchy of the Potts spectrum; the identification is
   stated as empirical (no Temperley–Lieb equivalence exhibited for
   n≥3) — every measured number supports it, and the q>4 criterion
   then predicted the n=5 outcome correctly.  (ii) the annealed
   average is the disorder law tilted toward high-Z realizations, the
   tilt sharpening with n (Prop. prop:replica-int makes this exact);
   for this family high-Z disorder = measurement-poor records, the
   p_R² collision weight of Sec. II.E being the n=2 instance in
   microcosm — so the annealed singularity recedes as the tilt
   sharpens, and the chain 0.1597(8)<0.2338<0.305<0.383<0.47 is the
   n-axis trace of that single mechanism.  Closes by identifying
   gap_12 as the tunnelling splitting between the two coexisting phase
   free energies (interface tension vs. the power-law continuous gap),
   which is why the closing-factor and L·gap_12 diagnostics separate
   the behaviours.
2. **Remark rem:dichotomy** (end of Sec. IV.E, after the no-freeze
   verification paragraph) — "Corners versus affine branches — the
   physical dichotomy."  A corner (τ′ jump) is phase competition
   between invariant sectors, the free energy a maximum of analytic
   branches, as at a first-order thermodynamic transition; an affine
   branch (τ linear over an interval) is extremal domination by a
   single unbounded configuration class (the REM beyond
   q_c=√(2 log 2), τ′ continuous).  Finite-reachable allowable
   processes can do the first, never the second: the extremal
   configuration is bounded and the process mixes (Hilbert-metric
   contraction), so the growth mode is unique and analytic — no ladder
   of ever-more-extreme configurations for the tilt to climb.  Freezing
   is a statement about reachable-set geometry, not about the record
   observable.  Ties to the verification output (corners with curved
   branches in the reducible chains; affine terminal branch only in
   the REM benchmark).
3. **Logical-spine roadmap** (Sec. I) — one sentence mapping the paper:
   II A–E exact two-replica mechanics + closed-form solution; II F–H
   the spectral computation at n=3,4,5 and the q=n-Potts test;
   Sec. III Born-weighted separations and complexity; Sec. IV record
   large deviations, the no-freeze theorem, and the first quenched
   record SCGFs; Sec. V what remains conditional.  (Sec. I's
   enumeration of results also now includes the computed replica
   chain, the two-size confirmation, the no-freeze theorem and the SMC
   measurement — it previously stopped at the v14 content.)  Labels
   sec:born / sec:aux added to the two previously unlabelled sections.

Deliberately NOT added: a nomenclature/notation table (Sec. I already
fixes conventions), figure-level restatements of Tables (the tables
are self-explanatory), or any renumbering (all labels stable from
v19).

## S.3 Verification

- patch_v20_alignment.py: 11 asserted-anchor edits, each anchor
  asserted unique before replacement; self-check asserts the six stale
  strings are absent from the body and the seven new strings present.
- Compiled with tectonic: 36 pages (v19: 35).  pypdf verification: all
  key strings present in the rendered PDF ("0.1597(8)", "four sizes",
  "Potts universality classes", "Why q = n, and why the annealed
  points recede", "Corners versus affine branches", "logical spine",
  "0.2338 < 0.305 < 0.383 < 0.47", "reachable to L = 10",
  "L = 4, 6, 8, 10"); the stale strings absent.
- patch_v20_supplement.py + supplement_v3: 6 pages, compiled and
  verified (ledger note renders; content otherwise byte-identical to
  the deposited v2 apart from the header comment and the ledger
  paragraph).
- No scientific number changed: diff of v19→v20 restricted to the six
  cross-reference fixes, the keywords, the two remarks, the roadmap
  sentence, the two labels, and the header comment.

## S.4 Files

- versions/manuscript_revised_v20_alignment.tex / .pdf (36 pp)
- versions/supplement_v3.tex / .pdf (6 pp)
- versions/patch_v20_alignment.py, versions/patch_v20_supplement.py
- versions/changelog_v20.md (this file),
  versions/README_v20_alignment.md,
  versions/certificate_sha256_v7.txt (8 entries)
