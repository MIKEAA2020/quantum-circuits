"""Generate certificate_sha256_v9.txt — the v22 round ledger."""
import hashlib, os, datetime

VER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'versions')
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'results', 'v22-exactZ3-n5L8')
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
LEG = os.path.join(VER, 'v17-annealed-n3') if False else None

FILES_VER = ['manuscript_revised_v22_exactZ3.tex',
             'manuscript_revised_v22_exactZ3.pdf',
             'supplement_v5.tex', 'supplement_v5.pdf',
             'changelog_v22.md', 'README_v22_exactZ3.md',
             'mipt_numerical_report_v10.md']
FILES_RES = sorted(os.listdir(RES))
FILES_SCR = sorted(f for f in os.listdir(SCR) if f.endswith('.py')
                   or f == 'run_chain.sh')
# the gap_utils copies that repair the reproduction chain
COPIES = [os.path.join('..', 'v17-annealed-n3', 'gap_utils.py'),
          os.path.join('..', 'v18-n4n5-smc', 'gap_utils.py'),
          os.path.join('..', 'v19-n5L6-nofreeze', 'gap_utils.py')]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


out = ['# certificate_sha256_v9.txt — ledger v9 (v22, the exact Zbar_3 '
       'closure round)',
       '# generated: ' + datetime.datetime.utcnow().strftime(
           '%Y-%m-%dT%H:%M:%SZ'),
       '# v8 (v21) and earlier kept unmodified.',
       '# includes the gap_utils.py copies that repair the v17-v19 '
       'reproduction chain.']
for f in FILES_VER:
    out.append(f"{sha(os.path.join(VER, f))}  {f}")
out.append('')
out.append('# the v22 exact-closure suite (results):')
for f in FILES_RES:
    if f == 'tmp_n5L8block':
        continue
    out.append(f"{sha(os.path.join(RES, f))}  ../results/v22-exactZ3-n5L8/{f}")
out.append('')
out.append('# the v22 exact-closure suite (scripts):')
for f in FILES_SCR:
    if f == 'make_cert_v9.py':
        continue
    out.append(f"{sha(os.path.join(SCR, f))}  ../scripts/v22-exactZ3-n5L8/{f}")
out.append('')
out.append('# the reproduction-chain repair (identical copies):')
for c in COPIES:
    out.append(f"{sha(os.path.join(SCR, c))}  ../scripts/{c.replace('../', '', 1)}")
txt = '\n'.join(out) + '\n'
open(os.path.join(VER, 'certificate_sha256_v9.txt'), 'w').write(txt)
print(txt[:1500])
print(f'... ({len(out)} lines total)')
