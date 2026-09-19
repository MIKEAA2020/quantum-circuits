import numpy as np
from scipy.optimize import brentq
exec(open('final_verify.py').read().split('print("=== 1.')[0])

print("=== enclosures at full precision ===")
ENC = [ (16,2,2/5,0.0022886508026864124561,0.0022886508026864175903),
        (16,2,4/25,0.075189633382987646,0.075189633382987911),
        (16,2,1169/5000,0.0236927451718797476,0.0236927451718798042),
        (20,2,2/5,0.00050028570068131041,0.00050028570068131407),
        (16,3,2/5,6.3658872262159916e-05,6.3658872262160092e-05) ]
for L, d, p, lo, hi in ENC:
    lam = np.exp(log_lambda1(L, d, p))
    mid = 0.5*(lo+hi)
    print(f"  L={L} d={d} p={p}: lam1={lam:.19f}")
    print(f"     enclosure mid={mid:.19f}  rel-dev={abs(lam-mid)/mid:.2e}  width={(hi-lo)/mid:.2e}")

def p_eff(L, d, p):
    h = 1e-7
    if L is None:
        f = lambda pp: log_lambda1(1024, d, pp)/1024
    else:
        f = lambda pp: log_lambda1(L, d, pp)/L
    der = (f(p+h)-f(p-h))/(2*h)
    return p + p*(1-p)*der/2     # p_eff = p + p(1-p) dlog(lam1)/dp /(2L) = p + p(1-p) [d(log lam1/L)/dp]/2

print("\n=== p_eff at p=0.16, d=2 (deposited: 0.104948, 0.101111, 0.0920) ===")
for L in (8, 12, None):
    print(f"  L={L}: p_eff = {p_eff(L,2,0.16):.6f}")

print("\n=== p_eff at pc2 (deposited: 0.14929105, 0.25838537, 0.35469849) ===")
for d, Lref, tgt in ((2,16,0.14929105315176264),(3,12,0.25838536801495504),(5,12,0.3546984899540994)):
    beta = (d*d-1)/(d*d+1); thc = beta+np.sqrt(beta*beta+1); pc = (d-thc)/(d-1)
    print(f"  d={d}: p_eff(pc2) = {p_eff(Lref,d,pc):.8f}  vs {tgt}")

print("\n=== bare p with p_eff(thermo) = 0.16 (deposited 0.2460718781652951) ===")
f = lambda pp: p_eff(None, 2, pp) - 0.16
print(f"  bare p = {brentq(f, 0.18, 0.35, xtol=1e-13):.10f}")

print("\n=== tilt chain Z2 check at L=8, t=4, p=0.16 (deposited: Z2 exact 1.4796e-2) ===")
# Z2 ~ lam1^(t/L per period)... t=4=L/2: half a period? Try lam1^(t/(2L)):
lam = np.exp(log_lambda1(8, 2, 0.16))
for expo in (0.5, 1.0):
    print(f"  lam1^{expo} = {lam**expo:.6e}")
