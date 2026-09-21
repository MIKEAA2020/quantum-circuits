"""v22_traj_beta2_v1.py -- the well-conditioned beta=2 trajectory test of
the identification  E_omega[2^{-2 N_rand}] = Zbar_3.

CONTEXT.  The exact closure (v22_z3_exact_v1.py) gives Lambda(2) via the
Haar three-replica operator; the deposited t=4L trajectory estimates Xi_2.0
are grossly biased (ESS collapse: the true exponent is ~0.034 nats/site,
the trajectory ladder reports a decaying 0.0159 -> 0.0049).  Two hypotheses
remain: (H1) pure estimator bias at long t (the identification holds);
(H2) the Clifford-ensemble 3-replica moment genuinely differs from the
Haar Zbar_3 (no exact 3-design).  This script discriminates: at t = L/2
the collision tilt has ESS/B = exp(-2Lt(Lambda(2)-2Lambda(1))) ~ 0.15
(L=8), so a large-B trajectory run is WELL conditioned; it estimates
E[2^{-X}] (beta=1 control, exact by the 2-design) and E[2^{-2X}] (beta=2,
the identification under test) and compares both with the exact Zbar_2(t)
and Zbar_3(t).

The simulator is the deposited mipt_born_scgf.BatchCircuit (vectorized
phase-free F2 tableau, gates = uniform 720 symplectic actions, X = number
of random outcomes, P(R) = 2^{-X}), run in memory-bounded batches with a
fresh PCG64 seed per cell (recorded).
"""
import sys, os, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
from mipt_born_scgf import BatchCircuit
from v22_z3_exact_v1 import zbar_exact

OUT = os.path.join(HERE, '..', '..', 'results', 'v22-exactZ3-n5L8')
SEED0 = 20260612


def log(*a):
    print(*a, flush=True)


def run_cell_batched(L, p, t, Btot, batch, seed):
    """Batched trajectory run; returns X array (length Btot)."""
    rng = np.random.Generator(np.random.PCG64(seed))
    xs = []
    done = 0
    t0 = time.time()
    while done < Btot:
        b = min(batch, Btot - done)
        sim = BatchCircuit(L, p, b, rng)
        for _ in range(t):
            sim.step_period()
        xs.append(sim.X.copy())
        done += b
    X = np.concatenate(xs)
    return X, round(time.time() - t0, 1)


def moments(X, nboot=400, rng=None):
    if rng is None:
        rng = np.random.Generator(np.random.PCG64(777))
    B = len(X)
    ln2 = math.log(2.0)
    out = {}
    for beta, tag in ((1, 'b1'), (2, 'b2')):
        w = np.exp(-beta * ln2 * X)
        m = float(w.mean())
        out[f'E_w_{tag}'] = m
        out[f'log_E_w_{tag}'] = math.log(m)
        # empirical ESS of the beta-weights
        wmax = float(w.max())
        ws = w / wmax
        ess = float(ws.sum() ** 2 / (ws ** 2).sum())
        out[f'ESS_{tag}'] = ess
        boot = []
        for _ in range(nboot):
            idx = rng.integers(0, B, size=B)
            wb = np.exp(-beta * ln2 * X[idx])
            boot.append(math.log(float(wb.mean())))
        out[f'log_E_w_{tag}_se'] = float(np.std(boot))
    return out


def main():
    cells = [(8, 0.16), (12, 0.16), (16, 0.16),
             (8, 0.22), (12, 0.22), (16, 0.22)]
    plan = {8: (4_000_000, 500_000), 12: (2_400_000, 300_000),
            16: (1_600_000, 200_000)}
    rows = []
    for ci, (L, p) in enumerate(cells):
        t = L // 2
        Btot, batch = plan[L]
        seed = SEED0 + ci
        X, secs = run_cell_batched(L, p, t, Btot, batch, seed)
        mom = moments(X)
        z2, _ = zbar_exact(2, 2, p, L // 2, t)
        z3, _ = zbar_exact(3, 2, p, L // 2, t)
        rel1 = abs(mom['E_w_b1'] - z2) / z2
        rel2 = abs(mom['E_w_b2'] - z3) / z3
        z1 = abs(math.log(mom['E_w_b1']) - math.log(z2)) / mom['log_E_w_b1_se']
        z2s = abs(math.log(mom['E_w_b2']) - math.log(z3)) / mom['log_E_w_b2_se']
        row = {'L': L, 'p': p, 't': t, 'B': Btot, 'seed': seed,
               'secs': secs,
               'E_w1_traj': mom['E_w_b1'], 'E_w1_exact': z2,
               'rel_b1': rel1, 'z_b1': z1, 'ESS_b1': mom['ESS_b1'],
               'E_w2_traj': mom['E_w_b2'], 'E_w2_exact': z3,
               'rel_b2': rel2, 'z_b2': z2s, 'ESS_b2': mom['ESS_b2'],
               'se_log_b1': mom['log_E_w_b1_se'],
               'se_log_b2': mom['log_E_w_b2_se']}
        rows.append(row)
        log(f"L={L:2d} p={p} t={t} B={Btot}:")
        log(f"   beta=1: E[2^-X] = {mom['E_w_b1']:.6e} vs exact "
            f"{z2:.6e}  rel {rel1:.2e}  (z {z1:.1f} sigma; "
            f"ESS {mom['ESS_b1']:.0f})")
        log(f"   beta=2: E[2^-2X] = {mom['E_w_b2']:.6e} vs exact "
            f"{z3:.6e}  rel {rel2:.2e}  (z {z2s:.1f} sigma; "
            f"ESS(w^2) {mom['ESS_b2']:.0f})")
        json.dump(rows, open(f'{OUT}/v22_traj_beta2.json', 'w'), indent=1)
    log(f"written {OUT}/v22_traj_beta2.json")


if __name__ == '__main__':
    main()
