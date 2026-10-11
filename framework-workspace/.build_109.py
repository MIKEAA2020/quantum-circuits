#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-v10.9.md from formalism-v10.8.md (search-round adjudication + first gate-level compute; Part II only).
import io

SRC = "formalism-v10.8.md"
DST = "formalism-v10.9.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

H9 = """*v10.9 note (2026-10-11) — VERSION NOTE, not a version (Charter rule 4: one gate-run log entry, one capability-register correction, one printed warning — delivered bridge artifacts: none; throughput zero stands, restated under the v10.4 rule, now with extra force: the first gate-level compute in the program's history has run and changes none of those lines). Built on `formalism-v10.8.md` (unchanged on disk). Implements the search-round adjudication (`uploads/search.txt`; record `search-eval.md`; five engine turns, four resource claims verified, one proposal refused). Part II: **Gate-run log, first entry** — `cdt_cal_2d.py` (seed-frozen, targets registered in-script before execution) executed 2026-10-11: **Gate C0a-2D-flat PASS** (full return-prob d_s = 2.003 ± 0.006 vs target 2 ± 0.1; projected-meeting d_t = 0.996 ± 0.002 vs target 1 ± 0.1; slice ring d = 1.000 exact); **Gate C0b-2D partial PASS-partial** (6-configuration fluctuating-profile ensemble: d_s = 1.984 ± 0.004, consistent with the exact 1+1D CDT value 2; d_t = 0.938 ± 0.006 with a mild σ-drift **flagged, not claimed as flow** — analytic reason pinned: for the registered C1 kernel the strip-move probability is construction-fixed, the time-marginal is a 1D chain, d_t = 1 by kernel construction; residual = strip-width mixing + finite-T torus effects; noise-budget item for the MCMC-grade re-run). Scope passed-printed: pipeline validation only; not a bridge datum; report `cdt-2d-calibration-results.md`. **The trap-inheritance warning of v10.5 is now operational**: the 2D gate demonstrates by construction why a foliation-clean C1 kernel returns d_t ≡ 1 — the decisional reading remains 4D-only (L-8d). **Capability register corrected** (against the engine's download-claims, verified): dyntri-rs real (generic N-D structures public; *simulation generators public for 2D only* — the "causal_triangulation4d.rs" reference is the structure file, not a 4D sampler; Zenodo DOI 10.5281/zenodo.16950228; R2 engineering base); CDT-plusplus real with archival scope *spherical 2+1D, 4D explicitly unsupported* (moves/persistence reference only); JorenB/3d-cdt and Damicristi/cdt unverified (not surfaced); **the GRU "Causal Spine" Zenodo package: fourth non-detection — disposition stands, conditional flip rule now printed** (if a DOI is produced: label flips to "self-published, non-independent," weight unchanged: zero external-precedent, zero gate value). **Refusal registered:** the engine's proposal to run Gate C0b against the GRU 2+1D dataset is refused on procedural grounds — gate data must be analytic, MCMC-grade public code, or published-group ensembles; own-machine data of uncertain provenance inside gate machinery is a blinding-protocol breach *by construction*. **Engine-side line adopted with teeth:** "discipline without execution is registry-keeping" — printed in the release log. Part I byte-identical to v9.1–v10.8.*"""

