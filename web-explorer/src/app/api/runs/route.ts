import { NextResponse } from "next/server";
import { db } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const runs = await db.simRun.findMany({
      orderBy: { createdAt: "desc" },
      take: 20,
    });
    return NextResponse.json(runs);
  } catch {
    return NextResponse.json([]);
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => null);
    if (!body) return NextResponse.json({ error: "invalid JSON body" }, { status: 400 });
    const { label, L, p, nTraj, mode, sRefTau1, sRefTau1Se, metrics } = body as {
      label?: string;
      L?: number;
      p?: number;
      nTraj?: number;
      mode?: string;
      sRefTau1?: number | null;
      sRefTau1Se?: number | null;
      metrics?: unknown;
    };
    if (typeof L !== "number" || typeof p !== "number" || typeof nTraj !== "number") {
      return NextResponse.json({ error: "L, p, nTraj are required numbers" }, { status: 400 });
    }
    const run = await db.simRun.create({
      data: {
        label: typeof label === "string" && label ? label.slice(0, 120) : `L=${L} p=${p} n=${nTraj}`,
        L: Math.max(1, Math.min(4096, Math.floor(L))),
        p: Math.max(0, Math.min(1, p)),
        nTraj: Math.max(1, Math.min(100000, Math.floor(nTraj))),
        mode: mode === "pure" ? "pure" : "purif",
        sRefTau1: typeof sRefTau1 === "number" ? sRefTau1 : null,
        sRefTau1Se: typeof sRefTau1Se === "number" ? sRefTau1Se : null,
        metrics:
          metrics === undefined || metrics === null
            ? null
            : JSON.stringify(metrics).slice(0, 8000),
      },
    });
    return NextResponse.json(run, { status: 201 });
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "failed to save run" },
      { status: 500 }
    );
  }
}

export async function DELETE(req: Request) {
  const id = new URL(req.url).searchParams.get("id");
  if (!id) return NextResponse.json({ error: "id query param required" }, { status: 400 });
  try {
    await db.simRun.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch {
    // unknown or malformed id (Prisma throws on invalid cuid) — treat as not found
    return NextResponse.json({ error: "run not found" }, { status: 404 });
  }
}
