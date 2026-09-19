"use client";

import { useMemo, useState } from "react";
import { Database, SlidersHorizontal, BarChart3, RotateCcw, Sparkles } from "lucide-react";
import { PURIF_DATA, I3_DCHI2, BOOTSTRAP } from "@/lib/research-data";
import { SectionHeading } from "./section-heading";
import { Corners } from "./i3-sweep-panel";
import { PurifChart } from "@/components/charts/purif-chart";
import { CollapseChart } from "@/components/charts/collapse-chart";
import { Dchi2Chart } from "@/components/charts/dchi2-chart";

const BEST_FITS: Record<number, { pc: number; nu: number }> = {
  0.25: { pc: 0.16191, nu: 1.2808 },
  0.5: { pc: 0.16039, nu: 1.251 },
  1: { pc: 0.16009, nu: 1.2486 },
  2: { pc: 0.15977, nu: 1.2071 },
  4: { pc: 0.16041, nu: 1.3346 },
};

/**
 * Live "collapse quality": weighted quartic fit of y = F(x) over a fixed
 * |x| <= 3 window (the paper's own approach). Returns sqrt(chi2 / sum w) —
 * lower = tighter collapse.
 */
function collapseQuality(
  series: Record<number, { p: number; mean: number; se: number }[]>,
  sizes: number[],
  pc: number,
  nu: number,
  xWin = 3
): number {
  const pts: { x: number; y: number; w: number }[] = [];
  for (const L of sizes)
    for (const pt of series[L] ?? []) {
      const x = (pt.p - pc) * Math.pow(L, 1 / nu);
      if (Math.abs(x) > xWin) continue;
      pts.push({ x, y: pt.mean, w: 1 / Math.max(pt.se, 0.004) ** 2 });
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

export function FssSection() {
  const [tau, setTau] = useState(1);
  const slice = PURIF_DATA.find((s) => s.tau === tau)!;
  const best = BEST_FITS[tau];

  const [pc, setPc] = useState(0.16009);
  const [nu, setNu] = useState(1.2486);
  const [showPc, setShowPc] = useState(true);

  const quality = useMemo(
    () => collapseQuality(slice.series, slice.sizes, pc, nu),
    [slice, pc, nu]
  );
  const bestQuality = useMemo(
    () => collapseQuality(slice.series, slice.sizes, best.pc, best.nu),
    [slice, best]
  );
  const qNorm = quality / (bestQuality || 1);

  const selectTau = (t: number) => {
    setTau(t);
    const b = BEST_FITS[t];
    setPc(b.pc);
    setNu(b.nu);
  };

  return (
    <section id="data" className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading num="03" id="data" kicker="Data & finite-size scaling" title={<>The deposited purification dataset, in full</>}>
          135,000 trajectories · 270 chunk files · L = 16–256 · p = 0.140–0.180 · τ = t/L ∈ {"{0.25, 0.5, 1, 2, 4}"}.
          Every point below is quoted verbatim from the analysis log — error bars are one standard error of the mean.
          Tune the collapse by hand and watch the curves fuse at the published (p_c, ν).
        </SectionHeading>

        {/* tau tabs */}
        <div className="mt-8 flex flex-wrap items-center gap-2" role="tablist" aria-label="Select tau slice">
          {PURIF_DATA.map((s) => (
            <button
              key={s.tau}
              role="tab"
              aria-selected={tau === s.tau}
              onClick={() => selectTau(s.tau)}
              className={`rounded-lg border px-3.5 py-1.5 font-mono text-sm transition-colors ${
                tau === s.tau
                  ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300"
                  : "border-zinc-700 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200"
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>

        <div className="mt-6 grid gap-6 xl:grid-cols-2">
          {/* raw curves */}
          <div className="relative group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-5 min-w-0 chart-well">
            <Corners />
            <div className="flex items-center justify-between gap-3 mb-2">
              <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-zinc-500">
                <Database className="size-3.5 text-emerald-500/80" />
                ⟨S_ref⟩ vs p — raw data
              </div>
              <label className="flex items-center gap-1.5 text-xs text-zinc-500 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showPc}
                  onChange={(e) => setShowPc(e.target.checked)}
                  className="accent-amber-500"
                />
                p_c line
              </label>
            </div>
            <PurifChart series={slice.series} sizes={slice.sizes} showPc={showPc} height={330} />
            <div className="mt-3 grid gap-2 text-xs text-zinc-500">
              <div>
                <span className="text-zinc-300 font-medium">Pair crossings:</span>{" "}
                <span className="font-mono">{slice.crossings}</span>
              </div>
              <div>
                <span className="text-zinc-300 font-medium">Collapse fit:</span>{" "}
                <span className="font-mono">
                  p_c = {slice.collapse.pc.toFixed(5)}, ν = {slice.collapse.nu.toFixed(4)} (χ² = {slice.collapse.chi2})
                </span>
                {slice.collapse.note && <span className="text-zinc-600"> — {slice.collapse.note}</span>}
              </div>
            </div>
          </div>

          {/* interactive collapse */}
          <div className="relative group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-5 min-w-0 chart-well">
            <Corners />
            <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-zinc-500 mb-2">
              <SlidersHorizontal className="size-3.5 text-amber-500/80" />
              collapse — drag the exponents
            </div>
            <CollapseChart series={slice.series} sizes={slice.sizes} pc={pc} nu={nu} height={330} />

            <div className="mt-4 grid sm:grid-cols-2 gap-x-6 gap-y-4">
              <div>
                <div className="flex justify-between text-xs font-mono text-zinc-500">
                  <span>p_c</span>
                  <span className="text-amber-400">{pc.toFixed(4)}</span>
                </div>
                <input
                  type="range"
                  min={0.155}
                  max={0.166}
                  step={0.0002}
                  value={pc}
                  onChange={(e) => setPc(Number(e.target.value))}
                  className="mt-1.5 w-full accent-amber-500"
                  aria-label="Critical point p_c"
                />
              </div>
              <div>
                <div className="flex justify-between text-xs font-mono text-zinc-500">
                  <span>ν</span>
                  <span className="text-emerald-400">{nu.toFixed(3)}</span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={1.6}
                  step={0.005}
                  value={nu}
                  onChange={(e) => setNu(Number(e.target.value))}
                  className="mt-1.5 w-full accent-emerald-500"
                  aria-label="Exponent nu"
                />
              </div>
            </div>

            <div className="mt-4 flex flex-wrap items-center gap-3">
              <div className="flex-1 min-w-[180px]">
                <div className="flex justify-between text-[11px] font-mono text-zinc-500 mb-1">
                  <span>collapse tightness (fuller = better)</span>
                  <span className={qNorm <= 1.08 ? "text-emerald-400" : qNorm <= 1.4 ? "text-amber-400" : "text-rose-400"}>
                    {qNorm <= 1.08 ? "at the published minimum" : `${(qNorm * 100).toFixed(0)}% of best-fit scatter`}
                  </span>
                </div>
                <div className="h-1.5 rounded-full bg-zinc-800 overflow-hidden" role="progressbar" aria-valuenow={Math.round(Math.min(100, 100 / qNorm))} aria-valuemin={0} aria-valuemax={100}>
                  <div
                    className={`h-full rounded-full transition-all duration-300 ${
                      qNorm <= 1.08 ? "bg-emerald-500" : qNorm <= 1.4 ? "bg-amber-500" : "bg-rose-500"
                    }`}
                    style={{ width: `${Math.min(100, Math.max(4, 100 / qNorm))}%` }}
                  />
                </div>
              </div>
              <button
                onClick={() => { setPc(best.pc); setNu(best.nu); }}
                className="inline-flex items-center gap-1.5 rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-300 hover:bg-emerald-500/20 transition-colors"
              >
                <Sparkles className="size-3.5" />
                best fit ({best.pc.toFixed(4)}, {best.nu.toFixed(2)})
              </button>
              <button
                onClick={() => { setPc(0.1597); setNu(1.24); }}
                className="inline-flex items-center gap-1.5 rounded-lg border border-zinc-700 px-3 py-1.5 text-xs font-medium text-zinc-400 hover:border-zinc-500 transition-colors"
              >
                <RotateCcw className="size-3.5" />
                v14 headline
              </button>
            </div>
          </div>
        </div>

        {/* Δχ² profile + bootstrap */}
        <div className="mt-6 grid gap-6 xl:grid-cols-2">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-5 min-w-0">
            <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-zinc-500 mb-2">
              <BarChart3 className="size-3.5 text-rose-400/80" />
              frozen-ν Δχ² profile — purification, τ = 1, L ≥ 64
            </div>
            {slice.dchi2 ? (
              <Dchi2Chart data={slice.dchi2} height={250} />
            ) : (
              <Dchi2Chart data={I3_DCHI2} height={250} />
            )}
            <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
              Fixed point sets, so Δχ² is meaningful. ν = 1 is excluded outright; the percolation
              value 4/3 sits Δχ² ≥ 3 above the minimum in every tail-safe variant. The same profile
              for the I₃ locator gives Δχ²(ν = 1) = 52–334.
            </p>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-5 min-w-0">
            <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-zinc-500 mb-3">
              <Sparkles className="size-3.5 text-emerald-500/80" />
              bootstrap over trajectories (n = 100)
            </div>
            <table className="w-full text-sm font-mono">
              <thead>
                <tr className="text-zinc-500 text-left text-[11px] uppercase tracking-wider">
                  <th className="py-2 font-medium">τ</th>
                  <th className="py-2 font-medium">L_min</th>
                  <th className="py-2 font-medium">p_c</th>
                  <th className="py-2 font-medium">ν</th>
                </tr>
              </thead>
              <tbody>
                {BOOTSTRAP.purif.map((b, i) => (
                  <tr key={i} className="border-t border-zinc-800">
                    <td className="py-2 text-zinc-300">{b.tau}</td>
                    <td className="py-2 text-zinc-300">{b.Lmin}</td>
                    <td className="py-2 text-amber-300/90">{b.pc}</td>
                    <td className="py-2 text-emerald-300/90">{b.nu}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
              Statistical errors are small (±0.0001 on p_c); the honest uncertainty is systematic —
              the τ/L_min spread. Hence the adopted ν = 1.25(2)_stat(6)_sys for the purification
              locator, quoted separately from the I₃ headline.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
