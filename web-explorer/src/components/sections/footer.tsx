"use client";

import { Atom, Github } from "lucide-react";

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-zinc-900 bg-zinc-950">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10 pb-[max(2.5rem,env(safe-area-inset-bottom))]">
        <div className="flex flex-col sm:flex-row gap-6 sm:items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="grid place-items-center size-9 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400">
              <Atom className="size-5" />
            </span>
            <div>
              <div className="font-mono text-sm font-semibold text-zinc-200">
                quantum<span className="text-emerald-400">·</span>circuits
              </div>
              <div className="text-xs text-zinc-500">
                measurement-induced phase transition · interactive research explorer
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:items-end gap-2 text-xs text-zinc-500">
            <a
              href="https://github.com/MIKEAA2020/quantum-circuits"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 rounded-md border border-zinc-800 hover:border-zinc-600 hover:text-zinc-300 px-3 py-1.5 transition-colors"
            >
              <Github className="size-3.5" />
              MIKEAA2020/quantum-circuits
            </a>
            <div>
              figures &amp; tables quoted verbatim from the deposited analysis logs ·
              browser simulator: phase-free F₂ tableau, mulberry32 demo RNG
            </div>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-zinc-900 flex flex-col sm:flex-row gap-2 justify-between text-[11px] text-zinc-600 font-mono">
          <span>p_c = 0.1597(8) · ν = 1.24(7) · purification: 0.1601–0.1604 · annealed: 0.23381</span>
          <span>built with Next.js · Gottesman–Knill in TypeScript</span>
        </div>
      </div>
    </footer>
  );
}
