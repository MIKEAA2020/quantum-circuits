/**
 * Real research data extracted from the "quantum-circuits" workspace
 * (MIPT in random Clifford circuits — measurement-induced phase transition study).
 *
 * Sources: purification analysis log (mipt_purif_analysis.py output),
 * audit3 joint assessment v2, final2 FSS summary, exact-certificate dumps.
 * All values are quoted verbatim from the deposited logs.
 */

// ---------------------------------------------------------------------------
// Purification (Gullans–Huse) dataset: <S_ref> in bits, standard error in parens
// sizes [16, 32, 64, 128, 256]; p grid 0.140–0.180 step 0.005
// 135,000 trajectories total, 270 chunk files, seeds disjoint from the I3 dataset
// ---------------------------------------------------------------------------

export type PurifPoint = { p: number; mean: number; se: number };

const T025: [number, number][][] = [
  [[6.256, 0.0273], [7.9345, 0.0348], [10.0127, 0.0459], [13.0175, 0.0628], [18.4, 0.0736]],
  [[6.0652, 0.0279], [7.5412, 0.0331], [9.2363, 0.0435], [11.4, 0.0618], [15.2385, 0.0687]],
  [[5.8232, 0.0283], [7.103, 0.0327], [8.4543, 0.0435], [9.9115, 0.0595], [12.3675, 0.0649]],
  [[5.652, 0.0271], [6.818, 0.0329], [7.6623, 0.0425], [8.537, 0.0569], [9.7695, 0.0629]],
  [[5.4322, 0.0276], [6.429, 0.0315], [7.014, 0.0417], [7.38, 0.0544], [7.5175, 0.0552]],
  [[5.2453, 0.0278], [6.0598, 0.0315], [6.2717, 0.0392], [6.2265, 0.0506], [5.6025, 0.0511]],
  [[5.0838, 0.0265], [5.6792, 0.0308], [5.751, 0.0388], [5.141, 0.0462], [4.0915, 0.0425]],
  [[4.9432, 0.0261], [5.402, 0.0307], [5.1697, 0.037], [4.363, 0.0443], [2.8945, 0.0375]],
  [[4.716, 0.0263], [5.11, 0.0299], [4.6763, 0.0355], [3.577, 0.0401], [1.92, 0.0312]],
];

const T05: [number, number][][] = [
  [[3.9253, 0.0235], [4.9067, 0.0281], [6.5177, 0.0368], [9.1355, 0.0505], [14.41, 0.0595]],
  [[3.7645, 0.023], [4.595, 0.0268], [5.6783, 0.0348], [7.55, 0.0495], [11.1985, 0.0553]],
  [[3.585, 0.0234], [4.119, 0.0259], [4.953, 0.034], [6.084, 0.0462], [8.396, 0.0508]],
  [[3.364, 0.0229], [3.848, 0.0258], [4.2397, 0.0327], [4.8165, 0.0425], [5.8565, 0.0477]],
  [[3.18, 0.0227], [3.4752, 0.0245], [3.6237, 0.0309], [3.7635, 0.0396], [3.7215, 0.0397]],
  [[3.0002, 0.0224], [3.152, 0.0242], [3.057, 0.0293], [2.8115, 0.0353], [2.1865, 0.0331]],
  [[2.8098, 0.022], [2.8577, 0.0231], [2.6097, 0.0276], [1.9965, 0.0305], [1.2165, 0.0244]],
  [[2.6662, 0.0213], [2.6033, 0.0232], [2.178, 0.0255], [1.428, 0.0264], [0.5995, 0.017]],
  [[2.4893, 0.0208], [2.3178, 0.0217], [1.8037, 0.0236], [0.959, 0.0223], [0.238, 0.0109]],
];

