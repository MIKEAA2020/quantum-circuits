# Changelog — framework v9.4 (provenance-closure version note)

Date: 2026-10-12 (+03:00). Script:
`research/scripts/v27-framework-provenance/patch_v9_4_provenance.py`.
Source preserved unmodified: `formalism-v9.3.md` (re-read
byte-identical after the pass). New files: `formalism-v9.4.md`, this
changelog, `certificate_sha256_v22.txt`, the verification pair
`research/scripts/v27-framework-provenance/verify_f4_f6_provenance.py`
+ `research/results/framework_provenance_v1.json`, and the imported
`framework-workspace/` (273 files + `MANIFEST.sha256` +
`PROVENANCE.md`).

Provenance note: author-directed round (session 2026-10-12). The
author deposited the complete framework workspace as the public
release asset `workspace-framework.zip` (tag `metaphysical_framework`,
8,257,106 bytes, sha256
`e891a166e2d40538f5fb0891547151486829ef4140d97d51c1f0d465b064b978`)
— resolving the precondition the v9.3 round recorded for F4/F6
("requires the author's own uploads to resolve"). This round imports
the deposit byte-exactly into the repository and closes both findings.

## Self-label

v9.4 ships neither a bridge artifact nor refreshed digest content —
only provenance closure. Under Delivery Charter rule 4 as amended at
v9.3 it is a **PROVENANCE-CLOSURE VERSION NOTE**; the version history
table and the header note say so. No generative release is paired; the
v9.2 lineage appendix (the descriptive digest) is carried forward
unchanged — with **zero** changes this time (not even a typo line).

## The closure

1. **F4 (companion artifacts absent; the W4 provenance-key rule) —
   closed by publication.** Every artifact the audit names is now
   in-repo at `framework-workspace/`: the audit texts
   (`uploads/audit.txt`, `formalism-v8 audit.txt`,
   `generative.txt`, `enhancing generative.txt`), the joint
   adjudications (six / twelve / five-audits), the steelman
   completions (generativity, joints, apophatic, point-circle),
   `enhancement-agenda-evaluation.md`, `L8b-prereg.md`,
   `cdt_cal_2d.py`, the full prior version line (`formalism.txt` v1,
   `formalism-v2.md` … `formalism-v9.2.md`, `formalism-v10.md` …
   `v10.10.md`), and — beyond the audit's list — the generative line
   `formalism-generative-v10.11.md` … `v10.14.md`, the build scripts
   (`.build_*.py`), and the source-extraction chunks (`.chunks/`,
   `deepseek-chat-extraction.md`), against which the W4 key
   (S-numbers, chat-turn references, dated audit trails) resolves.
   Existence check: 35/35 audit-named artifacts present.
   `MANIFEST.sha256` re-verifies all 273 files (273/273 clean).

2. **F6 (byte-identity claims unverifiable) — closed by
   verification.** `verify_f4_f6_provenance.py` re-ran every claim
   from the repository (all PASS; deposit
   `research/results/framework_provenance_v1.json`):
   - repo `formalism-v9.2.md` is byte-identical to the deposit's
     `formalism-v9.2.md` (the author upload preserved);
   - **Part I lineage v9.1 → v9.2 → v9.3: byte-identical**
     (52,998 chars, one sha256) — the invariant the v9.3 patch
     asserted is now verified against the deposited v9.1;
   - **mirror rule re-run and extended: v10.1 through v10.14 Part I
     byte-identical to the deposited v9.1 Part I** (the v9.2 appendix
     claimed v10.0–v10.9 with split-checks "last at v10.9"; the
     deposit allows the re-run through v10.14);
   - **v10.0's Part I is byte-identical to the deposited v9 Part I** —
     exactly what v10.0's own header claims ("Built on
     `formalism-v9.md` … Part I is verbatim-identical to v9").

## The two precision observations (recorded, not corrected)

- The v9.2 lineage appendix words the mirror rule "Part I
  byte-identical since v9.1 across v10.0–v10.9". Verified facts:
  exact for v10.1+; v10.0 carries the v9 Part I (its own header's
  claim), so the appendix sentence reads v10.0 under its "since the
  v9.1 round" dating rather than as an identity claim. Both facts are
  on record in the verification deposit; the appendix itself is
  historical v9.2 text and is carried forward unchanged.
- `formalism-v10.md`'s title still reads "(v8)" (a stale-title quirk
  of the v10.0 build). Author file, byte-preserved, not corrected.

## Verification summary (the patch script's asserted invariants)

- 4 designed edits / 4 designed lines (1 title + 1 header note + 1
  v9.3-row relabel + 1 v9.4 table row); each old fragment asserted
  unique before replacement.
- `formalism-v9.3.md` re-read byte-identical after the pass.
- **Part I byte-identical between v9.3 and v9.4** (from
  "## 0. Status" up to "## RP0 — Mission statement").
- The lineage appendix carried forward with **zero** changes.
- Line-level difflib audit: every non-blank changed line matches a
  designed edit marker; no undesigned line touched.
- No proposition, truth-value, derivation, or registry row changed.

## Not done this round (deliberately)

- No manuscript change (v32 stands; the Tier-2 round's proposed v33
  sentence is recorded in
  `research/versions/tier2_interface_tension_20261012.md` for the
  author's call).
- No attribute-inventory alignment across manuscript / framework /
  `absolute.txt` (the audit's observation; no direction given).
- The v10.0 title quirk and the appendix wording precision point are
  recorded only — author files are never edited repo-side.
