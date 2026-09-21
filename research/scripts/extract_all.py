import numpy as np
from scipy.optimize import fsolve
from fractions import Fraction
exec(open('match2.py').read().split("L, m = 4, 2")[0])

L, m = 4, 2
PC2 = {2: 0.23380962103093994, 3: 0.45968757625671497, 5: 0.6790037305201129}

def extract(d, p):
    above = p > PC2[d]
    T = build_T(L, d, p, "MAMB")
    ev = np.sort(np.real(np.linalg.eigvals(T)))[::-1][:3]
    def F(x):
        Kd, Kh, lnW0 = x
        return ising_spec(Kd, Kh, np.exp(lnW0), m, above) - ev
    for x0 in ([0.6,-0.26,np.log(0.28)], [0.5,-0.1,np.log(0.28)], [0.3,0.1,np.log(0.3)], [0.7,-0.4,np.log(0.35)]):
        try:
            sol, info, ier, msg = fsolve(F, x0, full_output=True, xtol=1e-14)
            if ier==1 and np.max(np.abs(F(sol)))<1e-11: 
                Kd, Kh, W0 = sol[0], sol[1], np.exp(sol[2])
                a = W0*np.exp(2*Kd+Kh); b=W0*np.exp(-Kh); c=W0*np.exp(-2*Kd+Kh)
                return dict(Kd=Kd, Kh=Kh, W0=W0, a=a, b=b, c=c,
                            gapless=np.sinh(2*Kd)*np.exp(2*Kh))
        except Exception: pass
    return None

print("p-grid d=2 (full precision):")
for p in [0.05, 0.1, 0.16, 0.2, 0.23380962103093994, 0.3, 0.4, 0.5, 0.6, 0.8]:
    r = extract(2, p)
    print(f"  p={p:.5f}: a={r['a']:.9f} b={r['b']:.9f} c={r['c']:.9f} W0={r['W0']:.9f} gapless={r['gapless']:.7f}")
print("\np-grid d=3:")
for p in [0.1, 0.2, 0.3, 0.45968757625671497, 0.5, 0.6]:
    r = extract(3, p)
    print(f"  p={p:.5f}: a={r['a']:.9f} b={r['b']:.9f} c={r['c']:.9f} W0={r['W0']:.9f} gapless={r['gapless']:.7f}")
print("\np-grid d=5:")
for p in [0.2, 0.4, 0.6790037305201129, 0.75]:
    r = extract(5, p)
    print(f"  p={p:.5f}: a={r['a']:.9f} b={r['b']:.9f} c={r['c']:.9f} W0={r['W0']:.9f} gapless={r['gapless']:.7f}")
