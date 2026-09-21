"""v22_q4_logcorr_v1.py -- the marginal-q=4 log-correction analysis of the
n=4 annealed chain (L = 4, 6, 8, 10; the deposited v18/v19 scans).

BACKGROUND.  The v18 reading of the n=4 amplitude-ratio diagnostic
(R = log(lam1/lam_sigma)/log(lam1/lam_eps) at the consecutive-size
crossings of X_L = L log(lam1/lam_sigma)): "it starts at the q=4 value 1/8
at L=4 and drifts upward, past both the Ising-like 1/8 and the q=3 value
1/6 --- the one clean diagnostic of n=2,3 degrades exactly where the
borderline class predicts", with the tabulated caption "The q=4 Potts
class shares the Ising values x_sigma/x_eps = 1/8".

THE CORRECTION THIS SCRIPT TESTS.  The q=4-Potts energy dimension is
x_eps = d - y_t = 2 - 3/2 = 1/2 (y_t = 1/nu = 3/2), so the amplitude-ratio
target is x_sigma/x_eps = (1/8)/(1/2) = 1/4 --- NOT the Ising 1/8 (which
requires x_eps = 1, i.e. y_t = 1).  The measured drift 0.128 -> 0.176 ->
0.203 is then not a degrading diagnostic but a LOGARITHMICALLY CONVERGENT
one: at the marginal point the effective scaling dimensions carry
1/ln L corrections (multiplicative logarithmic corrections, Cardy 1986),
x^{eff}_sigma(L) = x_sigma (1 + a_sigma/ln L), x^{eff}_eps(L) = x_eps
(1 + a_eps/ln L) + marginal-operator mixing, hence
    R(L) = 1/4 + a/ln L + O(1/ln^2 L).
The fits below test this marginal form against (i) the power-law
alternative R = 1/4 + a L^{-omega} and (ii) the v18 no-target reading,
for R, for the slope exponent 1/nu_eff (target 3/2, marginal form
slope_L = C L^{3/2} (1 + c/ln L)), and for the raw sigma gap
(gap_L * L = 2 pi x_sigma A_lat (1 + a_sigma/ln L)).  The n=3 chain
(L = 4..12, targets R -> 1/6, 1/nu -> 6/5) is run through the identical
machinery as the non-marginal control.

Data: results/v18-n4n5-smc/n4_annealed_scan_L{4,6,8}_v1.json (+eps
top-ups), results/v19-n5L6-nofreeze/n4_L10_scan_v2.json,
results/v17-annealed-n3/n3_annealed_scan_dense.json.
"""
import sys, os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', '..', 'results')
OUT = os.path.join(RES, 'v22-exactZ3-n5L8')


def log(*a):
    print(*a, flush=True)


def load(fn):
    return json.load(open(os.path.join(RES, fn)))


def curve(rows, key):
    ps = np.array([r['p'] for r in rows if r.get(key)])
    vs = np.array([r[key] for r in rows if r.get(key)])
    o = np.argsort(ps)
    return ps[o], vs[o]


def X_of(rows, L):
    """X_L(p) = L log(lam1/lam_sigma)."""
    ps = np.array([r['p'] for r in rows if r.get('lam1') and r.get('lam_sigma')])
    xs = np.array([L * math.log(r['lam1'] / r['lam_sigma']) for r in rows
                   if r.get('lam1') and r.get('lam_sigma')])
    o = np.argsort(ps)
    return ps[o], xs[o]


def crossing(pA, xA, pB, xB):
    """First sign change of X_A - X_B (X rises with p below pc)."""
    d = np.interp(pB, pA, xA) - xB
    s = np.sign(d)
    idx = np.where(s[:-1] * s[1:] < 0)[0]
    if not len(idx):
        return None, None
    i = idx[0]
    lo, hi = pB[i], pB[i + 1]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if (np.interp(mid, pA, xA) - np.interp(mid, pB, xB)) * \
                (np.interp(lo, pA, xA) - np.interp(lo, pB, xB)) <= 0:
            hi = mid
        else:
            lo = mid
    pc = 0.5 * (lo + hi)
    return pc, float(np.interp(pc, pB, xB))


def at_val(rows, key, p, L=None):
    ps, vs = curve(rows, key)
    return float(np.interp(p, ps, vs))


def slope_at(ps, xs, p, h=0.01):
    return float((np.interp(p + h, ps, xs) - np.interp(p - h, ps, xs))
                 / (2 * h))


