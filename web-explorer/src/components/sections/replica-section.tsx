"use client";

import { TrendingUp, Scale, Waves, Snowflake, Sigma, BadgeCheck } from "lucide-react";
import {
  REPLICA_LADDER,
  REPLICA_QUENCHED,
  REPLICA_TREND,
  N5_TWOSIZE,
  SMC_HAAR,
  NO_FREEZE,
} from "@/lib/research-data";
import { SectionHeading } from "./section-heading";

function Formula({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950/70 px-4 py-3 font-mono text-[13px] leading-relaxed text-zinc-300 overflow-x-auto">
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* chart scales — replica ladder (p_c^(n) vs n)                        */
/* ------------------------------------------------------------------ */

const LW = 640;
const LH = 400;
const LM = { top: 28, right: 44, bottom: 54, left: 64 };
const PMIN = 0.12;
const PMAX = 0.55;
const nx = (n: number) => LM.left + ((n - 2) / 3) * (LW - LM.left - LM.right);
const py = (p: number) => LM.top + ((PMAX - p) / (PMAX - PMIN)) * (LH - LM.top - LM.bottom);

const LADDER_Y_TICKS = [0.55, 0.45, 0.35, 0.25, 0.15];

const EMERALD = "#10b981";
const TEAL = "#14b8a6";
const ROSE = "#fb7185";
const AMBER = "#f59e0b";

/** short on-chart class annotation per rung (universality class) */
const RUNG_CLASS_SHORT: Record<number, string> = {
  2: "Ising · exact",
  3: "3-state Potts",
  4: "q = 4 marginal",
  5: "first order",
};

const RUNGS = REPLICA_LADDER.map((r) => ({
  ...r,
  x: nx(r.n),
  y: py(r.pc),
  color: r.order === "first order" ? ROSE : EMERALD,
  band: r.n === 4 ? ([0.38, 0.385] as const) : r.n === 5 ? ([0.47, 0.48] as const) : null,
  errPx: r.n === 3 ? (0.003 / (PMAX - PMIN)) * (LH - LM.top - LM.bottom) : 0,
}));

/* ------------------------------------------------------------------ */
/* chart scales — Haar record SCGF (psi(k) vs k)                       */
/* ------------------------------------------------------------------ */

const SW = 640;
const SH = 400;
const SM = { top: 26, right: 20, bottom: 54, left: 60 };
const YMIN = -7;
const YMAX = 9.5;
const kx = (k: number) => SM.left + ((k + 2) / 4) * (SW - SM.left - SM.right);
const sy = (v: number) => SM.top + ((YMAX - v) / (YMAX - YMIN)) * (SH - SM.top - SM.bottom);
const sePx = (se: number) => (se / (YMAX - YMIN)) * (SH - SM.top - SM.bottom);

const PSI_TICKS = [8, 6, 4, 2, 0, -2, -4, -6];
const K_TICKS = [-2, -1, 0, 1, 2];

/** per-rung key-fact cells under the ladder chart (verbatim numbers) */
const RUNG_FACTS: { n: number; head: string; body: string; accent: string }[] = [
  {
    n: 2,
    head: "0.233810 · continuous",
    body: "EXACT closed form (condition a − c = 2b) — Houtappel triangular-lattice Ising class.",
    accent: "text-emerald-300/90",
  },
  {
    n: 3,
    head: "0.305(3) · continuous",
    body: "Crossings 0.27114 / 0.29678 / 0.30244 / 0.30403 (L = 4–12) · 1/ν_eff = 1.15(10) (Potts 6/5) · R_L(0.305) 0.108 → 0.141 → 0.157 → 0.167 on the target 1/6.",
    accent: "text-emerald-300/90",
  },
  {
    n: 4,
    head: "≈ 0.383 · continuous",
    body: "Crossings 0.35820 / 0.37899 / 0.3823 · R_L(0.383) 0.1315 / 0.1829 / 0.2142 / 0.2378 → 1/4 logarithmically (1/4 − 0.90/ln L + 0.46/ln²L, residual ≤ 8×10⁻⁴ — not degrading) · slope exponent 1.00 → 1.38 → 1.57 through 3/2 · L = 10 at N = 24⁵ = 7,962,624 labels (< 1.8 GB vs ≈ 500 TB dense).",
    accent: "text-emerald-300/90",
  },
  {
    n: 5,
    head: "≈ 0.47–0.48 · first order",
    body: "Closing ×2.12 · L·gap₁₂ 6.85 → 4.85 · plateau 0.060 → 0.040 (fixed ξ) · X-crossing p ≈ 0.449, slope ratio 2.18 · locator 0.48 (L = 4) / 0.47 (L = 6) · next rung L = 8 (120⁴ = 2.1×10⁸ labels).",
    accent: "text-rose-300/90",
  },
];

export function ReplicaSection() {
  return (
    <section id="replica" className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading
          num="06"
          id="replica"
          kicker="Replica ladder · v19"
          title={<>The annealed ladder climbs away from the quenched point</>}
        >
          Exact transfer-matrix spectra now span the full annealed replica chain n = 2…5: q = n-Potts
          universality with first order setting in at n = 5, confirmed at the two-size level. Beside
          it, the first numerical quenched record SCGFs for Haar circuits — genuine record
          multifractality — and a theorem that rules out finite-q freezing for every finite-reachable
          monitored process.
        </SectionHeading>

        {/* ------------------------- ladder chart ------------------------- */}
        <div className="mt-10 rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-6 min-w-0">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <TrendingUp className="size-4 text-emerald-400" />
              Annealed replica ladder — p_c⁽ⁿ⁾ vs replica number n (d = 2)
            </div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-600">
              hover / focus a point for the exact numbers
            </span>
          </div>

          <p className="sr-only">
            Scatter plot of the annealed critical points p_c superscript n against replica number n
            from 2 to 5: {REPLICA_TREND}
          </p>

          <div className="mt-4">
            <svg
              viewBox={`0 0 ${LW} ${LH}`}
              className="w-full h-auto select-none"
              role="img"
              aria-label="Annealed replica ladder: critical point versus replica number n equals 2 to 5, with the quenched line at 0.1597"
            >
              {/* grid + axes */}
              {LADDER_Y_TICKS.map((t) => (
                <g key={t}>
                  <line
                    x1={LM.left}
                    x2={LW - LM.right}
                    y1={py(t)}
                    y2={py(t)}
                    stroke="currentColor"
                    className="text-zinc-800/60"
                    strokeWidth={1}
                  />
                  <text
                    x={LM.left - 8}
                    y={py(t) + 4}
                    textAnchor="end"
                    className="fill-zinc-500 text-[11px] font-mono"
                  >
                    {t.toFixed(2)}
                  </text>
                </g>
              ))}
              {[2, 3, 4, 5].map((n) => (
                <g key={n}>
                  <line
                    x1={nx(n)}
                    x2={nx(n)}
                    y1={LH - LM.bottom}
                    y2={LH - LM.bottom + 6}
                    stroke="currentColor"
                    className="text-zinc-700"
                    strokeWidth={1}
                  />
                  <text
                    x={nx(n)}
                    y={LH - LM.bottom + 22}
                    textAnchor="middle"
                    className="fill-zinc-400 text-[12px] font-mono"
                  >
                    {n}
                  </text>
                </g>
              ))}
              <rect
                x={LM.left}
                y={LM.top}
                width={LW - LM.left - LM.right}
                height={LH - LM.top - LM.bottom}
                fill="none"
                stroke="currentColor"
                className="text-zinc-800"
                strokeWidth={1}
              />
              <text
                x={(LM.left + LW - LM.right) / 2}
                y={LH - 10}
                textAnchor="middle"
                className="fill-zinc-400 text-[11px]"
              >
                replica number n
              </text>
              <text
                x={16}
                y={(LM.top + LH - LM.bottom) / 2}
                textAnchor="middle"
                transform={`rotate(-90 16 ${(LM.top + LH - LM.bottom) / 2})`}
                className="fill-zinc-400 text-[11px]"
              >
                p_c⁽ⁿ⁾ — annealed
              </text>

              {/* trend guide through the rungs */}
              <polyline
                points={RUNGS.map((r) => `${r.x},${r.y}`).join(" ")}
                fill="none"
                stroke="currentColor"
                className="text-zinc-700"
                strokeWidth={1.5}
                strokeDasharray="5 5"
                opacity={0.8}
              />

              {/* quenched reference line */}
              <line
                x1={LM.left}
                x2={LW - LM.right}
                y1={py(REPLICA_QUENCHED.pc)}
                y2={py(REPLICA_QUENCHED.pc)}
                stroke={AMBER}
                strokeWidth={1.5}
                strokeDasharray="7 5"
                opacity={0.9}
              />
              <text
                x={LW - LM.right}
                y={py(REPLICA_QUENCHED.pc) - 8}
                textAnchor="end"
                className="fill-amber-400/90 text-[10px] font-mono"
              >
                quenched (Clifford, Born-weighted) · {REPLICA_QUENCHED.label}
              </text>

              {/* rungs */}
              {RUNGS.map((r) => {
                const labelTop = r.band ? py(r.band[1]) : r.y;
                /* the n = 2 rung sits at the left edge — label it beside the point */
                const side = r.n === 2;
                return (
                  <g
                    key={r.n}
                    tabIndex={0}
                    role="img"
                    aria-label={`n = ${r.n}: p_c = ${r.pcLabel}, ${r.cls}, ${r.order}`}
                    className="outline-none group cursor-default"
                  >
                    {r.band && (
                      <rect
                        x={r.x - 26}
                        y={py(r.band[1])}
                        width={52}
                        height={Math.max(py(r.band[0]) - py(r.band[1]), 2)}
                        rx={2}
                        fill={r.color}
                        fillOpacity={0.16}
                        stroke={r.color}
                        strokeOpacity={0.55}
                        strokeWidth={1}
                        className="group-focus-visible:stroke-opacity-100"
                      />
                    )}
                    {r.errPx > 0 && (
                      <g stroke={r.color} strokeWidth={1.5} opacity={0.9}>
                        <line x1={r.x} x2={r.x} y1={r.y - r.errPx} y2={r.y + r.errPx} />
                        <line x1={r.x - 5} x2={r.x + 5} y1={r.y - r.errPx} y2={r.y - r.errPx} />
                        <line x1={r.x - 5} x2={r.x + 5} y1={r.y + r.errPx} y2={r.y + r.errPx} />
                      </g>
                    )}
                    <circle
                      cx={r.x}
                      cy={r.y}
                      r={r.n === 5 ? 6.5 : 6}
                      fill={r.color}
                      fillOpacity={0.95}
                      stroke="#052e16"
                      strokeWidth={1}
                      className="group-focus-visible:fill-opacity-100 group-focus-visible:stroke-zinc-100"
                    />
                    <text
                      x={side ? r.x + 16 : r.x}
                      y={side ? r.y - 3 : labelTop - 28}
                      textAnchor={side ? "start" : "middle"}
                      className={`text-[12px] font-mono font-semibold ${
                        r.n === 5 ? "fill-rose-300" : "fill-emerald-300"
                      }`}
                    >
                      {r.pcLabel}
                    </text>
                    <text
                      x={side ? r.x + 16 : r.x}
                      y={side ? r.y + 12 : labelTop - 13}
                      textAnchor={side ? "start" : "middle"}
                      className="fill-zinc-500 text-[10px] font-mono"
                    >
                      {RUNG_CLASS_SHORT[r.n]}
                    </text>
                    <title>{`n = ${r.n}: p_c = ${r.pcLabel} — ${r.cls} (${r.order})`}</title>
                  </g>
                );
              })}
            </svg>
          </div>

          {/* takeaway + verbatim trend strip */}
          <div className="mt-4 grid gap-3 lg:grid-cols-[1fr_auto] lg:items-center">
            <p className="text-sm text-zinc-400 leading-relaxed">
              The annealed points recede from the quenched transition as n grows — the{" "}
              <span className="text-zinc-200">q = n-Potts chain</span>, with first order setting in
              at n = 5.
            </p>
            <div className="rounded-lg border border-zinc-800 bg-zinc-950/70 px-4 py-2 font-mono text-xs text-zinc-300 whitespace-nowrap overflow-x-auto">
              <span className="text-amber-400/90">0.1597(8)</span>
              <span className="text-zinc-600"> quenched &lt; </span>
              <span className="text-emerald-300/90">0.233810</span>
              <span className="text-zinc-600"> &lt; </span>
              <span className="text-emerald-300/90">0.305(3)</span>
              <span className="text-zinc-600"> &lt; </span>
              <span className="text-emerald-300/90">0.383</span>
              <span className="text-zinc-600"> &lt; </span>
              <span className="text-rose-300/90">0.47</span>
            </div>
          </div>
          <p className="mt-2 text-xs text-zinc-500 leading-relaxed">
            No annealed sequence converges to the Born-weighted point from above — the quenched
            transition is genuinely non-perturbative in the measurement noise.
          </p>
          <p className="mt-1.5 text-xs text-zinc-500 leading-relaxed">
            The n = 3 rung reappears as the Λ(2) tilt of the record SCGF —{" "}
            <a
              href="#record-scgf"
              className="text-emerald-400/90 hover:text-emerald-300 underline decoration-dotted underline-offset-2 whitespace-nowrap"
            >
              cf. the Record SCGF section
            </a>
            : the same Z̄₂ anchor and the n = 3 operator.
          </p>

          {/* rung fact cells */}
          <div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
            {RUNG_FACTS.map((f) => (
              <div
                key={f.n}
                className="rounded-lg border border-zinc-800 bg-zinc-950/50 px-3.5 py-3 min-w-0"
              >
                <div className="flex items-center gap-2">
                  <span className="grid place-items-center size-5 rounded border border-zinc-700 bg-zinc-900 font-mono text-[10px] font-semibold text-zinc-400">
                    {f.n}
                  </span>
                  <span className={`font-mono text-xs font-semibold ${f.accent}`}>{f.head}</span>
                </div>
                <p className="mt-1.5 text-[11px] text-zinc-500 leading-relaxed">{f.body}</p>
              </div>
            ))}
          </div>
        </div>

        {/* ------------------------- two-size test ------------------------- */}
        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-6 min-w-0">
          <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
            <Scale className="size-4 text-amber-400" />
            The two-size test — n = 5 is first order (L = 4 → 6)
          </div>
          <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
            At the coexistence locator p ≈ 0.47 the two-phase gap log(λ₁/λ₂) closes{" "}
            <span className="font-mono text-zinc-200">1.711 → 0.806</span> — factor ×2.12 — against
            ×1.94 (n = 4) and ×1.81 (n = 3, the continuous baseline) at matched sizes and locators.
          </p>

          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-sm font-mono min-w-[760px]">
              <thead>
                <tr className="text-left text-[10px] uppercase tracking-wider text-zinc-500 border-b border-zinc-800">
                  <th scope="col" className="py-2 pr-4 font-medium">n</th>
                  <th scope="col" className="py-2 pr-4 font-medium">locator p</th>
                  <th scope="col" className="py-2 pr-4 font-medium">gap₁₂ (L = 4)</th>
                  <th scope="col" className="py-2 pr-4 font-medium">gap₁₂ (L = 6)</th>
                  <th scope="col" className="py-2 pr-4 font-medium bg-amber-500/[0.07] text-amber-300/90">
                    closing factor
                  </th>
                  <th scope="col" className="py-2 pr-4 font-medium">L·gap₁₂ (L = 4→6)</th>
                  <th scope="col" className="py-2 font-medium">verdict</th>
                </tr>
              </thead>
              <tbody>
                {N5_TWOSIZE.map((r) => (
                  <tr
                    key={r.n}
                    className={`border-b border-zinc-800/60 last:border-0 hover:bg-zinc-800/20 ${
                      r.n === 5 ? "bg-rose-500/[0.05]" : ""
                    }`}
                  >
                    <td className={`py-2.5 pr-4 tabular-nums ${r.n === 5 ? "text-rose-200 font-semibold" : "text-zinc-300"}`}>
                      {r.n}
                    </td>
                    <td className="py-2.5 pr-4 text-zinc-300 tabular-nums">{r.locator}</td>
                    <td className="py-2.5 pr-4 text-zinc-300 tabular-nums">{r.gapL4.toFixed(3)}</td>
                    <td className="py-2.5 pr-4 text-zinc-300 tabular-nums">{r.gapL6.toFixed(3)}</td>
                    <td className="py-2.5 pr-4 bg-amber-500/[0.07] text-amber-300 font-semibold tabular-nums">
                      ×{r.closing.toFixed(2)}
                    </td>
                    <td className="py-2.5 pr-4 text-zinc-300 tabular-nums">{r.lgap}</td>
                    <td className={`py-2.5 ${r.n === 5 ? "text-rose-300 font-medium" : "text-zinc-500"}`}>
                      {r.cls}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
            Closing factor monotone across replica number; L·gap₁₂ saturates at n = 3
            (energy-operator amplitude — n = 3 continues 8.59 → 7.11 → 6.53 → 6.21 at 2πx_ε) and
            falls below the continuous envelope at n = 5 — the signature of an exponentially closing
            tunnelling splitting. Two sizes caveat: they cannot yet separate exponential from
            power-law closing; L = 8 (120⁴ = 2.1×10⁸ bond labels) is the next rung.
          </p>

          <div className="mt-4 flex flex-wrap gap-2">
            <span className="rounded-full border border-zinc-700/80 bg-zinc-950/60 px-3 py-1 font-mono text-[11px] text-zinc-400">
              plateau narrows by the full size ratio 4/6 — 0.060 → 0.040 (fixed ξ)
            </span>
            <span className="rounded-full border border-zinc-700/80 bg-zinc-950/60 px-3 py-1 font-mono text-[11px] text-zinc-400">
              X-curves cross at p ≈ 0.449 · slope ratio 2.18 vs n = 3&rsquo;s 1.69 ≈ (6/4)^1.15
            </span>
            <span className="rounded-full border border-zinc-700/80 bg-zinc-950/60 px-3 py-1 font-mono text-[11px] text-zinc-400">
              locator stable — 0.48 (L = 4) / 0.47 (L = 6)
            </span>
          </div>
        </div>

        {/* ------------------------- Haar record SCGF ------------------------- */}
        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-5 min-w-0 lg:col-span-2">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <Waves className="size-4 text-teal-400" />
              Haar record SCGF ψ(k) — the first numerical quenched record SCGFs
            </div>
            <p className="mt-1 text-[11px] font-mono text-zinc-500">
              {SMC_HAAR.params} · p ∈ {"{0.10, 0.1597, 0.2338, 0.4}"}
            </p>

            <p className="sr-only">
              Line chart of the record scaled cumulant generating function psi of tilt k at
              p = 0.2338, for L = 8 and L = 12, with one-standard-error bars. Both curves pass
              through the origin and are strictly convex.
            </p>

            <div className="mt-3">
              <svg
                viewBox={`0 0 ${SW} ${SH}`}
                className="w-full h-auto select-none"
                role="img"
                aria-label="Haar record SCGF psi versus tilt k at p equals 0.2338 for L equals 8 and L equals 12 with standard error bars"
              >
                {/* grid */}
                {PSI_TICKS.map((t) => (
                  <g key={t}>
                    <line
                      x1={SM.left}
                      x2={SW - SM.right}
                      y1={sy(t)}
                      y2={sy(t)}
                      stroke="currentColor"
                      className="text-zinc-800/60"
                      strokeWidth={1}
                    />
                    <text
                      x={SM.left - 8}
                      y={sy(t) + 4}
                      textAnchor="end"
                      className="fill-zinc-500 text-[11px] font-mono"
                    >
                      {t > 0 ? t : t === 0 ? "0" : `−${Math.abs(t)}`}
                    </text>
                  </g>
                ))}
                {K_TICKS.map((k) => (
                  <g key={k}>
                    <line
                      x1={kx(k)}
                      x2={kx(k)}
                      y1={SH - SM.bottom}
                      y2={SH - SM.bottom + 6}
                      stroke="currentColor"
                      className="text-zinc-700"
                      strokeWidth={1}
                    />
                    <text
                      x={kx(k)}
                      y={SH - SM.bottom + 22}
                      textAnchor="middle"
                      className="fill-zinc-400 text-[12px] font-mono"
                    >
                      {k > 0 ? k : k === 0 ? "0" : `−${Math.abs(k)}`}
                    </text>
                  </g>
                ))}
                <rect
                  x={SM.left}
                  y={SM.top}
                  width={SW - SM.left - SM.right}
                  height={SH - SM.top - SM.bottom}
                  fill="none"
                  stroke="currentColor"
                  className="text-zinc-800"
                  strokeWidth={1}
                />

                {/* zero line */}
                <line
                  x1={SM.left}
                  x2={SW - SM.right}
                  y1={sy(0)}
                  y2={sy(0)}
                  stroke="#71717a"
                  strokeWidth={1}
                  strokeDasharray="6 4"
                  opacity={0.8}
                />

                {/* L = 8 curve */}
                <polyline
                  points={SMC_HAAR.k.map((k, i) => `${kx(k)},${sy(SMC_HAAR.psiL8[i])}`).join(" ")}
                  fill="none"
                  stroke={EMERALD}
                  strokeWidth={2}
                  strokeLinejoin="round"
                  strokeLinecap="round"
                  opacity={0.9}
                />
                {/* L = 12 curve */}
                <polyline
                  points={SMC_HAAR.k.map((k, i) => `${kx(k)},${sy(SMC_HAAR.psiL12[i])}`).join(" ")}
                  fill="none"
                  stroke={TEAL}
                  strokeWidth={2}
                  strokeLinejoin="round"
                  strokeLinecap="round"
                  opacity={0.9}
                />

                {/* L = 8 points + error bars */}
                {SMC_HAAR.k.map((k, i) => {
                  const v = SMC_HAAR.psiL8[i];
                  const se = SMC_HAAR.psiL8se[i];
                  const x = kx(k);
                  const y = sy(v);
                  const e = sePx(se);
                  return (
                    <g
                      key={`l8-${k}`}
                      tabIndex={0}
                      role="img"
                      aria-label={`L = 8, k = ${k}: psi = ${v} plus or minus ${se} nats per period`}
                      className="outline-none group cursor-default"
                    >
                      {se > 0 && (
                        <g stroke={EMERALD} strokeWidth={1.2} opacity={0.8}>
                          <line x1={x} x2={x} y1={y - e} y2={y + e} />
                          <line x1={x - 4} x2={x + 4} y1={y - e} y2={y - e} />
                          <line x1={x - 4} x2={x + 4} y1={y + e} y2={y + e} />
                        </g>
                      )}
                      <circle
                        cx={x}
                        cy={y}
                        r={3.5}
                        fill={EMERALD}
                        stroke="#052e16"
                        strokeWidth={1}
                        className="group-focus-visible:stroke-zinc-100"
                      />
                      <title>{`L = 8 · k = ${k}: ψ = ${v.toFixed(2)} ± ${se.toFixed(2)} nats/period`}</title>
                    </g>
                  );
                })}
                {/* L = 12 points + error bars */}
                {SMC_HAAR.k.map((k, i) => {
                  const v = SMC_HAAR.psiL12[i];
                  const se = SMC_HAAR.psiL12se[i];
                  const x = kx(k);
                  const y = sy(v);
                  const e = sePx(se);
                  return (
                    <g
                      key={`l12-${k}`}
                      tabIndex={0}
                      role="img"
                      aria-label={`L = 12, k = ${k}: psi = ${v} plus or minus ${se} nats per period`}
                      className="outline-none group cursor-default"
                    >
                      {se > 0 && (
                        <g stroke={TEAL} strokeWidth={1.2} opacity={0.8}>
                          <line x1={x} x2={x} y1={y - e} y2={y + e} />
                          <line x1={x - 4} x2={x + 4} y1={y - e} y2={y - e} />
                          <line x1={x - 4} x2={x + 4} y1={y + e} y2={y + e} />
                        </g>
                      )}
                      <circle
                        cx={x}
                        cy={y}
                        r={3.5}
                        fill={TEAL}
                        stroke="#042f2e"
                        strokeWidth={1}
                        className="group-focus-visible:stroke-zinc-100"
                      />
                      <title>{`L = 12 · k = ${k}: ψ = ${v.toFixed(2)} ± ${se.toFixed(2)} nats/period`}</title>
                    </g>
                  );
                })}

                {/* legend */}
                <g>
                  <circle cx={SM.left + 18} cy={SM.top + 16} r={4} fill={EMERALD} />
                  <text x={SM.left + 30} y={SM.top + 20} className="fill-zinc-400 text-[11px] font-mono">
                    L = 8
                  </text>
                  <circle cx={SM.left + 82} cy={SM.top + 16} r={4} fill={TEAL} />
                  <text x={SM.left + 94} y={SM.top + 20} className="fill-zinc-400 text-[11px] font-mono">
                    L = 12
                  </text>
                  <text x={SM.left + 146} y={SM.top + 20} className="fill-zinc-600 text-[11px] font-mono">
                    p = 0.2338 · bars = 1 s.e.
                  </text>
                </g>

                {/* axis titles */}
                <text
                  x={(SM.left + SW - SM.right) / 2}
                  y={SH - 10}
                  textAnchor="middle"
                  className="fill-zinc-400 text-[11px]"
                >
                  k (tilt)
                </text>
                <text
                  x={15}
                  y={(SM.top + SH - SM.bottom) / 2}
                  textAnchor="middle"
                  transform={`rotate(-90 15 ${(SM.top + SH - SM.bottom) / 2})`}
                  className="fill-zinc-400 text-[11px]"
                >
                  ψ (nats / period)
                </text>
              </svg>
            </div>

            <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
              D(q) nonconstant — genuine record multifractality (Clifford circuits have D exactly
              constant). τ remains strictly convex, with no linear branch — the freezing signature —
              up to q = 3 at L ≤ 12.
            </p>

            {/* validation chips */}
            <div className="mt-3 flex flex-wrap gap-1.5">
              {SMC_HAAR.validation.map((v) => (
                <span
                  key={v}
                  className="inline-flex items-center gap-1 rounded-full border border-zinc-700/80 bg-zinc-950/60 px-2.5 py-1 font-mono text-[10px] text-zinc-500"
                >
                  <span className="text-emerald-500/90" aria-hidden>✓</span>
                  {v}
                </span>
              ))}
            </div>
          </div>

          {/* stats strip */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 sm:p-5 min-w-0 flex flex-col gap-4">
            <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-zinc-500">
              <Sigma className="size-3.5 text-emerald-500/80" />
              what ψ says
            </div>

            <div>
              <div className="text-xs font-semibold text-zinc-200">
                D(q) nonconstant — record multifractality
              </div>
              <div className="mt-2 space-y-1.5">
                {SMC_HAAR.pValues.map((p, i) => (
                  <div key={p} className="flex items-center gap-2">
                    <span className="w-16 text-right text-[10px] font-mono text-zinc-500">
                      p = {p}
                    </span>
                    <div
                      className="h-1.5 flex-1 min-w-0 rounded-full bg-zinc-800 overflow-hidden"
                      role="img"
                      aria-label={`D-spread ${SMC_HAAR.dSpreadL8[i]} nats per period at p = ${p}`}
                    >
                      <div
                        className="h-full rounded-full bg-emerald-500"
                        style={{ width: `${(SMC_HAAR.dSpreadL8[i] / 1.96) * 100}%` }}
                      />
                    </div>
                    <span className="w-9 text-[10px] font-mono text-emerald-300/90 tabular-nums">
                      {SMC_HAAR.dSpreadL8[i].toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
              <p className="mt-2 text-[11px] text-zinc-500 leading-relaxed">
                D-spread over q ∈ [−1, 3] at L = 8, nats per period · 1.19 at L = 12 (p = 0.2338) —
                grows with monitoring rate and with L · Clifford: exactly constant.
              </p>
            </div>

            <div className="border-t border-zinc-800/70 pt-3">
              <div className="text-xs font-semibold text-zinc-200">Record entropy rate ψ′(0)</div>
              <p className="mt-1.5 text-[11px] font-mono text-zinc-400 leading-relaxed">
                per period (L = 8):{" "}
                <span className="text-zinc-200">
                  {SMC_HAAR.entropyRatesL8.map((r) => r.toFixed(2)).join(" / ")}
                </span>{" "}
                nats
                <br />
                per site-period (p = 0.2338):{" "}
                <span className="text-zinc-200">
                  {SMC_HAAR.perSite.rates.map((r) => r.toFixed(3)).join(" / ")}
                </span>{" "}
                at L = 6/8/10 — L-independent to 5%.
              </p>
            </div>

            <div className="border-t border-zinc-800/70 pt-3">
              <div className="text-xs font-semibold text-zinc-200">No linear τ branch</div>
              <p className="mt-1.5 text-[11px] text-zinc-500 leading-relaxed">
                Up to q = 3 at L ≤ 12 — no finite-q freezing; the freezing signature (an affine
                branch of τ) is absent.
              </p>
            </div>

            <div className="border-t border-zinc-800/70 pt-3">
              <div className="text-xs font-semibold text-zinc-200">Annealed vs quenched (k = 1)</div>
              <p className="mt-1.5 text-[11px] font-mono leading-relaxed">
                <span className="text-amber-300/90">annealed {SMC_HAAR.annealedVsQuenched.annealed.toFixed(2)}</span>
                <span className="text-zinc-600"> vs </span>
                <span className="text-emerald-300/90">quenched {SMC_HAAR.annealedVsQuenched.quenched.toFixed(2)}</span>
              </p>
              <p className="mt-1 text-[11px] text-zinc-500 leading-relaxed">
                At L = 8, p = 0.2338 — ≈6% level, growing with L and p: the disorder average does
                not commute with the logarithm.
              </p>
            </div>
          </div>
        </div>

        {/* ------------------------- no-freeze theorem ------------------------- */}
        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
                <Snowflake className="size-4 text-teal-400" />
                The no-freeze theorem
              </div>
              <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-1 font-mono text-[10px] uppercase tracking-wider text-emerald-300">
                <BadgeCheck className="size-3.5" />
                machine verification {NO_FREEZE.machine}
              </span>
            </div>

            <div className="mt-4 rounded-lg border-l-2 border-emerald-500/60 bg-zinc-950/70 px-4 py-3">
              <div className="font-mono text-[10px] uppercase tracking-wider text-emerald-400/90">
                Theorem (v19)
              </div>
              <p className="mt-1 text-sm text-zinc-200 leading-relaxed">{NO_FREEZE.theorem}</p>
            </div>

            <ul className="mt-4 space-y-1.5">
              {NO_FREEZE.proofRoute.map((step) => (
                <li key={step} className="flex items-start gap-2 text-xs text-zinc-500 leading-relaxed">
                  <span className="mt-1.5 size-1 shrink-0 rounded-full bg-emerald-500/80" aria-hidden />
                  {step}
                </li>
              ))}
            </ul>

            <div className="mt-4 rounded-lg border border-rose-500/25 bg-rose-500/[0.04] px-4 py-3">
              <div className="font-mono text-[10px] uppercase tracking-wider text-rose-300/90">
                REM contrast
              </div>
              <p className="mt-1 text-xs text-zinc-400 leading-relaxed">
                The random-energy construction realizes freezing at q_c = √(2 log 2), where τ′
                stays continuous at the onset — the side-by-side counterexample: freezing requires
                an <span className="text-zinc-200">unbounded reachable set</span>.
              </p>
            </div>

            <p className="mt-3 text-xs text-zinc-500 leading-relaxed">
              Corollary: {NO_FREEZE.corollary}.
            </p>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6 min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-zinc-100">
              <Sigma className="size-4 text-emerald-400" />
              Replica interpolation identity
            </div>
            <p className="mt-1 font-mono text-[10px] uppercase tracking-wider text-zinc-600">
              Proposition (v19)
            </p>

            <div className="mt-4 space-y-3">
              <Formula>
                <span className="text-emerald-400">g(r)</span> − r·E log X ={" "}
                <span className="text-zinc-500">∫</span>₀ʳ (r−s)·Var<sub>s</sub>(log X) ds
              </Formula>
              <div className="flex flex-wrap gap-2">
                {NO_FREEZE.interpolation.consequences.map((c) => (
                  <span
                    key={c}
                    className="rounded-full border border-zinc-700/80 bg-zinc-950/60 px-3 py-1 font-mono text-[11px] text-zinc-300"
                  >
                    {c}
                  </span>
                ))}
              </div>
              <Formula>
                <span className="text-zinc-500">interchange ⟺</span> sup<sub>T</sub>{" "}
                Var(T⁻¹ log Z) &lt; ∞
              </Formula>
            </div>

            <p className="mt-4 text-xs text-zinc-500 leading-relaxed">
              Replica free energies f<sub>m</sub> form a monotone ladder: m ↓ 0 recovers the quenched
              value quadratically, while m → ∞ overshoots to the extremal value log ess sup X — the
              naive replica limit is <em>not</em> an interchange. The disorder-replica interchange
              reduces to the measurable self-averaging criterion{" "}
              <span className="font-mono text-zinc-400">sup_T Var(T⁻¹ log Z) &lt; ∞</span>, where
              Var<sub>s</sub> is the variance under the r-tilted law.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
