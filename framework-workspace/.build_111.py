#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-generative-v10.11.md from formalism-v10.10.md — Node A gate content, in place, no diary.
import io

SRC = "formalism-v10.10.md"
DST = "formalism-generative-v10.11.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "Research Program (v10.10, GENERATIVE LINEAGE)", "Research Program (v10.11, GENERATIVE LINEAGE)", 1)

ENTRY = """

**Gate-run log, second entry (2026-10-11; Node A — MCMC-grade 1+1D re-run, `cdt_mh_2d.py` + diagnostics, publish-either-way honored).** Direct-composition sampler replaced by an equilibrated Metropolis chain (microcanonical volume Σn_t = 1200, T = 48, pair-shift moves + uniform type-string Gibbs; measure convention printed: uniform labeled-slot microstates, profile-marginal ∝ ∏ C(m_s+m_{s+1}, m_s); rooted-convention collation with Ambjørn–Loll '98 = open item A1b). **C0b-full DENIED** (d_s = 1.687 ± 0.027 vs ~2 ± 0.25; d_t = 0.609 ± 0.033 vs 1 ± 0.1, window [4,40]) — diagnosed, not buried: **the projected-meeting d_t estimator has a finite-mixing-time crossover** (within-slice equilibration vs strip-jumping competition; windowed readings below the crossover read d_t < 1, deficit scaling with slice size and rate heterogeneity; asymptotic recovery d_t → 1). Diagnostics: D1 flat-profile small-slice 0.771 ± 0.042; D2 reduced strip-chain from measured profile rates 0.746 ± 0.131, same σ-shape with finite-T overshoot signature; v10.9's 0.94 re-reads as the same systematic's large-slice tail — noise-budget item closed. **Gate C0b2 registered via amendment `L8b-prereg-am1.md` (binding): full σ-table mandatory; windows must sit above the per-ensemble within-slice mixing time; crossover diagnostic printed before any flow language; no rescoring.** Both failure modes the rule guards against ran live in this gate round (a phantom kill and a phantom hit were each one naive window away from being reported). Partial status retained; promotion by evidence only. Report: `cdt-2d-mcmc-results.md`. Throughput zero; a quantified gate failure is the machinery working."""

s = rep(s, "refused (blinding protocol applied before the fact: gate data must be analytic, MCMC-grade public code, or published-group ensembles).",
          "refused (blinding protocol applied before the fact: gate data must be analytic, MCMC-grade public code, or published-group ensembles)." + ENTRY, 1)

io.open(DST, "w", encoding="utf-8").write(s)

p1 = io.open(SRC, encoding="utf-8").read().split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
p2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.10:", p1 == p2)
print("title:", s.count("(v10.11, GENERATIVE LINEAGE)"))
print("second gate entry:", s.count("Gate-run log, second entry"), "| C0b2:", s.count("Gate C0b2"))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
