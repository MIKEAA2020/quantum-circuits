#!/usr/bin/env python3
r"""patch_v31_appearance_terms.py -- build manuscript_revised_v31.tex
from the canonical v30 file (manuscript_revised_v30.tex, preserved
unmodified alongside its predecessors).  Scope (author-directed
appearance-terms pass, session 2026-10-10):

The author diagnosed a category error in Sec. VII (sec:interpretation).
The v28 pass that aligned the section to the author's standing
metaphysics (absolute.txt) correctly relocated the readings of quantum
mechanics to the level of appearance, but it kept four
analogies/identifications that map ATTRIBUTES OF THE ABSOLUTE onto
APPEARANCE-LEVEL features of the formalism, plus the general pattern
of treating appearance as a mirror of the Absolute.  In the author's
framework appearance is the Absolute's display, not a copy of it:
neither real nor unreal, neither identical with nor different from the
Absolute (maya); its structure is its own (division, relation, time,
change); nothing in it echoes, honors, or mirrors the ground.
Directive: drop the analogies and identifications, keep the
metaphysics non-load-bearing, describe appearance in its own terms.

(1) Sec. VII paragraph 2 (relocation of the readings): kept; the
    mirror-pattern tail removed ("the appearance-stream in exact
    mathematical form ... immutable law ... as timeless
    characterizations of the temporal stream") and replaced by the
    author's characterization of appearance (the Absolute's display:
    not a copy of it and not a mirror of it -- maya: neither real nor
    unreal, neither identical with nor different from the Absolute;
    its structure is its own: division, relation, time, change) and an
    explicit statement that no feature of the display is taken to
    reflect an attribute of the Absolute.  The Born record is stated
    in the display's own terms.
(2) Sec. VII paragraph 3 (was "Non-eliminable division at the level
    of appearance", which read thm:no-go as an echo of the Absolute's
    undividedness -- the author's diagnosis: inverted, division is a
    feature of appearance): now "Division in the appearance."  The
    theorems state how division functions in the appearance's own
    structure; no claim about the Absolute, whose undividedness the
    display neither echoes nor mirrors.
(3) Sec. VII paragraph 4 (was "The primitive Born law and
    self-existence"): now "The primitive Born rule."  The
    self-existence analogy sentence deleted; every physics statement
    carried verbatim.
(4) Sec. VII paragraph 5 (was "The one and the many."): now
    "Self-averaging: the ensemble and the single stream."  The
    one/many framing and the "one appearing as many" mapping deleted;
    self-averaging is an exact statistical property of the record
    statistics; the readings' relocated places, all theorem
    references, numbers, and citations carried verbatim.
(5) Sec. VII paragraph 6 (was "Virtuous circularity, honored
    exactly."): now "The exactness program."  The identification of
    the program with the Absolute's virtuous circularity deleted; the
    commitments stated in their own terms, "not a participation in
    the Absolute's self-identity".
(6) Sec. VII paragraph 7 (Reconciliation): "the grammar of the
    Absolute's self-appearance" and "the conditions of coincidence"
    reworded; an explicit closing non-claim added ("nothing in the
    work asserts that the appearance mirrors, echoes, or honors the
    Absolute").
(7) Paragraph 1 (the statement of the standing metaphysics) carried
    VERBATIM.  The intro-spine entry for Sec. VII updated to match
    ("... locates the readings of quantum mechanics at the level of
    appearance, and draws no structural parallel between the display
    and the Absolute").

No other change.  Companion supplement_v10.tex carries no metaphysics
content and passes forward unchanged (ledger v18 re-hashes it).
"""
from collections import Counter
from pathlib import Path

V = Path(__file__).resolve().parent.parent.parent / 'versions'

MS = (V / 'manuscript_revised_v30.tex').read_text()

