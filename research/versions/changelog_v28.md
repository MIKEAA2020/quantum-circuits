# Changelog — v28 (demotion + interpretive-status pass)

Date: 2026-10-09/10 (build 2026-10-09 16:2x UTC). Script:
`research/scripts/v22-exactZ3-n5L8/patch_v28_absolute_interpret.py`.
Source preserved unmodified: `manuscript_revised_v27.tex` (and all
earlier versions). New files: `manuscript_revised_v28.tex/.pdf`, this
changelog, `README_v28.md`, `certificate_sha256_v15.txt`. Companion
submission files unchanged this pass: `supplement_v9.tex/.pdf`.

Provenance note: this pass executes the author decision recorded in
the v27 QA round — the demotion review of that round reported the
candidates; this pass demotes the clear candidate, decides the
optional one, and adds the interpretive-status section the author
requested. The standing document `absolute.txt` was uploaded to the
repository by the author directly (GitHub web upload, commits
5717619/144b628, 2026-10-09) and is preserved verbatim and unmodified;
the interpretive section is aligned to the author's document, not to
any reconstruction of it.

## 1. The demotion (Sec. III.B → Appendix C), zero content loss

**What moved.** The 47-line subsection "Precisely promised trajectory
complexity" (gate-set conventions; the CTD definition; the
PostBQP-completeness proposition with its full proof; the
conditional-expectation estimation corollary with proof; the
conditional-purity decision corollary with proof; the
BQP-estimability boundary paragraph) moved **verbatim** to the new
**Appendix C** of the same title (`app:complexity`), inserted after
Appendix B (the FSS benchmark) and before the bibliography.

**What replaced it.** A compact summary subsection
(`sec:ctd`, "Worst-case trajectory complexity") in Sec. III that
states every result in full — CTD and its PostBQP-completeness with
the architecture/terminal-postselection persistence, both estimation
corollaries, the BQP-estimability boundary of the moment family
M(j,k), and the worst-case scope caveats — with pointers to
Appendix C for the definitions and proofs. A main-text-only reader
loses no statements, only the proofs.

**No-content-loss verification (inside the patch script, re-runnable).**
Two independent assertions: (i) the demoted body appears as an exact
substring, exactly once, in the v28 output (byte-identical carry);
(ii) a line-multiset audit over all visible (non-comment, non-blank)
lines: 1746 visible v27 lines, 6 deliberately edited lines excluded,
all remaining 1740 lines survive in v28 with at least their original
multiplicity. The diff between v27 and v28 is confined to the
designed hunks: header, spine line, the demotion pair, three
cross-reference lines, the interpretation-section insertion, the
appendix insertion, and the bibliography entries.

