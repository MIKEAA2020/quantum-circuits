# Forward Plan — topological order, feasibility-first (2026-10-11)

Time-of-writing state: L-8d pre-registration frozen; 2D gate pipeline PASS/PASS-partial; data landscape verified; no public 4D de Sitter sampler; two live clocks: **Lakatos 2027-10-10** (≈364 days; framework contracts unless theory-progress event) and **L-8d read-out horizon 2029-10-10**.

Ordering rule: every node lists its dependencies; nothing is started before its dependencies exist. Feasibility = (cost × current capability), honestly graded. Compute-bound steps are marked — they do not scale with AI labor.

---

## Node A — remove the "partial" from Gate C0b *(feasibility: HIGH; in-house; days)*

**Depends on:** existing pipeline (`cdt_cal_2d.py`), verified resource dyntri-cdt2d.
**Do:** replace the direct-composition fibration sampler with the proper MCMC-grade 2D CDT sampler (two routes: link dyntri-cdt2d output, or implement exact 2D-CDT Regge-measure Metropolis in Python — the 2D measure is combinatorially closed, so this is tractable). Quantify the flagged d_t drift item (0.952→0.915) under thermalized measure.
**Ends with:** C0b promoted partial → full, with noise budget printed. Either outcome reported (publish-either-way stands).
**Blocks:** nothing downstream depends on it, but it is the cheapest unflawed item on the board and it de-risks Node D's estimator code on a household case.
**Kill:** if MCMC run on a correct 2D measure still shows a window-stable d_t ≠ 1, that is no longer a noise item — it contradicts the kernel-construction analysis and forces a real look at the estimator before any 4D work.

## Node B — open the R1 collaboration route *(feasibility: HIGH-cost-of-writing, LOW-cost-of-sending; in-house now, external after)*

**Depends on:** `L8b-prereg.md` (exists).
**Do:** draft the outreach package — cover email + the artifact + a one-page summary of what is asked (access to C_dS-phase 4D ensembles or a joint run) and what is offered (the pre-registered, blinded, kill-on-criteria protocol; the question itself, which no CDT group has posed). Recipient order: Loll group (Nijmegen/IMAPP) first, Jurkiewicz group (Kraków) second.
**Delivered this round:** `r1-outreach-email.md` (see below; a draft ready for the user's identity/details).
**Blocks:** Node D's blinded run via *someone else's* ensembles — the cleanest path to a decision, and it simultaneously satisfies SR8 (external hands, external review).

## Node C — begin the 4D software chapter *(feasibility: MEDIUM; in-house; weeks-class)*

**Depends on:** Node A (estimator hardened on 2D), B optional.
**Do:** start the 4D CDT codebase on the verified engineering base (dyntri-rs core gives arbitrary-dimension structures; CDT-plusplus gives the move/MH reference): ergodic moves preserving the foliation, phase-scan utility, then C_dS ensemble generation, then port the validated estimator. Enterprise-grade honesty: this is the multi-month node even with AI labor; compute is a real constraint (ensemble-scale runs want a cluster — cloud is rentable; phase-scan is compute-bound, not labor-bound).
**Ends with:** a working 4D C_dS sampler + estimator, evaluated against Gate C0a and C0b-coded gates before any ensemble science.
**Blocks:** the R2 fallback for Node D, standing on our own feet if B yields nothing.
**Kill:** folded into L-8d's own disposal mapping (infeasible → retirement-as-inapplicable, E5-tier).

## Node D — the decisional run *(feasibility: NOT in-house; external/B-dependent)*

**Depends on:** B (preferred) or C (fallback), plus SR8 discipline fully staffed (external reviewer).
**Do:** nothing new — L-8d IS the node. Executed by whoever holds the ensembles under the frozen artifact.

## Parallel thread — the descriptive line

**Do:** nothing, by convention: the descriptive fortress updates only on trigger (a generative release that changes a fact it asserts, a stake closure, or a milestone). Nodes A and B do not trigger. Node D — whatever its outcome — triggers.

## What is NOT scheduled (printed, to close loops)

- No new audit rounds, version notes, or registrations unless a Node completes or a dossier arrives from the user. The registry-keeping warning is operational: the next generative release (`formalism-generative-v10.11.md`) happens when Node A lands, and its content will be the gate result, in-place, no diary.
- No reopening of the GRU package without a DOI.
- No re-scoping of the Lakatos clock.

---

**Immediate execution (this turn):** Node B's artifact is delivered (`r1-outreach-email.md`). Node A begins on the user's go — the exact-2D-measure Metropolis route is implementable in pure Python here (no external toolchain needed), and it upgrades a standing "partial" to "full," which is the cheapest genuine strengthening available anywhere in the program.
