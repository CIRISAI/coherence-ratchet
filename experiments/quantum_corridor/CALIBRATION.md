# Quantum-corridor calibration leg (N5) — does the estimator separate the state classes at Sycamore scale?

**Status: calibration only. No real quantum data touched.** This is the falsifier-N5
leg of `SPEC.md` §4.4: push synthetic controls for every declared state class through
the *identical* estimator front-end at the substrate's (N,T), and check whether the
subsample-PR exponent β separates the hypotheses **there**. Only if it does is any
real-data verdict admissible. Every number below is a classical surrogate; the shots are
synthesized from the known outcome statistics of each state class (`synth_shots.py`), never
from a quantum device or simulator.

## What was run

- **Estimator front-end** reused from `experiments/keff_saturation/spectral_test.py`:
  `corr_eig`, `participation_ratio`, `mp_edge` imported unchanged; `subsample_pr` /
  `phase_randomize` ported verbatim with an explicit RNG (numerics identical — the
  subsample-PR loop subsamples the row-z-scored correlation matrix directly, which equals
  `corr_eig(X[idx])` because z-scoring is per-row). β = upper-range dlog(PR)/dlog(N′) slope,
  same fit logic as `spectral_test.main`.
- **Grain:** Operationalization A (one qubit = one unit), correlation matrix over shots,
  N = #qubits, T = S shots (SPEC §4.2).
- **Scale:** Sycamore-like **N=53** at **S ∈ {1e4, 1e5, 5e5}** (T-dependence), and
  IBM-like **N=20** at S=1e5.
- **β CI:** bootstrap over shots (resample observations with replacement, B=25).
- **Fixed seed** 20260709; rerun is deterministic. Outputs: `calibration_results.json`,
  `beta_separation.png`, `c3_ramp_overlay.png`, `run.log`.

## Results — grid (class × N × S)

β with 95% bootstrap CI, PR/k_eff, eff-rank (spikes above the phase-randomized surrogate
floor), ρ̄ (mean off-diagonal), and the corridor verdict.

### Sycamore-like, N=53

| class | S=1e4 β [CI] | S=1e5 β [CI] | S=5e5 β [CI] | PR (5e5) | eff-rank | ρ̄ | verdict |
|---|---|---|---|---|---|---|---|
| product (Z)     | 0.996 [0.99,0.99] | 1.000 [1.00,1.00] | 1.000 [1.00,1.00] | 52.99 | 0–3 | ≈0 | **CHAOS** |
| GHZ (Z)         | 0.000 [0.00,0.00] | 0.000 [0.00,0.00] | 0.000 [0.00,0.00] | 1.00 | 1 | **1.000** | **RIGIDITY** |
| GHZ (X, parity) | 0.997 [0.99,0.99] | 1.000 [1.00,1.00] | 1.000 [1.00,1.00] | 52.99 | 1 | ≈0 | **CHAOS** |
| low-rank r=3    | 0.193 [0.16,0.23] | 0.205 [0.17,0.23] | **0.185 [0.14,0.21]** | 7.37 | 3 | ≈0 | **CORRIDOR** |
| power-law α=1.0 | 0.630 [0.59,0.65] | 0.585 [0.57,0.63] | **0.627 [0.56,0.62]** | 26.13 | 12 | ≈0 | **CRITICAL** |
| power-law α=0.6 | 0.863 [0.85,0.88] | 0.876 [0.86,0.88] | **0.874 [0.87,0.88]** | 43.25 | 15 | ≈0 | **CRITICAL** |
| shot-noise      | 0.996 [0.99,0.99] | 1.000 [1.00,1.00] | 1.000 [1.00,1.00] | 52.99 | 0 | ≈0 | **CHAOS** |

### IBM-like, N=20, S=1e5

| class | β [CI] | PR | eff-rank | ρ̄ | verdict |
|---|---|---|---|---|---|
| product (Z)     | 1.000 [1.00,1.00] | 20.00 | 1 | ≈0 | **CHAOS** |
| GHZ (Z)         | 0.000 [0.00,0.00] | 1.00 | 1 | 1.000 | **RIGIDITY** |
| GHZ (X, parity) | 1.000 [1.00,1.00] | 20.00 | 1 | ≈0 | **CHAOS** |
| low-rank r=3    | **0.452 [0.41,0.47]** | 7.44 | 3 | 0.05 | CRITICAL ✗ (should be corridor) |
| power-law α=1.0 | 0.781 [0.75,0.80] | 14.04 | 6 | ≈0 | **CRITICAL** |
| power-law α=0.6 | 0.919 [0.90,0.93] | 17.67 | 6 | ≈0 | CHAOS (α=0.6 collapses onto noise) |
| shot-noise      | 1.000 [1.00,1.00] | 20.00 | 2 | ≈0 | **CHAOS** |