const T1: [number, number][][] = [
  [[2.2997, 0.0192], [3.027, 0.0221], [4.3247, 0.0292], [6.901, 0.0404], [11.9825, 0.0474]],
  [[2.1235, 0.0184], [2.679, 0.0212], [3.5123, 0.0276], [5.2715, 0.0383], [8.9245, 0.0445]],
  [[1.9592, 0.0183], [2.2807, 0.02], [2.8183, 0.0255], [3.875, 0.0356], [6.0575, 0.0414]],
  [[1.7548, 0.0174], [1.9695, 0.019], [2.2487, 0.0244], [2.731, 0.0325], [3.599, 0.0364]],
  [[1.6115, 0.0172], [1.686, 0.0183], [1.722, 0.022], [1.7525, 0.0277], [1.765, 0.0276]],
  [[1.445, 0.0163], [1.4418, 0.0172], [1.3073, 0.0203], [1.041, 0.0223], [0.628, 0.0177]],
  [[1.322, 0.0159], [1.1958, 0.0159], [0.9367, 0.0171], [0.523, 0.0158], [0.191, 0.0098]],
  [[1.1855, 0.0156], [0.9792, 0.0149], [0.6567, 0.0146], [0.246, 0.0113], [0.0365, 0.0043]],
  [[1.0482, 0.0144], [0.8147, 0.0136], [0.4517, 0.0124], [0.108, 0.0076], [0.005, 0.0016]],
];

const T2: [number, number][][] = [
  [[1.1173, 0.0143], [1.6373, 0.0167], [2.759, 0.0225], [5.2165, 0.033], [10.275, 0.0377]],
  [[0.9775, 0.0136], [1.3485, 0.0158], [2.0467, 0.0212], [3.6505, 0.0305], [7.2105, 0.0361]],
  [[0.8313, 0.0127], [1.0143, 0.0143], [1.4773, 0.0191], [2.411, 0.0281], [4.3465, 0.0324]],
  [[0.7055, 0.0121], [0.8257, 0.0131], [0.9837, 0.0166], [1.3435, 0.0235], [2.1275, 0.0275]],
  [[0.5875, 0.0114], [0.6115, 0.0115], [0.5983, 0.0133], [0.6155, 0.0172], [0.6155, 0.017]],
  [[0.4785, 0.0103], [0.4602, 0.0103], [0.35, 0.0106], [0.222, 0.0103], [0.0905, 0.0069]],
  [[0.4175, 0.0095], [0.3065, 0.0084], [0.19, 0.0077], [0.0575, 0.0053], [0.0045, 0.0015]],
  [[0.3307, 0.0086], [0.2205, 0.0072], [0.0927, 0.0054], [0.0135, 0.0026], [0.0, 0.0005]],
  [[0.2585, 0.0077], [0.147, 0.006], [0.0423, 0.0038], [0.0035, 0.0013], [0.0, 0.0005]],
];

const T4: [number, number][][] = [
  [[0.3392, 0.0086], [0.6735, 0.0118], [1.5657, 0.018], [3.9065, 0.0276]],
  [[0.261, 0.0076], [0.4637, 0.0099], [1.0007, 0.0158], [2.4095, 0.0254]],
  [[0.192, 0.0066], [0.2785, 0.008], [0.5493, 0.0123], [1.231, 0.0211]],
  [[0.1365, 0.0057], [0.1955, 0.0068], [0.2623, 0.0091], [0.445, 0.014]],
  [[0.0973, 0.0048], [0.1035, 0.005], [0.0963, 0.0056], [0.1115, 0.0073]],
  [[0.0688, 0.0041], [0.0602, 0.0039], [0.03, 0.0032], [0.015, 0.0027]],
  [[0.051, 0.0035], [0.022, 0.0023], [0.01, 0.0018], [0.002, 0.001]],
  [[0.0333, 0.0029], [0.0105, 0.0017], [0.0027, 0.0009], [0.0, 0.0005]],
  [[0.0163, 0.0021], [0.005, 0.0011], [0.0007, 0.0005], [0.0, 0.0005]],
];

const P_GRID = [0.14, 0.145, 0.15, 0.155, 0.16, 0.165, 0.17, 0.175, 0.18];
const SIZES5 = [16, 32, 64, 128, 256];

function buildSeries(table: [number, number][][], sizes: number[]): Record<number, PurifPoint[]> {
  const out: Record<number, PurifPoint[]> = {};
  table.forEach((row, pi) => {
    row.forEach(([mean, se], li) => {
      const L = sizes[li];
      if (!out[L]) out[L] = [];
      out[L].push({ p: P_GRID[pi], mean, se });
    });
  });
  return out;
}

