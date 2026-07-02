# Emergent cosmic structure -- k_eff saturation verdict (ADVERSARIAL probe)

## GRAIN CAVEAT (read first)

The universe is the one truly complete unit, but **any dataset is a subsample of
it** -- a finite volume of our past light cone. By the objective measure used this
session (saturation tested on a *complete* unit, e.g. the whole zebrafish brain),
a subsample can read high-dimensional for grain reasons **alone** -- exactly as
mouse-V1 cortex did. A complete-unit test is impossible in principle for
cosmology. Therefore a **non-saturating read here is GRAIN-INCONCLUSIVE, not a
falsification.** Nothing below should be read as either confirming or refuting the
corridor at the universal scale.

Also load-bearing: **this is NOT the CMB.** The framework is *exactly* LambdaCDM
for the CMB (orthogonality theorem). The corridor / low-rank content concerns
*emergent, gravitationally-evolved coordinating structure* -- the cosmic web --
which is what is spectrumed here. The two must not be conflated.

## Why this substrate is adversarial

The primordial matter power spectrum is nearly scale-invariant (n_s ~ 0.96 -- a
near power law). In this discriminator's language a **power-law, non-saturating
spectrum IS the criticality signature.** So cosmology is the one substrate whose
natural prior is exactly the "trivial / power-law" read. A corridor that is a
universal claim has to survive here; the honest expectation is that it will look
power-law, and the interesting question is whether that read is grain-confounded.

## Dataset + where

- **SDSS DR17 spectroscopic galaxies**, pulled live from the SkyServer SQL service
  (`https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch`, CSV).
- Selection: `class='GALAXY'`, `zWarning=0`, `z in [0.02,0.15]`, contiguous NGC
  window `ra in [130,240]`, `dec in [0,60]`. **389,751 real galaxies.** Cached to
  `cosmo_sdss_galaxies.parquet`.
- Real data only. Synthetics (low-rank / power-law / noise) are used **solely** to
  calibrate the estimator at this (N,T); they never enter the verdict.

## The units x observations matrix (N, T)

Galaxies -> comoving Cartesian (Planck-ish flat LambdaCDM, H0=100 so units are
Mpc/h) -> a fine cubic mesh of **micro-cells (L = 10 Mpc/h)**. The survey interior
is tiled with disjoint **sub-cubes of 5^3 = 125 micro-cells (50 Mpc/h)**; each
sub-cube fully inside the footprint is one observation.

    X[i, t] = overdensity delta of relative micro-cell position i in sub-cube t
    UNITS (rows, subsampled)   N = 125  relative micro-cell positions
    OBSERVATIONS (cols)        T = 159  survey-interior sub-cubes   (T > N, well-conditioned)

The unit x unit correlation over sub-cubes is, by construction, the **normalized
two-point density covariance** C_ij ~ xi(|r_i - r_j|). **Its eigenvalues are the
discrete power-spectrum modes** -- so alpha (eigenvalue power-law slope) is
literally a P(k) diagnostic. This is why the matrix was built this way rather than
as a galaxies x few-properties table (which would be trivially rank-bounded by the
feature count).

## Calibration at N=125, T=159 (the ruler works here)

| synthetic | PR | eff_rank (vs surrogate) | beta_sub | alpha |
|---|---|---|---|---|
| low-rank r=3   |  4.2 | 3 | 0.043 | 1.06 |
| power-law a=1.0| 20.5 | 7 | 0.279 | 1.08 |
| power-law a=0.6| 49.3 | 6 | 0.529 | 0.73 |
| power-law a=0.3| 64.5 | 3 | 0.650 | 0.58 |
| pure noise     | 70.7 | 0 | 0.693 | 0.50 |

beta cleanly separates saturation (~0) from power-law growth (0.3-0.7); alpha
recovers the injected slope. Estimator validated at this grain.

## Result on the real cosmic web

| N | T | PR / k_eff | eff_rank (MP) | eff_rank (surrogate) | MP edge | beta | alpha |
|---|---|---|---|---|---|---|---|
| 125 | 159 | **51.76** | 7 | 7 | 3.56 | **0.574** | **0.745** |

Saturation curve (PR vs N') -- **climbs monotonically, no plateau:**

| N' | 8 | 12 | 16 | 24 | 32 | 48 | 64 | 80 | 100 | 125 |
|----|---|----|----|----|----|----|----|----|-----|-----|
| PR | 7.4 | 10.7 | 13.7 | 19.1 | 23.7 | 31.4 | 37.2 | 42.0 | 47.0 | 51.8 |

- Top eigenvalues decline **smoothly** (6.08, 5.52, 4.96, 4.54, 4.12, 3.87, ...)
  -- a smooth power-law decay, **not a few spikes over a flat noise bulk**. That
  is the power-law / criticality fingerprint (near-scale-invariant P(k)), not the
  low-rank one. (Only 7 modes clear the phase-randomized noise floor, but PR is
  high because the tail is a heavy power law, not because of many discrete spikes.)
- **Robustness (not a grid artifact):** re-tiling at other resolutions gives the
  same regime -- 48 Mpc/h (N=64,T=192): beta=0.675, alpha=0.636, PR=36.8; 60 Mpc/h
  (N=64,T=85): beta=0.580, alpha=0.753, PR=30.3; 50 Mpc/h (N=125): beta=0.577,
  alpha=0.745, PR=51.8. beta ~ 0.58-0.68, alpha ~ 0.64-0.75 throughout.

## VERDICT: NON-SATURATING / POWER-LAW -- but GRAIN-INCONCLUSIVE

Effective dimensionality does **not** saturate at the ~10 corridor ceiling
(PR=52 and still climbing at full N); the eigenspectrum is a smooth power law
(alpha ~ 0.75, beta ~ 0.57), sitting between the a=0.6 and a=1.0 synthetics and
well above the pure-noise floor (alpha=0.50). **This is exactly the adversarial
cosmological scale-invariance signature** -- the near-power-law P(k) of emergent
large-scale structure showing through, as expected for this substrate.

**But it is grain-confounded and must not be over-read.** The SDSS wedge is a
finite past-light-cone subsample, and a complete-unit test is impossible for the
universe in principle. By this session's own standard (saturation only decisive on
a *complete* unit), a power-law read from a subsample is **inconclusive, not a
falsification** -- the same reason mouse-V1 cortex was set aside. It neither
confirms nor refutes the corridor at the universal scale; it confirms only that
cosmology behaves adversarially exactly where the framework predicted it would
(power-law, because P(k) is near-scale-invariant), and that the discriminator
cannot resolve the corridor question at any grain we can actually sample.

Artifacts: `spectral_cosmo.py`, `spectral_results_cosmo.json`,
`cosmo_sdss_galaxies.parquet`.
