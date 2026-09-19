"""Fixed parity rule: even sector needs EVEN # of '-'. lam_eps = two-mode state (+-pi/m).
Verify ratio row; then fit the local trajectory (Kd', Kh') at p_c from the 4 crossings."""
import numpy as np
from scipy.optimize import least_squares

def wpm(k, Kd, Kh):
    c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
    c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
    Q = c2d**2*c2h + s2d**2*s2h - s2h*np.cos(k)
    R = 2*s2d*np.cos(k/2)
    s = np.sqrt(np.maximum(Q**2 - R**2, 0.0))
    return Q+s, Q-s

def gaps_L(m, Kd, Kh):
    """(L*log(l1/lodd), L*log(l1/leps)) with correct parity rules, L=2m, p<p_c side."""
    L = 2*m
    kp = (2*np.arange(1, m+1)-1)*np.pi/m
    ko = 2*np.pi*np.arange(m)/m
    wpp, wmp = wpm(kp, Kd, Kh)
    wpo, wmo = wpm(ko, Kd, Kh)
    l1 = np.sum(np.log(wpp))
    lodd = np.sum(np.log(wpo))
    # even sector: even # of '-'. 2nd = best 2-mode: '- at +-k*'
    g = np.log(wpp) - np.log(np.maximum(wmp, 1e-300))
    leps = l1 - 2*np.min(g)
    return L*(l1-lodd), L*(l1-leps)

beta = {2: 3/5, 3: 4/5}
Kd_c = 0.5*np.arcsinh(1/beta[2]); Kh_c = 0.25*np.log(beta[2]**2)
print("=== ratio row (fixed parity), d=2, p_c ===")
print("deposited: L=16: 0.1220 ... L=32: 0.1243 (-> 0.125)")
for L in (16, 20, 24, 28, 32):
    go, ge = gaps_L(L//2, Kd_c, Kh_c)
    print(f"  L={L}: odd-gap*L={go:.5f} eps-gap*L={ge:.5f} ratio={go/ge:.5f}")

print("\n=== fit (Kd', Kh') at p_c from the 4 d=2 crossings ===")
pc = 0.23380962103093994
targets = [((16,20), 0.23319), ((20,24), 0.23348), ((24,28), 0.23361), ((28,32), 0.23368)]
def resid(v):
    a, b = v  # Kd', Kh' at p_c
    out = []
    for (L1, L2), tgt in targets:
        def D(p):
            g1, _ = gaps_L(L1//2, Kd_c + a*(p-pc), Kh_c + b*(p-pc))
            g2, _ = gaps_L(L2//2, Kd_c + a*(p-pc), Kh_c + b*(p-pc))
            return g1 - g2
        # find crossing in [pc-0.001, pc-0.0001]
        lo, hi = pc-0.0012, pc-0.00005
        fl, fh = D(lo), D(hi)
        if fl*fh > 0:
            out.append(1e-3); continue
        for _ in range(80):
            mid = 0.5*(lo+hi)
            if D(lo)*D(mid) <= 0: hi = mid
            else: lo = mid
        out.append(0.5*(lo+hi) - tgt)
    return np.array(out)
sol = least_squares(resid, [-2.0, 2.0], xtol=1e-14, ftol=1e-14)
print(f"  Kd'={sol.x[0]:.6f}  Kh'={sol.x[1]:.6f}   residuals={resid(sol.x)}")
print(f"  -> d/dp sinh(2Kd) = {2*np.cosh(2*Kd_c)*sol.x[0]:.4f}; d/dp e^2Kh = {2*np.exp(2*Kh_c)*sol.x[1]:.4f}")

print("\n=== same for d=3 (crossings 0.45934, 0.45950, 0.45957, 0.45961) ===")
Kd3c = 0.5*np.arcsinh(1/beta[3]); Kh3c = 0.25*np.log(beta[3]**2)
pc3 = 0.45968757625671497
targets3 = [((16,20), 0.45934), ((20,24), 0.45950), ((24,28), 0.45957), ((28,32), 0.45961)]
def resid3(v):
    a, b = v
    out = []
    for (L1, L2), tgt in targets3:
        def D(p):
            g1, _ = gaps_L(L1//2, Kd3c + a*(p-pc3), Kh3c + b*(p-pc3))
            g2, _ = gaps_L(L2//2, Kd3c + a*(p-pc3), Kh3c + b*(p-pc3))
            return g1 - g2
        lo, hi = pc3-0.0012, pc3-0.00005
        if D(lo)*D(hi) > 0:
            out.append(1e-3); continue
        for _ in range(80):
            mid = 0.5*(lo+hi)
            if D(lo)*D(mid) <= 0: hi = mid
            else: lo = mid
        out.append(0.5*(lo+hi) - tgt)
    return np.array(out)
sol3 = least_squares(resid3, [-1.5, 1.5], xtol=1e-14, ftol=1e-14)
print(f"  Kd'={sol3.x[0]:.6f}  Kh'={sol3.x[1]:.6f}   residuals={resid3(sol3.x)}")
