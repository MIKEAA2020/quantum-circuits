#!/usr/bin/env python3
"""patch_v27_extL8.py -- build manuscript_revised_v27.tex + supplement_v9.tex
from the canonical v26 files (manuscript_revised_v26.tex + supplement_v8.tex,
both preserved unmodified).  Content: integration of the completed extension
campaign -- the d=3 L=8 rung (p=0.82/0.84/0.86, interior minimum 0.453 at
p=0.84, completing the d=3 three-size ladder) and the finer d=2 locator grid
at L=8 (p=0.455/0.465/0.475/0.485, minimum 0.4797 at p=0.465).  Main text:
the size-ladder table cell 0.481 -> 0.480 (fine-grid minimum) with caption
provenance, 8*gap12 3.85 -> 3.84, the closing-rate cells sigma_eff(6->8)
0.258 -> 0.259 and alpha_eff(6->8) 1.794 -> 1.802 (same table-value
convention as v25_sigma_extract.py), the L=8 rung paragraph extended by the
fine grid and the d=3 ladder, the locator sentence, the Scope note, one
abstract clause, and the Conclusion extensions paragraph restated from
promissory to deposited.  Supplement: the local-dimension extension
paragraph completed with both deposits, the reproduction chain extended by
the extension script.  Every replacement is asserted to occur the stated
number of times.  No earlier version file is touched."""
import math
import re
from pathlib import Path

V = Path('/home/z/my-project/quantum-circuits/research/versions')
MS_OLD = (V / 'manuscript_revised_v26.tex').read_text()
SM_OLD = (V / 'supplement_v8.tex').read_text()

# ---------------------------------------------------------------- arithmetic
# Same convention as the deposited v25_sigma_extract.py: rates derived from
# the quoted table cells (3 decimals), cross-checked to rounding.  The n=5
# L=8 cell is the fine-grid minimum 0.479650 -> quoted 0.480.
GAPS_D2 = {4: 1.711, 6: 0.806, 8: 0.480}
GAPS_D3 = {4: 1.482, 6: 0.621, 8: 0.453}   # at the d=3 locators


def rates(g):
    out = {}
    for L1, L2 in [(4, 6), (6, 8)]:
        c = math.log(g[L1] / g[L2])
        out[(L1, L2)] = (c / (L2 - L1), c / math.log(L2 / L1), g[L1] / g[L2])
    return out


r2, r3 = rates(GAPS_D2), rates(GAPS_D3)
assert f"{r2[(6, 8)][0]:.3f}" == "0.259"      # sigma_eff, d=2, L=6->8
assert f"{r2[(6, 8)][1]:.3f}" == "1.802"      # alpha_eff, d=2, L=6->8
assert f"{r2[(6, 8)][2]:.2f}" == "1.68"       # closing factor, d=2, L=6->8
assert f"{8 * GAPS_D2[8]:.2f}" == "3.84"      # 8*gap12, d=2
assert f"{r3[(4, 6)][2]:.2f}" == "2.39"       # closing factor, d=3, L=4->6
assert f"{r3[(6, 8)][2]:.2f}" == "1.37"       # closing factor, d=3, L=6->8
assert f"{r3[(4, 6)][0]:.3f}" == "0.435"      # sigma_eff, d=3, L=4->6
assert f"{r3[(6, 8)][0]:.3f}" == "0.158"      # sigma_eff, d=3, L=6->8
assert f"{r3[(4, 6)][1]:.3f}" == "2.145"      # alpha_eff, d=3, L=4->6
assert f"{r3[(6, 8)][1]:.3f}" == "1.096"      # alpha_eff, d=3, L=6->8
assert f"{8 * GAPS_D3[8]:.2f}" == "3.62"      # 8*gap12, d=3
assert f"{6 * GAPS_D3[6]:.2f}" == "3.73"      # 6*gap12, d=3 (existing quote)
# level ordering: gap(d=3) < gap(d=2) at every size
assert all(GAPS_D3[L] < GAPS_D2[L] for L in (4, 6, 8))
print("arithmetic cross-checks PASS "
      f"(d2: sig68={r2[(6,8)][0]:.3f} alp68={r2[(6,8)][1]:.3f}; "
      f"d3: sig46={r3[(4,6)][0]:.3f} sig68={r3[(6,8)][0]:.3f} "
      f"alp46={r3[(4,6)][1]:.3f} alp68={r3[(6,8)][1]:.3f})")

