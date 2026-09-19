import { runI3Sweep } from "../src/lib/quantum/clifford";
import { bootstrapCrossing } from "../src/lib/stats/collapse";

// L=8 and L=16 sweeps with per-trajectory data
const ps = [0.08, 0.12, 0.14, 0.16, 0.18, 0.2, 0.24];
const a = runI3Sweep({ L: 8, ps, nTraj: 48, tau: 1, seed0: 5000 + 8 * 977 });
const b = runI3Sweep({ L: 16, ps, nTraj: 48, tau: 1, seed0: 5000 + 16 * 977 });

// 1. trajectory-level bootstrap (non-parametric)
const t0 = Date.now();
const trajBoot = bootstrapCrossing(a.points, b.points, { B: 2000, seed: 42, trajA: a.traj, trajB: b.traj });
const trajMs = Date.now() - t0;

// 2. parametric bootstrap on the same curves
const p0 = Date.now();
const parBoot = bootstrapCrossing(a.points, b.points, { B: 2000, seed: 42 });
const parMs = Date.now() - p0;

// 3. fallback: traj data mismatched length → parametric
const badBoot = bootstrapCrossing(a.points, b.points, { B: 200, seed: 42, trajA: a.traj, trajB: (b.traj ?? []).slice(0, 3) });

// 4. statistics sanity: resampling trajectory values reproduces the actual se
const meanOf = (arr: number[]) => arr.reduce((x, y) => x + y, 0) / arr.length;
const seOf = (arr: number[]) => {
  const m = meanOf(arr);
  return Math.sqrt(arr.reduce((s, v) => s + (v - m) * (v - m), 0) / (arr.length - 1) / arr.length);
};
const piCritical = ps.findIndex((p) => Math.abs(p - 0.16) < 1e-9);
const actualSeA = seOf(a.traj![piCritical]);
const actualMeanA = meanOf(a.traj![piCritical]);

console.log("traj bootstrap:", JSON.stringify({
  kind: trajBoot?.kind,
  point: trajBoot?.point.toFixed(4),
  median: trajBoot?.median.toFixed(4),
  lo: trajBoot?.lo.toFixed(4),
  hi: trajBoot?.hi.toFixed(4),
  hitRate: trajBoot?.hitRate,
  ms: trajMs,
}));
console.log("param bootstrap:", JSON.stringify({
  kind: parBoot?.kind,
  point: parBoot?.point.toFixed(4),
  lo: parBoot?.lo.toFixed(4),
  hi: parBoot?.hi.toFixed(4),
  ms: parMs,
}));
console.log("fallback (mismatched):", badBoot?.kind);
console.log("sanity: mean@0.16 A =", actualMeanA.toFixed(3), "vs points", a.points[piCritical].mean.toFixed(3),
  "| se", actualSeA.toFixed(4), "vs points", a.points[piCritical].se.toFixed(4));

const ok =
  trajBoot?.kind === "traj" &&
  parBoot?.kind === "parametric" &&
  badBoot?.kind === "parametric" &&
  Math.abs(actualMeanA - a.points[piCritical].mean) < 1e-12 &&
  Math.abs(actualSeA - a.points[piCritical].se) < 1e-12;
console.log(ok ? "ALL CHECKS PASS" : "CHECKS FAILED");
