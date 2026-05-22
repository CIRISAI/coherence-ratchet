# Shadow 3 — the ℓ=3 inflection shadow in the CMB — pre-registration

**Date:** 2026-05-22. The cosmological shadow: a present-epoch structural
feature in the CMB shape sector, after the joint P_ω operator is documented
non-constructible (F-11).

## The idea

The orthogonality theorem leaves bulk CMB power exactly ΛCDM; any
framework-distinctive content is in the shape sector. The framework's signed
multipole structure has a crossover — quadrupole (ℓ=2) toward isotropy, higher
multipoles toward concentration. The claim under test: the present-epoch CMB
ρ_ℓ profile carries a genuine structural inflection near ℓ=3, distinguishable
from ΛCDM Gaussian cosmic variance.

## The test

Use the CMB ρ_ℓ profile already computed this session (WMAP ILC + Planck SMICA,
reproduced to mean |Δ| = 0.0015; octupole excess +0.033/+0.037). Pre-register a
statistical test: build a ΛCDM Gaussian-cosmic-variance Monte-Carlo ensemble of
ρ_ℓ profiles; ask whether the observed signed-crossover structure (the ℓ=3
inflection) is **significant** against that ensemble, and whether its location
matches the framework's out-of-sample A3+-corridor calibration rather than a
free fit.

## Honest scope — read this

The session already established that the present-epoch CMB profile is
**calibration, not the framework-distinctive prediction** — the prediction is
the *temporal drift* (~10⁻⁹/decade, unobservably small). This test does **not**
re-label calibration as prediction. It asks only the narrow, genuine question:
is there a present-epoch ℓ=3 *structural feature* significant beyond cosmic
variance? This is the weakest of the three shadows and the most likely to NULL —
pre-registered as such.

## Two-sided verdict

- **PASS:** the ℓ=3 inflection is significant vs the ΛCDM cosmic-variance
  ensemble AND at the framework-predicted (out-of-sample-calibrated) location —
  a genuine present-epoch CMB signature.
- **NULL:** the ℓ=3 feature is within cosmic variance — the framework's CMB
  content remains the (unobservable-now) temporal drift; no present-epoch
  signature. A valid, expected-plausible result.

## Discipline

CUDA for the Monte-Carlo ensemble (cupy). Do not conflate present-epoch profile
(calibration) with temporal drift (prediction). The significance test is against
a genuine ΛCDM cosmic-variance ensemble, pre-registered. Two-sided; NULL is the
honest likely outcome and is reported flat. Incremental output.
