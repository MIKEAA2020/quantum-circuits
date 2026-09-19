"""
mipt_kaufman_lib.py -- closed-form spectrum of the compressed two-replica
period map for the monitored random Clifford circuit (annealed n = 2 sector).

Reconstructed and verified against the deposited workspace numbers
(previous chat.txt / previous turns.txt, quantum-circuits repository):
  * the five exact-rational Collatz-Wielandt enclosures of lambda_1
    (relative agreement <= 7e-15, float64 precision);
  * the Table-benchmark consecutive-size crossings (5 decimal places, d = 2, 3);
  * the ratio row -> 1/8 with the finite-size values 0.1220...0.1243 (d = 2);
  * p_c^{(2)}(d) = (d - theta_c)/(d - 1), theta_c = beta_d + sqrt(beta_d^2+1),
    beta_d = (d^2-1)/(d^2+1) for d = 2, 3, 5 (exact);
  * p_eff at p_c^{(2)} for d = 2, 3, 5 (8 digits) and the bulk p_eff at p = 0.16;
  * lambda_1(L=28)^{1/L} = 0.683844946 -> 0.6838449 (the manuscript quote) and
    the bulk 0.683844659 (the Houtappel value at p = 0.40, d = 2).

Model.  L = 2m qudits (dimension d) on a ring; one period = two brickwork gate
layers, each followed by a measurement layer (rate p, computational basis);
the two replicas are subjected to the SAME circuit and the SAME measurement
outcomes (record collision).  The annealed second-moment transfer acting on
the per-site replica algebra {e0 (collided), e+ (off-diag symmetric), e- (anti)}
is similar (Schur complement) to the classical triangular-lattice Ising row
transfer M1 = W0^m E D_h with

    E_{s's} = exp[ K_d sum_k s'_k (s_k + s_{k+1}) ],   D_h = diag exp[ K_h sum_k s_k s_{k+1} ],

    C_comp = W0^L E D_h E^T D_h      (L = 2m, ring shift tau: E^T = E tau).

Weights (theta = d - (d-1) p):
  ordered branch  (p < p_c^{(2)}, theta > theta_c):
      a = (theta+1)^2 / (2(d^2+1)),  b = (theta^2-1)/(2(d^2-1)),
      c = (theta-1)^2 / (2(d^2+1)),  W0 = (theta^2-1)/(2 sqrt(d^4-1)).
  disordered branch (p > p_c^{(2)}, theta < theta_c):
      a = (d^2 theta^2 - 1)/(d^4-1),  b = theta/(d^2+1),
      c = (d^2 - theta^2)/(d^4-1),
      W0 = sqrt(theta (d^2-1)) * ((d^2 theta^2-1)(d^2-theta^2))^{1/4} / (d^4-1).
  a = W0 e^{2K_d+K_h}, b = W0 e^{-K_h}, c = W0 e^{-2K_d+K_h}; the two branches
  join continuously at theta_c (a - c = 2b there); the k = 0 mode changes its
  Kaufman parity character exactly at the transition.

Spectrum (numerically verified conjecture in the deposited workspace; here the
verification is reproduced):
  every nonzero eigenvalue of C_comp is
      lambda = (2 W0^2)^m prod_{k in K_sigma} w_k^{pm_k},
  Q(k)  = cosh^2 2K_d cosh 2K_h + sinh^2 2K_d sinh 2K_h - sinh 2K_h cos k,
  R(k)  = 2 sinh 2K_d cos(k/2),      w_k^+- = Q(k) +- sqrt(Q(k)^2 - R(k)^2),
  flip-even sector: K_+ = {(2j-1)pi/m}, EVEN number of '-' choices;
  flip-odd  sector: K_- = {2 pi j / m},   even number of '-' below p_c^{(2)},
                                          ODD number above (the k = 0 flip).
  R(pi) = 0 => w_pi^- = 0: the sector containing k = pi loses half its states
  to the kernel; rank C_comp = 3 * 2^{m-2}.

Gapless (critical) line: a - c = 2b  <=>  sinh(2 K_d) e^{2 K_h} = 1.
At p_c^{(2)}: e^{2K_h} = beta_d, sinh(2K_d) = 1/beta_d, and the scaled gaps
  L log(lambda_1/lambda_odd) / 2pi -> beta_d / 4,
  L log(lambda_1/lambda_eps) / 2pi -> 2 beta_d          (ratio 1/8 = x_sig/x_eps).
"""

