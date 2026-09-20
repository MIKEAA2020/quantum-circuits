"""n=4 at L=10 (v2): the third crossing with full S4 colour resolution.

L=10 -> nb=5, N = 24^5 = 7,962,624 bond labels.  A DENSE transfer matrix
would need N^2 = 6.3e13 entries (~500 TB); the iterative ring route does it
in ~500 MB -- this run is the demonstration that the "dense matrices"
budget barrier is overcome by the same GEMM ring kernel (validated to
4e-16) that carried the n=5 L=6 two-size test.

Phases:
  validate   L=8 anchor: this machinery vs the deposited v18 L=8 scan
             (lam1, lam_sigma at 3 p's, f64).
  scan       L=10 production sweep on p in [0.32, 0.46] (15 points, f32,
             checkpointed/resumable): triv.triv k=3 (lam1, lam_eps) and
             std.std k=1 (lam_sigma) with warm starts.
  f64spot    float64 confirmation at the crossing-region points.
"""
import sys, os, json, math, time, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n5_L6_scan_v2 import RingOpFast, restricted_eigs, log

OUT = 'mipt_results'
LOG = 'logs'


def phase_validate(args):
    dep = json.load(open(f'{OUT}/n4_annealed_scan_L8_v1.json'))
    v0t = v0s = None
    for p in (0.34, 0.40, 0.44):
        row = next(r for r in dep if abs(r['p'] - p) < 1e-9)
        opT = RingOpFast(4, 2, p, 4, beta=8, colour=('triv', 'triv'),
                         dtype=np.float64)
        triv, v0t = restricted_eigs(opT, 2, v0=v0t, tol=1e-11)
        opS = RingOpFast(4, 2, p, 4, beta=8, colour=('std', 'std'),
                         dtype=np.float64)
        sig, v0s = restricted_eigs(opS, 1, v0=v0s, tol=1e-11)
        e1 = abs(float(triv[0]) - row['lam1']) / row['lam1']
        es = abs(float(sig[0]) - row['lam_sigma']) / row['lam_sigma']
        log(f"  [L8 anchor] p={p}: lam1 {float(triv[0]):.12e} (dep "
            f"{row['lam1']:.12e}, rel {e1:.1e})  sig {float(sig[0]):.12e} "
            f"(dep {row['lam_sigma']:.12e}, rel {es:.1e})")


GRID4 = [round(x, 4) for x in np.arange(0.32, 0.4601, 0.01)]


def phase_scan(args):
    ckpt = f'{OUT}/n4_L10_scan_v2.json'
    vckpt = f'{OUT}/n4_L10_scan_v2_v0.npz'
    done = {}
    if os.path.exists(ckpt):
        done = {round(float(r['p']), 4): r
                for r in json.load(open(ckpt))}
    out = [done[p] for p in GRID4 if p in done]
    log(f"--- n=4 L=10 scan (nb=5, N={24**5}), {len(GRID4)} points, "
        f"{len(out)} done ---")
    v0t = v0s = None
    if os.path.exists(vckpt):
        zz = np.load(vckpt)
        v0t = zz['v0t'] if 'v0t' in zz.files else None
        v0s = zz['v0s'] if 'v0s' in zz.files else None
    for p in GRID4:
        if p in done:
            continue
        t0 = time.time()
        row = {'p': p, 'L': 10, 'n': 4}
        import gc
        try:
            opT = RingOpFast(4, 2, float(p), 5, beta=2,
                             colour=('triv', 'triv'), dtype=np.float32)
            triv, v0t = restricted_eigs(opT, 2, v0=v0t, tol=1e-8)
            row['lam1'] = float(triv[0])
            row['lam_eps'] = float(triv[1])
            del opT
            gc.collect()
        except Exception as e:
            log(f"  p={p}: triv FAILED ({e})")
        try:
            opS = RingOpFast(4, 2, float(p), 5, beta=2,
                             colour=('std', 'std'), dtype=np.float32)
            sig, v0s = restricted_eigs(opS, 1, v0=v0s, tol=1e-8)
            row['lam_sigma'] = float(sig[0])
            row['X10'] = (10 * math.log(row['lam1'] / row['lam_sigma'])
                          if row.get('lam1') and sig[0] > 0 else None)
            del opS
            gc.collect()
        except Exception as e:
            log(f"  p={p}: sigma FAILED ({e})")
        row['growth'] = row['lam1'] ** 0.1 if row.get('lam1') else None
        row['secs'] = round(time.time() - t0, 1)
        out.append(row)
        # checkpoint: scalars in JSON; the 8M-element warm-start vectors in
        # a compact side .npz (NOT JSON -- the first attempted JSON dump of
        # v0 was 431 MB per row)
        json.dump(out, open(ckpt, 'w'), indent=1)
        np.savez_compressed(
            vckpt,
            v0t=(v0t.astype(np.float32) if v0t is not None
                 else np.zeros(0, np.float32)),
            v0s=(v0s.astype(np.float32) if v0s is not None
                 else np.zeros(0, np.float32)))
        log(f"  p={p:.3f} lam1={row.get('lam1')} eps={row.get('lam_eps')} "
            f"sig={row.get('lam_sigma')} X10={row.get('X10')} "
            f"[{row.get('secs')}s]")
    log(f"written {ckpt}")


def phase_f64spot(args):
    pts = [0.36, 0.38, 0.40, 0.42]
    res = []
    v0t = v0s = None
    for p in pts:
        t0 = time.time()
        opT = RingOpFast(4, 2, float(p), 5, beta=2, colour=('triv', 'triv'),
                         dtype=np.float64)
        triv, v0t = restricted_eigs(opT, 2, v0=v0t, tol=1e-11)
        opS = RingOpFast(4, 2, float(p), 5, beta=2, colour=('std', 'std'),
                         dtype=np.float64)
        sig, v0s = restricted_eigs(opS, 1, v0=v0s, tol=1e-11)
        row = {'p': p, 'lam1': float(triv[0]), 'lam_eps': float(triv[1]),
               'lam_sigma': float(sig[0]),
               'X10': 10 * math.log(float(triv[0]) / float(sig[0])),
               'secs': round(time.time() - t0, 1)}
        res.append(row)
        log(f"  [f64] p={p}: lam1 {row['lam1']:.10e} sig "
            f"{row['lam_sigma']:.10e} X10 {row['X10']:.4f} "
            f"[{row['secs']}s]")
        json.dump(res, open(f'{OUT}/n4_L10_f64spot_v2.json', 'w'), indent=1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['validate', 'scan', 'f64spot'])
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(LOG, exist_ok=True)
    {'validate': phase_validate, 'scan': phase_scan,
     'f64spot': phase_f64spot}[args.phase](args)
