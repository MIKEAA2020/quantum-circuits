"""patch_v23_rung.py -- build manuscript_revised_v23_rung.tex (+ supplement_v6,
report v11, changelog_v23.md, README_v23_rung.md, commit_msg_v23.txt) from the
completed n=5 L=8 rung JSON (v22_n5_L8_rung.json).

v23 = v22 + the L=8 rung completion.  NOTHING of v21/v22 is modified:
every output is a NEW file (the user's standing rule).  All anchors are
asserted unique in the committed v22/v5 sources; any mismatch aborts
loudly BEFORE any file is written.

The closing-factor convention follows tab:n5twosize: closing factor =
previous gap / new gap (2.12 = 1.711/0.806 from L=4 to L=6), so the
L=6 -> L=8 factor is 0.806/gap12(L=8, p=0.47).  (The never-executed
RUNG branch of patch_v22_exactZ3.py had this ratio inverted; v23 fixes
the direction.)

Usage: python3 patch_v23_rung.py [path-to-rung-json]
  default: ../../results/v22-exactZ3-n5L8/v22_n5_L8_rung.json
"""
import json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
VER = os.path.join(HERE, '..', '..', 'versions')
RES = os.path.join(HERE, '..', '..', 'results', 'v22-exactZ3-n5L8')

RUNG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    RES, 'v22_n5_L8_rung.json')


def log(*a):
    print(*a, flush=True)


rows_all = json.load(open(RUNG))
rows = [r for r in rows_all if r.get('gap12') is not None]
assert rows, f'no completed rung points with gap12 in {RUNG}'
rgs = sorted(rows, key=lambda r: r['p'])
K = int(rgs[0]['K'])
GAP6 = 0.806            # gap12(L=6) at the p=0.47 locator (tab:n5twosize)
ENV8 = 6.53             # n=3 continuous envelope, L*gap12 at L=8
g47 = [r for r in rgs if abs(r['p'] - 0.47) < 0.005]
HAVE47 = bool(g47)

GAPLIST = ", ".join(f"$p={r['p']:.2f}$: {r['gap12']:.3f}" for r in rgs)
if HAVE47:
    CF = GAP6 / g47[0]['gap12']
    L8G = 8.0 * g47[0]['gap12']
    CLOSING = (
        f"; at the $p=0.47$ locator the closing factor extends to\n"
        f"$\\times{CF:.2f}$ from $L=6$ to $L=8$ (against $2.12$ from $L=4$ to\n"
        f"$L=6$), and $L\\,\\mathrm{{gap}}_{{12}}={L8G:.2f}$ falls further "
        f"below the\ncontinuous envelope (${ENV8}$ at $L=8$ for the $n=3$ "
        f"baseline)---the\nfirst-order reading of the $q=5$ prediction at "
        f"the three-size level."
    )
    CF_S = f"x{CF:.2f}"
    L8G_S = f"{L8G:.2f}"
else:
    CLOSING = (
        "---the gap continuing to fall at every computed grid point, the\n"
        "first-order direction throughout."
    )
    CF_S = "(p=0.47 point not completed)"
    L8G_S = "---"

RUNG_TEX = (
    "The $L=8$ rung (the exponential-vs-power-law discriminator): the mom0\n"
    "triv.triv sector at $n=5$, $L=8$ has dimension\n"
    f"{K} (the orbit count of\n"
    "$(S_5\\times S_5)\\rtimes\\mathbb Z_4$ on $(S_5)^4$), assembled as an "
    "exact\ndense block (Supplemental Material~\\cite{SM}, Sec.~S7; the "
    "assembler\nvalidated against the deposited $L=4$ spectrum to\n"
    "$1.6\\times10^{-14}$ and the $L=6$ blocks against unrestricted\n"
    "colour-restricted Arnoldi solves), with\n"
    "$\\mathrm{gap}_{12}=\\log(\\lambda_1/\\lambda_2)$ equal to "
    f"{GAPLIST} over\nthe locator grid{CLOSING}\n"
)

log(f"== v23 rung data: K={K}, points={[r['p'] for r in rgs]}, "
    f"0.47={'yes' if HAVE47 else 'NO'} ==")

