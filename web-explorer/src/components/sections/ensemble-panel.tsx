"use client";

import { useCallback, useEffect, useState } from "react";
import { FlaskConical, Loader2, Save, Trash2, CheckCircle2, AlertTriangle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { PURIF_DATA } from "@/lib/research-data";

interface SimResponse {
  L: number;
  p: number;
  nTraj: number;
  sRef: { tau: number; mean: number; se: number }[];
  sA: { tau: number; mean: number; se: number }[];
  elapsedMs: number;
}

interface SavedRun {
  id: string;
  label: string;
  L: number;
  p: number;
  nTraj: number;
  sRefTau1: number | null;
  sRefTau1Se: number | null;
  createdAt: string;
}

const DEPOSITED_TAU1: Record<number, Record<string, number>> = {
  16: Object.fromEntries(
    PURIF_DATA.find((s) => s.tau === 1)!.series[16].map((pt) => [pt.p.toFixed(3), pt.mean])
  ),
  32: Object.fromEntries(
    PURIF_DATA.find((s) => s.tau === 1)!.series[32].map((pt) => [pt.p.toFixed(3), pt.mean])
  ),
  64: Object.fromEntries(
    PURIF_DATA.find((s) => s.tau === 1)!.series[64].map((pt) => [pt.p.toFixed(3), pt.mean])
  ),
};

const P_PRESETS = [0.14, 0.145, 0.15, 0.155, 0.16, 0.165, 0.17, 0.175, 0.18];

export function EnsemblePanel({ L: liveL, p: liveP }: { L: number; p: number }) {
  const [L, setL] = useState(16);
  const [p, setP] = useState(0.16);
  const [nTraj, setNTraj] = useState(200);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<SimResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [runs, setRuns] = useState<SavedRun[]>([]);
  const [saveState, setSaveState] = useState<"idle" | "saving" | "saved">("idle");
  const { toast } = useToast();
  const notify = useCallback(
    (title: string, description?: string, variant?: "default" | "destructive") =>
      toast({ title, description, variant, duration: 3400 }),
    [toast]
  );

  useEffect(() => {
    // sync from the live simulator when in range
    if ([16, 32, 64].includes(liveL)) setL(liveL);
    if (P_PRESETS.includes(Number(liveP.toFixed(3)))) setP(Number(liveP.toFixed(3)));
  }, [liveL, liveP]);

  const loadRuns = useCallback(async () => {
    try {
      const res = await fetch("/api/runs");
      if (res.ok) setRuns(await res.json());
    } catch {
      /* offline is fine */
    }
  }, []);

  useEffect(() => {
    loadRuns();
  }, [loadRuns]);

  const run = async () => {
    setBusy(true);
    setError(null);
    setResult(null);
    setSaveState("idle");
    try {
      const res = await fetch("/api/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // τ = 4 is offered at L ≤ 32 (bench: L=32 ≈ 2s at 400 traj) — the deposited
        // table has τ = 4 rows for both L = 16 and L = 32, so the comparison column works
        body: JSON.stringify({ L, p, nTraj, mode: "purif", taus: L >= 64 ? [1] : [1, 2, 4] }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error ?? `request failed (${res.status})`);
      }
      setResult(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "simulation failed");
    } finally {
      setBusy(false);
    }
  };

  const save = async () => {
    if (!result) return;
    setSaveState("saving");
    try {
      const res = await fetch("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          label: `L=${result.L} p=${result.p.toFixed(3)} n=${result.nTraj}`,
          L: result.L,
          p: result.p,
          nTraj: result.nTraj,
          sRefTau1: result.sRef.find((s) => s.tau === 1)?.mean ?? null,
          sRefTau1Se: result.sRef.find((s) => s.tau === 1)?.se ?? null,
        }),
      });
      if (res.ok) {
        setSaveState("saved");
        loadRuns();
        notify("Ensemble saved", "Your ⟨S_ref⟩ run is now in the reproducibility ledger.");
        setTimeout(() => setSaveState("idle"), 2000);
      } else {
        setSaveState("idle");
        const body = await res.json().catch(() => ({}));
        notify("Save failed", body.error ?? undefined, "destructive");
      }
    } catch {
      setSaveState("idle");
      notify("Save failed", "The server could not be reached.", "destructive");
    }
  };

  const del = async (id: string) => {
    try {
      const res = await fetch(`/api/runs?id=${id}`, { method: "DELETE" });
      if (res.ok) notify("Run deleted", undefined);
      loadRuns();
    } catch {
      notify("Delete failed", "The server could not be reached.", "destructive");
    }
  };

  const deposited = DEPOSITED_TAU1[L]?.[p.toFixed(3)];
  const mine = result?.sRef.find((s) => s.tau === 1);
  const agree =
    deposited != null && mine != null
      ? Math.abs(mine.mean - deposited) <= 3 * Math.max(mine.se, 0.03)
      : null;

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 sm:p-6">
      <div className="flex flex-wrap items-center gap-3">
        <span className="grid place-items-center size-8 rounded-lg bg-amber-500/15 border border-amber-500/30 text-amber-400">
          <FlaskConical className="size-4" />
        </span>
        <div className="min-w-0">
          <h3 className="text-base font-semibold text-zinc-100">Reproduce the deposited numbers</h3>
          <p className="text-sm text-zinc-500">
            Server-side ensemble of the purification protocol — your own ⟨S_ref⟩ vs the published table.
          </p>
        </div>
      </div>

      <div className="mt-5 grid sm:grid-cols-[1fr_1fr_auto] gap-3 items-end">
        <label className="block">
          <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">system size L</span>
          <div className="mt-1.5 flex gap-1">
            {[16, 32, 64].map((v) => (
              <button
                key={v}
                onClick={() => { setL(v); setResult(null); }}
                className={`flex-1 rounded-md border px-2 py-3 sm:py-1.5 text-xs font-mono transition-colors ${
                  L === v ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-300" : "border-zinc-700 text-zinc-400 hover:border-zinc-500"
                }`}
              >
                {v}
              </button>
            ))}
          </div>
        </label>
        <label className="block">
          <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">measurement rate p</span>
          <select
            value={p}
            onChange={(e) => { setP(Number(e.target.value)); setResult(null); }}
            className="mt-1.5 w-full rounded-md border border-zinc-700 bg-zinc-950 px-2.5 py-2 font-mono text-sm text-zinc-200 focus:border-emerald-500/60 focus:outline-none"
          >
            {P_PRESETS.map((v) => (
              <option key={v} value={v}>{v.toFixed(3)}</option>
            ))}
          </select>
        </label>
        <div className="flex gap-2">
          <label className="block">
            <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">trajectories</span>
            <select
              value={nTraj}
              onChange={(e) => setNTraj(Number(e.target.value))}
              className="mt-1.5 rounded-md border border-zinc-700 bg-zinc-950 px-2.5 py-2 font-mono text-sm text-zinc-200 focus:border-emerald-500/60 focus:outline-none"
            >
              {(L >= 64 ? [30, 60] : [50, 100, 200, 400]).map((v) => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </label>
          <button
            onClick={run}
            disabled={busy}
            className="mt-[26px] inline-flex items-center gap-2 rounded-lg bg-amber-500 hover:bg-amber-400 disabled:opacity-50 disabled:hover:bg-amber-500 active:scale-[0.98] transition-all px-4 py-2 text-sm font-medium text-amber-950 shadow-[0_0_20px_-8px_rgba(245,158,11,0.55)] hover:shadow-[0_0_28px_-8px_rgba(245,158,11,0.75)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500/40"
          >
            {busy ? <Loader2 className="size-4 animate-spin" /> : <FlaskConical className="size-4" />}
            {busy ? "running…" : "Run ensemble"}
          </button>
        </div>
      </div>

      {error && (
        <div className="mt-4 flex items-center gap-2 rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-2 text-sm text-rose-300">
          <AlertTriangle className="size-4" /> {error}
        </div>
      )}

      {result && (
        <div className="mt-5 overflow-x-auto">
          <table className="w-full text-sm font-mono">
            <thead>
              <tr className="text-zinc-500 text-left text-[11px] uppercase tracking-wider">
                <th className="py-2 pr-4 font-medium">τ</th>
                <th className="py-2 pr-4 font-medium">your ensemble</th>
                <th className="py-2 pr-4 font-medium">deposited table</th>
                <th className="py-2 font-medium">status</th>
              </tr>
            </thead>
            <tbody>
              {result.sRef.map((s) => {
                const dep =
                  s.tau === 1
                    ? deposited
                    : PURIF_DATA.find((x) => x.tau === s.tau)?.series[result.L]?.find(
                        (pt) => Math.abs(pt.p - result.p) < 1e-9
                      )?.mean;
                const ok = dep != null ? Math.abs(s.mean - dep) <= 3 * Math.max(s.se, 0.03) : null;
                return (
                  <tr key={s.tau} className="border-t border-zinc-800 transition-colors hover:bg-zinc-800/25">
                    <td className="py-2 pr-4 text-zinc-300">{s.tau}</td>
                    <td className="py-2 pr-4 text-zinc-100 tabular-nums">
                      {s.mean.toFixed(3)} <span className="text-zinc-500">± {s.se.toFixed(3)}</span>
                    </td>
                    <td className="py-2 pr-4 text-amber-300/90 tabular-nums">{dep != null ? dep.toFixed(4) : "—"}</td>
                    <td className="py-2">
                      {ok == null ? (
                        <span className="text-zinc-600">n/a</span>
                      ) : ok ? (
                        <span className="inline-flex items-center gap-1 text-emerald-400">
                          <CheckCircle2 className="size-3.5" /> agrees (≤3σ)
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-rose-400">
                          <AlertTriangle className="size-3.5" /> {s.mean > (dep ?? 0) ? "high" : "low"} — add trajectories
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-zinc-500">
            <span>{result.elapsedMs} ms · {result.nTraj} trajectories · seeds 1000…{1000 + result.nTraj - 1}</span>
            <button
              onClick={save}
              disabled={saveState !== "idle"}
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700 hover:border-zinc-500 px-2.5 py-1 text-zinc-300 transition-colors disabled:opacity-50"
            >
              {saveState === "saving" ? <Loader2 className="size-3.5 animate-spin" /> : saveState === "saved" ? <CheckCircle2 className="size-3.5" /> : <Save className="size-3.5" />}
              {saveState === "saved" ? "saved" : "save run"}
            </button>
            {agree != null && (
              <span className={agree ? "text-emerald-500" : "text-amber-500"}>
                {agree ? "τ=1 within 3σ of the deposited value" : "τ=1 outside 3σ — statistics are cheap here, add more trajectories"}
              </span>
            )}
          </div>
        </div>
      )}

      {runs.length > 0 && (
        <div className="mt-6">
          <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500 mb-2">saved experiments (SQLite)</div>
          <div className="max-h-44 overflow-y-auto rounded-lg border border-zinc-800 divide-y divide-zinc-800/70 custom-scroll">
            {runs.map((r) => (
              <div key={r.id} className="flex items-center gap-3 px-3 py-2 text-sm font-mono transition-colors hover:bg-zinc-800/30">
                <span className="text-zinc-400 tabular-nums">L={r.L}</span>
                <span className="text-zinc-400 tabular-nums">p={r.p.toFixed(3)}</span>
                <span className="text-zinc-400 tabular-nums">n={r.nTraj}</span>
                <span className="ml-auto text-emerald-400 tabular-nums">
                  ⟨S_ref⟩τ=1 = {r.sRefTau1?.toFixed(3) ?? "—"}
                  {r.sRefTau1Se != null && <span className="text-zinc-600"> ± {r.sRefTau1Se.toFixed(3)}</span>}
                </span>
                <span className="text-zinc-600 text-xs hidden sm:inline tabular-nums">{new Date(r.createdAt).toLocaleString()}</span>
                <button
                  onClick={() => del(r.id)}
                  className="text-zinc-600 hover:text-rose-400 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-500/40 rounded"
                  aria-label={`Delete run ${r.label}`}
                >
                  <Trash2 className="size-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
