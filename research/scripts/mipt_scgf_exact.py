"""mipt_scgf_exact.py -- exact annealed anchors for the record SCGF study (v16).

Closes the exact side of the theorem-level items:
  * Z_2(t) = E_omega[ sum_R p_R^2 ] = tr sigma(t): the two-replica (record-
    collision) partition function, evolved EXACTLY on the per-site algebra
    {e_0 (collided), e_+ (off-diag symmetric), e_- (antisymmetric)}^L.
  * P_{2,A}(t) = tr[ sigma(t) . S_A ]  (S_A = replica swap on region A):
    the annealed collision observable;  S~_2 = -log2( P_{2,A} / Z_2 ).
  * The SCGF anchor at beta = 1:   Xi(1; L, t) = ln Z_2(t) / (2Lt),
    and its t -> inf limit  ln lambda_1(L) / (2L)  (closed form, Kaufman lib).

Method (exact in the algebra representation, float64 arithmetic):
  State = coefficient vector over the 3^L product basis otimes_k e_{a_k}
  (digit 0 = e_0, 1 = e_+, 2 = e_-; site 0 = most significant base-3 digit).
  Layer maps:
    gate bond (i,j) (factorized twirl, exact on product elements):
        per-site (t, s) = (tr e_a, tr e_a S): e_0:(2,2), e_+:(1,1), e_-:(1,-1)
        alpha  = (4 t_i t_j - s_i s_j)/60,  beta = (4 s_i s_j - t_i t_j)/60
        alpha I + beta S = (a+b)(AA + BB) + (a-b)(AB + BA),
          A = e_0+e_+, B = e_-,  a+b = (t_i t_j + s_i s_j)/20,
          a-b = (t_i t_j - s_i s_j)/12.
    measurement layer (rate p): diagonal,
        c_a *= prod_k [ a_k = e_0 ? 1 : (1-p)^2 ].
  Initial state sigma_0 = |0..0><0..0|^{otimes 2}: the first M layer is inert
  (sigma_0 is computational-classical), and the first A layer maps it to
        otimes_{even bonds} [ (AA + BB)/10 ],
  whose trace is exactly 1 (verified below).
  Circuit order (the deposited simulator): one period = M, A (even bonds),
  M, B (odd bonds).

Observables (S e_a = eps_a e_a, eps = (+1, +1, -1)):
    Z_2(t)     = sum_a c_a prod_k t_{a_k}
    P_{2,A}(t) = sum_a c_a prod_k t_{a_k} prod_{k in A} eps_{a_k}

Calibration targets (deposited audit3_tiltchain.json, quoted in the logs):
  L=8,  t=4 periods (t = L/2), p=0.16:  Z_2 = 1.4796e-2,  S~_2 = 2.155 bits
  L=12, t=6 periods (t = L/2), p=0.16:  S~_2 = 3.128 bits
NOTE (v16 finding): the deposited numbers unambiguously correspond to t
 counted in PERIODS with t = L/2 -- the v15 manuscript's "t = 4L" for this
 chain is a mis-transcription of the deposit's convention.

New v16 computation (not from the deposit); deposited numbers are used only
as external calibration targets.
"""

import json
import sys
import time
import numpy as np

sys.path.insert(0, ".")
from mipt_kaufman_lib import log_lambda1

T_SITE = np.array([2.0, 1.0, 1.0])     # tr(e_a), d=2
S_SITE = np.array([2.0, 1.0, -1.0])    # tr(e_a S)


def bond_table():
    """K4[p, q, r, s]: coefficient of output digits (p, q) given input (r, s)."""
    K = np.zeros((3, 3, 3, 3))
    for di in range(3):
        for dj in range(3):
            apb = (T_SITE[di] * T_SITE[dj] + S_SITE[di] * S_SITE[dj]) / 20.0
            amb = (T_SITE[di] * T_SITE[dj] - S_SITE[di] * S_SITE[dj]) / 12.0
            if apb != 0.0:
                for a in (0, 1):
                    for b in (0, 1):
                        K[a, b, di, dj] += apb
                K[2, 2, di, dj] += apb
            if amb != 0.0:
                K[0, 2, di, dj] += amb
                K[1, 2, di, dj] += amb
                K[2, 0, di, dj] += amb
                K[2, 1, di, dj] += amb
    return K


K4 = bond_table()