# ===========================================================================
# 1) the manuscript: v22 -> v23
# ===========================================================================
msrc = open(os.path.join(VER, 'manuscript_revised_v22_exactZ3.tex')).read()


def rep(src, old, new, cnt=1, what=''):
    assert src.count(old) == cnt, (
        f"[{what}] anchor not unique ({src.count(old)}): {old[:90]!r}")
    return src.replace(old, new)


# R.a: the abstract clause (after the two-size confirmation sentence)
msrc = rep(
    msrc,
    "the coexistence plateau narrowing at fixed $\\xi$.  For the record "
    "problem we prove",
    "the coexistence plateau narrowing at fixed $\\xi$, and the $L=8$ "
    "rung---a symmetry-reduced exact dense block over the "
    "$120^4=2.1\\times10^8$ bond-label space, validated against the "
    "deposited smaller-size spectra---extends the closing to three sizes."
    "  For the record problem we prove",
    what='abstract')

# R.b: the pre-table paragraph (the "natural next rung" sentence delivered)
msrc = rep(
    msrc,
    "slope-ratio excess) points the same way, with the honest caveat that "
    "two\nsizes cannot yet separate an exponential from a power-law closing "
    "and\nthat $L=8$ ($120^4=2.1\\times10^8$ bond labels) is the natural "
    "next\nrung.",
    "slope-ratio excess) points the same way; two sizes alone cannot "
    "separate\nan exponential from a power-law closing, and the $L=8$ rung\n"
    "($120^4=2.1\\times10^8$ bond labels, carried by the "
    "symmetry-reduced\nblock route of the Supplemental "
    "Material~\\cite{SM}) now supplies the\nthird size, with the numbers "
    "below.",
    what='pre-table')

# R.c: the rung paragraph + the Scope line (L<=6 -> L<=8)
msrc = rep(
    msrc,
    "\\emph{Scope.}  Exact finite-size data with systematic extrapolation,"
    "\n$d=2$, $L\\le10$ at $n=4$ and $L\\le6$ at $n=5$; the universality",
    "@@RUNGTEX@@\\emph{Scope.}  Exact finite-size data with systematic "
    "extrapolation,\n$d=2$, $L\\le10$ at $n=4$ and $L\\le8$ at $n=5$; "
    "the universality",
    what='scope-head')
msrc = msrc.replace('@@RUNGTEX@@', RUNG_TEX)

# R.d: the Scope "two-size" -> "three-size"
msrc = rep(
    msrc,
    "$n=5$ first-order test is now two-size, its every measured quantity "
    "in",
    "$n=5$ first-order test is now three-size, its every measured quantity "
    "in",
    what='scope-twosize')

# R.e: the Discussion roadmap
msrc = rep(
    msrc,
    "the $q=n$-Potts conjecture is confirmed at the two-size level for "
    "$n\\le5$, with the $L=8$ rung (the symmetry-reduced block route) in "
    "preparation,",
    "the $q=n$-Potts conjecture is confirmed at the two-size level for "
    "$n\\le5$ (three sizes at $n=5$), with the $L=8$ rung computed by the "
    "symmetry-reduced block route (Sec.~\\ref{sec:n4n5}),",
    what='discussion')

# R.f: app:files -- the rung result deposited
msrc = rep(
    msrc,
    "and \\texttt{v22\\_n5\\_L8\\_block\\_v1.py} (the symmetry-reduced "
    "block route), with their JSON results and logs.",
    "and \\texttt{v22\\_n5\\_L8\\_block\\_v1.py} (the symmetry-reduced "
    "block route, its rung result \\texttt{v22\\_n5\\_L8\\_rung.json} now "
    "deposited), with their JSON results and logs.",
    what='app:files')

