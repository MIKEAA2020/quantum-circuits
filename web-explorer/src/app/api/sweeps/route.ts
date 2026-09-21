import { NextResponse } from "next/server";
import { db } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

interface SweepPoint {
  p: number;
  mean: number;
  se: number;
}

/** per-trajectory values: traj[L][pointIndex][trajectoryIndex] — aligned with series */
interface TrajMap {
  [L: string]: number[][];
}

/* ── abuse guards (in-memory; module resets on server reload) ────────────
 * Rate limit: ≤ 6 saves per client per 2 minutes.
 * Dedup: an identical payload (same series JSON) is rejected with 409
 * instead of cluttering the board — the DB check survives restarts.       */
const RATE_WINDOW_MS = 2 * 60 * 1000;
const RATE_MAX = 6;
const rateBuckets = new Map<string, number[]>();

function rateLimited(key: string): boolean {
  const now = Date.now();
  const stamps = (rateBuckets.get(key) ?? []).filter((t) => now - t < RATE_WINDOW_MS);
  if (stamps.length >= RATE_MAX) {
    rateBuckets.set(key, stamps);
    return true;
  }
  stamps.push(now);
  rateBuckets.set(key, stamps);
  if (rateBuckets.size > 256) {
    // drop stale buckets so the map cannot grow unbounded
    for (const [k, v] of rateBuckets) {
      if (v.every((t) => now - t >= RATE_WINDOW_MS)) rateBuckets.delete(k);
    }
  }
  return false;
}

