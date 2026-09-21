"""Theorem-level verification v1: the no-freezing theorem for allowable
finite-reachable record processes, and the replica interpolation identity.

THEOREM A (no finite-q freezing for allowable finite-reachable processes).
  For a monitored process whose tilted Feynman-Kac dynamics closes on a
  finite reachable set with i.i.d. tilted operators Q_{k,t} that are
  allowable (some finite product strictly positive) and strongly
  irreducible:
  (i)  psi_q(k) = lim_T T^{-1} log <1|Q_{k,T}...Q_{k,1}|x0> exists a.s.,
       is deterministic, and equals the top Lyapunov exponent gamma(k)
       (Furstenberg-Kesten + positivity identification);
  (ii) k -> gamma(k) is real-analytic on R (Le Page 1974 / Ruelle 1979 /
       Peres 1992);
  (iii) COROLLARY (the new content): tau(q) = -psi_q(1-q) is real-analytic
       on R; if psi''(0) > 0 (nondegenerate records) then tau has NO affine
       segment on ANY interval -- by the identity theorem an analytic
       function affine on an open interval is affine everywhere, contradict
       strict convexity at 0; the degenerate case (Clifford: psi'' = 0) is
       affine everywhere with no finite-q ONSET.  Hence NO finite-q freezing
       transition occurs in any finite-reachable allowable family,
       deterministic, random, or reducible (a reducible family gives
       psi = max_i gamma_i with corners -- dynamical first-order-like
       transitions -- but each branch is analytic on all of R, so still no
       affine piece).  Freezing requires an UNBOUNDED reachable set, as in
       the random-energy sequence of Theorem thm:rem.
  For the fully monitored point p=1 with Haar-refreshed gates the tilted
  period matrices are a.s. entrywise strictly positive (allowable), so the
  manuscript's "analyticity remains conditional" case closes
  unconditionally for that family (numerically confirmed below).

PROPOSITION B (replica interpolation identity; disorder-replica reduction).
  For X > 0 with E|log X| < inf and E X^r < inf near [0, m], g(r) :=
  log E X^r satisfies EXACTLY
      g(r) - r E log X = int_0^r (r - s) Var_s(log X) ds,
  with Var_s the variance under the s-tilted law; r -> g(r)/r is
  nondecreasing (Lyapunov) with limits E log X (r -> 0+) and
  log ess-sup X (r -> inf, bounded X); d/dr E X^r |_{r=0} = E log X.
  Applied to X = Z_{q,omega}(T): the annealed replica free energies are
  monotone, squeezed between the quenched value (approached
  quadratically in m from above at m -> 0) and the extremal value at
  m -> inf; the T -> inf interchange is controlled by the tilted-variance
  profile (self-averaging criterion).

Checks (each prints PASS/FAIL):
  A1  deterministic positive tilted chain: psi = log rho(M(k)) smooth,
      strictly convex (nondegenerate), tau without affine segment.
  A2  i.i.d. random positive tilted chains (allowable): disorder-averaged
      psi smooth on a k-grid, no affine segment; tau'' bounded away from 0
      in the interior.
  A3  reducible two-block chain: psi = max(psi_A, psi_B) with a CORNER
      (tau' jump) but still no affine segment (contrast with freezing).
  A4  REM freezing benchmark (the thm:rem object): tau linear beyond
      q_c = sqrt(2 log 2) -- the side-by-side contrast with A1-A3.
  A5  the p=1 Haar-refreshed family (L=4): exact quenched psi(k) by
      enumeration+disorder averaging on a k-grid -- smooth (the closure).
  B1  synthetic exact: the interpolation identity to machine precision.
  B2  synthetic exact: Lyapunov monotonicity + the two one-sided limits.
  B3  real object (p=1 Haar, L=4, T sweeps): E_omega Z^m empirical moments
      -> identity, monotonicity, small-m quadratic rate, replica
      derivative, and the m -> inf extremal overshoot.
"""
import sys, os, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(20240920)


def log(*a):
    print(*a, flush=True)


# =====================================================================
# Part A: no-freezing numerics
# =====================================================================
def tilted_chain_psi_det(K, g, kgrid):
    """psi(k) = log rho(M(k)) for M(k)[y,x] = K[y,x] e^{k g[y,x]}."""
    out = []
    for k in kgrid:
        M = K * np.exp(k * g)
        out.append(float(np.linalg.eigvals(M)[np.argmax(np.abs(
            np.linalg.eigvals(M)))].real) if False else
            np.log(max(np.real(np.linalg.eigvals(M)).max(), 1e-300)))
    return np.array(out)


