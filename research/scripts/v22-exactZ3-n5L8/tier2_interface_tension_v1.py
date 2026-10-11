#!/usr/bin/env python3
r"""tier2_interface_tension_v1.py -- the Tier-2 interface-tension round:
the sigma_eff(L) = Sigma - A/L finite-size fits on the deposited size
ladders, executed from the deposits of record (session 2026-10-12).

This is the computation the v32 registered conditional points at: the
manuscript's Table tab:closingrates carries sigma_eff at
  n=3: intervals 4->6, 6->8, 8->10   (three points)
  n=4: intervals 4->6, 6->8          (two points)
  n=5: intervals 4->6, 6->8          (two points)
and states the completion test qualitatively ("if the closing is
genuinely exponential, the fourth size will show sigma_eff stabilizing
at a positive interface tension; if a slowly decaying power law, it
will continue to decay").  This round makes the test quantitative and
adds the two ladder cells that were already deposited but never used:

  NEW  n=3, L=12 : gap12 at p=0.30 from n3_annealed_scan_block12.json
                  (dim_k0 = 7826, the manuscript's anchor) -- giving a
                  FOURTH sigma_eff interval (10->12);
  NEW  n=4, L=10 : gap12 at p=0.38 from n4_L10_scan_v2.json -- giving
                  a THIRD sigma_eff interval (8->10).

Every published ladder cell is re-extracted from its named deposit and
validated against the published table values before use.

Definitions (per consecutive-size pair L -> L+2, midpoint Lbar):
  sigma_eff = ln[gap12(L)/gap12(L+2)]/2       (exponential reading;
              gap ~ e^{-sigma L} gives sigma_eff -> Sigma, the
              interface tension in units of the ring length)
  alpha_eff = ln[gap12(L)/gap12(L+2)]/ln[(L+2)/L]   (power-law
              reading; gap ~ L^{-alpha} gives alpha_eff -> alpha)
  ansatz:   sigma_eff(Lbar) = Sigma - A/Lbar + O(1/Lbar^2)

Fits delivered:
  n=3 (4 points): Sigma_hat +- cov error + leave-one-out spread;
  n=4 (3 points): Sigma_hat +- cov error (1 dof);
  n=5 (2 points): no fit -- the registered quantitative discriminator
      for the L=10 point (the power-law-continuation prediction, the
      flip threshold at which the 3-point fit turns positive, and the
      alpha_eff cross-reading);
  envelope fits: L*gap12 -> asymptote (three forms) for n=3 (5 points,
      incl. an out-of-sample L=12 prediction check), n=4 (4 points,
      marginal-log caveat), n=5 (sequence only);
  alpha_eff asymptote fits for n=3/n=4 (the saturating-envelope value).

Honesty notes carried in the deposit: the ansatz is a first-order
finite-size form and the accessible sizes sit in the crossover region
(the q>4 Potts systems' pre-asymptotic window); the negative Sigma
values returned at n=3/n=4 are the misspecification signature, not
negative tensions; the n=5 discriminator is a 2-point extrapolation
registered as a prediction, not a measurement; the manuscript is NOT
edited (v32's registered conditional stands; this deposit quantifies
its completion test).
"""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
R = ROOT / 'research' / 'results'
OUT = R / 'tier2_interface_tension_v1.json'


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(rel: str):
    return json.loads((R / rel).read_text())


# ---------------------------------------------------------------- dataset
print('== dataset: every ladder cell re-extracted from its deposit ==')
dataset = {}


def cell(n, L, rel, p, mode, note):
    d = load(rel)
    rows = ([r for r in d if abs(r['p'] - p) < 1e-9 and r.get('L') == L]
            if mode != 'min' else [r for r in d if r.get('L') == L])
    assert rows or mode == 'min', f'{rel}: p={p} L={L} not on grid'
    if mode == 'eps':
        r = rows[0]
        g = math.log(r['lam1'] / r['lam_eps'])
    elif mode == 'triv3':
        t = rows[0]['triv3']
        g = math.log(t[0] / t[1])
    elif mode == 'field':
        g = rows[0]['gap12']
    elif mode == 'min':
        g = min(r['gap12'] for r in d)
        p = min(d, key=lambda r: r['gap12'])['p']
    dataset.setdefault(n, {'locator_p': p, 'gaps': {}})['gaps'][L] = {
        'gap12': g, 'deposit': f'research/results/{rel}',
        'sha256': sha(R / rel), 'note': note}
    return g


