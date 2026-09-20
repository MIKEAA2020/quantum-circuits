"use client";

import { KeyRound, FileStack, ScrollText, ShieldAlert } from "lucide-react";
import { HEADLINE, REPRO } from "@/lib/research-data";
import { SectionHeading } from "./section-heading";

export function ReproSection() {
  return (
    <section id="repro" className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading num="07" id="repro" kicker="Reproducibility" title={<>Bit-exact by contract, honest by design</>} />

        <div className="mt-10 grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <KeyRound className="size-4 text-amber-400" />
              The seed contract
            </div>
            <p className="mt-3 text-sm text-zinc-400 leading-relaxed">{REPRO.seedContract}</p>
            <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-950/70 px-4 py-3 font-mono text-xs text-zinc-400 [overflow-wrap:anywhere]">
              trajectory k of file (L, p){" "}
              <span className="text-zinc-600">≡</span> MT19937(seed0(L, p) + k)
              <br />
              purification seeds <span className="text-zinc-600">=</span> pure-state blocks + 500,000,000{" "}
              <span className="text-zinc-600"># disjoint</span>
            </div>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <FileStack className="size-4 text-emerald-400" />
              Dataset inventory
            </div>
            <table className="mt-3 w-full text-sm font-mono">
              <tbody className="divide-y divide-zinc-800/70">
                <tr>
                  <td className="py-2.5 pr-4 text-zinc-500">I₃ locator</td>
                  <td className="py-2.5 text-zinc-200 tabular-nums">
                    {HEADLINE.trajectoriesI3.toLocaleString()} trajectories · {HEADLINE.sizesI3} · t = 2L, 4L
                  </td>
                </tr>
                <tr>
                  <td className="py-2.5 pr-4 text-zinc-500">purification</td>
                  <td className="py-2.5 text-zinc-200 tabular-nums">
                    {HEADLINE.trajectoriesPurif.toLocaleString()} trajectories · {HEADLINE.purifFiles} files ·{" "}
                    {HEADLINE.sizesPurif}
                  </td>
                </tr>
                <tr>
                  <td className="py-2.5 pr-4 text-zinc-500">p grid</td>
                  <td className="py-2.5 text-zinc-300">{REPRO.pGrid}</td>
                </tr>
                <tr>
                  <td className="py-2.5 pr-4 text-zinc-500">τ grid</td>
                  <td className="py-2.5 text-zinc-300">{REPRO.tauGrid}</td>
                </tr>
                <tr>
                  <td className="py-2.5 pr-4 text-zinc-500">samples / (L, p)</td>
                  <td className="py-2.5 text-zinc-300 tabular-nums">
                    {REPRO.purifSpec.map((s) => `L${s.L}: ${s.n.toLocaleString()}`).join(" · ")}
                  </td>
                </tr>
                <tr>
                  <td className="py-2.5 pr-4 text-zinc-500">file format</td>
                  <td className="py-2.5 text-zinc-300 [overflow-wrap:anywhere]">purif_L{"{L}"}_p{"{p:.4f}"}_c{"{chunk}"}.npz</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-amber-500/25 bg-amber-500/[0.04] p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-amber-200">
              <ShieldAlert className="size-4 text-amber-400" />
              The disclosed weighting defect
            </div>
            <p className="mt-3 text-sm text-zinc-400 leading-relaxed">
              A 10⁻⁴ standard-error floor let one point with I₃ ≡ 0 across all 800 trajectories (L = 384,
              p = 0.18) carry 98% of a fit&rsquo;s weight, and a sextic polynomial forced through the saturated
              area-law tail tilted the collapse core — together pushing ν to 1.30–1.35. Root cause found,
              disclosed, fixed: floors raised to 1/N_traj, tail handled by spline scaling functions or
              exclusion. The tail-safe envelope is ν = 1.21–1.29; the headline 1.24(7) covers it.
            </p>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <ScrollText className="size-4 text-teal-400" />
              Versioning &amp; audit trail
            </div>
            <p className="mt-3 text-sm text-zinc-400 leading-relaxed [overflow-wrap:anywhere]">
              The manuscript progressed v13 → v14 under three external audit rounds (10 remaining points,
              all adjudicated; none requiring a change to any theorem, proof, or exact number). Every
              analysis step is a versioned script with a JSON result and a log:{" "}
              <span className="font-mono text-zinc-300 text-xs">
                mipt_purif_sim.py → mipt_data_purif/*.npz → mipt_purif_analysis.py → purif_summary.json
              </span>
              . Bootstrap resamples, floor definitions, and window choices are all stated in the deposited
              report — the numbers on this page trace back to those files.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
