# Shadow 3 — the ℓ=3 inflection shadow in the CMB — RESULTS

**Date:** 2026-05-22. Two-sided, pre-registered (`PREREGISTRATION.md`).
**Verdict: NULL.** The honest, pre-registered-as-likely outcome.

## What was tested

Is there a genuine present-epoch structural inflection near ℓ=3 in the CMB ρ_ℓ
shape profile, statistically distinguishable from a ΛCDM Gaussian cosmic-variance
ensemble, at the framework's out-of-sample-calibrated location?

- **Observed profile.** Rotation-averaged (frame-invariant) ρ_ℓ for ℓ=2..12,
  computed from WMAP 9-yr ILC and Planck 2018 SMICA — the session's profile,
  reproduced. The octupole excess reproduces in both maps (joint
  D₃ = ρ₃ − ensemble-mean = **+0.0283**; consistent with the session's
  +0.033/+0.037 figures). The Kish-ρ measure is the session's: ρ_ℓ from the
  power-participation ratio over the 2ℓ+1 real harmonic modes.
- **ΛCDM cosmic-variance ensemble.** Under ΛCDM + statistical isotropy the
  2ℓ+1 aₗₘ at fixed ℓ are i.i.d. Gaussian. ρ_ℓ is scale-free in the power
  (depends only on the *shape* of the power distribution over m, not on Cℓ), so
  the per-ℓ cosmic-variance distribution of ρ_ℓ is exactly the distribution over
  Gaussian aₗₘ draws — no Cℓ input needed. Built on GPU (cupy), N = 4,000,000
  realizations per multipole.

## Result — the ℓ=3 feature is within cosmic variance

| ℓ | obs ρ_ℓ | ΛCDM ens. mean | ens. std | z | p (two-sided) |
|---|---------|----------------|----------|------|---------------|
| 2 | 0.2862 | 0.2857 | 0.176 | +0.00 | 0.81 |
| **3** | **0.2505** | **0.2222** | **0.130** | **+0.22** | **0.64** |
| 4 | 0.1708 | 0.1818 | 0.102 | −0.11 | 0.88 |
| 5 | 0.1440 | 0.1539 | 0.082 | −0.12 | 0.89 |

Structure tests against the ΛCDM ensemble:

- **Octupole excess** D₃ = +0.0283 — P(D₃_null ≥ D₃_obs) = **0.319**, z = +0.22.
- **ℓ=3 inflection** C₃ = ρ₃ − ½(ρ₂+ρ₄) = +0.0220 (the discrete second
  difference centred on ℓ=3) — two-sided p = **0.756**, z = +0.13.
- **Quadrupole offset** D₂ = +0.0005 — essentially at the ensemble mean; no
  signed "toward-isotropy" deficit.

Every multipole sits within ±0.25σ of the ΛCDM cosmic-variance mean. The
two-sided p-values are all ≥ 0.6.

## Why the earlier "+0.033 excess" is not a signal

The session's octupole figure (+0.033 WMAP / +0.037 Planck) was the departure
from the ensemble **mean**. This shadow's test is against the full cosmic-variance
**distribution**. At low ℓ the ρ_ℓ cosmic-variance spread is large — std ≈ 0.13
at ℓ=3, ≈ 0.18 at ℓ=2 — because ρ_ℓ is computed over only 2ℓ+1 = 7 modes, and a
7-mode participation ratio is intrinsically noisy. A +0.028 excess against a
0.13 spread is z ≈ +0.22: entirely ordinary. The octupole excess reproduces
across two independent instruments and pipelines (it is real CMB structure, not
ILC residual — the session established that), but reproducing-across-maps tests
the *measurement*, not *significance vs cosmic variance*. A single-sky feature
that is sub-σ in the cosmic-variance distribution is sub-σ no matter how many
instruments confirm the sky.

## ℓ=3 is not the framework-predicted location

The framework's out-of-sample crossover — the A3+-calibrated corridor (k_eff ∈
[2.8, 4.8], 5 substrates, no CMB data) mapped through the Kish identity to a
per-ℓ corridor centre — has the observed profile crossing the centre curve at
**ℓ=4** here (the session's `cmb_corridor_prediction.py` reported ℓ~5; either
way, not ℓ=3). The octupole ℓ=3 is a known CMB anomaly, but the framework does
not single it out: its out-of-sample calibration points at ℓ~4–5. Treating ℓ=3
as the predicted location would be a free fit to the famous anomaly, not a
prediction. Neither the significance leg nor the location leg passes.

## Verdict

**NULL** on both legs:

1. The ℓ=3 feature (octupole excess and the centred inflection statistic) is
   within ΛCDM Gaussian cosmic variance — p = 0.32 and 0.76 respectively.
2. The framework's out-of-sample-calibrated crossover is at ℓ≈4, not ℓ=3.

There is no present-epoch ℓ=3 structural signature distinguishable from ΛCDM.

## Honest assessment — calibration vs prediction

This NULL does not weaken the framework, and it does not strengthen it. It
confirms the line the session already drew:

- The **present-epoch CMB ρ_ℓ profile is calibration**, not the
  framework-distinctive prediction. The Planck/WMAP cross-check secured that the
  Kish-ρ observable is trustworthy (mean |Δ| = 0.0015 between independent maps).
  This shadow adds: the calibration profile is also statistically
  indistinguishable from ΛCDM — exactly what "calibration" should be. A
  present-epoch profile that *was* anomalous would be a different and harder
  thing to explain.
- The **framework-distinctive prediction is the temporal drift**
  (d⟨ρ_ℓ⟩/dβ, signed per multipole), of order ~10⁻⁹/decade — unobservably
  small at present. This shadow does not test it and does not re-label the
  calibration profile as a prediction. The drift remains the open, untested,
  framework-distinctive content.

The pre-registration named this the weakest of the three shadows and the most
likely to NULL. It NULLed, cleanly, and the result is reported flat. The honest
read: at the present epoch the CMB shape sector carries no framework signature
beyond cosmic variance; the framework's only CMB claim with teeth is the
temporal drift, which is not observable now.

## Files

- `measure_ell3_shadow.py` — analysis (GPU ensemble, incremental JSON output)
- `results_ell3_shadow.json` — full numeric results
- Input maps: `experiments/open_system_pomega/cmb_data/` (WMAP ILC 9yr,
  Planck SMICA R3) — real CMB data, no synthetic data used.
