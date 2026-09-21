"""v22_n4_eps_topup_v1.py -- L=8 lam_eps top-up for the marginal-q=4
log-correction analysis.

The deposited v18 chain has lam_eps (the second colour-trivial eigenvalue,
the epsilon-sector proxy) missing at L=8 for p >= 0.39
(n4_eps_L8_fast_v1.json stops at 0.38), which the v18 analysis bridged
with an un-deposited "projected epsilon top-up".  This script recomputes
the leading three colour-trivial (triv.triv, momentum-zero) eigenvalues of
C_comp^{(4)} at L=8, p in {0.38, 0.39, 0.40, 0.41} with the repaired
gap_utils machinery (n45_annealed_lib_v1.RingOperator, colour-restricted
Arnoldi), VALIDATING against the deposited fast-file value at p=0.38
(0.00114715...) before producing the new points.
"""
import sys, os, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'v18-n4n5-smc'))
sys.path.insert(0, os.path.join(HERE, '..'))
from n45_annealed_lib_v1 import RingOperator, leading_eigs

RES = os.path.join(HERE, '..', '..', 'results')
OUT = os.path.join(RES, 'v22-exactZ3-n5L8')


def log(*a):
    print(*a, flush=True)


def triv3(L, p, v0=None, tol=1e-11):
    op = RingOperator(4, 2, p, L // 2, beta=16, mom_k0=True,
                      colour=('triv', 'triv'))
    vals, vecs = leading_eigs(op, k_want=4, v0=v0, tol=tol)
    v1 = None
    if vecs is not None and vecs.shape[1] > 0:
        n0 = np.linalg.norm(vecs[:, 0])
        if n0 > 1e-300:
            v1 = vecs[:, 0] / n0
    return vals, v1


def main():
    pts = [0.38, 0.39, 0.40, 0.41]
    dep = {e['p']: e['triv3'][1] for e in
           json.load(open(f'{RES}/v18-n4n5-smc/n4_eps_L8_fast_v1.json'))}
    out = []
    v0 = None
    for p in pts:
        t0 = time.time()
        vals, v0 = triv3(8, p, v0=v0)
        row = {'p': p, 'L': 8, 'triv3': [float(v) for v in vals[:3]],
               'secs': round(time.time() - t0, 1)}
        if p in dep:
            rel = abs(vals[1] - dep[p]) / dep[p]
            row['dep_lam_eps'] = dep[p]
            row['rel_vs_dep'] = rel
            log(f"   p={p}: triv3 = {row['triv3']}  vs deposit "
                f"{dep[p]:.10f}  rel {rel:.2e}  "
                f"[{'OK' if rel < 1e-6 else 'FAIL'}]")
        else:
            log(f"   p={p}: triv3 = {row['triv3']}  (new)")
        out.append(row)
        json.dump(out, open(f'{OUT}/v22_n4_eps_topup.json', 'w'), indent=1)
    log(f"written {OUT}/v22_n4_eps_topup.json")


if __name__ == '__main__':
    main()
