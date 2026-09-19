import { NextResponse } from "next/server";
import { getSweepJob, startSweepJob } from "@/lib/jobs";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Large-L background I₃ sweeps (L = 128 / 256) — DURABLE since phase 10:
 * every job is mirrored to the SweepJobRecord table (progress persisted
 * point-by-point), survives dev-server reloads, and resumes under the same
 * job id. Excess jobs are queued (FIFO, ≤ 4 waiting) instead of rejected.
 *
 * POST { L, sweepPs: number[3–9] ⊂ [0, 0.5], tau, nTraj } → { jobId, status }
 *   caps (benchmarked, phase 6): L=128 → nTraj ≤ 8;  L=256 → nTraj ≤ 4;  tau ≤ 2
 *   ~0.25 s per p-point at L=128×8, ~0.9 s at L=256×4 — a 9-point sweep is
 *   2–8 s, too long for one request, so it runs point-by-point in the
 *   background and the client polls. 429 only when the queue itself is full.
 * GET ?id=… → { status, points (partial), total, elapsedMs, … } · 404 when
 *   the job is unknown; a reload mid-run answers from the persisted record
 *   (the remaining p-points resume automatically).
 */
const LARGE_L = [128, 256];

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => null);
    if (!body || typeof body !== "object") {
      return NextResponse.json({ error: "invalid JSON body" }, { status: 400 });
    }
    const { L, sweepPs, tau, nTraj } = body as {
      L?: number;
      sweepPs?: number[];
      tau?: number;
      nTraj?: number;
    };

    if (!LARGE_L.includes(L)) {
      return NextResponse.json(
        { error: `background jobs exist for L ∈ {${LARGE_L.join(", ")}} — smaller sizes run synchronously via /api/simulate` },
        { status: 400 }
      );
    }
    if (!Array.isArray(sweepPs) || sweepPs.length < 3 || sweepPs.length > 9) {
      return NextResponse.json(
        { error: "sweepPs must be an array of 3–9 measurement probabilities" },
        { status: 400 }
      );
    }
    const ps = Array.from(new Set(sweepPs.map((v) => Number(v)).filter((v) => v >= 0 && v <= 0.5)));
    if (ps.length < 3) {
      return NextResponse.json({ error: "sweepPs values must lie in [0, 0.5]" }, { status: 400 });
    }
    ps.sort((a, b) => a - b);

    const jobTau = Math.min(4, Math.max(0.5, Number(tau) || 2));
    const maxTraj = L >= 256 ? 4 : 8;
    const n = Math.max(1, Math.min(maxTraj, Math.floor(nTraj ?? 4)));

    const started = startSweepJob({ L: L as number, ps, nTraj: n, tau: jobTau });
    if (typeof started !== "string") {
      return NextResponse.json({ error: started.error }, { status: 429 });
    }
    const job = await getSweepJob(started);
    return NextResponse.json({ jobId: started, status: job?.status ?? "queued" }, { status: 201 });
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "job creation failed" },
      { status: 500 }
    );
  }
}

export async function GET(req: Request) {
  const id = new URL(req.url).searchParams.get("id");
  if (!id) {
    return NextResponse.json({ error: "missing ?id= job parameter" }, { status: 400 });
  }
  const job = await getSweepJob(id);
  if (!job) {
    return NextResponse.json({ error: "job not found or expired" }, { status: 404 });
  }
  return NextResponse.json(job);
}
