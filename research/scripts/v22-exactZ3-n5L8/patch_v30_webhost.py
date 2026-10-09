#!/usr/bin/env python3
r"""patch_v30_webhost.py -- build manuscript_revised_v30.tex from the
canonical v29 file (manuscript_revised_v29.tex, preserved unmodified
alongside its predecessors).  Scope (author-directed web-simulation
hosting pass, data availability):

(1) DATA AVAILABILITY -> HOSTED URL.  The author asked that the data
    availability statement GIVE THE URL of the web simulation, hosted
    on GitHub, instead of stating that the Supplementary Material
    includes it.  The v29 sentence

        "The Supplementary Material includes the web simulation of the
        monitored circuits: an interactive stabilizer-tableau
        simulator of the Clifford dynamics of Appendix~\ref{app:numerics},
        with the finite-size-scaling benchmark, the annealed replica
        chain, and the record SCGF analyses of the paper presented in
        interactive form."

    becomes

        "The web simulation of the monitored circuits---an interactive
        stabilizer-tableau simulator of the Clifford dynamics of
        Appendix~\ref{app:numerics}, with the finite-size-scaling
        benchmark, the annealed replica chain, and the record SCGF
        analyses of the paper presented in interactive form---is hosted
        at \url{https://mikeaa2020.github.io/quantum-circuits/web-simulation/}."

    Every clause of the description is preserved verbatim; only the
    framing changes (supplementary inclusion -> hosted address).  The
    deposited-artifact list and the preprints.org sentence ahead of it
    are untouched.  hyperref is loaded, so \url typesets, breaks and
    hyperlinks the address.

The web simulation itself is committed to the repository at
web-simulation/index.html (ONE self-contained offline HTML file with
the full interactive companion, plus web_simulation.zip for
archival/supplementary upload); the address above serves that folder
once GitHub Pages is enabled for the repository (branch source:
main / root -- .nojekyll markers already committed).

No other change.  The companion supplement (supplement_v10.tex)
carries no web-simulation or deposit-host reference, so it is carried
forward unchanged (ledger v17 re-hashes it).
"""
from collections import Counter
from pathlib import Path

V = Path(__file__).resolve().parent.parent.parent / 'versions'

MS = (V / 'manuscript_revised_v29.tex').read_text()

# =====================================================================
# MANUSCRIPT: header
# =====================================================================
i_dc = MS.index('\\documentclass')
NEW_HEADER = """% manuscript_revised_v30.tex -- web-simulation hosting pass
% (data availability gives the URL; patch_v30_webhost.py) of
% manuscript_revised_v29.tex, which is preserved unmodified alongside
% its predecessors.  Scope of this pass, in full:
% (1) the data availability statement now gives the address of the web
%     simulation, hosted on GitHub, replacing the v29 statement that
%     the Supplementary Material includes it; the description clauses
%     (interactive stabilizer-tableau simulator of the Clifford
%     dynamics, finite-size-scaling benchmark, annealed replica chain,
%     record SCGF analyses, presented in interactive form) are carried
%     verbatim -- asserted in the patch script; the deposited-artifact
%     list and the preprints.org DOI sentence are untouched;
% (2) nothing else: the companion supplement_v10.tex carries no
%     web-simulation or deposit-host reference and passes forward
%     unchanged (ledger v17 re-hashes it).
% The web simulation referenced: web-simulation/index.html in this
% repository -- one self-contained offline HTML file (the interactive
% companion of the paper), with web_simulation.zip alongside it for
% archival upload; the address serves the folder via GitHub Pages
% (branch source main / root, .nojekyll committed).
% Change log: changelog_v30.md.
% Provenance ledger: certificate_sha256_v17.txt.
"""
ms = NEW_HEADER + MS[i_dc:]