# ------------------------------------------------------------------- headers
MS_HEADER_OLD = """% manuscript_revised_v26.tex -- closing-rate diagnostics pass (patch_v26_closing.py)
% of manuscript_revised_v25_tjp.tex, which is preserved unmodified alongside its
% predecessors (v25 = the TJP editorial pass by the parallel instance; v26 was
% reserved by the worklog coordination claim for the compute-extension promotion).
% Scope of this pass: the dual effective closing rates of the two-phase gap -- the
% interface-tension (sigma_eff) and power-law (alpha_eff) readings of the deposited
% size-ladder values -- as a new table and two paragraphs in Sec. II.G; one abstract
% clause; one last-digit correction (6*0.806 = 4.836, quoted "4.85" -> "4.84", two
% sites); two Conclusion extension sentences (the closing-rate table pointer; the
% deposited d=3 locator scans); Supplement v8 with the extraction protocol and the
% d=3 local-dimension extension.  Companion: supplement_v8.tex (same pass).
% Change log: changelog_v26.md.  Provenance ledger: certificate_sha256_v13.txt.
"""

MS_HEADER_NEW = r"""% manuscript_revised_v27.tex -- extension-integration pass (patch_v27_extL8.py)
% of manuscript_revised_v26.tex, which is preserved unmodified alongside its
% predecessors.  Scope of this pass: integration of the completed extension
% campaign -- the d=3 L=8 rung (p=0.82/0.84/0.86, interior minimum 0.453 at
% p=0.84, completing the d=3 three-size ladder) and the finer d=2 locator grid
% at L=8 (p=0.455/0.465/0.475/0.485, minimum 0.4797 at p=0.465) -- into the
% size-ladder table (cell 0.481 -> 0.480, 8*gap12 3.85 -> 3.84), the closing-
% rate table (sigma_eff 0.258 -> 0.259, alpha_eff 1.794 -> 1.802, same
% table-value convention as v25_sigma_extract.py), the L=8 rung paragraph, the
% locator sentence, the Scope note, one abstract clause, and the Conclusion
% (the extensions paragraph restated from promissory to deposited).  Every
% number verbatim from the deposited results (v25_n5_L8_rung_d3.json,
% v25_n5_L8_finegrid.json).  Companion: supplement_v9.tex (same pass).
% Change log: changelog_v27.md.  Provenance ledger: certificate_sha256_v14.txt.
"""

SM_HEADER_OLD = """% supplement_v8.tex -- closing-rate diagnostics pass (patch_v26_closing.py) of
% supplement_v7.tex, which is preserved unmodified.  Same pass as the manuscript:
% two new paragraphs in Sec. S7 (the effective closing rates of the two-phase gap;
% the local-dimension extension at d=3 -- block-route validation and the deposited
% locator scans).  Provenance ledger: certificate_sha256_v13.txt.
"""

SM_HEADER_NEW = r"""% supplement_v9.tex -- extension-integration pass (patch_v27_extL8.py) of
% supplement_v8.tex, which is preserved unmodified.  Same pass as the manuscript:
% the local-dimension extension paragraph of Sec. S7 completed with the two
% extension deposits (the d=3 L=8 rung and the finer d=2 locator grid at L=8:
% values, protocol, and the three-size readings), and the reproduction chain
% extended with the extension script.  Provenance ledger:
% certificate_sha256_v14.txt.
"""

