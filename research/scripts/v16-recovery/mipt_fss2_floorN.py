"""Definitive FSS analysis (v2; v14 item 13: 1/N standard-error floors; new version file, mipt_fss2.py unchanged): local crossings + extrapolation, slope method for nu, windowed collapse,
S_half logarithm at p_c, figures.  All uncertainties = bootstrap over trajectories (disorder samples).
usage: python mipt_fss2.py [nboot] [tfac]
"""
import numpy as np, json, os, sys, functools
print = functools.partial(print, flush=True)
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import CubicSpline
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mipt_analysis import load
from mipt_fss import means, COL, log_slope, log_slope_interp, fit_s_collapse

# v14 item 13 (audit3): standard-error floor of 1/N_traj per (L,p) instead of the legacy
# 1e-4/1e-6 absolute floors.  set_nsamp(D) fills NSAMP; without it the legacy floor is retained.
NSAMP = {}

def set_nsamp(D):
    NSAMP.clear()
    for (L, p), (data, rec) in D.items():
        NSAMP[(L, p)] = 1.0 / len(data)

def _floor(L, p):
    return NSAMP.get((L, p), 1e-4)

OUT = "mipt_results"; os.makedirs(OUT, exist_ok=True)
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 200
TF = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
rng = np.random.default_rng(7)

def local_crossing(M, L1, L2, ps, half=0.0125):
    ps = [p for p in ps if (L1, p) in M and (L2, p) in M and p <= 0.19]
    x = np.array(ps); d = np.array([M[(L1, p)][0] - M[(L2, p)][0] for p in ps])
    e = np.array([max(np.hypot(M[(L1, p)][1], M[(L2, p)][1]), max(_floor(L1, p), _floor(L2, p))) for p in ps])
    # sign change of d (small L is more negative at small p -> d<0 at small p, d>0 at large p)
    idx = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    if len(idx) == 0: return np.nan
    i = idx[np.argmin(np.abs(d[idx]))]
    p0 = x[i] - d[i] * (x[i + 1] - x[i]) / (d[i + 1] - d[i])
    sel = np.abs(x - p0) <= half + 1e-9
    if sel.sum() < 3: sel = np.argsort(np.abs(x - p0))[:3]
    c = np.polyfit(x[sel], d[sel], 2 if sel.sum() >= 4 else 1, w=1 / e[sel])
    r = np.roots(c); r = r[np.isreal(r)].real
    if len(r) == 0: return np.nan
    return r[np.argmin(np.abs(r - p0))]

def slope_at(M, L, ps, pc, half=0.02):
    pp = np.array([p for p in ps if (L, p) in M and abs(p - pc) <= half + 1e-9])
    y = np.array([M[(L, p)][0] for p in pp]); e = np.array([max(M[(L, p)][1], _floor(L, p)) for p in pp])
    c = np.polyfit(pp - pc, y, 3, w=1 / e)
    return c[-2]   # derivative at pc

def collapse_cost(M, Ls, ps, pc, nuinv, deg, xmax):
    xs, ys, ws = [], [], []
    for L in Ls:
        for p in ps:
            if (L, p) not in M: continue
            x = (p - pc) * L ** nuinv
            if abs(x) > xmax: continue
            m, se = M[(L, p)]; xs.append(x); ys.append(m); ws.append(1 / max(se, _floor(L, p)) ** 2)
    xs, ys, ws = map(np.array, (xs, ys, ws))
    if len(xs) < deg + 4: return np.inf, 0
    V = np.vander(xs, deg + 1); W = np.sqrt(ws)
    coef, *_ = np.linalg.lstsq(V * W[:, None], ys * W, rcond=None)
    r = (V @ coef - ys) * W
    return np.sum(r * r) / (len(xs) - deg - 1), len(xs)

def fit_collapse(M, Ls, ps, deg=4, xmax=1.0, pc0=0.16, nuinv0=0.77):
    f = lambda v: collapse_cost(M, Ls, ps, v[0], v[1], deg, xmax)[0]
    best = None
    for pc, ni in ((pc0, nuinv0), (pc0 - 0.004, nuinv0 + 0.12), (pc0 + 0.004, nuinv0 - 0.12)):
        r = minimize(f, [pc, ni], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-7, maxiter=500))
        if best is None or r.fun < best.fun: best = r
    n = collapse_cost(M, Ls, ps, best.x[0], best.x[1], deg, xmax)[1]
    return best.x[0], 1 / best.x[1], best.fun, n

