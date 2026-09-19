import { NextResponse } from "next/server";
import { runEnsemble, runI3Sweep } from "@/lib/quantum/clifford";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ALLOWED_L = [8, 16, 32, 64];

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => null);
    if (!body || typeof body !== "object") {
      return NextResponse.json({ error: "invalid JSON body" }, { status: 400 });
    }
    const { L, p, mode, nTraj, taus, sweep, sweepPs, tau } = body as {
      L?: number;
      p?: number;
      mode?: string;
      nTraj?: number;
      taus?: number[];
      sweep?: boolean;
      sweepPs?: number[];
      tau?: number;
    };

    if (!ALLOWED_L.includes(L)) {
      return NextResponse.json(
        { error: `L must be one of ${ALLOWED_L.join(", ")} for the ensemble endpoint` },
        { status: 400 }
      );
    }

    // -----------------------------------------------------------------
    // I₃ crossing sweep (pure-state locator over a p-grid, one L)
    // -----------------------------------------------------------------
    if (sweep === true) {
      if (!Array.isArray(sweepPs) || sweepPs.length < 3 || sweepPs.length > 9) {
        return NextResponse.json(
          { error: "sweepPs must be an array of 3–9 measurement probabilities" },
          { status: 400 }
        );
      }
      const ps = sweepPs
        .map((v) => Number(v))
        .filter((v) => v >= 0 && v <= 0.5);
      if (ps.length < 3) {
        return NextResponse.json({ error: "sweepPs values must lie in [0, 0.5]" }, { status: 400 });
      }
      // τ ∈ [0.5, 4] — τ = 4 matches the deepest deposited purification depth;
      // it doubles the circuit depth vs τ = 2, so L = 64 caps at half the trajectories
      const sweepTau = Math.min(4, Math.max(0.5, Number(tau) || 2));
      // trajectory caps that keep the sweep request ~2s at most per L
      // (benchmarked: L=64×24 traj×9 points ≈ 2.0s at τ ≤ 2, 3.2s at τ = 4 → 12 traj;
      //  L=32×32 ≈ 0.75s at τ = 4; L≤16×64 ≈ 0.43s at τ = 4)
      const maxTraj = L >= 64 ? (sweepTau > 2 ? 12 : 24) : L >= 32 ? 32 : 64;
      const n = Math.max(1, Math.min(maxTraj, Math.floor(nTraj ?? 24)));
      const result = runI3Sweep({
        L,
        ps: Array.from(new Set(ps)).sort((a, b) => a - b),
        nTraj: n,
        tau: sweepTau,
        seed0: 5000 + L * 977, // disjoint stream per system size
      });
      return NextResponse.json(result);
    }

    // -----------------------------------------------------------------
    // Single (L, p) ensemble (purification / pure)
    // -----------------------------------------------------------------
    if (typeof p !== "number" || p < 0 || p > 1) {
      return NextResponse.json({ error: "p must be in [0, 1]" }, { status: 400 });
    }
    const m = mode === "pure" ? "pure" : "purif";

    // trajectory caps that keep the request under a few seconds
    const maxTraj = L >= 64 ? 60 : 400;
    const n = Math.max(1, Math.min(maxTraj, Math.floor(nTraj ?? 100)));

    // tau caps by size (depth = tau * L periods). τ = 4 is offered at L ≤ 32 —
    // bench: L=32 τ=4 ≈ 1.0s @ 200 traj / 2.0s @ 400 traj (recorded once at t=4L);
    // the deposited table has τ = 4 rows for BOTH L = 16 and L = 32, so the
    // comparison column keeps working. L = 64 stays at τ = 1 (≈ 0.9s @ 60 traj).
    const maxTau = L >= 64 ? 1 : 4;
    const tauList = (Array.isArray(taus) ? taus : [1])
      .map((t) => Number(t))
      .filter((t) => t > 0 && t <= maxTau)
      .slice(0, 3);
    const finalTaus = tauList.length ? Array.from(new Set(tauList)).sort((a, b) => a - b) : [1];

    const result = runEnsemble({
      L,
      p,
      mode: m,
      nTraj: n,
      taus: finalTaus,
      seed0: 1000,
    });

    return NextResponse.json(result);
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "simulation failed" },
      { status: 500 }
    );
  }
}
