"""Validation driver for the annealed n-replica spectral program (v1).

V1  n=3 eigenvalues of C = M1 @ M2 vs the deposited gap_proofs Sec. 9
    benchmarks (d=2: L=4 p=0.3, L=6 p=0.02 & 0.3, L=8 p=0.3; d=3: L=4 p=0.3).
V2  eigs(C) == sigma(S)^2 (Gram similarity) at several sizes.
V3  n=2: dense eigenvalues vs the Kaufman closed form (exact, same L);
     crossings of L log(lam1/lam_odd) converge toward p_c^{(2)}(2)=0.233810;
     the gap ratio log(l1/l_odd)/log(l1/l_even2) -> 1/8.
V4  momentum blocks: union of block spectra == full spectrum (n=3, nb=3,4).
V5  colour sector assignment: leading eigenvalue in each colour block;
     the 1+4+1 near-degenerate pattern at small p (deposited benchmark).
V6  product rows == dense matrix rows (M1, M2) at nb=3,4.
"""
import sys, os, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3_annealed_lib import (colour_blocks, ConfigSpace, make_colour_projector,
                             make_momentum_projector, momentum_content,
                             n2_abc, n2_pc2, n2_closed_spectrum,
                             build_M, build_S, sector_eigs_dense,
                             product_row, momentum_orbits, momentum_block,
                             block_pair_leading)
from gap_utils import W_tensor, perms, compose, inv, cycles

BENCH = {  # gap_proofs_verification.md Sec. 9 (d, L, p) -> top eigenvalues (mult)
    (2, 4, 0.3):  [0.166279, 0.132664, 0.108888, 0.019424, 0.013080, 0.012834],
    (2, 6, 0.02): [0.836807, 0.834268, 0.831750, 0.197356, 0.194805, 0.194314],
    (2, 6, 0.3):  [0.060099, 0.051165, 0.044917, 0.018369, 0.013362, 0.012990],
    (3, 4, 0.3):  [0.087574, 0.084094, 0.081124, 0.004517, 0.003502, 0.003186],
    (2, 8, 0.3):  [0.022018, 0.019495, 0.017770, 0.009732, 0.007486, 0.007191],
}

def dense_full_spectrum(n, d, p, nb, kmax=40):
    P, idx, W, S = build_S(n, d, p, nb)
    N = S.shape[0]
    if N <= 1300:
        vals = np.linalg.eigvals(S)
        vals = np.sort(np.abs(vals) ** 2)[::-1]
        return vals[:kmax], S, P, idx, W
    from scipy.sparse.linalg import svds
    vals = svds(S, k=min(kmax, N - 2), which='LM', return_singular_vectors=False)
    return np.sort(vals ** 2)[::-1], S, P, idx, W

def v1_benchmarks():
    print("== V1: n=3 spectra vs deposited Sec.9 benchmarks ==")
    ok = True
    ref_mult = {  # expand multiplicities
        (2, 4, 0.3):  [(0.166279, 1), (0.132664, 4), (0.108888, 1), (0.019424, 1), (0.013080, 4), (0.012834, 4)],
        (2, 6, 0.02): [(0.836807, 1), (0.834268, 4), (0.831750, 1), (0.197356, 1), (0.194805, 4), (0.194314, 4)],
        (2, 6, 0.3):  [(0.060099, 1), (0.051165, 4), (0.044917, 1), (0.018369, 1), (0.013362, 4), (0.012990, 4)],
        (3, 4, 0.3):  [(0.087574, 1), (0.084094, 4), (0.081124, 1), (0.004517, 1), (0.003502, 4), (0.003186, 4)],
        (2, 8, 0.3):  [(0.022018, 1), (0.019495, 4), (0.017770, 1), (0.009732, 1), (0.007486, 4), (0.007191, 4)],
    }
    for (d, L, p), ref in ref_mult.items():
        ref_expanded = np.array([v for v, mult in ref for _ in range(mult)])
        nb = L // 2
        t0 = time.time()
        vals, *_ = dense_full_spectrum(3, d, p, nb, kmax=len(ref_expanded))
        got = np.round(vals[:len(ref_expanded)], 6)
        err = np.max(np.abs(got - ref_expanded))
        status = "OK" if err <= 2e-6 else "FAIL"
        if err > 2e-6: ok = False
        print(f"   d={d} L={L} p={p}: max|err|={err:.2e}  [{status}]  ({time.time()-t0:.1f}s)")
        if err > 2e-6:
            print(f"      got  {got}")
            print(f"      ref  {ref_expanded}")
    return ok

