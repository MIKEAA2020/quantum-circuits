WEB SIMULATION — MIPT in random Clifford circuits
==================================================

This folder hosts the paper's web simulation (the interactive companion of
the manuscript "MIPT in random Clifford circuits").

  index.html            the web simulation — ONE self-contained file
                        (no server, no network, no dependencies)

WHAT IT IS
----------
An interactive research explorer for the measurement-induced phase
transition in hybrid random Clifford circuits:

  * a live Gottesman–Knill stabilizer-tableau simulator of the monitored
    circuit dynamics (pure-state I3 and purification S_ref protocols),
    with the circuit visualized gate-by-gate as it runs;
  * the finite-size-scaling benchmark: the deposited purification dataset
    in full, an interactive data-collapse explorer (p_c / nu sliders with a
    chi-square quality gauge), and an I3 crossing-sweep explorer with
    trajectory-level bootstraps;
  * the annealed replica chain (exact free-fermion results, rank
    certificates, tilt chain) and the record SCGF analyses, quoted
    verbatim from the deposited analysis logs;
  * the reproducibility inventory (seed contract, dataset inventory,
    disclosed weighting defect).

Everything runs locally in the browser. The ensemble and sweep computing
that the hosted version performs on a server is executed by the same
pure-TypeScript Clifford engine in-page, with the same seed contracts,
so every number produced here is bit-identical to the hosted build.
Saved runs and board sweeps persist in the browser's localStorage.

HOW TO USE
----------
  * Hosted:  https://mikeaa2020.github.io/quantum-circuits/web-simulation/
  * Offline: download index.html (or web_simulation.zip) and open it in
             any modern desktop browser (double-click; JavaScript enabled).

web_simulation.zip    index.html + this README, ready for supplementary
                      material upload or archival.

PROVENANCE
----------
Generated from the application source tree of this repository
(MIKEAA2020/quantum-circuits). The generator lives outside the paper
repo; the file is committed as the built artifact so the hosted URL and
the archival copy cannot drift apart.
