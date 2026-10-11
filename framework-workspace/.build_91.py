import sys

def build(src, VTAG, PART2_NOTE):
    ops = []
    def rep(old, new, note, cnt=1):
        nonlocal src
        a = src.count(old)
        assert a == cnt, f"exp {cnt} got {a} [{note}]: {old[:70]!r}"
        src = src.replace(old, new, cnt)
        ops.append(note)

    rep('# The Framework — Consolidated Formalism and Research Program (v8)',
        '# The Framework — Consolidated Formalism and Research Program (' + VTAG + ')\n\n'
        '*' + VTAG + ' note (2026-10-11) — VERSION NOTE, not a version (Delivery Charter rule 4: no bridge artifact shipped this round). Built on `formalism-'
        + ('v9.md' if VTAG == 'v9.1' else 'v10.md') + '` (unchanged on disk). Implements the **five-audit standing-pressure-points adjudication** (`five-audits-joint-adjudication.md`; uni, glm, glm2, gpt, deepseek). **Part I — correction-class + registry + reading-layer only, freeze honored (no proposition added, none changed in truth-value):** the **L1a/L1b split** (L1b = D3-scope at the ground; the turn-136 fork priced); §0.3↔D3-scope cross-link; T12 provenance clause; D3\'s Newman answer spelled out; **A4 evaluative split** (sixth demotion refused); **the privation-filter table** run in public (uncomfortable exclusions owned); **the apophatic net** (§4) — the registry re-mapped as **kataphatic excess**; J2 **priced comparatively** + orthogonality; J9 conditionalized + dated + J6-coupled; **Premise Fallback Matrix**; §16 re-configured; title corrected (was stale "(v8)" — deepseek). ' + PART2_NOTE + '*',
        'S0-header')

    rep('are retracted (chat turn 136). No brute facts in the display; the only boundary is **epistemic**.',
        'are retracted (chat turn 136). No brute facts in the display; the only boundary is **epistemic**. *(Cross-link, five-audit round — glm2: this is textually the same commitment as **D3\'s scope** (§2, the fourth declared premise), stated at the display tier; see T12\'s provenance clause and §5\'s L1a/L1b split.)*',
        'S1-03link')

    rep('**D3 — Mathematical.** X is mathematical iff X has structure: identity, relation, distinction, order, symmetry, correspondence.',
        '**D3 — Mathematical.** X is mathematical iff X has structure: identity, relation, distinction, order, symmetry, correspondence. *Newman answer (five-audit round — glm2; deepseek\'s pressure logged):* "structure only" vocabulary is not empty because the typed-slots/yield discipline supplies **substantive constraint by demonstration** — fixed-but-brute excluded (J6), triadic structures excluded from the necessary template (P4), correct exclusions counted as yield; Newman (1928) is defeated exactly when the yield test passes. Standing pressure: typed slots are a grammar; the demonstrations are the substance (deepseek).',
        'S2-D3')

    rep('promotion beyond attribute-status is unearned. See J4, J8.',
        '''promotion beyond attribute-status is unearned. See J4, J8.

**The filter run in public (five-audit round — glm2; this table also satisfies glm's J8.1 privation-schedule demand).** The *operative* filter is the **A1/A3-lack criterion** — the classical privation rhetoric (blindness/sight) is lineage and warrant-form, decorative *around* it; the attributes are **mutually supporting under A1/A2 pressure**, not individually licensed by standalone privation logic (the v7 privation argument stands as the warrant's classical form). Verdicts are *derived*, uncomfortable ones owned — the Absolute is not personal, not an agent, not morally good in the anthropic sense:

| Predicate | Absence = lack-in-A? | Verdict |
|---|---|---|
| Complete, simple, self-existent, necessary, immutable, timeless | Negation implies dependence / two-ness / lack | **Pass** (A1, T1–T5) |
| Self-luminous, intelligible | Self-ignorance / unintelligibility = lack | **Pass** (T9, T10/A3) |
| Omniscience-of-others | There are no others (A2) | **Excluded — structurally malformed, not a lack** |
| Omnipotence (causal) | Causation is display-internal (P16); ultimate productivity contradicts Cor. 1.1 | **Excluded — mixed perfection** |
| Personality | Knower/known split is display-internal (D12, transjectivity) | **Excluded — mixed** |
| Moral goodness (anthropic) | Normative relation is display-internal; survives only as T8's apophatic core (non-defective) | **Excluded as essential predicate; analogical reading regulated** |
| Spatiotemporality, agency, discursive rationality | Manifestly mode-bound | **Excluded — mixed** |''',
        'S3-filter')

    rep('## 5. The articulation premise and the derivation of appearance',
        '''**The apophatic net (five-audit round — glm2; reading-layer: no proposition's truth-value or derivation changes; the theorems are re-described at the tier where they actually operate).** Every derivation runs through a **negation** — the positive vocabulary is nomenclature laid over an apophatic net; the framework is *apophatic in derivation, kataphatic only in naming*:

| Theorem | Derived core (negative) | Kataphatic name | Kataphatic excess |
|---|---|---|---|
| T1 | A is not composite | "simple" | ~0 |
| T2 | A is not dependent | "self-existent" | ~0 |
| T3 | A is not contingent | "necessary" | ~0 |
| T4/T5 | A is not subject-to-change, not in-time | "immutable", "timeless" | ~0 |
| T6/T7 | A is not extended, not externally related | "spaceless", "relationless" | ~0 |
| T8 | A is not defective | "perfect" | ~0 |
| T9 | A is not self-ignorant | "self-luminous" | the articulation of identity-knowing → **J1's site (L1b/D3-scope)** |
| T10 | A is not unintelligible | "fully intelligible" | ~0 |
| T11 | A is not disorderly | "maximally beautiful" | the value-content → **J4's site** |

Three consequences (glm2): (i) **negations transfer across the analogy barrier without loss** — "not composite" is exactly as true at the ultimate tier — so the analogical-slack objection lands on the naming layer, where it does no inferential work (J8); (ii) the apophatic disagreement shrinks to **naming** — the silence-tradition's method is no longer a rival method, only a label-preference; (iii) **the J-registry is a map of kataphatic excess** — the joints sit exactly where naming outruns negation (§16), and any future proposition's exposure is computable in advance.

## 5. The articulation premise and the derivation of appearance''',
        'S4-net')

    rep('**Status decision (v6, strengthened v8).** Lemma 1 **remains a defended premise**',
        '''**The L1a/L1b split (five-audit round — glm2; adopted as ADJ-3.1).** Lemma 1 is two claims under one name, of very different status: **L1a — self-knowledge has nonzero content** (near-analytic: zero-content self-knowing would make T9 vacuous under D1's identity-of-knowing-and-being); **L1b — that content is articulated structure** (the contested horn, where the analogy objection actually lands). L1b is **not an independent assumption**: it is **D3-scope applied at the ultimate tier** — the fourth declarative read at the ground rather than the display. Its honest form is gpt's *articulation commitment*: A's self-knowledge is assumed to possess differentiated content without independently subsisting ultimate constituents; the necessity of appearance is conditional on this commitment and L2. The fork is priced: structural ground vs **qualitative-remainder ground** (the *anirvacanīya* alternative — Advaita's rival terminus, rejected at turn 136 as a **choice**, not a theorem). *Underivability check:* a stipulated primitive quality R — P-present, fully known to A, non-articulable to finite perspectives — violates neither T10 (D10's scope covers it) nor L2 (which covers *structure*): **D3-scope cannot be derived from A1–A4** — the D10-apparatus that shields the framework from derivation-demand is the same apparatus that blocks this derivation (glm2). The formal-distinction criterion's scholastic lineage (Thomist *esse*/analogy) is declared as a **dependency, not a neutral criterion** (deepseek).

**Status decision (v6, strengthened v8).** Lemma 1 **remains a defended premise**''',
        'S5-L1split')

    rep("repaired by restoring A3 axiom-side and keeping T12 as exactly this application.* ∎",
        "repaired by restoring A3 axiom-side and keeping T12 as exactly this application.* *§0.3-clause (five-audit round — gpt/glm2):* the §0.3 invocation above is **cross-reference, not derivation** — §0.3 is D3-scope restated at the display tier (the same commitment); the no-brute-facts commitment was never claimed *eliminated*, only correctly located; T12's independent premises remain {A3, P2}. ∎",
        'S6-T12')

    cor_lines = [l for l in src.split('\n') if l.lstrip().startswith('- **Corollary 2.1') or l.lstrip().startswith('**Corollary 2.1')]
    cor_status = 'skip(%d)' % len(cor_lines)
    if len(cor_lines) == 1:
        rep(cor_lines[0], cor_lines[0] + ' *Grounding-semantics clause (five-audit round — gpt):* "non-dually identical" (P2) does not license treating Cor. 2.1\'s grounding as a relation of the identical referent to itself (self-grounding would trivialize the asymmetry); grounding relates **aspects/facts**, not the identical entity — asymmetric grounding holds between A qua ground and A qua appearing, which the formal distinction (Lemma 1) makes statable without two realities. See the J1 registry line.',
            'S7-cor21')
        cor_status = 'ok'

    rep("P1's necessity re-graded *strong-metaphysical-given-L1* (§5).",
        "P1's necessity re-graded *strong-metaphysical-given-L1* (§5). **Five-audit round (ADJ-3.1):** L1 split (L1a/L1b, §5); the contested half relocated to **D3-scope's priced fork** (structural ground vs qualitative-remainder). deepseek's promote-or-demote binary **refused** (demotion internally fatal — v6 arithmetic; immediate promotion would axiomatize near-analytic L1a and duplicate already-declared D3-scope — and promotion clarifies commitment, cures no contradiction: gpt); A5 stays pre-committed as the formal-distinction-failure fallback. Cor. 2.1 grounding ≠ self-grounding (aspects/facts, not the identical referent — gpt). Premise-load accounting (glm2): the v8 episode's net gain was *explicitness*, not economy — D3-scope now visibly carries L1b, T12, and RP13.8's falsifiability.",
        'S8-J1')

    rep('- **J2 — Ontological gap.** Existence not derivable from content (E1); cumulative convergence foregrounded in RP6 (v6).',
        '''- **J2 — Ontological gap.** Existence not derivable from content (E1). **Five-audit round (ADJ-3.2) — the gap is priced comparatively** (glm2): every terminus pays a terminus-cost; this one is named in advance. **Orthogonality printed:** bridge success does not touch J2; J2 does not excuse bridge failure (glm's E8-ban refused — E2/E3 already do its work; deepseek's strengthen-the-cumulative-case refused as vindication drift). The RP6 routes converge on a **structural description**, not on existence (uni); their contributions are not assumed independent (gpt); the transcendental route's deliverable is the immediate non-objectified ground of awareness — not the full attribute set (uni/gpt/deepseek concur).

| Terminus | Its priced gap |
|---|---|
| **This framework** | Existence of A underived (J2); four declared load-bearing premises |
| Physicalism | Consciousness as *its* brute remainder; initial conditions primitive |
| Mathematical platonism | Efficacy/instantiation of structure; why any sub-web is physical |
| Classical theism | Why create at all; modal scope of divine choice |
| No terminus (infinite regress) | Explanation never starts — the most expensive option |
| Apophatic silence | Content-collapse: affirmed but unspecifiable |''',
        'S9-J2')

    rep('"schema" marks access, not a lack in A.',
        '"schema" marks access, not a lack in A. **Five-audit round (ADJ-3.3):** downgraded to **declared premise, yield-governed** — the residual is D3-scope (priced at §5) plus the Newman question (answered at D3 by demonstration; deepseek\'s pressure logged). **P10-vs-RP13.8 tension resolved by tier** (glm2 — the round\'s largest structural find): ultimate tier — consciousness is what structure *is* (P10, not structure-emergent); display tier — description-is-structure is the *bet* (RP13.8). **RP13.8 is thereby wired as D3-scope\'s only display-level falsification route:** a structure-identical qualitative difference would be a display-level suchness remainder, cascading L1b → T12 → P1. glm\'s formalism-commitment for M adopted at Part II only (kernel/engine run on a declared restricted class M₀; [Uncomputable-Illustrative] tag for M∖M₀ results); refused for Part I — the schema *is* the honest commitment. gpt\'s index-discipline adopted as Part-II grammar (S⊨φ / T⊨¬φ indices retained).',
        'S10-J3')

    rep('"plenitude runs on A1+A2+A3" is literal again. Demotion still refused.',
        '"plenitude runs on A1+A2+A3" is literal again. Demotion still refused. **Five-audit round (ADJ-3.4) — sixth demotion attempt (glm + deepseek) refused on the standing record**; the constructive payload adopted instead: **evaluative split explicit** (uni) — "mystery is a defect" is **[aesthetic-regulative]**, never Ultimate-inferential: maximal-intelligibility ⇒ that value verdict is *not* licensed, matching the beauty⇒truth non-license; **filter table installed** (§3 — uncomfortable exclusions owned; satisfies glm\'s J8.1 schedule); T11\'s weakness *explained*: it carries the system\'s maximal **kataphatic excess**, the largest naming-to-negative-core gap (§4 net). glm\'s search-priority content ≈ the existing aesthetic-regulative tag — absorbed without axiom-list surgery.',
        'S11-J4')

    rep('*Not F-deducible:* no finite derivation of it from the axioms exists or is claimed.',
        '*Not F-deducible:* no finite derivation of it from the axioms has been **supplied**, and none is claimed — and no impossibility is asserted either: per-instance openness is D10\'s settled doctrine (v9\'s P8; gpt\'s precision rule).',
        'S12-J5a')

    rep('exactly what A3 predicts can always be done, and what D10 predicts never finishes.',
        '''exactly what A3 predicts can always be done, and what D10 predicts never finishes. **Five-audit-round relabel (glm2/gpt):** the Gleason example is **recognition/calibration-class** — the field's theorem read through the framework afterward; it calibrates what a discharge *looks like*. Progress = **yielded discharges only**, tallied annually in W5: current count **0 yielded** vs 3+ recognition-calibrations (Gleason, Wigner, spin–statistics). The two reductions stay distinct (uni): Reduction-1 (feature ⇒ derivable from Part I) is forbidden; Reduction-2 (feature ⇒ necessitated by the web's own grammar) is the only legitimate target — never presented as approaching Reduction-1.''',
        'S12-J5b')

    rep('a live scientific question.',
        '''a live scientific question. **Five-audit round (ADJ-3.5-refinements):** (i) horn-2's structure printed — it covers *discrete choice + measure* (e.g., a landscape case: parameter set consistency-forced, vacuum not), not only continuous variation (glm2); (ii) **J6↔J9 coupling:** horn-2 is hostage to the Selection Kernel's deliverable — if no admissible measure exists, any parameter it was carrying becomes fixed-but-brute and the disjunction dies; the two joints rise and fall together (glm2); (iii) protocol: standing W5 line item, re-scored at each leading-candidate status change; strongest form stated — **zero free parameters at the final node**; (iv) **divergence printed:** landscape-real + measure-satisfied = J6 horn-2 wins while RP13.3's strong swampland thesis loses — different bets, scored separately (glm2); (v) the engine's scoped claim format per problem: Γ ⊢ C(θ) — countermodel defeats the conjecture, observational disagreement tests the package (gpt). Falsifier-bar note (deepseek): the bar is high because the bet is strong; it survives on record, honestly.''',
        'S13-J6')

    rep('- **J7 — Baseline empirical caution.** Physics does not decide timelessness vs. passage (stalemate); P15 carries no novel predictions; empirical value is heuristic under E3; **v6:** bridge claims are evidence of *heuristic* value — *empirical* value accrues only to bridges that survive hostile tests (RP8 intro).',
        '- **J7 — Baseline empirical caution.** Physics does not decide timelessness vs. passage (stalemate); P15 carries no novel predictions; empirical value is heuristic under E3; **v6:** bridge claims are evidence of *heuristic* value — *empirical* value accrues only to bridges that survive hostile tests (RP8 intro). **Five-audit round (ADJ-3.6):** metricized and doubled — running counter in W5 (proposed / survived / killed = **0/0/0**); un-stalemating triggers both directions (timeless-side: thermal-time-class derivation of an arrow; community-standard timeless QG; Page–Wootters extension to cosmology. passage-side: an accepted QG with a fundamental time variable); the **honest asymmetry printed with its tier label**: current activity is timeless-weighted — it favors the framework — and *must* stay labeled theory-choice-tier or it functions as covert credit-claiming (glm2). **Double discipline:** physics\'s *failures* are not absorbed either (SUSY\'s non-appearance costs nothing — H7 was already candidate). **Productivity mandate (glm):** every domain program outputs ≥1 *genuine* exclusion (forbid-channel) per cycle — genuine, never manufactured (gpt-guard) — or is demoted to interpretive. **Vindication-drift flag extended (deepseek):** engine success validates the *heuristics*, never the metaphysics.',
        'S14-J7')

    rep('Apophatic silence-tradition registered as **acknowledged rival horizon** — engaged where it argues, accommodated where it marks the medium\'s limit; not refuted, not adopted.',
        'Apophatic silence-tradition registered as **acknowledged rival horizon** — engaged where it argues, accommodated where it marks the medium\'s limit; not refuted, not adopted. **Five-audit round (ADJ-3.7):** the **apophatic-net reading installed** (§4 — derivations run negative; excess lives in naming; the disagreement shrinks to *naming*). **Non-refutation disclaimer (gpt):** universal ineffability is *rejected as commitment*, **not claimed neutrally refuted** — an objection applying to an entire class can undermine that class; the "non-discriminating" verdict stands only scoped: it selects against no *claim-making* system, and claim-free methodological apophaticisms are exempt from the self-application argument. What analogical predicates license is exactly the negative cores (§4) — tier tags mark, they do not supply, semantics (gpt); the privation schedule is the §3 filter table (glm\'s J8.1, satisfied by the same artifact).',
        'S15-J8')

    rep('no typicality rule = the standard reductio: a typical perspective would sit in a structureless or incoherent configuration (far more numerous); we observe a lawful world with records.',
        'no typicality rule = the reductio, **conditionalized (five-audit round — glm2/gpt):** "typical" is *undefined* without a measure, and "far more numerous" is measure-relative — the reductio holds **conditional on no admissible measure existing** that weights-without-excluding (D7-safe), is encoding-robust, and renders lawful observers non-atypical; if none exists, P14/P15 die by their own kill-criteria, and if one exists the reductio never launches (glm\'s pre-emptive P14-demotion **refused**, ADJ-3.6 — the armed conditional sanction, not pre-emptive closure, is the honest mechanism). The observer reference class is a *declared research output* — whatever N4\'s self-modeling invariants pick out — not a stipulation. The obligation is **dated** (kernel kill row, 2027-10-10) and **coupled to J6** — horn-2 of the constants bet is hostage to this deliverable; the joints rise and fall together (glm2). We observe a lawful world with records.',
        'S16-J9')

    # S17 fallback matrix before worked example
    rep('**Worked example — P-present ≠ F-deducible (v6, J5).**',
        '''**Premise Fallback Matrix (five-audit round — glm; a joint without a declared fallback is a hidden axiom — with this table, none stays hidden).**

| Declared non-axiomatic premise | If it fails | Declared fallback |
|---|---|---|
| **L1** (Lemma 1) | P1's totality-step loses its modal support | **A5 promotion** (pre-committed; promotion clarifies commitment, cures no contradiction — gpt) |
| **Predication Premise** (§3) | T1–T11 + A4 lose their license; A1 goes inert | Bare non-dual monism without attributes |
| **L2** (Expression Premise) | Plenitude falls — D8/P9 local, not universal | Scoped plenitude of the mapping-rule's range only |
| **D3-scope** (§0.3/§2) | L1b, T12, and RP13.8's test lose their premise | The qualitative-remainder terminus (the turn-136 fork's other horn) — registered, priced, not held |

**Worked example — P-present ≠ F-deducible (v6, J5).**''',
        'S17-matrix')

    # S18 §16 rewrite (last section: replace from header to EOF)
    i = src.find('## 16. Standing pressure points')
    assert i > 0
    src = src[:i] + '''## 16. Standing pressure points (restated from v2; re-configured in the five-audit round)

The v2-era list stands — Lemma 1 (J1); ontological gap (J2); M as schema (J3); beauty axiom (J4); P-present vs F-deducible (J5); plenitude's specific form (J6); empirical baseline caution (J7); plus J8 (v7) and J9 (v8). What changes now is the registry's *shape* — after this round the nine joints are **one structure, not nine separate exposures** (glm2's closing configuration, adopted):

1. **An apophatic derivation-net** — T1–T11 derive negative cores; near-zero systematic exposure (table in §4).
2. **A kataphatic naming layer** where all live excess concentrates — the excess map: **J1/J3** sit at T9's articulation (L1b = D3-scope's priced fork); **J4** sits at T11's value-content; **J8** is the naming question itself.
3. **One priced existence-gap** — J2, with the comparative table and the orthogonality clause printed (§12).
4. **Three metricized engines with printed counters** — J5's yield-tally (**0 yielded / 3+ recognition-calibrations**, carried annually in W5); J6's standing bet (re-scored per W5, **coupled to J9**); J9's dated obligation (kernel by **2027-10-10**, kill-armed).

The per-joint details stay in §12 with full provenance. Open joints remain features of an honest system — but the registry is now a **map** (of kataphatic excess), not a list (uni's assessment, glm2's completion): each joint is a located quantity with a declared fallback, a priced cost, or a running counter — and any future proposition's exposure is computable before adversaries run it.
'''
    ops.append('S18-s16')
    return src, ops, cor_status

if __name__ == '__main__':
    v, note = sys.argv[1], sys.argv[2]
    src = open(sys.argv[3]).read()
    out, ops, cor = build(src, v, note)
    open(sys.argv[4], 'w').write(out)
    print(f'{sys.argv[4]} written: {len(out)} bytes; {len(ops)} blocks; cor2.1={cor}')
