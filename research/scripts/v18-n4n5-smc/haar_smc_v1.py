"""Haar SMC record-multifractality (Target C) — driver (v1).

Phases:
  validate : Va (k=0 identity + deposited-surprisal comparison),
             Vb (brute-force unbiasedness at L=4: E[Zhat] vs exact Z_T(k)),
             Vc (p=1 exact Markov-chain Z vs E[Zhat]).
  produce  : the production grid — for each (L, p): circuits x k-grid x
             N particles, T = 2L periods; writes per-(L,p) JSON with
             psi per k (mean of log Zhat over circuits; also the annealed
             log mean), ESS stats, and the k=0 A_T moments.
  analyze  : assembles psi(k) curves, tau(q) = -psi(1-q), D(q), alpha(q),
             f(alpha), freezing diagnostics (tau'' ~ 0 / linear branch),
             and the L- and p-dependence tables.

Conventions per haar_smc_lib_v1 (manuscript Eq. SMC / Prop SMC).
"""
import sys, os, json, math, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from haar_smc_lib_v1 import (draw_circuit, smc_run, brute_force_Z,
                              p1_exact_Z)

OUT = 'mipt_results'
LOG = 'logs'
def log(*a):
    print(*a, flush=True)

# ---------------------------------------------------------------------------
def phase_validate(args):
    ok_all = True
    # ---------------- Vb: brute-force unbiasedness (L=4) ----------------
    log("Vb  brute force: L=4, p=0.2, T=4 — E[Zhat] vs exact Z_T(k):")
    L, p, T, N, R = 4, 0.2, 4, 64, 600
    kgrid = [-1.5, -0.5, 0.5, 1.5]
    rng = np.random.default_rng(20240601)
    gates, sched = draw_circuit(L, p, T, rng)
    Zexact, M = brute_force_Z(L, T, gates, sched, 0.0)  # count events
    log(f"    fixed circuit: {M} measurement events "
        f"({2 ** M} records enumerated)")
    for k in kgrid:
        Zex, _ = brute_force_Z(L, T, gates, sched, k)
        ests = []
        for r in range(R):
            rr = np.random.default_rng(700000 + r)
            ests.append(smc_run(L, p, T, k, N, gates, sched,
                                rr)['logZ'])
        ests = np.exp(np.array(ests))
        mean = float(np.mean(ests))
        se = float(np.std(ests) / math.sqrt(R))
        z = (mean - Zex) / se if se > 0 else 0.0
        ok = abs(z) < 4.0
        ok_all &= ok
        log(f"    k={k:+.1f}: E[Zhat]={mean:.6g} +- {se:.2g}  "
            f"exact={Zex:.6g}  z={z:+.2f}  [{'OK' if ok else 'FAIL'}]")
    # ---------------- Vc: p=1 exact Markov chain ----------------
    log("Vc  p=1 exact: L=4, T=3 — E[Zhat] vs 1^T K_k^{S-1} e_0:")
    L, T, N, R = 4, 3, 96, 400
    rng = np.random.default_rng(20240602)
    gates, sched = draw_circuit(L, 1.0, T, rng)
    for k in (-1.0, 0.5, 1.5):
        Zex = p1_exact_Z(L, T, gates, sched, k)
        ests = []
        for r in range(R):
            rr = np.random.default_rng(800000 + r)
            ests.append(np.exp(smc_run(L, 1.0, T, k, N, gates, sched,
                                       rr)['logZ']))
        mean, se = float(np.mean(ests)), float(np.std(ests) /
                                               math.sqrt(R))
        z = (mean - Zex) / se if se > 0 else 0.0
        ok = abs(z) < 4.0
        ok_all &= ok
        log(f"    k={k:+.1f}: E[Zhat]={mean:.6g} +- {se:.2g}  "
            f"exact={Zex:.6g}  z={z:+.2f}  [{'OK' if ok else 'FAIL'}]")
    # ---------------- Va: k=0 + deposited surprisal ----------------
    log("Va  k=0 identity + deposited-surprisal comparison (L=8):")
    L, p, T, N = 8, 0.2338, 16, 256
    rng = np.random.default_rng(20240603)
    gates, sched = draw_circuit(L, p, T, rng)
    r = smc_run(L, p, T, 0.0, N, gates, sched,
                np.random.default_rng(900001), track_A=True)
    ok = abs(r['psi_hat']) < 1e-12
    ok_all &= ok
    log(f"    psi_hat(0) = {r['psi_hat']:.2e}  "
        f"[{'OK' if ok else 'FAIL'}]")
    # deposited npz: mean surprisal RATE at the matched rec time
    try:
        d = np.load(f'mipt_data/haar_L{L}_p{p:.4f}.npz')
        recs = list(d['rec'])
        i16 = recs.index(T)
        sur = d['data'][:, i16, -1] / T        # surprisal rate (nats/period)
        mine = r['A_T'] / T
        dm, dd = float(np.mean(mine)), float(np.std(mine) /
                                             math.sqrt(len(mine)))
        sm, sd = float(np.mean(sur)), float(np.std(sur) /
                                            math.sqrt(len(sur)))
        z = (dm - sm) / math.sqrt(dd ** 2 + sd ** 2)
        ok = abs(z) < 4.0
        ok_all &= ok
        log(f"    A_T/T: SMC {dm:.4f}+-{dd:.4f} (N={len(mine)}) vs "
            f"deposited {sm:.4f}+-{sd:.4f} (n={len(sur)})  z={z:+.2f}  "
            f"[{'OK' if ok else 'FAIL'}]")
    except FileNotFoundError:
        log("    [deposited npz not found — skipped]")
    log(f"=== haar SMC validation: "
        f"{'ALL OK' if ok_all else 'FAILURES PRESENT'} ===")
    return 0 if ok_all else 1

