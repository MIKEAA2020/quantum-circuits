"""RERUN on the recovered fuller_workspace dataset (new file; mipt_purif_analysis.py untouched).
Original docstring: Analysis of the purification (mixed-initial-state) locator run, mipt_data_purif/ (see mipt_purif_sim.py).
Order parameter: average reference entropy <S_ref>(p, L, tau=t/L) = <S(rho_system)> (Gullans-Huse PRX 10, 041020).
Scaling ansatz (GH Eq. 37, z=1): <S> = F(x, tau), x = (p - p_c) L^{1/nu}.
Outputs mipt_results/purif_summary.json and prints crossings, collapse fits and bootstrap errors.
Standard errors are floored at 1/N_traj (integer-valued observable; a zero sample variance is not a zero error)."""
import numpy as np, glob, json, sys, itertools, collections
from scipy.optimize import minimize, brentq

TAUS = [0.25, 0.5, 1.0, 2.0, 4.0]

def load():
    acc = collections.defaultdict(list)
    for f in sorted(glob.glob('mipt_data_purif/purif_L*_c*.npz')):
        z = np.load(f); L = int(z['L']); p = float(z['p']); rec = z['rec']
        acc[(L, p)].append((rec, z['data']))
    out = {}
    for (L, p), lst in acc.items():
        rec = lst[0][0]; data = np.concatenate([d for (_, d) in lst], axis=0)
        assert all(np.array_equal(r, rec) for (r, _) in lst)
        out[(L, p)] = (rec, data)
    return out

def stats(D):
    """mean, se (floored at 1/N), N of S_ref for each (L, p, tau)."""
    T = {}
    for (L, p), (rec, data) in D.items():
        for it, t in enumerate(rec):
            tau = t / L
            S = data[:, it, 0].astype(float)
            N = len(S); m = S.mean(); se = max(S.std(ddof=1) / np.sqrt(N), 1.0 / N)
            IAB = (data[:, it, 1] + data[:, it, 2] - data[:, it, 3]).astype(float)
            T[(L, p, round(tau, 4))] = dict(mean=m, se=se, N=N, IAB=IAB.mean(), IAB_se=max(IAB.std(ddof=1) / np.sqrt(N), 1.0 / N),
                                            nonzero=float((S > 0).mean()))
    return T

