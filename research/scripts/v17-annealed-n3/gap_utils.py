"""gap_utils.py -- RECONSTRUCTED (v22) shared library for the annealed
replica spectral program.

PROVENANCE NOTE (v22 finding).  This module is the common dependency of the
deposited v17/v18/v19 script suites (n3_annealed_lib.py, n45_annealed_lib_v1.py,
n5_L6_scan_v2.py all do `from gap_utils import perms, compose, inv, cycles,
W_tensor`), but it was never committed to the repository: the deposited runs
happened in a scratch working directory whose gap_utils.py was lost, so the
reproduction chain of research/ v4-v7 was silently broken.  This file rebuilds
it EXACTLY from the manuscript's Eq. (Wpn) (manuscript_revised_v21_clifford.tex,
Proposition prop:general-n(iii)):

    W_{p,n}(pi|mu,nu) = sum_{sigma in S_n} Wg_{d^2}(pi^{-1} sigma)
                        * [(1-p) d^{c(sigma^{-1} mu)} + p d]
                        * [(1-p) d^{c(sigma^{-1} nu)} + p d],

with Wg_D the Weingarten function of U(D) -- the inverse of the Gram matrix
G[sigma,tau] = D^{c(sigma^{-1} tau)} for D >= n and its Moore-Penrose
pseudo-inverse otherwise -- and c(.) counting cycles (fixed points included,
so that Tr U_pi = d^{c(pi)}).

Conventions (matched to the deposited code):
  * permutations are image tuples:  pi[i] = image of i;
  * compose(a, b) = a after b:  i -> b[i] -> a[b[i]];
  * cycles(s) counts cycles of the map i -> s[i], fixed points included;
  * W_tensor(n, d, p) -> (P, idx, W) with P the tuple list of S_n,
    idx the tuple->index map, and W[pi, mu, nu] = W_{p,n}(pi|mu,nu)
    (FIRST index = output label; M2[tau;pi] = prod_k W[tau_k, pi_k, pi_{k+1}],
     M1[pi';tau] = prod_k W[pi'_k, tau_{k-1}, tau_k], C = M1 @ M2).

Validation: v22_gaputils_validate_v1.py reproduces, with THIS module,
  (V1) the n=2 Kaufman closed-form spectrum of C_comp (to ~1e-13),
  (V2) the deposited n=3 dense-scan eigenvalues (lam1/lam_eps/lam_sigma,
       L=4..12, to the last digit),
  (V3) the deposited n=4 L=8 scan rows,
  (V4) the deposited n=5 L=4 scan rows (triv3, lam_sigma, gap12),
  (V5) the n=2 control crossings 0.23319/0.23347/0.23361/0.23368,
  (V6) the p=1 closed form lam1(nb) = [d^2 G(d^2)G(n+1)/G(d^2+n)]^{2 nb}
       and rank one, for n=2..5 (the n=5 value 1/14 exercises the pinv
       Weingarten channel),
which is the complete deposited validation chain of gap_utils.
"""
import math
import itertools
import numpy as np

__all__ = ["perms", "compose", "inv", "cycles", "weingarten", "W_tensor",
           "cycle_type", "bond_ops", "build_M", "n_repl_pc1_eig"]


# ---------------------------------------------------------------------------
# basic group utilities (image-tuple convention)
def perms(n):
    """All n! permutations of S_n as image tuples pi[i] = pi(i)."""
    return list(itertools.permutations(range(n)))


def compose(a, b):
    """(a after b)(i) = a[b[i]]."""
    return tuple(a[b[i]] for i in range(len(b)))


def inv(s):
    out = [0] * len(s)
    for i, si in enumerate(s):
        out[si] = i
    return tuple(out)


def cycles(s):
    """Number of cycles of i -> s[i], fixed points counted as cycles."""
    n = len(s)
    seen = [False] * n
    c = 0
    for i in range(n):
        if not seen[i]:
            j = i
            while not seen[j]:
                seen[j] = True
                j = s[j]
            c += 1
    return c


def cycle_type(pi):
    n = len(pi)
    seen = [False] * n
    lens = []
    for i in range(n):
        if not seen[i]:
            j = i
            c = 0
            while not seen[j]:
                seen[j] = True
                j = pi[j]
                c += 1
            lens.append(c)
    return tuple(sorted(lens, reverse=True))


