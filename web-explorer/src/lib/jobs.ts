import { sweepTrajI3, type I3SweepPoint } from "@/lib/quantum/clifford";
import { db } from "@/lib/db";

/**
 * Background-job registry for large-L I₃ sweeps (L = 128 / 256).
 *
 * These sweeps take 3–20 s of CPU — too long for a single request — so the
 * API route POST /api/jobs starts a job here and the client polls
 * GET /api/jobs?id=… . The runner computes ONE TRAJECTORY of ONE p-point per
 * chunk (≈ 30 ms at L=128, ≈ 220 ms at L=256) and pauses ~12 ms between
 * chunks, so poll requests, response flushes, and the rest of the site
 * interleave with the computation (a per-point chunk proved too coarse: a
 * 2 s L=256 block starved response flushing, and polls were answered seconds
 * late). A p-point's mean ± s.e. lands on the job as soon as all its
 * trajectories are done — the client chart fills in point-by-point.
 *
 * DURABILITY (phase 10): every job is mirrored into the SweepJobRecord table.
 * Completed points (with per-trajectory values) are written after each
 * p-point, so a dev-server reload — which resets this module — loses at most
 * the partially-computed point in flight. On module (re)load, queued/running
 * records are rehydrated: completed points are kept (the runner is
 * seed-deterministic, so recomputation is bit-identical anyway) and the
 * remaining p-points resume under the same job id, two at a time. When both
 * compute slots are busy, new jobs are QUEUED instead of rejected — the
 * client shows the queued status and the poll loop just keeps waiting.
 * getSweepJob() falls back to the table, so polls during a reload read the
 * last persisted state instead of 404ing.
 */

export interface SweepJob {
  id: string;
  status: "queued" | "running" | "done" | "error";
  createdAt: number;
  updatedAt: number;
  /** job parameters (echoed for the client) */
  L: number;
  tau: number;
  nTraj: number;
  ps: number[];
  /** points completed so far — progressive partial results */
  points: I3SweepPoint[];
  /** per-point trajectory values, aligned with points (non-parametric bootstrap material) */
  traj: number[][];
  total: number;
  error?: string;
  elapsedMs: number;
}

const MAX_RUNNING = 2;
/** queued (waiting-for-a-slot) jobs beyond this → POST returns 429 */
const MAX_PENDING = 4;
const MAX_JOBS = 16;
const TTL_MS = 10 * 60 * 1000; // finished jobs are pollable for 10 min in memory
/** pause between trajectory chunks — gives the event loop real I/O time */
const CHUNK_YIELD_MS = 12;
/** finished DB records older than this are pruned (opportunistically, rate-limited) */
const DB_TTL_MS = 60 * 60 * 1000;
const DB_TRL_MS = 5 * 60 * 1000; // prune at most once per 5 minutes

const jobs = new Map<string, SweepJob>();
/** FIFO of job ids waiting for a compute slot */
const queue: string[] = [];
/** ids of jobs currently executing (subset of jobs, status "running") */
let runningCount = 0;

let lastDbPrune = 0;

/** Lazy cleanup: drop stale finished jobs and trim the registry. */
function cleanup() {
  const now = Date.now();
  for (const [id, job] of jobs) {
    if (job.status !== "running" && job.status !== "queued" && now - job.updatedAt > TTL_MS) jobs.delete(id);
  }
  // trim to MAX_JOBS, dropping the oldest finished jobs first
  if (jobs.size > MAX_JOBS) {
    const finished = [...jobs.values()]
      .filter((j) => j.status !== "running" && j.status !== "queued")
      .sort((a, b) => a.updatedAt - b.updatedAt);
    for (const job of finished) {
      if (jobs.size <= MAX_JOBS) break;
      jobs.delete(job.id);
    }
  }
  // opportunistic one-shot DB prune (rate-limited; failures are non-fatal)
  if (now - lastDbPrune > DB_TRL_MS) {
    lastDbPrune = now;
    void db.sweepJobRecord
      .deleteMany({
        where: { status: { in: ["done", "error"] }, updatedAt: { lt: new Date(now - DB_TTL_MS) } },
      })
      .catch(() => {});
  }
}

