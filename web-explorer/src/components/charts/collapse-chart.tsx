"use client";

import { useMemo } from "react";
import type { PurifPoint } from "@/lib/research-data";
import { L_COLORS, lerpScale, ticks, fmt } from "./chart-utils";

interface Props {
  series: Record<number, PurifPoint[]>;
  sizes: number[];
  pc: number;
  nu: number;
  height?: number;
}

/** Finite-size-scaling collapse: x = (p - p_c) L^{1/nu}, y = <S_ref>. */
export function CollapseChart({ series, sizes, pc, nu, height = 340 }: Props) {
  const W = 720;
  const H = height;
  const M = { top: 16, right: 16, bottom: 38, left: 52 };

  const { pts, xScale, yScale, xs, ys } = useMemo(() => {
    const all: { x: number; y: number; L: number; se: number }[] = [];
    let ymin = Infinity, ymax = -Infinity;
    for (const L of sizes) {
      for (const pt of series[L] ?? []) {
        const x = (pt.p - pc) * Math.pow(L, 1 / nu);
        all.push({ x, y: pt.mean, L, se: pt.se });
        ymin = Math.min(ymin, pt.mean - 2 * pt.se);
        ymax = Math.max(ymax, pt.mean + 2 * pt.se);
      }
    }
    const xmax = Math.max(2.2, ...all.map((d) => Math.abs(d.x))) * 1.06;
    const y0 = Math.max(0, ymin - (ymax - ymin) * 0.06);
    const y1 = ymax * 1.04;
    return {
      pts: all,
      xScale: lerpScale(-xmax, xmax, M.left, W - M.right),
      yScale: lerpScale(y0, y1, H - M.bottom, M.top),
      xs: ticks(-Math.round(xmax), Math.round(xmax), 5),
      ys: ticks(y0, y1, 5),
    };
  }, [series, sizes, pc, nu, H]);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto select-none" role="img" aria-label="Finite-size scaling collapse plot">
      {ys.map((y, i) => (
        <g key={`gy${i}`}>
          <line x1={M.left} x2={W - M.right} y1={yScale(y)} y2={yScale(y)} stroke="currentColor" className="text-zinc-800" strokeWidth={1} />
          <text x={M.left - 8} y={yScale(y) + 4} textAnchor="end" className="fill-zinc-500 text-[11px] font-mono">{fmt(y, y > 10 ? 1 : 2)}</text>
        </g>
      ))}
      {xs.map((x, i) => (
        <text key={`tx${i}`} x={xScale(x)} y={H - M.bottom + 18} textAnchor="middle" className="fill-zinc-500 text-[11px] font-mono">{x}</text>
      ))}
      {/* x = 0 axis */}
      <line x1={xScale(0)} x2={xScale(0)} y1={M.top} y2={H - M.bottom} stroke="currentColor" className="text-zinc-700" strokeWidth={1} />
      <text x={W / 2} y={H - 4} textAnchor="middle" className="fill-zinc-400 text-[11px]">x = (p − p_c) · L<tspan className="text-[9px]" dy="-4">1/ν</tspan></text>
      <text x={13} y={H / 2} textAnchor="middle" transform={`rotate(-90 13 ${H / 2})`} className="fill-zinc-400 text-[11px]">⟨S_ref⟩ (bits)</text>

      {/* per-L connecting curves to visualise collapse quality */}
      {sizes.map((L) => {
        const lp = pts
          .filter((d) => d.L === L)
          .sort((a, b) => a.x - b.x);
        if (!lp.length) return null;
        const d = lp.map((p, i) => `${i === 0 ? "M" : "L"}${xScale(p.x).toFixed(2)},${yScale(p.y).toFixed(2)}`).join(" ");
        return <path key={`c${L}`} d={d} fill="none" stroke={L_COLORS[L] ?? "#10b981"} strokeWidth={1.4} opacity={0.35} />;
      })}

      {/* scatter */}
      {pts.map((d, i) => (
        <circle key={i} cx={xScale(d.x)} cy={yScale(d.y)} r={3.4} fill={L_COLORS[d.L] ?? "#10b981"} opacity={0.95}>
          <title>{`L = ${d.L}, ⟨S_ref⟩ = ${d.y.toFixed(3)} ± ${d.se.toFixed(3)} bits, x = ${d.x.toFixed(2)}`}</title>
        </circle>
      ))}

      <g transform={`translate(${M.left + 8}, ${M.top + 4})`}>
        {sizes.map((L, i) => (
          <g key={L} transform={`translate(0, ${i * 16})`}>
            <circle cx={0} cy={-3} r={3.5} fill={L_COLORS[L] ?? "#10b981"} />
            <text x={9} y={0} className="fill-zinc-400 text-[11px] font-mono">L = {L}</text>
          </g>
        ))}
      </g>
    </svg>
  );
}
