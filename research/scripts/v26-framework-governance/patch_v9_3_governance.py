#!/usr/bin/env python3
r"""patch_v9_3_governance.py -- build formalism-v9.3.md from the
author-uploaded formalism-v9.2.md (preserved unmodified on disk).

Scope (author-directed, session 2026-10-11): the four governance-layer
fixes F1/F2/F3/F5 of the external line-level audit
(research/versions/audit_formalism_v9_2_and_gap_20261011.md, audit
item 9: "framework-side: fix F1/F2/F3/F5 whenever the descriptive
line next ships" -- the descriptive line ships NOW, as v9.3):

  F1 (line 520): the SS13 version table is stale in v9.2 -- its last
      row still reads "v9.1 (this file ...)", true only in v9.1, and
      there is no v9.2 row.  Fix: re-label the v9.1 row, add the v9.2
      row (from the v9.2 note's own content) and the v9.3 row.

  F2 (line 3 vs 283): the "DESCRIPTIVE LINEAGE RELEASE" self-label
      conflicts with Delivery Charter rule 4 as written ("a version
      ships at least one developed bridge artifact or it is a version
      note").  Fix chosen (the alternative -- relabeling v9.2 a
      version note -- rejected: it would rewrite user-mandated
      release labeling): amend rule 4 with the explicit
      descriptive-lineage exception, under which v9.2's label is
      accurate as it stood; v9.3 itself ships neither bridge artifact
      nor refreshed digest content and therefore self-labels a
      GOVERNANCE-CORRECTION VERSION NOTE under the amended rule.

  F3 (line 486): the RP12 citation-hygiene note's own citations do
      not resolve -- under the numbering the note itself asserts
      (P1-P22 + six corollaries in v3+), P7 is "no brute facts in
      appearance" (not the web/correspondence proposition); the
      web/correspondence propositions are P17/P20; the
      deducible-in-principle doctrine is P8 (P-present) + D10 with
      the J5 caveat (not P3 + P5 with the J3 caveat; the J2 gap
      reference was correct).  Fix: restate by NAME, per the note's
      own rule, with numbers demoted to parenthetical anchors.

  F5 (line 583): "program-stateonly" -> "program-state only".

Invariants asserted:
  - formalism-v9.2.md re-read byte-identical after the pass;
  - Part I (from "## 0. Status" up to "## RP0 - Mission statement")
    byte-identical between v9.2 and v9.3 (the lineage invariant);
  - the v9.2 lineage appendix carried forward unchanged except the
    F5 typo line;
  - every edit applied exactly once; the line-level diff contains
    only the designed changes (8 edited/inserted lines).
"""
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # repo root
F92 = ROOT / 'formalism-v9.2.md'
F93 = ROOT / 'formalism-v9.3.md'

SRC = F92.read_text()
ms = SRC

edits = []


def rep(old, new, note):
    global ms
    n = ms.count(old)
    assert n == 1, f'[{note}] count {n} != 1'
    ms = ms.replace(old, new)
    edits.append(note)


# --- (title) -----------------------------------------------------------
rep(
    '# The Framework — DESCRIPTIVE LINEAGE (v9.2) — Consolidated '
    'Formalism and Research Program',
    '# The Framework — DESCRIPTIVE LINEAGE (v9.3) — Consolidated '
    'Formalism and Research Program',
    'title v9.2 -> v9.3')

# --- (v9.3 note insertion) ----------------------------------------------
V93_NOTE = (
    "*v9.3 note (2026-10-11) — GOVERNANCE-CORRECTION VERSION NOTE "
    "(descriptive lineage; Charter rule 4 as amended this round — no "
    "bridge artifact and no new digest content shipped: corrections "
    "only). Built on `formalism-v9.2.md` (unchanged on disk). "
    "Implements findings F1/F2/F3/F5 of the external line-level audit "
    "(`research/versions/audit_formalism_v9_2_and_gap_20261011.md`, "
    "author-directed session 2026-10-11): **F1** — the §13 version "
    "table is completed (the v9.2 row added, this v9.3 row added, the "
    "v9.1 row's stale “(this file)” self-reference re-labeled); "
    "**F2** — Delivery Charter rule 4 amended with the explicit "
    "descriptive-lineage exception (the rule as written predated the "
    "lineage split): on the descriptive line a release ships a "
    "refreshed descriptive digest, the bridge-artifact criterion "
    "governing the generative line — under which v9.2's DESCRIPTIVE "
    "LINEAGE RELEASE label is accurate as it stood (the alternative — "
    "relabeling v9.2 a version note — rejected: it would rewrite "
    "user-mandated release labeling); **F3** — the RP12 "
    "citation-hygiene note's own citations restated by name (they "
    "were wrong by number: P7 is not the web/correspondence "
    "proposition; the doctrine is not P3 + P5), satisfying the note's "
    "own cite-by-name rule; **F5** — the “program-state only” typo "
    "repaired. Part I untouched (byte-identical lineage invariant "
    "preserved — asserted by the patch script); no proposition, "
    "truth-value, derivation, or registry row changed; the lineage "
    "appendix (the v9.2 descriptive digest) is carried forward "
    "unchanged; no generative release is paired (a governance note, "
    "not a milestone round).*"
)
rep(
    'Formalism and Research Program\n\n*v9.2 note (2026-10-11) —',
    'Formalism and Research Program\n\n' + V93_NOTE + '\n\n'
    '*v9.2 note (2026-10-11) —',
    'v9.3 note inserted above the v9.2 note')

