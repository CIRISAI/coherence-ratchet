# Thirdness of the cosmic halo field — blind higher-order measurement (PRE-REGISTRATION)

**Date 2026-07-20. Method frozen BEFORE any result is seen. No outcome predicted.**
Discovery run under the program's discipline: blind, exhaustive reporting, incremental
flush. This is the one uncashed measurement named in the Peirce/Thirdness thread — run
without a finger on the scale.

## The question

`S = −ln det C` reads the **pairwise (Secondness)** coordination of the matter field — it
is a functional of the correlation matrix alone (`s_of_a.py`: `C_ij = ξ(r_ij)/σ²`, and even
the "nonlinear" lognormal `S` is a Hadamard transform of that pairwise matrix). Is there
genuine **≥3-order ("Thirdness")** coordination in the SAME field, on the SAME grain, that
`S` is provably blind to? If so: how big is it relative to the pairwise books, and does it
carry its own history across cosmic time?

## The object

TNG300-1 halos, `large_volume/data/` — 26 snapshots, z = 3.0 → 0, positions + M200,
box L ≈ 205 Mpc/h. Mass-weighted density on a comoving grid = the field whose pairwise
books the DE pipeline reads. Same field, same box, same grain.

## The instrument's blind spot, turned into a null: phase randomization

FFT the gridded density `δ`, keep the amplitudes `|δ_k|` (the power spectrum = **all**
pairwise / Secondness content), randomize the phases (Hermitian-symmetric), inverse FFT.
The surrogate has an **identical correlation matrix `C`, hence identical `S`**, but zero
connected ≥3-point structure. Therefore any higher-order statistic that differs between the
real field and its phase-randomized surrogate **is** the Thirdness — and `S` cannot see it
by construction. (Standard non-Gaussianity isolation; here it doubles as the exact operational
definition of "what the ledger's Secondness misses.")

## Estimators — computed identically on real field and on each surrogate

1. **Raw reduced skewness** `S3(R) = ⟨δ_R³⟩ / ⟨δ_R²⟩²`, smoothing scales R ∈ {4, 8, 16} Mpc/h.
   The standard amplitude 3-point. AMPLITUDE-CARRYING → by the provenance line this channel
   is **upstream / off-ledger** (`S` is designed blind to amplitude). Recorded as the
   "expected, off-books" control, not the test.

2. **DECISIVE — copula skewness.** Normal-score the density cells: `g = Φ⁻¹(rank/(N+1))`,
   marginally N(0,1) by construction (this removes ALL amplitude/marginal structure — exactly
   the copula transform `S` is itself invariant under). Smooth, measure the standardized
   skewness `⟨g_R³⟩ / ⟨g_R²⟩^{3/2}`. A linear combination of *jointly* Gaussian cells is
   Gaussian (skew 0); nonzero smoothed skewness of a marginally-Gaussian field detects
   **joint (copula) non-Gaussianity** — genuine SHAPE-level 3-way coordination, dimensionless
   and amplitude-blind, legitimately on the same footing as `S`. **This is the one that matters.**

3. **Copula equilateral bispectrum** of `g` (Fourier), as an independent cross-check of (2).

**Null band:** N_surr = 20 phase-randomized surrogates per snapshot → null mean/std per
estimator → each estimator reported as a z-score `(signal − null_mean)/null_std`. Surrogate
subtraction also cancels finite-grid estimator bias (identical estimator, grid, sample size,
marginals, and power spectrum on both sides).

## Context recorded (NOT the test)

Per snapshot: halo count k(a) (total and above mass thresholds), σ(δ), and the pairwise
`S`-proxy for scale. These frame magnitude/epoch; they do not decide the verdict.

## Blind questions (no prediction filed — read sideways when the numbers land)

- Is the **copula** Thirdness above the null (z ≫ 0), or does it vanish once amplitude is
  removed (Thirdness entirely in the marginals → off-books by provenance, no shape-level Third)?
- Magnitude: copula Thirdness vs the pairwise books, and vs the raw amplitude channel.
- History: does R3(a) evolve — monotone, or interior-peaked? If peaked, does the peak sit at
  the DE epoch (z ≈ 0.5–0.6), at the halo count-peak (z ≈ 0.55), or nowhere in particular?
- Dilution: matter-like (∝ a⁻³) or its own law?

## Discipline

No synthetic data — the phase-randomized surrogate is the pre-committed NULL/control, not
data standing in for a measurement (same status as the CMB null ensembles). Grain fixed
before spectrum. Method frozen at this commit; nothing below is tuned after seeing R3.
Whatever it shows is a sliver to build into the whole — including "the copula Third is empty,"
which would confirm the current stance (higher-order coordination posts no κS) rather than
refute it.
