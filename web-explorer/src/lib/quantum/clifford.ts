/**
 * Stabilizer (Gottesman–Knill) simulator of the random hybrid Clifford circuit
 * studied in the "quantum-circuits" MIPT workspace.
 *
 * Model (verbatim from the deposited simulator spec):
 *   - L qubits on a ring (periodic boundary conditions), brickwork circuit.
 *   - One period = [measurement layer][gates on odd matching][measurement layer][gates on even matching].
 *   - Every site is measured in Z with probability p per measurement layer.
 *   - Gates: uniform random symplectic Sp(4,2) elements (the 720 two-qubit
 *     Clifford symplectic actions).
 *
 * Purification (Gullans–Huse) protocol: 2L qubits; system starts completely
 * mixed, realised as L Bell pairs between system qubit i and reference qubit
 * L+i. The circuit and all measurements act on the system only; the reference
 * is never touched, so S(reference) is the purification entropy of the mixed
 * system state.
 *
 * Implementation notes:
 *   - Phase-free tableau: every recorded quantity (entropies = stabilizer
 *     ranks, measurement counts) is invariant under Pauli phases, and
 *     Z-measurement outcome signs do not change the F2 structure of the
 *     stabilizer group. So we track only the binary generator matrix.
 *   - Entropy of subsystem A for a pure n-qubit stabilizer state:
 *       S(A) = |A| - n + rank(T restricted to columns OUTSIDE A),
 *     where T is the n x 2n generator matrix over F2.
 *   - The browser demo uses a fast 32-bit PRNG (mulberry32); the deposited
 *     pipeline uses the MT19937 seed contract (seed0 + k per trajectory).
 */

// ---------------------------------------------------------------------------
// Seeded RNG (mulberry32) — deterministic, seedable, adequate for this demo
// ---------------------------------------------------------------------------

export class RNG {
  private s: number;
  constructor(seed: number) {
    this.s = seed >>> 0;
    if (this.s === 0) this.s = 0x9e3779b9;
  }
  next(): number {
    // mulberry32
    let t = (this.s += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }
  int(maxExclusive: number): number {
    return Math.floor(this.next() * maxExclusive) % maxExclusive;
  }
}

// ---------------------------------------------------------------------------
// The 720 symplectic Sp(4,2) matrices, enumerated once.
// A 4x4 binary matrix M (acting on (x_i, z_i, x_j, z_j)) is symplectic iff
// M J M^T = J with J = [[0,I2],[I2,0]].
// Stored as 16 bytes row-major.
// ---------------------------------------------------------------------------

function enumerateSp4(): Uint8Array[] {
  const out: Uint8Array[] = [];
  // J as 4x4 (row-major) for the bit ordering (x_i, z_i, x_j, z_j):
  // the symplectic form pairs (x_i, z_i) and (x_j, z_j), i.e. J[a][b] = 1
  // for (0,1),(1,0),(2,3),(3,2).
  const Jbits = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0];
  const popParity = (x: number): number => {
    let v = x;
    v ^= v >> 2;
    v ^= v >> 1;
    return v & 1;
  };
  for (let m = 0; m < 65536; m++) {
    const r0 = (m >> 0) & 15;
    const r1 = (m >> 4) & 15;
    const r2 = (m >> 8) & 15;
    const r3 = (m >> 12) & 15;
    const rows = [r0, r1, r2, r3];
    // (MJ)[a] as a 4-bit row: bit b = XOR_l M[a][l] & J[l][b]
    const mj: number[] = [0, 0, 0, 0];
    for (let a = 0; a < 4; a++) {
      let row = 0;
      for (let b = 0; b < 4; b++) {
        let bit = 0;
        for (let l = 0; l < 4; l++) {
          if ((rows[a] >> l) & 1 && Jbits[l * 4 + b]) bit ^= 1;
        }
        row |= bit << b;
      }
      mj[a] = row;
    }
    // check (MJ) M^T == J : [a][b] = parity(mj[a] & r[b])
    let ok = true;
    outer: for (let a = 0; a < 4; a++) {
      for (let b = 0; b < 4; b++) {
        if (popParity(mj[a] & rows[b]) !== Jbits[a * 4 + b]) {
          ok = false;
          break outer;
        }
      }
    }
    if (ok) {
      const M = new Uint8Array(16);
      for (let a = 0; a < 4; a++) {
        for (let b = 0; b < 4; b++) M[a * 4 + b] = (rows[a] >> b) & 1;
      }
      out.push(M);
    }
  }
  return out;
}

