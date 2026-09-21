"""SMC top-up (v1): larger populations for the k = +2 tail.

The production grid (N=384) leaves the k=+2 estimates population-starved
(ESS_min as low as 1-6 at p >= 0.2338).  This top-up reruns the k in
{+1.5, +2.0} column with N=1536 (and k=-2 as a control) at the same
circuits/seeds structure, for L in {8, 10, 12} and p in {0.2338, 0.4}.
"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from haar_smc_lib_v1 import draw_circuit, smc_run

OUT = 'mipt_results'
def log(*a):
    print(*a, flush=True)

def main():
    N = 1536
    ks = [-2.0, 1.5, 2.0]
    for L in (8, 10, 12):
        T = 2 * L
        nc = 8 if L <= 10 else 6
        for p in (0.2338, 0.4):
            rows = []
            for ic in range(nc):
                rng = np.random.default_rng(
                    (L * 1000003 + int(round(p * 1e4)) * 7919
                     + ic * 104729) % (1 << 30))
                gates, sched = draw_circuit(L, p, T, rng)
                for k in ks:
                    rr = np.random.default_rng(
                        (int(round((p + 3) * 1e4)) * 31 + ic * 1009
                         + int(round((k + 3) * 10))) % (1 << 30))
                    res = smc_run(L, p, T, k, N, gates, sched, rr)
                    rows.append({'circuit': ic, 'k': k,
                                 'logZ': res['logZ'],
                                 'psi': res['psi_hat'],
                                 'ess_min': res['ess_min'],
                                 'ess_mean': res['ess_mean']})
            out = {'L': L, 'p': p, 'T': T, 'N': N, 'ncirc': nc,
                   'kgrid': ks, 'rows': rows}
            fn = f'{OUT}/haar_smc_topup_L{L}_p{p:g}_v1.json'
            json.dump(out, open(fn, 'w'), indent=1)
            for k in ks:
                ps_k = [r['psi'] for r in rows if r['k'] == k]
                log(f"  L={L} p={p:g} k={k:+.1f}: psi = "
                    f"{np.mean(ps_k):+.5f} +- "
                    f"{np.std(ps_k)/math.sqrt(len(ps_k)):.5f}  ess_min="
                    f"{min(r['ess_min'] for r in rows if r['k']==k):.0f}")
            log(f"  -> {fn}")

if __name__ == '__main__':
    main()
