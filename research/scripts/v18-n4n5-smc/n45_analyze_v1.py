"""Master analysis (v1): n=4 crossings/universality + n=5 first-order test.

Assembles from:
  mipt_results/n4_annealed_scan_L{4,6,8}_v1.json  (classification scans)
  mipt_results/n4_eps_L8_v1.json                   (lam_eps top-up at L=8)
  mipt_results/n4_growth_v1.json                   (growth-rate chain)
  mipt_results/n5_annealed_scan_v1.json            (n=5 L=4 diagnostics)
  mipt_results/n4_colour_table_v1.json             (25-block table)
  mipt_results/n5_colour_table_v1.json             (49-block table)
  deposited n3 results (n3_annealed_final.json) for the trend comparison.

Deliverables:
  n=4: X_L curves, consecutive-size crossings, p_c^{(4)} extrapolations,
       amplitude ratio R_L (q=4 Potts prediction 1/8 with log corrections),
       gap law / xi/L (continuous), slope exponent 1/nu_eff (q=4: 3/2),
       lam1 simplicity, growth-rate chain.
  n=5: X_4 curve + sharpness, gap12 = log(lam1/lam2) (two-phase degeneracy),
       gap at the X_4 minimum vs n=2,3,4 at L=4 (first-order contrast),
       colour content.
  Writes mipt_results/n45_final_v1.json and a printed report.
"""
import sys, os, json, math
import numpy as np

OUT = 'mipt_results'
def log(*a):
    print(*a, flush=True)

def load(fn):
    try:
        return json.load(open(f'{OUT}/{fn}'))
    except Exception:
        return None

def interp_crossing(xs1, ys1, xs2, ys2):
    """Last crossing (linear interp) of two curves on a common grid."""
    x1 = dict(zip(xs1, ys1)); x2 = dict(zip(xs2, ys2))
    common = sorted(set(x1) & set(x2))
    cross = []
    for a, b in zip(common[:-1], common[1:]):
        f1a, f1b = x1[a] - x2[a], x1[b] - x2[b]
        if f1a == 0:
            cross.append(a)
        elif f1a * f1b < 0:
            cross.append(a + (b - a) * (-f1a) / (f1b - f1a))
    return cross

