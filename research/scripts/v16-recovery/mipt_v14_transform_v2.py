"""v14 item 13 transforms, v2 (fixes: stale final assertion; invalid binds_old_1e-6 identifier;
floor-audit rec-dict clobbering -> recw; v1 kept unmodified; new version files; originals untouched):
  mipt_fss2.py        -> mipt_fss2_floorN.py    (1/N standard-error floors instead of 1e-4/1e-6)
  mipt_final2.py      -> mipt_final2_rerun.py   (uses the floorN module, incremental JSON,
                                                 Sec. 8 v14 additions, Sec. 9 comparison)
Every anchor is asserted before any write; syntax is checked afterwards.
"""
import ast

# ---------------------------------------------------------------- mipt_fss2_floorN.py
src = open("mipt_fss2.py").read()
assert src.count("1e-4") == 2
assert src.count("1e-6") == 2  # one standard-error floor (collapse_cost) + one Nelder-Mead xatol (untouched)

anchor = "from mipt_fss import means, COL, log_slope, log_slope_interp, fit_s_collapse\n"
assert anchor in src
mach = anchor + """
# v14 item 13 (audit3): standard-error floor of 1/N_traj per (L,p) instead of the legacy
# 1e-4/1e-6 absolute floors.  set_nsamp(D) fills NSAMP; without it the legacy floor is retained.
NSAMP = {}

def set_nsamp(D):
    NSAMP.clear()
    for (L, p), (data, rec) in D.items():
        NSAMP[(L, p)] = 1.0 / len(data)

def _floor(L, p):
    return NSAMP.get((L, p), 1e-4)
"""
src = src.replace(anchor, mach, 1)

old = "e = np.array([max(np.hypot(M[(L1, p)][1], M[(L2, p)][1]), 1e-4) for p in ps])"
assert old in src
src = src.replace(old, "e = np.array([max(np.hypot(M[(L1, p)][1], M[(L2, p)][1]), max(_floor(L1, p), _floor(L2, p))) for p in ps])", 1)

old = "y = np.array([M[(L, p)][0] for p in pp]); e = np.array([max(M[(L, p)][1], 1e-4) for p in pp])"
assert old in src
src = src.replace(old, "y = np.array([M[(L, p)][0] for p in pp]); e = np.array([max(M[(L, p)][1], _floor(L, p)) for p in pp])", 1)

old = "m, se = M[(L, p)]; xs.append(x); ys.append(m); ws.append(1 / max(se, 1e-6) ** 2)"
assert old in src
src = src.replace(old, "m, se = M[(L, p)]; xs.append(x); ys.append(m); ws.append(1 / max(se, _floor(L, p)) ** 2)", 1)

old = "    D = load()\n    D = {k: v for k, v in D.items() if k[0] <= 256}"
assert old in src
src = src.replace(old, "    D = load()\n    set_nsamp(D)\n    D = {k: v for k, v in D.items() if k[0] <= 256}", 1)

src = src.replace('"""Definitive FSS analysis (v2):',
                  '"""Definitive FSS analysis (v2; v14 item 13: 1/N standard-error floors; new version file, mipt_fss2.py unchanged):', 1)
# v2 correction (the true stopping point of the deposited session): the naive count-based
# check can never hold, because the inserted comment block itself mentions "1e-4/1e-6" and
# _floor() intentionally retains the legacy 1e-4 default. The semantic check is that NO
# analysis floor site remains and the Nelder-Mead xatol is preserved:
assert src.count("1e-4") == 2 and src.count("1e-6") == 2  # comment mention + fallback / comment + xatol
assert "max(np.hypot(M[(L1, p)][1], M[(L2, p)][1]), 1e-4)" not in src  # L22 floor replaced
assert "max(M[(L, p)][1], 1e-4)" not in src                            # L37 floor replaced
assert "max(se, 1e-6)" not in src                                      # L48 floor replaced
assert "xatol=1e-6" in src and "NSAMP.get((L, p), 1e-4)" in src        # xatol kept, fallback in place
ast.parse(src)
open("mipt_fss2_floorN.py", "w").write(src)
print("wrote mipt_fss2_floorN.py")

# ---------------------------------------------------------------- mipt_final2_rerun.py
src = open("mipt_final2.py").read()

old = "from mipt_fss2 import local_crossing, fit_collapse, slope_at, collapse_cost"
assert old in src
src = src.replace(old,
                  "import mipt_fss2_floorN as _mf\n"
                  "local_crossing, fit_collapse, slope_at, collapse_cost = _mf.local_crossing, _mf.fit_collapse, _mf.slope_at, _mf.collapse_cost")

old = "D = load()\nLs_all = sorted(set(L for L, p in D)); ps_all = sorted(set(p for L, p in D))"
assert old in src
src = src.replace(old,
                  "D = load()\n_mf.set_nsamp(D)   # v14 item 13: 1/N standard-error floors\n"
                  "Ls_all = sorted(set(L for L, p in D)); ps_all = sorted(set(p for L, p in D))")