# --------------------------------------------------------------- MS edits
MS_EDITS = [

    # (1) abstract clause
    ("at matched sizes.  We further prove",
     "at matched sizes, and at local dimension $d=3$ the same three-size test "
     "keeps the gap level below the $d=2$ values at every size.  We further "
     "prove", 1),

    # (2) locator sentence
    ("the gap-minimum locator is stable ($0.48$ at $L=4$, $0.47$ at $L=6$),\n"
     "placing the annealed five-replica point at $p_c^{(5)}\\approx0.47$--$0.48$.",
     "the gap-minimum locator is stable across the ladder ($0.48$, $0.47$, "
     "$0.465$ at\n$L=4,6,8$, the last on the finer grid), placing the annealed "
     "five-replica point\nat $p_c^{(5)}\\approx0.47$--$0.48$.", 1),

    # (3) size-ladder table caption provenance
    ("and at $n=5$ from the symmetry-reduced block route.}",
     "and at $n=5$ from the symmetry-reduced block route, the $L=8$ value being\n"
     "the minimum of the finer locator grid ($p=0.455$--$0.485$, minimum at\n"
     "$p=0.465$; Supplemental Material~\\cite{SM}, Sec.~S7).}", 1),

    # (4) size-ladder table cell
    ("$\\mathrm{gap}_{12}(L{=}8)$ & $0.816$ & $0.645$ & $0.481$ \\\\",
     "$\\mathrm{gap}_{12}(L{=}8)$ & $0.816$ & $0.645$ & $0.480$ \\\\", 1),

    # (5) scaled-gap row
    ("$8\\,\\mathrm{gap}_{12}$ & $6.53$ & $5.16$ & $3.85$ \\\\",
     "$8\\,\\mathrm{gap}_{12}$ & $6.53$ & $5.16$ & $3.84$ \\\\", 1),

    # (6) L=8 rung paragraph: fine grid + d=3 ladder
    ("the locator grid; at the $p=0.47$ locator the closing factor extends to\n"
     "$\\times1.68$ from $L=6$ to $L=8$ (against $2.12$ from $L=4$ to\n"
     "$L=6$), and $L\\,\\mathrm{gap}_{12}=3.85$ falls further below the\n"
     "continuous envelope ($6.53$ at $L=8$ for the $n=3$ baseline)---the\n"
     "first-order reading of the $q=5$ prediction at the three-size level.",
     "the locator grid, refined by the finer locator grid ($p=0.455$: 0.484, "
     "$p=0.465$:\n0.480, $p=0.475$: 0.485, $p=0.485$: 0.501); at the refined "
     "$p=0.465$ locator\nthe closing factor extends to $\\times1.68$ from "
     "$L=6$ to $L=8$ (against\n$2.12$ from $L=4$ to $L=6$), and "
     "$L\\,\\mathrm{gap}_{12}=3.84$ falls further\nbelow the continuous "
     "envelope ($6.53$ at $L=8$ for the $n=3$ baseline)---the\nfirst-order "
     "reading of the $q=5$ prediction at the three-size level.  The\nsame orbit "
     "basis serves the local-dimension extension at $d=3$ (only the\nper-bond "
     "channel changes, through the Gram $D=9$): the $d=3$ ladder reads\n"
     "$1.482$ ($L=4$, $p\\approx0.85$), $0.621$ ($L=6$, $p=0.85$), $0.453$ "
     "($L=8$,\nthe interior minimum at $p=0.84$, bracketed by the rung values "
     "$0.948$ at\n$p=0.82$ and $0.519$ at $p=0.86$)---the gap level sits below "
     "the $d=2$ value\nat every size and $8\\,\\mathrm{gap}_{12}=3.62$ below "
     "the $d=2$ value $3.84$,\nwhile the interval closing factors read "
     "$\\times2.39$ then $\\times1.37$\n(against $\\times2.12$, $\\times1.68$ "
     "at $d=2$): the level ordering carries the\nfirst-order direction with "
     "local dimension, and the interval rates sit in\nthe crossover region at "
     "both dimensions (deposits: Supplemental\nMaterial~\\cite{SM}, Sec.~S7).",
     1),

    # (7) closing-rate caption: fine-grid provenance of the n=5 L=8 cell
    # (caption is a single source line)
    ("computed from the size-ladder values of Table~\\ref{tab:n5twosize} (the $n=3$ $L=10$ rate from the deposited envelope value $10\\,\\mathrm{gap}_{12}=6.21$).",
     "computed from the size-ladder values of Table~\\ref{tab:n5twosize} (the"
     "$n=5$ $L{=}8$ value being the finer-grid minimum; the $n=3$ $L=10$ rate "
     "from the deposited envelope value $10\\,\\mathrm{gap}_{12}=6.21$).", 1),

    # (8) closing-rate cells (n=5, L=6->8)
    ("$\\sigma_{\\rm eff}$, $L{=}6\\to8$ & $0.187$ & $0.214$ & $0.258$ \\\\",
     "$\\sigma_{\\rm eff}$, $L{=}6\\to8$ & $0.187$ & $0.214$ & $0.259$ \\\\", 1),
    ("$\\alpha_{\\rm eff}$, $L{=}6\\to8$ & $1.297$ & $1.489$ & $1.794$ \\\\",
     "$\\alpha_{\\rm eff}$, $L{=}6\\to8$ & $1.297$ & $1.489$ & $1.802$ \\\\", 1),

    # (9) Scope note
    ("$d=2$, $L\\le10$ at $n=4$ and $L\\le8$ at $n=5$; the universality",
     "$d=2$, $L\\le10$ at $n=4$ and $L\\le8$ at $n=5$ (the local-dimension\n"
     "extension $d=3$ at $n=5$ through $L=8$); the universality", 1),

    # (10) Conclusion: last-digit
    ("falls to $3.85$ at $n=5$",
     "falls to $3.84$ at $n=5$", 1),

    # (11) Conclusion: extensions paragraph, promissory -> deposited
    ("Three extensions follow immediately from the machinery as deposited: the $d=3$ rung at $L=8$ on the same orbit basis, a finer $p$-grid resolving the $n=5$ locator, and interface-tension and latent-heat extraction from the deposited eigensystems.  The interface-tension reading of the deposited size ladder is delivered in Table~\\ref{tab:closingrates}, and the $d=3$ locator scans at $L=4$ and $L=6$ are deposited: the gap minimum sits at $p\\approx0.85$ at both sizes, and the two-size closing factor is $2.39$ against $2.12$ at $d=2$---the first-order direction strengthens with local dimension (Supplemental Material~\\cite{SM}, Sec.~S7).",
     "The extensions that follow immediately from the deposited machinery---the\n"
     "$d=3$ rung at $L=8$ on the same orbit basis and the finer $p$-grid "
     "resolving\nthe $n=5$ locator---join the interface-tension reading of "
     "Table~\\ref{tab:closingrates}\nin the deposits.  The finer grid places the "
     "$L=8$ locator at $p=0.465$ (gap\n$0.4797$; locator sequence "
     "$0.48/0.47/0.465$ over $L=4,6,8$); the $d=3$\nladder through $L=8$ reads "
     "$1.482/0.621/0.453$ at its locators ($p\\approx0.85$,\n$0.85$, $0.84$), "
     "the gap level sitting below the $d=2$ value at every size\nand "
     "$8\\,\\mathrm{gap}_{12}=3.62$ below the $d=2$ value $3.84$: the level\n"
     "ordering carries the first-order direction with local dimension, while "
     "the\ninterval closing factors ($\\times2.39$ then $\\times1.37$) decelerate "
     "as at\n$d=2$ ($\\times2.12$ then $\\times1.68$)---both dimensions sitting "
     "in the\ncrossover region before the asymptotic exponential regime "
     "(Supplemental\nMaterial~\\cite{SM}, Sec.~S7).  The remaining "
     "extension---latent-heat extraction\nfrom the deposited eigensystems---"
     "follows from the same deposits.", 1),
]

