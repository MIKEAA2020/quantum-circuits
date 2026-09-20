"use client";

import { useEffect, useRef, useState } from "react";
import { Atom } from "lucide-react";

const LINKS = [
  { href: "#model", label: "Model", id: "model" },
  { href: "#simulator", label: "Simulator", id: "simulator" },
  { href: "#data", label: "Data & FSS", id: "data" },
  { href: "#results", label: "Results", id: "results" },
  { href: "#theory", label: "Exact theory", id: "theory" },
  { href: "#replica", label: "Replica ladder", id: "replica" },
  { href: "#repro", label: "Reproducibility", id: "repro" },
];

export function SiteNav() {
  const [scrolled, setScrolled] = useState(false);
  /** reading progress 0–1 for the thin indicator line under the header */
  const [progress, setProgress] = useState(0);
  const [active, setActive] = useState<string | null>(null);
  const [edge, setEdge] = useState({ left: false, right: false });
  const navRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const onScroll = () => {
      setScrolled(window.scrollY > 12);
      const max = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(max > 0 ? Math.min(1, window.scrollY / max) : 0);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, []);

  // scroll-spy: highlight the section currently in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) setActive(e.target.id);
        }
      },
      { rootMargin: "-40% 0px -55% 0px" }
    );
    for (const { id } of LINKS) {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    }
    return () => observer.disconnect();
  }, []);

  // horizontal-edge fades: hint that the link strip scrolls on small screens
  useEffect(() => {
    const nav = navRef.current;
    if (!nav) return;
    const update = () =>
      setEdge({
        left: nav.scrollLeft > 6,
        right: nav.scrollLeft + nav.clientWidth < nav.scrollWidth - 6,
      });
    update();
    nav.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update, { passive: true });
    return () => {
      nav.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, []);

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        scrolled ? "bg-zinc-950/85 backdrop-blur-md border-b border-zinc-800/80" : "bg-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center gap-4">
        <a href="#top" className="flex items-center gap-2 shrink-0 group" aria-label="Back to top">
          <span className="grid place-items-center size-7 rounded-md bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 group-hover:bg-emerald-500/25 group-hover:scale-105 transition-all">
            <Atom className="size-4 group-hover:rotate-180 transition-transform duration-500" />
          </span>
          <span className="font-mono text-sm font-semibold tracking-tight text-zinc-100">
            quantum<span className="text-emerald-400">·</span>circuits
          </span>
        </a>
        <nav
          ref={navRef}
          className="relative ml-auto flex items-center gap-1 overflow-x-auto no-scrollbar"
          aria-label="Sections"
        >
          {LINKS.map((l) => {
            const isActive = active === l.id;
            return (
              <a
                key={l.href}
                href={l.href}
                aria-current={isActive ? "true" : undefined}
                className={`relative px-2.5 py-1.5 rounded-md text-[13px] transition-colors whitespace-nowrap ${
                  isActive
                    ? "text-emerald-300"
                    : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60"
                }`}
              >
                {l.label}
                {isActive && (
                  <span className="absolute inset-x-2.5 -bottom-0.5 h-0.5 rounded-full bg-gradient-to-r from-emerald-500/0 via-emerald-400/80 to-emerald-500/0" />
                )}
              </a>
            );
          })}
          {/* edge fades — the strip scrolls horizontally on small screens */}
          <span
            aria-hidden
            className={`pointer-events-none absolute inset-y-0 left-0 w-8 bg-gradient-to-r from-zinc-950/95 to-transparent transition-opacity sm:hidden ${edge.left ? "opacity-100" : "opacity-0"}`}
          />
          <span
            aria-hidden
            className={`pointer-events-none absolute inset-y-0 right-0 w-8 bg-gradient-to-l from-zinc-950/95 to-transparent transition-opacity sm:hidden ${edge.right ? "opacity-100" : "opacity-0"}`}
          />
        </nav>
      </div>
      {/* reading progress — a hairline emerald trace of how far down the page you are */}
      <div
        aria-hidden
        className={`absolute bottom-0 inset-x-0 h-px transition-opacity duration-300 ${scrolled ? "opacity-100" : "opacity-0"}`}
      >
        <div
          className="h-full bg-gradient-to-r from-emerald-600 via-emerald-400 to-teal-300 origin-left"
          style={{ transform: `scaleX(${progress})` }}
        />
      </div>
    </header>
  );
}
