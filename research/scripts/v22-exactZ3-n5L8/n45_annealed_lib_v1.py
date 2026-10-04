"""General-n annealed replica spectral program (v1) — library.

n=4 with full S_4 colour resolution at larger L, and n=5 (the q=n-Potts
first-order test).  Extends the deposited n3_annealed_lib.py machinery:

  * colour: central (isotypic) idempotents of S_n from character tables
    (hardcoded n=2..5), i.e. the (lambda,mu) blocks of the global
    S_n x S_n replica symmetry, applied FAST in O(N*g^2) through the
    (key, member) bijections of the free left/right regular orbits
    (left key: sigma_1^{-1} sigma_k;  right key: sigma_k sigma_1^{-1}).
  * transfer: an iterative ring matvec for M1/M2 (boundary-carry with a
    pi_0 block loop), which reaches sizes far beyond the dense limit
    (n=4: L=8, N=331776;  n=5: L=6, N=1.7e6).
    M1 v = moveaxis(M2-ring(v), -1, 0) exactly (validated).
  * momentum-k=0 restriction by shift averaging (all leading eigenvalues
    live at k=0, as at n=3).
  * Arnoldi ('LR') leading-eigenvalue extraction with colour classification
    of eigenvectors (the deposited block12 pattern, generalized), plus a
    colour-restricted solve.

Conventions identical to the deposited code (gap_utils.W_tensor with the
Weingarten pinv for n > D;  M2[tau;pi] = prod_k W[tau_k, pi_k, pi_{k+1}],
M1[pi';tau] = prod_k W[pi'_k, tau_{k-1}, tau_k];  flat config index =
ravel(sigma_1..sigma_nb), nb = L/2).

Validation (n45_annealed_validate_v1.py): n=2 vs the Kaufman closed form,
n=3 vs the deposited scan JSON, n=4 vs dense, block completeness/idempotency,
and the p=1 closed-form bond eigenvalue d^2 Gamma(d^2) Gamma(n+1)/Gamma(d^2+n)
(which is 0.4, 0.2, 8/70, 1/14 for n=2..5 at d=2 — a pinv-level check of the
n=5 Weingarten channel).
"""
import sys, os, math
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gap_utils import perms, compose, inv, cycles, W_tensor

# ---------------------------------------------------------------------------
# character tables.  classes: cycle types (sorted, descending); sizes; chars.
CHAR_TABLES = {
    2: {'classes': [(1, 1), (2,)], 'sizes': [1, 1],
        'irreps': [('triv', [1, 1]), ('sgn', [1, -1])]},
    3: {'classes': [(1, 1, 1), (2, 1), (3,)], 'sizes': [1, 3, 2],
        'irreps': [('triv', [1, 1, 1]), ('sgn', [1, -1, 1]),
                   ('std', [2, 0, -1])]},
    4: {'classes': [(1, 1, 1, 1), (2, 1, 1), (2, 2), (3, 1), (4,)],
        'sizes': [1, 6, 3, 8, 6],
        'irreps': [('triv', [1, 1, 1, 1, 1]), ('sgn', [1, -1, 1, 1, -1]),
                   ('std', [3, 1, -1, 0, -1]), ('stdsgn', [3, -1, -1, 0, 1]),
                   ('two', [2, 0, 2, -1, 0])]},
    5: {'classes': [(1, 1, 1, 1, 1), (2, 1, 1, 1), (2, 2, 1), (3, 1, 1),
                    (3, 2), (4, 1), (5,)],
        'sizes': [1, 10, 15, 20, 20, 30, 24],
        'irreps': [('triv', [1, 1, 1, 1, 1, 1, 1]),
                   ('sgn', [1, -1, 1, 1, -1, -1, 1]),
                   ('std', [4, 2, 0, 1, -1, 0, -1]),
                   ('stdsgn', [4, -2, 0, 1, 1, 0, -1]),
                   ('three2', [5, 1, 1, -1, 1, -1, 0]),
                   ('three1', [6, 0, -2, 0, 0, 0, 1]),
                   ('two2', [5, -1, 1, -1, -1, 1, 0])]},
}

