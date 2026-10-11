#!/usr/bin/env python3
r"""patch_v9_4_provenance.py -- build formalism-v9.4.md from
formalism-v9.3.md (preserved unmodified on disk).

Scope (author-directed, session 2026-10-12): close audit findings F4
and F6 -- the two findings the line-level audit
(research/versions/audit_formalism_v9_2_and_gap_20261011.md) left
author-side -- now that the author has deposited the complete
framework workspace as the public release asset `metaphysical_framework`
(workspace-framework.zip, sha256 e891a166...; imported byte-exactly at
framework-workspace/, 273 files + MANIFEST.sha256):

  F4 (companion artifacts absent; the W4 provenance-key rule):
      closed by publication -- every artifact the audit names is now
      in-repo; the audit trail's S-numbers / chat-turn references /
      dated audit trails resolve against the imported workspace.

  F6 (byte-identity claims unverifiable):
      closed by verification -- research/scripts/v27-framework-
      provenance/verify_f4_f6_provenance.py re-ran every claim from
      the deposits (all PASS): Part I v9.1 -> v9.2 -> v9.3 byte-
      identical (52,998 chars, one sha256); the mirror rule re-run
      and extended (v10.1 .. v10.14 Part I == the deposited v9.1
      Part I); v10.0's Part I == the deposited v9 Part I exactly as
      its own header claims; the repo's formalism-v9.2.md == the
      deposit's.  Deposit: research/results/framework_provenance_v1.json.

Edits (all governance-layer; the v9.3 note, Charter rule 4, the RP12
hygiene note and the lineage appendix are carried forward untouched):

  1. title: DESCRIPTIVE LINEAGE (v9.3) -> (v9.4);
  2. the v9.4 header note inserted above the v9.3 note;
  3. the SS13 version table: the v9.3 row's "this file" self-reference
     re-labeled to the file name; the v9.4 row added.

Invariants asserted:
  - formalism-v9.3.md re-read byte-identical after the pass;
  - Part I (from "## 0. Status" up to "## RP0 - Mission statement")
    byte-identical between v9.3 and v9.4 (the lineage invariant);
  - the lineage appendix carried forward with ZERO changes;
  - every edit applied exactly once; the line-level diff contains
    only the 4 designed lines.
"""
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # repo root
F93 = ROOT / 'formalism-v9.3.md'
F94 = ROOT / 'formalism-v9.4.md'

SRC = F93.read_text(encoding='utf-8')
ms = SRC
edits = []


def rep(old, new, note):
    global ms
    n = ms.count(old)
    assert n == 1, f'[{note}] count {n} != 1'
    ms = ms.replace(old, new)
    edits.append(note)


# --- (1) title -----------------------------------------------------------
rep(
    '# The Framework — DESCRIPTIVE LINEAGE (v9.3) — Consolidated '
    'Formalism and Research Program',
    '# The Framework — DESCRIPTIVE LINEAGE (v9.4) — Consolidated '
    'Formalism and Research Program',
    'title v9.3 -> v9.4')

# --- (2) the v9.4 header note ---------------------------------------------
V94_NOTE = (
    "*v9.4 note (2026-10-12) — PROVENANCE-CLOSURE VERSION NOTE "
    "(descriptive lineage; Charter rule 4 as amended at v9.3 — no "
    "bridge artifact and no new digest content shipped: provenance "
    "closure only). Built on `formalism-v9.3.md` (unchanged on disk). "
    "Implements findings **F4** and **F6** of the external line-level "
    "audit (`research/versions/audit_formalism_v9_2_and_gap_20261011."
    "md`) — the two findings that audit left author-side, now resolved "
    "by the author's release deposit (tag `metaphysical_framework`, "
    "asset `workspace-framework.zip`, sha256 `e891a166e2d40538f5fb0891"
    "547151486829ef4140d97d51c1f0d465b064b978`): the complete "
    "framework workspace — every prior version v2–v9.2, the generative "
    "line v10.0–v10.14, the v1 source, the ~15 companion audit "
    "artifacts, the build scripts and the source-extraction chunks — "
    "is imported byte-exactly at `framework-workspace/` (273 files, "
    "`MANIFEST.sha256`; `PROVENANCE.md` records the deposit). **F6 "
    "closed by verification** (`research/scripts/v27-framework-"
    "provenance/verify_f4_f6_provenance.py` → `research/results/"
    "framework_provenance_v1.json`, all checks PASS): the Part-I "
    "lineage chain re-run from the deposits — v9.1 → v9.2 → v9.3 Part "
    "I byte-identical (52,998 chars, one sha256); the mirror rule "
    "re-run and extended — v10.1 through v10.14 Part I byte-identical "
    "to the deposited v9.1 Part I; v10.0's Part I byte-identical to "
    "the deposited **v9** Part I, exactly as v10.0's own header claims "
    "(the v9.2 lineage appendix's “since v9.1 across v10.0–v10.9” is "
    "exact for v10.1+ and dates v10.0 to the v9.1 round — both facts "
    "recorded in the verification deposit, which also notes in passing "
    "that `formalism-v10.md`'s title still reads “(v8)”: author file, "
    "byte-preserved, not corrected); the repo's `formalism-v9.2.md` "
    "verified byte-identical to the deposit's. **F4 closed by "
    "publication**: the W4 provenance-key rule (“publish the key or "
    "strip it”) is satisfied — every artifact the audit names is "
    "in-repo, and the audit trail's S-numbers, chat-turn references "
    "and dated audit trails resolve against the imported workspace. "
    "Part I untouched (byte-identical lineage invariant preserved — "
    "asserted by the patch script); no proposition, truth-value, "
    "derivation, or registry row changed; the lineage appendix (the "
    "v9.2 descriptive digest) carried forward unchanged; no generative "
    "release is paired (a provenance note, not a milestone round).*"
)
rep(
    'Formalism and Research Program\n\n*v9.3 note (2026-10-11) —',
    'Formalism and Research Program\n\n' + V94_NOTE + '\n\n'
    '*v9.3 note (2026-10-11) —',
    'v9.4 note inserted above the v9.3 note')

