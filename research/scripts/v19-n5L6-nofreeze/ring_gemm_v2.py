"""GEMM-structured ring transfer v2 (pure numpy + BLAS).

v1 of this module: 33 s/M2 at n=5 nb=3 — profiled: the final contraction
took 4.2 s/chunk because X[:, j, :] (middle-axis slice) forces a
stride-b gather copy.  v2 restructures every stage so that
  * the lift broadcasts DIRECTLY into the step-1 layout (b, pi_2.., tau_0, pi_1)
    (no strided copy at nb=3 at all),
  * each step GEMM batches over (b, pi_{k+1}) leading axes, so its output is
    naturally (b, pi_{k+1}, M, tau_k) — the final slices the LEADING b axis
    (contiguous views only),
  * only nb>=4 intermediate steps need one strided transpose each.

Mathematical operation IDENTICAL to n45_annealed_lib_v1.ring_M2 (validated):
  (M2 v)[tau_0..tau_{nb-1}] = sum_pi prod_k W[tau_k, pi_k, pi_{k+1}] v[pi..]
  lift  W[tau_0, a, pi_1]; step k W[tau_k, pi_k, pi_{k+1}]; final
  W[tau_{nb-1}, pi_{nb-1}, a];  a = pi_0 blocked in chunks of beta.
"""
import numpy as np


def ring_m2_gemm(v_flat, W, nb, beta=8, dtype=np.float64):
    W = np.ascontiguousarray(np.asarray(W), dtype=dtype)
    Wk = np.ascontiguousarray(W.transpose(2, 1, 0), dtype=dtype)  # (pi',pi,tau)
    g = W.shape[0]
    N = g ** nb
    v = np.ascontiguousarray(np.asarray(v_flat), dtype=dtype)
    if v.size != N:
        raise ValueError("bad v size")
    if nb == 1:
        Wd = W[:, np.arange(g), np.arange(g)]
        return Wd @ v
    vt = v.reshape((g,) * nb)
    out = np.zeros(N, dtype=dtype)
    outr = out.reshape(g ** (nb - 1), g)
    Ghead = g ** (nb - 1)
    for a0 in range(0, g, beta):
        a1 = min(a0 + beta, g)
        b = a1 - a0
        vb = vt[a0:a1]                       # (b, pi_1..pi_{nb-1}) contiguous
        Kl = np.ascontiguousarray(W[:, a0:a1, :].transpose(1, 0, 2))
        if nb == 2:
            # T[b, tau_0, pi_1] = Kl * vb ; final GEMMs consume T[j] directly
            T = Kl * vb[:, None, :]             # (b, tau0, pi1)
            for j in range(b):
                Waj = np.ascontiguousarray(W[:, :, a0 + j].T)   # (pi1, tau1)
                oj = np.matmul(T[j], Waj)                       # (tau0, tau1)
                outr += oj
            continue
        # ---- lift straight into step-1 layout: (b, pi_2..pi_{nb-1}, tau_0, pi_1)
        vb2 = vb.transpose([0] + list(range(2, nb)) + [1])   # view (b, pi_2.., pi_1)
        vb3 = np.expand_dims(vb2, -2)                        # view (b, pi_2.., 1, pi_1)
        Kl2 = Kl.reshape((b,) + (1,) * (nb - 2) + (g, g))   # (b, 1..1, tau0, pi_1)
        T = Kl2 * vb3                                        # (b, pi_2.., tau0, pi_1) fresh
        # T axes: [0]=b, [1..nb-2]=pi_2..pi_{nb-1}, [nb-1]=tau_0, [nb]=pi_1
        # ---- steps k = 1 .. nb-2
        X = T
        from_lift = True
        for k in range(1, nb - 1):
            if from_lift:
                # T axes: [0]=b, [1..nb-2]=pi_2..pi_{nb-1}, [nb-1]=tau_0, [nb]=pi_1
                # Tp' = (b, pi_2, tau_0, pi_3..pi_{nb-1}, pi_1)   [k=1 only]
                order = [0] + [1] + [nb - 1] + list(range(2, nb - 1)) + [nb]
            else:
                # X axes: [0]=b, [1]=pi_{k}, [2..k]=tau_0..tau_{k-2},
                #         [k+1..nb-1]=pi_{k+1}..pi_{nb-1}, [nb]=tau_{k-1}
                # Tp' = (b, pi_{k+1}, tau_0..tau_{k-1}, pi_{k+2}.., pi_k)
                order = [0] + [k + 1] + list(range(2, k + 1)) + [nb] + \
                    list(range(k + 2, nb)) + [1]
            Tp = np.ascontiguousarray(X.transpose(tuple(order)))
            pish = Tp.shape                       # (b, pi_{k+1}, M..., pi_k)
            M = int(np.prod(pish[2:-1]))
            Tp = Tp.reshape((b, g, M, g))
            R = np.matmul(Tp, Wk.reshape((1, g, g, g)))   # (b, pi_{k+1}, M, tau_k)
            X = R.reshape((b, g) + pish[2:-1] + (g,))     # X_k layout
            from_lift = False
        # ---- final: X axes (b, pi_{nb-1}, tau_0..tau_{nb-2})  [head = tau_0..tau_{nb-2}]
        # NOTE: W[:, :, a].T is a strided view that knocks numpy off the BLAS
        # fast path (measured 1.6 vs 64 GFLOPS); make the small panels
        # contiguous explicitly.
        for j in range(b):
            Xj = X[j].reshape(g, Ghead)           # (pi, head) contiguous view
            Waj = np.ascontiguousarray(W[:, :, a0 + j].T)   # (pi, tau_last)
            oj = np.matmul(Xj.T, Waj)             # (head, tau_last) BLAS fast
            outr += oj
    return out


def ring_m1_gemm(v_flat, W, nb, beta=8, dtype=np.float64):
    """M1 v = moveaxis(ring_M2(v), -1, 0)  (the validated v1 identity)."""
    X = ring_m2_gemm(v_flat, W, nb, beta=beta, dtype=dtype)
    g = W.shape[0]
    return np.ascontiguousarray(
        X.reshape((g,) * nb).transpose(tuple([nb - 1] + list(range(nb - 1))))
    ).reshape(-1)
