/**
 * Finite-size-scaling fit machinery for user-generated I₃ sweeps.
 *
 * Implements the paper's own method: weighted quartic fit of ⟨I₃⟩ vs
 * x = (p − p_c)·L^{1/ν} inside a fixed |x| ≤ 3 window, with an error floor
 * of 1/N per point (the deposited fix for the 10⁻⁴-floor weighting defect —
 * a point with I₃ ≡ 0 across all trajectories would otherwise carry ~98% of
 * a fit's weight).
 */

export interface SeriesPoint {
  p: number;
  mean: number;
  se: number;
}

export type SeriesMap = Record<number, SeriesPoint[]>;

export interface CollapseFit {
  /** sqrt(chi² / Σw) — tightness metric, lower = better collapse */
  q: number;
  /** raw weighted χ² of the quartic fit */
  chi2: number;
  /** total weight Σw */
  wsum: number;
  /** number of points inside the window */
  npts: number;
  /** quartic coefficients c0..c4 (null if underdetermined) */
  coeffs: number[] | null;
}

/** Solve the 5×5 weighted normal equations for a quartic in x. */
function quarticFit(pts: { x: number; y: number; w: number }[]): number[] | null {
  const K = 5;
  const A: number[][] = Array.from({ length: K }, () => new Array(K).fill(0));
  const b: number[] = new Array(K).fill(0);
  for (const pt of pts) {
    const pw = [1, pt.x, pt.x * pt.x, pt.x ** 3, pt.x ** 4];
    for (let i = 0; i < K; i++) {
      for (let j = 0; j < K; j++) A[i][j] += pt.w * pw[i] * pw[j];
      b[i] += pt.w * pw[i] * pt.y;
    }
  }
  const M = A.map((row, i) => [...row, b[i]]);
  for (let col = 0; col < K; col++) {
    let piv = col;
    for (let r = col + 1; r < K; r++) if (Math.abs(M[r][col]) > Math.abs(M[piv][col])) piv = r;
    [M[col], M[piv]] = [M[piv], M[col]];
    if (Math.abs(M[col][col]) < 1e-12) return null;
    for (let r = col + 1; r < K; r++) {
      const f = M[r][col] / M[col][col];
      for (let c = col; c <= K; c++) M[r][c] -= f * M[col][c];
    }
  }
  const c = new Array(K).fill(0);
  for (let i = K - 1; i >= 0; i--) {
    let s = M[i][K];
    for (let j = i + 1; j < K; j++) s -= M[i][j] * c[j];
    c[i] = s / M[i][i];
  }
  return c;
}

/** Weighted quartic collapse fit at (p_c, ν). */
export function collapseFit(
  series: SeriesMap,
  sizes: number[],
  pc: number,
  nu: number,
  nTraj: number,
  xWin = 3
): CollapseFit | null {
  const floor = 1 / Math.max(nTraj, 1);
  const pts: { x: number; y: number; w: number }[] = [];
  for (const L of sizes)
    for (const pt of series[L] ?? []) {
      const x = (pt.p - pc) * Math.pow(L, 1 / nu);
      if (Math.abs(x) > xWin) continue;
      pts.push({ x, y: pt.mean, w: 1 / Math.max(pt.se, floor) ** 2 });
    }
  if (pts.length < 9) return null; // need ≥ 9 points for a meaningful 5-param fit
  const c = quarticFit(pts);
  if (!c) return null;
  let chi2 = 0;
  let wsum = 0;
  for (const pt of pts) {
    const yh = c[0] + c[1] * pt.x + c[2] * pt.x ** 2 + c[3] * pt.x ** 3 + c[4] * pt.x ** 4;
    chi2 += pt.w * (pt.y - yh) ** 2;
    wsum += pt.w;
  }
  return { q: Math.sqrt(chi2 / wsum), chi2, wsum, npts: pts.length, coeffs: c };
}

/** Tightness-only convenience wrapper (NaN when underdetermined). */
export function collapseQuality(
  series: SeriesMap,
  sizes: number[],
  pc: number,
  nu: number,
  nTraj: number,
  xWin = 3
): number {
  const f = collapseFit(series, sizes, pc, nu, nTraj, xWin);
  return f ? f.q : NaN;
}