GATELOG = """

**Gate-run log (v10.9; L-8d gate machinery).** *2026-10-11, first entry — `cdt_cal_2d.py`, targets registered in-script before execution, seed-frozen (seed 20261011), Convention C1 kernel (lazy RW: stay 1/2, neighbors 1/6):* **GATE C0a-2D-flat — PASS.** Flat 60×600 zigzag torus (72,000 nodes): d_s window [16–128] = 2.003 ± 0.006 (target 2 ± 0.1), d_t = 0.996 ± 0.002 (target 1 ± 0.1); per-σ table stable through σ = 256 (1.993→2.000 / 0.995→0.999); slice-ring RW d = 1.000 exact. *The strongest possible negative gate outcome: the pipeline manufactures no structure on a control with none.* **GATE C0b-2D — PASS-partial.** Six fluctuating-profile configurations (uniform-composition fibrations, T = 48, N = 36k–99k): d_s = 1.984 ± 0.004 (exact 1+1D CDT value: 2); d_t = 0.938 ± 0.006 — inside tolerance with a mild σ-drift (0.952→0.915) **flagged as measurement artifact, and printed with its analytic reason**: under C1 the strip-move probability per step is construction-fixed (1/6), the time-marginal is a 1D chain, and d_t = 1 is a *kernel construction fact*; residual drift tracks strip-width mixing in the meeting marginal plus finite-T effects — noise-budget item for the dyntri-cdt2d MCMC-grade re-run (measure caveat: direct-composition sampling, not the Haar/Regge measure — hence "partial"). Scope carried verbatim from the report: *pipeline validation only; not a bridge datum; throughput (bridge-artifact deliveries) remains zero.* The v10.5 trap-inheritance warning now has a runnable mechanical demonstration; the decisional reading of d_t remains 4D-only under L-8d. Refusal of record: GRU/spine-lineage data inside gate machinery — refused (blinding protocol applied before the fact: gate data must be analytic, MCMC-grade public code, or published-group ensembles)."""

VROW9 = """| **v10.9 (`formalism-v10.9.md`) — VERSION NOTE, Charter rule 4** | 2026-10-11 | Same Part I as v9.1–v10.8 (byte-identical). **Part II — search-round + first gate-level compute:** Gate-run log opened (C0a-2D-flat **PASS**: d_s 2.003 ± 0.006, d_t 0.996 ± 0.002, slice exact; C0b-2D **PASS-partial**: d_s 1.984 ± 0.004 vs exact 2, d_t 0.938 ± 0.006 with the drift flagged-not-claimed, kernel-construction reason pinned); trap-inheritance warning operationalized in 2D; capability register corrected (dyntri-rs: N-D structures yes / generators 2D-only; CDT-plusplus: 2+1D archival, 4D explicitly unsupported; JorenB/3d-cdt, Damicristi/cdt unverified; **GRU package: fourth non-detection, conditional flip rule printed**); GRU-dataset-in-gates proposal **refused** (blinding protocol pre-fact); "discipline without execution is registry-keeping" adopted wholesale. Records: `search-eval.md`, `cdt-2d-calibration-results.md`, `cdt_cal_2d.py` |"""

DL8 = """- **Search-round + gate compute (2026-10-11, v10.9):** engine's "email next" defeated-in-part by the user's execution pressure (2D gate was always buildable in-house; verdict logged as claw-back engine→framework, accepted); four resource claims verified (dyntri-rs real-with-correction, CDT-plusplus real-with-scope-correction, two unverified); GRU Zenodo package unverified a fourth time (conditional flip rule: DOI-produced ⇒ "self-published, non-independent," weight unchanged); **first numerical event in program history**: C0a-2D-flat PASS, C0b-2D PASS-partial, slice exact — scope printed inside the artifact: pipeline hygiene, zero yield, throughput unchanged; trap-inheritance made mechanical. Full: `search-eval.md` + `cdt-2d-calibration-results.md`.
- **External audit (S1–S77):**"""

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.8)", "Research Program (v10.9)", 1)
s = rep(s, "*v10.8 note (2026-10-11) — VERSION NOTE", H9 + "\n\n*v10.8 note (2026-10-11) — VERSION NOTE", 1)
s = rep(s, "a pre-registered test under a printed schedule, not a paragraph claiming to be one. Registrations are not results.", "a pre-registered test under a printed schedule, not a paragraph claiming to be one. Registrations are not results." + GATELOG, 1)
s = rep(s, "Records: `before-running-eval.md`, `L8b-prereg.md` |", "Records: `before-running-eval.md`, `L8b-prereg.md` |\n" + VROW9, 1)
s = rep(s, "- **External audit (S1–S77):**", DL8, 1)

io.open(DST, "w", encoding="utf-8").write(s)

a = io.open(SRC, encoding="utf-8").read()
m1 = a.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
m2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.8:", m1 == m2)
print("title (v10.9):", s.count("Research Program (v10.9)"))
for k in ["Gate-run log", "2.003", "1.984", "registry-keeping", "dyntri-rs", "conditional flip", "search-eval.md", "cdt-2d-calibration-results.md"]:
    print("anchor %r: %d" % (k, s.count(k)))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
