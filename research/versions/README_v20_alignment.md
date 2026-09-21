# v20 — the alignment pass

This round answers the author review's three questions with executed
work:

## 1. Title / abstract / keywords / sections / supplementary alignment

**Audited everything against the v19 findings.**  Title: aligned (the
v17–v19 results live under its two declared pillars).  Abstract:
aligned except one internal inconsistency ("three sizes" vs. the L=10
third crossing) — fixed.  Keywords: extended with "Potts universality
classes" and "sequential Monte Carlo".  Sections: six stale pre-v19
cross-reference strings found and fixed (Scope p_c 0.1595(10) →
0.1597(8); sec:n3annealed's "three sizes / p_c^(4)=0.40 / reachable
to L=6 / first n=5 diagnostics"; the tab:n4annealed caption; the n=5
single-size trend 0.40<0.49 → 0.383<0.47 with the two-size refinement;
the Discussion's p_c^(4)=0.40).  Supplementary: content aligned with
the [SM] promise; v3 adds the versioned-ledger note
(certificate_sha256_v5/v6.txt).  A suspected supplement bracket defect
was disproven by hexdump (display artifact) — the asserted-anchor
patch refused the non-existent anchor, as designed.

## 2. Pedagogical / expository enhancements

Yes — three targeted, non-decorative additions:
- **Remark rem:whyqn**: why the q=n-Potts classes appear (T_p central
  in Q[S_n]; std of dimension n−1 = q−1 carries σ at multiplicity
  (n−1)²; empirical identification, honestly scoped) and why the
  annealed points recede from the quenched transition as n grows
  (the Z^n disorder tilt sharpening with n; the p_R² weight as the
  n=2 instance; gap_12 as the coexistence tunnelling splitting).
- **Remark rem:dichotomy**: corners (phase competition, max of
  analytic branches) vs. affine branches (extremal domination,
  unbounded reachable set) — the physical dichotomy of the no-freeze
  theorem.
- **Sec. I logical-spine roadmap** + the Sec. I enumeration extended
  to the computed replica chain, the two-size confirmation, the
  no-freeze theorem and the SMC measurement.

## 3. Simulation alignment

The web explorer (root project + the repository mirror) gained a new
"Replica ladder" section presenting the v19 findings: the annealed
replica chain chart (n = 2…5 vs. the quenched line), the two-size
first-order test table, the Haar record SCGF ψ(k) curves (L = 8, 12)
with the record-multifractality statistics, and the no-freeze theorem
card with the interpolation identity.  All numbers verbatim from
manuscript v19.  (Task 15-a; see the worklog.)

## Files

- `manuscript_revised_v20_alignment.tex/.pdf` (36 pp) — built by
  `patch_v20_alignment.py` (11 asserted-anchor edits) from v19;
  compiled with tectonic; pypdf-verified.
- `supplement_v3.tex/.pdf` (6 pp) — built by
  `patch_v20_supplement.py` from the deposited supplement v2.
- `changelog_v20.md`, `certificate_sha256_v7.txt`.
- Web explorer: `src/lib/research-data.ts` (v19 data blocks),
  `src/components/sections/replica-section.tsx` (new),
  `page.tsx` / `nav.tsx` / `hero.tsx` / `repro-section.tsx` (section
  order + numbering).