/** Best p_c at frozen ν (fine p_c scan inside the deposited search window). */
export function bestPcAtNu(
  series: SeriesMap,
  sizes: number[],
  nu: number,
  nTraj: number,
  pcMin = 0.14,
  pcMax = 0.18,
  step = 0.0005
): { pc: number; chi2: number; q: number } | null {
  let best: { pc: number; chi2: number; q: number } | null = null;
  for (let pc = pcMin; pc <= pcMax + 1e-9; pc += step) {
    const f = collapseFit(series, sizes, pc, nu, nTraj);
    if (f && (!best || f.chi2 < best.chi2)) best = { pc, chi2: f.chi2, q: f.q };
  }
  return best;
}

export interface ProfilePoint {
  nu: number;
  /** minimum χ² over p_c at this ν */
  chi2: number;
  /** χ² − χ²_min (profile minimum) */
  dchi2: number;
  /** argmin p_c at this ν */
  bestPc: number;
  q: number;
}

export interface Dchi2Profile {
  points: ProfilePoint[];
  best: { nu: number; pc: number; chi2: number };
  /** 1σ interval (Δχ² = 1 crossings); null when the profile never recovers to 1 */
  sigma: { lo: number | null; hi: number | null };
  /** reference (p_c, ν) at which the frozen window was taken */
  refUsed: { pc: number; nu: number; deposited: boolean };
}

/** Deposited reference values (Gullans–Huse locator, this workspace). */
export const DEPOSITED_REF = { pc: 0.1597, nu: 1.24 };

/** A frozen membership point: (L, p, y, w) fixed at the reference window. */
interface Member {
  L: number;
  p: number;
  y: number;
  w: number;
}

/**
 * Frozen membership + weights at a reference window, with an adaptive
 * fallback: if the deposited reference window captures too few points
 * (< 9) — e.g. a custom sweep grid centred far from p_c — fall back to a
 * coarse (p_c, ν) grid scan of the user's own data and freeze at its best.
 * Returns which reference was used so the UI can be honest about it.
 */
function frozenMembers(
  series: SeriesMap,
  sizes: number[],
  nTraj: number,
  ref: { pc: number; nu: number },
  xWin = 3
): { members: Member[]; refUsed: { pc: number; nu: number; deposited: boolean } } | null {
  const floor = 1 / Math.max(nTraj, 1);
  const collect = (pc: number, nu: number): Member[] => {
    const out: Member[] = [];
    for (const L of sizes)
      for (const pt of series[L] ?? []) {
        const xRef = (pt.p - pc) * Math.pow(L, 1 / nu);
        if (Math.abs(xRef) > xWin) continue;
        out.push({ L, p: pt.p, y: pt.mean, w: 1 / Math.max(pt.se, floor) ** 2 });
      }
    return out;
  };

  const deposited = ref.pc === DEPOSITED_REF.pc && ref.nu === DEPOSITED_REF.nu;
  let members = collect(ref.pc, ref.nu);
  if (members.length >= 9) return { members, refUsed: { pc: ref.pc, nu: ref.nu, deposited } };

  // adaptive fallback: coarse scan of the user's own data for a window centre
  let best = { pc: NaN, nu: NaN, chi2: Infinity };
  for (let pc = 0.14; pc <= 0.1801; pc += 0.002) {
    for (let nu = 0.9; nu <= 1.7001; nu += 0.05) {
      const f = collapseFit(series, sizes, pc, nu, nTraj, xWin);
      if (f && f.chi2 < best.chi2) best = { pc, nu, chi2: f.chi2 };
    }
  }
  if (!Number.isFinite(best.chi2)) return null;
  members = collect(best.pc, best.nu);
  if (members.length < 9) return null;
  return { members, refUsed: { pc: best.pc, nu: best.nu, deposited: false } };
}

/** χ² of the best weighted quartic through the frozen membership at (pc, ν). */
function memberChi2(members: Member[], pc: number, nu: number): { chi2: number; coeffs: number[] } | null {
  const pts = members.map((m) => ({
    x: (m.p - pc) * Math.pow(m.L, 1 / nu),
    y: m.y,
    w: m.w,
  }));
  const c = quarticFit(pts);
  if (!c) return null;
  let chi2 = 0;
  for (const pt of pts) {
    const yh = c[0] + c[1] * pt.x + c[2] * pt.x ** 2 + c[3] * pt.x ** 3 + c[4] * pt.x ** 4;
    chi2 += pt.w * (pt.y - yh) ** 2;
  }
  return { chi2, coeffs: c };
}