def crossings(T, Ls, ps, tau):
    """Pairwise crossing p*(L1,L2) of <S_ref>(p) using local cubic interpolation of the two curves."""
    out = []
    for L1, L2 in zip(Ls[:-1], Ls[1:]):
        y1 = np.array([T[(L1, p, tau)]['mean'] for p in ps]); y2 = np.array([T[(L2, p, tau)]['mean'] for p in ps])
        c1 = np.polyfit(ps, y1, 3); c2 = np.polyfit(ps, y2, 3)
        f = lambda p: np.polyval(c1, p) - np.polyval(c2, p)
        grid = np.linspace(ps[0], ps[-1], 401); vals = f(grid)
        roots = [brentq(f, grid[i], grid[i + 1]) for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
        out.append((L1, L2, roots[0] if len(roots) == 1 else (roots if roots else None)))
    return out

def collapse(T, Ls, ps, tau, K=6, x_max=None, nu0=1.25, pc0=0.16, fixed=None):
    """Least-squares collapse S = F(x) with F a polynomial of degree K in x; returns (pc, nu, chi2, npts)."""
    pts = [(L, p, T[(L, p, tau)]['mean'], T[(L, p, tau)]['se']) for L in Ls for p in ps]
    Lv = np.array([q[0] for q in pts], float); pv = np.array([q[1] for q in pts]); yv = np.array([q[2] for q in pts]); ev = np.array([q[3] for q in pts])
    def chi2(par):
        pc, nu = par
        x = (pv - pc) * Lv ** (1.0 / nu)
        sel = np.ones(len(x), bool) if x_max is None else (np.abs(x) <= x_max)
        if sel.sum() < K + 4: return 1e9
        A = np.vander(x[sel], K + 1) / ev[sel, None]
        b = yv[sel] / ev[sel]
        coef, *_ = np.linalg.lstsq(A, b, rcond=None)
        return float(np.sum((A @ coef - b) ** 2))
    if fixed is not None:
        pc, nu = fixed
        return pc, nu, chi2((pc, nu)), int(np.sum(np.abs((pv - pc) * Lv ** (1 / nu)) <= (x_max if x_max else 1e9)))
    best = None
    for nu_s in (1.1, 1.25, 1.4):
        for pc_s in (0.158, 0.160, 0.162):
            r = minimize(chi2, [pc_s, nu_s], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
            if best is None or r.fun < best.fun: best = r
    pc, nu = best.x
    npts = int(np.sum(np.abs((pv - pc) * Lv ** (1 / nu)) <= (x_max if x_max else 1e9)))
    return float(pc), float(nu), float(best.fun), npts

def bootstrap_collapse(D, Ls, ps, tau, nboot, K=6, x_max=None, seed=1):
    rng = np.random.default_rng(seed)
    res = []
    for b in range(nboot):
        Tb = {}
        for L in Ls:
            for p in ps:
                rec, data = D[(L, p)]
                it = [i for i, t in enumerate(rec) if abs(t / L - tau) < 1e-9][0]
                S = data[:, it, 0].astype(float); N = len(S)
                idx = rng.integers(0, N, N); Sb = S[idx]
                Tb[(L, p, tau)] = dict(mean=Sb.mean(), se=max(S.std(ddof=1) / np.sqrt(N), 1.0 / N))
        res.append(collapse(Tb, Ls, ps, tau, K=K, x_max=x_max)[:2])
    res = np.array(res)
    return res.mean(0), res.std(0, ddof=1)

if __name__ == '__main__':
    nboot = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    D = load(); T = stats(D)
    Ls = sorted(set(L for (L, p) in D)); ps = sorted(set(p for (L, p) in D))
    taus = sorted(set(k[2] for k in T))
    summary = dict(Ls=Ls, ps=ps, taus=taus, table={}, crossings={}, collapses={}, frozen={}, boot={})
    print('sizes', Ls, 'p', ps, 'taus', taus)
    for tau in taus:
        print(f'\n=== tau = t/L = {tau} ===')
        print('p      ' + ''.join(f'L={L:<4d}          ' for L in Ls if (Ls[0], ps[0], tau) in T and (L, ps[0], tau) in T))
        for p in ps:
            row = []
            for L in Ls:
                if (L, p, tau) in T:
                    s = T[(L, p, tau)]; row.append(f"{s['mean']:.4f}({s['se']:.4f}) ")
                    summary['table'][f'{L}_{p}_{tau}'] = dict(mean=s['mean'], se=s['se'], N=s['N'], IAB=s['IAB'], IAB_se=s['IAB_se'], nonzero=s['nonzero'])
            print(f'{p:.3f}  ' + ''.join(row))
        Lt = [L for L in Ls if (L, ps[0], tau) in T]
        if len(Lt) < 2: continue
        cr = crossings(T, Lt, ps, tau)
        print('crossings p*(L1,L2):', [(a, b, (round(c, 5) if isinstance(c, float) else c)) for (a, b, c) in cr])
        summary['crossings'][str(tau)] = [(a, b, c) for (a, b, c) in cr]
        for Lmin in (16, 32, 64):
            Lset = [L for L in Lt if L >= Lmin]
            if len(Lset) < 3: continue
            for xm in (None, 2.0):
                pc, nu, chi2, npts = collapse(T, Lset, ps, tau, K=6, x_max=xm)
                dof = npts - 2 - 7
                print(f'  collapse L>={Lmin} |x|<={xm}: p_c={pc:.5f} nu={nu:.4f} chi2/dof={chi2:.1f}/{dof}')
                summary['collapses'][f'{tau}_L{Lmin}_x{xm}'] = dict(pc=pc, nu=nu, chi2=chi2, dof=dof, npts=npts)
                if xm is None:
                    fro = {}
                    for nuf in (1.0, 1.2, 1.24, 1.28, 4 / 3, 1.4):
                        # profile over p_c at frozen nu on the same (full) point set
                        r = minimize(lambda q: collapse(T, Lset, ps, tau, K=6, x_max=None, fixed=(q[0], nuf))[2], [pc], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-8))
                        fro[round(nuf, 4)] = dict(pc=float(r.x[0]), dchi2=float(r.fun - chi2))
                    print('   frozen-nu dchi2 (full set):', {k: round(v['dchi2'], 1) for k, v in fro.items()})
                    summary['frozen'][f'{tau}_L{Lmin}'] = fro
        if nboot and tau in (1.0, 2.0):
            for Lmin in (32, 64):
                Lset = [L for L in Lt if L >= Lmin]
                mean, sd = bootstrap_collapse(D, Lset, ps, tau, nboot, K=6, x_max=None)
                print(f'  bootstrap L>={Lmin} (n={nboot}): p_c={mean[0]:.5f}+-{sd[0]:.5f} nu={mean[1]:.4f}+-{sd[1]:.4f}')
                summary['boot'][f'{tau}_L{Lmin}'] = dict(pc=float(mean[0]), pc_sd=float(sd[0]), nu=float(mean[1]), nu_sd=float(sd[1]), nboot=nboot)
    json.dump(summary, open('mipt_results/purif_summary_rerun.json', 'w'), indent=1, default=float)
    print('\nwritten mipt_results/purif_summary_rerun.json')
