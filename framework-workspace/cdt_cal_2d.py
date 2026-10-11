#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cdt_cal_2d.py — 1+1D calibration of the L-8b/L-8d extraction pipeline (Gate-level, v10.9 round).

WHAT THIS IS: a self-contained pipeline validation. It generates
  (a) a FLAT 2D foliated control lattice (regular zigzag, degrees 3) — analog of Gate C0a in 2D, and
  (b) an ensemble of FLUCTUATING-PROFILE 1+1D CDT configurations (uniform-composition fibration per strip) — Gate C0b-partial,
and measures, with the SAME kernel on both (Convention C1, lazy RW on the 3-regular dual):
  full return-probability spectral dimension d_s(sigma),
  projected two-walker meeting probability on the time-marginal -> d_t(sigma)  [Eichhorn-Mizera projected lineage],
  slice-RW analytic cross-check (ring d_s = 1).

WHAT THIS IS NOT: not a bridge datum, not d_s flow on CDT quantum geometries, not the L-8 test.
No MCMC thermalization: the fibration sampler is uniform-on-compositions x arbitrary fibration phase,
NOT the Haar/Regge-weighted 2D CDT measure (upgrade path: dyntri-cdt2d MCMC). Printed on the record.

Analytic targets (registered before the run):
  Flat control:  d_s = 2 (IR window), d_t = 1.  CDT ensemble: d_s ~ 2 window (finite-size), d_t = 1
  (kernel-level: degree-3 dual, step changes strip w.p. 1/6 -> time-RW -> d_t = 1 in any instance:
   the gate validates the pipeline AND makes the trap-inheritance warning operational in 2D).