# n=3 (p=0.30): the deposited n=3 chain
for L in (4, 6, 8, 10):
    cell(3, L, 'v17-annealed-n3/n3_annealed_scan_dense.json', 0.30, 'eps',
         'dense annealed scan, exact p=0.30 grid point')
cell(3, 12, 'v17-annealed-n3/n3_annealed_scan_block12.json', 0.30, 'eps',
     'NEW: the L=12 block scan (dim_k0=7826, the manuscript anchor), '
     'exact p=0.30 grid point')

# n=4 (p=0.38): the eps scans + the top-up + the L=10 scan
cell(4, 4, 'v18-n4n5-smc/n4_eps_L4_v1.json', 0.38, 'triv3',
     'eps scan, exact p=0.38 grid point')
cell(4, 6, 'v18-n4n5-smc/n4_eps_L6_v1.json', 0.38, 'triv3',
     'eps scan, exact p=0.38 grid point')
cell(4, 8, 'v22-exactZ3-n5L8/v22_n4_eps_topup.json', 0.38, 'triv3',
     'the deposited lambda_eps top-up (the Table IV provenance)')
cell(4, 10, 'v19-n5L6-nofreeze/n4_L10_scan_v2.json', 0.38, 'eps',
     'NEW: the L=10 scan, exact p=0.38 grid point')

# n=5 (locator grid + the refined locator minimum at L=8)
cell(5, 4, 'v18-n4n5-smc/n5_annealed_scan_v1.json', 0.47, 'triv3',
     'annealed scan, exact p=0.47 grid point')
cell(5, 6, 'v19-n5L6-nofreeze/n5_L6_scan_v2.json', 0.47, 'field',
     'L=6 scan v2 (gap12 field), exact p=0.47 grid point')
cell(5, 8, 'v22-exactZ3-n5L8/v25_n5_L8_finegrid.json', None, 'min',
     'the finer locator grid minimum (p=0.465; the Table IV provenance)')

# validation against the published v32 tables
PUB_GAP = {3: {4: 2.147, 6: 1.185, 8: 0.816, 10: 0.621},
           4: {4: 1.919, 6: 0.990, 8: 0.645},
           5: {4: 1.711, 6: 0.806, 8: 0.480}}
ok = True
for n, tab in PUB_GAP.items():
    for L, v in tab.items():
        g = dataset[n]['gaps'][L]['gap12']
        m = abs(g - v) <= 6e-4
        ok &= m
        print(f'  n={n} L={L}: gap12 = {g:.6f} vs published {v:.3f} '
              f'[{"OK" if m else "MISMATCH"}]')
assert ok, 'published-value validation failed'

# ------------------------------------------------------- sigma/alpha ladders
print('\n== effective closing rates (interval midpoints) ==')
ladders = {}
for n in (3, 4, 5):
    gaps = dataset[n]['gaps']
    Ls = sorted(gaps)
    rows = []
    for L1, L2 in zip(Ls, Ls[1:]):
        g1, g2 = gaps[L1]['gap12'], gaps[L2]['gap12']
        d = math.log(g1 / g2)
        rows.append({'interval': f'{L1}->{L2}', 'Lbar': (L1 + L2) / 2,
                     'sigma_eff': d / (L2 - L1),
                     'alpha_eff': d / math.log(L2 / L1),
                     'closing': g1 / g2})
    ladders[n] = rows
    for r in rows:
        print(f"  n={n} {r['interval']}: sigma_eff={r['sigma_eff']:.4f} "
              f"alpha_eff={r['alpha_eff']:.4f} closing=x{r['closing']:.3f}")

# validation against Table tab:closingrates (v32 lines 878-883)
PUB_SIG = {(3, '4->6'): 0.297, (3, '6->8'): 0.187, (3, '8->10'): 0.137,
           (4, '4->6'): 0.331, (4, '6->8'): 0.214,
           (5, '4->6'): 0.376, (5, '6->8'): 0.259}
PUB_ALP = {(3, '4->6'): 1.466, (3, '6->8'): 1.297, (3, '8->10'): 1.224,
           (4, '4->6'): 1.632, (4, '6->8'): 1.489,
           (5, '4->6'): 1.857, (5, '6->8'): 1.802}
