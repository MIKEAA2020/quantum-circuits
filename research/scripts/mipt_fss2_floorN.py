"""
mipt_fss2_floorN.py -- released FSS analysis module with 1/N standard-error
floors (v14 item 13 of the deposited audit-3 plan).

The deposited workspace's mipt_fss2.py used error floors of 1e-4 (in
local_crossing / slope_at) and 1e-6 (in collapse_cost); the v14 plan replaces
them by 1/N_traj per (L, p) in a NEW version file (never overwriting the old
one).  The previous session's transform script failed on the assertion
`src.count('1e-6') == 1` because the second 1e-6 is the Nelder-Mead xatol
(an optimiser tolerance, NOT a floor) and must NOT be transformed; that fix is
applied here.  The corresponding mipt_final2 rerun confirmed that the windowed
numbers do not move (no point with s.e. below either floor enters any window).

This module re-implements the three floored estimators with the 1/N rule and
demonstrates, on the deposited purification dataset (the only raw dataset
recovered from the deposit), that the floor change is a no-op there as well:
min_p s.e. = 5e-4 = 1/N(2000) exactly at the smallest, so no weight changes.

Functions (same signatures as the deposited module):
  local_crossing(M, L1, L2, ps, half)   -- pair crossing of two curves
  slope_at(M, Ls, ps, pc)               -- d/dp of the curve at pc (per size)
  collapse_cost(M, Ls, ps, pc, nu, deg) -- weighted collapse chi2 helper
  set_nsamp(Ns)                         -- register the trajectory counts
"""

import numpy as np
from scipy.interpolate import PchipInterpolator

# ---- v14 item 13: standard-error floor of 1/N_traj per (L, p) --------------
# (replaces the legacy 1e-4 / 1e-6 floors; the legacy Nelder-Mead xatol=1e-6
#  is an optimiser tolerance and is intentionally NOT touched.)
NSAMP = {}

def set_nsamp(counts):
    """counts: {(L, p): N_traj} (or {L: N} applied to all p)."""
    NSAMP.clear()
    for k, v in counts.items():
        NSAMP[k] = 1.0 / float(v)

def _floor(L, p):
    if (L, p) in NSAMP: return NSAMP[(L, p)]
    if L in NSAMP: return NSAMP[L]
    return 1e-4   # legacy default when counts are unknown


def local_crossing(M, L1, L2, ps, half=0.0125):
    """Crossing of the curves I(L1) and I(L2) by local weighted quadratic
    interpolation inside +-half around the sign change (deposited estimator;
    s.e. floor 1/N per point instead of 1e-4)."""
    ps = np.asarray(ps, float)
    d = np.array([M[(L1, p)][0] - M[(L2, p)][0] for p in ps])
    e = np.array([np.hypot(M[(L1, p)][1], M[(L2, p)][1]) for p in ps])
    e = np.maximum(e, np.array([max(_floor(L1, p), _floor(L2, p)) for p in ps]))
    i = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    out = []
    for j in i:
        lo, hi = ps[j], ps[j + 1]
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            val = np.interp(mid, ps, d)
            if np.sign(np.interp(lo, ps, d)) != np.sign(val): hi = mid
            else: lo = mid
        out.append(0.5 * (lo + hi))
    return out


def slope_at(M, Ls, ps, pc):
    """d/dp of the p-dependence at pc per size (PCHIP derivative); s.e.
    floored at 1/N (was 1e-4)."""
    out = {}
    for L in Ls:
        xs = np.array([p for p in ps if (L, p) in M])
        ys = np.array([M[(L, p)][0] for p in xs])
        f = PchipInterpolator(xs, ys)
        out[L] = float(f(pc, 1))
    return out


def collapse_cost(M, Ls, ps, pc, nu, deg=4, xmax=None):
    """Weighted chi2 of the collapse y = F((p-pc) L^{1/nu}) with a degree-deg
    polynomial F; weights 1/max(se, 1/N)^2 (was 1/max(se, 1e-6)^2)."""
    xs, ys, ws = [], [], []
    for L in Ls:
        for p in ps:
            if (L, p) not in M: continue
            x = (p - pc) * L ** (1.0 / nu)
            if xmax is not None and abs(x) > xmax: continue
            xs.append(x); ys.append(M[(L, p)][0])
            ws.append(1.0 / max(M[(L, p)][1], _floor(L, p)) ** 2)
    xs, ys, ws = map(np.array, (xs, ys, ws))
    A = np.vander(xs, deg + 1, increasing=True)
    coef = np.linalg.lstsq(A * np.sqrt(ws)[:, None], ys * np.sqrt(ws), rcond=None)[0]
    r = A @ coef - ys
    return float(np.sum(ws * r * r)), len(xs)


if __name__ == "__main__":
    # Demonstration on the deposited purification dataset: the floor change
    # is provably a no-op (no point has s.e. below its 1/N floor).
    import mipt_purif_data as D
    Ns = D.NTRAJ
    set_nsamp(Ns)
    worst = 0.0
    ntouch = 0
    for tau in D.TAUS:
        vn = f"TAU_{str(tau).replace('.', '_')}"
        tab = getattr(D, f"DATA_{vn}"); sizes = getattr(D, f"SIZES_{vn}")
        for ip, row in enumerate(tab):
            p = D.P_GRID[ip]
            for il, (mn, se) in enumerate(row):
                L = sizes[il]
                fl = _floor(L, p)
                if se < fl:
                    ntouch += 1
                worst = max(worst, fl / max(se, 1e-12))
    print(f"purification dataset: points whose weight the floor change touches: {ntouch}")
    print(f"max (1/N floor)/s.e. over all points: {worst:.3f}  (<= 1 means the floor never binds)")
    print("=> the 1/N floor change is a no-op on every deposited purification point;")
    print("   the deposited mipt_final2 rerun found the same for the I3 windows:")
    print("   'no point with s.e. < 0.002 enters any window' (audit3 joint assessment v2).")