"""
import numpy as np, json, time, sys

rng = np.random.default_rng(20261011)

def composition(n_total, n_parts, rng):
    """Uniform positive composition of n_total into n_parts (stars and bars)."""
    cuts = np.sort(rng.choice(np.arange(1, n_total), n_parts - 1, replace=False))
    return np.diff(np.concatenate(([0], cuts, [n_total])))

def sample_profile(T, n0, sigma, lo, hi, rng):
    ns = [n0]
    for _ in range(T - 1):
        ns.append(int(np.clip(ns[-1] + rng.normal(0, sigma), lo, hi)))
    return ns

def build_config(profile, rng):
    """Build one 1+1D CDT-like configuration, time-periodic (torus).
    Returns neighbor arrays (nb_prev, nb_next, nb_inter) and strip_of_node."""
    T = len(profile)
    strips = []                      # per strip: node global-id list in zigzag cyclic order
    u_id = []                        # strips x lower-edge index -> global id (u-triangle)
    d_id = []                        # strips x upper-edge index -> global id (d-triangle) ; strip s d's base = ring s+1 edge
    nid = 0
    for s in range(T):
        n_lo, n_hi = profile[s], profile[(s + 1) % T]
        seq, ui, di = [], {}, {}
        if n_hi >= n_lo:
            comp = composition(n_hi, n_lo, rng)
            j = 0
            for i in range(n_lo):
                ui[i] = nid; seq.append(nid); nid += 1
                for _ in range(comp[i]):
                    di[j] = nid; seq.append(nid); nid += 1; j += 1
        else:
            comp = composition(n_lo, n_hi, rng)
            i = 0
            for j in range(n_hi):
                di[j] = nid; seq.append(nid); nid += 1
                for _ in range(comp[j]):
                    ui[i] = nid; seq.append(nid); nid += 1; i += 1
        strips.append(seq); u_id.append(ui); d_id.append(di)
    N = nid
    nb_prev = np.empty(N, np.int64); nb_next = np.empty(N, np.int64); nb_inter = np.empty(N, np.int64)
    strip_of = np.empty(N, np.int64)
    for s in range(T):
        seq = strips[s]; L = len(seq)
        for k, g in enumerate(seq):
            strip_of[g] = s
            nb_prev[g] = seq[(k - 1) % L]
            nb_next[g] = seq[(k + 1) % L]
        for i, g in u_id[s].items():
            nb_inter[g] = d_id[(s - 1) % T][i]        # u_i(s) base = ring-s edge i = upper edge i of strip s-1
        for j, g in d_id[s].items():
            nb_inter[g] = u_id[(s + 1) % T][j]        # d_j(s) base = ring-(s+1) edge j = lower edge j of strip s+1
    return nb_prev, nb_next, nb_inter, strip_of, T

def run(nb_prev, nb_next, nb_inter, strip_of, T, nseeds=48, smax=384):
    N = len(nb_prev)
    seeds = rng.choice(N, nseeds, replace=False)
    p = np.zeros((nseeds, N)); p[np.arange(nseeds), seeds] = 1.0
    Pret = np.zeros(smax + 1); Meet = np.zeros(smax + 1)
    for sig in range(1, smax + 1):
        p = 0.5 * p + (p[:, nb_prev] + p[:, nb_next] + p[:, nb_inter]) / 6.0
        Pret[sig] = p[np.arange(nseeds), seeds].mean()
        PM = np.zeros((nseeds, T))
        for k in range(nseeds):
            np.add.at(PM[k], strip_of, p[k])
        Meet[sig] = (PM * PM).sum(axis=1).mean()
    return Pret, Meet

def dim_at(sigs, vals, s0, span=1.5):
    m = (sigs >= s0 / span) & (sigs <= s0 * span) & (vals > 0)
    if m.sum() < 4: return float("nan")
    a = np.polyfit(np.log(sigs[m]), np.log(vals[m]), 1)[0]
    return float(-2.0 * a)

def window_mean(sigs, vals, lo, hi):
    vals = vals[1:]
    ds = [dim_at(sigs, vals, s) for s in range(lo, hi + 1)]
    ds = [d for d in ds if d == d]
    return float(np.mean(ds)), float(np.std(ds))

def dim_table(name, Pret, Meet, smax):
    sigs = np.arange(1, smax + 1, dtype=float)
    Pret, Meet = Pret[1:], Meet[1:]
    out = {}
    for s0 in [8, 16, 32, 64, 128, 256]:
        if s0 <= smax:
            out[s0] = (round(dim_at(sigs, Pret, s0), 3), round(dim_at(sigs, Meet, s0), 3))
    return out

t0 = time.time()
report = {"date": "2026-10-11", "seed": 20261011, "kernel": "lazy RW, stay 1/2, neighbors 1/6 each (Convention C1)",
          "conventions": ["time-periodic torus (endcap-free control)", "fibration = uniform composition x arbitrary phase (NOT Haar/Regge measure)"]}

# ---------- FLAT 2D CONTROL (Gate C0a-analog) ----------
T_FL, N_RING = 60, 600
prof_flat = [N_RING] * T_FL
at = build_config(prof_flat, rng)
assert (np.unique(np.concatenate([at[0], at[1], at[2]])).size == len(at[0])), "neighbor degeneracy"
Pret_f, Meet_f = run(*at, T_FL)
sigs = np.arange(1, 385, dtype=float)
ds_f, ds_f_std = window_mean(sigs, Pret_f, 16, 128)
dt_f, dt_f_std = window_mean(sigs, Meet_f, 16, 128)
c0a_pass = (abs(ds_f - 2.0) <= 0.1 + ds_f_std) and (abs(dt_f - 1.0) <= 0.1 + dt_f_std)
report["flat_2d"] = {
    "N_nodes": int(len(at[0])), "table_sigma:": dim_table("flat", Pret_f, Meet_f, 384),
    "d_s_window16_128": [round(ds_f, 3), round(ds_f_std, 3)],
    "d_t_window16_128": [round(dt_f, 3), round(dt_f_std, 3)],
    "targets": {"d_s": "2 +/- 0.1", "d_t": "1 +/- 0.1"}, "C0a-2D-flat": "PASS" if c0a_pass else "FAIL"}

# ---------- SLICE-RW CROSS-CHECK (ring d_s = 1 analytic) ----------
ring = np.arange(N_RING)
nbp, nbn = (ring - 1) % N_RING, (ring + 1) % N_RING
nbi = ring.copy()
Pret_r, _ = run(nbp, nbn, nbi, np.zeros(N_RING, np.int64), 1, nseeds=48, smax=384)
ds_r, ds_r_std = window_mean(sigs, Pret_r, 16, 128)
report["slice_ring"] = {"d_slice_window16_128": [round(ds_r, 3), round(ds_r_std, 3)], "target": "1 (analytic)",
                        "note": "slice-dual of one spatial ring; sanity check of the estimator on a trivially-known case"}

# ---------- CDT-LIKE ENSEMBLE (Gate C0b-partial) ----------
ens = []
for c in range(6):
    prof = sample_profile(48, 700, 90, 128, 1600, rng)
    cf = build_config(prof, rng)
    Pret_c, Meet_c = run(*cf, 48)
    ens.append((Pret_c, Meet_c, int(len(cf[0]))))
    print("config %d done: N=%d  t=%.1fs" % (c, len(cf[0]), time.time() - t0), flush=True)
Pret_e = np.mean([e[0] for e in ens], axis=0)
Meet_e = np.mean([e[1] for e in ens], axis=0)
ds_e, ds_e_std = window_mean(sigs, Pret_e, 16, 128)
dt_e, dt_e_std = window_mean(sigs, Meet_e, 16, 128)
c0b_pass = (abs(ds_e - 2.0) <= 0.25) and (abs(dt_e - 1.0) <= 0.1)
report["cdt_ensemble_2d"] = {
    "configs": 6, "N_nodes_range": [int(min(e[2] for e in ens)), int(max(e[2] for e in ens))],
    "table_sigma:": dim_table("cdt", Pret_e, Meet_e, 384),
    "d_s_window16_128": [round(ds_e, 3), round(ds_e_std, 3)],
    "d_t_window16_128": [round(dt_e, 3), round(dt_e_std, 3)],
    "targets": {"d_s": "~2 window (finite-size, +-0.25 flagged)", "d_t": "1 +/- 0.1 (analytic by kernel construction)"},
    "C0b-2D-partial": "PASS-partial" if c0b_pass else "FAIL",
    "measure_caveat": "not the Haar/Regge-weighted 2D CDT measure; MCMC upgrade available via dyntri-cdt2d"}

report["runtime_s"] = round(time.time() - t0, 1)
report["standing_note"] = ("Gate-level pipeline validation only. Not a bridge datum. Throughput (bridge-artifact deliveries) remains zero. "
                           "d_t = 1 in 2D is a KERNEL CONSTRUCTION FACT (degree-3 dual, strip-move probability 1/6): "
                           "the 2D gate validates the pipeline and operationalizes the trap-inheritance warning; "
                           "only the 4D ensemble flow test (L-8d) is decisional.")

print(json.dumps(report, indent=1))
with open("cdt_cal_2d_report.json", "w") as f:
    json.dump(report, f, indent=1)