const yieldToEventLoop = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

let jobCounter = 0;

const recordToJob = (r: {
  id: string;
  L: number;
  tau: number;
  nTraj: number;
  psJson: string;
  pointsJson: string;
  trajJson: string;
  total: number;
  status: string;
  error: string | null;
  elapsedMs: number;
  createdAt: Date;
  updatedAt: Date;
}): SweepJob => ({
  id: r.id,
  status: (["queued", "running", "done", "error"].includes(r.status) ? r.status : "error") as SweepJob["status"],
  createdAt: r.createdAt.getTime(),
  updatedAt: r.updatedAt.getTime(),
  L: r.L,
  tau: r.tau,
  nTraj: r.nTraj,
  ps: JSON.parse(r.psJson) as number[],
  points: JSON.parse(r.pointsJson) as I3SweepPoint[],
  traj: JSON.parse(r.trajJson) as number[][],
  total: r.total,
  error: r.error ?? undefined,
  elapsedMs: r.elapsedMs,
});

const persist = (job: SweepJob) =>
  db.sweepJobRecord
    .update({
      where: { id: job.id },
      data: {
        status: job.status,
        pointsJson: JSON.stringify(job.points),
        trajJson: JSON.stringify(job.traj),
        error: job.error ?? null,
        elapsedMs: job.elapsedMs,
      },
    })
    .catch(() => {}); // persistence is best-effort — the in-memory copy stays authoritative

/**
 * Execute a job (from its current completed-point state — resume-friendly):
 * one (p-point, trajectory) per chunk, yielding between chunks; a point's
 * mean ± s.e. is published (memory + DB) when its last trajectory lands.
 * The seed stream is disjoint per (L, k, p-index), so a resumed point
 * recomputes bit-identically to a fresh one.
 */
async function executeJob(job: SweepJob) {
  job.status = "running";
  job.updatedAt = Date.now();
  void persist(job);
  const t0 = Date.now();
  const priorMs = job.elapsedMs; // resumed jobs keep their earlier compute time
  const seed0 = 5000 + job.L * 977; // same disjoint seed stream per system size as the synchronous route
  try {
    for (let pi = job.points.length; pi < job.ps.length; pi++) {
      const vals: number[] = [];
      for (let k = 0; k < job.nTraj; k++) {
        vals.push(
          sweepTrajI3({
            L: job.L,
            p: job.ps[pi],
            tau: job.tau,
            seed: seed0 + k * job.ps.length + pi,
          })
        );
        await yieldToEventLoop(CHUNK_YIELD_MS);
      }
      const n = vals.length || 1;
      const mean = vals.reduce((a, b) => a + b, 0) / n;
      const varr = n > 1 ? vals.reduce((a, b) => a + (b - mean) * (b - mean), 0) / (n - 1) : 0;
      job.points.push({ p: job.ps[pi], mean, se: Math.sqrt(varr / n) });
      job.traj.push([...vals]);
      job.updatedAt = Date.now();
      job.elapsedMs = priorMs + (Date.now() - t0);
      void persist(job); // one small write per completed p-point
    }
    job.status = "done";
    job.elapsedMs = priorMs + (Date.now() - t0);
    job.updatedAt = Date.now();
    void persist(job);
  } catch (e) {
    job.status = "error";
    job.error = e instanceof Error ? e.message : "sweep failed";
    job.updatedAt = Date.now();
    void persist(job);
  }
}

