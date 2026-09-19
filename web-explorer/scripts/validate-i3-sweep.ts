/** Validate the I₃ sweep: curves must go negative at small p, ~0 at large p, crossing near p_c. */
import { runI3Sweep } from "../src/lib/quantum/clifford";

const ps = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24];

function pairCrossing(a: { p: number; mean: number }[], b: { p: number; mean: number }[]): number | null {
  const shared = a.map((pt) => ({ p: pt.p, d: pt.mean - (b.find((q) => q.p === pt.p)?.mean ?? NaN) })).filter((x) => Number.isFinite(x.d));
  const cands: { p: number; strength: number }[] = [];
  for (let i = 0; i < shared.length - 1; i++) {
    const d0 = shared[i].d, d1 = shared[i + 1].d;
    if ((d0 < 0 && d1 > 0) || (d0 > 0 && d1 < 0)) {
      const t = d0 / (d0 - d1);
      cands.push({ p: shared[i].p + t * (shared[i + 1].p - shared[i].p), strength: Math.min(Math.abs(d0), Math.abs(d1)) });
    }
  }
  if (!cands.length) return null;
  return cands.reduce((best, c) => (c.strength > best.strength ? c : best)).p;
}

for (const L of [8, 16, 32]) {
  const t0 = Date.now();
  const res = runI3Sweep({ L, ps, nTraj: 24, tau: 2, seed0: 5000 + L * 977 });
  console.log(`\nL=${L}  (${Date.now() - t0}ms)  nTraj=24  tau=2`);
  console.log("  p    : " + ps.map((p) => p.toFixed(2)).join("  "));
  console.log("  I3   : " + res.points.map((pt) => (pt.mean >= 0 ? " " : "") + pt.mean.toFixed(2)).join("  "));
  console.log("  ±se  : " + res.points.map((pt) => pt.se.toFixed(2)).join("  "));
}

// crossings
const r8 = runI3Sweep({ L: 8, ps, nTraj: 48, tau: 2, seed0: 5000 + 8 * 977 });
const r16 = runI3Sweep({ L: 16, ps, nTraj: 48, tau: 2, seed0: 5000 + 16 * 977 });
const r32 = runI3Sweep({ L: 32, ps, nTraj: 48, tau: 2, seed0: 5000 + 32 * 977 });
console.log("\ncrossings (nTraj=48):");
console.log("  L=8×16  →", pairCrossing(r8.points, r16.points)?.toFixed(4));
console.log("  L=16×32 →", pairCrossing(r16.points, r32.points)?.toFixed(4));
console.log("  deposited p_c = 0.1597(8)");
