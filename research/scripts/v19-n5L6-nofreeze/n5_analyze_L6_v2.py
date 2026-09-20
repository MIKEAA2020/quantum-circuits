"""Two-size first-order battery v2: the n=5 L=6 results vs L=4 (and the
n=3, n=4 L=4->L=6 comparisons from the deposited v17/v18 scans).

Diagnostics (all colour-trivial sector unless stated):
  gap12(p)  = log(lam1/lam2)  -- two-phase degeneracy measure
  closing   = gap12_4(p) - gap12_6(p) at matched p (first-order: grows
              with L; continuous: power-law slow)
  sharpness = |d log(lam1)/dp| and |d(gap12)/dp| flank slopes
  X_L(p)    = L log(lam1/lam_sigma) (sigma sector, spectator at n=5)
  locator   = argmin gap12(p) per size (the two-phase swap point)

Usage:  python3 n5_analyze_L6_v2.py   (after the L=6 scan + f64spot finish)
"""
import sys, os, json, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = 'mipt_results'


def log(*a):
    print(*a, flush=True)


def load(fn):
    return json.load(open(f'{OUT}/{fn}'))


def curve(rows, key, pkey='p'):
    ps = np.array([r[pkey] for r in rows if r.get(key) is not None])
    vs = np.array([r[key] for r in rows if r.get(key) is not None])
    o = np.argsort(ps)
    return ps[o], vs[o]


def interp_at(ps, vs, p):
    return float(np.interp(p, ps, vs))


def gap12_from_eps(rows):
    """gap12 = log(lam1/lam_eps) for the deposited scans (lam_eps field)."""
    out = []
    for r in rows:
        if r.get('lam1') and r.get('lam_eps'):
            out.append({'p': r['p'],
                        'gap12': math.log(r['lam1'] / r['lam_eps'])})
    return out