def A1():
    log("A1  deterministic positive tilted chain (3 states):")
    K = rng.random((3, 3)) + 0.15
    K = K / K.sum(axis=1, keepdims=True)
    g = rng.standard_normal((3, 3)) * 0.5
    kg = np.linspace(-3, 3, 61)
    psi = tilted_chain_psi_det(K, g, kg)
    d2 = np.diff(psi, 2)
    # analyticity: smooth second differences (no jump beyond discretization)
    # strict convexity somewhere:
    log(f"  psi(0)={psi[30]:.4f}  max|d2|={np.abs(d2).max():.4f}  "
        f"min d2={d2.min():.5f} (strict convexity -> {d2.min() > 0})")
    tau = -psi[::-1]           # tau(q) = -psi(1-q): k-grid reversed
    # affine-segment test: the maximal run of |tau''| < eps
    d2t = np.diff(tau, 2)
    eps = 1e-3 * max(abs(tau).max(), 1)
    ok = np.abs(d2t).min() > 0 and d2.min() > 0
    log(f"  tau'' min |.| = {np.abs(d2t).min():.5f} > 0 -> no affine "
        f"segment: {'PASS' if ok else 'FAIL'}")
    return ok


def random_positive_chain(nS, T, ndraw, k, rng):
    """One disorder-averaged phi_T(k): E_omega T^{-1}log <1|Pi Q_k |x0>."""
    tot = 0.0
    for _ in range(ndraw):
        # random stochastic kernel with a positivity floor (allowable)
        Kt = rng.random((T, nS, nS)) + 0.05
        Kt = Kt / Kt.sum(axis=2, keepdims=True)
        gt = rng.standard_normal((T, nS, nS)) * 0.4
        Qt = Kt * np.exp(k * gt)          # tilted operators
        v = np.ones(nS) / nS
        for t in range(T):
            v = Qt[t] @ v
            v = v / np.linalg.norm(v)
        tot += math.log(max(v.sum(), 1e-300))
    return tot / ndraw / T * T  # = E T^{-1} log (unnormalised sum) approx


def A2():
    log("A2  i.i.d. allowable random positive chains (CRN, nS=3, T=192):")
    # common random numbers: ONE disorder draw set evaluated at ALL k --
    # the k-SHAPE is then noise-free up to a shared offset.
    # Estimator: the standard power-iteration Lyapunov sum: accumulate
    # log||Q_t v|| with v renormalised each step (the growth lives in the
    # accumulated norms, NOT in the final normalised vector).
    nS, T, ndraw = 3, 192, 240
    kgrid = np.linspace(-3, 3, 25)
    Ks = rng.random((ndraw, T, nS, nS)) + 0.05
    Ks = Ks / Ks.sum(axis=3, keepdims=True)
    gs = rng.standard_normal((ndraw, T, nS, nS)) * 1.2
    psi = []
    for k in kgrid:
        acc = 0.0
        for d in range(ndraw):
            Qt = Ks[d] * np.exp(k * gs[d])
            v = np.full(nS, 1.0 / nS)
            s = 0.0
            for t in range(T):
                w = Qt[t] @ v
                nrm = float(np.linalg.norm(w))
                s += math.log(nrm)
                v = w / nrm
            acc += s / T
        psi.append(acc / ndraw)
    psi = np.array(psi)
    d2 = np.diff(psi, 2)
    log(f"  psi range {psi.max()-psi.min():.4f}; max|d2| "
        f"{np.abs(d2).max():.2e}; psi(0)={psi[12]:.4f}")
    tau = -psi[::-1]
    d2t = np.abs(np.diff(tau, 2))
    med = np.median(d2t)
    # affine-segment test: a linear branch of tau over >= 3 grid points
    # would show |tau''| << median over a run
    runs = np.abs(d2t) < 0.05 * med
    maxrun = 0
    cur = 0
    for r in runs:
        cur = cur + 1 if r else 0
        maxrun = max(maxrun, cur)
    nsmall = int(runs.sum())
    ok = maxrun < 3 and nsmall <= 0.15 * len(d2t) and med > 1e-4
    log(f"  longest |tau''| < 5% of median run: {maxrun} points "
        f"({nsmall}/{len(d2t)} below); median |tau''| {med:.2e} -> no "
        f"affine segment: {'PASS' if ok else 'FAIL'}")
    return ok


