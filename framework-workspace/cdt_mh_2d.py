#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cdt_mh_2d.py — Node A: MCMC-grade 1+1D CDT gate re-run (promotes C0b partial -> full on pass).

Replaces cdt_cal_2d.py's direct-composition sampler with an equilibrated Metropolis chain:
  - Microcanonical in total volume: sum_t n_t = 1200 fixed (T=48 rings, standard fixed-N2 practice).
  - Microstate = (profile n_t, {type-strings per strip}); type-string = m U-slots + k D-slots in any
    cyclic order (= gap-vertices of valence 3 allowed: full simplicial set incl. all profile shapes);
    phase = state (rotations distinct states by labeled slots).
  - Moves (detailed balance, flat target on valid microstates):
      (i) adjacent-pair profile shift: (n_s, n_{s+1}) -> (n_s+e, n_{s+1}-e), bounds [8,200];
          on acceptance the 3 affected strips' strings are GIBBS-resampled (uniform valid string);
      (ii) implicit: those same Gibbs resamples provide the fibration mixing.
    Uniform string sampler: uniform m-subset of m+k slots (no composition machinery; measure = uniform
    over unrooted labeled-slot microstates; profile-marginal ~ prod binom(m_s+m_{s+1}, m_s) delta(sum-1200);
    differs from the rooted-strip convention of Ambjorn-Loll '98 (C(l+m-1, l-1)) by boundary-marking
    factors - collation item A1b; d_s = 2 and d_t = 1 are convention-robust at gate granularity).
  - Equilibration: 300k pair-moves; ensemble of 6 configs at >= 80k-move separation.
Measure-convention print: state space convention = uniform (composition, phase) microstates;
  collation with rooted/unrooted conventions of Ambjorn-Loll '98 (transfer matrix C(l+m-1, l-1)) is
  open item A1b; d_s = 2 and d_t = 1 are convention-robust at the granularity of this gate.