# =====================================================================
# MANUSCRIPT: header
# =====================================================================
i_dc = MS.index('\\documentclass')
NEW_HEADER = """% manuscript_revised_v31.tex -- appearance-terms pass
% (patch_v31_appearance_terms.py) of manuscript_revised_v30.tex,
% which is preserved unmodified alongside its predecessors.  Scope of
% this pass, in full (author-directed, session 2026-10-10):
% (1) Sec. VII (sec:interpretation): remove the four
%     analogies/identifications that map attributes of the Absolute
%     onto appearance-level features of the formalism (category
%     errors diagnosed by the author): the self-existence analogy for
%     the primitive Born rule; the no-go theorem read as an echo of
%     the Absolute's undividedness (inverted -- division is a feature
%     of appearance); self-averaging framed as a one/many coincidence
%     condition; the exactness program identified with virtuous
%     circularity.  Appearance is described in its own terms: the
%     display is not a copy of the Absolute and not a mirror of it
%     (maya: neither real nor unreal, neither identical with nor
%     different from the Absolute); its structure is its own
%     (division, relation, time, change); no feature of the display
%     is taken to reflect an attribute of the Absolute.
% (2) The first paragraph of Sec. VII (the statement of the standing
%     metaphysics) is carried verbatim; the relocation of the
%     readings to the level of appearance is unchanged; every
%     theorem reference, number, and citation of the section
%     survives (asserted below).
% (3) Intro spine entry for Sec. VII updated to match.
% (4) Nothing else; the metaphysics remains non-load-bearing.
% Change log: changelog_v31.md.
% Provenance ledger: certificate_sha256_v18.txt.
"""
ms = NEW_HEADER + MS[i_dc:]

# =====================================================================
# MANUSCRIPT: Sec. VII -- the six rewritten paragraphs (para 1 is
# extracted from v30 and carried verbatim; see below).
# =====================================================================
P2 = r"""\emph{What the metaphysics does to the interpretations.}  It relocates their referents.  Every interpretation of quantum mechanics posits structure that the metaphysics assigns to appearance rather than to the Absolute: the classical--quantum interface of the operational reading; the branching universal wavefunction of Everett~\cite{Everett1957}; the definite configurations and guiding field of de~Broglie--Bohm~\cite{Bohm1952}; the dynamical collapse process of Ghirardi--Rimini--Weber~\cite{GRW1986}; the fundamental agent plurality of QBism~\cite{Fuchs2014}; the system--environment relations of einselection~\cite{Zurek2003}.  Under the metaphysics none of these is a rival ultimate ontology: each is a partial grammar of the appearance, and its empirical content is untouched.  That a serious reading of quantum mechanics can place its central structure outside the objectifiable has ample precedent~\cite{dEspagnat1995}; what the metaphysics adds is the strict non-duality of what remains.  The appearance itself, in the metaphysics, is the Absolute's display: not a copy of it and not a mirror of it---\emph{maya}: neither real nor unreal, neither identical with nor different from the Absolute---and its structure is its own: division, relation, time, change.  No feature of the display is required to reflect an attribute of the Absolute, and none is taken to.  What the appearance's exact grammar is, for one class of models, is a physics question, and it is the question this paper answers for monitored circuits: the Born record with its large deviations, stated in the display's own terms---succession (the record in time), resolution (the outcome division), and law (the SCGF, the rate function, and the no-freezing dichotomy of Remark~\ref{rem:dichotomy})."""

P3 = r"""\emph{Division in the appearance.}  The metaphysics assigns division, multiplicity, and relation to the appearance, and the paper's first separation is an exact statement of how division functions there.  Theorem~\ref{thm:no-go} proves that the symmetric, unconditioned data do not determine the Born-weighted entropy, and Proposition~\ref{prop:bivariate} proves that record-resolved data do: the undivided summary of the record process is exactly insufficient, and conditioning on the record is not eliminable from the statistics of the display.  This is a statement about the appearance's own structure; it carries no claim about the Absolute, whose undividedness the display neither echoes nor mirrors."""

