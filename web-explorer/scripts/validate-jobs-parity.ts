import { runI3Sweep, sweepPointI3 } from "../src/lib/quantum/clifford";

// parity: point-wise computation must equal the batch sweep exactly
const ps = [0.12, 0.14, 0.16, 0.18, 0.2];
for (const { L, nTraj, tau } of [
  { L: 128, nTraj: 8, tau: 1 },
  { L: 256, nTraj: 4, tau: 1 },
]) {
  const batch = runI3Sweep({ L, ps, nTraj, tau, seed0: 5000 + L * 977 });
  let mismatch = 0;
  for (let pi = 0; pi < ps.length; pi++) {
    const pt = sweepPointI3({ L, p: ps[pi], nTraj, tau, seed0: 5000 + L * 977, psIndex: pi, psCount: ps.length });
    const ref = batch.points[pi];
    if (pt.p !== ref.p || pt.mean !== ref.mean || pt.se !== ref.se) {
      mismatch++;
      console.log(`  MISMATCH p=${ps[pi]}: point (${pt.mean}, ${pt.se}) vs batch (${ref.mean}, ${ref.se})`);
    }
  }
  console.log(`L=${L} n=${nTraj} tau=${tau}: ${mismatch === 0 ? "PARITY OK — bit-identical" : mismatch + " mismatches"}`);
  console.log(`  I3 curve: ${batch.points.map(p => p.mean.toFixed(3)).join("  ")}`);
}