export type TauSlice = {
  tau: number;
  label: string;
  sizes: number[];
  series: Record<number, PurifPoint[]>;
  crossings: string;
  collapse: { pc: number; nu: number; chi2: string; note?: string };
  dchi2?: { nu: number; dchi2: number }[];
};

export const PURIF_DATA: TauSlice[] = [
  {
    tau: 0.25,
    label: "τ = t/L = 0.25",
    sizes: SIZES5,
    series: buildSeries(T025, SIZES5),
    crossings: "no crossing yet (16,32); 0.16998 (32,64); 0.16365 (64,128); 0.16127 (128,256)",
    collapse: { pc: 0.16191, nu: 1.2808, chi2: "48.1/18" },
    dchi2: [
      { nu: 1.0, dchi2: 426.3 },
      { nu: 1.2, dchi2: 28.2 },
      { nu: 1.24, dchi2: 6.9 },
      { nu: 1.28, dchi2: 0.0 },
      { nu: 4 / 3, dchi2: 10.7 },
      { nu: 1.4, dchi2: 52.3 },
    ],
  },
  {
    tau: 0.5,
    label: "τ = t/L = 0.5",
    sizes: SIZES5,
    series: buildSeries(T05, SIZES5),
    crossings: "0.172 (16,32); 0.16306 (32,64); 0.16128 (64,128); 0.16067 (128,256)",
    collapse: { pc: 0.16039, nu: 1.251, chi2: "15.5/18", note: "spline F, L ≥ 64" },
    dchi2: [
      { nu: 1.0, dchi2: 1360.6 },
      { nu: 1.2, dchi2: 94.8 },
      { nu: 1.24, dchi2: 27.6 },
      { nu: 1.28, dchi2: 1.0 },
      { nu: 4 / 3, dchi2: 18.7 },
      { nu: 1.4, dchi2: 110.8 },
    ],
  },
  {
    tau: 1,
    label: "τ = t/L = 1",
    sizes: SIZES5,
    series: buildSeries(T1, SIZES5),
    crossings: "0.16353 (16,32); 0.16097 (32,64); 0.16064 (64,128)",
    collapse: { pc: 0.16009, nu: 1.2486, chi2: "18.3/18", note: "L ≥ 64" },
    dchi2: [
      { nu: 1.0, dchi2: 544.3 },
      { nu: 1.2, dchi2: 16.9 },
      { nu: 1.24, dchi2: 0.5 },
      { nu: 1.28, dchi2: 6.6 },
      { nu: 4 / 3, dchi2: 45.8 },
      { nu: 1.4, dchi2: 138.6 },
    ],
  },
  {
    tau: 2,
    label: "τ = t/L = 2",
    sizes: SIZES5,
    series: buildSeries(T2, SIZES5),
    crossings: "0.16147 (16,32); 0.16032 (32,64); 0.16148 (64,128)",
    collapse: {
      pc: 0.16027,
      nu: 1.3096,
      chi2: "82.8/18",
      note: "L ≥ 64 — saturated S→0 tail inflates ν; |x| ≤ 2 window gives 0.15977 / 1.207",
    },
    dchi2: [
      { nu: 1.0, dchi2: 1206.8 },
      { nu: 1.2, dchi2: 102.0 },
      { nu: 1.24, dchi2: 38.9 },
      { nu: 1.28, dchi2: 6.7 },
      { nu: 4 / 3, dchi2: 4.0 },
      { nu: 1.4, dchi2: 53.8 },
    ],
  },
  {
    tau: 4,
    label: "τ = t/L = 4",
    sizes: [16, 32, 64, 128],
    series: buildSeries(T4, [16, 32, 64, 128]),
    crossings: "0.16089 (16,32); 0.16016 (32,64); 0.16128 (64,128)",
    collapse: { pc: 0.16041, nu: 1.3346, chi2: "37.4/27", note: "L ≥ 16" },
  },
];

// ---------------------------------------------------------------------------
// Headline results
// ---------------------------------------------------------------------------

export const HEADLINE = {
  pc: 0.1597,
  pcErr: 0.0008,
  nu: 1.24,
  nuErr: 0.07,
  alpha: 1.55,
  alphaErr: 0.07,
  pcPurif: "0.1601–0.1604",
  nuPurif: "1.25(2)_stat(6)_sys",
  trajectoriesI3: 475_600,
  trajectoriesPurif: 135_000,
  sizesI3: "L = 16–512",
  sizesPurif: "L = 16–256",
  purifFiles: 270,
};

