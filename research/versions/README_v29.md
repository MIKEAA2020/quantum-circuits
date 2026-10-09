# README — v29 (layout-polish + metaphysics + data-availability pass)

**Deliverable (current submission candidate):**
`manuscript_revised_v29.tex/.pdf` + `supplement_v10.tex/.pdf`,
built by
`research/scripts/v22-exactZ3-n5L8/patch_v29_layout_polish.py`
from the canonical v28 (`manuscript_revised_v28.tex`) and the v9
companion (`supplement_v9.tex`), both preserved unmodified alongside
all earlier versions. Changelog: `changelog_v29.md`; ledger:
`certificate_sha256_v16.txt`. Standing document: `absolute.txt`
(repository root, author-uploaded, preserved verbatim).

## Version map (this round)

- **v28** (previous): the demotion + interpretive-status pass —
  Sec. III's worst-case complexity subsection demoted verbatim to
  Appendix C; new Sec. VII "Interpretive status of the record
  formalism" stating the standing metaphysics and reconciling the
  work with it; six new bibliography entries.
- **v29** (this pass): the layout-polish + metaphysics +
  data-availability pass — (1) the four column-overflowing tables
  (IV, V, VI, IX) promoted to two-column `table*` floats, tabular
  bodies byte-identical (the author-reported TABLE IV/V overflow and
  the two further tables the round's scan measured); (2) the two
  clipped displays of the closed-form spectrum (eqs. (48) and (50),
  whose R(k) resp. $\tilde Y$/$U_k$ definitions fell outside the page
  box in v28) re-set as multi-line displays with every token
  preserved, eq. (87) tightened; (3) the "(i)" label of
  Proposition 11's enumerate detached from the proposition header
  (was protruding 19pt into the margin); (4) Sec. VII refers to the
  standing metaphysics as metaphysics throughout, established once as
  the working assumption (author's wording), incl. the intro spine
  entry; (5) data availability: preprints.org replaces figshare and
  the supplementary's web simulation is stated formally; (6)
  supplement v10: the SMC weight display split (was clipped off-page),
  the calibration table promoted to `table*`, the reproduction block
  re-set as a list (was rendering on top of the neighbouring
  column), and six literal label-name references replaced by the
  explicit main-text numbers (Remark 7, Proposition 13, Tables
  IV/V/VII, Eqs. (55)/(87)/(14)).

## Layout QA state (v29, measured)

- tectonic overfull boxes: manuscript — only a pre-existing 1.78pt
  sub-visible paragraph overfull (identical in v28); supplement —
  zero. All nine v28/v9 defect sites (four tables, two clipped
  equations, one 11pt equation, one 23pt item label, one clipped
  supplement display, one colliding supplement table, one colliding
  supplement reproduction block) eliminated.
- Word-level bbox scans of both rendered PDFs: no content past the
  column/page edges (page-1 title block and full-width `table*`
  regions are intentional); VLM page inspections confirm the four
  promoted tables and both repaired equation regions render
  completely and cleanly.
- Content audits inside the patch script: byte-identical tabulars,
  token-preserving equation re-sets, line-multiset audits (manuscript
  1751→1757 visible lines, 12 edited; supplement 876→876 visible
  lines, 19 edited), Sec. VII terminology audit (1 "assumption", 17
  "metaphysics"), no label-name strings, no figshare, no informal
  vocabulary.

## Simulation currency

The quenched Clifford FSS benchmark (Appendix D) and the
`mipt_numerical_report` series are untouched by this pass; the web
simulation (repository `web-explorer/`) is unchanged and is now
formally referenced in the data availability statement. Title,
keywords, and abstract unchanged.
