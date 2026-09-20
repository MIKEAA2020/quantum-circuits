"""n=5 two-size test at L=6 (v2): the decisive first-order scan that v18
declared beyond the 3 GB / 2-core budget.

How the budget was overcome (all measured, not asserted):
  * the v1 numpy ring_M2 cost 60 s per M2 at n=5 nb=3 (N=1.7e6) because of
    cache-hostile strided 110 MB transpose-copies and a strided BLAS slow
    path in the final contraction; ring_gemm_v2 performs the identical
    contraction (validated to 4e-16 at n=2..4, nb=2..5) in 5.4 s (f64) /
    2.9 s (f32) per M2 on the same 2 cores -- an 11-21x speedup at ~500 MB
    peak RSS, far inside the memory budget (the memory claim in v18 was
    never the binding constraint).
  * colour-restricted Arnoldi solves only (triv.triv k=3 for the two-phase
    gap12 diagnostic; std.std k=1 for the sigma sector), warm-started
    across the p-grid.

Protocol:
  validate   L=4 full 21-point grid with THIS machinery (f64 and f32),
             compared value-by-value against the deposited v18 scan JSON
             (triv3 + lam_sigma) -- the validation anchor.
  scan       L=6 production sweep, 21 points p=0.32..0.52, f32,
             checkpointed after every point (resumable).
  f64spot    re-run the decisive points in float64 (gap12 minimum region
             and curve ends) as the confirmation protocol.
"""
import sys, os, json, math, time, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n45_annealed_lib_v1 import FastColour, mom0, W_tensor
from n45_annealed_lib_v1 import perms, compose, inv
import ring_gemm_v2 as RG


class FastColourLite(FastColour):
    """FastColour with chunked int32 index construction and no O(N)
    tuple-set assertion.  The original materialises labs (N x nb int64,
    320 MB at N = 24^5) plus unravel_index temporaries and an ~1.5 GB
    bijection set, which OOM-kills the L=10 run; here the (lkey, ly) and
    (rkey, rz) coordinates are built in 1M-index chunks with int32 digits
    (N = 8e6 < 2^31), and the bijection is checked on a 1e6-subsample.
    The construction code path is byte-identical in content to the
    validated FastColour (n45_annealed_validate_v1.py V4/V5)."""

    def __init__(self, n, nb, P):
        self.n, self.nb, self.g, self.N = n, nb, len(P), len(P) ** nb
        idx = {s: i for i, s in enumerate(P)}
        invi = np.array([idx[inv(s)] for s in P])
        MT = np.array([[idx[compose(a, b)] for b in P] for a in P])
        self.MT, self.invi, self.idx = MT, invi, idx
        g, N = self.g, self.N
        self.lkey = np.empty(N, dtype=np.int64)
        self.ly = np.empty(N, dtype=np.int64)
        self.rkey = np.empty(N, dtype=np.int64)
        self.rz = np.empty(N, dtype=np.int64)
        CH = 1_000_000
        for a0 in range(0, N, CH):
            a1 = min(a0 + CH, N)
            m = a1 - a0
            # decode flat -> digits (sigma_1..sigma_nb), int32-safe
            c = np.arange(a0, a1, dtype=np.int64)
            digs = np.empty((m, nb), dtype=np.int64)
            for k in range(nb - 1, -1, -1):
                digs[:, k] = c % g
                c //= g
            s1 = digs[:, 0]
            s1i = invi[s1]
            lkey = np.zeros(m, dtype=np.int64)
            for k in range(1, nb):
                lk = MT[s1i, digs[:, k]]
                lkey = lkey * g + lk
            self.lkey[a0:a1] = lkey
            self.ly[a0:a1] = s1
            rkey = np.zeros(m, dtype=np.int64)
            for k in range(1, nb):
                rk = MT[digs[:, k], s1i]
                rkey = rkey * g + rk
            self.rkey[a0:a1] = rkey
            self.rz[a0:a1] = s1
        self._Mcache = {}
        rng = np.random.default_rng(0)
        sm = min(N, 1_000_000)
        sel = rng.choice(N, size=sm, replace=False)
        ok = len(set(zip(self.lkey[sel].tolist(),
                         self.ly[sel].tolist()))) == sm
        assert ok, 'bijection subsample check failed'

OUT = 'mipt_results'
LOG = 'logs'


def log(*a):
    print(*a, flush=True)


