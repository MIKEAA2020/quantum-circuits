/** Benchmark τ=4 sweeps to set API trajectory caps (phase 8). */
import { runI3Sweep } from "../src/lib/quantum/clifford";

const ps = [0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28];

const cases: { L: number; nTraj: number; tau: number }[] = [
  { L: 8, nTraj: 64, tau: 4 },
  { L: 16, nTraj: 64, tau: 4 },
  { L: 16, nTraj: 32, tau: 4 },
  { L: 32, nTraj: 32, tau: 4 },
  { L: 32, nTraj: 16, tau: 4 },
  { L: 64, nTraj: 24, tau: 4 },
  { L: 64, nTraj: 12, tau: 4 },
];

for (const { L, nTraj, tau } of cases) {
  const t0 = Date.now();
  const r = runI3Sweep({ L, ps, nTraj, tau, seed0: 5000 + L * 977 });
  console.log(
    `L=${String(L).padStart(3)} tau=${tau} nTraj=${String(nTraj).padStart(2)} ` +
      `→ ${String(Date.now() - t0).padStart(5)} ms  (engine ${r.elapsedMs} ms, ` +
      `I3(p=0.16) = ${r.points[2].mean.toFixed(3)}±${r.points[2].se.toFixed(3)})`
  );
}
