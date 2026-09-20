"""GEMM-structured ring transfer v1 (pure numpy + BLAS).

The v1 numpy ring_M2 costs 121 s/matvec at n=5 nb=3 (N=1.7e6) because of
~4 cache-hostile strided 110 MB transpose-copies per chunk; the contraction
itself is only ~2 g^5 MACs.  This module performs the SAME contraction
(validated) with ONE strided copy per step and BLAS-3 batched GEMMs whose
output layouts are consumed directly by the next stage:

  per carry-chunk (a0:a1, size b):
    lift : T[b, tau0, pi_1..] = W[tau0, a, pi_1] * v[a, pi_1..]   (broadcast)
    step : Tp = T/X transposed to (pi_{k+1}, M, pi_k)      [ONE strided copy]
           R  = matmul(Tp, Wk) -> (pi_{k+1}, M, tau_k)      [batched GEMM]
           X  = R reshaped    -> (pi_{k+1}, b, taus.., pis.., tau_k)
    final: per a: out[head, tau_last] += X[:, a, :].T @ W[:, :, a].T  (GEMMs;
           only small per-a panels are contiguous-ified by matmul)

Mathematical operation IDENTICAL to n45_annealed_lib_v1.ring_M2:
  (M2 v)[tau_0..tau_{nb-1}] = sum_pi prod_k W[tau_k, pi_k, pi_{k+1}] v[pi..]
  lift  W[tau_0, a, pi_1]; step k W[tau_k, pi_k, pi_{k+1}]; final
  W[tau_{nb-1}, pi_{nb-1}, a];  a = pi_0 blocked in chunks of beta.
"""
import numpy as np


def ring_m2_gemm(v_flat, W, nb, beta=8, dtype=np.float64):
    W = np.ascontiguousarray(np.asarray(W), dtype=dtype)
    Wk = np.ascontiguousarray(W.transpose(2, 1, 0), dtype=dtype)
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
    for a0 in range(0, g, beta):
        a1 = min(a0 + beta, g)
        b = a1 - a0
        vb = vt[a0:a1]                                    # (b, pi_1..) contig
        Kl = np.ascontiguousarray(W[:, a0:a1, :].transpose(1, 0, 2))
        T = (Kl.reshape((b, g, g) + (1,) * (nb - 2))
             * vb.reshape((b, 1) + (g,) * (nb - 1)))      # (b, tau0, pi_1..)
        if nb == 2:
            # final directly on T-layout: out[tau0, tau1] += T[j] @ W[:,:,a].T
            for j in range(b):
                oj = np.matmul(T[j], W[:, :, a0 + j].T)
                outr += oj
            continue
        # ---- steps k = 1 .. nb-2
        X = T
        from_T = True        # X is in lift layout (b, tau0, pi_1..pi_{nb-1})
        for k in range(1, nb - 1):
            if from_T:
                # T axes: [0]=b, [1]=tau_0, [2..nb]=pi_1..pi_{nb-1}
                # Tp = (pi_{k+1}, b, tau_0..tau_{k-1}, pi_{k+2}.., pi_k)
                order = [k + 2] + [0] + list(range(1, k + 1)) + \
                    list(range(k + 3, nb + 1)) + [k + 1]
            else:
                # X axes: [0]=pi_k, [1]=b, [2..k]=tau_0..tau_{k-2},
                #         [k+1..nb-1]=pi_{k+1}.., [nb]=tau_{k-1}
                # Tp = (pi_{k+1}, b, tau_0..tau_{k-1}, pi_{k+2}.., pi_k)
                order = [k + 1] + [1] + list(range(2, k + 1)) + [nb] + \
                    list(range(k + 2, nb)) + [0]
            Tp = np.ascontiguousarray(X.transpose(tuple(order)))
            pish = Tp.shape
            M = int(np.prod(pish[1:-1]))
            Tp = Tp.reshape((pish[0], M, pish[-1]))
            R = np.matmul(Tp, Wk)                          # (pi_{k+1}, M, tau_k)
            X = R.reshape((pish[0],) + pish[1:-1] + (g,))  # X_k layout
            from_T = False
        # ---- final: X axes (pi_{nb-1}, b, head..., ) with head = tau_0..tau_{nb-2}
        # X = (pi, b, tau_0..tau_{nb-3}, tau_{nb-2})  [head ravel = tau_0..tau_{nb-2}]
        Ghead = g ** (nb - 1)
        for j in range(b):
            Xa = X[:, j, :].reshape(g, Ghead)              # (pi, head) strided
            Wa = W[:, :, a0 + j].T                         # (pi, tau_last) view
            oj = np.matmul(Xa.T, Wa)                       # (head, tau_last)
            outr += oj
    return out


def ring_m1_gemm(v_flat, W, nb, beta=8, dtype=np.float64):
    """M1 v = moveaxis(ring_M2(v), -1, 0)  (the validated v1 identity)."""
    X = ring_m2_gemm(v_flat, W, nb, beta=beta, dtype=dtype)
    g = W.shape[0]
    return np.ascontiguousarray(
        X.reshape((g,) * nb).transpose(tuple([nb - 1] + list(range(nb - 1))))
    ).reshape(-1)