def main():
    # ---------------- n=5 two-size ----------------
    L4 = load('n5_annealed_scan_v1.json')
    L6 = load('n5_L6_scan_v2.json')
    f64 = load('n5_L6_f64spot_v2.json') if os.path.exists(
        f'{OUT}/n5_L6_f64spot_v2.json') else []
    p4, g4 = curve(L4, 'gap12')
    p6, g6 = curve(L6, 'gap12')
    p4x, x4 = curve(L4, 'X') if any('X' in r for r in L4) else (None, None)
    # X at L=4: recompute from lam1/lam_sigma
    x4v = [4 * math.log(r['lam1'] / r['lam_sigma'])
           for r in L4 if r.get('lam1') and r.get('lam_sigma')]
    p4x = np.array([r['p'] for r in L4
                    if r.get('lam1') and r.get('lam_sigma')])
    p6x, x6 = curve(L6, 'X6')

    log("=== n=5 two-size battery (d=2) ===")
    log(f"grid L=4: {p4.min():.2f}..{p4.max():.2f} ({len(p4)} pts); "
        f"L=6: {p6.min():.2f}..{p6.max():.2f} ({len(p6)} pts)")
    # gap12 closing at matched p
    log("\ngap12 = log(lam1/lam2) at matched p:")
    log(f"{'p':>6} {'gap12_L4':>10} {'gap12_L6':>10} {'closing':>9}")
    for p in np.arange(0.32, 0.521, 0.02):
        if p <= p4.max() and p <= p6.max():
            a = interp_at(p4, g4, p)
            b = interp_at(p6, g6, p)
            log(f"{p:6.2f} {a:10.4f} {b:10.4f} {a-b:9.4f}")
    # minima
    i4 = int(np.argmin(g4)); i6 = int(np.argmin(g6))
    log(f"\ngap12 minimum: L=4 at p={p4[i4]:.3f} (value {g4[i6]:.4f}); "
        f"L=6 at p={p6[i6]:.3f} (value {g6[i6]:.4f})")
    # f64 confirmation of the minimum region
    if f64:
        log("f64 spot checks (confirmation of the f32 sweep):")
        for r in f64:
            log(f"  p={r['p']:.2f}: gap12 {r['gap12']:.5f}  "
                f"(f32 interp {interp_at(p6, g6, r['p']):.5f})")
    # sharpness of the two-phase structure: flank slopes of gap12
    for tag, (ps, gs) in [('L=4', (p4, g4)), ('L=6', (p6, g6))]:
        sl = np.gradient(gs, ps)
        log(f"\n{tag}: d(gap12)/dp over p: min {sl.min():.3f} "
            f"at p={ps[np.argmin(sl)]:.2f}; max {sl.max():.3f} "
            f"at p={ps[np.argmax(sl)]:.2f}")
    # X curves (sigma spectator)
    log(f"\nX_L = L log(lam1/lam_sigma):  X4(0.32)={x4v[0]:.4f} "
        f"X6(0.32)={x6[0]:.4f}; X4(0.52)={x4v[-1]:.4f} "
        f"X6(0.52)={x6[-1]:.4f}")
    # crossing of X4 and X6 on the grid?
    d = np.interp(p6x, p4x, np.array(x4v)) - x6
    sgn = np.sign(d)
    xsw = np.where(sgn[:-1] * sgn[1:] < 0)[0]
    if len(xsw):
        i = xsw[0]
        pc = (p6x[i] * abs(d[i+1]) + p6x[i+1] * abs(d[i])) / \
             (abs(d[i]) + abs(d[i+1]))
        log(f"X4-X6 crossing at p ~ {pc:.4f}")
    else:
        log(f"X4-X6 no crossing in grid (X4-X6 range "
            f"[{d.min():.3f}, {d.max():.3f}])")
    # sigma-sector sharpness |dX/dp| steepening with L -- WITH the n=3
    # continuous baseline (sigma condenses -> slope grows like a power of L)
    s4 = float(np.gradient(np.array(x4v), p4x).max())
    s6 = float(np.gradient(x6, p6x).max())
    log(f"|dX/dp| max: L=4 {s4:.2f}  L=6 {s6:.2f}  ratio {s6/s4:.2f} "
        f"(first-order: sigma decouples -> ratio ~ 1)")
    try:
        n3d = load('n3_annealed_scan_dense.json')
        log("  n=3 continuous baseline (sigma CONDENSES at p_c):")
        for L in (4, 6, 8, 10):
            rows = [r for r in n3d if r['L'] == L and
                    r.get('lam1') and r.get('lam_sigma')]
            ps = np.array([r['p'] for r in rows])
            xs = np.array([L * math.log(r['lam1'] / r['lam_sigma'])
                           for r in rows])
            m = (ps > 0.20) & (ps < 0.40)
            log(f"    L={L}: |dX/dp| max (0.20<p<0.40) "
                f"{float(np.abs(np.gradient(xs[m], ps[m])).max()):.2f}")
    except Exception as e:
        log(f"  n=3 baseline skipped ({e})")
    # gap12 plateau width (two-phase coexistence signature)
    def plateau(ps, gs, rel=0.01):
        gmin = gs.min()
        return float(((gs <= gmin + rel)).sum()) * \
            float(np.median(np.diff(np.sort(ps))))
    log(f"\ngap12 plateau width (+1% band): L=4 "
        f"{plateau(p4, g4):.3f}  L=6 {plateau(p6, g6):.3f}")

    # ---------------- n=3, n=4 L=4 -> L=6 comparisons ----------------
    log("\n=== matched two-size comparison across n (gap12 closing) ===")
    try:
        n3d = load('n3_annealed_scan_dense.json')
        n3 = {L: gap12_from_eps([r for r in n3d if r['L'] == L])
              for L in (4, 6, 8, 10)}
        for L in sorted(n3):
            ps = np.array([r['p'] for r in n3[L]])
            gs = np.array([r['gap12'] for r in n3[L]])
            at = float(np.interp(0.30, ps, gs))
            log(f"n=3 L={L}: gap12 at p=0.30: {at:.4f}  "
                f"(x L: {at*L:.2f})")
    except Exception as e:
        log(f"n=3 comparison skipped ({e})")
    # n=4: lam_eps from the dedicated eps files (v18 top-ups; two formats)
    try:
        n4rows = {}
        for L in (4, 6, 8):
            base = load(f'n4_annealed_scan_L{L}_v1.json')
            eps = load(f'n4_eps_L{L}_v1.json')
            epsmap = {}
            for e in eps:
                if isinstance(e, dict) and 'p' in e:
                    if e.get('triv3'):
                        epsmap[round(float(e['p']), 4)] = {
                            'lam_eps': e['triv3'][1]}
                    else:
                        for k in ('lam_eps', 'lam1'):
                            if e.get(k) is not None:
                                epsmap.setdefault(
                                    round(float(e['p']), 4), {})[k] = e[k]
            rows = []
            for r in base:
                rr = dict(r)
                em = epsmap.get(round(float(r['p']), 4), {})
                if 'lam_eps' in em:
                    rr['lam_eps'] = em['lam_eps']
                rows.append(rr)
            n4rows[L] = gap12_from_eps(rows)
        for L in sorted(n4rows):
            ps = np.array([r['p'] for r in n4rows[L]])
            gs = np.array([r['gap12'] for r in n4rows[L]])
            if len(ps):
                at = float(np.interp(0.38, ps, gs))
                log(f"n=4 L={L}: gap12 at p=0.38: {at:.4f}  "
                    f"(x L: {at*L:.2f})")
    except Exception as e:
        log(f"n=4 comparison skipped ({e})")
    # matched-p closing table at p=0.32 and the n=5 gap12-min region
    log("\nmatched-p gap12 closing, n=5 (L=4 -> L=6):")
    for p in (0.32, 0.40, 0.44, 0.48, 0.52):
        if p <= p6.max():
            log(f"  p={p:.2f}: {interp_at(p4, g4, p):.4f} -> "
                f"{interp_at(p6, g6, p):.4f}  "
                f"(closing {interp_at(p4, g4, p) - interp_at(p6, g6, p):.4f})")
    # the decisive discriminator: gap12 * L at each n's own transition
    log("\ngap12 x L at the own-transition point (continuous -> constant "
        "~ 2 pi x_eps; first-order -> growing):")
    try:
        n3d = load('n3_annealed_scan_dense.json')
        for L in (4, 6, 8, 10):
            rows = gap12_from_eps([r for r in n3d if r['L'] == L])
            ps = np.array([r['p'] for r in rows])
            gs = np.array([r['gap12'] for r in rows])
            log(f"  n=3 (p_c=0.305): L={L}: {float(np.interp(0.30, ps, gs))*L:.2f}")
    except Exception as e:
        log(f"  n=3 skipped ({e})")
    for pstar, tag in ((0.46, 'pc5-lo'), (0.48, 'pc5-mid'), (0.50, 'pc5-hi')):
        try:
            a = interp_at(p4, g4, pstar)
            b = interp_at(p6, g6, pstar) if pstar <= p6.max() else float('nan')
            log(f"  n=5 ({tag} p={pstar}): L=4: {a*4:.2f}"
                + (f"  L=6: {b*6:.2f}" if pstar <= p6.max() else ""))
        except Exception:
            pass


if __name__ == '__main__':
    main()
