/** Benchmark: how expensive are larger-L I₃ sweeps? (inform API caps + UI size options) */
import { runI3Sweep } from "../src/lib/quantum/clifford";

const ps = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24];

for (const [L, nTraj, tau] of [
  [32, 24, 2],
  [64, 16, 2],
  [64, 24, 2],
  [128, 8, 2],
  [128, 16, 2],
] as const) {
  const t0 = Date.now();
  runI3Sweep({ L, ps, nTraj, tau, seed0: 5000 + L * 977 });
  console.log(`L=${L} nTraj=${nTraj} tau=${tau}: ${Date.now() - t0}ms`);
}