# --- (F2: Charter rule 4 amendment) --------------------------------------
rep(
    '(4) **Versions vs version notes:** a version ships at least one '
    'developed bridge artifact or it is a version note (fable 4.10).',
    '(4) **Versions vs version notes:** a version ships at least one '
    'developed bridge artifact or it is a version note (fable 4.10). '
    '**v9.3 amendment (audit F2, 2026-10-11 — the descriptive-lineage '
    'exception):** the rule as written predates the lineage split; on '
    'the **descriptive line** (v9.x) a release ships a **refreshed '
    'descriptive digest** — the bridge-artifact criterion governs the '
    '**generative line** (v10.x) — and a version shipping neither is a '
    'version note on both lines. Under this exception v9.2\'s '
    'DESCRIPTIVE LINEAGE RELEASE label is accurate as it stood; v9.3 '
    'self-labels a version note.',
    'F2 Charter rule 4 descriptive-lineage exception')

# --- (F3: citation-hygiene note restated by name) -------------------------
rep(
    'Non-technical correction: the audited text\'s "P7 = '
    'deducible-in-principle" is a mis-citation; P7 is the '
    'web/correspondence proposition; the doctrine aimed at is P3 + P5 '
    'with the J3 epistemic-only caveat (and the J2 ontological gap).',
    'Non-technical correction: the audited text\'s "P7 = '
    'deducible-in-principle" is a mis-citation; under the v3+ '
    'numbering, P7 is *no brute facts in appearance*; the '
    'web/correspondence propositions are *the unified structure of '
    'physics is the mathematical web* and *the display is the '
    'mathematical web*; and the doctrine the audited text aimed at is '
    'the P-present-but-not-exhaustively-derivable one — *the specific '
    'form of D is P-present in M*, with the boundary *the boundary is '
    'in us, not in reality* — under the **P-present ≠ F-deducible** '
    'caveat (the doctrine claims necessity of features, never hands '
    'anyone the derivation), and beside the ontological gap (existence '
    'not derivable from content). (Number anchors, convenience only: '
    'P7; P17/P20; P8 + D10; J5; J2. Restated by name at v9.3 — audit '
    'F3: the v5 text\'s own numbers pointed at the wrong propositions, '
    'violating this rule.)',
    'F3 citation-hygiene restated by name')

# --- (F1a: re-label the v9.1 row) ------------------------------------------
rep(
    '| **v9.1 (this file — VERSION NOTE, Charter rule 4)** | '
    '2026-10-11 |',
    '| **v9.1 (`formalism-v9.1.md` — VERSION NOTE, Charter rule 4)** | '
    '2026-10-11 |',
    'F1a v9.1 row self-reference re-labeled')

# --- (F1b: add the v9.2 and v9.3 rows after the v9.1 row) -------------------
V92_ROW = (
    '| **v9.2 (`formalism-v9.2.md` — DESCRIPTIVE LINEAGE RELEASE)** | '
    '2026-10-11 | +Lineage-split release (user-mandated): lineage '
    'labels explicit (this v9.x line the descriptive fortress; the '
    'v10.x generative line the engine, independent numbering); '
    'alignment discharge — the appended **descriptive digest** '
    'records, in descriptive register, the program-side adjudications, '
    'registrations, kills and executions since v9.1 (including the '
    'sum-invariance withdrawal); **pairing rule** stated (digest '
    'refresh mandatory when a generative release changes a fact the '
    'descriptive line asserts — trigger-based cadence). Part I '
    'byte-identical to v9.1 |'
)
V93_ROW = (
    '| **v9.3 (`formalism-v9.3.md` — this file — GOVERNANCE-CORRECTION '
    'VERSION NOTE, Charter rule 4 as amended)** | 2026-10-11 | '
    '+External line-level audit round '
    '(`research/versions/audit_formalism_v9_2_and_gap_20261011.md`, '
    'findings F1/F2/F3/F5): version table completed (the v9.2 row '
    'added; the v9.1 row\'s “(this file)” re-labeled); Delivery '
    'Charter rule 4 amended with the descriptive-lineage exception; '
    'the RP12 citation-hygiene note\'s own citations restated by name; '
    '“program-state only” typo repaired. No proposition, truth-value, '
    'derivation, or registry row changed; Part I untouched; the v9.2 '
    'lineage appendix carried forward unchanged |'
)
lines = ms.split('\n')
i_v91 = [i for i, l in enumerate(lines)
         if l.startswith('| **v9.1 (`formalism-v9.1.md` — VERSION '
                         'NOTE, Charter rule 4)**')]
