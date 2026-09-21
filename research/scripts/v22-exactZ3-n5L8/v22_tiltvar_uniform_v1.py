"""v22_tiltvar_uniform_v1.py -- the tilted-variance (L,T)-uniformity
measurement: the open self-averaging criterion of Proposition
prop:replica-int / the v21 Discussion.

THE OBJECT.  The interpolation identity
    g(r) - r E log X = int_0^r (r - s) Var_s(log X) ds
reduces the disorder-replica interchange to the tilted-variance profile
Var_s (the variance of log X under the s-tilted disorder measure
dP_s ∝ X^s dP).  What remains open is precisely the UNIFORMITY of that
profile in (L, T).  v21 supplied one measured profile (the Clifford
record count: sub-Gaussian, the leading cumulant overshooting the gap by
13%).  This script measures the profile FAMILY:

  Part A (Haar, fully monitored p=1, exactly enumerated record partition
  functions -- the family the no-freeze theorem closes):
    grid L in {3,4,5,6} x T in {2L, 4L, 8L}, ndraw = 6000 circuits per cell
    (the deposited B3 protocol), Z_{T,omega} exactly per circuit
    (haar_smc_lib_v1.p1_exact_Z);
  Part B (Clifford disorder direction, the deposited production ladder):
    the raw trajectory arrays scgf_born_raw_L{8,12,16,24}_p{0.16,0.22}.npz
    (X = N_rand at t = 4L), X-object = 2^{-N_rand}.

Metrics per cell (all dimensionless, bootstrap SEs over 200 resamples):
  v(s)       = Var_s(log X)/T  (Part A, per period)  -- the profile;
  v(0)       the untilted variance rate (the self-averaging backbone);
  rho        = 2 int_0^1 (1-s) v(s) ds / v(0)  -- the sub-Gaussian profile
              ratio (rho = 1: flat/Gaussian; rho < 1: decaying; v21's
              Clifford point: rho ~ 0.885, the 13% overshoot);
  kappa      = -d ln[v(s)/v(0)]/ds |_{s=0}  -- the initial decay rate;
  ESS(s)     the effective tilted sample size (conditioning flag);
  the interpolation identity at m = 1, 2 per cell (validation).

The uniformity question: do rho and kappa (and the collapsed shapes
v(s)/v(0)) stay (L,T)-independent across the grid?
"""
import sys, os, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'v18-n4n5-smc'))
from haar_smc_lib_v1 import draw_circuit, p1_exact_Z

RES = os.path.join(HERE, '..', '..', 'results')
OUT = os.path.join(RES, 'v22-exactZ3-n5L8')


def log(*a):
    print(*a, flush=True)


SGRID = np.linspace(0.0, 1.5, 61)


def tilted_profile(logX, sgrid=SGRID):
    """Var_s(log X) and tilted ESS on the s-grid, empirical."""
    n = len(logX)
    vs, ess = [], []
    lx = np.asarray(logX, dtype=float)
    for s in sgrid:
        if s == 0.0:
            vs.append(float(lx.var()))
            ess.append(float(n))
            continue
        w = np.exp(s * lx - s * lx.max())
        tot = w.sum()
        wn = w / tot
        mu = float(np.sum(wn * lx))
        v = float(np.sum(wn * (lx - mu) ** 2))
        vs.append(v)
        ess.append(float(tot ** 2 / np.sum(w ** 2)))
    return np.array(vs), np.array(ess)


def profile_metrics(logX, Tnorm, sgrid=SGRID, nboot=200, rng=None):
    if rng is None:
        rng = np.random.default_rng(4242)
    vs, ess = tilted_profile(logX, sgrid)
    v0 = vs[0] / Tnorm
    vn = vs / Tnorm
    # rho: 2 * int_0^1 (1-s) v(s) ds / v(0)
    m1 = sgrid <= 1.0
    rho = 2.0 * float(np.trapezoid((1.0 - sgrid[m1]) * vn[m1], sgrid[m1])) \
        / (vn[0] + 1e-300)
    # kappa: initial log-decay rate over s in [0, 0.5]
    m2 = sgrid <= 0.5
    r = vn[m2] / (vn[0] + 1e-300)
    kap = -float(np.polyfit(sgrid[m2], np.log(np.maximum(r, 1e-300)), 1)[0])
    # bootstrap
    n = len(logX)
    rhos, kaps, v0s = [], [], []
    for _ in range(nboot):
        idx = rng.integers(0, n, size=n)
        vb, _ = tilted_profile(np.asarray(logX)[idx], sgrid)
        vnb = vb / Tnorm
        rhos.append(2.0 * float(np.trapezoid(
            (1.0 - sgrid[m1]) * vnb[m1], sgrid[m1])) / (vnb[0] + 1e-300))
        rb = vnb[m2] / (vnb[0] + 1e-300)
        kaps.append(-float(np.polyfit(
            sgrid[m2], np.log(np.maximum(rb, 1e-300)), 1)[0]))
        v0s.append(vnb[0])
    return dict(v0=v0, rho=rho, kappa=kap,
                rho_se=float(np.std(rhos)), kappa_se=float(np.std(kaps)),
                v0_se=float(np.std(v0s)),
                shape=[round(float(x / (vs[0] + 1e-300)), 4) for x in vs],
                ess_min=float(ess[sgrid > 0].min()))


