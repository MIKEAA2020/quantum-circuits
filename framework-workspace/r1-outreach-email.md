# R1 Outreach — draft email (Node B; edit bracketed fields before sending)

**To:** [Prof. Renate Loll, IMAPP, Radboud University Nijmegen] — *fallback: [Prof. Jerzy Jurkiewicz, Jagiellonian University, Kraków]*
**Subject:** Pre-registered proposal: first extraction of the temporal spectral dimension in 4D CDT (de Sitter phase)

---

Dear Professor [Loll / Jurkiewicz],

I am writing to propose a collaboration on a measurement that, to my knowledge, has not been performed on CDT, and for which the data and the tool both already exist — the only missing piece is running one against the other.

**The question.** CDT's celebrated dimensional reduction of the *total* spectral dimension (≈ 4 → ≈ 2) is established, and Benedetti–Henson/Kommu measured the *spatial-slice* spectral dimension (UV ≈ 1.5–1.56), showing that directional decomposition is non-trivial. What has never been measured is the complementary object: the **foliation-direction ("temporal") spectral dimension d_t(σ)**. Eichhorn & Mizera's causal spectral dimension — explicitly proposed by its authors for application to CDT — is the natural instrument. I have adapted their two-walker meeting-probability estimator to CDT's dual graph and foliation structure (the adaptation is validated against the flat and 1+1D controls with pre-registered targets; all controls pass).

**What I am asking.** Access to an existing ensemble of 4D CDT configurations in the extended de Sitter phase, with foliation-time assignment — or a joint run on your group's code. The analysis code is written, frozen, and hash-committed before any data would be seen.

**What the collaboration gets.**

1. A fully **pre-registered** protocol (attached as `L8b-prereg.md`): calibration gates that must pass before any ensemble analysis, named kill criteria (including "d_t ≡ 1 at all scales ⇒ claim dead"), pre-declared σ-windows, whole-ensemble inclusion, and analyst blinding — the comparison to the predicted direction is only made after the pipeline is frozen. The protocol is designed so that it *can* cleanly fail.
2. A genuinely open measurement in your field: whatever d_t(σ) does — flow or no flow — is a publishable answer to a question the literature has flagged but not run.
3. External-review parity: the protocol *requires* a CDT-experienced reviewer before scoring, which is you.

**What I am not asking.** No compute from your side beyond what an existing ensemble provides; no endorsement of any framework behind the question; the registered null-expectation in the document (a Lifshitz-type picture yields d_t ≡ 1) is printed in the proposal itself.

If this is of interest, I would be glad to discuss the adaptation details, or to send the frozen extraction code. Should it not fit, a pointer to a student or postdoc for whom it might is already a good outcome.

With best regards,
[Name]
[Affiliation / ORCID]
[Contact]

---

**Attachment:** `L8b-prereg.md` (frozen pre-registration, fingerprint L-8d-PR-2026-10-11).

*Sender notes: this draft deliberately says nothing about the broader framework — the ask stands on the measurement's own merit. Calibration evidence available on request (Gate C0a/C0b 2D controls, artifacts in the project workspace). SR8 applies: values of σ-windows and seeds are in the frozen artifact, not in this email.*