export const COMPARISON = [
  { source: "This work — I₃ locator (Clifford)", pc: "0.1597(8)", nu: "1.24(7)", note: "475,600 trajectories, L ≤ 512" },
  { source: "This work — purification locator", pc: "0.1601–0.1604", nu: "1.25(2)", note: "independent seeds, mixed initial state" },
  { source: "Gullans & Huse (PRX 10, 041020)", pc: "0.1593(5)", nu: "1.28(2)", note: "I₃ crossing, pure states" },
  { source: "Sierant et al.", pc: "0.15995(10)", nu: "—", note: "quoted in manuscript comparison" },
];

// Frozen-ν Δχ² profile (I₃ collapses, fixed point sets, spline F with tail in, L ≥ 64)
export const I3_DCHI2 = [
  { nu: 1.0, dchi2: 52 },
  { nu: 1.2, dchi2: 0.2 },
  { nu: 1.24, dchi2: 0.1 },
  { nu: 1.28, dchi2: 0.0 },
  { nu: 4 / 3, dchi2: 3.0 },
  { nu: 1.4, dchi2: 12.5 },
];

// ---------------------------------------------------------------------------
// Annealed (exact) results — two-replica / 8-vertex sector
// ---------------------------------------------------------------------------

export const ANNEALED = {
  beta: (d: number) => (d * d - 1) / (d * d + 1),
  pc2: [
    { d: 2, pc2: 0.23381 },
    { d: 3, pc2: 0.45969 },
    { d: 5, pc2: 0.679 },
  ],
};

// Exact-rational Collatz–Wielandt enclosures of λ₁ (Level-B certificates)
export const CERTIFICATES = [
  { L: 16, d: 2, p: "2/5", lo: "0.0022886508026864124561", hi: "0.0022886508026864175903", rel: "2.2e-15" },
  { L: 16, d: 2, p: "4/25", lo: "0.075189633382987646", hi: "0.075189633382987911", rel: "3.5e-15" },
  { L: 16, d: 2, p: "1169/5000", lo: "0.0236927451718797476", hi: "0.0236927451718798042", rel: "2.4e-15" },
  { L: 20, d: 2, p: "2/5", lo: "0.00050028570068131041", hi: "0.00050028570068131407", rel: "7.3e-15" },
  { L: 16, d: 3, p: "2/5", lo: "6.3658872262159916e-05", hi: "6.3658872262160092e-05", rel: "2.9e-15" },
];

// Tilt mechanism chain (L = 8, t = 4, p = 0.16; 40,000 Born trajectories, ESS 5935)
export const TILT_CHAIN = {
  peff: { L8: 0.1049, L12: 0.1011, Linf: 0.092 },
  steps: [
    { label: "E_Born S(p = 0.16)", value: 2.019, note: "quenched mean" },
    { label: "E_Born S(p_eff = 0.1049)", value: 2.339, note: "density shift ≈ 80% of gain" },
    { label: "E_tilt S", value: 2.429, note: "p_R²-tilted average" },
    { label: "S̃₂ (annealed)", value: 2.155, note: "exact quasi-entropy" },
  ],
};

export const BOOTSTRAP = {
  purif: [
    { tau: 1, Lmin: 32, pc: "0.16025(7)", nu: "1.265(9)" },
    { tau: 1, Lmin: 64, pc: "0.16011(9)", nu: "1.250(14)" },
    { tau: 2, Lmin: 64, pc: "0.16028(8)", nu: "1.310(11)" },
  ],
};

export const REPRO = {
  seedContract:
    "trajectory k of file (L, p) is regenerated bit-exactly by the legacy MT19937 stream seeded with seed0(L, p) + k; seed0 is stored in the file. Verified for 23 trajectories spanning L = 16–512, including the I₃ ≡ 0 file at L = 384, p = 0.18.",
  purifSpec: [
    { L: 16, n: 4000 }, { L: 32, n: 4000 }, { L: 64, n: 3000 }, { L: 128, n: 2000 }, { L: 256, n: 2000 },
  ],
  pGrid: "p = 0.140 … 0.180 (9 values, step 0.005)",
  tauGrid: "τ = t/L ∈ {0.25, 0.5, 1, 2, 4}",
  seedBlock: "purification seeds offset by +500,000,000 — disjoint from the pure-state blocks",
};

