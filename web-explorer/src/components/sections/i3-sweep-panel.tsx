"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Crosshair, Loader2, Copy, Check, AlertTriangle, SlidersHorizontal, Sparkles, Save, Trash2, FolderOpen, GitCompare, LineChart, Download, Upload, FlaskConical, Link2, BarChart3, RefreshCw } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { I3SweepChart, type I3SeriesPoint, type SweepOverlay, type LitBand } from "@/components/charts/i3-sweep-chart";
import { I3CollapseChart } from "@/components/charts/i3-collapse-chart";
import { Dchi2ProfileChart, type ProfileViewPoint } from "@/components/charts/dchi2-profile-chart";
import { lerpScale } from "@/components/charts/chart-utils";
import { collapseQuality, dchi2Profile, dchi2ProfilePc, pGrid, dominantCrossing, bootstrapCrossing, bootstrapProfileIter, type Dchi2Profile, type Dchi2PcProfile, type CrossingBootstrap, type ProfileBootstrap } from "@/lib/stats/collapse";

const L_CHOICES = [8, 16, 32, 64, 128, 256];
const LARGE_L = 128; // ≥ this → background job (POST /api/jobs + polling)
const JOB_POLL_MS = 650;
const PC_REF = 0.1597;
const NU_REF = 1.24;

/** p-grid presets — the API accepts any 3–9 values in [0, 0.5]. */
const P_PRESETS = {
  wide: { label: "wide", hint: "0.08–0.24 · both phases", min: 0.08, max: 0.24, n: 9 },
  zoom: { label: "critical zoom", hint: "0.13–0.19 · around p_c", min: 0.13, max: 0.19, n: 9 },
  fine: { label: "fine", hint: "0.145–0.175 · crossing detail", min: 0.145, max: 0.175, n: 9 },
} as const;
type PresetKey = keyof typeof P_PRESETS;

/** dashed-overlay colors for saved sweeps (distinct from emerald L palette + amber p_c). */
const OVERLAY_COLORS = ["#fb7185", "#c084fc", "#fb923c"];

/** literature p_c estimates for the comparison overlay (quoted verbatim from the
 *  deposited comparison table — this work / Gullans–Huse / Sierant). */
const LIT_BANDS: { id: string; label: string; pc: number; err: number; color: string }[] = [
  { id: "this", label: "this work 0.1597(8)", pc: 0.1597, err: 0.0008, color: "#fbbf24" },
  { id: "gh", label: "Gullans–Huse 0.1593(5)", pc: 0.1593, err: 0.0005, color: "#c084fc" },
  { id: "sierant", label: "Sierant 0.15995(10)", pc: 0.15995, err: 0.001, color: "#fb923c" },
];

interface SweepResponse {
  L: number;
  tau: number;
  nTraj: number;
  elapsedMs: number;
  points: I3SeriesPoint[];
  /** per-p trajectory values, aligned with points (non-parametric bootstrap) */
  traj?: number[][];
}

/** poll payload of a background large-L job (partial results included) */
interface SweepJobStatus {
  id: string;
  status: "queued" | "running" | "done" | "error";
  L: number;
  tau: number;
  nTraj: number;
  ps: number[];
  points: I3SeriesPoint[];
  traj?: number[][];
  total: number;
  error?: string;
  elapsedMs: number;
}

/** exported sweep-state JSON (exact reproduction of a explorer session) */
interface SweepStateJson {
  version: 1;
  kind: "i3-sweep-state";
  sizes: number[];
  tau: number;
  nTraj: number;
  pc: number;
  nu: number;
  series: Record<string, I3SeriesPoint[]>;
  traj?: Record<string, number[][]>;
}

interface SavedSweep {
  id: string;
  label: string;
  tau: number;
  nTraj: number;
  sizes: string;
  seriesJson: string;
  /** present on single-sweep fetches (?id=): per-trajectory values for non-parametric bootstraps */
  trajJson?: string | null;
  /** present on list fetches: whether the stored record carries trajectory data */
  hasTraj?: boolean;
  createdAt: string;
}

/** Clipboard write with a hidden-textarea fallback (headless / older browsers). */
async function copyText(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    try {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand("copy");
      document.body.removeChild(ta);
      return ok;
    } catch {
      return false;
    }
  }
}

/** Save text as a downloaded file (Blob + object URL). */
function downloadTextFile(filename: string, text: string): boolean {
  try {
    const blob = new Blob([text], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    return true;
  } catch {
    return false;
  }
}

/** Mini illustration for the empty state: two I₃-like curves crossing near p_c. */
function EmptySketch() {
  return (
    <svg width="180" height="72" viewBox="0 0 180 72" aria-hidden className="opacity-70">
      <line x1="14" y1="8" x2="14" y2="62" stroke="#27272a" strokeWidth="1" />
      <line x1="14" y1="62" x2="172" y2="62" stroke="#27272a" strokeWidth="1" />
      <line x1="104" y1="8" x2="104" y2="62" stroke="#f59e0b" strokeWidth="1.2" strokeDasharray="5 4" opacity="0.8" />
      <path d="M18,58 C50,58 70,50 104,40 C140,30 160,26 170,25" fill="none" stroke="#6ee7b7" strokeWidth="1.8" />
      <path d="M18,54 C50,54 70,42 104,30 C140,18 160,12 170,10" fill="none" stroke="#34d399" strokeWidth="1.8" />
      <circle cx="104" cy="35" r="3" fill="#09090b" stroke="#fb7185" strokeWidth="1.6" />
      <text x="108" y="18" className="fill-amber-500/90 text-[9px] font-mono">p_c</text>
    </svg>
  );
}

/** Tiny sparkline of a saved sweep's smallest-L mean curve (board-row identity at a glance). */
function SweepSparkline({ seriesJson }: { seriesJson: string }) {
  // parse + scale inside a plain helper (no JSX in try/catch — error-boundary rule)
  const data = (() => {
    try {
      const parsed = JSON.parse(seriesJson) as Record<string, { p: number; mean: number }[]>;
      const Ls = Object.keys(parsed).map(Number).sort((a, b) => a - b);
      const pts = parsed[String(Ls[0])] ?? [];
      if (pts.length < 3) return null;
      const W = 56;
      const H = 18;
      const pMin = pts[0].p;
      const pMax = pts[pts.length - 1].p;
      const ys = pts.map((q) => q.mean);
      let yLo = Math.min(...ys);
      let yHi = Math.max(...ys);
      if (yHi - yLo < 1e-9) { yLo -= 0.5; yHi += 0.5; }
      const x = (p: number) => 2 + ((p - pMin) / (pMax - pMin || 1)) * (W - 4);
      const y = (v: number) => H - 3 - ((v - yLo) / (yHi - yLo)) * (H - 6);
      const d = pts.map((q, i) => `${i === 0 ? "M" : "L"}${x(q.p).toFixed(1)},${y(q.mean).toFixed(1)}`).join("");
      const zeroY = yHi >= 0 && yLo <= 0 ? y(0) : null;
      return { W, H, d, zeroY, L: Ls[0], nPts: pts.length, pRange: `${pts[0].p.toFixed(3)}–${pts[pts.length - 1].p.toFixed(3)}` };
    } catch {
      return null;
    }
  })();
  if (!data) return null;
  return (
    <svg
      width={data.W}
      height={data.H}
      viewBox={`0 0 ${data.W} ${data.H}`}
      aria-hidden
      className="shrink-0 opacity-80"
      role="img"
    >
      <title>{`⟨I₃⟩(p) at L = ${data.L} · ${data.nPts} points · p ∈ [${data.pRange}] — the smallest size in this saved sweep`}</title>
      {data.zeroY != null && (
        <line x1={2} x2={data.W - 2} y1={data.zeroY} y2={data.zeroY} stroke="#52525b" strokeWidth={0.6} strokeDasharray="2 2" />
      )}
      <path d={data.d} fill="none" stroke="#34d399" strokeWidth={1.3} strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  );
}

/** HUD corner brackets for chart containers (shared with the FSS section). */
export function Corners() {
  const c = "absolute size-3 border-emerald-500/30 group-hover:border-emerald-500/60 transition-colors pointer-events-none";
  return (
    <div aria-hidden>
      <span className={`${c} left-0 top-0 border-l border-t`} />
      <span className={`${c} right-0 top-0 border-r border-t`} />
      <span className={`${c} left-0 bottom-0 border-l border-b`} />
      <span className={`${c} right-0 bottom-0 border-r border-b`} />
    </div>
  );
}

/** Compact confidence-interval "ruler": 1σ band, best value, deposited reference. */
function IntervalRuler({
  mode,
  best,
  sigma,
}: {
  mode: "nu" | "pc";
  best: number;
  sigma: { lo: number | null; hi: number | null };
}) {
  const isNu = mode === "nu";
  const fmt = (v: number) => (isNu ? v.toFixed(2) : v.toFixed(4));
  const refV = isNu ? NU_REF : PC_REF;
  const refLabel = isNu ? "deposited 1.24" : "deposited 0.1597";
  if (sigma.lo == null && sigma.hi == null) return null;
  const W = 720;
  const H = 64;
  const vals = [best, sigma.lo ?? best, sigma.hi ?? best, refV];
  let lo = Math.min(...vals);
  let hi = Math.max(...vals);
  const pad = (hi - lo) * 0.14 || (isNu ? 0.05 : 0.0015);
  lo -= pad;
  hi += pad;
  const x = lerpScale(lo, hi, 20, W - 20);
  const bandLo = sigma.lo ?? best;
  const bandHi = sigma.hi ?? best;
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto" role="img" aria-label={`1σ interval on ${isNu ? "ν" : "p_c"}: ${fmt(sigma.lo ?? best)} to ${fmt(sigma.hi ?? best)}`}>
      {/* track */}
      <line x1={20} x2={W - 20} y1={40} y2={40} stroke="#3f3f46" strokeWidth={1.5} strokeLinecap="round" />
      {/* 1σ band */}
      <rect x={x(bandLo)} y={34} width={Math.max(x(bandHi) - x(bandLo), 2)} height={12} rx={3} fill="#10b981" opacity={0.18} />
      <line x1={x(bandLo)} x2={x(bandLo)} y1={32} y2={48} stroke="#10b981" strokeWidth={2} />
      <line x1={x(bandHi)} x2={x(bandHi)} y1={32} y2={48} stroke="#10b981" strokeWidth={2} />
      <text x={x(bandLo)} y={58} textAnchor="middle" className="fill-emerald-400/90 text-[11px] font-mono">{fmt(bandLo)}</text>
      <text x={x(bandHi)} y={58} textAnchor="middle" className="fill-emerald-400/90 text-[11px] font-mono">{fmt(bandHi)}</text>
      {/* best marker */}
      <line x1={x(best)} x2={x(best)} y1={28} y2={52} stroke="#34d399" strokeWidth={2} />
      <circle cx={x(best)} cy={40} r={3.2} fill="#34d399" />
      <text x={x(best) - 6} y={16} textAnchor="end" className="fill-emerald-300 text-[11px] font-mono">
        {isNu ? "ν̂" : "p̂_c"} = {fmt(best)}
      </text>
      {/* deposited reference tick */}
      <line x1={x(refV)} x2={x(refV)} y1={30} y2={50} stroke="#f59e0b" strokeWidth={1.2} strokeDasharray="3 3" opacity={0.85} />
      <text x={x(refV) + 6} y={16} className="fill-amber-400/80 text-[11px] font-mono">{refLabel}</text>
      <text x={20} y={16} className="fill-zinc-600 text-[11px] font-mono">1σ (Δχ² = 1)</text>
    </svg>
  );
}

/** 1σ interval annotation for the profile chips: two-sided, or one-sided with a tooltip. */
function SigmaNote({ best, sigma, digits }: { best: number; sigma: { lo: number | null; hi: number | null }; digits: number }) {
  if (sigma.lo == null && sigma.hi == null) return null;
  if (sigma.lo != null && sigma.hi != null) {
    return (
      <span className="text-emerald-400/70">
        (−{(best - sigma.lo).toFixed(digits)} / +{(sigma.hi - best).toFixed(digits)})
      </span>
    );
  }
  if (sigma.hi != null) {
    return (
      <span className="text-emerald-400/70" title="the Δχ² = 1 crossing on the low side was not found inside the profile grid — one-sided interval">
        (+{(sigma.hi - best).toFixed(digits)} one-sided)
      </span>
    );
  }
  return (
    <span className="text-emerald-400/70" title="the Δχ² = 1 crossing on the high side was not found inside the profile grid — one-sided interval">
      (−{(best - (sigma.lo as number)).toFixed(digits)} one-sided)
    </span>
  );
}

