#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build formalism-v10.4.md from formalism-v10.3.md (dialogue-continuation round; Part II only).
import io

SRC = "formalism-v10.3.md"
DST = "formalism-v10.4.md"

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, "COUNT %d != %d for %r..." % (c, n, old[:90])
    return s.replace(old, new)

H4 = """*v10.4 note (2026-10-11) — VERSION NOTE, not a version (Charter rule 4: protocol registration and discipline amendments — no bridge artifact delivered; throughput zero stands). Built on `formalism-v10.3.md` (unchanged on disk). Implements the point-to-circle continuation adjudication (`point to circle audit2.txt`; record `point-circle-2-steelman-completion.md`; 5 blocks). Part II amendments: **L-8a protocol annex** (named extraction — the causal spectral dimension on CDT's foliation; declared normalization; static restatement of "flow"; **kill-warning registered — under Hořava's dispersion decomposition (arXiv:0902.3657) the d_s flow is spatial-only and d_t = 1 by construction: the 1/3 window stands as a motivating target only, and kill-1 is the parent model's own answer**; the "spine" route unregistered after a failed citation check; the two-extrema-are-definitional-artifacts rule); **privileged-not-master clause** (geometry privileged because extension is the dimension of appearance; the mathematical web stays plural — "everything is geometric" and "only dimensional relations" refused at the trivial-or-contested bar); **standing-risk line** (audit-of-audit finding, accepted: every round restates throughput-zero / benchmark-unrun / clause-binding; registrations are not results). Two register findings on the prior record accepted (ranking-claims require rubrics; adoption statements phrased as program content). Part I byte-identical to v9.1/v10.1/v10.2/v10.3.*"""

L8A = """
**L-8a — protocol annex (v10.4; satisfies gate (a) at text level, under the kill-warning that disciplines it).** (1) *Static restatement:* "flow" in this seed means **scale-dependence of a static ensemble**, probed by the diffusion parameter σ — no temporal process is claimed (P12/P13/Cor 5.1). (2) *Named extraction — the gate:* **the causal spectral dimension** (foliation-sensitive directional estimator; causal-set lineage, Eichhorn–Mizera class) applied to CDT's foliation; secondary route: the two-rate anisotropic diffusion decomposition. **Excluded:** naive timelike-link restriction (likely a line graph — d_t = 1 trivially) and the ω/k dispersion decomposition of the anisotropic-scaling model (builds d_t = 1 in by construction — see (4)). (3) *Normalization, declared:* d_s = spectral dimension of a spatial slice at fixed foliation time; d_t = foliation-direction causal spectral dimension at fixed position; any "sum invariance" wording is convention-bound, and the qualitative stake — *d_t varies across scales* — is not. (4) **Kill-warning (verification against arXiv:0902.3657):** under Hořava's dispersion kernel (ω² + k^{2z}), the return probability factors as σ^{−1/2} (time part) × σ^{−D/(2z)} (space part) — the measured d_s flow 4 → 2 is carried **entirely by the spatial factor** (3 → 1), and the temporal factor is constant 1 by construction. **The d_t = 1/z ⇒ 1/3 window therefore inherits no warrant from the model that suggested it**; it stands only as a motivating target, with the derivation-obligation unchanged. The claim's survival channel is a *named, foliation-sensitive estimator* whose result the decomposition does not pre-decide. Kill-1 (d_t ≡ 1 ± 0.1) is the parent model's own answer, not a hostile outside construction — and symmetrically: any extraction that *builds* d_t-flow or d_t-constancy into its definition scores zero either way (the two-extrema-are-artifacts rule). (5) The "spine spectral dimension" route proposed in the dialogue is **unregistered**: its cited published value was not found on literature check (possible confabulation); the candidate list stands on the causal estimator and the two-rate decomposition only. (6) *Status:* protocol text registered 2026-10-11; execution requires CDT ensemble data/computation outside this workspace — external execution, horizon **2029-10-10** unchanged. The seed remains a registered stake, not a result."""

