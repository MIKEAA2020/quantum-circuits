# README — v30 (web-simulation hosting pass)

**Deliverable (current submission candidate):**
`manuscript_revised_v30.tex/.pdf` + `supplement_v10.tex/.pdf` (companion,
carried forward unchanged), built by
`research/scripts/v22-exactZ3-n5L8/patch_v30_webhost.py`
from the canonical v29 (`manuscript_revised_v29.tex`), preserved
unmodified alongside all earlier versions. Changelog: `changelog_v30.md`;
ledger: `certificate_sha256_v17.txt`. Standing document: `absolute.txt`
(repository root, author-uploaded, preserved verbatim).

## Version map (this round)

- **v29** (previous): the layout-polish + metaphysics +
  data-availability pass — the four column-overflowing tables (IV, V,
  VI, IX) promoted to two-column `table*` floats with byte-identical
  tabulars; the two clipped displays of the closed-form spectrum
  re-set with every token preserved; Sec. VII refers to the standing
  metaphysics as metaphysics throughout; data availability named
  preprints.org and stated the supplementary's web simulation
  formally.
- **v30** (this pass): the web-simulation hosting pass — the data
  availability statement now GIVES THE URL of the web simulation,
  hosted on GitHub
  (`https://mikeaa2020.github.io/quantum-circuits/web-simulation/`),
  replacing the supplementary-inclusion framing; every description
  clause carried verbatim (asserted). The web simulation itself is
  built and committed: `web-simulation/index.html` — one
  self-contained offline HTML file reproducing the full interactive
  explorer bit-identically (in-page fetch shim over the same
  pure-TypeScript Clifford drivers, same seed contracts; localStorage
  persistence seeded with the deposited board), plus
  `web_simulation.zip` (210 KB) for archival upload; `.nojekyll`
  markers for Pages serving.

## The single edit, in full

The data-availability sentence changes from "The Supplementary Material
includes the web simulation of the monitored circuits: … presented in
interactive form." to "The web simulation of the monitored
circuits---… presented in interactive form---is hosted at
\url{https://mikeaa2020.github.io/quantum-circuits/web-simulation/}."
Nothing else in the manuscript or the supplement changes.

## Verification summary

- Line-multiset audit: 1775 visible lines → 1775, exactly 1 edited,
  zero content loss; both description clauses verbatim; figshare 0;
  deposited-artifact anchors intact.
- tectonic: 42 pages (v29: 42), 604.85 KiB; zero new overfulls (only
  the pre-existing 1.78pt sub-visible paragraph overfull, documented
  since v28); zero `??` refs; the URL renders and is hyperlinked.
- The standalone archive is browser-verified via `file://` (agent
  browser): 58 charts, zero console/page errors, ensemble bit-parity,
  saves/board/jobs (L = 128 chunked) all green, mobile 390 px clean.

## Hosting

Repository fully prepared (`.nojekyll` at root + `web-simulation/`): the
cited address goes live when the owner enables GitHub Pages with source
"Deploy from a branch: main / (root)" (the session PAT lacks the Pages
API scope; the URL is the deterministic outcome of that one setting).
