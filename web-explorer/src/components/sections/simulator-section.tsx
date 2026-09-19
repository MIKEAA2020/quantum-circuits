"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Play, Pause, StepForward, RotateCcw, Dices, Gauge, Zap, Share2, Check } from "lucide-react";
import { HybridCircuit, getSp4, type LayerEvent, type PeriodRecord, type SimMode } from "@/lib/quantum/clifford";
import { LiveChart, SERIES_COLORS } from "@/components/charts/live-chart";
import { EnsemblePanel } from "./ensemble-panel";
import { I3SweepPanel } from "./i3-sweep-panel";
import { SectionHeading } from "./section-heading";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const PC = 0.1597;

function phaseOf(p: number): { label: string; cls: string; dot: string } {
  if (p < 0.145) return { label: "volume-law phase", cls: "text-emerald-300 border-emerald-500/30 bg-emerald-500/10", dot: "bg-emerald-400" };
  if (p <= 0.175) return { label: "critical regime", cls: "text-amber-300 border-amber-500/30 bg-amber-500/10", dot: "bg-amber-400" };
  return { label: "area-law phase", cls: "text-rose-300 border-rose-500/30 bg-rose-500/10", dot: "bg-rose-400" };
}

/** 4×4 symplectic matrix of gate g, as 4 binary rows — for the tooltips. */
function gateMatrixLabel(g: number): string {
  const M = getSp4()[g];
  const rows: string[] = [];
  for (let r = 0; r < 4; r++) {
    rows.push(`${M[r * 4]}${M[r * 4 + 1]} ${M[r * 4 + 2]}${M[r * 4 + 3]}`);
  }
  return `Sp(4,2) #${g} · (${rows.join(" / ")})`;
}

