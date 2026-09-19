"use client";

import { useState } from "react";
import { L_COLORS, ACCENT, lerpScale, ticks, fmt } from "./chart-utils";

export interface I3SeriesPoint {
  p: number;
  mean: number;
  se: number;
}

export interface SweepOverlay {
  id: string;
  label: string;
  color: string;
  series: Record<number, I3SeriesPoint[]>;
}

/** literature / deposited p_c estimates — 1σ vertical bands on the raw chart */
export interface LitBand {
  id: string;
  label: string;
  /** central estimate */
  pc: number;
  /** one standard error (band half-width) */
  err: number;
  color: string;
}

interface Props {
  /** series[L] = I₃ mean ± s.e. over a shared p-grid */
  series: Record<number, I3SeriesPoint[]>;
  sizes: number[];
  /** crossing estimates to mark on the x-axis (from the panel); lo/hi = bootstrap 68% */
  crossings?: { pair: string; p: number; lo?: number; hi?: number }[];
  /** saved sweeps to overlay (dashed) on top of the live curves */
  overlays?: SweepOverlay[];
  /** literature p_c estimates — 1σ bands (this work / Gullans–Huse / Sierant) */
  litBands?: LitBand[];
  pc?: number;
  height?: number;
  busy?: boolean;
}

const OVERLAY_DASH = "7 5";

/**
 * Gullans–Huse I₃ locator: ⟨I₃⟩ vs p for several system sizes. The volume-law
 * phase sits deep negative (monogamy of entanglement, ≈ −L/2), the area-law
 * phase collapses to 0, and the curves cross near p_c with a finite-size
 * drift that shrinks as L grows. Saved sweeps can be overlaid dashed for
 * direct comparison; hovering shows a crosshair readout at the nearest p.
 */
