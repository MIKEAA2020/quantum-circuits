# Numerical report — v5 (recovered-data verification)

**Manuscript:** `versions/manuscript_revised_v16_recovered.tex/.pdf` (v16; v13,
and the reconstructed v14/v15, kept unmodified). This report supersedes v4;
everything in v4 stands. The new material is the recovery and end-to-end
re-verification of the **original deposited workspace**.

**Status box:** I3 locator $p_c = 0.1597(8)$, $\nu = 1.24(7)$, $\alpha =
1.55(7)$; purification locator $p_c^{\rm purif} = 0.1601$–$0.1604$, $\nu^{\rm
purif} = 1.25(2)_{\rm stat}(6)_{\rm sys}$; exact annealed line $p_c^{(2)}(2) =
0.233810$, $p_c^{(2)}(3) = 0.459688$, $p_c^{(2)}(5) = 0.679004$. No numerical
result of the manuscript changes in v16; v16 replaces every "quoted from the
deposit" caveat by "recomputed from the recovered raw dataset".

## 8. The recovered workspace (NEW in v5)

The fuller_workspace release of the repository
(`workspace-phys2.zip`, 116 411 529 bytes, SHA-256
`15ec3a0e76b2e39fb9d152b7925db062189b7eccca0231b6f0892fdd310948d9`,
verified against the GitHub release digest) contains the **complete original
working workspace**, previously believed lost:

- `mipt_data/` — the raw I3 dataset: 192 `.npz` files, $L = 16$–$512$
  (4000/3000/2000/800/400 trajectories by size), $p = 0.12$–$0.22$,
  $475\,600$ trajectories in total;
- `mipt_data_purif/` — the purification dataset: 270 chunk files,
  $135\,000$ trajectories ($L=16$–$256$, $\tau = 0.25$–$4$);
- `mipt_data_time/`, `mipt_data_purif_bench/` — the time-growth and
  benchmark runs;
- `manuscript_revised.tex` (v13, 1218 lines) + `.pdf`, `supplement.tex`,
  every version $v5$–$v13$ in `versions/`, all analysis scripts, all
  `mipt_results/*.json`, all logs, and the two chat logs of the deposited
  session.

Consequences: (i) the v14/v15 reconstruction's caveat "raw I3 data not
recoverable" is void; (ii) every number in the reconstruction that was
"quoted from the deposit" can now be **recomputed from raw data**; (iii) the
one computation the deposited session left unfinished — item 13, the $1/N$-floor
re-run — can be completed as specified.

## 8.1 Item 13 completed: the released $1/N$-floor pipeline (the exact stopping point of the deposited session)

The deposited session died while generating the floor-fixed analysis code. Its
transform script (`mipt_v14_transform.py`) contained **three latent defects**,
now fixed in `mipt_v14_transform_v2.py` (v1 kept unmodified):

1. a stale final assertion — a naive token count that can never hold, because
   the inserted `_floor()` helper legitimately retains the legacy `1e-4`
   default and the inserted comment mentions `1e-4/1e-6`;
2. an invalid Python identifier `binds_old_1e-6` (dict key with a hyphen) in
   the floor-audit block — a syntax error;
3. a loop-variable clobbering bug: the floor-audit loop rebinds `rec` (the
   global record-time dict) to the per-file record array, crashing
   `has_t()` on the next iteration.

The corrected transform (asserted anchors, originals untouched) generates
`mipt_fss2_floorN.py` (the released module: standard errors floored at
$1/N_{\rm traj}$ per $(L,p)$ instead of the legacy $10^{-4}$/$10^{-6}$; the
Nelder–Mead `xatol=1e-6` is a tolerance and is intentionally untouched) and
`mipt_final2_rerun.py` (the full v13 pipeline with incremental JSON saves and
the v14 additions, Secs. 8–9).

**Result of the re-run on the recovered raw dataset** (318 s;
`logs/mipt_final2_rerun.log`, `mipt_results/final2_summary_floorN.json`):

- every crossing, windowed collapse, $\Delta S$ crossing, log-scaling row,
  chord fit and depth-stability row reproduces the deposited
  `final2_summary.json`;
- **`v14_comparison`: max |Δp_c| = 0, max |Δν| = 0, max |Δχ²| = 0** over all
  24 windowed collapses — the $1/N$ floor is a **provable no-op** on the
  windowed backbone, and the floor audit *explains* it: the smallest
  standard error inside any quoted window is $3.35\times10^{-3}$ bits
  (at $L=256$, $p=0.175$), two orders of magnitude above the $1/N$
  floor ($2.5$–$5\times10^{-4}$); **no window contains a floored point**
  (0/24 windows bind);