# --------------------------------------------------------------- SM edits
SM_EDITS = [

    # (1) extension paragraph: two-size claim closed; completed deposits
    ("$4.84$: the first-order direction strengthens with local dimension.\n"
     "The $L=8$ rung at $d=3$ and a finer $d=2$ locator grid follow the same\n"
     "chunk-checkpointed block assembly and the same driving protocol as the\n"
     "deposited rung.",
     "$4.84$ at the two-size level.  The $L=8$ rung at $d=3$ "
     "($p=0.82,0.84,0.86$;\ndeposited as \\texttt{v25\\_n5\\_L8\\_rung\\_d3.json}) "
     "and the finer $d=2$\nlocator grid at $L=8$ ($p=0.455,0.465,0.475,0.485$; "
     "deposited as\n\\texttt{v25\\_n5\\_L8\\_finegrid.json}), both hashed in\n"
     "\\texttt{certificate\\_sha256\\_v14.txt}, are computed with the same\n"
     "chunk-checkpointed block assembly and the same bounded-window execution\n"
     "protocol as the deposited rung (restart-safe; each $L=8$\n"
     "point costs ${\\sim}17$\\,h of wall time).  The finer grid reads\n"
     "$\\mathrm{gap}_{12}=0.484/0.480/0.485/0.501$: the $L=8$ minimum refines\n"
     "to $0.4797$ at $p=0.465$ (against $0.481$ at both $p=0.46$ and $p=0.47$\n"
     "on the rung grid), the locator sequence reads $0.48\\to0.47\\to0.465$\n"
     "over $L=4,6,8$, and the main-text cells move in the last digit only\n"
     "($0.481\\to0.480$; $8\\,\\mathrm{gap}_{12}=3.84$; "
     "$\\sigma_{\\rm eff}(6\\to8)=0.259$,\n$\\alpha_{\\rm eff}(6\\to8)=1.802$).  "
     "The $d=3$ rung reads $0.948/0.453/0.519$\nwith the interior minimum at "
     "$p=0.84$, completing the $d=3$ three-size ladder\n$1.482\\to0.621\\to0.453$ "
     "at its locators: the gap level sits below the\n$d=2$ value at every size "
     "and $8\\,\\mathrm{gap}_{12}=3.62$ below the\n$d=2$ value $3.84$, while the "
     "interval closing factors read $\\times2.39$\nthen $\\times1.37$ "
     "($\\sigma_{\\rm eff}=0.435\\to0.158$,\n$\\alpha_{\\rm eff}=2.145\\to1.096$) "
     "against $\\times2.12$, $\\times1.68$ at\n$d=2$---the level ordering carries "
     "the first-order direction with local\ndimension, and the interval rates "
     "decelerate at both dimensions, the\ncrossover-region behaviour the main "
     "text records.", 1),

    # (2) reproduction chain: extension script
    ("\\texttt{v22\\_n5\\_L8\\_block\\_v1.py run --pgrid 0.44,0.46,0.47,0.48,0.50}.\n"
     "Dependencies:",
     "\\texttt{v22\\_n5\\_L8\\_block\\_v1.py run --pgrid 0.44,0.46,0.47,0.48,0.50},\n"
     "\\texttt{v25\\_n5\\_L8\\_ext\\_v1.py} (validates the $d=3$ route, scans the "
     "locators,\nand computes the extension points---the $d=3$ $L=8$ rung and the "
     "finer $d=2$\ngrid; its JSONs land in \\texttt{results/v22-exactZ3-n5L8/} "
     "and its logs in\n\\texttt{logs/v25-n5L8-ext/}).\nDependencies:", 1),

    # (3) formal-prose fix: compute-round language in the reproduction block
    ("The files of this round are hashed in\n\\texttt{certificate\\_sha256\\_v8.txt} (round files) and",
     "The files of this computational suite are hashed in\n\\texttt{certificate\\_sha256\\_v8.txt} and", 1),
]