/** Pull the next queued job (if a compute slot is free). */
function kickQueue() {
  while (runningCount < MAX_RUNNING && queue.length > 0) {
    const id = queue.shift()!;
    const job = jobs.get(id);
    if (!job || (job.status !== "queued" && job.status !== "running")) continue;
    // NOTE: "running" here is only possible for a rehydrated record (see
    // rehydrateOrphan) — treat it as queued so it actually gets a slot
    runningCount++;
    void executeJob(job).finally(() => {
      runningCount--;
      kickQueue();
    });
  }
}

/** Rehydrate a persisted orphan (server reloaded mid-run): completed points are
 *  kept (the seed stream is deterministic, so recomputation is bit-identical
 *  anyway) and the remaining p-points re-enter the FIFO queue. A DB-"running"
 *  record is demoted to "queued" — its old runner died with the process. */
function rehydrateOrphan(rec: {
  id: string;
  L: number;
  tau: number;
  nTraj: number;
  psJson: string;
  pointsJson: string;
  trajJson: string;
  total: number;
  status: string;
  error: string | null;
  elapsedMs: number;
  createdAt: Date;
  updatedAt: Date;
}): SweepJob {
  const job = recordToJob(rec);
  if (job.status === "running") job.status = "queued";
  if (!jobs.has(job.id) && !queue.includes(job.id)) {
    jobs.set(job.id, job);
    queue.push(job.id);
  }
  return jobs.get(job.id) ?? job;
}

/** Start (or queue) a large-L sweep. Returns the job id, or a reason object. */
export function startSweepJob(params: {
  L: number;
  ps: number[];
  nTraj: number;
  tau: number;
}): string | { error: string } {
  cleanup();
  // queued jobs waiting for a slot: everything on the FIFO queue (in-process
  // starts and rehydrated records alike)
  if (queue.length >= MAX_PENDING) {
    return { error: `the sweep queue is full (${queue.length} waiting) — try again in a few minutes` };
  }
  const id = `job-${Date.now().toString(36)}-${(jobCounter++).toString(36)}`;
  const job: SweepJob = {
    id,
    status: "queued",
    createdAt: Date.now(),
    updatedAt: Date.now(),
    L: params.L,
    tau: params.tau,
    nTraj: params.nTraj,
    ps: params.ps,
    points: [],
    traj: [],
    total: params.ps.length,
    elapsedMs: 0,
  };
  jobs.set(id, job);
  queue.push(id);
  // durable copy: a reload rehydrates this job from the table
  void db.sweepJobRecord
    .create({
      data: {
        id,
        L: params.L,
        tau: params.tau,
        nTraj: params.nTraj,
        psJson: JSON.stringify(params.ps),
        pointsJson: "[]",
        trajJson: "[]",
        total: params.ps.length,
        status: "queued",
      },
    })
    .catch(() => {});
  kickQueue();
  return id;
}

/** Poll a job by id: memory first, then the persisted record (null when unknown/expired). */
export async function getSweepJob(id: string): Promise<SweepJob | null> {
  cleanup();
  const mem = jobs.get(id);
  if (mem) return mem;
  // in-memory entry gone (reload or TTL trim) — the durable copy answers
  try {
    const rec = await db.sweepJobRecord.findUnique({ where: { id } });
    if (!rec) return null;
    // rehydrate a live-but-lost job (server reloaded mid-run): completed points
    // are kept, remaining p-points resume under the same id
    if (rec.status === "queued" || rec.status === "running") {
      const job = rehydrateOrphan(rec);
      kickQueue();
      return job;
    }
    return recordToJob(rec);
  } catch {
    return null;
  }
}

// On module load: rehydrate queued/running records (dev-server reloads, restarts).
// Older records first — FIFO fairness matches the in-process queue.
void (async () => {
  try {
    const orphans = await db.sweepJobRecord.findMany({
      where: { status: { in: ["queued", "running"] } },
      orderBy: { createdAt: "asc" },
      take: 16,
    });
    for (const rec of orphans) {
      rehydrateOrphan(rec);
    }
    if (orphans.length > 0) kickQueue();
  } catch {
    // DB unavailable at boot — the registry still works, just not durably
  }
})();
