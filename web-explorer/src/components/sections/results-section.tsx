"use client";

import { Trophy, Ban, Scale, GitFork } from "lucide-react";
import { COMPARISON, HEADLINE } from "@/lib/research-data";
import { SectionHeading } from "./section-heading";

export function ResultsSection() {
  return (
    <section id="results" className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading num="04" id="results" kicker="Results" title={<>One transition, two independent locators, exact bookends</>}>
          The I₃ locator and the purification locator agree within combined errors — and use disjoint
          trajectory data. The annealed sector is exactly solvable and sits at a different point:
          the quenched transition is genuinely non-perturbative in the measurement noise.
        </SectionHeading>

        <div className="mt-10 overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-900/40">
          <table className="w-full text-sm min-w-[560px]">
            <thead>
              <tr className="text-left text-[11px] font-mono uppercase tracking-wider text-zinc-500 border-b border-zinc-800">
                <th className="px-5 py-3 font-medium">source</th>
                <th className="px-5 py-3 font-medium">p_c</th>
                <th className="px-5 py-3 font-medium">ν</th>
                <th className="px-5 py-3 font-medium hidden md:table-cell">note</th>
              </tr>
            </thead>
            <tbody>
              {COMPARISON.map((r, i) => (
                <tr
                  key={r.source}
                  className={`border-b border-zinc-800/60 last:border-0 ${
                    i < 2 ? "bg-emerald-500/[0.03]" : ""
                  }`}
                >
                  <td className={`px-5 py-3.5 ${i < 2 ? "text-zinc-100 font-medium" : "text-zinc-400"}`}>
                    {r.source}
                  </td>
                  <td className="px-5 py-3.5 font-mono text-amber-300/90 tabular-nums">{r.pc}</td>
                  <td className="px-5 py-3.5 font-mono text-emerald-300/90 tabular-nums">{r.nu}</td>
                  <td className="px-5 py-3.5 text-zinc-500 hidden md:table-cell">{r.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-6 grid md:grid-cols-3 gap-4">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 min-w-0">
            <Ban className="size-5 text-rose-400" />
            <h3 className="mt-3 text-sm font-semibold text-zinc-100">ν = 1 is excluded</h3>
            <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
              Fixed-point-set frozen-ν comparisons: Δχ² = 52–334 for the I₃ locator, 544 for the
              purification locator at τ = 1. The entanglement transition is not a first-order or
              log-divergence phenomenon.
            </p>
          </div>
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 min-w-0">
            <Scale className="size-5 text-amber-400" />
            <h3 className="mt-3 text-sm font-semibold text-zinc-100">4/3 disfavoured, not excluded</h3>
            <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
              The percolation value sits Δχ² ≥ 3 above the minimum in every tail-safe variant
              (≥ 20 without a correction term) — disfavoured, honestly stated as such rather than
              claimed excluded. The v13 &ldquo;1.3σ&rdquo; wording was withdrawn in the audit.
            </p>
          </div>
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 min-w-0">
            <GitFork className="size-5 text-teal-400" />
            <h3 className="mt-3 text-sm font-semibold text-zinc-100">The independence gate</h3>
            <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
              All I₃/entropy locators share the same 475,600 trajectories — stated openly. The one
              independent observable is the purification protocol: disjoint seeds, mixed initial
              state, reference-qubit order parameter. It lands at{" "}
              <span className="font-mono text-teal-300">{HEADLINE.pcPurif}</span>.
            </p>
          </div>
        </div>

        <div className="mt-6 rounded-xl border border-emerald-500/20 bg-emerald-500/[0.04] p-5 sm:p-6 flex gap-4">
          <Trophy className="size-6 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <h3 className="text-sm font-semibold text-emerald-200">What survived three audit rounds</h3>
            <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
              p_c = <span className="font-mono text-zinc-200">0.1597(8)</span> and{" "}
              ν = <span className="font-mono text-zinc-200">1.24(7)</span> stand. What changed in v14 was the{" "}
              <em>justification</em>: the 10⁻⁴ error-floor defect that let one saturated point carry 98% of a fit&rsquo;s
              weight was found, disclosed, and fixed (floors → 1/N; spline scaling functions); the sextic-through-tail
              artefact that pushed ν to 1.30–1.35 was root-caused and withdrawn; the Jensen misattribution was replaced
              by the exact p_R² tilt mechanism. Every exact statement — the rank theorems, the Collatz–Wielandt
              enclosures, the Houtappel benchmark — is untouched.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
