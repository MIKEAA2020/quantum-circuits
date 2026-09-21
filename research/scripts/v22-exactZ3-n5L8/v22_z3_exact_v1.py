"""v22_z3_exact_v1.py -- the exact Zbar_3 computation via the v17 operator,
closing Lambda(2) of the Clifford record-count disorder SCGF exactly.

The object (manuscript v21, Prop. prop:ess): Lambda_L(2) = (2Lt)^{-1} ln
E_omega[2^{-2 N_rand}] = (2Lt)^{-1} ln Zbar_3(t) at the production cells
(t = L/2 periods, d = 2, p in {0.16, 0.22}); the ESS-law exponent
Lambda(2) - 2 Lambda(1) = (2Lt)^{-1} [ln Zbar_3 - 2 ln Zbar_2] then closes
EXACTLY, replacing the trajectory estimates 0.0159 / 0.0080 / 0.0049
nats/site at L = 8/12/16.

Method (all on the compressed bond-label space (S_n)^{L/2}, the v17
operator C_comp = M1 M2 of Eq. (Wpn)):
  * boundary vectors: the initial state |0..0><0..0|^{(x)n} is
    computational-classical, so the first measurement layer is inert and
    the first gate layer projects it onto the bond span with per-bond
    coordinates y_sigma = sum_rho Wg_{d^2}(sigma^{-1} rho) * t_rho,
    t_rho = tr[U_rho^dag P_0^{(x)n}]^2 = 1  =>  c1 = wbar^{nb} . 1,
    wbar = sum_tau Wg_{d^2}(tau);
  * one period [M, A(even), M, B(odd)] maps coordinates by M2 (even->odd)
    then M1 (odd->even): after t periods the state is
    o_t = (M2 M1)^{t-1} M2 c1  (odd-bond coordinates);
  * the trace functional  Zbar_n(t) = tr sigma(t) = sum_tau o_t[tau]
    prod_b d^{2 c(tau_b)}  (tr[U_tau x U_tau] = d^{2c(tau)});
  * the layer parity (A-first vs B-first) is immaterial: translating the
    ring by one site exchanges the matchings and leaves the initial state,
    the trace and the measurement measure invariant -- verified numerically
    at L=8 (both orders agree to f64 rounding).

Phases:
  validate   exact Zbar_2 vs the deposited scgf_exact.json anchors
             (L=8 t=4 p=0.16: Z2 = 0.014796386937441494; L=12 t=6 p=0.16:
             3.8173099057181784e-05; L=8 t=4/t=8 p=0.22; the z2_tail
             Z2/lambda1^t -> 2.4512...) -- the boundary-convention anchor.
  z3         exact Zbar_3, Lambda(2), and the ESS exponent at the
             production cells (p=0.16: L=8,12,16,20; p=0.22: L=8,12,16).
  ladder     lambda_1^{(3)}(L,p) by power iteration on the same operator
             (validated at L=8 against the dense spectrum), the asymptotic
             Lambda(2)_inf = ln lambda_1/(2L) ladder, and the amplitudes
             A_3(L) = Zbar_3(t)/lambda_1^t (t-tail convergence).
"""
import sys, os, json, math, time, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'v19-n5L6-nofreeze'))
sys.path.insert(0, os.path.join(HERE, '..'))
from gap_utils import W_tensor, weingarten, perms, compose, inv, cycles
from ring_gemm_v2 import ring_m2_gemm, ring_m1_gemm
from mipt_kaufman_lib import log_lambda1

OUT = os.path.join(HERE, '..', '..', 'results', 'v22-exactZ3-n5L8')
LOG = os.path.join(HERE, '..', '..', 'logs', 'v22-exactZ3-n5L8')
os.makedirs(OUT, exist_ok=True)
os.makedirs(LOG, exist_ok=True)

_T_CACHE = {}


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------------------
def bond_factors(n, d, dtype=np.float64):
    """f[tau] = d^{2 c(tau)} (trace of U_tau x U_tau on one bond)."""
    P = perms(n)
    return np.array([float(d) ** (2 * cycles(t)) for t in P], dtype=dtype)


