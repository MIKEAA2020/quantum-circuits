"""
spinor_gridsearch.py -- find the parameter map and Majorana convention that
make the deposited Kaufman product identity hold for our E / E_OBC / M1.

Claimed identity (manuscript Eq. spinor):
    E   = cosh(K2) Ytil + sinh(K2) z_m Ytil z_1
    Ytil = c e^{K1 x_m} U_{m-1} ... U_1,
    U_k  = e^{K2 z_k z_{k+1}} c e^{K1 x_k},   c = sqrt(2 sinh 2 K1).

Verified already (element-wise algebra): the sandwich with z = sigma^z encodes
the wrap bond, E = cosh(K_d) E_OBC + sinh(K_d) sz_m E_OBC sz_1.  What remains:
the PRODUCT form of E_OBC (or M1_OBC / M1) with the right (K1, K2, x, z).

Grid: Majorana conventions x (plain / left-string / right-string sigma^x or
Majorana gamma1/gamma2), z (plain sigma^z / gamma1 / gamma2), parameter maps
(K1, K2) in terms of (K_d, K_h) and their Kramers-Wannier duals, targets
{E_OBC, E, M1_OBC, M1}, product order (forward / reversed), optimal overall
scale.  Reports the best relative residual per family.
"""
import numpy as np
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mipt_kaufman_lib as K

def pauli_on(m, k, which):
    N = 1 << m
    if which == 'z':
        n = np.arange(N); bit = (n >> k) & 1
        return np.diag(1.0 - 2.0 * bit).astype(float)
    if which == 'x':
        M = np.zeros((N, N))
        for i in range(N):
            M[i ^ (1 << k), i] = 1.0
        return M
    if which == 'y':
        M = np.zeros((N, N), dtype=complex)
        for i in range(N):
            b = (i >> k) & 1
            M[i ^ (1 << k), i] = 1j if b == 0 else -1j
        return M
    raise ValueError

def stringed(m, k, which, side):
    """sigma^{which}_k with a sigma^z string on the left or right."""
    M = pauli_on(m, k, which)
    if side == 'L':
        for i in range(k):
            M = pauli_on(m, i, 'z') @ M
    else:
        for i in range(k + 1, m):
            M = M @ pauli_on(m, i, 'z')
    return M

def S_arrays(m):
    N = 1 << m
    S = np.zeros((m, N))
    for k in range(m):
        S[k] = 1.0 - 2.0 * ((np.arange(N) >> k) & 1)
    return S

def build_E(m, Kd, obc=False):
    S = S_arrays(m)
    acc = np.zeros((1 << m, 1 << m))
    for k in range(m):
        acc += np.outer(S[k], S[k] + S[(k + 1) % m])
    if obc:
        acc -= np.outer(S[m - 1], S[0])
    return np.exp(Kd * acc)

def build_Dh(m, Kh, obc=False):
    S = S_arrays(m)
    if obc:
        w = sum(S[k] * S[(k + 1) % m] for k in range(m - 1))
    else:
        w = sum(S[k] * S[(k + 1) % m] for k in range(m))
    return np.diag(np.exp(Kh * w))

def dual(K):      # sinh 2K sinh 2K* = 1
    return 0.5 * np.arcsinh(1.0 / np.sinh(2 * K))

def adual(K):     # tanh K* = e^{-2K}
    return 0.5 * np.arctanh(np.exp(-2 * K))

def exp_of(A, ang):
    """exp(ang * A) for A with A^2 = +-I (Majorana / bilinear)."""
    A2 = A @ A
    if np.allclose(A2, np.eye(A.shape[0]), atol=1e-12):
        return np.cosh(ang) * np.eye(A.shape[0]) + np.sinh(ang) * A
    elif np.allclose(A2, -np.eye(A.shape[0]), atol=1e-12):
        return np.cos(ang) * np.eye(A.shape[0]) + np.sin(ang) * A
    else:
        from scipy.linalg import expm
        return expm(ang * A)

def build_claim(m, K1, K2, xs, zs, reverse=False, K2s=None):
    """Ytil = c e^{K1 x_m} [e^{K2 z_{m-1} z_m} c e^{K1 x_{m-1}}] ... [e^{K2 z_1 z_2} c e^{K1 x_1}]
    (deposited order: U_{m-1} ... U_1).  K2s = boundary/sandwich coupling
    (defaults to K2 as in the deposit)."""
    if K2s is None:
        K2s = K2
    c = np.sqrt(2 * np.sinh(2 * K1))
    if not reverse:
        Y = c * exp_of(xs[m - 1], K1)
        for k in range(m - 2, -1, -1):
            Y = Y @ (exp_of(zs[k] @ zs[k + 1], K2) @ (c * exp_of(xs[k], K1)))
    else:
        Y = c * exp_of(xs[m - 1], K1)
        for k in range(0, m - 1):
            Y = (exp_of(zs[k] @ zs[k + 1], K2) @ (c * exp_of(xs[k], K1))) @ Y
    return Y, K2s