P4 = r"""\emph{The primitive Born rule.}  In the formalism the Born rule is primitive, and Theorem~\ref{thm:no-go} is the precise statement of why it cannot be recovered from unconditioned data, while the Mellin derivative of Proposition~\ref{prop:replica-derivative} shows what the recovery does require---the asymmetric, record-resolved factor.  The replica ladder then measures how the derived objects approach the primitive level: the annealed points recede monotonically from the quenched benchmark ($0.2338\to0.305(3)\to0.383\to0.47$ against $0.1597(8)$), Proposition~\ref{prop:replica-int} identifies the tilted-variance profile as the exact bridge, and the $m\to\infty$ replica limit overshoots the quenched value to the extremal one---the appearance's summary statistics never silently become the stream they summarize."""

P5 = r"""\emph{Self-averaging: the ensemble and the single stream.}  The self-averaging criterion of Proposition~\ref{prop:replica-int} is the exact statistical condition under which the disorder-averaged description and the single-realization description of the record statistics coincide: where it holds, the difference between the two descriptions is surplus; where it fails, they differ by a measurable and irreducible gap, the $L$-independent $0.0226(2)$ nats-per-site Clifford disorder gap of Sec.~\ref{sec:clifforddisorder} being one measured instance.  On this exact stage the readings take their relocated places, each claiming only what the statistics support.  The Everett branches are the outcome decomposition---a structure of the display's grammar, not an ultimate multiplicity---and the annealed--quenched separation states that the totality's symmetric content does not determine the single stream.  The QBist agents are experience taken as many~\cite{Fuchs2014}, and self-averaging is the measurable condition under which agents holding different histories converge to the same probabilities.  The Bohmian configurations and the collapse process are surplus phenomenal structure~\cite{Bohm1952,GRW1986}: the record large deviations of Theorem~\ref{thm:record-mf} apply to them verbatim (Born typicality is the same stochastic law under another grammar), the no-freezing theorem (Theorem~\ref{thm:nofreeze}) bounds the freezing they can exhibit, and the exact anchors---the Clifford record-count closure of Eq.~\eqref{eq:collision}, the closed-form $p=1$ annealed record SCGF, the Ising critical point of Proposition~\ref{prop:houtappel}---are the fixed benchmarks that such structure must reproduce or break.  Einselection~\cite{Zurek2003} receives its controlled laboratory: the measurement rate is the coupling, and the transition of Appendix~\ref{app:numerics} is the phase boundary between the volumetric and the logarithmic conditional-entropy regimes---the boundary of how much unresolved structure the appearance retains."""

P6 = r"""\emph{The exactness program.}  The program has methodological commitments, and they are stated here in their own terms.  The record process is estimated from records themselves: the sequential Monte Carlo machinery of Sec.~\ref{sec:smcnumerics} estimates the record law from record samples, with the finite-population contract stated, not hidden.  Every exact number is regenerable from the deposited artifact, every certificate is an integer statement, and the computational process delivers what does not depend on the process.  The primitive interface---the Born rule---is declared as primitive rather than disguised as derived.  These are commitments of practice---checkability, regenerability, declared primitives---not a participation in the Absolute's self-identity."""

P7 = r"""\emph{Reconciliation.}  The work and the metaphysics do not compete.  The metaphysics locates the referent of the paper's exact structures at the level of appearance, and the paper describes that appearance, for monitored circuits, in exact form and in its own terms: the separations (annealed versus quenched, symmetric versus record-resolved, corner versus affine, BQP-estimable versus PP-hard), the exact conditions under which distinct descriptions of the record statistics coincide (self-averaging, record-resolved data), and the benchmarks (the anchor identities).  Nothing in this paper asserts an ultimate ontology; nothing in the metaphysics contradicts an exact phenomenal grammar; and nothing in the work asserts that the appearance mirrors, echoes, or honors the Absolute.  The readings, finally, are the partial grammars, and the theorems of this paper are the invariant structure they share.  The metaphysics frames the work; the theorems carry it; no theorem depends on the former, and no number in the paper would change under its revision."""

NEW_PARAS = [P2, P3, P4, P5, P6, P7]

# --- locate the section and carry para 1 verbatim -------------------
lines = ms.split('\n')
i_sec = [i for i, l in enumerate(lines)
         if l.startswith('\\section{Interpretive status of the record formalism}')]
