/** Offline validation: p_c-side Δχ² profile (ν re-optimised) + adaptive window fallback. */
import { runI3Sweep } from "../src/lib/quantum/clifford";
import { dchi2Profile, dchi2ProfilePc, collapseFit, type SeriesMap } from "../src/lib/stats/collapse";

const sizes = [8, 16, 32, 64];
const ps = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24];
const tau = 2;
const nTraj = 24;

const series: SeriesMap = {};
for (const L of sizes) {
  const r = runI3Sweep({ L, ps, nTraj, tau, seed0: 5000 + L * 977 });
  series[L] = r.points;
}

// --- 1. p_c profile on the standard wide grid (deposited window works) ---
const t0 = Date.now();
const prof = dchi2ProfilePc(series, sizes, nTraj);
const ms = Date.now() - t0;

if (!prof) {
  console.error("PC PROFILE FAILED (null) on the wide grid");
  process.exit(1);
}
console.log(`p_c profile computed in ${ms}ms over ${prof.points.length} p_c values`);
console.log(`window reference used: deposited=${prof.refUsed.deposited} (${prof.refUsed.pc}, ${prof.refUsed.nu})`);
console.log(`best: p_c = ${prof.best.pc.toFixed(4)}, ν = ${prof.best.nu.toFixed(2)}, χ²_min = ${prof.best.chi2.toFixed(2)}`);
console.log(`1σ interval: p_c ∈ [${prof.sigma.lo?.toFixed(4) ?? "—"}, ${prof.sigma.hi?.toFixed(4) ?? "—"}]`);

// consistency: the p_c profile minimum must agree with the ν profile's best p_c
const nuProf = dchi2Profile(series, sizes, nTraj);
if (nuProf) {
  const dp = Math.abs(nuProf.best.pc - prof.best.pc);
  console.log(`\nν-profile best (p_c, ν) = (${nuProf.best.pc.toFixed(4)}, ${nuProf.best.nu.toFixed(2)})`);
  console.log(`p_c-profile best (p_c, ν) = (${prof.best.pc.toFixed(4)}, ${prof.best.nu.toFixed(2)})`);
  console.log(`|Δp_c| = ${dp.toFixed(5)}, |Δχ²_min| = ${Math.abs(nuProf.best.chi2 - prof.best.chi2).toFixed(3)}`);
  console.log(dp < 0.002 ? "OK — both profiles share one global minimum" : "WARN — minima disagree");
}

// the interval must bracket the best and be non-degenerate
const w = (prof.sigma.lo != null ? prof.best.pc - prof.sigma.lo : 0) + (prof.sigma.hi != null ? prof.sigma.hi - prof.best.pc : 0);
console.log(`interval width ≈ ${w.toFixed(5)} (deposited: 0.0008)`);
console.log(w > 0.0008 ? "OK — small systems give a wider interval than the deposited 0.1597(8)" : "WARN — interval suspiciously tight");

// Δχ² must grow away from the minimum
const edge = Math.max(...prof.points.map((p) => Math.abs(p.pc - prof.best.pc)));
const edgePt = prof.points.reduce((m, p) => (Math.abs(p.pc - prof.best.pc) > Math.abs(m.pc - prof.best.pc) ? p : m));
console.log(`Δχ² at grid edge (|Δp_c| ≈ ${edge.toFixed(4)}): ${edgePt.dchi2.toFixed(2)}`);
console.log(edgePt.dchi2 > 4 ? "OK — edges strongly disfavoured" : "WARN — flat profile?");

// --- 2. adaptive fallback: large sizes + a grid far from the deposited window ---
// (small L have compressed x-ranges — their windows reach p ≈ 0.7, so the
// deposited window only starves when the larger sizes are far off-centre)
const farPs = [0.34, 0.36, 0.38, 0.4, 0.42, 0.44, 0.46];
const farSizes = [32, 64];
const farSeries: SeriesMap = {};
for (const L of farSizes) {
  const r = runI3Sweep({ L, ps: farPs, nTraj: 12, tau, seed0: 7000 + L * 131 });
  farSeries[L] = r.points;
}
const far = dchi2ProfilePc(farSeries, farSizes, 12);
console.log(`\nfar-centred grid (0.34–0.46, L = 32, 64): profile = ${far ? "computed" : "null (no fallback possible)"}`);
if (far) {
  console.log(`  refUsed: deposited=${far.refUsed.deposited} → (${far.refUsed.pc.toFixed(4)}, ${far.refUsed.nu.toFixed(2)})`);
  if (far.refUsed.deposited) console.log("  WARN — should have needed the fallback");
  else console.log("  OK — adaptive fallback engaged");
}
const farNu = dchi2Profile(farSeries, farSizes, 12);
console.log(`far-centred ν profile: ${farNu ? `refUsed deposited=${farNu.refUsed.deposited}` : "null"}`);

// sanity: fit at the p_c-profile best must beat the deposited fit
const qBest = collapseFit(series, sizes, prof.best.pc, prof.best.nu, nTraj);
const qDep = collapseFit(series, sizes, 0.1597, 1.24, nTraj);
if (qBest && qDep) {
  console.log(`\ntightness at profile best: ${qBest.q.toFixed(4)} vs deposited (0.1597, 1.24): ${qDep.q.toFixed(4)}`);
  console.log(qBest.q <= qDep.q ? "OK — profile best is tighter (or equal)" : "WARN — deposited is tighter?!");
}
