# Changelog — framework v9.3 (governance-correction version note)

Date: 2026-10-11 (build 2026-10-11 +03:00). Script:
`research/scripts/v26-framework-governance/patch_v9_3_governance.py`.
Source preserved unmodified: `formalism-v9.2.md` (author-uploaded,
byte-identical re-read after the pass). New files:
`formalism-v9.3.md`, this changelog, `certificate_sha256_v20.txt`.

Provenance note: author-directed round (session 2026-10-11): "framework-
side F1/F2/F3/F5 fixes (audit item 9)" — item 9 of the recommended
order of action in the line-level audit of `formalism-v9.2.md` and
`gap.txt` (`audit_formalism_v9_2_and_gap_20261011.md`), which read
"Framework-side: fix F1/F2/F3/F5 whenever the descriptive line next
ships." The descriptive line ships now, as **v9.3** — per the
framework's own discipline (prior versions untouched on disk; the
descriptive fortress never overwrites), via the NEW-patch-script
protocol mirroring the manuscript rounds.

## Self-label

v9.3 ships neither a bridge artifact nor refreshed digest content —
only governance corrections. Under Delivery Charter rule 4 **as
amended this round** it is therefore a **GOVERNANCE-CORRECTION VERSION
NOTE**, and the version history table and the header note say so. No
generative release is paired (a governance note, not a milestone
round); the v9.2 lineage appendix (the descriptive digest) is carried
forward unchanged.

## The four fixes

1. **F1 — the §13 version table completed.** The v9.1 row's stale
   "(this file)" self-reference (true only in v9.1) is re-labeled to
   `formalism-v9.1.md`; a **v9.2 row** is added (content drawn from
   the v9.2 note's own summary: the lineage-split release, the
   descriptive digest with the sum-invariance withdrawal, the pairing
   rule, Part I byte-identical to v9.1); and the **v9.3 row** is added
   (this round).
2. **F2 — Charter rule 4 amended with the descriptive-lineage
   exception.** The audit found the "DESCRIPTIVE LINEAGE RELEASE"
   self-label of v9.2 in conflict with rule 4 as written ("a version
   ships at least one developed bridge artifact or it is a version
   note") — the rule predates the user-mandated lineage split. Chosen
   fix: the explicit exception (on the descriptive line a release
   ships a refreshed descriptive digest; the bridge-artifact criterion
   governs the generative line; a version shipping neither is a
   version note on both lines), under which v9.2's label is accurate
   as it stood. The alternative — relabeling v9.2 a version note —
   was rejected on record: it would rewrite user-mandated release
   labeling.
3. **F3 — the RP12 citation-hygiene note restated by name.** The v5
   text's own citations did not resolve and violated the note's own
   cite-by-name rule: P7 is *no brute facts in appearance* (not the
   web/correspondence proposition — those are P17/P20); the
   deducible-in-principle doctrine is the P-present proposition
   together with the derivability boundary (P8 + D10) under the
   **P-present ≠ F-deducible** caveat (J5) — not "P3 + P5 with the J3
   epistemic-only caveat". The J2 (ontological gap) reference in the
   v5 text was correct and survives, now by name ("existence not
   derivable from content"). Numbers are demoted to parenthetical
   anchors, per the rule.
4. **F5 — the "program-stateonly" typo** (lineage appendix, mirror-rule
   paragraph) → "program-state only".

## Verification summary

- 7 designed edits / 8 designed lines (1 title + 1 header note + 1
  rule-4 amendment + 1 hygiene restatement + 1 v9.1 relabel + 2 table
  rows + 1 typo); each old fragment asserted unique before replacement.
- `formalism-v9.2.md` re-read byte-identical after the pass.
- **Part I byte-identical between v9.2 and v9.3** (from "## 0. Status"
  up to "## RP0 — Mission statement") — the lineage invariant asserted
  by the patch script.
- The v9.2 lineage appendix carried forward unchanged except the
  single F5 typo line (unified-diff check).
- Line-level difflib audit: every non-blank changed line matches a
  designed edit marker; no undesigned line touched.
- No proposition, truth-value, derivation, or registry row changed.

## Not done this round (deliberately)

- **F4** (~15 companion audit artifacts absent from the repo; the
  provenance-key rule): not in the directed scope; requires the
  author's own uploads to resolve.
- **F6** (byte-identity claims unverifiable without depositing the
  prior files): likewise author-side.
- The audit's note that manuscript / framework / `absolute.txt` are
  three texts whose attribute inventories do not coincide: recorded in
  the audit; no alignment directed.
