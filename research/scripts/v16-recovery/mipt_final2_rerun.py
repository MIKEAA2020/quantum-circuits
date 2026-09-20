"""v14 rerun of mipt_final2.py (item 13): identical pipeline with 1/N standard-error floors via mipt_fss2_floorN, incremental JSON, v14 additions (Secs. 8-9). Original mipt_final2.py unchanged.

Everything is bootstrapped over trajectories (disorder samples); no by-eye fits.
Outputs: mipt_results/final2_summary.json, mipt_results/final2_tables.md, figures mipt_results/fig_final_*.{png,pdf}
usage: python3 mipt_final2.py [NB]   (NB = bootstrap resamples, default 200)
"""
import numpy as np, json, os, sys, functools, time
print = functools.partial(print, flush=True)
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mipt_analysis import load
from mipt_fss import means, COL, log_slope_interp
import mipt_fss2_floorN as _mf
local_crossing, fit_collapse, slope_at, collapse_cost = _mf.local_crossing, _mf.fit_collapse, _mf.slope_at, _mf.collapse_cost

NB = int(sys.argv[1]) if len(sys.argv) > 1 else 200
OUT = "mipt_results"; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20260916)
T0 = time.time()

def _save(tag="partial"):
    json.dump(out, open(os.path.join(OUT, "final2_summary_floorN_" + tag + ".json"), "w"), indent=1, default=float)
    print("   [partial save:", tag, "%.0f s" % (time.time() - T0), flush=True)

D = load()
_mf.set_nsamp(D)   # v14 item 13: 1/N standard-error floors
Ls_all = sorted(set(L for L, p in D)); ps_all = sorted(set(p for L, p in D))
grid = {L: sorted(p for (LL, p) in D if LL == L) for L in Ls_all}
ns = {L: len(D[(L, grid[L][0])][0]) for L in Ls_all}
rec = {L: [int(t) for t in D[(L, grid[L][0])][1]] for L in Ls_all}
print("sizes/samples:", ns)
print("record times:", rec)
out = {"samples": ns, "grids": {str(L): grid[L] for L in Ls_all}, "rec_times": {str(L): rec[L] for L in Ls_all}, "nboot": NB}
LN2 = np.log(2.0)

def has_t(L, tf): return int(round(tf * L)) in rec[L]

# ------------------------------------------------------------------ helper crossing estimators
def lin_cross(M, L1, L2, ps):
    ps = [p for p in ps if (L1, p) in M and (L2, p) in M and p <= 0.19]
    x = np.array(ps); d = np.array([M[(L1, p)][0] - M[(L2, p)][0] for p in ps])
    idx = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    if len(idx) == 0: return np.nan
    i = idx[np.argmin(np.abs(d[idx]))]
    return x[i] - d[i] * (x[i + 1] - x[i]) / (d[i + 1] - d[i])

def curve_cross(M, L1, L2, ps, deg=3, lo=0.145, hi=0.175):
    """separate weighted cubic fits of I3(p) for the two sizes over [lo,hi], intersected."""
    ps = [p for p in ps if (L1, p) in M and (L2, p) in M and lo - 1e-9 <= p <= hi + 1e-9]
    x = np.array(ps)
    def fit(L):
        y = np.array([M[(L, p)][0] for p in ps]); e = np.array([max(M[(L, p)][1], 1e-3) for p in ps])
        return np.polyfit(x - 0.16, y, min(deg, len(ps) - 1), w=1 / e)
    c = fit(L1) - fit(L2); r = np.roots(c); r = r[np.isreal(r)].real + 0.16; r = r[(r >= lo) & (r <= hi)]
    return r[np.argmin(np.abs(r - 0.16))] if len(r) else np.nan

from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
def pchip_cross(M, L1, L2, ps, lo=0.14, hi=0.18):
    """monotone (PCHIP) interpolation of each I3(p) curve through all grid points in [lo,hi]; intersection by brentq."""
    pp = [p for p in ps if (L1, p) in M and (L2, p) in M and lo - 1e-9 <= p <= hi + 1e-9]
    f1 = PchipInterpolator(pp, [M[(L1, p)][0] for p in pp]); f2 = PchipInterpolator(pp, [M[(L2, p)][0] for p in pp])
    g = lambda p: f1(p) - f2(p)
    xs = np.linspace(pp[0], pp[-1], 2001); v = g(xs); idx = np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0]
    if len(idx) == 0: return np.nan
    roots = np.array([brentq(g, xs[i], xs[i + 1]) for i in idx])
    return roots[np.argmin(np.abs(roots - 0.16))]

