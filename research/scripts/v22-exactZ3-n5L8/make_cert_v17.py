#!/usr/bin/env python3
"""make_cert_v17.py -- ledger v17 for the v30 web-simulation hosting pass.
Run from research/versions/.  Regenerates certificate_sha256_v17.txt
(8 hashes: manuscript v30 tex+pdf, supplement v10 tex+pdf (companion,
carried forward unchanged), changelog_v30, README_v30,
../../absolute.txt, the patch script).
"""
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

V = Path(__file__).resolve().parent.parent.parent / 'versions'

FILES = [
    'manuscript_revised_v30.tex', 'manuscript_revised_v30.pdf',
    'supplement_v10.tex', 'supplement_v10.pdf',
    'changelog_v30.md', 'README_v30.md',
    '../../absolute.txt',
    '../scripts/v22-exactZ3-n5L8/patch_v30_webhost.py',
]

ts = datetime.now(timezone(timedelta(hours=3))).strftime(
    '%Y-%m-%dT%H:%M:%S+03:00')
hdr = f"""# certificate_sha256_v17.txt -- ledger v17 (v30, the web-simulation
# hosting pass: the data availability statement gives the hosted URL
# of the web simulation -- https://mikeaa2020.github.io/
# quantum-circuits/web-simulation/ -- replacing the v29
# supplementary-inclusion framing; every description clause carried
# verbatim, asserted; the deposited-artifact list and the preprints.org
# DOI sentence untouched; the companion supplement_v10 carries no
# such reference and passes forward unchanged; the web simulation
# artifact itself is committed at web-simulation/ (one
# self-contained offline index.html, 737 KB, browser-verified via
# file://, plus web_simulation.zip for archival upload, .nojekyll
# markers for Pages serving))
# generated: {ts}
# v16 (v29) and earlier kept unmodified.
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

(V / 'certificate_sha256_v17.txt').write_text("\n".join(lines) + "\n")
print(f"written: certificate_sha256_v17.txt ({len(FILES)} hashes)")
for name in FILES:
    h = subprocess.run(['sha256sum', str(V / name)],
                       capture_output=True, text=True).stdout.split()[0]
    print(f"  {h[:16]}…  {name}")
