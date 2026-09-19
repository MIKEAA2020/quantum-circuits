"""Annealed two-replica transfer on the per-site algebra {e0,e+,e-}^L,
implemented via factorized per-site traces. Match to Ising closed form."""
import numpy as np
from itertools import product

# per-site data for dimension d: (tr(e_a), tr(e_a S)) for a in {0,+,-}
def site_ts(d):
    t0, s0 = float(d), float(d)               # e0: S e0 = e0
    tp, sp = (d*d-d)/2.0, (d*d-d)/2.0         # e+: S e+ = e+
    tm, sm = (d*d-d)/2.0, -(d*d-d)/2.0        # e-: S e- = -e-
    return [(t0,s0),(tp,sp),(tm,sm)]
EPS = [1.0, 1.0, -1.0]   # epsilon_a: S = e0+e+ - e-

def build_T(L, d, p, order):
    """order: string over A (even-bond gates), B (odd-bond gates), M (measure all)."""
    D = d*d
    ts = site_ts(d)
    n = 3**L
    # state index: base-3 over sites
    def idx(a): 
        r = 0
        for x in a: r = 3*r + x
        return r
    even = [(2*k, 2*k+1) for k in range(L//2)]
    odd  = [(2*k+1, (2*k+2) % L) for k in range(L//2)]
    T = np.zeros((n, n))
    states = list(product(range(3), repeat=L))
    for a in states:
        j = idx(a)
        coeffs = {a: 1.0}
        for ch in order:
            new = {}
            for st, c in coeffs.items():
                if ch == 'M':
                    key = tuple((1-p) + (p if st[i]==0 else 0.0) for i in range(L))
                    # per-site multiplier
                    mult = 1.0
                    for i in range(L):
                        mult *= (1-p) + (p if st[i]==0 else 0.0)
                    new[st] = new.get(st, 0.0) + c*mult
                else:
                    bonds = even if ch=='A' else odd
                    # apply bonds sequentially (they commute within a layer)
                    cur = {st: c}
                    for (i, k) in bonds:
                        nxt = {}
                        for s2, c2 in cur.items():
                            ti, si = ts[s2[i]]; tk, sk = ts[s2[k]]
                            al = (D*ti*tk - si*sk)/(D*(D*D-1))
                            be = (D*si*sk - ti*tk)/(D*(D*D-1))
                            for b in range(3):
                                for cc in range(3):
                                    w = al + be*EPS[b]*EPS[cc]
                                    if abs(w) < 1e-15: continue
                                    s3 = list(s2); s3[i] = b; s3[k] = cc; s3 = tuple(s3)
                                    nxt[s3] = nxt.get(s3, 0.0) + c2*w
                        cur = nxt
                    for s2, c2 in cur.items():
                        new[s2] = new.get(s2, 0.0) + c2
            coeffs = new
        for st, c in coeffs.items():
            T[idx(st), j] += c
    return T

def ising_spectrum(m, Kd, Kh, W0):
    """Nonzero Ising C_comp eigenvalues (closed form), L=2m."""
    def wpm(k):
        c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
        c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
        Q = c2d**2*c2h + s2d**2*s2h - s2h*np.cos(k)
        R = 2*s2d*np.cos(k/2)
        s = np.sqrt(max(Q**2-R**2, 0.0))
        return Q+s, Q-s
    out = []
    kp = (2*np.arange(1, m+1)-1)*np.pi/m
    ko = 2*np.pi*np.arange(m)/m
    # even sector: even # of '-'; odd sector: even # for p<pc
    import itertools as it
    for grid, sect in ((kp, 'even'), (ko, 'odd')):
        wp, wm = wpm(grid)
        for choice in it.product([0,1], repeat=m):   # 1 = '-'
            if sum(choice) % 2: continue
            lam = (2*W0**2)**m * np.prod([wm[i] if choice[i] else wp[i] for i in range(m)])
            if lam > 0: out.append(lam)
    return np.sort(out)[::-1]

L = 4
for order in ["AMBM", "AMB", "ABM", "AMAM", "AMBAMB", "AMBMAMBM"]:
    T = build_T(L, 2, 0.4, order)
    ev = np.linalg.eigvals(T)
    evr = np.sort(np.real(ev[np.abs(np.imag(ev)) < 1e-9*np.max(np.abs(ev))]))[::-1]
    print(f"order={order}: top6 = {np.round(evr[:6], 6)}")
