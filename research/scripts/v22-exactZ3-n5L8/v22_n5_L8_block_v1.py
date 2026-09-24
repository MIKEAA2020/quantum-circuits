"""v22_n5_L8_block_v1.py -- the n=5 L=8 rung: the exponential-vs-power-law
discriminator, via the symmetry-reduced dense block of C_comp^{(5)}.

THE PROBLEM.  At n = 5, L = 8 the compressed bond-label space is
(S_5)^4 = 120^4 = 2.07e8: an iterative Arnoldi needs several 0.8-1.7 GB
vectors and ~10 min per ring matvec (2*120^6 = 6e12 MACs), i.e. days.
The decisive eigenvalues -- lam1, lam2 of the two-phase gap12 diagnostic
-- live in the momentum-zero colour-trivial (triv.triv, mom0) sector,
whose dimension is the number of orbits of the symmetry group
G = (S_5 x S_5) : Z_nb  (bond-wise relabeling sigma_k -> a sigma_k b,
semidirect with the ring shift) on (S_5)^nb.  This script assembles the
RESTRICTED dense block exactly and diagonalizes it.

THE BASIS.  Left-invariant functions on (S_5)^nb depend only on
lkey = (sigma_1^{-1} sigma_2, ..., sigma_1^{-1} sigma_nb); right
invariance acts by simultaneous conjugation of the lkey tuple; the shift
acts by the rational maps (nb=4):
    s=1: (l2^{-1} l3, l2^{-1} l4, l2^{-1});
    s=2: (l3^{-1} l4, l3^{-1},   l3^{-1} l2);
    s=3: (l4^{-1},   l4^{-1} l2, l4^{-1} l3).
The G-canonical form = min over (c in S_5, s) of the encoded conjugated
shifted lkey tuple (an exact canonical form: the min is an element of the
orbit's image set, so distinct orbits have distinct minima).  Orbit
indicators w_beta = 1[orbit]/sqrt(|orbit|) give the basis, and
    B[alpha, beta] = (1/sqrt(n_alpha n_beta)) * sum_{tau in O_beta}
                     M[rep_alpha, tau]
assembled by a chunked pass (bincount/segment-sum of the row values by
canonical id).  M1 and M2 are relabel- and shift-equivariant (the W
channel of Eq. (Wpn) is bi-invariant), so the restriction is exact and
C_block = B_M1 @ B_M2 has the exact mom0 triv.triv spectrum.

VALIDATION: nb = 2 blocks vs the deposited n=5 L=4 scan (triv3), and
nb = 2, 3 vs fresh unrestricted colour-restricted Arnoldi solves (the
deposited n45_annealed route).

Phases: ids (canonical-id table at nb=4, p-independent, memmapped),
validate, run (L=8 p-grid, checkpointed).
"""
import sys, os, json, math, time, argparse, fcntl
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'v18-n4n5-smc'))
sys.path.insert(0, os.path.join(HERE, '..', 'v19-n5L6-nofreeze'))
from gap_utils import W_tensor, perms, compose, inv, cycles
from n45_annealed_lib_v1 import RingOperator, leading_eigs

OUT = os.path.join(HERE, '..', '..', 'results', 'v22-exactZ3-n5L8')
TMP = os.path.join(OUT, 'tmp_n5L8block')
os.makedirs(TMP, exist_ok=True)

P5 = perms(5)
G5 = len(P5)
IDX5 = {s: i for i, s in enumerate(P5)}
INV5 = np.array([IDX5[inv(s)] for s in P5])
MT5 = np.array([[IDX5[compose(a, b)] for b in P5] for a in P5])
CONJ5 = np.array([[MT5[c][MT5[t][INV5[c]]] for t in range(G5)]
                  for c in range(G5)])


def log(*a):
    print(*a, flush=True)


def _ckpt_write(ckpt, p, row):
    """Race-safe rung-checkpoint write.

    Two run segments launched in the same driving window can complete in
    that same window; each process loaded `rows` once at ITS start, so the
    later json.dump clobbered the earlier point's entry (lost update,
    observed 2026-09-25 02:42: p=0.46's completed entry was overwritten by
    p=0.44's).  Fix: under an exclusive flock, RE-READ the file fresh,
    merge by p, dump to a temp file and os.replace (atomic for readers).
    Deterministic per-point physics is untouched -- this only hardens the
    checkpoint protocol.
    """
    lockf = open(ckpt + '.lock', 'w')
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX)
        cur = json.load(open(ckpt)) if os.path.exists(ckpt) else []
        merged = {round(r['p'], 4): r for r in cur}
        merged[round(p, 4)] = row
        tmp = ckpt + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(list(merged.values()), f, indent=1)
        os.replace(tmp, ckpt)
    finally:
        fcntl.flock(lockf, fcntl.LOCK_UN)
        lockf.close()


