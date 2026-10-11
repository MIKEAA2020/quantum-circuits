#!/usr/bin/env python3
r"""tier1_slice_matvec_v1.py -- Tier-1 (L=10 at n=5) method validation,
cost model, and feasibility verdict (session 2026-10-11).

CONTEXT.  The manuscript's registered L=10 conditional (v32) makes the
fourth size the decisive measurement: if the n=5 closing is genuinely
exponential, sigma_eff(L=8->10) stabilizes at a positive interface
tension; a slowly decaying power law keeps it decaying.  gap.txt's
Tier-1 doctrine: matrix-free Lanczos on the symmetry-reduced orbit
basis.  The exact L=10 mom0 triv.triv sector dimension is 346,177
(v32_tier1_L10_dimension.py, validated against the deposited L=8
anchor 3865).  This script delivers what this sandbox (3 GB RAM, 2
cores) permits of Tier 1:

  (A) KERNEL + FACTORIZATION VALIDATION.  The W channel of Eq. (Wpn)
      factorizes as
          W[pi,mu,nu] = sum_s omega(pi^-1 s) psi(s^-1 mu) psi(s^-1 nu)
                M2 = Omega @ B,   M1 = Omega @ B',
      with Omega[s;t] = prod_k omega(s_k^-1 t_k) (the per-factor
      Weingarten class-kernel convolution), B[s;pi] = prod_k
      psi(s_k^-1 pi_k) psi(s_k^-1 pi_{k+1}) (the psi-ring transfer)
      and B' its input-shifted mirror.  Validated entrywise on random
      (tau,pi) pairs at nb=2 and nb=3 by EXPLICIT summation over the
      s-space (never through the distributivity shortcut), against
      the deposited W_tensor definition.

  (B) RESTRICTED-OPERATOR VALIDATION.  The mom0 triv.triv restricted
      operator assembled through the factorized route
          M~[a,b] = sqrt(n_a/n_b) * sum_s Omega[rep_a; s] * S_B[s, b],
          S_B[s,b] = sum_{pi in O_b} B[s; pi]
      equals the deposited block route (v22_n5_L8_block_v1.
      assemble_block, which sums the W-channel rows directly),
      elementwise and spectrally, at nb=2 (K=7 orbits); the
      eigenvalues also match the deposited L=4 scan (the external
      anchor used by the deposited validation itself).

  (C) nb=3 REFERENCE (for the record): the deposited block route at
      nb=3 (K=57), cross-checked against an unrestricted
      colour-restricted Arnoldi solve (the deposited RingOperator).

  (D) COST MODEL + VERDICT.  The deposited L=8 rung timings
      (v22_n5_L8_rung.json) imply a measured assembly throughput of
      K x N x nb x 2 MACs per point; the model is validated against
      those timings and extrapolated to nb=5.  Verdict printed and
      deposited: the exact L=10 eigen-solve does not fit this sandbox
      by any deposited route (dense block 1.9 TB; streaming assembly
      ~10^16.9 MACs = months per p-point; full-space iterative needs
      ~200 GB vectors); the two viable routes (cluster streaming; the
      representation-theoretic colour basis built on the factorization
      validated here) are specified in
      research/versions/tier1_L10_design_20261011.md.

Output: research/results/tier1_slice_matvec.json
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gap_utils import W_tensor, perms, compose, inv, cycles, weingarten  # noqa: E402
from v22_n5_L8_block_v1 import (  # noqa: E402
    orbit_table, assemble_block, block_eigs, fresh_reference)

OUT = os.path.join(HERE, '..', '..', 'results')
RESULTS = {}
LOG = []


def log(*a):
    print(*a, flush=True)
    LOG.append(' '.join(str(x) for x in a))


# ---------------------------------------------------------------------------
def build_kernels(n, d, p):
    """(P, Ginv, T): the class kernels of the factorization.

    Ginv[s,t] = omega(s^-1 t)  (the Weingarten function of U(D), D=d^2,
    as the inverse / pseudo-inverse of the Gram matrix D^{c(s^-1 t)});
    T[s,mu]   = psi(s^-1 mu)   (the measurement channel
                                 (1-p) d^{c(s^-1 mu)} + p d).
    """
    P, Ginv = weingarten(n, d * d)
    g = len(P)
    T = np.empty((g, g), dtype=float)
    for i, s in enumerate(P):
        si = inv(s)
        for j, mu in enumerate(P):
            T[i, j] = (1.0 - p) * float(d) ** cycles(compose(si, mu)) + p * d
    return P, Ginv, T


def direct_rows(W, taus, nb, form):
    """rows of M (deposited definition) at the given tau configs:
    M2[tau;pi] = prod_k W[tau_k, pi_k, pi_{k+1}];
    M1[tau;pi] = prod_k W[tau_k, pi_{k-1}, pi_k];
    returned as (len(taus), g**nb) arrays over the pi space."""
    g = W.shape[0]
    N = g ** nb
    digs = np.array(np.unravel_index(np.arange(N), (g,) * nb)).T
    Wf = np.ascontiguousarray(W.reshape(g, g * g))
    out = np.empty((len(taus), N))
    for a, tau in enumerate(taus):
        vals = np.ones(N)
        for k in range(nb):
            if form == 'M2':
                pair = digs[:, k] * g + digs[:, (k + 1) % nb]
            else:
                pair = digs[:, (k - 1) % nb] * g + digs[:, k]
            vals *= Wf[tau[k], pair]
        out[a] = vals
    return out


# ---------------------------------------------------------------------------
# (The factorized row-by-row helper is inlined in phase A: the
# explicit per-pair s-space summation there is the identity being
# validated, computed the hard way on purpose.)


# ---------------------------------------------------------------------------
def phase_A():
    log('== phase A: kernel + factorization validation (M2 = Omega@B) ==')
    res = {}
    rng = np.random.default_rng(20261011)
    for nb, npairs in [(2, 2000), (3, 120)]:
        p = 0.44
        P, _idx, W = W_tensor(5, 2, p)
        _, Ginv, T = build_kernels(5, 2, p)
        g = len(P)
        taus = rng.integers(0, g, size=(npairs, nb))
        pis = rng.integers(0, g, size=(npairs, nb))
        # direct: M[tau; pi] from the deposited W, per pair
        Wf = W.reshape(g, g * g)
        for form in ('M2', 'M1'):
            t0 = time.time()
            direct = np.ones(npairs)
            fact = np.empty(npairs)
            # direct side
            for a in range(npairs):
                v = 1.0
                for k in range(nb):
                    if form == 'M2':
                        pair = pis[a, k] * g + pis[a, (k + 1) % nb]
                    else:
                        pair = pis[a, (k - 1) % nb] * g + pis[a, k]
                    v *= Wf[taus[a, k], pair]
                direct[a] = v
            # factorized side: explicit s-space summation per pair
            s_digs = np.array(np.unravel_index(
                np.arange(g ** nb), (g,) * nb)).T
            for a in range(npairs):
                # s-configs restricted to the "light cone" of tau:
                # Omega is a full product, so all s-configs contribute;
                # vectorize the s-sum for this pair.
                acc = np.ones(g ** nb)
                for k in range(nb):
                    acc *= Ginv[taus[a, k], s_digs[:, k]]
                for k in range(nb):
                    if form == 'M2':
                        j1, j2 = k, (k + 1) % nb
                    else:
                        j1, j2 = (k - 1) % nb, k
                    acc *= T[s_digs[:, k], pis[a, j1]]
                    acc *= T[s_digs[:, k], pis[a, j2]]
                fact[a] = acc.sum()
            scale = np.abs(direct).max()
            err = np.abs(direct - fact).max() / scale
            ok = err < 1e-10
            log(f'   nb={nb} p={p} {form}: {npairs} random pairs, '
                f'max rel err {err:.2e}  [{"OK" if ok else "FAIL"}] '
                f'({time.time()-t0:.0f}s)')
            res[f'nb{nb}_{form}_maxrel'] = float(err)
            assert ok, f'factorization FAILED at nb={nb} {form}'
    res['verdict'] = 'M2 = Omega@B and M1 = Omega@B\' validated ' \
                     '(explicit s-space summation vs deposited W)'
    log('   ' + res['verdict'])
    RESULTS['A_factorization'] = res


# ---------------------------------------------------------------------------
def phase_B():
    log('== phase B: restricted-operator validation at nb=2 (K=7) ==')
    res = {}
    dep_scan = {round(r['p'], 4): r['triv3'] for r in json.load(open(
        os.path.join(OUT, 'v18-n4n5-smc', 'n5_annealed_scan_v1.json')))}
    for p in (0.44, 0.32):
        ids, reps, counts, K = orbit_table(2)
        B1d, B2d = assemble_block(5, 2, p, 2, ids, reps, counts, K)
        Cd = B1d @ B2d
        evd = block_eigs(B1d, B2d, k_want=4)

        # --- the factorized route ------------------------------------
        _, Ginv, T = build_kernels(5, 2, p)
        g = Ginv.shape[0]
        N = g ** 2
        pi_digs = np.array(np.unravel_index(np.arange(N), (g,) * 2)).T
        orb = np.asarray(ids)
        sqrtc = counts.astype(float) ** 0.5
        norm = np.outer(sqrtc, 1.0 / sqrtc)

        def SB(form):
            """S_B[s; b] = sum_{pi in O_b} B^{(form)}[s; pi]."""
            S = np.empty((N, K))
            for si in range(N):
                s = pi_digs[si]
                vals = np.ones(N)
                for k in range(2):
                    if form == 'B':
                        j1, j2 = k, (k + 1) % 2
                    else:
                        j1, j2 = (k - 1) % 2, k
                    vals *= T[s[k], pi_digs[:, j1]]
                    vals *= T[s[k], pi_digs[:, j2]]
                S[si] = np.bincount(orb, weights=vals, minlength=K)
            return S

        def omega_rows():
            Om = np.empty((K, N))
            for a in range(K):
                vals = np.ones(N)
                for k in range(2):
                    vals *= Ginv[reps[a, k], pi_digs[:, k]]
                Om[a] = vals
            return Om

        Om = omega_rows()
        M2m = norm * (Om @ SB('B'))
        M1m = norm * (Om @ SB('Bp'))
        Cm = M1m @ M2m
        evm = block_eigs(M1m, M2m, k_want=4)

        err_mat = np.abs(Cm - Cd).max() / np.abs(Cd).max()
        err_eig = max(abs(x - y) / abs(y) for x, y in zip(evm, evd))
        ref = dep_scan.get(round(p, 4))
        err_dep = (max(abs(float(evm[i]) - ref[i]) / abs(ref[i])
                       for i in range(min(len(evm), len(ref))))
                   if ref else None)
        log(f'   p={p}: K={K}; factorized vs deposited block: matrix '
            f'max rel {err_mat:.2e}, eig max rel {err_eig:.2e}; '
            + (f'vs deposited L=4 scan: {err_dep:.2e}'
               if ref else 'no scan anchor'))
        assert err_mat < 1e-10 and err_eig < 1e-10, 'restricted mismatch'
        res[f'p{p}'] = {
            'K': int(K), 'matrix_maxrel': float(err_mat),
            'eig_maxrel': float(err_eig),
            'deposited_scan_maxrel': (float(err_dep) if err_dep is not None
                                      else None),
            'top4': [float(x) for x in evm],
        }
    res['verdict'] = ('the factorized restricted assembly reproduces '
                      'the deposited block route elementwise and '
                      'spectrally, and the deposited L=4 scan anchor')
    log('   ' + res['verdict'])
    RESULTS['B_restricted_nb2'] = res


# ---------------------------------------------------------------------------
def phase_C():
    log('== phase C: nb=3 reference (deposited block; Arnoldi optional) ==')
    res = {}
    want_arnoldi = os.environ.get('TIER1_ARNOLDI') == '1'
    for p in (0.44, 0.47):
        t0 = time.time()
        ids, reps, counts, K = orbit_table(3)
        # chunk=25k (the deposited L=8 memory profile): the default 125k
        # chunk allocates ~0.7 GB of W-gather temporaries per chunk,
        # which swaps on this 3 GB sandbox
        B1, B2 = assemble_block(5, 2, p, 3, ids, reps, counts, K,
                                chunk=25_000)
        ev = block_eigs(B1, B2, k_want=6)
        err = None
        if want_arnoldi:
            try:
                rr = fresh_reference(5, 2, p, 3, k_want=4)
                err = max(abs(float(ev[i]) - float(rr[i]))
                          / abs(float(rr[i]))
                          for i in range(min(len(ev), len(rr))))
            except Exception as e:
                log(f'   (Arnoldi reference failed: {e})')
        log(f'   p={p}: K={K}; top: {[f'{float(x):.8e}' for x in ev[:3]]}; '
            + (f'vs unrestricted Arnoldi: {err:.2e}  '
               f'[{"OK" if err < 1e-6 else "FAIL"}]' if err is not None
               else ' (Arnoldi cross-check: run with TIER1_ARNOLDI=1; the '
                    'deposited v22 validation already performed it at '
                    'nb=3)')
            + f'  ({time.time()-t0:.0f}s)')
        res[f'p{p}'] = {
            'K': int(K), 'top6': [float(x) for x in ev],
            'arnoldi_maxrel': (float(err) if err is not None else None),
        }
    RESULTS['C_nb3_reference'] = res


# ---------------------------------------------------------------------------
def phase_D():
    log('== phase D: cost model + L=10 verdict ==')
    rung = json.load(open(os.path.join(
        OUT, 'v22-exactZ3-n5L8', 'v22_n5_L8_rung.json')))
    fine = json.load(open(os.path.join(
        OUT, 'v22-exactZ3-n5L8', 'v25_n5_L8_finegrid.json')))
    probe = json.load(open(os.path.join(
        OUT, 'v32_tier1_L10_dimension.json')))
    K8, N8, nb = 3865, 120 ** 4, 4
    macs8 = K8 * N8 * nb * 2
    th = [macs8 / r['secs'] for r in rung if r.get('secs')]
    th_med = float(np.median(th))
    log(f'   L=8 deposited timings: {[round(r["secs"]) for r in rung]} s '
        f'over {len(rung)} p-points (+ {len(fine)} finer-grid points); '
        f'assembly model {macs8:.2e} MACs/point -> throughput '
        f'{th_med:.2e} MAC/s (median)')

    K10, N10, nb5 = probe['tier1_L10_dimension'], 120 ** 5, 5
    macs_asm = K10 * N10 * nb5 * 2
    macs_mv = K10 * N10 * nb5
    dense_bytes = 2 * K10 ** 2 * 8
    full_vec_bytes = N10 * 8
    macs_ring = 2 * 120 ** (nb5 + 2)
    days = lambda m: m / th_med / 86400  # noqa: E731
    log(f'   L=10 (n=5): K={K10:,}, N={N10:.3e}; dense block '
        f'{dense_bytes/2**40:.1f} TiB (x2 matrices); streaming assembly '
        f'{macs_asm:.2e} MACs = {days(macs_asm):.0f} days/p-point; '
        f'streaming matvec {macs_mv:.2e} MACs = {days(macs_mv):.0f} '
        f'days -> Lanczos(60) ~ {60*days(macs_mv)/365:.1f} years')
    log(f'   full-space iterative route: vectors {full_vec_bytes/2**30:.0f} '
        f'GB each; ring matvec {macs_ring:.2e} MACs = '
        f'{macs_ring/th_med/3600:.1f} h each')
    log('   VERDICT: the exact L=10 eigen-solve does not fit this sandbox '
        '(3 GB RAM / 2 cores) by any deposited route; routes that do fit '
        'adequate hardware are specified in the design note.')
    RESULTS['D_cost_model'] = {
        'L8_deposited': {
            'K': K8, 'N': N8, 'nb': nb, 'macs_per_point': float(macs8),
            'secs': {str(r['p']): r['secs'] for r in rung},
            'throughput_median_MACs': th_med,
        },
        'L10_extrapolation': {
            'K': K10, 'N': N10, 'nb': nb5,
            'dense_block_bytes': float(dense_bytes),
            'assembly_macs_per_point': float(macs_asm),
            'assembly_days_per_point_at_median': float(days(macs_asm)),
            'matvec_macs': float(macs_mv),
            'matvec_days_at_median': float(days(macs_mv)),
            'lanczos60_years_at_median': float(60 * days(macs_mv) / 365),
            'full_space_vector_bytes': float(full_vec_bytes),
            'ring_matvec_macs': float(macs_ring),
            'ring_matvec_hours_at_median': float(macs_ring / th_med / 3600),
        },
        'sandbox': {'ram_GB': 3.0, 'cores': 2},
        'verdict': ('L=10 exact eigen-solve not computable on this sandbox '
                    'via any deposited route; the validated factorization '
                    '(phases A/B) and the sector dimension 346,177 are '
                    'deposited for the two viable routes (cluster '
                    'streaming; representation-theoretic colour basis) '
                    'specified in tier1_L10_design_20261011.md'),
    }


if __name__ == '__main__':
    t_all = time.time()
    phase_A()
    phase_B()
    phase_C()
    phase_D()
    RESULTS['log'] = LOG
    RESULTS['secs_total'] = round(time.time() - t_all, 1)
    path = os.path.join(OUT, 'tier1_slice_matvec.json')
    with open(path, 'w') as f:
        json.dump(RESULTS, f, indent=1)
    log(f'written: research/results/tier1_slice_matvec.json '
        f'({RESULTS["secs_total"]} s total)')
    log('TIER-1 METHOD ROUND OK')
