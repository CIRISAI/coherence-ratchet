# Pre-registration — GPU-substrate corridor-exit rate

**Experiment**: Measure the framework's corridor-EXIT / relaxation RATE from the
CIRISArray multi-GPU strain gauge, on the actual RTX 4090. Condition 2, the GPU
angle. Independent of the CMB shape-drift definition.

**Date pre-registered**: 2026-05-21. Committed BEFORE results, in its own commit.

## Motivation

The framework's dynamics (Piece 2, `dρ/dt = α − γM`; Claim 1, the corridor as a
bounded attractor) asserts that the within-rung correlation ρ has a *rate*. When
the active maintenance work `γM` is removed, `dρ/dt` is non-zero and the system
drifts off the corridor toward a pole. That exit RATE has never been measured at
any substrate — only the static corridor value of ρ has been.

Three prior attempts this session failed (`experiments/open_system_pomega/
corridor_exit_rate_llm.py`; `experiments/structural_series/corridor_dynamics/
paired/`; `.../celegans/`). Common cause: the corridor observable ρ was built as
a *static windowed correlation* with no clean time axis, OR (C. elegans) the
relaxation timescale τ_ac was comparable to or shorter than the sliding window W
— window-domination — so the measured "rate" was an artifact of the estimator,
not of the substrate. The C. elegans run produced a WINDOW-DOMINATED NULL:
τ_ac ≈ 15 s with a 30 s window, τ_ac > W in only 1/12 worms.

The GPU is the framework's HOME substrate: the Kish k_eff and the corridor were
originally calibrated there. CIRISArray Exp 51 Test 4 ("Coherence Decay") has
ALREADY measured a relevant quantity on the real RTX 4090: after a reset, the
running coherence r(t) of the oscillator array decays as
`r(t) = r∞ + A·exp(-t/τ)` with τ = 46.1 ± 2.5 s, a clean fit (r∞ ≈ 0, A ≈ 1).
This is the *unmaintained* relaxation: after a reset the array is not actively
held in any band — it relaxes freely. r∞ ≈ 0 is the chaos pole (decorrelated).
So the decay is, on its face, a corridor-EXIT toward the chaos pole, and
1/τ is the exit rate.

Crucially, τ ≈ 46 s while the running-correlation window in exp51 is 5 s
(50 samples at 10 Hz). τ ≫ W by ~9×. The window-domination failure mode that
killed the C. elegans measurement does NOT apply here — but this must be
verified directly from the run, not assumed.

This pre-registration fixes the analysis and the artifact controls BEFORE
re-running exp51 and looking at any fresh τ.

## Data

- **Instrument**: CIRISArray `experiments/exp51_physics_validation.py`, Test 4
  (`--test decay`), on the real RTX 4090 Laptop GPU with the CuPy backend
  (cupy 13.6.0, GPU confirmed available). 2048 ossicles × depth 64.
- **What is captured**: 120 s of continuous capture at 10 Hz of the array's
  k_eff signal `k_eff = r_ab·(1-x)·COUPLING_FACTOR·1000`, where r_ab is the
  within-array correlation between oscillator banks a and b on one device, and
  x is a clamped variance term. Then a running correlation r(t) is formed
  between adjacent 5 s (50-sample) windows of that k_eff series, and
  `r(t) = r∞ + A·exp(-t/τ)` is fit.
- **Real GPU runs only.** If exp51 will not run on the GPU in this environment
  (no CuPy, no device, import failure), that is reported honestly and the
  measurement is abandoned — no synthetic series is substituted.
- We run `--test decay` **three times** (independent resets / captures) to get
  an across-run spread on τ in addition to exp51's own single-fit covariance
  error bar.

## What r(t) must be for τ to count as a genuine corridor-exit rate

This is the load-bearing pre-commitment. τ counts as a genuine framework
corridor-exit relaxation rate ONLY IF all of the following hold. Any failure is
reported as artifact-contamination, an honest negative.

**(C1) r(t) is the relaxation of the framework's own coherence observable.**
The decaying quantity must be a correlation of the array's coherence/k_eff
state — the same family of object as the framework's within-rung ρ — and the
decay must be the array *losing* that coherence over time after a reset. We
verify by inspecting the exp51 code path directly: r(t) is the Pearson
correlation between consecutive windows of the single-device k_eff(t) series;
k_eff is the participation-style coherence signal; the decay is r → r∞.
This is an autocorrelation-of-coherence within ONE device's own time series.

