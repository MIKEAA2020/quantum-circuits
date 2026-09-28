"""v25_n5_L8_ext_v1.py -- the v25 extension compute: (a) the d=3 rung at
n=5, L=8, (b) the finer d=2 locator grid at L=8, (c) the d=3 locator scans
at L=4/L=6 (which also supply the d=3 size-ladder rows at small L).

The whole heavy machinery is REUSED from v22_n5_L8_block_v1 (imported, never
modified): the canonical orbit table ids/reps/counts at nb=4 is p- AND
d-independent (the group (S_5 x S_5) : Z_4 acts on bond labels, not on local
states), so the deposited 830 MB ids_nb4.npy serves the d=3 rung unchanged.
Only the per-bond channel W_{p,n} depends on d (through the Gram D = d^2),
which assemble_block already takes as a parameter.

Phases:
  validate-d3 -- the block route at d=3 vs the unrestricted Arnoldi route
                 (nb=2, 3) + the exact p=1 rank-one anchor (per-bond value
                 [d^2 G(d^2) G(n+1) / G(d^2+n)] = 1/143 at n=5, d=3).
  locate-d3   -- gap12(p; d=3) scans at nb=2 (L=4) and nb=3 (L=6) via the
                 symmetry-reduced BLOCK route (cheap and exact at these
                 sizes: K=7 at nb=2, K=57 at nb=3; validated against the
                 unrestricted Arnoldi solve at nb=2 to 8e-15 and the exact
                 p=1 rank-one anchors at nb=2,3), appended to
                 results/v22-exactZ3-n5L8/v25_n5_d3_locator.json (merged by
                 (nb, p) under flock).
  run-d3      -- the L=8 d=3 grid (chunk-checkpointed, driven windows),
                 -> v25_n5_L8_rung_d3.json.
  run-fine    -- the L=8 d=2 finer locator grid, -> v25_n5_L8_finegrid.json.

Driving protocol: identical to the v23 rung campaign (see followup_v23.sh) --
the cron-era sandbox reaps background processes, so each call advances the
resumable chunk-checkpointed assembly by one bounded foreground segment
(external `timeout`); a segment ending in 124/143 is NORMAL.  Single point per
segment (sequential mode, ~1.2 GB peak anon) per the user-approved OOM-safe
profile; NEVER two python segments at once.
"""
import sys, os, json, math, time, argparse, fcntl

import numpy as np  # module-level: _phase_run_grid loads reps/counts via np.load

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v22_n5_L8_block_v1 as blk   # deposited, unmodified machinery

OUT = blk.OUT                       # results/v22-exactZ3-n5L8
TMP = blk.TMP                       # results/v22-exactZ3-n5L8/tmp_n5L8block
LOGDIR = os.path.join(HERE, '..', '..', 'logs', 'v25-n5L8-ext')
os.makedirs(LOGDIR, exist_ok=True)


def log(*a):
    print(*a, flush=True)


def _merge_write(path, key, row):
    """Race-safe append/merge into a small results JSON by string key."""
    lockf = open(path + '.lock', 'w')
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX)
        cur = json.load(open(path)) if os.path.exists(path) else []
        merged = {r['key']: r for r in cur}
        row = dict(row)
        row['key'] = key
        merged[key] = row
        tmp = path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(list(merged.values()), f, indent=1)
        os.replace(tmp, path)
    finally:
        fcntl.flock(lockf, fcntl.LOCK_UN)
        lockf.close()


def _load_rows(path):
    return json.load(open(path)) if os.path.exists(path) else []


# ---------------------------------------------------------------------------
def phase_validate_d3(args):
    log("== phase validate-d3: block route vs unrestricted Arnoldi (d=3) ==")
    ok_all = True
    # 1) the exact p=1 rank-one anchor at nb=2: per-bond value 1/143,
    #    lam1(p=1) = (1/143)^(2*nb).
    for nb in (2, 3):
        ids, reps, counts, K = blk.orbit_table(nb)
        B1, B2 = blk.assemble_block(5, 3, 1.0, nb, ids, reps, counts, K)
        ev = blk.block_eigs(B1, B2, k_want=3)
        tgt = (1.0 / 143.0) ** (2 * nb)
        rel = abs(ev[0] - tgt) / tgt
        ok = rel < 1e-12
        ok_all &= ok
        log(f"   nb={nb} p=1: block lam1={ev[0]:.12e} vs (1/143)^{2*nb}="
            f"{tgt:.12e}  rel {rel:.2e}  [{'OK' if ok else 'FAIL'}]")
    # 2) block vs unrestricted Arnoldi at interior points.
    for nb, p in [(2, 0.50), (2, 0.55), (3, 0.52)]:
        ids, reps, counts, K = blk.orbit_table(nb)
        B1, B2 = blk.assemble_block(5, 3, p, nb, ids, reps, counts, K)
        ev = blk.block_eigs(B1, B2, k_want=4)
        try:
            rr = blk.fresh_reference(5, 3, p, nb, k_want=4)
            errs = [abs(float(ev[i]) - float(rr[i])) / abs(float(rr[i]))
                    for i in range(min(len(ev), len(rr)))]
            ok = max(errs) < 1e-6
            ok_all &= ok
            log(f"   nb={nb} p={p}: K={K} block "
                f"{[f'{float(x):.10f}' for x in ev[:3]]} vs unrestricted "
                f"{[f'{float(x):.10f}' for x in rr[:3]]}  max rel "
                f"{max(errs):.2e}  [{'OK' if ok else 'FAIL'}]")
        except Exception as e:
            ok_all = False
            log(f"   nb={nb} p={p}: reference solve FAILED ({e})")
    log(f"   VALIDATION {'PASS' if ok_all else 'FAIL'}")
    return 0 if ok_all else 1