def shift_lkeys(ls, s, nb):
    """Shifted lkey tuple: (T^s sigma)_1^{-1} (T^s sigma)_k =
    l_{1+s}^{-1} l_{k+s}  (cyclic, l_1 = e)."""
    if s == 0:
        return ls

    def lk(j):
        return 0 if j == 1 else ls[j - 2]
    out = []
    for k in range(2, nb + 1):
        j1 = ((s) % nb) + 1
        jk = ((k - 1 + s) % nb) + 1
        out.append(MT5[INV5[lk(j1)], lk(jk)])
    return out


def canonical_ids_chunk(digs, nb):
    """(relabel x shift)-canonical encoded lkey id per config (int64)."""
    s1 = digs[:, 0]
    s1i = INV5[s1]
    ls = [MT5[s1i, digs[:, k]] for k in range(1, nb)]
    m = nb - 1
    best = None
    for s in range(nb):
        lshift = shift_lkeys(ls, s, nb) if s else ls
        for c in range(G5):
            cc = CONJ5[c]
            e = np.int64(cc[lshift[0]])
            for j in range(1, m):
                e = e * G5 + cc[lshift[j]]
            if best is None:
                best = e.copy()
            else:
                np.minimum(best, e, out=best)
    return best


def decode_rep(u, nb):
    r = []
    u = int(u)
    for j in range(nb - 1):
        r.append(int(u % G5))
        u //= G5
    r.reverse()
    return [0] + r        # sigma_1 = e;  sigma_{k+1} = l_{k+1}