def bond_apply(c, L, i, j):
    """Twirl on bond (i, j) (j = i+1, or the wrap pair (0, L-1))."""
    if i == 0 and j == L - 1:
        v = c.reshape(3, 3 ** (L - 2), 3)
        return np.einsum("pqrs,rms->pmq", K4, v, optimize=True).reshape(3 ** L)
    pre = 3 ** i
    mid = 3 ** (j - i - 1)
    post = 3 ** (L - 1 - j)
    v = c.reshape(pre, 3, mid, 3, post)
    return np.einsum("pqrs,armsb->apmqb", K4, v, optimize=True).reshape(3 ** L)


def meas_apply(c, L, p):
    """Collided measurement layer: sigma -> (1-p) sigma + p Pi sigma Pi per site.
    On the algebra: e_0 -> e_0, e_pm -> (1-p) e_pm (ONE factor: the measure /
    no-measure choice is a single event shared by both replicas)."""
    site_w = np.array([1.0, (1 - p), (1 - p)])
    cube = c.reshape((3,) * L)
    for k in range(L):
        bshape = [1] * L
        bshape[k] = 3
        cube = cube * site_w.reshape(bshape)
    return cube.reshape(3 ** L)


def init_state(L):
    """State after [inert M] + first A layer: otimes_{even bonds}(AA+BB)/10."""
    blk = np.array([[1.0, 1.0, 0.0],
                    [1.0, 1.0, 0.0],
                    [0.0, 0.0, 1.0]]) * 0.1
    c = blk
    for _ in range(L // 2 - 1):
        c = np.multiply.outer(c, blk)
    # c indexes as (bond0-di, bond0-dj, bond1-di, bond1-dj, ...) with bond k
    # covering sites (2k, 2k+1) -- this IS the site order. Reshape to 3^L:
    return c.reshape(3 ** L)


def obs_weights(L, A):
    wtr = np.ones((3,) * L)
    wA = np.ones((3,) * L)
    for k in range(L):
        bshape = [1] * L
        bshape[k] = 3
        wtr = wtr * T_SITE.reshape(bshape)
        eps = np.where(np.arange(3) < 2, 1.0, -1.0) if k in A else np.ones(3)
        wA = wA * (T_SITE * eps).reshape(bshape)
    return wtr.reshape(3 ** L), wA.reshape(3 ** L)


def evolve(L, p, tmax, A=None, log_every=8, quiet=False):
    if A is None:
        A = set(range(L // 2))
    wtr, wA = obs_weights(L, A)
    even = [(2 * k, 2 * k + 1) for k in range(L // 2)]
    odd = [(2 * k + 1, (2 * k + 2) % L) for k in range(L // 2)]
    # normalise the wrap bond to (0, L-1)
    odd = [(min(i, j), max(i, j)) if j < i else (i, j) for (i, j) in odd]

    Z2 = [1.0]
    P2A = [1.0]
    t0 = time.time()
    # period 1: [M inert] A M B
    c = init_state(L)
    c = meas_apply(c, L, p)
    for (i, j) in odd:
        c = bond_apply(c, L, i, j)
    Z2.append(float(c @ wtr))
    P2A.append(float(c @ wA))
    for t in range(2, tmax + 1):
        c = meas_apply(c, L, p)
        for (i, j) in even:
            c = bond_apply(c, L, i, j)
        c = meas_apply(c, L, p)
        for (i, j) in odd:
            c = bond_apply(c, L, i, j)
        Z2.append(float(c @ wtr))
        P2A.append(float(c @ wA))
        if not quiet and (t % log_every == 0 or t == tmax):
            s2t = -np.log2(max(P2A[t], 1e-300) / max(Z2[t], 1e-300))
            print(f"  L={L} p={p} t={t}: Z2={Z2[t]:.6e} S~2={s2t:.4f} "
                  f"({time.time()-t0:.1f}s)", flush=True)
    return Z2, P2A


def main():
    results = {"calibration": [], "anchors": [], "meta": {
        "script": "mipt_scgf_exact.py",
        "method": "exact per-site algebra evolution (3^L basis), float64",
        "order": "M A M B per period (deposited simulator order)",
    }}

    # bond table sanity: each column trace-preserving
    ok_all = True
    for di in range(3):
        for dj in range(3):
            tr_in = T_SITE[di] * T_SITE[dj]
            tr_out = sum(K4[a, b, di, dj] * T_SITE[a] * T_SITE[b]
                         for a in range(3) for b in range(3))
            if abs(tr_in - tr_out) > 1e-12:
                ok_all = False
                print(f"  TRACE FAIL ({di},{dj}): {tr_in} vs {tr_out}")
    print("bond table trace preservation:", "OK (all 9 columns)" if ok_all else "FAIL")

    # init state trace = 1 exactly
    for L in (4, 8):
        c = init_state(L)
        wtr, _ = obs_weights(L, set(range(L // 2)))
        print(f"init_state trace L={L}: {float(c @ wtr):.12f} (target 1)")

    # --- calibration against the deposited tilt chain: try several t values ---
    print("== Z2(t), S~2(t) tables for t-convention diagnosis (p=0.16) ==")
    for L in (8, 12):
        Z2, P2A = evolve(L, 0.16, 16, log_every=1, quiet=True)
        for t in (1, 2, 3, 4, 6, 8, 16):
            s2t = -np.log2(P2A[t] / Z2[t])
            print(f"  L={L} t={t:3d}: Z2={Z2[t]:.6e}  S~2={s2t:.4f}")
        results.setdefault("tables", []).append(
            {"L": L, "Z2": Z2, "S2tilde": [-np.log2(P2A[t] / Z2[t]) for t in range(len(Z2))]})

    for (L, t, p, z2_target, s2_target) in [
        (8, 4, 0.16, 1.4796e-2, 2.155),
        (12, 6, 0.16, None, 3.128),
    ]:
        print(f"== calibration L={L} t={t} p={p} "
              f"(deposit: Z2={z2_target}, S~2={s2_target}) ==", flush=True)
        Z2, P2A = evolve(L, p, t, log_every=max(4, t // 8))
        s2t = -np.log2(P2A[t] / Z2[t])
        rec = {"L": L, "t": t, "p": p, "Z2": Z2[t], "S2tilde": s2t,
               "deposit_Z2": z2_target, "deposit_S2tilde": s2_target,
               "Z2_rel_diff": (abs(Z2[t] - z2_target) / z2_target) if z2_target else None,
               "S2_diff": s2t - s2_target}
        results["calibration"].append(rec)
        print(f"  -> Z2 = {Z2[t]:.4e} (deposit {z2_target}); "
              f"S~2 = {s2t:.4f} (deposit {s2_target})")

    # --- p = 0.22 contrast point (L=8, t = L/2) ---
    Z2b, P2Ab = evolve(8, 0.22, 8, log_every=4)
    results["calibration"].append({
        "L": 8, "t": 8, "p": 0.22, "Z2": Z2b[8],
        "S2tilde": -np.log2(P2Ab[8] / Z2b[8]),
        "Z2_at_t4": Z2b[4], "S2tilde_at_t4": -np.log2(P2Ab[4] / Z2b[4])})

    # --- lambda1 anchors (t -> inf SCGF at beta = 1) ---
    print("== lambda_1 anchors (closed form) ==")
    for L in (8, 12, 16, 24, 32):
        for p in (0.16, 0.22):
            ll1 = float(log_lambda1(L // 2, 2, p))
            results["anchors"].append({
                "L": L, "p": p, "log_lambda1": ll1,
                "Xi1_inf_per_site": ll1 / (2 * L)})
            print(f"  L={L:3d} p={p}: ln l1 = {ll1:.6f}, "
                  f"Xi(1,inf) = {ll1/(2*L):.6e} nats/site")

    # --- Z2(t)/lambda1^t tail (L=8, p=0.16): compressibility check ---
    print("== Z2(t)/lambda1^t tail (L=8, p=0.16) ==")
    Z2, P2A = evolve(8, 0.16, 32, log_every=16, quiet=True)
    ll1 = float(log_lambda1(4, 2, 0.16))
    tail = [{"t": tt, "Z2": Z2[tt], "Z2_over_lambda1t": Z2[tt] / np.exp(ll1 * tt)}
            for tt in (8, 12, 16, 24, 32)]
    for r in tail:
        print(f"  t={r['t']}: Z2/l1^t = {r['Z2_over_lambda1t']:.6f}")
    results["z2_tail"] = {"L": 8, "p": 0.16, "log_lambda1": ll1, "tail": tail}

    with open("../results/scgf_exact.json", "w") as f:
        json.dump(results, f, indent=1)
    print("wrote ../results/scgf_exact.json")


if __name__ == "__main__":
    main()
