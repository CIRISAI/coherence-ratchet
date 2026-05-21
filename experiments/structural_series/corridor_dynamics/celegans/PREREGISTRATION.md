# Pre-registration — C. elegans corridor relaxation rate

**Experiment**: Measure the framework's corridor-exit / relaxation RATE from real
C. elegans whole-brain calcium-imaging time-series data. Condition 2, the
C. elegans angle.

**Date pre-registered**: 2026-05-21. Committed BEFORE results.

## Motivation

The framework (Piece 2, `dρ/dt = α − γM`; Claim 1, the corridor) asserts a
*dynamics* for the within-rung correlation ρ. It has only ever measured the
STATIC value of ρ — including at C. elegans whole-brain calcium (v15_celegans:
within-rung |ρ| ≈ 0.41–0.52, cross-rung |τ| ≈ 0.86–0.96). The corridor's local
RATE CONSTANT — how fast ρ(t) relaxes back toward its mean after a fluctuation
— has never been measured at any biological substrate.

A computable cosmological "time to fidelity" needs a corridor-exit-rate
calibration that is INDEPENDENT of the CMB shape-drift definition (which is
otherwise circular: that drift rate was itself defined as order-unity-per-Hubble
-time). C. elegans whole-brain calcium is a real neural TIME SERIES, so a
relaxation rate is genuinely extractable, unlike from a static snapshot.

This pre-registration fixes the analysis BEFORE looking at any rate result.

## Data

- **Source**: `qsimeon/celegans_neural_data` (HuggingFace), the `Kato2015`
  subset — Kato et al. 2015, *Cell* 163:656, "Global Brain Dynamics Embed the
  Motor Command Sequence of C. elegans". This is the canonical whole-brain
  calcium-imaging dataset. Already present on disk from prior v15 work.
- **Worms**: all 12 Kato2015 worms (`worm0`–`worm11`). N ≈ 107–151 neurons each;
  T ≈ 2161 (dt ≈ 0.336 s, 720 s) or 3243 (dt ≈ 0.375 s, 1080 s) timepoints.
- Calcium traces are provider-preprocessed: standard (z-score) normalization,
  moving-average smoothing. We use ALL neurons per worm (not only labeled ones)
  — the corridor observable is a population statistic, identity is not needed.
- The per-worm `time_in_seconds` column gives the real sampling interval dt.

**Real data only.** If the parquet is not readable in this environment we
report "not accessible" and stop. No time series is fabricated.

## Step 1 — The corridor observable ρ(t)

The framework's within-rung correlation ρ is read from the effective
dimensionality k_eff of the neural population state via the Kish identity
(Piece 1): for a population of N constituents,

    k_eff = (Σλ)² / Σλ²        (participation ratio of the covariance spectrum)
    ρ(t)  = (N/k_eff − 1) / (N − 1)        (invert k_eff = N/(1+ρ(N−1)))

ρ(t) is computed on a SLIDING WINDOW of the neuron×time matrix:

- Window length W_sec = 30 s (a fixed wall-clock window; converted to a sample
  count W = round(W_sec / dt) per worm, so all worms use the same physical
  window despite different dt). 30 s is chosen to span ≈ 1–2 global brain-state
  cycles (the Kato global cycle is tens of seconds) so each window contains a
  representative slice of the dynamics. The window covariance is over time
  WITHIN the window, neurons as variables.
- Step = 1 sample (maximally resolved trajectory).
- At each window position t: covariance of the N×W sub-matrix, eigenvalues
  λ ≥ 0, k_eff and ρ(t) as above.

This yields ρ(t), a time series, the corridor trajectory.

**Pre-committed expectation**: ρ(t) fluctuates around a mean ρ̄ in the static
corridor band (v15 found ≈ 0.4–0.5 for labeled-neuron subsets; the all-neuron
population value may differ and is not pre-committed to a band).

## Step 2 — The relaxation rate (the corridor's local rate constant)

The corridor is, in the framework, an attractor for ρ. After a fluctuation away
from ρ̄, ρ(t) relaxes back. The relaxation rate is the rate constant of that
return. Two estimators, pre-committed, reported together:

**(2a) Autocorrelation time τ_ac.** Compute the autocorrelation function (ACF)
of the mean-subtracted ρ(t). Fit an exponential `ACF(lag) = exp(−lag/τ_ac)` to
the ACF over the lag range from 0 up to the first zero-crossing (or to 3·τ_ac,
whichever is reached first; if no zero-crossing, up to lag = T/4). τ_ac is the
e-folding lag, in seconds. The relaxation RATE is `k_relax = 1/τ_ac` (units 1/s).
Also report the integrated autocorrelation time τ_int = 1 + 2·Σ_{lag>0} ACF(lag)
(summed to the first zero-crossing) as a fit-free cross-check.