let SP4_CACHE: Uint8Array[] | null = null;
export function getSp4(): Uint8Array[] {
  if (!SP4_CACHE) SP4_CACHE = enumerateSp4();
  return SP4_CACHE;
}

// ---------------------------------------------------------------------------
// Phase-free stabilizer tableau
// ---------------------------------------------------------------------------

export class Tableau {
  n: number; // number of qubits (rows = independent generators)
  rows: Uint8Array; // n x 2n bytes; columns 0..n-1 = x, n..2n-1 = z
  ncols: number;

  constructor(n: number) {
    this.n = n;
    this.ncols = 2 * n;
    this.rows = new Uint8Array(n * this.ncols);
  }

  // |0...0>: generator i = Z_i
  static zeros(n: number): Tableau {
    const t = new Tableau(n);
    for (let i = 0; i < n; i++) t.rows[i * t.ncols + n + i] = 1;
    return t;
  }

  // Bell pairs (i, L+i): generators X_i X_{L+i}, Z_i Z_{L+i}
  static bellPairs(L: number): Tableau {
    const n = 2 * L;
    const t = new Tableau(n);
    for (let i = 0; i < L; i++) {
      t.rows[2 * i * t.ncols + i] = 1;
      t.rows[2 * i * t.ncols + (L + i)] = 1;
      t.rows[(2 * i + 1) * t.ncols + n + i] = 1;
      t.rows[(2 * i + 1) * t.ncols + n + (L + i)] = 1;
    }
    return t;
  }

  clone(): Tableau {
    const t = new Tableau(this.n);
    t.rows.set(this.rows);
    return t;
  }

  rowXor(a: number, b: number): void {
    const nc = this.ncols;
    const ra = a * nc;
    const rb = b * nc;
    for (let c = 0; c < nc; c++) this.rows[ra + c] ^= this.rows[rb + c];
  }

  /**
   * Apply a two-qubit Clifford (given by its 4x4 symplectic matrix M) to
   * qubits (i, j). Each generator row's 4 bits (x_i, z_i, x_j, z_j) transform
   * as v -> M v over F2.
   */
  applyTwoQubit(i: number, j: number, M: Uint8Array): void {
    const n = this.n;
    const nc = this.ncols;
    const rows = this.rows;
    const ci = i;
    const czi = n + i;
    const cj = j;
    const czj = n + j;
    for (let r = 0; r < n; r++) {
      const base = r * nc;
      const b0 = rows[base + ci];
      const b1 = rows[base + czi];
      const b2 = rows[base + cj];
      const b3 = rows[base + czj];
      if (b0 === 0 && b1 === 0 && b2 === 0 && b3 === 0) continue;
      const nb0 = (b0 && M[0] ? 1 : 0) ^ (b1 && M[1] ? 1 : 0) ^ (b2 && M[2] ? 1 : 0) ^ (b3 && M[3] ? 1 : 0);
      const nb1 = (b0 && M[4] ? 1 : 0) ^ (b1 && M[5] ? 1 : 0) ^ (b2 && M[6] ? 1 : 0) ^ (b3 && M[7] ? 1 : 0);
      const nb2 = (b0 && M[8] ? 1 : 0) ^ (b1 && M[9] ? 1 : 0) ^ (b2 && M[10] ? 1 : 0) ^ (b3 && M[11] ? 1 : 0);
      const nb3 = (b0 && M[12] ? 1 : 0) ^ (b1 && M[13] ? 1 : 0) ^ (b2 && M[14] ? 1 : 0) ^ (b3 && M[15] ? 1 : 0);
      rows[base + ci] = nb0;
      rows[base + czi] = nb1;
      rows[base + cj] = nb2;
      rows[base + czj] = nb3;
    }
  }

  /**
   * Measure qubit i in the Z basis (phase-free):
   * find a pivot generator with x_i = 1 (anticommutes with Z_i);
   * if found, XOR it into every other such row, then set the pivot row to Z_i.
   * Returns 1 if the outcome was random (pivot existed), 0 if deterministic.
   */
  measureZ(i: number): 0 | 1 {
    const n = this.n;
    const nc = this.ncols;
    const rows = this.rows;
    let pivot = -1;
    for (let r = 0; r < n; r++) {
      if (rows[r * nc + i] === 1) {
        if (pivot < 0) pivot = r;
        else this.rowXor(r, pivot);
      }
    }
    if (pivot < 0) return 0;
    const base = pivot * nc;
    for (let c = 0; c < nc; c++) rows[base + c] = 0;
    rows[base + n + i] = 1;
    return 1;
  }

