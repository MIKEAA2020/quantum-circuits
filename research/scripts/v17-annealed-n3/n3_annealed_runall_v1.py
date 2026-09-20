"""Full runner for the annealed n=3 transition (v1) — daemon-safe.

1. dense scan  : n=3, d=2, L=4,6,8,10 on the combined p-grid.
2. block12     : n=3, d=2, L=12 (exact momentum blocks, k=0).
3. control2    : n=2, d=2, L=16..32 via momentum blocks on a fine grid near
                 p_c^{(2)}=0.233810; crossings must reproduce the deposited
                 Table benchmark (0.23319/0.23348/0.23361/0.23368).
4. analyze     : crossings, ratio, gap closure, nu, growth rates.
"""
import sys, os, time, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3_annealed_lib import (colour_blocks, ConfigSpace, make_colour_projector,
                             momentum_orbits, momentum_block, block_pair_leading,
                             build_S, sector_eigs_dense, momentum_content,
                             n2_pc2, n2_closed_spectrum)
from gap_utils import W_tensor

OUT = 'mipt_results'
os.makedirs(OUT, exist_ok=True)

def log(*a):
    print(*a, flush=True)

GRID = sorted(set([round(x, 4) for x in np.arange(0.05, 0.90, 0.05)] +
                  [round(x, 4) for x in np.arange(0.22, 0.42, 0.01)]))

def dense_records(n, d, p, nb):
    t0 = time.time()
    P, idx, W, S = build_S(n, d, p, nb)
    cs = ConfigSpace(len(P), nb)
    cb = colour_blocks(n)
    rec = {'p': p, 'L': 2 * nb, 'n': n, 'd': d}
    proj_t = make_colour_projector(cb[0], cs, P)
    v1, r1 = sector_eigs_dense(S, projs=[proj_t], k_want=1, seed=11)
    rec['lam1'] = float(v1[0])
    v2, r2 = sector_eigs_dense(S, projs=[proj_t], k_want=1,
                               deflate=[(float(v1[0]), r1[:, 0])], seed=12)
    rec['lam_eps'] = float(v2[0]) if len(v2) else None
    rec['mom1'] = momentum_content(r1[:, 0], cs)
    if r2 is not None and len(v2):
        rec['mom_eps'] = momentum_content(r2[:, 0], cs)
    best, bestname, bestmom = -1.0, None, None
    per_block = {}
    for blk in cb[1:]:
        proj = make_colour_projector(blk, cs, P)
        vv, rr = sector_eigs_dense(S, projs=[proj], k_want=1, seed=13)
        if len(vv):
            per_block[blk[0]] = float(vv[0])
            if float(vv[0]) > best:
                best, bestname = float(vv[0]), blk[0]
                bestmom = momentum_content(rr[:, 0], cs) if rr is not None else None
    rec['lam_sigma'] = best
    rec['sigma_block'] = bestname
    rec['mom_sigma'] = bestmom
    rec['per_block'] = per_block
    rec['growth'] = float(v1[0]) ** (1.0 / (2 * nb))
    rec['secs'] = round(time.time() - t0, 2)
    return rec

def block_records(n, d, p, nb, kmax=16):
    """Exact momentum-block records (k=0) for any n (n=2 and n=3).
    Sector-restricted: for each colour block, eigs on the projected block-pair
    operator (k=2 in the triv sector: lam1 and lam_eps; k=1 elsewhere)."""
    from scipy.sparse.linalg import LinearOperator, eigs
    t0 = time.time()
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    N = g ** nb
    labs = np.array(np.unravel_index(np.arange(N), (g,) * nb)).T
    orbits = momentum_orbits(labs, nb, g)
    cs = ConfigSpace(g, nb)
    cb = colour_blocks(n)
    B1, inc1, _ = momentum_block(W, labs, orbits, nb, g, 0, 'M1')
    B2, inc2, _ = momentum_block(W, labs, orbits, nb, g, 0, 'M2')
    dim = B1.shape[0]
    conc = np.concatenate([orbits[oi][1] for oi in inc1])
    pers = np.array([orbits[oi][2] for oi in inc1], dtype=float)
    pers_i = pers.astype(int)
    invsq = 1.0 / np.sqrt(pers)
    rec = {'p': p, 'L': 2 * nb, 'n': n, 'd': d, 'dim_k0': dim}
    rng = np.random.default_rng(17)
    def to_full(v):
        vf = np.zeros(N)
        vf[conc] = np.repeat(v * invsq, pers_i)
        return vf
    def to_block(wf):
        return np.add.reduceat(wf[conc], np.concatenate([[0], np.cumsum(pers_i)])[:-1]) * invsq
    per_block = {}
    lam_eps = None
    for blk in cb:
        proj = make_colour_projector(blk, cs, P)
        def matvec(v, proj=proj):
            x = B1 @ (B2 @ v)
            wf = proj(to_full(x))
            return to_block(wf)
        LO = LinearOperator((dim, dim), matvec=matvec, dtype=B1.dtype)
        # k=4 in the triv sector: ARPACK with k=2 can miss the 2nd eigenvalue
        # (spurious Ritz value); k=4 is validated to separate lam1/lam_eps.
        kw = 4 if blk[0].startswith('triv') else 1
        try:
            vals, _ = eigs(LO, k=min(kw, dim - 2), which='LR', v0=rng.standard_normal(dim),
                           maxiter=30000, tol=1e-13)
            vals = np.real(vals[np.abs(np.imag(vals)) < 1e-7])
            vals = np.sort(vals)[::-1]
        except Exception as e:
            log(f"    [block_records] eigs failed for {blk[0]}: {e}")
            vals = np.array([])
        if len(vals):
            per_block[blk[0]] = float(vals[0])
            if blk[0] == 'triv.triv,i+' and len(vals) > 1:
                lam_eps = float(vals[1])
    # consistency guard: every per-block leading must appear in the global top-k
    gv, _ = block_pair_leading(B1, B2, k_want=12)
    if gv is not None and len(gv):
        for k, v in per_block.items():
            if not np.any(np.abs(gv - v) < 1e-7 * max(abs(v), 1e-12)):
                log(f"    [block_records] WARNING: {k} leading {v:.8e} not in global top-12")
    del B1, B2
    rec['per_block'] = per_block
    rec['lam1'] = per_block.get('triv.triv,i+')
    rec['lam_eps'] = lam_eps
    nontriv = [(v, k) for k, v in per_block.items() if not k.startswith('triv')]
    if nontriv:
        v, k = max(nontriv)
        rec['lam_sigma'] = v
        rec['sigma_block'] = k
    if rec.get('lam1'):
        rec['growth'] = rec['lam1'] ** (1.0 / (2 * nb))
    rec['secs'] = round(time.time() - t0, 1)
    return rec

