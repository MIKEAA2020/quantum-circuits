import type { ReactNode } from "react";
import { Link2 } from "lucide-react";

interface Props {
  /** section number, e.g. "01" */
  num: string;
  /** anchor id of the section (for the hover self-link) */
  id: string;
  /** kicker label, e.g. "The model" */
  kicker: string;
  title: ReactNode;
  children?: ReactNode;
}

/**
 * Shared editorial section header: numbered chip + kicker, hover-revealed
 * self-anchor link, gradient rule under the title, lede paragraph.
 */
export function SectionHeading({ num, id, kicker, title, children }: Props) {
  return (
    <div className="max-w-3xl group/head">
      <div className="flex items-center gap-3">
        <span
          aria-hidden
          className="grid place-items-center size-7 rounded-md border border-emerald-500/30 bg-gradient-to-b from-emerald-500/15 to-emerald-500/5 font-mono text-xs font-semibold text-emerald-400"
        >
          {num}
        </span>
        <p className="font-mono text-xs uppercase tracking-widest text-emerald-500/90">{kicker}</p>
        <a
          href={`#${id}`}
          className="text-zinc-600 hover:text-emerald-400 transition-colors opacity-0 group-hover/head:opacity-100 focus-visible:opacity-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/40 rounded"
          aria-label={`Link to section ${kicker}`}
        >
          <Link2 className="size-3.5" />
        </a>
        <span aria-hidden className="flex-1 h-px bg-gradient-to-r from-zinc-800 via-zinc-800/40 to-transparent" />
      </div>
      <h2 className="mt-3 text-2xl sm:text-3xl font-semibold tracking-tight text-zinc-50">{title}</h2>
      <div aria-hidden className="mt-4 h-px w-16 bg-gradient-to-r from-emerald-500/60 to-transparent" />
      {children && <div className="mt-4 text-zinc-400 leading-relaxed">{children}</div>}
    </div>
  );
}
