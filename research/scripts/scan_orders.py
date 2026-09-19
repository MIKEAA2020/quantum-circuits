import numpy as np
from itertools import product
exec(open('quantum_transfer2.py').read().split("L = 4")[0])  # reuse build_T

# Ising m=2 spectrum at the SOLVED couplings (d=2, p=0.4) for comparison:
def ising_m2(Kd, Kh, W0):
    def wpm(k):
        c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
        c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
        Q = c2d**2*c2h + s2d**2*s2h - s2h*np.cos(k); R = 2*s2d*np.cos(k/2)
        s = np.sqrt(max(Q**2-R**2,0.0)); return Q+s, Q-s
    wp2, wm2 = wpm(np.pi/2); wp0, _ = wpm(0.0); wpp, _ = wpm(np.pi)
    A = (2*W0**2)**2 * wp2*wp2      # even all+
    B = (2*W0**2)**2 * wm2*wm2      # even both-
    C = (2*W0**2)**2 * wp0*wpp      # odd all+
    return sorted([A,B,C], reverse=True)

ising_ref = ising_m2(0.47276, -0.145385, 0.2774049)
print("Ising m=2 (solved coupl. p=0.4):", np.round(ising_ref, 6))

orders = ["MAMB","MBMA","AMMB","BMMA","MABM","MBAM","ABMM","BAMM",
          "MAM","MBM","AMXBM","MAAM","MBBM","AAM","BBM"]
for order in orders:
    try:
        T = build_T(4, 2, 0.4, order)
        ev = np.linalg.eigvals(T)
        evr = np.sort(np.real(ev[np.abs(np.imag(ev)) < 1e-9*np.max(np.abs(ev))]))[::-1]
        print(f"order={order:8s}: top4 = {np.round(evr[:4], 6)}")
    except Exception as e:
        print(f"order={order}: ERR {e}")