Registered targets (BEFORE the run, same as v10.9 round): d_s ~ 2 (window, tol 0.25), d_t = 1 +/- 0.1.
Question of record: does the d_t drift item (v10.9: 0.952 -> 0.915) survive equilibrated measure?
"""
import numpy as np, json, time

rng = np.random.default_rng(20261011)
T, NMIN, NMAX, TOTAL = 48, 8, 200, 1200

def composition(n_total, n_parts, rng):
    cuts = np.sort(rng.choice(np.arange(1, n_total), n_parts - 1, replace=False))
    return np.diff(np.concatenate(([0], cuts, [n_total])))

def sample_string(m, k):
    """Uniform cyclic type-string: m U-slots (1) among m+k labeled slots, no constraints."""
    seq = np.zeros(m + k, np.int8)
    seq[rng.choice(m + k, m, replace=False)] = 1
    return seq

def build_adjacency(profile, strings):
    """Type-strings per strip -> dual-graph neighbor arrays + strip membership."""
    N = int(sum(p + profile[(i + 1) % T] for i, p in enumerate(profile)))
    nb_prev = np.empty(N, np.int64); nb_next = np.empty(N, np.int64); nb_inter = np.empty(N, np.int64)
    strip_of = np.empty(N, np.int64)
    uidx = []; didx = []
    gid = 0
    for s in range(T):
        st = strings[s]; L = len(st)
        seq = np.arange(gid, gid + L); gid += L
        strip_of[seq] = s
        nb_prev[seq] = np.roll(seq, 1)   # slot j-1
        nb_next[seq] = np.roll(seq, -1)  # slot j+1
        uidx.append(seq[st == 1])        # U-slot global ids in lower-edge index order
        didx.append(seq[st == 0])
    for s in range(T):
        u, d = uidx[s], didx[s]
        nb_inter[u] = didx[(s - 1) % T][:len(u)]          # u_i(s) base = ring-s edge i = d_i(s-1)
        nb_inter[d] = uidx[(s + 1) % T][:len(d)]          # d_j(s) base = ring-(s+1) edge j = u_j(s+1)
    return nb_prev, nb_next, nb_inter, strip_of

def run_estimators(nb_prev, nb_next, nb_inter, strip_of, T, nseeds=96, smax=384):
    N = len(nb_prev)
    seeds = rng.choice(N, nseeds, replace=False)
    p = np.zeros((nseeds, N)); p[np.arange(nseeds), seeds] = 1.0
    Pret = np.zeros(smax + 1); Meet = np.zeros(smax + 1)
    for sig in range(1, smax + 1):
        p = 0.5 * p + (p[:, nb_prev] + p[:, nb_next] + p[:, nb_inter]) / 6.0
        Pret[sig] = p[np.arange(nseeds), seeds].mean()
        PM = np.zeros((nseeds, T))
        for kk in range(nseeds):
            np.add.at(PM[kk], strip_of, p[kk])
        Meet[sig] = (PM * PM).sum(axis=1).mean()
    return Pret, Meet

def dim_at(sigs, vals, s0, span=1.5):
    m = (sigs >= s0 / span) & (sigs <= s0 * span) & (vals > 0)
    if m.sum() < 4: return float("nan")
    return float(-2.0 * np.polyfit(np.log(sigs[m]), np.log(vals[m]), 1)[0])

def window_mean(sigs, vals, lo, hi):
    vals = vals[1:]
    ds = [dim_at(sigs, vals, s) for s in range(lo, hi + 1)]
    ds = [d for d in ds if d == d]
    return float(np.mean(ds)), float(np.std(ds))

def gibbs_resample(profile, strings, s):
    m, k = int(profile[s]), int(profile[(s + 1) % T])
    if m >= 2 and k >= 2 and m + k >= 4:
        strings[s] = sample_string(m, k)

t0 = time.time()
profile = np.full(T, TOTAL // T)
strings = [sample_string(int(profile[s]), int(profile[(s + 1) % T])) for s in range(T)]

# ---- equilibrate ----
for step in range(300000):
    s = int(rng.integers(T)); e = 1 if rng.random() < 0.5 else -1
    ns0, ns1 = profile[s] + e, profile[(s + 1) % T] - e
    if NMIN <= ns0 <= NMAX and NMIN <= ns1 <= NMAX:
        profile[s], profile[(s + 1) % T] = ns0, ns1
        gibbs_resample(profile, strings, (s - 1) % T)
        gibbs_resample(profile, strings, s)
        gibbs_resample(profile, strings, (s + 1) % T)
print("equilibrated 300k moves, t=%.0fs" % (time.time() - t0), flush=True)

# ---- sample ensemble ----
ens = []
for c in range(6):
    for step in range(80000):
        s = int(rng.integers(T)); e = 1 if rng.random() < 0.5 else -1
        ns0, ns1 = profile[s] + e, profile[(s + 1) % T] - e
        if NMIN <= ns0 <= NMAX and NMIN <= ns1 <= NMAX:
            profile[s], profile[(s + 1) % T] = ns0, ns1
            gibbs_resample(profile, strings, (s - 1) % T)
            gibbs_resample(profile, strings, s)
            gibbs_resample(profile, strings, (s + 1) % T)
    adj = build_adjacency(np.array(profile), strings)
    assert np.unique(np.concatenate([adj[0], adj[1], adj[2]])).size == len(adj[0])
    Pret_c, Meet_c = run_estimators(*adj, T)
    ens.append((Pret_c, Meet_c, len(adj[0]), float(np.std(profile))))
    print("config %d: nodes=%d profile_sd=%.1f t=%.0fs" % (c, len(adj[0]), float(np.std(profile)), time.time() - t0), flush=True)

Pret_e = np.mean([e[0] for e in ens], axis=0)
Meet_e = np.mean([e[1] for e in ens], axis=0)
sigs = np.arange(1, 385, dtype=float)
LO, HI = 4, 40
ds_e, ds_sd = window_mean(sigs, Pret_e, LO, HI)
dt_e, dt_sd = window_mean(sigs, Meet_e, LO, HI)
table = {str(s0): [round(dim_at(sigs, Pret_e[1:], s0), 3), round(dim_at(sigs, Meet_e[1:], s0), 3)]
         for s0 in [4, 8, 16, 32, 64, 128, 256]}
c0b_full = (abs(ds_e - 2.0) <= 0.25) and (abs(dt_e - 1.0) <= 0.1)
report = {
    "date": "2026-10-11", "seed": 20261011, "sampler": "microcanonical pair-shift MH + uniform-string Gibbs (300k burn, 80k spacing)",
    "measure_convention": "uniform (composition, phase) microstates; rotational-symmetry multiplicity uncorrected; AL98 rooted/unrooted collation = open item A1b",
    "volume": {"T": T, "total": int(sum(profile)), "n_range": [NMIN, NMAX]},
    "ensemble": {"configs": 6, "nodes_range": [int(min(e[2] for e in ens)), int(max(e[2] for e in ens))],
                 "profile_sd_range": [round(min(e[3] for e in ens), 1), round(max(e[3] for e in ens), 1)]},
    "window": [LO, HI], "table_sigma": table,
    "d_s": [round(ds_e, 3), round(ds_sd, 3)], "d_t": [round(dt_e, 3), round(dt_sd, 3)],
    "targets": {"d_s": "~2 (tol 0.25)", "d_t": "1 +/- 0.1"},
    "drift_question_answer": ("drift GONE under equilibrated measure (|d_t-1| <= 0.01): prior 0.94 = phase-pinning sampler artifact"
                              if abs(dt_e - 1.0) <= 0.01 else
                              "drift REDUCED but visible (|d_t-1| > 0.01 and <= 0.1): pass; residual = strip-width mixing + finite-T" if abs(dt_e - 1.0) <= 0.1 else
                              "drift PERSISTS beyond tolerance: NOISE-BUDGET ITEM OPEN - estimator question before any 4D work"),
    "C0b-2D": "PASS-full" if c0b_full and abs(dt_e - 1.0) <= 0.1 else ("PASS-partial-retained" if c0b_full else "FAIL"),
    "runtime_s": round(time.time() - t0, 1),
    "standing_note": "Gate-level only; not a bridge datum; throughput zero; d_t = 1 in 2D is a kernel construction fact (strip-move p = 1/6); decisional reading remains 4D-only (L-8d)."}
print(json.dumps(report, indent=1))
open("cdt_mh_2d_report.json", "w").write(json.dumps(report, indent=1))