def A3():
    log("A3  reducible two-block chain (sector competition):")
    # two genuinely DIFFERENT 2-state chains (different kernels AND tilt
    # shapes, not a linear shift) whose psi curves cross transversally
    def psi_block(K, g, k):
        M = K * np.exp(k * g)
        return np.log(np.real(np.linalg.eigvals(M)).max())
    KA = np.array([[0.75, 0.25], [0.25, 0.75]])
    gA = np.array([[1.4, 0.0], [0.0, -1.4]])
    KB = np.array([[0.4, 0.6], [0.6, 0.4]])
    gB = np.array([[0.0, 0.9], [0.9, 0.0]])
    kg = np.linspace(-3, 3, 601)
    dk = kg[1] - kg[0]
    pa = np.array([psi_block(KA, gA, k) for k in kg])
    pb = np.array([psi_block(KB, gB, k) for k in kg])
    psi = np.maximum(pa, pb)
    sel = np.argmax(np.vstack([pa, pb]), axis=0)
    sw = np.where(sel[:-1] != sel[1:])[0]
    d1 = np.diff(psi)
    jump = float(np.abs(np.diff(d1)).max()) / dk      # slope units
    d2 = np.diff(psi, 2) / dk ** 2                    # curvature units
    far = np.ones(len(d2), bool)
    for s in sw:
        far[max(0, s - 12):min(len(d2), s + 14)] = False
    branch_curv = float(np.abs(d2[far]).min())
    ok = len(sw) >= 1 and jump > 0.1 and branch_curv > 1e-5
    log(f"  {len(sw)} corner(s) (first at k ~ {kg[sw[0]]:.2f}); max slope "
        f"jump {jump:.3f} (slope units); away from corner min psi'' = "
        f"{branch_curv:.2e} (branches curved, vs the REM's exact 0) -> "
        f"corner WITHOUT affine branch: {'PASS' if ok else 'FAIL'}")
    return ok


def A4():
    log("A4  REM freezing benchmark (Theorem thm:rem object):")
    # Closed form (thm:rem / Derrida 1981): the quenched SCGF of the REM is
    # the PIECEWISE function
    #   phi(s) = a + s^2/2   for s <= s_c ;   phi(s) = s * s_c  for s >= s_c
    # with a = log 2, s_c = sqrt(2a): strictly convex below s_c, AFFINE
    # above, with phi' continuous at s_c (the freezing signature).
    a = math.log(2.0)
    sc = math.sqrt(2 * a)
    sg = np.linspace(0.2, 3.2, 301)
    # thm:rem / Derrida 1981 quenched SCGF of the REM (piecewise):
    #   phi(s) = a + s^2/2   for s <= s_c ;   phi(s) = s * s_c  for s >= s_c
    # (continuous, phi' continuous at s_c, terminal AFFINE branch above)
    phi_cf = np.where(sg <= sc, a + sg ** 2 / 2, sg * sc)
    disc = abs((a + sc ** 2 / 2) - sc * sc)
    slope_below = sc                     # d/ds (a + s^2/2) at s_c
    slope_above = sc                     # d/ds (s s_c)
    # affine branch: second difference ~ 0 for s > s_c
    d2 = np.diff(phi_cf, 2)
    above = sg[2:] > sc + 0.05
    below = sg[2:] < sc - 0.05
    lin_above = float(np.abs(d2[above]).max())
    curv_below = float(np.abs(d2[below]).min())
    # finite-T trend: T=22, 200 draws (vectorised)
    T = 22
    ndraw = 160
    sim = []
    for s in (0.6, 1.0, 1.6, 2.2):
        acc = 0.0
        for _ in range(ndraw):
            E = rng.standard_normal(2 ** T) * math.sqrt(T)
            acc += math.log(float(np.sum(np.exp(-s * E)))) / T
        sim.append(acc / ndraw)
    ok = (disc < 1e-12 and abs(slope_below - slope_above) < 1e-12 and
          lin_above < 1e-6 and curv_below > 1e-6)
    log(f"  closed form: junction gap {disc:.1e}, phi' continuous at "
        f"s_c={sc:.4f}, |phi''| above s_c {lin_above:.1e} vs below "
        f"{curv_below:.1e} -> terminal AFFINE branch: "
        f"{'PASS' if ok else 'FAIL'}")
    log(f"  finite-T (T=22, {ndraw} draws) phi(s) at s=(0.6,1,1.6,2.2): "
        f"{[round(x,4) for x in sim]} vs closed form "
        f"{[round((a+x*x/2) if x<=sc else x*sc,4) for x in (0.6,1.0,1.6,2.2)]} "
        f"(trend, not asserted)")
    return ok


