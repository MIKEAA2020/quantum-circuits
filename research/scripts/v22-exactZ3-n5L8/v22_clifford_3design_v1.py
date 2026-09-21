"""v22_clifford_3design_v1.py -- is the two-qubit Clifford group an exact
conjugation 3-design on U(4)?

WHY THIS MATTERS (this round): the exact Zbar_3 closure of Lambda(2)
identifies the Clifford-ensemble disorder moment E_omega[2^{-2 N_rand}]
with the Haar-averaged three-replica partition function Zbar_3 of the v17
operator.  At n = 2 the identification is exact because two-qubit Cliffords
form an exact 2-design (Remark rem:clifford).  At n = 3 it requires the
conjugation-channel 3-design property
    E_{C in Cl2}[ C^{(x)3} X C^{dagger (x)3} ] == E_Haar[ ... ]   for all X,
i.e. Cl2 must reproduce the Haar twirl T_Haar^{(n)}[X] = sum_pi U_pi y_pi,
G y = t, t_pi = tr[U_pi^dagger X], G[pi,rho] = (d^2)^{c(pi^{-1} rho)}
(the Hilbert-Schmidt projector onto span{U_pi}, Proposition
prop:general-n(iii)).  This script tests n = 2 (control: must PASS),
n = 3 (the identification under test), n = 4 (negative control: the
Clifford group is famously NOT a 4-design -- the test must FAIL).

Method: BFS closure from {H(x)I, I(x)H, S(x)I, I(x)S, CNOT_01, CNOT_10}
gives 92160 unitaries -- the phase-extended Clifford group
{e^{i k pi/4}} x Cl2 (8 phases x 11520).  Conjugation channels are
phase-invariant, so the uniform average over 92160 equals the uniform
average over the 11520 phase classes; we deduplicate by the phase-free
canonical form (first nonzero entry rotated to be real positive) and test
on the 11520 representatives.  The symplectic action of each element on
the 15 unsigned two-qubit Paulis (which Pauli, up to phase, C P C^dag is)
is recorded: 720 distinct actions with exactly 16 elements each -- the
equal-weight fact behind E_{720 actions} = E_{Cl2} on sigma-measurable
trajectory quantities (the deposited simulator samples the 720 symplectic
actions uniformly).
"""
import sys, os, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
from gap_utils import perms, compose, inv, cycles

OUT = os.path.join(HERE, '..', '..', 'results', 'v22-exactZ3-n5L8')
os.makedirs(OUT, exist_ok=True)


def log(*a):
    print(*a, flush=True)


_H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
_S = np.array([[1, 0], [0, 1j]], dtype=complex)
_I2 = np.eye(2, dtype=complex)
_CNOT01 = np.eye(4, dtype=complex)
_CNOT01[2, 2] = 0; _CNOT01[3, 3] = 0
_CNOT01[2, 3] = 1; _CNOT01[3, 2] = 1
_CNOT10 = np.eye(4, dtype=complex)
_CNOT10[1, 1] = 0; _CNOT10[3, 3] = 0
_CNOT10[1, 3] = 1; _CNOT10[3, 1] = 1
GENS = [np.kron(_H, _I2), np.kron(_I2, _H),
        np.kron(_S, _I2), np.kron(_I2, _S), _CNOT01, _CNOT10]


def _key(U, nd=9):
    return tuple(np.round(U.real, nd).ravel()) + \
        tuple(np.round(U.imag, nd).ravel())


def _phase_free_key(U):
    """Phase-invariant injective key: U -> U (x) conj(U) is constant on
    phase classes and separates them (U (x) Ubar = V (x) Vbar iff
    V = e^{i theta} U).  No tie-breaking, unlike argmax canonicalization."""
    K = np.kron(U, U.conj())
    return _key(K, nd=9)


def clifford_group():
    ident = np.eye(4, dtype=complex)
    seen = {_key(ident): ident}
    frontier = [ident]
    while frontier:
        new = []
        for U in frontier:
            for G in GENS:
                V = U @ G
                k = _key(V)
                if k not in seen:
                    seen[k] = V
                    new.append(V)
        frontier = new
    return list(seen.values())


def paulis2():
    X1 = np.array([[0, 1], [1, 0]], dtype=complex)
    Z1 = np.array([[1, 0], [0, -1]], dtype=complex)
    I1 = np.eye(2, dtype=complex)
    out = []
    for x1 in (I1, X1):
        for z1 in (I1, Z1):
            for x2 in (I1, X1):
                for z2 in (I1, Z1):
                    P = np.kron(x1 @ z1, x2 @ z2)
                    if np.linalg.norm(P) > 0:
                        out.append(P)
    # drop the identity, keep the 15 nontrivial unsigned Paulis
    out = [P for P in out if np.linalg.norm(P - np.eye(4)) > 1e-9]
    return out[:15]