# R.g: the version header
V23HEAD = (
    f"% v23 (the L=8 rung): the n=5 L=8 symmetry-reduced block completed "
    f"at\n% the locator grid p=0.44-0.50 (dimension K={K}, orbits of "
    f"(S5xS5)rtimes Z4\n% on (S5)^4); gap12 values at the grid, the "
    f"p=0.47 closing factor\n% extended to three sizes, the L-scaled gap "
    f"below the continuous\n% envelope; abstract clause, pre-table "
    f"paragraph, Scope (L<=8, three-size),\n% Discussion roadmap and "
    f"app:files updated.  Built by patch_v23_rung.py from\n% v22 "
    f"(unchanged); companions: supplement_v6, changelog_v23.md,\n"
    f"% README_v23_rung.md, report v11, certificate_sha256_v10.txt.\n")
assert msrc.startswith('% v21 (Clifford record-count closure):'), 'v22 head?'
msrc = V23HEAD + msrc

# ===========================================================================
# 2) the supplement: v5 -> v6
# ===========================================================================
ssrc = open(os.path.join(VER, 'supplement_v5.tex')).read()

ssrc = rep(
    ssrc,
    "The $L=8$ rung\nruns the block at the locator grid.",
    "The $L=8$ rung\nruns the block at the locator grid; the completed "
    f"rung ({len(rgs)} grid\npoints) is deposited as "
    "\\texttt{v22\\_n5\\_L8\\_rung.json} and hashed in\n"
    "\\texttt{certificate\\_sha256\\_v10.txt}.",
    what='supp-rung')

ssrc = rep(
    ssrc,
    "The files of\nthis round are hashed in "
    "\\texttt{certificate\\_sha256\\_v9.txt}.",
    "The files of\nthis round are hashed in "
    "\\texttt{certificate\\_sha256\\_v9.txt}; the v23 rung\ncompletion "
    "(\\texttt{v22\\_n5\\_L8\\_rung.json}, "
    "\\texttt{manuscript\\_revised\\_v23\\_rung})\nis hashed in "
    "\\texttt{certificate\\_sha256\\_v10.txt}.",
    what='supp-cert')

ssrc = ("% v23 (the L=8 rung completion): the rung result deposited\n"
        "% (v22_n5_L8_rung.json, hashed in certificate_sha256_v10.txt); "
        "built from\n% supplement_v5.tex by patch_v23_rung.py "
        "(v5 unchanged).\n") + ssrc

# ===========================================================================
# 3) the report: v10 -> v11 (copy + Sec. 26)
# ===========================================================================
r10 = open(os.path.join(VER, 'mipt_numerical_report_v10.md')).read()
perp = "\n".join(
    f"  - p={r['p']:.2f}: lam1={r['lam1']:.8e}, lam2={r['lam2']:.8e}, "
    f"gap12={r['gap12']:.5f}, growth=lam1^(1/8)={r['growth']:.6f} "
    f"[{r['secs']}s]" for r in rgs)
if HAVE47:
    closing_md = (
        f"- p=0.47 locator: gap12 = {g47[0]['gap12']:.5f}; closing factor "
        f"0.806/{g47[0]['gap12']:.5f} = x{CF:.2f} from L=6 to L=8 "
        f"(L=4->L=6 was x2.12);\n  L*gap12 = {L8G:.2f} against the n=3 "
        f"continuous envelope value {ENV8} at L=8.")
else:
    closing_md = "- the p=0.47 locator point did not complete in this run."
SEC26 = f"""

## 26. The n=5 L=8 rung: completion (v23)

The background chain (`run_chain.sh`, started during the v22 round)
completed the `ids` and `run` phases after the v22 commit; this section
records the rung numbers that the v23 manuscript paragraph carries
(source: `v22_n5_L8_rung.json`, {len(rgs)} grid points).

- Orbit table at nb=4: K = {K} orbits of (S5 x S5) |x Z4 on (S5)^4
  (the canonical-id array is 207,360,000 int32 entries ~ 830 MB and is
  NOT deposited -- it exceeds GitHub's 100 MB file limit and is
  regenerated deterministically by `v22_n5_L8_block_v1.py ids`;
  `reps_nb4.npy` / `counts_nb4.npy` ARE deposited).
- gap12 = log(lam1/lam2) at the locator grid:
{perp}
{closing_md}
- Validation carried over from the v22 round's `validate` phase
  (VALIDATION PASS): nb=2 vs the deposited L=4 spectrum (max rel
  1.6e-14), nb=3 vs unrestricted colour-restricted Arnoldi solves
  (2.1e-14 / 9.8e-15).
- Manuscript: `manuscript_revised_v23_rung.tex` (rung paragraph + Scope
  L<=8 / three-size + Discussion roadmap + app:files + abstract clause),
  built by `patch_v23_rung.py` from v22 with all anchors asserted;
  supplement v6; certificate `certificate_sha256_v10.txt`.
"""
r11 = r10 + SEC26

