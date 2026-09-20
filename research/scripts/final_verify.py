"""GRAND VERIFICATION: closed-form couplings vs ALL deposited numbers."""
import numpy as np
from scipy.optimize import brentq

def weights(d, p):
    th = d - (d-1)*p
    beta = (d*d-1)/(d*d+1)
    thc = beta + np.sqrt(beta*beta+1)
    if th >= thc:   # ordered
        a = (th+1)**2/(2*(d*d+1)); b = (th*th-1)/(2*(d*d-1)); c = (th-1)**2/(2*(d*d+1))
        W0 = (th*th-1)/(2*np.sqrt(d**4-1))
    else:           # disordered
        a = (d*d*th*th-1)/(d**4-1); b = th/(d*d+1); c = (d*d-th*th)/(d**4-1)
        W0 = np.sqrt(th*(d*d-1))*((d*d*th*th-1)*(d*d-th*th))**0.25/(d**4-1)
    return a, b, c, W0

def couplings(d, p):
    a, b, c, W0 = weights(d, p)
    return 0.25*np.log(a/c), 0.25*np.log(a*c/b/b), W0

def wpm(k, Kd, Kh):
    k = np.atleast_1d(k).astype(float)
    c2d, s2d = np.cosh(2*Kd), np.sinh(2*Kd)
    c2h, s2h = np.cosh(2*Kh), np.sinh(2*Kh)
    Q = c2d**2*c2h + s2d**2*s2h - s2h*np.cos(k); R = 2*s2d*np.cos(k/2)
    s = np.sqrt(np.maximum(Q*Q-R*R, 0.0)); return Q+s, Q-s

def log_lambda1(L, d, p):
    m = L//2
    Kd, Kh, W0 = couplings(d, p)
    ks = (2*np.arange(1, m+1)-1)*np.pi/m
    wp, _ = wpm(ks, Kd, Kh)
    return m*(np.log(2.0)+2*np.log(W0)) + np.sum(np.log(wp))

def gaps(L, d, p):
    """(log(l1/lodd), log(l1/leps)) with Kaufman parity rules."""
    m = L//2
    Kd, Kh, W0 = couplings(d, p)
    beta = (d*d-1)/(d*d+1); thc = beta+np.sqrt(beta*beta+1)
    above = (d-(d-1)*p) < thc
    kp = (2*np.arange(1, m+1)-1)*np.pi/m; ko = 2*np.pi*np.arange(m)/m
    wpp, wmp = wpm(kp, Kd, Kh); wpo, wmo = wpm(ko, Kd, Kh)
    l1 = np.sum(np.log(wpp))
    if not above:
        lodd = np.sum(np.log(wpo))          # odd: even # of '-'
    else:
        lodd = np.log(wmo[0]) + np.sum(np.log(wpo[1:]))   # odd: odd # of '-', '-' at k=0
    g = np.log(wpp) - np.log(np.maximum(wmp, 1e-300))
    leps = l1 - 2*np.min(g)                  # even: even # of '-' -> 2-mode state
    return l1 - lodd, l1 - leps

print("=== 1. THE FIVE EXACT ENCLOSURES ===")
ENC = [ (16,2,"2/5",0.0022886508026864124561,0.0022886508026864175903),
        (16,2,"4/25",0.075189633382987646,0.075189633382987911),
        (16,2,"1169/5000",0.0236927451718797476,0.0236927451718798042),
        (20,2,"2/5",0.00050028570068131041,0.00050028570068131407),
        (16,3,"2/5",6.3658872262159916e-05,6.3658872262160092e-05) ]
for L, d, ps, lo, hi in ENC:
    p = eval(ps)
    lam = np.exp(log_lambda1(L, d, p))
    ok = lo <= lam <= hi
    print(f"  L={L} d={d} p={ps}: closed-form lam1={lam:.16f}  inside enclosure: {ok}")

print("\n=== 2. lambda1(28)^{1/28} at d=2, p=0.40 ===")
for L in (28, 32, 64):
    print(f"  L={L}: {np.exp(log_lambda1(L,2,0.4)/L):.9f}  (text quote: 0.6838449; bulk: 0.683844659)")

print("\n=== 3. BENCHMARK CROSSINGS (deposited: d=2: .23319 .23348 .23361 .23368; d=3: .45934 .45950 .45957 .45961) ===")
for d, tgt in ((2, [0.23319,0.23348,0.23361,0.23368]), (3,[0.45934,0.45950,0.45957,0.45961])):
    beta = (d*d-1)/(d*d+1); thc = beta+np.sqrt(beta*beta+1); pc = (d-thc)/(d-1)
    out = []
    for (L1, L2) in ((16,20),(20,24),(24,28),(28,32)):
        f = lambda p: L1*gaps(L1,d,p)[0]-L2*gaps(L2,d,p)[0]
        out.append(brentq(f, pc-0.0015, pc-0.00002, xtol=1e-12))
    print(f"  d={d}: {[f'{x:.5f}' for x in out]}  vs {tgt}")

print("\n=== 4. RATIO ROW at p_c (deposited 0.1220...0.1243 -> 0.125) ===")
for d in (2,3,5):
    beta = (d*d-1)/(d*d+1); thc = beta+np.sqrt(beta*beta+1); pc = (d-thc)/(d-1)
    r = [gaps(L,d,pc)[0]/gaps(L,d,pc)[1] for L in (16,20,24,28,32)]
    print(f"  d={d}: {[f'{x:.5f}' for x in r]}")

print("\n=== 5. p_eff at p=0.16, d=2 (deposited: L=8: 0.104948, L=12: 0.101111, L->inf: 0.0920) ===")
def p_eff(L, d, p):
    if L is None:
        m = 512
        h = 1e-7
        f = lambda pp: log_lambda1(2*m, d, pp)/(2*m)
    else:
        h = 1e-7
        f = lambda pp: log_lambda1(L, d, pp)/L
    der = (f(p+h)-f(p-h))/(2*h)
    return p + p*(1-p)*der
for L in (8, 12, None):
    print(f"  L={L}: p_eff = {p_eff(L,2,0.16):.6f}")

print("\n=== 6. p_eff at pc2 (deposited: d=2: 0.14929105, d=3: 0.25838537, d=5: 0.35469849) ===")
for d, Lref, tgt in ((2,16,0.14929105315176264),(3,12,0.25838536801495504),(5,12,0.3546984899540994)):
    beta = (d*d-1)/(d*d+1); thc = beta+np.sqrt(beta*beta+1); pc = (d-thc)/(d-1)
    h = 1e-7
    f = lambda pp: log_lambda1(Lref, d, pp)/Lref
    pe = pc + pc*(1-pc)*(f(pc+h)-f(pc-h))/(2*h)
    print(f"  d={d}: p_eff(pc2) = {pe:.8f}  vs {tgt}")

print("\n=== 7. bare p with p_eff=0.16 (deposited: 0.2460718781652951) ===")
m = 512
f = lambda pp: p_eff(None, 2, pp) - 0.16
print(f"  bare p = {brentq(f, 0.2, 0.3, xtol=1e-12):.10f}")

print("\n=== 8. critical points (deposited: 0.23381, 0.45969, 0.679) ===")
for d in (2,3,5):
    beta = (d*d-1)/(d*d+1); thc = beta+np.sqrt(beta*beta+1)
    print(f"  d={d}: p_c^(2) = {(d-thc)/(d-1):.11f}")
