#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-generative-v10.12.md from v10.11 — fold-in: RP11b engine v0.1 calibration (5/5 + F1) and
# W3b adjunction atlas v0.1 (3 rows + paper-pending marks). In place after gate-run log; no diary; Part I frozen.
import io

SRC = "formalism-generative-v10.11.md"
DST = "formalism-generative-v10.12.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.11, GENERATIVE LINEAGE)", "Research Program (v10.12, GENERATIVE LINEAGE)", 1)

ENTRY = """

**Framework-instrument build round (2026-10-11; RP11b engine v0.1 + W3b adjunction atlas v0.1 — both first-run, publish-either-way).** RP11b engine (`rp11b_engine.py`, exact-probe: two invariants enumerated independently, identity-tested, assumption-debt ledger H1–H5 printed every case) calibrated on five registered expectations: C1 Ising KW planar 3×3 (map t = t̃ recovered exactly, K* = 0.440686793510 ✓); C2 q = 3 Potts RC primal/dual (unique library hit ṽ = q/v with prefactor v^E q^{−(V*−1)} recovered *from the sweep, not assumed*; v* = √3 ✓); C3 Ising 3×3 torus (OBSTRUCTION certified: four distinct homology-sector polynomials; residual = spin-structure sum ✓); C4 S-duality structure (S² = −I, (ST)³ = S², coroot(B₃) = roots(C₃); residual = center/level ✓); C5 particle-vortex Poisson chain certified numerically at 1e−11 over 25 random probes (residual = windings ✓). **5/5 substantive; calibration also produced the engine's first rig-level defect (finding F1): verdict taxonomy asymmetric between bare (C1) and prefactor-normalized (C2) comparisons — v0.1 printed record stands; v0.1.1 fix registered forward-only, no re-scoring.** Ledger: `rp11b-calibration-results.md`. W3b atlas (`w3b_atlas.py`): row i (J,K) split pair → **failure published first**: linear-world adjunction impossible (rank certificate: ‖JK − I₈‖ = 8.72, rank 3 < 8) with the exposed trap class that triangle identities PASS (1e-14) yet are insufficient — promoted to a standing atlas check rule; canonical repair K# = Jᵀ yields the reflective inclusion with exact projector counit; ambient setting-flip (ordered world: same data IS a Galois connection) recorded as an empirical atlas axis. Row ii Weingarten = Gram: counit certified ⟺ d ≥ n with full rank-audit table (n = 3: ranks 1/5/6 for d = 1/2/3, σ_min = 0/6e-16/6); known n=2 values matched exactly. Row iii S_n × S_n bimodule: positive at module level (Peter–Weyl certificate Σdλ² = |S₃|); expectation postmortem logged: the anticipated failure attaches to the strict level, which is queued. Paper-specific rows (B_even·B_odd, C_comp, Φ_n strict, Clifford 3-design) marked definition-pending — none guessed. Ledger: `w3b-atlas-results.md`. W3-v10 benchmark (pre-cutoff, blinded, externally scored) remains registered, unrun."""

s = rep(s, "Report: `cdt-2d-mcmc-results.md`. Throughput zero; a quantified gate failure is the machinery working.\"\"\"", "PLACEHOLDER", 1) if False else s

ANCHOR = "Report: `cdt-2d-mcmc-results.md`. Throughput zero; a quantified gate failure is the machinery working."
s = rep(s, ANCHOR, ANCHOR + ENTRY, 1)

io.open(DST, "w", encoding="utf-8").write(s)

p1 = io.open(SRC, encoding="utf-8").read().split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
p2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.11:", p1 == p2)
print("title:", s.count("(v10.12, GENERATIVE LINEAGE)"))
print("fold-in entry:", s.count("Framework-instrument build round"), "| F1:", s.count("finding F1"), "| trap class:", s.count("trap class"))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