def boot_stat(vals):
    v = np.array(vals, float); v = v[np.isfinite(v)]
    if len(v) < 3: return float("nan"), float("nan")
    return float(np.std(v, ddof=1)), float(1.4826 * np.median(np.abs(v - np.median(v))))

# ------------------------------------------------------------------ 1. crossings
print("\n== 1. I3 crossings p_x(L,2L) ==")
cr = {}
for tf in (4.0, 2.0):
    Ls = [L for L in Ls_all if has_t(L, tf)]
    pairs = [(L, 2 * L) for L in Ls if 2 * L in Ls]
    M = means(D, Ls, ps_all, COL["I3"], tf)
    meth = {"pchip": lambda M, a, b: pchip_cross(M, a, b, ps_all),
            "local_quad": lambda M, a, b: local_crossing(M, a, b, ps_all),
            "cubic_per_curve": lambda M, a, b: curve_cross(M, a, b, ps_all),
            "linear_bracket": lambda M, a, b: lin_cross(M, a, b, ps_all)}
    boots = {(pr, k): [] for pr in pairs for k in meth}
    for b in range(NB):
        Mb = means(D, Ls, ps_all, COL["I3"], tf, rng)
        for pr in pairs:
            for k, f in meth.items(): boots[(pr, k)].append(f(Mb, *pr))
    res = {}
    for pr in pairs:
        row = {}
        for k, f in meth.items():
            v = f(M, *pr); sd, mad = boot_stat(boots[(pr, k)])
            row[k] = dict(value=float(v), se=sd, se_robust=mad)
        # I3 value at the crossing (local quad estimate), interpolated on the L1 curve
        pp = [p for p in ps_all if (pr[0], p) in M]; y = [M[(pr[0], p)][0] for p in pp]
        row["I3_at_crossing_bits"] = float(np.interp(row["pchip"]["value"], pp, y))
        res[f"{pr[0]}-{pr[1]}"] = row
        print(f"t={tf:g}L ({pr[0]},{pr[1]}): pchip {row['pchip']['value']:.4f}±{row['pchip']['se']:.4f} "
              f"| local-quad {row['local_quad']['value']:.4f}±{row['local_quad']['se']:.4f} "
              f"| cubic-per-curve {row['cubic_per_curve']['value']:.4f}±{row['cubic_per_curve']['se']:.4f} "
              f"| linear {row['linear_bracket']['value']:.4f}±{row['linear_bracket']['se']:.4f} | I3(p_x)={row['I3_at_crossing_bits']:+.3f} bits")
    # extrapolations of the pchip ladder
    Lp = np.array([pr[0] for pr in pairs], float)
    px = np.array([res[f"{pr[0]}-{pr[1]}"]["pchip"]["value"] for pr in pairs])
    se = np.array([max(res[f"{pr[0]}-{pr[1]}"]["pchip"]["se"], 2e-4) for pr in pairs])
    ext = {}
    for Lmin, label in ((24, "power_L>=24"), (32, "power_L>=32"), (48, "power_L>=48")):
        sel = Lp >= Lmin
        try:
            f = lambda L, pc, a, w: pc + a * L ** (-w)
            popt, pcov = curve_fit(f, Lp[sel], px[sel], p0=[0.16, -0.05, 1.0], sigma=se[sel], absolute_sigma=True, maxfev=20000)
            ext[label] = dict(pc=float(popt[0]), pc_se=float(np.sqrt(pcov[0, 0])), omega=float(popt[2]), omega_se=float(np.sqrt(pcov[2, 2])))
            print(f"   extrapolation {label}: p_c = {popt[0]:.4f} ± {np.sqrt(pcov[0,0]):.4f}, exponent {popt[2]:.2f} ± {np.sqrt(pcov[2,2]):.2f}")
        except Exception as e:
            ext[label] = dict(error=str(e))
    for Lmin in (48, 64, 96):
        sel = Lp >= Lmin
        if sel.sum() >= 3:
            c, cov = np.polyfit(1 / Lp[sel], px[sel], 1, w=1 / se[sel], cov="unscaled")
            ext[f"linear_1/L_L>={Lmin}"] = dict(pc=float(c[1]), pc_se=float(np.sqrt(cov[1, 1])))
            print(f"   linear in 1/L, L>={Lmin}: p_c = {c[1]:.4f} ± {np.sqrt(cov[1,1]):.4f}")
    sel = Lp >= 96
    w = 1 / se[sel] ** 2; pl = float(np.sum(w * px[sel]) / np.sum(w)); pl_se = float(np.sqrt(1 / np.sum(w))); pl_sc = float(np.std(px[sel], ddof=1)) if sel.sum() > 1 else float("nan")
    ext["plateau_L>=96"] = dict(pc=pl, pc_se=pl_se, scatter=pl_sc, n=int(sel.sum()))
    print(f"   plateau (weighted mean of pchip crossings with L>=96): p_c = {pl:.4f} ± {pl_se:.4f} (scatter {pl_sc:.4f}, n={sel.sum()})")
    cr[f"t={tf:g}L"] = dict(pairs=res, extrapolation=ext)