def cycle_type(pi):
    n = len(pi); seen = [False] * n; lens = []
    for i in range(n):
        if not seen[i]:
            j = i; c = 0
            while not seen[j]:
                seen[j] = True; j = pi[j]; c += 1
            lens.append(c)
    return tuple(sorted(lens, reverse=True))

def irrep_names(n):
    return [name for name, _ in CHAR_TABLES[n]['irreps']]

def irrep_dims(n):
    return {name: chars[0] for name, chars in CHAR_TABLES[n]['irreps']}

def char_of(n, name, pi):
    tab = CHAR_TABLES[n]
    ci = tab['classes'].index(cycle_type(pi))
    return dict(tab['irreps'])[name][ci]

def central_idempotent(n, name):
    """e_lambda = (d/n!) sum_sigma chi(sigma) sigma  as {perm: coeff}."""
    P = perms(n)
    d = irrep_dims(n)[name]
    nf = math.factorial(n)
    return {s: (d / nf) * char_of(n, name, s) for s in P}

# ---------------------------------------------------------------------------
class FastColour:
    """Applies L(e_lam) R(e_mu) on flat config vectors in O(N*g^2) BLAS.

    Left action a: sigma_k -> a sigma_k (all bonds); free orbits of size n!;
    config <-> (lkey = ravel(sigma_1^{-1}sigma_2,..,sigma_1^{-1}sigma_nb),
                ly = sigma_1);  member y of the orbit of C is (y, y*tau_2, ..).
    Right action b: sigma_k -> sigma_k b;  config <-> (rkey =
    ravel(sigma_2 sigma_1^{-1}, .., sigma_nb sigma_1^{-1}), rz = sigma_1);
    member z is (z, rho_2 z, ..).
    L(e) f[y0] = sum_y e[y y0^{-1}] f[y];   R(e) f[z0] = sum_b e[b] f[z0 b].
    """
    def __init__(self, n, nb, P):
        self.n, self.nb, self.g, self.N = n, nb, len(P), len(P) ** nb
        idx = {s: i for i, s in enumerate(P)}
        invi = np.array([idx[inv(s)] for s in P])
        MT = np.array([[idx[compose(a, b)] for b in P] for a in P])
        self.MT, self.invi, self.idx = MT, invi, idx
        labs = np.array(np.unravel_index(np.arange(self.N),
                                         (self.g,) * nb)).T
        s1 = labs[:, 0]
        lcols = [MT[invi[s1], labs[:, k]] for k in range(1, nb)]
        self.lkey = (np.ravel_multi_index(lcols, (self.g,) * (nb - 1))
                     if nb > 1 else np.zeros(self.N, dtype=np.int64))
        self.ly = s1.astype(np.int64)
        rcols = [MT[labs[:, k], invi[s1]] for k in range(1, nb)]
        self.rkey = (np.ravel_multi_index(rcols, (self.g,) * (nb - 1))
                     if nb > 1 else np.zeros(self.N, dtype=np.int64))
        self.rz = s1.astype(np.int64)
        self._Mcache = {}
        assert len(set(zip(self.lkey.tolist(), self.ly.tolist()))) == self.N
        assert len(set(zip(self.rkey.tolist(), self.rz.tolist()))) == self.N

    def _Ml(self, name):
        if ('L', name) not in self._Mcache:
            e = central_idempotent(self.n, name)
            M = np.zeros((self.g, self.g))
            for a, c in e.items():
                ia = self.idx[a]
                for y0 in range(self.g):
                    M[y0, self.MT[ia, y0]] += c     # y = a y0
            self._Mcache[('L', name)] = M
        return self._Mcache[('L', name)]

    def _Mr(self, name):
        if ('R', name) not in self._Mcache:
            e = central_idempotent(self.n, name)
            M = np.zeros((self.g, self.g))
            for b, c in e.items():
                ib = self.idx[b]
                for z0 in range(self.g):
                    M[z0, self.MT[z0, ib]] += c     # z = z0 b
            self._Mcache[('R', name)] = M
        return self._Mcache[('R', name)]

    def left(self, name, v):
        V = np.zeros((self.g ** max(self.nb - 1, 0), self.g))
        V[self.lkey, self.ly] = v
        V = V @ self._Ml(name).T
        return V[self.lkey, self.ly]

    def right(self, name, v):
        V = np.zeros((self.g ** max(self.nb - 1, 0), self.g))
        V[self.rkey, self.rz] = v
        V = V @ self._Mr(name).T
        return V[self.rkey, self.rz]

    def block(self, lname, rname, v):
        return self.left(lname, self.right(rname, v))

    def block_mass(self, lname, rname, v):
        w = self.block(lname, rname, v)
        return float(np.dot(w, w) / np.dot(v, v))

