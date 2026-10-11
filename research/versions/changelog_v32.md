# Changelog — v32 (claims-alignment + registered-conditional + fidelity pass)

Date: 2026-10-11 (build 2026-10-11 +03:00). Script:
`research/scripts/v22-exactZ3-n5L8/patch_v32_claims_alignment.py`.
Source preserved unmodified: `manuscript_revised_v31.tex` (and all
earlier versions). New files: `manuscript_revised_v32.tex/.pdf`, this
changelog, `README_v32.md`, `certificate_sha256_v19.txt`, and the
Tier-1 feasibility probe
`research/scripts/v22-exactZ3-n5L8/v32_tier1_L10_dimension.py` with
its result `research/results/v32_tier1_L10_dimension.json`.
Companion submission files unchanged this pass:
`supplement_v10.tex/.pdf` (verified: the supplement contains none of
the passages this pass touches — no abstract, intro-spine, Sec II A/H,
conclusion, or Sec VII content is mirrored in it).

Provenance note: author-directed pass. In the directing session
(2026-10-11) the author read the line-level audit of
`formalism-v9.2.md` and `gap.txt`
(`research/versions/audit_formalism_v9_2_and_gap_20261011.md`),
directed the restoration of the omitted `mass-less` attribute
(audit finding M1), asked for the necessity-classification decision
aligned with the framework (audit G8 / gap.txt Addition 9 — adopted,
plain-language only), and ordered the audit's recommended sequence of
wording fixes (items 1–7), all through the NEW-patch-script protocol;
v21–v31 untouched. Tier 1 compute (L=10 at n=5) itself was NOT run;
the exact L=10 sector dimension is delivered by the probe instead
(see §6 below).

## 1. Verb alignment (audit G6-1, M2, G5-locators)

The body's honest register — "Three sizes do not yet separate the two
asymptotics at $n=5$, and the honest statement is directional"
(Sec II H) — is now propagated into every claims-level location:

| Location | v31 | v32 |
|---|---|---|
| Abstract | "confirms the first-order prediction of the $q=n$-Potts identification at $n=5$" | "supports, at the three-size level, the first-order prediction ..." |
| Abstract | "dual effective closing rates that separate the continuous, marginal and first-order behaviours" | "dual effective closing rates ordered consistently with ..." |
| Abstract | "the scaled gap falling below the continuous envelope" | "... below the continuous envelope at the matched sizes" (explicitly finite-size) |
| Intro | "provides the first three-size discrimination of exponential from power-law gap closing" | "provides the first three-size evidence in the first-order direction ..., with a registered prediction for its completion" |
| Intro spine | "the three-size confirmation of the first-order prediction" | "the directional three-size evidence for the first-order prediction" |
| Body (two-size register) | "is therefore \emph{confirmed} at the two-size level" | "is therefore \emph{supported} at the two-size level" (the honest gloss carried verbatim) |
| Discussion | "the size-ladder confirmation ... conjecture being confirmed at the three-size level" | "the size-ladder directional evidence ... being supported directionally at the three-size level" |
| Conclusion | "Two sizes alone cannot separate ...; the three-size ladder does." | "Two sizes alone cannot separate ..., and three sizes do not yet do so either: what the ladder delivers is directional ... and the separation is registered as a prediction rather than claimed as performed" |
| Conclusion | "which saturates on the continuous $n=3$ envelope ($6.53$ at $L=8$)" | "which converges toward the continuous $n=3$ envelope ($6.53$ at $L=8$, $6.21$ at $L=10$), falls to $3.84$ at $n=5$ at the matched size" (the still-decaying sequence is now shown; the comparison is explicitly at the matched size) |
| Conclusion | "rates that separate the continuous, marginal and first-order behaviours at every matched interval" | "rates ordered consistently with ..." |

The Table V caption's register (rise monotonically / stay above) —
which the audit identified as the honest reference — is unchanged, as
is every data fact ("closing faster than the continuous baseline at
every size" kept; "falling below the continuous envelope" kept as an
explicitly finite-size comparison).

## 2. The registered L=10 conditional (audit G10 doctrine)

gap.txt's 19:15 doctrine: "'plausible' is a legitimate scientific
category, but only if it is anchored... Without that, 'plausible'
slides into motivated reasoning." The conditional is now registered
in three places, always as a prediction of the first-order hypothesis
(never "expected"; the interface tension is a quantity of the q=5
Potts class, a physics prediction, not a framework prediction):

- **Body (Sec II H, appended to the honest-statement paragraph):**
  "The test is therefore registered with its completion rather than
  declared finished: if the $n=5$ closing is genuinely exponential,
  the fourth size ($L=10$) will show $\sigma_{\rm eff}$ stabilizing
  at a positive interface tension, and if the asymptotic is a slowly
  decaying power law, $\sigma_{\rm eff}$ will continue to decay; the
  current data cannot distinguish these outcomes, and the registered
  conditional---not a performed discrimination---is the claim."
