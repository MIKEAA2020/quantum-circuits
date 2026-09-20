"""Verify the closed-form machinery at the exact critical couplings.
Ratio row deposited (tab:benchmark): L=16..32 -> 0.1220, ..., 0.1243 (-> 1/8 = 0.125).
Crossings deposited (d=2): p*(16,20)=0.23319, (20,24)=0.23348, (24,28)=0.23361, (28,32)=0.23368.
"""
import numpy as np

def QR(k, Kd, Kh):
    c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
    c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
    Q = c2d**2*c2h + s2d**2*s2h - s2h*np.cos(k)
    R = 2*s2d*np.cos(k/2)
    return Q, R

def wpm(k, Kd, Kh):
    Q, R = QR(np.atleast_1d(k), Kd, Kh)
    s = np.sqrt(np.maximum(Q**2 - R**2, 0.0))
    return Q+s, Q-s

def sector_logs(m, Kd, Kh):
    """log-products over the two momentum grids (W0-independent parts)."""
    kp = (2*np.arange(1, m+1)-1)*np.pi/m      # K+ antiperiodic (even sector)
    ko = 2*np.pi*np.arange(m)/m               # K- periodic (odd sector)
    wpp, wpm_p = wpm(kp, Kd, Kh)              # even grid
    wpo, wpm_o = wpm(ko, Kd, Kh)              # odd grid
    log_l1   = np.sum(np.log(wpp))            # even all+
    log_lodd = np.sum(np.log(wpo))            # odd all+  (p < p_c side)
    # second even: best single '-' on the even grid
    gaps = np.log(wpp) - np.log(np.maximum(wpm_p, 1e-300))
    log_leps = log_l1 - np.min(gaps)
    return log_l1, log_lodd, log_leps

beta = {2: 3/5, 3: 4/5, 5: 24/26}
print("=== ratio row at p_c (exact couplings), d=2 ===")
Kd_c = 0.5*np.arcsinh(1/beta[2]); Kh_c = 0.25*np.log(beta[2]**2)
print(f"Kd={Kd_c:.10f} Kh={Kh_c:.10f}")
print("deposited ratio row: L=16:0.1220, 20:?, 24:?, 28:?, 32:0.1243 -> 0.125")
for L in (16, 20, 24, 28, 32):
    m = L//2
    l1, lodd, leps = sector_logs(m, Kd_c, Kh_c)
    ratio = (l1-lodd)/(l1-leps)
    print(f"  L={L}: L*log(l1/lodd)={L*(l1-lodd):.5f}  L*log(l1/leps)={L*(l1-leps):.5f}  ratio={ratio:.5f}")
print("amplitude limits: pi*beta/2 =", np.pi*beta[2]/2, " 4*pi*beta =", 4*np.pi*beta[2])

print("\n=== d=3 ratio row at p_c ===")
Kd3 = 0.5*np.arcsinh(1/beta[3]); Kh3 = 0.25*np.log(beta[3]**2)
for L in (16, 20, 24, 28, 32):
    m = L//2
    l1, lodd, leps = sector_logs(m, Kd3, Kh3)
    print(f"  L={L}: ratio={((l1-lodd)/(l1-leps)):.5f}")