def trace_functional(n, d, nb, dtype=np.float64):
    """g[config] = prod_b d^{2c(tau_b)} on flat (S_n)^nb configs."""
    g = len(perms(n))
    f = bond_factors(n, d, dtype)
    N = g ** nb
    out = np.ones(N, dtype=dtype)
    c = np.arange(N, dtype=np.int64)
    for k in range(nb - 1, -1, -1):
        out *= f[c % g]
        c //= g
    return out


def initial_coords(n, d, nb, dtype=np.float64):
    """c1 = wbar^{nb} . 1 (per-bond coordinates of the projected |0..0> state)."""
    _, Ginv = weingarten(n, d * d)
    wbar = float(Ginv.sum()) / Ginv.shape[0]
    return np.full(len(perms(n)) ** nb, wbar ** nb, dtype=dtype), wbar


def half_period(v, W, nb, which, dtype=np.float64):
    if which == 'M2':
        return ring_m2_gemm(v, W, nb, dtype=dtype)
    return ring_m1_gemm(v, W, nb, dtype=dtype)


def zbar_exact(n, d, p, nb, t, dtype=np.float64, first='M2', beta=None):
    """Zbar_n(t periods) exactly:  o_t = (M2 M1)^{t-1} M2 c1, trace."""
    if beta is None:
        beta = 8 if nb <= 8 else 2
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    c1, wbar = initial_coords(n, d, nb, dtype)
    o = ring_m2_gemm(c1, W, nb, beta=beta, dtype=dtype)
    for _ in range(t - 1):
        e = ring_m1_gemm(o, W, nb, beta=beta, dtype=dtype)
        o = ring_m2_gemm(e, W, nb, beta=beta, dtype=dtype)
    gfun = trace_functional(n, d, nb, dtype)
    return float(gfun @ o), dict(wbar=wbar, N=g ** nb)


def lambda1_power(n, d, p, nb, iters=400, tol=1e-13, seed=0,
                  dtype=np.float64, v0=None):
    """Leading eigenvalue of C = M1 M2 by power iteration (Perron)."""
    P, idx, W = W_tensor(n, d, p)
    N = len(P) ** nb
    if v0 is None:
        rng = np.random.default_rng(seed)
        v = rng.random(N).astype(dtype) + 0.5
    else:
        v = np.asarray(v0, dtype=dtype)
    v /= np.linalg.norm(v)
    lam = 0.0
    for it in range(iters):
        w = ring_m1_gemm(ring_m2_gemm(v, W, nb, dtype=dtype), W, nb,
                         dtype=dtype)
        nw = np.linalg.norm(w)
        if nw < 1e-300:
            break
        w = w / nw
        lam_new = float(v @ w)
        if abs(lam_new - lam) < tol * max(abs(lam_new), 1e-300) and it > 20:
            lam = lam_new
            break
        v, lam = w, lam_new
    # one Rayleigh refinement on C (not the normalized iterate)
    w = ring_m1_gemm(ring_m2_gemm(v, W, nb, dtype=dtype), W, nb, dtype=dtype)
    lam = float((v @ w) / (v @ v))
    return lam, v


