# quantum-circuits — MIPT research workspace

Research workspace for the measurement-induced phase transition (MIPT) in random
Clifford circuits: exact (annealed) results via a two-replica mapping to the
triangular-lattice Ising model, and large-scale Clifford-simulator numerics
(quenched) for the I3 / entropy locators and an independent Gullans–Huse
purification locator.

Contents:
- `previous chat.txt`, `previous turns.txt` — the deposited research-session
  logs (source of the deposited results quoted in the manuscript).
- `research/` — the academic manuscript work (versions, computation scripts,
  results, report, changelog, ledger). See `research/README.md`.
- `web-explorer/` — the interactive research-explorer web application
  (Next.js 16 + TypeScript; simulator, FSS explorer, community board).
  Secondary artifact; see `web-explorer/worklog.md` for its build log.

Versioning policy: revisions are always added as new version files
(v13 → v14, report v2 → v3, ...); existing files are never overwritten.
