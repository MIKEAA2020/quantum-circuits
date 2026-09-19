"use client";

import { CircuitBoard, Ruler, Scan } from "lucide-react";
import { SectionHeading } from "./section-heading";

function CircuitDiagram() {
  const L = 8;
  const rows = Array.from({ length: L }, (_, i) => i);
  const y = (i: number) => 28 + i * 34;
  const gateXs = [60, 100, 140, 180, 220, 260]; // alternating matchings
  const W = 320;
  const H = y(L - 1) + 34;

  const gates: { x: number; a: number; b: number }[] = [];
  gateXs.forEach((x, k) => {
    const parity = k % 2;
    for (let b = 0; b < L / 2; b++) {
      const i = (2 * b + parity) % L;
      const j = (2 * b + 1 + parity) % L;
      gates.push({ x: x + (parity ? 6 : 0), a: i, b: j });
    }
  });

  const measCols = [42, 122, 202, 282];
  const measSets = [
    [0, 3, 5],
    [1, 2, 6, 7],
    [0, 4],
    [2, 5, 7],
  ];

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto max-w-md" role="img" aria-label="Brickwork circuit with measurements">
      {rows.map((i) => (
        <g key={i}>
          <line x1={20} x2={W - 14} y1={y(i)} y2={y(i)} stroke="currentColor" className="text-zinc-700" strokeWidth={1.4} />
          <circle cx={20} cy={y(i)} r={3} fill="#52525b" />
          <text x={12} y={y(i) + 4} textAnchor="end" className="fill-zinc-600 text-[10px] font-mono">{i}</text>
        </g>
      ))}
      {measSets.map((sites, mi) =>
        sites.map((s) => (
          <g key={`m${mi}-${s}`}>
            <circle cx={measCols[mi]} cy={y(s)} r={6.5} fill="#f59e0b" fillOpacity={0.22} stroke="#f59e0b" strokeWidth={1.4} />
            <path d={`M${measCols[mi] - 2.6},${y(s) - 2.6} L${measCols[mi] + 2.6},${y(s) + 2.6}`} stroke="#f59e0b" strokeWidth={1.2} />
          </g>
        ))
      )}
      {gates.map((g, k) => {
        const top = y(Math.min(g.a, g.b));
        const bot = y(Math.max(g.a, g.b));
        const h = bot - top;
        const wrap = h > 40;
        return (
          <g key={k} opacity={wrap ? 0.85 : 1}>
            <rect x={g.x - 8} y={top - 9} width={16} height={h + 18} rx={5} fill="#10b981" fillOpacity={0.16} stroke="#10b981" strokeWidth={1.3} />
            <text x={g.x} y={top + h / 2 + 3.5} textAnchor="middle" className="fill-emerald-400 text-[9px] font-mono">U</text>
          </g>
        );
      })}
      {/* period bracket */}
      <path d={`M32,${H - 6} h70 M32,${H - 6} v5 M102,${H - 6} v5`} stroke="#71717b" strokeWidth={1} fill="none" />
      <text x={67} y={H + 12} textAnchor="middle" className="fill-zinc-500 text-[9px] font-mono">one period</text>
    </svg>
  );
}

export function ModelSection() {
  return (
    <section id="model" className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading num="01" id="model" kicker="The model" title={<>Random Clifford brickwork, attacked by measurements</>}>
          L qubits on a ring evolve under a periodic brickwork of uniformly random two-qubit
          Cliffords — the <span className="font-mono text-zinc-200">720 symplectic Sp(4,2)</span> actions.
          Every site is projectively measured in the Z basis with probability <span className="font-mono text-amber-400">p</span> per
          measurement layer. One period = <span className="font-mono text-zinc-200">[meas][gates-odd][meas][gates-even]</span>.
          Small <span className="font-mono text-amber-400">p</span>: the entanglement grows volumetrically. Large{" "}
          <span className="font-mono text-amber-400">p</span>: measurements win, and the state collapses to an area law.
          Between the two lies a critical point at <span className="font-mono text-amber-400">p_c ≈ 0.16</span>.
        </SectionHeading>

        <div className="mt-10 grid lg:grid-cols-2 gap-6 items-start min-w-0">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 overflow-x-auto">
            <CircuitDiagram />
            <div className="mt-4 flex flex-wrap gap-x-5 gap-y-2 text-xs text-zinc-500">
              <span className="flex items-center gap-1.5">
                <span className="inline-block size-3 rounded-[4px] border border-emerald-500 bg-emerald-500/20" />
                random two-qubit Clifford (Sp(4,2))
              </span>
              <span className="flex items-center gap-1.5">
                <span className="inline-block size-3 rounded-full border border-amber-500 bg-amber-500/20" />
                Z-measurement, prob. p per layer
              </span>
            </div>
          </div>

          <div className="grid gap-4">
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 min-w-0">
              <div className="flex items-center gap-2 text-sm font-medium text-zinc-200">
                <Ruler className="size-4 text-emerald-400" />
                Pure-state protocol — the I₃ locator
              </div>
              <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
                Start from <span className="font-mono text-zinc-300">|0…0⟩</span> and run to depth t = τL. The order
                parameter is the tripartite mutual information{" "}
                <span className="font-mono text-zinc-300">I₃ = S_A + S_B + S_C − S_AB − S_AC − S_BC + S_ABC</span>{" "}
                of three contiguous quarters: <span className="text-rose-400">negative</span> in the volume-law phase
                (long-range entanglement), <span className="text-zinc-300">→ 0</span> in the area-law phase. Crossings
                of ⟨I₃⟩(p) at fixed τ for successive L bracket p_c; a finite-size-scaling collapse fixes{" "}
                <span className="font-mono text-amber-400">p_c = 0.1597(8)</span>,{" "}
                <span className="font-mono text-amber-400">ν = 1.24(7)</span>.
              </p>
            </div>
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 min-w-0">
              <div className="flex items-center gap-2 text-sm font-medium text-zinc-200">
                <Scan className="size-4 text-teal-400" />
                Purification protocol — the independent locator
              </div>
              <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
                Gullans–Huse: double the register to 2L qubits and prepare L Bell pairs{" "}
                <span className="font-mono text-zinc-300">(i, L+i)</span> — the system starts completely mixed, purified
                by the reference. The circuit and all measurements act on the system only; the reference is never
                touched, so <span className="font-mono text-zinc-300">S_ref = S(system)</span> is the purification
                entropy. At p = 0 it stays at L bits forever; at p = 1 it purifies to 0 after a single layer. Its
                crossings locate the same transition with <span className="text-emerald-400">disjoint seeds</span> and
                a <span className="text-emerald-400">different observable</span> — the independence gate the audits demanded.
              </p>
            </div>
            <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/[0.04] p-5">
              <div className="flex items-center gap-2 text-sm font-medium text-emerald-300">
                <CircuitBoard className="size-4" />
                Why Clifford?
              </div>
              <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
                Every state above is a stabilizer state, so the whole dynamics is a{" "}
                <span className="text-zinc-200">Gottesman–Knill tableau computation</span> — classical, bit-exact, and
                reproducible to the last bit. That is what the simulator below runs in your browser: an F₂ generator
                matrix, random symplectic gates, and Z-measurement as a rank-one row reduction. No amplitudes anywhere.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
