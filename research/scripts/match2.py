import numpy as np
from scipy.optimize import fsolve
from itertools import product as iproduct
exec(open('quantum_transfer2.py').read().split("L = 4")[0])

def wpm(k, Kd, Kh):
    k = np.atleast_1d(k)
    c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
    c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
    Q = c2d**2*c2h + s2d**2*s2h - s2h*np.cos(k); R = 2*s2d*np.cos(k/2)
    s = np.sqrt(np.maximum(Q**2-R**2, 0.0)); return Q+s, Q-s

def ising_spec(Kd, Kh, W0, m, above):
    """nonzero eigenvalues; odd-sector parity: even # of '-' below pc, odd # above."""
    out = []
    grids = [( (2*np.arange(1,m+1)-1)*np.pi/m, 0), (2*np.pi*np.arange(m)/m, 1)]
    for grid, isodd in grids:
        wp, wm = wpm(grid, Kd, Kh)
        for ch in iproduct([0,1], repeat=m):
            par = sum(ch) % 2
            if isodd and (par != (1 if above else 0)): continue
            if (not isodd) and par: continue
            lam = (2*W0**2)**m * np.prod([wm[i] if ch[i] else wp[i] for i in range(m)])
            if lam > 1e-300: out.append(lam)
    return np.sort(np.array(out))[::-1]

def log_lambda1(m, Kd, Kh, lnW0):
    ks = (2*np.arange(1, m+1)-1)*np.pi/m
    wp, _ = wpm(ks, Kd, Kh)
    return m*(np.log(2.0)+2*lnW0) + np.sum(np.log(wp))

L, m = 4, 2
ENC16_016 = 0.0751896333829877785
ENC16_04, ENC20_04 = 0.0022886508026864150, 0.0005002857006813122

for p, above in ((0.16, False), (0.23380962103093994, False), (0.4, True)):
    T = build_T(L, 2, p, "MAMB")
    ev = np.sort(np.real(np.linalg.eigvals(T)))[::-1][:3]
    def F(x):
        Kd, Kh, lnW0 = x
        return ising_spec(Kd, Kh, np.exp(lnW0), m, above) - ev
    got = None
    for x0 in ([0.5,-0.15,np.log(0.28)], [0.65,-0.26,np.log(0.27)], [0.47,-0.15,np.log(0.28)], [0.3,0.1,np.log(0.3)]):
        try:
            sol, info, ier, msg = fsolve(F, x0, full_output=True, xtol=1e-13)
            if ier==1 and np.max(np.abs(F(sol)))<1e-11: got = sol; break
        except Exception: pass
    Kd, Kh, W0 = got[0], got[1], np.exp(got[2])
    print(f"p={p:.5f} above={above}: Kd={Kd:.7f} Kh={Kh:.7f} W0={W0:.7f} "
          f"gapless={np.sinh(2*Kd)*np.exp(2*Kh):.7f}")
    a = W0*np.exp(2*Kd+Kh); b=W0*np.exp(-Kh); c=W0*np.exp(-2*Kd+Kh)
    print(f"   a={a:.7f} b={b:.7f} c={c:.7f}   check lam1(16)={np.exp(log_lambda1(8,Kd,Kh,np.log(W0))):.10f}"
          f"  (enclosure: {ENC16_016 if p<0.2 else ENC16_04})")
