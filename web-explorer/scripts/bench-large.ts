import { runI3Sweep } from "../src/lib/quantum/clifford";

const grid = [0.12, 0.14, 0.16, 0.18, 0.20];
for (const nTraj of [4, 8]) {
  const t0 = Date.now();
  const r = runI3Sweep({ L: 128, ps: grid, nTraj, tau: 1, seed0: 5000 + 128 * 977 });
  console.log(`L=128 n=${nTraj} tau=1 pts=5: ${Date.now() - t0}ms, I3@0.16 = ${r.points.find(p => Math.abs(p.p - 0.16) < 1e-9)?.mean.toFixed(3)}`);
}
