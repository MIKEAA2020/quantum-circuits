# CDT Data-Landscape — Evaluation, Verification, Steelman & Completion (task eighteen)

**Corpus:** user-supplied summary "Here is the CDT data situation based on the web search" (tabular, 4 sections). Subject: the L-8/L-8b bridge's data feasibility. Four load-bearing claims were verified against primary/near-primary sources; one claim — the very one that feeds the previously-flagged "spine/GRU" route — **fails** and is disposed of decisively below. Register flat, per the standing rule.

**Standing risk, restated (v10.4 rule):** throughput zero; benchmark unrun; contraction/Lakatos 2027-10-10 binding; L-8 whole-ensemble read-outs under 2029-10-10. This evaluation changes none of those; it verifies *infrastructure*, not a result.

---

## I. Verification ledger

| # | Claim (as summarized) | Verdict | Basis |
|---|---|---|---|
| W1 | Total CDT spectral dimension flows 4 → ~2; UV value d_s(σ→0) = 1.80 ± 0.25 with a specific fit form | **VERIFIED** | Ambjørn–Jurkiewicz–Loll (2005) line, re-carried through the 2026 Scholarpedia review [arXiv:2604.05641] and *Gateway* [arXiv:2401.09399]: central fit **D_S(σ) = 4.02 − 119/(54+σ)** ⇒ σ→0 gives ≈ 1.82 ± 0.25. The fit form in the summary matches. |
| W2 | Spatial-slice spectral dimension measured; UV ≈ 1.5; methodology from Benedetti & Henson (2009) | **VERIFIED (with an attribution refinement)** | Methodology + slice spectral geometry: Benedetti & Henson, PRD 80, 124036 (2009) [arXiv:0911.0401] ✓. Slice UV ≈ 1.5: Kommu's validation [arXiv:1110.6875 §4.3] measures ≈1.5 on max-volume slices and quotes **1.56** from ref [4] (the Ambjørn et al. 2005 slice measurement). So: slice methodology real, slice datum 1.5–1.56 real — the "≈1.5" number sits in the 2005/2011 line, not in B&H 2009 itself. |
| W3 | **"A recent (2026) extraction of a 1D causal spine from CDT geometries yields d_s(spine) = 1.019 ± 0.015"** | **FAILED — third independent check; closed as fabrication-risk** | Two targeted searches (this task) + two prior (V-k, tasks 15–16): zero hits. The actual 2026 CDT review [arXiv:2604.05641] reports the standard 4→2 flow, no spine extraction. All real "spine" CDT material = Durhuus–Jonsson–Wheater single-spine trees (uniform infinite causal triangulations), which carry the *analytic* d_s = 4/3 branched-polymer direction — nothing like 1.019±0.015. A highly precise, uncited number matching exactly the pre-registered GRU-line prediction is the signature of a confabulated "hit". **Disposition: permanently unregistered under the exact-citation rule; banned from every prediction context both for and against the bridge.** |
| W4 | Eichhorn & Mizera causal spectral dimension (two-walker meeting probability, foliation-sensitive), explicitly proposed for CDT, never executed | **VERIFIED** (banked since L-8/L-8b underwriting) | E&M 2014 lineage; active neighborhood: Eichhorn–Surya–Versteegen [arXiv:1905.13498] on spatial-hypersurface spectral dimension in causal sets. The "proposed but not done" status is consistent with everything the review literature carries through 2026. |
| W5 | Open-source code exists: JorenB/2d-cdt; a "Simulating CDT quantum gravity" guide | **VERIFIED, with a dimensional caveat the summary missed** | Repo exists: github.com/JorenB/2d-cdt; accompanying paper [arXiv:2310.16744] (Brunekreef–Görlich–Loll, submitted **2023**, not 2024 — minor date slip). **But it is a *2D* CDT framework.** The L-8b protocol needs **4D de Sitter-phase (C_dS) configurations**: those ensembles/code are not public at that link; known routes are collaboration with the triangulations groups or new 4D generation (CDT "CDT" 4D code circulates within the groups). This is the *named resource gap*, see completion C3. |
| W6 | "Zenodo protocol paper with full audit trails/scripts/JSON" | **UNVERIFIED — not load-bearing** | Not chased in this pass; it alters no verdict either way. Logged as [open]. |
| W7 | Headline conclusion: extraction "live-but-hard"; bridge = pre-registered test waiting to be run | **CONFIRMED as the summary's own verdict and adopted** | Follows from W1–W5. |

