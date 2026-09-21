"use client";

import { useState } from "react";
import { lerpScale, ticks } from "./chart-utils";
import type { ProfileBandPoint } from "@/lib/stats/collapse";

/** Normalised profile point — v is ν or p_c depending on mode. */
export interface ProfileViewPoint {
  v: number;
  dchi2: number;
  /** the re-optimised nuisance at this v (best p_c or best ν) */
  bestOther: number;
}

interface Props {
  mode: "nu" | "pc";
  points: ProfileViewPoint[];
  sigma: { lo: number | null; hi: number | null };
  /** bootstrap 68% envelope + median of Δχ²(v) across resamples (optional) */
  band?: ProfileBandPoint[] | null;
  /** resample count behind the band (label) */
  bootB?: number | null;
  height?: number;
}

/** Colors: amber line, emerald minimum / 1σ band, rose exclusion zone. */
const C = {
  line: "#f59e0b",
  min: "#10b981",
  ref: "#34d399",
  excl: "#fb7185",
};

/** Literature references drawn as dashed vertical lines, per mode. */
const REFS: Record<Props["mode"], { v: number; label: string; kind: "emerald" | "rose" }[]> = {
  nu: [
    { v: 1.24, label: "deposited ν = 1.24", kind: "emerald" },
    { v: 1.0, label: "ν = 1", kind: "rose" },
  ],
  pc: [
    { v: 0.1597, label: "deposited p_c = 0.1597", kind: "emerald" },
    { v: 0.1593, label: "GH p_c = 0.1593", kind: "rose" },
  ],
};

/**
 * Δχ² profile of the user's own sweep (log y-scale): at each value of the
 * profiled parameter the χ² is minimised over the other one; Δχ² = χ² − χ²_min.
 * The Δχ² = 1 crossings give the 1σ interval — the same construction behind
 * the deposited ν = 1.24(7), the ν = 1 exclusion at Δχ² ≥ 52, and p_c = 0.1597(8).
 */