def residual(target, claim):
    """optimal-scale relative residual."""
    num = np.trace(claim.conj().T @ target)
    den = np.trace(claim.conj().T @ claim)
    if abs(den) < 1e-300:
        return 1e9, 0
    N = num / den
    return np.linalg.norm(N * claim - target) / np.linalg.norm(target), N

def make_ops(m, conv):
    """Return (xs, zs): lists of m operators each, per convention."""
    kind = conv[0]
    if kind == 'bothplain':
        # z_k = sigma^z_k, x_k = sigma^x_k (plain Paulis -- the SML Clifford algebra)
        zs = [pauli_on(m, k, 'z') for k in range(m)]
        xs = [pauli_on(m, k, 'x') for k in range(m)]
    elif kind == 'zplain':
        # z_k = sigma^z_k ; x_k = stringed sigma^x
        zs = [pauli_on(m, k, 'z') for k in range(m)]
        side = conv[1]
        xs = [stringed(m, k, 'x', side) for k in range(m)]
    elif kind == 'xplain':
        xs = [pauli_on(m, k, 'x') for k in range(m)]
        side = conv[1]
        zs = [stringed(m, k, 'z', side) for k in range(m)]
    elif kind == 'jw':
        g1 = [stringed(m, k, 'x', 'L') for k in range(m)]
        g2 = [stringed(m, k, 'y', 'L') for k in range(m)]
        xs, zs = (g1, g2) if conv[1] == 'xg1' else (g2, g1)
    elif kind == 'jwr':
        g1 = [stringed(m, k, 'x', 'R') for k in range(m)]
        g2 = [stringed(m, k, 'y', 'R') for k in range(m)]
        xs, zs = (g1, g2) if conv[1] == 'xg1' else (g2, g1)
    else:
        raise ValueError(conv)
    return xs, zs

def main():
    m = 3
    d, p = 2, 0.16
    Kd, Kh, W0 = K.couplings(d, p)
    print(f"Kd={Kd:.6f} Kh={Kh:.6f}  (d={d}, p={p})")

    E = build_E(m, Kd)
    Eo = build_E(m, Kd, obc=True)
    Dh = build_Dh(m, Kh)
    Dho = build_Dh(m, Kh, obc=True)
    targets = {
        'E_OBC': Eo, 'E': E,
        'M1_OBC': Eo @ Dho, 'M1': E @ Dh,
        'E_OBC*Dh': Eo @ Dh, 'Dh*E_OBC': Dh @ Eo,
    }

    k1cands = {
        'Kd': Kd, 'Kh': Kh, 'dual(Kd)': dual(Kd), 'dual(Kh)': dual(Kh),
        'adual(Kd)': adual(Kd), 'Kd/2': Kd / 2, 'Kh/2': Kh / 2,
        'dual(Kd)/2': dual(Kd) / 2, '-Kh': -Kh,
    }
    k2cands = {
        'Kd': Kd, 'Kh': Kh, 'dual(Kd)': dual(Kd), 'dual(Kh)': dual(Kh),
        'adual(Kd)': adual(Kd), 'adual(Kh)': adual(Kh), 'Kd/2': Kd / 2, '-Kh': -Kh,
    }
    convs = [
        ('bothplain', ''),
        ('zplain', 'L'), ('zplain', 'R'),
        ('xplain', 'L'), ('xplain', 'R'),
        ('jw', 'xg1'), ('jw', 'xg2'),
        ('jwr', 'xg1'), ('jwr', 'xg2'),
    ]

    results = []
    for conv in convs:
        xs, zs = make_ops(m, conv)
        for n1, K1 in k1cands.items():
            for n2, K2 in k2cands.items():
                if K1 <= 0 or K2 <= 0 or not np.isfinite(K1) or not np.isfinite(K2):
                    continue
                for K2s, n2s in ((K2, n2), (Kd, 'Kd(bdry)'), (Kh, 'Kh(bdry)')):
                    if not np.isfinite(K2s):
                        continue
                    for rev in (False, True):
                        Y, _ = build_claim(m, K1, K2, xs, zs, reverse=rev, K2s=K2s)
                        for tname, T in targets.items():
                            R = np.cosh(K2s) * Y + np.sinh(K2s) * (zs[m - 1] @ Y @ zs[0])
                            r, N = residual(T, R)
                            results.append((r, conv, n1, n2, n2s, rev, tname, N))
    results.sort(key=lambda t: t[0])
    print("\nbest 25 matches (rel residual, conv, K1, K2, K2boundary, reverse, target, scale):")
    for r, conv, n1, n2, n2s, rev, tname, N in results[:25]:
        print(f"  {r:.3e}  {conv}  K1={n1:10s} K2={n2:10s} bdry={n2s:10s} rev={rev}  T={tname:9s} N={N:.4f}")

if __name__ == '__main__':
    main()
