# README_v24_editorial.md — v24: the editorial pass (2026-09-28/29)

**What landed.** The journal-readiness revision of the manuscript and
supplement, executing the user-approved fix order from the v23-review
editorial audit: internal version/meta tokens purged from visible text
(previous-version/now/recomputed/mis-transcription clusters, the
engineering changelog, the gap_utils deposit saga, machine specs, round
names incl. the SM heading "The v22 exact-closure runs"); the two/three-size
framing reconciled — `tab:n5twosize` is now the full size-ladder table with
the L=8 row at all three replica numbers
(`gap12(L=8)` = 0.816 / 0.645 / 0.481 at n=3/4/5; closing factors 6->8 =
1.45 / 1.54 / 1.68; `8 gap12` = 6.53 / 5.16 / 3.85 — the n=4 value mined
from the deposited `v22_n4_eps_topup.json`, extraction validated against
the known L=4/L=6 gaps); the internal changelog source headers and the
orphaned mid-body patch comment stripped; the abstract restructured
(~250 words, headline-first); the DOI note normalized to
`[DOI to be inserted upon public deposition]`; Sec. I retitled
"Introduction, scope, and conventions" with new introductory paragraphs
(section numbering unchanged, so the supplement's hardcoded main-text
references stay valid).

**Files (all new; v21/v22/v23 preserved unmodified).**
- `versions/manuscript_revised_v24.tex/.pdf` — 38 pages, tectonic-compiled.
- `versions/supplement_v7.tex/.pdf` — 11 pages.
- `versions/changelog_v24.md` — the full edit log with verification.
- `versions/certificate_sha256_v11.txt` — ledger v11 (this round).
- `scripts/v22-exactZ3-n5L8/patch_v24_editorial.py` — the patch script
  (47 anchored edits, each asserted).

**No numerical result changed** except the table extension, whose new
cells come verbatim from the deposited chains (see changelog). This is a
presentation-only revision.

**Race note (recorded for provenance):** two agent instances executed this
pass concurrently on 2026-09-28 ~17:50-18:05 UTC (a direct dispatch and
the 01:44 +08 cron firing). The committed build (bec57ee, df91bbd) is the
cron-side instance's; the parallel build was verified equivalent-or-weaker
(its table used em-dashes for n=3/4 at L=8), its uncommitted duplicates
were removed, and the accidentally-rebuilt `manuscript_revised_v23_rung.pdf`
was restored byte-exact from git. Details: worklog Task ID v24-race.

**Known submission prerequisites (user-side):** mint the actual figshare
DOI; decide the venue (assessment delivered: PRR / SciPost Physics primary;
PRX possible, strongest if split into two papers; arXiv first regardless).
Candidate v25 work: the money figure (L*gap12 vs L with the n=3 envelope),
a d=3 rung at L=8 (the orbit table is d-independent), a finer locator grid.