/** 1σ (Δχ² = 1) crossings around the minimum, by linear interpolation. */
function sigmaCrossings<T extends { dchi2: number }>(
  points: T[],
  bestIdx: number,
  at: (pt: T) => number
): { lo: number | null; hi: number | null } {
  const cross = (dir: 1 | -1): number | null => {
    for (let i = bestIdx; i > 0 && i < points.length - 1; i += dir) {
      const a = points[i];
      const b = points[i + dir];
      if (a.dchi2 <= 1 && b.dchi2 > 1) {
        const t = (1 - a.dchi2) / (b.dchi2 - a.dchi2);
        return at(a) + t * (at(b) - at(a));
      }
    }
    return null;
  };
  return { lo: cross(-1), hi: cross(1) };
}

/**
 * Frozen-ν Δχ² profile of the user's own sweep — the same construction the
 * paper used to quote ν = 1.24(7) and exclude ν = 1 at Δχ² ≥ 52.
 *
 * Comparability subtlety: the |x| ≤ 3 window membership depends on (p_c, ν),
 * so a naive per-parameter window lets fits with fewer points win spuriously.
 * Here the membership + weights are FROZEN at a reference window (deposited
 * values by default, scan-best on fallback) and only the coordinates
 * x = (p − p_c)·L^{1/ν} are recomputed — every ν is then scored on exactly
 * the same data, and the Δχ² = 1 crossings give a genuine 1σ interval on ν.
 */
export function dchi2Profile(
  series: SeriesMap,
  sizes: number[],
  nTraj: number,
  opts?: {
    ref?: { pc: number; nu: number };
    nuMin?: number;
    nuMax?: number;
    nuStep?: number;
    pcMin?: number;
    pcMax?: number;
  }
): Dchi2Profile | null {
  const ref = opts?.ref ?? { pc: DEPOSITED_REF.pc, nu: DEPOSITED_REF.nu };
  const nuMin = opts?.nuMin ?? 0.9;
  const nuMax = opts?.nuMax ?? 1.7;
  const nuStep = opts?.nuStep ?? 0.05;
  const pcMin = opts?.pcMin ?? 0.14;
  const pcMax = opts?.pcMax ?? 0.18;

  const frozen = frozenMembers(series, sizes, nTraj, ref);
  if (!frozen) return null;
  const { members, refUsed } = frozen;
  const wsum = members.reduce((a, m) => a + m.w, 0);

  const points: ProfilePoint[] = [];
  let best: ProfilePoint | null = null;
  const nSteps = Math.round((nuMax - nuMin) / nuStep);
  for (let i = 0; i <= nSteps; i++) {
    const nu = +(nuMin + i * nuStep).toFixed(4);
    let bestPc = NaN;
    let bestChi2 = Infinity;
    for (let pc = pcMin; pc <= pcMax + 1e-9; pc += 0.0005) {
      const r = memberChi2(members, pc, nu);
      if (r && r.chi2 < bestChi2) { bestChi2 = r.chi2; bestPc = pc; }
    }
    if (!Number.isFinite(bestChi2)) continue;
    const pt: ProfilePoint = { nu, chi2: bestChi2, dchi2: 0, bestPc, q: Math.sqrt(bestChi2 / wsum) };
    points.push(pt);
    if (!best || pt.chi2 < best.chi2) best = pt;
  }
  if (!best || points.length < 3) return null;
  for (const pt of points) pt.dchi2 = pt.chi2 - best.chi2;

  const sigma = sigmaCrossings(points, points.indexOf(best), (pt) => pt.nu);
  return {
    points,
    best: { nu: best.nu, pc: best.bestPc, chi2: best.chi2 },
    sigma,
    refUsed,
  };
}

export interface PcProfilePoint {
  pc: number;
  chi2: number;
  dchi2: number;
  /** argmin ν at this p_c (the re-optimised nuisance) */
  bestNu: number;
}

