"""n=4 annealed scan (v1): full S_4 colour resolution at L = 4, 6, 8.

For every p on the grid: the leading momentum-k=0 eigenvalues of
C = M1 M2 with colour classification (triv.triv -> lam1, lam_eps;
std.std -> lam_sigma; ...), the growth rate, the momentum content of the
leading eigenvector, and the per-block maxima among the returned spectrum.

Phases:
  scan    : the p-grid at all three sizes (warm-started Arnoldi chain).
  blocks  : the complete 25-block colour table at L=4,6 (leading eigenvalue
            of every (lambda,mu) isotypic block via projected solves) at a
            few p values — the 'full S_4 colour resolution' record.
  growth  : a few extra p points at L=4,6 for the growth-rate chain.

All eigenvalues are exact finite-size transfer-matrix eigenvalues (no
statistical error).  Validated by n45_annealed_validate_v1.py (V1-V8).
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

CLS_BLOCKS = [('triv', 'triv'), ('sgn', 'sgn'), ('std', 'std'),
              ('stdsgn', 'stdsgn'), ('two', 'two'), ('triv', 'sgn'),
              ('triv', 'std'), ('sgn', 'std'), ('triv', 'two')]

def strip(rec):
    r = {k: v for k, v in rec.items() if k != 'v0_out'}
    return r

def phase_scan(args):
    grid = [round(x, 4) for x in np.arange(0.26, 0.4601, 0.01)]
    sizes = [int(x) for x in args.sizes.split(',')] if args.sizes else [4, 6, 8]
    k_want = 18
    for L in sizes:
        nb = L // 2
        out = []
        v0 = None
        log(f"--- n=4 scan L={L} (nb={nb}), {len(grid)} p-values, "
            f"k_want={k_want} ---")
        for p in grid:
            try:
                rec = solve_record(4, 2, float(p), nb, k_want=k_want,
                                   blocks=CLS_BLOCKS, v0=v0, beta=8)
            except Exception as e:
                log(f"  p={p}: FAILED ({e})")
                continue
            v0 = rec.pop('v0_out', None)
            out.append(strip(rec))
            X = (L * math.log(rec['lam1'] / rec['lam_sigma'])
                 if rec.get('lam_sigma') else float('nan'))
            log(f"  p={p:.3f} lam1={rec['lam1']:.8f} "
                f"sig={rec['lam_sigma']:.8f} ({rec.get('sigma_block')}) "
                f"eps={rec.get('lam_eps')} X={X:.5f} "
                f"mom1={rec.get('mom1', [0])[0]:.2f} [{rec['secs']}s]")
            json.dump(out, open(f'{OUT}/n4_annealed_scan_L{L}_v1.json', 'w'),
                      indent=1)
    # combined
    comb = {}
    for L in sizes:
        try:
            comb[str(L)] = json.load(
                open(f'{OUT}/n4_annealed_scan_L{L}_v1.json'))
        except Exception:
            pass
    json.dump(comb, open(f'{OUT}/n4_annealed_scan_v1.json', 'w'), indent=1)
    log(f"written {OUT}/n4_annealed_scan_v1.json")

def phase_blocks(args):
    """Complete 25-block colour table at L=4,6 via projected solves."""
    ps = [0.20, 0.30, 0.36, 0.42]
    names = irrep_names(4)
    res = {}
    for L in (4, 6):
        nb = L // 2
        res[str(L)] = {}
        for p in ps:
            tbl = {}
            for l in names:
                for r in names:
                    op = RingOperator(4, 2, p, nb, beta=8, mom_k0=True,
                                      colour=(l, r))
                    vals, _ = leading_eigs(op, k_want=3, tol=1e-10)
                    tbl[f"{l}.{r}"] = float(vals[0]) if len(vals) else None
            res[str(L)][f"{p:.2f}"] = tbl
            top3 = sorted(tbl.items(), key=lambda kv: -(kv[1] or 0))[:5]
            log(f"  L={L} p={p}: top blocks " +
                ", ".join(f"{k}={v:.6f}" for k, v in top3))
            json.dump(res, open(f'{OUT}/n4_colour_table_v1.json', 'w'),
                      indent=1)
    log(f"written {OUT}/n4_colour_table_v1.json")

def phase_growth(args):
    grid = [0.05, 0.15, 0.55, 0.75]
    res = {}
    for L in (4, 6):
        nb = L // 2
        res[str(L)] = []
        v0 = None
        for p in grid:
            rec = solve_record(4, 2, float(p), nb, k_want=6,
                               blocks=CLS_BLOCKS[:3], v0=v0)
            v0 = rec.pop('v0_out', None)
            res[str(L)].append([p, rec['growth']])
            log(f"  L={L} p={p}: growth {rec['growth']:.6f} "
                f"[{rec['secs']}s]")
    json.dump(res, open(f'{OUT}/n4_growth_v1.json', 'w'), indent=1)
    log(f"written {OUT}/n4_growth_v1.json")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['scan', 'blocks', 'growth'])
    ap.add_argument('--sizes', default=None)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    {'scan': phase_scan, 'blocks': phase_blocks,
     'growth': phase_growth}[args.phase](args)