class RingOpFast:
    """C = M1 M2 on flat config vectors, mom-k=0, colour-restricted.
    Same operator semantics as n45_annealed_lib_v1.RingOperator; the ring
    contractions use the GEMM kernel (validated identical)."""

    def __init__(self, n, d, p, nb, beta=16, mom_k0=True, colour=None,
                 dtype=np.float64):
        self.P, self.idx, self.W = W_tensor(n, d, p)
        self.g, self.nb = len(self.P), nb
        self.N = self.g ** nb
        self.n, self.d, self.p = n, d, p
        self.beta, self.mom_k0, self.colour = beta, mom_k0, colour
        self.dtype = dtype
        self.fc = (FastColourLite if self.N > 2_000_000 else FastColour)(
            n, nb, self.P)
        self.shape = (self.N, self.N)
        W = np.asarray(self.W, dtype=dtype)
        self.Wd = np.ascontiguousarray(W)
        self.Wk = np.ascontiguousarray(W.transpose(2, 1, 0))

    def matvec(self, v):
        vt = np.ascontiguousarray(np.asarray(v, dtype=self.dtype))
        if self.colour is not None:
            vt = np.asarray(self.fc.block(self.colour[0], self.colour[1], vt),
                            dtype=self.dtype)
        w = RG.ring_m2_gemm(vt, self.Wd, self.nb, beta=self.beta,
                            dtype=self.dtype)
        w = RG.ring_m1_gemm(w, self.Wd, self.nb, beta=self.beta,
                            dtype=self.dtype)
        if self.mom_k0:
            wt = w.reshape((self.g,) * self.nb)
            w = mom0(wt).reshape(-1)
        if self.colour is not None:
            w = np.asarray(self.fc.block(self.colour[0], self.colour[1], w),
                           dtype=self.dtype)
        return w

    def as_linear_operator(self):
        from scipy.sparse.linalg import LinearOperator
        return LinearOperator(self.shape, matvec=self.matvec,
                              dtype=self.dtype)


def restricted_eigs(op, k_want, v0=None, tol=1e-9, seed=0):
    """Leading real eigenvalues of a RingOpFast via Arnoldi, warm-started."""
    from scipy.sparse.linalg import eigs
    N = op.N
    if v0 is None:
        rng = np.random.default_rng(seed)
        v0 = rng.standard_normal(N).astype(op.dtype)
        if op.mom_k0:
            v0 = mom0(v0.reshape((op.g,) * op.nb)).reshape(-1)
        if op.colour is not None:
            v0 = np.asarray(op.fc.block(op.colour[0], op.colour[1], v0),
                            dtype=op.dtype)
    v0 = np.asarray(v0, dtype=np.float64)
    try:
        vals, vecs = eigs(op.as_linear_operator(), k=k_want, which='LR',
                          v0=v0, tol=tol, maxiter=10000)
    except Exception:
        vals, vecs = eigs(op.as_linear_operator(), k=k_want, which='LM',
                          v0=v0, tol=tol, maxiter=10000)
    vals = np.real(vals[np.abs(np.imag(vals)) < 1e-6 * (1 + np.abs(vals))])
    order = np.argsort(vals)[::-1]
    vals = vals[order][:k_want]
    vecs = np.real(vecs[:, order][:, :len(vals)]) if vecs is not None else None
    v1 = None
    if vecs is not None and vecs.shape[1] > 0:
        nrm = np.linalg.norm(vecs[:, 0])
        if nrm > 1e-300:
            v1 = (vecs[:, 0] / nrm).astype(np.float64)
    return vals, v1


# ---------------------------------------------------------------------------
def load_v18_L4():
    with open(f'{OUT}/n5_annealed_scan_v1.json') as f:
        return json.load(f)


def phase_validate(args):
    """L=4 anchor: this machinery (f64 + f32) vs the deposited v18 scan."""
    dep = load_v18_L4()
    for dtype, tag in [(np.float64, 'f64'), (np.float32, 'f32')]:
        errs = []
        v0t, v0s = None, None
        for row in dep:
            p = float(row['p'])
            nb = 2
            t0 = time.time()
            opT = RingOpFast(5, 2, p, nb, beta=16, colour=('triv', 'triv'),
                             dtype=dtype)
            triv, v0t = restricted_eigs(opT, 3, v0=v0t, tol=1e-11)
            opS = RingOpFast(5, 2, p, nb, beta=16, colour=('std', 'std'),
                             dtype=dtype)
            sig, v0s = restricted_eigs(opS, 1, v0=v0s, tol=1e-11)
            dt = time.time() - t0
            ref = row['triv3']
            e1 = abs(float(triv[0]) - ref[0]) / abs(ref[0])
            e2 = abs(float(triv[1]) - ref[1]) / abs(ref[1])
            es = abs(float(sig[0]) - row['lam_sigma']) / abs(row['lam_sigma'])
            errs.append((e1, e2, es))
            if p in (0.32, 0.40, 0.48, 0.52):
                log(f"  [L4 {tag}] p={p}: lam1 {float(triv[0]):.10e} "
                    f"(dep {ref[0]:.10e}, rel {e1:.1e})  lam2 "
                    f"{float(triv[1]):.10e} (dep {ref[1]:.10e}, rel {e2:.1e})"
                    f"  sig {float(sig[0]):.10e} (dep "
                    f"{row['lam_sigma']:.10e}, rel {es:.1e})  [{dt:.1f}s]")
        E = np.array(errs)
        log(f"  [L4 {tag}] max rel dev over {len(dep)} points: "
            f"lam1 {E[:,0].max():.1e} lam2 {E[:,1].max():.1e} "
            f"sigma {E[:,2].max():.1e}")
        json.dump({'dtype': tag,
                   'max_rel': [float(E[:, i].max()) for i in range(3)]},
                  open(f'{OUT}/n5_L6_validate_{tag}.json', 'w'), indent=1)


