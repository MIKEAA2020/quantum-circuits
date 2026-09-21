"""mipt_born_scgf.py -- quenched record-SCGF trajectories (v16).

Vectorised stabilizer (Gottesman-Knill) simulator of the monitored random
Clifford circuit, tracking per trajectory:
  * X_R = -log2 P(R) = the number of random (non-deterministic) measurement
    outcomes (each random outcome contributes exactly a factor 1/2 to the
    record probability -- stabilizer measurement outcomes are uniform over
    the free bits), so P(R) = 2^{-X_R} EXACTLY;
  * S_{L/2} at the recording time t = tau*L periods.

Model (identical to the exact channel of mipt_scgf_exact.py and to the
deposited simulator spec): ring of L qubits, one period =
[measurement layer][gates on the even matching][measurement layer][gates on
the odd matching]; every site measured in Z with probability p per layer;
gates uniform over the 720 symplectic Sp(4,2) two-qubit Clifford actions.

Batch implementation: B trajectories evolve simultaneously; the tableau is
(B, n) uint64 pairs (x-word, z-word), one row per stabilizer generator.
New seed contract (v16 data, NOT the deposit's): numpy PCG64 seeded with
seed = SEED0 + cell_index; the full RNG stream per cell is reproducible.

Validation targets:
  (L=8, t=4, p=0.16, 40k traj): E[2^{-X}] vs exact Z2 = 1.4796e-2
      (deposit sampled 1.4942e-2); E[S_{L/2}] vs deposit 2.019(4);
      tilt ESS vs deposit 5935.
  (L=12, t=6, p=0.16): E[2^{-X}] vs exact Z2 = 3.8173e-5.

Production (t = 4L): Xi_L(beta) = ln E[2^{-beta X}]/(2Lt), the quenched
information density xbar = E[X]/(2Lt), Var(x)*L, the Jensen (annealed minus
quenched) gap, the collision-tilt ESS and IPR, tilted densities; bootstrap
errors (200 resamples).
"""

import json
import sys
import time
import numpy as np

sys.path.insert(0, ".")


# ---------------------------------------------------------------------------
# The 720 symplectic Sp(4,2) matrices as 16-entry LUTs on the bit slice
# (x_i, z_i, x_j, z_j) -> new (x_i, z_i, x_j, z_j).
# ---------------------------------------------------------------------------

def enumerate_sp4_luts():
    """Returns (720, 16) uint8 array: LUT[g][v] = M v over F2, v = 4-bit."""
    Jbits = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]

    def pop_parity(x):
        v = x & 0xFFFFFFFF
        v ^= v >> 2
        v ^= v >> 1
        return v & 1

    luts = []
    for m in range(65536):
        rows = [(m >> (4 * a)) & 15 for a in range(4)]
        mj = []
        for a in range(4):
            row = 0
            for b in range(4):
                bit = 0
                for l in range(4):
                    if ((rows[a] >> l) & 1) and Jbits[l * 4 + b]:
                        bit ^= 1
                row |= bit << b
            mj.append(row)
        ok = True
        for a in range(4):
            for b in range(4):
                if pop_parity(mj[a] & rows[b]) != Jbits[a * 4 + b]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            lut = np.zeros(16, dtype=np.uint8)
            for v in range(16):
                out = 0
                for b in range(4):
                    bit = 0
                    for a in range(4):
                        if (v >> a) & 1 and (rows[b] >> a) & 1:
                            bit ^= 1
                    out |= bit << b
                lut[v] = out
            luts.append(lut)
    return np.array(luts)


SP4_LUTS = enumerate_sp4_luts()   # (720, 16)
assert SP4_LUTS.shape == (720, 16), SP4_LUTS.shape


# ---------------------------------------------------------------------------
# Batch tableau
# ---------------------------------------------------------------------------

