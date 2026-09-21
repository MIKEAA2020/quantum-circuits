"use client";

import { useMemo } from "react";
import { EMERALD, TEAL, ROSE, lerpScale, ticks, fmt } from "./chart-utils";

export interface LiveSeries {
  name: string;
  color: string;
  points: { t: number; v: number }[];
}

interface Props {
  series: LiveSeries[];
  height?: number;
  tauMax?: number;
  L?: number;
}

/** Live time-series chart for the simulator (entropies vs period t). */
export function LiveChart({ series, height = 260, tauMax = 2, L = 16 }: Props) {
  const W = 720;
  const H = height;
  const M = { top: 18, right: 18, bottom: 36, left: 52 };

  const { xs, ys, xScale, yScale } = useMemo(() => {
    const all = series.flatMap((s) => s.points);
    const tmax = Math.max(L * tauMax, ...all.map((p) => p.t), 8);
    let vmin = Math.min(0, ...all.map((p) => p.v));
    let vmax = Math.max(L / 2, ...all.map((p) => p.v), 1);
    if (vmax - vmin < 1e-9) vmax = vmin + 1;
    const pad = (vmax - vmin) * 0.06;
    vmin = vmin - pad;
    vmax = vmax + pad;
    return {
      xs: ticks(0, tmax, 6),
      ys: ticks(vmin, vmax, 5),
      xScale: lerpScale(0, tmax, M.left, W - M.right),
      yScale: lerpScale(vmin, vmax, H - M.bottom, M.top),
    };
  }, [series, H, L, tauMax]);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto select-none" role="img" aria-label="Simulator time series">
      {ys.map((y, i) => (
        <g key={`gy${i}`}>
          <line x1={M.left} x2={W - M.right} y1={yScale(y)} y2={yScale(y)} stroke="currentColor" className="text-zinc-800" strokeWidth={1} />
          <text x={M.left - 8} y={yScale(y) + 4} textAnchor="end" className="fill-zinc-500 text-[11px] font-mono">{fmt(y, 1)}</text>
        </g>
      ))}
      {xs.map((x, i) => (
        <g key={`tx${i}`}>
          <text x={xScale(x)} y={H - M.bottom + 18} textAnchor="middle" className="fill-zinc-500 text-[11px] font-mono">{x}</text>
        </g>
      ))}
      {/* τ = t/L markers */}
      {Array.from({ length: tauMax + 1 }, (_, k) => k).filter((k) => k >= 1 && k * L >= 1).map((k) => (
        <g key={`tau${k}`}>
          <line x1={xScale(k * L)} x2={xScale(k * L)} y1={M.top} y2={H - M.bottom} stroke="currentColor" className="text-zinc-700" strokeWidth={1} strokeDasharray="3 4" />
          <text x={xScale(k * L) + 4} y={M.top + 10} className="fill-zinc-600 text-[10px] font-mono">τ={k}</text>
        </g>
      ))}
      <text x={W / 2} y={H - 4} textAnchor="middle" className="fill-zinc-400 text-[11px]">periods t (circuit depth)</text>
      <text x={13} y={H / 2} textAnchor="middle" transform={`rotate(-90 13 ${H / 2})`} className="fill-zinc-400 text-[11px]">
        {series.some((s) => s.name.includes("I₃")) ? "bits (I₃ < 0: monogamy)" : "entropy (bits)"}
      </text>

      {series.map((s) => {
        if (s.points.length < 1) return null;
        const d = s.points.map((p, i) => `${i === 0 ? "M" : "L"}${xScale(p.t).toFixed(2)},${yScale(p.v).toFixed(2)}`).join(" ");
        const last = s.points[s.points.length - 1];
        return (
          <g key={s.name}>
            <path d={d} fill="none" stroke={s.color} strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" />
            <circle cx={xScale(last.t)} cy={yScale(last.v)} r={4} fill={s.color} />
          </g>
        );
      })}

      {/* legend */}
      <g transform={`translate(${W - M.right - 150}, ${M.top + 2})`}>
        {series.map((s, i) => (
          <g key={s.name} transform={`translate(0, ${i * 16})`}>
            <line x1={0} x2={16} y1={-4} y2={-4} stroke={s.color} strokeWidth={2} />
            <text x={21} y={0} className="fill-zinc-400 text-[11px] font-mono">{s.name}</text>
          </g>
        ))}
      </g>
    </svg>
  );
}

export const SERIES_COLORS = { sA: EMERALD, sRef: TEAL, i3: ROSE };