## II. Steelman (both directions)

**Steelman of the summary.** Its architecture is exactly right and, for once, an engine-side digest got the *shape* of the situation cleaner than prior rounds' prose: (i) it separates *what is measured* (total d_s flow; slice d_s) from *what is proposed-not-done* (causal/temporal d_t via E&M on CDT); (ii) it keeps Convention C1's necessity implicit-but-present by noting slice d_s ≠ total d_s; (iii) it lands the correct bottom line — a pre-registered test, not a result. Under the framework's own arithmetic, this is the right genre of talk about L-8: feasibility talk, horizon talk, kill talk.

**Steelman of the failure mode it exhibits anyway.** W3 is not a random error; it is the same attractor that produced the original "spine spectral dimension ≈1 (GRU)" line (V-k): a pre-registered numerical commitment (≈1) plus a web-scale literature full of *spine-shaped words* generates a counterfeit "confirmation" with invented error bars. The defense of counts-and-dates applies in full: the number arrives with no author, no venue, no arXiv id, and sits one sigma from the desired value. That is precisely the population the exact-citation rule was built to keep out. Note the asymmetry and keep it explicit: **rejecting W3 protects the bridge** — if the GRU/spine route ever produces a real paper (e.g., Giasemidis–Thürigen–Zohren-adjacent radial/multigraph reduction work, which *does* exist but gives 4→2, not ≈1), the clean registration channel is open; nothing about this closure forecloses it.

## III. Completions shipped (v10.7)

C1. **L-8c addendum (data-landscape, 2026-10-11):** the verified inventory with citations pinned: total-flow fit D_S(σ) = 4.02 − 119/(54+σ), UV 1.80±0.25; B&H 2009 methodology; slice datum 1.5–1.56 ([4]/Kommu cross-check); Coumbe–Jurkiewicz UV total ≈ 3/2 ([1411.7712]); E&M estimator proposed-not-executed; Eichhorn–Surya–Versteegen 2019 neighborhood.

C2. **V-k/W3 closed: the "1.019 ± 0.015 spine" datum is fabrication-risk, permanently unregistered.** Exact-citation rule outcome printed: unregistered ≠ false — it means *no framework weight ever*, unless and until an exact citation (authors, venue, arXiv/DOI, page/ table number) exists. Standing instruction to every future audit round: any un-traceable "precise number with error bars and no citation" is downgraded by default.

C3. **Named resource gap registered inside L-8b's execution block:** public code = 2D CDT (JorenB/2d-cdt + arXiv:2310.16744); the bridge needs 4D C_dS ensembles → execution route = (i) collaboration with a running group, or (ii) port/extend the 4D CDT codebase, or (iii) re-analysis of existing ensemble snapshots if released. Text-level registration stands; external execution under horizon **2029-10-10**.

C4. **Quantitative-context strengthening of the "direction-of-flow only" stake (H1 consistent):** three independent UV numbers now on record — total 1.80 ± 0.25 (2005/fit 4.02−119/(54+σ)); total ≈ 3/2 (Coumbe–Jurkiewicz 2015); slice 1.5–1.56 — scatter inconsistent with any *single* pinned z; every z-parametrized table number in L-8b stays "hypothesis-window, derivation-obligation." No sum column returns.

C5. **Consensus-Delta kept open, not scored to us:** W2+Coumbe line = the published record already contains directional-decomposition precedent (slice ≠ total) *and* a d_t=1-held rival mechanism (scale-dependent time dilation co-variation in spirit). Kill-1's near-cousin is in print (that's the H2 refinement, unchanged). What this evaluation adds: the slice-UV ≈ 1.5 vs total-UV ≈ 1.8 non-equality is now the sharpest published evidence that **directional decomposition is non-trivial** — i.e., the premise of L-8b (that d_t is something you must measure, not read off) is validated by the data the summary surfaced. Zero framework credit taken for any of it (census rule 2).

C6. Version rows: §13 VROW7, §15 sixth line. Part I byte-identical (chain v9.1→v10.7).

---

**One-line verdict:** the CDT data landscape *underwrites the L-8b protocol's feasibility and sharpened kill-context exactly as registered*, invalidates the one previously-flagged counterfeit datum (spine 1.019±0.015 — closed), and delivers zero new results: the bridge remains a pre-registered test awaiting external execution, now with its resource gap named (4D ensembles) and its quantitative humility re-pinned (direction-of-flow only).