# ---------------------------------------------------------------------------
# Weingarten function of U(D) on S_n (operator-basis convention:
# inverse / pseudo-inverse of the Gram matrix D^{c(sigma^{-1} tau)})
def weingarten(n, D):
    """Return (P, Wg) with P the tuple list of S_n and
    Wg[s, t] = Wg_D(s^{-1} t) -- the inverse of the Gram matrix
    G[s, t] = D^{c(s^{-1} t)} for D >= n, its Moore-Penrose pseudo-inverse
    otherwise (the deposited two-value signature)."""
    P = perms(n)
    g = len(P)
    G = np.empty((g, g), dtype=float)
    for i, s in enumerate(P):
        si = inv(s)
        for j, t in enumerate(P):
            G[i, j] = float(D) ** cycles(compose(si, t))
    if D >= n:
        Ginv = np.linalg.inv(G)
    else:
        Ginv = np.linalg.pinv(G)
    return P, Ginv


def weingarten_gram(n, D):
    """(P, G, Ginv) -- weingarten() plus the Gram matrix itself."""
    P, Ginv = weingarten(n, D)
    g = len(P)
    G = np.empty((g, g), dtype=float)
    for i, s in enumerate(P):
        si = inv(s)
        for j, t in enumerate(P):
            G[i, j] = float(D) ** cycles(compose(si, t))
    return P, G, Ginv


# ---------------------------------------------------------------------------
# the exact bond channel of Eq. (Wpn)
def W_tensor(n, d, p):
    """(P, idx, W):  W[pi, mu, nu] = W_{p,n}(pi|mu,nu) of Eq. (Wpn)."""
    P, Ginv = weingarten(n, d * d)
    idx = {s: i for i, s in enumerate(P)}
    g = len(P)
    # T[s, mu] = Tr[U_s^dag M_p^{(n)}(U_mu)] = (1-p) d^{c(s^{-1} mu)} + p d
    T = np.empty((g, g), dtype=float)
    for i, s in enumerate(P):
        si = inv(s)
        for j, mu in enumerate(P):
            T[i, j] = (1.0 - p) * float(d) ** cycles(compose(si, mu)) + p * d
    # W[pi, mu, nu] = sum_sigma Ginv[pi, sigma] T[sigma, mu] T[sigma, nu]
    W = np.einsum("ps,sm,sn->pmn", Ginv, T, T)
    return P, idx, W


def n_repl_pc1_eig(n, d=2):
    """p=1 per-bond eigenvalue d^2 Gamma(d^2) Gamma(n+1) / Gamma(d^2+n)."""
    from scipy.special import gammaln
    D = d * d
    return float(math.exp(math.log(D) + gammaln(D) + gammaln(n + 1)
                           - gammaln(D + n)))


# ---------------------------------------------------------------------------
# dense bond-label operators (the deposited, benchmark-verified convention:
# gap_utils.bond_ops of the v17/v18 runs; construction identical to
# n3_annealed_lib.build_M, row-chunked to bound temporary memory):
#   M2[tau; pi] = prod_k W[tau_k, pi_k, pi_{k+1}]   (even -> odd)
#   M1[pi'; tau] = prod_k W[pi'_k, tau_{k-1}, tau_k] (odd  -> even)
def build_M(W, nb, g, form, chunk=1024):
    """Dense M1/M2 (N x N, N = g**nb) by Hadamard product of broadcast
    local gathers, row-chunked."""
    N = g ** nb
    labs = np.array(np.unravel_index(np.arange(N), (g,) * nb)).T
    W2 = np.asarray(W).reshape(g, g * g)
    M = np.ones((N, N))
    if form == 'M2':      # M2[tau; pi] = prod_k W[tau_k, pi_k, pi_{k+1}]
        cols = [labs[:, k] * g + labs[:, (k + 1) % nb] for k in range(nb)]
        rows = [labs[:, k] for k in range(nb)]
    elif form == 'M1':    # M1[pi'; tau] = prod_k W[pi'_k, tau_{k-1}, tau_k]
        cols = [labs[:, (k - 1) % nb] * g + labs[:, k] for k in range(nb)]
        rows = [labs[:, k] for k in range(nb)]
    else:
        raise ValueError(form)
    for i0 in range(0, N, chunk):
        i1 = min(i0 + chunk, N)
        blk = M[i0:i1]
        for k in range(nb):
            blk *= W2[rows[k][i0:i1, None], cols[k][None, :]]
        M[i0:i1] = blk
    return M


def bond_ops(n, d, p, nb):
    """(P, idx, W, M1, M2): dense bond-label operators on (S_n)^nb."""
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    M1 = build_M(W, nb, g, 'M1')
    M2 = build_M(W, nb, g, 'M2')
    return P, idx, W, M1, M2
