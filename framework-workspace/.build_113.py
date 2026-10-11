#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-generative-v10.13.md from v10.12 — absorb the trap class into RP11b admissibility rules (D4),
# cross-ref FT1/W3b, and fold in the four-directive atlas round. In place; no diary; Part I frozen.
import io

SRC = "formalism-generative-v10.12.md"
DST = "formalism-generative-v10.13.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.12, GENERATIVE LINEAGE)", "Research Program (v10.13, GENERATIVE LINEAGE)", 1)

# D4: trap class into RP11b admissibility rules
s = rep(s,
 "**W3b — Correspondence atlas, failures first (v4 atlas re-scoped v8).** Render E-status corpus rows as **typed exact correspondences** (species: duality / conjugacy / Z₂ — ADJ-1); adjunction only where an adjunction is actually claimed. The first published page is **designated failures and the control class**, not the gallery (grok 4.4, glm §4). Failure-tolerant by design.",
 "**W3b — Correspondence atlas, failures first (v4 atlas re-scoped v8).** Render E-status corpus rows as **typed exact correspondences** (species: duality / conjugacy / Z₂ — ADJ-1); adjunction only where an adjunction is actually claimed. The first published page is **designated failures and the control class**, not the gallery (grok 4.4, glm §4). Failure-tolerant by design. **Admissibility amendment (v10.13, ADJ-12 — atlas v0.1/v0.2 yield absorbed):** every adjunction candidate must pass a **decisive identity test** (dimension/rank or an exact operator identity), not merely the triangle identities — triangle residuals at machine precision are *necessary, not sufficient* (trap class: certified live at (J,K) split pair, and on the Weingarten row below threshold d<n where MP-identities pass while ‖GG⁺−I‖ = 1). Every row carries a printed **trap_class block** (triangles vs decisive). Species assignment is **empirical**: rows iv–vi (Energy → conjugacy with Fenchel–Moreau boundary; Particles → Z₂-with-Kramers-sign; Spin/statistics → Z₂-grading) carried no surviving adjunction rendering — the high adjunction-failure rate across E-rows is itself data registered for P4/H8's inversion-rule bookkeeping. Ledger/engine: `w3b-atlas-results.md` (v0.1+v0.2), `w3b_atlas.py`, `w3b_atlas_v02.py`.", 1)

# FT1 cross-ref
s = rep(s,
 "Program: render each E-status corpus row as an adjunction candidate (work package W3b). Rows that resist adjunction form are diagnostic data for H8 and the inversion rule — the corpus becomes a conjecture engine, not a gallery.",
 "Program: render each E-status corpus row as an adjunction candidate (work package W3b). Rows that resist adjunction form are diagnostic data for H8 and the inversion rule — the corpus becomes a conjecture engine, not a gallery. **v10.13 status line (executed):** atlas v0.1 + v0.2 ran 7 row-tests (i–vi incl. two audits); **zero artifacts passed as adjunctions on triangles alone** — every surviving adjunction claim rides a decisive certificate (GG⁺ = I at d ≥ n; balanced-tensor rank/null-space identities), every failure is covariance-free data. FT1's \"one admissible species\" claim now has its first failure-rate measurement (high), forwarding the H8 diagnostic as designed.", 1)

ANCHOR = "W3-v10 benchmark (pre-cutoff, blinded, externally scored) remains registered, unrun."
ENTRY = """

**Adjunction-atlas second round (2026-10-11; four external-assessment directives, all executed; ADJ-12 above).** D1 row-iii strict level run at the atlas's own *registered* strict definition (balanced tensor over C[S₃]; the paper's Φ_n monoidal level stays definition-pending): PASSED with exact certificates — dim(X ⊗_A X) = 6 vs 36 for the naive tensor, kernel-of-multiplication = relations (containment 0.0), End_bimod = 3 = #classes, tensor–hom dim 3 = 3; failure intuition now excluded at two levels. D2 trap-class audit of row ii: **row ii is a confirmed trap-class instance below threshold** (d=2: triangles 1e-17 pass, decisive ‖GG⁺−I₆‖ = 1.000 fails; d=3 both pass) — v0.1's positive was saved by the decisive test. D3 new rows: **Energy → adjunction DENIED, conjugacy certified with Fenchel–Moreau boundary** (on-grid biconjugation residual exactly 0.0; disclosed half-step floor 9.5e-6; off-domain deficit 1.000); **Particles → mode-swap Z₂ certified exactly, Kramers sign table measured (CC* = TT* = ΘΘ* = −I), adjunction denied** (first build hardcoded \"C² = +1\" in prose against a −1 certificate — rig defect logged: prose must be certificate-generated); **Spin/statistics → Z₂-grading certified** (3-mode CAR exact, parity conjugation exact, CCR 1.8e-15 interior with truncation boundary disclosed, R(2π) = −I at spin ½) with the honesty clause that the spin-statistics *connection* theorem is not matrix-derivable. D4: trap_class block mandatory on every row, absorbed into W3b admissibility as ADJ-12. Species taxonomy empirically populated; **adjunction failure rate across E-status rows now measured as high — registered P4/narrowing data per the assessor's either-way rule.** Report: `w3b-atlas-results.md` (v0.2 section)."""
s = rep(s, ANCHOR, ANCHOR + ENTRY, 1)

io.open(DST, "w", encoding="utf-8").write(s)

p1 = io.open(SRC, encoding="utf-8").read().split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
p2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical:", p1 == p2)
print("title:", s.count("(v10.13, GENERATIVE LINEAGE)"))
print("ADJ-12:", s.count("ADJ-12"), "| trap_class:", s.count("trap_class"), "| FT1 status:", s.count("v10.13 status line"))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