// ---------------------------------------------------------------------------
// v19 — annealed replica ladder (n = 2…5), the two-size first-order test,
// the Haar record SCGFs, and the no-freeze theorem.
// All values are quoted verbatim from manuscript v19 / deposited results.
// ---------------------------------------------------------------------------

/** Quenched reference point for the ladder (Clifford, Born-weighted). */
export const REPLICA_QUENCHED = {
  pc: 0.1597,
  err: 0.0008,
  label: "0.1597(8)",
  note: "I₃ locator; purification locator 0.1601–0.1604",
};

export type ReplicaRung = {
  n: number;
  pc: number;
  /** verbatim label, e.g. "0.305(3)" */
  pcLabel: string;
  cls: string;
  order: "continuous" | "first order";
  note: string;
};

/** Annealed critical points (d = 2), replica number n = 2…5 — all verified. */
export const REPLICA_LADDER: ReplicaRung[] = [
  {
    n: 2,
    pc: 0.23381,
    pcLabel: "0.233810",
    cls: "Ising (Houtappel triangular-lattice)",
    order: "continuous",
    note: "EXACT closed form — the condition a − c = 2b. Continuous, Ising class.",
  },
  {
    n: 3,
    pc: 0.305,
    pcLabel: "0.305(3)",
    cls: "three-state Potts",
    order: "continuous",
    note: "Potts amplitude ratio converges cleanly: R_L(0.305) = 0.108 → 0.141 → 0.157 → 0.167 on the q = 3 target x_σ/x_ε = 1/6 (at L = 10); slope exponent 1/ν_eff = 1.15(10) (Potts 6/5); exact sector-resolved transfer-matrix spectra, L = 4–12. Crossings: (4,6) 0.27114, (6,8) 0.29678, (8,10) 0.30244, (10,12) 0.30403.",
  },
  {
    n: 4,
    pc: 0.383,
    pcLabel: "≈ 0.383",
    cls: "marginal q = 4 Potts",
    order: "continuous",
    note: "Multiplicative log corrections; full S₄ colour resolution, four sizes L = 4, 6, 8, 10 (the previously missing L = 8 λ_ε values recomputed); crossings 0.35820, 0.37899, 0.3823; drift collapses 0.0208 → 0.0033 (vs 0.68 for a 1/ν = 1.28 power law); the amplitude ratio R_L(p* = 0.383) = 0.1315 / 0.1829 / 0.2142 / 0.2378 converges logarithmically to the q = 4 target x_σ/x_ε = 1/4 — the two-term marginal form 1/4 − 0.90/ln L + 0.46/ln²L fits with residual ≤ 8×10⁻⁴ (the diagnostic does NOT degrade — it converges with exactly the multiplicative-logarithmic slowness the marginal point predicts; the target is 1/4, not the Ising 1/8, which would require x_ε = 1: at q = 4, 1/ν = 3/2 so x_ε = d − 1/ν = 1/2); the slope exponent rises 1.00 → 1.38 → 1.57 through the q = 4 value 3/2 with the expected 1/ln L correction. N = 24⁵ = 7,962,624 bond labels at L = 10 (dense would need 6.3×10¹³ entries ≈ 500 TB; iterative ring route < 1.8 GB).",
  },
  {
    n: 5,
    pc: 0.475,
    pcLabel: "≈ 0.47–0.48",
    cls: "first order",
    order: "first order",
    note: "Confirmed at the two-size level (L = 4 → 6): closing factor ×2.12, L·gap12 falls below the continuous envelope, plateau narrows by the full size ratio 4/6, X-curves cross at p ≈ 0.449 with slope ratio 2.18 vs n = 3's 1.69 ≈ (6/4)^1.15; locator stable 0.48 (L = 4) / 0.47 (L = 6). Two sizes cannot yet separate exponential from power-law closing; L = 8 (120⁴ = 2.1×10⁸ bond labels) is the next rung.",
  },
];

