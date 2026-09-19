"""
mipt_purif_analysis.py -- analysis of the deposited Gullans-Huse
reference-qubit (purification) locator on the deposited dataset
(the N2 run of the deposited workspace, reproduced and verified).

Protocol: the L-qubit system starts completely mixed, purified by L reference
qubits; the same circuit and measurements act on the system only; S_ref(t) at
t = tau*L for tau in {0.25, 0.5, 1, 2, 4}; independent seeds (disjoint from
the I3 dataset).  Deposition: 135,000 trajectories, 270 files.

Reproduces (deposited purif_summary.json / the v14 N2 paragraph):
  tau = 1 collapse (sextic F, L >= 64): p_c = 0.16009, nu = 1.2486,
      chi2/dof = 18.3/18;
  tau = 0.5: p_c = 0.16039, nu = 1.251, chi2/dof = 15.5/18;
  tau = 2: 0.16027/1.310, 82.8/18 (saturated tail -- not used);
  frozen-nu Delta-chi2 (tau = 1, L >= 64): 544 / 16.9 / 0.5 / 6.6 / 45.8 / 138.6
      for nu = 1 / 1.2 / 1.24 / 1.28 / 4/3 / 1.4;
  bootstrap (tau = 1, L >= 64, 100 resamples): p_c = 0.16011(9), nu = 1.250(14);
  pair crossings (L >= 64): 0.1606 - 0.1628.
Verdict: p_c^purif = 0.1601 - 0.1604, nu^purif = 1.25(2).
"""
import json, os, sys
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mipt_purif_data as D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)
LOGF = open(os.path.join(LOG, "mipt_purif_analysis.log"), "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOGF.write(s + "\n"); LOGF.flush()

def slice_for(tau):
    vn = f"TAU_{str(tau).replace('.', '_')}"
    return getattr(D, f"DATA_{vn}"), getattr(D, f"SIZES_{vn}")

def means(tau):
    """M[(L, p)] = (mean, se) with the 1/N standard-error floor (item 13)."""
    tab, sizes = slice_for(tau)
    M = {}
    for ip, row in enumerate(tab):
        p = D.P_GRID[ip]
        for il, (mn, se) in enumerate(row):
            L = sizes[il]
            floor = 1.0 / D.NTRAJ[L]
            M[(L, p)] = (mn, max(se, floor))
    return M, sizes

# ------------------------------------------------------------------ crossings
def crossings(M, sizes, L1, L2):
    ps = sorted({p for (L, p) in M if L in (L1, L2)})
    x, y, w = [], [], []
    for p in ps:
        if (L1, p) in M and (L2, p) in M:
            x.append(p)
            y.append(M[(L1, p)][0] - M[(L2, p)][0])
            w.append(1.0 / np.hypot(M[(L1, p)][1], M[(L2, p)][1]))
    x, y, w = map(np.array, (x, y, w))
    # monotone piecewise-cubic (PCHIP) crossing of the difference curve
    from scipy.interpolate import PchipInterpolator
    f = PchipInterpolator(x, y)
    # find sign changes
    xg = np.linspace(x[0], x[-1], 4001)
    yg = f(xg)
    out = []
    for i in range(len(xg) - 1):
        if yg[i] == 0 or yg[i] * yg[i + 1] < 0:
            lo, hi = xg[i], xg[i + 1]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if f(lo) * f(mid) <= 0: hi = mid
                else: lo = mid
            out.append(0.5 * (lo + hi))
    return out

# ------------------------------------------------------------------ collapse
def design(x, deg):
    return np.vander(x, deg + 1, increasing=True)

def fit_collapse(M, sizes, pc0=0.160, nu0=1.25, deg=6, Lmin=64, xmax=None,
                 nu_fixed=None, pc_fixed=None):
    ps = sorted({p for (L, p) in M})
    xs, ys, ws, Ls = [], [], [], []
    for L in sorted(sizes):
        if L < Lmin: continue
        for p in ps:
            if (L, p) not in M: continue
            xs.append((p - pc0) * L ** (1.0 / nu0))
            ys.append(M[(L, p)][0]); ws.append(1.0 / M[(L, p)][1] ** 2); Ls.append(L)
    xs, ys, ws = map(np.array, (xs, ys, ws))
    if xmax is not None:
        keep = np.abs(xs) <= xmax
        xs, ys, ws = xs[keep], ys[keep], ws[keep]
    def cost(theta):
        pc, nu = (theta[0], theta[1]) if pc_fixed is None and nu_fixed is None else \
                 ((pc_fixed, theta[0]) if nu_fixed is None else
                  ((theta[0], nu_fixed) if pc_fixed is None else (pc_fixed, nu_fixed)))
        x = np.array([(p - pc) * L ** (1.0 / nu)
                      for (L, p) in zip(Ls, ps_cycle)])
        A = design(x, deg)
        coef = np.linalg.lstsq(A * np.sqrt(ws)[:, None], ys * np.sqrt(ws), rcond=None)[0]
        r = A @ coef - ys
        return float(np.sum(ws * r * r))
    # rebuild point list
    pts = []
    for L in sorted(sizes):
        if L < Lmin: continue
        for p in ps:
            if (L, p) not in M: continue
            if xmax is not None and abs((p - pc0) * L ** (1.0 / nu0)) > xmax:
                continue
            pts.append((L, p, M[(L, p)][0], 1.0 / M[(L, p)][1] ** 2))
    Ls = [t[0] for t in pts]; ps_cycle = [t[1] for t in pts]
    ys = np.array([t[2] for t in pts]); ws = np.array([t[3] for t in pts])
    global _pts
    _pts = pts
    def cost2(theta):
        pc, nu = (theta[0], theta[1]) if pc_fixed is None and nu_fixed is None else \
                 ((pc_fixed, theta[0]) if nu_fixed is None else
                  ((theta[0], nu_fixed) if pc_fixed is None else (pc_fixed, nu_fixed)))
        x = np.array([(p - pc) * L ** (1.0 / nu) for (L, p) in zip(Ls, ps_cycle)])
        A = design(x, deg)
        coef = np.linalg.lstsq(A * np.sqrt(ws)[:, None], ys * np.sqrt(ws), rcond=None)[0]
        r = A @ coef - ys
        return float(np.sum(ws * r * r))
    if pc_fixed is not None and nu_fixed is not None:
        return dict(pc=pc_fixed, nu=nu_fixed, chi2=cost2(np.array([0.0])),
                    n=len(pts), deg=deg)
    x00 = [pc0 if pc_fixed is None else nu0, nu0] if (pc_fixed is None and nu_fixed is None) \
        else ([nu0] if pc_fixed is not None else [pc0])
    r = minimize(cost2, x00, method="Nelder-Mead",
                 options=dict(xatol=1e-9, fatol=1e-10, maxiter=2000))
    pc, nu = (r.x[0], r.x[1]) if pc_fixed is None and nu_fixed is None else \
             ((pc_fixed, r.x[0]) if nu_fixed is None else (r.x[0], nu_fixed))
    return dict(pc=pc, nu=nu, chi2=r.fun, n=len(pts), deg=deg)

def dchi2_profile(M, sizes, nus, deg=6, Lmin=64, xmax=2.0):
    base = fit_collapse(M, sizes, deg=deg, Lmin=Lmin, xmax=xmax)
    out = {}
    for nu in nus:
        f = fit_collapse(M, sizes, deg=deg, Lmin=Lmin, xmax=xmax, nu_fixed=nu)
        out[nu] = f["chi2"] - base["chi2"]
    return base, out

def bootstrap(M, sizes, B=100, deg=6, Lmin=64, xmax=2.0, seed=7):
    rng = np.random.default_rng(seed)
    ps = sorted({p for (L, p) in M})
    pcs, nus = [], []
    for b in range(B):
        Mb = {}
        for L in sorted(sizes):
            if L < Lmin: continue
            for p in ps:
                if (L, p) not in M: continue
                mn, se = M[(L, p)]
                Mb[(L, p)] = (mn + se * rng.standard_normal(), se)
        f = fit_collapse(Mb, sizes, deg=deg, Lmin=Lmin, xmax=xmax)
        pcs.append(f["pc"]); nus.append(f["nu"])
    return (float(np.mean(pcs)), float(np.std(pcs, ddof=1)),
            float(np.mean(nus)), float(np.std(nus, ddof=1)))

# ------------------------------------------------------------------ run
res = {"taus": {}}
for tau in (0.25, 0.5, 1.0, 2.0, 4.0):
    M, sizes = means(tau)
    log(f"=== tau = {tau} ===")
    cr = {}
    for (L1, L2) in ((16, 32), (32, 64), (64, 128), (128, 256)):
        if L1 in sizes and L2 in sizes:
            xs = crossings(M, sizes, L1, L2)
            if xs: cr[f"{L1}x{L2}"] = [round(x, 5) for x in xs]
    log("  crossings:", cr)
    coll = {}
    for Lmin in (16, 32, 64):
        if all(L >= Lmin for L in [64]) and Lmin <= sizes[-1]:
            f = fit_collapse(M, sizes, deg=6, Lmin=Lmin)
            coll[f"L>={Lmin}"] = dict(pc=round(f["pc"], 5), nu=round(f["nu"], 4),
                                      chi2dof=f"{f['chi2']:.1f}/{f['n']-9}")
            log(f"  collapse L>={Lmin} (sextic): p_c={f['pc']:.5f} nu={f['nu']:.4f} "
                f"chi2/dof={f['chi2']:.1f}/{f['n']-9}")
    base, dch = dchi2_profile(M, sizes, [1.0, 1.2, 1.24, 1.28, 4/3, 1.4])
    log("  frozen-nu dchi2:", {k: round(v, 1) for k, v in dch.items()})
    res["taus"][str(tau)] = dict(crossings=cr, collapses=coll,
                                  dchi2={str(k): v for k, v in dch.items()},
                                  base=dict(pc=base["pc"], nu=base["nu"]))

log("\n=== bootstrap (tau = 1, L >= 64, B = 100) ===")
M1, sizes1 = means(1.0)
pcm, pcs, num, nus = bootstrap(M1, sizes1, B=100)
log(f"  p_c = {pcm:.5f} +- {pcs:.5f}, nu = {num:.4f} +- {nus:.4f}")
res["bootstrap_tau1_L64"] = dict(pc=pcm, pc_se=pcs, nu=num, nu_se=nus, B=100)

log("\n=== verification against the deposited numbers ===")
dep = {
    "tau1_collapse": (0.16009, 1.2486, "18.3/18"),
    "tau05_collapse": (0.16039, 1.251, "15.5/18"),
    "tau2_collapse": (0.16027, 1.310, "82.8/18"),
    "tau1_dchi2": {1.0: 544.3, 1.2: 16.9, 1.24: 0.5, 1.28: 6.6, 4/3: 45.8, 1.4: 138.6},
    "bootstrap": (0.16011, 0.00009, 1.250, 0.014),
}
c1 = res["taus"]["1.0"]["collapses"]["L>=64"]
ok1 = abs(c1["pc"] - dep["tau1_collapse"][0]) < 3e-4 and abs(c1["nu"] - dep["tau1_collapse"][1]) < 0.006
log(f"  tau=1 collapse: got pc={c1['pc']}, nu={c1['nu']}; deposited 0.16009/1.2486 -> {ok1}")
c05 = res["taus"]["0.5"]["collapses"]["L>=64"]
ok05 = abs(c05["pc"] - dep["tau05_collapse"][0]) < 3e-4 and abs(c05["nu"] - dep["tau05_collapse"][1]) < 0.006
log(f"  tau=0.5 collapse: got pc={c05['pc']}, nu={c05['nu']}; deposited 0.16039/1.251 -> {ok05}")
d1 = res["taus"]["1.0"]["dchi2"]
okd = all(abs(d1[str(k)] - v) < max(3.0, 0.06 * v) for k, v in dep["tau1_dchi2"].items())
log(f"  tau=1 frozen-nu dchi2 vs deposited {{1: 544.3, 1.2: 16.9, 1.24: 0.5, 1.28: 6.6, 4/3: 45.8, 1.4: 138.6}} -> {okd}")
b = res["bootstrap_tau1_L64"]
okb = abs(b["pc"] - dep["bootstrap"][0]) < 4e-4 and abs(b["nu"] - dep["bootstrap"][2]) < 0.01
log(f"  bootstrap: got ({b['pc']:.5f}({b['pc_se']*1e4:.0f}), {b['nu']:.3f}({b['nu_se']*1e3:.0f})); "
    f"deposited 0.16011(9)/1.250(14) -> {okb}")
res["verification"] = dict(tau1=ok1, tau05=ok05, dchi2=okd, bootstrap=okb)
log(f"\nALL VERIFIED: {ok1 and ok05 and okd and okb}")

json.dump(res, open(os.path.join(OUT, "purif_summary.json"), "w"), indent=1, default=str)
log(f"written {os.path.join(OUT, 'purif_summary.json')}")
LOGF.close()
