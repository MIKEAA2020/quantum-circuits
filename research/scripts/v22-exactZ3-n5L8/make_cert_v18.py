#!/usr/bin/env python3
"""make_cert_v18.py -- ledger v18 for the v31 appearance-terms pass.
Run from research/versions/.  Regenerates certificate_sha256_v18.txt
(8 hashes: manuscript v31 tex+pdf, supplement v10 tex+pdf (companion,
carried forward unchanged), changelog_v31, README_v31,
../../absolute.txt, the patch script).
"""
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

V = Path(__file__).resolve().parent.parent.parent / 'versions'

FILES = [
    'manuscript_revised_v31.tex', 'manuscript_revised_v31.pdf',
    'supplement_v10.tex', 'supplement_v10.pdf',
    'changelog_v31.md', 'README_v31.md',
    '../../absolute.txt',
    '../scripts/v22-exactZ3-n5L8/patch_v31_appearance_terms.py',
]

ts = datetime.now(timezone(timedelta(hours=3))).strftime(
    '%Y-%m-%dT%H:%M:%S+03:00')
hdr = f"""# certificate_sha256_v18.txt -- ledger v18 (v31, the appearance-terms
# pass: Sec VII rewritten per the author's category-error diagnosis --
# the four analogies/identifications mapping attributes of the Absolute
# onto appearance-level features of the formalism are removed (the
# self-existence analogy for the primitive Born rule; the no-go read as
# an echo of the Absolute's undividedness; self-averaging framed as a
# one/many coincidence condition; the exactness program identified with
# virtuous circularity), together with the mirror pattern ("timeless
# characterizations", "immutable law", "appearance-stream",
# "self-appearance"); appearance is now described in its own terms --
# the Absolute's display: not a copy of it and not a mirror of it
# (maya: neither real nor unreal, neither identical with nor different
# from the Absolute), its structure its own (division, relation, time,
# change), no feature of it taken to reflect an attribute of the
# Absolute; the author's metaphysics statement (para 1) carried
# verbatim; every theorem reference, number, and citation preserved
# (asserted); line-multiset 1775->1775 visible lines, exactly 7 edited;
# tectonic: 42 pages (v30: 42), 605.20 KiB, zero new warnings (fresh
# v30 probe reproduces the identical warning classes), zero ?? refs;
# companion supplement_v10 carries no metaphysics content and passes
# forward unchanged)
# generated: {ts}
# v17 (v30) and earlier kept unmodified.
# The 830 MB canonical-id array ids_nb4.npy is NOT deposited (GitHub
# 100 MB limit) and is REUSED unchanged from the v23 round (it is
# d-independent; the post-rollback rebuild was verified
# byte-identical).
"""

lines = [hdr.rstrip('\n')]
for name in FILES:
    h = subprocess.run(['sha256sum', str(V / name)],
                       capture_output=True, text=True).stdout.split()[0]
    lines.append(f"{h}  {name}")

(V / 'certificate_sha256_v18.txt').write_text("\n".join(lines) + "\n")
print(f"written: certificate_sha256_v18.txt ({len(FILES)} hashes)")
for name in FILES:
    h = subprocess.run(['sha256sum', str(V / name)],
                       capture_output=True, text=True).stdout.split()[0]
    print(f"  {h[:16]}…  {name}")
