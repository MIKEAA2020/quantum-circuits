#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cdt_mh_diag.py - mechanism diagnostics for the C0b-full FAIL (Node A).
D1: same ensemble conventions, FLAT profile (n=25 all rings), strings equilibrated -> isolates
    profile-heterogeneity as the only variable vs the failed run. Expect d_t ~ 1 if mechanism pinned.
D2: synthetic birth-death strip-chain with rates measured from the failed run's profiles:
    p^+_s = (1/6) n_{s+1}/(n_s+n_{s+1}), p^-_s = (1/6) n_s/(n_s+n_{s+1}), stay = 1/2 + (1/3);
    propagated distributions -> M(sigma) -> d_t. Expect ~ measured 0.61 if the reduced process suffices.
"""
import numpy as np, json, time

rng = np.random.default_rng(777)
T = 48
NMIN, NMAX, TOTAL = 8, 200, 1200

def sample_string(m, k):
    seq = np.zeros(m + k, np.int8); seq[rng.choice(m + k, m, replace=False)] = 1
    return seq

def build_adjacency(profile, strings):
    N = int(sum(p + profile[(i + 1) % T] for i, p in enumerate(profile)))
    nb_prev = np.empty(N, np.int64); nb_next = np.empty(N, np.int64); nb_inter = np.empty(N, np.int64)
    strip_of = np.empty(N, np.int64); uidx = []; didx = []; gid = 0
    for s in range(T):
        st = strings[s]; L = len(st); seq = np.arange(gid, gid + L); gid += L
        strip_of[seq] = s
        nb_prev[seq] = np.roll(seq, 1); nb_next[seq] = np.roll(seq, -1)
        uidx.append(seq[st == 1]); didx.append(seq[st == 0])
    for s in range(T):
        u, d = uidx[s], didx[s]
        nb_inter[u] = didx[(s - 1) % T][:len(u)]
        nb_inter[d] = uidx[(s + 1) % T][:len(d)]
    return nb_prev, nb_next, nb_inter, strip_of

def estimators(nb_prev, nb_next, nb_inter, strip_of, nseeds=96, smax=384):
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

sigs = np.arange(1, 385, dtype=float)

# ---- D1: FLAT profile, equilibrated strings, SAME slice sizes as the failed run ----
prof1 = np.full(T, TOTAL // T)
str1 = [sample_string(int(prof1[s]), int(prof1[(s + 1) % T])) for s in range(T)]
for _ in range(120000):
    s = int(rng.integers(T)); str1[s] = sample_string(int(prof1[s]), int(prof1[(s + 1) % T]))
P1s, M1s = [], []
for _ in range(6):
    for _ in range(30000):
        s = int(rng.integers(T)); str1[s] = sample_string(int(prof1[s]), int(prof1[(s + 1) % T]))
    adj = build_adjacency(prof1, str1)
    Pr, Me = estimators(*adj)
    P1s.append(Pr); M1s.append(Me)
ds1, ds1s = window_mean(sigs, np.mean(P1s, 0), 4, 40)
dt1, dt1s = window_mean(sigs, np.mean(M1s, 0), 4, 40)

# ---- D2: synthetic strip-chain with rates from an equilibrated fluctuating profile ----
prof2 = np.full(T, TOTAL // T)
str2 = [sample_string(int(prof2[s]), int(prof2[(s + 1) % T])) for s in range(T)]
def gibbs(profile, strings, s):
    strings[s] = sample_string(int(profile[s]), int(profile[(s + 1) % T]))
for _ in range(300000):
    s = int(rng.integers(T)); e = 1 if rng.random() < 0.5 else -1
    a, b = prof2[s] + e, prof2[(s + 1) % T] - e
    if NMIN <= a <= NMAX and NMIN <= b <= NMAX:
        prof2[s], prof2[(s + 1) % T] = a, b
        gibbs(prof2, str2, (s - 1) % T); gibbs(prof2, str2, s); gibbs(prof2, str2, (s + 1) % T)
n = prof2.astype(float)
pp = (n[(np.arange(T) + 1) % T] / (n + n[(np.arange(T) + 1) % T])) / 6.0   # prob move strip s -> s+1 per step
pm = (n / (n + n[(np.arange(T) + 1) % T])) / 6.0                           # prob move s -> s-1
q = np.zeros((48, T)); q[:, 0] = 1.0                                       # two walkers? meeting from same strip 0
M = np.zeros(385)
for sig in range(1, 385):
    nq = (1.0 - pp - pm) * q
    nq += pp[np.arange(T)][:, None] * np.roll(q, -1, axis=1) * 0           # placeholder guard
    nq = (1.0 - pp - pm) * q + np.roll(pp * q, 0)[None, :] * 0             # (rebuilt below)
    nq = (1.0 - pp - pm) * q
    nq2 = np.zeros_like(q)
    for s in range(T):
        # stays
        nq2[:, s] += (1.0 - pp[s] - pm[s]) * q[:, s]
        # from s-1 moving + : pp[s-1] ; from s+1 moving - : pm[s+1]
        nq2[:, s] += pp[(s - 1) % T] * q[:, (s - 1) % T] + pm[(s + 1) % T] * q[:, (s + 1) % T]
    q = nq2
    M[sig] = (q * q).sum(axis=0).mean()
dt2 = {str(s0): round(dim_at(sigs, M[1:], s0), 3) for s0 in [4, 8, 16, 32, 64, 128, 256]}
dt2w, dt2s = window_mean(sigs, M, 4, 40)

out = {
 "D1_flat_profile_equilibrated_strings": {
   "d_s_window4_40": [round(ds1, 3), round(ds1s, 3)],
   "d_t_window4_40": [round(dt1, 3), round(dt1s, 3)],
   "prediction": "d_t ~ 1 if heterogeneity is the mechanism"},
 "D2_strip_chain_from_profile_rates": {
   "table_sigma": dt2, "d_t_window4_40": [round(dt2w, 3), round(dt2s, 3)],
   "prediction": "reproduce ~0.6 ballpark if reduced process suffices"},
 "note": "diagnostics for cdt_mh_2d.py FAIL (d_t=0.609, d_s=1.687, window [4,40])"}
print(json.dumps(out, indent=1))
open("cdt_mh_diag_report.json", "w").write(json.dumps(out, indent=1))