out["crossings"] = cr
_save("crossings")

# ------------------------------------------------------------------ 2. windowed I3 collapse
print("\n== 2. windowed I3 collapse: I3 = F((p-p_c) L^{1/nu}), deg-4 polynomial, |x|<=xmax ==")
coll = {}
ps_use = [p for p in ps_all if 0.13 <= p <= 0.19]
for tf in (4.0, 2.0):
    Lsz = [L for L in Ls_all if has_t(L, tf)]
    for Lmin in (32, 48, 64, 96):
        for xmax in (0.6, 1.0, 1.5):
            Lset = [L for L in Lsz if L >= Lmin]
            M = means(D, Lset, ps_all, COL["I3"], tf)
            pc, nu, cost, n = fit_collapse(M, Lset, ps_use, xmax=xmax)
            bs = np.array([fit_collapse(means(D, Lset, ps_all, COL["I3"], tf, rng), Lset, ps_use, xmax=xmax)[:2] for b in range(NB)])
            key = f"t={tf:g}L;L>={Lmin};xmax={xmax}"
            coll[key] = dict(pc=float(pc), pc_se=float(bs[:, 0].std(ddof=1)), nu=float(nu), nu_se=float(bs[:, 1].std(ddof=1)),
                             chi2dof=float(cost), npts=int(n), Ls=Lset, Lmax=Lset[-1])
            print(f"{key:28s} L={Lset[0]}..{Lset[-1]}: p_c={pc:.4f}±{bs[:,0].std(ddof=1):.4f}  nu={nu:.3f}±{bs[:,1].std(ddof=1):.3f}  chi2/dof={cost:.2f} ({n} pts)")
out["collapse_I3"] = coll
_save("collapse_I3")

# ------------------------------------------------------------------ 3. slope method
print("\n== 3. slope method: dI3/dp|_{p_c} ~ L^{1/nu} (cubic fit over |p-p_c|<=0.011) ==")
sl = {}
for tf, Lmin in ((4.0, 32), (4.0, 48), (2.0, 32), (2.0, 48), (2.0, 64)):
    Lsz = [L for L in Ls_all if has_t(L, tf) and L >= Lmin]
    M = means(D, Lsz, ps_all, COL["I3"], tf)
    for pc_try in (0.1585, 0.1590, 0.1595, 0.1600, 0.1605):
        Luse = [L for L in Lsz if all((L, p) in M for p in (0.15, 0.155, 0.16, 0.165, 0.17))]
        s = np.array([slope_at(M, L, ps_all, pc_try, half=0.011) for L in Luse]); c = np.polyfit(np.log(Luse), np.log(s), 1)
        bs = []
        for b in range(NB):
            Mb = means(D, Luse, ps_all, COL["I3"], tf, rng); sb = np.array([slope_at(Mb, L, ps_all, pc_try, half=0.011) for L in Luse])
            bs.append(1 / np.polyfit(np.log(Luse), np.log(sb), 1)[0])
        # local exponents from consecutive pairs
        loc = {f"{Luse[i]}-{Luse[i+1]}": float(np.log(Luse[i + 1] / Luse[i]) / np.log(s[i + 1] / s[i])) for i in range(len(Luse) - 1)}
        sl[f"t={tf:g}L;L>={Lmin};pc={pc_try}"] = dict(nu=float(1 / c[0]), nu_se=float(np.std(bs, ddof=1)), Ls=Luse, local_nu=loc)
        print(f"t={tf:g}L L>={Lmin} p_c={pc_try}: nu={1/c[0]:.3f}±{np.std(bs,ddof=1):.3f} (L={Luse[0]}..{Luse[-1]})" + ("; local nu: " + str({k: round(v, 2) for k, v in loc.items() if int(k.split('-')[0]) >= 64}) if Lmin == 48 else ""))
