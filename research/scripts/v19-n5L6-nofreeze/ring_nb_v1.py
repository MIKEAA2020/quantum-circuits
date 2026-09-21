"""Fused numba ring-transfer kernel v1 for the general-n annealed machinery.

Replaces the transpose-copy-heavy numpy ring_M2 (121 s/matvec at n=5, nb=3,
N=1.7e6) with a carry-block fused kernel: the SAME mathematical operation
(validated to 1e-13), ~2 g^5 MACs, no large temporaries beyond two
(beta * g^nb) work buffers passed in by the caller.

Layout conventions IDENTICAL to n45_annealed_lib_v1.ring_M2 (verified against
its source):
  (M2 v)[tau_0..tau_{nb-1}] = sum_pi prod_k W[tau_k, pi_k, pi_{k+1}] v[pi..]
  lift  factor 0 : W[tau_0, a, pi_1]          (multiply; a = pi_0, blocked)
  step  factor k : W[tau_k, pi_k, pi_{k+1}]   (sum pi_k),  k = 1..nb-2
  final factor   : W[tau_{nb-1}, pi_{nb-1}, a](sum pi_{nb-1}, sum over a)

Buffer layouts (ravel order, tau_0 slowest as in v1):
  after lift : [a, tau_0, pi_1..pi_{nb-1}]              size b*g^nb
  after step k: [a, tau_0..tau_k, pi_{k+1}..pi_{nb-1}]  size b*g^nb  (const)
  final      : out[tau_0..tau_{nb-1}] = sum_a sum_{pi} cur[a, head, pi] * W[tau_last, pi, a]
"""
import numpy as np
from numba import njit, prange


@njit(parallel=True, cache=True)
def _ring_m2_kernel(v, Wf, g, nb, beta, bufA, bufB, out):
    """Wf = W.reshape(-1) (C-contiguous flat view of the (g,g,g) tensor)."""
    Gnb1 = g ** (nb - 1)
    Gnb2 = g ** (nb - 2)
    out[:] = 0.0
    for a0 in range(0, g, beta):
        b = beta if (a0 + beta <= g) else (g - a0)
        # ---- lift: bufA[a, tau_0, pi_code] = W[tau_0, a0+a, pi_1] * v[a0+a, pi_code]
        for i in prange(b * g * Gnb1):
            a = i // (g * Gnb1)
            r = i - a * g * Gnb1
            tau0 = r // Gnb1
            pic = r - tau0 * Gnb1
            pi1 = pic // Gnb2
            bufA[i] = Wf[(tau0 * g + a0 + a) * g + pi1] * v[(a0 + a) * Gnb1 + pic]
        cur = bufA
        nxt = bufB
        ntau = g           # g^1 accumulated tau codes
        rest_size = Gnb1   # number of remaining pi digits
        # ---- steps k = 1 .. nb-2
        for k in range(1, nb - 1):
            new_rest = rest_size // g
            tot = b * (g * ntau) * new_rest
            for i in prange(tot):
                a = i // (g * ntau * new_rest)
                r = i - a * g * ntau * new_rest
                taup = r // new_rest            # new tau code = tau_old*g + tau_new
                rest = r - taup * new_rest
                tau_new = taup % g
                tau_old = taup // g
                pi2 = rest // (new_rest // g)   # first digit of rest' = pi_{k+1}
                s = 0.0
                base_cur = (a * ntau + tau_old) * rest_size + rest
                base_W = (tau_new * g) * g + pi2
                for pi in range(g):
                    s += cur[base_cur + pi * new_rest] * Wf[base_W + pi * g]
                nxt[(a * g * ntau + taup) * new_rest + rest] = s
            rest_size = new_rest
            ntau = ntau * g
            tmp = cur
            cur = nxt
            nxt = tmp
        # ---- final: cur = [a, head(g^{nb-1}), pi]; head = tau_0..tau_{nb-2}
        Gt = Gnb1
        for i in prange(Gt):
            for tau_last in range(g):
                s = 0.0
                for a in range(b):
                    base = (a * Gt + i) * g
                    wA = a0 + a
                    for pi in range(g):
                        s += cur[base + pi] * Wf[(tau_last * g + pi) * g + wA]
                out[i * g + tau_last] += s
    return out


def ring_m2_nb(v_flat, W, nb, beta=8, bufs=None):
    """Numba ring-M2 matvec; same result as n45_annealed_lib_v1.ring_M2."""
    v = np.ascontiguousarray(np.asarray(v_flat, dtype=np.float64))
    W = np.ascontiguousarray(np.asarray(W, dtype=np.float64))
    g = W.shape[0]
    N = g ** nb
    if v.size != N:
        raise ValueError("bad v size")
    if nb == 1:
        Wd = W[:, np.arange(g), np.arange(g)]
        return Wd @ v
    out = np.zeros(N)
    big = beta * N
    if bufs is None:
        bufA = np.empty(big)
        bufB = np.empty(big)
    else:
        bufA, bufB = bufs
    _ring_m2_kernel(v, W.reshape(-1), g, nb, beta, bufA, bufB, out)
    return out


def ring_m1_nb(v_flat, W, nb, beta=8, bufs=None):
    """M1 v = moveaxis(ring_M2(v), -1, 0)  (the validated v1 identity)."""
    X = ring_m2_nb(v_flat, W, nb, beta=beta, bufs=bufs)
    g = W.shape[0]
    return np.ascontiguousarray(X.reshape((g,) * nb).transpose(
        tuple([nb - 1] + list(range(nb - 1)))).reshape(-1))
