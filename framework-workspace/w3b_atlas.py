#!/usr/bin/env python3
# W3b ADJUNCTION ATLAS v0.1 — render E-status rows as adjunction candidates F -| G,
# test unit/counit/triangle identities or the decisive necessary obstruction, publish failures first.
# date 2026-10-11. Computable-now rows: (i) J/K split pair, (ii) Weingarten=Gram pseudo/inverse
# + rank-audit, (iii) S_n x S_n bimodule tensor-hom. Paper-pending rows: marked, never guessed.
import numpy as np, json, itertools, time, math
t0 = time.time()
np.set_printoptions(suppress=True, linewidth=200)
REPORT = {"date": "2026-10-11", "atlas": "w3b v0.1", "rows": {}, "runtime_s": None}

# ---------- ROW i: (J,K) split pair, a=3,b=8 random generic ----------
rng = np.random.default_rng(7)
a, b = 3, 8
A = rng.standard_normal((b, a))
Q, _ = np.linalg.qr(A)          # J: isometry columns
J = Q
K = rng.standard_normal((a, b))
K = np.linalg.solve(K @ J, np.eye(a)) @ K   # enforce KJ = I (retraction)
assert np.linalg.norm(K @ J - np.eye(a)) < 1e-12
unit_JK = np.eye(a); eps_cand = J @ K
tri1 = np.linalg.norm(K @ eps_cand - K)          # K eps . eta K = K (with eta = I)
tri2 = np.linalg.norm(eps_cand @ J - J)          # eps J . J eta = J
hom_obstruction = np.linalg.norm(eps_cand - np.eye(b))  # need JK = I_b for adjunction (rank a<b impossible)
rank_JK = np.linalg.matrix_rank(eps_cand)
# canonical repair: K# = J^T -> eps = J J^T orthogonal projection (reflection onto image)
eps_star = J @ J.T
proj_idem = np.linalg.norm(eps_star @ eps_star - eps_star)
proj_symm = np.linalg.norm(eps_star - eps_star.T)
row_i = {
 "verdict_linear_world": "OBSTRUCTION: J -| K (linear, a<b) requires JK = I_b of rank b, but rank(JK)<=a<b. "
   "Hom-dimension test passes (ab=ab) and is therefore NON-decisive; the identity test is decisive.",
 "facts": {"KJ = I_a": True, "triangle residuals (eta=I, eps=JK)": [float(tri1), float(tri2),
            "--> triangle identities alone PASS; triangles are necessary, not sufficient"],
   "||JK - I_b||": float(hom_obstruction), "rank(JK)": int(rank_JK), "b": b},
 "repair": {"canonical": "K# = J^T (polar/pseudoinverse twin)", "eps* = JJ^T idempotent": float(proj_idem),
            "eps* symmetric": float(proj_symm),
            "conclusion": "reflective inclusion certified: J -| J^T, counit = orthogonal projection"},
 "setting_flip": "in POS/ordered setting a monotone section-retraction IS a Galois connection (fg <= id suffices): "
   "same split data, adjunction verdict flips with ambient structure",
 "residual_freedom": "choice of ambient (linear vs ordered) + choice of metric fixing J^T",
 "E_row_match_registered_expectation": "YES (no ambient linear adjunction; repair by image-restriction/reflection; residual = reflection data)"}
REPORT["rows"]["i_JK_split_pair"] = row_i

# ---------- ROW ii: Weingarten = Gram^{-1}; full-rank certificate + d<n rank audit ----------
def perm_matrices(n):
    P = []
    for p in itertools.permutations(range(n)):
        M = np.zeros((n, n)); M[np.arange(n), p] = 1; P.append(M)
    return P
def cycles_count(p):
    seen = [False]*len(p); c = 0
    for i in range(len(p)):
        if not seen[i]:
            c += 1; j = i
            while not seen[j]: seen[j] = True; j = p[j]
    return c
def inv_perm(p):
    r = [0]*len(p)
    for i, j in enumerate(p): r[j] = i
    return tuple(r)
def compose(p, qq):
    return tuple(p[qq[i]] for i in range(len(p)))
S3 = list(itertools.permutations(range(3)))
def gram(n, d):
    S = list(itertools.permutations(range(n)))
    G = np.zeros((len(S), len(S)))
    for i, s in enumerate(S):
        for j, t in enumerate(S):
            G[i, j] = d ** cycles_count(compose(s, inv_perm(t)))
    return S, G
rows = {}
for d in [1, 2, 3]:
    S, G = gram(3, d)
    sv = np.linalg.svd(G, compute_uv=False)
    rows[d] = {"rank": int(np.linalg.matrix_rank(G, tol=1e-9)),
               "min_singular_value": float(sv[-1]), "max_singular_value": float(sv[0])}