old = "T0 = time.time()"
assert old in src
src = src.replace(old,
                  'T0 = time.time()\n\n'
                  'def _save(tag="partial"):\n'
                  '    json.dump(out, open(os.path.join(OUT, "final2_summary_floorN_" + tag + ".json"), "w"), indent=1, default=float)\n'
                  '    print("   [partial save:", tag, "%.0f s" % (time.time() - T0), flush=True)\n', 1)

for line, tag in [('out["crossings"] = cr', "crossings"),
                  ('out["collapse_I3"] = coll', "collapse_I3"),
                  ('out["deltaS_crossings"] = dsr', "deltaS_crossings"),
                  ('out["log_scaling"] = lg', "log_scaling"),
                  ('out["chord_fits_p0.16"] = chord', "chord_fits"),
                  ('out["depth_stability"] = dep', "depth_stability")]:
    assert line in src, line
    src = src.replace(line, line + '\n_save("%s")' % tag, 1)

old = 'for ext in ("png", "pdf"): plt.savefig(os.path.join(OUT, f"fig_final_fss.{ext}"), dpi=150)'
assert old in src
src = src.replace(old, 'for ext in ("png", "pdf"): plt.savefig(os.path.join(OUT, f"fig_final_fss_floorN.{ext}"), dpi=150)')
old = 'print("saved", os.path.join(OUT, "fig_final_fss.{png,pdf}"))'
assert old in src
src = src.replace(old, 'print("saved", os.path.join(OUT, "fig_final_fss_floorN.{png,pdf}"))')

