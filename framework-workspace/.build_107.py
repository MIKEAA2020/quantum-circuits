#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-v10.7.md from formalism-v10.6.md (CDT data-landscape verification; Part II only).
import io

SRC = "formalism-v10.6.md"
DST = "formalism-v10.7.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

H7 = """*v10.7 note (2026-10-11) — VERSION NOTE, not a version (Charter rule 4: a ledger addendum with pinned citations, a resource gap named, a closed counterfeit datum — delivered bridge artifacts: none; throughput zero stands, restated under the v10.4 rule). Built on `formalism-v10.6.md` (unchanged on disk). Implements the CDT data-landscape evaluation (`cdt-data-eval.md`). Part II: **L-8c addendum** — the physics literature's actual data situation for the L-8b protocol, verified item-by-item against primary/near-primary sources: total spectral flow 4 → ~2 with the pinned fit D_S(σ) = 4.02 − 119/(54+σ) (UV 1.80 ± 0.25; Ambjørn–Jurkiewicz–Loll 2005/2026-review line); Benedetti–Henson (PRD 80, 124036) slice methodology; the spatial-slice UV datum 1.5–1.56 (Kommu/arXiv:1110.6875 §4.3 cross-check) — the sharpest published evidence that directional decomposition is non-trivial, i.e., that d_t must be *measured*, not read off; Coumbe–Jurkiewicz (arXiv:1411.7712) UV total ≈ 3/2; Eichhorn–Mizera causal estimator proposed-for-CDT, never executed (Eichhorn–Surya–Versteegen 2019 neighborhood live). **Resource gap named:** public code is *2D* CDT (JorenB/2d-cdt; the accompanying guide is arXiv:2310.16744, submitted 2023) — the bridge needs 4D de Sitter-phase ensembles; routes: collaboration with a running group, port/extend the 4D codebase, or released-snapshot re-analysis. **The "spine d_s = 1.019 ± 0.015 (2026)" datum: closed as fabrication-risk — third failed independent citation check (no authors, no venue, no arXiv id); permanently unregistered under the exact-citation rule; banned from every prediction context, for and against.** Quantitative humility re-pinned: three independent UV numbers (1.80 ± 0.25; ≈ 3/2; slice 1.5–1.56) scatter more than any single z-parametrization tolerates — L-8b's table numbers stay "hypothesis-window, derivation-obligation"; direction-of-flow remains the whole stake (H1, unchanged). Part I byte-identical to v9.1–v10.6.*"""

L8C = """

**L-8c — data-landscape addendum (verified 2026-10-11; L-8/L-8b execution context).** *Verified inventory (citations pinned):* total spectral flow pinned by D_S(σ) = 4.02 − 119/(54+σ) ⇒ d_s(σ→0) = 1.80 ± 0.25 (Ambjørn–Jurkiewicz–Loll 2005; re-carried by the 2026 Scholarpedia review arXiv:2604.05641); spatial-slice methodology: Benedetti & Henson, PRD 80, 124036 (arXiv:0911.0401); spatial-slice UV datum ≈ 1.5–1.56 (Kommu arXiv:1110.6875 §4.3, cross-checking the 2005 slice measurement); total-UV ≈ 3/2 (Coumbe & Jurkiewicz, arXiv:1411.7712); the causal-spectral-dimension estimator (Eichhorn & Mizera) explicitly proposed for CDT and still never executed (active neighborhood: Eichhorn–Surya–Versteegen, arXiv:1905.13498). *What this fixes for L-8b:* (i) feasibility — extraction infrastructure-verified; (ii) non-triviality — slice d_s ≠ total d_s in the UV is published fact, so d_t is a quantity that must be *measured*, not read off (the protocol's premise); (iii) discipline — the three UV numbers scatter beyond any single zparametrization: table numbers remain hypothesis-window, derivation-obligation; direction-of-flow is the whole stake; (iv) the resource gap — public code is *2D* CDT (JorenB/2d-cdt + arXiv:2310.16744); the protocol needs 4D C_dS ensembles: route = running-group collaboration, 4D-codebase port/extension, or released-snapshot re-analysis; (v) the counterfeit datum — "spine d_s = 1.019 ± 0.015 (2026)" closed as fabrication-risk after a third failed independent citation check; permanently unregistered (exact-citation rule); banned from prediction contexts in both directions. Execution remains external; horizon **2029-10-10** unchanged; registrations are not results."""

VROW7 = """| **v10.7 (`formalism-v10.7.md`) — VERSION NOTE, Charter rule 4** | 2026-10-11 | Same Part I as v9.1–v10.6 (byte-identical). **Part II — CDT data-landscape verification:** **L-8c addendum** (pinned citations: total-flow fit and UV 1.80 ± 0.25; Benedetti–Henson methodology; slice UV 1.5–1.56; Coumbe–Jurkiewicz ≈ 3/2; E&M proposed-not-executed); resource gap named (public code = 2D; 4D C_dS ensembles required; three execution routes); **"spine 1.019 ± 0.015" closed as fabrication-risk, third failed check — permanently unregistered, banned from prediction contexts both directions**; quantitative humility re-pinned (three UV numbers scatter beyond any single z; direction-of-flow is the whole stake). Record: `cdt-data-eval.md` |"""

DL6 = """- **CDT data-landscape verification (2026-10-11, v10.7):** user-side summary evaluated item-by-item against primary sources; verified: total-flow fit 4.02 − 119/(54+σ) (UV 1.80 ± 0.25), Benedetti–Henson slice methodology, slice UV ≈ 1.5–1.56, Coumbe–Jurkiewicz ≈ 3/2, E&M proposed-for-CDT/never-executed, JorenB/2d-cdt (2D + arXiv:2310.16744, 2023); **failed/closed: "spine d_s = 1.019 ± 0.015 (2026)" — fabrication-risk, third failed independent citation check, permanently unregistered under the exact-citation rule**; published slice ≠ total UV datum confirms L-8b's premise (d_t must be measured, not read off); resource gap named (4D ensembles); three-UV-number scatter keeps z-tables hypothesis-window-only. Full: `cdt-data-eval.md`.
- **External audit (S1–S77):**"""

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.6)", "Research Program (v10.7)", 1)
s = rep(s, "*v10.6 note (2026-10-11) — VERSION NOTE", H7 + "\n\n*v10.6 note (2026-10-11) — VERSION NOTE", 1)
s = rep(s, "**point-circle first, its echo second** (census/atlas/engine are echo-readings of ground, never ground).", "**point-circle first, its echo second** (census/atlas/engine are echo-readings of ground, never ground)." + L8C, 1)
s = rep(s, "Record: `point-circle-4-steelman-completion.md` |", "Record: `point-circle-4-steelman-completion.md` |\n" + VROW7, 1)
s = rep(s, "- **External audit (S1–S77):**", DL6, 1)

io.open(DST, "w", encoding="utf-8").write(s)

a = io.open(SRC, encoding="utf-8").read()
m1 = a.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
m2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.6:", m1 == m2)
print("title (v10.7):", s.count("Research Program (v10.7)"))
for k in ["L-8c", "4.02", "1.019", "fabrication-risk", "JorenB", "cdt-data-eval.md", "dim(ambient)", "HV-7"]:
    print("anchor %r: %d" % (k, s.count(k)))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