export interface Dchi2PcProfile {
  points: PcProfilePoint[];
  best: { pc: number; nu: number; chi2: number };
  sigma: { lo: number | null; hi: number | null };
  refUsed: { pc: number; nu: number; deposited: boolean };
}

/**
 * The p_c-side twin of {@link dchi2Profile}: at every p_c on a fine grid the
 * χ² is minimised over ν (nuisance re-optimised), giving a genuine profile
 * Δχ²(p_c) whose Δχ² = 1 crossings are a 1σ interval on p_c — symmetric to
 * how the paper brackets ν. Membership + weights stay frozen at the same
 * reference window as the ν profile, so both curves describe one fit.
 */
export function dchi2ProfilePc(
  series: SeriesMap,
  sizes: number[],
  nTraj: number,
  opts?: {
    ref?: { pc: number; nu: number };
    pcHalfWidth?: number;
    pcStep?: number;
    nuMin?: number;
    nuMax?: number;
    nuStep?: number;
  }
): Dchi2PcProfile | null {
  const ref = opts?.ref ?? { pc: DEPOSITED_REF.pc, nu: DEPOSITED_REF.nu };
  const halfWidth = opts?.pcHalfWidth ?? 0.012;
  const pcStep = opts?.pcStep ?? 0.0005;
  const nuMin = opts?.nuMin ?? 0.9;
  const nuMax = opts?.nuMax ?? 1.7;
  const nuStep = opts?.nuStep ?? 0.05;

  const frozen = frozenMembers(series, sizes, nTraj, ref);
  if (!frozen) return null;
  const { members, refUsed } = frozen;

  // locate the global (p_c, ν) minimum on the frozen membership first —
  // it is the profile minimum by construction (ν re-optimised at each p_c)
  let gBest = { pc: NaN, nu: NaN, chi2: Infinity };
  for (let pc = 0.14; pc <= 0.1801; pc += 0.0005) {
    for (let nu = nuMin; nu <= nuMax + 1e-9; nu += 0.05) {
      const r = memberChi2(members, pc, nu);
      if (r && r.chi2 < gBest.chi2) gBest = { pc, nu, chi2: r.chi2 };
    }
  }
  if (!Number.isFinite(gBest.chi2)) return null;

  // fine p_c grid centred on the global minimum, clamped to a sane range
  const lo = Math.max(0.13, gBest.pc - halfWidth);
  const hi = Math.min(0.19, gBest.pc + halfWidth);
  const points: PcProfilePoint[] = [];
  for (let pc = lo; pc <= hi + 1e-9; pc += pcStep) {
    const p = +pc.toFixed(5);
    let bestNu = NaN;
    let bestChi2 = Infinity;
    for (let nu = nuMin; nu <= nuMax + 1e-9; nu += nuStep) {
      const r = memberChi2(members, p, nu);
      if (r && r.chi2 < bestChi2) { bestChi2 = r.chi2; bestNu = nu; }
    }
    if (!Number.isFinite(bestChi2)) continue;
    points.push({ pc: p, chi2: bestChi2, dchi2: 0, bestNu: +bestNu.toFixed(3) });
  }
  if (points.length < 3) return null;
  for (const pt of points) pt.dchi2 = pt.chi2 - gBest.chi2;

  // best grid point (Δχ² = 0 sits at the global minimum)
  let bestPt = points[0];
  for (const pt of points) if (pt.chi2 < bestPt.chi2) bestPt = pt;
  const sigma = sigmaCrossings(points, points.indexOf(bestPt), (pt) => pt.pc);
  return {
    points,
    best: { pc: bestPt.pc, nu: bestPt.bestNu, chi2: bestPt.chi2 },
    sigma,
    refUsed,
  };
}

/** Evenly spaced grid, rounded to 4 decimals (for custom sweep ranges). */
export function pGrid(min: number, max: number, n: number): number[] {
  const out: number[] = [];
  for (let i = 0; i < n; i++) out.push(+(min + ((max - min) * i) / (n - 1)).toFixed(4));
  return out;
}

/* ────────────────────────────────────────────────────────────────────────────
 * Bootstrap of the Δχ² profiles (trajectory-level when available)
 * ──────────────────────────────────────────────────────────────────────── */

