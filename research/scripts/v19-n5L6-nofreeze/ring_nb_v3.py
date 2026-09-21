"""Fused numba ring-transfer kernel v3 for the general-n annealed machinery.

v1: correct but 48 s (stride-g inner loops).  v2: streaming step-loop but an
L3-thrashing final loop (timeout).  v3: all three loops stride-1 streaming,
with a specialised blk==1 path (the nb=3 case: n=5 L=6) and L2-panel-reuse
in the final contraction.

Mathematical operation IDENTICAL to n45_annealed_lib_v1.ring_M2:
  (M2 v)[tau_0..tau_{nb-1}] = sum_pi prod_k W[tau_k, pi_k, pi_{k+1}] v[pi..]
  lift  factor 0 : W[tau_0, a, pi_1]          (multiply; a = pi_0, blocked)
  step  factor k : W[tau_k, pi_k, pi_{k+1}]   (sum pi_k),  k = 1..nb-2
  final factor   : W[tau_{nb-1}, pi_{nb-1}, a](sum pi_{nb-1}, sum over a)
"""
import numpy as np
from numba import njit, prange


@njit(parallel=True, cache=True)
def _ring_m2_kernel(v, Wf, g, nb, beta, bufA, bufB, out):
    """Wf = W.reshape(-1); buffers sized beta * g^nb; out sized g^nb."""
    Gnb1 = g ** (nb - 1)
    Gnb2 = g ** (nb - 2)
    out[:] = 0.0
    for a0 in range(0, g, beta):
        b = beta if (a0 + beta <= g) else (g - a0)
        # ---- lift: bufA[a, tau_0, pi_code(1..nb-1)] = W[tau_0,a0+a,pi_1]*v[a0+a,pi_code]
        for at in prange(b * g):
            a = at // g
            tau0 = at - a * g
            wbase = (tau0 * g + a0 + a) * g
            vbase = (a0 + a) * Gnb1
            obase = (a * g + tau0) * Gnb1
            for pi1 in range(g):
                w = Wf[wbase + pi1]
                pbase = pi1 * Gnb2
                for t in range(Gnb2):
                    bufA[obase + pbase + t] = w * v[vbase + pbase + t]
        cur = bufA
        nxt = bufB
        ntau = g           # g^1 accumulated tau codes
        rest_size = Gnb1   # remaining pi digits
        # ---- steps k = 1..nb-2
        for k in range(1, nb - 1):
            new_rest = rest_size // g
            blk = new_rest // g          # tail size under the W third digit
            for i in prange(b * g * ntau):
                a = i // (g * ntau)
                taup = i - a * g * ntau
                tau_new = taup % g
                tau_old = taup // g
                base_nxt = (a * g * ntau + taup) * new_rest
                base_cur = (a * ntau + tau_old) * rest_size
                for r in range(new_rest):
                    nxt[base_nxt + r] = 0.0
                if blk == 1:
                    # nb=3 case: rest' is a single digit (pi2 == r): pure streaming
                    for pi in range(g):
                        bcur = base_cur + pi * new_rest
                        bw = (tau_new * g + pi) * g
                        for r in range(new_rest):
                            nxt[base_nxt + r] += cur[bcur + r] * Wf[bw + r]
                else:
                    for pi in range(g):
                        bcur = base_cur + pi * new_rest
                        bw = (tau_new * g + pi) * g
                        for p2 in range(g):
                            w = Wf[bw + p2]
                            rb = p2 * blk
                            bn = base_nxt + rb
                            bc = bcur + rb
                            for r in range(blk):
                                nxt[bn + r] += cur[bc + r] * w
            rest_size = new_rest
            ntau = ntau * g
            tmp = cur
            cur = nxt
            nxt = tmp
        # ---- final: cur = [a, head(g^{nb-1}), pi]; out[head,tau_last] += cur*W[tau_last,pi,a]
        # Wf[(tau_last*g + pi)*g + a0+a]: for fixed (tau_last, a) a stride-g panel
        # (115 KB span, L2-resident, reused across heads).  cur contiguous in pi.
        Gt = Gnb1
        for i in prange(Gt):
            for tau_last in range(g):
                s = 0.0
                for a in range(b):
                    base = (a * Gt + i) * g
                    bw = (tau_last * g) * g + (a0 + a)
                    for pi in range(g):
                        s += cur[base + pi] * Wf[bw + pi * g]
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