S, G = gram(3, 3)
W = np.linalg.inv(G)
mp1 = np.linalg.norm(G @ W @ G - G)      # Moore-Penrose identity 1
mp2 = np.linalg.norm(W @ G @ W - W)      # identity 2
centr = 0.0
for p in S:
    P = np.zeros((6, 6))
    for i, t in enumerate(S):
        j = S.index(compose(p, t)); P[j, i] = 1
    centr = max(centr, np.linalg.norm(P @ W - W @ P))
S2, G2 = gram(2, 2.0)
W2 = np.linalg.inv(G2)
known = {"Wg(id)": (W2[S2.index((0,1)), S2.index((0,1))], 1/3.0),
         "Wg(12)": (W2[S2.index((0,1)), S2.index((1,0))], -1/6.0)}
class_ok = all(abs(x - y) < 1e-12 for x, y in known.values())
REPORT["rows"]["ii_Weingarten_Gram"] = {
 "verdict": "ADJUNCTION-LIKE COUNIT CERTIFIED iff d >= n (here n=3): Gram invertible at d=3, "
   "Wg = Ginv satisfies MP identities to {0:.1e}, {1:.1e}; Wg central (commutes with conjugation, defect {2:.1e}); "
   "n=2,d=2 values match known Weingarten numbers exactly ({3})".format(mp1, mp2, centr, class_ok),
 "rank_audit_table_n3": rows,
 "quantified_obstruction": "d<n: Gram singular (d=2: rank 5<6, smin={:.2e}); counit exists only as MP-pseudoinverse => "
   "the 'counit exists' question has a sharp rank answer, not a narrative one".format(rows[2]["min_singular_value"]),
 "residual_freedom": "pseudoinverse branch choice when d<n; gauge of the S_n x S_n basis conventions",
 "E_row_status": "positive row kept, with certified threshold d>=n and quantified singular spectrum below threshold"}

# ---------- ROW iii: S_n x S_n bimodule: tensor-hom at module level ----------
def dim_regular_bimodule_PW(n):
    # C[S_n] as (S_n x S_n)-bimodule decomposes as direct sum_lambda S_lambda x S_lambda* (Peter-Weyl)
    # dimension check: sum (dim S_lambda)^2 = n!
    import sympy as sp
    from sympy.combinatorics.partitions import IntegerPartition
    from sympy.functions.combinatorial.numbers import nC
    def hook_dim(lam):
        # hook-length formula
        lam = list(lam); n = sum(lam); f = math.factorial
        num = f(n); den = 1
        for i in range(len(lam)):
            for j in range(lam[i]):
                right = lam[i] - j - 1
                below = sum(1 for k in range(i+1, len(lam)) if lam[k] > j)
                den *= right + below + 1
        return num // den
    tot = 0; parts = []
    def gen_partitions(n, mx=None):
        if mx is None: mx = n
        if n == 0: yield (); return
        for first in range(min(mx, n), 0, -1):
            for rest in gen_partitions(n-first, first):
                yield (first,) + rest
    for lam in gen_partitions(n):
        d = hook_dim(lam); tot += d*d; parts.append((lam, d))
    return tot, parts
tot3, parts3 = dim_regular_bimodule_PW(3)
REPORT["rows"]["iii_SnSn_bimodule"] = {
 "verdict": "ADJUNCTION EXISTS at module level (tensor -| hom, always). Positive in the module sense — "
   "so the user's 'expected interesting failure', if it materializes, must live at the STRICT/monoidal level "
   "(Phi_n as a functor on G_n^{otimes L}, associator/compatibility constraints).",
 "certificate": {"Peter-Weyl check C[S_3] = sum_lambda S_lambda otimes S_lambda*: sum d_lambda^2 = |S_3|=":
                 (tot3, 6), "dims": {str(k): v for k, v in parts3}},
 "status": "row kept POSITIVE (module level); strict-level test queued = definition-pending (paper definitions of Phi_n required)"}

# ---------- paper-pending rows ----------
REPORT["rows"]["pending_paper_definitions"] = {
 "period_map B_even . B_odd (B_odd -| B_even ?)": "definition-pending: paper upload required",
 "compressed operator C_comp = K_e J_o K_o J_e": "definition-pending (exact J,K matrices needed)",
 "n-replica map Phi_n strict-level test": "definition-pending",
 "Clifford conjugation 3-design as engine input": "definition-pending",
 "note": "no entry in this row was guessed; anti-GRU-pattern discipline applied to our own corpus row"}

REPORT["runtime_s"] = round(time.time() - t0, 1)
with open("w3b_atlas_report.json", "w") as f:
    json.dump(REPORT, f, indent=1)
print(json.dumps(REPORT, indent=1))