def main():
    res = {}
    # ---------------- n=4 ----------------
    scans = {L: load(f'n4_annealed_scan_L{L}_v1.json') for L in (4, 6, 8)}
    eps8 = load('n4_eps_v1.json') or {}
    if not eps8:
        eps8 = {}
        for L in (4, 6):
            d = load(f'n4_eps_L{L}_v1.json')
            if d:
                eps8[str(L)] = d
        d = load('n4_eps_L8_fast_v1.json')
        if d:
            eps8['8'] = d
    log("=== n=4: X_L(p) = L log(lam1/lam_sigma) ===")
    X, LAM = {}, {}
    for L in (4, 6, 8):
        rows = [r for r in scans[L] if r and r.get('lam1') and
                r.get('lam_sigma')]
        X[L] = ([r['p'] for r in rows],
                [L * math.log(r['lam1'] / r['lam_sigma']) for r in rows])
        LAM[L] = {r['p']: (r['lam1'], r['lam_sigma'], r.get('lam_eps'))
                  for r in rows}
        pts = list(zip(X[L][0], X[L][1]))
        s = '  '.join(f"{p:.3f}:{x:.3f}" for p, x in
                      pts[::max(1, len(pts) // 8)])
        log(f"  L={L}: {s}")
    # merge lam_eps top-ups into every L
    for L in (4, 6, 8):
        for row in (eps8.get(str(L)) or []):
            p = row['p']
            if p in LAM[L]:
                l1, ls, _ = LAM[L][p]
                LAM[L][p] = (l1, ls, row['triv3'][1])
    log("=== n=4 consecutive-size crossings ===")
    crossings = []
    for (L1, L2) in [(4, 6), (6, 8)]:
        cr = interp_crossing(*X[L1], *X[L2])
        if cr:
            c = cr[-1]
            crossings.append({'pair': [L1, L2], 'p': c})
            # values at crossing
            def at(L, p):
                ps, xs = X[L]
                return float(np.interp(p, ps, xs))
            def gapat(L, p):
                ps = sorted(LAM[L])
                gs = [math.log(LAM[L][q][0] / LAM[L][q][1]) for q in ps]
                return float(np.interp(p, ps, gs))
            def epsat(L, p):
                ps = sorted(q for q in LAM[L] if LAM[L][q][2])
                gs = [math.log(LAM[L][q][0] / LAM[L][q][2]) for q in ps]
                return float(np.interp(p, ps, gs))
            g1, g2 = gapat(L1, c), gapat(L2, c)
            crossings[-1].update({'X_at': [at(L1, c), at(L2, c)],
                                  'gap': [g1, g2],
                                  'xi_over_L': [1.0 / (L1 * g1),
                                                1.0 / (L2 * g2)]})
            log(f"  ({L1},{L2}): p* = {c:.5f}  X = {at(L1,c):.4f}/"
                f"{at(L2,c):.4f}  gap = {g1:.4f}/{g2:.4f}  "
                f"xi/L = {1.0/(L1*g1):.3f}/{1.0/(L2*g2):.3f}")
        else:
            log(f"  ({L1},{L2}): no crossing on the grid")
    # amplitude ratio R at the last crossing
    if crossings:
        pc4 = crossings[-1]['p']
        log(f"=== n=4 amplitude ratio R = log(l1/l_sig)/log(l1/l_eps) "
            f"near p = {pc4:.4f} ===")
        R = {}
        for L in (4, 6, 8):
            ps = sorted(q for q in LAM[L] if LAM[L][q][2])
            if not ps:
                continue
            rat = [math.log(LAM[L][q][0] / LAM[L][q][1]) /
                   math.log(LAM[L][q][0] / LAM[L][q][2]) for q in ps]
            rr = float(np.interp(pc4, ps, rat))
            R[L] = rr
            log(f"  L={L}: R = {rr:.4f}  (Ising 1/8 = 0.125, "
                f"Potts-3 1/6 = 0.1667; q=4 Potts -> 1/8 with log "
                f"corrections)")
        res['ratio'] = R
    # slope exponent
    if crossings:
        pc4 = crossings[-1]['p']
        log(f"=== n=4 slope dX/dp at p ~ {pc4:.4f} ===")
        sl = {}
        for L in (4, 6, 8):
            ps, xs = X[L]
            sl[L] = float(np.interp(pc4, ps, np.gradient(xs, ps)))
            log(f"  L={L}: slope = {sl[L]:.4f}")
        Ls = sorted(sl)
        if len(Ls) >= 2:
            fits = []
            for a, b in zip(Ls[:-1], Ls[1:]):
                nu_inv = math.log(sl[b] / sl[a]) / math.log(b / a)
                fits.append(nu_inv)
                log(f"    1/nu_eff ({a},{b}) = {nu_inv:.3f}")
            res['nu_inv'] = fits
    # simplicity + growth
    log("=== n=4 growth lam1^{1/L} ===")
    gr = load('n4_growth_v1.json') or {}
    for L in (4, 6):
        if str(L) in gr:
            log(f"  L={L}: " + '  '.join(f"{p:.2f}:{g:.4f}"
                                          for p, g in gr[str(L)]))
    res['crossings'] = crossings
    res['X'] = {str(L): [list(X[L][0]), list(X[L][1])] for L in X}
    # ---------------- n=5 ----------------
    n5 = load('n5_annealed_scan_v1.json')
    if n5:
        log("=== n=5 L=4: X_4, gap12 = log(lam1/lam2) (two-phase "
            "degeneracy) ===")
        rows = [r for r in n5 if r.get('lam1') and r.get('lam_sigma')]
        X5 = [(r['p'], 4 * math.log(r['lam1'] / r['lam_sigma']))
              for r in rows]
        G12 = [(r['p'], r['gap12']) for r in n5 if r.get('gap12')]
        for (p, x), (_, g) in zip(X5, G12):
            log(f"  p={p:.3f}  X_4={x:+.4f}  gap12={g:.4f}")
        res['n5'] = {'X4': X5, 'gap12': G12}
        # gap12 minimum location (single-size transition indicator,
        # calibrated at n=4 where the minimum sits at the crossing region)
        gp = [q for q, _ in G12]; gv = [g for _, g in G12]
        if len(gp) > 3:
            imin = int(np.argmin(gv))
            res['n5']['gap12_min'] = {'p': gp[imin], 'value': gv[imin]}
            log(f"  n=5 gap12 minimum: p={gp[imin]:.3f} "
                f"(gap12={gv[imin]:.4f})")
        # n=4 calibration: gap12 minimum from the eps L=4 file
        eps4 = {r['p']: r['triv3'] for r in
                (load('n4_eps_L4_v1.json') or [])}
        if eps4:
            gp4 = sorted(eps4)
            gv4 = [math.log(eps4[q][0] / eps4[q][1]) for q in gp4]
            imin = int(np.argmin(gv4))
            res['n4_gap12_min'] = {'p': gp4[imin], 'value': gv4[imin]}
            log(f"  n=4 gap12 minimum (calibration): p={gp4[imin]:.3f} "
                f"(vs extrapolated pc4 ~ "
                f"{crossings[-1]['p'] + (crossings[-1]['p'] - crossings[-2]['p']):.3f})")
        # matched-p (p=0.40, L=4) comparison across n=3,4,5
        log("=== L=4 matched-p (p=0.40) comparison across n ===")
        comp = {}
        # n=4
        lam4 = {}
        for r in scans[4]:
            lam4[r['p']] = (r['lam1'], r.get('lam_sigma'))
        eps4 = {r['p']: r['triv3'] for r in
                (load('n4_eps_L4_v1.json') or [])}
        ps4, xs4 = X[4]
        comp[4] = {
            'X': float(np.interp(0.40, ps4, xs4)),
            'slope': float(np.interp(0.40, ps4, np.gradient(xs4, ps4))),
            'gap12': (math.log(eps4[0.40][0] / eps4[0.40][1])
                      if 0.40 in eps4 else None),
            'sig_gap': (math.log(lam4[0.40][0] / lam4[0.40][1])
                        if 0.40 in lam4 else None)}
        # n=3 from deposited
        try:
            n3 = [r for r in json.load(
                open(f'{OUT}/n3_annealed_scan_dense.json'))
                if r['L'] == 4]
            lam3 = {r['p']: (r['lam1'], r.get('lam_sigma'),
                             r.get('lam_eps')) for r in n3}
            n3X = [(r['p'], 4 * math.log(r['lam1'] / r['lam_sigma']))
                   for r in n3 if r.get('lam_sigma')]
            ps3 = [q for q, _ in n3X]; xx3 = [v for _, v in n3X]
            comp[3] = {
                'X': float(np.interp(0.40, ps3, xx3)),
                'slope': float(np.interp(0.40, ps3,
                                         np.gradient(xx3, ps3))),
                'gap12': (math.log(lam3[0.40][0] / lam3[0.40][2])
                          if 0.40 in lam3 and lam3[0.40][2] else None),
                'sig_gap': (math.log(lam3[0.40][0] / lam3[0.40][1])
                            if 0.40 in lam3 else None)}
        except Exception as e:
            log(f"  [n=3 comparison unavailable: {e}]")
        # n=5
        if X5:
            ps5 = [q for q, _ in X5]; xx5 = [v for _, v in X5]
            g12 = dict(G12)
            lam5 = {r['p']: (r['lam1'], r['lam_sigma']) for r in rows}
            comp[5] = {
                'X': float(np.interp(0.40, ps5, xx5)),
                'slope': float(np.interp(0.40, ps5,
                                         np.gradient(xx5, ps5))),
                'gap12': (float(np.interp(0.40, [q for q, _ in G12],
                                          [g for _, g in G12]))),
                'sig_gap': (math.log(lam5[0.40][0] / lam5[0.40][1])
                            if 0.40 in lam5 else None)}
        for n in sorted(comp):
            c = comp[n]
            log(f"  n={n}: X_4={c['X']:.4f}  slope={c['slope']:.2f}  "
                f"gap12={c['gap12']:.4f}  sig_gap={c['sig_gap']:.4f}")
        res['matched_p40'] = comp
        # sharpness + gap12 at each n's own estimated transition
        own = {3: 0.305, 4: 0.400, 5: 0.480}
        ownres = {}
        for n, pc in own.items():
            if n == 3:
                ps, xs = ps3, xx3
                g12 = None
                try:
                    g12 = math.log(lam3[0.30][0] / lam3[0.30][2])
                except Exception:
                    pass
            elif n == 4:
                ps, xs = ps4, xs4
                g12 = None
                if 0.40 in eps4:
                    g12 = math.log(eps4[0.40][0] / eps4[0.40][1])
            else:
                ps, xs = ps5, xx5
                g12 = float(np.interp(0.48, [q for q, _ in G12],
                                      [g for _, g in G12]))
            ownres[n] = {
                'pc': pc,
                'slope': float(np.interp(pc, ps, np.gradient(xs, ps))),
                'X': float(np.interp(pc, ps, xs)),
                'gap12': g12}
            log(f"  n={n} at own pc~{pc}: slope="
                f"{ownres[n]['slope']:.2f}  X_4={ownres[n]['X']:.3f}  "
                f"gap12={g12 if g12 else float('nan'):.4f}")
        res['own_pc'] = ownres
        json.dump(res, open(f'{OUT}/n45_final_v1.json', 'w'), indent=1)
    log(f"written {OUT}/n45_final_v1.json")

if __name__ == '__main__':
    main()