**(C2) It is the WITHIN-array decay, not the cross-DEVICE artifact.**
CIRISArray explicitly flags cross-DEVICE coherence (r ≈ 0.97 between two
separate GPUs) as an ALGORITHMIC ARTIFACT: independent devices' k_eff series
correlate because the shared k_eff algorithm maps any thermalizing oscillator
bank onto similar r_ab trajectories — "the sensing was the algorithm itself"
(README Root Cause Analysis, Exp 55-56). That artifact concerns correlation
BETWEEN devices. The exp51 Test-4 decay is a correlation WITHIN a single
device's own k_eff time series across time. These are different quantities.
For C2 to pass we require: the decay is computed from one device only (verified
in code — `test_coherence_decay` instantiates one `PhysicsTestSensor`), and the
quantity that decays is the *temporal* autocorrelation of that one device's
coherence, which the artifact analysis does not touch. If on inspection the
decay turns out to be a cross-device or cross-bank quantity of the flagged kind,
C2 FAILS and the result is reported as artifact-contaminated.

**(C3) τ ≫ W — not window-dominated.** The running correlation uses a 5 s
window (50 samples at 10 Hz). A genuine relaxation rate requires the fitted
τ to substantially exceed the window: we pre-commit the gate **τ > 3·W = 15 s**.
If τ ≲ 15 s the decay is plausibly an artifact of the windowing (the
C. elegans failure mode) and is reported as a WINDOW-DOMINATED NULL. The
prior τ = 46 s clears this by ~3×; we require the fresh τ to clear it too.

**(C4) The fit is real, not imposed.** The exponential model must fit well:
we pre-commit (a) the fit converges, (b) r∞ and A are physically sane
(r∞ ∈ [-0.1, 0.3] — near the chaos pole; A ∈ [0.5, 1.5] — starts near full
correlation), and (c) the decay is monotone in the gross sense (r at the end of
the capture is below r at the start by at least 0.3). A flat r(t), or a fit that
rails against the bounds, fails C4.

**(C5) Reproducible across resets.** τ from the three independent runs must
agree within a factor of 2 (max/min < 2). The corridor-exit rate is then
reported as the across-run mean ± SD, combined with exp51's per-fit covariance
error. Wild run-to-run scatter (factor > 2) is reported as INCONCLUSIVE with the
full spread shown — not narrowed by dropping runs.

## Error / noise controls (pre-committed)

1. **Three independent captures.** Run-to-run SD of τ is the primary empirical
   error bar, reported alongside exp51's own curve_fit covariance σ_τ.
2. **No run dropping.** All three τ values enter the aggregate regardless of
   value. If one run fails to fit, that is reported as a failed run, not
   silently dropped.
3. **Window-domination gate (C3)** is checked and reported explicitly with the
   numbers (τ, W, τ/W).
4. **Artifact cross-check (C2)** is settled by direct code inspection of
   `test_coherence_decay`, reported in the results with the specific lines that
   establish it is a single-device temporal autocorrelation.
5. **r∞ reading.** r∞ is reported with its error. r∞ ≈ 0 means the array
   relaxes to the chaos pole (full corridor exit); r∞ substantially > 0 would
   mean it relaxes to a residual band, changing the framework reading from
   "exit to a pole" to "relaxation to a lower fixed point" — both are reported
   faithfully, only the first is a clean corridor-exit-to-pole.
6. **Honest scope clause.** Whatever the outcome, the result is ONE substrate
   (the GPU oscillator array) and ONE exit direction (toward chaos, r∞ ≈ 0,
   unmaintained). It does NOT yield a cosmological time-to-fidelity: that needs
   the cross-rung transport law and P_ω, both currently blocked. It gives
   condition 2 its first real substrate corridor-exit-rate datum, independent
   of the CMB shape-drift.

## Outcomes (pre-committed reading)

- **POSITIVE — genuine GPU corridor-exit rate.** C1–C5 all hold: the within-
  array coherence decays exponentially with τ > 15 s, reproducible across
  resets, r∞ near the chaos pole, clean fit. → Record
  `corridor-exit rate = 1/τ` (units 1/s) with error bars as condition 2's first
  real substrate datum at the GPU — the framework's home substrate.
- **WINDOW-DOMINATED NULL.** C3 fails (τ ≲ 15 s). → No rate claimed; the decay
  is an estimator artifact, same failure class as C. elegans.
- **ARTIFACT-CONTAMINATED NULL.** C2 fails (the decay is the flagged
  cross-device / shared-algorithm quantity). → Honest negative; reported as
  contaminated.
- **FIT-FAILURE / NON-MONOTONE NULL.** C4 fails. → No rate; reported plainly.
- **INCONCLUSIVE.** C5 fails (run-to-run scatter > factor 2). → Full spread
  reported, no headline number.

Whichever occurs is reported. An honest negative is a valid outcome and is as
informative as a positive — it tells condition 2 where the GPU substrate
breaks.

## Secondary (no pre-commitment, descriptive only)

Exp E4 (operational collapse threshold, k_eff_critical = 4.0) and Exp E1
(block-structure resilience, ρ_intra > ρ_inter) are read off their existing
committed CIRISArray results and described in framework terms — the corridor
k_eff floor, and Simon near-decomposability. These are not re-run and carry no
pre-registered pass/fail here.