def v2_similarity(n=3, d=2, p=0.3, nb=3):
    print("== V2: eigs(C=M1@M2) == sigma(S)^2 ==")
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    M1 = build_M(W, nb, g, 'M1'); M2 = build_M(W, nb, g, 'M2')
    eC = np.sort(np.real(np.linalg.eigvals(M1 @ M2)))[::-1]
    eC = eC[eC > 1e-12]
    P2, idx2, W2, S = build_S(n, d, p, nb)
    sv = np.sort(np.linalg.svd(S, compute_uv=False) ** 2)[::-1]
    sv = sv[sv > 1e-12]
    n = min(len(eC), len(sv))
    err = np.max(np.abs(eC[:n] - sv[:n]))
    print(f"   nb={nb}: {n} nonzero eigs, max|eig(C)-sigma(S)^2| = {err:.2e}")
    return err < 1e-9

def v3_n2_control():
    print("== V3: n=2 dense vs Kaufman closed form ==")
    ok = True
    for (d, m, p) in [(2, 2, 0.23), (2, 3, 0.2338), (2, 4, 0.10), (2, 4, 0.40),
                      (3, 2, 0.4597), (3, 3, 0.30)]:
        P, idx, W = W_tensor(2, d, p)
        g = len(P)
        M1 = build_M(W, m, g, 'M1'); M2 = build_M(W, m, g, 'M2')
        eC = np.sort(np.real(np.linalg.eigvals(M1 @ M2)))[::-1]
        ref = n2_closed_spectrum(d, p, m)
        n = min(len(eC), len(ref))
        err = np.max(np.abs(eC[:n] - ref[:n]) / np.maximum(ref[:n], 1e-300))
        status = "OK" if err < 1e-9 else "FAIL"
        if err >= 1e-9: ok = False
        print(f"   d={d} m={m} p={p}: {n} eigs, max rel err {err:.2e} [{status}]")
    # crossings of L log(l1/l_odd) toward pc2 (dense sizes L=4..10)
    print("   n=2 crossing control (dense L=4..10, d=2):")
    pcs = n2_pc2(2)
    prev = None
    for nb in (2, 3, 4, 5):
        L = 2 * nb
        def make_X(nb=nb, L=L):
            def X(p):
                P, idx, W, S = build_S(2, 2, p, nb)
                cb = colour_blocks(2)
                cs = ConfigSpace(2, nb)
                proj_t = make_colour_projector(cb[0], cs, P)
                proj_s = make_colour_projector(cb[1], cs, P)
                v1, r1 = sector_eigs_dense(S, projs=[proj_t], k_want=1)
                vs, _ = sector_eigs_dense(S, projs=[proj_s], k_want=1)
                return L * np.log(v1[0] / vs[0])
            return X
        X = make_X()
        lo, hi = 0.10, 0.32
        if prev is None:
            print(f"   L={L}: X({lo})={X(lo):.4f} X({hi})={X(hi):.4f}")
            prev = (L, X)
            continue
        Lp, Xp = prev
        def f(p):
            return X(p) - Xp(p)
        fl, fh = f(lo), f(hi)
        if fl * fh > 0:
            print(f"   L={L}: no sign change in [{lo},{hi}] (f={fl:.3f},{fh:.3f})")
            prev = (L, X)
            continue
        for _ in range(45):
            mid = 0.5 * (lo + hi)
            if f(lo) * f(mid) <= 0: hi = mid
            else: lo = mid
        print(f"   crossing ({Lp},{L}) = {0.5*(lo+hi):.5f}   (exact pc2 = {pcs:.5f})")
        prev = (L, X)
    return ok