function CircuitView({
  events,
  L,
  mode,
  t,
}: {
  events: LayerEvent[][]; // events[period-1] = 4 layers
  L: number;
  mode: SimMode;
  t: number;
}) {
  const rows = mode === "purif" ? 2 * L : L;
  const colW = 30;
  const W = Math.max(events.length * colW + 60, 360);
  const rowH = Math.min(22, 380 / Math.max(rows, 1));
  const y = (i: number) => 26 + i * rowH;
  const H = y(rows - 1) + 30;
  const gateTone = (g: number) => {
    const tones = ["#34d399", "#2dd4bf", "#6ee7b7", "#10b981"];
    return tones[g % 4];
  };

  return (
    <div className="overflow-x-auto rounded-lg border border-zinc-800 bg-zinc-950/60 custom-scroll" aria-label="Circuit visualization">
      <svg viewBox={`0 0 ${W} ${H}`} width={W} height={H} className="block" role="img" aria-label="Circuit diagram of the running simulation">
        {Array.from({ length: rows }, (_, i) => {
          const isRef = mode === "purif" && i >= L;
          return (
            <g key={i} opacity={isRef ? 0.38 : 1}>
              <line x1={40} x2={W - 12} y1={y(i)} y2={y(i)} stroke="currentColor" className={isRef ? "text-zinc-800" : "text-zinc-700"} strokeWidth={1.2} />
              <text x={34} y={y(i) + 3.5} textAnchor="end" className="fill-zinc-600 text-[9px] font-mono">{i}</text>
            </g>
          );
        })}
        {mode === "purif" && (
          <>
            <line x1={40} x2={W - 12} y1={(y(L - 1) + y(L)) / 2} y2={(y(L - 1) + y(L)) / 2} stroke="#f59e0b" strokeOpacity={0.35} strokeWidth={1} strokeDasharray="4 4" />
            <text x={44} y={(y(L - 1) + y(L)) / 2 - 4} className="fill-amber-600/90 text-[8px] font-mono uppercase tracking-wider">reference · untouched</text>
          </>
        )}

        {events.map((layers, pi) => {
          const x0 = 48 + pi * colW;
          return (
            <g key={pi}>
              {layers.map((layer, li) => {
                const dx = x0 + (layer.kind === "meas" ? 0 : 12);
                if (layer.kind === "meas") {
                  return (layer.measured ?? []).map((s) => (
                    <g key={`${pi}-${li}-${s}`} className="cursor-help">
                      <title>{`Z-measurement · site ${s}`}</title>
                      <circle cx={dx} cy={y(s)} r={5} fill="#f59e0b" fillOpacity={0.25} stroke="#f59e0b" strokeWidth={1.2} />
                      <path d={`M${dx - 2},${y(s) - 2} L${dx + 2},${y(s) + 2}`} stroke="#f59e0b" strokeWidth={1} />
                    </g>
                  ));
                }
                return (layer.gates ?? []).map((g, gi) => {
                  const a = Math.min(g.i, g.j);
                  const b = Math.max(g.i, g.j);
                  const top = y(a);
                  const bot = y(b);
                  const h = bot - top;
                  const tone = gateTone(g.g);
                  const tip = <title>{gateMatrixLabel(g.g)} · qubits ({g.i}, {g.j})</title>;
                  if (g.i > g.j) {
                    // wraparound gate on the ring
                    return (
                      <g key={`${pi}-${li}-${gi}`} className="cursor-help">
                        {tip}
                        <rect x={dx - 5.5} y={y(0) - 8} width={11} height={(top - y(0)) + 14} rx={4} fill={tone} fillOpacity={0.14} stroke={tone} strokeWidth={1} className="hover:[fill-opacity:0.4] hover:stroke-zinc-300" />
                        <rect x={dx - 5.5} y={bot - 6} width={11} height={y(rows - 1) - bot + 12} rx={4} fill={tone} fillOpacity={0.14} stroke={tone} strokeWidth={1} className="hover:[fill-opacity:0.4] hover:stroke-zinc-300" />
                      </g>
                    );
                  }
                  return (
                    <g key={`${pi}-${li}-${gi}`} className="cursor-help">
                      {tip}
                      <rect x={dx - 5.5} y={top - 7} width={11} height={h + 14} rx={4} fill={tone} fillOpacity={0.14} stroke={tone} strokeWidth={1} className="hover:[fill-opacity:0.4] hover:stroke-zinc-300" />
                    </g>
                  );
                });
              })}
              {pi % Math.max(1, Math.round(L / 2)) === 0 && (
                <text x={x0 + 4} y={H - 6} className="fill-zinc-600 text-[8px] font-mono">{pi + 1}</text>
              )}
            </g>
          );
        })}
        {/* playhead */}
        {t > 0 && (
          <line x1={48 + t * colW - colW / 2} x2={48 + t * colW - colW / 2} y1={14} y2={H - 14} stroke="#fafafa" strokeOpacity={0.25} strokeWidth={1} />
        )}
      </svg>
    </div>
  );
}

interface SharedState {
  mode: SimMode;
  L: number;
  p: number;
  tau: number;
  seed: number;
}

const L_CHOICES = [8, 12, 16, 20, 24];

function encodeSim(s: SharedState): string {
  return `sim=${s.mode},${s.L},${s.p.toFixed(3)},${s.tau},${s.seed}`;
}

