"""Reverse-engineer the couplings (K_d, K_h, W0)(p, d) of the compressed
two-replica operator from the deposited exact enclosures + benchmark values.

Closed form (verified statement, audit3 v2 doc Sec. 2.6):
  lambda_1(2m) = (2 W0^2)^m * prod_{j=1..m} w^+((2j-1)pi/m)
  Q(k)  = cosh^2(2Kd) cosh(2Kh) + sinh^2(2Kd) sinh(2Kh) - sinh(2Kh) cos k
  R(k)  = 2 sinh(2Kd) cos(k/2)
  w^+-  = Q +- sqrt(Q^2 - R^2)
Gapless (critical) condition: a - c = 2b  <=>  sinh(2Kd) e^{2Kh} = 1
At p_c^{(2)}(d): ac/b^2 = beta_d^2, beta_d = (d^2-1)/(d^2+1)
"""
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

def solve_point(eqs, x0):
    """eqs: list of (m, target_log_lambda1). unknowns (Kd, Kh, lnW0)."""
    def F(x):
        Kd, Kh, lnW0 = x
        return [log_lambda1(m, Kd, Kh, lnW0) - t for (m, t) in eqs]
    sol = fsolve(F, x0, full_output=True, xtol=1e-14)
    return sol[0], np.max(np.abs(F(sol[0])))

# ---- deposited data -------------------------------------------------
ENC = {  # (L, d, p) -> lambda_1 (midpoint of exact enclosure)
    (16, 2, 2/5):      0.0022886508026864150,
    (16, 2, 4/25):     0.0751896333829877785,
    (16, 2, 1169/5000):0.0236927451718797759,
    (20, 2, 2/5):      0.00050028570068131224,
    (16, 3, 2/5):      6.3658872262160004e-05,
}
L28_ROOT = 0.683844659   # lambda_1(28)^{1/28} at d=2, p=0.40 (closed form, L>=64 value quoted as bulk)

print("=== d=2, p=0.4: solve (Kd, Kh, lnW0) from lambda1(16), lambda1(20), lambda1(28) ===")
eqs = [(8,  np.log(ENC[(16,2,2/5)])),
       (10, np.log(ENC[(20,2,2/5)])),
       (14, 28*np.log(L28_ROOT))]
x0 = [0.65, -0.26, np.log(0.5)]   # informed initial guess from critical-point values
(x, res) = solve_point(eqs, x0)
Kd40, Kh40, W0_40 = x[0], x[1], np.exp(x[2])
print(f"  residual {res:.2e}   Kd={Kd40:.10f}  Kh={Kh40:.10f}  W0={W0_40:.10f}")
print(f"  a={W0_40*np.exp(2*Kd40+Kh40):.8f}  b={W0_40*np.exp(-Kh40):.8f}  c={W0_40*np.exp(-2*Kd40+Kh40):.8f}")
print(f"  sinh(2Kd)={np.sinh(2*Kd40):.8f}  e^{{2Kh}}={np.exp(2*Kh40):.8f}  e^{{4Kh}}={np.exp(4*Kh40):.8f}")
# cross-check the 4th enclosure at p=0.4: none besides L=16,20. good.

print("\n=== d=2, p=p_c: critical conditions + lambda1(16) ===")
beta2 = 3/5
Kd_pc = 0.5*np.arcsinh(1/beta2)      # sinh(2Kd) = 1/beta
Kh_pc = 0.25*np.log(beta2**2)        # e^{4Kh} = beta^2
t16 = np.log(ENC[(16,2,1169/5000)])
f = lambda lnW0: log_lambda1(8, Kd_pc, Kh_pc, lnW0) - t16
lnW0_pc = brentq(f, -3, 3, xtol=1e-15)
W0_pc = np.exp(lnW0_pc)
print(f"  Kd={Kd_pc:.10f} (=0.5 asinh(5/3))  Kh={Kh_pc:.10f} (=0.25 ln(9/25))")
print(f"  W0={W0_pc:.10f}")
print(f"  a={W0_pc*np.exp(2*Kd_pc+Kh_pc):.8f}  b={W0_pc*np.exp(-Kh_pc):.8f}  c={W0_pc*np.exp(-2*Kd_pc+Kh_pc):.8f}")
print(f"  gapless check sinh(2Kd)e^2Kh = {np.sinh(2*Kd_pc)*np.exp(2*Kh_pc):.12f}")

print("\n=== structural inspection: a,b,c at p=0.4 vs p=pc vs p=0.16 ===")
# at p=0.16 we have only lambda1(16): show the 1-param family and test candidate
# functional forms once the two solved points reveal the pattern.
for (p, Kd, Kh, W0) in [(0.4, Kd40, Kh40, W0_40), (1169/5000, Kd_pc, Kh_pc, W0_pc)]:
    a = W0*np.exp(2*Kd+Kh); b = W0*np.exp(-Kh); c = W0*np.exp(-2*Kd+Kh)
    print(f"  p={p:.4f}: a={a:.8f} b={b:.8f} c={c:.8f}  (a-2b-c)={a-2*b-c:+.2e}")
    print(f"           1-p={1-p:.4f}  a+(d^2-2)d?.. ")