**Cross-reference updates (5 sites):** the intro spine (complexity
pointer + the new section's spine entry), the Clifford remark
("worst-case PostBQP completeness of Appendix~C"), the Discussion
paragraph, the Conclusion deliverables list, and the summary
subsection's own pointers.

## 2. The no-freezing decision: NOT demoted (author-directed criterion)

The no-freezing proof body of Sec. IV.C (157 lines) was evaluated
under the author's criterion — "demote only if merited and helpful
for readability/presentation" — and **kept in the main text**. The
recorded reasons: (i) both constituent results (the no-freezing
theorem, the replica interpolation identity) are headline
contributions named in the abstract, the introduction, and the
Conclusion; (ii) the following SMC subsection builds directly on the
self-averaging criterion that the interpolation identity introduces;
(iii) the paper's presentation brand is exactness-on-display, and the
page budget is not binding; (iv) the supplement carries the *freezing*
counterexample's proof, so the main text carrying the *no-freezing*
theorem preserves the dichotomy balance that Remark `rem:dichotomy`
articulates. The counterpoint recorded in the v27 QA round was
weighed and accepted.

## 3. The interpretive-status section (new Sec. VII)

`sec:interpretation` ("Interpretive status of the record
formalism"), between the Discussion and the Conclusion. It states
the author's standing working assumption — the **non-dual Absolute**
of `absolute.txt`: reality as pure self-luminous awareness,
universal consciousness; self-existent, timeless, spaceless,
unchanging, complete, non-dual, without relations, parts, defects or
lack; only the Absolute is; the negative-form attributes
(simplicity, self-existence, non-duality, necessity, immutability,
timelessness, spacelessness, completeness); self-knowledge as
identity, with any account of it circular for want of an external
vantage point — and then reconciles the work with it:

- **Relocation of referents.** Every interpretation's posit (the
  classical–quantum interface, the branching wavefunction, hidden
  configurations, the collapse process, agent plurality,
  system–environment relations) is assigned to *appearance*, not to
  the Absolute: each reading is a partial grammar of the appearance,
  its empirical content untouched (precedent noted: d'Espagnat).
- **The record as the appearance-stream.** The Born record with its
  exact large deviations is the appearance-stream in mathematical
  form: succession, resolution, immutable law (the SCGF, the rate
  function, the no-freezing dichotomy as timeless characterizations
  of the temporal stream).
- **Non-eliminable division.** Thm. `thm:no-go` (symmetric data do
  not determine the Born-weighted entropy) + Prop. `prop:bivariate`
  (record-resolved data do): the undivided summary is exactly
  insufficient — the in-formalism echo of the assumption's "no
  external vantage point," stated with its modest claim.
- **The primitive Born law and self-existence.** The no-go as the
  precise statement of why the primitive cannot be recovered from
  unconditioned data (analogy flagged as analogy); the annealed
  ladder receding from the quenched benchmark; the interpolation
  identity as the exact bridge; the m→∞ overshoot.
- **The one and the many.** Self-averaging as the exact
  many-realization/single-stream coincidence condition (measured
  Clifford gap 0.0226(2) nats/site as the failure signature); on
  this stage the readings take their relocated places — Everett
  branches as appearance-level decomposition, QBist agents as
  experience-taken-as-many vs. one-appearing-as-many, Bohm/GRW as
  surplus phenomenal structure with the anchor identities as
  benchmarks, einselection with its controlled laboratory and the
  transition as the phase boundary of conditional entropy.
- **Virtuous circularity, honored exactly.** The SMC self-estimation
  of the record law from records, the checksummed regenerability of
  every exact number, the declared primitivity of the Born rule: the
  circle closed exactly rather than broken by pretending to stand
  outside it.
- **Reconciliation.** No competition: the assumption locates the
  referent of the paper's exact structures at the level of
  appearance; the paper supplies that grammar in exact form; no
  theorem depends on the assumption, and no number would change
  under its revision.

Six new bibliography entries: Everett (1957), Bohm (1952),
Ghirardi–Rimini–Weber (1986), Zurek (2003), Fuchs–Mermin–Schack
(2014), d'Espagnat (*Veiled Reality*, 1995).

## 4. The standing document

`absolute.txt` (repository root) is the author's document, uploaded
directly to the repository on 2026-10-09 and preserved verbatim,
unmodified. It is a research-record document, not a submitted text;
no theorem, number, or derivation in the manuscript depends on it,
and the manuscript states the assumption self-contained in Sec. VII.
The patch script asserts that the string "absolute.txt" appears in no
visible line of the manuscript.

## 5. Verification summary

- Patch assertions: all PASS (verbatim carry, line-multiset audit —
  1769 visible v28 lines, 11-section structure, label/reference
  counts, six citation entries with per-key counts, forbidden-token
  scan clean, zero "\bnow\b" occurrences).
- Build: tectonic, `manuscript_revised_v28.pdf` (604.23 KiB, 41
  pages against v27's 39). No "??" (undefined reference) occurrences
  in the rendered text; the new section renders as Sec. VII with the
  Conclusion renumbered to Sec. VIII; Appendix C renders after
  Appendix B; all six new citations resolve ([57]–[62]). The
  "PDF destination proposition.N not defined" build warning is
  pre-existing (a fresh v27 probe build reproduces the same warning
  class) and is not introduced by this pass.
- Supplement untouched (v9 remains the companion); title, keywords,
  and abstract unchanged (the demotion relocates proofs, not claims;
  the interpretive section is explicitly non-load-bearing).
