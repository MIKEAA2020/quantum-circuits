import numpy as np
from scipy.optimize import fsolve
from itertools import product as iproduct
exec(open('quantum_transfer2.py').read().split("L = 4")[0])

def wpm(k, Kd, Kh):
    c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
    c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
    Q = c2d**2*c2h + s2d**2*s2h - s2h*np.cos(k); R = 2*s2d*np.cos(k/2)
    s = np.sqrt(np.maximum(Q**2-R**2, 0.0)); return Q+s, Q-s

def ising_spec_m(Kd, Kh, W0, m):
    """nonzero eigenvalues (2W0^2)^m * prod w^+- with even-'-' parity in both sectors."""
    out = []
    for grid in ((2*np.arange(1,m+1)-1)*np.pi/m, 2*np.pi*np.arange(m)/m):
        wp, wm = wpm(grid, Kd, Kh)
        for ch in iproduct([0,1], repeat=m):
            if sum(ch) % 2: continue
            lam = (2*W0**2)**m * np.prod([wm[i] if ch[i] else wp[i] for i in range(m)])
            if lam > 1e-300: out.append(lam)
    return np.sort(np.array(out))[::-1]

L = 4  # m=2
for p in (0.16, 0.23380962103093994, 0.4):
    T = build_T(L, 2, p, "MAMB")
    ev = np.sort(np.real(np.linalg.eigvals(T)))[::-1][:3]
    # solve (Kd, Kh, lnW0) from the 3 eigenvalues
    def F(x):
        Kd, Kh, lnW0 = x
        return ising_spec_m(Kd, Kh, np.exp(lnW0), L//2) - ev
    for x0 in ([0.5, -0.15, np.log(0.28)], [0.65, -0.26, np.log(0.27)], [0.3, 0.0, np.log(0.3)]):
        sol, info, ier, msg = fsolve(F, x0, full_output=True, xtol=1e-13)
        if ier == 1 and np.max(np.abs(F(sol))) < 1e-10:
            break
    Kd, Kh, W0 = sol[0], sol[1], np.exp(sol[2])
    gapless = np.sinh(2*Kd)*np.exp(2*Kh)
    print(f"p={p:.5f}: Kd={Kd:.6f} Kh={Kh:.6f} W0={W0:.6f}  sinh(2Kd)e^2Kh={gapless:.6f}")
    a = W0*np.exp(2*Kd+Kh); b = W0*np.exp(-Kh); c = W0*np.exp(-2*Kd+Kh)
    print(f"        a={a:.6f} b={b:.6f} c={c:.6f}  a-2b-c={a-2*b-c:+.2e}")
