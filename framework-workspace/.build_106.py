#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-v10.6.md from formalism-v10.5.md (dialogue fourth round; Part II only).
import io

SRC = "formalism-v10.5.md"
DST = "formalism-v10.6.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

H6 = """*v10.6 note (2026-10-11) — VERSION NOTE, not a version (Charter rule 4: one registered software-family, guard lines, instrumentation rules — delivered bridge artifacts: none; throughput zero stands, restated again under the v10.4 rule). Built on `formalism-v10.5.md` (unchanged on disk). Implements the point-to-circle fourth-round adjudication (`point to circle audit4.txt`; record `point-circle-4-steelman-completion.md`; 8 units R1–R8). That corpus is render-corrupted inside otherwise well-formed lines (machine trade-prose folded from the framework's own vocabulary); reconstruction-confidence is marked per unit in the record and low-confidence material was not over-adjudicated. Part II: **HV-7 registered** (the corpus's own answer to "is the point-circle done after c = 1?" — no: c = 1 closed as a *codomain calibration*; what the foundation asks for now is the family done as an *object*: (i) bifurcation analysis across suppressed-and-activated modes, regime-by-regime down the Epstein–Tauber ladder, obstruction-locus named per regime; (ii) ≥2 first-precendence descendants from the three standing candidate-series; (iii) the d_t-monitor run to its encompassing convergence-crossing point with the five-way classification converge / kill / redirect / clarify / upgrade; printed kill: limit un-holdable ⇒ HV-7 dies, program contracts to L-4's holdout route); the **SPATE-epilogue reading** (H = dim(ambient) parameter-register; L-4's arms re-fixed: bridge #1 inscriptive-energy partial-reading ↔ masked-base still unidentified; bridge #2 real-Poisson-mode candidate named; all read-out components under horizon 2029-10-10); **three guard lines** (calibration ≠ physics bet, both directions; $F_n^{(s)}$ degeneracy = the default-null until the monoidal way-of-sequence is shown; the "d_t attains the crossing point" idiom is observer/*evaluation*-convergence and is flagged wherever used); **two instrumentation rules** (no-weird-miracles yield-typing: every yield line must type as specifiable fact + observer-injection; Will = object-shell not theorem, with the ordering fixed: point-circle first, its echo second — never echo-as-ground). Adjudications (record §IV): c=1→calibration; critic's closure-demand vs defense's declarative-appendage → split (defense on scaffold-classification, critic on every earned-content drift); independence-vs-degeneracy → standing monitor; sameness-of-bridge across rounds → obligation-sameness, priced against self-citation. Part I byte-identical to v9.1–v10.5.*"""

HV7 = """

**HV-7 — the object-stage charge (registered as software-family, 36-month budget; the fourth-round "what now," taken at full strength).** *Premise (the corpus's own verdict, adopted):* c = 1 and the SPATE codomain machinery closed as a **calibration map** — that is earned and finished; the family is not yet done **as an object**. *Charge:* (i) a **bifurcation analysis** of the family across suppressed-and-activated modes, regime-by-regime down the Epstein–Tauber ladder, with the obstruction-locus **named at each regime** (the critical obstruction treated as what it is: a *limit*); (ii) ** at least two first-precendence descendants delivered** — genuine emerging-branch candidates drawn from the three standing candidate-series: Pair-Point (+1), Ground-vector (0), and the projectable-forward-difference family — each with its card-2 shape computed; (iii) the **d_t-monitor carried to its encompassing convergence-crossing point** and the outcome classified, one of: *converge / kill / redirect / clarify / upgrade*. *Deliverables:* a verifier-approved bifurcation report, and two registered candidate-first-precendants. *Printed kill:* if the bifurcation analysis shows the limit un-holdable within the family, HV-7 dies and the program contracts to L-4's holdout route. Registrations are not results.

**SPATE-epilogue note (v10.6).** The codomain parameter-register of the fixed-ray family is the ambient dimension: **H = dim(ambient)**; the seed computed-up as both-fix-bar. Ledger consequence: **L-4's two arms re-fixed** — bridge #1 (inscriptive-energy partial-reading) stays live with its masked base still unidentified; bridge #2 now has its candidate named (the real Poisson-mode); **every read-out component of the whole ensemble sits under horizon 2029-10-10**. This note reads L-4's existing text; it relocates nothing.

**Guard lines (v10.6; binding on all Part-II yield speech).** (a) **Calibration ≠ bet:** a calibration closes a map and earns nothing of physical content, in either direction — and no sentence may drift a calibration into earned-content-of-reality (the critic's floor, adopted against us). (b) **Degeneracy-default:** $F_n^{(s)}$-independence carries degeneracy as its default-null until the monoidal way-of-sequence is exhibited; independence claimed earlier than that conflates imaging with independence. (c) **Convergence idiom-flag:** any occurrence of "d_t attains the (encompassing) crossing point" is observer/*evaluation*-convergence, not object-attainment; the flag rides with the idiom wherever it is used, including in HV-7 (iii) above.

**Instrumentation rules (v10.6).** (a) **No-weird-miracles:** no yield line may type as *(weird miracle)*; every yield line types as *(specifiable fact + observer-injection)*. The artifact is model; the body is transformation. (b) **Will-as-object:** the program's stake-shell is an object-shell (HV-7's candidates), not a thesis to be proved; the reading order is fixed — **point-circle first, its echo second** (census/atlas/engine are echo-readings of ground, never ground)."""

