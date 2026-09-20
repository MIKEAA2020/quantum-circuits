"""Annealed n-replica spectral program (v1) — library.

Sector-resolved spectra of the compressed n-replica period operator
C_comp = M1 @ M2 on bond labels (S_n)^{L/2} with the exact bond channel
W_{p,n}(pi|mu,nu) of Eq. (Wpn) (Weingarten data at D = d^2), for n=2
(control against the Kaufman closed form) and n=3 (the annealed
three-replica transition).

Deposited, benchmark-verified conventions (gap_utils.bond_ops):
  M2[tau;pi]  = prod_k W(tau_k | pi_k, pi_{k+1})     (even -> odd)
  M1[pi';tau] = prod_k W(pi'_k | tau_{k-1}, tau_k)   (odd  -> even)
  C = M1 @ M2 ;  Gram G = (d^{2c(sigma^-1 tau)})^{⊗ nb} ;
  eigs(C) = sigma(S)^2 with S = G^{1/2} M1 G^{-1/2}  (similarity).

Sectors: colour (S_n x S_n irreps via deposited group-algebra idempotents),
inversion parity, ring momentum k.  Validated against gap_proofs
verification Sec. 9 benchmarks and the n=2 Kaufman closed form.

Momentum-orbit algebra (used by the block route):  with
|k,O> = (1/sqrt(p)) sum_j e^{2 pi i k j/nb} |T^j c>  (p = orbit period,
admissible iff e^{2 pi i k p/nb}=1) and translation covariance
M[T x, T y] = M[x, y],
  <k,O_a| M |k,O_b> = sqrt(p_a/p_b) sum_{j'<p_b} e^{2 pi i k j'/nb}
                       M[c_a, T^{j'} c_b].
"""
import sys, os, math
from fractions import Fraction
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh, eigs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gap_utils import perms, compose, inv, cycles, W_tensor

# ---------------------------------------------------------------------------
# colour idempotents (group algebra elements; copied from the deposited
# n3_mult_certificates.py for n=3, analogous for n=2)
def _ga_mul(x, y):
    out = {}
    for a, xa in x.items():
        for b, yb in y.items():
            c = compose(a, b); out[c] = out.get(c, 0) + xa * yb
    return {k: v for k, v in out.items() if v != 0}

def _ga_add(x, y, cy=1):
    out = dict(x)
    for k, v in y.items(): out[k] = out.get(k, 0) + cy * v
    return {k: v for k, v in out.items() if v != 0}

def _ga_scale(x, c): return {k: v * c for k, v in x.items()}

def colour_blocks(n):
    """[(name, el, er, eps, dim)] colour blocks of (S_n x S_n) rt Z2^inv."""
    if n == 3:
        P3 = perms(3)
        sgn = {s: (1 if (3 - cycles(s)) % 2 == 0 else -1) for s in P3}
        ONE = {P3[0]: Fraction(1)}
        t12 = (1, 0, 2); t13 = (2, 1, 0); t23 = (0, 2, 1)
        e_triv = {s: Fraction(1, 6) for s in P3}
        e_sgn = {s: Fraction(sgn[s], 6) for s in P3}
        X2 = {t12: Fraction(1)}
        X3 = {t13: Fraction(1), t23: Fraction(1)}
        A = _ga_scale(_ga_add(ONE, X2), Fraction(1, 2))
        Bq = _ga_mul(_ga_mul(_ga_add(X3, ONE, -2), _ga_add(X3, ONE, 2)), _ga_add(X3, ONE, -1))
        E_std = _ga_mul(A, _ga_scale(Bq, Fraction(1, 6)))
        for name, e in [('triv', e_triv), ('sgn', e_sgn), ('std', E_std)]:
            assert _ga_mul(e, e) == e, name + " not idempotent"
        return [('triv.triv,i+', e_triv, e_triv, +1, 1),
                ('triv.triv,i-', e_triv, e_triv, -1, 1),
                ('sgn.sgn,i+', e_sgn, e_sgn, +1, 1),
                ('sgn.sgn,i-', e_sgn, e_sgn, -1, 1),
                ('Ind(triv.sgn)', e_triv, e_sgn, 0, 2),
                ('std.std,i+', E_std, E_std, +1, 4),
                ('std.std,i-', E_std, E_std, -1, 4),
                ('Ind(triv.std)', e_triv, E_std, 0, 4),
                ('Ind(sgn.std)', e_sgn, E_std, 0, 4)]
    if n == 2:
        P2 = perms(2); e_ = P2[0]; s_ = P2[1]
        e_triv = {e_: Fraction(1, 2), s_: Fraction(1, 2)}
        e_sgn = {e_: Fraction(1, 2), s_: Fraction(-1, 2)}
        return [('triv.triv,i+', e_triv, e_triv, +1, 1),
                ('sgn.sgn,i+', e_sgn, e_sgn, +1, 1),
                ('Ind(triv.sgn)', e_triv, e_sgn, 0, 1)]
    raise ValueError("n=2,3 only")