export function SimulatorSection() {
  const [mode, setMode] = useState<SimMode>("purif");
  const [L, setL] = useState(16);
  const [p, setP] = useState(0.16);
  const [tauMax, setTauMax] = useState(2);
  const [seed, setSeed] = useState(20240613);
  const [speed, setSpeed] = useState(2);
  const [running, setRunning] = useState(false);
  const [copied, setCopied] = useState(false);
  /** active ensemble-tools tab; auto-switches to the I₃ locator for board shares */
  const [toolsTab, setToolsTab] = useState<"purif" | "i3">("purif");
  /** ?board=<id> from a shared link — consumed by the sweep panel when it mounts */
  const [boardId, setBoardId] = useState<string | null>(null);

  const [records, setRecords] = useState<PeriodRecord[]>([]);
  const [events, setEvents] = useState<LayerEvent[][]>([]);
  const [stats, setStats] = useState<PeriodRecord | null>(null);

  const simRef = useRef<HybridCircuit | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const sectionRef = useRef<HTMLElement | null>(null);
  const visibleRef = useRef(false);
  const maxT = tauMax * L;

  const reset = useCallback(
    (m: SimMode, LL: number, pp: number, sd: number) => {
      simRef.current = new HybridCircuit({ L: LL, p: pp, mode: m, seed: sd });
      setRecords([]);
      setEvents([]);
      setStats(null);
      setRunning(false);
    },
    []
  );

  // deep-link support: apply ?sim=mode,L,p,tau,seed once after mount
  // (deferred one tick so the first paint matches the SSR output)
  useEffect(() => {
    let boardTimer: ReturnType<typeof setTimeout> | undefined;
    let simTimer: ReturnType<typeof setTimeout> | undefined;
    // shared community-board link: ?board=<id>#simulator — activate the I₃
    // locator tab and hand the id to the panel (it consumes it on mount),
    // then clean the URL so refreshes don't re-trigger the load
    try {
      const board = new URLSearchParams(window.location.search).get("board");
      if (board) {
        const url = new URL(window.location.href);
        url.searchParams.delete("board");
        window.history.replaceState(null, "", url.toString());
        boardTimer = setTimeout(() => {
          setBoardId(board);
          setToolsTab("i3");
        }, 0);
      }
    } catch {
      /* non-browser context */
    }
    try {
      const raw = new URLSearchParams(window.location.search).get("sim");
      if (!raw) return () => {
        if (boardTimer) clearTimeout(boardTimer);
      };
      const [m, l, pp, t, s] = raw.split(",");
      const md: SimMode | undefined = m === "pure" || m === "purif" ? m : undefined;
      const LL = L_CHOICES.includes(Number(l)) ? Number(l) : undefined;
      const pv = Number(pp);
      const tv = [1, 2, 4].includes(Number(t)) ? Number(t) : undefined;
      const sv = Number.isInteger(Number(s)) && Number(s) > 0 ? Number(s) : undefined;
      if (md && LL && pv >= 0 && pv <= 0.5 && tv && sv) {
        simTimer = setTimeout(() => {
          setMode(md);
          setL(LL);
          setP(pv);
          setTauMax(tv);
          setSeed(sv);
          reset(md, LL, pv, sv);
        }, 0);
      }
    } catch {
      /* malformed link — fall back to defaults */
    }
    return () => {
      if (boardTimer) clearTimeout(boardTimer);
      if (simTimer) clearTimeout(simTimer);
    };
  }, [reset]);

  // keep the URL shareable (replaceState: no navigation, no history spam)
  useEffect(() => {
    try {
      const url = new URL(window.location.href);
      url.searchParams.set("sim", `${mode},${L},${p.toFixed(3)},${tauMax},${seed}`);
      window.history.replaceState(null, "", url);
    } catch {
      /* SSR or file:// — ignore */
    }
  }, [mode, L, p, tauMax, seed]);

  const share = async () => {
    const link = `${window.location.origin}${window.location.pathname}?${encodeSim({ mode, L, p, tau: tauMax, seed })}#simulator`;
    try {
      await navigator.clipboard.writeText(link);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      window.prompt("Copy this link:", link);
    }
  };

  // param updaters reset the trajectory in the same handler (no effects needed)
  const updateMode = (m: SimMode) => {
    setMode(m);
    reset(m, L, p, seed);
  };
  const updateL = (v: number) => {
    setL(v);
    reset(mode, v, p, seed);
  };
  const updateP = (v: number) => {
    setP(v);
    reset(mode, L, v, seed);
  };
  const updateSeed = (v: number) => {
    setSeed(v);
    reset(mode, L, p, v);
  };

  // create the initial simulator lazily (once) for the first step
  if (simRef.current === null) {
    simRef.current = new HybridCircuit({ L, p, mode, seed });
  }

  const step = useCallback(
    (n = 1) => {
      const sim = simRef.current;
      if (!sim) return;
      const newRecords: PeriodRecord[] = [];
      const newEvents: LayerEvent[][] = [];
      for (let k = 0; k < n; k++) {
        if (sim.t >= maxT) break;
        const rec = sim.stepPeriod();
        newRecords.push({ ...rec });
        newEvents.push(sim.events.slice());
      }
      if (newRecords.length) {
        setRecords((r) => [...r, ...newRecords].slice(0, maxT));
        setEvents((e) => [...e, ...newEvents]);
        setStats(newRecords[newRecords.length - 1]);
      }
      if (simRef.current && simRef.current.t >= maxT) setRunning(false);
    },
    [maxT]
  );

  useEffect(() => {
    if (!running) return;
    const id = setInterval(() => step(speed), 90);
    return () => clearInterval(id);
  }, [running, speed, step]);

  // auto scroll circuit view
  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollLeft = el.scrollWidth;
  }, [events]);

  const done = (stats?.t ?? 0) >= maxT;

  // keyboard shortcuts — only while the simulator is in view and focus is
  // not on an interactive element (typing a seed must never be hijacked)
  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return;
    const io = new IntersectionObserver(([e]) => { visibleRef.current = e.isIntersecting; }, { threshold: 0.15 });
    io.observe(section);
    return () => io.disconnect();
  }, []);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!visibleRef.current) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "SELECT" || t.tagName === "TEXTAREA" || t.tagName === "BUTTON" || t.isContentEditable)) return;
      if (e.code === "Space") {
        e.preventDefault();
        if (done) {
          reset(mode, L, p, seed);
          setTimeout(() => setRunning(true), 30);
        } else setRunning((r) => !r);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        if (!running) step(1);
      } else if (e.key === "r" || e.key === "R") {
        reset(mode, L, p, seed);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [done, running, step, reset, mode, L, p, seed]);

  const series = useMemo(() => {
    const s: { name: string; color: string; points: { t: number; v: number }[] }[] = [];
    if (mode === "purif") {
      s.push({ name: "S_ref (purification)", color: SERIES_COLORS.sRef, points: records.map((r) => ({ t: r.t, v: r.sRef })) });
      s.push({ name: "S_A (system half-chain)", color: SERIES_COLORS.sA, points: records.map((r) => ({ t: r.t, v: r.sA })) });
    } else {
      s.push({ name: "S_A (half-chain)", color: SERIES_COLORS.sA, points: records.map((r) => ({ t: r.t, v: r.sA })) });
      s.push({ name: "I₃ (tripartite MI)", color: SERIES_COLORS.i3, points: records.map((r) => ({ t: r.t, v: r.i3 })) });
    }
    return s;
  }, [records, mode]);

  const phase = phaseOf(p);

  return (
    <section id="simulator" ref={sectionRef} className="scroll-mt-20 py-16 sm:py-20 border-t border-zinc-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <SectionHeading num="02" id="simulator" kicker="Live simulator" title={<>Run the Gottesman–Knill tableau yourself</>}>
          A faithful re-implementation of the deposited simulator: phase-free stabilizer tableau,
          uniform Sp(4,2) gates, Z-measurements at rate p. Watch entanglement grow, get cut down by
          measurements, and sit at the critical plateau near p ≈ p_c.
        </SectionHeading>

        <div className="mt-10 grid lg:grid-cols-[340px,1fr] gap-6 items-start">
          {/* controls */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 space-y-5 lg:sticky lg:top-20">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono uppercase tracking-wider text-zinc-500">protocol</span>
                <span className={`inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 text-[11px] font-mono ${phase.cls}`}>
                  <span className={`size-1.5 rounded-full ${phase.dot}`} />
                  {phase.label}
                </span>
              </div>
              <div className="mt-2 grid grid-cols-2 gap-2">
                {(["pure", "purif"] as SimMode[]).map((m) => (
                  <button
                    key={m}
                    onClick={() => updateMode(m)}
                    aria-pressed={mode === m}
                    className={`rounded-lg border px-3 py-2 text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                      mode === m
                        ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300 shadow-[0_0_16px_-8px_rgba(16,185,129,0.6)]"
                        : "border-zinc-700 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200"
                    }`}
                  >
                    {m === "pure" ? "Pure state · I₃" : "Purification · S_ref"}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-zinc-500">
                <span>qubits L</span>
                <span className="text-zinc-200">{L}</span>
              </div>
              <input
                type="range"
                min={8}
                max={24}
                step={4}
                value={L}
                onChange={(e) => updateL(Number(e.target.value))}
                className="mt-2 w-full accent-emerald-500"
                aria-label="System size L"
              />
              <p className="mt-1 text-[11px] text-zinc-500">
                {mode === "purif" ? `${L} system + ${L} reference qubits` : `${L} qubits`}
              </p>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-zinc-500">
                <span>measurement rate p</span>
                <span className={Math.abs(p - PC) < 0.01 ? "text-amber-400" : "text-zinc-200"}>{p.toFixed(3)}</span>
              </div>
              <input
                type="range"
                min={0}
                max={0.5}
                step={0.005}
                value={p}
                onChange={(e) => updateP(Number(e.target.value))}
                className="mt-2 w-full accent-amber-500"
                aria-label="Measurement probability p"
              />
              <div className="mt-1 flex justify-between text-[11px] text-zinc-600">
                <span>0</span>
                <span className={Math.abs(p - PC) < 0.01 ? "text-amber-500 font-mono" : ""}>p_c ≈ 0.160</span>
                <span>0.5</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-zinc-500">
                  <span>depth τ</span>
                  <span className="text-zinc-200">{tauMax}L</span>
                </div>
                <div className="mt-2 flex gap-1">
                  {[1, 2, 4].map((t) => (
                    <button
                      key={t}
                      onClick={() => setTauMax(t)}
                      aria-pressed={tauMax === t}
                      className={`flex-1 rounded-md border px-2 py-3 sm:py-1.5 text-xs font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                        tauMax === t ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300" : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
                      }`}
                    >
                      {t}L
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-zinc-500">
                  <span>speed</span>
                  <span className="text-zinc-200">{speed}×/tick</span>
                </div>
                <div className="mt-2 flex gap-1">
                  {[1, 2, 8, 32].map((s) => (
                    <button
                      key={s}
                      onClick={() => setSpeed(s)}
                      aria-pressed={speed === s}
                      className={`flex-1 rounded-md border px-1.5 py-3 sm:py-1.5 text-xs font-mono transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 ${
                        speed === s ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300" : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div>
              <div className="text-xs font-mono uppercase tracking-wider text-zinc-500">seed</div>
              <div className="mt-2 flex gap-2">
                <input
                  type="number"
                  value={seed}
                  onChange={(e) => updateSeed(Number(e.target.value) || 1)}
                  className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2 font-mono text-sm text-zinc-200 focus:border-emerald-500/60 focus:outline-none"
                  aria-label="Random seed"
                />
                <button
                  onClick={() => {
                    const s = Math.floor(Math.random() * 1e9);
                    setSeed(s);
                    reset(mode, L, p, s);
                  }}
                  className="shrink-0 inline-flex items-center gap-1.5 rounded-lg border border-zinc-700 px-3 py-2 text-sm text-zinc-300 hover:border-zinc-500 hover:bg-zinc-800/40 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
                  title="Randomize seed"
                >
                  <Dices className="size-4" />
                </button>
                <button
                  onClick={share}
                  className="shrink-0 inline-flex items-center gap-1.5 rounded-lg border border-zinc-700 px-3 py-2 text-sm text-zinc-300 hover:border-emerald-500/50 hover:bg-zinc-800/40 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
                  title="Copy a deep link to this simulator state"
                >
                  {copied ? <Check className="size-4 text-emerald-400" /> : <Share2 className="size-4" />}
                </button>
              </div>
              <p className="mt-1 text-[11px] text-zinc-600">
                deterministic — same seed, same trajectory (demo PRNG; deposited runs use MT19937)
                {copied && <span className="ml-1 text-emerald-500">· link copied</span>}
              </p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => {
                  if (done) {
                    reset(mode, L, p, seed);
                    setTimeout(() => setRunning(true), 30);
                  } else {
                    setRunning((r) => !r);
                  }
                }}
                className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 transition-all hover:-translate-y-0.5 px-4 py-2.5 text-sm font-medium text-emerald-950 shadow-[0_0_24px_-8px_rgba(16,185,129,0.55)] hover:shadow-[0_0_32px_-8px_rgba(16,185,129,0.75)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 active:translate-y-0 active:scale-[0.98]"
              >
                {done ? <RotateCcw className="size-4" /> : running ? <Pause className="size-4" /> : <Play className="size-4" />}
                {done ? "Restart" : running ? "Pause" : "Run"}
              </button>
              <button
                onClick={() => step(1)}
                className="inline-flex items-center justify-center rounded-lg border border-zinc-700 px-3.5 py-2.5 text-sm text-zinc-300 hover:border-zinc-500 hover:bg-zinc-800/40 active:scale-[0.96] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
                title="Advance one period"
              >
                <StepForward className="size-4" />
              </button>
              <button
                onClick={() => reset(mode, L, p, seed)}
                className="inline-flex items-center justify-center rounded-lg border border-zinc-700 px-3.5 py-2.5 text-sm text-zinc-300 hover:border-zinc-500 hover:bg-zinc-800/40 active:scale-[0.96] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40"
                title="Reset"
              >
                <RotateCcw className="size-4" />
              </button>
            </div>

            {/* keyboard hints */}
            <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-[11px] text-zinc-500 pt-1">
              <span className="inline-flex items-center gap-1.5">
                <kbd className="min-w-[2.1rem] text-center rounded border border-zinc-700 bg-zinc-900 px-1.5 py-1 font-mono text-[10px] text-zinc-300 shadow-[0_1px_0_rgba(255,255,255,0.06)_inset,0_-1px_0_rgba(0,0,0,0.4)_inset]">Space</kbd>
                run / pause
              </span>
              <span className="inline-flex items-center gap-1.5">
                <kbd className="min-w-[1.6rem] text-center rounded border border-zinc-700 bg-zinc-900 px-1.5 py-1 font-mono text-[10px] text-zinc-300 shadow-[0_1px_0_rgba(255,255,255,0.06)_inset,0_-1px_0_rgba(0,0,0,0.4)_inset]">→</kbd>
                step
              </span>
              <span className="inline-flex items-center gap-1.5">
                <kbd className="min-w-[1.6rem] text-center rounded border border-zinc-700 bg-zinc-900 px-1.5 py-1 font-mono text-[10px] text-zinc-300 shadow-[0_1px_0_rgba(255,255,255,0.06)_inset,0_-1px_0_rgba(0,0,0,0.4)_inset]">R</kbd>
                reset
              </span>
              <span className="text-zinc-600">(when this section is in view)</span>
            </div>

            {/* stats */}
            <div className="mt-1 rounded-lg border border-zinc-800 bg-zinc-950/60 p-3.5 grid grid-cols-2 gap-x-4 gap-y-2.5 font-mono text-sm">
              <Stat label="t / t_max" value={`${stats?.t ?? 0} / ${maxT}`} />
              <Stat label="t / L" value={stats ? (stats.t / L).toFixed(2) : "0.00"} />
              <Stat label="S_A" value={stats ? stats.sA.toFixed(2) : "—"} accent="text-emerald-400" />
              {mode === "purif" ? (
                <Stat label="S_ref" value={stats ? stats.sRef.toFixed(2) : "—"} accent="text-teal-400" />
              ) : (
                <Stat label="I₃" value={stats ? stats.i3.toFixed(2) : "—"} accent="text-rose-400" />
              )}
              <Stat label="N_meas" value={stats ? stats.nMeas.toString() : "—"} />
              <Stat label="random outcomes" value={stats ? stats.nRand.toString() : "—"} />
            </div>
          </div>

          {/* viz + chart */}
          <div className="space-y-6 min-w-0">
            <div ref={scrollRef} className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-zinc-400 mb-3">
                <Gauge className="size-3.5 text-emerald-500/80" />
                circuit · scroll horizontally · hover a gate for its symplectic matrix
              </div>
              <CircuitView events={events} L={L} mode={mode} t={stats?.t ?? 0} />
              <p className="mt-3 text-[11px] text-zinc-600 flex flex-wrap gap-x-4 gap-y-1">
                <span><span className="text-emerald-400">▮</span> random Sp(4,2) gate</span>
                <span><span className="text-amber-500">◉</span> Z-measurement</span>
                {mode === "purif" && <span><span className="text-amber-700">---</span> system / reference boundary</span>}
              </p>
            </div>

            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-zinc-400 mb-3">
                <Zap className="size-3.5 text-amber-500/80" />
                observables vs time
              </div>
              {records.length === 0 ? (
                <div className="h-[240px] grid place-items-center text-sm text-zinc-500 border border-dashed border-zinc-800 rounded-lg">
                  press <span className="mx-1 px-1.5 py-0.5 rounded bg-zinc-800 font-mono text-xs text-zinc-300">Run</span> to start the trajectory
                </div>
              ) : (
                <LiveChart series={series} tauMax={tauMax} L={L} height={260} />
              )}
            </div>
          </div>
        </div>

        {/* ensemble tools — the I₃ explorer is force-mounted (hidden, not
            unmounted, when inactive): its runs, crossings, profiles and
            bootstrap state survive a switch to the purification tab */}
        <Tabs value={toolsTab} onValueChange={(v) => setToolsTab(v as "purif" | "i3")} className="mt-8">
          <TabsList className="bg-zinc-900/70 border border-zinc-800 h-auto p-1 rounded-xl gap-1">
            <TabsTrigger
              value="purif"
              className="text-zinc-400 hover:text-zinc-100 data-[state=active]:bg-emerald-500/10 data-[state=active]:text-emerald-300 data-[state=active]:border-emerald-500/40 data-[state=active]:shadow-none rounded-lg px-3 sm:px-4 py-1.5 text-[11px] sm:text-xs font-mono"
            >
              Purification ensemble
            </TabsTrigger>
            <TabsTrigger
              value="i3"
              className="text-zinc-400 hover:text-zinc-100 data-[state=active]:bg-emerald-500/10 data-[state=active]:text-emerald-300 data-[state=active]:border-emerald-500/40 data-[state=active]:shadow-none rounded-lg px-3 sm:px-4 py-1.5 text-[11px] sm:text-xs font-mono"
            >
              I₃ crossing sweep
            </TabsTrigger>
          </TabsList>
          <TabsContent value="purif" className="mt-2">
            <EnsemblePanel L={L} p={p} />
          </TabsContent>
          <TabsContent value="i3" forceMount className="mt-2 data-[state=inactive]:hidden">
            <I3SweepPanel boardId={boardId} active={toolsTab === "i3"} />
          </TabsContent>
        </Tabs>
      </div>
    </section>
  );
}

function Stat({ label, value, accent }: { label: string; value: string; accent?: string }) {
  return (
    <div className="flex items-baseline justify-between gap-2 border-b border-zinc-800/70 pb-1.5">
      <span className="text-[11px] uppercase tracking-wider text-zinc-400">{label}</span>
      <span className={`tabular-nums text-sm ${accent ?? "text-zinc-100"}`}>{value}</span>
    </div>
  );
}