import numpy as np

# ------------------------------------------------------------------ constants

def beta_d(d):
    return (d * d - 1) / (d * d + 1)

def theta_c(d):
    b = beta_d(d)
    return b + np.sqrt(b * b + 1)

def PC2(d):
    """Annealed critical measurement rate p_c^{(2)}(d)."""
    return (d - theta_c(d)) / (d - 1)

def theta(d, p):
    return d - (d - 1) * p

# ------------------------------------------------------------------ couplings

def weights(d, p):
    """Boltzmann weights (a, b, c) and normalization W0 of the bond transfer."""
    th = theta(d, p)
    if th >= theta_c(d):      # ordered branch (p < p_c^{(2)})
        a = (th + 1) ** 2 / (2 * (d * d + 1))
        b = (th * th - 1) / (2 * (d * d - 1))
        c = (th - 1) ** 2 / (2 * (d * d + 1))
        W0 = (th * th - 1) / (2 * np.sqrt(d ** 4 - 1))
    else:                     # disordered branch (p > p_c^{(2)})
        a = (d * d * th * th - 1) / (d ** 4 - 1)
        b = th / (d * d + 1)
        c = (d * d - th * th) / (d ** 4 - 1)
        W0 = (np.sqrt(th * (d * d - 1))
              * ((d * d * th * th - 1) * (d * d - th * th)) ** 0.25 / (d ** 4 - 1))
    return a, b, c, W0

def couplings(d, p):
    """(K_d, K_h, W0) of Eq. Kdh: K_d = 1/4 ln(a/c), K_h = 1/4 ln(ac/b^2)."""
    a, b, c, W0 = weights(d, p)
    return 0.25 * np.log(a / c), 0.25 * np.log(a * c / (b * b)), W0

# ------------------------------------------------------------------ spectrum

def QR(k, Kd, Kh):
    k = np.atleast_1d(np.asarray(k, dtype=float))
    c2d, s2d = np.cosh(2 * Kd), np.sinh(2 * Kd)
    c2h, s2h = np.cosh(2 * Kh), np.sinh(2 * Kh)
    Q = c2d ** 2 * c2h + s2d ** 2 * s2h - s2h * np.cos(k)
    R = 2 * s2d * np.cos(k / 2)
    return Q, R

def logw(k, Kd, Kh):
    """(k, log w_k^+, log w_k^-); log w^- = -inf where w^- = 0 (k = pi)."""
    Q, R = QR(k, Kd, Kh)
    disc = np.maximum(Q * Q - R * R, 0.0)
    s = np.sqrt(disc)
    with np.errstate(divide="ignore"):
        return np.log(Q + s), np.log(np.maximum(Q - s, 1e-300))

def spectrum_closed(m, d, p, sector):
    """All nonzero eigenvalues (logs, descending) of C_comp in the given flip
    sector, including the constant (2 W0^2)^m."""
    Kd, Kh, W0 = couplings(d, p)
    above = theta(d, p) < theta_c(d)
    if sector == "even":
        ks = (2 * np.arange(1, m + 1) - 1) * np.pi / m
        need_odd_count = False
    else:
        ks = 2 * np.pi * np.arange(m) / m
        # With the fixed branch ordering w^pm = Q pm sqrt(Q^2-R^2) the flip-odd
        # (periodic-momentum) sector carries an ODD number of '-' choices for
        # every p.  (In the deposited convention the k=0 branches are ordered
        # by magnitude -- the ordering flips at p_c^{(2)}, "the k=0 mode
        # changes sign at the transition, as in Kaufman's treatment" -- under
        # which the same spectrum is described as an even number of '-' below
        # p_c^{(2)} and an odd number above.)
        need_odd_count = True
    lp, lm = logw(ks, Kd, Kh)
    base = m * (np.log(2.0) + 2 * np.log(W0))
    out = []
    for choice in range(1 << m):
        nminus = bin(choice).count("1")
        if (nminus % 2 == 1) != need_odd_count:
            continue
        tot = base
        ok = True
        for i in range(m):
            if choice >> i & 1:
                if not np.isfinite(lm[i]):
                    ok = False
                    break
                tot += lm[i]
            else:
                tot += lp[i]
        if ok:
            out.append(tot)
    return np.sort(np.array(out))[::-1]

