#!/usr/bin/env python3
r"""v32_tier1_L10_dimension.py -- Tier-1 feasibility probe (v32 round).

Computes the exact dimension of the momentum-zero colour-trivial
(mom0 triv.triv) sector of the n=5 annealed transfer problem at L=10:
the orbit count of G = (S_5 x S_5) . Z_5 acting on (S_5)^5, where
(a, b) in S_5 x S_5 acts componentwise as sigma_i -> a sigma_i b and
the ring rotation acts as sigma_i -> sigma_{i+k} (k in Z_m, m = L/2).

This is the same orbit-count specification the manuscript gives for
the L=8 rung: "dimension 3865 (the orbit count of
(S_5 x S_5) rt Z_4 on (S_5)^4)" (manuscript_revised_v31.tex, Sec II H,
the L=8 rung paragraph).  Validation levels:

(i)  the Burnside-by-conjugacy-class formula is cross-checked against
     direct BFS orbit enumeration on (S_n)^m for small (n, m);
(ii) the n=5, m=4 value must reproduce the deposited 3865 exactly.

Method (Burnside over classes).  For the element (a, b, rho^k):
fixed points satisfy sigma_i = a sigma_{i+k} b for all i.  With
g = gcd(m, k), t = m/g, the index cycles have length t and the
per-cycle solution count is

    f_t(a, b) = n! / |cl(pow_t(a))|   if type(pow_t(a)) == type(pow_t(b))
                0                       otherwise,

where pow_t maps a conjugacy class to the class of its t-th power
(a cycle of length l becomes gcd(l, t) cycles of length l/gcd(l, t)),
and |fix| = f_t(a,b)^g (k = 0 included, with t = 1, g = m).  The
class-level formula for f_t follows from the conjugation-equivariance
and uniformity of the t-th-power map on classes.

Output: research/results/v32_tier1_L10_dimension.json
"""
import json
import sys
from collections import deque
from math import factorial, gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # repo root
RESULTS = ROOT / 'research' / 'results'

# ----------------------------------------------------------------------
# permutation utilities (tuples of images, 0-indexed)
# ----------------------------------------------------------------------


def perms_of(n):
    """All permutations of range(n) as tuples."""
    out = []

    def rec(prefix, used):
        if len(prefix) == n:
            out.append(tuple(prefix))
            return
        for v in range(n):
            if not used[v]:
                used[v] = True
                rec(prefix + (v,), used)
                used[v] = False

    rec((), [False] * n)
    return out


