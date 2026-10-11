#!/usr/bin/env python3
r"""patch_v32_claims_alignment.py -- build manuscript_revised_v32.tex
from the canonical v31 file (manuscript_revised_v31.tex, preserved
unmodified alongside its predecessors).  Scope (author-directed,
session 2026-10-11; implements items 1-7 of the recommended order of
action in research/versions/audit_formalism_v9_2_and_gap_20261011.md,
the line-level audit of formalism-v9.2.md and gap.txt):

(1) VERB ALIGNMENT (audit G6-1, M2): abstract / intro / intro-spine /
    discussion / conclusion claim verbs aligned with the body's honest
    register ("Three sizes do not yet separate the two asymptotics at
    n=5", line 862):  "confirms" -> "supports ... at the three-size
    level";  "the three-size confirmation" -> "the directional
    three-size evidence";  "is therefore confirmed at the two-size
    level" -> "is therefore supported at the two-size level";
    "first three-size discrimination of exponential from power-law gap
    closing" -> "first three-size evidence in the first-order
    direction ..., with a registered prediction for its completion";
    "rates that separate the continuous, marginal and first-order
    behaviours" -> "rates ordered consistently with ..." (abstract and
    conclusion);  conclusion "Two sizes alone cannot separate ...;
    the three-size ladder does." -> the directional statement with the
    registered conditional;  "saturates on the continuous n=3 envelope
    (6.53 at L=8)" -> "converges toward the continuous n=3 envelope
    (6.53 at L=8, 6.21 at L=10)" with the comparison explicitly at
    the matched size.

(2) REGISTERED L=10 CONDITIONAL (audit G10 doctrine -- "'plausible'
    only with a registered refutation clause; never 'suggests' as a
    substitute"): stated in the body (Sec II H, appended to the
    honest-statement paragraph), in the abstract, and in the
    conclusion: if the n=5 closing is genuinely exponential, the
    fourth size (L=10) will show the effective closing rate
    stabilizing at a positive interface tension; a slowly decaying
    power law will keep it decaying; the current data cannot
    distinguish these outcomes.  The interface tension is stated as a
    prediction of the first-order hypothesis (a quantity of the q=5
    Potts class), never as expected or derived.

(3) p_c^(5) EXTRAPOLATION NOTE (audit G6-2, G5a): the locator
    sequence 0.48/0.47/0.465 is monotone decreasing; no size
    extrapolation is applied at n=5 (the n=3 and n=4 points state
    theirs); the quoted p_c^(5) ~ 0.47-0.48 is labeled a plausibility
    range over the locator trend, not a derived interval (body) and
    not an extrapolated interval (conclusion).

(4) REF [15] IMPROVEMENT SENTENCE (audit G6-5): Sec II A now states
    what the paper establishes relative to Kuo-Akhtar-Arovas-You
    [Kuo2020]: the fixed-basis leakage (Theorem thm:fixed-algebra,
    Eq. eq:leaknorm) and its exact post-Haar closure (Theorem
    thm:strobe; general-n Eq. eq:Wpn), for every replica number.

(5) L=8 VERIFICATION-GAP SENTENCE (audit G6-4): the conclusion's
    exactness paragraph now states plainly that the L=8, n=5 block
    has no independent-method check at its own size (its validations
    are at smaller sizes or internal to the block route), and that a
    randomized lower-bound rank estimate at the decisive p's would
    close the gap.

(6) SEC VII: (a) the M3 residue "The replica ladder then measures how
    the derived objects approach the primitive level" is replaced by
    the display-level statement ("the distance of the derived family
    from the quenched benchmark"), restoring internal consistency
    with its own "recede monotonically" continuation;  (b) the
    author's "mass-less" attribute is RESTORED to the standing
    metaphysics statement's attribute string (absolute.txt fidelity;
    audit M1: 0 manuscript hits in v31 was a silent abridgment of the
    v28-era adaptation; the negative-form gloss of 8 attributes
    matches absolute.txt's own 8-item attribute list and is
    unchanged).  The metaphysics remains non-load-bearing.

(7) SEC VII: new paragraph "The modal character of the results." --
    the plain-language necessitation classification of the paper's
    results (audit G8 / gap.txt Addition 9, author-approved
    "plain text only"): results necessitated by the grammar of the
    structures that carry them (no-freezing, complexity trichotomy,
    exact rank, exact closure of Lambda(2)); exclusions (the no-go;
    the marginal q=4 log corrections; the n=5 ladder excluding the
    continuous baseline at the matched sizes themselves -- an
    exclusion the registered L=10 conditional is designed to extend
    or break); relations (annealed-quenched separation,
    Born-versus-symmetric separations, self-averaging criterion);
    contingent values (the numbers, the specific Potts classes).
    Display-tier only: it classifies RESULTS, not attributes of the
    Absolute; it claims no generative power for any structure over
    the results and offers none of them as evidence for anything
    outside themselves; no framework notation is used (the 19:08
    plain-language rule).  Intro-spine entry for Sec VII updated.

No other change.  Companion supplement_v10.tex carries no
claims-strength, interpretation, or metaphysics content affected by
this pass and passes forward unchanged (ledger v19 re-hashes it).
Tier 1 compute itself (L=10 eigen-solve) is NOT performed; the
sector dimension is computed exactly by the separate probe
v32_tier1_L10_dimension.py (deposited with its JSON result).
"""
import difflib
from collections import Counter
from pathlib import Path