- **Abstract:** "... a directional trend, with the registered
  conditional that completes it: if the closing is genuinely
  exponential, a fourth size ($L=10$) will show the effective closing
  rate stabilizing at a positive interface tension, and if the
  asymptotic is a slowly decaying power law, that rate will continue
  to decay ..."
- **Conclusion:** "... the separation is registered as a prediction
  rather than claimed as performed---if the $n=5$ closing is
  genuinely exponential, the fourth size ($L=10$) will show the
  effective closing rate stabilizing at a positive interface
  tension, and if it is a slowly decaying power law, that rate will
  continue to decay."

## 3. The three remaining wording fixes

- **$p_c^{(5)}$ extrapolation note (audit G6-2, G5a).** Body: the
  locator sequence $0.48/0.47/0.465$ is now stated to be monotone
  decreasing, no size extrapolation is applied at $n=5$ (the $n=3$
  and $n=4$ points state theirs), and the quoted
  $p_c^{(5)}\approx0.47$–$0.48$ is "a plausibility range over the
  locator trend rather than a derived interval---an extrapolated
  value would sit at or below the last locator $0.465$, the firm
  constraint being $p_c^{(5)}>p_c^{(4)}\approx0.383$." Conclusion:
  the bracket is labeled "a plausibility range over the sequence,
  not an extrapolated interval."
- **Ref [15] improvement sentence (audit G6-5).** Sec II A, after the
  name adoption: "Relative to that reference, the present analysis
  supplies the two-sided statement the feature space requires:
  Theorem 1 (fixed-basis algebra and failure of local feature
  closure) proves that the span is not closed under fixed-basis
  projective measurement---the leakage of Eq. (leaknorm)---and
  Theorem 2 (exact gate-to-gate feature dynamics), with its
  general-$n$ form (Eq. Wpn), proves that a subsequent layer of
  independently Haar-averaged two-site gates on a perfect matching
  closes the leaked directions exactly, for every replica number."
- **L=8 verification-gap sentence (audit G6-4).** Conclusion,
  exactness paragraph: "One gap in the chain is stated plainly: the
  $L=8$, $n=5$ block itself has no independent-method check at its
  own size---its validations are the assembler's agreement with the
  deposited $L=4$ spectrum, the $L=6$ blocks' agreement with
  unrestricted colour-restricted Arnoldi solves, and the float64
  spot-checks, all at smaller sizes or internal to the block
  route---and an independent method at $L=8$ itself, for instance a
  randomized lower-bound rank estimate at the decisive $p$'s, would
  close it."

## 4. Sec VII: fidelity and the modal-character paragraph

- **M3 residue removed.** "The replica ladder then measures how the
  derived objects approach the primitive level: the annealed points
  recede monotonically from the quenched benchmark ..." → "The
  replica ladder then measures the distance of the derived family
  from the quenched benchmark: the annealed points recede
  monotonically ...". The sentence is now internally consistent with
  its own continuation; no Absolute attribute is involved.
- **mass-less restored (audit M1).** The standing metaphysics
  statement's attribute string now reads "self-existent, timeless,
  spaceless, **massless**, unchanging, complete, non-dual, without
  relations, parts, defects, or lack" — matching `absolute.txt`'s
  opening string ("self-existent, time-less, space-less, mass-less,
  unchanging, complete, non-dual, without relations, parts, defects
  or lack") under the paragraph's established hyphen normalization.
  The negative-form gloss of eight attributes is unchanged — it
  matches `absolute.txt`'s own eight-item attribute list (which like
  the string's mass-less placement does not gloss mass-less
  separately). The metaphysics remains exactly as non-load-bearing as
  before: no theorem, computation, or number depends on it.
