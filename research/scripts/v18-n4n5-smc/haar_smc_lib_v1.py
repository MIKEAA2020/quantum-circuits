"""Haar SMC record-multifractality (Target C) — library (v1).

Sequential Monte Carlo estimation of the quenched record SCGF
psi_{L,omega}(k) = lim (1/T) log E_{P_omega} e^{k A_T} for Haar-monitored
circuits, exactly per the manuscript's Definition (SMC estimator) and
Proposition (SMC):

  * circuit protocol identical to the deposited mipt_haar_sim.py:
    L qubits, PBC, |0..0>, per period two layers, each layer = measurement
    sweep (site s measured with probability p, computational basis) followed
    by L/2 Haar two-site gates on the matching (2b+layer, 2b+1+layer) mod L;
    the schedule coins are part of omega (NOT of r), matching the deposited
    surprisal convention (logp accumulates only outcome probabilities);
  * block = one full brickwork period, so T counts periods;
  * incremental weight  l_t^i = -k log r_t^i  with r_t^i the product of the
    period's sequential conditional Born probabilities;
  * stabilized normalizer  log c_t = m_t + log mean exp(l_t - m_t);
    Zhat_T(k) = prod c_t;  psihat = (1/T) sum log c_t;
  * systematic resampling (conditionally unbiased);
  * per-particle surprisal A_T recorded at k=0 (direct Born MC) for the
    entropy rate / variance identities and the deposited-data comparison.

Validations (haar_smc_v1.py phase 'validate'):
  Va  k=0: psihat = 0 exactly and the A_T/T moments match the deposited
      haar npz surprisal statistics at matched (L, p, t).
  Vb  brute force: L=4 — enumerate ALL records of a fixed circuit, compute
      Z_T(k) = sum_Y P(Y)^{1-k} exactly, and check E[Zhat] over many
      independent SMC runs (unbiasedness, Prop SMC).
  Vc  p=1: the record is a Markov chain on the d^L basis states with
      K(y'|y) = prod_b |U_b(y'_b, y_b)|^2 per gate sub-layer; Z_T(k) =
      1^T K_k^{S-1} e_0 with K_k = K^{1-k} — exact, compared to E[Zhat].
"""
import math
import numpy as np

# ---------------------------------------------------------------------------
def haar_unitary(rng, n=4):
    z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) \
        / np.sqrt(2)
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    return q * (d / np.abs(d))

def apply_gate_batch(psi, U, i, j, L):
    """psi: (N, 2^L); two-qubit gate on bond (i, j) for every particle.
    Bit order: site 0 = most significant (deposited convention)."""
    U4 = U.reshape(2, 2, 2, 2)
    N = psi.shape[0]
    if j == i + 1:
        X = psi.reshape(N, 2 ** i, 2, 2, 2 ** (L - i - 2))
        return np.einsum('abcd,npcdr->npabr', U4, X).reshape(N, -1)
    # wrap bond: i = L-1 (least significant), j = 0 (most significant)
    X = psi.reshape(N, 2, 2 ** (L - 2), 2)
    return np.einsum('abcd,ndmc->nbma', U4, X).reshape(N, -1)

def measure_batch(psi, s, L, outcomes):
    """Computational-basis measurement of site s with per-particle outcomes
    (0/1 int array).  Returns (psi', pr).  outcomes[i] drawn by the caller
    from the particle's own predictor."""
    N = psi.shape[0]
    X = psi.reshape(N, 2 ** s, 2, 2 ** (L - s - 1))
    p0 = np.sum(np.abs(X[:, :, 0, :]) ** 2, axis=(1, 2))
    pr = np.where(outcomes == 0, p0, 1.0 - p0)
    keep = outcomes.astype(np.int64)
    # zero the DISCARDED branch per particle (advanced indexing must be
    # per-row: put_along_axis, NOT X[:, :, 1-keep, :] which mixes rows)
    Xx = X.copy()
    np.put_along_axis(Xx, (1 - keep).reshape(N, 1, 1, 1), 0.0, axis=2)
    psin = Xx.reshape(N, -1)
    psin = psin / np.sqrt(pr)[:, None]
    return psin, pr

def apply_gate_single(psi, U, i, j, L):
    """Deposited single-state gate (mipt_haar_sim.apply_gate)."""
    U4 = U.reshape(2, 2, 2, 2)
    if j == i + 1:
        X = psi.reshape(2 ** i, 2, 2, 2 ** (L - i - 2))
        return np.einsum('abcd,pcdr->pabr', U4, X).reshape(-1)
    X = psi.reshape(2, 2 ** (L - 2), 2)
    return np.einsum('abcd,dmc->bma', U4, X).reshape(-1)

def measure_single(psi, s, L, outcome):
    X = psi.reshape(2 ** s, 2, 2 ** (L - s - 1))
    p0 = float(np.sum(np.abs(X[:, 0, :]) ** 2))
    pr = p0 if outcome == 0 else 1.0 - p0
    X[:, 1 - outcome, :] = 0.0
    return X.reshape(-1) / math.sqrt(pr), pr

