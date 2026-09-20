# v17 — the annealed three-replica critical point (round summary)

The user's question: what remains from the audits, and what novel computational
work is most merited?  Answer delivered as a new computation that closes the
manuscript's own #1 open computational item.

**Result.** The annealed three-replica transition of the monitored Haar circuit
(d=2) is located and classified from exact transfer-matrix spectra:
p_c^{(3)} = 0.305(3); CONTINUOUS; amplitude ratio -> 1/6 and 1/nu_eff = 1.15(10)
(three-state Potts; the n=2 row of the same benchmark gives Ising 1/8 and 1);
sigma sector = std (x) std (4-fold); growth-rate curve recorded; lambda_1
simple at every tested (L, p).  Conjecture: annealed n-replica points follow
q = n-state Potts universality; q > 4 predicts first order at n >= 5.

**Validation.** Every convention validated against the deposit: the Sec. 9
benchmarks reproduce exactly; the n=2 path reproduces the Kaufman closed form
and — the strongest control — the same momentum-block code at L = 16..32
reproduces the deposited benchmark crossings 0.23319/0.23347/0.23361/0.23368
to 1e-5.

**Files.** scripts: n3_annealed_{lib,validate_v1,runall_v1,analysis_v1}.py;
results: mipt_results/n3_annealed_*.json, n2_control_*.json; logs:
logs/n3_annealed_*.log; manuscript: versions/manuscript_revised_v17_annealed-n3
(.tex/.pdf, 31 pp, Sec. sec:n3annealed); report v6 (Sec. 11); changelog
Section S; ledger certificate_sha256_v4.txt.
