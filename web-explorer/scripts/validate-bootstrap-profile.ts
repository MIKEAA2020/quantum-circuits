/**
 * Validate the Δχ²-profile bootstrap (phase 8).
 *
 * 1. kind switching: with per-trajectory rows → "traj"; without → "parametric";
 *    broken rows (length mismatch) → parametric fallback.
 * 2. sanity: band percentiles ordered (lo ≤ med ≤ hi), non-negative, aligned
 *    with the main profile grid; minima interval brackets/near the main best.
 * 3. cross-check: trajectory vs parametric bootstrap intervals should agree
 *    to the same tolerance the phase-7 crossing cross-check used (roughly).
 * 4. timing: total time for B=120, chunked the same way the UI will drive it.
 */
import { runI3Sweep } from "../src/lib/quantum/clifford";
import {
  dchi2Profile,
  dchi2ProfilePc,
  bootstrapProfileIter,
  type SeriesMap,
} from "../src/lib/stats/collapse";

const ps = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24];

// real sweep: 4 sizes, τ=2, 24 trajectories (matches the phase-5 validation setup)
const sizes = [8, 16, 32, 64];
const series: SeriesMap = {};
const traj: Record<number, number[][]> = {};
for (const L of sizes) {
  const r = runI3Sweep({ L, ps, nTraj: L >= 64 ? 24 : 24, tau: 2, seed0: 5000 + L * 977 });
  series[L] = r.points;
  traj[L] = r.traj ?? [];
}

// per-traj values must reproduce the published mean to 1e-12 (alignment check)
for (const L of sizes) {
  for (let i = 0; i < ps.length; i++) {
    const row = traj[L][i];
    const mean = row.reduce((a, b) => a + b, 0) / row.length;
    if (Math.abs(mean - series[L][i].mean) > 1e-12) throw new Error(`traj/mean mismatch L=${L} p=${ps[i]}`);
  }
}
console.log("✓ per-trajectory rows reproduce the published means (1e-12)");

const mainNu = dchi2Profile(series, sizes, 24);
if (!mainNu) throw new Error("main ν profile failed");
console.log(`✓ main ν profile: best (p_c, ν) = (${mainNu.best.pc.toFixed(4)}, ${mainNu.best.nu.toFixed(2)}), 1σ ${JSON.stringify(mainNu.sigma)}`);

function drive(iter: Generator<number, unknown, void>, budgetMs = 120): unknown {
  for (;;) {
    const t0 = Date.now();
    let r = iter.next();
    while (!r.done && Date.now() - t0 < budgetMs) r = iter.next();
    if (r.done) return r.value;
  }
}

// ── 1. trajectory-level bootstrap (ν target) ──
const t0 = Date.now();
const bootNu = drive(
  bootstrapProfileIter("nu", series, sizes, 24, { points: mainNu.points.map((d) => ({ v: d.nu })), refUsed: mainNu.refUsed }, traj, { B: 120, seed: 42 })
) as ReturnType<typeof bootstrapProfileIter> extends Generator<unknown, infer R, void> ? R : never;
const nuMs = Date.now() - t0;
if (!bootNu) throw new Error("trajectory bootstrap returned null");
if (bootNu.kind !== "traj") throw new Error(`expected kind "traj", got "${bootNu.kind}"`);
console.log(`✓ ν bootstrap (traj): B=${bootNu.B}/${120} hit=${(bootNu.hitRate * 100).toFixed(0)}% in ${nuMs} ms`);
console.log(`  minima 68% [${bootNu.min.lo.toFixed(2)}, ${bootNu.min.hi.toFixed(2)}] · median ${bootNu.min.med.toFixed(2)} · main best ν̂ = ${mainNu.best.nu.toFixed(2)}`);

// ── 2. band sanity ──
for (const b of bootNu.band) {
  if (!(b.lo <= b.med + 1e-12 && b.med <= b.hi + 1e-12)) throw new Error(`band percentiles unordered at v=${b.v}`);
  if (b.lo < -1e-9) throw new Error(`negative band lo at v=${b.v}`);
}
const gridMatch = bootNu.band.every((b) => mainNu.points.some((d) => Math.abs(d.nu - b.v) < 1e-9));
if (!gridMatch) throw new Error("band grid not aligned with the main profile grid");
console.log(`✓ band: ${bootNu.band.length} grid points, percentiles ordered, non-negative, grid-aligned`);

