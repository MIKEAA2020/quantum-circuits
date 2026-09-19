import numpy as np
from sympy import nsimplify, Rational, sqrt, factor
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
                return a, b, c, W0
        except Exception: pass
    return None

def theta(d, p): return d - (d-1)*p

print("=== disordered side, rational p, d=2 ===")
for p in (Rational(1,2), Rational(3,4), Rational(9,10)):
    a,b,c,W0 = extract(2, float(p)); th = theta(2, float(p))
    print(f"p={p} theta={th}: a={a!r} b={b!r} c={c!r} W0={W0!r}")
    for name, val, thx in (("a", a, th), ("b", b, th), ("c", c, th), ("W0^2", W0**2, th), ("W0", W0, th)):
        try:
            e = nsimplify(val, [Rational(int(round(th*100000)),100000)], full=True, tolerance=1e-9)
            if e != 0: print(f"   {name} ~ {e}")
        except Exception as ex: pass
    # direct guesses
    print(f"   check: b-theta/5={b-th/5:.2e}  c-(4-th**2)/15={c-(4-th**2)/15:.2e}")
    print(f"   a*15={a*15!r}  a*15/(4-th*th)={a*15/(4-th*th)!r}  a/(th/5)={a/(th/5)!r}")

print("\n=== ordered side, rational p, d=2 ===")
for p in (Rational(1,5), Rational(1,10), Rational(3,20)):
    a,b,c,W0 = extract(2, float(p)); th = theta(2, float(p))
    print(f"p={p} theta={th}: a={a!r} b={b!r} c={c!r} W0={W0!r}")
    print(f"   check: b-(th^2-1)/6={b-(th*th-1)/6:.2e}")
    print(f"   a*6/(th^2-1)={a*6/(th*th-1)!r}  a*6={a*6!r}  c*6={c*6!r}")