out["slope_method"] = sl

# ------------------------------------------------------------------ 4. Delta S crossings (second observable)
print("\n== 4. Delta S(L) = S_half(2L) - S_half(L): crossings of Delta S(L) with Delta S(2L) ==")
dsr = {}
for tf in (4.0, 2.0):
    Lsz = [L for L in Ls_all if has_t(L, tf)]
    M = means(D, Lsz, ps_all, COL["S_half"], tf)
    def dS(M, L, p):
        return (M[(2 * L, p)][0] - M[(L, p)][0], np.hypot(M[(2 * L, p)][1], M[(L, p)][1])) if ((L, p) in M and (2 * L, p) in M) else None
    def cross(M, L):
        ps = [p for p in ps_all if dS(M, L, p) and dS(M, 2 * L, p) and 0.13 <= p <= 0.19]
        x = np.array(ps); d = np.array([dS(M, L, p)[0] - dS(M, 2 * L, p)[0] for p in ps]); e = np.array([np.hypot(dS(M, L, p)[1], dS(M, 2 * L, p)[1]) for p in ps])
        idx = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
        if len(idx) == 0: return np.nan
        i = idx[np.argmin(np.abs(d[idx]))]; p0 = x[i] - d[i] * (x[i + 1] - x[i]) / (d[i + 1] - d[i])
        sel = np.abs(x - p0) <= 0.0125 + 1e-9
        if sel.sum() < 3: sel = np.argsort(np.abs(x - p0))[:3]
        c = np.polyfit(x[sel], d[sel], 2 if sel.sum() >= 4 else 1, w=1 / e[sel]); r = np.roots(c); r = r[np.isreal(r)].real
        return r[np.argmin(np.abs(r - p0))] if len(r) else np.nan
    trip = [L for L in Lsz if 2 * L in Lsz and 4 * L in Lsz]
    boots = {L: [] for L in trip}
    for b in range(NB):
        Mb = means(D, Lsz, ps_all, COL["S_half"], tf, rng)
        for L in trip: boots[L].append(cross(Mb, L))
    res = {}
    for L in trip:
        v = cross(M, L); sd, mad = boot_stat(boots[L])
        ps = [p for p in ps_all if dS(M, L, p) and 0.13 <= p <= 0.19]; y = [dS(M, L, p)[0] for p in ps]
        val = float(np.interp(v, ps, y)) if np.isfinite(v) else float("nan")
        res[f"{L}-{2*L}-{4*L}"] = dict(px=float(v), se=sd, se_robust=mad, dS_bits=val, alpha_from_dS=val / LN2)
        print(f"t={tf:g}L sizes ({L},{2*L},{4*L}): p_x = {v:.4f} ± {sd:.4f} (robust {mad:.4f}); Delta S(p_x) = {val:.3f} bits -> alpha = {val/LN2:.2f}")
    dsr[f"t={tf:g}L"] = res
out["deltaS_crossings"] = dsr
_save("deltaS_crossings")