# ---------------------------------------------------------------------------
# configuration space: labels in S_g^nb, flat index ravel base g
class ConfigSpace:
    def __init__(self, g, nb):
        self.g, self.nb, self.N = g, nb, g ** nb
        self.labs = np.array(np.unravel_index(np.arange(self.N), (g,) * nb)).T
        self.flat = lambda arr: np.ravel_multi_index(np.asarray(arr).T, (g,) * nb)
    def relabel_gather(self, a, b, perm_list):
        """gather[j] = i  s.t.  relabel(config_i, a, b) = config_j;
        then (U_{a,b} v)[j] = v[gather[j]]  =>  U v = v[gather]."""
        idx = {s: i for i, s in enumerate(perm_list)}
        symap = np.array([idx[compose(a, compose(perm_list[s], b))] for s in range(self.g)])
        newlab = symap[self.labs]                      # (N, nb) labels of relabeled configs
        j = self.flat(newlab)                          # j = destination of each i
        gather = np.empty(self.N, dtype=np.int64)
        gather[j] = np.arange(self.N)
        return gather
    def inversion_gather(self, perm_list):
        idx = {s: i for i, s in enumerate(perm_list)}
        symap = np.array([idx[inv(s)] for s in perm_list])
        j = self.flat(symap[self.labs])
        gather = np.empty(self.N, dtype=np.int64)
        gather[j] = np.arange(self.N)
        return gather
    def shift_gather(self, s=1):
        j = self.flat(np.roll(self.labs, s, axis=1))
        gather = np.empty(self.N, dtype=np.int64)
        gather[j] = np.arange(self.N)
        return gather

def make_colour_projector(block, cs, perm_list):
    """P = L(el) R(er) (1 + eps*iota)/2 as a dense-vector map."""
    name, el, er, eps, dim = block
    gathers = []
    for a, xa in el.items():
        for b, yb in er.items():
            gathers.append((float(xa * yb), cs.relabel_gather(a, b, perm_list)))
    iota = cs.inversion_gather(perm_list)
    def proj(v):
        out = np.zeros_like(v)
        for c, gg in gathers:
            out += c * v[gg]
        if eps:
            out = 0.5 * (out + eps * out[iota])
        return out
    return proj

def make_momentum_projector(k, cs):
    nb, N = cs.nb, cs.N
    Tg = [cs.shift_gather(s) for s in range(nb)]
    ph = np.array([np.exp(-2j * np.pi * k * s / nb) for s in range(nb)])
    def proj(v):
        out = np.zeros(N, dtype=complex)
        for s in range(nb):
            out += ph[s] * v[Tg[s]]
        return out / nb
    return proj

def momentum_content(vec, cs):
    """|<k|v>|^2 / |v|^2 for k=0..nb-1 (v real or complex)."""
    nb = cs.nb
    v = np.asarray(vec, dtype=complex)
    n2 = np.linalg.norm(v) ** 2
    if n2 < 1e-300: return [0.0] * nb
    Tg = [cs.shift_gather(s) for s in range(nb)]
    out = []
    for k in range(nb):
        pk = sum(np.exp(2j * np.pi * k * s / nb) * v[Tg[s]] for s in range(nb)) / nb
        out.append(float(np.real(np.vdot(pk, pk)) / n2))
    return out

# ---------------------------------------------------------------------------
# n=2 Kaufman closed form (manuscript Prop. spectrum) — control
def n2_abc(d, p):
    th = d - (d - 1) * p
    a = (d * d * th * th - 1) / (d ** 4 - 1)
    b = th / (d * d + 1)
    c = (d * d - th * th) / (d ** 4 - 1)
    return a, b, c

def n2_pc2(d):
    beta = (d * d - 1) / (d * d + 1)
    thc = beta + math.sqrt(beta * beta + 1)
    return (d - thc) / (d - 1)