class BatchCircuit:
    def __init__(self, L, p, B, rng):
        self.L = L
        self.n = L
        self.p = p
        self.B = B
        self.rng = rng
        self.rx = np.zeros((B, L), dtype=np.uint64)
        self.rz = np.zeros((B, L), dtype=np.uint64)
        for i in range(L):
            self.rz[:, i] = np.uint64(1 << i)   # |0...0>: row i = Z_i
        self.X = np.zeros(B, dtype=np.int64)    # record information (bits)
        self.t = 0

    def _apply_gate_layer(self, parity):
        L, B, n = self.L, self.B, self.n
        half = L // 2
        for b in range(half):
            i = (2 * b + parity) % L
            j = (2 * b + 1 + parity) % L
            g = self.rng.integers(0, 720, size=B)
            mi, mj = (1 << i), (1 << j)
            v = (((self.rx >> np.uint64(i)) & np.uint64(1))
                 | (((self.rz >> np.uint64(i)) & np.uint64(1)) << np.uint64(1))
                 | (((self.rx >> np.uint64(j)) & np.uint64(1)) << np.uint64(2))
                 | (((self.rz >> np.uint64(j)) & np.uint64(1)) << np.uint64(3)))
            vnew = SP4_LUTS[g[:, None], v]
            keep = ~np.uint64(mi | mj)
            self.rx = (self.rx & keep) | ((vnew & np.uint64(1)) << np.uint64(i)) \
                | (((vnew >> np.uint64(2)) & np.uint64(1)) << np.uint64(j))
            self.rz = (self.rz & keep) | (((vnew >> np.uint64(1)) & np.uint64(1)) << np.uint64(i)) \
                | (((vnew >> np.uint64(3)) & np.uint64(1)) << np.uint64(j))

    def _measure_site(self, i, enable):
        """Z-measure site i on enabled trajectories. Returns random-outcome flags."""
        rx, rz, B, n = self.rx, self.rz, self.B, self.n
        hasx = (((rx >> np.uint64(i)) & np.uint64(1)) != 0) & enable[:, None]
        anyx = hasx.any(axis=1)
        pivot = np.argmax(hasx, axis=1)   # first True (valid where anyx)
        ar = np.arange(B)
        piv_rx = rx[ar, pivot]
        piv_rz = rz[ar, pivot]
        # XOR pivot row into other rows with the bit (excluding the pivot)
        mask = hasx & (ar[:, None] != pivot[:, None])
        self.rx = rx ^ (mask * piv_rx[:, None])
        self.rz = rz ^ (mask * piv_rz[:, None])
        # reset the pivot row to Z_i
        sel = ar[anyx]
        if sel.size:
            self.rx[sel, pivot[anyx]] = np.uint64(0)
            self.rz[sel, pivot[anyx]] = np.uint64(1 << i)
        return anyx

    def _meas_sweep(self):
        L, B = self.L, self.B
        measured = self.rng.random((B, L)) < self.p
        for i in range(L):
            flags = self._measure_site(i, measured[:, i])
            self.X += flags
        return measured

    def step_period(self):
        self._meas_sweep()
        self._apply_gate_layer(0)
        self._meas_sweep()
        self._apply_gate_layer(1)
        self.t += 1

    def entropy_half(self):
        """S(A), A = sites 0..L/2-1: S = |A| - n + rank(T outside A)."""
        L, B, n = self.L, self.B, self.n
        half = L // 2
        # outside-A columns: x_k, z_k for k >= half -> pack per row into uint32
        # bit ordering of packed word: for k in range(half, L):
        #   bit 2*(k-half)   = x_k,  bit 2*(k-half)+1 = z_k
        mat = np.zeros((B, n), dtype=np.uint32)
        for k in range(half, L):
            xk = ((self.rx >> np.uint64(k)) & np.uint64(1)).astype(np.uint32)
            zk = ((self.rz >> np.uint64(k)) & np.uint64(1)).astype(np.uint32)
            mat |= (xk << np.uint32(2 * (k - half))) | (zk << np.uint32(2 * (k - half) + 1))
        used = np.zeros((B, n), dtype=bool)
        rank = np.zeros(B, dtype=np.int64)
        ar = np.arange(B)
        ncols = 2 * (L - half)
        for col in range(ncols):
            hasbit = ((mat >> np.uint32(col)) & np.uint32(1)) != 0
            elig = hasbit & ~used
            found = elig.any(axis=1)
            piv = np.argmax(elig, axis=1)
            piv_row = mat[ar, piv]
            elim = hasbit & ~used & (ar[:, None] != piv[:, None])
            mat = mat ^ (elim * piv_row[:, None])
            used[ar[found], piv[found]] = True
            rank += found
        return half - n + rank