/** Bootstrap-distribution popover for a pair crossing: histogram + 68% band + deposited p_c. */
function CrossingHisto({ boot, pair }: { boot: CrossingBootstrap; pair: string }) {
  const W = 216;
  const H = 84;
  const M = { top: 10, right: 8, bottom: 18, left: 8 };
  const hmin = boot.histogram[0].p;
  const hmax = boot.histogram[boot.histogram.length - 1].p;
  const span = hmax - hmin || 1e-6;
  const max = Math.max(...boot.histogram.map((h) => h.count), 1);
  const x = lerpScale(hmin - span * 0.03, hmax + span * 0.03, M.left, W - M.right);
  const barW = Math.max((W - M.left - M.right) / boot.histogram.length - 1.5, 1.5);
  const y = (count: number) => H - M.bottom - (count / max) * (H - M.top - M.bottom);
  const depIn = PC_REF >= hmin && PC_REF <= hmax;
  return (
    <span className="pointer-events-none absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-30 hidden group-hover/crs:block group-focus-within/crs:block">
      <span className="block w-[232px] rounded-lg border border-zinc-700 bg-zinc-900/97 shadow-[0_8px_30px_rgba(0,0,0,0.45)] p-2.5 backdrop-blur">
        <span className="block text-[10px] font-mono text-zinc-400">{pair} · {boot.kind === "traj" ? "trajectory" : "parametric"} bootstrap ({boot.B})</span>
        <svg viewBox={`0 0 ${W} ${H}`} className="mt-1 w-full h-auto" role="img" aria-label={`Bootstrap distribution of the ${pair} crossing: 68% from ${boot.lo.toFixed(3)} to ${boot.hi.toFixed(3)}`}>
          {/* 68% band underlay */}
          <rect x={x(boot.lo)} width={Math.max(x(boot.hi) - x(boot.lo), 2)} y={M.top - 4} height={H - M.bottom - M.top + 4} fill="#fb7185" opacity={0.12} rx={2} />
          {/* bars */}
          {boot.histogram.map((h, i) => {
            const bx = x(h.p) - barW / 2;
            const by = y(h.count);
            return (
              <rect key={i} x={bx} y={by} width={barW} height={H - M.bottom - by} fill="#fb7185" opacity={0.55} rx={1} />
            );
          })}
          {/* median marker */}
          <line x1={x(boot.median)} x2={x(boot.median)} y1={M.top - 4} y2={H - M.bottom} stroke="#fda4af" strokeWidth={1.4} />
          {/* point estimate */}
          <circle cx={x(boot.point)} cy={H - M.bottom} r={2.8} fill="#fb7185" stroke="#09090b" strokeWidth={1} />
          {/* deposited p_c */}
          {depIn && (
            <g>
              <line x1={x(PC_REF)} x2={x(PC_REF)} y1={M.top - 4} y2={H - M.bottom} stroke="#f59e0b" strokeWidth={1.2} strokeDasharray="3 3" opacity={0.9} />
              <text x={x(PC_REF)} y={H - 5} textAnchor="middle" className="fill-amber-500/90 text-[8px] font-mono">0.1597</text>
            </g>
          )}
          <text x={M.left} y={H - 5} className="fill-zinc-500 text-[8px] font-mono">{boot.lo.toFixed(3)}</text>
          <text x={W - M.right} y={H - 5} textAnchor="end" className="fill-zinc-500 text-[8px] font-mono">{boot.hi.toFixed(3)}</text>
        </svg>
        <span className="mt-1 block text-[10px] text-zinc-500 font-mono leading-relaxed">
          median {boot.median.toFixed(3)} · 68% [{boot.lo.toFixed(3)}, {boot.hi.toFixed(3)}]
          {boot.hitRate < 0.95 && ` · crossing in ${(boot.hitRate * 100).toFixed(0)}% of resamples`}
        </span>
      </span>
    </span>
  );
}

/** Bootstrap popover for the profile minima: histogram + 68% band + median. */
function BootHisto({ boot, target }: { boot: ProfileBootstrap; target: "nu" | "pc" }) {
  const W = 216;
  const H = 84;
  const M = { top: 10, right: 8, bottom: 18, left: 8 };
  const isNu = target === "nu";
  const fmt = (v: number) => (isNu ? v.toFixed(2) : v.toFixed(4));
  const hmin = boot.minHist[0].v;
  const hmax = boot.minHist[boot.minHist.length - 1].v;
  const span = hmax - hmin || 1e-6;
  const max = Math.max(...boot.minHist.map((h) => h.count), 1);
  const x = lerpScale(hmin - span * 0.03, hmax + span * 0.03, M.left, W - M.right);
  const barW = Math.max((W - M.left - M.right) / boot.minHist.length - 1.5, 1.5);
  const y = (count: number) => H - M.bottom - (count / max) * (H - M.top - M.bottom);
  return (
    <span className="pointer-events-none absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-30 hidden group-hover/crs:block group-focus-within/crs:block">
      <span className="block w-[232px] rounded-lg border border-zinc-700 bg-zinc-900/97 shadow-[0_8px_30px_rgba(0,0,0,0.45)] p-2.5 backdrop-blur">
        <span className="block text-[10px] font-mono text-zinc-400">
          {isNu ? "ν̂" : "p̂_c"} distribution · {boot.kind === "traj" ? "trajectory" : "parametric"} bootstrap ({boot.B})
          {boot.edgeRate > 0.05 && " · edge re-centred"}
        </span>
        <svg viewBox={`0 0 ${W} ${H}`} className="mt-1 w-full h-auto" role="img" aria-label={`Bootstrap distribution of the profile minimum: 68% from ${fmt(boot.min.lo)} to ${fmt(boot.min.hi)}`}>
          {/* 68% band underlay */}
          <rect x={x(boot.min.lo)} width={Math.max(x(boot.min.hi) - x(boot.min.lo), 2)} y={M.top - 4} height={H - M.bottom - M.top + 4} fill="#34d399" opacity={0.12} rx={2} />
          {/* bars */}
          {boot.minHist.map((h, i) => (
            <rect key={i} x={x(h.v) - barW / 2} y={y(h.count)} width={barW} height={H - M.bottom - y(h.count)} fill="#34d399" opacity={0.55} rx={1} />
          ))}
          {/* median marker */}
          <line x1={x(boot.min.med)} x2={x(boot.min.med)} y1={M.top - 4} y2={H - M.bottom} stroke="#6ee7b7" strokeWidth={1.4} />
          <text x={M.left} y={H - 5} className="fill-zinc-500 text-[8px] font-mono">{fmt(boot.min.lo)}</text>
          <text x={W - M.right} y={H - 5} textAnchor="end" className="fill-zinc-500 text-[8px] font-mono">{fmt(boot.min.hi)}</text>
        </svg>
        <span className="mt-1 block text-[10px] text-zinc-500 font-mono leading-relaxed">
          median {fmt(boot.min.med)} · 68% [{fmt(boot.min.lo)}, {fmt(boot.min.hi)}]
          {boot.hitRate < 0.95 && ` · ${Math.round(boot.hitRate * 100)}% usable`}
          {boot.edgeRate > 0.05 && ` · ${Math.round(boot.edgeRate * 100)}% re-centred`}
        </span>
      </span>
    </span>
  );
}

