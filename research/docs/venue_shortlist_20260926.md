# Venue Shortlist — "Exact Replica Mechanics and Born-Record Large Deviations in Monitored Quantum Circuits"

Compiled 2026-09-26, after the novelty scan (see `novelty_scan_20260926.md`). Paper profile: long (≈1,900 tex lines), proof-heavy with an exact-computation backbone; sits at the intersection of quantum information (monitored circuits, Clifford designs, PostBQP) and statistical mechanics (Potts universality, transfer matrices, large deviations). Single independent author, no funding line.

## Step 0 — arXiv preprint (before any submission)

- **arXiv cond-mat.stat-mech** (primary) + **quant-ph** (cross-list). The paper's own numerics benchmark cites cond-mat audiences; complexity sections pull quant-ph readers.
- Practical note: an independent researcher needs **endorsement** for a first arXiv submission in these categories — start the endorsement request early (it is the slowest non-computational step of the whole submission pipeline).
- Preprint first also timestamps priority on the p_c ladder and the pre-registered L=8 decision rule.

## Tier 1 — best-fit first submissions

1. **Physical Review Research** (APS, open access, no length cap, validity-driven acceptance)
   - Fit: exact, complete, verifiable work with methods transparency; PRR accepts long theorem+computation papers and does not require "broad interest" claims (that is PRX's bar).
   - The manuscript's revtex4-2 PRX-class layout ports to PRR with a one-line documentclass change.
   - Data/certificates (figshare) exceed its open-data expectations.
   - Fee: check current APS open-access fee schedule; traditional-subscription route historically available.
2. **Quantum** (the open-access quantum-science journal; donor-funded, no author fee)
   - Fit: the Clifford/design/PostBQP/complexity content is squarely in scope; long papers routine; open referee dialogue suits a proof-dense manuscript.
   - The stat-mech half (Potts ladder, Ising benchmark) is unusual for Quantum but not out of scope as "quantum many-body dynamics."
3. **SciPost Physics Core** (or SciPost Physics if a punchier core is extracted)
   - Fit: open peer review, free; exact-results culture; the scientific statement is "exact finite-n replica mechanics + measured universality ladder," which SciPost referees evaluate on correctness.

## Tier 2 — statistical-mechanics homes (if the paper is repositioned or split)

4. **J. Stat. Mech. (JSTAT)** — the natural audience for transfer-matrix + Potts-universality + large-deviation content; accepts long papers; SciPost-style submission pipeline.
5. **J. Phys. A: Mathematical and Theoretical** — exact methods, rank certificates, and the no-freezing theorem fit its "mathematical methods" scope well.
6. **Phys. Rev. E** — if the manuscript is trimmed to the annealed-replica-ladder core (C4, C6–C9) with the record/complexity sections moved to a companion; PRE referees are exactly the Potts-critical-phenomena community.

## Tier 3 — stretch / derivatives

7. **PRX or PRX Quantum (letter/paper)** — the pre-registered L=8 three-size verdict at n=5 (first-order vs power-law closing of the annealed replica transition) plus the four-point ladder 0.2338 < 0.305 < 0.383 < 0.47 is a genuine letter-sized result IF it lands on "first-order confirmed." Risk: high for a single independent author; only attempt with the L=8 verdict in hand and the p_c^(5) bracket sharpened.
8. **PRL letter** — same content consideration, same risk profile; PRR/PRX Quantum is the more realistic APS letter-adjacent home.
9. **Computer Physics Communications** — methods spin-off: the symmetry-reduced block route (orbit-count K compression, 2.1×10⁸ bond labels at L=8 on a 4 GB/2-core box, checkpointed chunk-resumable windows, Z[p] certificate machinery). This is a separate, publishable methods paper that also strengthens the main paper's reproducibility story.

## Recommendation

- **Primary route:** arXiv first, then **Phys. Rev. Research** (full paper, after L=8 completion), with **Quantum** as the parallel-friendly fallback and **JSTAT/J.Phys.A** as the stat-mech repositioning option.
- **Derivative papers:** (a) CPC methods paper on the exact block route; (b) possible PRX Quantum letter on the three-size verdict.
- **Pre-submission blockers (from the claims-evidence map):** figshare placeholder DOI; L=8 rung completion; add the novelty-scan references (Delmonte 2025, Suzuki 2025, Fyodorov freezing line, Webb 2016, Hoke et al. 2023).
- **Format notes:** APS venues want REVTeX (already used); Quantum and SciPost accept the same source with their class files; supplement (SM v5/v6) maps to APS Supplemental Material.

## Not recommended

- Nature-family or PRX without the L=8 verdict — the single remaining two-size caveat is the first thing such referees would attack; it is also the one thing currently being fixed by the running grid.
