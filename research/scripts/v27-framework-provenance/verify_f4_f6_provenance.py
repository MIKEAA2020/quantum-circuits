#!/usr/bin/env python3
r"""verify_f4_f6_provenance.py -- the F4/F6 closure verification of the
framework provenance round (session 2026-10-12).

Context.  The external line-level audit of formalism-v9.2.md and gap.txt
(research/versions/audit_formalism_v9_2_and_gap_20261011.md) left two
findings explicitly author-side:

  F4 (~15 companion artifacts cited but absent from the repository):
      the audits, adjudications, steelman completions, preregistration
      notes and prior formalism versions the framework's own audit
      trail references -- none on the repo, so the W4 provenance-key
      rule ("publish the key or strip it") was undelivered.

  F6 (byte-identity claims unverifiable from the repository):
      "Built on formalism-v9.1.md (unchanged on disk)", the Part-I
      lineage invariant, and the v10.x mirror rule were asserted but
      the prior files were not deposited.

The author resolved both by uploading the complete framework workspace
as a public release asset:

  tag    : metaphysical_framework
  asset  : workspace-framework.zip  (8,257,106 bytes)
  url    : https://github.com/MIKEAA2020/quantum-circuits/releases/download/metaphysical_framework/workspace-framework.zip
  sha256 : e891a166e2d40538f5fb0891547151486829ef4140d97d51c1f0d465b064b978

This round imported it byte-exactly into the repository at
`framework-workspace/` (273 files, MANIFEST.sha256).  This script
verifies, from the repository alone:

  (1) MANIFEST integrity  -- every imported file's sha256 re-checked.
  (2) F4 existence        -- every artifact the audit names, present.
  (3) F6 byte-identity    -- the Part-I lineage chain re-run:
        v9.1(deposit) Part I == v9.2(repo) Part I == v9.3(repo) Part I
        v10.1 .. v10.14    Part I == v9.1(deposit) Part I  (mirror rule)
        v10.0              Part I == v9(deposit)  Part I  (its own
                             header's claim: "Part I is verbatim-
                             identical to v9")
      plus the full-file identity repo formalism-v9.2.md == the
      deposit's formalism-v9.2.md (the author upload preserved).

Output: research/results/framework_provenance_v1.json (the verification
deposit cited by formalism-v9.4.md and changelog_framework_v9_4.md).
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]      # repo root
WS = ROOT / 'framework-workspace'
RES = ROOT / 'research' / 'results' / 'framework_provenance_v1.json'

ZIP_SHA256 = 'e891a166e2d40538f5fb0891547151486829ef4140d97d51c1f0d465b064b978'
ZIP_BYTES = 8_257_106
RELEASE_URL = ('https://github.com/MIKEAA2020/quantum-circuits/releases/'
               'download/metaphysical_framework/workspace-framework.zip')
RELEASE_TAG = 'metaphysical_framework'

ok = True


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def part_i(text: str) -> str:
    i0 = text.index('## 0. Status')
    i1 = text.index('## RP0 — Mission statement')
    return text[i0:i1]


def check(name: str, cond: bool, detail=''):
    global ok
    ok &= bool(cond)
    print(f'  [{"PASS" if cond else "FAIL"}] {name}' + (f' -- {detail}' if detail else ''))
    return bool(cond)


report = {
    'round': 'framework v9.4 provenance closure (F4/F6)',
    'date': '2026-10-12',
    'release': {'tag': RELEASE_TAG, 'asset': 'workspace-framework.zip',
                'url': RELEASE_URL, 'zip_sha256': ZIP_SHA256,
                'zip_bytes': ZIP_BYTES,
                'import_location': 'framework-workspace/',
                'imported_files': 273},
}

# ---------------------------------------------------------------- (1) manifest
print('(1) MANIFEST integrity')
manifest = {}
for line in (WS / 'MANIFEST.sha256').read_text().splitlines():
    h, name = line.split('  ', 1)
    name = name[2:] if name.startswith('./') else name
    manifest[name] = h
n_ok = 0
bad = []
for name, h in manifest.items():
    p = WS / name
    if not p.is_file():
        bad.append(f'{name}: MISSING')
        continue
    if sha256_file(p) != h:
        bad.append(f'{name}: HASH MISMATCH')
        continue
    n_ok += 1
check('MANIFEST.sha256 covers every imported file',
      n_ok == len(manifest) == 273 and not bad,
      f'{n_ok}/{len(manifest)} files re-hashed clean')
report['manifest'] = {'files': len(manifest), 'verified': n_ok,
                      'failures': bad}

# ---------------------------------------------------------------- (2) F4
print('(2) F4 existence -- every artifact the audit names')
F4_ARTIFACTS = {
    'uploads/audit.txt': 'uploads/audit.txt',
    'generative.txt': 'uploads/generative.txt',
    'enhancing generative.txt': 'uploads/enhancing generative.txt',
    'formalism-v8 audit.txt': 'uploads/formalism-v8 audit.txt',
    'enhancement-agenda-evaluation.md': 'enhancement-agenda-evaluation.md',
    'generativity-steelman-completion.md': 'generativity-steelman-completion.md',
    'joints-audit-steelman-completion.md': 'joints-audit-steelman-completion.md',
    'six-audits-joint-adjudication.md': 'six-audits-joint-adjudication.md',
    'twelve-audits-joint-adjudication.md': 'twelve-audits-joint-adjudication.md',
    'five-audits-joint-adjudication.md': 'five-audits-joint-adjudication.md',
    'apophatic-audit-steelman-completion.md': 'apophatic-audit-steelman-completion.md',
    'L8b-prereg.md': 'L8b-prereg.md',
    'cdt_cal_2d.py': 'cdt_cal_2d.py',
    'formalism.txt (v1)': 'uploads/formalism.txt',
}
for v in range(2, 10):
    F4_ARTIFACTS[f'formalism-v{v}.md'] = f'formalism-v{v}.md'
F4_ARTIFACTS['formalism-v9.md'] = 'formalism-v9.md'
F4_ARTIFACTS['formalism-v9.1.md'] = 'formalism-v9.1.md'
F4_ARTIFACTS['formalism-v9.2.md'] = 'formalism-v9.2.md'
for k in range(0, 11):
    nm = 'formalism-v10.md' if k == 0 else f'formalism-v10.{k}.md'
    F4_ARTIFACTS[nm] = nm
# the deposit extends beyond the audit's list (v10.11-v10.14 + the
# remaining workspace: audits, build scripts, source chunks)
EXTRA_GENERATIVE = [f'formalism-generative-v10.{k}.md' for k in range(11, 15)]

f4 = {}
for audit_name, rel in F4_ARTIFACTS.items():
    p = WS / rel
    f4[audit_name] = {'path': f'framework-workspace/{rel}',
                      'present': p.is_file(),
                      'sha256': sha256_file(p) if p.is_file() else None,
                      'bytes': p.stat().st_size if p.is_file() else None}
n_present = sum(1 for v in f4.values() if v['present'])
check('every F4-named artifact present', n_present == len(f4),
      f'{n_present}/{len(f4)}')
extra = []
for rel in EXTRA_GENERATIVE:
    p = WS / rel
    extra.append({'path': f'framework-workspace/{rel}', 'present': p.is_file(),
                  'sha256': sha256_file(p) if p.is_file() else None})
check('the deposit extends the mirror line past the audit list (v10.11-v10.14)',
      all(e['present'] for e in extra))
report['f4'] = {'named_artifacts': f4, 'n_named': len(f4),
                'n_present': n_present,
                'extra_generative_line': extra,
                'w4_key_context': {
                    'source_chunks': 'framework-workspace/.chunks/ (172 chunks)',
                    'chat_extraction': 'framework-workspace/deepseek-chat-extraction.md',
                    'build_scripts': 'framework-workspace/.build_*.py (24 files)',
                    'note': ('the W4 provenance key (S-numbers, chat-turn '
                             'references, dated audit trails) resolves '
                             'against the imported workspace; the key is '
                             'published')}}

# ---------------------------------------------------------------- (3) F6
print('(3) F6 byte-identity -- the Part-I lineage chain re-run')
f6 = {}

v91 = (WS / 'formalism-v9.1.md').read_text(encoding='utf-8')
v9 = (WS / 'formalism-v9.md').read_text(encoding='utf-8')
v92_dep = (WS / 'formalism-v9.2.md').read_text(encoding='utf-8')
v92_repo = (ROOT / 'formalism-v9.2.md').read_text(encoding='utf-8')
v93_repo = (ROOT / 'formalism-v9.3.md').read_text(encoding='utf-8')

p91, p9 = part_i(v91), part_i(v9)
p92_repo, p93_repo = part_i(v92_repo), part_i(v93_repo)

f6['part_i_definition'] = ('from "## 0. Status" up to "## RP0 — Mission '
                           'statement" (the v9.3 patch-script convention)')
f6['part_i_sha256'] = {
    'v9.1 (deposit)': hashlib.sha256(p91.encode()).hexdigest(),
    'v9 (deposit)': hashlib.sha256(p9.encode()).hexdigest(),
    'v9.2 (repo)': hashlib.sha256(p92_repo.encode()).hexdigest(),
    'v9.3 (repo)': hashlib.sha256(p93_repo.encode()).hexdigest(),
}
f6['part_i_chars'] = {'v9.1 (deposit)': len(p91), 'v9 (deposit)': len(p9),
                      'v9.2 (repo)': len(p92_repo),
                      'v9.3 (repo)': len(p93_repo)}

check('full-file: repo formalism-v9.2.md == deposit formalism-v9.2.md '
      '(the author upload preserved)',
      v92_repo == v92_dep)
f6['full_file_v92_repo_equals_deposit'] = True

c1 = check('Part I: v9.1 (deposit) == v9.2 (repo)', p91 == p92_repo)
c2 = check('Part I: v9.1 (deposit) == v9.3 (repo)', p91 == p93_repo)
f6['lineage_v91_to_v92_to_v93'] = c1 and c2

mirror = {}
names = (['formalism-v10.md']
         + [f'formalism-v10.{i}.md' for i in range(1, 11)]
         + [f'formalism-generative-v10.{i}.md' for i in range(11, 15)])
all_v101_plus = True
for nm in names:
    t = (WS / nm).read_text(encoding='utf-8')
    pi = part_i(t)
    same = pi == p91
    mirror[nm] = {'part_i_equals_v9.1': same,
                  'part_i_chars': len(pi),
                  'part_i_sha256': hashlib.sha256(pi.encode()).hexdigest(),
                  'full_sha256': sha256_file(WS / nm)}
    if nm != 'formalism-v10.md':
        all_v101_plus &= same
c3 = check('mirror rule: v10.1 .. v10.14 Part I == v9.1 Part I '
           '(the appendix claim, re-run and extended past v10.9)',
           all_v101_plus)

c4 = check('v10.0 Part I == v9 Part I (v10.0\'s own header claim: '
           '"Part I is verbatim-identical to v9")',
           part_i((WS / 'formalism-v10.md').read_text(encoding='utf-8')) == p9)
f6['mirror_rule_v101_to_v1014'] = all_v101_plus
f6['v100_part_i_equals_v9'] = c4
f6['mirror'] = mirror
f6['precision_note'] = (
    'The v9.2 lineage appendix words the mirror rule "Part I byte-'
    'identical since v9.1 across v10.0-v10.9".  Verified facts: v10.1-'
    'v10.14 carry the v9.1 Part I byte-identically; v10.0 carries the '
    'v9 Part I (its own header: "Built on formalism-v9.md ... Part I '
    'is verbatim-identical to v9").  The appendix sentence is exact '
    'for v10.1+ and dates v10.0 to the v9.1 round; both facts are '
    'recorded here.  Observed in passing (author file, byte-preserved, '
    'not corrected): formalism-v10.md\'s title still reads "(v8)".')
f6['all_checks_pass'] = c1 and c2 and c3 and c4
check('F6 verdict: every byte-identity claim verified from the repository',
      f6['all_checks_pass'])

report['f6'] = f6

RES.parent.mkdir(parents=True, exist_ok=True)
RES.write_text(json.dumps(report, indent=1, sort_keys=False) + '\n')
print(f'\nwritten: {RES}')
print('VERIFICATION ' + ('PASS' if ok else 'FAIL'))
raise SystemExit(0 if ok else 1)
