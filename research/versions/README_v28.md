# README — v28 (demotion + interpretive-status pass)

**Deliverable (current submission candidate):**
`manuscript_revised_v28.tex/.pdf` + `supplement_v9.tex/.pdf` (companion,
unchanged this pass), built by
`research/scripts/v22-exactZ3-n5L8/patch_v28_absolute_interpret.py`
from the canonical v27 (`manuscript_revised_v27.tex`, the
extension-integration pass). All earlier versions preserved
unmodified. Changelog: `changelog_v28.md`; ledger:
`certificate_sha256_v15.txt`. Standing document: `absolute.txt`
(repository root, author-uploaded, preserved verbatim).

## Version map (this round)

- **v27** (previous): the extension-integration pass — the completed
  extension campaign's two deposits integrated into the tables, the
  L=8 rung paragraph, the locator sentence, the Scope note, one
  abstract clause, the Conclusion, and Supplement S7 (v9).
- **v28** (this pass): the demotion + interpretive-status pass —
  (1) Sec. III's worst-case complexity subsection demoted verbatim to
  the new Appendix C, replaced by a compact summary subsection with
  pointers (zero content loss, asserted in the patch script by
  exact-substring carry + a full line-multiset audit); (2) five
  cross-reference sites updated; (3) new Sec. VII, "Interpretive
  status of the record formalism" — the author's standing assumption
  (the non-dual Absolute of `absolute.txt`) stated, the major
  readings of quantum mechanics relocated to the level of
  appearance, and the work reconciled with the assumption through
  exact reconciliation conditions; six new bibliography entries.

## The demotion, precisely

- **Moved verbatim to Appendix C** (`app:complexity`, title
  preserved: "Precisely promised trajectory complexity"): the
  gate-set conventions, the CTD definition, the PostBQP-completeness
  proposition and proof, the estimation corollary and proof, the
  conditional-purity corollary and proof, the BQP-estimability
  boundary paragraph — 47 source lines.
- **Kept in the main text** (`sec:ctd`, "Worst-case trajectory
  complexity"): the full statement of every result with pointers.
- **Not demoted** (author criterion applied): the no-freezing proof
  body of Sec. IV.C — both constituent results are headline
  contributions, the SMC subsection builds on the self-averaging
  criterion, the brand is exactness-on-display; reasons recorded in
  `changelog_v28.md` §2.
- **No content loss, verified twice inside the patch script**: the
  demoted body is an exact substring of the output (count == 1), and
  a line-multiset audit confirms every visible v27 line except the
  six deliberately edited ones survives in v28.

## The interpretive-status section (Sec. VII)

States the author's standing working assumption — the **non-dual
Absolute** (`absolute.txt`, uploaded by the author 2026-10-09 and
preserved verbatim): reality as pure self-luminous awareness,
universal consciousness, self-existent, timeless, spaceless,
unchanging, complete, non-dual, without relations, parts, defects or
lack; only the Absolute is; self-knowledge as identity, any account
circular for want of an external vantage point. The section then
relocates the referents of the major readings of quantum mechanics
(operational, Everett, de Broglie–Bohm, GRW, QBism, einselection) to
the level of appearance, and reconciles the work with the assumption:
the Born record as the appearance-stream in exact mathematical form;
the no-go theorem as non-eliminable division (the in-formalism echo
of "no external vantage point"); the primitive Born law and the
attribute of self-existence; self-averaging as the exact one/many
coincidence condition (with the measured Clifford disorder gap as
the failure signature); the exactness program as virtuous circularity
honored exactly. The assumption is explicitly non-load-bearing: no
theorem, computation, or number in the paper depends on it, and no
number would change under its revision. Six new bibliography entries
(Everett, Bohm, GRW, Zurek, Fuchs–Mermin–Schack, d'Espagnat).

## Open author actions (unchanged unless noted)

- figshare DOI minting (Data and code availability placeholders).
- Optional TJP template transcode.
- Deletion of the campaign cron jobs 431600/431599 (user-facing
  session; they fire harmlessly as no-ops).