V = Path(__file__).resolve().parent.parent.parent / 'versions'

MS = (V / 'manuscript_revised_v31.tex').read_text()

# =====================================================================
# MANUSCRIPT: header
# =====================================================================
i_dc = MS.index('\\documentclass')
NEW_HEADER = """% manuscript_revised_v32.tex -- claims-alignment +
% registered-conditional + fidelity pass
% (patch_v32_claims_alignment.py) of manuscript_revised_v31.tex,
% which is preserved unmodified alongside its predecessors.  Scope of
% this pass, in full (author-directed, session 2026-10-11; items 1-7
% of the recommended order of action in the line-level audit of
% formalism-v9.2.md and gap.txt,
% research/versions/audit_formalism_v9_2_and_gap_20261011.md):
% (1) verb alignment: abstract/intro/intro-spine/discussion/
%     conclusion claim verbs aligned with the body's honest register
%     ("Three sizes do not yet separate the two asymptotics at n=5"):
%     "confirms" -> "supports ... at the three-size level"; "the
%     three-size confirmation" -> "the directional three-size
%     evidence"; "separate" -> "ordered consistently with"; "the
%     three-size ladder does" -> the directional statement;
%     "saturates on the continuous n=3 envelope (6.53 at L=8)" ->
%     "converges toward ... (6.53 at L=8, 6.21 at L=10)", the
%     comparison explicitly at the matched size.
% (2) registered L=10 conditional (the audit's G10 doctrine:
%     "plausible" only with a registered refutation clause): if the
%     n=5 closing is genuinely exponential, the fourth size (L=10)
%     will show the effective closing rate stabilizing at a positive
%     interface tension; a slowly decaying power law will keep it
%     decaying; the current data cannot distinguish these.  Stated in
%     the body (Sec II H), the abstract, and the conclusion.  The
%     interface tension is a prediction of the first-order hypothesis
%     (a quantity of the q=5 Potts class), never stated as expected.
% (3) p_c^(5) extrapolation note: the locator sequence 0.48/0.47/0.465
%     is monotone decreasing, no size extrapolation is applied at n=5,
%     and the 0.47-0.48 bracket is labeled a plausibility range, not
%     a derived/extrapolated interval (body + conclusion).
% (4) Ref [15] (Kuo-Akhtar-Arovas-You) improvement sentence in
%     Sec II A: the fixed-basis leakage and its exact post-Haar
%     closure, for every replica number.
% (5) L=8 verification-gap sentence in the conclusion's exactness
%     paragraph: no independent-method check at L=8 itself; a
%     randomized lower-bound rank estimate at the decisive p's would
%     close it.
% (6) Sec VII: the "approach the primitive level" residue replaced by
%     the display-level statement; the author's "mass-less" attribute
%     restored to the standing metaphysics statement's attribute
%     string (absolute.txt fidelity; audit finding M1).  The
%     metaphysics remains non-load-bearing.
% (7) Sec VII: new paragraph "The modal character of the results." --
%     the plain-language necessitation classification of the paper's
%     results (audit G8 / gap.txt Addition 9, author-approved plain
%     text only): display-tier, classifying results not attributes of
%     the Absolute, claiming no generative power, no framework
%     notation.  Intro-spine entry for Sec VII updated.
% Change log: changelog_v32.md.
% Provenance ledger: certificate_sha256_v19.txt.
"""
ms = NEW_HEADER + MS[i_dc:]