def compose(p, q):
    """p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    r = [0] * len(p)
    for i, v in enumerate(p):
        r[v] = i
    return tuple(r)


def cycle_type(p):
    """Sorted-descending tuple of cycle lengths."""
    n = len(p)
    seen = [False] * n
    lens = []
    for i in range(n):
        if not seen[i]:
            j, ln = i, 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                ln += 1
            lens.append(ln)
    return tuple(sorted(lens, reverse=True))


def class_size(n, ctype):
    from collections import Counter
    cnt = Counter(ctype)
    s = factorial(n)
    for length, mult in cnt.items():
        s //= (length ** mult) * factorial(mult)
    return s


def pow_type(ctype, t):
    """Cycle type of the t-th power of a permutation of type ctype."""
    from collections import Counter
    cnt = Counter(ctype)
    out = Counter()
    for length, mult in cnt.items():
        d = gcd(length, t)
        out[length // d] += mult * d
    return tuple(sorted((l for l, m in out.items()
                         for _ in range(m)), reverse=True))


# ----------------------------------------------------------------------
# Burnside orbit count for G = {(a,b) . rho^k} on (S_n)^m
# ----------------------------------------------------------------------


def orbits_burnside(n, m):
    """Exact orbit count of (S_n x S_n) . Z_m (componentwise a.x.b,
    rotation rho^k) on (S_n)^m, by conjugacy classes."""
    reps = {}
    for p in perms_of(n):
        reps.setdefault(cycle_type(p), p)
    classes = [(ctype, rep, class_size(n, ctype)) for ctype, rep in reps.items()]
    nfact = factorial(n)
    total = 0
    terms = {}
    for k in range(m):
        g = gcd(m, k)
        t = m // g
        # precompute pow_t classes
        powmap = {}
        for ctype, rep, size in classes:
            pt = pow_type(ctype, t)
            powmap[ctype] = (pt, class_size(n, pt))
        s_k = 0
        for ctype_a, rep_a, size_a in classes:
            pta, cl_size_pta = powmap[ctype_a]
            for ctype_b, rep_b, size_b in classes:
                if powmap[ctype_b][0] != pta:
                    continue
                f = nfact // cl_size_pta
                s_k += size_a * size_b * (f ** g)
        terms[f'k={k}'] = s_k
        total += s_k
    group_order = nfact * nfact * m
    assert total % group_order == 0, (n, m, total, group_order)
    return total // group_order, terms


# ----------------------------------------------------------------------
# BFS orbit enumeration (independent validation for small n, m)
# ----------------------------------------------------------------------


def orbits_bfs(n, m):
    perms = perms_of(n)
    # generators: adjacent transpositions on the left and on the right,
    # plus the ring rotation
    transps = []
    for i in range(n - 1):
        t = list(range(n))
        t[i], t[i + 1] = t[i + 1], t[i]
        transps.append(tuple(t))
    states = {}
    for x in _all_tuples(perms, m):
        states[x] = False
    orbits = 0
    rot = tuple(range(1, m)) + (0,)
    for start in states:
        if states[start]:
            continue
        orbits += 1
        dq = deque([start])
        states[start] = True
        while dq:
            x = dq.popleft()
            for gen in _neighbours(x, transps, rot, n, m):
                if not states[gen]:
                    states[gen] = True
                    dq.append(gen)
    return orbits


def _all_tuples(perms, m):
    if m == 0:
        yield ()
        return
    for head in perms:
        for tail in _all_tuples(perms, m - 1):
            yield (head,) + tail


def _neighbours(x, transps, rot, n, m):
    # left mult, right mult (componentwise), rotation
    for t in transps:
        yield tuple(compose(t, xi) for xi in x)
        yield tuple(compose(xi, t) for xi in x)
    if m > 1:
        yield tuple(x[rot[i]] for i in range(m))


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------

if __name__ == '__main__':
    log = []

    def say(msg):
        print(msg)
        log.append(msg)

    say('== Tier-1 feasibility probe: L=10 sector dimension at n=5 ==')
    say('(orbit count of (S_n x S_n) . Z_m on (S_n)^m, m = L/2)')

    # (i) formula vs BFS on small cases
    say('')
    say('-- validation (i): Burnside formula vs direct BFS enumeration --')
    for (n, m) in [(2, 2), (2, 3), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3),
                   (4, 4), (5, 2), (5, 3)]:
        bf, _ = orbits_burnside(n, m)
        bfs = orbits_bfs(n, m)
        status = 'OK' if bf == bfs else 'MISMATCH'
        say(f'  n={n} m={m}:  Burnside={bf}  BFS={bfs}  [{status}]')
        assert bf == bfs, f'validation failed at (n={n}, m={m})'
    say('  all small-case validations agree.')

    # (ii) the deposited L=8 anchor
    say('')
    say('-- validation (ii): deposited L=8 anchor (n=5, m=4) --')
    dim8, terms8 = orbits_burnside(5, 4)
    say(f'  computed (S_5 x S_5) . Z_4 on (S_5)^4 : {dim8}')
    say(f'  manuscript deposited L=8 sector dim   : 3865')
    assert dim8 == 3865, 'L=8 anchor NOT reproduced'
    say('  ANCHOR REPRODUCED (3865) -- the orbit-count model is correct.')

    # the Tier-1 number
    say('')
    say('-- the Tier-1 (L=10, n=5) sector dimension --')
    dim10, terms10 = orbits_burnside(5, 5)
    say(f'  (S_5 x S_5) . Z_5 on (S_5)^5 : {dim10}')
    say(f'  full bond-label space 120^5  : {120 ** 5}')
    say(f'  reduction factor              : {120 ** 5 // dim10}'
        f' ({(120 ** 5) / dim10:.3e})')
    dim6, _ = orbits_burnside(5, 3)
    dim4, _ = orbits_burnside(5, 2)
    say(f'  ladder: L=4 -> {dim4}, L=6 -> {dim6}, L=8 -> {dim8}, '
        f'L=10 -> {dim10}')

    # per-L growth factors (for the feasibility statement)
    say('')
    say(f'  growth L=4->6:   x{dim6 / dim4:.2f}')
    say(f'  growth L=6->8:   x{dim8 / dim6:.2f}')
    say(f'  growth L=8->10:  x{dim10 / dim8:.2f}')
    say('')
    say('  feasibility: a dense block would need '
        f'{dim10 ** 2:.2e} entries (impossible);')
    say('  a matrix-free Lanczos route on the orbit basis is the '
        'documented Tier-1 method (days-scale engineering), NOT run '
        'this session.')

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = {
        'probe': 'v32_tier1_L10_dimension.py',
        'date': '2026-10-11',
        'specification': ('orbit count of (S_n x S_5) [componentwise '
                          'a.sigma_i.b] semidirect Z_m [ring rotation] '
                          'on (S_n)^m, m = L/2'),
        'validation_bfs_small_cases': ['(2,2)', '(2,3)', '(3,2)', '(3,3)',
                                       '(3,4)', '(4,2)', '(4,3)', '(4,4)',
                                       '(5,2)', '(5,3)'],
        'anchor_L8': {'computed': dim8, 'manuscript_deposited': 3865,
                      'reproduced': True},
        'n5_ladder': {'L4': dim4, 'L6': dim6, 'L8': dim8, 'L10': dim10},
        'tier1_L10_dimension': dim10,
        'full_bond_space_L10': 120 ** 5,
        'reduction_factor': (120 ** 5) // dim10,
        'tier1_eigen_solve_run': False,
        'tier1_eigen_solve_note': ('dense assembly impossible at this '
                                   'dimension; matrix-free Lanczos on the '
                                   'orbit basis is days-scale engineering '
                                   'per the Tier-1 doctrine; registered '
                                   'conditional added to the manuscript '
                                   'in the v32 pass instead'),
        'log': log,
    }
    (RESULTS / 'v32_tier1_L10_dimension.json').write_text(
        json.dumps(out, indent=2) + '\n')
    say('')
    say(f"written: research/results/v32_tier1_L10_dimension.json")
    say("PROBE OK")
