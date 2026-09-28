# Changelog — v24 (editorial pass)

Date: 2026-09-29 (build 2026-09-28 18:01 UTC). Script: `patch_v24_editorial.py`.
Sources preserved unmodified: `manuscript_revised_v23_rung.tex`, `supplement_v6.tex` (and all
earlier versions). New files: `manuscript_revised_v24.tex/.pdf`, `supplement_v7.tex/.pdf`,
this changelog, `certificate_sha256_v11.txt`.

Scope: the user-approved editorial fix order — (1) purge internal version/meta tokens,
(2) reconcile two-size/three-size claims, (3) strip source comments, (4) abstract restructure,
(5) DOI note normalization, (6) Introduction work. No numbers changed except where stated.

## 1. Version/meta-token purge (visible text)

Manuscript:
- Sec. II.G: "replacing the two-size proxy of the previous version" — clause removed;
  "revises to ... the lower edge of the previous bracket" -> "is $p_c^{(4)}\approx0.383$";
  "the previously missing $L=8$ $\varepsilon$ values now recomputed (the deposited chain
  stopped ... un-deposited projection ...)" -> "the $L=8$ $\varepsilon$ values (extended
  scan, Supplement, Sec. S7)".
- Sec. II.G: the engineering paragraph (BLAS ring contraction: "The decisive two-size test
  is now done", 5.4 s/2.9 s per matvec, two cores, cache-hostile temporaries of "the
  previous implementation", 500 MB vs 2.3 GB, 11-21x speedup) condensed to the physics
  content with a pointer to the Supplement; the timings moved to Supplement Sec. S7.
- Sec. II.G: "now supplies the third size" -> "supplies"; "no longer a prediction ...
  but" -> "not a prediction ... alone but"; rung paragraph now defines the term ("the
  third rung of the size ladder $L=4,6,8$").
- Sec. III (records): the "earlier t=4L reading being a mis-transcription" erratum note
  replaced by the stated convention + calibration pointer.
- Sec. IV: "The trajectory estimates of the previous version ... are superseded by" ->
  "Trajectory estimates (...) are superseded by" (method contrast kept, version framing
  removed).
- Sec. IV: "corrected v21 anchors" -> "corrected $\beta=1$ anchors"; "exceeds the present
  memory budget" -> "exceeds the memory available for exact dense treatment";
  "$L=24$ ... now run/is now measured" family removed.
- Discussion: "now exist / now extends / now proves / now supplies / now measured /
  now an exact" narration removed (6 sites); "two-size confirmation ... confirmed at the
  two-size level for $n\le5$ (three sizes at $n=5$)" -> "size-ladder confirmation ...
  confirmed at the three-size level for $n=5$".
- app:files: gap_utils reconstruction narrative ("the original was missing from the
  deposit, breaking the reproduction chain of the v17-v19 scripts") -> neutral validation
  statement; "The v22 exact-closure suite" -> "The exact-closure suite" (2 sites).
- app:numerics: "The present revision re-verified the recovered dataset" -> "The dataset
  was re-verified end to end"; "recovered dataset" -> "deposited dataset" (2 more sites).
- Abstract: rewritten (see 4) — the "now resolved" narration gone.
- All residual \bnow\b in visible text: 860-word abstract excluded, zero remaining.
- Source: 49-line internal changelog header replaced by a 7-line provenance header;
  orphaned mid-body comment block ("v19 staged LaTeX fragments ... patch_v19_twosize.py")
  removed.

Supplement (v7):
- Section heading "The v22 exact-closure runs" -> "The exact-closure runs: $\bar Z_3$,
  the Clifford design, and the $n=5$ $L=8$ block".
- Intro: "the v22 exact-closure suite ... reconstructed gap_utils library" -> neutral.
- S4 ledger note: "the v21 round / the v22 round" -> "the Clifford record-count round /
  the exact-closure round"; the "repair the reproduction chain of the v17-v19 scripts"
  clause neutralized.
- S7.4 first paragraph: "was missing from the repository: the deposit's reproduction
  chain was silently broken. It is rebuilt ..." -> "is included in the deposit ... It is
  validated by re-running the deposited batteries unmodified".
- "recomputes the missing $L=8$ $\lambda_\varepsilon$ values" -> "extends the $L=8$
  $\lambda_\varepsilon$ scan"; "of the v21 Discussion" -> "anticipated in the main-text
  Discussion"; "are NOT used ... flagged" -> "are not used ... for completeness";
  "the v23 rung completion (..., manuscript_revised_v23_rung) is hashed" -> version-free.
- Source header (12 lines of version notes) replaced by a 4-line provenance header.
- The S7 "mis-transcription" erratum sentence -> "the ``$t=4L$'' reading of this chain is
  excluded by the calibration (at $t=4L=32$ one instead gets $Z_2=4.57\times10^{-18}$,
  twenty-nine orders away)."
- Reproduction paragraph gains the timing/memory note moved from the main text.

## 2. Two-size/three-size reconciliation

- Sec. I Scope: "two-size confirmation" -> "three-size confirmation" (the stale sentence).
- Sec. II.C closing sentence: "two-size test that confirms" -> "size-ladder test
  ($L=4,6,8$) that supports ... at the three-size level".
- Table `tab:n5twosize` retitled "The $n=5$ size-ladder test" and extended with the
  $L=8$ rung rows, making the three-size comparison uniform across $n$:
  - $\mathrm{gap}_{12}(L{=}8)$: $n=3$: $0.816$ (from the deposited $n=3$ chain, the
    quoted $8\,\mathrm{gap}_{12}=6.53$); $n=4$: $0.645$ (NEW: from the deposited
    $\lambda_\varepsilon$ top-up `results/v22-exactZ3-n5L8/v22_n4_eps_topup.json`,
    $p=0.38$ cell, $\lambda_1=2.18531\times10^{-3}$, $\lambda_\varepsilon=1.14715\times
    10^{-3}$; the $p=0.38$ anchor was verified to $5.7\times10^{-16}$ against the
    deposited value; extraction method validated against the known $L=4$ and $L=6$ gaps
    $1.919/0.990$); $n=5$: $0.481$ (rung JSON).
  - closing factor $L{=}6\to8$: $1.45$ / $1.54$ / $1.68$ — the ordering continuous
    ($n=3$) $<$ marginal ($n=4$) $<$ first-order ($n=5$) persists at the third size.
  - $8\,\mathrm{gap}_{12}$: $6.53$ / $5.16$ / $3.85$ — only $n=5$ falls below the
    continuous envelope at $L=8$.
- Caption updated with the provenance of the $L=8$ column.

## 3. Source-comment strip

Both files: internal version-history header comments replaced by short provenance
headers; no mid-body patch comments remain. The detailed history stays in the
changelog_*.md files.

## 4. Abstract restructure

860-word single-paragraph inventory -> ~250-word abstract carrying the three headline
contributions (exact replica mechanics + Ising identification; the annealed ladder
$n=2..5$ with the three-size first-order confirmation at $n=5$; the record program with
no-freezing, first quenched record SCGFs, and the Clifford 3-design closure). The detailed
results inventory remains in Sec. I.

## 5. DOI note

"[placeholder DOI]" + fake href -> "are deposited on figshare (DOI to be assigned prior
to submission)." (Figshare DOI cannot be minted from this environment; the author must
create it at submission.)

## 6. Introduction

Sec. I retitled "Introduction, scope, and conventions" and opens with four new
paragraphs: field context, the first contribution (exact replica mechanics + Ising
solution), the second (the annealed replica ladder with the three-size first-order
confirmation), the third (Born separation + record program), and the annealed/quenched
delimitation. The section numbering is unchanged (no new \section), so all hard-coded
main-text references in the Supplement (Secs. II.F/IV, Appendix A, Eq. (Wpn), Eq. (A1),
Table II) remain valid.

## Verification

- Every patch anchor asserted unique (count==1) before application; 47 edits total
  (41 manuscript, 6 supplement + header/abstract replacements).
- Residual-token report on the outputs (visible lines only): forbidden phrases = 0;
  stray \bnow\b = 0; remaining v-tokens only inside \texttt{...} deposit filenames.
- tectonic compile: both PDFs built (manuscript 570.96 KiB, supplement 210.47 KiB);
  warnings unchanged from v23 (underfull hbox, one pre-existing hyperref
  "proposition.12" destination note, bbl-rerun note).
- PDF text extraction confirms the new abstract, the new Introduction, and the new
  size-ladder table rows.