# =====================================================================
# MANUSCRIPT: the edits
# =====================================================================

EDITS = []


def rep(old, new, note):
    global ms
    n = ms.count(old)
    assert n == 1, f'[{note}] old fragment count {n} != 1'
    ms = ms.replace(old, new)
    EDITS.append(note)


# --- (1)+(2) abstract -------------------------------------------------
rep(
    'and confirms the first-order prediction of the $q=n$-Potts '
    'identification at $n=5$: an exact three-size test',
    'and supports, at the three-size level, the first-order prediction '
    'of the $q=n$-Potts identification at $n=5$: an exact three-size '
    'test',
    'A1 abstract confirms->supports')

rep(
    'with the scaled gap falling below the continuous envelope and '
    'dual effective closing rates that separate the continuous, '
    'marginal and first-order behaviours at matched sizes, and at '
    'local dimension $d=3$',
    'with the scaled gap falling below the continuous envelope at the '
    'matched sizes and dual effective closing rates ordered '
    'consistently with the continuous, marginal and first-order '
    'behaviours at matched sizes---a directional trend, with the '
    'registered conditional that completes it: if the closing is '
    'genuinely exponential, a fourth size ($L=10$) will show the '
    'effective closing rate stabilizing at a positive interface '
    'tension, and if the asymptotic is a slowly decaying power law, '
    'that rate will continue to decay---and at local dimension $d=3$',
    'A2 abstract separate->ordered + registered conditional')

# --- (1) intro ---------------------------------------------------------
rep(
    'provides the first three-size discrimination of exponential from '
    'power-law gap closing in this family.',
    'provides the first three-size evidence in the first-order '
    'direction on the gap closing in this family, with a registered '
    'prediction for its completion.',
    'I1 intro discrimination->directional evidence')

# --- (1) intro spine ----------------------------------------------------
rep(
    'with the three-size confirmation of the first-order prediction '
    'at $n=5$, the no-freezing theorem',
    'with the directional three-size evidence for the first-order '
    'prediction at $n=5$, the no-freezing theorem',
    'S1 spine confirmation->directional evidence')

# --- (7) intro spine: Sec VII entry --------------------------------------
rep(
    'states the standing metaphysics, locates the readings of quantum '
    'mechanics at the level of appearance, and draws no structural '
    'parallel between the display and the Absolute; '
    'Sec.~\\ref{sec:conclusion} concludes.',
    'states the standing metaphysics, locates the readings of quantum '
    'mechanics at the level of appearance, classifies the paper\'s '
    'results by their relation to necessity, and draws no structural '
    'parallel between the display and the Absolute; '
    'Sec.~\\ref{sec:conclusion} concludes.',
    'S2 spine Sec VII entry + classification')

# --- (4) Ref [15] improvement sentence -----------------------------------
rep(
    'we use that name for the span '
    '$\\operatorname{span}\\{I,S\\}^{\\otimes L}$.',
    'we use that name for the span '
    '$\\operatorname{span}\\{I,S\\}^{\\otimes L}$.  Relative to that '
    'reference, the present analysis supplies the two-sided statement '
    'the feature space requires: Theorem~\\ref{thm:fixed-algebra} '
    'proves that the span is not closed under fixed-basis projective '
    'measurement---the leakage of Eq.~\\eqref{eq:leaknorm}---and '
    'Theorem~\\ref{thm:strobe}, with its general-$n$ form '
    '(Eq.~\\eqref{eq:Wpn}), proves that a subsequent layer of '
    'independently Haar-averaged two-site gates on a perfect matching '
    'closes the leaked directions exactly, for every replica number.',
    'R1 Ref [15] improvement sentence')

