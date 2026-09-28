# changelog_v25.md — the TJP targeting pass (manuscript_revised_v25_tjp.tex)

Built by `patch_v25_tjp.py` from the deposited `manuscript_revised_v24.tex`
(preserved unmodified, like all predecessors).  Companion `supplement_v7.tex`
is unchanged by this pass.  Date: 2026-09-28 (session of 2026-09-29 +08).

User directive: target the Turkish Journal of Physics; convince referees that
the exact results are correct, that the numerical evidence is compelling, and
that the advance is significant; structure the full manuscript clearly with a
dedicated Conclusion section.

## Edits (each anchored and asserted unique before application)

- **E1 — provenance header.**  Source header comment replaced with the v25
  provenance block (scope, companion, ledger).
- **E2 — conjecture label.**  `\label{conj:continuum}` added to the
  conditional-continuum conjecture so the Conclusion can reference it.
- **E3 — dedicated Conclusion (`\section{Conclusion}`, `\label{sec:conclusion}`).**
  Inserted between "Discussion and open problems" and the Declarations; five
  paragraphs:
  1. the exact mechanics (minimal invariant algebra, leakage + exact Haar
     closure, $\mathsf A\mathsf A^\dagger$ spectrum, the $n=2$ Ising
     identification with $p_c^{(2)}=0.2338$ closed form);
  2. the annealed ladder $n=3,4,5$ and the three-size first-order test at
     $n=5$ (orbit basis $3{,}865$ over $120^4=2.1\times10^8$ bond labels;
     closing factors $1.81/1.94/2.12$ and $1.45/1.54/1.68$;
     $L\,\mathrm{gap}_{12}=3.85$ vs the $6.53$ continuous envelope);
  3. the Born-weighted and record objects (no-go + bivariate recovery,
     PP-hardness, the no-freezing theorem, the interpolation identity and
     self-averaging criterion, the first quenched record SCGFs, the Clifford
     conjugation-$3$-design closure);
  4. the exactness/verification layer (referee-facing): rank certificates
     with no floating point in any proved statement, Collatz–Wielandt
     rational-point certification, the Kaufman/Ising $3\times10^{-15}$
     anchor, the exact $p=1$ rank-one anchor for $n=2,\dots,5$,
     compressed-vs-full agreement $4\times10^{-16}$, assembler-vs-deposit
     $1.6\times10^{-14}$, Arnoldi cross-checks $<2\times10^{-15}$, checksum
     ledgers, and the bounded float-roundoff residual;
  5. significance and outlook (the controlled calibration target role, the
     receding annealed points, and the three approved extensions: the $d=3$
     rung at $L=8$, the finer $p$-grid, interface-tension/latent-heat
     extraction).
  Every number is verbatim from v24 and the deposited results; no new claims
  and no new "first"s beyond those v24 already makes.
- **E4–E7 — Discussion readability.**  The unresolved-questions mega-paragraph
  split at four sentence boundaries into five paragraphs (n≥3 operators;
  complexity; record large deviations; disorder-replica interchange; the
  continuum program).  Pure paragraph breaks — zero text changes.
- **E8 — Introduction spine.**  The logical-spine sentence now ends
  "…Sec.~\ref{sec:aux} delimits what remains conditional;
  Sec.~\ref{sec:conclusion} concludes."

## Deliberately unchanged

- Title, abstract, keywords, all physics content, all tables, the
  Declarations text (incl. the figshare DOI placeholder — author action:
  mint the DOI before submission), the appendices, and `supplement_v7.tex`.
- The two "superseded" tokens flagged by the residual scan are pre-existing
  v24 text comparing estimates against exact closures (scientific usage, not
  version meta-talk) and are intentionally kept.

## Verification

- `patch_v25_tjp.py`: 9 edits, all anchor counts == 1; post-checks assert the
  Conclusion heading, `sec:conclusion`, `conj:continuum` and the spine pointer
  each appear exactly once; residual-token report clean (2 pre-existing
  legitimate "superseded" uses only).
- `tectonic manuscript_revised_v25_tjp.tex`: success, 592,645-byte PDF,
  warnings identical to the v23/v24 baseline (underfull hboxes, the
  pre-existing `proposition.12` hyperref note, the bbl-rerun note).
- `pdftotext`: 39 pages (v24: 38); section order Discussion < Conclusion <
  Declarations confirmed; the Conclusion body, the three-size numbers
  (3.85 / 6.53 / 1.68), K = 3,865, the conjecture reference and the spine
  pointer all render; zero unresolved `??` references.

## Provenance

- Patch script: `research/scripts/v22-exactZ3-n5L8/patch_v25_tjp.py`.
- Checksums: `certificate_sha256_v12.txt`.
- Build log: this file; run record in `/home/z/my-project/worklog.md`
  (Task ID `v25-tjp`).
