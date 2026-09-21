"""Generate versions/certificate_sha256_v5.txt (new version) for the v18
files: scripts, results, logs, and the v18 manuscript/report/changelog."""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    # library + validation
    'n45_annealed_lib_v1.py',
    'n45_annealed_validate_v1.py',
    'n4_annealed_scan_v1.py',
    'n5_annealed_scan_v1.py',
    'n4_eps_L8_v1.py',
    'n45_analyze_v1.py',
    # SMC
    'haar_smc_lib_v1.py',
    'haar_smc_v1.py',
    'haar_smc_topup_v1.py',
    # results
    'mipt_results/n4_annealed_scan_L4_v1.json',
    'mipt_results/n4_annealed_scan_L6_v1.json',
    'mipt_results/n4_annealed_scan_L8_v1.json',
    'mipt_results/n4_annealed_scan_v1.json',
    'mipt_results/n4_colour_table_v1.json',
    'mipt_results/n4_growth_v1.json',
    'mipt_results/n4_eps_L4_v1.json',
    'mipt_results/n4_eps_L6_v1.json',
    'mipt_results/n4_eps_L8_v1.json',
    'mipt_results/n4_eps_L8_fast_v1.json',
    'mipt_results/n5_annealed_scan_v1.json',
    'mipt_results/n45_final_v1.json',
    'mipt_results/haar_smc_summary_v1.json',
]
# every per-(L,p) SMC file
for fn in sorted(os.listdir(os.path.join(HERE, 'mipt_results'))):
    if fn.startswith('haar_smc_L') and fn.endswith('_v1.json'):
        FILES.append(f'mipt_results/{fn}')
    if fn.startswith('haar_smc_topup') and fn.endswith('_v1.json'):
        FILES.append(f'mipt_results/{fn}')
# logs
for fn in ['n45_annealed_validate_v1.log', 'n4_scan_v1.log',
           'n5_scan_v1.log', 'haar_smc_v1.log',
           'haar_smc_topup_v1.log']:
    p = os.path.join(HERE, 'logs', fn)
    if os.path.exists(p):
        FILES.append(f'logs/{fn}')
# versions
for fn in ['manuscript_revised_v18_n4n5-smc.tex',
           'manuscript_revised_v18_n4n5-smc.pdf',
           'mipt_numerical_report_v7.md', 'changelog_v18.md',
           'README_v18_n4n5-smc.md', 'certificate_sha256_v5.txt']:
    p = os.path.join(HERE, 'versions', fn)
    if os.path.exists(p):
        FILES.append(f'versions/{fn}')

out = []
missing = []
for rel in FILES:
    p = os.path.join(HERE, rel)
    if not os.path.exists(p):
        missing.append(rel)
        continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    out.append(f"{h}  {rel}")
dst = os.path.join(HERE, 'versions', 'certificate_sha256_v5.txt')
open(dst, 'w').write('\n'.join(out) + '\n')
print(f"written {dst} with {len(out)} entries")
if missing:
    print("MISSING (not yet produced):")
    for m in missing:
        print("   ", m)