# =====================================================================
# MANUSCRIPT: the single edit (data availability -> hosted URL)
# =====================================================================
oldDA = ("The Supplementary Material includes the web simulation of "
         "the monitored circuits: an interactive stabilizer-tableau "
         "simulator of the Clifford dynamics of "
         "Appendix~\\ref{app:numerics}, with the finite-size-scaling "
         "benchmark, the annealed replica chain, and the record SCGF "
         "analyses of the paper presented in interactive form.")
newDA = ("The web simulation of the monitored circuits---an "
         "interactive stabilizer-tableau simulator of the Clifford "
         "dynamics of Appendix~\\ref{app:numerics}, with the "
         "finite-size-scaling benchmark, the annealed replica chain, "
         "and the record SCGF analyses of the paper presented in "
         "interactive form---is hosted at "
         "\\url{https://mikeaa2020.github.io/quantum-circuits/"
         "web-simulation/}.")
assert ms.count(oldDA) == 1, 'old data-availability sentence not unique'
ms = ms.replace(oldDA, newDA)

# post-edit invariants
URL = 'https://mikeaa2020.github.io/quantum-circuits/web-simulation/'
assert 'Supplementary Material includes the web simulation' not in ms
assert ms.count('\\url{' + URL + '}') == 1
assert 'figshare' not in ms
assert 'preprints.org' in ms and 'web simulation' in ms
# the deposited-artifact list is preserved verbatim:
for keep in ('release\\_checksums.sha256', 'certificate\\_sha256.txt',
             'npz', 'app:rank3', 'app:numerics',
             'DOI to be assigned prior to submission'):
    assert keep in ms, f'deposited-artifact anchor lost: {keep!r}'
# every description clause survives verbatim inside the new sentence:
for clause in ('an interactive stabilizer-tableau simulator of the '
               'Clifford dynamics of',
               'with the finite-size-scaling benchmark, the annealed '
               'replica chain, and the record SCGF analyses of the '
               'paper presented in interactive form'):
    assert ms.count(clause) == 1, f'clause not carried verbatim: {clause[:50]!r}'

# =====================================================================
# MANUSCRIPT: line-multiset no-content-loss audit (house protocol).
# =====================================================================
EDITED_MARKERS = [
    'The Supplementary Material includes the web simulation',  # the DA line
]


def visible(text):
    return [l for l in text.splitlines()
            if l.strip() and not l.lstrip().startswith('%')]


c29, c30 = Counter(visible(MS)), Counter(visible(ms))
removed = Counter()
for m in EDITED_MARKERS:
    hits = [l for l in c29 if m in l]
    assert len(hits) == 1, f'edited marker not unique: {m[:60]!r}'
    removed[hits[0]] = c29[hits[0]]
lost = {l: n for l, n in (c29 - removed).items() if c30[l] < n}
assert not lost, f'CONTENT LOSS: {list(lost)[:3]}'
print(f"manuscript line-multiset audit PASS: {sum(c29.values())} visible "
      f"v29 lines, {sum(removed.values())} deliberately edited, "
      f"{sum(c30.values())} visible v30 lines")

# =====================================================================
# final submission-cleanliness scan (house protocol)
# =====================================================================
FORBIDDEN = ['TODO', 'FIXME', 'XXX', 'placeholder', 'absolute.txt',
             'campaign', 'queue', 'driver', 'watch ', 'rollback', 'cron',
             'worklog', 'OOM', 'sandbox', 'diary', 'chat ', 'changelog',
             'figshare']
tvis = "\n".join(l for l in ms.splitlines()
                 if not l.lstrip().startswith('%'))
hits = [t for t in FORBIDDEN if t in tvis]
assert not hits, f'manuscript forbidden tokens: {hits}'
print("forbidden-token scan PASS (manuscript)")

(V / 'manuscript_revised_v30.tex').write_text(ms)
print(f"written: manuscript_revised_v30.tex ({len(ms)} chars; "
      f"v29 was {len(MS)} chars)")
print("PATCH OK")