  /**
   * Entropy (bits) of the subsystem given by `sites`, for this pure
   * stabilizer state:  S(A) = |A| - n + rank(T_{outside A}).
   */
  entropy(sites: number[]): number {
    const n = this.n;
    const nc = this.ncols;
    const inA = new Uint8Array(nc);
    for (const s of sites) {
      inA[s] = 1;
      inA[n + s] = 1;
    }
    const outCols: number[] = [];
    for (let c = 0; c < nc; c++) if (!inA[c]) outCols.push(c);
    const w = outCols.length;
    const mat = new Uint8Array(n * w);
    for (let r = 0; r < n; r++) {
      for (let k = 0; k < w; k++) mat[r * w + k] = this.rows[r * nc + outCols[k]];
    }
    // Gaussian elimination over F2
    let rank = 0;
    for (let col = 0; col < w && rank < n; col++) {
      let piv = -1;
      for (let r = rank; r < n; r++) {
        if (mat[r * w + col] === 1) {
          piv = r;
          break;
        }
      }
      if (piv < 0) continue;
      if (piv !== rank) {
        for (let k = 0; k < w; k++) {
          const tmp = mat[piv * w + k];
          mat[piv * w + k] = mat[rank * w + k];
          mat[rank * w + k] = tmp;
        }
      }
      for (let r = rank + 1; r < n; r++) {
        if (mat[r * w + col] === 1) {
          for (let k = col; k < w; k++) mat[r * w + k] ^= mat[rank * w + k];
        }
      }
      rank++;
    }
    return sites.length - n + rank;
  }
}

// ---------------------------------------------------------------------------
// Simulator: hybrid random Clifford circuit with measurements
// ---------------------------------------------------------------------------

export type SimMode = "pure" | "purif";

export interface SimOptions {
  L: number;
  p: number;
  mode: SimMode;
  seed: number;
}

export interface LayerEvent {
  kind: "meas" | "gates";
  parity: 0 | 1; // gate matching (0 = odd pairs, 1 = even pairs)
  measured?: number[]; // measured sites (meas layers)
  gates?: { i: number; j: number; g: number }[];
}

export interface PeriodRecord {
  t: number; // period index (1-based)
  sA: number; // half-chain entropy of the SYSTEM (bits)
  sRef: number; // purification entropy (purif mode only)
  i3: number; // tripartite mutual information (pure mode, L % 4 === 0)
  nMeas: number; // cumulative measurements
  nRand: number; // cumulative random outcomes
}

function range(a: number, b: number): number[] {
  const out: number[] = [];
  for (let k = a; k < b; k++) out.push(k);
  return out;
}

export class HybridCircuit {
  L: number;
  p: number;
  mode: SimMode;
  n: number;
  tab: Tableau;
  rng: RNG;
  sp4: Uint8Array[];
  t: number; // completed periods
  nMeas: number;
  nRand: number;
  events: LayerEvent[]; // visualization log of the CURRENT period

  constructor(opts: SimOptions) {
    this.L = opts.L;
    this.p = opts.p;
    this.mode = opts.mode;
    this.n = opts.mode === "purif" ? 2 * opts.L : opts.L;
    this.tab = opts.mode === "purif" ? Tableau.bellPairs(opts.L) : Tableau.zeros(opts.L);
    this.rng = new RNG(opts.seed);
    this.sp4 = getSp4();
    this.t = 0;
    this.nMeas = 0;
    this.nRand = 0;
    this.events = [];
  }

  /** One measurement sweep over the system sites. */
  private measSweep(): LayerEvent {
    const measured: number[] = [];
    for (let s = 0; s < this.L; s++) {
      if (this.rng.next() < this.p) {
        this.nMeas++;
        if (this.tab.measureZ(s) === 1) this.nRand++;
        measured.push(s);
      }
    }
    return { kind: "meas", parity: 0, measured };
  }