export interface ProfileBandPoint {
  v: number;
  /** 16th percentile of the resampled Δχ² at this grid value */
  lo: number;
  /** median of the resampled Δχ² at this grid value */
  med: number;
  /** 84th percentile of the resampled Δχ² at this grid value */
  hi: number;
}

export interface ProfileBootstrap {
  /** how the resamples were drawn: trajectories (non-parametric) or mean±se (parametric) */
  kind: "traj" | "parametric";
  /** usable resamples (those that produced a profile with ≥ 3 finite grid points) */
  B: number;
  /** 68% envelope + median of Δχ²(v) across resamples, on the main profile's grid */
  band: ProfileBandPoint[];
  /** central 68% of the per-resample profile minima — the bootstrap interval on the profiled parameter */
  min: { lo: number; med: number; hi: number };
  /** coarse histogram of the minima distribution (popover viz) */
  minHist: { v: number; count: number }[];
  /** fraction of resamples that yielded a usable profile */
  hitRate: number;
  /** fraction of usable resamples whose minimum started at a grid edge and was
   *  re-centred outward (strongly drifting resamples — no longer censored) */
  edgeRate: number;
}

/**
 * Bootstrap of a Δχ² profile (ν or p_c target) — a generator so the UI can
 * drive it in time-boxed chunks with a progress readout.
 *
 * Each resample redraws the frozen membership's y-values:
 *  - trajectory-level (preferred): per-L trajectory indices with replacement,
 *    the SAME indices across all p for a given L (paired-by-trajectory, the
 *    conservative block choice) — means AND standard errors recomputed from
 *    the resampled rows, weights from the recomputed s.e. with the same 1/N
 *    floor. This resamples the actual empirical distribution.
 *  - parametric (fallback): y ~ N(y, 1/√w) with the original weights kept.
 *
 * On every resample the full profile is recomputed on the SAME v-grid as the
 * main profile (nuisance re-optimised, inner scans at a slightly coarser
 * step for speed), giving
 *  (a) a 68% envelope + median of Δχ²(v) — how uncertain the curve itself is,
 *  (b) the distribution of per-resample minima — a bootstrap interval on ν̂
 *      or p̂_c that makes no Gaussian-shape assumption about the profile.
 */
