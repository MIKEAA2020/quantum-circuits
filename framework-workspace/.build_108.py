#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-v10.8.md from formalism-v10.7.md (pre-registration artifact round; Part II only).
import io

SRC = "formalism-v10.7.md"
DST = "formalism-v10.8.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

H8 = """*v10.8 note (2026-10-11) — VERSION NOTE, not a version (Charter rule 4: one artifact-reference, one verdict, tiering — delivered bridge artifacts: none; throughput zero stands, restated under the v10.4 rule). Built on `formalism-v10.7.md` (unchanged on disk). Implements the adjudication of the "what remains before running" operational doc (`before-running-eval.md`; seven adjudications A1–A7). Part II: **L-8d — the pre-registration artifact registered:** `L8b-prereg.md` (frozen 2026-10-11; gates C0a/C0b with pass-before-ensemble and publish-either-way; **prediction tiering: P0 direction-of-flow as the SOLE primary; the 1/z-form, incl. 1/3, demoted to conditional secondary tested only if P0 confirms** — any sum-form permanently out of scope; **registered null-expectation: Lifshitz-type kernels give d_t ≡ 1, so a P0-confirm is a double finding by construction**; blinding discipline SR8: code-before-data with printed hash, analyst blinding, whole-ensemble inclusion, windows pre-declared at gate time, external CDT-expert review, no re-windowing without a new round; resource routes prioritized R1 collaboration > R2 port > R3 snapshot; outcome → disposition mapping incl. retirement-as-inapplicable as an E5-tier boundary, not a result). The round's main verdict, printed: the operational doc's "none of this is in the formal document" was **false at text level** (L-8b, v10.5; L-8c, v10.7) and **true at artifact level** — the artifact now exists; the E&M→CDT adaptation-check is promoted from warning to Gate C0a-precursor. Flat-register amendment to the doc's "none is a loss": a kill is a kill — kill-log is an asset at program level only. Part I byte-identical to v9.1–v10.7.*"""

L8D = """

**L-8d — pre-registration artifact (2026-10-11; the test made definite).** The L-8b protocol now exists as a standalone frozen artifact: **`L8b-prereg.md`** — scope, data (SR1), kernel/Convention C1 (SR2), frozen observables and estimators incl. the E&M→CDT adaptation-check as Gate C0a-precursor (SR3), calibration gates C0a (flat control: d_t = 1, d_s = 4 exact targets; ±0.05 mid-window) and C0b (2D CDT analytic control), pass-before-ensemble with publish-either-way (SR4), prediction tiering **P0 direction-of-flow (sole primary) / P1 z-form (conditional secondary)** (SR6), three kills double-gate (SR7), blinding discipline SR8 (code-before-data + hash, analyst blinding, whole-ensemble, pre-declared windows, external review, no re-windowing), resource routes R1 > R2 > R3 (SR9), disposition mapping incl. retirement-as-inapplicable as an E5-tier boundary event (SR10), schedule with read-out horizon **2029-10-10** unchanged (SR11). Adjudication of record (`before-running-eval.md`): the "not in the formal document" charge was false at text level (registered since v10.5/v10.7) and true at artifact level — remedied by this artifact; the layer test is now: absent a resource route, L-8 remains exactly what its own SR11 says — a pre-registered test under a printed schedule, not a paragraph claiming to be one. Registrations are not results."""

VROW8 = """| **v10.8 (`formalism-v10.8.md`) — VERSION NOTE, Charter rule 4** | 2026-10-11 | Same Part I as v9.1–v10.7 (byte-identical). **Part II — pre-registration round:** **L-8d artifact registered** (`L8b-prereg.md`, frozen): calibration gates C0a/C0b pass-before-ensemble; **P0 direction-of-flow sole primary, z-form/1/3 demoted to conditional secondary**; registered null-expectation (Lifshitz ⇒ d_t ≡ 1 ⇒ P0-confirm = double finding); blinding discipline SR8 against the W3/spine confabulation signature; resource priority R1 > R2 > R3; split-verdict on the "not in the formal document" charge (false text-level since v10.5, true artifact-level until now). Records: `before-running-eval.md`, `L8b-prereg.md` |"""

DL7 = """- **Pre-registration round (2026-10-11, v10.8):** "what remains before running" adjudicated (A1–A7) → **L-8d artifact** `L8b-prereg.md` frozen: C0a/C0b calibration gates, tiered predictions (P0 direction-of-flow sole primary; z-form conditional), SR8 blinding discipline built against the confabulation signature just detected in the spine datum, R1-collaboration-first resource plan, disposal mapping with retirement-as-inapplicable as an E5-tier boundary (flat-register amendment: a kill is a kill — kill-log is program-level asset only). The engine-side doc's only "over-claim" — protocol absent — was false at text level (since v10.5), true at artifact level, remedied same-round. Full: `before-running-eval.md` + `L8b-prereg.md`.
- **External audit (S1–S77):**"""

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.7)", "Research Program (v10.8)", 1)
s = rep(s, "*v10.7 note (2026-10-11) — VERSION NOTE", H8 + "\n\n*v10.7 note (2026-10-11) — VERSION NOTE", 1)
s = rep(s, "Execution remains external; horizon **2029-10-10** unchanged; registrations are not results.", "Execution remains external; horizon **2029-10-10** unchanged; registrations are not results." + L8D, 1)
s = rep(s, "Record: `cdt-data-eval.md` |", "Record: `cdt-data-eval.md` |\n" + VROW8, 1)
s = rep(s, "- **External audit (S1–S77):**", DL7, 1)

io.open(DST, "w", encoding="utf-8").write(s)

a = io.open(SRC, encoding="utf-8").read()
m1 = a.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
m2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.7:", m1 == m2)
print("title (v10.8):", s.count("Research Program (v10.8)"))
for k in ["L-8d", "L8b-prereg.md", "direction-of-flow (sole primary)".replace(' (sole primary)',''), "direction-of-flow", "double finding", "before-running-eval.md", "Gate C0a"]:
    print("anchor %r: %d" % (k, s.count(k)))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
