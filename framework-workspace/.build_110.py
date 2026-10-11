#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-v10.10.md from formalism-v10.9.md — GENERATIVE LINEAGE: registers the lineage decree.
import io

SRC = "formalism-v10.9.md"
DST = "formalism-v10.10.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

H10 = """*v10.10 note (2026-10-11) — GENERATIVE LINEAGE; VERSION NOTE, not a version (Charter rule 4: a labeling/numbering decree registered — delivered bridge artifacts: none; throughput zero stands, restated under the v10.4 rule). Built on `formalism-v10.9.md` (unchanged on disk). Registers the **lineage decree (user-mandated 2026-10-11)**: the program runs as **two numbered lineages** — the **DESCRIPTIVE LINEAGE (v9.x)**: the stable fortress register (last: `formalism-v9.1.md`; newly aligned: **`formalism-v9.2.md`**, title labeled "DESCRIPTIVE LINEAGE", with the full digest of the generative line v10.0–v10.9 in its Lineage Appendix) and the **GENERATIVE LINEAGE (v10.x)**: this engine register (titles labeled "GENERATIVE LINEAGE" from this release). **Numbering is independent per branch; the pairing rule is standing**: descriptive and generative releases travel as a labeled pair at milestone rounds, and a descriptive digest refresh is mandatory whenever a generative release corrects/updates a fact the descriptive line asserts (trigger-cadence, not calendar). **The decree's own alignment discharge**: the descriptive line had not been advanced since v9.1 while ten generative releases accumulated — including one arithmetic correction (sum-invariance withdrawal, v10.5) that superseded wording the descriptive text carried, one kill-warning annex (v10.4), one counterfeit closure (v10.7), and the gate-run log (v10.9); all are mirrored descriptively in v9.2's appendix. Part I remains the shared lineage invariant — byte-identical across both lines (v9.1 = v9.2 = v10.0–v10.10, split-checked every build); any Part-I change would be contraction-class in both. Historical titles v10.0–v10.9 keep their unlabeled text; the label applies forward. Part I byte-identical to v9.1–v10.9.*"""

VROW10 = """| **v10.10 (`formalism-v10.10.md`, GENERATIVE LINEAGE) — VERSION NOTE, Charter rule 4** | 2026-10-11 | Same Part I as v9.1–v10.9 (byte-identical). **Part II — lineage decree (user-mandated):** two numbered lineages registered — **DESCRIPTIVE (v9.x)** = fortress register, newly aligned as **`formalism-v9.2.md`** ("DESCRIPTIVE LINEAGE" title; Lineage Appendix mirrors the generative line v10.0–v10.9 incl. the sum-invariance withdrawal, kill-warning annex, counterfeit closure, gate-run log); **GENERATIVE (v10.x)** = engine register, labeled from this release; numbering independent per branch; **pairing rule standing** (labeled pair at milestones; descriptive refresh trigger-cadenced whenever a generative release alters a descriptive-line assertion). The stale-descriptive gap acknowledged on record: ten generative releases unmirrorred, corrected this round. Part I = the shared lineage invariant. |"""

DL9 = """- **Lineage decree (2026-10-11, v10.10 GENERATIVE / v9.2 DESCRIPTIVE):** user-mandated split operationalized — descriptive line (v9.x) and generative line (v10.x) labeled in titles, independently numbered, paired at milestones with trigger-cadenced descriptive refresh; the v9.1→v9.2 alignment discharge mirrors all ten generative releases in descriptive register (including the withdrawal that superseded text the descriptive line carried). Part I byte-identical across both lines; historical titles untouched. Records: `formalism-v9.2.md` Lineage Appendix + this row.
- **External audit (S1–S77):**"""

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.9)", "Research Program (v10.10, GENERATIVE LINEAGE)", 1)
s = rep(s, "*v10.9 note (2026-10-11) — VERSION NOTE", H10 + "\n\n*v10.9 note (2026-10-11) — VERSION NOTE", 1)
s = rep(s, "Records: `search-eval.md`, `cdt-2d-calibration-results.md`, `cdt_cal_2d.py` |", "Records: `search-eval.md`, `cdt-2d-calibration-results.md`, `cdt_cal_2d.py` |\n" + VROW10, 1)
s = rep(s, "- **External audit (S1–S77):**", DL9, 1)

io.open(DST, "w", encoding="utf-8").write(s)

a = io.open(SRC, encoding="utf-8").read()
m1 = a.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
m2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.9:", m1 == m2)
v9 = io.open("formalism-v9.1.md", encoding="utf-8").read()
m0 = v9.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I v9.1 == v10.10:", m0 == m2)
print("title gen-label:", s.count("GENERATIVE LINEAGE"))
for k in ["DESCRIPTIVE LINEAGE", "formalism-v9.2.md", "pairing rule", "lineage decree"]:
    print("anchor %r: %d" % (k, s.count(k)))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