export function* bootstrapProfileIter(
  target: "nu" | "pc",
  series: SeriesMap,
  sizes: number[],
  nTraj: number,
  main: { points: { v: number }[]; refUsed: { pc: number; nu: number } },
  traj?: Record<number, number[][]>,
  opts?: { B?: number; seed?: number; bins?: number }
): Generator<number, ProfileBootstrap | null, void> {
  const B = opts?.B ?? 120;
  const bins = opts?.bins ?? 26;
  const rng = mulberry32(opts?.seed ?? 20260920);
  const floor = 1 / Math.max(nTraj, 1);

  // rebuild the frozen membership at the SAME reference the main profile used
  const frozen = frozenMembers(series, sizes, nTraj, main.refUsed);
  if (!frozen) return null;
  const { members } = frozen;

  // attach per-trajectory rows to members (aligned by exact p match)
  const rowsOf = new Map<Member, number[]>();
  let usableTraj = traj != null;
  if (traj != null) {
    for (const m of members) {
      const idx = (series[m.L] ?? []).findIndex((q) => q.p === m.p);
      const row = idx >= 0 ? traj[m.L]?.[idx] : undefined;
      if (!Array.isArray(row) || row.length < 4) {
        usableTraj = false;
        break;
      }
      rowsOf.set(m, row);
    }
  }

  // group members by L (paired-by-trajectory draws reuse one index set per L)
  const byL = new Map<number, Member[]>();
  for (const m of members) {
    const g = byL.get(m.L);
    if (g) g.push(m);
    else byL.set(m.L, [m]);
  }

  const vGrid = main.points.map((p) => p.v);
  if (vGrid.length < 3) return null;
  const dchi2ByV: number[][] = vGrid.map(() => []);
  const minima: number[] = [];

  // adaptive re-centre bounds: resamples whose minimum piles at a grid edge are
  // rescanned OUTWARD (bounded to the analysis range) instead of being censored —
  // the Δχ² values stay on the main grid but are measured against the refined
  // global minimum, and the minima distribution spreads honestly beyond the edge
  const vLo = vGrid[0];
  const vHi = vGrid[vGrid.length - 1];
  const vStep = vGrid.length > 1 ? vGrid[1] - vGrid[0] : 0.05;
  const vAllowedMin = target === "pc" ? 0.13 : 0.8;
  const vAllowedMax = target === "pc" ? 0.19 : 1.8;
  let recentered = 0;

  // one resample's member values (same (L, p) membership, new y / w)
  const resampled: Member[] = members.map((m) => ({ L: m.L, p: m.p, y: m.y, w: m.w }));

  // inner (nuisance) scan: p_c at ν for the nu target, ν at p_c for the pc target
  const innerScan =
    target === "nu"
      ? (mem: Member[], nu: number): number => {
          let best = Infinity;
          for (let pc = 0.14; pc <= 0.1801; pc += 0.001) {
            const r = memberChi2(mem, pc, nu);
            if (r && r.chi2 < best) best = r.chi2;
          }
          return best;
        }
      : (mem: Member[], pc: number): number => {
          let best = Infinity;
          for (let nu = 0.9; nu <= 1.7001; nu += 0.05) {
            const r = memberChi2(mem, pc, nu);
            if (r && r.chi2 < best) best = r.chi2;
          }
          return best;
        };

  for (let b = 0; b < B; b++) {
    // ── draw the resample ──
    if (usableTraj) {
      const drawOf = new Map<number, number[]>();
      for (const [L, group] of byL) {
        const n = rowsOf.get(group[0])!.length;
        const draw: number[] = [];
        for (let j = 0; j < n; j++) draw.push(Math.floor(rng() * n));
        drawOf.set(L, draw);
      }
      for (let i = 0; i < members.length; i++) {
        const m = members[i];
        const row = rowsOf.get(m)!;
        const draw = drawOf.get(m.L)!;
        let s = 0;
        for (const k of draw) s += row[k];
        const mean = s / draw.length;
        let ss = 0;
        for (const k of draw) {
          const d = row[k] - mean;
          ss += d * d;
        }
        const se = draw.length > 1 ? Math.sqrt(ss / (draw.length - 1) / draw.length) : 0;
        resampled[i] = { L: m.L, p: m.p, y: mean, w: 1 / Math.max(se, floor) ** 2 };
      }
    } else {
      for (let i = 0; i < members.length; i++) {
        const m = members[i];
        const sigma = 1 / Math.sqrt(m.w); // the σ the weight actually encodes
        resampled[i] = { L: m.L, p: m.p, y: m.y + sigma * gauss(rng), w: m.w };
      }
    }

    // ── the resample's profile on the main grid ──
    let vmin = Infinity;
    let vstar = NaN;
    const chi2s: number[] = new Array(vGrid.length).fill(Infinity);
    for (let gi = 0; gi < vGrid.length; gi++) {
      const chi2 = innerScan(resampled, vGrid[gi]);
      chi2s[gi] = chi2;
      if (chi2 < vmin) {
        vmin = chi2;
        vstar = vGrid[gi];
      }
    }
    const finite = chi2s.filter(Number.isFinite).length;
    // ── adaptive re-centre: edge-piled minimum → rescan outward, bounded ──
    if (
      Number.isFinite(vstar) &&
      (Math.abs(vstar - vLo) < 1e-9 || Math.abs(vstar - vHi) < 1e-9)
    ) {
      const dir = Math.abs(vstar - vLo) < 1e-9 ? -1 : 1;
      let bestV = vstar;
      let bestC = vmin;
      for (let k = 1; k <= 12; k++) {
        const vTry = +(vstar + dir * k * vStep).toFixed(5);
        if (vTry < vAllowedMin || vTry > vAllowedMax) break;
        const c = innerScan(resampled, vTry);
        if (Number.isFinite(c) && c < bestC) {
          bestC = c;
          bestV = vTry;
        }
      }
      if (bestV !== vstar) recentered++;
      vmin = bestC;
      vstar = bestV;
    }
    if (finite >= 3 && Number.isFinite(vstar)) {
      for (let gi = 0; gi < vGrid.length; gi++) {
        if (Number.isFinite(chi2s[gi])) dchi2ByV[gi].push(chi2s[gi] - vmin);
      }
      minima.push(vstar);
    }
    yield b + 1;
  }

  // ── finalize percentiles ──
  const used = minima.length;
  if (used < Math.max(10, B * 0.25)) return null;
  const q = (arr: number[], f: number) => {
    const s = [...arr].sort((x, y) => x - y);
    return s[Math.min(s.length - 1, Math.floor(f * s.length))];
  };
  const band: ProfileBandPoint[] = [];
  for (let gi = 0; gi < vGrid.length; gi++) {
    const arr = dchi2ByV[gi];
    if (arr.length < Math.max(5, used * 0.25)) continue;
    band.push({ v: vGrid[gi], lo: q(arr, 0.16), med: q(arr, 0.5), hi: q(arr, 0.84) });
  }
  if (band.length < 3) return null;
  minima.sort((x, y) => x - y);
  const m0 = minima[0];
  const m1 = minima[minima.length - 1];
  const span = m1 - m0 || 1e-6;
  const counts = new Array(bins).fill(0);
  for (const v of minima) counts[Math.min(bins - 1, Math.floor(((v - m0) / span) * bins))]++;
  return {
    kind: usableTraj ? "traj" : "parametric",
    B: used,
    band,
    min: { lo: q(minima, 0.16), med: q(minima, 0.5), hi: q(minima, 0.84) },
    minHist: counts.map((count, i) => ({ v: m0 + ((i + 0.5) / bins) * span, count })),
    hitRate: used / B,
    edgeRate: used > 0 ? recentered / used : 0,
  };
}