assert len(i_sec) == 1, 'Sec VII header not unique'
i0 = i_sec[0]
i_con = [i for i, l in enumerate(lines) if l.startswith('\\section{Conclusion}')]
assert len(i_con) == 1, 'Conclusion header not unique'
i1 = i_con[0]
assert i0 < i1, 'section order'
block = lines[i0:i1]
# expected shape: sec(0) label(1) blank(2) p1(3) blank p2 ... blank p7(15) blank(16)
para_idx = [k for k, l in enumerate(block)
            if l.strip() and not l.startswith('\\section')
            and not l.startswith('\\label')]
assert para_idx == [3, 5, 7, 9, 11, 13, 15], f'unexpected block shape: {para_idx}'
assert block[1].strip() == '\\label{sec:interpretation}'
p1_old = block[3]
assert p1_old.startswith('\\emph{The standing metaphysics.}'), 'para 1 head'
OLD_HEADS = [
    '\\emph{What the metaphysics does to the interpretations.}',
    '\\emph{Non-eliminable division at the level of appearance.}',
    '\\emph{The primitive Born law and self-existence.}',
    '\\emph{The one and the many.}',
    '\\emph{Virtuous circularity, honored exactly.}',
    '\\emph{Reconciliation.}',
]
for k, head in zip(para_idx[1:], OLD_HEADS):
    assert block[k].startswith(head), f'old paragraph head mismatch: {head!r}'
old_paras = [block[k] for k in para_idx[1:]]

new_block = [block[0], block[1], block[2], p1_old]
for p in NEW_PARAS:
    new_block += ['', p]
new_block += ['']
assert len(new_block) == len(block) == 17, 'block length'
lines[i0:i1] = new_block
ms = '\n'.join(lines)

# --- the intro-spine entry ------------------------------------------
OLD_SPINE = (r'Sec.~\ref{sec:interpretation} states the standing '
             'metaphysics and its reconciliation conditions; '
             r'Sec.~\ref{sec:conclusion} concludes.')
NEW_SPINE = (r'Sec.~\ref{sec:interpretation} states the standing '
             'metaphysics, locates the readings of quantum mechanics '
             'at the level of appearance, and draws no structural '
             'parallel between the display and the Absolute; '
             r'Sec.~\ref{sec:conclusion} concludes.')
assert ms.count(OLD_SPINE) == 1, 'old spine fragment not unique'
ms = ms.replace(OLD_SPINE, NEW_SPINE)

# =====================================================================
# post-edit invariants
# =====================================================================
# (a) para 1 (the author's metaphysics statement) carried verbatim
assert ms.count(p1_old) == 1, 'para 1 not carried verbatim'

# (b) the six old paragraph lines are gone
for op in old_paras:
    assert op not in ms, 'old paragraph survived: %r' % op[:60]

# (c) required theorem/number/citation content of the new section
sec31 = '\n'.join(new_block)
REQUIRED_COUNTS = {
    'Everett1957': 1, 'Bohm1952': 2, 'GRW1986': 2, 'Fuchs2014': 2,
    'Zurek2003': 2, 'dEspagnat1995': 1,
    'thm:no-go': 2, 'prop:bivariate': 1, 'prop:replica-derivative': 1,
    'prop:replica-int': 2, 'thm:record-mf': 1, 'thm:nofreeze': 1,
    'prop:houtappel': 1, 'rem:dichotomy': 1, 'eq:collision': 1,
    'sec:smcnumerics': 1, 'sec:clifforddisorder': 1, 'app:numerics': 1,
    '0.0226(2)': 1, '0.1597(8)': 1,
    r'0.2338\to0.305(3)\to0.383\to0.47': 1,
    r'closed-form $p=1$ annealed record SCGF': 1,
}
for tok, n in REQUIRED_COUNTS.items():
    got = sec31.count(tok)
    assert got == n, f'required content {tok!r}: {got} != {n}'

# (d) the removed misapplications are gone (category-error phrases)
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
tvis = '\n'.join(l for l in ms.splitlines()
                 if not l.lstrip().startswith('%'))