/** Headline trend (verbatim): the annealed points recede from the quenched point. */
export const REPLICA_TREND =
  "0.1597(8) quenched < 0.233810 < 0.305(3) < 0.383 < 0.47 — annealed points move AWAY from the quenched transition as n grows (no annealed sequence converges to the Born-weighted point from above); q = n-Potts universality at n = 2, 3, 4, first order at n = 5.";

/** Two-size test rows (L = 4 → 6, matched locators). */
export const N5_TWOSIZE = [
  { n: 3, locator: "0.30", gapL4: 2.147, gapL6: 1.185, closing: 1.81, lgap: "8.59 → 7.11", cls: "continuous baseline" },
  { n: 4, locator: "0.38", gapL4: 1.919, gapL6: 0.990, closing: 1.94, lgap: "7.67 → 5.94", cls: "marginal q = 4" },
  { n: 5, locator: "0.47", gapL4: 1.711, gapL6: 0.806, closing: 2.12, lgap: "6.85 → 4.85", cls: "first order — confirmed" },
];

/** First numerical quenched record SCGFs — Haar circuits (manuscript v19, Sec. smcnumerics). */
export const SMC_HAAR = {
  params: "N = 384 particles, T = 2L periods, systematic resampling, 8 circuits/point, L = 6–12",
  pValues: [0.10, 0.1597, 0.2338, 0.4],
  k: [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2],
  /** ψ(k) at p = 0.2338, nats per period */
  psiL8: [-4.08, -3.16, -2.18, -1.13, 0.0, 1.24, 2.6, 4.13, 5.78],
  psiL8se: [0.12, 0.09, 0.06, 0.03, 0, 0.04, 0.09, 0.15, 0.2],
  psiL12: [-6.03, -4.66, -3.21, -1.67, 0.0, 1.82, 3.8, 6.02, 8.41],
  psiL12se: [0.27, 0.21, 0.15, 0.08, 0, 0.1, 0.23, 0.39, 0.57],
  /** D(q) spread over q ∈ [−1, 3] at L = 8, at the four p values (Clifford: exactly constant) */
  dSpreadL8: [0.2, 0.32, 0.85, 1.96],
  /** D-spread at L = 12, p = 0.2338 — grows with L */
  dSpreadL12: 1.19,
  /** record entropy rate ψ′(0) per period at L = 8, nats, at the four p values */
  entropyRatesL8: [1.02, 1.5, 2.36, 3.62],
  /** per-site rate, L-independent to 5% over L = 6–10 at p = 0.2338 */
  perSite: { p: 0.2338, L: [6, 8, 10], rates: [0.287, 0.295, 0.288] },
  /** annealed vs quenched, L = 8, p = 0.2338, k = 1 — disorder average does not commute with the logarithm */
  annealedVsQuenched: { annealed: 2.75, quenched: 2.6, level: "≈6%, growing with L and p" },
  noFreezing: "no finite-q freezing up to q = 3 at L ≤ 12 — τ remains strictly convex (no linear branch, the freezing signature)",
  validation: [
    "exact enumeration at L = 4 within 2σ across four decades of Z",
    "p = 1 exact Markov chain within 1.4σ up to Z ~ 4×10¹⁰",
    "ψ(0) = 0 exactly",
    "ψ″(0) = Var/T identity: 0.428 vs 0.427",
    "N = 1536 top-up confirms the k = +2 column",
  ],
};

