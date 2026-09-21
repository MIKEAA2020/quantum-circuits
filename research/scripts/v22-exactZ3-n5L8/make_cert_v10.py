"""Generate certificate_sha256_v10.txt — the v23 (L=8 rung) round ledger."""
import hashlib, os, datetime

VER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'versions')
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'results', 'v22-exactZ3-n5L8')
SCR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'logs', 'v22-exactZ3-n5L8')

FILES_VER = ['manuscript_revised_v23_rung.tex',
             'manuscript_revised_v23_rung.pdf',
             'supplement_v6.tex', 'supplement_v6.pdf',
             'changelog_v23.md', 'README_v23_rung.md',
             'mipt_numerical_report_v11.md']
FILES_RES = ['v22_n5_L8_rung.json',
             'tmp_n5L8block/reps_nb4.npy',
             'tmp_n5L8block/counts_nb4.npy']
FILES_SCR = ['patch_v23_rung.py', 'make_cert_v10.py', 'followup_v23.sh',
             'run_chain.sh', 'v22_n5_L8_block_v1.py']
FILES_LOG = ['v22_n5_L8_block_ids.log', 'v22_n5_L8_block_run.log',
             'v22_n5_L8_block_run_p0.44.log', 'v22_n5_L8_block_run_p0.46.log',
             'v22_n5_L8_block_run_p0.47.log', 'v22_n5_L8_block_run_p0.48.log',
             'v22_n5_L8_block_run_p0.50.log', 'chain.log']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


out = ['# certificate_sha256_v10.txt — ledger v10 (v23, the n=5 L=8 rung '
       'completion)',
       '# generated: ' + datetime.datetime.utcnow().strftime(
           '%Y-%m-%dT%H:%M:%SZ'),
       '# v9 (v22) and earlier kept unmodified.',
       '# the 830 MB canonical-id array ids_nb4.npy is NOT deposited '
       '(GitHub 100 MB',
       '# file limit); regenerate it with '
       '`v22_n5_L8_block_v1.py ids` (deterministic).']
for f in FILES_VER:
    out.append(f"{sha(os.path.join(VER, f))}  {f}")
out.append('')
out.append('# the v23 rung results (the orbit table reps/counts are '
           'deposited):')
for f in FILES_RES:
    out.append(f"{sha(os.path.join(RES, f))}  ../results/v22-exactZ3-n5L8/{f}")
out.append('')
out.append('# the v23 scripts:')
for f in FILES_SCR:
    if f == 'make_cert_v10.py':
        continue
    out.append(f"{sha(os.path.join(SCR, f))}  ../scripts/v22-exactZ3-n5L8/{f}")
out.append('')
out.append('# the chain completion logs (per-p logs may be absent on a partial grid):')
for f in FILES_LOG:
    fp = os.path.join(LOG, f)
    if not os.path.exists(fp):
        out.append(f'ABSENT  ../logs/v22-exactZ3-n5L8/{f}')
        continue
    out.append(f"{sha(fp)}  ../logs/v22-exactZ3-n5L8/{f}")
txt = '\n'.join(out) + '\n'
open(os.path.join(VER, 'certificate_sha256_v10.txt'), 'w').write(txt)
print(txt[:1500])
print(f'... ({len(out)} lines total)')