for (n, iv), v in PUB_SIG.items():
    r = [x for x in ladders[n] if x['interval'] == iv][0]
    assert abs(r['sigma_eff'] - v) <= 1e-3, (n, iv, r['sigma_eff'], v)
for (n, iv), v in PUB_ALP.items():
    r = [x for x in ladders[n] if x['interval'] == iv][0]
    # tolerance 4e-3: the published alpha_eff entries were computed
    # from the 3-decimal rounded table gaps (e.g. ln(0.816/0.621)),
    # which shifts the third decimal vs the full-precision re-extract
    assert abs(r['alpha_eff'] - v) <= 4e-3, (n, iv, r['alpha_eff'], v)
print('  published Table tab:closingrates validation: ALL OK')


# ------------------------------------------------------------ the fits
def fit_sigma(points):
    r"""LSQ fit y = Sigma - A/Lbar on [(Lbar, y)].  Returns dict."""
    Lb = np.array([p[0] for p in points], float)
    y = np.array([p[1] for p in points], float)
    X = np.column_stack([np.ones_like(Lb), -1.0 / Lb])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - 2
    rss = float(resid @ resid)
    cov = np.linalg.inv(X.T @ X)
    s2 = rss / dof if dof > 0 else None
    sSigma = math.sqrt(s2 * cov[0, 0]) if s2 is not None else None
    return {'Sigma': float(beta[0]), 'A': float(beta[1]),
            'sSigma': sSigma, 'rss': rss, 'dof': dof,
            'points': [[float(a), float(b)] for a, b in zip(Lb, y)],
            'residuals': [float(r) for r in resid]}


def fit_alpha(points):
    r"""LSQ fit alpha_eff = a_inf + B/Lbar (the power-law reading)."""
    Lb = np.array([p[0] for p in points], float)
    y = np.array([p[1] for p in points], float)
    X = np.column_stack([np.ones_like(Lb), 1.0 / Lb])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - 2
    s2 = float(resid @ resid) / dof if dof > 0 else None
    cov = np.linalg.inv(X.T @ X)
    return {'alpha_inf': float(beta[0]), 'B': float(beta[1]),
            's_alpha_inf': math.sqrt(s2 * cov[0, 0]) if s2 else None,
            'dof': dof}


def fit_envelope(Ls, ys, form):
    r"""LSQ fit L*gap = a + b*f(L); returns asymptote a +- s(a)."""
    L = np.array(Ls, float)
    y = np.array(ys, float)
    f = {'1/L': 1.0 / L, '1/L2': 1.0 / L ** 2,
         'lnL/L': np.log(L) / L}[form]
    X = np.column_stack([np.ones_like(L), f])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - 2
    s2 = float(resid @ resid) / dof if dof > 0 else None
    cov = np.linalg.inv(X.T @ X)
    return {'form': f'a + b/{form}', 'a': float(beta[0]),
            'b': float(beta[1]),
            's_a': math.sqrt(s2 * cov[0, 0]) if s2 else None,
            'dof': dof}


print('\n== Tier-2 fits: sigma_eff(Lbar) = Sigma - A/Lbar ==')
fits = {}
for n in (3, 4):
    pts = [(r['Lbar'], r['sigma_eff']) for r in ladders[n]]
    f = fit_sigma(pts)
    fits[n] = f
    print(f"  n={n}: Sigma = {f['Sigma']:+.4f}" +
          (f" +- {f['sSigma']:.4f}" if f['sSigma'] else '') +
          f", A = {f['A']:+.3f} (dof={f['dof']}, rss={f['rss']:.2e})")
    if n == 3:  # leave-one-out
        loos = []
        for k in range(len(pts)):
            sub = pts[:k] + pts[k + 1:]
            loos.append(fit_sigma(sub)['Sigma'])
        f['loo_Sigma'] = loos
        print(f"        leave-one-out Sigma: "
              f"{['%+.4f' % s for s in loos]} "
              f"(spread {max(loos) - min(loos):.4f})")
    # geometric-midpoint robustness
    gpts = [(math.sqrt(r['interval'] and
                       float(r['interval'].split('->')[0]) *
                       float(r['interval'].split('->')[1])),
             r['sigma_eff']) for r in ladders[n]]
    fg = fit_sigma(gpts)
    f['geo_midpoint_Sigma'] = fg['Sigma']
    print(f"        geometric-midpoint refit: Sigma = {fg['Sigma']:+.4f}")