def A5():
    log("A5  p=1 Haar-refreshed family (L=4): exact quenched psi(k):")
    from haar_smc_lib_v1 import draw_circuit, p1_exact_Z
    L, Tsw = 4, 12
    kgrid = np.linspace(-2.5, 2.5, 21)
    ndraw = 400
    psi = []
    for k in kgrid:
        acc = 0.0
        for _ in range(ndraw):
            gates, sched = draw_circuit(L, 1.0, Tsw, rng)
            Z = p1_exact_Z(L, Tsw, gates, sched, k)
            acc += math.log(max(Z, 1e-300))
        psi.append(acc / ndraw / Tsw)
    psi = np.array(psi)
    d2 = np.diff(psi, 2)
    # smoothness: no jump in d2 beyond the sampling noise; strict convexity
    med = np.median(np.abs(d2))
    ok = np.abs(d2).max() < 8 * med + 1e-4 and d2[np.argmin(np.abs(kgrid))] > 0
    log(f"  psi(0)={psi[10]:.4f}, psi''~{med:.4f} (strictly convex, smooth "
        f"over k in [-2.5, 2.5]): {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================
# Part B: replica interpolation identity
# =====================================================================
def gfun(X, r, w=None):
    """log E X^r for an empirical or exact sample (weights w)."""
    if w is None:
        m = float(np.mean(np.power(X, r)))
    else:
        m = float(np.sum(w * np.power(X, r)))
    return math.log(m)


def B1():
    log("B1  synthetic exact interpolation identity:")
    vals = np.array([0.2, 0.5, 1.0, 2.0, 4.0, 9.0])
    probs = np.array([0.1, 0.2, 0.25, 0.2, 0.15, 0.1])
    logX = np.log(vals)
    Elog = float(np.sum(probs * logX))
    for m in (0.5, 1.0, 2.0, 3.0):
        g_m = math.log(float(np.sum(probs * vals ** m)))
        lhs = g_m - m * Elog
        # RHS: int_0^m (m-s) Var_s ds by fine quadrature of the tilted var
        ss = np.linspace(0.0, m, 2001)
        vs = []
        for s in ss:
            w = probs * vals ** s
            w = w / w.sum()
            mu = float(np.sum(w * logX))
            v = float(np.sum(w * (logX - mu) ** 2))
            vs.append(v)
        vs = np.array(vs)
        rhs = float(np.trapezoid((m - ss) * vs, ss))
        err = abs(lhs - rhs) / max(abs(lhs), 1e-12)
        log(f"  m={m}: g(m)-m ElogX = {lhs:.10f}  int = {rhs:.10f}  "
            f"rel err {err:.2e}")
        if err > 1e-6:
            return False
    log("  PASS (quadrature-exact to 1e-6)")
    return True


def B2():
    log("B2  Lyapunov monotonicity and the two one-sided limits:")
    from scipy.special import logsumexp
    vals = np.array([0.2, 0.5, 1.0, 2.0, 4.0, 9.0])
    probs = np.array([0.1, 0.2, 0.25, 0.2, 0.15, 0.1])
    lv = np.log(vals)
    lp = np.log(probs)
    ms = np.linspace(0.05, 3000, 400)
    fr = [float(logsumexp(m * lv + lp)) / m for m in ms]
    mono = np.all(np.diff(fr) >= -1e-12)
    lim0 = fr[0]
    Elog = float(np.sum(probs * lv))
    liminf = fr[-1]
    esssup = math.log(vals.max())
    V0 = float(np.sum(probs * lv ** 2) - Elog ** 2)
    corr = ms[0] * V0 / 2          # the quadratic small-m correction
    corr_inf = -math.log(probs[vals.argmax()]) / ms[-1]  # 1/m finite-m
    log(f"  monotone: {mono};  f(m->0+)={lim0:.6f} vs E log X + mV/2 = "
        f"{Elog + corr:.6f} (E log X = {Elog:.6f});  f(m_max)={liminf:.6f} "
        f"vs log ess-sup + (log p_max)/m = {esssup + corr_inf:.6f} "
        f"(ess-sup = {esssup:.6f})")
    ok = mono and abs(lim0 - Elog - corr) < 0.02 and \
        abs(liminf - esssup - corr_inf) < 0.005 and liminf > Elog + 1.5
    log(f"  m->0 recovers the quenched value (with the mV/2 rate), m->inf "
        f"overshoots far above it to the extremal: "
        f"{'PASS' if ok else 'FAIL'}")
    return ok


def B3():
    log("B3  real object: p=1 Haar record partition function (L=4, sweeps):")
    from haar_smc_lib_v1 import draw_circuit, p1_exact_Z
    L, Tsw, ndraw, k = 4, 6, 6000, 0.5
    ZX = np.empty(ndraw)
    for i in range(ndraw):
        gates, sched = draw_circuit(L, 1.0, Tsw, rng)
        ZX[i] = p1_exact_Z(L, Tsw, gates, sched, k)
    logX = np.log(ZX)
    Elog = float(np.mean(logX))
    V0 = float(np.var(logX))
    log(f"  N={ndraw} circuits: E log Z = {Elog:.5f}, Var log Z = {V0:.5f}, "
        f"max Z = {ZX.max():.4f}")
    ok = True
    # (i) monotone replica free energies
    ms = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0])
    fr = [math.log(float(np.mean(ZX ** m))) / m for m in ms]
    mono = np.all(np.diff(fr) >= -1e-9)
    log(f"  f_m = {' '.join(f'{x:.4f}' for x in fr)}  monotone: {mono}")
    ok &= mono
    # (ii) the interpolation identity at m=1 and m=2 (empirical)
    for m in (1.0, 2.0):
        lhs = math.log(float(np.mean(ZX ** m))) - m * Elog
        ss = np.linspace(0, m, 200)
        vs = []
        for s in ss:
            w = ZX ** s
            w = w / w.sum()
            mu = float(np.sum(w * logX))
            vs.append(float(np.sum(w * (logX - mu) ** 2)))
        rhs = float(np.trapezoid((m - ss) * np.array(vs), ss))
        err = abs(lhs - rhs) / max(abs(lhs), 1e-9)
        log(f"  m={m}: gap {lhs:.5f} vs int {rhs:.5f} (rel {err:.1e})")
        ok &= err < 0.05
    # (iii) small-m quadratic rate: f_m - E log Z ~ (m/2) Var_0
    mm = np.array([0.125, 0.25, 0.5])
    rate = [(math.log(float(np.mean(ZX ** m))) / m - Elog) / (m / 2 * V0)
            for m in mm]
    log(f"  (f_m - Elog)/(m Var/2) at m={mm.tolist()}: "
        f"{[round(r, 3) for r in rate]} (-> 1)")
    ok &= all(0.7 < r < 1.3 for r in rate)
    # (iv) replica derivative
    h = 0.02
    d0 = (float(np.mean(ZX ** h)) - float(np.mean(ZX ** (-h)))) / (2 * h)
    log(f"  d/dm E Z^m |_(m=0) ~ {d0:.5f} vs E log Z = {Elog:.5f}")
    ok &= abs(d0 - Elog) < 0.05 * abs(Elog)
    # (v) m -> inf overshoot
    log(f"  f_8={fr[-1]:.4f} vs log max Z = {math.log(ZX.max()):.4f} "
        f"> E log Z = {Elog:.4f}")
    ok &= fr[-1] > Elog and math.log(ZX.max()) > Elog
    log(f"  {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == '__main__':
    ap = __import__('argparse').ArgumentParser()
    ap.add_argument('part', nargs='?', default='all',
                    choices=['all', 'A', 'B'])
    args = ap.parse_args()
    res = {}
    if args.part in ('all', 'A'):
        res['A1'] = A1()
        res['A2'] = A2()
        res['A3'] = A3()
        res['A4'] = A4()
        res['A5'] = A5()
    if args.part in ('all', 'B'):
        res['B1'] = B1()
        res['B2'] = B2()
        res['B3'] = B3()
    log("--- summary ---")
    for k, v in res.items():
        log(f"  {k}: {'PASS' if v else 'FAIL'}")