# ---------------------------------------------------------------------------
# iterative ring transfer matvec
def ring_M2(v_tens, W, beta=8):
    """(M2 v)[tau] = sum_pi prod_{k=0}^{nb-1} W[tau_k, pi_k, pi_{(k+1)%nb}] v[pi].

    v_tens: ndarray shape (g,)*nb.  Boundary-carry with a pi_0 block loop:
      lift   factor 0:    W[tau_0, a, pi_1]      (multiply, no sum)
      step k factor k:    W[tau_k, pi_k, pi_{k+1}]   (sum pi_k), k=1..nb-2
      final  factor nb-1: W[tau_{nb-1}, pi_{nb-1}, a] (sum pi_{nb-1})
    """
    W = np.asarray(W)
    g, nb = W.shape[0], v_tens.ndim
    if nb == 1:
        Wd = W[:, np.arange(g), np.arange(g)]
        return Wd @ v_tens
    out = np.zeros_like(v_tens)
    Wk = np.moveaxis(W, (0, 1, 2), (2, 1, 0))          # (q, p, u)
    for a0 in range(0, g, beta):
        a1 = min(a0 + beta, g)
        b = a1 - a0
        vb = v_tens[a0:a1]                              # (b, pi_1..pi_{nb-1})
        Kl = np.moveaxis(W[:, a0:a1, :], 1, 0)          # (b, tau_0, pi_1)
        Kl = Kl.reshape((b, g, g) + (1,) * max(nb - 2, 0))
        T = Kl * vb[:, None]      # (b, tau_0, pi_1, pi_2..pi_{nb-1})
        for k in range(1, nb - 1):
            # T axes: (b, tau_0..tau_{k-1}, pi_k, pi_{k+1}, pi_{k+2}..)
            #         positions:  0,   1..k,        k+1,   k+2,     k+3..nb
            ntau, nrest = k, nb - 2 - k
            order = ([k + 2] + [0] + list(range(1, k + 1)) +
                     list(range(k + 3, nb + 1)) + [k + 1])
            Tp = T.transpose(tuple(order))              # (q, b, taus, rest, p)
            fshp = Tp.shape
            Tp = Tp.reshape(fshp[0], -1, fshp[-1])      # (q, M, p)
            Tr = np.matmul(Tp, Wk)                      # (q, M, u)
            Tr = Tr.reshape((fshp[0],) + fshp[1:-1] + (fshp[-1],))
            # Tr axes: (q, b, taus..., rest..., u)
            nd = Tr.ndim
            order2 = ([1] + list(range(2, 2 + ntau)) + [nd - 1] + [0] +
                      list(range(2 + ntau, nd - 1)))
            T = Tr.transpose(tuple(order2))             # (b, taus, u, q, rest)
        # final: contract pi_{nb-1} with W[tau_{nb-1}, pi_{nb-1}, a]
        Tm = T.reshape(b, g ** (nb - 1), g)             # (b, A, p)
        Wf = np.moveaxis(W[:, :, a0:a1], (0, 1, 2), (2, 1, 0))  # (b, p, u)
        Tf = np.matmul(Tm, Wf)                          # (b, A, u)
        out += Tf.sum(axis=0).reshape((g,) * nb)
    return out

