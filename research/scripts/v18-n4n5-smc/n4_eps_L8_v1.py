"""n=4 lam_eps top-up (v1): triv.triv-projected solves at L = 4, 6, 8.

The classification scan (k_want=18) fills the top ranks with the colour
multiplets (std.std 9-fold, two.two 4-fold, stdsgn.stdsgn 9-fold, sgn.sgn)
before the second trivial eigenvalue, so lam_eps is missing for larger p.
The triv.triv-isotypic projection puts lam1, lam_eps at the top of its own
spectrum: a k=3 projected solve recovers both directly.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n45_annealed_lib_v1 import RingOperator, leading_eigs

OUT = 'mipt_results'

def main():
    res = {}
    for L in (4, 6, 8):
        nb = L // 2
        grid = [round(x, 4) for x in np.arange(0.26, 0.4601, 0.02)]
        rows = []
        for p in grid:
            op = RingOperator(4, 2, float(p), nb, beta=8, mom_k0=True,
                              colour=('triv', 'triv'))
            vals, _ = leading_eigs(op, k_want=3, tol=1e-11)
            rows.append({'p': p, 'L': L,
                         'triv3': [float(x) for x in vals[:3]]})
            print(f"  L={L} p={p}: lam1={vals[0]:.8f} "
                  f"lam_eps={vals[1]:.8f} lam3={vals[2]:.3e}", flush=True)
            json.dump(rows, open(f'{OUT}/n4_eps_L{L}_v1.json', 'w'),
                      indent=1)
        res[str(L)] = rows
    json.dump(res, open(f'{OUT}/n4_eps_v1.json', 'w'), indent=1)
    print(f"written {OUT}/n4_eps_v1.json")

if __name__ == '__main__':
    main()
