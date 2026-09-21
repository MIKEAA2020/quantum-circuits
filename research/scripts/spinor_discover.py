"""
spinor_discover.py -- structural discovery for the S5/S6 gap.

The deposited proof route claims (manuscript Eq. spinor):
    E = cosh(K2) Ytil + sinh(K2) z_m Ytil z_1
    Ytil = c e^{K1 x_m} U_{m-1}...U_1,   U_k = e^{K2 z_k z_{k+1}} c e^{K1 x_k},
    c = sqrt(2 sinh 2K1),
with (K1, K2) some function of (K_d, K_h), and "E and D_h exactly Gaussian in
the Jordan-Wigner representation with open ends".  The previous reconstruction
could not reproduce the parameter map.  This script finds the TRUE structure:

D1. Pauli-string expansion of log E, log E_OBC, log D_h, log D_h_OBC
    (m = 3, 4): which Pauli strings appear?  -> the exact algebraic content.
D2. Direct test of the boundary (sandwich) structure:
       E = cosh(K_d) E_OBC + sinh(K_d) sz_m E_OBC sz_1   (element-wise proof)
D3. Test of the claimed product form for E_OBC / M1_OBC over parameter maps
    and Majorana conventions (grid search, optimal overall scale).
"""
import numpy as np
import itertools
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mipt_kaufman_lib as K

np.set_printoptions(precision=4, suppress=True, linewidth=200)

# ---------------------------------------------------------------- Paulis
def pauli_on(m, k, which):
    """2^m x 2^m matrix: `which` in {'x','z','y'} on site k (bit k = site k)."""
    N = 1 << m
    n = np.arange(N)
    bit = (n >> k) & 1                      # 0 -> s=+1, 1 -> s=-1
    if which == 'z':
        M = np.diag(1.0 - 2.0 * bit).astype(float)
    elif which == 'x':
        # sigma^x flips bit k
        M = np.zeros((N, N))
        for i in range(N):
            M[i ^ (1 << k), i] = 1.0
    elif which == 'y':
        M = np.zeros((N, N), dtype=complex)
        for i in range(N):
            b = (i >> k) & 1
            # sigma^y = [[0,-i],[i,0]] in the z-basis (bit 0 = +1 eigenstate)
            val = 1j if b == 0 else -1j
            M[i ^ (1 << k), i] = val
    return M

I_cache = {}
def identity(m):
    return np.eye(1 << m)

# ---------------------------------------------------------------- E, D_h builders
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
    if obc:   # remove the wrap bond (s'_m, s_1): term k = m-1 uses S[0]
        acc -= np.outer(S[m - 1], S[0])
    return np.exp(Kd * acc)

def build_Dh(m, Kh, obc=False):
    S = S_arrays(m)
    n = np.arange(1 << m)
    if obc:
        w = sum(S[k] * S[(k + 1) % m] for k in range(m - 1))
    else:
        w = sum(S[k] * S[(k + 1) % m] for k in range(m))
    return np.diag(np.exp(Kh * w))

# ---------------------------------------------------------------- D1: Pauli-string expansion
def pauli_string_coeffs(m, M):
    """Expand operator M in the Pauli-string basis; return dict {(a_1..a_m): coeff}
    with a_k in {0:'I',1:'x',2:'y',3:'z'}, coeff = Tr(M P)/2^m (P Hermitian unitary,
    Tr(P P') = 2^m delta)."""
    N = 1 << m
    out = {}
    for letters in itertools.product(range(4), repeat=m):
        P = np.eye(N) + 0j
        for k in range(m):
            if letters[k] == 0:
                continue
            P = P @ pauli_on(m, k, 'xyz'[letters[k] - 1])
        c = np.trace(M @ P) / N
        if abs(c) > 1e-9:
            out[letters] = c
    return out

def fmt_letters(letters):
    return "".join("IXYZ"[a] for a in letters)

print("=" * 70)
print("D1. Pauli-string content of log E (PBC/OBC) and log D_h (PBC/OBC)")
print("=" * 70)
for m in (3, 4):
    Kd, Kh, W0 = K.couplings(2, 0.16)
    E = build_E(m, Kd)
    Eo = build_E(m, Kd, obc=True)
    Dh = build_Dh(m, Kh)
    Dho = build_Dh(m, Kh, obc=True)
    for name, M in (("E", E), ("E_OBC", Eo), ("D_h", Dh), ("D_h_OBC", Dho)):
        L = np.linalg.inv(M) if False else None
        # matrix log via eigendecomposition (M real positive definite? E is not
        # symmetric but is diagonalizable with positive spectrum in practice;
        # use scipy)
        from scipy.linalg import logm
        L = logm(M)
        if np.max(np.abs(np.imag(L))) < 1e-8:
            L = np.real(L)
        coeffs = pauli_string_coeffs(m, L)
        print(f"\n m={m}  log({name}):  Kd={Kd:.4f} Kh={Kh:.4f}")
        for letters, c in sorted(coeffs.items(), key=lambda kv: -abs(kv[1])):
            print(f"   {fmt_letters(letters)}   {c.real:+.6f}" + (f"  + {np.imag(c):+.6f}i" if abs(np.imag(c)) > 1e-9 else ""))

print()
print("=" * 70)
print("D2. Boundary structure:  E = cosh(K_d) E_OBC + sinh(K_d) sz_m E_OBC sz_1 ?")
print("=" * 70)
for m in (3, 4, 5):
    Kd, Kh, W0 = K.couplings(2, 0.16)
    E = build_E(m, Kd)
    Eo = build_E(m, Kd, obc=True)
    szm = pauli_on(m, m - 1, 'z')
    sz1 = pauli_on(m, 0, 'z')
    lhs = np.cosh(Kd) * Eo + np.sinh(Kd) * (szm @ Eo @ sz1)
    print(f" m={m}: ||lhs - E||/||E|| = {np.linalg.norm(lhs - E)/np.linalg.norm(E):.2e}")

print()
print("=" * 70)
print("D2b. D_h:  D_h = cosh(K_h) D_h_OBC + sinh(K_h) sz_m D_h_OBC sz_1 ?")
print("=" * 70)
for m in (3, 4, 5):
    Kd, Kh, W0 = K.couplings(2, 0.16)
    Dh = build_Dh(m, Kh)
    Dho = build_Dh(m, Kh, obc=True)
    szm = pauli_on(m, m - 1, 'z')
    sz1 = pauli_on(m, 0, 'z')
    lhs = np.cosh(Kh) * Dho + np.sinh(Kh) * (szm @ Dho @ sz1)
    print(f" m={m}: ||lhs - D_h||/||D_h|| = {np.linalg.norm(lhs - Dh)/np.linalg.norm(Dh):.2e}")