def step_dense():
    log(f"=== step 1: dense n=3 scan, L=4,6,8,10, {len(GRID)} p-values ===")
    out = []
    for nb in (2, 3, 4, 5):
        L = 2 * nb
        for p in GRID:
            r = dense_records(3, 2, float(p), nb)
            out.append(r)
            log(f"  L={L} p={p:.3f} lam1={r['lam1']:.8f} lam_sig={r['lam_sigma']:.8f} "
                f"({r['sigma_block']}) lam_eps={r['lam_eps']:.8f} "
                f"X={L*math.log(r['lam1']/r['lam_sigma']):.5f} [{r['secs']}s]")
            json.dump(out, open(f'{OUT}/n3_annealed_scan_dense.json', 'w'), indent=1)

def step_block12():
    log(f"=== step 2: block12 n=3, {len(GRID)} p-values ===")
    out = []
    for p in GRID:
        r = block_records(3, 2, float(p), 6)
        out.append(r)
        if r.get('lam1'):
            log(f"  L=12 p={p:.3f} lam1={r['lam1']:.8f} lam_sig={r['lam_sigma']:.8f} "
                f"({r.get('sigma_block')}) lam_eps={r.get('lam_eps')} "
                f"X={12*math.log(r['lam1']/r['lam_sigma']):.5f} [{r['secs']}s]")
        else:
            log(f"  L=12 p={p:.3f} FAILED")
        json.dump(out, open(f'{OUT}/n3_annealed_scan_block12.json', 'w'), indent=1)

def step_control2():
    """n=2 control via momentum blocks at L=16..32, fine grid near pc2."""
    pcs = n2_pc2(2)
    grid = [round(x, 5) for x in np.arange(pcs - 0.010, pcs + 0.012, 0.0005)]
    log(f"=== step 3: n=2 control blocks L=16..32, grid {grid[0]}..{grid[-1]} "
        f"({len(grid)} pts), pc2={pcs:.6f} ===")
    dep = {(16, 20): 0.23319, (20, 24): 0.23348, (24, 28): 0.23361, (28, 32): 0.23368}
    out = {}
    for nb in (8, 10, 12, 14, 16):
        L = 2 * nb
        recs = []
        for p in grid:
            r = block_records(2, 2, float(p), nb, kmax=8)
            lam_odd = r.get('per_block', {}).get('sgn.sgn,i+')
            r['lam_odd'] = lam_odd
            recs.append(r)
            if r.get('lam1') and lam_odd:
                log(f"  L={L} p={p:.4f} lam1={r['lam1']:.8f} lam_odd={lam_odd:.8f} "
                    f"lam_eps={r.get('lam_eps')} [{r['secs']}s]")
        out[str(L)] = [{'p': r['p'], 'lam1': r.get('lam1'),
                        'lam_odd': r.get('lam_odd'), 'lam_eps': r.get('lam_eps')}
                       for r in recs]
        json.dump(out, open(f'{OUT}/n2_control_blocks.json', 'w'), indent=1)
    # crossings
    log("  n=2 control crossings (vs deposited Table):")
    Ls = sorted(int(k) for k in out)
    res = []
    for i in range(len(Ls) - 1):
        L1, L2 = Ls[i], Ls[i + 1]
        a = {r['p']: L1 * math.log(r['lam1'] / r['lam_odd']) for r in out[str(L1)]
             if r.get('lam1') and r.get('lam_odd')}
        b = {r['p']: L2 * math.log(r['lam1'] / r['lam_odd']) for r in out[str(L2)]
             if r.get('lam1') and r.get('lam_odd')}
        common = sorted(set(a) & set(b))
        cross = None
        for u, v in zip(common[:-1], common[1:]):
            f1, f2 = a[u] - b[u], a[v] - b[v]
            if f1 == 0: cross = u
            elif f1 * f2 < 0:
                cross = u + (v - u) * (-f1) / (f2 - f1)
        if cross is not None:
            d = dep.get((L1, L2))
            log(f"    ({L1},{L2}): p* = {cross:.5f}"
                f"{'  deposited ' + str(d) + f'  diff {abs(cross-d):.5f}' if d else ''}")
            res.append({'pair': [L1, L2], 'p': cross, 'deposited': d})
    json.dump(res, open(f'{OUT}/n2_control_crossings.json', 'w'), indent=1)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--steps', default='1,2,3')
    args = ap.parse_args()
    t00 = time.time()
    steps = [int(x) for x in args.steps.split(',')]
    if 1 in steps: step_dense()
    if 2 in steps: step_block12()
    if 3 in steps: step_control2()
    log(f"=== runall done in {(time.time()-t00)/60:.1f} min ===")