- **The modal character of the results (necessity classification,
  plain text only).** New paragraph between "The exactness program"
  and "Reconciliation", classifying the paper's RESULTS by their
  relation to necessity, in the paper's own language (no framework
  notation — the 19:08 plain-language rule): necessitated by the
  grammar of the structures (no-freezing theorem; complexity
  trichotomy; exact rank; exact closure of $\Lambda(2)$ through the
  conjugation 3-design); exclusions (the information-theoretic no-go;
  the marginal $q=4$ log corrections; the $n=5$ ladder excluding the
  continuous baseline at the matched sizes themselves — an exclusion
  the registered $L=10$ conditional is designed to extend or break);
  relations (annealed–quenched separation; Born-versus-symmetric
  separations; the self-averaging criterion); contingent values (the
  numerical values and the specific Potts classes — facts of this
  display, necessitated by no grammar). Closing compliance clauses:
  the classification claims no generative power for any structure
  over the results, offers none of them as evidence for anything
  outside themselves, maps no attribute of the Absolute onto any of
  them, and leaves the standing metaphysics exactly where the first
  paragraph placed it. (This is gap.txt Addition 9 / audit G8 in its
  author-approved plain-language form: display-tier only, classifying
  results — not Absolute attributes — per the framework's E4
  discipline and the RP13.2 risk clause against vindication drift.)
  Intro-spine entry for Sec VII updated: "... states the standing
  metaphysics, locates the readings of quantum mechanics at the level
  of appearance, classifies the paper's results by their relation to
  necessity, and draws no structural parallel between the display and
  the Absolute ...".

## 5. Verification summary

- Patch script: 18 designed string replacements, each asserted unique
  before replacement; `manuscript_revised_v31.tex` re-read
  byte-identical after the pass (v21–v31 untouched).
- Over-claim verb scan: all flagged verbs/phrases absent
  ("confirms the first-order prediction", "the three-size
  confirmation", "the three-size ladder does", "saturates on the
  continuous", "rates that separate", "approach the primitive
  level", "is therefore \emph{confirmed}").
- New-statement presence: each new sentence/clause present exactly
  as designed ("massless" 1; "ordered consistently with" 2;
  "plausibility range" 2; "registered conditional" 2; "stabilizing
  at a positive interface tension" 3; modal-character paragraph 1).
- Reference accounting: `thm:fixed-algebra`, `thm:strobe`,
  `eq:leaknorm`, `eq:Wpn`, `thm:nofreeze`, `rem:trichotomy`,
  `thm:rank`, `prop:z3closure`, `sec:born`, `prop:replica-int` each
  +1 (the designed citations); every anchor token unchanged
  (data-availability URL, deposit list, all numbers).
- Category-error regression scan: the full v31 forbidden-token list
  still absent (Sec VII's appearance-terms state intact; the new
  paragraph introduces no Absolute-attribute mapping).
- Line-multiset audit: 1775 visible v31 lines → 1783 visible v32
  lines; 14 designed lines replaced, 22 designed lines entered
  (+8 net: the p_c^(5) note +4, the conclusion locator note +3, the
  new Sec VII paragraph +1), zero undesigned loss (difflib-positional
  audit: every changed line matched to a designed edit).
- Forbidden-token scan (house protocol, incl. `absolute.txt`
  never appearing in visible lines): PASS.
- Tectonic: 43 pages (v31: 42 — the growth is the added conditional
  ×3, the Ref [15] sentence, the L=8 gap note, the plausibility
  notes, and the new Sec VII paragraph), 609.13 KiB, zero
  unresolved references, zero new typesetting warnings (fresh v31
  probe reproduces the identical warning classes: 626 Underfull +
  7 Overfull, the Overfull being the pre-existing 1.77626pt
  sub-visible paragraph overfull documented since v28; the single
  extra build-log line is tectonic's benign .bbl pass-tracking note,
  one more typesetting pass from the page growth).

## 6. Tier 1 probe (L=10 sector dimension; compute NOT run)

`v32_tier1_L10_dimension.py` computes the exact dimension of the
mom0 triv.triv sector at $n=5$, $L=10$ by Burnside's lemma over
conjugacy classes: the orbit count of $(S_5\times S_5)\rtimes
\mathbb{Z}_5$ on $(S_5)^5$ (componentwise left/right multiplication
+ ring rotation). Validation: (i) the formula agrees with direct BFS
orbit enumeration on ten small $(n,m)$ cases; (ii) it reproduces the
deposited L=8 anchor **3865** exactly (the orbit count of
$(S_5\times S_5)\rtimes\mathbb{Z}_4$ on $(S_5)^4$, as quoted in the
manuscript's L=8 rung paragraph). Result: **L=10 sector dimension
346,177** (full bond-label space $120^5=2.49\times10^{10}$;
reduction factor 71,879; ladder 7 → 57 → 3865 → 346,177). A dense
block would need $1.2\times10^{11}$ entries — impossible; the
documented Tier-1 method is matrix-free Lanczos on the orbit basis
(days-scale engineering), which converts the registered conditional
into a measurement. It was not run this session; the number is
deposited in `research/results/v32_tier1_L10_dimension.json` for the
Tier-1 round. No number from the probe entered the manuscript (the
manuscript's L=10 statement is the registered conditional itself).

## 7. Companion record

`supplement_v10.tex/.pdf` carried forward unchanged (ledger v19
re-hashes them). The standing document `absolute.txt` (repository
root) is untouched and re-hashed by the ledger.
