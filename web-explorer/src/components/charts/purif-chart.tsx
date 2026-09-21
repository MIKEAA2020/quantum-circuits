"use client";

import { useMemo } from "react";
import type { PurifPoint } from "@/lib/research-data";
import { L_COLORS, ACCENT, lerpScale, ticks, fmt } from "./chart-utils";

interface Props {
  series: Record<number, PurifPoint[]>;
  sizes: number[];
  showPc?: boolean;
  pc?: number;
  height?: number;
}

/** Multi-series plot of <S_ref>(p) with error bars, one series per system size. */
export function PurifChart({ series, sizes, showPc = true, pc = 0.1597, height = 340 }: Props) {
  const W = 720;
  const H = height;
  const M = { top: 16, right: 16, bottom: 38, left: 52 };

  const { xs, ys, xScale, yScale, ymax } = useMemo(() => {
    let xmin = Infinity, xmax = -Infinity, ymin = Infinity, ymax2 = -Infinity;
    for (const L of sizes) {
      for (const pt of series[L] ?? []) {
        xmin = Math.min(xmin, pt.p);
        xmax = Math.max(xmax, pt.p);
        ymin = Math.min(ymin, pt.mean - 2 * pt.se);
        ymax2 = Math.max(ymax2, pt.mean + 2 * pt.se);
      }
    }
    const pad = (xmax - xmin) * 0.04;
    const x0 = xmin - pad, x1 = xmax + pad;
    const y0 = Math.max(0, ymin - (ymax2 - ymin) * 0.06);
    const y1 = ymax2 * 1.04;
    return {
      xs: ticks(x0, x1, 6),
      ys: ticks(y0, y1, 5),
      xScale: lerpScale(x0, x1, M.left, W - M.right),
      yScale: lerpScale(y0, y1, H - M.bottom, M.top),
      ymax: y1,
    };
  }, [series, sizes, H]);

  void ymax;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto select-none" role="img" aria-label="Purification entropy versus measurement probability for several system sizes">
      {/* grid */}
      {ys.map((y, i) => (
        <g key={`gy${i}`}>
          <line x1={M.left} x2={W - M.right} y1={yScale(y)} y2={yScale(y)} stroke="currentColor" className="text-zinc-800" strokeWidth={1} />
          <text x={M.left - 8} y={yScale(y) + 4} textAnchor="end" className="fill-zinc-500 text-[11px] font-mono">{fmt(y, y > 10 ? 1 : 2)}</text>
        </g>
      ))}
      {xs.map((x, i) => (
        <text key={`tx${i}`} x={xScale(x)} y={H - M.bottom + 18} textAnchor="middle" className="fill-zinc-500 text-[11px] font-mono">{x.toFixed(3)}</text>
      ))}
      <text x={W / 2} y={H - 4} textAnchor="middle" className="fill-zinc-400 text-[11px]">measurement probability p</text>
      <text x={13} y={H / 2} textAnchor="middle" transform={`rotate(-90 13 ${H / 2})`} className="fill-zinc-400 text-[11px]">⟨S_ref⟩ (bits)</text>

      {/* p_c line */}
      {showPc && pc > 0 && (
        <g>
          <line x1={xScale(pc)} x2={xScale(pc)} y1={M.top} y2={H - M.bottom} stroke={ACCENT} strokeWidth={1.5} strokeDasharray="6 4" opacity={0.9} />
          <text x={xScale(pc) + 6} y={M.top + 12} className="fill-amber-500 text-[11px] font-mono">p_c = 0.1597</text>
        </g>
      )}

      {/* series */}
      {sizes.map((L) => {
        const pts = (series[L] ?? []).slice().sort((a, b) => a.p - b.p);
        if (!pts.length) return null;
        const color = L_COLORS[L] ?? "#10b981";
        const path = pts.map((pt, i) => `${i === 0 ? "M" : "L"}${xScale(pt.p).toFixed(2)},${yScale(pt.mean).toFixed(2)}`).join(" ");
        return (
          <g key={L}>
            <path d={path} fill="none" stroke={color} strokeWidth={1.8} opacity={0.85} />
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

      {/* legend */}
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