**(2b) OU drift coefficient.** Model ρ(t) as an Ornstein–Uhlenbeck process:
`dρ = −θ(ρ − ρ̄) dt + σ dW`. Estimate θ by lag-1 autoregression on the
sampled series: regress (ρ_{t+1} − ρ_t) on (ρ_t − ρ̄); the slope is −θ·dt, so
`θ = −slope/dt` (units 1/s). θ is the OU mean-reversion rate — the direct
analogue of the corridor restoring rate in `dρ/dt = α − γM` linearised about
ρ̄. For a pure exponentially-correlated process θ ≈ 1/τ_ac; reporting both
checks consistency.

Both rates are computed per worm; the across-worm distribution (mean ± SD,
range, N=12) is the headline.

## Step 3 — Dimensionless normalisation (the transportable number)

A rate in 1/s is substrate-specific. The transportable, non-circular quantity
is the relaxation rate divided by the worm's INTRINSIC neural timescale.

- **Intrinsic timescale T_global**: the dominant period of the global
  brain-state dynamics. Computed from the first principal component (PC1) of the
  full neuron×time matrix — PC1 of Kato whole-brain data is the well-known
  global brain-state cycle. T_global = 1 / f_peak, where f_peak is the peak
  frequency of the PC1 power spectrum (Welch periodogram), searched in the band
  [1/300 s, 1/8 s] to exclude DC drift and high-frequency noise. Reported per
  worm in seconds; the Kato literature value is tens of seconds (≈ 30–100 s),
  which serves as a sanity range, not a pre-imposed answer.

- **Dimensionless relaxation rate**:

      r* = k_relax · T_global = T_global / τ_ac

  and likewise `θ* = θ · T_global`. r* is "how many corridor-relaxations occur
  per global brain-state cycle". This is the number transportable to other
  substrates and comparable to a cosmological corridor-exit rate per Hubble
  cycle. r* > 1: ρ relaxes faster than the global cycle (tightly corridor-
  pinned). r* < 1: ρ relaxes slower than the global cycle (loosely held).

## Step 4 — Finite-sample / noise controls (pre-committed)

1. **Phase-randomised surrogate null.** For each worm, generate 200 surrogates
   by independently phase-randomising each neuron's trace (preserves each
   neuron's power spectrum, destroys cross-neuron correlation structure and any
   genuine ρ-dynamics). Recompute ρ(t) and its τ_ac / θ on each surrogate. If
   the real τ_ac is within the surrogate τ_ac distribution, the measured
   relaxation rate is NOT distinguishable from the autocorrelation a windowed
   estimator imposes on independent traces — report that as a NULL. The
   surrogate distribution also gives the noise floor / error bar.

2. **Window-induced autocorrelation.** A sliding window of length W mechanically
   correlates ρ(t) at lags < W even for white input. We therefore (i) report
   τ_ac in seconds alongside W in seconds, and (ii) require, for a positive
   result, that the real τ_ac exceed both W and the surrogate τ_ac. If
   τ_ac ≲ W the measurement is window-dominated and reported as such — an
   honest null, not a rate.

3. **Window-length sensitivity.** Repeat the whole pipeline at W_sec ∈
   {20, 30, 45} s. A genuine relaxation rate should be roughly stable (within
   error bars) across W; strong W-dependence is reported as instability.

4. **Error bars.** The headline rate carries (a) across-worm SD (N=12) and
   (b) the surrogate-null spread. Both are reported. A rate whose across-worm
   SD or surrogate overlap is large is reported WITH the wide error bars and
   called inconclusive — not narrowed by selection.

5. **No worm dropping, no cherry-picking.** All 12 Kato2015 worms enter the
   aggregate. If a worm's PC1 has no clear spectral peak in the band, its
   T_global is flagged and it is excluded ONLY from the dimensionless aggregate
   (its 1/s rate still reported), and the exclusion is stated explicitly.

## Outcomes (pre-committed reading)

- **POSITIVE**: real τ_ac > W and > surrogate τ_ac across most worms; r* and θ*
  cluster with a reportable mean ± SD; roughly W-stable. → first measured
  corridor relaxation rate at a biological substrate, dimensionless.
- **WINDOW-DOMINATED NULL**: τ_ac ≲ W. → the observable is too noisy to carry a
  relaxation rate at this window; reported plainly.
- **SURROGATE NULL**: real τ_ac inside the surrogate distribution. → the
  ρ(t)-dynamics is not distinguishable from windowed independent noise.
- **INCONCLUSIVE**: large across-worm SD or strong W-dependence. → reported with
  the error bars, no headline number claimed.

Whichever occurs is reported. A null is a valid honest outcome.
