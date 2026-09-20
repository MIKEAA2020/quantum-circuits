"""n=5 annealed scan (v1): the q=n-Potts first-order test at L=4.

S_5 colour resolution (7 irreps: triv, sgn, std(4), stdsgn(4), three2(5),
three1(6), two2(5)) via the general-n machinery with the pinv Weingarten
channel (validated: the p=1 bond eigenvalue 1/14 and the pinv identity).

Per p on the grid:
  * classification solve (top-16, colour labels) -> lam1, lam_sigma;
  * triv.triv-projected solve (k=3) -> lam1, lam2, lam3 (the two-phase
    degeneracy diagnostic: at a first-order point lam2/lam1 -> 1);
  * growth rate, momentum content.
Plus the 49-block colour table at a few p (projected solves).

The first-order diagnostics assembled by n45_analyze_v1.py:
  gap12 = log(lam1/lam2) vs p (two-phase degeneracy), the X_4 curve and
  its sharpness, log(lam1/lam_sigma) at the X_4 minimum, all compared
  against the same observables at n=2,3,4 at L=4.
"""
import sys, os, json, math, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n45_annealed_lib_v1 import (RingOperator, solve_record, leading_eigs,
                                 irrep_names)

OUT = 'mipt_results'
LOG = 'logs'
def log(*a):
    print(*a, flush=True)

CLS_BLOCKS = None  # set in main

def strip(rec):
    return {k: v for k, v in rec.items() if k != 'v0_out'}

def phase_scan(args):
    grid = [round(x, 4) for x in np.arange(0.32, 0.5201, 0.01)]
    L = 4
    nb = L // 2
    out = []
    v0 = None
    log(f"--- n=5 scan L={L} (nb={nb}), {len(grid)} p-values ---")
    for p in grid:
        # (a) classification solve
        try:
            rec = solve_record(5, 2, float(p), nb, k_want=16,
                               blocks=CLS_BLOCKS, v0=v0, beta=8)
        except Exception as e:
            log(f"  p={p}: classification FAILED ({e})")
            rec = None
        # (b) triv.triv-projected solve for lam1, lam2, lam3
        try:
            op = RingOperator(5, 2, float(p), nb, beta=8, mom_k0=True,
                              colour=('triv', 'triv'))
            vals, _ = leading_eigs(op, k_want=3, tol=1e-11,
                                   v0=(v0 if v0 is not None else None))
            triv = [float(x) for x in vals[:3]]
        except Exception as e:
            log(f"  p={p}: triv solve FAILED ({e})")
            triv = [None, None, None]
        row = {'p': p, 'L': L, 'n': 5}
        if rec:
            v0 = rec.pop('v0_out', None)
            row.update({k: v for k, v in strip(rec).items()})
        row['triv3'] = triv
        row['gap12'] = (math.log(triv[0] / triv[1])
                        if triv[0] and triv[1] and triv[1] > 0 else None)
        out.append(row)
        X = (L * math.log(row['lam1'] / row['lam_sigma'])
             if row.get('lam1') and row.get('lam_sigma') else float('nan'))
        log(f"  p={p:.3f} lam1={row.get('lam1')} lam2={triv[1]} "
            f"gap12={row['gap12']} sig={row.get('lam_sigma')} "
            f"({row.get('sigma_block')}) X={X:.5f} [{row.get('secs')}s]")
        json.dump(out, open(f'{OUT}/n5_annealed_scan_v1.json', 'w'), indent=1)
    log(f"written {OUT}/n5_annealed_scan_v1.json")

def phase_blocks(args):
    names = irrep_names(5)
    ps = [0.30, 0.40, 0.45, 0.50]
    res = {}
    for p in ps:
        tbl = {}
        for l in names:
            for r in names:
                op = RingOperator(5, 2, p, 2, beta=8, mom_k0=True,
                                  colour=(l, r))
                vals, _ = leading_eigs(op, k_want=2, tol=1e-10)
                tbl[f"{l}.{r}"] = float(vals[0]) if len(vals) else None
        res[f"{p:.2f}"] = tbl
        top5 = sorted(tbl.items(), key=lambda kv: -(kv[1] or 0))[:6]
        log(f"  p={p}: " + ", ".join(f"{k}={v:.3e}" for k, v in top5))
        json.dump(res, open(f'{OUT}/n5_colour_table_v1.json', 'w'), indent=1)
    log(f"written {OUT}/n5_colour_table_v1.json")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['scan', 'blocks'])
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    diag = [(l, r) for l in irrep_names(5) for r in irrep_names(5)
            if l == r]
    offd = [('triv', 'sgn'), ('triv', 'std'), ('sgn', 'std'),
            ('triv', 'three2'), ('sgn', 'three2')]
    CLS_BLOCKS = diag + offd
    {'scan': phase_scan, 'blocks': phase_blocks}[args.phase](args)