  /** One gate layer with the given brickwork matching. */
  private gateLayer(parity: 0 | 1): LayerEvent {
    const gates: { i: number; j: number; g: number }[] = [];
    const half = this.L >> 1;
    for (let b = 0; b < half; b++) {
      const i = (2 * b + parity) % this.L;
      const j = (2 * b + 1 + parity) % this.L;
      const g = this.rng.int(720);
      this.tab.applyTwoQubit(i, j, this.sp4[g]);
      gates.push({ i, j, g });
    }
    return { kind: "gates", parity, gates };
  }

  /** Observables at the current time. */
  record(): PeriodRecord {
    const L = this.L;
    const half = L >> 1;
    const rec: PeriodRecord = {
      t: this.t,
      sA: this.tab.entropy(range(0, half)),
      sRef: this.mode === "purif" ? this.tab.entropy(range(L, 2 * L)) : 0,
      i3: 0,
      nMeas: this.nMeas,
      nRand: this.nRand,
    };
    if (this.mode === "pure" && L % 4 === 0) {
      // I3(A:B:C) = S_A + S_B + S_C - S_AB - S_AC - S_BC + S_ABC
      // for three contiguous quarters A, B, C (D = the last quarter)
      const q = L >> 2;
      const sA = this.tab.entropy(range(0, q));
      const sB = this.tab.entropy(range(q, 2 * q));
      const sC = this.tab.entropy(range(2 * q, 3 * q));
      const sAB = this.tab.entropy(range(0, 2 * q));
      const sAC = this.tab.entropy([...range(0, q), ...range(2 * q, 3 * q)]);
      const sBC = this.tab.entropy(range(q, 3 * q));
      const sABC = this.tab.entropy(range(0, 3 * q));
      rec.i3 = sA + sB + sC - sAB - sAC - sBC + sABC;
    }
    return rec;
  }

  /**
   * Advance one period:
   * [meas][gates odd][meas][gates even], then record observables.
   */
  stepPeriod(): PeriodRecord {
    this.events = [];
    this.events.push(this.measSweep());
    this.events.push(this.gateLayer(0));
    this.events.push(this.measSweep());
    this.events.push(this.gateLayer(1));
    this.t++;
    return this.record();
  }

  /**
   * Advance one period WITHOUT computing observables — the ensemble
   * fast path. Observable evaluation (7 rank computations for I₃) is the
   * dominant cost per period, and batch runs only need it at recording
   * times t = τL. Reusing measSweep/gateLayer keeps the trajectory
   * bit-identical to stepPeriod (same RNG stream, same operations).
   */
  stepPeriodFast(): void {
    this.events = [];
    this.measSweep();
    this.gateLayer(0);
    this.measSweep();
    this.gateLayer(1);
    this.t++;
  }
}

// ---------------------------------------------------------------------------
// Ensemble runner (used by the API for batch trajectories)
// ---------------------------------------------------------------------------

export interface EnsemblePoint {
  tau: number;
  mean: number;
  se: number;
}

export interface EnsembleResult {
  L: number;
  p: number;
  mode: SimMode;
  nTraj: number;
  sRef: EnsemblePoint[];
  sA: EnsemblePoint[];
  i3: EnsemblePoint[];
  elapsedMs: number;
}

export function runEnsemble(opts: {
  L: number;
  p: number;
  mode: SimMode;
  nTraj: number;
  taus: number[];
  seed0: number;
}): EnsembleResult {
  const t0 = Date.now();
  const { L, p, mode, nTraj, taus, seed0 } = opts;
  const recT = taus.map((tau) => Math.max(1, Math.round(tau * L)));
  const maxT = Math.max(...recT);
  const acc = recT.map(() => ({ sRef: [] as number[], sA: [] as number[], i3: [] as number[] }));

  for (let k = 0; k < nTraj; k++) {
    const sim = new HybridCircuit({ L, p, mode, seed: seed0 + k });
    let ri = 0;
    for (let t = 1; t <= maxT && ri < recT.length; t++) {
      if (t === recT[ri]) {
        const rec = sim.stepPeriod();
        acc[ri].sRef.push(rec.sRef);
        acc[ri].sA.push(rec.sA);
        acc[ri].i3.push(rec.i3);
        ri++;
      } else {
        sim.stepPeriodFast();
      }
    }
  }

  const mk = (arr: number[], tau: number): EnsemblePoint => {
    const n = arr.length || 1;
    const mean = arr.reduce((a, b) => a + b, 0) / n;
    const varr = n > 1 ? arr.reduce((a, b) => a + (b - mean) * (b - mean), 0) / (n - 1) : 0;
    return { tau, mean, se: Math.sqrt(varr / n) };
  };

  return {
    L,
    p,
    mode,
    nTraj,
    sRef: taus.map((tau, i) => mk(acc[i].sRef, tau)),
    sA: taus.map((tau, i) => mk(acc[i].sA, tau)),
    i3: taus.map((tau, i) => mk(acc[i].i3, tau)),
    elapsedMs: Date.now() - t0,
  };
}

