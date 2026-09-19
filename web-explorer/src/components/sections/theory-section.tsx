"use client";

import { Infinity as InfinityIcon, ShieldCheck, ArrowRight } from "lucide-react";
import { ANNEALED, CERTIFICATES, TILT_CHAIN } from "@/lib/research-data";
import { SectionHeading } from "./section-heading";

function Formula({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950/70 px-4 py-3 font-mono text-[13px] leading-relaxed text-zinc-300 overflow-x-auto">
      {children}
    </div>
  );
}

export function TheorySection() {
  return (
    <section id="theory" className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading num="05" id="theory" kicker="Exact theory" title={<>The annealed sector is exactly solvable</>}>
          Averaging the two-replica (n = 2) partition function over the measurement record turns the
          Clifford circuit into a solvable vertex model — the Houtappel 8-vertex / triangular-lattice
          Ising class. Its critical line is closed-form, and the compressed period map has a
          numerically-certified free-fermion spectrum.
        </SectionHeading>

        <div className="mt-10 grid lg:grid-cols-2 gap-6">
          {/* annealed critical line */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <InfinityIcon className="size-4 text-emerald-400" />
              Annealed critical line p_c⁽²⁾(d)
            </div>
            <div className="mt-4 space-y-3">
              <Formula>
                <span className="text-zinc-500">β_d =</span> (d²−1)/(d²+1){" "}
                <span className="text-zinc-600">·</span> θ_c = β_d + √(β_d²+1)
              </Formula>
              <Formula>
                <span className="text-amber-400">p_c⁽²⁾(d) = (d − θ_c)/(d − 1)</span>
              </Formula>
              <table className="w-full text-sm font-mono">
                <thead>
                  <tr className="text-left text-[11px] uppercase tracking-wider text-zinc-500">
                    <th className="py-1.5 font-medium">local dimension d</th>
                    <th className="py-1.5 font-medium">p_c⁽²⁾(d)</th>
                  </tr>
                </thead>
                <tbody>
                  {ANNEALED.pc2.map((r) => (
                    <tr key={r.d} className="border-t border-zinc-800">
                      <td className="py-2 text-zinc-300">{r.d}</td>
                      <td className="py-2 text-amber-300/90 tabular-nums">{r.pc2.toFixed(5)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p className="text-xs text-zinc-500 leading-relaxed">
                For the Clifford circuit (d = 2): p_c⁽²⁾ = 0.23381 — strictly above the quenched p_c =
                0.1597. The gap is real physics, not finite-size drift: at p = 0.22 the quenched chain is
                already in its area-law phase while the annealed model is still ordered.
              </p>
            </div>
          </div>

          {/* closed-form spectrum */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <ShieldCheck className="size-4 text-teal-400" />
              Closed-form spectrum of the compressed period map
            </div>
            <div className="mt-4 space-y-3">
              <Formula>
                Q(k) = cosh²2K_d cosh 2K_h + sinh²2K_d sinh 2K_h − sinh 2K_h cos k
              </Formula>
              <Formula>
                R(k) = 2 sinh 2K_d cos(k/2){" "}
                <span className="text-zinc-600">·</span> w_k^± = Q(k) ± √(Q(k)² − R(k)²)
              </Formula>
              <Formula>
                <span className="text-emerald-400">λ = (2W₀²)^m ∏_{"{"}k ∈ K_σ{"}"} w_k^±</span>
              </Formula>
              <p className="text-xs text-zinc-500 leading-relaxed">
                Every nonzero eigenvalue of C = E D_h Eᵀ D_h is a free-fermion product over momentum modes:
                antiperiodic set K₊ = {"{(2j−1)π/m}"}, periodic K₋ = {"{2πj/m}"}, with the parity rule flipping
                at p_c⁽²⁾ exactly as in Kaufman&rsquo;s Ising treatment. Verified to |Δlog λ| ≤ 10⁻¹⁰ for all
                eigenvalues at L ≤ 18, λ₁ to 3 × 10⁻¹⁴ at L = 32, and inside every exact enclosure below — a
                numerically-certified conjecture presented as a Proposition with proof in v14.
              </p>
            </div>
          </div>
        </div>

        {/* certificates */}
        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6">
          <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
            <ShieldCheck className="size-4 text-emerald-400" />
            Collatz–Wielandt enclosures of λ₁ — exact rational arithmetic (Level-B certificates)
          </div>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-xs font-mono min-w-[640px]">
              <thead>
                <tr className="text-left text-[10px] uppercase tracking-wider text-zinc-500 border-b border-zinc-800">
                  <th className="py-2 pr-4 font-medium">L</th>
                  <th className="py-2 pr-4 font-medium">d</th>
                  <th className="py-2 pr-4 font-medium">p</th>
                  <th className="py-2 pr-4 font-medium">λ₁ enclosure [lo, hi]</th>
                  <th className="py-2 font-medium">rel. width</th>
                </tr>
              </thead>
              <tbody>
                {CERTIFICATES.map((c, i) => (
                  <tr key={i} className="border-b border-zinc-800/60 last:border-0 hover:bg-zinc-800/20">
                    <td className="py-2.5 pr-4 text-zinc-300">{c.L}</td>
                    <td className="py-2.5 pr-4 text-zinc-300">{c.d}</td>
                    <td className="py-2.5 pr-4 text-amber-300/80">{c.p}</td>
                    <td className="py-2.5 pr-4 text-emerald-300/90 break-all">
                      [{c.lo}, {c.hi}]
                    </td>
                    <td className="py-2.5 text-zinc-500">{c.rel}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
            Positive matrix + Collatz–Wielandt + exact arithmetic on the rational matrix of the period map:
            these are theorems, not simulations. They certify the &ldquo;agrees with Houtappel to 3 × 10⁻⁷&rdquo;
            benchmark statement at these points.
          </p>
        </div>

        {/* tilt chain */}
        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6">
          <div className="text-sm font-semibold text-zinc-100">
            Why the annealed quasi-entropy exceeds the quenched mean — the p_R² tilt, exactly
          </div>
          <p className="mt-2 text-sm text-zinc-400">
            For stabilizer states tr ρ_A² = 2^(−S_A), so the annealed average is a tilted expectation with
            weight ∝ p_R² (record-collision weight) — a measure that favours records with{" "}
            <em>fewer</em> measurements. At L = 8, t = 4, p = 0.16 (40,000 Born trajectories, ESS 5935):
          </p>
          <div className="mt-5 flex flex-col sm:flex-row items-stretch gap-2 sm:gap-0">
            {TILT_CHAIN.steps.map((s, i) => (
              <div key={s.label} className="flex items-center gap-2 sm:flex-1">
                <div className="flex-1 rounded-lg border border-zinc-700 bg-zinc-950/70 px-4 py-3 text-center">
                  <div className="font-mono text-lg text-zinc-100 tabular-nums">{s.value.toFixed(3)}</div>
                  <div className="mt-0.5 text-[10px] font-mono text-zinc-500">{s.label}</div>
                  <div className="text-[10px] text-zinc-600">{s.note}</div>
                </div>
                {i < TILT_CHAIN.steps.length - 1 && (
                  <ArrowRight className="size-4 text-zinc-600 shrink-0 hidden sm:block" />
                )}
              </div>
            ))}
          </div>
          <p className="mt-4 text-xs text-zinc-500 leading-relaxed">
            The record-collision weight lowers the effective measurement density to p_eff = p + p(1−p)∂_p log λ₁/(2L):
            0.1049 at L = 8, 0.0920 in the thermodynamic limit (p = 0.16). The tilt gain (+0.41 bits) dominates
            the Jensen loss (−0.27 bits); ≈80% of the gain is the density shift alone. The v13 attribution to
            &ldquo;(Jensen)&rdquo; pointed the wrong way and was corrected in the audit.
          </p>
        </div>
      </div>
    </section>
  );
}