def orbit_table(nb, chunk=200_000, state_path=None, save_every=0):
    """Full pass over (S_5)^nb.  Returns (ids (int32, memmap for nb=4),
    reps (K,nb), counts (K,), K).

    state_path/save_every: optional chunk-level checkpoint/resume for the
    big (memmap) tables.  The cron-era sandbox reaps background processes,
    so the ~780 s nb=4 ids pass cannot survive a single 520 s foreground
    driving window; the checkpoint makes every window RESUME the scan
    exactly.  The first-appearance traversal is deterministic, so a
    resumed pass yields a table identical to an uninterrupted one; the
    state file is removed at completion."""
    N = G5 ** nb
    big = N * 4 > 400_000_000
    ids_path = os.path.join(TMP, f'ids_nb{nb}.npy')
    reps_path = os.path.join(TMP, f'reps_nb{nb}.npy')
    if big and os.path.exists(ids_path) and os.path.exists(reps_path):
        ids = np.load(ids_path, mmap_mode='r')
        reps = np.load(reps_path)
        counts = np.load(os.path.join(TMP, f'counts_nb{nb}.npy'))
        return ids, reps, counts, len(reps)
    # a partial ids memmap from a killed pre-checkpoint attempt must NOT
    # hit the fast path (reps file absent => incomplete => fall through)
    resuming = bool(big and state_path and os.path.exists(state_path)
                    and os.path.exists(ids_path))
    seen = {}
    reps = []
    t0 = time.time()
    if big:
        ids = np.lib.format.open_memmap(
            ids_path, mode='r+' if resuming else 'w+',
            dtype=np.int32, shape=(N,))
    else:
        ids = np.empty(N, dtype=np.int32)
    cnt = np.zeros(1 << 20, dtype=np.int64)
    K = 0
    ci_start = 0
    if resuming:
        try:
            st = np.load(state_path)
            if int(st['chunk']) == chunk:
                seen = {int(k): int(v)
                        for k, v in zip(st['skey'], st['sval'])}
                reps = [list(map(int, r)) for r in st['reps']]
                K = len(reps)
                cnt[:K] = st['cnt']
                ci_start = int(st['ci']) + 1
                log(f"   [ids nb={nb}] RESUMED at chunk {ci_start + 1} "
                    f"(K={K}, state {time.strftime('%H:%M:%S', time.localtime(float(st['ts'])))})")
            else:
                resuming = False
                log(f"   [ids nb={nb}] stale state file ignored")
        except Exception as e:
            resuming = False
            seen = {}
            reps = []
            K = 0
            log(f"   [ids nb={nb}] unreadable state ({e}) — starting fresh")
    for ci, i0 in enumerate(range(0, N, chunk)):
        if ci < ci_start:
            continue
        i1 = min(i0 + chunk, N)
        c = np.arange(i0, i1, dtype=np.int64)
        digs = np.empty((i1 - i0, nb), dtype=np.int64)
        for k in range(nb - 1, -1, -1):
            digs[:, k] = c % G5
            c //= G5
        enc = canonical_ids_chunk(digs, nb)
        uq, invi = np.unique(enc, return_inverse=True)
        loc = np.empty(len(uq), dtype=np.int64)
        for j, u in enumerate(uq.tolist()):
            o = seen.get(u)
            if o is None:
                o = K
                seen[u] = o
                reps.append(decode_rep(u, nb))
                K += 1
            loc[j] = o
        orb = loc[invi].astype(np.int32)
        ids[i0:i1] = orb
        bc = np.bincount(orb, minlength=K)
        if K > len(cnt):
            cnt = np.pad(cnt, (0, K - len(cnt)))
        cnt[:K] += bc
        if (i0 // chunk) % 10 == 0:
            log(f"      [ids nb={nb}] {i1}/{N}: K={K} "
                f"({time.time()-t0:.0f}s)")
        if save_every and big and state_path and ci % save_every == 0:
            ids.flush()
            tmpf = state_path + '.tmp.npy'
            with open(tmpf, 'wb') as fh:
                np.savez(fh, ci=ci, K=K, chunk=chunk, ts=time.time(),
                         skey=np.array(list(seen.keys()), dtype=np.int64),
                         sval=np.array(list(seen.values()), dtype=np.int32),
                         reps=np.array(reps, dtype=np.int64),
                         cnt=cnt[:K].copy())
            os.replace(tmpf, state_path)
    reps = np.array(reps, dtype=np.int64)
    counts = cnt[:K].copy()
    if big:
        ids.flush()
        del ids
        ids = np.load(ids_path, mmap_mode='r')
    np.save(reps_path, reps)
    np.save(os.path.join(TMP, f'counts_nb{nb}.npy'), counts)
    if state_path and os.path.exists(state_path):
        os.remove(state_path)
    log(f"   [ids nb={nb}] K = {K} orbits ({time.time()-t0:.0f}s)")
    return ids, reps, counts, K


# ---------------------------------------------------------------------------
def assemble_block(n, d, p, nb, ids, reps, counts, K, chunk=125_000,
                   dtype=np.float64, progress_every=8, R=64,
                   state_path=None, save_every=0):
    """B_M1, B_M2 (K x K) in the orbit basis (exact restriction).

    state_path/save_every: optional chunk-level checkpointing.  The cron-era
    sandbox reaps background processes a few minutes after launch, so the
    run phase is driven in FOREGROUND segments by the watcher; the partial
    B1/B2 and the chunk cursor survive across segments (atomic save via
    .tmp + os.replace).  The arithmetic is IDENTICAL either way."""
    P, idx, W = W_tensor(n, d, p)
    g = len(P)
    Wf = np.ascontiguousarray(W.reshape(g, g * g), dtype=dtype)
    N = g ** nb
    B1 = np.zeros((K, K), dtype=dtype)
    B2 = np.zeros((K, K), dtype=dtype)
    # B[alpha, beta] = sqrt(n_alpha/n_beta) * S[alpha, beta], with
    # S[alpha,beta] = sum_{tau' in O_beta} M[rep_alpha, tau']  (the raw
    # orbit-binned row sums).  Derivation: the equivariance relation
    # M[U_k x, z] = M[x, U_k^{-1} z] gives
    #   <w_a|M|w_b> = (1/sqrt(n_a n_b)) sum_{tau in O_a, tau' in O_b}
    #                 M[tau, tau']
    #               = (n_a/sqrt(n_a n_b)) sum_{tau' in O_b} M[rep_a, tau']
    #               = sqrt(n_a/n_b) S[a, b];
    # sanity M = I: S = delta => B = delta.
    sqrtc = counts.astype(dtype) ** 0.5
    norm = np.outer(sqrtc, 1.0 / sqrtc)
    t0 = time.time()
    nch = (N + chunk - 1) // chunk
    ci_start = 0
    if state_path and os.path.exists(state_path):
        try:
            st = np.load(state_path)
            if int(st['K']) == K and abs(float(st['p']) - p) < 1e-9 \
                    and int(st['chunk']) == chunk:
                B1[:] = st['b1']
                B2[:] = st['b2']
                ci_start = int(st['ci']) + 1
                log(f"   [block p={p}] RESUMED at chunk {ci_start + 1}/{nch} "
                    f"(state {time.strftime('%H:%M:%S', time.localtime(float(st['ts'])))})")
            else:
                log(f"   [block p={p}] stale state file ignored")
        except Exception as e:
            log(f"   [block p={p}] unreadable state ({e}) — starting fresh")
    for ci, i0 in enumerate(range(0, N, chunk)):
        if ci < ci_start:
            continue
        i1 = min(i0 + chunk, N)
        C = i1 - i0
        c = np.arange(i0, i1, dtype=np.int64)
        digs = np.empty((C, nb), dtype=np.int64)
        for k in range(nb - 1, -1, -1):
            digs[:, k] = c % g
            c //= g
        cols1 = [digs[:, (k - 1) % nb] * g + digs[:, k] for k in range(nb)]
        cols2 = [digs[:, k] * g + digs[:, (k + 1) % nb]
                 for k in range(nb)]
        A1 = [np.ascontiguousarray(Wf[:, cols1[k]]) for k in range(nb)]
        A2 = [np.ascontiguousarray(Wf[:, cols2[k]]) for k in range(nb)]
        orb = np.asarray(ids[i0:i1])
        order = np.argsort(orb, kind='stable')
        orb_s = orb[order]
        bounds = np.searchsorted(orb_s, np.arange(K + 1))
        starts = bounds[:-1]
        # orbit ids are assigned by FIRST APPEARANCE in the space scan, so a
        # chunk (a narrow slice of (S_5)^nb) can miss the high ids entirely:
        # for every orbit k absent from this chunk searchsorted gives
        # bounds[k] == C, and np.add.reduceat raises IndexError for indices
        # >= C (hit at nb=4, chunk 0: 125000 out-of-bounds).  Keep only the
        # orbits present in the chunk; absent ones contribute exactly 0
        # (what the old seg[:, empty] = 0.0 patch meant, now structural).
        nemp = np.flatnonzero(starts < bounds[1:])
        starts_nz = starts[nemp]      # strictly increasing, all < C
        for r0 in range(0, K, R):
            r1 = min(r0 + R, K)
            rb = reps[r0:r1]
            for Bm, A in ((B1, A1), (B2, A2)):
                vals = np.ones((r1 - r0, C), dtype=dtype)
                for k in range(nb):
                    vals *= A[k][rb[:, k]]
                vso = vals[:, order]
                seg = np.zeros((r1 - r0, K), dtype=dtype)
                if nemp.size:
                    seg[:, nemp] = np.add.reduceat(vso, starts_nz, axis=1)
                Bm[r0:r1] += seg
        if ci % progress_every == 0:
            el = time.time() - t0
            log(f"      [block p={p}] chunk {ci+1}/{nch}  {el:.0f}s  "
                f"(eta {el/(ci+1)*(nch-ci-1):.0f}s)")
        if state_path and save_every and (ci % save_every == 0 or ci == nch - 1):
            tmpf = state_path + '.tmp.npy'
            with open(tmpf, 'wb') as fh:
                np.savez(fh, b1=B1, b2=B2, ci=ci, p=p, K=K,
                         chunk=chunk, ts=time.time())
            os.replace(tmpf, state_path)
    B1 *= norm
    B2 *= norm
    return B1, B2


def block_eigs(B1, B2, k_want=6):
    C = B1 @ B2
    ev = np.linalg.eigvals(C)
    ev = np.real(ev[np.abs(np.imag(ev)) < 1e-6 * (1 + np.abs(ev))])
    ev = np.sort(ev)[::-1]
    return ev[:k_want]


def fresh_reference(n, d, p, nb, k_want=4):
    op = RingOperator(n, d, p, nb, beta=16, mom_k0=True,
                      colour=('triv', 'triv'))
    vals, _ = leading_eigs(op, k_want=k_want, tol=1e-10)
    return vals


# ---------------------------------------------------------------------------
def phase_ids(args):
    log("== phase ids: canonical orbit table at nb=4 (p-independent) ==")
    # checkpoint/resume: the ~780 s pass exceeds one 520 s driving window;
    # the state carries (ci, seen, reps, cnt) so every window resumes exactly
    orbit_table(4, state_path=os.path.join(TMP, 'ids_nb4_state.npz'),
                save_every=100)


def phase_validate(args):
    log("== phase validate: blocks vs deposited + unrestricted route ==")
    dep = {round(r['p'], 4): r['triv3'] for r in json.load(open(
        os.path.join(HERE, '..', '..', 'results', 'v18-n4n5-smc',
                     'n5_annealed_scan_v1.json')))}
    ok_all = True
    for nb, p in [(2, 0.44), (2, 0.32), (3, 0.44), (3, 0.47)]:
        ids, reps, counts, K = orbit_table(nb)
        B1, B2 = assemble_block(5, 2, p, nb, ids, reps, counts, K)
        ev = block_eigs(B1, B2, k_want=4)
        msg = f"   nb={nb} p={p}: K={K}  block "
        msg += f"{[f'{float(x):.10f}' for x in ev[:3]]}"
        ref = dep.get(round(p, 4)) if nb == 2 else None
        if ref is not None:
            errs = [abs(float(ev[i]) - ref[i]) / abs(ref[i])
                    for i in range(min(len(ev), len(ref)))]
            ok = max(errs) < 1e-6
            ok_all &= ok
            msg += (f"  vs deposited {ref[:3]}  max rel {max(errs):.2e}"
                    f"  [{'OK' if ok else 'FAIL'}]")
        else:
            try:
                rr = fresh_reference(5, 2, p, nb, k_want=4)
                errs = [abs(float(ev[i]) - float(rr[i])) / abs(float(rr[i]))
                        for i in range(min(len(ev), len(rr)))]
                ok = max(errs) < 1e-6
                ok_all &= ok
                msg += (f"  vs unrestricted {[f'{float(x):.10f}' for x in rr[:3]]}"
                        f"  max rel {max(errs):.2e}  "
                        f"[{'OK' if ok else 'FAIL'}]")
            except Exception as e:
                msg += f"  (ref failed: {e})"
        log(msg)
    log(f"   VALIDATION {'PASS' if ok_all else 'FAIL'}")


def phase_run(args):
    log("== phase run: the n=5 L=8 rung ==")
    pgrid = [float(x) for x in args.pgrid.split(',')]
    ids = np.load(os.path.join(TMP, 'ids_nb4.npy'), mmap_mode='r')
    reps = np.load(os.path.join(TMP, 'reps_nb4.npy'))
    counts = np.load(os.path.join(TMP, 'counts_nb4.npy'))
    K = len(reps)
    log(f"   K = {K} orbits; grid {pgrid}")
    ckpt = f'{OUT}/v22_n5_L8_rung.json'
    rows = json.load(open(ckpt)) if os.path.exists(ckpt) else []
    done = {round(r['p'], 4) for r in rows}
    for p in pgrid:
        if round(p, 4) in done:
            continue
        t0 = time.time()
        # chunk=25k + R=512: peak anon ~0.85 GB (the 4 GiB cgroup shared
        # with the dev server; the 125k profile OOM'd once) and the r-loop
        # re-streams A ~8x less.  state_path makes the assembly RESUMABLE
        # at chunk granularity: the cron-era sandbox reaps background
        # processes, so the watcher drives the run in foreground segments
        # (see followup_v23.sh driving mode); arithmetic is identical.
        B1, B2 = assemble_block(5, 2, p, 4, ids, reps, counts, K,
                                chunk=25_000, R=512,
                                state_path=os.path.join(
                                    TMP, f'run_nb4_p{round(p, 4):.4f}_state.npz'),
                                save_every=8)
        ev = block_eigs(B1, B2, k_want=6)
        gap12 = math.log(ev[0] / ev[1]) if ev[1] > 0 else None
        row = {'p': p, 'L': 8, 'n': 5, 'K': int(K),
               'triv6': [float(x) for x in ev],
               'lam1': float(ev[0]), 'lam2': float(ev[1]),
               'gap12': gap12, 'growth': float(ev[0]) ** (1.0 / 8),
               'secs': round(time.time() - t0, 1)}
        _ckpt_write(ckpt, p, row)
        try:  # the chunk-state file for this point is obsolete now
            os.remove(os.path.join(
                TMP, f'run_nb4_p{round(p, 4):.4f}_state.npz'))
        except OSError:
            pass
        log(f"   p={p}: lam1={ev[0]:.8e} lam2={ev[1]:.8e} "
            f"gap12={gap12:.5f}  [{row['secs']}s]")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['ids', 'validate', 'run', 'all'])
    ap.add_argument('--pgrid', default='0.47')
    args = ap.parse_args()
    {'ids': phase_ids, 'validate': phase_validate,
     'run': phase_run}[args.phase](args)