export async function GET(req: Request) {
  // ?id=… → a single sweep, INCLUDING trajectory data (share links / loads)
  const id = new URL(req.url).searchParams.get("id");
  if (id) {
    try {
      const sweep = await db.i3Sweep.findUnique({ where: { id } });
      if (!sweep) return NextResponse.json({ error: "sweep not found" }, { status: 404 });
      return NextResponse.json(sweep);
    } catch {
      // unknown or malformed id (Prisma throws on invalid cuid) — treat as not found
      return NextResponse.json({ error: "sweep not found" }, { status: 404 });
    }
  }
  try {
    // ?all=1 → up to 100 rows (the "show all" toggle); default board view = newest 12
    const all = new URL(req.url).searchParams.get("all") === "1";
    const sweeps = await db.i3Sweep.findMany({
      orderBy: { createdAt: "desc" },
      take: all ? 100 : 12,
    });
    const total = await db.i3Sweep.count();
    // list view: strip the (potentially large) traj blob, expose a hasTraj flag
    // instead — loads fetch the full record via ?id= when trajectory data matters
    return NextResponse.json(
      sweeps.map(({ trajJson, ...rest }) => ({ ...rest, hasTraj: trajJson != null })),
      { headers: { "X-Board-Total": String(total) } }
    );
  } catch {
    return NextResponse.json([]);
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => null);
    if (!body) return NextResponse.json({ error: "invalid JSON body" }, { status: 400 });
    const { label, tau, nTraj, series, traj } = body as {
      label?: string;
      tau?: number;
      nTraj?: number;
      series?: Record<string, SweepPoint[]>;
      traj?: TrajMap;
    };

    if (typeof tau !== "number" || typeof nTraj !== "number" || !series || typeof series !== "object") {
      return NextResponse.json({ error: "tau, nTraj and series are required" }, { status: 400 });
    }
    const sizes = Object.keys(series)
      .map(Number)
      .filter((v) => Number.isFinite(v) && v > 0 && v <= 4096)
      .sort((a, b) => a - b);
    if (sizes.length < 2) {
      return NextResponse.json({ error: "series must contain at least two system sizes" }, { status: 400 });
    }

    // validate + clamp the payload (protect the DB from oversized blobs)
    const clean: Record<string, SweepPoint[]> = {};
    let total = 0;
    for (const L of sizes) {
      const pts = series[String(L)];
      if (!Array.isArray(pts)) {
        return NextResponse.json({ error: `series[${L}] must be an array` }, { status: 400 });
      }
      const cleaned = pts
        .filter(
          (pt) =>
            pt && typeof pt.p === "number" && typeof pt.mean === "number" && Number.isFinite(pt.se)
        )
        .slice(0, 16)
        .map((pt) => ({
          p: Math.max(0, Math.min(1, pt.p)),
          mean: Math.max(-4096, Math.min(4096, pt.mean)),
          se: Math.max(0, Math.min(64, pt.se ?? 0)),
        }));
      total += cleaned.length;
      clean[String(L)] = cleaned;
    }
    if (total < 4 || total > 256) {
      return NextResponse.json({ error: "total point count must be 4–256" }, { status: 400 });
    }

    // optional trajectory payload: traj[L] must align 1:1 with series[L] points,
    // every row an array of finite numbers (≥ 1 trajectory) — the non-parametric
    // bootstrap data. Capped at 96 KB of JSON so the DB stays light.
    let trajJson: string | null = null;
    if (traj && typeof traj === "object") {
      const cleanTraj: TrajMap = {};
      for (const L of sizes) {
        const rows = traj[String(L)];
        if (rows === undefined) continue; // sizes without traj fall back to parametric
        if (!Array.isArray(rows) || rows.length !== clean[String(L)].length) {
          return NextResponse.json({ error: `traj[${L}] must align with series[${L}] point-by-point` }, { status: 400 });
        }
        for (const row of rows) {
          if (
            !Array.isArray(row) ||
            row.length < 1 ||
            row.length > 4096 ||
            row.some((v) => typeof v !== "number" || !Number.isFinite(v))
          ) {
            return NextResponse.json(
              { error: `traj[${L}] rows must be arrays of finite numbers (≥ 1 trajectory each)` },
              { status: 400 }
            );
          }
        }
        cleanTraj[String(L)] = rows.map((row) =>
          row.map((v) => Math.max(-4096, Math.min(4096, v)))
        );
      }
      const blob = JSON.stringify(cleanTraj);
      if (blob.length > 96000) {
        // too heavy to store — save the sweep anyway, means only (honest fallback)
        trajJson = null;
      } else if (Object.keys(cleanTraj).length > 0) {
        trajJson = blob;
      }
    }

    // abuse guards: per-client rate limit, then exact-payload dedup
    const clientKey = (req.headers.get("x-forwarded-for") ?? "local").split(",")[0].trim();
    if (rateLimited(clientKey)) {
      return NextResponse.json(
        { error: "too many saves from this client — wait a couple of minutes" },
        { status: 429 }
      );
    }
    const seriesJson = JSON.stringify(clean).slice(0, 24000);
    const existing = await db.i3Sweep.findFirst({ where: { seriesJson } });
    if (existing) {
      return NextResponse.json(
        { error: `this exact sweep is already on the board ("${existing.label}")` },
        { status: 409 }
      );
    }

    const sweep = await db.i3Sweep.create({
      data: {
        label:
          typeof label === "string" && label.trim()
            ? label.trim().slice(0, 120)
            : `I₃ sweep · L=${sizes.join(",")} · τ=${tau}`,
        tau: Math.max(0.25, Math.min(4, tau)),
        nTraj: Math.max(1, Math.min(100000, Math.floor(nTraj))),
        sizes: sizes.join(","),
        seriesJson,
        trajJson,
      },
    });
    return NextResponse.json({ ...sweep, hasTraj: trajJson != null }, { status: 201 });
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "failed to save sweep" },
      { status: 500 }
    );
  }
}

export async function DELETE(req: Request) {
  const id = new URL(req.url).searchParams.get("id");
  if (!id) return NextResponse.json({ error: "id query param required" }, { status: 400 });
  try {
    await db.i3Sweep.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch {
    // unknown or malformed id (Prisma throws on invalid cuid) — treat as not found
    return NextResponse.json({ error: "sweep not found" }, { status: 404 });
  }
}