# --- (3) body: p_c^(5) plausibility range -------------------------------
rep(
    'the gap-minimum locator is stable across the ladder ($0.48$, '
    '$0.47$, $0.465$ at\n$L=4,6,8$, the last on the finer grid), '
    'placing the annealed five-replica point\nat '
    '$p_c^{(5)}\\approx0.47$--$0.48$.',
    'the gap-minimum locator is stable across the ladder ($0.48$, '
    '$0.47$, $0.465$ at\n$L=4,6,8$, the last on the finer grid); the '
    'sequence is monotone\ndecreasing, no size extrapolation is '
    'applied at $n=5$ (the $n=3$ and\n$n=4$ points state theirs), and '
    'the quoted $p_c^{(5)}\\approx0.47$--$0.48$ is\naccordingly a '
    'plausibility range over the locator trend rather than a\n'
    'derived interval---an extrapolated value would sit at or below '
    'the last\nlocator $0.465$, the firm constraint being '
    '$p_c^{(5)}>p_c^{(4)}\\approx0.383$.',
    'B1 body p_c5 plausibility range')

# --- (1) body: two-size register ------------------------------------------
rep(
    'The $q=n$-Potts first-order prediction is therefore '
    '\\emph{confirmed} at',
    'The $q=n$-Potts first-order prediction is therefore '
    '\\emph{supported} at',
    'B2 body confirmed->supported')

# --- (2) body: the registered conditional ----------------------------------
rep(
    'they are the quantities a finite-size extraction of the '
    'interface tension would converge to if the asymptotic regime '
    'were reached.',
    'they are the quantities a finite-size extraction of the '
    'interface tension would converge to if the asymptotic regime '
    'were reached.  The test is therefore registered with its '
    'completion rather than declared finished: if the $n=5$ closing '
    'is genuinely exponential, the fourth size ($L=10$) will show '
    '$\\sigma_{\\rm eff}$ stabilizing at a positive interface '
    'tension, and if the asymptotic is a slowly decaying power law, '
    '$\\sigma_{\\rm eff}$ will continue to decay; the current data '
    'cannot distinguish these outcomes, and the registered '
    'conditional---not a performed discrimination---is the claim.',
    'B3 body registered conditional')

# --- (1) discussion verbs ----------------------------------------------------
rep(
    'the size-ladder confirmation of the first-order prediction is '
    'delivered in Sec.~\\ref{sec:n4n5} (Table~\\ref{tab:n5twosize}), '
    'the $q=n$-Potts conjecture being confirmed at the three-size '
    'level for $n=5$',
    'the size-ladder directional evidence for the first-order '
    'prediction is delivered in Sec.~\\ref{sec:n4n5} '
    '(Table~\\ref{tab:n5twosize}), the $q=n$-Potts conjecture being '
    'supported directionally at the three-size level for $n=5$',
    'D1 discussion verbs')

# --- (6a) Sec VII: approach the primitive level -------------------------------
rep(
    'The replica ladder then measures how the derived objects '
    'approach the primitive level: the annealed points recede '
    'monotonically from the quenched benchmark '
    '($0.2338\\to0.305(3)\\to0.383\\to0.47$ against $0.1597(8)$),',
    'The replica ladder then measures the distance of the derived '
    'family from the quenched benchmark: the annealed points recede '
    'monotonically ($0.2338\\to0.305(3)\\to0.383\\to0.47$ against '
    '$0.1597(8)$),',
    'M3 Sec VII primitive level -> display-level statement')

# --- (6b) Sec VII: restore mass-less --------------------------------------------
rep(
    'self-existent, timeless, spaceless, unchanging, complete, '
    'non-dual, without relations, parts, defects, or lack;',
    'self-existent, timeless, spaceless, massless, unchanging, '
    'complete, non-dual, without relations, parts, defects, or lack;',
    'M1 Sec VII restore mass-less')

# --- (1)+(2) conclusion: verbs + conditional -------------------------------------
rep(
    'which saturates on the continuous $n=3$ envelope ($6.53$ at '
    '$L=8$), falls to $3.84$ at $n=5$.',
    'which converges toward the continuous $n=3$ envelope ($6.53$ at '
    '$L=8$, $6.21$ at $L=10$), falls to $3.84$ at $n=5$ at the '
    'matched size.',
    'C1 conclusion saturates->converges')

rep(
    'Two sizes alone cannot separate exponential from power-law '
    'closing; the three-size ladder does.',
    'Two sizes alone cannot separate exponential from power-law '
    'closing, and three sizes do not yet do so either: what the '
    'ladder delivers is directional---every matched-size rate '
    'super-continuous and $n$-monotone---and the separation is '
    'registered as a prediction rather than claimed as performed---if '
    'the $n=5$ closing is genuinely exponential, the fourth size '
    '($L=10$) will show the effective closing rate stabilizing at a '
    'positive interface tension, and if it is a slowly decaying power '
    'law, that rate will continue to decay.',
    'C2 conclusion three-size ladder does -> directional + conditional')