# ---------------------------------------------------------------------------
def phase_validate(args):
    log("== A: exact Zbar_2 via the compressed operator vs the deposited "
        "anchors (scgf_exact.json) ==")
    dep = json.load(open(os.path.join(HERE, '..', '..', 'results',
                                      'scgf_exact.json')))
    cal = dep['calibration']
    rows = []
    ok_all = True
    for c in cal:
        L, t, p = c['L'], c['t'], c['p']
        if c.get('Z2') is None:
            continue
        z2, meta = zbar_exact(2, 2, p, L // 2, t)
        rel = abs(z2 - c['Z2']) / c['Z2']
        ok = rel < 1e-9
        ok_all &= ok
        rows.append({'L': L, 't': t, 'p': p, 'Z2_ex': z2, 'Z2_dep': c['Z2'],
                     'rel': rel})
        log(f"   L={L} t={t} p={p}: Z2 = {z2:.12e} vs deposit "
            f"{c['Z2']:.12e}  rel {rel:.2e}  [{'OK' if ok else 'FAIL'}]")
    # z2_tail: Z2/lambda1^t -> A (Kaufman closed form lambda1)
    log("   z2_tail check (Z2/lambda1^t, lambda1 from the Kaufman lib):")
    tail = dep.get('z2_tail')
    if tail:
        L, p = tail['L'], tail['p']
        ll1 = math.exp(log_lambda1(L // 2, 2, p))
        for r in tail['tail'][:3]:
            z2, _ = zbar_exact(2, 2, p, L // 2, r['t'])
            rat = z2 / ll1 ** r['t']
            rel = abs(rat - r['Z2_over_lambda1t']) / r['Z2_over_lambda1t']
            ok = rel < 1e-9
            ok_all &= ok
            log(f"     t={r['t']}: Z2/lam1^t = {rat:.10f} vs deposit "
                f"{r['Z2_over_lambda1t']:.10f}  rel {rel:.2e}  "
                f"[{'OK' if ok else 'FAIL'}]")
    # layer-order invariance at L=8 (the parity check)
    za, _ = zbar_exact(2, 2, 0.16, 4, 4)
    zb, _ = zbar_exact(2, 2, 0.16, 4, 4, first='M1')
    rel = abs(za - zb) / za
    ok = rel < 1e-10
    ok_all &= ok
    log(f"   layer-parity invariance (A-first vs B-first, L=8 t=4): "
        f"{za:.12e} vs {zb:.12e} rel {rel:.2e}  [{'OK' if ok else 'FAIL'}]")
    json.dump({'rows': rows, 'ok': bool(ok_all)},
              open(f'{OUT}/v22_z3_validate.json', 'w'), indent=1)
    return ok_all


# ---------------------------------------------------------------------------
# production cells: the trajectory ladder (mipt_born_scgf.py, scgf_born.json)
# runs t = 4L periods (nsite = 2Lt = 512/1152/2048/4608 at L = 8/12/16/24),
# so the exact closure must use the SAME (L, t): t = 4L.
PROD = [(8, 0.16), (12, 0.16), (16, 0.16),
        (8, 0.22), (12, 0.22), (16, 0.22)]


def load_traj():
    sb = json.load(open(os.path.join(HERE, '..', '..', 'results',
                                     'scgf_born.json')))
    out = {}
    for r in sb['production']:
        out[(r['L'], r['p'])] = r
    return out


def phase_z3(args):
    log("== B: exact Zbar_3 at the production cells (t = 4L, the "
        "trajectory-ladder convention) ==")
    traj = load_traj()
    ckpt = f'{OUT}/v22_z3_exact.json'
    rows = json.load(open(ckpt)) if os.path.exists(ckpt) else []
    done = {(r['L'], r['p']) for r in rows}
    for L, p in PROD:
        if (L, p) in done:
            continue
        nb, t = L // 2, 4 * L
        t0 = time.time()
        z3, m3 = zbar_exact(3, 2, p, nb, t)
        z2, m2 = zbar_exact(2, 2, p, nb, t)
        lam1 = (math.log(z2)) / (2 * L * t)
        lam2 = (math.log(z3)) / (2 * L * t)
        expo = (math.log(z3) - 2 * math.log(z2)) / (2 * L * t)
        row = {'L': L, 'p': p, 't': t, 'Z3': z3, 'Z2': z2,
               'Lambda1': lam1, 'Lambda2': lam2, 'ess_exponent': expo,
               'secs': round(time.time() - t0, 1)}
        tr = traj.get((L, p))
        if tr is not None:
            row['traj_Xi1'] = tr['Xi_1.0']
            row['traj_Xi2'] = tr['Xi_2.0']
            row['traj_exponent'] = (tr['Xi_2.0'] - 2 * tr['Xi_1.0']
                                    if np.isfinite(tr['Xi_2.0']) else None)
            row['traj_ESS_beta1'] = tr['ESS_beta1']
            row['traj_xbar'] = tr['xbar']
            # the v21 gap closure sanity: g = Lambda(1) + log2 * xbar_traj
            row['gap_closure'] = lam1 + math.log(2) * tr['xbar']
        rows.append(row)
        json.dump(rows, open(ckpt, 'w'), indent=1)
        log(f"   L={L:2d} p={p} t={t}: Z3 = {z3:.12e}  "
            f"Lambda(1) = {lam1:.6f}  Lambda(2) = {lam2:.6f}  "
            f"exponent = {expo:.6f}")
        if tr is not None:
            log(f"        traj: Xi1 {tr['Xi_1.0']:.6f}  Xi2 "
                f"{tr['Xi_2.0']:.6f}  exponent "
                f"{row['traj_exponent'] if row['traj_exponent'] is not None else 'collapsed(-inf)'}"
                f"  ESS(beta1) {tr['ESS_beta1']:.2f}"
                + (f"  gap-closure {row['gap_closure']:.4f}"
                   if 'gap_closure' in row else ""))
    log(f"   written {ckpt}")


def phase_ladder(args):
    log("== C: lambda_1^{(3)} ladders + amplitudes A_3(L) ==")
    rows = []
    ckpt = f'{OUT}/v22_z3_ladder.json'
    if os.path.exists(ckpt):
        rows = json.load(open(ckpt))
    done = {(r['L'], r['p']) for r in rows}
    # dense cross-check at L=8
    P, idx, W = W_tensor(3, 2, 0.16)
    from gap_utils import build_M
    M1 = build_M(W, 4, 6, 'M1')
    M2 = build_M(W, 4, 6, 'M2')
    ev = np.linalg.eigvals(M1 @ M2)
    ev = np.sort(np.real(ev[np.abs(np.imag(ev)) < 1e-9]))[::-1]
    lam_dense = float(ev[0])
    lam_pi, _ = lambda1_power(3, 2, 0.16, 4)
    log(f"   L=8 p=0.16 n=3 lambda1: dense {lam_dense:.12f} vs power "
        f"{lam_pi:.12f} (rel {abs(lam_pi-lam_dense)/lam_dense:.2e})")
    for p in (0.16, 0.22):
        for L in (8, 12, 16):
            if (L, p) in done:
                continue
            nb = L // 2
            t0 = time.time()
            lam, v0 = lambda1_power(3, 2, p, nb)
            # amplitude tail: Z3(t)/lam^t at t = L, 2L, 4L (production t = 4L)
            amps = {}
            for tt in sorted({L, 2 * L, 4 * L}):
                z3, _ = zbar_exact(3, 2, p, nb, tt)
                amps[tt] = z3 / lam ** tt
            rows.append({'n': 3, 'L': L, 'p': p, 'lam1': lam,
                         'lam1_per_2L': math.log(lam) / (2 * L),
                         'A3': amps, 'secs': round(time.time() - t0, 1)})
            json.dump(rows, open(ckpt, 'w'), indent=1)
            log(f"   n=3 L={L:2d} p={p}: lam1 = {lam:.10f}  "
                f"ln lam1/(2L) = {math.log(lam)/(2*L):.6f}  "
                f"A3(t) = "
                f"{ {k: round(v, 4) for k, v in amps.items()} }  "
                f"[{rows[-1]['secs']}s]")
    json.dump(rows, open(f'{OUT}/v22_z3_ladder.json', 'w'), indent=1)
    log(f"   written {OUT}/v22_z3_ladder.json")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['validate', 'z3', 'ladder', 'all'])
    args = ap.parse_args()
    t0 = time.time()
    ok = True
    if args.phase in ('validate', 'all'):
        ok = phase_validate(args)
    if args.phase in ('z3', 'all') and ok:
        phase_z3(args)
    if args.phase in ('ladder', 'all') and ok:
        phase_ladder(args)
    if not ok:
        log("VALIDATION FAILED -- Z3 phases skipped")
        sys.exit(1)
    log(f"total {time.time()-t0:.1f}s")