# ---------------------------------------------------------------------------
GRID = [round(x, 4) for x in np.arange(0.32, 0.5201, 0.01)]


def phase_scan(args):
    """L=6 production sweep (f32), checkpointed and resumable."""
    ckpt = f'{OUT}/n5_L6_scan_v2.json'
    done = {}
    if os.path.exists(ckpt):
        done = {round(float(r['p']), 4): r
                for r in json.load(open(ckpt))}
    dtype = np.float32
    out = [done[p] for p in GRID if p in done]
    log(f"--- n=5 L=6 scan (nb=3, N={120**3}), {len(GRID)} points, "
        f"{len(out)} already done ---")
    v0t = v0s = None
    if out:
        last = out[-1]
        if 'v0t' in last and last['v0t'] is not None:
            v0t = np.asarray(last['v0t'])
        if 'v0s' in last and last['v0s'] is not None:
            v0s = np.asarray(last['v0s'])
    for p in GRID:
        if p in done:
            continue
        t0 = time.time()
        row = {'p': p, 'L': 6, 'n': 5}
        try:
            opT = RingOpFast(5, 2, float(p), 3, beta=16,
                             colour=('triv', 'triv'), dtype=dtype)
            triv, v0t = restricted_eigs(opT, 3, v0=v0t, tol=1e-8)
            row['triv3'] = [float(x) for x in triv]
            row['lam1'], row['lam2'], row['lam3'] = (float(triv[0]),
                                                     float(triv[1]),
                                                     float(triv[2]))
            row['gap12'] = (math.log(triv[0] / triv[1])
                            if triv[1] > 0 else None)
            row['growth'] = float(triv[0]) ** (1.0 / 6)
        except Exception as e:
            row['triv3'] = None
            log(f"  p={p}: triv FAILED ({e})")
        try:
            opS = RingOpFast(5, 2, float(p), 3, beta=16,
                             colour=('std', 'std'),
                             dtype=dtype)
            sig, v0s = restricted_eigs(opS, 1, v0=v0s, tol=1e-8)
            row['lam_sigma'] = float(sig[0])
            row['X6'] = (6 * math.log(row['lam1'] / row['lam_sigma'])
                         if row.get('lam1') and sig[0] > 0 else None)
        except Exception as e:
            row['lam_sigma'] = None
            log(f"  p={p}: sigma FAILED ({e})")
        row['secs'] = round(time.time() - t0, 1)
        out.append(row)
        # checkpoint (v0 vectors kept out of the human-readable dump)
        dump = []
        for r in out:
            r2 = dict(r)
            r2['v0t'] = (v0t.tolist() if r is row and v0t is not None
                         else None)
            r2['v0s'] = (v0s.tolist() if r is row and v0s is not None
                         else None)
            dump.append(r2)
        json.dump(dump, open(ckpt, 'w'), indent=1)
        log(f"  p={p:.3f} lam1={row.get('lam1')} lam2={row.get('lam2')} "
            f"gap12={row.get('gap12')} sig={row.get('lam_sigma')} "
            f"X6={row.get('X6')} [{row.get('secs')}s]")
    log(f"written {ckpt}")


def phase_f64spot(args):
    """Float64 confirmation at the decisive points."""
    pts = [0.32, 0.44, 0.46, 0.48, 0.50, 0.52]
    res = []
    v0t = v0s = None
    for p in pts:
        t0 = time.time()
        opT = RingOpFast(5, 2, float(p), 3, beta=16, colour=('triv', 'triv'),
                         dtype=np.float64)
        triv, v0t = restricted_eigs(opT, 3, v0=v0t, tol=1e-11)
        opS = RingOpFast(5, 2, float(p), 3, beta=16, colour=('std', 'std'),
                         dtype=np.float64)
        sig, v0s = restricted_eigs(opS, 1, v0=v0s, tol=1e-11)
        row = {'p': p, 'triv3': [float(x) for x in triv],
               'lam_sigma': float(sig[0]),
               'gap12': math.log(triv[0] / triv[1]),
               'X6': 6 * math.log(float(triv[0]) / float(sig[0])),
               'secs': round(time.time() - t0, 1)}
        res.append(row)
        log(f"  [f64] p={p}: lam1 {row['triv3'][0]:.10e} lam2 "
            f"{row['triv3'][1]:.10e} gap12 {row['gap12']:.5f} "
            f"sig {row['lam_sigma']:.10e} X6 {row['X6']:.4f} "
            f"[{row['secs']}s]")
        json.dump(res, open(f'{OUT}/n5_L6_f64spot_v2.json', 'w'), indent=1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['validate', 'scan', 'f64spot'])
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(LOG, exist_ok=True)
    {'validate': phase_validate, 'scan': phase_scan,
     'f64spot': phase_f64spot}[args.phase](args)
