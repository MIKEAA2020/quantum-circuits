"""Fast lam_eps top-up at L=8 (v1): warm-started, tol 1e-9, focused grid."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n45_annealed_lib_v1 import RingOperator, leading_eigs

OUT = 'mipt_results'
rows = []
v0 = None
for p in [round(x, 4) for x in np.arange(0.32, 0.4201, 0.02)]:
    op = RingOperator(4, 2, float(p), 4, beta=8, mom_k0=True,
                      colour=('triv', 'triv'))
    vals, vecs = leading_eigs(op, k_want=3, tol=1e-9, v0=v0)
    if vecs is not None and vecs.shape[1] > 0:
        v0 = vecs[:, 0] / (np.linalg.norm(vecs[:, 0]) + 1e-300)
    rows.append({'p': p, 'L': 8, 'triv3': [float(x) for x in vals[:3]]})
    print(f"  L=8 p={p}: lam1={vals[0]:.8f} lam_eps={vals[1]:.8f}",
          flush=True)
    json.dump(rows, open(f'{OUT}/n4_eps_L8_fast_v1.json', 'w'), indent=1)
print(f"written {OUT}/n4_eps_L8_fast_v1.json")