def n2_closed_spectrum(d, p, m, max_evals=None):
    """Nonzero eigenvalues of C_comp (n=2) from the Kaufman product form,
    sorted descending.  Even sector: K+ = {(2j-1)pi/m}, even # of '-'.
    Odd sector:  K- = {2 pi j/m}, even # of '-' below pc2, odd above."""
    a, b, c = n2_abc(d, p)
    if min(a, b, c) <= 0:
        return np.array([])
    Kd = 0.25 * math.log(a / c)
    Kh = 0.25 * math.log(a * c / (b * b))
    W0 = (a * c * b * b) ** 0.25
    def QR(k):
        Q = math.cosh(2 * Kd) ** 2 * math.cosh(2 * Kh) \
            + math.sinh(2 * Kd) ** 2 * math.sinh(2 * Kh) \
            - math.sinh(2 * Kh) * math.cos(k)
        R = 2 * math.sinh(2 * Kd) * math.cos(k / 2)
        disc = max(Q * Q - R * R, 0.0)
        return Q - math.sqrt(disc), Q + math.sqrt(disc)
    Kp = [(2 * j - 1) * math.pi / m for j in range(1, m + 1)]
    Kl = [2 * math.pi * j / m for j in range(0, m)]
    base = (2 * W0 * W0) ** m
    lams = []
    def add_sector(Ks, parity):
        for mask in range(1 << m):
            if bin(mask).count('1') % 2 != parity % 2:
                continue
            lam = base
            for j, k in enumerate(Ks):
                wm, wp = QR(k)
                lam *= (wm if (mask >> j) & 1 else wp)
            lams.append(lam)
    add_sector(Kp, 0)
    add_sector(Kl, 0 if p < n2_pc2(d) else 1)
    lams = np.array(sorted(lams, reverse=True))
    lams = lams[lams > 1e-14]
    return lams[:max_evals] if max_evals else lams

# ---------------------------------------------------------------------------
# dense construction (nb <= 5)
def build_M(W, nb, g, form, chunk=1024):
    """Dense M1/M2 (N x N) by Hadamard product of broadcast local gathers,
    row-chunked to bound the temporary memory."""
    N = g ** nb
    labs = np.array(np.unravel_index(np.arange(N), (g,) * nb)).T
    W2 = W.reshape(g, g * g)
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

def kron_left(M, A, g, nb):
    """(A^{⊗ nb}) @ M (row-space Kronecker transform)."""
    N = g ** nb
    X = M.reshape([g] * nb + [N])
    for leg in range(nb):
        X = np.moveaxis(np.tensordot(A, X, axes=([1], [leg])), 0, leg)
    return X.reshape(N, N)

def build_S(n, d, p, nb, return_parts=False):
    """S = G^{1/2} M1 G^{-1/2}; eigs(C=M1 M2) = sigma(S)^2."""
    import gc
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    M1 = build_M(W, nb, g, 'M1')
    Gloc = np.array([[float(d * d) ** cycles(compose(inv(s), t)) for t in P] for s in P])
    wv, Vv = np.linalg.eigh(Gloc)
    Ghalf = (Vv * np.sqrt(wv)) @ Vv.T
    Gmhalf = (Vv / np.sqrt(wv)) @ Vv.T
    # S = Ghalf^{⊗} @ M1 @ Gmhalf^{⊗}; free M1 as soon as possible
    T = kron_left(M1.T, Gmhalf, g, nb)
    del M1; gc.collect()
    S = kron_left(T.T, Ghalf, g, nb)
    del T; gc.collect()
    if return_parts:
        return P, idx, W, S, None, Gloc
    return P, idx, W, S

# ---------------------------------------------------------------------------
# dense sector-restricted eigen-solver (symmetric SS^T with projection+deflation)
def sector_eigs_dense(S, projs=(), deflate=(), k_want=1, seed=0, tol=0):
    """Leading eigenvalues of C = sigma(S)^2 on the intersection of sector
    projectors; deflation shifts known eigenvectors to eigenvalue 0.
    Returns (vals (desc), vecs (columns) or None)."""
    N = S.shape[0]
    def matvec(v):
        w = S @ (S.T @ v)
        for P in projs:
            w = P(w)
        for lam, r in deflate:
            # (SS^T - lam r r^T) v = SS^T v - lam (r^T v) r; since r^T SS^T = lam r^T,
            # this equals w - (r^T w) r  (no extra factor!).
            w = w - (r @ w) * r
        return w
    rng = np.random.default_rng(seed)
    v0 = rng.standard_normal(N)
    for P in projs:
        v0 = P(v0)
    for lam, r in deflate:
        v0 = v0 - (r @ v0) * r
    if np.linalg.norm(v0) < 1e-12:
        return np.array([]), None
    v0 /= np.linalg.norm(v0)
    LO = LinearOperator((N, N), matvec=matvec, dtype=np.float64)
    try:
        vals, vecs = eigsh(LO, k=k_want, which='LM', v0=v0, tol=tol,
                           maxiter=10000)
        order = np.argsort(vals)[::-1]
        return vals[order], vecs[:, order]
    except Exception as e:
        print(f"   [sector_eigs_dense] eigsh failed ({e}); power fallback")
        v = v0; lam = -1.0
        for it in range(5000):
            w = matvec(v); nw = np.linalg.norm(w)
            if nw < 1e-300:
                break
            w /= nw
            lam_new = float(v @ matvec(v))
            if abs(lam_new - lam) < 1e-13 * max(abs(lam_new), 1e-300):
                v, lam = w, lam_new
                break
            v, lam = w, lam_new
        return np.array([lam]), v[:, None]