rep(
    'effective interface-tension and power-law rates that separate '
    'the continuous, marginal and first-order behaviours at every '
    'matched interval.',
    'effective interface-tension and power-law rates ordered '
    'consistently with the continuous, marginal and first-order '
    'behaviours at every matched interval.',
    'C3 conclusion rates separate->ordered')

# --- (5) conclusion: L=8 verification gap -----------------------------------------
rep(
    'bounded by the cross-route agreement above and, at the decisive '
    '$n=5$ points, by float64 spot-checks on the float32 sweep '
    'validated to $4.3\\times10^{-6}$.',
    'bounded by the cross-route agreement above and, at the decisive '
    '$n=5$ points, by float64 spot-checks on the float32 sweep '
    'validated to $4.3\\times10^{-6}$.  One gap in the chain is '
    'stated plainly: the $L=8$, $n=5$ block itself has no '
    'independent-method check at its own size---its validations are '
    'the assembler\'s agreement with the deposited $L=4$ spectrum, '
    'the $L=6$ blocks\' agreement with unrestricted '
    'colour-restricted Arnoldi solves, and the float64 spot-checks, '
    'all at smaller sizes or internal to the block route---and an '
    'independent method at $L=8$ itself, for instance a randomized '
    'lower-bound rank estimate at the decisive $p$\'s, would close '
    'it.',
    'C4 conclusion L=8 verification gap')

# --- (3) conclusion: locator plausibility range -------------------------------------
rep(
    '$0.4797$; locator sequence $0.48/0.47/0.465$ over $L=4,6,8$); '
    'the $d=3$\nladder through $L=8$ reads',
    '$0.4797$; locator sequence $0.48/0.47/0.465$ over '
    '$L=4,6,8$---monotone\ndecreasing, so the '
    '$p_c^{(5)}\\approx0.47$--$0.48$ bracket is a\nplausibility range '
    'over the sequence, not an extrapolated\ninterval); the $d=3$'
    '\nladder through $L=8$ reads',
    'C5 conclusion locator plausibility range')

# --- (7) Sec VII: the modal-character paragraph ---------------------------------------
MODAL_PARA = (
    "\\emph{The modal character of the results.}  Read as results, "
    "the paper's statements divide by their relation to necessity, "
    "and the division can be stated in the paper's own terms.  Some "
    "are necessitated by the grammar of the structures that carry "
    "them: the no-freezing theorem (Theorem~\\ref{thm:nofreeze}), the "
    "complexity trichotomy (Remark~\\ref{rem:trichotomy}), the exact "
    "rank of the compressed operator (Theorem~\\ref{thm:rank}), and "
    "the exact closure of $\\Lambda(2)$ through the conjugation "
    "$3$-design (Proposition~\\ref{prop:z3closure}) hold for every "
    "structure of their kind; they are necessities of the "
    "structures, not contingencies of this realization.  Some are "
    "exclusions: the information-theoretic no-go "
    "(Theorem~\\ref{thm:no-go}) excludes the symmetric, unconditioned "
    "data from determining the Born-weighted entropy; the marginal "
    "$q=4$ log corrections exclude clean scaling at the accessible "
    "sizes; and the $n=5$ size ladder excludes the continuous "
    "baseline at the matched sizes themselves---an exclusion the "
    "registered $L=10$ conditional of Sec.~\\ref{sec:n4n5} is "
    "designed to extend or break.  Some are relations: the "
    "annealed--quenched separation, the Born-versus-symmetric "
    "separations of Sec.~\\ref{sec:born}, and the self-averaging "
    "criterion (Proposition~\\ref{prop:replica-int}) each link two "
    "descriptions of the same record statistics exactly.  And some "
    "are contingent: the numerical values---the annealed critical "
    "points, the closing rates, the measured SCGFs---and the "
    "specific Potts classes are facts of this display, necessitated "
    "by no grammar and carrying no claim beyond themselves.  The "
    "classification is a reading of the results' own modal "
    "character: it claims no generative power for any structure over "
    "the results, offers none of them as evidence for anything "
    "outside themselves, maps no attribute of the Absolute onto any "
    "of them, and leaves the standing metaphysics exactly where the "
    "first paragraph placed it."
)