def identity_check(logX, m=1.0):
    lhs = math.log(float(np.mean(np.exp(np.asarray(logX) * m)))) \
        - m * float(np.mean(logX))
    ss = np.linspace(0, m, 200)
    vs, _ = tilted_profile(logX, ss)
    rhs = float(np.trapezoid((m - ss) * vs, ss))
    return lhs, rhs, abs(lhs - rhs) / max(abs(lhs), 1e-300)


# ---------------------------------------------------------------------------
def part_a():
    log("== Part A: Haar p=1 exact-enumeration profile family ==")
    rng = np.random.default_rng(20260529)
    rows = []
    for L in (3, 4, 5, 6):
        for Tmul in (2, 4, 8):
            T = Tmul * L
            ndraw = 6000
            t0 = time.time()
            ZX = np.empty(ndraw)
            for i in range(ndraw):
                gates, sched = draw_circuit(L, 1.0, T, rng)
                ZX[i] = p1_exact_Z(L, T, gates, sched, -1.0)  # the collision k*=-1
            logX = np.log(ZX)
            met = profile_metrics(logX, T)
            lhs, rhs, rel = identity_check(logX, 1.0)
            row = {'family': 'haar_p1', 'L': L, 'T': T, 'ndraw': ndraw,
                   'ElogZ_per_T': float(logX.mean()) / T,
                   'secs': round(time.time() - t0, 1), **met,
                   'identity_rel': rel}
            rows.append(row)
            log(f"   L={L} T={T:2d}: v0={met['v0']:.4f}  rho={met['rho']:.3f}"
                f"({met['rho_se']:.3f})  kappa={met['kappa']:.3f}"
                f"({met['kappa']:.3f})  ESSmin={met['ess_min']:.0f}  "
                f"identity {rel:.1e}  [{row['secs']}s]")
            json.dump(rows, open(f'{OUT}/v22_tiltvar_haar_p1.json', 'w'),
                      indent=1)
    return rows


def part_b():
    log("== Part B: Clifford disorder direction (FRESH t = L/2 trajectories "
        "-- well conditioned, unlike the t = 4L production npz whose "
        "tilted ESS collapses to 1) ==")
    from v22_traj_beta2_v1 import run_cell_batched
    rows = []
    for ci, (L, p) in enumerate([(8, 0.16), (12, 0.16), (16, 0.16),
                                 (8, 0.22), (12, 0.22), (16, 0.22)]):
        t = L // 2
        plan = {8: (4_000_000, 500_000), 12: (2_400_000, 300_000),
                16: (1_600_000, 200_000)}
        Btot, batch = plan[L]
        seed = 20260701 + ci
        X, secs = run_cell_batched(L, p, t, Btot, batch, seed)
        logX = -math.log(2.0) * X          # log of the record prob P
        met = profile_metrics(logX, 2 * L * t)
        lhs, rhs, rel = identity_check(logX, 1.0)
        row = {'family': 'clifford_disorder', 'L': L, 'p': p, 't': t,
               'B': Btot, 'seed': seed, 'v0': met['v0'], 'rho': met['rho'],
               'rho_se': met['rho_se'], 'kappa': met['kappa'],
               'kappa_se': met['kappa_se'],
               'shape': met['shape'], 'ess_min': met['ess_min'],
               'identity_rel': rel, 'secs': secs}
        rows.append(row)
        log(f"   L={L:2d} p={p} t={t} B={Btot}: v0={met['v0']:.4f}  "
            f"rho={met['rho']:.3f}({met['rho_se']:.3f})  "
            f"kappa={met['kappa']:.3f}({met['kappa']:.3f})  "
            f"ESSmin={met['ess_min']:.0f}  identity {rel:.1e}")
        json.dump(rows, open(f'{OUT}/v22_tiltvar_clifford.json', 'w'),
                  indent=1)
    return rows


if __name__ == '__main__':
    part_a()
    part_b()
    log("done")