export function I3SweepChart({ series, sizes, crossings = [], overlays = [], litBands = [], pc = 0.1597, height = 340, busy = false }: Props) {
  const W = 720;
  const H = height;
  const M = { top: 18, right: 18, bottom: 40, left: 56 };

  const [hoverP, setHoverP] = useState<number | null>(null);

  // scales + shared p-grid (auto-memoised by the React compiler)
  let xmin = Infinity, xmax = -Infinity, ymin = Infinity, ymax = -Infinity;
  const pset = new Set<number>();
  const track = (s: Record<number, I3SeriesPoint[]>) => {
    for (const pts of Object.values(s))
      for (const pt of pts) {
        pset.add(pt.p);
        xmin = Math.min(xmin, pt.p);
        xmax = Math.max(xmax, pt.p);
        ymin = Math.min(ymin, pt.mean - 2 * pt.se);
        ymax = Math.max(ymax, pt.mean + 2 * pt.se);
      }
  };
  track(series);
  for (const o of overlays) track(o.series);
  const empty = !Number.isFinite(xmin);
  const xpad = empty ? 0 : Math.max((xmax - xmin) * 0.04, 0.002);
  const yspan = empty ? 1 : (ymax - ymin) || 1;
  const ylo = empty ? -1 : ymin - yspan * 0.08;
  const yhi = empty ? 1 : ymax + yspan * 0.08;
  const xs = empty ? [0, 1] : ticks(xmin - xpad, xmax + xpad, 6);
  const ys = empty ? [0] : ticks(ylo, yhi, 5);
  const xScale = lerpScale(empty ? 0 : xmin - xpad, empty ? 1 : xmax + xpad, M.left, W - M.right);
  const yScale = lerpScale(ylo, yhi, H - M.bottom, M.top);
  const hasZero = ylo < 0 && yhi > 0;
  const pGrid = Array.from(pset).sort((a, b) => a - b);

  /** nearest grid p to a cursor x position */
  const nearestP = (clientX: number, el: SVGSVGElement) => {
    if (!pGrid.length) return null;
    const rect = el.getBoundingClientRect();
    const x = ((clientX - rect.left) / rect.width) * W;
    let best = pGrid[0];
    let bestDist = Infinity;
    for (const p of pGrid) {
      const dist = Math.abs(xScale(p) - x);
      if (dist < bestDist) { bestDist = dist; best = p; }
    }
    return best;
  };

  // readout rows at hoverP: live + overlays
  const readout = (() => {
    if (hoverP == null) return null;
    const rows: { label: string; color: string; L: number; mean: number; se: number; dashed?: boolean }[] = [];
    for (const L of sizes) {
      const pt = (series[L] ?? []).find((q) => Math.abs(q.p - hoverP) < 1e-6);
      if (pt) rows.push({ label: "this sweep", color: L_COLORS[L] ?? "#10b981", L, mean: pt.mean, se: pt.se });
    }
    for (const o of overlays) {
      for (const L of Object.keys(o.series).map(Number).sort((a, b) => a - b)) {
        const pt = o.series[L].find((q) => Math.abs(q.p - hoverP) < 1e-6);
        if (pt) rows.push({ label: o.label, color: o.color, L, mean: pt.mean, se: pt.se, dashed: true });
      }
    }
    return rows.length ? { p: hoverP, rows } : null;
  })();

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      className="w-full h-auto select-none"
      role="img"
      aria-label="Tripartite mutual information versus measurement probability for several system sizes"
      onMouseMove={(e) => setHoverP(nearestP(e.clientX, e.currentTarget))}
      onMouseLeave={() => setHoverP(null)}
    >
      {/* grid — dashed rules + short axis ticks, zero line emphasised */}
      {ys.map((y, i) => (
        <g key={`gy${i}`}>
          <line
            x1={M.left} x2={W - M.right} y1={yScale(y)} y2={yScale(y)}
            stroke="currentColor" className={y === 0 ? "text-zinc-600" : "text-zinc-800"}
            strokeWidth={y === 0 ? 1.2 : 1}
            strokeDasharray={y === 0 ? undefined : "3 5"}
          />
          <line x1={M.left - 5} x2={M.left} y1={yScale(y)} y2={yScale(y)} stroke="currentColor" className="text-zinc-600" strokeWidth={1} />
          <text x={M.left - 8} y={yScale(y) + 4} textAnchor="end" className="fill-zinc-500 text-[11px] font-mono">
            {fmt(y, Math.abs(y) >= 10 ? 1 : 2)}
          </text>
        </g>
      ))}
      {xs.map((x, i) => (
        <g key={`tx${i}`}>
          <line x1={xScale(x)} x2={xScale(x)} y1={H - M.bottom} y2={H - M.bottom - 5} stroke="currentColor" className="text-zinc-600" strokeWidth={1} />
          <text x={xScale(x)} y={H - M.bottom + 18} textAnchor="middle" className="fill-zinc-500 text-[11px] font-mono">
            {x.toFixed(3)}
          </text>
        </g>
      ))}
      {/* plot frame baseline */}
      <line x1={M.left} x2={W - M.right} y1={H - M.bottom} y2={H - M.bottom} stroke="currentColor" className="text-zinc-700" strokeWidth={1} />
      <text x={W / 2} y={H - 5} textAnchor="middle" className="fill-zinc-400 text-[11px]">measurement probability p</text>
      <text x={13} y={H / 2} textAnchor="middle" transform={`rotate(-90 13 ${H / 2})`} className="fill-zinc-400 text-[11px]">⟨I₃⟩ (bits)</text>

      {/* I3 = 0 area-law reference */}
      {hasZero && (
        <text x={W - M.right - 4} y={yScale(0) - 6} textAnchor="end" className="fill-zinc-600 text-[10px] font-mono">
          area law · I₃ → 0
        </text>
      )}

      {/* volume-law annotation — sits in the deep-negative region, bottom-left */}
      <text x={M.left + 8} y={H - M.bottom - 10} className="fill-zinc-600 text-[10px] font-mono">
        volume law · I₃ ≈ −L/2 (monogamy)
      </text>

      {/* p_c line */}
      {pc > 0 && (
        <g>
          <line x1={xScale(pc)} x2={xScale(pc)} y1={M.top} y2={H - M.bottom} stroke={ACCENT} strokeWidth={1.5} strokeDasharray="6 4" opacity={0.9} />
          <text x={xScale(pc) + 6} y={H - M.bottom - 8} className="fill-amber-500 text-[11px] font-mono">p_c = 0.1597</text>
        </g>
      )}

      {/* literature p_c bands — staggered so near-coincident estimates stay readable */}
      {litBands.map((b, i) => {
        const lo = Math.min(xScale(b.pc - b.err), xScale(b.pc + b.err));
        const w = Math.max(Math.abs(xScale(b.pc + b.err) - xScale(b.pc - b.err)), 2.5);
        const y0 = M.top + 6 + i * 11;
        return (
          <g key={b.id}>
            <rect x={lo} y={y0} width={w} height={H - M.bottom - y0 - 12} fill={b.color} opacity={0.08} rx={1.5}>
              <title>{`${b.label}: p_c = ${b.pc.toFixed(4)} ± ${b.err.toFixed(4)} (1σ band)`}</title>
            </rect>
            <line x1={xScale(b.pc)} x2={xScale(b.pc)} y1={y0} y2={H - M.bottom - 12} stroke={b.color} strokeWidth={1} opacity={0.4} />
            <text x={xScale(b.pc) + 6} y={y0 + 8} className="text-[8.5px] font-mono" fill={b.color} opacity={0.95}>
              {b.label}
            </text>
          </g>
        );
      })}

      {/* your crossings — bootstrap band + dashed point estimate */}
      {crossings.map((c, i) => (
        <g key={i}>
          {c.lo != null && c.hi != null && (
            <g>
              <rect
                x={Math.min(xScale(c.lo), xScale(c.hi))}
                width={Math.max(Math.abs(xScale(c.hi) - xScale(c.lo)), 2)}
                y={H - M.bottom - 9}
                height={9}
                fill="#fb7185"
                opacity={0.18}
                rx={2}
              >
                <title>{`${c.pair}: bootstrap 68% band [${c.lo.toFixed(3)}, ${c.hi.toFixed(3)}]`}</title>
              </rect>
              <line x1={xScale(c.lo)} x2={xScale(c.lo)} y1={H - M.bottom} y2={H - M.bottom - 9} stroke="#fb7185" strokeWidth={1} opacity={0.6} />
              <line x1={xScale(c.hi)} x2={xScale(c.hi)} y1={H - M.bottom} y2={H - M.bottom - 9} stroke="#fb7185" strokeWidth={1} opacity={0.6} />
            </g>
          )}
          <line x1={xScale(c.p)} x2={xScale(c.p)} y1={M.top} y2={H - M.bottom} stroke="#fb7185" strokeWidth={1} strokeDasharray="2 3" opacity={0.75}>
            <title>{`${c.pair} crossing → ${c.p.toFixed(3)}${c.lo != null && c.hi != null ? ` (68%: ${c.lo.toFixed(3)}–${c.hi.toFixed(3)})` : ""}`}</title>
          </line>
        </g>
      ))}

      {/* overlay sweeps first (underneath) */}
      {overlays.map((o) =>
        Object.keys(o.series)
          .map(Number)
          .sort((a, b) => a - b)
          .map((L) => {
            const pts = o.series[L].slice().sort((a, b) => a.p - b.p);
            if (!pts.length) return null;
            const path = pts
              .map((pt, i) => `${i === 0 ? "M" : "L"}${xScale(pt.p).toFixed(2)},${yScale(pt.mean).toFixed(2)}`)
              .join(" ");
            return (
              <path
                key={`${o.id}-${L}`}
                d={path}
                fill="none"
                stroke={o.color}
                strokeWidth={1.6}
                strokeDasharray={OVERLAY_DASH}
                opacity={0.65}
              >
                <title>{`${o.label} · L = ${L}`}</title>
              </path>
            );
          })
      )}

      {/* live series */}
      {sizes.map((L) => {
        const pts = (series[L] ?? []).slice().sort((a, b) => a.p - b.p);
        if (!pts.length) return null;
        const color = L_COLORS[L] ?? "#10b981";
        const path = pts
          .map((pt, i) => `${i === 0 ? "M" : "L"}${xScale(pt.p).toFixed(2)},${yScale(pt.mean).toFixed(2)}`)
          .join(" ");
        return (
          <g key={L} className={busy ? "chart-busy" : undefined}>
            <path d={path} fill="none" stroke={color} strokeWidth={1.8} opacity={0.9} />
            {pts.map((pt, i) => {
              const x = xScale(pt.p);
              const y = yScale(pt.mean);
              const e = Math.max(yScale(pt.mean - pt.se) - y, 1);
              return (
                <g key={i}>
                  <line x1={x} x2={x} y1={y - e} y2={y + e} stroke={color} strokeWidth={1.2} opacity={0.8} />
                  <line x1={x - 3} x2={x + 3} y1={y - e} y2={y - e} stroke={color} strokeWidth={1.2} opacity={0.8} />
                  <line x1={x - 3} x2={x + 3} y1={y + e} y2={y + e} stroke={color} strokeWidth={1.2} opacity={0.8} />
                  <circle cx={x} cy={y} r={3.2} fill="#09090b" stroke={color} strokeWidth={1.6} />
                </g>
              );
            })}
          </g>
        );
      })}

      {/* hover crosshair */}
      {readout && (
        <g pointerEvents="none">
          <line
            x1={xScale(readout.p)} x2={xScale(readout.p)}
            y1={M.top} y2={H - M.bottom}
            stroke="currentColor" className="text-zinc-500" strokeWidth={1} strokeDasharray="3 3"
          />
          {readout.rows.map((r, i) => (
            <circle
              key={i}
              cx={xScale(readout.p)}
              cy={yScale(r.mean)}
              r={r.dashed ? 3 : 4}
              fill={r.dashed ? "#09090b" : r.color}
              stroke={r.color}
              strokeWidth={r.dashed ? 1.6 : 1.2}
            />
          ))}
          {/* readout card */}
          <g transform={`translate(${Math.min(xScale(readout.p) + 12, W - M.right - 190).toFixed(1)}, ${M.top + 4})`}>
            <rect
              width={186}
              height={20 + readout.rows.length * 14}
              rx={6}
              fill="#18181b"
              stroke="#3f3f46"
              strokeWidth={1}
              opacity={0.97}
            />
            <text x={8} y={14} className="fill-zinc-400 text-[10px] font-mono">p = {readout.p.toFixed(3)}</text>
            {readout.rows.map((r, i) => (
              <g key={i} transform={`translate(8, ${26 + i * 14})`}>
                <line x1={0} x2={10} y1={-3} y2={-3} stroke={r.color} strokeWidth={1.6} strokeDasharray={r.dashed ? OVERLAY_DASH : undefined} />
                <text x={14} y={0} className="fill-zinc-300 text-[10px] font-mono">
                  {r.dashed ? `${r.label.slice(0, 14)} · L${r.L}` : `L = ${r.L}`} : {r.mean.toFixed(2)}±{r.se.toFixed(2)}
                </text>
              </g>
            ))}
          </g>
        </g>
      )}

      {/* legend */}
      <g transform={`translate(${M.left + 8}, ${M.top + 26})`}>
        {sizes.map((L, i) => (
          <g key={L} transform={`translate(0, ${i * 16})`}>
            <circle cx={0} cy={-3} r={3.5} fill={L_COLORS[L] ?? "#10b981"} />
            <text x={9} y={0} className="fill-zinc-300 text-[11px] font-mono">L = {L}</text>
          </g>
        ))}
        {overlays.map((o, i) => (
          <g key={o.id} transform={`translate(0, ${(sizes.length + i) * 16})`}>
            <line x1={-2} x2={12} y1={-3} y2={-3} stroke={o.color} strokeWidth={1.6} strokeDasharray={OVERLAY_DASH} />
            <text x={17} y={0} className="fill-zinc-400 text-[11px] font-mono">{o.label.slice(0, 22)}</text>
          </g>
        ))}
        {crossings.length > 0 && (
          <g transform={`translate(0, ${(sizes.length + overlays.length) * 16})`}>
            <line x1={0} x2={12} y1={-3} y2={-3} stroke="#fb7185" strokeWidth={1} strokeDasharray="2 3" />
            <text x={17} y={0} className="fill-zinc-400 text-[11px] font-mono">your crossings</text>
          </g>
        )}
        {litBands.length > 0 && (
          <g transform={`translate(0, ${(sizes.length + overlays.length + (crossings.length > 0 ? 1 : 0)) * 16})`}>
            <rect x={-1} y={-7} width={14} height={8} fill={litBands[0].color} opacity={0.18} rx={1.5} />
            <text x={17} y={0} className="fill-zinc-400 text-[11px] font-mono">literature p_c (1σ)</text>
          </g>
        )}
      </g>
    </svg>
  );
}