# ------------------------------------------------------------------ 5. logarithmic scaling at p_c
print("\n== 5. S_half(L,p_c) = alpha ln L + b (bits; PBC half chain = two cuts) ==")
ref_pc, ref_se = coll["t=2L;L>=48;xmax=1.0"]["pc"], max(coll["t=2L;L>=48;xmax=1.0"]["pc_se"], 0.0004)
print(f"reference p_c = {ref_pc:.4f} ± {ref_se:.4f} (t=2L, L>=48, xmax=1 collapse); p_c uncertainty propagated in the bootstrap")
lg = {}
ps_s = [p for p in ps_all if 0.145 <= p <= 0.175]
for tf in (4.0, 2.0):
    for Lmin in (16, 32, 48, 64):
        Lset = [L for L in Ls_all if has_t(L, tf) and L >= Lmin]
        M = means(D, Lset, ps_s, COL["S_half"], tf)
        Luse = [L for L in Lset if all((L, p) in M for p in (0.15, 0.155, 0.16, 0.165, 0.17))]
        a, b, c2 = log_slope_interp(M, Luse, ps_s, ref_pc)
        bs = [log_slope_interp(means(D, Luse, ps_s, COL["S_half"], tf, rng), Luse, ps_s, rng.normal(ref_pc, ref_se))[0] for _ in range(NB)]
        key = f"t={tf:g}L;L>={Lmin}"
        lg[key] = dict(alpha_bits=float(a), se=float(np.std(bs, ddof=1)), chi2dof=float(c2), Ls=Luse, intercept=float(b),
                       per_cut_bits=float(a / 2), per_cut_nats=float(a * LN2 / 2), c_eff=float(3 * a * LN2))
        print(f"{key:14s} L={Luse[0]}..{Luse[-1]}: alpha = {a:.3f} ± {np.std(bs,ddof=1):.3f} bits/lnL  chi2/dof={c2:.2f}  -> per cut {a/2:.3f} bits = {a*LN2/2:.3f} nats; c_eff=3*alpha*ln2 = {3*a*LN2:.2f}")
    # fixed grid points
    for p0 in (0.1575, 0.16, 0.1625):
        Lset = [L for L in Ls_all if has_t(L, tf) and L >= 32 and (L, p0) in D]
        M = means(D, Lset, [p0], COL["S_half"], tf)
        x = np.log(np.array(Lset, float)); y = np.array([M[(L, p0)][0] for L in Lset]); e = np.array([M[(L, p0)][1] for L in Lset])
        c, cov = np.polyfit(x, y, 1, w=1 / e, cov="unscaled"); chi2 = np.sum(((np.polyval(c, x) - y) / e) ** 2) / (len(x) - 2)
        lg[f"t={tf:g}L;grid p={p0}"] = dict(alpha_bits=float(c[0]), se=float(np.sqrt(cov[0, 0])), chi2dof=float(chi2), Ls=Lset)
        print(f"t={tf:g}L grid p={p0}: alpha = {c[0]:.3f} ± {np.sqrt(cov[0,0]):.3f}  chi2/dof={chi2:.2f}  (L={Lset[0]}..{Lset[-1]})")
out["log_scaling"] = lg
_save("log_scaling")

# chord (Calabrese-Cardy) fits of the block entropies S(l), l = L/8, L/4, 3L/8, L/2 at p=0.16
print("\n== 5b. chord fits S(l) = a ln[(L/pi) sin(pi l/L)] + b at p=0.16 (four block sizes per L) ==")
chord = {}
for tf in (4.0, 2.0):
    for L in [L for L in Ls_all if has_t(L, tf) and L >= 64 and (L, 0.16) in D]:
        data, rc = D[(L, 0.16)]; it = list(rc).index(int(round(tf * L)))
        ls = np.array([L / 8, L / 4, 3 * L / 8, L / 2]); xs = np.log(L / np.pi * np.sin(np.pi * ls / L))
        ys = data[:, it, 0:4].mean(0); es = data[:, it, 0:4].std(0, ddof=1) / np.sqrt(len(data))
        c, cov = np.polyfit(xs, ys, 1, w=1 / es, cov="unscaled")
        chord[f"t={tf:g}L;L={L}"] = dict(a_bits=float(c[0]), se=float(np.sqrt(cov[0, 0])))
        print(f"t={tf:g}L L={L}: a = {c[0]:.3f} ± {np.sqrt(cov[0,0]):.3f} bits")
out["chord_fits_p0.16"] = chord
_save("chord_fits")

# ------------------------------------------------------------------ 6. depth stability t=L, 2L, 4L
print("\n== 6. depth (aspect-ratio) stability at p=0.16 and p=0.1575 ==")
dep = {}
for p0 in (0.1575, 0.16):
    for L in Ls_all:
        if (L, p0) not in D: continue
        data, rc = D[(L, p0)]
        row = {}
        for tf in (0.5, 1.0, 2.0, 4.0):
            t = int(round(tf * L))
            if t in list(rc):
                it = list(rc).index(t); n = len(data)
                row[f"t={tf:g}L"] = dict(S_half=float(data[:, it, 3].mean()), S_se=float(data[:, it, 3].std(ddof=1) / np.sqrt(n)),
                                          I3=float(data[:, it, 4].mean()), I3_se=float(data[:, it, 4].std(ddof=1) / np.sqrt(n)))
        dep[f"p={p0};L={L}"] = row
        print(f"p={p0} L={L:3d}: " + "  ".join(f"{k}: S={v['S_half']:.3f}({v['S_se']:.3f}) I3={v['I3']:+.3f}({v['I3_se']:.3f})" for k, v in row.items()))
out["depth_stability"] = dep
_save("depth_stability")