def apply(text, edits, tag):
    for i, (old, new, n) in enumerate(edits, 1):
        c = text.count(old)
        assert c == n, f"{tag} edit {i}: expected {n} match(es), found {c}"
        text = text.replace(old, new)
    return text


def residual_report(text, tag):
    print(f"--- residual-token report [{tag}] (visible lines only) ---")
    hits = 0
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("%"):
            continue
        for pat in [r"\bprevious version\b", r"\bprevious implementation\b",
                    r"\bis now done\b", r"\bnow supplies\b", r"\bnow computed\b",
                    r"\bnow resolved\b", r"\bnow exists?\b", r"\bnow proves\b",
                    r"\bnow extends\b", r"\bnow measured\b", r"\bin flight\b",
                    r"\bfollow immediately\b.*\bfollow the same\b",
                    r"corrected v21", r"mis-transcription",
                    r"present revision", r"recovered dataset",
                    r"no longer a prediction", r"placeholder DOI",
                    r"XXXXXXX", r"\bstrengthens with local dimension\b",
                    # compute-infrastructure vocabulary (not journal prose)
                    r"\bcampaign\b", r"\bextension queue\b", r"\bwatch round",
                    r"\bpython segment\b", r"\bdriving protocol\b",
                    r"\bdrive[sd]? the extension\b", r"\bsandbox\b",
                    r"\brollback\b", r"\bcron\b", r"\bworklog\b",
                    r"\bOOM\b", r"\bsingle-segment\b"]:
            for m in re.finditer(pat, line):
                hits += 1
                print(f"  line {ln}: {pat}: ...{line[max(0, m.start()-40):m.end()+40]}...")
    print(f"  forbidden-token hits: {hits}")
    now_hits = [(ln, line.strip()[:110]) for ln, line in enumerate(text.splitlines(), 1)
                if not line.lstrip().startswith("%") and re.search(r"\bnow\b", line)]
    print(f"  remaining '\\bnow\\b' occurrences (review for benignity): {len(now_hits)}")
    for ln, ctx in now_hits:
        print(f"    line {ln}: {ctx}")