rep(
    "not a participation in the Absolute's self-identity.\n\n"
    "\\emph{Reconciliation.}",
    "not a participation in the Absolute's self-identity.\n\n"
    + MODAL_PARA + "\n\n\\emph{Reconciliation.}",
    'INS Sec VII modal-character paragraph')

print(f'applied {len(EDITS)} designed edits: {EDITS}')

# =====================================================================
# post-edit invariants
# =====================================================================
tvis = '\n'.join(l for l in ms.splitlines()
                 if not l.lstrip().startswith('%'))

# (a) the over-claim verbs are gone
GONE = [
    'confirms the first-order prediction',
    'the three-size confirmation',
    'the three-size ladder does',
    'saturates on the continuous',
    'approach the primitive level',
    'rates that separate the continuous, marginal and first-order',
    'that separate the continuous, marginal and first-order',
    'is therefore \\emph{confirmed}',
]
hits = [t for t in GONE if t in tvis]
assert not hits, f'over-claim verbs still present: {hits}'
print('over-claim verb scan PASS (all aligned)')

# (b) the new statements are present, exactly as designed
for tok, n in {
        'massless': 1,
        'ordered consistently with': 2,
        'plausibility range': 2,
        'registered conditional': 2,
        'stabilizing at a positive interface tension': 3,
        'first three-size evidence in the first-order direction': 1,
        'the directional three-size evidence': 1,
        'is therefore \\emph{supported} at': 1,
        'supported directionally at the three-size level': 1,
        'converges toward the continuous $n=3$ envelope': 1,
        '($6.53$ at $L=8$, $6.21$ at $L=10$)': 1,
        'falls to $3.84$ at $n=5$ at the matched size': 1,
        'The modal character of the results': 1,
        'necessitated by no grammar': 1,
        'no generative power for any structure over the results': 1,
        'maps no attribute of the Absolute onto any of them': 1,
        'classifies the paper\'s results by their relation to '
        'necessity': 1,
        'the distance of the derived family from the quenched '
        'benchmark': 1,
        'no independent-method check at its own size': 1,
        'randomized lower-bound rank estimate': 1,
        'Relative to that reference': 1,
        'the registered conditional---not a performed '
        'discrimination---is the claim': 1,
        'registered as a prediction rather than claimed as '
        'performed': 1,
}.items():
    got = tvis.count(tok)
    assert got == n, f'new statement {tok!r}: {got} != {n}'
print('new-statement presence PASS')

# (c) theorem/equation references added by this pass
for tok in ['thm:fixed-algebra', 'thm:strobe', 'eq:leaknorm', 'eq:Wpn',
            'thm:nofreeze', 'rem:trichotomy', 'thm:rank',
            'prop:z3closure', 'sec:born', 'prop:replica-int']:
    got, want = ms.count(tok), MS.count(tok) + 1
    assert got == want, f'ref count {tok!r}: {got} != {want}'
print('added-reference count PASS')

# (d) untouched anchors carry (same count as v31)
for tok in ['\\url{https://mikeaa2020.github.io/quantum-circuits/'
            'web-simulation/}',
            'preprints.org', 'tab:n5twosize', 'tab:closingrates',
            'eq:collision', 'prop:houtappel', 'thm:record-mf',
            'prop:bivariate', 'eq:collision', 'app:rank3',
            'app:numerics', 'DOI to be assigned prior to submission',
            'release\\_checksums.sha256', 'certificate\\_sha256.txt',
            '3{,}865', '0.0226(2)', '0.1597(8)', '1.6\\times10^{-14}',
            '4.3\\times10^{-6}', '$0.48/0.47/0.465$']:
    got, want = ms.count(tok), MS.count(tok)
    assert got == want, f'anchor {tok!r}: {got} != {want}'
assert ms.count('\\section{') == MS.count('\\section{')
assert ms.count('\\label{sec:interpretation}') == 1
assert 'figshare' not in ms
print('anchor carry PASS (data-availability URL, deposits, numbers)')