def phase_locate_d3(args):
    plist = [float(x) for x in args.plist.split(',')]
    nb = int(args.nb)
    L = 2 * nb
    path = os.path.join(OUT, 'v25_n5_d3_locator.json')
    done = {(int(r['nb']), round(float(r['p']), 4))
            for r in _load_rows(path)}
    log(f"== phase locate-d3: nb={nb} (L={L}), d=3, points {plist} ==")
    for p in plist:
        if (nb, round(p, 4)) in done:
            log(f"   p={p}: already scanned (skipped)")
            continue
        t0 = time.time()
        ids, reps, counts, K = blk.orbit_table(nb)
        B1, B2 = blk.assemble_block(5, 3, p, nb, ids, reps, counts, K)
        ev = blk.block_eigs(B1, B2, k_want=4)
        vals = [float(x) for x in ev[:4]]
        gap12 = math.log(vals[0] / vals[1]) if vals[1] > 0 else None
        row = {'nb': nb, 'L': L, 'n': 5, 'd': 3, 'p': p,
               'lam1': vals[0], 'lam2': vals[1],
               'gap12': gap12, 'K': int(K),
               'secs': round(time.time() - t0, 1)}
        _merge_write(path, f"nb{nb}:p{round(p, 4):.4f}", row)
        log(f"   p={p}: lam1={vals[0]:.8e} lam2={vals[1]:.8e} gap12={gap12:.5f} "
            f"[{row['secs']}s]")


def _phase_run_grid(tag, d, args):
    pgrid = [float(x) for x in args.pgrid.split(',')]
    ids = np_load_ids()
    reps = np.load(os.path.join(TMP, 'reps_nb4.npy'))
    counts = np.load(os.path.join(TMP, 'counts_nb4.npy'))
    K = len(reps)
    ckpt = os.path.join(OUT, f'v25_n5_L8_{"rung_d3" if tag == "d3" else "finegrid"}.json')
    rows = _load_rows(ckpt)
    done = {round(r['p'], 4) for r in rows}
    log(f"== phase run-{tag}: d={d} L=8 grid {pgrid} ==")
    log(f"   K = {K} orbits; done = {sorted(done)}")
    for p in pgrid:
        if round(p, 4) in done:
            continue
        t0 = time.time()
        B1, B2 = blk.assemble_block(5, d, p, 4, ids, reps, counts, K,
                                    chunk=25_000, R=512,
                                    state_path=os.path.join(
                                        TMP, f'run_{tag}_p{round(p, 4):.4f}_state.npz'),
                                    save_every=8)
        ev = blk.block_eigs(B1, B2, k_want=6)
        gap12 = math.log(ev[0] / ev[1]) if ev[1] > 0 else None
        row = {'p': p, 'L': 8, 'n': 5, 'd': d, 'K': int(K),
               'triv6': [float(x) for x in ev],
               'lam1': float(ev[0]), 'lam2': float(ev[1]),
               'gap12': gap12, 'growth': float(ev[0]) ** (1.0 / 8),
               'secs': round(time.time() - t0, 1)}
        blk._ckpt_write(ckpt, p, row)
        try:
            os.remove(os.path.join(
                TMP, f'run_{tag}_p{round(p, 4):.4f}_state.npz'))
        except OSError:
            pass
        log(f"   p={p}: lam1={ev[0]:.8e} lam2={ev[1]:.8e} "
            f"gap12={gap12:.5f}  [{row['secs']}s]")


def np_load_ids():
    import numpy as np
    return np.load(os.path.join(TMP, 'ids_nb4.npy'), mmap_mode='r')


def phase_run_d3(args):
    _phase_run_grid('d3', 3, args)


def phase_run_fine(args):
    _phase_run_grid('fine', 2, args)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['validate-d3', 'locate-d3',
                                      'run-d3', 'run-fine'])
    ap.add_argument('--pgrid', default='0.47')
    ap.add_argument('--plist', default='0.50')
    ap.add_argument('--nb', default='2')
    args = ap.parse_args()
    rc = {'validate-d3': phase_validate_d3,
          'locate-d3': phase_locate_d3,
          'run-d3': phase_run_d3,
          'run-fine': phase_run_fine}[args.phase](args)
    sys.exit(0 if rc is None else rc)
