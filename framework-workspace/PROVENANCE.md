# framework-workspace/ — the author's framework workspace, deposited

**What this is.** The complete framework workspace of the descriptive
(v9.x) and generative (v10.x) formalism line: every prior version
`formalism-v2.md` … `formalism-v9.2.md`, the generative series
`formalism-v10.md` … `formalism-v10.10.md` and
`formalism-generative-v10.11.md` … `v10.14.md`, the v1 source
(`uploads/formalism.txt`), the companion audit artifacts
(`uploads/*.txt`, the joint adjudications, the steelman completions,
`L8b-prereg.md`, `enhancement-agenda-evaluation.md`, the CDT / RP11b /
w3b calibration scripts and reports), the build scripts
(`.build_*.py`), and the source-extraction chunks (`.chunks/`,
`deepseek-chat-extraction.md`).

**Provenance.** Uploaded by the author as the public release asset

- tag: [`metaphysical_framework`](https://github.com/MIKEAA2020/quantum-circuits/releases/tag/metaphysical_framework)
- asset: `workspace-framework.zip` (8,257,106 bytes)
- url: https://github.com/MIKEAA2020/quantum-circuits/releases/download/metaphysical_framework/workspace-framework.zip
- zip sha256: `e891a166e2d40538f5fb0891547151486829ef4140d97d51c1f0d465b064b978`

imported byte-exactly (273 files; `MANIFEST.sha256` re-verifies every
file). This folder is the in-repo copy of record; the release asset is
the canonical binary.

**Why it is in the repository.** It closes audit findings F4 and F6 of
the line-level audit
(`research/versions/audit_formalism_v9_2_and_gap_20261011.md`):

- **F4** — the ~15 companion artifacts the framework's audit trail
  references were previously absent, leaving the W4 provenance-key rule
  ("publish the key or strip it") undelivered. They are published here.
- **F6** — the byte-identity claims ("Built on `formalism-v9.1.md`
  (unchanged on disk)", the Part-I lineage invariant, the v10.x mirror
  rule) were previously unverifiable from the repository. The
  verification round re-ran every one of them against this deposit:
  `research/scripts/v27-framework-provenance/verify_f4_f6_provenance.py`
  → `research/results/framework_provenance_v1.json`, recorded by
  `formalism-v9.4.md` (the provenance-closure version note) and
  `research/versions/changelog_framework_v9_4.md`.

**Verification summary** (all PASS, re-runnable from the repository):

| claim | verified fact |
|---|---|
| repo `formalism-v9.2.md` = the author upload | byte-identical to the deposit's `formalism-v9.2.md` |
| Part I lineage v9.1 → v9.2 → v9.3 | byte-identical (52,998 chars, one sha256) |
| mirror rule, v10.1 … v10.14 | Part I byte-identical to the deposited v9.1 Part I |
| v10.0's own header claim | Part I byte-identical to the deposited **v9** Part I |

One precision note and one passing observation are recorded in the
verification deposit: the v9.2 lineage appendix's "Part I byte-identical
since v9.1 across v10.0–v10.9" is exact for v10.1+ (v10.0 carries the
v9 Part I, as v10.0's own header states); and `formalism-v10.md`'s
title still reads "(v8)" (author file, byte-preserved, not corrected).

**Layout.** Root level: the formalism version line and the audit /
calibration artifacts. `uploads/`: the author's original upload files
(the v1 `formalism.txt`, the audit texts, the standing-pressure and
generative-circle dialogues, `Reality-Self-Simulation-Explained.txt`).
`.chunks/` + `deepseek-chat-extraction.md`: the source-extraction
chunks the build scripts (`.build_*.py`) assembled the version line
from — the W4 provenance key resolves against them.
`CONVENTIONS.md`: the workspace's own conventions.
