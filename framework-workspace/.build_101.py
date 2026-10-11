src = open('formalism-v10.1.md').read()
ops = []
def rep(old, new, note, cnt=1):
    global src
    a = src.count(old)
    assert a == cnt, f"exp {cnt} got {a} [{note}]: {old[:70]!r}"
    src = src.replace(old, new, cnt)
    ops.append(note)

# B1 DP1 watch-list de-triadicized (gpt)
rep('Watch-list: three generations, hierarchy problem, dark sector — each expected to resolve as the *other pole* of a known structure.',
    'Watch-list: hierarchy problem, dark sector — each expected to resolve as the *other pole* of a known structure. **v10.1 (gpt consistency edit): three generations is *removed from this watch-list*** — triadic structures are honestly outside the necessary template (P4\'s species clause); it stays on record as control fixture **Ctl-C2** (expected-fail), not as an expected binary.',
    'B1-DP1')

# B2 RP13.3 tier-clarification (gpt)
rep('with no swampland-margin explanation.',
    '''with no swampland-margin explanation. *v10.1 (gpt tier-clarification, ADJ-3.5):* the three consistency-meanings stay distinct — logical consistency ≠ EFT-consistency ≠ compatibility with *specified* quantum-gravity requirements; swampland claims concern the third only, and **an atypical-but-admissible model is not thereby a swampland model**: channel (A) *exclusion* claims run grammar-tier, scoped per problem as Γ ⊢ C(θ) (a Γ-countermodel defeats the conjecture; observational disagreement tests the assumption package), while channel (B) typicality governs parameter **values** (J6-horn-2), never what counts as an exclusion.''',
    'B2-swamp')

# B3 kernel μ-computability clause (gpt)
rep('the module retires to illustrative and P15 loses default status (RP8 row; muse sanction).',
    '''the module retires to illustrative and P15 loses default status (RP8 row; muse sanction). **v10.1 (gpt μ-computability clause):** the measure must be an actually computable object on the restricted space — for records R with 0 < μ(R) < ∞, P_μ(E|R) = μ(E∩R)/μ(R) must be calculable in the declared toy landscape, with encoding/cutoff sensitivity published; until one such instance ships, P15 receives *no* explanatory credit from this module. The observer reference class is a declared research output (N4's self-modeling invariants define it), never a stipulation (glm2). Part II operates on M₀ with gpt's index-discipline (S⊨φ / T⊨¬φ indices retained); results needing M∖M₀ are tagged [Uncomputable-Illustrative].''',
    'B3-mu')

# B4 RP11b Γ-format (gpt)
rep('advantage-over-baseline is the kicker in the charter metric.',
    'advantage-over-baseline is the kicker in the charter metric. Every engine claim is also stated per-problem as **Γ ⊢ C(θ)** — model class, assumptions Γ, dimensionless observables θ, proposed constraint C — so a Γ-countermodel defeats the conjecture mathematically and observational disagreement tests the whole assumption package (gpt).',
    'B4-gamma')

# B5 W5 standing counters (glm2)
w5 = [l for l in src.split('\n') if l.startswith('- **W5 — Annual re-audit.**')]
assert len(w5) == 1
rep(w5[0], w5[0] + ' **v10.1:** the standing counters ride every annual re-audit — **J5 yield-tally** (yielded discharges vs recognition-calibrations; currently 0 / 3+), **J7 bridge counter** (proposed / survived / killed = 0/0/0), **J6 re-score** at each leading-candidate status change (glm2), and the engine/benchmark score-line per W3-v10.',
    'B5-W5')

# B6 W3 benchmark-vs-spec honesty (deepseek)
w3 = [l for l in src.split('\n') if l.startswith('- **W3 — One concrete bridge claim')]
assert len(w3) == 1
rep(w3[0], w3[0] + ' *v10.1 (deepseek): the spec tells you how to score, not whether it will work — the benchmark\'s **outcome** is the test; the seeded ledger entries L-1–L-5 are hypotheses, not results; the kernel\'s honest success probability is modest (the anti-circularity guards raise the bar by design), and the kill rows exist precisely for that case.*',
    'B6-W3')

# B7 §13 note-row
anchor = 'until artifacts ship |'
assert src.count(anchor) == 1
rep(anchor, anchor + '''
| **v10.1 (this file — VERSION NOTE, Charter rule 4)** | 2026-10-11 | Same Part I as v9.1 (shared correction-class/reading-layer pass). **Part II:** DP1 de-triadicized; RP13.3 tier-clarification (grammar-tier exclusions, Γ ⊢ C(θ)); kernel μ-computability clause; W5 standing counters; RP11b Γ-format; W3 benchmark-vs-spec honesty. Five-audit record: `five-audits-joint-adjudication.md` |''',
    'B7-s13')

open('formalism-v10.1.md', 'w').write(src)
print('v10.1 complete:', len(src), 'bytes;', len(ops), 'part-II blocks on top of 20 shared')