assert len(i_v91) == 1, 're-labeled v9.1 row not unique'
i = i_v91[0]
assert lines[i + 1].strip() == '', 'expected blank line after v9.1 row'
lines[i + 1:i + 1] = [V92_ROW, V93_ROW]
ms = '\n'.join(lines)
edits.append('F1b v9.2 + v9.3 rows added to the version table')

# --- (F5: the typo) -----------------------------------------------------------
rep(
    'What follows is Part-II/program-stateonly — the ledger, stakes, '
    'and discipline layers',
    'What follows is Part-II/program-state only — the ledger, stakes, '
    'and discipline layers',
    'F5 program-stateonly typo')

print(f'applied {len(edits)} designed edits:')
for e in edits:
    print(f'  - {e}')

# =====================================================================
# invariants
# =====================================================================
# (a) v9.2 untouched
assert F92.read_text() == SRC, 'v9.2 was modified!'
print('v9.2 untouched (byte-identical re-read) PASS')


# (b) Part I byte-identical
def part_i(text):
    i0 = text.index('## 0. Status')
    i1 = text.index('## RP0 — Mission statement')
    return text[i0:i1]


assert part_i(SRC) == part_i(ms), 'Part I changed!'
print('Part I byte-identical (lineage invariant) PASS')

# (c) the lineage appendix unchanged except the typo line
a_src = SRC[SRC.index('# LINEAGE APPENDIX (v9.2)'):]
a_new = ms[ms.index('# LINEAGE APPENDIX (v9.2)'):]
d = difflib.unified_diff(a_src.splitlines(), a_new.splitlines(), n=0)
changes = [l for l in d if l[:1] in '+-' and l[:3] not in ('+++', '---')]
assert len(changes) == 2, f'appendix diff not the single typo: {changes}'
assert 'program-stateonly' in changes[0] and 'program-state only' in changes[1]
print('lineage appendix carried forward (single F5 typo line) PASS')

# (d) new content present exactly once; old fragments gone
for tok in [
        'DESCRIPTIVE LINEAGE (v9.3)',
        'v9.3 amendment (audit F2, 2026-10-11',
        'Restated by name at v9.3 — audit F3',
        '| **v9.2 (`formalism-v9.2.md` — DESCRIPTIVE LINEAGE '
        'RELEASE)**',
        '| **v9.3 (`formalism-v9.3.md` — this file — '
        'GOVERNANCE-CORRECTION',
]:
    n = ms.count(tok)
    assert n == 1, f'new token {tok[:50]!r}: {n} != 1'
for tok in [
        'DESCRIPTIVE LINEAGE (v9.2) — Consolidated',
        'program-stateonly',
        'P7 is the web/correspondence proposition',
        'is P3 + P5',
        'v9.1 (this file — VERSION NOTE',
]:
    assert tok not in ms, f'old fragment survived: {tok[:50]!r}'
assert ms.count('GOVERNANCE-CORRECTION VERSION NOTE') == 2  # note + table row
assert ms.count('the descriptive-lineage exception') == 2  # note + rule-4 amendment
assert ms.count('program-state only') == 3  # fix + note + table row
print('new/old fragment scan PASS')

# (e) the J2 reference survives (it was correct in v5); J3-caveat gone
assert 'ontological gap (existence not derivable from content)' in ms
assert 'J3 epistemic-only caveat' not in ms
print('J2/J5/J3 correction semantics PASS')

# (f) full-file line diff: only the designed lines
sm = difflib.SequenceMatcher(a=SRC.splitlines(), b=ms.splitlines(),
                             autojunk=False)
n_changed = 0
DESIGNED_SUBSTRINGS = [
    '# The Framework — DESCRIPTIVE LINEAGE (v9.3)',
    '*v9.3 note (2026-10-11) — GOVERNANCE-CORRECTION VERSION NOTE',
    '(4) **Versions vs version notes:** a version ships at least one '
    'developed bridge artifact or it is a version note (fable 4.10). '
    '**v9.3 amendment (audit F2, 2026-10-11',
    'Non-technical correction: the audited text\'s "P7 = '
    'deducible-in-principle" is a mis-citation; under the v3+ numbering',
    '| **v9.1 (`formalism-v9.1.md` — VERSION NOTE, Charter rule 4)**',
    '| **v9.2 (`formalism-v9.2.md` — DESCRIPTIVE LINEAGE RELEASE)**',
    '| **v9.3 (`formalism-v9.3.md` — this file — GOVERNANCE-CORRECTION',
    'What follows is Part-II/program-state only',
]
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    for l in ms.splitlines()[j1:j2]:
        if not l.strip():
            continue          # blank separator lines of the insertions
        assert any(s in l for s in DESIGNED_SUBSTRINGS), \
            f'undesigned new line: {l[:80]!r}'
        n_changed += 1
assert n_changed == 8, f'expected 8 designed new lines, got {n_changed}'
print(f'line-level diff audit PASS: exactly 8 designed lines '
      f'(1 title + 1 note + 1 rule-4 + 1 hygiene + 1 v9.1 relabel + '
      f'2 table rows + 1 typo)')

F93.write_text(ms)
print(f'written: formalism-v9.3.md ({len(ms)} chars; '
      f'v9.2 was {len(SRC)} chars)')
print('PATCH OK')