def fit_log(x, y, target):
    """y = target + a/ln x (1 param).  Returns (a, rss, yhat)."""
    t = 1.0 / np.log(x)
    A = t
    a = float(A @ (y - target) / (A @ A))
    yh = target + a * t
    return a, float(((y - yh) ** 2).sum()), yh


def fit_pow(x, y, target):
    """y = target + a x^{-omega} (2 params, grid over omega)."""
    best = None
    for om in np.arange(0.2, 3.01, 0.01):
        t = x ** (-om)
        a = float(t @ (y - target) / (t @ t))
        yh = target + a * t
        rss = float(((y - yh) ** 2).sum())
        if best is None or rss < best[0]:
            best = (rss, om, a, yh)
    rss, om, a, yh = best
    return om, a, rss, yh


def fit_free_log(x, y):
    """y = b + a/ln x (2 params)."""
    T = np.column_stack([np.ones_like(x), 1.0 / np.log(x)])
    c, *_ = np.linalg.lstsq(T, y, rcond=None)
    yh = T @ c
    return float(c[0]), float(c[1]), float(((y - yh) ** 2).sum()), yh


def analyse_chain(name, sizes, rows_by_L, targets, pstar=None):
    """Crossings, R, gaps, slopes; marginal fits.  targets = (R_inf,
    inv_nu, x_sigma)."""
    log(f"== {name}: crossings and marginal fits ==")
    rows = []
    prev = None
    for L in sizes:
        ps, xs = X_of(rows_by_L[L], L)
        if prev is None:
            prev = (L, ps, xs)
            continue
        Lp, pA, xA = prev
        pc, Xc = crossing(pA, xA, ps, xs)
        if pc is None:
            log(f"   ({Lp},{L}): no crossing in range")
            prev = (L, ps, xs)
            continue
        r = rows_by_L[L]
        lam1 = at_val(r, 'lam1', pc)
        lam_s = at_val(r, 'lam_sigma', pc)
        lam_e = at_val(r, 'lam_eps', pc)
        R = math.log(lam1 / lam_s) / math.log(lam1 / lam_e)
        gap = math.log(lam1 / lam_s)
        sl = slope_at(ps, xs, pc)
        sl_prev = slope_at(pA, xA, pc)
        nu_eff = math.log(sl / sl_prev) / math.log(L / Lp)
        row = {'pair': f"({Lp},{L})", 'L': L, 'pc': round(pc, 4),
               'R': round(R, 4), 'gap': round(gap, 4),
               'slope': round(sl, 2), 'inv_nu_eff': round(nu_eff, 3),
               'Llog_le': round(L * math.log(lam1 / lam_e), 2)}
        rows.append(row)
        log(f"   ({Lp},{L}) pc={pc:.4f}: R={R:.4f}  gap={gap:.4f}  "
            f"L.log(l1/le)={L*math.log(lam1/lam_e):.2f}  "
            f"dX/dp={sl:.1f}  1/nu_eff={nu_eff:.3f}")
        prev = (L, ps, xs)
    # ----- fits -----
    R_inf, inv_nu, x_sig = targets
    Ls = np.array([r['L'] for r in rows], dtype=float)
    R = np.array([r['R'] for r in rows])
    out = {'rows': rows, 'targets': dict(R_inf=R_inf, inv_nu=inv_nu,
                                         x_sigma=x_sig)}
    if len(rows) >= 3:
        a, rss, yh = fit_log(Ls, R, R_inf)
        om, ap, rss_p, yhp = fit_pow(Ls, R, R_inf)
        b, a2, rss_f, yhf = fit_free_log(Ls, R)
        out['R_fit_log'] = {'a': a, 'rss': rss, 'res': list(np.round(R - yh, 4))}
        out['R_fit_pow'] = {'omega': om, 'a': ap, 'rss': rss_p,
                            'res': list(np.round(R - yhp, 4))}
        out['R_fit_freelog'] = {'R_inf_free': b, 'a': a2, 'rss': rss_f}
        log(f"   R(L) -> {R_inf}: marginal 1/lnL fit a={a:.3f} "
            f"rss={rss:.2e} res={np.round(R-yh,4)}")
        log(f"        power fit omega={om:.2f} a={ap:.3f} rss={rss_p:.2e}")
        log(f"        free-log R_inf = {b:.4f}")
    # ----- the v18 convention: R_L(p*) for EVERY size at the common
    # reference p* (one more fit point than the crossing values) -----
    if pstar is not None:
        RL, LL = [], []
        for L in sizes:
            rows = rows_by_L[L]
            ps = [r['p'] for r in rows
                  if r.get('lam1') and r.get('lam_sigma') and r.get('lam_eps')]
            if not ps or not (min(ps) <= pstar <= max(ps)):
                continue
            rat = [math.log(r['lam1'] / r['lam_sigma'])
                   / math.log(r['lam1'] / r['lam_eps']) for r in rows
                   if r.get('lam1') and r.get('lam_sigma') and r.get('lam_eps')]
            RL.append(float(np.interp(pstar, ps, rat)))
            LL.append(L)
        out['R_at_pstar'] = {'pstar': pstar, 'L': LL,
                             'R': [round(v, 4) for v in RL]}
        log(f"   R_L(p*={pstar}) [the v18 convention]: "
            + "  ".join(f"L={L}: {v:.4f}" for L, v in zip(LL, RL)))
        if len(LL) >= 3:
            LLf = np.array(LL, dtype=float)
            RLf = np.array(RL)
            a, rss, yh = fit_log(LLf, RLf, R_inf)
            om, ap, rss_p, yhp = fit_pow(LLf, RLf, R_inf)
            b, a2, rss_f, yhf = fit_free_log(LLf, RLf)
            out['R_pstar_fit_log'] = {'a': a, 'rss': rss,
                                      'res': list(np.round(RLf - yh, 4))}
            out['R_pstar_fit_pow'] = {'omega': om, 'a': ap, 'rss': rss_p}
            out['R_pstar_fit_freelog'] = {'R_inf_free': b, 'a': a2}
            log(f"   R_L(p*) -> {R_inf}: marginal 1/lnL a={a:.3f} "
                f"rss={rss:.2e} res={np.round(RLf - yh, 4)}")
            log(f"        power omega={om:.2f} rss={rss_p:.2e};  "
                f"free-log R_inf={b:.4f}")
            if len(LL) >= 4:
                # two-term marginal form: R = R_inf + a/lnL + b2/ln^2 L
                T = np.column_stack([np.ones_like(LLf), 1.0 / np.log(LLf),
                                     1.0 / np.log(LLf) ** 2])
                c2, *_ = np.linalg.lstsq(T, RLf - R_inf, rcond=None)
                yh2 = R_inf + T @ c2
                out['R_pstar_fit_log2'] = {
                    'a': float(c2[1]), 'b': float(c2[2]),
                    'rss': float(((RLf - yh2) ** 2).sum()),
                    'res': list(np.round(RLf - yh2, 4))}
                log(f"        two-term marginal (a/lnL + b/ln^2L): "
                    f"a={c2[1]:.3f} b={c2[2]:.3f} "
                    f"rss={out['R_pstar_fit_log2']['rss']:.2e} "
                    f"res={np.round(RLf - yh2, 4)}")
    if pstar is not None and len(rows) >= 3:
        # slopes at a common p* (the last crossing / extrapolated pc)
        sls, Ls2, gaps, gL = [], [], [], []
        for L in sizes:
            ps, xs = X_of(rows_by_L[L], L)
            if ps.min() <= pstar <= ps.max():
                sls.append(slope_at(ps, xs, pstar))
                Ls2.append(L)
                lam1 = at_val(rows_by_L[L], 'lam1', pstar)
                lam_s = at_val(rows_by_L[L], 'lam_sigma', pstar)
                gaps.append(math.log(lam1 / lam_s))
                gL.append(L * math.log(lam1 / lam_s))
        if len(Ls2) >= 3:
            Ls2 = np.array(Ls2, dtype=float)
            sls = np.array(sls)
            gaps = np.array(gaps)
            gL = np.array(gL)
            lnS = np.log(sls)
            # ln slope = (1/nu) ln L + c + a/ln L  with 1/nu FIXED
            T = np.column_stack([np.ones_like(Ls2),
                                 np.log(Ls2), 1.0 / np.log(Ls2)])
            # fixed-slope variant: regress lnS - inv_nu*ln L on [1, 1/lnL]
            y2 = lnS - inv_nu * np.log(Ls2)
            Tf = np.column_stack([np.ones_like(Ls2), 1.0 / np.log(Ls2)])
            cf, *_ = np.linalg.lstsq(Tf, y2, rcond=None)
            yh = inv_nu * np.log(Ls2) + Tf @ cf
            out['slope_fit'] = {'inv_nu_fixed': inv_nu,
                                'c': float(cf[0]), 'a_lnL': float(cf[1]),
                                'rss': float(((lnS - yh) ** 2).sum()),
                                'res': list(np.round(lnS - yh, 4))}
            # free exponent variant
            Tg = np.column_stack([np.ones_like(Ls2), np.log(Ls2)])
            cg, *_ = np.linalg.lstsq(Tg, lnS, rcond=None)
            yhg = Tg @ cg
            out['slope_fit_free'] = {'inv_nu_free': float(cg[1]),
                                     'rss': float(((lnS - yhg) ** 2).sum())}
            log(f"   slopes at p*={pstar}: 1/nu fixed {inv_nu}: "
                f"a(1/lnL)={cf[1]:.3f} rss={out['slope_fit']['rss']:.2e} "
                f"res={out['slope_fit']['res']}")
            log(f"        free-exponent 1/nu = {cg[1]:.3f} "
                f"(rss {out['slope_fit_free']['rss']:.2e})")
            # gap * L = 2 pi x_sigma A (1 + a/ln L): linear in 1/ln L
            b, aa, rss_g, yhg2 = fit_free_log(Ls2, gL)
            out['gap_fit'] = {'A_2pix': b, 'a_lnL': aa, 'rss': rss_g,
                              'res': list(np.round(gL - yhg2, 3))}
            log(f"   gap*L (2 pi x_sig A): free-log b={b:.3f} "
                f"a={aa:.3f} rss={rss_g:.2e} res={np.round(gL-yhg2,3)}")
            out['xi_over_L'] = [round(float(1.0 / g), 3) for g in
                                [L * 0 + 1.0 / (L * gaps[i])
                                 for i, L in enumerate(Ls2)]]
    return out