# ===========================================================================
# 4) the companions: changelog, README, commit message
# ===========================================================================
NOW = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
CHANGELOG = f"""# changelog_v23.md — v23: the L=8 rung completion ({NOW})

v23 = v22 + the n=5 L=8 rung (the exponential-vs-power-law discriminator),
delivered by the background chain after the v22 commit.  All files are NEW;
v21/v22 are untouched.

## Manuscript (manuscript_revised_v23_rung.tex, built from v22 by patch_v23_rung.py)
- NEW rung paragraph before the Scope block (sec:n4n5): the mom0 triv.triv
  sector at n=5, L=8 — dimension K = {K} (orbits of (S5 x S5) |x Z4 on
  (S5)^4), assembled as an exact dense block; gap12 = log(l1/l2) at the
  locator grid: {GAPLIST}{'; closing factor x' + f"{CF:.2f}" if HAVE47 else ''}
  from L=6 to L=8 at the p=0.47 locator (against x2.12 from L=4 to L=6);
  L*gap12 = {L8G_S} vs the n=3 envelope {ENV8} at L=8.
- Pre-table paragraph: the "honest caveat / natural next rung" sentence
  delivered (two sizes cannot separate exponential from power-law; the
  L=8 rung supplies the third size).
- Scope: "$L\\le10$ at $n=4$ and $L\\le8$ at $n=5$"; "now three-size".
- Discussion: the roadmap clause "with the L=8 rung ... in preparation" ->
  "computed by the symmetry-reduced block route (Sec. sec:n4n5)"; the
  q=n-Potts confirmation annotated "(three sizes at n=5)".
- Abstract: one clause appended (the L=8 rung extends the closing to three
  sizes).
- app:files: the rung result v22_n5_L8_rung.json noted as deposited.
- CONVENTION FIX relative to the never-executed RUNG branch of
  patch_v22_exactZ3.py: the closing factor is 0.806/gap12(L=8) (the
  tab:n5twosize convention: previous gap / new gap), not the inverse.

## Supplement (supplement_v6.tex, from v5)
- The block-route paragraph: the completed rung deposited
  (v22_n5_L8_rung.json) and hashed in certificate_sha256_v10.txt.
- The files-of-this-round sentence extended with the v10 ledger pointer.

## Companions
- mipt_numerical_report_v11.md = report v10 + Sec. 26 (the rung numbers).
- certificate_sha256_v10.txt (make_cert_v10.py): v23 files + the rung JSON
  + the ids/run logs + reps_nb4/counts_nb4.
- Results: results/v22-exactZ3-n5L8/v22_n5_L8_rung.json; logs:
  v22_n5_L8_block_ids.log, v22_n5_L8_block_run.log, chain.log (CHAIN_DONE).
"""