# ---------------------------------------------------------------------------
def draw_circuit(L, p, T, rng):
    """Pre-draw the circuit disorder omega = (gates, schedule) for T periods.
    Returns (gates, sched):  gates[t][layer][b] = U (4x4);
    sched[t][layer][s] = bool (site s measured)."""
    gates = [[[haar_unitary(rng) for b in range(L // 2)]
              for layer in range(2)] for t in range(T)]
    sched = [[rng.random(L) < p for _ in range(2)] for t in range(T)]
    return gates, sched

# ---------------------------------------------------------------------------
def smc_run(L, p, T, k, N, gates, sched, rng, track_A=False):
    """One SMC run on a fixed circuit (gates, sched).  Returns dict:
    logZ, psi_hat, logc (list), ess_min, ess_mean, A_T (per surviving
    particle at the final period, if track_A)."""
    psi = np.zeros((N, 2 ** L), dtype=complex)
    psi[:, 0] = 1.0
    logpr = np.zeros(N)
    logc = []
    ess_list = []
    A_path = np.zeros(N)
    for t in range(T):
        logpr[:] = 0.0
        for layer in range(2):
            for s in range(L):
                if sched[t][layer][s]:
                    X = psi.reshape(N, 2 ** s, 2, 2 ** (L - s - 1))
                    p0 = np.sum(np.abs(X[:, :, 0, :]) ** 2, axis=(1, 2))
                    u = rng.random(N)
                    outcomes = np.where(u < p0, 0, 1)
                    psi, pr = measure_batch(psi, s, L, outcomes)
                    logpr += np.log(pr)
            for b in range(L // 2):
                i, j = (2 * b + layer) % L, (2 * b + 1 + layer) % L
                psi = apply_gate_batch(psi, gates[t][layer][b], i, j, L)
        # period block weight
        ell = -k * logpr                      # l_t^i = -k log r_t^i
        m = float(np.max(ell))
        w = np.exp(ell - m)
        sw = float(np.sum(w))
        logc.append(m + math.log(sw / N))
        wbar = w / sw
        ess_list.append(1.0 / float(np.sum(wbar ** 2)))
        if track_A:
            A_path += -logpr                 # surprisal accumulated
        # systematic resampling
        uu = rng.random() / N
        pos = (np.arange(N) + uu) / N
        cum = np.cumsum(wbar)
        cum[-1] = 1.0
        idx = np.searchsorted(cum, pos)
        psi = psi[idx].copy()
        if track_A:
            A_path = A_path[idx]            # records travel with ancestors
    logZ = float(np.sum(logc))
    return {'logZ': logZ, 'psi_hat': logZ / T, 'logc': logc,
            'ess_min': float(np.min(ess_list)),
            'ess_mean': float(np.mean(ess_list)),
            'A_T': (A_path.copy() if track_A else None)}

# ---------------------------------------------------------------------------
def record_logprob(L, T, gates, sched, outcome_bits):
    """log P_omega(Y) for one fixed record (used by the brute-force check);
    returns -inf for zero-probability records (excluded from Z per the
    manuscript definition: the sum is over Y with P(Y) > 0).
    outcome_bits: list of 0/1, one per scheduled measurement event, in
    chronological (t, layer, site) order."""
    psi = np.zeros(2 ** L, dtype=complex)
    psi[0] = 1.0
    logp = 0.0
    it = iter(outcome_bits)
    for t in range(T):
        for layer in range(2):
            for s in range(L):
                if sched[t][layer][s]:
                    psi, pr = measure_single(psi, s, L, next(it))
                    if pr <= 0.0:
                        return -math.inf
                    logp += math.log(pr)
            for b in range(L // 2):
                i, j = (2 * b + layer) % L, (2 * b + 1 + layer) % L
                psi = apply_gate_single(psi, gates[t][layer][b], i, j, L)
    return logp

def brute_force_Z(L, T, gates, sched, k):
    """Enumerate all records; Z_T(k) = sum_{Y: P(Y)>0} P(Y)^{1-k}."""
    events = [(t, layer, s) for t in range(T) for layer in range(2)
              for s in range(L) if sched[t][layer][s]]
    M = len(events)
    total = 0.0
    for mask in range(1 << M):
        bits = [(mask >> i) & 1 for i in range(M)]
        lp = record_logprob(L, T, gates, sched, bits)
        if lp == -math.inf:
            continue
        total += math.exp((1 - k) * lp)
    return total, M

# ---------------------------------------------------------------------------
def p1_exact_Z(L, T, gates, sched, k):
    """Exact Z_T(k) at p=1: the basis-state Markov chain.
    Between consecutive measurement sweeps exactly one gate sub-layer acts;
    K(y'|y) = |<y'| G_layer |y>|^2 (product over the layer's bonds).
    Z_T(k) = sum over sweep-outcomes of prod P^{1-k}
           = 1^T Kk^{S-1} e_{y0} with Kk = K^{1-k}, y0 = 0.
    Requires every sched entry True (p=1)."""
    assert all(all(s) for sl in sched for s in sl)
    S = 2 * T                                    # measurement sweeps
    dim = 2 ** L
    def build_K(t, layer):
        # apply gates[t][layer] to each basis state; K(y'|y) = |<y'|G|y>|^2
        K = np.zeros((dim, dim))
        for x in range(dim):
            psi = np.zeros(dim, dtype=complex)
            psi[x] = 1.0
            for b in range(L // 2):
                i, j = (2 * b + layer) % L, (2 * b + 1 + layer) % L
                U = gates[t][layer][b]
                psi = apply_gate_single(psi, U, i, j, L)
            K[:, x] = np.abs(psi) ** 2
        return K
    Ks = {(t, layer): build_K(t, layer) for t in range(T)
          for layer in range(2)}
    y0 = 0
    v = np.zeros(dim); v[y0] = 1.0
    # first sweep: measure |0..0> -> deterministic, r = 1, no weight
    for s in range(1, S):
        # gates before sweep s: those following sweep s-1
        t_g, layer_g = (s - 1) // 2, (s - 1) % 2
        Kk = Ks[(t_g, layer_g)] ** (1.0 - k)
        v = Kk @ v
    return float(np.sum(v))