# alpha_eff asymptotes
print('\n== alpha_eff asymptotes (alpha_eff = a_inf + B/Lbar) ==')
alpha_fits = {}
for n in (3, 4):
    pts = [(r['Lbar'], r['alpha_eff']) for r in ladders[n]]
    fa = fit_alpha(pts)
    alpha_fits[n] = fa
    print(f"  n={n}: alpha_inf = {fa['alpha_inf']:.3f}" +
          (f" +- {fa['s_alpha_inf']:.3f}" if fa['s_alpha_inf'] else '') +
          f" (dof={fa['dof']})")
a5 = fit_alpha([(r['Lbar'], r['alpha_eff']) for r in ladders[5]])
alpha_fits[5] = a5
print(f"  n=5 (2 points, no dof): alpha_inf = {a5['alpha_inf']:.3f} "
      f"-- the power-law reading's implied exponent, registered not "
      f"fitted")

# ------------------------------------------------- n=5 registered discriminator
print('\n== n=5: the registered quantitative discriminator for L=10 ==')
r46, r68 = ladders[5][0], ladders[5][1]
c1 = r46['sigma_eff'] * r46['Lbar']
c2 = r68['sigma_eff'] * r68['Lbar']
cbar = 0.5 * (c1 + c2)
pred_pl = cbar / 9.0
# flip threshold: Sigma_hat(x) is affine in the third point x at Lbar=9
pts = [(5, r46['sigma_eff']), (7, r68['sigma_eff'])]


def Sigma_with(x):
    return fit_sigma(pts + [(9.0, x)])['Sigma']


s0, s1 = Sigma_with(0.0), Sigma_with(1.0)
x_flip = -s0 / (s1 - s0)
disc = {'c_products': {'4->6': c1, '6->8': c2},
        'c_mean': cbar, 'c_spread': abs(c1 - c2),
        'power_law_prediction_sigma_eff_8to10': pred_pl,
        'sigma_eff_8to10_flip_threshold': x_flip,
        'note': ('sigma_eff(8->10) at or below the power-law '
                 'continuation (~%.3f) keeps the 3-point Sigma fit '
                 'non-positive; at or above the flip threshold (%.3f) '
                 'it turns positive -- the quantitative form of the '
                 'v32 registered conditional' % (pred_pl, x_flip))}
print(f"  sigma_eff*Lbar: {c1:.4f} (4->6), {c2:.4f} (6->8) "
      f"[spread {abs(c1 - c2):.4f}]")
print(f"  power-law continuation: sigma_eff(8->10) ~ {pred_pl:.4f} "
      f"(c = {cbar:.3f} +- {abs(c1 - c2) / 2:.3f})")
print(f"  flip threshold: sigma_eff(8->10) >= {x_flip:.4f} turns the "
      f"3-point Sigma fit positive")
for lab, x in [('power-law continuation', pred_pl),
               ('flip threshold', x_flip)]:
    # the gap12(L=10) each reading implies, and its alpha_eff
    g8 = dataset[5]['gaps'][8]['gap12']
    g10 = g8 * math.exp(-2 * x)
    print(f"    {lab}: implies gap12(L=10) = {g10:.4f}, "
          f"alpha_eff(8->10) = {2 * x / math.log(10 / 8):.3f}")
disc['alpha_eff_readings'] = {
    'power_law': 2 * pred_pl / math.log(10 / 8),
    'flip': 2 * x_flip / math.log(10 / 8)}
disc['caveat'] = ('the two readings sit ~0.007 apart in sigma_eff '
                  '(~3% of the value): a single L=10 point at the '
                  'threshold is ambiguous on its own; the decisive '
                  'observable is the TREND of sigma_eff across the '
                  'intervals (and, per Tier 3, a fifth size)')