# ---------------------------------------------------------------------------
# product rows + momentum blocks (nb=6 route)
def product_row(W, a_lab, labs, nb, g, form):
    """Row of M1/M2 at configuration a_lab (tuple of nb labels): dense length-N.
    M1[a, tau] = prod_k W[a_k, tau_{k-1}, tau_k];
    M2[a, tau] = prod_k W[a_k, tau_k, tau_{k+1}]."""
    N = labs.shape[0]
    W2 = W.reshape(g, g * g)
    v = np.ones(N)
    if form == 'M1':
        for k in range(nb):
            cols = labs[:, (k - 1) % nb] * g + labs[:, k]
            v *= W2[a_lab[k], cols]
    else:
        for k in range(nb):
            cols = labs[:, k] * g + labs[:, (k + 1) % nb]
            v *= W2[a_lab[k], cols]
    return v

def momentum_orbits(labs, nb, g):
    """Shift-orbits of configurations: list of (rep, orbit(list of flat idx in
    shift order), period)."""
    N = labs.shape[0]
    shifted = np.ravel_multi_index(np.roll(labs, 1, axis=1).T, (g,) * nb)
    seen = np.zeros(N, dtype=bool)
    orbits = []
    for i in range(N):
        if seen[i]:
            continue
        orbit = [i]; seen[i] = True
        j = int(shifted[i])
        while j != i:
            orbit.append(j); seen[j] = True
            j = int(shifted[j])
        orbits.append((i, orbit, len(orbit)))
    return orbits

def momentum_block(W, labs, orbits, nb, g, k, form, rows_cache=None):
    """Momentum-k block of M1 or M2 in the orbit basis
    |k,O> = (1/sqrt(p)) sum_j e^{2 pi i k j/nb}|T^j c>.
    <k,O_a|M|k,O_b> = sqrt(p_a/p_b) sum_{j'<p_b} e^{2 pi i k j'/nb} M[c_a, T^{j'} c_b].
    Vectorized over b per row; rows computed on the fly (no cache: at nb=6 the
    cached rows would need ~3 GB).  Returns (block, included_orbit_indices, cache)."""
    inc = [oi for oi, (rep, orb, per) in enumerate(orbits)
           if abs(np.exp(2j * np.pi * k * per / nb) - 1) < 1e-12]
    # concatenated orbit elements (in (orbit, position) order) + reduceat offsets
    conc = np.concatenate([orbits[oi][1] for oi in inc])          # flat config indices
    pers = np.array([orbits[oi][2] for oi in inc], dtype=float)
    offs = np.concatenate([[0], np.cumsum(pers)]).astype(int)
    js = np.arange(len(conc)) - np.repeat(offs[:-1], pers.astype(int))
    ph = np.exp(2j * np.pi * k * js / nb)
    invsq = 1.0 / np.sqrt(pers)
    dim = len(inc)
    dtype = np.float64 if (k == 0 or 2 * k == nb) else np.complex128
    B = np.zeros((dim, dim), dtype=dtype)
    for ia, oi_a in enumerate(inc):
        rep_a, orb_a, per_a = orbits[oi_a]
        row = product_row(W, tuple(labs[rep_a]), labs, nb, g, form)
        vals = row[conc] * ph
        sums = np.add.reduceat(vals, offs[:-1])
        res = math.sqrt(per_a) * invsq * sums
        B[ia, :] = res.real if dtype == np.float64 else res
        if rows_cache is not None and ia < 0:
            pass
    return B, inc, rows_cache

def block_pair_leading(B1, B2, k_want=8, seed=0):
    """Leading eigenvalues of B1 @ B2 (dense blocks) via eigs on a matvec LO."""
    dim = B1.shape[0]
    if dim == 0:
        return np.array([]), None
    def matvec(v):
        return B1 @ (B2 @ v)
    LO = LinearOperator((dim, dim), matvec=matvec, dtype=B1.dtype)
    rng = np.random.default_rng(seed)
    v0 = rng.standard_normal(dim) + 0j
    try:
        vals, vecs = eigs(LO, k=min(k_want, dim - 2), which='LR', v0=v0,
                          maxiter=20000, tol=1e-12)
    except Exception:
        try:
            vals, vecs = eigs(LO, k=min(k_want, dim - 2), which='LM', v0=v0,
                              maxiter=20000, tol=1e-12)
        except Exception as e:
            print(f"   [block_pair_leading] eigs failed: {e}")
            return np.array([]), None
    vals = np.real(vals[np.abs(np.imag(vals)) < 1e-8])
    order = np.argsort(vals)[::-1]
    return vals[order], (np.real(vecs[:, order]) if vecs is not None else None)