# (e) Sec VII category-error regression scan (v31 forbidden list)
FORBIDDEN_V31 = [
    'timeless characterization', 'immutable law', 'the appearance-stream',
    'view from nowhere', 'the same boundary that the metaphysics draws',
    'The parallel with the metaphysics', 'resonance with the attribute',
    'The primitive Born law and self-existence', 'The one and the many',
    'one appearing as many', 'Virtuous circularity, honored exactly',
    'circularity thesis', 'methodological echo', 'self-appearance',
    'conditions of coincidence', 'its reconciliation conditions',
    'projection modes', 'epistemic access to one absolute object',
    'absolute object', 'many-ness',
]
hits = [t for t in FORBIDDEN_V31 if t in tvis]
assert not hits, f'v31 forbidden tokens regressed: {hits}'
print('category-error regression scan PASS (Sec VII v31 state intact)')

# (f) the metaphysics statement stays non-load-bearing and faithful
for tok, n in {
        'No theorem, computation, or number in this paper depends on '
        'it': 1,
        'open to revision by evidence, not by preference': 1,
        'mass-less': 0,
        'self-existent, timeless, spaceless, massless, unchanging, '
        'complete, non-dual, without relations, parts, defects, or '
        'lack': 1,
        'simplicity (no composition into parts), self-existence '
        '(no dependence), non-duality (no standing over against '
        'another), necessity (no contingency wanting a ground), '
        'immutability (no change requiring potential and lack), '
        'timelessness (no succession), spacelessness (no extension '
        'implying parts and distinction), completeness (no lack in '
        'its own nature)': 1,
        'maya': 1,
        'neither real nor unreal': 1,
}.items():
    got = tvis.count(tok)
    assert got == n, f'metaphysics statement {tok[:50]!r}: {got} != {n}'
print('metaphysics fidelity + non-load-bearing PASS (massless restored)')

# (g) structure
assert ms.count('\\emph{Reconciliation.}') == 1
assert ms.count('\\emph{The exactness program.}') == 1
sec_start = ms.index('\\section{Interpretive status of the record '
                     'formalism}')
sec_end = ms.index('\\section{Conclusion}')
sec = ms[sec_start:sec_end]
for head in ['\\emph{The standing metaphysics.}',
             '\\emph{What the metaphysics does to the interpretations.}',
             '\\emph{Division in the appearance.}',
             '\\emph{The primitive Born rule.}',
             '\\emph{Self-averaging: the ensemble and the single '
             'stream.}',
             '\\emph{The exactness program.}',
             '\\emph{The modal character of the results.}',
             '\\emph{Reconciliation.}']:
    assert sec.count(head) == 1, f'Sec VII head {head!r}'
print('Sec VII structure PASS (8 paragraph heads, modal character '
      'between exactness program and reconciliation)')

# =====================================================================
# MANUSCRIPT: line-multiset + no-content-loss audit
# =====================================================================


def visible(text):
    return [l for l in text.splitlines()
            if l.strip() and not l.lstrip().startswith('%')]


vo, vn = visible(MS), visible(ms)
c31, c32 = Counter(vo), Counter(vn)

removed = c31 - c32
added = c32 - c31

DESIGNED_REMOVED_MARKERS = [
    'and confirms the first-order prediction',                    # A1
    'with the scaled gap falling below the continuous envelope '
    'and dual',                                                  # A2
    'provides the first three-size discrimination',               # I1
    'with the three-size confirmation',                           # S1
    'states the standing metaphysics, locates the readings',      # S2
    'we use that name for the span',                              # R1
    'the last on the finer grid), placing the annealed '
    'five-replica point',                                        # B1b
    'at $p_c^{(5)}\\approx0.47$--$0.48$.',                        # B1c
    'The $q=n$-Potts first-order prediction is therefore',        # B2
    'they are the quantities a finite-size extraction',           # B3
    'the size-ladder confirmation of the first-order '
    'prediction',                                                # D1
    'self-existent, timeless, spaceless, unchanging',             # M1
    'The replica ladder then measures how the derived '
    'objects',                                                   # M3
    'which saturates on the continuous',                          # C1
    'Two sizes alone cannot separate exponential from power-law '
    'closing; the three-size ladder does.',                      # C2
    'effective interface-tension and power-law rates that '
    'separate',                                                  # C3
    'bounded by the cross-route agreement above',                 # C4
    'locator sequence $0.48/0.47/0.465$ over $L=4,6,8$); the '
    '$d=3$',                                                     # C5
]
designed_removed = set()
for m in DESIGNED_REMOVED_MARKERS:
    hits_ = [l for l in removed if m in l]
    assert len(hits_) == 1, \
        f'designed-removed marker not matched once: {m[:60]!r}'
    designed_removed.add(hits_[0])
