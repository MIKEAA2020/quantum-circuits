import numpy as np
from scipy.optimize import fsolve, brentq

def QR(k, Kd, Kh):
    c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
    c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
    Q = c2d**2 * c2h + s2d**2 * s2h - s2h*np.cos(k)
    R = 2*s2d*np.cos(k/2)
    return Q, R

def log_lambda1(m, Kd, Kh, lnW0):
    ks = (2*np.arange(1, m+1)-1)*np.pi/m
    Q, R = QR(ks, Kd, Kh)
    s = np.sqrt(np.maximum(Q**2 - R**2, 0.0))
    return m*(np.log(2.0) + 2*lnW0) + np.sum(np.log(Q + s))

ENC = {
    (16, 2, 2/5):      0.0022886508026864150,
    (16, 2, 4/25):     0.0751896333829877785,
    (16, 2, 1169/5000):0.0236927451718797759,
    (20, 2, 2/5):      0.0005002857006813122,
    (16, 3, 2/5):      6.3658872262160004e-05,
}
pc2_d2 = 0.23380962103093994
pc2_d3 = 0.45968757625671497

# --- d=2, p=0.4: two exact enclosures + L28 (7 digits) ---
eqs = [(8, np.log(ENC[(16,2,2/5)])), (10, np.log(ENC[(20,2,2/5)]))]
def F2(x):
    Kd, Kh, lnW0 = x
    return [log_lambda1(m, Kd, Kh, lnW0) - t for (m,t) in eqs]
# scan Kd: for each Kd solve (Kh, lnW0) from 2 eqs, then residual on lambda1(28)
def solve_for_Kd(Kd):
    def f2(y):
        Kh, lnW0 = y
        return [log_lambda1(8, Kd, Kh, lnW0) - eqs[0][1],
                log_lambda1(10, Kd, Kh, lnW0) - eqs[1][1]]
    y, info, ier, msg = fsolve(f2, [-0.26, np.log(0.25)], full_output=True, xtol=1e-15)
    if ier != 1: return None, None, None, np.inf
    r28 = log_lambda1(14, Kd, y[0], y[1]) - 28*np.log(0.6838449)
    return Kd, y[0], y[1], r28

# bracket Kd by scanning
best = None
for Kd in np.linspace(0.3, 0.9, 401):
    Kd_, Kh, lnW0, r28 = solve_for_Kd(Kd)
    if r28 < best[3] if best else True:
        pass
    if best is None or abs(r28) < abs(best[3]):
        best = (Kd_, Kh, lnW0, r28)
# refine around best
Kd0 = best[0]
for Kd in np.linspace(Kd0-0.002, Kd0+0.002, 401):
    Kd_, Kh, lnW0, r28 = solve_for_Kd(Kd)
    if best is None or abs(r28) < abs(best[3]):
        best = (Kd_, Kh, lnW0, r28)
Kd40, Kh40, lnW040, r28 = best
W040 = np.exp(lnW040)
print("d=2, p=0.4 (L28 matches to %.2e):" % r28)
print(f"  Kd={Kd40:.9f}  Kh={Kh40:.9f}  W0={W040:.9f}")
a = W040*np.exp(2*Kd40+Kh40); b = W040*np.exp(-Kh40); c = W040*np.exp(-2*Kd40+Kh40)
print(f"  a={a:.9f}  b={b:.9f}  c={c:.9f}")
print(f"  sinh2Kd={np.sinh(2*Kd40):.9f}  e2Kh={np.exp(2*Kh40):.9f}  e4Kh={np.exp(4*Kh40):.9f}")

# --- reference: critical point values (exact) ---
beta2 = 0.6
Kd_pc = 0.5*np.arcsinh(1/beta2); Kh_pc = 0.25*np.log(beta2**2)
lnW0_pc = brentq(lambda w: log_lambda1(8, Kd_pc, Kh_pc, w) - np.log(ENC[(16,2,1169/5000)]), -3, 3, xtol=1e-15)
W0_pc = np.exp(lnW0_pc)
a_pc = W0_pc*np.exp(2*Kd_pc+Kh_pc); b_pc = W0_pc*np.exp(-Kh_pc); c_pc = W0_pc*np.exp(-2*Kd_pc+Kh_pc)
print("\nd=2, p=pc (exact):")
print(f"  Kd={Kd_pc:.9f}  Kh={Kh_pc:.9f}  W0={W0_pc:.9f}")
print(f"  a={a_pc:.9f}  b={b_pc:.9f}  c={c_pc:.9f}")
print(f"  sinh2Kd={np.sinh(2*Kd_pc):.9f}  e2Kh={np.exp(2*Kh_pc):.9f}")

# --- p=0.16, d=2: 1 equation (L=16); scan over Kd, record families ---
print("\nd=2, p=0.16: 1-param family (Kd free): [looking for the analytic trajectory]")
t16 = np.log(ENC[(16,2,4/25)])
rows = []
for Kd in [0.4, 0.5, 0.6, 0.7]:
    def f1(y):
        Kh, lnW0 = y
        return [log_lambda1(8, Kd, Kh, lnW0) - t16, y[0]+0.3]  # dummy 2nd
    # solve Kh from a guessed relation instead: scan Kh, get lnW0
    for Kh in np.linspace(-0.5, 0.1, 7):
        w = brentq(lambda lw: log_lambda1(8, Kd, Kh, lw) - t16, -5, 2, xtol=1e-14)
        rows.append((Kd, Kh, np.exp(w)))
for (Kd, Kh, W0) in rows[::3]:
    print(f"  Kd={Kd:.2f} Kh={Kh:+.3f} -> W0={W0:.6f}")

# --- structural search: theta = d-(d-1)p ---
print("\n--- structural candidates (d=2) ---")
for name, p, Kd, Kh, W0 in [("pc", pc2_d2, Kd_pc, Kh_pc, W0_pc), ("0.4", 0.4, Kd40, Kh40, W040)]:
    th = 2 - p
    print(f" p={name}: theta={th:.6f}")
    print(f"   sinh2Kd={np.sinh(2*Kd):.7f}   (theta^2-1)/2={(th**2-1)/2:.6f}  1/beta*th_c/th={0.6/np.sinh(2*Kd):.6f}")
    print(f"   e2Kh={np.exp(2*Kh):.7f}    beta*theta/th_c={0.6*th/1.76619037896906:.6f}")
    print(f"   W0={W0:.7f}      (theta-1)*W0={W0*(th-1):.6f}")