def sp_action(U, plist):
    """Index tuple: for each of the 15 Paulis, which Pauli (up to phase)
    U P U^dag is."""
    key = []
    for P in plist:
        Q = U @ P @ U.conj().T
        # match to the closest Pauli up to phase
        best, bestd = -1, 1e9
        for j, R in enumerate(plist):
            ov = abs(np.trace(R.conj().T @ Q)) / 4.0  # normalized overlap
            d = 1.0 - ov
            if d < bestd:
                bestd, best = d, j
        key.append(best)
    return tuple(key)


def perm_op(pi, D, n):
    dim = D ** n
    U = np.zeros((dim, dim), dtype=complex)
    for x in range(dim):
        digits = []
        y = x
        for _ in range(n):
            digits.append(y % D)
            y //= D
        tgt = [0] * n
        for i in range(n):
            tgt[pi[i]] = digits[i]
        y2 = 0
        for i in range(n):
            y2 += tgt[i] * (D ** i)
        U[y2, x] = 1
    return U


def main():
    t0 = time.time()
    log("== Cl2 enumeration (BFS from H,S,CNOT generators) ==")
    Gfull = clifford_group()
    log(f"   |<H,S,CNOT>| = {len(Gfull)} "
        f"(= 8 x 11520: the phase-extended Clifford group)")
    # phase dedup via the phase-invariant injective key U (x) Ubar
    seen = set()
    Greps = []
    for U in Gfull:
        k = _phase_free_key(U)
        if k not in seen:
            seen.add(k)
            Greps.append(U)
    log(f"   phase classes = {len(Greps)} (expected 11520)")
    # symplectic action census
    plist = paulis2()
    act = {}
    for U in Greps:
        kk = sp_action(U, plist)
        act[kk] = act.get(kk, 0) + 1
    log(f"   distinct Sp(4,2) actions = {len(act)} (expected 720); "
        f"class sizes min {min(act.values())} max {max(act.values())} "
        f"(expected 16 each)")
    ok_struct = (len(Greps) == 11520 and len(act) == 720
                 and min(act.values()) == 16 and max(act.values()) == 16)
    log(f"   structure: [{'OK' if ok_struct else 'FAIL'}]")

    # ---------------- the design test ----------------
    D = 4
    rng = np.random.default_rng(20260529)
    res = {'|G_full|': len(Gfull), '|G_phase_classes|': len(Greps),
           'n_actions': len(act),
           'class_min': int(min(act.values())),
           'class_max': int(max(act.values())),
           'structure_ok': bool(ok_struct), 'tests': {}}
    for n in (2, 3, 4):
        P = perms(n)
        Uops = [perm_op(pi, D, n) for pi in P]
        g = len(P)
        Gm = np.empty((g, g))
        for i, s in enumerate(P):
            si = inv(s)
            for j, t in enumerate(P):
                Gm[i, j] = float(D) ** cycles(compose(si, t))
        Ginv = (np.linalg.pinv(Gm) if D < n else np.linalg.inv(Gm))
        dim = D ** n
        trials = 6 if n <= 3 else 3
        devs = []
        for trial in range(trials):
            X = (rng.standard_normal((dim, dim))
                 + 1j * rng.standard_normal((dim, dim)))
            acc = np.zeros((dim, dim), dtype=complex)
            for U in Greps:
                Unp = U
                for _ in range(n - 1):
                    Unp = np.kron(Unp, U)
                acc += Unp @ X @ Unp.conj().T
            T_cl = acc / len(Greps)
            t = np.array([np.trace(Uops[i].conj().T @ X) for i in range(g)])
            y = Ginv @ t
            T_h = np.zeros_like(X)
            for i in range(g):
                T_h += y[i] * Uops[i]
            devs.append(float(np.linalg.norm(T_cl - T_h)
                              / np.linalg.norm(T_h)))
        mx = max(devs)
        verdict = ("PASS (exact design)" if mx < 1e-10 else
                   f"FAIL (not a {n}-design)")
        log(f"   n={n}: max ||T_Cl - T_Haar||/||T_Haar|| over {trials} "
            f"random X = {mx:.3e}   [{verdict}]")
        res['tests'][f'n={n}'] = {'max_dev': mx, 'devs': devs,
                                  'pass': bool(mx < 1e-10)}
    res['secs'] = round(time.time() - t0, 1)
    json.dump(res, open(f'{OUT}/v22_clifford_3design.json', 'w'), indent=1)
    log(f"   written {OUT}/v22_clifford_3design.json  ({res['secs']}s)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