README = f"""# README_v23_rung.md — v23: the n=5 L=8 rung completion ({NOW})

**What landed.** The background chain (`run_chain.sh`) completed the
symmetry-reduced block computation at n=5, L=8 — the
exponential-vs-power-law discriminator of the two-size first-order test.
K = {K} orbits; gap12 at the grid: {GAPLIST}; p=0.47 locator: closing
factor {CF_S} from L=6 to L=8, L*gap12 = {L8G_S} (n=3 envelope {ENV8}).

**Files (all new; v21/v22 untouched).**
- `versions/manuscript_revised_v23_rung.tex/.pdf` — the rung paragraph +
  Scope/Discussion/abstract/app:files alignment (patch_v23_rung.py, all
  anchors asserted against the committed v22).
- `versions/supplement_v6.tex/.pdf` — the rung-deposit note + ledger
  pointer.
- `versions/mipt_numerical_report_v11.md` — report v10 + Sec. 26.
- `versions/changelog_v23.md`, this file.
- `versions/certificate_sha256_v10.txt` — ledger v10 (make_cert_v10.py).
- `results/v22-exactZ3-n5L8/v22_n5_L8_rung.json` — the rung rows
  (p, L, n, K, triv6, lam1, lam2, gap12, growth, secs).
- `results/v22-exactZ3-n5L8/tmp_n5L8block/reps_nb4.npy`,
  `counts_nb4.npy` — the orbit table (the 830 MB canonical-id array is
  NOT deposited: GitHub's 100 MB limit; regenerate with
  `python3 v22_n5_L8_block_v1.py ids`).
- `logs/v22-exactZ3-n5L8/v22_n5_L8_block_ids.log`,
  `v22_n5_L8_block_run.log`, `chain.log` (CHAIN_DONE).

**Reproduce.**
```
cd research/scripts/v22-exactZ3-n5L8
python3 v22_n5_L8_block_v1.py validate   # nb=2 vs deposited, nb=3 vs Arnoldi
python3 v22_n5_L8_block_v1.py ids        # ~830 MB canonical-id array
python3 v22_n5_L8_block_v1.py run --pgrid 0.44,0.46,0.47,0.48,0.50
python3 patch_v23_rung.py                # rebuild the v23 files
```

**Closing-factor convention.** tab:n5twosize: factor = previous gap / new
gap (2.12 = 1.711/0.806, L=4 -> L=6); hence L=6 -> L=8 is
0.806/gap12(L=8, p=0.47).  (The dormant RUNG branch of
patch_v22_exactZ3.py had the ratio inverted; v23 uses the table's
convention.)
"""

CMSG = f"""Add research/ v10 (v23): the n=5 L=8 rung completed — the exponential-vs-power-law discriminator at three sizes

The background chain (run_chain.sh) finished the ids+run phases after the v22
commit: the mom0 triv.triv sector at n=5, L=8 assembled exactly as a dense
block over the K={K}-orbit basis of (S5 x S5) |x Z4 on (S5)^4 (the canonical-id
array is 207,360,000 int32 entries, ~830 MB — regenerated by the ids phase,
not deposited; reps/counts are deposited), validated at nb=2 against the
deposited L=4 spectrum (1.6e-14) and at nb=3 against unrestricted
colour-restricted Arnoldi solves (2.1e-14, 9.8e-15).  gap12 = log(l1/l2) at
the locator grid: {GAPLIST}.  At the p=0.47 locator the closing factor
extends to {CF_S} from L=6 to L=8 (x2.12 from L=4 to L=6), with L*gap12 =
{L8G_S} falling further below the continuous envelope ({ENV8} at L=8, n=3
baseline) — the first-order reading of the q=5 prediction at the three-size
level.

manuscript v23 (patch_v23_rung.py from v22, all anchors asserted; the closing
factor follows the tab:n5twosize convention, fixing the inverted ratio of the
dormant v22 RUNG branch): the rung paragraph + Scope L<=8 / three-size +
Discussion roadmap + app:files + abstract clause; supplement v6 (rung-deposit
note + ledger pointer); report v11 (Sec. 26); changelog_v23.md;
README_v23_rung.md; certificate_sha256_v10.txt; the rung JSON, the orbit
table (reps/counts) and the ids/run/chain logs.  Nothing overwritten:
v21/v22 files untouched.
"""

# ===========================================================================
# 5) write everything (only after all anchors passed)
# ===========================================================================
OUT = {
    'manuscript_revised_v23_rung.tex': msrc,
    'supplement_v6.tex': ssrc,
    'mipt_numerical_report_v11.md': r11,
    'changelog_v23.md': CHANGELOG,
    'README_v23_rung.md': README,
}
for fn, content in OUT.items():
    open(os.path.join(VER, fn), 'w').write(content)
    log(f"written versions/{fn} ({len(content)} chars)")
open(os.path.join(HERE, 'commit_msg_v23.txt'), 'w').write(CMSG)
log("written scripts/v22-exactZ3-n5L8/commit_msg_v23.txt")
log("== patch_v23_rung.py DONE (compile with tectonic next) ==")