VROW6 = """| **v10.6 (`formalism-v10.6.md`) — VERSION NOTE, Charter rule 4** | 2026-10-11 | Same Part I as v9.1–v10.5 (byte-identical). **Part II — the dialogue fourth round (render-corrupted corpus; confidence-marked adjudication):** **HV-7 registered** (bifurcation analysis down the Epstein–Tauber ladder with per-regime obstruction-loci; ≥2 first-precendence descendants from the three candidate-series; d_t-monitor to the convergence-crossing point with converge / kill / redirect / clarify / upgrade; printed kill → L-4 holdout contraction); SPATE-epilogue (H = dim(ambient); L-4 arms re-fixed; read-outs under 2029-10-10); three guard lines (calibration ≠ bet; degeneracy-default for $F_n^{(s)}$ independence; d_t crossing-point idiom flagged as observer-convergence); two instrumentation rules (no-weird-miracles yield-typing; Will-as-object, point-circle-first-its-echo ordering). Record: `point-circle-4-steelman-completion.md` |"""

DL5 = """- **Point-to-circle fourth-round adjudication (2026-10-11, v10.6):** 8 units (R1–R8); corpus render-corrupted inside well-formed lines — adjudication confidence-marked, low-confidence units not over-adjudicated (standing exception to the everything-adjudicated habit, printed). Verdicts: c = 1 closed as **calibration, not physics bet** (both directions); "is the point-circle done?" → **no — map done, object not done**; critic's official-credit demand vs declarative-appendage defense → **split verdict** (scaffolds graded as scaffolds, every earned-content drift cut); $F_n^{(s)}$ independence → degeneracy-default; same-bridge threading rule adopted (obligation-sameness, priced against self-citation); **HV-7 registered** (object-stage charge with printed kill); SPATE-epilogue folded into L-4's arms; two instrumentation rules instrumented (no-weird-miracles; Will-as-object, ordering fixed). Full: `point-circle-4-steelman-completion.md`.
- **External audit (S1–S77):**"""

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.5)", "Research Program (v10.6)", 1)
s = rep(s, "*v10.5 note (2026-10-11) — VERSION NOTE", H6 + "\n\n*v10.5 note (2026-10-11) — VERSION NOTE", 1)
s = rep(s, "**2029-10-10** unchanged. Registrations are not results.", "**2029-10-10** unchanged. Registrations are not results." + HV7, 1)
s = rep(s, "Record: `point-circle-3-steelman-completion.md` |", "Record: `point-circle-3-steelman-completion.md` |\n" + VROW6, 1)
s = rep(s, "- **External audit (S1–S77):**", DL5, 1)

io.open(DST, "w", encoding="utf-8").write(s)

a = io.open(SRC, encoding="utf-8").read()
m1 = a.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
m2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.5:", m1 == m2)
print("title (v10.6):", s.count("Research Program (v10.6)"))
for k in ["HV-7", "first-precendence", "dim(ambient)", "degeneracy-default", "No-weird-miracles", "Will-as-object", "point-circle-first-its-echo".replace('-',' '), "point-circle first", "point-circle-4-steelman-completion.md"]:
    print("anchor %r: %d" % (k, s.count(k)))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