def main():
    # ---------------- n=4 (the marginal chain) ----------------
    r4 = load('v18-n4n5-smc/n4_annealed_scan_L4_v1.json')
    r6 = load('v18-n4n5-smc/n4_annealed_scan_L6_v1.json')
    r8 = load('v18-n4n5-smc/n4_annealed_scan_L8_v1.json')
    r10 = load('v19-n5L6-nofreeze/n4_L10_scan_v2.json')
    # eps top-ups (v18 + this round's v22 top-up): merge lam_eps
    eps_files = ['v18-n4n5-smc/n4_eps_L4_v1.json',
                 'v18-n4n5-smc/n4_eps_L6_v1.json',
                 'v18-n4n5-smc/n4_eps_L8_v1.json',
                 'v18-n4n5-smc/n4_eps_L8_fast_v1.json',
                 'v22-exactZ3-n5L8/v22_n4_eps_topup.json']
    bases = [r4, r6, r8, r8, r8]
    for fn, base in zip(eps_files, bases):
        try:
            for e in load(fn):
                if not isinstance(e, dict) or 'p' not in e:
                    continue
                for r in base:
                    if abs(r['p'] - e['p']) < 1e-9 and not r.get('lam_eps'):
                        if e.get('lam_eps') is not None:
                            r['lam_eps'] = e['lam_eps']
                        elif e.get('triv3'):
                            r['lam_eps'] = e['triv3'][1]
        except FileNotFoundError:
            log(f"   [eps merge] {fn} not found (skipped)")
    rows_by_L = {4: r4, 6: r6, 8: r8, 10: r10}
    n4 = analyse_chain('n=4 (marginal q=4)', [4, 6, 8, 10], rows_by_L,
                       targets=(0.25, 1.5, 0.125), pstar=0.383)
    # ---------------- n=3 (the non-marginal control) ----------------
    n3d = load('v17-annealed-n3/n3_annealed_scan_dense.json')
    by = {}
    for r in n3d:
        by.setdefault(r['L'], []).append(r)
    sizes = sorted(by)
    n3 = analyse_chain('n=3 (control, q=3)', sizes, by,
                       targets=(1.0 / 6.0, 1.2, 2.0 / 15.0), pstar=0.305)
    json.dump({'n4': n4, 'n3': n3},
              open(f'{OUT}/v22_q4_logcorr.json', 'w'), indent=1)
    log(f"written {OUT}/v22_q4_logcorr.json")


if __name__ == '__main__':
    main()
