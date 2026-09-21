"use client";

import { Sigma, ShieldCheck, Scale, Activity, Waves, Cpu, ArrowRight } from "lucide-react";
import { RECORD_SCGF } from "@/lib/research-data";
import { SectionHeading } from "./section-heading";

function Formula({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950/70 px-4 py-3 font-mono text-[13px] leading-relaxed text-zinc-300 overflow-x-auto">
      {children}
    </div>
  );
}

const fmt = (v: number | null, digits = 5) =>
  v === null ? "—" : v.toFixed(digits);

export function RecordScgfSection() {
  const ladder = RECORD_SCGF.ladder;
  return (
    <section
      id="record-scgf"
      className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900"
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading
          num="07"
          id="record-scgf"
          kicker="Record SCGF · v16 data, v21 framing"
          title={
            <>
              The record SCGF — the disorder direction
            </>
          }
        >
          Every measurement outcome of a stabilizer circuit is either
          deterministic or a fair coin, so the Born probability of a whole
          trajectory is exactly dyadic — P(R) = 2^(−X_R) with X_R the count of
          random outcomes. The disorder-direction SCGF of the record count,
          Λ_L(β) = ln E_Born[2^(−βX_R)]/(2Lt), is the annealed record moment
          family at fractional order q = 1 + β: its β = 1 endpoint{" "}
          <em>is</em> exactly the annealed collision Z̄₂ (the two-replica
          transfer matrix), its β = 0 derivative <em>is</em> the quenched
          record-entropy density (the sampled side).
        </SectionHeading>

        <div className="mt-10 grid lg:grid-cols-2 gap-6">
          {/* the SCGF definition + exact endpoints */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <Sigma className="size-4 text-emerald-400" />
              The record SCGF and its two exact endpoints
            </div>
            <div className="mt-4 space-y-3">
              <Formula>
                P(R) = 2^(−X_R){" "}
                <span className="text-zinc-600">·</span>{" "}
                <span className="text-zinc-500">X_R = # random outcomes</span>
              </Formula>
              <Formula>
                <span className="text-emerald-400">Λ_L(β)</span> =
                ln&nbsp;E_Born[2^(−βX_R)] / (2Lt)
                <span className="text-zinc-600"> · </span>
                <span className="text-zinc-500">Ξ_L(β) in the v16 notation</span>
              </Formula>
              <Formula>
                <span className="text-amber-400">Λ_L(1) = ln Z̄₂(t)/(2Lt)</span>{" "}
                <span className="text-zinc-500">— the annealed collision, exactly</span>
              </Formula>
              <div className="flex flex-col sm:flex-row items-stretch gap-2">
                <div className="flex-1 rounded-lg border border-zinc-700 bg-zinc-950/70 px-4 py-3 text-center">
                  <div className="font-mono text-sm text-zinc-500">β = 0</div>
                  <div className="font-mono text-base text-zinc-100 tabular-nums">
                    Λ&prime;(0) = −ln2 · x̄
                  </div>
                  <div className="text-[10px] text-zinc-600 mt-1">
                    quenched record-entropy density → 0.1489 bits/site (p = 0.16)
                  </div>
                </div>
                <ArrowRight className="size-4 text-zinc-600 shrink-0 hidden sm:block self-center" />
                <div className="flex-1 rounded-lg border border-zinc-700 bg-zinc-950/70 px-4 py-3 text-center">
                  <div className="font-mono text-sm text-zinc-500">β = 1</div>
                  <div className="font-mono text-base text-amber-300 tabular-nums">
                    Λ(1) = ½(ln W₀ + f_H)
                  </div>
                  <div className="text-[10px] text-zinc-600 mt-1">
                    Houtappel limit: −0.08101 nats/site (p = 0.16)
                  </div>
                </div>
              </div>
              <p className="text-xs text-zinc-500 leading-relaxed">
                Z̄₂(t) = A(L)·λ₁^t with A(L) = 2.4512 / 4.2354 / 7.2288 at
                L = 8/12/16 — subexponential in t, constant to six digits for
                t ≳ 3L — so the β = 1 anchor is certified at every L by the
                closed-form λ₁ ladder and the Collatz–Wielandt enclosures
                above.
              </p>
            </div>
          </div>

          {/* the L-ladder table */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <ShieldCheck className="size-4 text-teal-400" />
              Thermodynamic limit — the exact β = 1 anchors (p = 0.16, τ = 4)
            </div>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-xs font-mono min-w-[520px]">
                <thead>
                  <tr className="text-left text-[10px] uppercase tracking-wider text-zinc-500 border-b border-zinc-800">
                    <th className="py-2 pr-3 font-medium">L</th>
                    <th className="py-2 pr-3 font-medium">x̄ (bits/site)</th>
                    <th className="py-2 pr-3 font-medium">Λ(1) exact</th>
                    <th className="py-2 pr-3 font-medium">Var(X)/2Lt</th>
                    <th className="py-2 pr-3 font-medium">gap g</th>
                    <th className="py-2 font-medium">ESS</th>
                  </tr>
                </thead>
                <tbody>
                  {ladder.map((r) => (
                    <tr
                      key={r.L}
                      className="border-b border-zinc-800/60 last:border-0 hover:bg-zinc-800/20"
                    >
                      <td className="py-2.5 pr-3 text-zinc-300">{r.L}</td>
                      <td className="py-2.5 pr-3 text-zinc-200 tabular-nums">
                        {fmt(r.xbar)}
                      </td>
                      <td className="py-2.5 pr-3 text-amber-300/90 tabular-nums">
                        {r.xi1Exact.toFixed(6)}
                      </td>
                      <td className="py-2.5 pr-3 text-zinc-400 tabular-nums">
                        {fmt(r.varPerSite, 4)}
                      </td>
                      <td className="py-2.5 pr-3 text-emerald-300/90 tabular-nums">
                        {fmt(r.gap, 4)}
                      </td>
                      <td className="py-2.5 text-zinc-500 tabular-nums">
                        {r.ess === null
                          ? "—"
                          : `${r.ess.toFixed(r.ess < 4 ? 1 : 0)} / ${(
                              r.essB / 1000
                            ).toFixed(0)}k`}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
              x̄ → 0.1489 bits/site (0.1971 at p = 0.22); Λ(1) → the
              closed-form Houtappel limit ½(ln W₀ + f_H) = −0.08101 nats/site
              at p = 0.16 (−0.11082 at p = 0.22) — λ₁ ladder: −0.07974 →
              −0.08101 for L = 8 → 32. Var(X)/(2Lt) = 0.105 at{" "}
              <em>every</em> L — the per-site variance is L-independent, so
              the density self-averages like a sum of weakly-correlated bits
              (the LDP backbone). The annealed–quenched record gap{" "}
              <span className="text-emerald-300/90 font-mono">
                g = Λ(1) + ln2·x̄ = {RECORD_SCGF.gapValue}
              </span>{" "}
              nats/site is L-independent — the record analogue of the
              annealed/quenched transition-point separation.
            </p>
            <p className="mt-2 text-[11px] text-zinc-600 leading-relaxed">
              Λ(1) column: exact β = 1 anchor — finite-t 3^L evolution at
              L ≤ 16; amplitude-corrected λ₁ at L = 24 (A(24) ≈ 21.4);
              λ₁-asymptotic at L = 32.
            </p>
          </div>
        </div>

        {/* the reframed theorem cards */}
        <div className="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 min-w-0">
            <div className="flex items-center gap-2 text-[13px] font-semibold text-zinc-100">
              <Scale className="size-4 text-emerald-400" />
              Trajectory-trivial, disorder-nontrivial
            </div>
            <p className="mt-2 text-xs text-zinc-400 leading-relaxed">
              For a fixed Clifford circuit the record surprisal is
              deterministic — the unsigned stabilizer group evolves
              identically on every branch, so{" "}
              <span className="font-mono text-zinc-300">
                P(R) = 2^(−N_rand(ω))
              </span>{" "}
              for every positive-probability record; all nontrivial record
              statistics live in the disorder direction.
            </p>
          </div>
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 min-w-0">
            <div className="flex items-center gap-2 text-[13px] font-semibold text-zinc-100">
              <Activity className="size-4 text-teal-400" />
              Self-averaging — verified
            </div>
            <p className="mt-2 text-xs text-zinc-400 leading-relaxed">
              Var<sub>ω</sub>(X)/(2Lt) = 0.105 (p = 0.16; 0.124–0.125 at
              p = 0.22), L-independent for L = 8–24 — the measurable
              self-averaging criterion of the manuscript&rsquo;s replica
              interpolation identity, verified. The annealed–quenched record
              gap g = Λ(1) + ln2·x̄ = 0.0226(2) nats/site is L-independent
              (0.027 at p = 0.22); the leading Gaussian cumulant 0.0252
              overestimates g by ≈13% (sub-Gaussian tail).
            </p>
          </div>
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 min-w-0">
            <div className="flex items-center gap-2 text-[13px] font-semibold text-zinc-100">
              <Cpu className="size-4 text-violet-300" />
              Complexity trichotomy
            </div>
            <p className="mt-2 text-xs text-zinc-400 leading-relaxed">
              Clifford realization — poly-time by Gottesman–Knill; any exact
              2-design — the β = 1 annealed endpoint coincides with Haar;
              Haar realization — average-case-hard (conditional on standard
              conjectures). Complements the worst-case PP-hardness result.
            </p>
          </div>
        </div>

        {/* collision-tilt ESS + calibration */}
        <div className="mt-6 grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <Waves className="size-4 text-teal-400" />
              Collision-tilt ESS — estimator difficulty, not a transition
            </div>
            <div className="mt-4 space-y-3">
              <Formula>
                <span className="text-teal-300">ESS/B</span> = exp[−2Lt·(Λ(2) −
                2Λ(1))]{" "}
                <span className="text-zinc-500">— exact law</span>
              </Formula>
              <div className="flex flex-wrap gap-2">
                {RECORD_SCGF.essExponent.map((e) => (
                  <span
                    key={e.L}
                    className="rounded-full border border-zinc-700/80 bg-zinc-950/60 px-2.5 py-1 font-mono text-[11px] text-zinc-400"
                  >
                    L={e.L} ·{" "}
                    <span className="text-teal-300/90 tabular-nums">
                      {e.exponent.toFixed(4)}
                    </span>{" "}
                    nats/site
                  </span>
                ))}
              </div>
              {ladder
                .filter((r) => r.ess !== null)
                .map((r) => {
                  const frac = (r.ess ?? 0) / r.essB;
                  const w = Math.max(1.5, -Math.log10(Math.max(frac, 1e-9)) * 9);
                  return (
                    <div key={r.L} className="flex items-center gap-3">
                      <div className="w-10 shrink-0 font-mono text-xs text-zinc-500">
                        L={r.L}
                      </div>
                      <div className="flex-1 h-5 rounded bg-zinc-950/70 border border-zinc-800 overflow-hidden" role="img" aria-label={`ESS ${r.ess} out of ${r.essB} trajectories at L = ${r.L}`}>
                        <div
                          className="h-full bg-gradient-to-r from-teal-500/70 to-teal-300/70"
                          style={{ width: `${Math.min(w, 100)}%` }}
                          aria-hidden
                        />
                      </div>
                      <div className="w-36 shrink-0 text-right font-mono text-[11px] text-zinc-400 tabular-nums">
                        ESS {r.ess!.toFixed(r.ess! < 4 ? 1 : 0)} /{" "}
                        {(r.essB / 1000).toFixed(0)}k
                      </div>
                    </div>
                  );
                })}
              <p className="text-xs text-zinc-500 leading-relaxed">
                ESS collapses to 11.7 / 3.9 / 1.4 / 1.0 out of 40k / 40k /
                30k / 15k trajectories (τ = 4, p = 0.16) — any fixed budget
                fails exponentially in system size. This is estimator
                difficulty (the manuscript&rsquo;s clone-collapse clause),
                <em> not</em> a thermodynamic transition: the no-freeze
                theorem classifies the Clifford family as the degenerate
                zero-variance case, and the collapse measures extremal
                domination of the annealed endpoint by an atypical minority
                of circuits (tilted density 0.097 vs typical 0.145 at L = 8).
              </p>
              <p className="text-xs text-zinc-500 leading-relaxed">
                Λ(2) is itself exactly the n = 3 annealed replica moment Z̄₃ —{" "}
                <a
                  href="#replica"
                  className="text-emerald-400/90 hover:text-emerald-300 underline decoration-dotted underline-offset-2 whitespace-nowrap"
                >
                  cf. the Replica-ladder section
                </a>
                : the same Z̄₂ anchor and the n = 3 operator.
              </p>
            </div>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <ShieldCheck className="size-4 text-emerald-400" />
              Calibration — the exact evolution vs the deposited chain
            </div>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-[11px] font-mono min-w-[560px]">
                <thead>
                  <tr className="text-left text-[10px] uppercase tracking-wider text-zinc-500 border-b border-zinc-800">
                    <th className="py-2 pr-3 font-medium">quantity</th>
                    <th className="py-2 pr-3 font-medium">L=8, t=4</th>
                    <th className="py-2 pr-3 font-medium">deposit</th>
                    <th className="py-2 pr-3 font-medium">L=12, t=6</th>
                    <th className="py-2 font-medium">deposit</th>
                  </tr>
                </thead>
                <tbody>
                  {RECORD_SCGF.calibration.rows.map((row) => (
                    <tr
                      key={row.q}
                      className="border-b border-zinc-800/60 last:border-0 hover:bg-zinc-800/20"
                    >
                      <td className="py-2 pr-3 text-zinc-300">{row.q}</td>
                      <td className="py-2 pr-3 text-emerald-300/90">{row.L8}</td>
                      <td className="py-2 pr-3 text-zinc-500">{row.deposit8}</td>
                      <td className="py-2 pr-3 text-emerald-300/90">{row.L12}</td>
                      <td className="py-2 text-zinc-500">{row.deposit12}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
              The deposited exact values are reproduced to their rounding —
              which pins the chain&rsquo;s time convention to{" "}
              <span className="text-zinc-300">t = L/2 periods</span>{" "}
              (convention fixed by this calibration). The trajectory ensemble
              is an independent implementation and reproduces both the exact
              Z₂ and the deposited quenched chain at L = 8.
            </p>
          </div>
        </div>

        <p className="mt-8 text-center text-[11px] text-zinc-600">
          Framing aligned with manuscript v21 (trajectory-trivial /
          disorder-nontrivial dichotomy).
        </p>
      </div>
    </section>
  );
}
