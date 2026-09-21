"""n=4 L=10 analysis: the (8,10) crossing and the slope through three
size-pairs.  X_L = L log(lam1/lam_sigma) from the deposited v18 L=4,6,8
scans and the new L=10 sweep."""
import sys, os, json, math
import numpy as np

OUT = 'mipt_results'


def log(*a):
    print(*a, flush=True)


def XL_rows(fn, L):
    d = json.load(open(f'{OUT}/{fn}'))
    rows = [r for r in d if r.get('lam1') and r.get('lam_sigma')]
    ps = np.array([r['p'] for r in rows])
    xs = np.array([L * math.log(r['lam1'] / r['lam_sigma']) for r in rows])
    o = np.argsort(ps)
    return ps[o], xs[o]


def cross(pa, xa, pb, xb):
    """crossings of two curves on their common p-range."""
    lo = max(pa.min(), pb.min())
    hi = min(pa.max(), pb.max())
    m = (pa >= lo - 1e-9) & (pa <= hi + 1e-9)
    ya = np.interp(pb, pa[m], xa[m])
    d = ya - xb
    s = np.sign(d)
    out = []
    for i in np.where(s[:-1] * s[1:] < 0)[0]:
        p1, p2 = pb[i], pb[i + 1]
        d1, d2 = d[i], d[i + 1]
        out.append((p1 * abs(d2) + p2 * abs(d1)) / (abs(d1) + abs(d2)))
    return out, lo, hi


def main():
    p4, x4 = XL_rows('n4_annealed_scan_L4_v1.json', 4)
    p6, x6 = XL_rows('n4_annealed_scan_L6_v1.json', 6)
    p8, x8 = XL_rows('n4_annealed_scan_L8_v1.json', 8)
    p10, x10 = XL_rows('n4_L10_scan_v2.json', 10)
    log(f"X_L curves: L4 ({p4.min():.2f}..{p4.max():.2f}), "
        f"L6, L8, L10 ({p10.min():.2f}..{p10.max():.2f}, "
        f"{len(p10)} pts)")
    for (pa, xa, pb, xb, tag) in [(p4, x4, p6, x6, '(4,6)'),
                                   (p6, x6, p8, x8, '(6,8)'),
                                   (p8, x8, p10, x10, '(8,10)')]:
        cs, lo, hi = cross(pa, xa, pb, xb)
        log(f"crossing {tag}: {['%.4f' % c for c in cs]} "
            f"(common range {lo:.2f}..{hi:.2f})")
    # slope exponent through the pairs: p*(L) crossing drift
    cs46 = cross(p4, x4, p6, x6)[0]
    cs68 = cross(p6, x6, p8, x8)[0]
    cs810 = cross(p8, x8, p10, x10)[0]
    if cs46 and cs68 and cs810:
        a, b, c = cs46[0], cs68[0], cs810[0]
        # p*(L) = pc + a L^{-1/nu - 2 + y} style: estimate 1/nu from the
        # successive-difference log-log (the deposited convention:
        # slope exponent from dX/dp at the crossings)
        log(f"crossing drift: {a:.4f} -> {b:.4f} -> {c:.4f}")
        r1 = (b - a)
        r2 = (c - b)
        log(f"successive drifts: {r1:.5f}, {r2:.5f} "
            f"(ratio {r2/r1 if r1 else float('nan'):.3f})")
    # slope of X at the crossings (the deposited 1/nu_eff diagnostic)
    for (pp, xx, tag) in [(p6, x6, 'X6'), (p8, x8, 'X8'),
                          (p10, x10, 'X10')]:
        if len(pp) > 2:
            sl = np.gradient(xx, pp)
            log(f"max|d{tag}/dp| = {np.abs(sl).max():.2f} "
                f"at p={pp[np.argmax(np.abs(sl))]:.2f}")
    # gap12 at L=10 (triv sector): from lam1, lam_eps
    d10 = json.load(open(f'{OUT}/n4_L10_scan_v2.json'))
    rows = [r for r in d10 if r.get('lam1') and r.get('lam_eps')]
    if rows:
        ps = np.array([r['p'] for r in rows])
        gs = np.array([math.log(r['lam1'] / r['lam_eps']) for r in rows])
        i = int(np.argmin(gs))
        log(f"L=10 gap12: min {gs[i]:.4f} at p={ps[i]:.2f}; "
            f"at p=0.38: {float(np.interp(0.38, ps, gs)):.4f} "
            f"(x L: {float(np.interp(0.38, ps, gs))*10:.2f})")


if __name__ == '__main__':
    main()