assert MS_OLD.count(MS_HEADER_OLD) == 1
ms = MS_OLD.replace(MS_HEADER_OLD, MS_HEADER_NEW)
assert SM_OLD.count(SM_HEADER_OLD) == 1
sm = SM_OLD.replace(SM_HEADER_OLD, SM_HEADER_NEW)
ms = apply(ms, MS_EDITS, "MS")
sm = apply(sm, SM_EDITS, "SM")

# structural assertions on the outputs (visible lines only: the new header
# comments legitimately mention the before->after values)
ms_vis = "\n".join(l for l in ms.splitlines() if not l.lstrip().startswith("%"))
sm_vis = "\n".join(l for l in sm.splitlines() if not l.lstrip().startswith("%"))
assert ms.count(r"\section{Conclusion}") == 1
assert ms.count(r"\label{tab:n5twosize}") == 1
assert ms.count(r"\label{tab:closingrates}") == 1
assert ms_vis.count("3.85") == 0                    # stale scaled gap gone
assert ms_vis.count("0.481") == 2                  # rung-grid quotes only
assert ms_vis.count("0.480") == 2                  # table cell + fine grid
assert ms_vis.count("0.4797") == 1                 # conclusion
assert ms_vis.count("0.465") >= 3                  # locator/rung/conclusion
assert ms_vis.count("0.259") == 1 and ms_vis.count("1.802") == 1
assert ms_vis.count("3.62") == 3   # 2 new (rung para + conclusion) + the
                                    # pre-existing unrelated SMC entropy-rate
                                    # quote in Sec. smcnumerics (visible line)
assert ms_vis.count("strengthens with local dimension") == 0
assert sm_vis.count("v25\\_n5\\_L8\\_rung\\_d3.json") == 1
assert sm_vis.count("v25\\_n5\\_L8\\_finegrid.json") == 1
assert sm_vis.count("certificate\\_sha256\\_v14.txt") == 1
assert sm_vis.count("follow the same") == 0         # promissory sentence gone
assert sm_vis.count("strengthens with local dimension") == 0
secs = re.findall(r"\\section\{([^}]*)\}", ms)
print(f"MS sections ({len(secs)}): {secs}")
assert len(secs) == 9
sm_paras = re.findall(r"\\paragraph\{([^}]*)\}", sm)
print(f"SM paragraphs: {len(sm_paras)} (last three: {sm_paras[-3:]})")

(V / "manuscript_revised_v27.tex").write_text(ms)
(V / "supplement_v9.tex").write_text(sm)
print(f"written: manuscript_revised_v27.tex ({len(ms)} chars), "
      f"supplement_v9.tex ({len(sm)} chars)")
residual_report(ms, "MS v27")
residual_report(sm, "SM v9")
print("PATCH OK")
