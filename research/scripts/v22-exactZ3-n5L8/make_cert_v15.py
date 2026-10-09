"""Generate certificate_sha256_v15.txt -- the v28 (demotion +
interpretive-status pass) round ledger.  Incremental over v14 (the
v27 extension-integration pass): hashes the v28 version files, the
unchanged companion supplement v9 (still the submission pair), the
new standing document absolute.txt (repository root), the changelog,
the README, and the v28 patch script."""
import hashlib, os, datetime

VER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '..', 'versions')
SCR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCR, '..', '..', '..'))

FILES_VER = ['manuscript_revised_v28.tex',
             'manuscript_revised_v28.pdf',
             'supplement_v9.tex',
             'supplement_v9.pdf',
             'changelog_v28.md', 'README_v28.md']
FILES_ROOT = ['absolute.txt']
FILES_SCR = ['patch_v28_absolute_interpret.py']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


out = ['# certificate_sha256_v15.txt -- ledger v15 (v28, the demotion +',
       '# interpretive-status pass: Sec. III worst-case complexity',
       '# demoted verbatim to Appendix C with a summary subsection left in',
       '# the main text (zero content loss, asserted in the patch script);',
       '# new Sec. VII "Interpretive status of the record formalism"; the',
       '# standing working assumption deposited as absolute.txt at the',
       '# repository root)',
       '# generated: ' + datetime.datetime.now(
           datetime.timezone.utc).strftime(
           '%Y-%m-%dT%H:%M:%SZ'),
       '# v14 (v27) and earlier kept unmodified.',
       '# The supplement is unchanged this pass (v9 remains the companion).',
       '# The 830 MB canonical-id array ids_nb4.npy is NOT deposited (GitHub',
       '# 100 MB limit) and is REUSED unchanged from the v23 round (it is',
       '# d-independent; the post-rollback rebuild was verified'
       ' byte-identical).']
for f in FILES_VER:
    out.append(f"{sha(os.path.join(VER, f))}  {f}")
out.append('')
out.append('# the standing document (research record, not submitted text):')
for f in FILES_ROOT:
    out.append(f"{sha(os.path.join(ROOT, f))}  ../../{f}")
out.append('')
out.append('# the v28 patch script (contains the no-content-loss assertions):')
for f in FILES_SCR:
    out.append(f"{sha(os.path.join(SCR, f))}  "
               f"../scripts/v22-exactZ3-n5L8/{f}")
txt = '\n'.join(out) + '\n'
open(os.path.join(VER, 'certificate_sha256_v15.txt'), 'w').write(txt)
print(txt)
print(f'... ({len(out)} lines total)')