export function I3SweepPanel({ boardId, active = true }: { boardId?: string | null; active?: boolean }) {
  const [sizes, setSizes] = useState<number[]>([8, 16, 32]);
  const [tau, setTau] = useState(2);
  const [nTraj, setNTraj] = useState(24);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(0);
  /** live background-job telemetry while an L ≥ 128 sweep polls (queued = waiting for a free server slot) */
  const [jobInfo, setJobInfo] = useState<{ L: number; done: number; total: number; elapsedMs: number; queued?: boolean } | null>(null);
  const [series, setSeries] = useState<Record<number, I3SeriesPoint[]>>({});
  /** per-L trajectory values aligned with series — enables the non-parametric bootstrap */
  const [trajSeries, setTrajSeries] = useState<Record<number, number[][]>>({});
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();
  const notify = useCallback(
    (title: string, description?: string, variant?: "default" | "destructive") =>
      toast({ title, description, variant, duration: 3400 }),
    [toast]
  );

  // p-grid state
  const [preset, setPreset] = useState<PresetKey>("wide");
  const [customCenter, setCustomCenter] = useState(0.16);
  const [customSpan, setCustomSpan] = useState(0.1);
  const [customN, setCustomN] = useState(9);

  // view state: raw curves / FSS collapse / Δχ² profile
  const [view, setView] = useState<"raw" | "collapse" | "profile">("raw");
  /** literature p_c comparison bands on the raw chart (this work / G–H / Sierant) */
  const [showLit, setShowLit] = useState(true);
  const [pc, setPc] = useState(PC_REF);
  const [nu, setNu] = useState(NU_REF);
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState<{ pc: number; nu: number } | null>(null);
  const [profile, setProfile] = useState<Dchi2Profile | null>(null);
  const [pcProfile, setPcProfile] = useState<Dchi2PcProfile | null>(null);
  const [profileTarget, setProfileTarget] = useState<"nu" | "pc">("nu");
  /** whether a compute has been attempted per target (auto-compute runs on view entry) */
  const [profileTried, setProfileTried] = useState<{ nu: boolean; pc: boolean }>({ nu: false, pc: false });
  const [profiling, setProfiling] = useState(false);
  const [copiedProfile, setCopiedProfile] = useState(false);
  const [downloadedProfile, setDownloadedProfile] = useState(false);

  // community board state
  const [sweeps, setSweeps] = useState<SavedSweep[]>([]);
  /** total rows on the board (X-Board-Total header) — drives the "show all" toggle */
  const [boardTotal, setBoardTotal] = useState<number | null>(null);
  /** when true, fetch up to 100 rows instead of the newest 12 */
  const [showAll, setShowAll] = useState(false);
  const [saveState, setSaveState] = useState<"idle" | "saving" | "saved">("idle");
  const [compareIds, setCompareIds] = useState<string[]>([]);

  // bootstrap sample counts (user-selectable — bigger B = smoother distributions)
  const [crossB, setCrossB] = useState(2000);
  const [profB, setProfB] = useState(120);

  // bootstrap-profile state (per target; the driver runs in ~110 ms chunks)
  const [bootNu, setBootNu] = useState<ProfileBootstrap | null>(null);
  const [bootPc, setBootPc] = useState<ProfileBootstrap | null>(null);
  const [bootRunning, setBootRunning] = useState(false);
  const [bootProgress, setBootProgress] = useState({ done: 0, total: 120 });
  /** invalidates any running bootstrap driver (new sweep / load / target switch) */
  const bootRunIdRef = useRef(0);

  // community-board share + loaded-sweep provenance
  const [sharedId, setSharedId] = useState<string | null>(null);
  /** true after loading a board sweep (means only) — offers the re-run upgrade */
  const [loadedMeansOnly, setLoadedMeansOnly] = useState(false);
  const boardLoadedRef = useRef(false);

  const toggleSize = (L: number) => {
    setSizes((prev) =>
      prev.includes(L) ? prev.filter((v) => v !== L) : [...prev, L].sort((a, b) => a - b)
    );
  };

  /** the active p-grid (preset or custom) */
  const activeGrid = useMemo(() => {
    if (preset !== "custom") {
      const p = P_PRESETS[preset];
      return pGrid(p.min, p.max, p.n);
    }
    const min = Math.max(0, customCenter - customSpan / 2);
    const max = Math.min(0.5, customCenter + customSpan / 2);
    return pGrid(min, max, customN);
  }, [preset, customCenter, customSpan, customN]);

  const loadSweeps = useCallback(async () => {
    try {
      const res = await fetch(showAll ? "/api/sweeps?all=1" : "/api/sweeps");
      if (res.ok) {
        setSweeps(await res.json());
        const t = Number(res.headers.get("X-Board-Total"));
        setBoardTotal(Number.isFinite(t) ? t : null);
      }
    } catch {
      /* offline is fine */
    }
  }, [showAll]);

  useEffect(() => {
    loadSweeps();
  }, [loadSweeps]);

  const run = async () => {
    if (!sizes.length) return;
    setBusy(true);
    setError(null);
    setSeries({});
    setTrajSeries({});
    setProgress(0);
    setJobInfo(null);
    setScanResult(null);
    setProfile(null);
    setPcProfile(null);
    setProfileTried({ nu: false, pc: false });
    bootRunIdRef.current++; // invalidate any running bootstrap driver
    setBootNu(null);
    setBootPc(null);
    setBootRunning(false);
    setLoadedMeansOnly(false);
    setView("raw");
    let completed = false;
    // collected locally during the run — state updates won't be visible to any
    // closure created in this render, so the auto-save receives these directly
    const collected: Record<number, I3SeriesPoint[]> = {};
    const collectedTraj: Record<number, number[][]> = {};
    // tracks whether the active background job is still waiting for a compute
    // slot (queued jobs poll at half frequency)
    let jobQueued = false;
    try {
      for (const L of sizes) {
        if (L >= LARGE_L) {
          // background job: POST then poll, chart updates point-by-point
          const res = await fetch("/api/jobs", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ L, sweepPs: activeGrid, tau, nTraj }),
          });
          if (!res.ok) {
            const body = await res.json().catch(() => ({}));
            throw new Error(body.error ?? `job creation failed (${res.status})`);
          }
          const { jobId } = (await res.json()) as { jobId: string };
          for (;;) {
            await new Promise((r) => setTimeout(r, jobQueued ? JOB_POLL_MS * 2 : JOB_POLL_MS));
            const pr = await fetch(`/api/jobs?id=${encodeURIComponent(jobId)}`);
            if (!pr.ok) {
              // since phase 10 jobs persist to SQLite and resume after reloads —
              // a 404 here means the record itself is gone (or very old)
              throw new Error("background job not found — it may have been pruned after an hour; run the sweep again");
            }
            const job = (await pr.json()) as SweepJobStatus;
            jobQueued = job.status === "queued";
            setSeries((prev) => ({ ...prev, [L]: job.points }));
            setTrajSeries((prev) => ({ ...prev, [L]: job.traj ?? [] }));
            collected[L] = job.points;
            collectedTraj[L] = job.traj ?? [];
            setJobInfo({ L, done: job.points.length, total: job.total, elapsedMs: job.elapsedMs, queued: jobQueued });
            if (job.status === "done") break;
            if (job.status === "error") throw new Error(job.error ?? "background sweep failed");
          }
        } else {
          // synchronous sweep (small sizes, capped server-side)
          const res = await fetch("/api/simulate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ L, sweep: true, sweepPs: activeGrid, tau, nTraj }),
          });
          if (!res.ok) {
            const body = await res.json().catch(() => ({}));
            throw new Error(body.error ?? `request failed (${res.status})`);
          }
          const data: SweepResponse = await res.json();
          setSeries((prev) => ({ ...prev, [L]: data.points }));
          setTrajSeries((prev) => ({ ...prev, [L]: data.traj ?? [] }));
          collected[L] = data.points;
          collectedTraj[L] = data.traj ?? [];
        }
        setProgress((k) => k + 1);
      }
      completed = true;
    } catch (e) {
      setError(e instanceof Error ? e.message : "sweep failed");
    } finally {
      setBusy(false);
    }
    // background jobs are expensive (L ≥ 128, seconds of server time) — persist
    // the finished sweep to the board automatically so it survives reloads and
    // can be shared. Means-only failures (rate limit / dedup) degrade gracefully.
    if (completed && sizes.some((L) => L >= LARGE_L)) {
      void autoSaveJobResult(sizes, collected, collectedTraj);
    }
  };

  /** fire-and-forget auto-save of a finished background sweep (run() calls it with
   *  the data it collected — never reads series state, which is stale in the closure). */
  const autoSaveJobResult = useCallback(
    async (runSizes: number[], runSeries: Record<number, I3SeriesPoint[]>, runTraj: Record<number, number[][]>) => {
      const doneSizes = runSizes.filter((L) => (runSeries[L] ?? []).length > 0);
      if (doneSizes.length < 2) return;
      try {
        const res = await fetch("/api/sweeps", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            label: `background L=${doneSizes.join(",")} · τ=${tau} · n=${nTraj}`,
            tau,
            nTraj,
            series: Object.fromEntries(doneSizes.map((L) => [L, runSeries[L]])),
            traj: Object.fromEntries(
              doneSizes
                .filter((L) => (runTraj[L] ?? []).length === (runSeries[L] ?? []).length)
                .map((L) => [L, runTraj[L]])
            ),
          }),
        });
        if (res.ok) {
          loadSweeps();
          notify("Background sweep saved", "The finished L ≥ 128 sweep was added to the board (with trajectory data).", "default");
        } else if (res.status === 409) {
          notify("Already on the board", "This exact background sweep was saved before.");
        } else if (res.status === 429) {
          notify("Auto-save skipped", "Too many saves from this client — save it manually in a couple of minutes.");
        }
        // other failures stay quiet — the sweep is still on screen
      } catch {
        /* offline is fine — the sweep is still on screen */
      }
    },
    [tau, nTraj, loadSweeps, notify]
  );

  const crossings = useMemo(() => {
    const done = sizes.filter((L) => (series[L] ?? []).length > 0);
    const out: { pair: string; p: number; lo?: number; hi?: number; boot: CrossingBootstrap | null }[] = [];
    for (let i = 0; i < done.length - 1; i++) {
      const c = dominantCrossing(series[done[i]], series[done[i + 1]]);
      if (c == null) continue;
      const boot = bootstrapCrossing(series[done[i]], series[done[i + 1]], {
        B: crossB,
        seed: 90210 + done[i] * 31 + done[i + 1],
        // per-trajectory values when BOTH curves carry them → non-parametric
        trajA: trajSeries[done[i]],
        trajB: trajSeries[done[i + 1]],
      });
      out.push({
        pair: `L=${done[i]}×${done[i + 1]}`,
        p: c.p,
        lo: boot?.lo,
        hi: boot?.hi,
        boot,
      });
    }
    return out;
  }, [series, sizes, trajSeries, crossB]);

  const quality = useMemo(
    () => collapseQuality(series, sizes, pc, nu, nTraj),
    [series, sizes, pc, nu, nTraj]
  );

  /** Grid-scan (p_c, ν) for the tightest collapse of the user's own data. */
  const scanBestFit = () => {
    setScanning(true);
    // let the spinner paint before the synchronous scan
    setTimeout(() => {
      let best = { pc: NaN, nu: NaN, q: Infinity };
      for (let pcTry = 0.14; pcTry <= 0.1801; pcTry += 0.0005) {
        for (let nuTry = 0.9; nuTry <= 1.7001; nuTry += 0.02) {
          const q = collapseQuality(series, sizes, pcTry, nuTry, nTraj);
          if (Number.isFinite(q) && q < best.q) best = { pc: pcTry, nu: nuTry, q };
        }
      }
      if (Number.isFinite(best.q)) {
        setPc(best.pc);
        setNu(best.nu);
        setScanResult({ pc: best.pc, nu: best.nu });
      }
      setScanning(false);
    }, 30);
  };

  /** Frozen-parameter Δχ² profile — target "nu" re-optimises p_c at each ν, target "pc" re-optimises ν at each p_c. */
  const computeProfileFor = (target: "nu" | "pc") => {
    setProfiling(true);
    setTimeout(() => {
      if (target === "nu") {
        const prof = dchi2Profile(series, sizes, nTraj);
        setProfile(prof);
        setProfileTried((t) => ({ ...t, nu: true }));
        if (prof) {
          // align the collapse sliders with the profile minimum
          setPc(prof.best.pc);
          setNu(prof.best.nu);
        }
      } else {
        const prof = dchi2ProfilePc(series, sizes, nTraj);
        setPcProfile(prof);
        setProfileTried((t) => ({ ...t, pc: true }));
        if (prof) {
          setPc(prof.best.pc);
          setNu(prof.best.nu);
        }
      }
      setProfiling(false);
    }, 30);
  };

  const computeProfile = () => computeProfileFor(profileTarget);

  /** Chunked bootstrap of the active Δχ² profile (~110 ms batches with a progress readout).
   *  Resamples trajectories (or means, for board sweeps) B times and re-fits
   *  the whole profile per resample: 68% envelope on the Δχ² curve + a bootstrap
   *  interval on the profiled parameter — no Gaussian-shape assumption. */
  const runBootstrap = () => {
    const activeMain = profileTarget === "nu" ? profile : pcProfile;
    if (!activeMain) return;
    const main = {
      points:
        profileTarget === "nu"
          ? profile!.points.map((d) => ({ v: d.nu }))
          : pcProfile!.points.map((d) => ({ v: d.pc })),
      refUsed: activeMain.refUsed,
    };
    const iter = bootstrapProfileIter(profileTarget, series, sizes, nTraj, main, trajSeries, {
      B: profB,
      seed: profileTarget === "nu" ? 20260920 : 20260921,
    });
    const myRun = ++bootRunIdRef.current;
    const target = profileTarget;
    setBootRunning(true);
    setBootProgress({ done: 0, total: profB });
    const step = () => {
      if (bootRunIdRef.current !== myRun) return; // superseded — the new driver owns the state
      const t0 = performance.now();
      let r = iter.next();
      while (!r.done && performance.now() - t0 < 110) r = iter.next();
      if (r.done) {
        const res = r.value as ProfileBootstrap | null;
        if (target === "nu") setBootNu(res);
        else setBootPc(res);
        setBootRunning(false);
        if (!res) notify("Bootstrap failed", "Too few stable resamples — add trajectories or sizes.", "destructive");
      } else {
        setBootProgress({ done: r.value as number, total: profB });
        setTimeout(step, 0);
      }
    };
    setTimeout(step, 30);
  };

  /** entering the profile view auto-computes the selected target (no dead-empty chart). */
  const switchView = (v: "raw" | "collapse" | "profile") => {
    setView(v);
    if (v === "profile" && Object.keys(series).length > 0 && !profileTried[profileTarget]) {
      computeProfileFor(profileTarget);
    }
  };

  const switchTarget = (t: "nu" | "pc") => {
    setProfileTarget(t);
    bootRunIdRef.current++; // stop any bootstrap running for the other target
    setBootRunning(false);
    if (Object.keys(series).length > 0 && !profileTried[t]) computeProfileFor(t);
  };

  const copyCsv = async () => {
    const rows = ["L,p,i3_mean,i3_se"];
    for (const L of Object.keys(series).map(Number).sort((a, b) => a - b)) {
      for (const pt of series[L]) {
        rows.push(`${L},${pt.p},${pt.mean.toFixed(4)},${pt.se.toFixed(4)}`);
      }
    }
    if (await copyText(rows.join("\n"))) {
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    }
  };

  const downloadCsv = () => {
    const doneSizes = sizes.filter((L) => (series[L] ?? []).length > 0);
    const rows = ["L,p,i3_mean,i3_se"];
    for (const L of doneSizes) {
      for (const pt of series[L]) {
        rows.push(`${L},${pt.p},${pt.mean.toFixed(4)},${pt.se.toFixed(4)}`);
      }
    }
    const name = `i3-sweep_L${doneSizes.join("-")}_tau${tau}_n${nTraj}.csv`;
    if (downloadTextFile(name, rows.join("\n"))) {
      setDownloaded(true);
      setTimeout(() => setDownloaded(false), 1800);
    }
  };

  const save = async () => {
    const doneSizes = sizes.filter((L) => (series[L] ?? []).length > 0);
    if (doneSizes.length < 2) return;
    setSaveState("saving");
    try {
      const res = await fetch("/api/sweeps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          label: `I₃ sweep · L=${doneSizes.join(",")} · τ=${tau} · n=${nTraj}`,
          tau,
          nTraj,
          series: Object.fromEntries(doneSizes.map((L) => [L, series[L]])),
          // per-trajectory values → the board keeps non-parametric bootstraps
          traj: Object.fromEntries(
            doneSizes
              .filter((L) => (trajSeries[L] ?? []).length === (series[L] ?? []).length && (series[L] ?? []).length > 0)
              .map((L) => [L, trajSeries[L]])
          ),
        }),
      });
      if (res.ok) {
        setSaveState("saved");
        loadSweeps();
        notify(
          "Sweep saved",
          doneSizes.some((L) => (trajSeries[L] ?? []).length > 0)
            ? "On the board with trajectory data — loads and share links keep non-parametric bootstraps."
            : "It is now on the community board and can be overlaid or reloaded by any visitor."
        );
        setTimeout(() => setSaveState("idle"), 2000);
      } else {
        setSaveState("idle");
        const body = await res.json().catch(() => ({}));
        notify(
          res.status === 409 ? "Already on the board" : res.status === 429 ? "Too many saves" : "Save failed",
          body.error ?? undefined,
          "destructive"
        );
      }
    } catch {
      setSaveState("idle");
      notify("Save failed", "The server could not be reached.", "destructive");
    }
  };

  /** apply a saved board sweep to the explorer — trajectory data restored when
   *  the record carries it (phase-9 schema); means-only records still work. */
  const applySweep = useCallback((sw: SavedSweep): boolean => {
    try {
      const parsed = JSON.parse(sw.seriesJson) as Record<string, I3SeriesPoint[]>;
      const loaded: Record<number, I3SeriesPoint[]> = {};
      for (const [k, v] of Object.entries(parsed)) loaded[Number(k)] = v;
      setSeries(loaded);
      // restore per-trajectory values when present + aligned (bootstrap upgrade)
      const loadedTraj: Record<number, number[][]> = {};
      if (sw.trajJson) {
        try {
          const parsedTraj = JSON.parse(sw.trajJson) as Record<string, number[][]>;
          for (const [k, rows] of Object.entries(parsedTraj)) {
            const L = Number(k);
            if (
              Number.isFinite(L) &&
              Array.isArray(rows) &&
              rows.length === (loaded[L] ?? []).length &&
              rows.every((row) => Array.isArray(row) && row.every((v) => typeof v === "number" && Number.isFinite(v)))
            ) {
              loadedTraj[L] = rows;
            }
          }
        } catch {
          /* malformed traj blob → means-only fallback */
        }
      }
      setTrajSeries(loadedTraj);
      setSizes(sw.sizes.split(",").map(Number).filter(Number.isFinite));
      setTau(sw.tau);
      setNTraj(sw.nTraj);
      setScanResult(null);
      setProfile(null);
      setPcProfile(null);
      setProfileTried({ nu: false, pc: false });
      bootRunIdRef.current++;
      setBootNu(null);
      setBootPc(null);
      setBootRunning(false);
      // means-only records (older saves) offer the re-run upgrade; traj records do not
      setLoadedMeansOnly(Object.keys(loadedTraj).length === 0);
      setView("raw");
      setError(null);
      return true;
    } catch {
      setError("could not load this saved sweep");
      return false;
    }
  }, []);

  // shared board link: consume the ?board=<id> handed up by the section
  // (the section activates this tab and passes the id; the panel is
  // force-mounted, so the id can arrive any time after mount — the
  // boardLoadedRef guard makes the consumption run exactly once)
  useEffect(() => {
    if (boardLoadedRef.current || !boardId) return;
    boardLoadedRef.current = true;
    void (async () => {
      try {
        const res = await fetch(`/api/sweeps?id=${encodeURIComponent(boardId)}`);
        if (!res.ok) {
          notify("Shared sweep not found", "It may have been deleted from the board.", "destructive");
          return;
        }
        const sw = (await res.json()) as SavedSweep;
        if (applySweep(sw)) {
          notify(
            "Shared sweep loaded",
            sw.trajJson
              ? `${sw.label} — trajectory data restored, non-parametric bootstraps live`
              : sw.label
          );
        }
      } catch {
        /* offline is fine */
      }
    })();
  }, [boardId, applySweep, notify]);

  // keyboard shortcuts — R = run sweep · V = cycle view. Live only while this
  // panel's tab is the selected one and no form control has focus, so typing
  // a seed or a label never triggers a run.
  useEffect(() => {
    if (!active) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "SELECT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
      if (e.key === "r" || e.key === "R") {
        if (!busy && sizes.length >= 2) void run();
      } else if (e.key === "v" || e.key === "V") {
        if (Object.keys(series).length > 0) {
          switchView(view === "raw" ? "collapse" : view === "collapse" ? "profile" : "raw");
        }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  const loadSweep = async (sw: SavedSweep) => {
    // the board list omits the traj blob (payload weight) — fetch the full record
    // so loads restore trajectory-level bootstraps when the sweep carries them
    if (sw.trajJson == null && sw.hasTraj !== false) {
      try {
        const res = await fetch(`/api/sweeps?id=${encodeURIComponent(sw.id)}`);
        if (res.ok) {
          const full = (await res.json()) as SavedSweep;
          if (applySweep(full)) {
            notify(
              "Sweep loaded",
              full.trajJson
                ? `${full.label} — trajectory data restored (non-parametric bootstraps live)`
                : full.label
            );
            return;
          }
          return;
        }
      } catch {
        /* fall through to the list record */
      }
    }
    applySweep(sw);
  };

  const del = async (id: string) => {
    try {
      const res = await fetch(`/api/sweeps?id=${id}`, { method: "DELETE" });
      if (res.ok) {
        notify("Sweep deleted", undefined);
      }
      setCompareIds((prev) => prev.filter((v) => v !== id));
      loadSweeps();
    } catch {
      notify("Delete failed", "The server could not be reached.", "destructive");
    }
  };

  /** Copy a deep link that loads this saved sweep on open (?board=<id>#simulator). */
  const shareSweep = async (sw: SavedSweep) => {
    const url = `${window.location.origin}${window.location.pathname}?board=${sw.id}#simulator`;
    if (await copyText(url)) {
      setSharedId(sw.id);
      setTimeout(() => setSharedId(null), 1600);
    } else {
      notify("Copy failed", "The link could not be copied.", "destructive");
    }
  };

  const toggleCompare = (id: string) => {
    setCompareIds((prev) =>
      prev.includes(id) ? prev.filter((v) => v !== id) : prev.length >= 3 ? prev : [...prev, id]
    );
  };

  /** parsed overlays for the raw chart */
  const overlays: SweepOverlay[] = useMemo(() => {
    return compareIds
      .map((id, i) => {
        const sw = sweeps.find((s) => s.id === id);
        if (!sw) return null;
        try {
          const parsed = JSON.parse(sw.seriesJson) as Record<string, I3SeriesPoint[]>;
          const s: Record<number, I3SeriesPoint[]> = {};
          for (const [k, v] of Object.entries(parsed)) s[Number(k)] = v;
          return { id, label: `L=${sw.sizes} τ=${sw.tau}`, color: OVERLAY_COLORS[i % OVERLAY_COLORS.length], series: s };
        } catch {
          return null;
        }
      })
      .filter((o): o is SweepOverlay => o != null);
  }, [compareIds, sweeps]);

  const hasData = Object.keys(series).length > 0;
  const qIsNum = Number.isFinite(quality);
  const qRef = scanResult ? collapseQuality(series, sizes, PC_REF, NU_REF, nTraj) : NaN;
  const qNorm = qIsNum && Number.isFinite(qRef) ? quality / qRef : NaN;

  /** Δχ² at the headline reference: ν = 1 (ν profile) or the deposited p_c (p_c profile). */
  const dchi2AtReference = useMemo(() => {
    if (profileTarget === "nu" && profile) {
      const pt = profile.points.find((d) => Math.abs(d.nu - 1) < 1e-6);
      return pt ? { at: "ν = 1", dchi2: pt.dchi2, caveat: null } : null;
    }
    if (profileTarget === "pc" && pcProfile) {
      let best: { pc: number; dchi2: number } | null = null;
      for (const pt of pcProfile.points)
        if (!best || Math.abs(pt.pc - PC_REF) < Math.abs(best.pc - PC_REF)) best = { pc: pt.pc, dchi2: pt.dchi2 };
      if (!best) return null;
      // deposited value inside the scanned window → quote it directly
      if (Math.abs(best.pc - PC_REF) <= 0.0006) return { at: "p_c = 0.1597", dchi2: best.dchi2, caveat: null };
      // otherwise quote the NEAREST scanned grid point + distance instead of hiding the chip
      const dist = PC_REF - best.pc;
      return {
        at: `p_c = ${best.pc.toFixed(4)}`,
        dchi2: best.dchi2,
        caveat: `your profile window did not reach the deposited 0.1597 — this is the nearest scanned grid point, ${Math.abs(dist).toFixed(4)} ${dist > 0 ? "below" : "above"} it`,
      };
    }
    return null;
  }, [profileTarget, profile, pcProfile]);

  /** true when the profile minimum sits on the grid boundary (weak constraint). */
  const edgeMinimum = useMemo(() => {
    if (profileTarget === "nu" && profile) {
      const nus = profile.points.map((d) => d.nu);
      return profile.best.nu <= Math.min(...nus) + 1e-9 || profile.best.nu >= Math.max(...nus) - 1e-9;
    }
    if (profileTarget === "pc" && pcProfile) {
      const pcs = pcProfile.points.map((d) => d.pc);
      return pcProfile.best.pc <= Math.min(...pcs) + 1e-9 || pcProfile.best.pc >= Math.max(...pcs) - 1e-9;
    }
    return false;
  }, [profileTarget, profile, pcProfile]);

  /** cross-profile consistency (phase-9): both profiles exist → is the deposited
   *  (0.1597, 1.24) inside your JOINT 1σ region (both intervals simultaneously)?
   *  One chip, glanceable, honest about which coordinate disagrees. */
  const jointVsDeposited = useMemo(() => {
    if (!profile || !pcProfile) return null;
    const inPc =
      pcProfile.sigma.lo != null && pcProfile.sigma.hi != null
        ? pcProfile.sigma.lo <= PC_REF && PC_REF <= pcProfile.sigma.hi
        : pcProfile.sigma.hi != null
          ? PC_REF <= pcProfile.sigma.hi
          : pcProfile.sigma.lo != null
            ? PC_REF >= pcProfile.sigma.lo
            : false;
    const inNu =
      profile.sigma.lo != null && profile.sigma.hi != null
        ? profile.sigma.lo <= NU_REF && NU_REF <= profile.sigma.hi
        : profile.sigma.hi != null
          ? NU_REF <= profile.sigma.hi
          : profile.sigma.lo != null
            ? NU_REF >= profile.sigma.lo
            : false;
    return { inPc, inNu, both: inPc && inNu };
  }, [profile, pcProfile]);

  /** methods agreement (Δχ² interval vs bootstrap interval on the active target):
   *  two independent uncertainty constructions — they should overlap substantially. */
  const methodsAgree = useMemo(() => {
    const boot = profileTarget === "nu" ? bootNu : bootPc;
    const sigma = profileTarget === "nu" ? profile?.sigma ?? null : pcProfile?.sigma ?? null;
    const best = profileTarget === "nu" ? profile?.best.nu ?? null : pcProfile?.best.pc ?? null;
    if (!boot || !sigma || best == null || sigma.lo == null || sigma.hi == null) return null;
    const a = { lo: sigma.lo, hi: sigma.hi };
    const b = { lo: boot.min.lo, hi: boot.min.hi };
    const overlap = Math.max(0, Math.min(a.hi, b.hi) - Math.max(a.lo, b.lo));
    const union = Math.max(a.hi, b.hi) - Math.min(a.lo, b.lo) || 1e-9;
    return { overlapFrac: overlap / union, delta: Math.abs((a.lo + a.hi) / 2 - (b.lo + b.hi) / 2) };
  }, [profileTarget, profile, pcProfile, bootNu, bootPc]);

  /** the profile of the currently selected target, normalised for the chart. */
  const profileViewPoints = useMemo<ProfileViewPoint[] | null>(() => {
    if (profileTarget === "nu" && profile)
      return profile.points.map((d) => ({ v: d.nu, dchi2: d.dchi2, bestOther: d.bestPc }));
    if (profileTarget === "pc" && pcProfile)
      return pcProfile.points.map((d) => ({ v: d.pc, dchi2: d.dchi2, bestOther: d.bestNu }));
    return null;
  }, [profileTarget, profile, pcProfile]);

  const profileSigma = profileTarget === "nu" ? profile?.sigma ?? null : pcProfile?.sigma ?? null;
  const profileRefUsed = (profileTarget === "nu" ? profile?.refUsed : pcProfile?.refUsed) ?? null;
  const activeBoot = profileTarget === "nu" ? bootNu : bootPc;
  const fmtBoot = (v: number) => (profileTarget === "nu" ? v.toFixed(2) : v.toFixed(4));

  /** profile CSV rows — with the bootstrap band columns appended when available. */
  const profileCsvRows = (): string[] => {
    const boot = activeBoot;
    if (profileTarget === "nu" && profile) {
      const head = boot ? "nu,dchi2,best_pc,boot_lo,boot_med,boot_hi" : "nu,dchi2,best_pc";
      return [
        head,
        ...profile.points.map((d) => {
          const base = `${d.nu},${d.dchi2.toFixed(4)},${d.bestPc.toFixed(4)}`;
          const b = boot?.band.find((x) => Math.abs(x.v - d.nu) < 1e-9);
          return b ? `${base},${b.lo.toFixed(4)},${b.med.toFixed(4)},${b.hi.toFixed(4)}` : base;
        }),
      ];
    }
    if (pcProfile) {
      const head = boot ? "pc,dchi2,best_nu,boot_lo,boot_med,boot_hi" : "pc,dchi2,best_nu";
      return [
        head,
        ...pcProfile.points.map((d) => {
          const base = `${d.pc},${d.dchi2.toFixed(4)},${d.bestNu.toFixed(2)}`;
          const b = boot?.band.find((x) => Math.abs(x.v - d.pc) < 1e-9);
          return b ? `${base},${b.lo.toFixed(4)},${b.med.toFixed(4)},${b.hi.toFixed(4)}` : base;
        }),
      ];
    }
    return [];
  };

  const copyProfileCsv = async () => {
    const rows = profileCsvRows();
    if (!rows.length) return;
    if (await copyText(rows.join("\n"))) {
      setCopiedProfile(true);
      setTimeout(() => setCopiedProfile(false), 1800);
    }
  };

  const downloadProfileCsv = () => {
    const doneSizes = sizes.filter((L) => (series[L] ?? []).length > 0);
    const rows = profileCsvRows();
    if (!rows.length) return;
    const name = `dchi2-profile-${profileTarget}_L${doneSizes.join("-")}_tau${tau}${activeBoot ? "_boot" : ""}.csv`;
    if (downloadTextFile(name, rows.join("\n"))) {
      setDownloadedProfile(true);
      setTimeout(() => setDownloadedProfile(false), 1800);
    }
  };

  /** Export the complete explorer state (params + series + trajectory values)
   *  as a JSON file — exact reproduction: reload it with "import state". */
  const exportState = () => {
    const doneSizes = sizes.filter((L) => (series[L] ?? []).length > 0);
    if (!doneSizes.length) return;
    const state: SweepStateJson = {
      version: 1,
      kind: "i3-sweep-state",
      sizes: doneSizes,
      tau,
      nTraj,
      pc,
      nu,
      series: Object.fromEntries(doneSizes.map((L) => [L, series[L]])),
      traj: Object.fromEntries(doneSizes.filter((L) => (trajSeries[L] ?? []).length > 0).map((L) => [L, trajSeries[L]])),
    };
    const name = `i3-sweep-state_L${doneSizes.join("-")}_tau${tau}.json`;
    if (downloadTextFile(name, JSON.stringify(state, null, 1))) {
      notify(
        "State exported",
        doneSizes.some((L) => (trajSeries[L] ?? []).length > 0)
          ? "Includes per-trajectory values — the imported session keeps non-parametric bootstraps."
          : "Means only — the imported session falls back to parametric bootstraps."
      );
    } else {
      notify("Export failed", "The file could not be created.", "destructive");
    }
  };

  /** Validate + apply an imported state JSON. */
  const importState = (raw: string) => {
    let state: SweepStateJson;
    try {
      state = JSON.parse(raw) as SweepStateJson;
    } catch {
      notify("Import failed", "The file is not valid JSON.", "destructive");
      return;
    }
    if (state?.kind !== "i3-sweep-state" || !Array.isArray(state.sizes)) {
      notify("Import failed", 'Not a sweep state file — expected kind "i3-sweep-state".', "destructive");
      return;
    }
    const inSizes = state.sizes.map(Number).filter((v) => Number.isFinite(v) && v > 0 && v <= 4096);
    if (inSizes.length < 2 || inSizes.length > 6) {
      notify("Import failed", "The state must carry 2–6 system sizes.", "destructive");
      return;
    }
    const loaded: Record<number, I3SeriesPoint[]> = {};
    const loadedTraj: Record<number, number[][]> = {};
    for (const L of inSizes) {
      const pts = state.series?.[String(L)];
      if (!Array.isArray(pts) || pts.length < 3 || pts.length > 16) {
        notify("Import failed", `series[${L}] must have 3–16 points.`, "destructive");
        return;
      }
      loaded[L] = pts
        .filter((pt) => pt && Number.isFinite(pt.p) && Number.isFinite(pt.mean) && Number.isFinite(pt.se))
        .map((pt) => ({ p: Math.max(0, Math.min(0.5, pt.p)), mean: pt.mean, se: Math.max(0, pt.se) }));
      const tr = state.traj?.[String(L)];
      if (Array.isArray(tr) && tr.length === loaded[L].length && tr.every((row) => Array.isArray(row))) {
        loadedTraj[L] = tr;
      }
    }
    setSeries(loaded);
    setTrajSeries(loadedTraj);
    setSizes(inSizes);
    setTau(Math.max(0.5, Math.min(4, Number(state.tau) || 2)));
    setNTraj(Math.max(1, Math.min(64, Math.floor(Number(state.nTraj) || 24))));
    if (Number.isFinite(state.pc)) setPc(Math.max(0.13, Math.min(0.19, state.pc)));
    if (Number.isFinite(state.nu)) setNu(Math.max(0.8, Math.min(1.8, state.nu)));
    setScanResult(null);
    setProfile(null);
    setPcProfile(null);
    setProfileTried({ nu: false, pc: false });
    bootRunIdRef.current++;
    setBootNu(null);
    setBootPc(null);
    setBootRunning(false);
    setLoadedMeansOnly(false);
    setView("raw");
    setError(null);
    notify(
      "State imported",
      `${inSizes.join(", ")} · τ=${state.tau} · ${Object.keys(loadedTraj).length ? "trajectory data included" : "means only (parametric bootstrap)"}`
    );
  };

  const onImportFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = ""; // allow re-selecting the same file
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => importState(String(reader.result ?? ""));
    reader.onerror = () => notify("Import failed", "The file could not be read.", "destructive");
    reader.readAsText(file);
  };

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6">
      <div className="flex flex-wrap items-center gap-3">
        <span className="grid place-items-center size-8 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400">
          <Crosshair className="size-4" />
        </span>
        <div className="min-w-0">
          <h3 className="text-base font-semibold text-zinc-100">Locate the transition with I₃</h3>
          <p className="text-sm text-zinc-500">
            Live Gullans–Huse locator — sweep p, watch the ⟨I₃⟩ curves cross near p_c, then collapse your own data and profile ν or p_c.
          </p>
        </div>
      </div>

      <div className="mt-5 grid sm:grid-cols-[1fr_1fr_1fr_auto] gap-3 items-end">
        <div>
          <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">system sizes (multi)</span>
          <div className="mt-1.5 flex gap-1">
            {L_CHOICES.map((v) => {
              const large = v >= LARGE_L;
              const on = sizes.includes(v);
              return (
                <button
                  key={v}
                  onClick={() => toggleSize(v)}
                  aria-pressed={on}
                  title={large ? "background job — computed server-side, chart fills in point-by-point" : "synchronous sweep"}
                  className={`flex-1 rounded-md border px-2 py-3 sm:py-1.5 text-xs font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                    on
                      ? large
                        ? "border-amber-500/50 bg-amber-500/10 text-amber-300"
                        : "border-emerald-500/50 bg-emerald-500/10 text-emerald-300"
                      : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
                  }`}
                >
                  {v}
                </button>
              );
            })}
          </div>
        </div>
        <div>
          <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">depth τ</span>
          <div className="mt-1.5 flex gap-1">
            {[1, 2, 4].map((v) => (
              <button
                key={v}
                onClick={() => setTau(v)}
                aria-pressed={tau === v}
                title={v === 4 ? "the deepest deposited purification depth — doubles circuit depth vs τ = 2" : undefined}
                className={`flex-1 rounded-md border px-2 py-3 sm:py-1.5 text-xs font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                  tau === v
                    ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300"
                    : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
                }`}
              >
                {v}L
              </button>
            ))}
          </div>
        </div>
        <label className="block">
          <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">trajectories / point</span>
          <select
            value={nTraj}
            onChange={(e) => setNTraj(Number(e.target.value))}
            className="mt-1.5 w-full rounded-md border border-zinc-700 bg-zinc-950 px-2.5 py-2 font-mono text-sm text-zinc-200 focus:border-emerald-500/60 focus:outline-none"
          >
            {[12, 24, 48].map((v) => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </label>
        <button
          onClick={run}
          disabled={busy || sizes.length < 2}
          className="inline-flex items-center gap-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 active:scale-[0.98] disabled:opacity-50 disabled:hover:bg-emerald-500 disabled:active:scale-100 transition-all px-4 py-2.5 text-sm font-medium text-emerald-950 shadow-[0_0_20px_-6px_rgba(16,185,129,0.45)] hover:shadow-[0_0_28px_-6px_rgba(16,185,129,0.65)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
        >
          {busy ? <Loader2 className="size-4 animate-spin" /> : <Crosshair className="size-4" />}
          {busy ? `sweeping… ${progress}/${sizes.length}` : "Run sweep"}
        </button>
      </div>

      {/* keyboard-shortcut hint (R = run · V = cycle view — active only in this panel) */}
      <p className="mt-2 hidden sm:flex items-center gap-2 text-[10px] font-mono text-zinc-600">
        <kbd className="rounded border border-zinc-700 bg-zinc-900 px-1.5 py-px text-[10px] text-zinc-400 shadow-[0_1px_0_rgba(0,0,0,0.4)]">R</kbd>
        run sweep
        <kbd className="rounded border border-zinc-700 bg-zinc-900 px-1.5 py-px text-[10px] text-zinc-400 shadow-[0_1px_0_rgba(0,0,0,0.4)]">V</kbd>
        cycle view (raw → collapse → profile)
      </p>

      {/* large-L background-job hint + live progress */}
      {sizes.some((v) => v >= LARGE_L) && !busy && (
        <p className="mt-2 inline-flex items-center gap-1.5 rounded-md border border-amber-500/20 bg-amber-500/5 px-2.5 py-1.5 text-[11px] text-amber-400/80 font-mono">
          <FlaskConical className="size-3 shrink-0" />
          L ≥ 128 runs as a server-side background job — trajectories capped at 8 (L = 128) / 4 (L = 256); the chart fills in point-by-point as points land; extra jobs queue FIFO, and every job persists to SQLite and resumes under the same id after a server reload
        </p>
      )}
      {tau === 4 && !busy && (
        <p className="mt-2 inline-flex items-center gap-1.5 rounded-md border border-amber-500/20 bg-amber-500/5 px-2.5 py-1.5 text-[11px] text-amber-400/80 font-mono">
          <FlaskConical className="size-3 shrink-0" />
          τ = 4 is the deepest deposited purification depth — it doubles the circuit depth, so L = 64 sweeps cap at 12 trajectories/point
        </p>
      )}
      {busy && jobInfo && (
        <div className="mt-3 rounded-lg border border-amber-500/25 bg-amber-500/5 px-3.5 py-2.5">
          <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1 text-[11px] font-mono">
            <span className="text-amber-300/90 flex items-center gap-1.5">
              <Loader2 className="size-3 animate-spin" />
              {jobInfo.queued
                ? `queued · L = ${jobInfo.L} — waiting for a free server slot (jobs are persisted, this survives reloads)`
                : `background job · L = ${jobInfo.L}`}
            </span>
            <span className="text-zinc-500 tabular-nums">
              {jobInfo.done}/{jobInfo.total} points · {(jobInfo.elapsedMs / 1000).toFixed(1)} s server time
            </span>
          </div>
          <div
            className="mt-2 h-1.5 overflow-hidden rounded-full bg-zinc-800"
            role="progressbar"
            aria-valuenow={jobInfo.total ? Math.round((100 * jobInfo.done) / jobInfo.total) : 0}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label="Background sweep progress"
          >
            <div
              className={`relative h-full rounded-full transition-all duration-500 ${
                jobInfo.queued
                  ? "bg-zinc-600"
                  : "bg-gradient-to-r from-amber-500/70 to-amber-300"
              }`}
              style={{ width: `${jobInfo.total ? Math.max(4, (100 * jobInfo.done) / jobInfo.total) : 4}%` }}
            >
              {!jobInfo.queued && (
                <span className="job-progress-shimmer absolute inset-y-0 left-0 w-1/2 rounded-full bg-gradient-to-r from-transparent via-white/25 to-transparent" />
              )}
            </div>
          </div>
        </div>
      )}

      {/* p-grid controls */}
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">p-grid:</span>
        {(Object.keys(P_PRESETS) as PresetKey[]).map((k) => (
          <button
            key={k}
            onClick={() => setPreset(k)}
            title={P_PRESETS[k].hint}
            aria-pressed={preset === k}
            className={`rounded-full border px-2.5 py-2 sm:py-0.5 text-[11px] font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
              preset === k
                ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300"
                : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
            }`}
          >
            {P_PRESETS[k].label}
          </button>
        ))}
        <button
          onClick={() => setPreset("custom")}
          aria-pressed={preset === "custom"}
          title="custom centre / span / density"
          className={`rounded-full border px-2.5 py-2 sm:py-0.5 text-[11px] font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
            preset === "custom"
              ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300"
              : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
          }`}
        >
          custom
        </button>
        <span className="ml-auto text-[11px] text-zinc-600 font-mono">
          {activeGrid.length} pts · [{activeGrid[0].toFixed(3)}…{activeGrid[activeGrid.length - 1].toFixed(3)}]
        </span>
      </div>
      {preset === "custom" && (
        <div className="mt-2 grid sm:grid-cols-3 gap-x-6 gap-y-2 rounded-lg border border-zinc-800 bg-zinc-950/40 px-4 py-3">
          <div>
            <div className="flex justify-between text-[11px] font-mono text-zinc-500">
              <span>centre</span>
              <span className="text-emerald-400">{customCenter.toFixed(3)}</span>
            </div>
            <input
              type="range" min={0.05} max={0.3} step={0.005}
              value={customCenter}
              onChange={(e) => setCustomCenter(Number(e.target.value))}
              className="mt-1 w-full accent-emerald-500"
              aria-label="Custom p-grid centre"
            />
          </div>
          <div>
            <div className="flex justify-between text-[11px] font-mono text-zinc-500">
              <span>span</span>
              <span className="text-emerald-400">±{(customSpan / 2).toFixed(3)}</span>
            </div>
            <input
              type="range" min={0.04} max={0.2} step={0.005}
              value={customSpan}
              onChange={(e) => setCustomSpan(Number(e.target.value))}
              className="mt-1 w-full accent-emerald-500"
              aria-label="Custom p-grid span"
            />
          </div>
          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">points</span>
            <div className="mt-1 flex gap-1">
              {[5, 7, 9].map((v) => (
                <button
                  key={v}
                  onClick={() => setCustomN(v)}
                  aria-pressed={customN === v}
                  className={`flex-1 rounded-md border px-2 py-2.5 sm:py-1 text-xs font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                    customN === v
                      ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300"
                      : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
                  }`}
                >
                  {v}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
      {sizes.length < 2 && !busy && (
        <p className="mt-2 text-xs text-zinc-500">select at least two sizes — crossings need pairs of curves</p>
      )}

      {error && (
        <div className="mt-4 flex items-center gap-2 rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-2 text-sm text-rose-300">
          <AlertTriangle className="size-4" /> {error}
        </div>
      )}

      {/* view toggle */}
      {hasData && (
        <div className="mt-5 flex flex-wrap items-center gap-2">
          <div className="inline-flex rounded-lg border border-zinc-800 bg-zinc-950/60 p-1 gap-1" role="tablist" aria-label="Sweep view">
            {(["raw", "collapse", "profile"] as const).map((v) => (
              <button
                key={v}
                role="tab"
                aria-selected={view === v}
                onClick={() => switchView(v)}
                className={`rounded-md px-3 py-1 text-xs font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                  view === v
                    ? "bg-emerald-500/10 text-emerald-300 border border-emerald-500/40"
                    : "text-zinc-400 border border-transparent hover:text-zinc-200"
                }`}
              >
                {v === "raw" ? "⟨I₃⟩ vs p" : v === "collapse" ? "collapse view" : "Δχ² profile"}
              </button>
            ))}
          </div>
          {view === "profile" && (
            <div className="inline-flex rounded-lg border border-zinc-800 bg-zinc-950/60 p-1 gap-1" role="tablist" aria-label="Profile target">
              {(["nu", "pc"] as const).map((t) => (
                <button
                  key={t}
                  role="tab"
                  aria-selected={profileTarget === t}
                  onClick={() => switchTarget(t)}
                  className={`rounded-md px-3 py-1 text-xs font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500/40 ${
                    profileTarget === t
                      ? "bg-amber-500/10 text-amber-300 border border-amber-500/40"
                      : "text-zinc-400 border border-transparent hover:text-zinc-200"
                  }`}
                >
                  {t === "nu" ? "profile ν" : "profile p_c"}
                </button>
              ))}
            </div>
          )}
          <span className="ml-auto text-[11px] text-zinc-600 font-mono">
            {sizes.filter((L) => (series[L] ?? []).length > 0).length} sizes · {Object.values(series).reduce((a, b) => a + b.length, 0)} points
          </span>
        </div>
      )}

      <div className="mt-5">
        {!hasData ? (
          <div className="relative group h-[280px] grid place-items-center border border-dashed border-zinc-800 rounded-lg text-center px-6 chart-well">
            <Corners />
            {busy ? (
              <span className="inline-flex items-center gap-2 text-emerald-400/90">
                <Loader2 className="size-4 animate-spin" /> running {sizes[Math.min(progress, sizes.length - 1)]}…
              </span>
            ) : (
              <div className="space-y-3">
                <EmptySketch />
                <p className="text-sm text-zinc-600">
                  run the sweep to see ⟨I₃⟩(p) curves — deep negative plateau (volume law), crossing to 0 (area law)
                </p>
              </div>
            )}
          </div>
        ) : view === "raw" ? (
          <div className="relative group rounded-lg border border-zinc-800/60 bg-zinc-950/40 chart-well p-2.5 sm:p-3">
            <Corners />
            <I3SweepChart
              series={series}
              sizes={sizes}
              crossings={crossings}
              overlays={overlays}
              litBands={showLit ? (LIT_BANDS as LitBand[]) : []}
              busy={busy}
            />
          </div>
        ) : view === "collapse" ? (
          <div className="relative group rounded-lg border border-zinc-800/60 bg-zinc-950/40 chart-well p-2.5 sm:p-3">
            <Corners />
            <I3CollapseChart series={series} sizes={sizes} pc={pc} nu={nu} overlays={overlays} />
          </div>
        ) : (
          <div className="relative group rounded-lg border border-zinc-800/60 bg-zinc-950/40 chart-well p-2.5 sm:p-3">
            <Corners />
            {profileViewPoints ? (
              <Dchi2ProfileChart
                mode={profileTarget}
                points={profileViewPoints}
                sigma={profileSigma ?? { lo: null, hi: null }}
                band={activeBoot?.band ?? null}
                bootB={activeBoot?.B ?? null}
              />
            ) : profiling ? (
              <div className="h-[300px] grid place-items-center text-center px-6">
                <span className="inline-flex items-center gap-2 text-amber-400/90 font-mono text-sm">
                  <Loader2 className="size-4 animate-spin" /> profiling {profileTarget === "nu" ? "ν" : "p_c"}…
                </span>
              </div>
            ) : profileTried[profileTarget] ? (
              <div className="h-[300px] grid place-items-center text-center px-6">
                <div className="space-y-3">
                  <AlertTriangle className="size-8 text-zinc-700 mx-auto" />
                  <p className="text-sm text-zinc-500 max-w-sm">
                    not enough points inside the frozen |x| ≤ 3 window for a {profileTarget === "nu" ? "ν" : "p_c"} profile — try
                    the <span className="text-zinc-300">critical zoom</span> or <span className="text-zinc-300">fine</span> p-grid,
                    more sizes, or more trajectories
                  </p>
                  <button
                    onClick={computeProfile}
                    disabled={profiling}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-300 hover:bg-emerald-500/20 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
                  >
                    {profiling ? <Loader2 className="size-3.5 animate-spin" /> : <Sparkles className="size-3.5" />}
                    retry
                  </button>
                </div>
              </div>
            ) : (
              <div className="h-[300px] grid place-items-center text-center px-6">
                <div className="space-y-3">
                  <LineChart className="size-8 text-zinc-700 mx-auto" />
                  <p className="text-sm text-zinc-500 max-w-sm">
                    at each frozen {profileTarget === "nu" ? "ν, re-optimise p_c" : "p_c, re-optimise ν"} and record Δχ² = χ² − χ²_min —
                    the construction behind the deposited <span className="font-mono text-emerald-400">ν = 1.24(7)</span>, the
                    ν = 1 exclusion, and <span className="font-mono text-emerald-400">p_c = 0.1597(8)</span>
                  </p>
                  <button
                    onClick={computeProfile}
                    disabled={profiling}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-300 hover:bg-emerald-500/20 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
                  >
                    {profiling ? <Loader2 className="size-3.5 animate-spin" /> : <Sparkles className="size-3.5" />}
                    {profiling ? "profiling…" : `compute ${profileTarget === "nu" ? "ν" : "p_c"} profile`}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* raw-view readout */}
      {hasData && view === "raw" && (
        <div className="mt-4 space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">your crossings:</span>
            {crossings.length ? (
              crossings.map((c) => (
                <span
                  key={c.pair}
                  tabIndex={c.boot ? 0 : undefined}
                  title={
                    c.boot
                      ? `${c.pair} crossing · ${c.boot.kind === "traj" ? "trajectory-level (non-parametric) bootstrap — resamples the actual per-trajectory values" : "parametric bootstrap — resamples each mean from its ± s.e."} · hover for the distribution`
                      : `${c.pair} crossing (bootstrap too weak to quantify — add trajectories)`
                  }
                  className={`relative group/crs inline-flex max-w-full items-center gap-1.5 rounded-full border border-rose-500/30 bg-rose-500/10 px-2.5 py-0.5 font-mono text-[11px] text-rose-300 ${
                    c.boot ? "cursor-help hover:border-rose-400/50 hover:bg-rose-500/15 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-400/40" : ""
                  }`}
                >
                  {c.pair} → {c.p.toFixed(3)}
                  {c.boot && (
                    <span className="text-rose-400/80">
                      (+{(c.boot.hi - c.p).toFixed(3)}/−{(c.p - c.boot.lo).toFixed(3)})
                    </span>
                  )}
                  {c.boot?.hitRate != null && c.boot.hitRate < 0.95 && (
                    <span className="text-amber-400/80" title="fraction of bootstrap resamples in which a crossing was found">
                      · {(c.boot.hitRate * 100).toFixed(0)}%
                    </span>
                  )}
                  {c.boot && <CrossingHisto boot={c.boot} pair={c.pair} />}
                </span>
              ))
            ) : (
              <span className="text-xs text-zinc-500">no sign change in the p-grid yet — add sizes or trajectories</span>
            )}
            <button
              onClick={copyCsv}
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-zinc-500 px-2.5 py-1 text-xs text-zinc-300 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              {copied ? <Check className="size-3.5 text-emerald-400" /> : <Copy className="size-3.5" />}
              {copied ? "copied" : "copy CSV"}
            </button>
            <button
              onClick={downloadCsv}
              title="download the sweep as a .csv file"
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-emerald-500/50 px-2.5 py-1 text-xs text-zinc-300 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              {downloaded ? <Check className="size-3.5 text-emerald-400" /> : <Download className="size-3.5" />}
              {downloaded ? "saved" : "download"}
            </button>
            <span
              className="inline-flex items-center gap-1 rounded-md border border-zinc-800 bg-zinc-950/60 pl-2 pr-1 py-0.5"
              title="bootstrap resamples per crossing — bigger B smooths the distributions at the cost of a brief synchronous recompute"
            >
              <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-600">B</span>
              {[500, 2000, 8000].map((v) => (
                <button
                  key={v}
                  onClick={() => setCrossB(v)}
                  aria-pressed={crossB === v}
                  className={`rounded px-1.5 py-0.5 text-[11px] font-mono transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-400/40 ${
                    crossB === v ? "bg-rose-500/15 text-rose-300" : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  {v}
                </button>
              ))}
            </span>
            <button
              onClick={() => setShowLit((v) => !v)}
              aria-pressed={showLit}
              title="overlay the deposited + literature p_c estimates on your curves — this work 0.1597(8) · Gullans–Huse 0.1593(5) · Sierant 0.15995(10), each as a 1σ vertical band"
              className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-xs font-mono transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500/40 ${
                showLit
                  ? "border-amber-500/40 bg-amber-500/10 text-amber-300"
                  : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
              }`}
            >
              <GitCompare className="size-3.5" />
              literature p_c
            </button>
          </div>
          {showLit && crossings.length > 0 && (
            <p className="text-[11px] text-zinc-500 font-mono flex flex-wrap items-center gap-x-3 gap-y-1">
              <span className="text-amber-400/80">■ this work 0.1597(8)</span>
              <span className="text-purple-400/80">■ Gullans–Huse 0.1593(5)</span>
              <span className="text-orange-400/80">■ Sierant 0.15995(10)</span>
              <span className="text-zinc-600">— three independent locators of the same transition; your crossings (rose) should drift toward them as L grows</span>
            </p>
          )}
          {overlays.length > 0 && (
            <p className="text-xs text-zinc-500 flex items-center gap-1.5">
              <GitCompare className="size-3.5 text-zinc-600" />
              overlaying {overlays.length} saved sweep{overlays.length > 1 ? "s" : ""} (dashed) — hover the chart for a point-by-point readout
            </p>
          )}
          {loadedMeansOnly && (
            <p className="text-xs text-amber-400/80 flex flex-wrap items-center gap-1.5 font-mono">
              <RefreshCw className="size-3.5 shrink-0" />
              <span>loaded from the board — this save carries means only (older record), so bootstraps fall back to parametric;</span>
              <button
                onClick={run}
                disabled={busy}
                className="underline underline-offset-2 hover:text-amber-300 disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500/40 rounded"
              >
                re-run at these sizes
              </button>
              <span>to unlock trajectory-level statistics</span>
            </p>
          )}
          <p className="text-xs text-zinc-500 leading-relaxed">
            Small-system sweeps of the same engine (L ≤ {Math.max(...sizes, 8)}, τ ≤ {tau}L, {nTraj} trajectories/point): the
            I₃ crossing drifts toward p_c as L grows. The deposited locator —{" "}
            <span className="text-amber-400/90 font-mono">p_c = 0.1597(8)</span> — used L up to 512 with
            475,600 trajectories; pair crossings of L ≥ 64 curves landed at 0.1606–0.1628 before
            extrapolation. Error bars shrink as ~1/√N.
          </p>
        </div>
      )}

      {/* collapse-view controls */}
      {hasData && view === "collapse" && (
        <div className="mt-4 space-y-4">
          <div className="grid sm:grid-cols-2 gap-x-6 gap-y-4">
            <div>
              <div className="flex justify-between text-xs font-mono text-zinc-500">
                <span>p_c</span>
                <span className="text-amber-400">{pc.toFixed(4)}</span>
              </div>
              <input
                type="range"
                min={0.13}
                max={0.19}
                step={0.0005}
                value={pc}
                onChange={(e) => { setPc(Number(e.target.value)); setScanResult(null); }}
                className="mt-1.5 w-full accent-amber-500"
                aria-label="Critical point p_c for your collapse"
              />
            </div>
            <div>
              <div className="flex justify-between text-xs font-mono text-zinc-500">
                <span>ν</span>
                <span className="text-emerald-400">{nu.toFixed(3)}</span>
              </div>
              <input
                type="range"
                min={0.8}
                max={1.8}
                step={0.005}
                value={nu}
                onChange={(e) => { setNu(Number(e.target.value)); setScanResult(null); }}
                className="mt-1.5 w-full accent-emerald-500"
                aria-label="Exponent nu for your collapse"
              />
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="flex-1 min-w-[180px]">
              <div className="flex justify-between text-[11px] font-mono text-zinc-500 mb-1">
                <span>collapse tightness (fuller = better)</span>
                <span className={Number.isFinite(qNorm) ? (qNorm <= 1.1 ? "text-emerald-400" : qNorm <= 1.5 ? "text-amber-400" : "text-rose-400") : "text-zinc-500"}>
                  {!qIsNum
                    ? "not enough points in window"
                    : scanResult
                      ? "at your scan minimum"
                      : Number.isFinite(qNorm)
                        ? `${(qNorm * 100).toFixed(0)}% of (0.1597, 1.24) scatter`
                        : "—"}
                </span>
              </div>
              <div className="h-1.5 rounded-full bg-zinc-800 overflow-hidden" role="progressbar" aria-valuenow={Number.isFinite(qNorm) ? Math.round(Math.min(100, 100 / qNorm)) : 0} aria-valuemin={0} aria-valuemax={100}>
                <div
                  className={`h-full rounded-full transition-all duration-300 ${
                    !Number.isFinite(qNorm) ? "bg-zinc-600" : qNorm <= 1.1 ? "bg-emerald-500" : qNorm <= 1.5 ? "bg-amber-500" : "bg-rose-500"
                  }`}
                  style={{ width: `${Number.isFinite(qNorm) ? Math.min(100, Math.max(4, 100 / qNorm)) : 4}%` }}
                />
              </div>
            </div>
            <button
              onClick={scanBestFit}
              disabled={scanning}
              className="inline-flex items-center gap-1.5 rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-300 hover:bg-emerald-500/20 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              {scanning ? <Loader2 className="size-3.5 animate-spin" /> : <Sparkles className="size-3.5" />}
              {scanning ? "scanning…" : "scan for best collapse"}
            </button>
            <button
              onClick={() => { setPc(PC_REF); setNu(NU_REF); setScanResult(null); }}
              className="inline-flex items-center gap-1.5 rounded-lg border border-zinc-700 px-3 py-1.5 text-xs font-medium text-zinc-400 hover:border-zinc-500 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              <SlidersHorizontal className="size-3.5" />
              deposited values
            </button>
          </div>

          {scanResult && (
            <p className="text-xs text-emerald-400/90 font-mono">
              grid scan (p_c ∈ [0.140, 0.180] × ν ∈ [0.90, 1.70]) → best collapse at p_c = {scanResult.pc.toFixed(4)}, ν = {scanResult.nu.toFixed(2)}
            </p>
          )}
          {overlays.length > 0 && (
            <p className="text-xs text-zinc-500 flex items-center gap-1.5">
              <GitCompare className="size-3.5 text-zinc-600" />
              overlaying {overlays.length} saved sweep{overlays.length > 1 ? "s" : ""} (dashed) — collapsed at your current (p_c, ν), so sweeps at different τ or trajectory counts can be compared in collapsed coordinates
            </p>
          )}
          <p className="text-xs text-zinc-500 leading-relaxed">
            The same quartic-fit-in-window method the paper uses (|x| ≤ 3), with the error floor set to
            1/N per point — the paper&apos;s own disclosed fix for the 10⁻⁴-floor weighting defect that let a
            saturated I₃ ≡ 0 point carry 98% of a fit&apos;s weight. With L ≤ {Math.max(...sizes, 64)} and O(10²) trajectories,
            finite-size corrections dominate: expect your best (p_c, ν) to drift from the deposited
            0.1597(8) / 1.24(7) — that drift is the finite-size story itself.
          </p>
        </div>
      )}

      {/* profile-view readout */}
      {hasData && view === "profile" && (profileTarget === "nu" ? profile : pcProfile) && (
        <div className="mt-4 space-y-3" aria-live="polite">
          <div className="flex flex-wrap items-center gap-2">
            {profileTarget === "nu" && profile ? (
              <>
                <span className="inline-flex max-w-full items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-0.5 font-mono text-[11px] text-emerald-300">
                  your ν = {profile.best.nu.toFixed(2)}
                  <SigmaNote best={profile.best.nu} sigma={profile.sigma} digits={2} />
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 font-mono text-[11px] text-amber-300">
                  best p_c = {profile.best.pc.toFixed(4)}
                </span>
              </>
            ) : pcProfile ? (
              <>
                <span className="inline-flex max-w-full items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-0.5 font-mono text-[11px] text-emerald-300">
                  your p_c = {pcProfile.best.pc.toFixed(4)}
                  <SigmaNote best={pcProfile.best.pc} sigma={pcProfile.sigma} digits={4} />
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 font-mono text-[11px] text-amber-300">
                  best ν = {pcProfile.best.nu.toFixed(2)}
                </span>
              </>
            ) : null}
            {dchi2AtReference != null && (
              <span
                title={dchi2AtReference.caveat ?? undefined}
                className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[11px] ${dchi2AtReference.dchi2 >= 25 ? "border-rose-500/30 bg-rose-500/10 text-rose-300" : "border-zinc-700 text-zinc-400"}`}
              >
                Δχ²({dchi2AtReference.at}) = {dchi2AtReference.dchi2 < 10 ? dchi2AtReference.dchi2.toFixed(2) : dchi2AtReference.dchi2.toFixed(0)}
                {dchi2AtReference.dchi2 >= 25 ? " · excluded" : dchi2AtReference.dchi2 >= 1 ? " · disfavoured" : " · not excluded"}
                {dchi2AtReference.caveat && " · nearest pt"}
              </span>
            )}
            {profileRefUsed && !profileRefUsed.deposited && (
              <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 font-mono text-[11px] text-amber-300" title="The deposited (0.1597, 1.24) window captured too few of your grid points — the window was frozen at your own scan-best instead, keeping membership comparable across the profile.">
                window frozen at your scan-best ({profileRefUsed.pc.toFixed(4)}, {profileRefUsed.nu.toFixed(2)})
              </span>
            )}
            {edgeMinimum && (
              <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 font-mono text-[11px] text-amber-300">
                minimum at grid edge — {profileTarget === "nu" ? "ν" : "p_c"} not yet constrained
              </span>
            )}
            {jointVsDeposited && (
              <span
                title={`Joint 1σ region from BOTH profiles (ν from the ν-profile, p_c from the p_c-profile) vs the deposited point (0.1597, 1.24). ${jointVsDeposited.inPc ? "deposited p_c inside your p_c interval" : "deposited p_c outside your p_c interval"}; ${jointVsDeposited.inNu ? "deposited ν inside your ν interval" : "deposited ν outside your ν interval"}. At these sizes a coordinate outside is the honest finite-size story, not an error.`}
                className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[11px] ${
                  jointVsDeposited.both
                    ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
                    : jointVsDeposited.inPc || jointVsDeposited.inNu
                      ? "border-amber-500/30 bg-amber-500/10 text-amber-300"
                      : "border-zinc-700 text-zinc-400"
                }`}
              >
                <GitCompare className="size-3" />
                joint 1σ vs deposited: p_c {jointVsDeposited.inPc ? "✓" : "✗"} · ν {jointVsDeposited.inNu ? "✓" : "✗"}
              </span>
            )}
            {activeBoot && (
              <span
                tabIndex={0}
                title={`${activeBoot.kind === "traj" ? "trajectory-level (non-parametric) bootstrap — resamples your actual per-trajectory values" : "parametric bootstrap — resamples each mean from its ± s.e."} B = ${activeBoot.B} times, re-fitting the whole profile per resample; the central 68% of the minima distribution. Hover for the distribution.`}
                className="relative group/crs inline-flex max-w-full cursor-help items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-0.5 font-mono text-[11px] text-emerald-300 transition-colors hover:border-emerald-400/50 hover:bg-emerald-500/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
              >
                bootstrap {profileTarget === "nu" ? "ν̂" : "p̂_c"} 68% [{fmtBoot(activeBoot.min.lo)}, {fmtBoot(activeBoot.min.hi)}] · B={activeBoot.B} · {activeBoot.kind === "traj" ? "traj" : "param"}
                <BootHisto boot={activeBoot} target={profileTarget} />
              </span>
            )}
            <button
              onClick={runBootstrap}
              disabled={bootRunning || profiling || !(profileTarget === "nu" ? profile : pcProfile)}
              title="resample your trajectories — a 68% envelope on the Δχ² curve plus a bootstrap interval on the profiled parameter (no Gaussian-shape assumption)"
              className="inline-flex items-center gap-1.5 rounded-md border border-amber-500/40 bg-amber-500/10 hover:bg-amber-500/20 px-2.5 py-1 text-xs font-medium text-amber-300 transition-colors disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500/40 active:scale-[0.97]"
            >
              {bootRunning ? <Loader2 className="size-3.5 animate-spin" /> : <BarChart3 className="size-3.5" />}
              {bootRunning ? `bootstrap… ${bootProgress.done}/${bootProgress.total}` : "bootstrap band"}
            </button>
            <span
              className="inline-flex items-center gap-1 rounded-md border border-zinc-800 bg-zinc-950/60 pl-2 pr-1 py-0.5"
              title="bootstrap resamples — bigger B smooths the envelope + minima histogram; the driver stays chunked and non-blocking either way"
            >
              <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-600">B</span>
              {[60, 120, 240].map((v) => (
                <button
                  key={v}
                  onClick={() => setProfB(v)}
                  disabled={bootRunning}
                  aria-pressed={profB === v}
                  className={`rounded px-1.5 py-0.5 text-[11px] font-mono transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500/40 disabled:opacity-40 ${
                    profB === v ? "bg-amber-500/15 text-amber-300" : "text-zinc-500 hover:text-zinc-300"
                  }`}
                >
                  {v}
                </button>
              ))}
            </span>
            {methodsAgree != null && (
              <span
                title={`The Δχ² = 1 interval and the bootstrap interval are two independent uncertainty constructions on the same ${profileTarget === "nu" ? "ν" : "p_c"}. Shared span / combined span: ${(methodsAgree.overlapFrac * 100).toFixed(0)}% — they should agree substantially at small-system resolution.`}
                className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[11px] ${
                  methodsAgree.overlapFrac >= 0.5
                    ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
                    : "border-amber-500/30 bg-amber-500/10 text-amber-300"
                }`}
              >
                methods agree {(methodsAgree.overlapFrac * 100).toFixed(0)}%
              </span>
            )}
            {bootRunning && (
              <span
                className="w-32 h-1.5 rounded-full bg-zinc-800 overflow-hidden inline-block"
                role="progressbar"
                aria-valuenow={Math.round((100 * bootProgress.done) / bootProgress.total)}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label="Bootstrap progress"
              >
                <span
                  className="block h-full rounded-full bg-amber-400/80 transition-all duration-200"
                  style={{ width: `${Math.max(4, (100 * bootProgress.done) / bootProgress.total)}%` }}
                />
              </span>
            )}
            <button
              onClick={computeProfile}
              disabled={profiling}
              className="ml-auto inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-zinc-500 px-2.5 py-1 text-xs text-zinc-300 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              {profiling ? <Loader2 className="size-3.5 animate-spin" /> : <Sparkles className="size-3.5" />}
              recompute
            </button>
            <button
              onClick={copyProfileCsv}
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-zinc-500 px-2.5 py-1 text-xs text-zinc-300 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              {copiedProfile ? <Check className="size-3.5 text-emerald-400" /> : <Copy className="size-3.5" />}
              {copiedProfile ? "copied" : "copy CSV"}
            </button>
            <button
              onClick={downloadProfileCsv}
              title="download the profile as a .csv file"
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-emerald-500/50 px-2.5 py-1 text-xs text-zinc-300 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              {downloadedProfile ? <Check className="size-3.5 text-emerald-400" /> : <Download className="size-3.5" />}
              {downloadedProfile ? "saved" : "download"}
            </button>
          </div>
          {(profileTarget === "nu" ? profile : pcProfile) && (
            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 px-3 sm:px-4 py-2.5">
              <IntervalRuler
                mode={profileTarget}
                best={profileTarget === "nu" ? profile!.best.nu : pcProfile!.best.pc}
                sigma={profileSigma ?? { lo: null, hi: null }}
              />
            </div>
          )}
          <p className="text-xs text-zinc-500 leading-relaxed">
            {profileTarget === "nu" ? (
              <>
                Every ν on this profile re-optimises p_c over [0.140, 0.180] before recording χ² — so the curve
                is a genuine profile, not a slice{(sizes.length < 3 ? "; with fewer than 3 sizes ν is only weakly constrained — the minimum can sit at the grid edge" : "")}.
                The Δχ² = 1 crossings (green band) give your 1σ interval on ν;
                the paper&apos;s full-size version of this same construction quotes{" "}
                <span className="text-emerald-400/90 font-mono">ν = 1.24(7)</span> and excludes ν = 1 at{" "}
                <span className="text-rose-400/90 font-mono">Δχ² ≥ 52</span>. Your L ≤ 64, O(10²)-trajectory
                profile is wider — watch it tighten as you add sizes and trajectories.
                {activeBoot && <> The dashed curve + shaded envelope add the trajectory-resampled bootstrap median and 68% band{activeBoot.kind === "traj" ? " (non-parametric — your actual trajectories, resampled)" : " (parametric — this sweep carries no trajectory data; re-run to upgrade)"}.</>}
              </>
            ) : (
              <>
                The mirror construction: every p_c re-optimises ν over [0.90, 1.70] before recording χ², so this
                curve brackets p_c the same way the ν profile brackets ν{(sizes.length < 3 ? "; with fewer than 3 sizes the interval is dominated by finite-size drift" : "")}.
                The Δχ² = 1 crossings give your 1σ interval on p_c — the paper&apos;s full-size
                version of this construction quotes <span className="text-emerald-400/90 font-mono">p_c = 0.1597(8)</span>{" "}
                (purification locator 0.1601–0.1604; Gullans–Huse 0.1593(5), rose line). Your small-system
                interval is wider and centred slightly low — the same finite-size drift the raw crossings show.
                {activeBoot && <> The bootstrap band shows how much the whole curve wanders under trajectory resampling; strongly drifting resamples whose minimum piles at the grid edge are re-centred outward (bounded to [0.13, 0.19]) — the histogram discloses how often.</>}
              </>
            )}
          </p>
        </div>
      )}

      {/* community board */}
      {hasData && (
        <div className="mt-5 pt-5 border-t border-zinc-800/70">
          <div className="flex flex-wrap items-center gap-2.5">
            <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">community sweeps</span>
            {sweeps.length > 0 && (
              <span className="rounded-full border border-zinc-700 bg-zinc-900/60 px-2 py-px text-[10px] font-mono text-zinc-500 tabular-nums">
                {boardTotal != null && boardTotal > sweeps.length ? `${sweeps.length} of ${boardTotal} saved` : `${sweeps.length} saved`}
              </span>
            )}
            <button
              onClick={exportState}
              title="download the full explorer state (params + curves + trajectory values) as a .json file"
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-zinc-500 px-2.5 py-1 text-xs text-zinc-300 transition-colors active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              <Download className="size-3.5" />
              export state
            </button>
            <button
              onClick={() => fileRef.current?.click()}
              title="restore a previously exported sweep-state .json"
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-zinc-500 px-2.5 py-1 text-xs text-zinc-300 transition-colors active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              <Upload className="size-3.5" />
              import state
            </button>
            <input
              ref={fileRef}
              type="file"
              accept="application/json,.json"
              onChange={onImportFile}
              className="hidden"
              aria-label="Import sweep-state JSON file"
            />
            <button
              onClick={save}
              disabled={saveState !== "idle" || sizes.filter((L) => (series[L] ?? []).length > 0).length < 2}
              className="ml-auto inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-emerald-500/50 px-2.5 py-1 text-xs text-zinc-300 transition-colors disabled:opacity-50 active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
            >
              {saveState === "saving" ? <Loader2 className="size-3.5 animate-spin" /> : saveState === "saved" ? <Check className="size-3.5 text-emerald-400" /> : <Save className="size-3.5" />}
              {saveState === "saved" ? "saved" : "save this sweep"}
            </button>
          </div>
          {sweeps.length > 0 ? (
            <>
              <p className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-[10px] font-mono text-zinc-600">
                <span className="inline-flex items-center gap-1">
                  <svg width="18" height="7" viewBox="0 0 18 7" aria-hidden>
                    <path d="M1,6 C5,6 7,3 10,3 C13,3 15,2 17,1" fill="none" stroke="#34d399" strokeWidth="1.3" />
                  </svg>
                  smallest-L mean curve
                </span>
                <span className="inline-flex items-center gap-1">
                  <span className="rounded border border-emerald-500/30 bg-emerald-500/10 px-1 text-[9px] text-emerald-400/90">traj</span>
                  carries per-trajectory values — non-parametric bootstraps survive the round trip
                </span>
                <span>{showAll ? `all ${sweeps.length} rows` : "newest first · up to 12"}</span>
                {boardTotal != null && boardTotal > 12 && (
                  <button
                    onClick={() => setShowAll((v) => !v)}
                    className="inline-flex items-center gap-1 rounded border border-zinc-700 px-1.5 py-px text-[9px] text-zinc-400 transition-colors hover:border-emerald-500/40 hover:text-emerald-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
                    title={showAll ? "collapse the board back to the newest 12 rows" : `show all ${boardTotal} saved sweeps (up to 100)`}
                  >
                    {showAll ? "← newest 12" : `show all ${boardTotal}`}
                  </button>
                )}
              </p>
              <div className="mt-2.5 max-h-44 overflow-y-auto rounded-lg border border-zinc-800 divide-y divide-zinc-800/70 custom-scroll">
              {sweeps.map((sw) => {
                const selected = compareIds.includes(sw.id);
                return (
                  <div key={sw.id} className="flex items-center gap-3 px-3 py-2 text-sm font-mono hover:bg-zinc-800/30 transition-colors">
                    <button
                      onClick={() => toggleCompare(sw.id)}
                      role="checkbox"
                      aria-checked={selected}
                      title={selected ? "Remove from comparison" : "Overlay on the chart (dashed)"}
                      className={`shrink-0 grid place-items-center size-4 rounded border transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                        selected
                          ? "border-emerald-500/60 bg-emerald-500/20 text-emerald-300"
                          : "border-zinc-600 text-transparent hover:border-zinc-400"
                      }`}
                    >
                      <Check className="size-3" />
                    </button>
                    <SweepSparkline seriesJson={sw.seriesJson} />
                    <button
                      onClick={() => void loadSweep(sw)}
                      className="min-w-0 flex-1 text-left group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 rounded px-0.5"
                      title={sw.hasTraj === false ? "Load this sweep into the explorer (means only — older save)" : "Load this sweep into the explorer"}
                    >
                      <span className={`transition-colors truncate ${selected ? "text-emerald-300" : "text-zinc-300 group-hover:text-emerald-300"}`}>{sw.label}</span>
                      {sw.hasTraj && (
                        <span
                          title="this save carries per-trajectory values — loading it restores non-parametric (trajectory-level) bootstraps"
                          className="ml-1.5 inline-flex items-center rounded border border-emerald-500/30 bg-emerald-500/10 px-1 py-px text-[9px] font-mono text-emerald-400/90 align-middle"
                        >
                          traj
                        </span>
                      )}
                      <span className="ml-2 text-[11px] text-zinc-600 hidden sm:inline">{new Date(sw.createdAt).toLocaleString()}</span>
                    </button>
                    <button
                      onClick={() => shareSweep(sw)}
                      className={`shrink-0 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 rounded ${
                        sharedId === sw.id ? "text-emerald-400" : "text-zinc-600 hover:text-emerald-400"
                      }`}
                      aria-label={`Copy a share link for ${sw.label}`}
                      title="copy a link that loads exactly this sweep on open"
                    >
                      {sharedId === sw.id ? <Check className="size-3.5" /> : <Link2 className="size-3.5" />}
                    </button>
                    <button
                      onClick={() => del(sw.id)}
                      className="shrink-0 text-zinc-600 hover:text-rose-400 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-500/40 rounded"
                      aria-label={`Delete sweep ${sw.label}`}
                    >
                      <Trash2 className="size-3.5" />
                    </button>
                  </div>
                );
              })}
              </div>
            </>
          ) : (
            <p className="mt-2 text-xs text-zinc-600 flex items-center gap-1.5">
              <FolderOpen className="size-3.5" />
              no saved sweeps yet — run one and save it to share with future visitors (stored in SQLite, now with trajectory data)
            </p>
          )}
          {compareIds.length > 0 && (
            <p className="mt-2 text-[11px] text-zinc-600 font-mono flex items-center gap-1.5">
              <GitCompare className="size-3" />
              comparing {compareIds.length}/3 saved sweeps (dashed) with your live curves — up to 3; toggle off or load one to edit
            </p>
          )}
        </div>
      )}
    </div>
  );
}
