"""Build the annealed two-replica transfer from the quantum per-site algebra
{e0 (collided diag), e+ (off-diag symmetric), e- (antisym)} and match its
spectrum against the Ising closed form to extract (Kd, Kh, W0)(p, d)."""
import numpy as np
from itertools import product

def site_basis(d):
    """Per-site (replica-pair) projectors on C^d (x) C^d: e0, e+, e-."""
    N = d*d
    S = np.zeros((N, N))
    for a in range(d):
        for b in range(d):
            S[a*d+b, b*d+a] = 1.0
    P = np.zeros((N, N))
    for x in range(d):
        P[x*d+x, x*d+x] = 1.0
    e0 = P
    ep = (np.eye(N)+S)/2 - P
    em = (np.eye(N)-S)/2
    return [e0, ep, em], S

def kron_list(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def build_transfer(L, d, p, order="ABM"):
    """Transfer on the 3^L algebra. Gates on even (A) then odd (B) bonds, each
    followed by a measurement layer (rate p). Returns the 3^L x 3^L matrix."""
    bas, S = site_basis(d)
    N = d**(2*L)
    # basis elements
    elems = []
    labels = []
    for combo in product(range(3), repeat=L):
        elems.append(kron_list([bas[c] for c in combo]))
        labels.append(combo)
    # per-site swap operators (embedded)
    Sw = [kron_list([S if i==k else np.eye(d*d) for k in range(L)]) for i in range(L)]
    I_full = np.eye(N)
    D = d*d  # bond dimension per replica

    def twirl_bond(X, i, j):
        Sij = Sw[i] @ Sw[j] if i != j else np.eye(N)
        trX = np.trace(X); trXS = np.trace(X @ Sij)
        al = (D*trX - trXS)/(D*(D*D-1))
        be = (D*trXS - trX)/(D*(D*D-1))
        return al*I_full + be*Sij

    def meas_site(X, i):
        Pi = kron_list([bas[0] if k==i else np.eye(d*d) for k in range(L)])
        return (1-p)*X + p*(Pi @ X @ Pi)

    even = [(2*k, 2*k+1) for k in range(L//2)]
    odd  = [(2*k+1, (2*k+2) % L) for k in range(L//2)]

    def apply_layers(X, order):
        for ch in order:
            if ch == 'A':
                for (i, j) in even: X = twirl_bond(X, i, j)
            elif ch == 'B':
                for (i, j) in odd: X = twirl_bond(X, i, j)
            elif ch == 'M':
                for i in range(L): X = meas_site(X, i)
        return X

    T = np.zeros((3**L, 3**L))
    # transfer matrix in coefficient space: T(basis_j) = sum_i T[i,j] basis_i
    # basis is orthogonal under trace-inner-product? Not orthonormal; use duals:
    # e0,e+,e- are mutually orthogonal PROJECTORS: dual of e_a is e_a (tr(e_a e_b)=0 for a!=b)
    trs = np.array([np.trace(E) for E in elems])
    for j, Ej in enumerate(elems):
        Ej2 = apply_layers(Ej, order)
        for i, Ei in enumerate(elems):
            ov = np.trace(Ei @ Ej2)
            if i == j and labels[i] == labels[j]:
                pass
            T[i, j] = ov / trs[i] if trs[i] != 0 else 0.0
        # correction: off-diagonal overlaps vanish only if Ej2 stays in span...
    return T, labels

# quick test L=4, d=2, p=0.4: top eigenvalues
for order in ["ABM", "AMB", "AMBM", "ABMM"]:
    T, labels = build_transfer(4, 2, 0.4, order=order)
    ev = np.linalg.eigvals(T)
    ev = np.sort(np.real(ev[np.abs(np.imag(ev)) < 1e-9]))[::-1]
    print(f"order={order}: top eigenvalues: {ev[:5]}")
