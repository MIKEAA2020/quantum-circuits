"""Budget benchmark v1: measure the REAL cost of the n=5 L=6 (nb=3) and
n=4 L=10 (nb=5) ring-transfer matvecs that v18 declared beyond the
3 GB / 2-core budget.

For each case: build the RingOperator (colour-restricted), time 3 matvecs,
report wall seconds, flops estimate and peak RSS.  Also verify the
colour-commutation [C, P] = 0 at n=5 nb=2 (justifies single projection)
and the correctness of the restricted matvec vs the v1 double-projection.
"""
import sys, os, time, resource
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n45_annealed_lib_v1 import RingOperator, leading_eigs

def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

def bench(n, d, p, nb, beta, colour, reps=3):
    t0 = time.time()
    op = RingOperator(n, d, p, nb, beta=beta, mom_k0=True, colour=colour)
    t_build = time.time() - t0
    rng = np.random.default_rng(0)
    v = rng.standard_normal(op.N)
    if op.mom_k0:
        v = v.reshape((op.g,) * op.nb).sum(axis=tuple())  # dummy
    v = rng.standard_normal(op.N)
    # project into the colour block once (warm start equivalent)
    t0 = time.time()
    w = op.matvec(v)
    t_first = time.time() - t0
    ts = []
    for _ in range(reps):
        t0 = time.time()
        w = op.matvec(v)
        ts.append(time.time() - t0)
    flops = 2 * nb * 2 * op.g ** (nb + 1)          # M1+M2 ring contractions
    print(f"n={n} nb={nb} (L={2*nb}) N={op.N:.3e} colour={colour} beta={beta}: "
          f"build {t_build:.1f}s, first {t_first:.2f}s, steady "
          f"{min(ts):.2f}s/matvec, ~{flops/1e9:.1f} GFlop -> "
          f"{flops/min(ts)/1e9:.1f} GFLOPS, peak RSS {rss_mb():.0f} MB",
          flush=True)
    return op, w

# --- colour commutation check at n=5, nb=2 (small) ---
print("--- [C,P]=0 check, n=5 nb=2 ---", flush=True)
op = RingOperator(5, 2, 0.4, 2, beta=8, mom_k0=False, colour=None)
rng = np.random.default_rng(1)
v = rng.standard_normal(op.N)
Cv = op.matvec(v)
Pv = op.fc.block('triv', 'triv', v)
CP = op.fc.block('triv', 'triv', Cv)     # P C v
PC = op.matvec(Pv)                        # C P v
err = np.linalg.norm(CP - PC) / np.linalg.norm(CP)
print(f"||PC v - CP v|| / ||CP v|| = {err:.2e}  "
      f"({'commutes' if err < 1e-10 else 'DOES NOT commute'})", flush=True)

# --- the two budget-breaking cases ---
print("--- the v18 budget-breaking cases ---", flush=True)
bench(5, 2, 0.45, 3, beta=8, colour=('triv', 'triv'))   # n=5 L=6: N=1.7e6
bench(5, 2, 0.45, 3, beta=8, colour=('std', 'std'))
bench(4, 2, 0.38, 5, beta=2, colour=('triv', 'triv'))   # n=4 L=10: N=8.0e6
bench(4, 2, 0.38, 5, beta=2, colour=('std', 'std'))
print(f"final peak RSS {rss_mb():.0f} MB", flush=True)