PNM = """ **Privileged, not master (v10.4):** geometry is the privileged register *because extension is the dimension of appearance*; the mathematical web stays plural (§7) — no master-register collapse and no reduction of the algebraic, categorical, or arithmetic registers to the geometric one (E4; the trivial-or-contested dilemma: broad geometrizability is trivial, reduction is Wheeler's failed program; "only dimensional relations" refused at the same bar)."""

SR = """ **Standing risk restated (v10.4, per the audit-of-audit):** throughput remains zero; the benchmark has not run; the contraction clause remains binding; every audit round — this one included — is internal hygiene until a bridge scores. Registrations are not results."""

VROW4 = """| **v10.4 (`formalism-v10.4.md`) — VERSION NOTE, Charter rule 4** | 2026-10-11 | Same Part I as v9.1–v10.3 (byte-identical). **Part II — the dialogue-continuation round:** **L-8a protocol annex** (causal-spectral-dimension extraction named; normalization declared; static restatement; **kill-warning: d_t = 1 by construction under the Hořava dispersion decomposition — the 1/3 window is a motivating target, not a licensed prediction; kill-1 is the parent model's own answer**; spine route unregistered after failed citation check; two-extrema-are-artifacts rule); **privileged-not-master** (geometry privileged because extension is the dimension of appearance; web plurality preserved; "everything is geometric" and "only dimensional relations" refused); **standing-risk line** (throughput zero; benchmark unrun; clause binding — restated on every round). Record: `point-circle-2-steelman-completion.md` |"""

DL3 = """- **Point-to-circle continuation adjudication (2026-10-11, v10.4):** 5 blocks; geometricity three-readings verdict (privileged register, web plural); "no ultimate change/causation" tier-accepted with D11/D12 print, "only dimensional relations" refused; the audit-of-audit's four flags graded — standing-risk line installed, ranking-claims require rubrics; **L-8a protocol annex with the arXiv:0902.3657 kill-warning** (under the parent model's own dispersion decomposition d_t = 1 by construction: window = motivating target, kill-1 = the model's answer); static restatement of "flow"; spine route unregistered (unverifiable citation). Full: `point-circle-2-steelman-completion.md`.
- **External audit (S1–S77):**"""

s = io.open(SRC, encoding="utf-8").read()
s = rep(s, "(v10.3)", "(v10.4)", 1)
s = rep(s, "*v10.3 note (2026-10-11) — VERSION NOTE", H4 + "\n\n*v10.3 note (2026-10-11) — VERSION NOTE", 1)
s = rep(s, "resolution-route rule); 36-month budget.", "resolution-route rule); 36-month budget." + L8A, 1)
s = rep(s, "rescinded in favor of the corrected reading.", "rescinded in favor of the corrected reading." + PNM, 1)
s = rep(s, "engine rules changed only where listed above.", "engine rules changed only where listed above." + SR, 1)
s = rep(s, "Record: `point-circle-steelman-completion.md` |", "Record: `point-circle-steelman-completion.md` |\n" + VROW4, 1)
s = rep(s, "- **External audit (S1–S77):**", DL3, 1)

io.open(DST, "w", encoding="utf-8").write(s)

a = io.open(SRC, encoding="utf-8").read()
m1 = a.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
m2 = s.split("# PART I — THE STRICT FORMALISM", 1)[1].split("# PART II — THE RESEARCH PROGRAM", 1)[0]
print("Part I byte-identical to v10.3:", m1 == m2)
print("(v10.3) remaining:", s.count("(v10.3)"))
print("(v10.4) present:", s.count("(v10.4)"))
for k in ["L-8a", "kill-warning", "causal spectral dimension", "Privileged, not master", "Standing risk restated", "two-extrema-are-artifacts", "spine spectral dimension", "point-circle-2-steelman-completion.md"]:
    print("anchor %r: %d" % (k, s.count(k)))
print("bytes:", len(s.encode("utf-8")), "lines:", s.count("\n") + 1)
print("SUCCESS")
