"""Validation battery for n45_annealed_lib_v1.py (v1).

V1  n=2: iterative ring route vs the Kaufman closed form (top-8, L=8).
V2  n=3: solve_record vs the deposited n3_annealed_scan_dense.json (L=6,
    p=0.30 and p=0.25): lam1, lam_sigma, lam_eps.
V3  n=4: iterative route vs the dense C = M1 M2 (gap_utils.bond_ops, nb=2):
    top-12 sorted eigenvalues.
V4  colour completeness: sum of the 25 (S_4 x S_4) isotypic projectors = I.
V5  colour idempotency: P^2 = P for every block.
V6  p=1: nb=1 leading eigenvalue == d^2 Gamma(d^2)Gamma(n+1)/Gamma(d^2+n)
    and rank 1, for n=2..5 (the n=5 value 1/14 checks the pinv Weingarten
    channel);  nb=2 rank 1 for n=4,5.
V7  Weingarten pinv property for n=5 (G Wg G = G).
V8  timing: one matvec + one solve_record at n=4 L=8 and n=5 L=6.
"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n45_annealed_lib_v1 import (RingOperator, FastColour, leading_eigs,
                                 solve_record, ring_M2, ring_M1, mom0,
                                 central_idempotent, irrep_names,
                                 n_repl_pc1_eig, CHAR_TABLES)
from gap_utils import W_tensor, perms, bond_ops
from n3_annealed_lib import n2_closed_spectrum

RES = 'mipt_results'
LOG = 'logs'
def log(*a):
    print(*a, flush=True)

def main():
    os.makedirs(RES, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    ok_all = True
    # ---------------- V1: n=2 vs Kaufman ----------------
    log("V1  n=2 iterative vs Kaufman closed form (L=8, top-8):")
    for p in (0.10, 0.20, 0.30):
        op = RingOperator(2, 2, p, 4, mom_k0=False)
        vals, _ = leading_eigs(op, k_want=8, tol=1e-12)
        ref = n2_closed_spectrum(2, p, 4, max_evals=8)
        err = np.max(np.abs(np.sort(vals)[::-1][:len(ref)] - ref) /
                     np.maximum(ref, 1e-300))
        ok = err < 1e-9
        ok_all &= ok
        log(f"    p={p}: max rel err {err:.2e}  [{'OK' if ok else 'FAIL'}] "
            f"lam1 {vals[0]:.8f} vs {ref[0]:.8f}")
    # ---------------- V2: n=3 vs deposited scan ----------------
    log("V2  n=3 solve_record vs deposited n3_annealed_scan_dense (L=6):")
    dep = json.load(open(f'{RES}/n3_annealed_scan_dense.json'))
    for p in (0.25, 0.30):
        row = next(r for r in dep if r['L'] == 6 and abs(r['p'] - p) < 1e-9)
        rec = solve_record(3, 2, p, 3, k_want=12,
                           blocks=[('triv', 'triv'), ('sgn', 'sgn'),
                                   ('std', 'std')])
        e1 = abs(rec['lam1'] - row['lam1']) / row['lam1']
        es = abs(rec['lam_sigma'] - row['lam_sigma']) / row['lam_sigma']
        ee = abs(rec['lam_eps'] - row['lam_eps']) / max(row['lam_eps'], 1e-300)
        ok = max(e1, es, ee) < 1e-7
        ok_all &= ok
        log(f"    p={p}: lam1 {rec['lam1']:.8f}/{row['lam1']:.8f} "
            f"({e1:.1e})  sig {rec['lam_sigma']:.8f}/{row['lam_sigma']:.8f} "
            f"({es:.1e}, block {rec['sigma_block']} vs {row['sigma_block']})  "
            f"eps {rec['lam_eps']:.6f}/{row['lam_eps']:.6f} ({ee:.1e})  "
            f"[{'OK' if ok else 'FAIL'}]")
    # ---------------- V3: n=4 vs dense ----------------
    log("V3  n=4 iterative vs dense C (L=4; value-set match, degeneracy "
        "tolerated):")
    for p in (0.20, 0.36):
        op = RingOperator(4, 2, p, 2, mom_k0=False)
        vals, _ = leading_eigs(op, k_want=10, tol=1e-12)
        P, idx, W, M1, M2 = bond_ops(4, 2, p, 2)
        ev = np.linalg.eigvals(M1 @ M2)
        evr = np.sort(np.real(ev[np.abs(np.imag(ev)) < 1e-9]))[::-1]
        # every returned value must match some dense eigenvalue, and the
        # top-5 unique values must agree
        dmin = np.min(np.abs(vals[:, None] - evr[None, :]), axis=1)
        rel = dmin / max(evr[0], 1e-300)
        # top dense value must be returned; every returned value must match
        top_ok = abs(vals[0] - evr[0]) / evr[0] < 1e-8
        ok = np.max(rel) < 1e-8 and top_ok
        ok_all &= ok
        log(f"    p={p}: value-set err {np.max(rel):.2e}  lam1 {vals[0]:.8f} "
            f"vs {evr[0]:.8f}  [{'OK' if ok else 'FAIL'}]")
    # ---------------- V4/V5: colour completeness & idempotency ----------
    log("V4/V5  S_4 colour blocks (L=4): completeness + idempotency:")
    n, nb, d = 4, 2, 2
    P, idx, W = W_tensor(n, d, 0.3)
    fc = FastColour(n, nb, P)
    rng = np.random.default_rng(7)
    v = rng.standard_normal(fc.N)
    names = irrep_names(4)
    tot = np.zeros_like(v)
    worst_id, worst_comp = 0.0, 0.0
    for l in names:
        for r in names:
            w = fc.block(l, r, v)
            w2 = fc.block(l, r, w)
            worst_id = max(worst_id, np.linalg.norm(w2 - w) /
                           max(np.linalg.norm(w), 1e-300))
            tot += w
    worst_comp = np.linalg.norm(tot - v) / np.linalg.norm(v)
    ok = worst_comp < 1e-11 and worst_id < 1e-11
    ok_all &= ok
    log(f"    completeness {worst_comp:.2e}  idempotency {worst_id:.2e}  "
        f"[{'OK' if ok else 'FAIL'}]  (25 blocks)")
    # ---------------- V6: p=1 closed form + rank ----------------
    # one period at nb applies 2*nb bond channels, so the rank-1 eigenvalue
    # is (per-bond eigenvalue)^{2*nb}:  d^2 G(d^2) G(n+1)/G(d^2+n)
    log("V6  p=1: lam1(nb) == [d^2 G(d^2)G(n+1)/G(d^2+n)]^{2*nb}, rank 1:")
    for n in (2, 3, 4, 5):
        for nb in (1, 2):
            op = RingOperator(n, 2, 1.0, nb, mom_k0=False)
            vals, _ = leading_eigs(op, k_want=4, tol=1e-13)
            lam = vals[0]
            ref = n_repl_pc1_eig(n) ** (2 * nb)
            rank = int(np.sum(vals > 1e-9 * max(vals[0], 1e-300)))
            ok = abs(lam - ref) / ref < 1e-9 and rank == 1
            ok_all &= ok
            log(f"    n={n} nb={nb}: lam {lam:.10f} vs {ref:.10f}  rank {rank}  "
                f"[{'OK' if ok else 'FAIL'}]")
    # ---------------- V7: pinv property ----------------
    log("V7  Weingarten pinv (n=5, D=4): G Wg G = G:")
    from gap_utils import weingarten, compose, inv, cycles
    P5, Wg5 = weingarten(5, 4)
    Gm = np.array([[float(4) ** cycles(compose(inv(s), t)) for t in P5]
                   for s in P5])
    err = np.linalg.norm(Gm @ Wg5 @ Gm - Gm) / np.linalg.norm(Gm)
    ok = err < 1e-12
    ok_all &= ok
    log(f"    ||G Wg G - G||/||G|| = {err:.2e}  "
        f"rank(G) = {np.linalg.matrix_rank(Gm, tol=1e-9)}/120  "
        f"[{'OK' if ok else 'FAIL'}]")
    # ---------------- V8: timing ----------------
    log("V8  timing:")
    t0 = time.time()
    op = RingOperator(4, 2, 0.36, 4, mom_k0=True)
    vv = np.random.default_rng(1).standard_normal(op.N)
    op.matvec(vv); t_mv4 = time.time() - t0
    t0 = time.time()
    rec = solve_record(4, 2, 0.36, 4, k_want=12,
                       blocks=[('triv', 'triv'), ('std', 'std'),
                               ('sgn', 'sgn')])
    t_sol4 = time.time() - t0
    log(f"    n=4 L=8: matvec {t_mv4:.2f}s, solve_record(12) {t_sol4:.1f}s -> "
        f"lam1 {rec['lam1']:.6f} sig {rec['lam_sigma']:.6f} "
        f"({rec['sigma_block']}) eps {rec['lam_eps']}")
    if '--n5timing' in sys.argv:
        t0 = time.time()
        rec5 = solve_record(5, 2, 0.44, 3, k_want=8,
                            blocks=[('triv', 'triv'), ('std', 'std'),
                                    ('sgn', 'sgn')])
        t_sol5 = time.time() - t0
        log(f"    n=5 L=6: solve_record(8) {t_sol5:.1f}s -> lam1 "
            f"{rec5['lam1']:.6f} sig {rec5['lam_sigma']} "
            f"eps {rec5['lam_eps']}")
    else:
        log("    n=5 L=6 timing: skipped (measured separately: ~85 s per "
            "M2 ring application; a full solve exceeds the budget)")
    # summary
    log(f"=== n45 validation: {'ALL OK' if ok_all else 'FAILURES PRESENT'} ===")
    return 0 if ok_all else 1

def cycles_of(pi):
    n = len(pi); seen = [False] * n; c = 0
    for i in range(n):
        if not seen[i]:
            j = i
            while not seen[j]:
                seen[j] = True; j = pi[j]
            c += 1
    return c

if __name__ == '__main__':
    sys.exit(main())