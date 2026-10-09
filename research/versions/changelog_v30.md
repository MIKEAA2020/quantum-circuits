# Changelog — v30 (web-simulation hosting pass)

Date: 2026-10-10 (build 2026-10-10 ~00:2x +0330). Script:
`research/scripts/v22-exactZ3-n5L8/patch_v30_webhost.py`.
Source preserved unmodified: `manuscript_revised_v29.tex` (and all
earlier versions). New files: `manuscript_revised_v30.tex/.pdf`, this
changelog, `README_v30.md`, `certificate_sha256_v17.txt`. Companion
`supplement_v10.tex/.pdf` carried forward unchanged (no
web-simulation or deposit-host reference exists in the supplement; the
ledger re-hashes it).

Author asks of this round: the data availability statement should GIVE
THE URL of the web simulation, hosted on GitHub, instead of stating
that the Supplementary Material includes it — with the standalone
archive built and committed for that purpose.

## 1. The web simulation artifact (new this round, outside the versions tree)

`web-simulation/index.html` — the interactive companion of the paper as
ONE self-contained offline HTML file (737 KB: React, the Clifford
engine, all deposited data, and the stylesheet inlined; zero network at
runtime; works from `file://` by double-click). It is the full
explorer: the live Gottesman–Knill tableau simulator with gate-by-gate
circuit visualization (pure-state I₃ and purification S_ref), the
deposited purification dataset with the interactive data-collapse
explorer (p_c/ν sliders, χ² quality gauge), the I₃ crossing-sweep
explorer with trajectory-level bootstraps and an L = 128/256 chunked
background-job runner, the annealed replica chain and record SCGF
analyses, and the reproducibility inventory. The server-side
ensemble/sweep API of the hosted build is reproduced by an in-page
fetch shim over the SAME pure-TypeScript Clifford drivers with the
SAME seed contracts, so every number the file produces is bit-identical
to the hosted explorer; records persist in localStorage (seeded with
the deposited board content: 5 sweeps, 1 saved run).
`web-simulation/web_simulation.zip` (210 KB) wraps index.html +
README.txt for archival/supplementary upload. `.nojekyll` markers
committed at the repository root and inside the folder.

Browser verification (file://, agent-browser): 58 canvas/SVG charts
render; zero console/page errors; ensemble endpoint reproduced
bit-identically through the shim (200 trajectories, 274 ms, seeds
1000…1199, values agreeing with the deposited table ≤3σ); run saving
and board load/save/delete work over localStorage; the L = 128
background job completes point-by-point (9 pts, [0.080…0.240]); mobile
390 px viewport shows no horizontal overflow; computed-style checks
confirm the inlined stylesheet resolves (zinc-950 body, radius
variables, html background).

## 2. The data-availability edit (the manuscript change, in full)

The v29 sentence

> The Supplementary Material includes the web simulation of the
> monitored circuits: an interactive stabilizer-tableau simulator of
> the Clifford dynamics of Appendix~\ref{app:numerics}, with the
> finite-size-scaling benchmark, the annealed replica chain, and the
> record SCGF analyses of the paper presented in interactive form.

becomes

> The web simulation of the monitored circuits---an interactive
> stabilizer-tableau simulator of the Clifford dynamics of
> Appendix~\ref{app:numerics}, with the finite-size-scaling benchmark,
> the annealed replica chain, and the record SCGF analyses of the paper
> presented in interactive form---is hosted at
> \url{https://mikeaa2020.github.io/quantum-circuits/web-simulation/}.

Every description clause is carried verbatim (asserted in the patch
script, count == 1 per clause); only the framing changes
(supplementary inclusion → hosted address).  `hyperref` is loaded, so
`\url` typesets and hyperlinks the address.  The deposited-artifact
list, the preprints.org DOI sentence, and everything else in the paper
are untouched.

## 3. Verification

- Patch-script audits: old sentence unique (count == 1); new URL
  present exactly once; `figshare` count 0; deposited-artifact anchors
  (`release\_checksums.sha256`, `certificate\_sha256.txt`, `npz`,
  `app:rank3`, `app:numerics`, DOI-to-be-assigned phrase) all survive;
  both description clauses carried verbatim.
- Line-multiset no-content-loss audit: 1775 visible v29 lines → 1775
  visible v30 lines, exactly 1 deliberately edited (the data-availability
  line). Zero content loss.
- Forbidden-token scan (visible text): clean.
- tectonic build: `manuscript_revised_v30.pdf`, 42 pages (v29: 42),
  604.85 KiB (v29: 604.23 KiB). Overfull scan: only the pre-existing
  1.77626pt sub-visible paragraph overfull at line 1851 — the same
  one documented in the v29 audit (identical in v28), repeated across
  tectonic's six internal passes; ZERO new overfulls. Two mild
  underfull hboxes (badness 2875/1168) at lines 1963/2030 sit in
  content unchanged from v29 (the CPD corollary and a bibliography
  entry) — pre-existing typesetting looseness, cosmetic.
- Rendered-content check (pdftotext): the full new statement renders
  with the URL intact and hyperlinked; zero `??` unresolved references.
- Page count parity: 42 = 42 (the statement edit is length-neutral at
  the paragraph scale).

## 4. Hosting status note

The repository is fully prepared for GitHub Pages branch-source
serving (`.nojekyll` at root; `web-simulation/index.html`): the address
https://mikeaa2020.github.io/quantum-circuits/web-simulation/ goes live
when the repository owner enables Pages with source "Deploy from a
branch: main / (root)". The session's fine-grained PAT carries
Contents read/write only (Pages/Workflows API scopes absent), so the
one-time repository setting remains a single owner action; the URL
cited in the manuscript is the deterministic outcome of that setting.