/** No-freeze theorem + replica interpolation identity (manuscript v19, Sec. nofreeze). */
export const NO_FREEZE = {
  theorem:
    "No allowable finite-reachable monitored process — deterministic, i.i.d.-random, or reducible — can exhibit finite-q freezing. Freezing requires an unbounded reachable set.",
  proofRoute: [
    "Furstenberg–Kesten + Hilbert-metric cone contraction — existence + determinism",
    "Le Page / Ruelle / Peres analyticity of the top Lyapunov exponent",
    "identity-theorem corollary: an analytic ψ affine on an interval is affine everywhere, contradicting strict convexity",
    "reducible chains give corners (jumps of τ′), not affine branches",
  ],
  rem: {
    qc: "√(2 log 2)",
    note: "the random-energy construction realizes freezing at q_c = √(2 log 2) with τ′ continuous at the onset — the side-by-side counterexample",
  },
  corollary: "the fully monitored p = 1 Haar-refreshed family's analyticity is unconditional",
  machine: "8/8 PASS",
  interpolation: {
    formula: "g(r) − r·E log X = ∫₀ʳ (r−s)·Var_s(log X) ds",
    consequences: [
      "m ↓ 0: quenched value, quadratically",
      "m → ∞: overshoots to extremal — not an interchange",
      "interchange ⟺ measurable self-averaging criterion",
    ],
    criterion: "sup_T Var(T⁻¹ log Z) < ∞",
    ladder: "replica free energies f_m form a monotone ladder; m → ∞ overshoots to the extremal value log ess sup X — the naive replica limit is not an interchange",
  },
};

// ---------------------------------------------------------------------------
// Record SCGF (v16 data, v21 framing) — the disorder-direction SCGF of the
// record count: the annealed record moment family at fractional order
// q = 1 + β; the β = 1 endpoint is exactly the annealed collision Z̄₂ (the
// two-replica transfer matrix). Values produced and verified in the present
// workspace (research/scripts/mipt_scgf_exact.py = exact two-replica algebra
// evolution; mipt_born_scgf.py = vectorised tableau trajectories;
// results/scgf_exact.json, scgf_born.json).
// ---------------------------------------------------------------------------