# ------------------------------------------------------------ envelopes
print('\n== envelopes: L*gap12 -> asymptote ==')
env = {}
for n in (3, 4):
    gaps = dataset[n]['gaps']
    Ls = sorted(gaps)
    ys = [L * gaps[L]['gap12'] for L in Ls]
    env[n] = {'L': Ls, 'Lgap': ys, 'fits': {}}
    for form in ('1/L', '1/L2', 'lnL/L'):
        f = fit_envelope(Ls, ys, form)
        env[n]['fits'][form] = f
        print(f"  n={n} ({'L=' + ','.join(map(str, Ls))}): "
              f"{f['form']}: a = {f['a']:.3f}" +
              (f" +- {f['s_a']:.3f}" if f['s_a'] else '') +
              f" (dof={f['dof']})")
# out-of-sample check: fit n=3 on L=4..10, predict L=12
Ls4 = [4, 6, 8, 10]
ys4 = [L * dataset[3]['gaps'][L]['gap12'] for L in Ls4]
oos = {}
for form in ('1/L', '1/L2', 'lnL/L'):
    f = fit_envelope(Ls4, ys4, form)
    L12, g12 = 12, dataset[3]['gaps'][12]['gap12']
    fx = {'1/L': 1 / L12, '1/L2': 1 / L12 ** 2,
          'lnL/L': math.log(L12) / L12}[form]
    pred = f['a'] + f['b'] * fx
    oos[form] = {'predicted': pred, 'deposited': L12 * g12}
    print(f"  n=3 out-of-sample (fit L=4..10, predict L=12): "
          f"{f['form']}: {pred:.3f} vs deposited {L12 * g12:.3f} "
          f"(diff {pred - L12 * g12:+.3f})")
env[3]['out_of_sample_L12'] = oos
env[5] = {'L': sorted(dataset[5]['gaps']),
          'Lgap': [L * dataset[5]['gaps'][L]['gap12']
                   for L in sorted(dataset[5]['gaps'])],
          'note': 'sequence only: steeply declining, not extrapolable '
                  '(both asymptotic readings send it to 0)'}
cft = 2 * math.pi * (4.0 / 5.0)
env['cft_reference'] = {
    'value': cft,
    'statement': ('the q=3 Potts thermal scaling dimension x_eps = 4/5 '
                  'gives 2*pi*x_eps = %.3f; the n=3 extrapolated '
                  'asymptotes are compared against it as a consistency '
                  'observation (interpretive, non-load-bearing: the '
                  'operator identification is the natural reading of a '
                  'two-phase thermal splitting)' % cft)}
for form in ('1/L', '1/L2', 'lnL/L'):
    a = env[3]['fits'][form]['a']
    print(f"  n=3 {form} asymptote {a:.3f} vs 2*pi*x_eps(4/5) = "
          f"{cft:.3f} (diff {a - cft:+.3f})")

# ---------------------------------------------------------------- deposit
report = {
    'round': 'Tier-2 interface-tension fits (research v23)',
    'date': '2026-10-12',
    'input_manuscript': 'research/versions/manuscript_revised_v32.tex '
                        '(Tables tab:n5twosize, tab:closingrates)',
    'dataset': dataset,
    'ladders': ladders,
    'sigma_fits': fits,
    'alpha_fits': alpha_fits,
    'n5_discriminator': disc,
    'envelopes': env,
    'honesty': [
        'the sigma_eff(L) = Sigma - A/L ansatz is the first-order '
        'finite-size form; the accessible sizes (Lbar <= 11) sit in '
        'the crossover region the manuscript itself flags',
        'the fits return Sigma = -0.05 at BOTH n=3 and n=4: negative '
        'values are the ansatz-misspecification signature at these '
        'sizes, not negative tensions; what the fits exclude is any '
        'positive interface tension at this order',
        'the n=5 discriminator is a 2-point extrapolation registered '
        'as a prediction with numbers, not a measurement; the '
        'power-law continuation and the flip threshold sit ~3% apart '
        'in sigma_eff, so a single L=10 point at the threshold is '
        'ambiguous -- the trend across intervals (and Tier 3) carries '
        'the decision',
        'the n=3 L=12 and n=4 L=10 cells are not new computations: '
        'they are deposited results newly used (block12 scan; L=10 '
        'scan v2)',
        'the manuscript is NOT edited: v32\'s registered conditional '
        'stands; this deposit quantifies its completion test',
    ],
}
OUT.write_text(json.dumps(report, indent=1) + '\n')
print(f'\nwritten: {OUT}')
print('ALL VALIDATIONS PASS')