# ------------------------------------------------------------------ 7. figures
print("\n== 7. figures ==")
tf = 2.0
Lsz = [L for L in Ls_all if has_t(L, tf)]
M = means(D, Lsz, ps_all, COL["I3"], tf)
best = coll["t=2L;L>=48;xmax=1.0"]
cmap = plt.get_cmap("viridis")
fig, ax = plt.subplots(2, 2, figsize=(11, 8.2))
# (a) I3 vs p
a = ax[0, 0]
for i, L in enumerate(Lsz):
    pp = [p for p in ps_all if (L, p) in M and 0.12 <= p <= 0.22]
    a.errorbar(pp, [M[(L, p)][0] for p in pp], yerr=[M[(L, p)][1] for p in pp], fmt="o-", ms=3, lw=1, color=cmap(i / (len(Lsz) - 1)), label=f"L={L}")
a.axvline(best["pc"], ls="--", c="k", lw=0.8); a.set_ylim(-2.6, 0.1); a.set_xlabel("p"); a.set_ylabel(r"$I_3$ (bits)")
a.set_title(r"(a) tripartite information, $t=2L$"); a.legend(fontsize=6.5, ncol=2, loc="upper left")
# inset: crossing ladder
ins = a.inset_axes([0.50, 0.10, 0.47, 0.44])
for tf2, mk, col in ((4.0, "s", "C3"), (2.0, "o", "C0")):
    prs = cr[f"t={tf2:g}L"]["pairs"]; Lp = [int(k.split("-")[0]) for k in prs]
    ins.errorbar([1 / L for L in Lp], [prs[k]["pchip"]["value"] for k in prs], yerr=[prs[k]["pchip"]["se"] for k in prs], fmt=mk, ms=3, color=col, label=f"t={tf2:g}L")
ins.axhline(best["pc"], ls="--", c="k", lw=0.8); ins.set_xlabel("1/L", fontsize=7); ins.set_ylabel(r"$p_\times(L,2L)$", fontsize=7); ins.tick_params(labelsize=6); ins.legend(fontsize=6)
# (b) collapse
a = ax[0, 1]
Lset = best["Ls"]
for i, L in enumerate(Lset):
    pp = [p for p in ps_use if (L, p) in M]
    x = (np.array(pp) - best["pc"]) * L ** (1 / best["nu"]); sel = np.abs(x) <= 1.6
    a.errorbar(x[sel], np.array([M[(L, p)][0] for p in pp])[sel], yerr=np.array([M[(L, p)][1] for p in pp])[sel], fmt="o", ms=3.5, color=cmap(i / max(len(Lset) - 1, 1)), label=f"L={L}")
a.set_xlabel(r"$(p-p_c)\,L^{1/\nu}$"); a.set_ylabel(r"$I_3$ (bits)"); a.legend(fontsize=7, ncol=2)
a.set_title(rf"(b) collapse: $p_c={best['pc']:.4f}$, $\nu={best['nu']:.2f}$ ($L\geq{Lset[0]}$, $t=2L$)")
# (c) S_half vs ln L at p_c (interpolated) and at p=0.16
a = ax[1, 0]
for tf2, mk, col in ((2.0, "o", "C0"), (4.0, "s", "C3")):
    Lset2 = [L for L in Ls_all if has_t(L, tf2) and L >= 16]
    MS = means(D, Lset2, ps_s, COL["S_half"], tf2)
    Luse = [L for L in Lset2 if all((L, p) in MS for p in (0.15, 0.155, 0.16, 0.165, 0.17))]
    y = []; e = []
    for L in Luse:
        pp = [p for p in ps_s if (L, p) in MS]
        y.append(CubicSpline(pp, [MS[(L, p)][0] for p in pp])(ref_pc)); e.append(CubicSpline(pp, [MS[(L, p)][1] for p in pp])(ref_pc))
    a.errorbar(np.log(Luse), y, yerr=e, fmt=mk, color=col, ms=4, label=rf"$t={tf2:g}L$, $p=p_c$")
    k = f"t={tf2:g}L;L>=32"; a.plot(np.log(Luse), lg[k]["alpha_bits"] * np.log(Luse) + lg[k]["intercept"], "-", color=col, lw=1, label=rf"$\alpha={lg[k]['alpha_bits']:.2f}\pm{lg[k]['se']:.2f}$ ($L\geq32$)")