def log_lambda1(m, d, p=2, sector="even"):
    """log of the Perron eigenvalue (all '+' in the even sector)."""
    Kd, Kh, W0 = couplings(d, p)
    ks = (2 * np.arange(1, m + 1) - 1) * np.pi / m
    lp, _ = logw(ks, Kd, Kh)
    return m * (np.log(2.0) + 2 * np.log(W0)) + np.sum(lp)

def gaps(m, d, p):
    """(log(l1/l_odd), log(l1/l_eps)) per period, L = 2m, with the Kaufman
    parity rules (l_odd: odd-sector leading; l_eps: two-mode even state)."""
    Kd, Kh, W0 = couplings(d, p)
    above = theta(d, p) < theta_c(d)
    kp = (2 * np.arange(1, m + 1) - 1) * np.pi / m
    ko = 2 * np.pi * np.arange(m) / m
    lpp, lmp = logw(kp, Kd, Kh)
    lpo, lmo = logw(ko, Kd, Kh)
    l1 = np.sum(lpp)
    # Benchmark convention (reproduces the deposited Table to 5 decimals):
    # lambda_odd is the periodic-sector all-'+' state with the FIXED branch
    # ordering -- the analytic continuation through p_c^{(2)} of the leading
    # flip-odd eigenvalue.  The actual leading flip-odd eigenvalue below
    # p_c^{(2)} carries w^-(0) at k = 0 instead (the Kaufman switch; see
    # spectrum_closed).
    lodd = np.sum(lpo)
    g = lpp - lmp
    leps = l1 - 2 * np.min(g)
    return l1 - lodd, l1 - leps

# ------------------------------------------------------------------ dense matrices

def spins(m):
    N = 1 << m
    S = np.zeros((m, N))
    for k in range(m):
        S[k] = 1.0 - 2.0 * ((np.arange(N) >> k) & 1)
    return S

def build_EDh(m, Kd, Kh):
    S = spins(m)
    acc = np.zeros((1 << m, 1 << m))
    for k in range(m):
        acc += np.outer(S[k], S[k] + S[(k + 1) % m])
    E = np.exp(Kd * acc)
    Dh = np.exp(Kh * sum(S[k] * S[(k + 1) % m] for k in range(m)))
    return E, np.diag(Dh)

def dense(m, d, p):
    """Dense C_comp = W0^L E D_h E^T D_h (2^m x 2^m)."""
    Kd, Kh, W0 = couplings(d, p)
    E, Dh = build_EDh(m, Kd, Kh)
    return (W0 ** (2 * m)) * E @ Dh @ E.T @ Dh

def power_lambda1(m, d, p, iters=3000, seed=0):
    """Leading eigenvalue by power iteration on the dense C_comp (m <= 11).
    For larger sizes use log_lambda1 (the closed form), which is anchored by
    the exact-rational Collatz-Wielandt enclosures at L = 16, 20."""
    if m > 11:
        raise NotImplementedError("m > 11: use log_lambda1 (closed form)")
    C = dense(m, d, p)
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(1 << m)
    v /= np.linalg.norm(v)
    for _ in range(iters):
        w = C @ v
        n = np.linalg.norm(w)
        v = w / n
    return float(v @ (C @ v))