## N5 verdict — does β separate the classes?

**At Sycamore scale (N=53): YES, cleanly, and stably across S=1e4→5e5.** The three
mechanism branches land in three non-overlapping β bands, CIs disjoint:

```
 low-rank r=3   β ≈ 0.19   ── saturation (CORRIDOR)
 power-law α=1  β ≈ 0.61   ┐
 power-law α=.6 β ≈ 0.87   ┘  criticality band (0.30–0.80+)
 product/GHZ-X/noise β ≈ 1.0 ── chaos/extensive
 GHZ (Z)        β = 0.00, PR = 1  ── rigidity pole (separate axis: ρ̄=1)
```

The eff-rank readout corroborates independently: low-rank = 3 spikes, power-law = a heavy
12–15-mode tail, product/noise = 0. β separation is **T-robust** — the bands do not move
between S=1e4 and S=5e5 (CIs only tighten). **A real-data C1 verdict at N≈53 is therefore
admissible** by the N5 criterion.

**At IBM scale (N=20): NO — the estimator is underpowered (N5 fails there).** The
subsample range is too short (N′ up to 20), which biases β upward and **collapses the
corridor/criticality distinction**: low-rank r=3 reads β=0.45 (inside the criticality
band, misclassified as CRITICAL), and power-law α=0.6 reads β=0.92 (indistinguishable
from noise). Only the **eff-rank** readout still separates them (low-rank=3 vs
power-law=6 vs noise=2). Consistent with the house finding that when β is ambiguous the
effective-rank readout is the intrinsic one; **at N=20, β alone is not admissible and any
real verdict must lean on eff-rank, or escalate N.**

## MUB / basis-fragility (N4), demonstrated exactly

GHZ is the pre-declared basis-fragile case and the surrogate reproduces it **exactly**,
not approximately:

| GHZ basis | ρ̄ | PR / k_eff | β | reads as |
|---|---|---|---|---|
| **Z** (computational) | 1.000 | 1.00 | 0.00 | **RIGIDITY** |
| **X** (parity)        | ≈0    | 52.99 | 1.00 | **CHAOS** |

X-basis GHZ shots are generated exactly (draw N−1 fair ±1, fix the last to enforce even
global parity). The N-body parity constraint `X^{⊗N}|GHZ⟩=|GHZ⟩` is real coordination, but
it is **invisible to a pairwise correlation matrix** (⟨X_iX_j⟩=0 for N>2), so the
correlation matrix is ≈ I and the register reads pure chaos. This is the SPEC §2 pitfall
and falsifier **N4** made concrete: on GHZ the β verdict flips between the two MUBs, so a
GHZ-like real register would be reported **basis-fragile / inconclusive**, not a pass. The
single-qubit grain cannot see N-body stabilizer coordination — a genuine limit of
Operationalization A, and the reason the SPEC requires ≥2 MUBs.

## C3 leg — the depolarized-GHZ maintenance ramp