a.set_xlabel(r"$\ln L$"); a.set_ylabel(r"$S_{L/2}$ (bits)"); a.set_title(r"(c) half-chain entropy at $p_c$"); a.legend(fontsize=8)
# (d) Delta S ladder
a = ax[1, 1]
MS = means(D, Lsz, ps_all, COL["S_half"], 2.0)
Lh = [L for L in Lsz if 2 * L in Lsz]
for i, L in enumerate(Lh):
    pp = [p for p in ps_all if (L, p) in MS and (2 * L, p) in MS and 0.13 <= p <= 0.19]
    a.errorbar(pp, [MS[(2 * L, p)][0] - MS[(L, p)][0] for p in pp], yerr=[np.hypot(MS[(2 * L, p)][1], MS[(L, p)][1]) for p in pp], fmt="o-", ms=3, lw=1, color=cmap(i / (len(Lh) - 1)), label=f"L={L}")
a.axvline(best["pc"], ls="--", c="k", lw=0.8); a.axhline(lg["t=2L;L>=32"]["alpha_bits"] * LN2, ls=":", c="k", lw=0.8)
a.set_xlabel("p"); a.set_ylabel(r"$\Delta S = S_{L}(2L)-S_{L/2}(L)$ (bits)"); a.set_title(r"(d) entropy increment under $L\to2L$, $t=2L$"); a.legend(fontsize=7, ncol=2); a.set_ylim(-0.2, 4)
plt.tight_layout()
for ext in ("png", "pdf"): plt.savefig(os.path.join(OUT, f"fig_final_fss_floorN.{ext}"), dpi=150)
plt.close()
print("saved", os.path.join(OUT, "fig_final_fss_floorN.{png,pdf}"))


# ------------------------------------------------------------------ 8. v14: alpha at adopted p_c, s1 test, chi2 p-values, floor audit
print("\n== 8. v14 additions: alpha at adopted p_c=0.1597, s1*L^-y AIC test, chi2 p-values, floor audit ==")
from scipy import stats as _stats
PC14 = 0.1597
v14 = {}
ps_s8 = [p for p in ps_all if 0.145 <= p <= 0.175]
arows = {}
for tf in (4.0, 2.0):
    for Lmin in (16, 32, 48, 64):
        Lset = [L for L in Ls_all if has_t(L, tf) and L >= Lmin]
        Luse = [L for L in Lset if all((L, p) in D for p in (0.15, 0.155, 0.16, 0.165, 0.17))]
        M8 = means(D, Luse, ps_s8, COL["S_half"], tf)
        a8, b8, c8 = log_slope_interp(M8, Luse, ps_s8, PC14)
        bs = [log_slope_interp(means(D, Luse, ps_s8, COL["S_half"], tf, rng), Luse, ps_s8, rng.normal(PC14, 0.0004))[0] for _ in range(NB)]
        arows["t=%gL;L>=%d" % (tf, Lmin)] = dict(alpha=float(a8), se=float(np.std(bs, ddof=1)), chi2dof=float(c8), Ls=Luse)
        print("  alpha at p_c=0.1597, t=%gL, L>=%d: %.4f +/- %.4f  chi2/dof=%.2f" % (tf, Lmin, a8, np.std(bs, ddof=1), c8))
v14["alpha_at_0.1597"] = arows
s1 = {}
for tf in (4.0, 2.0):
    for Lmin in (32, 64):
        Lset = [L for L in Ls_all if has_t(L, tf) and L >= Lmin]
        Luse = [L for L in Lset if all((L, p) in D for p in (0.15, 0.155, 0.16, 0.165, 0.17))]
        M8 = means(D, Luse, ps_s8, COL["S_half"], tf)
        xv = np.log(np.array(Luse, float))
        y8 = np.array([CubicSpline([p for p in ps_s8 if (L, p) in M8], [M8[(L, p)][0] for p in ps_s8 if (L, p) in M8])(PC14) for L in Luse])
        e8 = np.array([CubicSpline([p for p in ps_s8 if (L, p) in M8], [M8[(L, p)][1] for p in ps_s8 if (L, p) in M8])(PC14) for L in Luse])
        W8 = 1.0 / e8
        V0 = np.vstack([xv, np.ones_like(xv)]).T
        c0, *_ = np.linalg.lstsq(V0 * W8[:, None], y8 * W8, rcond=None); r0 = (V0 @ c0 - y8) * W8
        ch0 = float((r0 * r0).sum())
        for ylab, inv in (("0.5", 0.5), ("1", 1.0), ("2", 2.0)):
            V1 = np.vstack([xv, np.ones_like(xv), np.array(Luse, float) ** -inv]).T
            c1, *_ = np.linalg.lstsq(V1 * W8[:, None], y8 * W8, rcond=None); r1 = (V1 @ c1 - y8) * W8
            ch1 = float((r1 * r1).sum())
            dAIC = 2.0 * (V1.shape[1] - V0.shape[1]) - 2.0 * (ch0 - ch1)
            s1["t=%gL;L>=%d;y=%s" % (tf, Lmin, ylab)] = dict(dAIC=float(dAIC), d_alpha=float(c1[0] - c0[0]))
            print("  s1 test t=%gL L>=%d y=%s: dAIC=%+.2f  d_alpha=%+.4f" % (tf, Lmin, ylab, dAIC, c1[0] - c0[0]))
