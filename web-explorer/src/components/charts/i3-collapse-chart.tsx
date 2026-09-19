"use client";

import { useMemo } from "react";
import type { SweepOverlay } from "./i3-sweep-chart";
import { L_COLORS, lerpScale, ticks, fmt } from "./chart-utils";

interface Props {
  /** series[L] = I₃ mean ± s.e. over a shared p-grid */
  series: Record<number, { p: number; mean: number; se: number }[]>;
  sizes: number[];
  pc: number;
  nu: number;
  /** saved sweeps to overlay (dashed) under the live points — collapsed with the same (p_c, ν) */
  overlays?: SweepOverlay[];
  height?: number;
}

const OVERLAY_DASH = "7 5";

/**
 * Finite-size-scaling collapse of the user's own I₃ sweep:
 * x = (p − p_c) · L^{1/ν}, y = ⟨I₃⟩ (negative — monogamy of entanglement).
 * Saved sweeps can be overlaid dashed at the same exponents, so two sweeps
 * can be compared directly in collapsed coordinates.
 */
export function I3CollapseChart({ series, sizes, pc, nu, overlays = [], height = 320 }: Props) {
  const W = 720;
  const H = height;
  const M = { top: 16, right: 16, bottom: 38, left: 52 };

  const { pts, overlayPaths, xScale, yScale, xs, ys } = useMemo(() => {
    const all: { x: number; y: number; L: number; se: number }[] = [];
    for (const L of sizes) {
      for (const pt of series[L] ?? []) {
        const x = (pt.p - pc) * Math.pow(L, 1 / nu);
        all.push({ x, y: pt.mean, L, se: pt.se });
      }
    }
    // overlay points at the same exponents — dashed, beneath the live curves
    const overlayPaths = overlays.map((o) => {
      const perL = Object.keys(o.series)
        .map(Number)
        .sort((a, b) => a - b)
        .map((L) => {
          const lp = (o.series[L] ?? [])
            .map((pt) => ({ x: (pt.p - pc) * Math.pow(L, 1 / nu), y: pt.mean, L }))
            .sort((a, b) => a.x - b.x);
          return { L, lp };
        })
        .filter(({ lp }) => lp.length > 0);
      return { o, perL };
    });
    // pure bounds: live points carry ±2σ error bars, overlay points are bare means
    const overlayFlat = overlayPaths.flatMap(({ perL }) => perL.flatMap(({ lp }) => lp));
    const xmax = Math.max(2.5, ...all.map((d) => Math.abs(d.x)), ...overlayFlat.map((d) => Math.abs(d.x))) * 1.06;
    const rawYmin = Math.min(...all.map((d) => d.mean - 2 * d.se), ...overlayFlat.map((d) => d.y));
    const rawYmax = Math.max(...all.map((d) => d.mean + 2 * d.se), ...overlayFlat.map((d) => d.y));
    const ymin = Number.isFinite(rawYmin) ? rawYmin : -1;
    const ymaxRaw = Number.isFinite(rawYmax) ? rawYmax : 0;
    const ymax = ymaxRaw - ymin < 1e-9 ? ymin + 1 : ymaxRaw;
    const ypad = (ymax - ymin) * 0.08;
    return {
      pts: all,
      overlayPaths,
      xScale: lerpScale(-xmax, xmax, M.left, W - M.right),
      yScale: lerpScale(ymin - ypad, ymax + ypad, H - M.bottom, M.top),
      xs: ticks(-Math.round(xmax), Math.round(xmax), 5),
      ys: ticks(ymin - ypad, ymax + ypad, 5),
    };
  }, [series, sizes, pc, nu, overlays, H]);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto select-none" role="img" aria-label="Finite-size scaling collapse of the I3 sweep">
      {ys.map((y, i) => (
        <g key={`gy${i}`}>
          <line x1={M.left} x2={W - M.right} y1={yScale(y)} y2={yScale(y)} stroke="currentColor" className="text-zinc-800" strokeWidth={1} strokeDasharray="3 5" />
          <line x1={M.left - 5} x2={M.left} y1={yScale(y)} y2={yScale(y)} stroke="currentColor" className="text-zinc-600" strokeWidth={1} />
          <text x={M.left - 8} y={yScale(y) + 4} textAnchor="end" className="fill-zinc-500 text-[11px] font-mono">{fmt(y, Math.abs(y) >= 10 ? 1 : 2)}</text>
        </g>
      ))}
      {xs.map((x, i) => (
        <g key={`tx${i}`}>
          <line x1={xScale(x)} x2={xScale(x)} y1={H - M.bottom} y2={H - M.bottom - 5} stroke="currentColor" className="text-zinc-600" strokeWidth={1} />
          <text x={xScale(x)} y={H - M.bottom + 18} textAnchor="middle" className="fill-zinc-500 text-[11px] font-mono">{x}</text>
        </g>
      ))}
      {/* plot frame baseline */}
      <line x1={M.left} x2={W - M.right} y1={H - M.bottom} y2={H - M.bottom} stroke="currentColor" className="text-zinc-700" strokeWidth={1} />
      {/* x = 0 axis */}
      <line x1={xScale(0)} x2={xScale(0)} y1={M.top} y2={H - M.bottom} stroke="currentColor" className="text-zinc-700" strokeWidth={1} />
      <text x={W / 2} y={H - 4} textAnchor="middle" className="fill-zinc-400 text-[11px]">x = (p − p_c) · L<tspan className="text-[9px]" dy="-4">1/ν</tspan></text>
      <text x={13} y={H / 2} textAnchor="middle" transform={`rotate(-90 13 ${H / 2})`} className="fill-zinc-400 text-[11px]">⟨I₃⟩ (bits)</text>

      {/* overlay sweeps first (dashed, beneath) */}
      {overlayPaths.map(({ o, perL }) =>
        perL.map(({ L, lp }) => {
          const d = lp.map((p, i) => `${i === 0 ? "M" : "L"}${xScale(p.x).toFixed(2)},${yScale(p.y).toFixed(2)}`).join(" ");
          return (
            <g key={`${o.id}-${L}`}>
              <path d={d} fill="none" stroke={o.color} strokeWidth={1.5} strokeDasharray={OVERLAY_DASH} opacity={0.55}>
                <title>{`${o.label} · L = ${L} (collapsed at your current p_c, ν)`}</title>
              </path>
              {lp.map((p, i) => (
                <circle key={i} cx={xScale(p.x)} cy={yScale(p.y)} r={2.2} fill="#09090b" stroke={o.color} strokeWidth={1.1} opacity={0.7} />
              ))}
            </g>
          );
        })
      )}

      {/* per-L connecting curves to visualise collapse quality */}
      {sizes.map((L) => {
        const lp = pts.filter((d) => d.L === L).sort((a, b) => a.x - b.x);
        if (!lp.length) return null;
        const d = lp.map((p, i) => `${i === 0 ? "M" : "L"}${xScale(p.x).toFixed(2)},${yScale(p.y).toFixed(2)}`).join(" ");
        return <path key={`c${L}`} d={d} fill="none" stroke={L_COLORS[L] ?? "#10b981"} strokeWidth={1.4} opacity={0.35} />;
      })}

      {/* scatter with tooltips */}
      {pts.map((d, i) => (
        <circle key={i} cx={xScale(d.x)} cy={yScale(d.y)} r={3.4} fill={L_COLORS[d.L] ?? "#10b981"} opacity={0.95}>
          <title>{`L = ${d.L}, ⟨I₃⟩ = ${d.y.toFixed(3)} ± ${d.se.toFixed(3)} bits, x = ${d.x.toFixed(2)}`}</title>
        </circle>
      ))}

      <g transform={`translate(${M.left + 8}, ${M.top + 4})`}>
        {sizes.map((L, i) => (
          <g key={L} transform={`translate(0, ${i * 16})`}>
            <circle cx={0} cy={-3} r={3.5} fill={L_COLORS[L] ?? "#10b981"} />
            <text x={9} y={0} className="fill-zinc-400 text-[11px] font-mono">L = {L}</text>
          </g>
        ))}
        {overlays.map((o, i) => (
          <g key={o.id} transform={`translate(0, ${(sizes.length + i) * 16})`}>
            <line x1={-2} x2={12} y1={-3} y2={-3} stroke={o.color} strokeWidth={1.6} strokeDasharray={OVERLAY_DASH} />
            <text x={17} y={0} className="fill-zinc-400 text-[11px] font-mono">{o.label.slice(0, 22)}</text>
          </g>
        ))}
      </g>
    </svg>
  );
}