# --- (3a) re-label the v9.3 row --------------------------------------------
rep(
    '| **v9.3 (`formalism-v9.3.md` — this file — GOVERNANCE-CORRECTION '
    'VERSION NOTE, Charter rule 4 as amended)** |',
    '| **v9.3 (`formalism-v9.3.md` — GOVERNANCE-CORRECTION '
    'VERSION NOTE, Charter rule 4 as amended)** |',
    'F1-pattern v9.3 row self-reference re-labeled')

# --- (3b) add the v9.4 row after the v9.3 row -------------------------------
V94_ROW = (
    '| **v9.4 (`formalism-v9.4.md` — this file — PROVENANCE-CLOSURE '
    'VERSION NOTE, Charter rule 4 as amended)** | 2026-10-12 | '
    '+Provenance closure (audit F4/F6, author-deposited release '
    '`metaphysical_framework` → `framework-workspace/`, 273 files + '
    '`MANIFEST.sha256`): every byte-identity claim re-run and PASS '
    '(Part I v9.1→v9.2→v9.3 identical, 52,998 chars; mirror v10.1–'
    'v10.14 ≡ the deposited v9.1 Part I; v10.0 ≡ the deposited v9 Part '
    'I per its own header; the repo v9.2 ≡ the deposit; verification '
    'deposit `research/results/framework_provenance_v1.json`); the W4 '
    'provenance key published. No proposition, truth-value, derivation, '
    'or registry row changed; Part I untouched; the lineage appendix '
    'carried forward unchanged |'
)
lines = ms.split('\n')
i_v93 = [i for i, l in enumerate(lines)
         if l.startswith('| **v9.3 (`formalism-v9.3.md` — GOVERNANCE-'
                         'CORRECTION')]
assert len(i_v93) == 1, 're-labeled v9.3 row not unique'
i = i_v93[0]
assert lines[i + 1].strip() == '', 'expected blank line after v9.3 row'
lines[i + 1:i + 1] = [V94_ROW]
ms = '\n'.join(lines)
edits.append('v9.4 row added to the version table')

print(f'applied {len(edits)} designed edits:')
for e in edits:
    print(f'  - {e}')

# =====================================================================
# invariants
# =====================================================================
# (a) v9.3 untouched
assert F93.read_text(encoding='utf-8') == SRC, 'v9.3 was modified!'
print('v9.3 untouched (byte-identical re-read) PASS')


# (b) Part I byte-identical
def part_i(text):
    i0 = text.index('## 0. Status')
    i1 = text.index('## RP0 — Mission statement')
    return text[i0:i1]


assert part_i(SRC) == part_i(ms), 'Part I changed!'
print('Part I byte-identical (lineage invariant) PASS')

# (c) the lineage appendix carried forward with ZERO changes
a_src = SRC[SRC.index('# LINEAGE APPENDIX (v9.2)'):]
a_new = ms[ms.index('# LINEAGE APPENDIX (v9.2)'):]
assert a_src == a_new, 'lineage appendix changed!'
print('lineage appendix carried forward (zero changes) PASS')

# (d) new content present exactly once; old fragments gone
for tok in [
        'DESCRIPTIVE LINEAGE (v9.4)',
        '*v9.4 note (2026-10-12) — PROVENANCE-CLOSURE VERSION NOTE',
        '| **v9.4 (`formalism-v9.4.md` — this file — PROVENANCE-CLOSURE',
        '| **v9.3 (`formalism-v9.3.md` — GOVERNANCE-CORRECTION',
]:
    n = ms.count(tok)
    assert n == 1, f'new token {tok[:50]!r}: {n} != 1'
for tok in [
        'DESCRIPTIVE LINEAGE (v9.3) — Consolidated',
        'this file — GOVERNANCE-CORRECTION',
]:
    assert tok not in ms, f'old fragment survived: {tok[:50]!r}'
assert ms.count('PROVENANCE-CLOSURE VERSION NOTE') == 2  # note + table row
assert ms.count('framework-workspace/') >= 2             # note + row
print('new/old fragment scan PASS')

# (e) full-file line diff: only the designed lines
sm = difflib.SequenceMatcher(a=SRC.splitlines(), b=ms.splitlines(),
                             autojunk=False)
n_changed = 0
DESIGNED_SUBSTRINGS = [
    '# The Framework — DESCRIPTIVE LINEAGE (v9.4)',
    '*v9.4 note (2026-10-12) — PROVENANCE-CLOSURE VERSION NOTE',
    '| **v9.3 (`formalism-v9.3.md` — GOVERNANCE-CORRECTION',
    '| **v9.4 (`formalism-v9.4.md` — this file — PROVENANCE-CLOSURE',
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
assert n_changed == 4, f'expected 4 designed new lines, got {n_changed}'
print(f'line-level diff audit PASS: exactly 4 designed lines '
      f'(1 title + 1 note + 1 v9.3 relabel + 1 v9.4 row)')

F94.write_text(ms, encoding='utf-8')
print(f'written: formalism-v9.4.md ({len(ms)} chars; '
      f'v9.3 was {len(SRC)} chars)')
print('PATCH OK')