export function Dchi2ProfileChart({ mode, points, sigma, band, bootB, height = 300 }: Props) {
  const W = 720;
  const H = height;
  const M = { top: 22, right: 18, bottom: 42, left: 52 };
  const isNu = mode === "nu";

  const [hover, setHover] = useState<number | null>(null); // profiled value under cursor

  // scales + path (auto-memoised by the React compiler)
  const data = points;
  const vs = data.map((d) => d.v);
  const vmin = Math.min(...vs);
  const vmax = Math.max(...vs);
  const vPad = isNu ? 0.02 : (vmax - vmin) * 0.04;
  const vLo = vmin - vPad;
  const vHi = vmax + vPad;
  // log-y window: adaptive floor below the smallest nonzero Δχ² (a fixed
  // floor would clamp the near-minimum points onto one pixel), top with headroom
  const positives = data.map((d) => d.dchi2).filter((v) => v > 0);
  const lo = positives.length ? Math.min(0.25, Math.min(...positives) / 2) : 0.1;
  const hi = Math.max(...data.map((d) => d.dchi2), 30) * 1.5;
  const yScale = lerpScale(Math.log10(lo), Math.log10(hi), H - M.bottom, M.top);
  const xScale = lerpScale(vLo, vHi, M.left, W - M.right);
  const sorted = data.slice().sort((a, b) => a.v - b.v);
  const path = sorted
    .map((d, i) => `${i === 0 ? "M" : "L"}${xScale(d.v).toFixed(2)},${yScale(Math.log10(Math.max(d.dchi2, lo))).toFixed(2)}`)
    .join(" ");
  const logTicks = [0.1, 0.25, 0.5, 1, 2, 5, 10, 30, 100, 300, 1000, 3000].filter(
    (v) => v >= lo && v <= hi
  );
  const minPt = data.reduce((m, d) => (d.dchi2 < m.dchi2 ? d : m), data[0]);
  const d25 = yScale(Math.log10(25));

  // x grid: fixed ν ladder, or p-range-derived ticks
  const xGrid = isNu
    ? [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
    : ticks(vmin, vmax, 6);

  const yOf = (d: number) => yScale(Math.log10(Math.max(d, lo)));
  // keep the minimum marker + label clear of the axis floor
  const minY = Math.min(yOf(minPt.dchi2), H - M.bottom - 7);
  // band values can shoot past the plot top — clamp into the frame
  const yBand = (d: number) => Math.min(Math.max(yOf(d), M.top), H - M.bottom);

  // 1σ band region (x-pixels)
  const bandX0 = sigma.lo != null ? xScale(sigma.lo) : null;
  const bandX1 = sigma.hi != null ? xScale(sigma.hi) : null;

  const hoverPt = hover != null
    ? sorted.reduce((best, d) => (Math.abs(d.v - hover) < Math.abs(best.v - hover) ? d : best), sorted[0])
    : null;

  const fmtV = (v: number) => (isNu ? v.toFixed(2) : v.toFixed(4));

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      className="w-full h-auto select-none"
      role="img"
      aria-label={isNu ? "Frozen-nu delta chi-squared profile of your sweep" : "p_c delta chi-squared profile of your sweep"}
      onMouseMove={(e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * W;
        const v = ((x - M.left) / (W - M.right - M.left)) * (vHi - vLo) + vLo;
        setHover(Math.min(Math.max(v, sorted[0].v), sorted[sorted.length - 1].v));
      }}
      onMouseLeave={() => setHover(null)}
    >
      {/* horizontal grid + log ticks */}
      {logTicks.map((v, i) => (
        <g key={i}>
          <line
            x1={M.left} x2={W - M.right} y1={yScale(Math.log10(v))} y2={yScale(Math.log10(v))}
            stroke="currentColor"
            className={v === 1 ? "text-zinc-600" : "text-zinc-800"}
            strokeWidth={v === 1 ? 1 : 1}
            strokeDasharray={v === 1 ? "4 3" : "3 5"}
          />
          <line x1={M.left - 5} x2={M.left} y1={yScale(Math.log10(v))} y2={yScale(Math.log10(v))} stroke="currentColor" className="text-zinc-600" strokeWidth={1} />
          <text x={M.left - 8} y={yScale(Math.log10(v)) + 4} textAnchor="end" className="fill-zinc-500 text-[11px] font-mono">
            {v}
          </text>
        </g>
      ))}
      {/* vertical grid */}
      {xGrid.map((v, i) => (
        <g key={i}>
          <line x1={xScale(v)} x2={xScale(v)} y1={M.top} y2={H - M.bottom} stroke="currentColor" className="text-zinc-800/60" strokeWidth={1} strokeDasharray="3 5" />
          <line x1={xScale(v)} x2={xScale(v)} y1={H - M.bottom} y2={H - M.bottom - 5} stroke="currentColor" className="text-zinc-600" strokeWidth={1} />
          <text x={xScale(v)} y={H - M.bottom + 16} textAnchor="middle" className="fill-zinc-500 text-[11px] font-mono">
            {isNu ? v.toFixed(1) : v.toFixed(3)}
          </text>
        </g>
      ))}
      <line x1={M.left} x2={W - M.right} y1={H - M.bottom} y2={H - M.bottom} stroke="currentColor" className="text-zinc-700" strokeWidth={1} />
      <text x={W / 2} y={H - 5} textAnchor="middle" className="fill-zinc-400 text-[11px]">
        {isNu ? "frozen ν (p_c re-optimised at every ν)" : "p_c (ν re-optimised at every p_c)"}
      </text>
      {band && band.length >= 2 && (
        <text x={M.left} y={H - 5} className="fill-amber-500/70 text-[10px] font-mono">
          ┄ bootstrap median · 68% band
        </text>
      )}
      <text x={13} y={H / 2} textAnchor="middle" transform={`rotate(-90 13 ${H / 2})`} className="fill-zinc-400 text-[11px]">Δχ² (log scale)</text>

      {/* 1σ band */}
      {bandX0 != null && bandX1 != null && (
        <g>
          <rect x={bandX0} y={M.top} width={Math.max(bandX1 - bandX0, 1)} height={H - M.bottom - M.top} fill={C.min} opacity={0.07} />
          <text x={(bandX0 + bandX1) / 2} y={M.top + 12} textAnchor="middle" className="fill-emerald-400/80 text-[10px] font-mono">
            1σ
          </text>
        </g>
      )}

      {/* Δχ² = 25 exclusion zone tint */}
      <rect x={M.left} y={M.top} width={W - M.right - M.left} height={Math.max(d25 - M.top, 0)} fill={C.excl} opacity={0.05} />
      {d25 > M.top && (
        <text x={W - M.right - 6} y={d25 - 5} textAnchor="end" className="fill-rose-400/70 text-[10px] font-mono">
          Δχ² = 25 · strong exclusion
        </text>
      )}

      {/* literature reference lines */}
      {REFS[mode].map((r) => {
        if (r.v < vLo || r.v > vHi) return null;
        const x = xScale(r.v);
        return (
          <g key={r.v}>
            <line x1={x} x2={x} y1={M.top} y2={H - M.bottom} stroke={r.kind === "emerald" ? C.ref : C.excl} strokeWidth={1} strokeDasharray="2 4" opacity={r.kind === "emerald" ? 0.7 : 0.55} />
            <text
              x={x + 4}
              y={r.kind === "emerald" ? H - M.bottom - 8 : M.top + 14}
              className={r.kind === "emerald" ? "fill-emerald-500/80 text-[10px] font-mono" : "fill-rose-400/80 text-[10px] font-mono"}
            >
              {r.label}
            </text>
          </g>
        );
      })}

      {/* the bootstrap band (behind the main curve): 68% envelope + median */}
      {band && band.length >= 2 && (
        <g pointerEvents="none">
          <path
            d={
              "M" +
              band.map((b) => `${xScale(b.v).toFixed(2)},${yBand(b.hi).toFixed(2)}`).join(" L") +
              " L" +
              band.slice().reverse().map((b) => `${xScale(b.v).toFixed(2)},${yBand(b.lo).toFixed(2)}`).join(" L") +
              " Z"
            }
            fill={C.line}
            opacity={0.1}
          />
          <path
            d={band.map((b, i) => `${i === 0 ? "M" : "L"}${xScale(b.v).toFixed(2)},${yBand(b.med).toFixed(2)}`).join(" ")}
            fill="none"
            stroke={C.line}
            strokeWidth={1.2}
            strokeDasharray="4 4"
            opacity={0.5}
          />
        </g>
      )}

      {/* the profile curve + area fill */}
      <path d={`${path} L${xScale(sorted[sorted.length - 1].v).toFixed(2)},${(H - M.bottom).toFixed(2)} L${xScale(sorted[0].v).toFixed(2)},${(H - M.bottom).toFixed(2)} Z`} fill={C.line} opacity={0.08} />
      <path d={path} fill="none" stroke={C.line} strokeWidth={2} />

      {/* minimum marker */}
      <g>
        <circle cx={xScale(minPt.v)} cy={minY} r={4.5} fill="#09090b" stroke={C.min} strokeWidth={2} />
        <text x={xScale(minPt.v)} y={minY - 9} textAnchor="middle" className="fill-emerald-400 text-[10px] font-mono">
          {isNu ? "ν̂" : "p̂_c"} = {fmtV(minPt.v)}
        </text>
      </g>

      {/* hover guide */}
      {hoverPt && (
        <g pointerEvents="none">
          <line x1={xScale(hoverPt.v)} x2={xScale(hoverPt.v)} y1={M.top} y2={H - M.bottom} stroke="currentColor" className="text-zinc-500" strokeWidth={1} strokeDasharray="3 3" />
          <circle cx={xScale(hoverPt.v)} cy={yOf(hoverPt.dchi2)} r={3.5} fill={C.line} stroke="#09090b" strokeWidth={1.5} />
          <g transform={`translate(${Math.min(xScale(hoverPt.v) + 10, W - M.right - 150).toFixed(1)}, ${M.top + 6})`}>
            <rect width={140} height={44} rx={6} fill="#18181b" stroke="#3f3f46" strokeWidth={1} opacity={0.97} />
            <text x={8} y={16} className="fill-zinc-300 text-[10px] font-mono">
              {isNu ? "ν" : "p_c"} = {fmtV(hoverPt.v)} · Δχ² = {hoverPt.dchi2 < 10 ? hoverPt.dchi2.toFixed(2) : hoverPt.dchi2.toFixed(0)}
            </text>
            <text x={8} y={32} className="fill-zinc-500 text-[10px] font-mono">
              {isNu ? "best p_c" : "best ν"} = {isNu ? hoverPt.bestOther.toFixed(4) : hoverPt.bestOther.toFixed(2)}
            </text>
          </g>
        </g>
      )}
    </svg>
  );
}