extra = '''
# ------------------------------------------------------------------ 8. v14: alpha at adopted p_c, s1 test, chi2 p-values, floor audit
print("\\n== 8. v14 additions: alpha at adopted p_c=0.1597, s1*L^-y AIC test, chi2 p-values, floor audit ==")
from scipy import stats as _stats
PC14 = 0.1597
v14 = {}
ps_s8 = [p for p in ps_all if 0.145 <= p <= 0.175]
arows = {}
for tf in (4.0, 2.0):
    for Lmin in (16, 32, 48, 64):
        Lset = [L for L in Ls_all if has_t(L, tf) and L >= Lmin]
        Luse = [L for L in Lset if all((L, p) in D for p in (0.15, 0.155, 0.16, 0.165, 0.17))]
        M8 = means(D, Luse, ps_s8, COL["S_half"], tf)
        a8, b8, c8 = log_slope_interp(M8, Luse, ps_s8, PC14)
        bs = [log_slope_interp(means(D, Luse, ps_s8, COL["S_half"], tf, rng), Luse, ps_s8, rng.normal(PC14, 0.0004))[0] for _ in range(NB)]
        arows["t=%gL;L>=%d" % (tf, Lmin)] = dict(alpha=float(a8), se=float(np.std(bs, ddof=1)), chi2dof=float(c8), Ls=Luse)
        print("  alpha at p_c=0.1597, t=%gL, L>=%d: %.4f +/- %.4f  chi2/dof=%.2f" % (tf, Lmin, a8, np.std(bs, ddof=1), c8))
v14["alpha_at_0.1597"] = arows
s1 = {}
for tf in (4.0, 2.0):
    for Lmin in (32, 64):
        Lset = [L for L in Ls_all if has_t(L, tf) and L >= Lmin]
        Luse = [L for L in Lset if all((L, p) in D for p in (0.15, 0.155, 0.16, 0.165, 0.17))]
        M8 = means(D, Luse, ps_s8, COL["S_half"], tf)
        xv = np.log(np.array(Luse, float))
        y8 = np.array([CubicSpline([p for p in ps_s8 if (L, p) in M8], [M8[(L, p)][0] for p in ps_s8 if (L, p) in M8])(PC14) for L in Luse])
        e8 = np.array([CubicSpline([p for p in ps_s8 if (L, p) in M8], [M8[(L, p)][1] for p in ps_s8 if (L, p) in M8])(PC14) for L in Luse])
        W8 = 1.0 / e8
        V0 = np.vstack([xv, np.ones_like(xv)]).T
        c0, *_ = np.linalg.lstsq(V0 * W8[:, None], y8 * W8, rcond=None); r0 = (V0 @ c0 - y8) * W8
        ch0 = float((r0 * r0).sum())
        for ylab, inv in (("0.5", 0.5), ("1", 1.0), ("2", 2.0)):
            V1 = np.vstack([xv, np.ones_like(xv), np.array(Luse, float) ** -inv]).T
            c1, *_ = np.linalg.lstsq(V1 * W8[:, None], y8 * W8, rcond=None); r1 = (V1 @ c1 - y8) * W8
            ch1 = float((r1 * r1).sum())
            dAIC = 2.0 * (V1.shape[1] - V0.shape[1]) - 2.0 * (ch0 - ch1)
            s1["t=%gL;L>=%d;y=%s" % (tf, Lmin, ylab)] = dict(dAIC=float(dAIC), d_alpha=float(c1[0] - c0[0]))
            print("  s1 test t=%gL L>=%d y=%s: dAIC=%+.2f  d_alpha=%+.4f" % (tf, Lmin, ylab, dAIC, c1[0] - c0[0]))
v14["s1_test"] = s1
pv = {}
for key, row in coll.items():
    dof = int(row["npts"]) - 5
    ch2 = row["chi2dof"] * dof
    pv[key] = float(_stats.chi2.sf(ch2, dof))
v14["collapse_chi2_pvalues"] = pv
minpv64 = min(v for k, v in pv.items() if "L>=64" in k)
print("  chi2 p-values of windowed collapses: min over L>=64 windows = %.3f" % minpv64)
v14["min_chi2_p_L64"] = minpv64
faudit = []
for key, row in coll.items():
    pcw, nuw = row["pc"], row["nu"]
    Lmin = int(key.split("L>=")[1].split(";")[0]); xmax = float(key.split("xmax=")[1]); tfw = float(key.split("t=")[1].split("L")[0])
    worst = None
    for L in Ls_all:
        if L < Lmin or not has_t(L, tfw): continue
        for p in ps_use:
            if (L, p) not in D: continue
            xw = (p - pcw) * L ** (1.0 / nuw)
            if abs(xw) > xmax: continue
            data, recw = D[(L, p)]; tw = int(round(tfw * L)); iit = list(recw).index(tw)
            sew = float(data[:, iit, COL["I3"]].std(ddof=1) / np.sqrt(len(data)))
            Nw = len(data); flw = 1.0 / Nw
            if worst is None or sew < worst[0]:
                worst = (sew, L, p, Nw, flw)
    faudit.append(dict(window=key, min_se=worst[0], at="L=%d,p=%g" % (worst[1], worst[2]), N=worst[3], floor_1N=worst[4],
                       binds_old_1em6=bool(worst[0] < 1e-6), binds_new_1N=bool(worst[0] < worst[4])))
    print("  floor audit %s: min se in window = %.2e (L=%d, p=%g), 1/N = %.2e -> binds old 1e-6: %s, binds new 1/N: %s"
          % (key, worst[0], worst[1], worst[2], worst[4], worst[0] < 1e-6, worst[0] < worst[4]))
v14["floor_audit"] = faudit
out["v14"] = v14
_save("v14")

# ------------------------------------------------------------------ 9. comparison with the v13 run
try:
    oldj = json.load(open(os.path.join(OUT, "final2_summary.json")))
    cmp9 = {}
    for key, row in coll.items():
        o = oldj["collapse_I3"][key]
        cmp9[key] = dict(dpc=row["pc"] - o["pc"], dnu=row["nu"] - o["nu"], dchi2=row["chi2dof"] - o["chi2dof"])
    out["v14_comparison"] = dict(max_abs_dpc=max(abs(v["dpc"]) for v in cmp9.values()),
                                 max_abs_dnu=max(abs(v["dnu"]) for v in cmp9.values()),
                                 max_abs_dchi2=max(abs(v["dchi2"]) for v in cmp9.values()),
                                 note="0 => windowed numbers unchanged by the 1/N floor")
    print("  comparison vs final2_summary.json: max |dpc| = %.3e, max |dnu| = %.3e, max |dchi2| = %.3e"
          % (out["v14_comparison"]["max_abs_dpc"], out["v14_comparison"]["max_abs_dnu"], out["v14_comparison"]["max_abs_dchi2"]))
except Exception as e:
    out["v14_comparison"] = dict(error=str(e))
    print("  comparison failed:", e)
_save("v14_comparison")
'''

old = 'json.dump(out, open(os.path.join(OUT, "final2_summary.json"), "w"), indent=1, default=float)\nprint(f"saved {OUT}/final2_summary.json  ({time.time()-T0:.0f} s)")'
assert old in src
src = src.replace(old, extra + '\njson.dump(out, open(os.path.join(OUT, "final2_summary_floorN.json"), "w"), indent=1, default=float)\nprint(f"saved {OUT}/final2_summary_floorN.json  ({time.time()-T0:.0f} s)")')

src = src.replace('"""Definitive finite-size-scaling analysis of the quenched Clifford-brickwork MIPT data (all scans A-D).',
                  '"""v14 rerun of mipt_final2.py (item 13): identical pipeline with 1/N standard-error floors via mipt_fss2_floorN, incremental JSON, v14 additions (Secs. 8-9). Original mipt_final2.py unchanged.')
ast.parse(src)
open("mipt_final2_rerun.py", "w").write(src)
print("wrote mipt_final2_rerun.py")