# ---------------------------------------------------------------------------
# Cell runner + SCGF statistics
# ---------------------------------------------------------------------------

SEED0 = 20260529


def run_cell(L, p, tau, B, seed, want_entropy=True):
    rng = np.random.Generator(np.random.PCG64(seed))
    sim = BatchCircuit(L, p, B, rng)
    tmax = max(1, int(round(tau * L)))
    t0 = time.time()
    for _ in range(tmax):
        sim.step_period()
    sA = sim.entropy_half() if want_entropy else np.zeros(B)
    elapsed = time.time() - t0
    return {"X": sim.X, "S": sA, "t": tmax, "elapsed": elapsed}


def scgf_stats(X, S, L, t, nboot=200, rng=None):
    """SCGF and freezing diagnostics from per-trajectory X (= -log2 P(R))."""
    if rng is None:
        rng = np.random.Generator(np.random.PCG64(12345))
    B = len(X)
    nsite = 2 * L * t
    logp = -np.log(2.0) * X                    # ln P(R)
    out = {
        "B": B, "L": L, "t": t, "nsite": nsite,
        "xbar": float(X.mean()) / nsite,        # quenched info density (bits/site)
        "xbar_var": float(X.var()) / nsite ** 2,
        "varX_over_nsite": float(X.var()) / nsite,   # effective per-site variance
        "var_x": float(X.var()) / nsite ** 2,
        "S_mean": float(S.mean()), "S_se": float(S.std() / np.sqrt(B)),
        "Elogp_per_site": float(logp.mean()) / nsite,
    }
    betas = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    for beta in betas:
        w = np.exp(-beta * np.log(2.0) * X)     # 2^{-beta X} = P^beta
        m = float(w.mean())
        out[f"Xi_{beta}"] = float(np.log(m)) / nsite
        # tilted density m(beta) = E[2^{-bX} X]/E[2^{-bX}]/nsite
        out[f"mtilt_{beta}"] = float((w * X).mean() / m) / nsite
        if beta == 1.0:
            wmax = float(w.max())
            ws = w / wmax
            ess = float(ws.sum() ** 2 / (ws ** 2).sum())
            out["ESS_beta1"] = ess
            out["ESS_frac"] = ess / B
            out["IPR_beta1"] = B / ess if ess > 0 else np.inf   # E[p^2]^2/E[p^4]
        if beta == 2.0:
            m2 = float((np.exp(-np.log(2.0) * X)).mean())      # E[p]
            m4 = float(w.mean())                                # E[p^2] (beta=2)
            out["Y2_collision"] = float(np.exp(-np.log(2.0) * X).mean() ** 2 / m4) \
                if m4 > 0 else np.inf
    # Jensen gap (annealed minus quenched, per site)
    out["jensen_gap"] = float(np.log(np.exp(logp).mean()) - logp.mean()) / nsite
    # bootstrap
    keys = ["xbar", "Xi_0.25", "Xi_1.0", "ESS_frac", "jensen_gap", "S_mean"]
    boot = {k: [] for k in keys}
    for _ in range(nboot):
        idx = rng.integers(0, B, size=B)
        Xb, Sb = X[idx], S[idx]
        lp = -np.log(2.0) * Xb
        boot["xbar"].append(Xb.mean() / nsite)
        for beta in (0.25, 1.0):
            w = np.exp(-beta * lp)
            out_k = f"Xi_{beta}"
            if out_k in boot:
                boot[out_k].append(np.log(w.mean()) / nsite)
        w1 = np.exp(-lp)
        wmax = float(w1.max())
        ws = w1 / wmax
        ess = ws.sum() ** 2 / (ws ** 2).sum()
        boot["ESS_frac"].append(ess / B)
        boot["jensen_gap"].append((np.log(np.exp(lp).mean()) - lp.mean()) / nsite)
        boot["S_mean"].append(Sb.mean())
    out["boot_se"] = {k: float(np.std(v)) for k, v in boot.items()}
    return out


