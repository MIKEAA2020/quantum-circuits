#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-generative-v10.14.md from v10.13 — D6: FT1 FORMALLY NARROWED to the measured adjunction
# subset; species-track registry created; v0.3 atlas round folded. In place; no diary; Part I frozen.
import io

SRC = "formalism-generative-v10.13.md"
DST = "formalism-generative-v10.14.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.13, GENERATIVE LINEAGE)", "Research Program (v10.14, GENERATIVE LINEAGE)", 1)

# D6: FT1 formally narrowed — replace the v10.13 status line paragraph with the measured narrowing.
s = rep(s,
 "**v10.13 status line (executed):** atlas v0.1 + v0.2 ran 7 row-tests (i–vi incl. two audits); **zero artifacts passed as adjunctions on triangles alone** — every surviving adjunction claim rides a decisive certificate (GG⁺ = I at d ≥ n; balanced-tensor rank/null-space identities), every failure is covariance-free data. FT1's \"one admissible species\" claim now has its first failure-rate measurement (high), forwarding the H8 diagnostic as designed.",
 "**v10.13 status line (executed):** atlas v0.1 + v0.2 ran 7 row-tests (i–vi incl. two audits); **zero artifacts passed as adjunctions on triangles alone** — every surviving adjunction claim rides a decisive certificate (GG⁺ = I at d ≥ n; balanced-tensor rank/null-space identities), every failure is covariance-free data. FT1's \"one admissible species\" claim now has its first failure-rate measurement (high), forwarding the H8 diagnostic as designed.\n\n**FT1 FORMAL NARROWING (v10.14, ADJ-13 — measured, external-assessment directive D6).** FT1 = the **adjunction track only**: its scope is the subset of corpus rows carrying a decisive adjunction certificate. Measured subset after v0.3: **4/8 row-tests positive** — (ii) Weingarten channel at d ≥ n *only*; (iii) S₃ balanced tensor (strategy level passed at the atlas's registered strict definition); (vii) universal constructions Δ ⊣ Π, ⊔ ⊣ Δ (72/72 exact count-identities, naturality brute-forced); (viii-b) Free ⊣ Forgetful (eval-at-generators bijection, 252/252 assignments, hom property exact on 3,600 sampled word pairs per assignment). The other P4 species now operate as **parallel tracks with certified instances, no longer adjunction's shadow**: *conjugacy* (iv Energy, Fenchel–Moreau boundary disclosed with grid floor 9.5e-6); *Z₂-involution* (v Particles, mode-swap certified, Kramers sign table measured CC* = TT* = ΘΘ* = −I); *Z₂-grading* (vi Spin/statistics, CAR/CCR/parity/R(2π) certificates, truncation disclosed). **FT1 is no longer readable as \"the formalization center\", even rhetorically**: adjunction passed nowhere on triangles alone; where both renderings live in one row (viii: named anti-involution polarity + free/forgetful adjunction), the species label must name the rendering. Process rule absorbed from two live bites: **verdict prose must be certificate-generated** (C²-sign row v; evaluator-order row viii — both caught by certificates, fixed forward). Atlas engines: `w3b_atlas.py` (v0.1), `w3b_atlas_v02.py`, `w3b_atlas_v03.py`; ledger: `w3b-atlas-results.md` (v0.1–v0.3, records stand unaltered).", 1)

ANCHOR = "Report: `w3b-atlas-results.md` (v0.2 section)."
ENTRY = """

**Atlas third round (2026-10-11; directives D5/D6 executed).** v0.3 stressed the rate in the positive direction exactly as instructed, on pre-registered expectation: **vii universal constructions CERTIFIED both sides (72/72 exact), viii group theory CERTIFIED twice (anti-involution S₃/Z₆/S₄ exact Cayley arithmetic; Free ⊣ Forgetful 252/252)** — with the evaluator-order bug logged first (right-to-left word accumulation made the hom property measure FALSE against hardcoded \"verified\" prose; certificate caught it; verdict text now programmatically branches on the measured flag). Measured rate: **4/8 adjunction-positive**, rendering-dependent — positives live exactly where universal properties or freeness exist; the physical E-rows iv–vi stay adjunction-negative. D6 implemented above as ADJ-13: FT1 formally narrowed to its measured subset; species tracks registered in parallel; the rate itself is P4/H8 data. Pending unchanged: row iii at the paper's Φ_n monoidal level (definition-pending: upload), block row, W3-v10 benchmark (pre-cutoff, blinded, externally scored), CDT Nodes B–D behind the email reply."""
s = rep(s, ANCHOR, ANCHOR + ENTRY, 1)

io.open(DST, "w", encoding="utf-8").write(s)

p1 = io.open(SRC, encoding="utf-8").read().split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
p2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical:", p1 == p2)
print("title:", s.count("(v10.14, GENERATIVE LINEAGE)"))
print("ADJ-13:", s.count("ADJ-13"), "| narrowing:", s.count("FT1 FORMAL NARROWING"), "| 4/8:", s.count("4/8"))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
