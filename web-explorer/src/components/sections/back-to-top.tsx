"use client";

import { useEffect, useState } from "react";
import { ArrowUp } from "lucide-react";

/** Floating back-to-top button — appears after the hero scrolls away. */
export function BackToTop() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 900);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <button
      id="back-to-top"
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      aria-label="Back to top"
      className={`fixed bottom-5 right-5 z-40 grid place-items-center size-10 rounded-full border border-emerald-500/40 bg-zinc-950/90 text-emerald-400 backdrop-blur-md shadow-[0_0_24px_-8px_rgba(16,185,129,0.5)] transition-all duration-300 hover:bg-emerald-500 hover:text-emerald-950 hover:-translate-y-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/50 ${
        show ? "opacity-100 translate-y-0 pointer-events-auto" : "opacity-0 translate-y-4 pointer-events-none"
      }`}
    >
      <ArrowUp className="size-4" />
    </button>
  );
}