hits = [t for t in FORBIDDEN_V31 if t in tvis]
assert not hits, f'v31 forbidden tokens: {hits}'
print('category-error phrase scan PASS (all removed)')

# (e) the new corrective statements are present, exactly once
for tok, n in {
        r'\emph{maya}': 1, 'neither real nor unreal': 1,
        'neither identical with nor different from the Absolute': 1,
        'not a copy of it and not a mirror of it': 1,
        'whose undividedness the display neither echoes nor mirrors': 1,
        'asserts that the appearance mirrors, echoes, or honors the Absolute': 1,
        "not a participation in the Absolute's self-identity": 1,
        'draws no structural parallel between the display and the Absolute': 1,
        'Division in the appearance': 1, 'The primitive Born rule': 1,
        'Self-averaging: the ensemble and the single stream': 1,
        'The exactness program': 1,
        'in the display\'s own terms': 1,
        'No feature of the display is required to reflect an attribute': 1,
        'a structure of the display\'s grammar, not an ultimate multiplicity': 1,
        'each claiming only what the statistics support': 1,
        'commitments of practice---checkability, regenerability, '
        'declared primitives': 1}.items():
    got = tvis.count(tok)
    assert got == n, f'new statement {tok!r}: {got} != {n}'
print('corrective-statement presence PASS')

# (f) structure unchanged
assert MS.count('\\section{') == ms.count('\\section{'), 'section count'
assert ms.count('\\label{sec:interpretation}') == 1
assert MS.count('\\label{sec:interpretation}') == 1

# (g) v30 anchors intact (data availability, deposit, numerics)
URL = 'https://mikeaa2020.github.io/quantum-circuits/web-simulation/'
assert ms.count('\\url{' + URL + '}') == 1
assert 'preprints.org' in ms and 'web simulation' in ms
assert 'figshare' not in ms
for keep in ('release\\_checksums.sha256', 'certificate\\_sha256.txt',
             'npz', 'app:rank3', 'app:numerics',
             'DOI to be assigned prior to submission'):
    assert keep in ms, f'anchor lost: {keep!r}'
print('v30 anchor carry PASS (data-availability URL, deposit list)')

# =====================================================================
# MANUSCRIPT: line-multiset + positional no-content-loss audit
# =====================================================================


def visible(text):
    return [l for l in text.splitlines()
            if l.strip() and not l.lstrip().startswith('%')]


EDITED_MARKERS = OLD_HEADS[:5] + [
    'The work and the metaphysics do not compete.',
    'states the standing metaphysics and its reconciliation conditions',
]

c30, c31 = Counter(visible(MS)), Counter(visible(ms))
removed = Counter()
for m in EDITED_MARKERS:
    hits_ = [l for l in c30 if m in l]
    assert len(hits_) == 1, f'edited marker not unique: {m[:60]!r}'
    removed[hits_[0]] = c30[hits_[0]]
lost = {l: n for l, n in (c30 - removed).items() if c31[l] < n}
assert not lost, f'CONTENT LOSS: {list(lost)[:3]}'
print(f"manuscript line-multiset audit PASS: {sum(c30.values())} visible "
      f"v30 lines, {sum(removed.values())} deliberately edited, "
      f"{sum(c31.values())} visible v31 lines")

vo, vn = visible(MS), visible(ms)
assert len(vo) == len(vn), 'visible line count changed'
d = [i for i in range(len(vo)) if vo[i] != vn[i]]
assert len(d) == 7, f'expected 7 edited visible lines, got {len(d)}'
for i in d:
    assert any(m in vo[i] for m in EDITED_MARKERS), \
        f'unexpected edited line: {vo[i][:80]!r}'
print('positional audit PASS: exactly 7 visible lines differ '
      '(6 Sec VII paragraphs + intro spine), all designed')

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

(V / 'manuscript_revised_v31.tex').write_text(ms)
print(f"written: manuscript_revised_v31.tex ({len(ms)} chars; "
      f"v30 was {len(MS)} chars)")
print("PATCH OK")