# ---------------------------------------------------------------------------
def phase_produce(args):
    Ls = [int(x) for x in args.Ls.split(',')] if args.Ls else [6, 8, 10, 12]
    ps = [float(x) for x in args.ps.split(',')] if args.ps else \
        [0.10, 0.1597, 0.2338, 0.40]
    kgrid = ([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
             if not args.ks else
             [float(x) for x in args.ks.split(',')])
    N = args.N or 384
    ncirc = args.ncirc or 8
    for L in Ls:
        T = 2 * L
        nc = ncirc if L <= 10 else max(4, ncirc // 2)
        for p in ps:
            t0 = time.time()
            rows = []
            # circuits
            for ic in range(nc):
                rng = np.random.default_rng(
                    (L * 1000003 + int(round(p * 1e4)) * 7919
                     + ic * 104729) % (1 << 30))
                gates, sched = draw_circuit(L, p, T, rng)
                for k in kgrid:
                    rr = np.random.default_rng(
                        (int(round((p + 3) * 1e4)) * 31 + ic * 1009
                         + int(round((k + 3) * 10))) % (1 << 30))
                    res = smc_run(L, p, T, k, N, gates, sched, rr,
                                  track_A=(k == 0.0))
                    rows.append({'circuit': ic, 'k': k,
                                 'logZ': res['logZ'],
                                 'psi': res['psi_hat'],
                                 'ess_min': res['ess_min'],
                                 'ess_mean': res['ess_mean'],
                                 'A_mean': (float(np.mean(res['A_T']) / T)
                                            if res['A_T'] is not None
                                            else None),
                                 'A_var': (float(np.var(res['A_T']) / T)
                                           if res['A_T'] is not None
                                           else None)})
                # per-circuit summary line
            out = {'L': L, 'p': p, 'T': T, 'N': N, 'ncirc': nc,
                   'kgrid': kgrid, 'rows': rows}
            fn = f'{OUT}/haar_smc_L{L}_p{p:g}_v1.json'
            json.dump(out, open(fn, 'w'), indent=1)
            # quick summary
            for k in kgrid:
                ps_k = [r['psi'] for r in rows if r['k'] == k]
                log(f"  L={L} p={p:g} k={k:+.1f}: psi = "
                    f"{np.mean(ps_k):+.5f} +- {np.std(ps_k)/math.sqrt(len(ps_k)):.5f}"
                    f"  ess_min={min(r['ess_min'] for r in rows if r['k']==k):.0f}")
            log(f"  -> {fn}  [{time.time()-t0:.1f}s]")
    log("produce done")

def phase_analyze(args):
    """Assemble psi(k), tau(q), D(q), alpha, f(alpha); freezing test."""
    import glob
    files = sorted(glob.glob(f'{OUT}/haar_smc_L*_p*_v1.json'))
    res = {}
    for fn in files:
        d = json.load(open(fn))
        key = f"L{d['L']}_p{d['p']:g}"
        ks, psis, ses, anns, essmins = [], [], [], [], []
        for k in d['kgrid']:
            rows = [r for r in d['rows'] if r['k'] == k]
            lz = np.array([r['logZ'] for r in rows])
            psis.append(float(np.mean(lz) / d['T']))
            ses.append(float(np.std(lz) / math.sqrt(len(lz)) / d['T']))
            anns.append(float(np.log(np.mean(np.exp(lz))) / d['T']))
            essmins.append(float(min(r['ess_min'] for r in rows)))
        res[key] = {'L': d['L'], 'p': d['p'], 'T': d['T'], 'N': d['N'],
                    'ncirc': d['ncirc'], 'k': d['kgrid'], 'psi': psis,
                    'psi_se': ses, 'psi_annealed': anns,
                    'ess_min': essmins}
    # tau(q) = -psi(1-q); D(q) = tau(q)/(q-1)
    for key, d in res.items():
        k = np.array(d['k']); psi = np.array(d['psi'])
        q = 1.0 - k
        tau = -psi
        D = np.where(np.abs(q - 1) > 1e-9, tau / (q - 1), np.nan)
        d['q'] = q.tolist(); d['tau'] = tau.tolist()
        d['D'] = D.tolist()
        # freezing diagnostic: second difference of tau vs q (linear branch)
        if len(q) >= 3:
            o = np.argsort(q)
            qs, taus = q[o], tau[o]
            d['tau_dd'] = np.gradient(np.gradient(taus, qs), qs).tolist()
            d['q_sorted'] = qs.tolist(); d['tau_sorted'] = taus.tolist()
        # entropy rate + variance from k=0 rows
        rows0 = [r for r in json.load(
            open(f"{OUT}/haar_smc_L{d['L']}_p{d['p']:g}_v1.json"))['rows']
            if r['k'] == 0.0]
        d['A_mean'] = float(np.mean([r['A_mean'] for r in rows0]))
        d['A_var'] = float(np.mean([r['A_var'] for r in rows0]))
    json.dump(res, open(f'{OUT}/haar_smc_summary_v1.json', 'w'), indent=1)
    # print tables
    log("=== psi(k) / tau(q) / D(q) per (L, p) ===")
    for key in sorted(res, key=lambda s: (res[s]['L'], res[s]['p'])):
        d = res[key]
        log(f"--- {key} (T={d['T']}, N={d['N']}, {d['ncirc']} circuits) "
            f"A/T = {d['A_mean']:.4f} nats/period, var/T = {d['A_var']:.4f}")
        for k, psi, tau, D in zip(d['k'], d['psi'], d['tau'], d['D']):
            log(f"    k={k:+.1f}  q={1-k:+.2f}  psi={psi:+.5f}  "
                f"tau={tau:+.5f}  D={D:+.4f}")
    log(f"written {OUT}/haar_smc_summary_v1.json")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['validate', 'produce', 'analyze'])
    ap.add_argument('--Ls', default=None)
    ap.add_argument('--ps', default=None)
    ap.add_argument('--ks', default=None)
    ap.add_argument('--N', type=int, default=0)
    ap.add_argument('--ncirc', type=int, default=0)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    {'validate': phase_validate, 'produce': phase_produce,
     'analyze': phase_analyze}[args.phase](args)