lost = {l: n for l, n in removed.items() if l not in designed_removed}
assert not lost, f'UNDESIGNED CONTENT LOSS: {list(lost)[:3]}'

DESIGNED_ADDED_MARKERS = [
    'and supports, at the three-size level,',
    'a directional trend, with the registered conditional',
    'provides the first three-size evidence in the first-order',
    'with the directional three-size evidence',
    'classifies the paper\'s results by their relation to '
    'necessity',
    'Relative to that reference, the present analysis supplies',
    'the sequence is monotone',
    'decreasing, no size extrapolation is applied at $n=5$',
    'the quoted $p_c^{(5)}\\approx0.47$--$0.48$ is',
    'accordingly a plausibility range over the locator trend',
    'derived interval---an extrapolated value would sit at or '
    'below the last',
    'constraint being $p_c^{(5)}>p_c^{(4)}\\approx0.383$.',
    'The $q=n$-Potts first-order prediction is therefore '
    '\\emph{supported} at',
    'locator sequence $0.48/0.47/0.465$ over '
    '$L=4,6,8$---monotone',
    'The test is therefore registered with its completion',
    'the size-ladder directional evidence for the first-order',
    'self-existent, timeless, spaceless, massless, unchanging',
    'The replica ladder then measures the distance of the derived',
    'which converges toward the continuous $n=3$ envelope',
    'Two sizes alone cannot separate exponential from power-law '
    'closing, and three sizes do not yet do so either',
    'effective interface-tension and power-law rates ordered',
    'One gap in the chain is stated plainly',
    'independent method at $L=8$ itself',
    'decreasing, so the $p_c^{(5)}\\approx0.47$--$0.48$ bracket '
    'is a',
    'plausibility range over the sequence, not an extrapolated',
    'interval); the $d=3$',
    'The modal character of the results',                        # INS
]
designed_added = set()
for m in DESIGNED_ADDED_MARKERS:
    hits_ = [l for l in added if m in l]
    assert len(hits_) == 1, \
        f'designed-added marker not matched once: {m[:60]!r}'
    designed_added.add(hits_[0])
extra = {l: n for l, n in added.items() if l not in designed_added}
assert not extra, f'UNDESIGNED ADDED LINES: {list(extra)[:3]}'

# positional diff: every changed/inserted position is designed
sm = difflib.SequenceMatcher(a=vo, b=vn, autojunk=False)
changed_old, changed_new = 0, 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    for l in vo[i1:i2]:
        assert l in designed_removed, \
            f'unexpected positional removal: {l[:80]!r}'
        changed_old += 1
    for l in vn[j1:j2]:
        assert l in designed_added, \
            f'unexpected positional addition: {l[:80]!r}'
        changed_new += 1
print(f'manuscript line-multiset audit PASS: {sum(c31.values())} '
      f'visible v31 lines -> {sum(c32.values())} visible v32 lines; '
      f'{changed_old} designed lines replaced, '
      f'{changed_new} designed lines entered '
      f'(+{sum(c32.values()) - sum(c31.values())} net), '
      'zero undesigned loss')
assert sum(c32.values()) == sum(c31.values()) + 8, \
    (sum(c31.values()), sum(c32.values()))

# =====================================================================
# final submission-cleanliness scan (house protocol)
# =====================================================================
FORBIDDEN = ['TODO', 'FIXME', 'XXX', 'placeholder', 'absolute.txt',
             'campaign', 'queue', 'driver', 'watch ', 'rollback', 'cron',
             'worklog', 'OOM', 'sandbox', 'diary', 'chat ', 'changelog',
             'figshare']
hits = [t for t in FORBIDDEN if t in tvis]
assert not hits, f'manuscript forbidden tokens: {hits}'
print('forbidden-token scan PASS (manuscript)')

assert (V / 'manuscript_revised_v31.tex').read_text() == MS, \
    'v31 was modified!'
print('v31 untouched (byte-identical re-read) PASS')

(V / 'manuscript_revised_v32.tex').write_text(ms)
print(f'written: manuscript_revised_v32.tex ({len(ms)} chars; '
      f'v31 was {len(MS)} chars)')
print(f'edits applied ({len(EDITS)}):')
for e in EDITS:
    print(f'  - {e}')
print('PATCH OK')
