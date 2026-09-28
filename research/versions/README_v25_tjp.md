# README_v25_tjp.md — the v25 Turkish Journal of Physics targeting pass

## What this version is

`manuscript_revised_v25_tjp.tex/.pdf` is the submission-shaped revision of
`manuscript_revised_v24.tex` targeted at the **Turkish Journal of Physics**,
produced by the user-approved editorial pass of 2026-09-28/29.  v21–v24 are
preserved unmodified alongside it (no-overwrite convention).  The companion
supplement is unchanged: **`supplement_v7.tex/.pdf`** remains the current SM.

## What changed relative to v24

1. **Dedicated `\section{Conclusion}`** before the Declarations — five
   paragraphs: (i) the exact mechanics; (ii) the annealed ladder and the
   three-size first-order test at $n=5$; (iii) the Born-weighted and record
   objects; (iv) a referee-facing summary of the exactness/verification
   layer (certificates, anchors, cross-route agreement, checksummed
   deposits, bounded roundoff residual); (v) significance and outlook,
   including the three approved extensions (the $d=3$ rung at $L=8$, the
   finer $p$-grid around the $n=5$ locator, interface-tension/latent-heat
   extraction).
2. The Discussion's unresolved-questions mega-paragraph split into five
   paragraphs (pure breaks, zero text changes).
3. `\label{conj:continuum}` added to the conditional-continuum conjecture;
   the Introduction's logical spine now points to the Conclusion.
4. No physics content, number, table, title, abstract or keyword changed.

## How it was built and checked

```
python3 research/scripts/v22-exactZ3-n5L8/patch_v25_tjp.py   # 9 anchored edits, all unique
cd research/versions && tectonic manuscript_revised_v25_tjp.tex
pdftotext manuscript_revised_v25_tjp.pdf -                   # 39 pp; order and refs verified
```

Details and verification record: `changelog_v25.md`; checksums in
`certificate_sha256_v12.txt`.

## Venue notes (TJP)

- Keywords, ORCID, funding/competing-interests/ethics/AI-declaration and
  data-availability statements are present and TJP-compatible.
- The manuscript keeps the `revtex4-2` (APS, reprint) class; convert to the
  journal template at submission if the editors require it — the source is
  plain LaTeX apart from the class options.
- **Author actions before submission:** mint the figshare DOI (the
  Declarations still say "DOI to be assigned prior to submission") and
  confirm the final author list/affiliation.

## Relationship to the running extension compute

The v25 **compute** extension (`v25_n5_L8_ext_v1.py`: the $d=3$ rung at
$L=8$, the finer $d=2$ locator grid, the $d=3$ locators at $L=4/6$) is a
separate, parallel campaign whose results will be deposited first and only
then promoted into a **v26** manuscript — the version number v25 is reserved
for this editorial pass.  Coordinate through `/home/z/my-project/worklog.md`
(Task IDs `v25-tjp`, and the compute round's own entry) before building.