if __name__ == "__main__":
    D = load()
    set_nsamp(D)
    D = {k: v for k, v in D.items() if k[0] <= 256}            # L=384 (partial grid) is analysed separately
    Ls_all = sorted(set(L for L, p in D)); ps_all = sorted(set(p for L, p in D))
    nsamp = {L: len(D[(L, 0.16)][0]) for L in Ls_all}
    print("sizes", Ls_all, "samples", nsamp, "t =", TF, "L")
    res = dict(sizes=Ls_all, samples=nsamp, p_grid=ps_all, tfac=TF, nboot=NB)
    ps_w = [p for p in ps_all if 0.12 <= p <= 0.22]
    M_I3 = means(D, Ls_all, ps_w, COL["I3"], TF); M_S = means(D, Ls_all, ps_w, COL["S_half"], TF)
    BOOT_I3 = [means(D, Ls_all, ps_w, COL["I3"], TF, rng) for b in range(NB)]
    BOOT_S = [means(D, Ls_all, ps_w, COL["S_half"], TF, rng) for b in range(NB // 2)]

    # ---------- 1. local crossings ----------
    pairs = [(L, 2 * L) for L in Ls_all if 2 * L in Ls_all]
    cross = {}
    print("\n== 1. I3 crossings p_x(L,2L) (local quadratic fit, |p-p_x|<=0.0125) ==")
    for a, b in pairs:
        v = local_crossing(M_I3, a, b, ps_w); bs = np.array([local_crossing(Mb, a, b, ps_w) for Mb in BOOT_I3])
        cross[f"{a}-{b}"] = (float(v), float(np.nanstd(bs, ddof=1)), int(np.isnan(bs).sum()))
        print(f"  ({a:3d},{b:3d}): p_x = {v:.4f} ± {np.nanstd(bs, ddof=1):.4f}")
    res["crossings"] = cross
    # extrapolation p_x(L) = pc + A L^-b (pairs with L>=24) and linear in 1/L (L>=48)
    def extrap(cr, Lmin, mode):
        Lx = np.array([a for a, b in pairs if a >= Lmin], float); y = np.array([cr[f"{a}-{b}"][0] for a, b in pairs if a >= Lmin])
        if mode == "power":
            f = lambda L, pc, A, bb: pc + A * L ** (-bb)
            try:
                popt, _ = curve_fit(f, Lx, y, p0=[0.16, -0.1, 1.0], maxfev=20000); return popt[0], popt[2]
            except Exception: return np.nan, np.nan
        else:
            c = np.polyfit(1 / Lx, y, 1); return c[1], np.nan
    ext = {}
    for Lmin, mode in ((16, "power"), (24, "power"), (48, "linear"), (64, "linear")):
        v, bexp = extrap(cross, Lmin, mode)
        bs = []
        for Mb in BOOT_I3:
            crb = {f"{a}-{b}": (local_crossing(Mb, a, b, ps_w),) for a, b in pairs}
            bs.append(extrap(crb, Lmin, mode)[0])
        ext[f"{mode};Lmin={Lmin}"] = (float(v), float(np.nanstd(bs, ddof=1)), float(bexp))
        print(f"  extrapolation ({mode}, L>={Lmin}): p_c = {v:.4f} ± {np.nanstd(bs, ddof=1):.4f}" + (f"  (exponent b={bexp:.2f})" if mode == "power" else ""))
    res["crossing_extrapolation"] = ext

    # ---------- 2. slope method: dI3/dp|pc ~ L^{1/nu} ----------
    print("\n== 2. slope method: d I3/dp at p_c ∝ L^{1/nu} ==")
    slopes = {}
    for pc_try in (0.158, 0.1595, 0.161):
        for Lmin in (16, 32, 48):
            Ls = [L for L in Ls_all if L >= Lmin and L <= 256]
            s = np.array([slope_at(M_I3, L, ps_w, pc_try) for L in Ls])
            c = np.polyfit(np.log(Ls), np.log(s), 1)
            bs = []
            for Mb in BOOT_I3:
                sb = np.array([slope_at(Mb, L, ps_w, pc_try) for L in Ls]); bs.append(1 / np.polyfit(np.log(Ls), np.log(sb), 1)[0])
            slopes[f"pc={pc_try};Lmin={Lmin}"] = (float(1 / c[0]), float(np.std(bs, ddof=1)))
            print(f"  p_c={pc_try:.4f} L>={Lmin:3d}: nu = {1/c[0]:.3f} ± {np.std(bs, ddof=1):.3f}   slopes: " + " ".join(f"{v:.2f}" for v in s))
    res["slope_method"] = slopes

    # ---------- 3. windowed collapse ----------
    print("\n== 3. I3 collapse with |x| = |p-p_c| L^{1/nu} <= x_max (deg-4 polynomial scaling function) ==")
    coll = {}
    for xmax in (0.6, 1.0, 1.5):
        for Lmin in (16, 32, 48, 64):
            Ls = [L for L in Ls_all if L >= Lmin and L <= 256]
            pc, nu, cost, n = fit_collapse(M_I3, Ls, ps_w, xmax=xmax)
            bs = np.array([fit_collapse(Mb, Ls, ps_w, xmax=xmax)[:2] for Mb in BOOT_I3[:NB // 2]])
            coll[f"xmax={xmax};Lmin={Lmin}"] = dict(pc=float(pc), pc_se=float(bs[:, 0].std(ddof=1)), nu=float(nu), nu_se=float(bs[:, 1].std(ddof=1)), chi2dof=float(cost), npts=int(n))
            print(f"  xmax={xmax} L>={Lmin:3d}: p_c={pc:.4f}±{bs[:,0].std(ddof=1):.4f}  nu={nu:.3f}±{bs[:,1].std(ddof=1):.3f}  chi2/dof={cost:.2f} ({n} pts)")
    res["collapse_I3"] = coll

    # ---------- 4. S_half collapse ----------
    print("\n== 4. S_half collapse (S(p,L)-S(p_c,L) = G(x), window [0.13,0.19]) ==")
    scoll = {}
    ps_s = [p for p in ps_all if 0.13 <= p <= 0.19]
    for Lmin in (16, 32, 48):
        Ls = [L for L in Ls_all if L >= Lmin and L <= 256]
        pc, nu, cost = fit_s_collapse(M_S, Ls, ps_s)
        bs = np.array([fit_s_collapse(Mb, Ls, ps_s)[:2] for Mb in BOOT_S])
        scoll[f"Lmin={Lmin}"] = dict(pc=float(pc), pc_se=float(bs[:, 0].std(ddof=1)), nu=float(nu), nu_se=float(bs[:, 1].std(ddof=1)), chi2dof=float(cost))
        print(f"  L>={Lmin:3d}: p_c={pc:.4f}±{bs[:,0].std(ddof=1):.4f}  nu={nu:.3f}±{bs[:,1].std(ddof=1):.3f}  chi2/dof={cost:.2f}")
    res["collapse_S_half"] = scoll

    # ---------- 5. logarithmic entanglement at p_c ----------
    print("\n== 5. S_half = alpha ln L + b (bits, two cuts) ==")
    logs = {}
    pc_ref, pc_ref_se = coll["xmax=1.0;Lmin=32"]["pc"], max(coll["xmax=1.0;Lmin=32"]["pc_se"], 0.0004)
    for Lmin in (16, 24, 32, 48, 64):
        Ls = [L for L in Ls_all if L >= Lmin]
        a, b, c2 = log_slope_interp(M_S, Ls, ps_s, pc_ref)
        bs = [log_slope_interp(Mb, Ls, ps_s, rng.normal(pc_ref, pc_ref_se))[0] for Mb in BOOT_S]
        logs[f"pc_interp;Lmin={Lmin}"] = dict(pc=float(pc_ref), pc_se=float(pc_ref_se), alpha=float(a), alpha_se=float(np.std(bs, ddof=1)), chi2dof=float(c2), Ls=Ls)
        print(f"  p=p_c={pc_ref:.4f}±{pc_ref_se:.4f}, L>={Lmin:3d}: alpha = {a:.3f} ± {np.std(bs, ddof=1):.3f} bits/lnL   chi2/dof={c2:.2f}")
    for p in (0.155, 0.16, 0.165):
        for Lmin in (16, 32):
            Ls = [L for L in Ls_all if L >= Lmin]
            a, b, ea, c2 = log_slope(M_S, Ls, p)
            logs[f"p={p};Lmin={Lmin}"] = dict(alpha=float(a), alpha_se=float(ea), chi2dof=float(c2))
            print(f"  p={p:.3f} grid, L>={Lmin:3d}: alpha = {a:.3f} ± {ea:.3f}   chi2/dof={c2:.2f}")
    res["log_fits"] = logs

    # ---------- 6. annealed vs quenched: p_c^(2) and the area-law check at p=0.2338 ----------
    res["annealed_point"] = dict(pc2_exact=0.233810, note="exact anisotropic triangular Ising point of the n=2 annealed model (Prop. 4)")
    print("\n== 6. quenched observables near the annealed point p_c^(2)=0.2338 (p=0.22 grid point) ==")
    for L in Ls_all:
        if (L, 0.22) in M_S: print(f"  L={L:3d}: S_half={M_S[(L,0.22)][0]:.3f}±{M_S[(L,0.22)][1]:.3f}  I3={M_I3[(L,0.22)][0]:.4f}")

    json.dump(res, open(os.path.join(OUT, f"fss2_summary_t{TF:g}L.json"), "w"), indent=1, default=float)

    # ---------- figures ----------
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    cols = plt.cm.viridis(np.linspace(0, 0.95, len(Ls_all)))
    for c, L in zip(cols, Ls_all):
        pp = [p for p in ps_w if (L, p) in M_I3]
        ax[0].errorbar(pp, [M_I3[(L, p)][0] for p in pp], [M_I3[(L, p)][1] for p in pp], fmt="o-", ms=3, color=c, label=f"L={L}")
    ax[0].set_xlabel("p"); ax[0].set_ylabel("$I_3$ (bits)"); ax[0].set_ylim(-2.5, 0.1); ax[0].axvline(pc_ref, color="k", ls="--", lw=0.8); ax[0].legend(fontsize=7, ncol=2)
    ax[0].set_title(f"Clifford brickwork, t={TF:g}L, tripartite information")
    pcx, nux = coll["xmax=1.0;Lmin=32"]["pc"], coll["xmax=1.0;Lmin=32"]["nu"]
    for c, L in zip(cols, Ls_all):
        if L < 32: continue
        pp = [p for p in ps_w if (L, p) in M_I3]
        ax[1].errorbar([(p - pcx) * L ** (1 / nux) for p in pp], [M_I3[(L, p)][0] for p in pp], [M_I3[(L, p)][1] for p in pp], fmt="o", ms=3, color=c, label=f"L={L}")
    ax[1].set_xlim(-1.6, 1.6); ax[1].set_ylim(-2.2, 0.1); ax[1].set_xlabel(r"$(p-p_c)\,L^{1/\nu}$"); ax[1].set_ylabel("$I_3$ (bits)")
    ax[1].set_title(f"collapse: $p_c$={pcx:.4f}, $\\nu$={nux:.2f} (L≥32)"); ax[1].legend(fontsize=7)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, f"fig_I3_crossing_collapse_t{TF:g}L.png"), dpi=140); plt.close()

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for p, c in zip((0.15, 0.155, 0.16, 0.165, 0.17), plt.cm.coolwarm(np.linspace(0, 1, 5))):
        Ls = [L for L in Ls_all if (L, p) in M_S]
        ax[0].errorbar(Ls, [M_S[(L, p)][0] for L in Ls], [M_S[(L, p)][1] for L in Ls], fmt="o-", ms=3, color=c, label=f"p={p}")
    Ls = Ls_all; yint = [CubicSpline([p for p in ps_s if (L, p) in M_S], [M_S[(L, p)][0] for p in ps_s if (L, p) in M_S])(pc_ref) for L in Ls]
    a = logs["pc_interp;Lmin=32"]["alpha"]; b = np.mean([y - a * np.log(L) for y, L in zip(yint, Ls) if L >= 32])
    ax[0].plot(Ls, yint, "k*", ms=7, label=f"p=p_c={pc_ref:.4f} (interp.)"); ax[0].plot(Ls, a * np.log(Ls) + b, "k--", lw=0.8, label=f"{a:.2f} ln L + const")
    ax[0].set_xscale("log"); ax[0].set_xlabel("L"); ax[0].set_ylabel("$S_{L/2}$ (bits, two cuts)"); ax[0].legend(fontsize=7); ax[0].set_title("half-chain entropy vs ln L")
    Lx = [a_ for a_, b_ in pairs]; ax[1].errorbar(Lx, [cross[f"{a_}-{b_}"][0] for a_, b_ in pairs], [cross[f"{a_}-{b_}"][1] for a_, b_ in pairs], fmt="s", color="C3", label="$p_\\times(L,2L)$")
    ax[1].axhline(pc_ref, color="k", ls="--", lw=0.8, label=f"collapse $p_c$={pc_ref:.4f}"); ax[1].set_xscale("log"); ax[1].set_xlabel("L (smaller size of the pair)"); ax[1].set_ylabel("crossing point"); ax[1].legend(fontsize=8); ax[1].set_title("crossing drift")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, f"fig_Shalf_log_crossings_t{TF:g}L.png"), dpi=140); plt.close()
    print("figures written")