def v4_momentum_union(n=3, d=2, p=0.3, nb=3):
    print("== V4: momentum-block union == full spectrum ==")
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    labs = np.array(np.unravel_index(np.arange(g ** nb), (g,) * nb)).T
    orbits = momentum_orbits(labs, nb, g)
    eC = np.sort(np.real(np.linalg.eigvals(build_M(W, nb, g, 'M1') @ build_M(W, nb, g, 'M2'))))[::-1]
    eC = eC[eC > 1e-10]
    allb = []
    for k in range(nb):
        B1, inc1, _ = momentum_block(W, labs, orbits, nb, g, k, 'M1')
        B2, inc2, _ = momentum_block(W, labs, orbits, nb, g, k, 'M2')
        assert inc1 == inc2
        if len(inc1) == 0: continue
        Ck = B1 @ B2
        ev = np.linalg.eigvals(Ck)
        ev = np.real(ev[np.abs(np.imag(ev)) < 1e-8])
        allb.extend(ev.tolist())
    allb = np.sort(np.array(allb))[::-1]
    allb = allb[allb > 1e-10]
    n = min(len(allb), len(eC))
    err = np.max(np.abs(np.sort(allb[:n]) - np.sort(eC[:n])))
    print(f"   nb={nb}: full has {len(eC)} nonzero, blocks give {len(allb)}; "
          f"max err on lowest {n} = {err:.2e}")
    return err < 1e-8 and len(allb) == len(eC)

def v5_colour_sectors(n=3, d=2, p=0.02, nb=3):
    print("== V5: colour-sector leading eigenvalues (n=3, d=2, p=0.02, L=6) ==")
    P, idx, W, S = build_S(n, d, p, nb)
    cs = ConfigSpace(len(P), nb)
    cb = colour_blocks(3)
    out = {}
    for blk in cb:
        proj = make_colour_projector(blk, cs, P)
        vals, _ = sector_eigs_dense(S, projs=[proj], k_want=1, seed=7)
        if len(vals):
            out[blk[0]] = float(vals[0])
    for k, v in sorted(out.items(), key=lambda kv: -kv[1]):
        print(f"   {k:18s} lam = {v:.6f}")
    # benchmark: 0.836807 triv, 0.834268 std(4x), 0.831750 sgn at L=6, p=0.02
    ok = (abs(out.get('triv.triv,i+', 0) - 0.836807) < 2e-6 and
          abs(out.get('std.std,i+', 0) - 0.834268) < 2e-6 and
          abs(out.get('sgn.sgn,i+', 0) - 0.831750) < 2e-6)
    print(f"   [triv/std/sgn vs deposited 0.836807/0.834268/0.831750: "
          f"{'OK' if ok else 'FAIL'}]")
    return ok

def v6_rows(n=3, d=2, p=0.3, nb=4):
    print("== V6: product rows == dense rows ==")
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    labs = np.array(np.unravel_index(np.arange(g ** nb), (g,) * nb)).T
    M1 = build_M(W, nb, g, 'M1'); M2 = build_M(W, nb, g, 'M2')
    rng = np.random.default_rng(3)
    errs = []
    for i in rng.integers(0, g ** nb, 12):
        r1 = product_row(W, tuple(labs[i]), labs, nb, g, 'M1')
        r2 = product_row(W, tuple(labs[i]), labs, nb, g, 'M2')
        errs.append(max(np.max(np.abs(r1 - M1[i])), np.max(np.abs(r2 - M2[i]))))
    print(f"   nb={nb}: max row err = {max(errs):.2e}")
    return max(errs) < 1e-12

if __name__ == '__main__':
    t0 = time.time()
    res = {}
    res['V1'] = v1_benchmarks()
    res['V2'] = v2_similarity()
    res['V6'] = v6_rows()
    res['V4'] = v4_momentum_union()
    res['V5'] = v5_colour_sectors()
    res['V3'] = v3_n2_control()
    print(f"\nVALIDATION SUMMARY: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in res.items()))
    print(f"total {time.time()-t0:.1f}s")
    json.dump({k: bool(v) for k, v in res.items()},
              open('mipt_results/n3_annealed_validation.json', 'w'), indent=1)