> **CORRECTED 2026-07-09 (issue #7).** The first version of this leg was **vacuous**. It
> set `S_measured = potential_S(PR, ρ̄)` — evaluating the *closed form* at the
> participation ratio, never taking a log-determinant — and compared it against
> `curve_C3(PR, ρ̄) = −(PR−1)ln(1−ρ̄)`, which is the **second term of that same formula**.
> The reported `deviation` was therefore identically `−ln(1+ρ̄(PR−1))` **by algebra**
> (verified: max |reported − analytic| = 2.8e-17 over all 11 points). The test could not
> fail, and the old table's `S measured` column was wrong by three orders of magnitude
> (0.123 where `−Tr ln C(53, 0.979) = 197.2`). Substituting PR for the matrix *dimension*
> also manufactured the old "S stays finite and does not diverge" caveat — which the fix
> dissolves. Numbers below are from the corrected estimator.

Sweep p (mixing rate of independent product noise into GHZ; p↑ = withdrawing the
coordinating drive). Trajectory (N=53, S=1e5). `S_spectral = −Tr ln C = −Σ ln λᵢ` over the
**measured** eigenvalues; `S_closed(N,ρ̄)` is the equicorrelation prediction at the true
dimension; `S_C3 = −(N−1)ln(1−ρ̄)` is the parameter-free rigidity asymptote.

| p | ρ̄ | k_eff (PR) | **S_spectral** | S_closed(53,ρ̄) | S_C3 | dev_equicorr | S/C3 |
|---|---|---|---|---|---|---|---|
| 0.02 | 0.979 | 1.04 | **197.80** | 197.20 | 201.15 | +0.609 | **0.983** |
| 0.05 | 0.950 | 1.11 | **151.62** | 151.37 | 155.29 | +0.248 | 0.976 |
| 0.10 | 0.900 | 1.23 | **115.84** | 115.71 | 119.58 | +0.123 | 0.969 |
| 0.15 | 0.849 | 1.38 | 94.40 | 94.32 | 98.13 | +0.082 | 0.962 |
| 0.20 | 0.802 | 1.54 | 80.39 | 80.32 | 84.08 | +0.069 | 0.956 |
| 0.30 | 0.700 | 2.00 | 58.99 | 58.95 | 62.57 | +0.043 | 0.943 |
| 0.40 | 0.601 | 2.68 | 44.32 | 44.29 | 47.77 | +0.032 | 0.928 |
| 0.55 | 0.448 | 4.64 | 27.68 | 27.66 | 30.85 | +0.025 | 0.897 |
| 0.70 | 0.300 | 9.31 | 15.79 | 15.77 | 18.58 | +0.019 | 0.850 |
| 0.85 | 0.150 | 24.44 | 6.29 | 6.27 | 8.44 | +0.016 | 0.744 |
| 1.00 | ≈0 | 52.97 | 0.014 | 0.000 | −0.002 | +0.014 | n/a |

- **C2 direction (pre-declared) confirmed:** ρ̄ moves **monotonically** from ≈0 (p=1,
  chaos) up to 0.98 (p=0.02, rigidity pole). Withdrawing the drive takes the unit to the
  correct declared pole.
- **S genuinely diverges toward the rigidity pole.** With `k` correctly the dimension
  N=53, `S_spectral` climbs 0.01 → 197.8 along the ramp, and on the pure GHZ (ρ̄=1) the
  correlation matrix is rank-1: 52 singular eigenvalues, `S = +∞` (`n_singular=52`). That
  is T-E1b exhibited, not asserted. The old leg's "no divergence" caveat was an artifact
  of substituting PR (which → 1) for N.
- **The parameter-free asymptote is approached, and this is now a real test.**
  `S_spectral / S_C3 → 0.983` as ρ̄ → 0.98, falling away from the pole to 0.744 at ρ̄=0.15
  (where the neglected first term matters). C3's declared regime is the pole, and there the
  parameter-free `−(N−1)ln(1−ρ̄)` tracks the measured potential to within ~2%.
- **`dev_equicorr` is a residual that can fail.** It is `S_spectral − S_closed(N,ρ̄)`, zero
  iff the measured spectrum is exactly equicorrelated. On this ramp (a genuinely
  equicorrelated family) it stays ≤ 0.61. On non-equicorrelated classes it explodes:

  | class | ρ̄ | S_spectral | S_closed(N,ρ̄) | dev_equicorr |
  |---|---|---|---|---|
  | ghz_depol p=0.3 (equicorrelated) | 0.701 | 59.13 | 59.08 | **0.045** |
  | product (equicorrelated, ρ̄≈0) | ≈0 | 0.014 | 0.000 | **0.014** |
  | low_rank r=3 | −0.004 | 36.69 | 0.031 | **36.66** |
  | powerlaw α=0.8 | −0.001 | 7.35 | 0.002 | **7.35** |
  | ghz_z (rigidity) | 1.000 | +∞ | +∞ | 0 (both diverge) |

  Three orders of magnitude between equicorrelated and structured spectra. The falsifier
  now has teeth.

- **What this exposes about ρ̄.** `low_rank r=3` has ρ̄ ≈ −0.004 — the *mean* off-diagonal
  is ≈0 because its correlations are **signed and cancel** — yet its true log-det is 36.7.
  Consequently `k_eff_kish(N, ρ̄) = 53.0` ("chaos") while the spectral `k_eff_PR = 7.8`
  ("low-rank"). **The Kish ρ̄-parameterization is only faithful on the equicorrelation
  manifold**; off it, the first moment is blind to structure that the spectrum sees. Gate-0
  reads PR / eff-rank (spectral), so it is unaffected — but any k_eff computed *from ρ̄*
  inherits this blind spot. This sharpens the note's "two functionals of one spectrum"
  claim: `k_eff_PR` and `S_spectral` are both spectral; `k_eff_kish(N,ρ̄)` is a
  first-moment object and agrees with them only when the state is equicorrelated.

## ±1-thresholding attenuation caveat

The low-rank and power-law classes are built from a latent Gaussian, then sign-thresholded
to ±1 (the physical measurement condition). By the Van Vleck arcsine law
E[sign(x)sign(y)] = (2/π)arcsin(ρ_gauss), so correlations are attenuated by ≈2/π≈0.637 near
small ρ. Measured directly at N=53, S=1e5:

| α | β (Gaussian latent) | β (±1 thresholded) | mean\|off-diag\| atten. |
|---|---|---|---|
| 1.0 | 0.401 | 0.622 | 0.646 |
| 0.6 | 0.722 | 0.866 | 0.640 |

The attenuation factor (0.64) matches 2/π, and it **inflates β toward the noise value 1**
(flattens the spectrum). This is why α=0.6 reads β≈0.87 (vs a Gaussian β≈0.72) and, at
N=20, collapses onto the noise floor. The separation reported above already survives this
attenuation at N=53 — that is the honest quantum-measurement condition and the reason it is
tested here rather than on Gaussian latents.

## What this does NOT show

- **No real quantum data.** Product/GHZ/random-circuit-like/critical outcomes are all
  classical surrogates from known statistics; no device, no state-vector/Lindblad
  simulator. This is the calibration ruler only (SPEC N5), never a verdict.
- **The X-basis GHZ result is a limit, not a pass.** It demonstrates that
  Operationalization A is blind to N-body stabilizer coordination — a documented weakness
  (SPEC §7.3), not a corridor confirmation.
- **N=20 is underpowered for β.** Corridor and criticality are not β-separable at IBM
  scale; eff-rank must carry the verdict there, or N must be raised.
- **The C3 divergence rate is only partially exercised** (k–ρ coupling in the surrogate,
  above).
- **Random-circuit "corridor" is asserted here via a low-rank/latent-factor surrogate**,
  not from real Sycamore XEB bitstrings. Whether real random-circuit outcome correlations
  actually land on the saturation branch is the C1 test the SPEC still gates on real data —
  this calibration only establishes that the estimator *could* tell them apart at that
  (N,T) if they do.

## Bottom line

**N5 passes at Sycamore scale (N=53): β separates low-rank (≈0.19) from power-law
(≈0.61/0.87) from chaos/noise (≈1.0) with disjoint CIs, stably across S=1e4→5e5, even
after ±1-thresholding attenuation — so a real-data C1 verdict at N≈53 would be admissible.**
It **fails at IBM scale (N=20)**, where the short subsample range collapses the
corridor/criticality β-distinction and only eff-rank still separates the classes. The
depolarized-GHZ ramp confirms the C2 exit direction (monotone to the rigidity pole) and,
**with the corrected estimator (issue #7)**, exhibits a genuine S-divergence
(`S_spectral` 0.01 → 197.8 → +∞ at rank-1, `n_singular=52`) and a real approach to the
parameter-free asymptote (`S/S_C3 → 0.983`). The `dev_equicorr` residual now separates
equicorrelated (≤0.05) from structured spectra (low-rank 36.7, power-law 7.4) by three
orders of magnitude, so the C3 falsifier can actually fail. The earlier "k–ρ coupling
prevents a true S-divergence" caveat was an artifact of substituting the participation
ratio for the matrix dimension and is withdrawn. GHZ reproduces the N4 basis-fragility
exactly (rigidity in Z, chaos in X), confirming the MUB requirement is load-bearing.

Artifacts: `synth_shots.py`, `calibrate.py`, `make_figures.py`,
`calibration_results.json`, `beta_separation.png`, `c3_ramp_overlay.png`, `run.log`.