// ---------------------------------------------------------------------------
// I₃ crossing sweep (pure-state locator): mean I₃(p, L) over a p-grid
// ---------------------------------------------------------------------------

export interface I3SweepPoint {
  p: number;
  mean: number;
  se: number;
}

export interface I3SweepResult {
  L: number;
  tau: number;
  nTraj: number;
  elapsedMs: number;
  points: I3SweepPoint[];
  /** per-p trajectory values, aligned with points — the raw material for
   *  non-parametric (trajectory-level) bootstraps on the client */
  traj?: number[][];
}

/**
 * Sweep the measurement probability over `ps` for one system size and
 * return ⟨I₃⟩ ± s.e. at time t = τL (pure state, three contiguous
 * quarters). This is the Gullans–Huse locator: the I₃(p) curves for
 * different L cross near p_c, with a drift that shrinks as L grows.
 */
export function runI3Sweep(opts: {
  L: number;
  ps: number[];
  nTraj: number;
  tau: number;
  seed0: number;
}): I3SweepResult {
  const t0 = Date.now();
  const { L, ps, nTraj, tau, seed0 } = opts;
  const recT = Math.max(1, Math.round(tau * L));
  const vals = ps.map(() => [] as number[]);

  for (let k = 0; k < nTraj; k++) {
    for (let pi = 0; pi < ps.length; pi++) {
      const sim = new HybridCircuit({
        L,
        p: ps[pi],
        mode: "pure",
        seed: seed0 + k * ps.length + pi,
      });
      for (let t = 1; t < recT; t++) sim.stepPeriodFast();
      vals[pi].push(sim.stepPeriod().i3);
    }
  }

  const points = ps.map((p, pi) => {
    const arr = vals[pi];
    const n = arr.length || 1;
    const mean = arr.reduce((a, b) => a + b, 0) / n;
    const varr = n > 1 ? arr.reduce((a, b) => a + (b - mean) * (b - mean), 0) / (n - 1) : 0;
    return { p, mean, se: Math.sqrt(varr / n) };
  });

  return { L, tau, nTraj, elapsedMs: Date.now() - t0, points, traj: vals.map((v) => [...v]) };
}

/**
 * One trajectory's I₃ at time t = τL for a single (L, p) — the atomic unit
 * the large-L background job runner chunks on (≈ 30 ms at L=128, ≈ 220 ms at
 * L=256), yielding to the event loop between units so poll requests and
 * response flushes interleave with the computation.
 */
export function sweepTrajI3(opts: {
  L: number;
  p: number;
  tau: number;
  seed: number;
}): number {
  const { L, p, tau, seed } = opts;
  const recT = Math.max(1, Math.round(tau * L));
  const sim = new HybridCircuit({ L, p, mode: "pure", seed });
  for (let t = 1; t < recT; t++) sim.stepPeriodFast();
  return sim.stepPeriod().i3;
}

/**
 * One p-point of an I₃ sweep (all its trajectories), computed synchronously.
 * Shares the exact seed contract of runI3Sweep — seed = seed0 + k·|ps| + pi —
 * so a point-wise (background) sweep reproduces the batch sweep bit-for-bit.
 */
export function sweepPointI3(opts: {
  L: number;
  p: number;
  nTraj: number;
  tau: number;
  seed0: number;
  psIndex: number;
  psCount: number;
}): I3SweepPoint {
  const { L, p, nTraj, tau, seed0, psIndex, psCount } = opts;
  const vals: number[] = [];
  for (let k = 0; k < nTraj; k++) {
    vals.push(sweepTrajI3({ L, p, tau, seed: seed0 + k * psCount + psIndex }));
  }
  const n = vals.length || 1;
  const mean = vals.reduce((a, b) => a + b, 0) / n;
  const varr = n > 1 ? vals.reduce((a, b) => a + (b - mean) * (b - mean), 0) / (n - 1) : 0;
  return { p, mean, se: Math.sqrt(varr / n) };
}
