# Changelog — v29 (layout-polish + metaphysics + data-availability pass)

Date: 2026-10-10 (build 2026-10-10 ~01:2x +0330). Script:
`research/scripts/v22-exactZ3-n5L8/patch_v29_layout_polish.py`.
Sources preserved unmodified: `manuscript_revised_v28.tex` and
`supplement_v9.tex` (and all earlier versions). New files:
`manuscript_revised_v29.tex/.pdf`, `supplement_v10.tex/.pdf`, this
changelog, `README_v29.md`, `certificate_sha256_v16.txt`.

Author asks of this round: (1) TABLE IV and TABLE V exceed the PDF
width/column; (2) Sec. VII uses "metaphysics" instead of "assumption"
throughout (specific opening-paragraph wording supplied); (3) the data
availability statement states formally that the supplementary includes
the web simulation, and figshare becomes preprints.org.

## 1. Column-overflow repair of the tables (and the same defect class)

**Pre-flight measurement** (tectonic on v28, figure present): TABLE IV
(`tab:n5twosize`) overfull by 62.75pt — its `$n=5$ ($p=0.47$)` header
and `$6.85\to4.84$` cells ran past the page edge (words to x=614 on a
612pt page); TABLE V (`tab:closingrates`) overfull by 30.76pt — its
header crossed 25pt into the neighbouring column's text zone. The same
defect class then measured on the rest of the document: TABLE VI
(`tab:smchaar`) overfull 94.98pt (cells to x=615, past the page edge),
TABLE IX (`tab:numerics`) overfull 46.36pt (cells to x=606), and two
display equations so wide that parts of their content fell outside the
page box and were invisible in the rendered PDF.

**Fix.** All four tables are promoted from single-column floats to
two-column-spanning floats (`table*`), the format TABLE I already
uses. The tabular bodies are carried **byte-identical** (asserted in
the patch script by exact substring comparison of each table's
tabular block), so no number, label, caption, or table number changes
(TABLE IV/V/VI/IX keep their numbers; `\ref`s unaffected).

**Post-fix verification.** tectonic on v29: zero alignment overfulls;
word-level bbox scan of the rendered PDF finds no content past the
column edges (the remaining flags are the intentional full-width
title block of page 1 and words *inside* the now-legitimate full-width
`table*` regions); VLM inspection of the four table pages confirms
full-width, cleanly typeset tables with nothing cut off.

## 2. The clipped display equations (content invisible in v28)

In the closed-form-spectrum proposition (Sec. II.E), eq. (48)
(`eq:QRdef`, overfull 163.42pt) rendered **without the definition of
R(k)** — it fell outside the page box — and eq. (50) (`eq:spinor`,
overfull 207.00pt) rendered **without the $\tilde Y$ and $U_k$
factors**. Both are re-set as multi-line displays:

- eq. (48): `aligned`, the Q(k) definition broken at the final minus
  term, R(k) on its own line — every token preserved (audited in the
  patch script); the rendered PDF now shows "Q(k)=..., R(k)=2 sinh
  2K_d cos(k/2)" in full;
- eq. (50): `gathered`, the E factorization on line 1, the $\tilde Y$
  and $U_k$ definitions on line 2 — every token preserved; the
  rendered PDF now shows all three factors;
- eq. (87) (`eq:dyadicmoments`, overfull 11.32pt): separator
  `\qquad` → `\!\quad`; no longer overfull.

Equation numbering is unchanged (each remains a single numbered
equation).

## 3. Item-label repair (Proposition 11)

The enumerate of `prop:gap` began on the same paragraph line as the
proposition header, so the item label "(i)" was typeset at the end of
the header line and protruded 19pt into the margin (overfull
23.09pt). A `\leavevmode` now separates the header from the enumerate;
the label starts the item line exactly as every other enumerate of the
paper renders. No text changes.

## 4. Metaphysics terminology (Sec. VII)

