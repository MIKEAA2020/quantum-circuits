#!/usr/bin/env python3
"""make_cert_v16.py -- ledger v16 for the v29 layout-polish pass.
Run from research/versions/.  Regenerates certificate_sha256_v16.txt
(8 hashes: manuscript v29 tex+pdf, supplement v10 tex+pdf, changelog,
README, ../../absolute.txt, the patch script).
"""
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

V = Path(__file__).resolve().parent.parent.parent / 'versions'

FILES = [
    'manuscript_revised_v29.tex', 'manuscript_revised_v29.pdf',
    'supplement_v10.tex', 'supplement_v10.pdf',
    'changelog_v29.md', 'README_v29.md',
    '../../absolute.txt',
    '../scripts/v22-exactZ3-n5L8/patch_v29_layout_polish.py',
]

ts = datetime.now(timezone(timedelta(hours=3))).strftime(
    '%Y-%m-%dT%H:%M:%S+03:00')
hdr = f"""# certificate_sha256_v16.txt -- ledger v16 (v29, the layout-polish +
# metaphysics + data-availability pass: the four column-overflowing
# tables (IV/V/VI/IX) promoted to two-column table* floats with
# byte-identical tabulars; the two clipped displays of the
# closed-form spectrum (eqs. (48)/(50)) re-set with every token
# preserved; Proposition 11's item label detached from the header;
# Sec. VII refers to the standing metaphysics as metaphysics
# throughout (established once as the working assumption); data
# availability names preprints.org and states the supplementary's
# web simulation formally; companion supplement_v10: the clipped SMC
# display split, the calibration table promoted, the reproduction
# block re-set as a list, six literal label-name references replaced
# by explicit main-text numbers)
# generated: {ts}
# v15 (v28) and earlier kept unmodified.
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

(V / 'certificate_sha256_v16.txt').write_text("\n".join(lines) + "\n")
print(f"{len(FILES)} files hashed -> certificate_sha256_v16.txt")
