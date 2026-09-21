/** Offline validation: Δχ² frozen-ν profile on a real 4-size sweep. */
import { runI3Sweep } from "../src/lib/quantum/clifford";
import { dchi2Profile, collapseFit, type SeriesMap } from "../src/lib/stats/collapse";

const sizes = [8, 16, 32, 64];
const ps = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24];
const tau = 2;
const nTraj = 24;

const series: SeriesMap = {};
for (const L of sizes) {
  const r = runI3Sweep({ L, ps, nTraj, tau, seed0: 5000 + L * 977 });
  series[L] = r.points;
  console.log(`L=${L}: I3(p=0.16) = ${r.points.find(p => Math.abs(p.p - 0.16) < 1e-9)?.mean.toFixed(3)}`);
}

const t0 = Date.now();
const prof = dchi2Profile(series, sizes, nTraj);
const ms = Date.now() - t0;

if (!prof) {
  console.error("PROFILE FAILED (null)");
  process.exit(1);
}
console.log(`\nprofile computed in ${ms}ms over ${prof.points.length} ν values`);
console.log(`best: ν = ${prof.best.nu.toFixed(2)}, p_c = ${prof.best.pc.toFixed(4)}, χ²_min = ${prof.best.chi2.toFixed(2)}`);
console.log(`1σ interval: ν ∈ [${prof.sigma.lo?.toFixed(3) ?? "—"}, ${prof.sigma.hi?.toFixed(3) ?? "—"}]`);
const at1 = prof.points.find(d => Math.abs(d.nu - 1) < 1e-6);
console.log(`Δχ²(ν=1) = ${at1?.dchi2.toFixed(2)}`);
console.log(`Δχ²(ν=1.24 deposited) = ${prof.points.find(d => Math.abs(d.nu - 1.25) < 1e-6)?.dchi2.toFixed(2)}`);
console.log("\nprofile sample (ν, bestPc, Δχ²):");
for (const pt of prof.points.filter((_, i) => i % 2 === 0)) {
  console.log(`  ν=${pt.nu.toFixed(2)}  p_c=${pt.bestPc.toFixed(4)}  Δχ²=${pt.dchi2.toFixed(2)}`);
}

// sanity: fit at the profile best must beat fit at deposited values
const qBest = collapseFit(series, sizes, prof.best.pc, prof.best.nu, nTraj);
const qDep = collapseFit(series, sizes, 0.1597, 1.24, nTraj);
if (qBest && qDep) {
  console.log(`\ntightness at profile best: ${qBest.q.toFixed(4)} vs deposited (0.1597, 1.24): ${qDep.q.toFixed(4)}`);
  console.log(qBest.q <= qDep.q ? "OK — profile best is tighter (or equal)" : "WARN — deposited is tighter?!");
}