v14["s1_test"] = s1
pv = {}
for key, row in coll.items():
    dof = int(row["npts"]) - 5
    ch2 = row["chi2dof"] * dof
    pv[key] = float(_stats.chi2.sf(ch2, dof))
v14["collapse_chi2_pvalues"] = pv
minpv64 = min(v for k, v in pv.items() if "L>=64" in k)
print("  chi2 p-values of windowed collapses: min over L>=64 windows = %.3f" % minpv64)
v14["min_chi2_p_L64"] = minpv64
faudit = []
for key, row in coll.items():
    pcw, nuw = row["pc"], row["nu"]
    Lmin = int(key.split("L>=")[1].split(";")[0]); xmax = float(key.split("xmax=")[1]); tfw = float(key.split("t=")[1].split("L")[0])
    worst = None
    for L in Ls_all:
        if L < Lmin or not has_t(L, tfw): continue
        for p in ps_use:
            if (L, p) not in D: continue
            xw = (p - pcw) * L ** (1.0 / nuw)
            if abs(xw) > xmax: continue
            data, recw = D[(L, p)]; tw = int(round(tfw * L)); iit = list(recw).index(tw)
            sew = float(data[:, iit, COL["I3"]].std(ddof=1) / np.sqrt(len(data)))
            Nw = len(data); flw = 1.0 / Nw
            if worst is None or sew < worst[0]:
                worst = (sew, L, p, Nw, flw)
    faudit.append(dict(window=key, min_se=worst[0], at="L=%d,p=%g" % (worst[1], worst[2]), N=worst[3], floor_1N=worst[4],
                       binds_old_1em6=bool(worst[0] < 1e-6), binds_new_1N=bool(worst[0] < worst[4])))
    print("  floor audit %s: min se in window = %.2e (L=%d, p=%g), 1/N = %.2e -> binds old 1e-6: %s, binds new 1/N: %s"
          % (key, worst[0], worst[1], worst[2], worst[4], worst[0] < 1e-6, worst[0] < worst[4]))
v14["floor_audit"] = faudit
out["v14"] = v14
_save("v14")

# ------------------------------------------------------------------ 9. comparison with the v13 run
try:
    oldj = json.load(open(os.path.join(OUT, "final2_summary.json")))
    cmp9 = {}
    for key, row in coll.items():
        o = oldj["collapse_I3"][key]
        cmp9[key] = dict(dpc=row["pc"] - o["pc"], dnu=row["nu"] - o["nu"], dchi2=row["chi2dof"] - o["chi2dof"])
    out["v14_comparison"] = dict(max_abs_dpc=max(abs(v["dpc"]) for v in cmp9.values()),
                                 max_abs_dnu=max(abs(v["dnu"]) for v in cmp9.values()),
                                 max_abs_dchi2=max(abs(v["dchi2"]) for v in cmp9.values()),
                                 note="0 => windowed numbers unchanged by the 1/N floor")
    print("  comparison vs final2_summary.json: max |dpc| = %.3e, max |dnu| = %.3e, max |dchi2| = %.3e"
          % (out["v14_comparison"]["max_abs_dpc"], out["v14_comparison"]["max_abs_dnu"], out["v14_comparison"]["max_abs_dchi2"]))
except Exception as e:
    out["v14_comparison"] = dict(error=str(e))
    print("  comparison failed:", e)
_save("v14_comparison")

json.dump(out, open(os.path.join(OUT, "final2_summary_floorN.json"), "w"), indent=1, default=float)
print(f"saved {OUT}/final2_summary_floorN.json  ({time.time()-T0:.0f} s)")