export const RECORD_SCGF = {
  // p = 0.16, tau = 4 (t = 4L); xbar = quenched record-entropy density
  // (bits/site); xi1 = exact beta=1 anchor: finite-t 3^L evolution at
  // L <= 16; amplitude-corrected lambda_1 at L = 24 (A(24) ~ 21.4 from
  // A(L) = 2.4512/4.2354/7.2288 at L = 8/12/16); lambda_1-asymptotic at
  // L = 32. varPerSite = Var(X)/(2Lt); ess = effective sample size of the
  // collision tilt out of essB trajectories; gap = Lambda(1) + ln2*xbar
  // (nats/site).
  ladder: [
    { L: 8, xbar: 0.14479, xi1Exact: -0.077984, xi1Inf: -0.079735, varPerSite: 0.1055, ess: 11.7, essB: 40000, gap: 0.0224, sMean: 2.036 },
    { L: 12, xbar: 0.14703, xi1Exact: -0.079362, xi1Inf: -0.080615, varPerSite: 0.1044, ess: 3.9, essB: 40000, gap: 0.0226, sMean: 2.675 },
    { L: 16, xbar: 0.14803, xi1Exact: -0.079901, xi1Inf: -0.080867, varPerSite: 0.1058, ess: 1.4, essB: 30000, gap: 0.0227, sMean: 3.116 },
    { L: 24, xbar: 0.14890, xi1Exact: -0.080325, xi1Inf: -0.080989, varPerSite: 0.1048, ess: 1.0, essB: 15000, gap: 0.0229, sMean: 3.732 },
    { L: 32, xbar: null as number | null, xi1Exact: -0.081009, xi1Inf: -0.081009, varPerSite: null as number | null, ess: null as number | null, essB: 0, gap: null as number | null, sMean: null as number | null },
  ],
  houtappelPerSite: -0.08101, // nats/site at p = 0.16 (the beta=1 thermodynamic limit)
  houtappelP22: -0.11082, // nats/site at p = 0.22
  xbarLimit: 0.1489, // bits/site (quenched record-entropy density, p = 0.16, L -> inf)
  xbarP22: 0.1971, // bits/site at p = 0.22
  gapValue: "0.0226(2)", // nats/site, L-independent (ladder values 0.0224/0.0226/0.0227/0.0229)
  gapP22: 0.027, // nats/site at p = 0.22, L-independent
  varP22: "0.124–0.125", // Var(X)/(2Lt) at p = 0.22 (0.105 at p = 0.16), L-independent for L = 8–24
  gaussianCumulant: 0.0252, // leading Gaussian cumulant — overestimates g by ≈13% (sub-Gaussian tail)
  // Z2(t) = A(L) * lambda_1^t — A subexponential in t, constant to 6 digits for t >= 3L
  aFactors: {
    L: [8, 12, 16],
    A: [2.4512, 4.2354, 7.2288],
    note: "subexponential in t, constant to 6 digits for t ≳ 3L; A(24) ≈ 21.4 extrapolated",
  },
  // collision-tilt ESS — exact law ESS/B = exp[-2Lt·(Λ(2) − 2Λ(1))];
  // exact (v22, via the three-replica operator) vs the superseded trajectory
  // estimates — the t=4L moments are biased low by the ESS collapse
  essExponent: [
    { L: 8, exponent: 0.0340, traj: 0.0159 },
    { L: 12, exponent: 0.0349, traj: 0.0080 },
    { L: 16, exponent: 0.0353, traj: 0.0049 },
  ],
  // v22 — the exact Λ(2) = (2Lt)⁻¹ ln Z̄₃ closure via the three-replica
  // transfer operator (the v17 object), and the Cl₂ conjugation-3-design
  // identification that makes it exact.
  z3closure: {
    design3: { n2: 2.1e-14, n3: 1.6e-14, n4: 0.578, note: "two-qubit Cliffords are an exact conjugation 3-design — verified against the Haar twirl; the design property fails at n=4 exactly where d² ≥ n still holds" },
    cells: [
      { L: 8, lambda2: -0.121924, exponent: 0.0340, trajExponent: 0.0159, essTrueFrac: 2.8e-8 },
      { L: 12, lambda2: -0.123857, exponent: 0.0349, trajExponent: 0.0080, essTrueFrac: 3.7e-11 },
      { L: 16, lambda2: -0.124526, exponent: 0.0353, trajExponent: 0.0049, essTrueFrac: 5.1e-13 },
    ],
    note: "p = 0.16, t = 4L; Λ(2) = (2Lt)⁻¹ ln Z̄₃ computed exactly by the three-replica transfer operator (the v17 object); the exact ESS-law exponent is ~0.034–0.035 nats/site, L-independent — twice to seven times the biased trajectory estimates",
    ladderP16: [-0.124775, -0.125861, -0.126047], // ln λ₁⁽³⁾/(2L), L = 8/12/16
    ladderP22: [-0.173595, -0.175609, -0.176101],
    a3: [4.3048, 10.068, 22.5566], // amplitudes Z̄₃(t)/λ₁^t, L = 8/12/16, p = 0.16, constant in t for t ≥ L
    beta2check: "rel 1.95e-3 (0.4σ, ESS(w²) 3.7×10⁴) at L=8 t=L/2 with B=4×10⁶; 2.7e-2 (0.3σ) at L=12 — the identification holds empirically",
  },
  // tilted density of the annealed-endpoint dominating minority vs typical (L = 8, p = 0.16)
  tiltedDensity: { atypical: 0.097, typical: 0.145 },
  // freezing: tilted-vs-quenched entropy gap (exact, t = 4L, p = 0.16)
  tiltedGap: [
    { L: 8, gap: 0.19, sTildeInf: 2.2243, sQuench: 2.036 },
    { L: 12, gap: 0.57, sTildeInf: 3.2496, sQuench: 2.675 },
  ],
  // exact-vs-deposit calibration of the two-replica algebra evolution
  calibration: {
    note: "t = L/2 periods (convention fixed by this calibration)",
    rows: [
      { q: "Z₂ (exact evolution)", L8: "1.479639e-2", deposit8: "1.4796e-2", L12: "3.81731e-5", deposit12: "—" },
      { q: "S̃₂ (exact)", L8: "2.1547", deposit8: "2.155", L12: "3.1281", deposit12: "3.128" },
      { q: "E[2^−X] (4×10⁴ traj)", L8: "1.4689e-2", deposit8: "1.4942e-2", L12: "3.8399e-5", deposit12: "—" },
      { q: "E S_{L/2} (traj)", L8: "2.015(4)", deposit8: "2.019(4)", L12: "2.632(5)", deposit12: "2.394(5)" },
      { q: "ESS (tilt)", L8: "6339", deposit8: "5935", L12: "478", deposit12: "454" },
    ],
  },
  cumulantCheck: [
    { L: 8, predicted: -0.02351, measured: -0.0236 },
    { L: 24, predicted: -0.02423, measured: -0.0243 },
  ],
};