def main():
    results = {"validation": [], "production": [], "meta": {
        "script": "mipt_born_scgf.py",
        "seed0": SEED0,
        "rng": "numpy PCG64; per-cell seed = SEED0 + cell index",
        "simulator": "vectorised phase-free F2 tableau; X_R = #random outcomes; P(R)=2^{-X_R}",
    }}
    cell = 0

    # ---- validation against the deposited tilt chain (t = L/2) ----
    print("== validation (deposit tilt-chain points, t = L/2 periods) ==", flush=True)
    for (L, t, p, B, exact_Z2, dep_E2X, dep_ES, dep_S) in [
        (8, 4, 0.16, 40000, 1.479639e-2, 1.4942e-2, 5935.0, 2.019),
        (12, 6, 0.16, 40000, 3.817310e-05, None, 454.0, 2.394),
    ]:
        r = run_cell(L, p, t / L, B, SEED0 + cell)
        cell += 1
        E2X = float(np.exp(-np.log(2) * r["X"]).mean())
        w = np.exp(-np.log(2) * r["X"])
        ess = float(w.sum() ** 2 / (w ** 2).sum())
        rec = {
            "L": L, "t": t, "p": p, "B": B,
            "E_2minusX": E2X, "exact_Z2": exact_Z2,
            "deposit_sampled": dep_E2X,
            "rel_diff_exact": abs(E2X - exact_Z2) / exact_Z2,
            "ESS": ess, "deposit_ESS": dep_ES,
            "E_S": float(r["S"].mean()), "E_S_se": float(r["S"].std() / np.sqrt(B)),
            "deposit_E_S": dep_S,
            "elapsed": r["elapsed"],
        }
        results["validation"].append(rec)
        print(f"  L={L} t={t} p={p}: E[2^-X] = {E2X:.4e} (exact {exact_Z2:.4e}, "
              f"deposit-sampled {dep_E2X}); ESS = {ess:.0f} (deposit {dep_ES}); "
              f"E[S] = {r['S'].mean():.3f}({r['S'].std()/np.sqrt(B):.3f}) "
              f"(deposit {dep_S})  [{r['elapsed']:.1f}s]", flush=True)

    # ---- production: t = 4L, the FSS times ----
    print("== production (t = 4L) ==", flush=True)
    grid = [(8, 0.16, 40000), (12, 0.16, 40000), (16, 0.16, 30000), (24, 0.16, 15000),
            (8, 0.22, 40000), (12, 0.22, 40000), (16, 0.22, 30000), (24, 0.22, 15000)]
    for (L, p, B) in grid:
        r = run_cell(L, p, 4, B, SEED0 + cell)
        cell += 1
        st = scgf_stats(r["X"], r["S"], L, r["t"])
        st.update({"p": p, "elapsed": r["elapsed"]})
        results["production"].append(st)
        print(f"  L={L:3d} p={p}: xbar={st['xbar']:.5f} bits/site, "
              f"Xi(0.25)={st['Xi_0.25']:.2e}, Xi(1)={st['Xi_1.0']:.2e}, "
              f"ESS%={100*st['ESS_frac']:.2e}, gap={st['jensen_gap']:.2e}, "
              f"Var(X)/nsite={st['varX_over_nsite']:.4f}, E[S]={st['S_mean']:.3f}"
              f"  [{r['elapsed']:.1f}s]", flush=True)
        np.savez_compressed(f"../results/scgf_born_raw_L{L}_p{int(100*p)}.npz",
                            X=r["X"].astype(np.int32), S=r["S"].astype(np.int32))

    with open("../results/scgf_born.json", "w") as f:
        json.dump(results, f, indent=1)
    print("wrote ../results/scgf_born.json")


if __name__ == "__main__":
    main()