Per the author's wording, the opening paragraph now reads: "**The
standing metaphysics.** This section records the working assumption
maintained with this project's research record and examines what it
implies for the readings of quantum mechanics." — the metaphysics is
established once, as the working assumption, and thereafter referred
to by its descriptive, ontological name. All further occurrences of
"assumption"/"assumption's" inside Sec. VII (sixteen sites across the
six paragraphs) become "metaphysics" or an equivalent grammatical
form (three possessive constructions are re-phrased to avoid the
awkward possessive: "the metaphysics having no external vantage
point", "the circularity thesis of the metaphysics", "that
circularity"). The introduction's logical-spine entry describing
Sec. VII follows ("states the standing metaphysics and its
reconciliation conditions"). Audited in the patch script: exactly one
"assumption" survives in Sec. VII (the opening "working assumption"),
seventeen "metaphysics" occurrences; outside Sec. VII only the
mathematical "self-averaging assumption" remains. No theorem, number,
or claim changes; the section remains explicitly non-load-bearing.

## 5. Data availability

The deposit host changes from figshare to **preprints.org** (DOI to
be assigned prior to submission), and the statement now records
formally: "The Supplementary Material includes the web simulation of
the monitored circuits: an interactive stabilizer-tableau simulator
of the Clifford dynamics of Appendix D, with the finite-size-scaling
benchmark, the annealed replica chain, and the record SCGF analyses
of the paper presented in interactive form." The deposited-artifact
list (two-replica release, rank certificates, stabilizer simulator,
raw trajectories, ledgers) is preserved verbatim.

## 6. Supplement v10 (same defect class, discovered in the round's scan)

- The SMC weight display of Sec. S6 (overfull 74.03pt; its $\bar w$
  term fell outside the page box) is split into two align lines,
  every token preserved; the rendered PDF now shows all three
  definitions.
- The calibration table `tabS:calib` (overfull 91.53pt, cells
  crossing into the neighbouring column's text) is promoted to a
  `table*`; tabular byte-identical.
- The reproduction command/purpose block (overfull 260.94/265.64pt —
  the centered tabular rendered **on top of** the right column's
  text) is re-set as an itemized list; both commands and their
  purposes are verbatim.
- Six literal label-name references (rendered as raw label strings in
  v9: "Remark rem:cliff3design", "Prop. prop:z3closure" ×2, "Table
  tab:z3exact", "Table tab:n5twosize", "Table tab:closingrates") and
  three label-style equation pointers ("Eq. (rank3)", "Eq.
  (dyadicmoments)", "Eq. (Wpn)" ×2) are replaced by the explicit
  numbers of the main text (Remark 7, Proposition 13, Tables IV/V/VII,
  Eqs. (55)/(87)/(14)) — the convention the supplement already uses
  elsewhere ("Theorem 8 of the main text", "Table II of the main
  text", ...). The patch script asserts no label-name strings remain.
- Post-fix: zero overfull boxes; no unresolved references; the
  reproduction block renders cleanly in its column (VLM-verified).

## 7. No-content-loss verification (inside the patch script)

- The four promoted tabular bodies: byte-identical to v28/v9
  (exact-substring assertion per table).
- The three re-set displays: token-preservation audit (every math
  token of the old body occurs in the new body).
- Line-multiset audit over visible lines (house protocol): manuscript
  1751 visible v28 lines − 12 deliberately edited lines all survive
  in v29 (1757 visible lines; the five added lines are the
  `aligned`/`gathered`/`\leavevmode` structure lines); supplement 876
  visible v9 lines − 19 deliberately edited lines all survive in v10
  (876 visible lines). Structural lines (float environments, `\hline`,
  list delimiters) are excluded from the multiset and verified by the
  byte-level checks.
- Submission-cleanliness scan: zero hits for TODO/FIXME/placeholder/
  diary/meta/infrastructure vocabulary in both files.

## 8. Known cosmetic residue (pre-existing, left as is)

A 1.78pt paragraph overfull (sub-visible) and two inter-column-gap
bleeds of 5.9pt/7.2pt that do not reach the neighbouring column's
text — all three present in v28 identically and invisible at print
size. Page counts: manuscript 42 pages (v28: 41), supplement 12 pages
(v9: 12).

## 9. Open author actions

preprints.org DOI minting; optional TJP template transcode; deletion
of the campaign cron jobs 431600/431599 (still firing harmlessly as
no-ops; needs a user-facing session with the scheduler tool present).
