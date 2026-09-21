import { getSp4, Tableau, HybridCircuit, runEnsemble } from "../src/lib/quantum/clifford.ts";

// 1. Sp(4,2) count
const sp4 = getSp4();
console.log("Sp(4,2) elements:", sp4.length, "(expect 720)");

// 2. Small entropy checks
const bell = Tableau.bellPairs(1); // 2 qubits
console.log("Bell S({q0}) =", bell.entropy([0]), "(expect 1)");
console.log("Bell S({q0,q1}) =", bell.entropy([0, 1]), "(expect 0)");
const zeros4 = Tableau.zeros(4);
console.log("|0000> S(half) =", zeros4.entropy([0, 1]), "(expect 0)");

// 3. p=0, pure mode: volume law — S_A should approach L/2 (minus small const)
let sim = new HybridCircuit({ L: 16, p: 0, mode: "pure", seed: 42 });
for (let t = 0; t < 20; t++) sim.stepPeriod();
let rec = sim.record();
console.log("pure p=0, L=16, t=20: S_A =", rec.sA.toFixed(2), "(expect ~8, volume law)");

// 4. p=1: area law, S_A = 0
sim = new HybridCircuit({ L: 16, p: 1, mode: "pure", seed: 42 });
for (let t = 0; t < 8; t++) sim.stepPeriod();
rec = sim.record();
console.log("pure p=1, L=16: S_A =", rec.sA, "I3 =", rec.i3, "(expect 0 / 0)");

// 5. purif p=0: S_ref = L forever; p=1: S_ref = 0 after one layer
sim = new HybridCircuit({ L: 16, p: 0, mode: "purif", seed: 7 });
for (let t = 0; t < 10; t++) sim.stepPeriod();
rec = sim.record();
console.log("purif p=0, L=16, t=10: S_ref =", rec.sRef, "(expect 16)");

sim = new HybridCircuit({ L: 16, p: 1, mode: "purif", seed: 7 });
sim.stepPeriod();
rec = sim.record();
console.log("purif p=1, L=16, t=1: S_ref =", rec.sRef, "(expect 0)");

// 6. Ensemble near the critical point: purif, L=16, p=0.16, tau=1
//    deposited table says <S_ref> = 1.6115(17) at L=16
const r = runEnsemble({ L: 16, p: 0.16, mode: "purif", nTraj: 400, taus: [1, 2], seed0: 12345 });
console.log("ensemble L=16 p=0.16 purif: tau=1 S_ref =", r.sRef[0].mean.toFixed(3), "+-", r.sRef[0].se.toFixed(3), "(deposited: 1.6115(17))");
console.log("                              tau=2 S_ref =", r.sRef[1].mean.toFixed(3), "+-", r.sRef[1].se.toFixed(3), "(deposited: 0.5875(11))");

// 7. Deep area law: p=0.4 purif should purify quickly
const r2 = runEnsemble({ L: 16, p: 0.4, mode: "purif", nTraj: 100, taus: [1], seed0: 999 });
console.log("ensemble L=16 p=0.40 purif tau=1: S_ref =", r2.sRef[0].mean.toFixed(3), "(expect ~0)");

// 8. Timing for API feasibility
const t0 = Date.now();
runEnsemble({ L: 32, p: 0.16, mode: "purif", nTraj: 200, taus: [0.5, 1, 2], seed0: 1 });
console.log("timing: L=32, 200 traj, tau<=2:", Date.now() - t0, "ms");
const t1 = Date.now();
runEnsemble({ L: 64, p: 0.16, mode: "purif", nTraj: 60, taus: [1], seed0: 1 });
console.log("timing: L=64, 60 traj, tau<=1:", Date.now() - t1, "ms");
