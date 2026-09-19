"use client";

import { motion } from "framer-motion";
import { Activity, GitBranch, Sigma, FlaskConical, ChevronDown } from "lucide-react";
import { HEADLINE } from "@/lib/research-data";

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: 0.08 * i, duration: 0.6, ease: [0.22, 1, 0.36, 1] as const },
  }),
};

export function Hero() {
  return (
    <section id="top" className="relative overflow-hidden pt-28 pb-16 sm:pt-36 sm:pb-20">
      {/* background decorations */}
      <div aria-hidden className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-[radial-gradient(60%_50%_at_50%_0%,rgba(16,185,129,0.10),transparent_70%)]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.025)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.025)_1px,transparent_1px)] bg-[size:56px_56px] [mask-image:radial-gradient(70%_60%_at_50%_20%,black,transparent)]" />
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <motion.div variants={fadeUp} initial="hidden" animate="show" custom={0}>
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-500/10 px-3 py-1 font-mono text-[11px] text-emerald-300">
            <span className="size-1.5 rounded-full bg-emerald-400 animate-pulse" />
            INTERACTIVE RESEARCH WORKSPACE · MIPT IN RANDOM CLIFFORD CIRCUITS
          </span>
        </motion.div>

        <motion.h1
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={1}
          className="mt-6 text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-zinc-50 leading-[1.05] max-w-4xl"
        >
          The measurement-induced
          <br />
          entanglement transition,
          <span className="text-emerald-400"> solved in the browser.</span>
        </motion.h1>

        <motion.p
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={2}
          className="mt-6 max-w-2xl text-base sm:text-lg text-zinc-400 leading-relaxed"
        >
          A complete exploration of the hybrid random Clifford circuit with projective
          measurements — the stabilizer-entropy locator, the Gullans–Huse purification
          protocol, the free-fermion solution of the annealed sector, and a live
          Gottesman–Knill simulator you can run yourself.
        </motion.p>

        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={3}
          className="mt-8 flex flex-wrap gap-3"
        >
          <a
            href="#simulator"
            className="inline-flex items-center gap-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 transition-all px-5 py-2.5 text-sm font-medium text-emerald-950 shadow-[0_0_28px_-8px_rgba(16,185,129,0.55)] hover:shadow-[0_0_36px_-8px_rgba(16,185,129,0.8)] hover:-translate-y-0.5 active:translate-y-0"
          >
            <FlaskConical className="size-4" />
            Run the circuit simulator
          </a>
          <a
            href="#data"
            className="inline-flex items-center gap-2 rounded-lg border border-zinc-700/80 hover:border-zinc-500 hover:bg-zinc-800/40 transition-all px-5 py-2.5 text-sm font-medium text-zinc-400 hover:text-zinc-200 hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98]"
          >
            <Activity className="size-4" />
            Explore the deposited data
          </a>
        </motion.div>

        {/* headline metrics */}
        <motion.dl
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={4}
          className="mt-14 grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4"
        >
          {[
            {
              icon: Sigma,
              label: "critical point (I₃ locator)",
              value: `p_c = ${HEADLINE.pc.toFixed(4)}`,
              err: `± ${HEADLINE.pcErr.toFixed(4)}`,
              note: "v14 re-centred, tail-safe fits",
              tip: "Where the ⟨I₃⟩(p) curves of different system sizes cross — the entanglement transition. Consistent with Gullans–Huse 0.1593(5) and Sierant 0.15995(10).",
            },
            {
              icon: GitBranch,
              label: "correlation-length exponent",
              value: `ν = ${HEADLINE.nu.toFixed(2)}`,
              err: `± ${HEADLINE.nuErr.toFixed(2)}`,
              note: "ν = 1 excluded at Δχ² ≥ 52",
              tip: "How the crossing window shrinks with system size, L^(1/ν). The frozen-ν Δχ² profile excludes free-fermion ν = 1 at Δχ² ≥ 52 — the headline evidence against the annealed approximation.",
            },
            {
              icon: FlaskConical,
              label: "purification locator",
              value: HEADLINE.pcPurif,
              err: "",
              note: "independent seeds · ν = 1.25(2)",
              tip: "The Gullans–Huse reference-state entropy locator — an independent probe that lands on the same transition, computed from a disjoint 135k-trajectory dataset.",
            },
            {
              icon: Activity,
              label: "trajectory budget",
              value: `${(HEADLINE.trajectoriesI3 / 1000).toFixed(0)}k + ${(HEADLINE.trajectoriesPurif / 1000).toFixed(0)}k`,
              err: "",
              note: "I₃ (L ≤ 512) + purification (L ≤ 256)",
              tip: "Total stabilizer trajectories behind the deposited numbers — every one reproducible from the seed contract (MT19937, seed₀ + k).",
            },
          ].map((m) => (
            <div
              key={m.label}
              title={m.tip}
              className="group relative flex flex-col rounded-xl border border-zinc-800 bg-gradient-to-b from-zinc-900/70 to-zinc-950/60 p-4 backdrop-blur-sm hover:border-emerald-500/30 hover:-translate-y-0.5 transition-all overflow-hidden cursor-default"
            >
              <div
                aria-hidden
                className="pointer-events-none absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-emerald-500/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"
              />
              <div
                aria-hidden
                className="pointer-events-none absolute -right-8 -top-8 size-24 rounded-full bg-emerald-500/[0.07] blur-xl opacity-0 group-hover:opacity-100 transition-opacity"
              />
              <dt className="flex items-center gap-1.5 text-[11px] font-mono uppercase tracking-wider text-zinc-500">
                <m.icon className="size-3.5 text-emerald-500/80" />
                {m.label}
              </dt>
              <dd className="mt-2 font-mono text-xl sm:text-2xl font-semibold text-zinc-50 tabular-nums">
                {m.value}
                {m.err && <span className="ml-1.5 text-sm font-normal text-zinc-500">{m.err}</span>}
              </dd>
              <dd className="mt-auto pt-1.5 text-xs text-zinc-500">{m.note}</dd>
            </div>
          ))}
        </motion.dl>

        {/* scroll hint */}
        <motion.a
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.1, duration: 0.8 }}
          href="#model"
          className="mt-12 hidden sm:inline-flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-zinc-500 hover:text-emerald-400 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 rounded px-2 py-1"
        >
          <motion.span
            animate={{ y: [0, 5, 0] }}
            transition={{ repeat: Infinity, duration: 1.8, ease: "easeInOut" }}
            className="inline-flex"
          >
            <ChevronDown className="size-4" />
          </motion.span>
          scroll — six sections, one transition
        </motion.a>
      </div>
    </section>
  );
}
