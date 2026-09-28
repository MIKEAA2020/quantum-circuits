"""Generate certificate_sha256_v13.txt -- the v26 (closing-rate diagnostics
pass) round ledger.  Incremental over v12 (the v25 TJP editorial pass):
hashes the v26 version files, the completed v25 extension results (the
d=3 locator scans and the queue config), the v26/extension scripts, and
the d=3 validation log."""
import hashlib, os, datetime

VER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'versions')
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'results', 'v22-exactZ3-n5L8')
SCR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'logs', 'v25-n5L8-ext')

FILES_VER = ['manuscript_revised_v26.tex',
             'manuscript_revised_v26.pdf',
             'supplement_v8.tex', 'supplement_v8.pdf',
             'changelog_v26.md', 'README_v26.md']
FILES_RES = ['v25_n5_d3_locator.json', 'v25_ext_config.json']
FILES_SCR = ['patch_v26_closing.py', 'v25_n5_L8_ext_v1.py',
             'drive_v25_ext.sh', 'v25_sigma_extract.py']
FILES_LOG = ['validate_d3.log']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


out = ['# certificate_sha256_v13.txt -- ledger v13 (v26, the closing-rate',
       '# rates table, the last-digit fix, Supplement v8 with the d=3',
       '# local-dimension extension; the d=3 L=8 rung and the finer grid follow)',
       '# generated: ' + datetime.datetime.utcnow().strftime(
           '%Y-%m-%dT%H:%M:%SZ'),
       '# v12 (v25, the TJP editorial pass) and earlier kept unmodified.',
       '# In-flight results (v25_n5_L8_rung_d3.json, v25_n5_L8_finegrid.json)',
       '# are committed and hashed by the watch rounds as their points',
       '# complete; the 830 MB canonical-id array ids_nb4.npy is NOT deposited',
       '# (GitHub 100 MB limit) and is REUSED unchanged from the v23 round',
       '# (it is d-independent).']
for f in FILES_VER:
    out.append(f"{sha(os.path.join(VER, f))}  {f}")
out.append('')
out.append('# the v25 extension results (locator scans complete; queue config):')
for f in FILES_RES:
    out.append(f"{sha(os.path.join(RES, f))}  ../results/v22-exactZ3-n5L8/{f}")
out.append('')
out.append('# the v26/extension scripts:')
for f in FILES_SCR:
    out.append(f"{sha(os.path.join(SCR, f))}  ../scripts/v22-exactZ3-n5L8/{f}")
out.append('')
out.append('# the d=3 validation log (block route vs Arnoldi + p=1 anchors):')
for f in FILES_LOG:
    fp = os.path.join(LOG, f)
    if not os.path.exists(fp):
        out.append(f'ABSENT  ../logs/v25-n5L8-ext/{f}')
        continue
    out.append(f"{sha(fp)}  ../logs/v25-n5L8-ext/{f}")
txt = '\n'.join(out) + '\n'
open(os.path.join(VER, 'certificate_sha256_v13.txt'), 'w').write(txt)
print(txt[:1600])
print(f'... ({len(out)} lines total)')