def ring_M1(v_tens, W, beta=8):
    """M1[pi';tau] = prod_k W[pi'_k, tau_{k-1}, tau_k]  ==  ring_M2 with the
    output axes rotated:  M1 v = moveaxis(ring_M2(v), -1, 0).  Validated."""
    X = ring_M2(v_tens, W, beta=beta)
    return np.ascontiguousarray(np.moveaxis(X, -1, 0))

# ---------------------------------------------------------------------------
def shift_tensor(v_tens, s):
    """Ring translation by s bonds:  (T^s v)[sigma_1..sigma_nb] =
    v[sigma_{1-s}, .., sigma_{nb-s}]  (axis permutation, not value roll)."""
    nb = v_tens.ndim
    order = tuple([(j - s) % nb for j in range(nb)])
    return np.transpose(v_tens, order)

def mom0(v_tens):
    """Projector onto ring momentum k=0 (shift-average over bond labels)."""
    nb = v_tens.ndim
    if nb == 1:
        return v_tens.copy()
    out = v_tens.copy()
    for s in range(1, nb):
        out = out + shift_tensor(v_tens, s)
    return out / nb

def mom_content(v_tens):
    """|<k|v>|^2 / |v|^2 for k=0..nb-1."""
    nb = v_tens.ndim
    v = np.asarray(v_tens, dtype=complex)
    n2 = float(np.real(np.vdot(v, v)))
    if n2 < 1e-300:
        return [0.0] * nb
    out = []
    for k in range(nb):
        w = np.zeros_like(v)
        for s in range(nb):
            w += np.exp(-2j * np.pi * k * s / nb) * shift_tensor(v, s)
        out.append(float(np.real(np.vdot(w, w))) / (nb * nb * n2))
    return out

# ---------------------------------------------------------------------------
class RingOperator:
    """C = M1 M2 on flat config vectors, optionally restricted to ring
    momentum k=0 and/or a colour block (lname, rname)."""
    def __init__(self, n, d, p, nb, beta=8, mom_k0=True, colour=None):
        self.P, self.idx, self.W = W_tensor(n, d, p)
        self.g, self.nb = len(self.P), nb
        self.N = self.g ** nb
        self.n, self.d, self.p = n, d, p
        self.beta, self.mom_k0, self.colour = beta, mom_k0, colour
        self.fc = FastColour(n, nb, self.P)
        self.shape = (self.N, self.N)
        self.dtype = np.float64

    def matvec(self, v):
        vt = np.asarray(v).reshape((self.g,) * self.nb)
        if self.colour is not None:
            vt = self.fc.block(self.colour[0], self.colour[1],
                               vt.reshape(-1)).reshape((self.g,) * self.nb)
        w = ring_M1(ring_M2(vt, self.W, beta=self.beta), self.W,
                    beta=self.beta)
        if self.mom_k0:
            w = mom0(w)
        if self.colour is not None:
            w = self.fc.block(self.colour[0], self.colour[1],
                              w.reshape(-1)).reshape((self.g,) * self.nb)
        return w.reshape(-1)

    def as_linear_operator(self):
        return LinearOperator(self.shape, matvec=self.matvec,
                              dtype=self.dtype)