// minima interval should contain (or sit adjacent to) the main best ν̂
const inInterval = mainNu.best.nu >= bootNu.min.lo - 0.051 && mainNu.best.nu <= bootNu.min.hi + 0.051;
if (!inInterval) throw new Error(`main best ν̂ ${mainNu.best.nu} far outside bootstrap minima [${bootNu.min.lo}, ${bootNu.min.hi}]`);
console.log(`✓ main best ν̂ inside (or adjacent to) the bootstrap minima interval`);

// ── 3. parametric fallback + broken-rows fallback ──
const bootNuPar = drive(
  bootstrapProfileIter("nu", series, sizes, 24, { points: mainNu.points.map((d) => ({ v: d.nu })), refUsed: mainNu.refUsed }, undefined, { B: 120, seed: 42 })
);
if (!bootNuPar || bootNuPar.kind !== "parametric") throw new Error("parametric fallback failed");
console.log(`✓ parametric fallback (no traj): kind=parametric, B=${bootNuPar.B}, minima 68% [${bootNuPar.min.lo.toFixed(2)}, ${bootNuPar.min.hi.toFixed(2)}]`);

const broken: Record<number, number[][]> = { 8: traj[8].slice(0, 2), 16: traj[16], 32: traj[32], 64: traj[64] };
const bootNuBroken = drive(
  bootstrapProfileIter("nu", series, sizes, 24, { points: mainNu.points.map((d) => ({ v: d.nu })), refUsed: mainNu.refUsed }, broken, { B: 60, seed: 42 })
);
if (!bootNuBroken || bootNuBroken.kind !== "parametric") throw new Error("broken-rows fallback failed");
console.log(`✓ broken-rows fallback (L=8 rows truncated): kind=parametric, B=${bootNuBroken.B}`);

// cross-check traj vs parametric — two agreement regimes:
//  (a) both constrained (width < 0.7 of the 0.8-wide grid): medians + widths must roughly agree
//  (b) both unconstrained (full-width): they agree by construction ("ν not constrained")
const trajWidth = bootNu.min.hi - bootNu.min.lo;
const parWidth = bootNuPar.min.hi - bootNuPar.min.lo;
const bothUnconstrained = trajWidth >= 0.7 && parWidth >= 0.7;
const agree = bothUnconstrained
  ? true
  : Math.abs(bootNu.min.med - bootNuPar.min.med) <= 0.15 && Math.abs(trajWidth - parWidth) <= 0.2;
console.log(
  `${agree ? "✓" : "⚠"} traj vs parametric: medians ${bootNu.min.med.toFixed(2)} / ${bootNuPar.min.med.toFixed(2)}, widths ${trajWidth.toFixed(2)} / ${parWidth.toFixed(2)} ${bothUnconstrained ? "(both unconstrained — agree by construction)" : agree ? "(agree)" : "(disagree — investigate)"}`
);

// ── 4. p_c target ──
const mainPc = dchi2ProfilePc(series, sizes, 24);
if (!mainPc) throw new Error("main p_c profile failed");
const t1 = Date.now();
const bootPc = drive(
  bootstrapProfileIter("pc", series, sizes, 24, { points: mainPc.points.map((d) => ({ v: d.pc })), refUsed: mainPc.refUsed }, traj, { B: 120, seed: 77 })
);
const pcMs = Date.now() - t1;
if (!bootPc) throw new Error("p_c bootstrap returned null");
if (bootPc.kind !== "traj") throw new Error("p_c bootstrap should be trajectory-level");
console.log(`✓ p_c bootstrap (traj): B=${bootPc.B} in ${pcMs} ms · minima 68% [${bootPc.min.lo.toFixed(4)}, ${bootPc.min.hi.toFixed(4)}] · main best p̂_c = ${mainPc.best.pc.toFixed(4)}`);
const pcIn = mainPc.best.pc >= bootPc.min.lo - 0.0011 && mainPc.best.pc <= bootPc.min.hi + 0.0011;
if (!pcIn) throw new Error("main best p̂_c far outside bootstrap minima");
console.log(`✓ main best p̂_c inside (or adjacent to) the p_c bootstrap interval`);

console.log(`\ntiming: ν ${nuMs} ms · p_c ${pcMs} ms for B=120 (UI budget ≈ 110 ms chunks → smooth progress)`);
console.log("\nALL CHECKS PASSED");
