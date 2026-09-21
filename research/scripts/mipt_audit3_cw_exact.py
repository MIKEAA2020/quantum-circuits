"""
mipt_audit3_cw_exact.py -- exact-rational Collatz-Wielandt enclosures of the
Perron eigenvalue lambda_1 of the compressed two-replica period map
(the N3 Level-B certificates of the deposited audit round 3, reproduced).

The period map C_comp = M1 M2 with
    (M1)_{s's} = prod_k w(s'_k | s_k, s_{k+1}),
    (M2)_{s's} = prod_k w(s_k | s'_k, s'_{k+1}),
where w(s'|s,s+) is the exact rational bond weight (a, b, c)(theta, d)
(rational for rational p, d).  Collatz-Wielandt: for a positive matrix A and
positive x,  min_i (Ax)_i/x_i <= lambda_1(A) <= max_i (Ax)_i/x_i, evaluated
in exact integer arithmetic (integer matrices over the common weight
denominator).  The iteration is warm-started from the float64 Perron vector
and run until the relative width is below ~1e-15 (the deposited widths).

Deposited certificates (audit3_cw_exact.json):
  L=16 d=2 p=2/5       [0.0022886508026864124561, 0.0022886508026864175903] rel 2.2e-15
  L=16 d=2 p=4/25      [0.075189633382987646,    0.075189633382987911]    rel 3.5e-15
  L=16 d=2 p=1169/5000 [0.0236927451718797476,   0.0236927451718798042]   rel 2.4e-15
  L=20 d=2 p=2/5       [0.00050028570068131041,  0.00050028570068131407]  rel 7.3e-15
  L=16 d=3 p=2/5       [6.3658872262159916e-05,  6.3658872262160092e-05]  rel 2.9e-15
"""
import json, os, sys, math
from fractions import Fraction
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)
LOGF = open(os.path.join(LOG, "mipt_audit3_cw_exact.log"), "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOGF.write(s + "\n"); LOGF.flush()

def exact_weights_int(d, p: Fraction):
    """(A, B, C, Delta): the weights a=A/Delta, b=B/Delta, c=C/Delta exactly."""
    th = Fraction(d) - Fraction(d - 1) * p
    lhs = Fraction(d * d + 1) * th * th - Fraction(2 * (d * d - 1)) * th - Fraction(d * d + 1)
    if lhs >= 0:      # ordered branch (theta >= theta_c)
        a = (th + 1) ** 2 / Fraction(2 * (d * d + 1))
        b = (th * th - 1) / Fraction(2 * (d * d - 1))
        c = (th - 1) ** 2 / Fraction(2 * (d * d + 1))
    else:             # disordered branch
        a = (Fraction(d * d) * th * th - 1) / Fraction(d ** 4 - 1)
        b = th / Fraction(d * d + 1)
        c = (Fraction(d * d) - th * th) / Fraction(d ** 4 - 1)
    Delta = 1
    for v in (a, b, c):
        Delta = Delta * v.denominator // math.gcd(Delta, v.denominator)
    return (a * Delta).numerator, (b * Delta).numerator, (c * Delta).numerator, Delta

def build_M_int(m, d, p: Fraction):
    """M1 (integer matrix over Delta^m) and the ring shift tau index.
    C_comp = M1^2 tau with (tau s)_k = s_{k-1} (E^T = E tau, [D_h, tau] = 0),
    so M2 = M1 tau is the column-permuted M1 and all entries are rational."""
    A, B, C, Delta = exact_weights_int(d, p)
    N = 1 << m
    Wsel = [[[ (A if sp == s else C) if s == su else B
               for sp in (0, 1)] for s in (0, 1)] for su in (0, 1)]
    def bit(n, k): return (n >> k) & 1
    M1 = [[0] * N for _ in range(N)]
    for sp in range(N):
        for s in range(N):
            v = 1
            for k in range(m):
                v *= Wsel[bit(s, (k + 1) % m)][bit(s, k)][bit(sp, k)]
            M1[sp][s] = v
    tau = [0] * N
    for n in range(N):
        for k in range(m):
            tau[n] |= ((n >> ((k - 1) % m)) & 1) << k
    return M1, tau, Delta ** m

def cw_run(M1, tau, den, N, warm=None, target=1e-16, max_iter=60):
    """Collatz-Wielandt brackets for lambda_1(M1^2 tau) in exact integers.
    C x = M1 (M1 (tau x)): apply the permutation, then two integer matvecs."""
    if warm is None:
        y = [1 + i for i in range(N)]
    else:
        y = warm
    D2 = den * den
    lo = hi = None
    for it in range(max_iter):
        # x_perm[i] = x[tau(i)]  (tau acts on the index of x)
        yperm = [y[tau[i]] for i in range(N)]
        z = [sum(M1[i][j] * yperm[j] for j in range(N)) for i in range(N)]
        w = [sum(M1[i][j] * z[j] for j in range(N)) for i in range(N)]
        ratios = [Fraction(w[i], D2 * y[i]) for i in range(N)]
        lo, hi = min(ratios), max(ratios)
        rel = float((hi - lo) / lo)
        y = w
        if rel < target:
            return lo, hi, it + 1, rel
    return lo, hi, max_iter, rel

def float_perron(M1, tau, den, N, iters=3000):
    Mf = np.array(M1, dtype=float) / den
    tauM = np.zeros((N, N))
    for j in range(N): tauM[tau[j], j] = 1.0
    Af = Mf @ Mf @ tauM
    rng = np.random.default_rng(0)
    v = rng.random(N)
    for _ in range(iters):
        w = Af @ v; v = w / np.linalg.norm(w)
    # scale to exact integers
    scale = 1 << 62
    vi = np.round(np.abs(v) / np.max(np.abs(v)) * scale).astype(object)
    return [int(x) for x in vi]

DEPOSITED = [
    (16, 2, "2/5",       "0.0022886508026864124561", "0.0022886508026864175903", "2.2e-15"),
    (16, 2, "4/25",      "0.075189633382987646",     "0.075189633382987911",     "3.5e-15"),
    (16, 2, "1169/5000", "0.0236927451718797476",    "0.0236927451718798042",    "2.4e-15"),
    (20, 2, "2/5",       "0.00050028570068131041",   "0.00050028570068131407",   "7.3e-15"),
    (16, 3, "2/5",       "6.3658872262159916e-05",   "6.3658872262160092e-05",   "2.9e-15"),
]
CLOSED = {
    (16, 2, "2/5"):       "0.002288650802686413894529",
    (16, 2, "4/25"):      "0.07518963338298773124186",
    (16, 2, "1169/5000"): "0.02369274517187977453766",
    (20, 2, "2/5"):       "0.0005002857006813118520095",
    (16, 3, "2/5"):       "0.00006365887226215996231924",
}

res = []
log("== Exact-rational Collatz-Wielandt enclosures of lambda_1(C_comp) ==")
allok = True
for L, d, ps, dlo, dhi, drel in DEPOSITED:
    p = Fraction(ps); m = L // 2
    M1, tau, den = build_M_int(m, d, p)
    N = 1 << m
    warm = float_perron(M1, tau, den, N)
    lo, hi, it, rel = cw_run(M1, tau, den, N, warm=warm, target=5e-16, max_iter=40)
    dloF, dhiF = Fraction(dlo), Fraction(dhi)
    clo = Fraction(CLOSED[(L, d, ps)])
    ok = (lo <= dhiF) and (hi >= dloF) and (lo <= clo <= hi) and (dloF <= clo <= dhiF)
    allok &= ok
    log(f"L={L} d={d} p={ps} ({it} exact CW iterations after warm start):")
    log(f"   reproduced : [{float(lo):.19f}, {float(hi):.19f}]  rel width {rel:.1e}")
    log(f"   deposited  : [{dlo}, {dhi}]  rel {drel}")
    log(f"   closed form: {CLOSED[(L,d,ps)]}  -> inside both: reproduced {lo<=clo<=hi}, deposited {dloF<=clo<=dhiF}")
    log(f"   overlap+containment consistent: {ok}")
    res.append(dict(L=L, d=d, p=ps, lo=str(float(lo)), hi=str(float(hi)),
                    rel_width=rel, iterations=it,
                    deposited=dict(lo=dlo, hi=dhi, rel=drel),
                    closed_form=CLOSED[(L, d, ps)], consistent=bool(ok)))

json.dump(res, open(os.path.join(OUT, "audit3_cw_exact.json"), "w"), indent=1)
log(f"\nALL CONSISTENT: {allok}")
log(f"written {os.path.join(OUT, 'audit3_cw_exact.json')}")
LOGF.close()