/* ────────────────────────────────────────────────────────────────────────────
 * Pair-crossing bootstrap
 * ──────────────────────────────────────────────────────────────────────── */

/** Deterministic 32-bit RNG (mulberry32) so bootstrap results are reproducible. */
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Standard normal draw (Box–Muller) from a uniform RNG. */
function gauss(rng: () => number): number {
  let u = 0;
  let v = 0;
  while (u === 0) u = rng();
  while (v === 0) v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

/** Dominant (strongest) linear-interpolated crossing of two mean curves. */
export function dominantCrossing(
  a: { p: number; mean: number }[],
  b: { p: number; mean: number }[]
): { p: number; strength: number } | null {
  const bMap = new Map(b.map((q) => [q.p, q.mean]));
  const shared = a
    .filter((pt) => bMap.has(pt.p))
    .map((pt) => ({ p: pt.p, d: pt.mean - (bMap.get(pt.p) as number) }));
  if (shared.length < 2) return null;
  const cands: { p: number; strength: number }[] = [];
  for (let i = 0; i < shared.length - 1; i++) {
    const d0 = shared[i].d;
    const d1 = shared[i + 1].d;
    if (d0 === 0) cands.push({ p: shared[i].p, strength: 0 });
    if ((d0 < 0 && d1 > 0) || (d0 > 0 && d1 < 0)) {
      const t = d0 / (d0 - d1);
      cands.push({ p: shared[i].p + t * (shared[i + 1].p - shared[i].p), strength: Math.min(Math.abs(d0), Math.abs(d1)) });
    }
  }
  if (!cands.length) return null;
  return cands.reduce((best, c) => (c.strength > best.strength ? c : best));
}

export interface CrossingBootstrap {
  /** point estimate from the mean curves */
  point: number;
  /** median of the resampling distribution */
  median: number;
  /** 16th / 84th percentile — the central 68% */
  lo: number;
  hi: number;
  /** fraction of resamples in which a crossing was found at all */
  hitRate: number;
  /** coarse histogram of the resampling distribution (mini viz) */
  histogram: { p: number; count: number }[];
  /** how the resamples were drawn: trajectories (non-parametric) or mean±se (parametric) */
  kind: "traj" | "parametric";
  /** number of resamples actually drawn (usable ones — feeds the popover label) */
  B: number;
}

/**
 * Bootstrap of a pair crossing.
 *
 * Non-parametric (preferred): when per-trajectory values are available for
 * both curves (aligned with the p-grid), each resample redraws trajectory
 * indices with replacement — the SAME indices across all p for a given L
 * (paired by trajectory, the conservative block choice that preserves any
 * seed-stream correlation) — recomputes the two mean curves, and re-finds
 * the dominant crossing. This resamples the actual empirical distribution.
 *
 * Parametric (fallback): resample every grid point's mean from N(mean, se).
 *
 * In both cases the result is the median + central 68% of the crossing
 * distribution — the statistical error the crossing carries at the user's
 * trajectory count, the same ~1/√N shrinkage the deposited analysis quotes.
 */
export function bootstrapCrossing(
  a: SeriesPoint[],
  b: SeriesPoint[],
  opts?: { B?: number; seed?: number; bins?: number; trajA?: number[][]; trajB?: number[][] }
): CrossingBootstrap | null {
  const point = dominantCrossing(a, b);
  if (!point) return null;
  const B = opts?.B ?? 2000;
  const bins = opts?.bins ?? 24;
  const rng = mulberry32(opts?.seed ?? 20260613);
  const bMap = new Map(b.map((q) => [q.p, q]));
  const shared = a.filter((pt) => bMap.has(pt.p));
  if (shared.length < 2) return null;

  // ── non-parametric path: both curves carry per-trajectory values ──
  const trajA = opts?.trajA;
  const trajB = opts?.trajB;
  const usableTraj =
    !!trajA &&
    !!trajB &&
    trajA.length === a.length &&
    trajB.length === b.length &&
    shared.every((pt) => {
      const ai = a.indexOf(pt); // shared elements are references from a
      const bi = b.findIndex((q) => q.p === pt.p);
      return ai >= 0 && bi >= 0 && (trajA[ai]?.length ?? 0) >= 4 && (trajB[bi]?.length ?? 0) >= 4;
    });

  const samples: number[] = [];
  if (usableTraj) {
    const tA = trajA as number[][];
    const tB = trajB as number[][];
    // row of each shared p inside the two traj matrices (computed once)
    const aiOf = shared.map((pt) => a.indexOf(pt));
    const biOf = shared.map((pt) => b.findIndex((q) => q.p === pt.p));
    const nA = tA[aiOf[0]]?.length ?? 0;
    const nB = tB[biOf[0]]?.length ?? 0;
    const rowMean = (rows: number[][], row: number, idx: number[]) => {
      const r = rows[row];
      let s = 0;
      for (const k of idx) s += r[k];
      return s / idx.length;
    };
    for (let k = 0; k < B; k++) {
      // paired-by-trajectory indices: one draw per L, reused across all p
      const idxA: number[] = [];
      for (let j = 0; j < nA; j++) idxA.push(Math.floor(rng() * nA));
      const idxB: number[] = [];
      for (let j = 0; j < nB; j++) idxB.push(Math.floor(rng() * nB));
      const ra = shared.map((pt, i) => ({ p: pt.p, mean: rowMean(tA, aiOf[i], idxA) }));
      const rb = shared.map((pt, i) => ({ p: pt.p, mean: rowMean(tB, biOf[i], idxB) }));
      const c = dominantCrossing(ra, rb);
      if (c) samples.push(c.p);
    }
  } else {
    for (let k = 0; k < B; k++) {
      const ra = shared.map((pt) => ({ p: pt.p, mean: pt.mean + pt.se * gauss(rng) }));
      const rb = shared.map((pt) => {
        const q = bMap.get(pt.p) as SeriesPoint;
        return { p: pt.p, mean: q.mean + q.se * gauss(rng) };
      });
      const c = dominantCrossing(ra, rb);
      if (c) samples.push(c.p);
    }
  }
  // a crossing found in fewer than 25% of resamples is too weak to quantify
  if (samples.length < Math.max(20, B * 0.25)) return null;
  samples.sort((x, y) => x - y);
  const q = (f: number) => samples[Math.min(samples.length - 1, Math.floor(f * samples.length))];
  const hmin = samples[0];
  const hmax = samples[samples.length - 1];
  const span = hmax - hmin || 1e-6;
  const counts = new Array(bins).fill(0);
  for (const s of samples) counts[Math.min(bins - 1, Math.floor(((s - hmin) / span) * bins))]++;
  return {
    point: point.p,
    median: q(0.5),
    lo: q(0.16),
    hi: q(0.84),
    hitRate: samples.length / B,
    histogram: counts.map((count, i) => ({ p: hmin + ((i + 0.5) / bins) * span, count })),
    kind: usableTraj ? "traj" : "parametric",
    B: samples.length,
  };
}
