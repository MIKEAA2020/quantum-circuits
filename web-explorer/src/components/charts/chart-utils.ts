"use client";

/** Shared chart utilities: scales, palettes, tick formatting. */

export const L_COLORS: Record<number, string> = {
  8: "#a7f3d0",
  16: "#6ee7b7",
  32: "#34d399",
  64: "#10b981",
  128: "#059669",
  256: "#047857",
};

export const ACCENT = "#f59e0b"; // amber — critical point
export const ROSE = "#fb7185";
export const TEAL = "#2dd4bf";
export const EMERALD = "#10b981";

export function lerpScale(d0: number, d1: number, r0: number, r1: number) {
  const span = d1 - d0 || 1;
  return (v: number) => r0 + ((v - d0) / span) * (r1 - r0);
}

export function ticks(min: number, max: number, count = 5): number[] {
  const out: number[] = [];
  const step = (max - min) / (count - 1);
  // round away float dust (e.g. 19.200000000000003 → 19.2) using a precision
  // derived from the step size: one guard digit below the step's own scale
  const decimals = Math.max(0, Math.min(10, Math.ceil(-Math.log10(step)) + 1));
  for (let i = 0; i < count; i++) out.push(Number((min + step * i).toFixed(decimals)));
  return out;
}

export function fmt(v: number, digits = 3): string {
  if (Math.abs(v) >= 1000) return v.toFixed(0);
  return v.toFixed(digits);
}