def leading_eigs(op, k_want=12, v0=None, tol=1e-11, seed=0):
    """Leading real eigenvalues of a RingOperator via Arnoldi ('LR').
    Dense fallback for tiny spaces.  NOTE: ARPACK may undercount the
    multiplicity of highly degenerate multiplets (e.g. the 9-fold std.std
    sigma multiplet at n=4); the VALUES are correct."""
    N = op.N
    if N <= 30:
        A = np.zeros((N, N))
        e = np.eye(N)
        for j in range(N):
            A[:, j] = op.matvec(e[:, j])
        ev = np.linalg.eigvals(A)
        vals = np.real(ev[np.abs(np.imag(ev)) < 1e-9])
        order = np.argsort(vals)[::-1]
        vals = vals[order][:min(k_want, len(vals))]
        return vals, None
    if v0 is None:
        rng = np.random.default_rng(seed)
        v0 = rng.standard_normal(N)
        if op.mom_k0:
            v0 = mom0(v0.reshape((op.g,) * op.nb)).reshape(-1)
    LO = op.as_linear_operator()
    kk = min(k_want, N - 2)
    try:
        vals, vecs = eigs(LO, k=kk, which='LR', v0=v0, tol=tol, maxiter=5000)
    except Exception as e:
        print(f"   [leading_eigs] LR failed ({e}); retrying LM")
        vals, vecs = eigs(LO, k=kk, which='LM', v0=v0, tol=tol, maxiter=5000)
    vals = np.real(vals[np.abs(np.imag(vals)) < 1e-6])
    order = np.argsort(vals)[::-1]
    return vals[order], (np.real(vecs[:, order]) if vecs is not None else None)

def solve_record(n, d, p, nb, k_want=16, blocks=None, v0=None, beta=8,
                 tol=1e-11, want_mom=True):
    """One (p, nb) record: leading k=0 eigenvalues with colour labels.

    Returns dict with lam [(value, block, mass)], lam1, lam_eps (2nd triv),
    lam_sigma (max colour-nontrivial), sigma_block, growth, mom check,
    secs, v0_out (warm start for the next p).
    """
    import time
    t0 = time.time()
    if blocks is None:
        blocks = [('triv', 'triv'), ('sgn', 'sgn'), ('std', 'std')]
    op = RingOperator(n, d, p, nb, beta=beta, mom_k0=True, colour=None)
    vals, vecs = leading_eigs(op, k_want=k_want, v0=v0, tol=tol)
    rec = {'p': p, 'L': 2 * nb, 'n': n, 'd': d, 'lam': []}
    triv, nontriv = [], []
    for j in range(len(vals)):
        if vecs is None:
            rec['lam'].append([float(vals[j]), None, None]); continue
        vj = vecs[:, j]
        nn = np.linalg.norm(vj)
        if nn < 1e-300:
            continue
        masses = {f"{l}.{r}": op.fc.block_mass(l, r, vj / nn)
                  for l, r in blocks}
        best = max(masses, key=masses.get)
        rec['lam'].append([float(vals[j]), best,
                           round(masses[best], 3)])
        if best == 'triv.triv' and masses[best] > 0.5:
            triv.append(float(vals[j]))
        elif masses[best] > 0.5:
            nontriv.append((float(vals[j]), best))
    rec['lam1'] = triv[0] if triv else None
    rec['lam_eps'] = triv[1] if len(triv) > 1 else None
    if nontriv:
        bv, bb = max(nontriv, key=lambda t: t[0])
        rec['lam_sigma'], rec['sigma_block'] = bv, bb
    else:
        rec['lam_sigma'], rec['sigma_block'] = None, None
    if rec['lam1']:
        rec['growth'] = rec['lam1'] ** (1.0 / (2 * nb))
    if want_mom and vecs is not None and vecs.shape[1] > 0:
        vj = vecs[:, 0] / (np.linalg.norm(vecs[:, 0]) + 1e-300)
        rec['mom1'] = [round(x, 4) for x in
                       mom_content(vj.reshape((op.g,) * op.nb))]
    rec['secs'] = round(time.time() - t0, 1)
    rec['v0_out'] = ((vecs[:, 0] / (np.linalg.norm(vecs[:, 0]) + 1e-300))
                     if vecs is not None else None)
    return rec

# ---------------------------------------------------------------------------
def n_repl_pc1_eig(n, d=2):
    """p=1 bond eigenvalue d^2 Gamma(d^2) Gamma(n+1) / Gamma(d^2+n)."""
    from scipy.special import gammaln
    D = d * d
    return float(math.exp(math.log(D) + gammaln(D) + gammaln(n + 1)
                          - gammaln(D + n)))