- the regenerated figure (`mipt_results/fig_final_fss_floorN.pdf`, embedded
  as `fig_final_fss_v16.pdf` in the v16 manuscript) reproduces the deposited
  figure with the same fitted dashed line ($p_c = 0.1593$ for the shown
  $t=2L$, $L\ge48$ window).

## 8.2 Seed contract re-verified (R6/E9)

`mipt_seed_recheck.py` (new file): 44 trajectories across one file per system
size $L = 16$–$512$, four $k$-values each, **including the $I_3\equiv0$
saturated file at $L=384$, $p=0.18$**. Result:
**44/44 regenerate bit-exactly** from `run_sample(L, p, rec, SP4, seed0 + k)`
with the stored `seed0` (legacy MT19937). `mipt_results/seed_recheck.json`.

## 8.3 Purification locator re-run (N2)

`mipt_purif_analysis_rerun.py` (new file; original untouched) on the
recovered 270-file dataset, bootstrap $n = 100$: **zero differences**
against the deposited `purif_summary.json` — every table entry, crossing,
collapse, frozen-$\nu$ $\Delta\chi^2$ and bootstrap value, including
$\tau=1$, $L\ge64$: $p_c = 0.16011(9)$, $\nu = 1.2499(14)$.
`mipt_results/purif_summary_rerun.json` (the deposited summary is preserved
at `versions/purif_summary_deposited.json`).

## 8.4 v14 additions on the real data (Sec. 8 of the re-run)

- $\alpha$ at the adopted $p_c = 0.1597$ (spline window $p\in[0.145,0.175]$):
  $t=4L$: $1.544(34)$ ($L\ge16$), $1.534(50)$ ($L\ge32$), $1.540(59)$
  ($L\ge48$), $1.557(67)$ ($L\ge64$); $t=2L$: $1.551(35)$, $1.541(48)$,
  $1.556(66)$, $1.586(70)$ — envelope $1.53$–$1.59$, inside the adopted
  $\alpha = 1.55(7)$.
- $s_1L^{-y}$ correction test ($y = 0.5, 1, 2$): $\Delta\mathrm{AIC} \ge
  -3.04$ (at most weakly preferred, $t=2L$, $L\ge32$ only), $|\Delta\alpha|
  \le 0.14$.
- $\chi^2$ $p$-values of the windowed collapses: $L\ge64$: $0.19$–$0.84$
  ($|x|_{\max} \le 1$), $\ge 0.40$ ($|x|_{\max} = 0.6$), $8\times10^{-6}$–
  $0.02$ ($|x|_{\max} = 1.5$, area-law-edge points).

## 8.5 The v16 manuscript

`versions/manuscript_revised_v16_recovered.tex/.pdf` (30 pp): the original
deposited v13 with the complete audit-3 v14 plan applied (E1–E9, N3, D6, N2;
`versions/patch_v16_recovered.py`, 21 asserted-anchor edits), the v15 spinor
factorisation in the proof of the closed-form-spectrum Proposition
(Prop.~\emph{spectrum}, with the $\det$/$k=\pi$ statements replacing the
inapplicable square-lattice $\rho_\varepsilon^2$ formula), the authorised
re-centring $p_c = 0.1595(10) \to 0.1597(8)$, and the recovery-verification
sentences. New labels: `prop:spectrum`, `eq:QRdef`, `eq:spectrum`,
`eq:spinor`, `rem:verification`, `app:enclosures`. New bibliography entries:
Kaufman 1949, Newell 1950, Schultz–Mattis–Lieb 1964.

## 8.6 Files produced in this round (all new; nothing overwritten)

Scripts: `mipt_v14_transform_v2.py`, `mipt_fss2_floorN.py`,
`mipt_final2_rerun.py`, `mipt_seed_recheck.py`,
`mipt_purif_analysis_rerun.py`, `daemon_run.py` (the double-fork launcher
required in this environment), `versions/patch_v16_recovered.py`.
Results: `mipt_results/final2_summary_floorN*.json`,
`mipt_results/purif_summary_rerun.json`, `mipt_results/seed_recheck.json`,
`mipt_results/fig_final_fss_floorN.{png,pdf}`.
Logs: `logs/mipt_final2_rerun.log`, `logs/mipt_seed_recheck.log`,
`logs/mipt_purif_analysis_rerun.log`.
Manuscript: `versions/manuscript_revised_v16_recovered.tex/.pdf`,
`versions/fig_final_fss_v16.pdf`.
This report: `versions/mipt_numerical_report_v5.md`; changelog
`versions/changelog_v16.md` (§R); ledger `logs/certificate_sha256_v3.txt`.
