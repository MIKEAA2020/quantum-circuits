/** Validate the I₃ collapse-scan: does the grid search find a sensible (p_c, ν)? */
import { runI3Sweep } from "../src/lib/quantum/clifford";
import type { I3SeriesPoint } from "../src/components/charts/i3-sweep-chart";

const P_GRID = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24];

function collapseQuality(
  series: Record<number, I3SeriesPoint[]>,
  sizes: number[],
  pc: number,
  nu: number,
  nTraj: number,
  xWin = 3
): number {
  const floor = 1 / Math.max(nTraj, 1);
  const pts: { x: number; y: number; w: number }[] = [];
  for (const L of sizes)
    for (const pt of series[L] ?? []) {
      const x = (pt.p - pc) * Math.pow(L, 1 / nu);
      if (Math.abs(x) > xWin) continue;
      pts.push({ x, y: pt.mean, w: 1 / Math.max(pt.se, floor) ** 2 });
    }
  const K = 5;
  if (pts.length < K + 4) return NaN;
  const A: number[][] = Array.from({ length: K }, () => new Array(K).fill(0));
  const b: number[] = new Array(K).fill(0);
  let wsum = 0;
  for (const pt of pts) {
    const pw = [1, pt.x, pt.x * pt.x, pt.x ** 3, pt.x ** 4];
    for (let i = 0; i < K; i++) {
      for (let j = 0; j < K; j++) A[i][j] += pt.w * pw[i] * pw[j];
      b[i] += pt.w * pw[i] * pt.y;
    }
    wsum += pt.w;
  }
  const M = A.map((row, i) => [...row, b[i]]);
  for (let col = 0; col < K; col++) {
    let piv = col;
    for (let r = col + 1; r < K; r++) if (Math.abs(M[r][col]) > Math.abs(M[piv][col])) piv = r;
    [M[col], M[piv]] = [M[piv], M[col]];
    if (Math.abs(M[col][col]) < 1e-12) return NaN;
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
  let chi2 = 0;
  for (const pt of pts) {
    const yh = c[0] + c[1] * pt.x + c[2] * pt.x ** 2 + c[3] * pt.x ** 3 + c[4] * pt.x ** 4;
    chi2 += pt.w * (pt.y - yh) ** 2;
  }
  return Math.sqrt(chi2 / wsum);
}

const nTraj = 24;
const tau = 2;
const sizes = [8, 16, 32];
const series: Record<number, I3SeriesPoint[]> = {};
for (const L of sizes) {
  const res = runI3Sweep({ L, ps: P_GRID, nTraj, tau, seed0: 5000 + L * 977 });
  series[L] = res.points;
}

// grid scan
let best = { pc: NaN, nu: NaN, q: Infinity };
const t0 = Date.now();
for (let pcTry = 0.14; pcTry <= 0.1801; pcTry += 0.0005) {
  for (let nuTry = 0.9; nuTry <= 1.7001; nuTry += 0.02) {
    const q = collapseQuality(series, sizes, pcTry, nuTry, nTraj);
    if (Number.isFinite(q) && q < best.q) best = { pc: pcTry, nu: nuTry, q };
  }
}
console.log(`scan (${Date.now() - t0}ms): best collapse at p_c = ${best.pc.toFixed(4)}, ν = ${best.nu.toFixed(2)}, quality = ${best.q.toFixed(4)}`);
console.log(`quality at deposited (0.1597, 1.24): ${collapseQuality(series, sizes, 0.1597, 1.24, nTraj).toFixed(4)}`);
console.log(`quality at ν=1 (p_c=0.1597):     ${collapseQuality(series, sizes, 0.1597, 1.0, nTraj).toFixed(4)}`);
console.log(`quality at (0.10, 1.5) far off:   ${collapseQuality(series, sizes, 0.10, 1.5, nTraj).toFixed(4)}`);
