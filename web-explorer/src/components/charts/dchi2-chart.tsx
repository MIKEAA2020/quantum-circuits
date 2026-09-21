"use client";

import { useMemo } from "react";
import { lerpScale } from "./chart-utils";

interface Props {
  data: { nu: number; dchi2: number }[];
  height?: number;
}

/** Frozen-ν Δχ² profile on a log scale; highlights the minimum. */
export function Dchi2Chart({ data, height = 260 }: Props) {
  const W = 720;
  const H = height;
  const M = { top: 24, right: 16, bottom: 40, left: 52 };

  const { bars, yScale } = useMemo(() => {
    const lo = Math.min(...data.map((d) => d.dchi2), 0.08);
    const hi = Math.max(...data.map((d) => d.dchi2), 10) * 1.6;
    const l0 = Math.log10(lo);
    const l1 = Math.log10(hi);
    const yS = lerpScale(l0, l1, H - M.bottom, M.top);
    const n = data.length;
    const band = (W - M.left - M.right) / n;
    const bw = Math.min(64, band * 0.56);
    const minD = Math.min(...data.map((d) => d.dchi2));
    const bars = data.map((d, i) => {
      const yVal = Math.max(d.dchi2, lo);
      return {
        ...d,
        x: M.left + band * i + band / 2 - bw / 2,
        bw,
        y: yS(Math.log10(yVal)),
        isMin: Math.abs(d.dchi2 - minD) < 1e-9,
      };
    });
    return { bars, yScale: yS };
  }, [data, H]);

  const logTicks = [0.1, 1, 10, 100, 1000].filter(
    (v) => v >= Math.pow(10, Math.log10(Math.min(...data.map((d) => d.dchi2), 0.08))) &&
           v <= Math.pow(10, Math.log10(Math.max(...data.map((d) => d.dchi2), 10)) * 1.6)
  );

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto select-none" role="img" aria-label="Frozen-nu delta chi-squared profile">
      {logTicks.map((v, i) => (
        <g key={i}>
          <line x1={M.left} x2={W - M.right} y1={yScale(Math.log10(v))} y2={yScale(Math.log10(v))} stroke="currentColor" className="text-zinc-800" strokeWidth={1} />
          <text x={M.left - 8} y={yScale(Math.log10(v)) + 4} textAnchor="end" className="fill-zinc-500 text-[11px] font-mono">{v}</text>
        </g>
      ))}
      <text x={W / 2} y={H - 4} textAnchor="middle" className="fill-zinc-400 text-[11px]">frozen ν</text>
      <text x={13} y={H / 2} textAnchor="middle" transform={`rotate(-90 13 ${H / 2})`} className="fill-zinc-400 text-[11px]">Δχ² (log scale)</text>

      {bars.map((b, i) => (
        <g key={i}>
          <rect
            x={b.x}
            y={b.y}
            width={b.bw}
            height={Math.max(H - M.bottom - b.y, 2)}
            rx={4}
            fill={b.isMin ? "#10b981" : b.dchi2 > 25 ? "#fb7185" : "#f59e0b"}
            opacity={b.isMin ? 0.95 : 0.75}
          >
            <title>{`ν = ${b.nu === 4 / 3 ? "4/3" : b.nu.toFixed(2)}: Δχ² = ${b.dchi2}`}</title>
          </rect>
          <text x={b.x + b.bw / 2} y={H - M.bottom + 16} textAnchor="middle" className="fill-zinc-400 text-[11px] font-mono">
            {b.nu === 4 / 3 ? "4/3" : b.nu.toFixed(2)}
          </text>
          <text
            x={b.x + b.bw / 2}
            y={b.y - 6}
            textAnchor="middle"
            className={`text-[10px] font-mono ${b.isMin ? "fill-emerald-400" : "fill-zinc-500"}`}
          >
            {b.dchi2 >= 100 ? b.dchi2.toFixed(0) : b.dchi2 >= 10 ? b.dchi2.toFixed(1) : b.dchi2.toFixed(1)}
          </text>
        </g>
      ))}
    </svg>
  );
}
