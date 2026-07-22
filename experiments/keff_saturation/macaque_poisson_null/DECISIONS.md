# Macaque detailed-balance |z| = 8.8 vs a Poisson-count-matched null — PRE-REGISTRATION

**Date: 2026-07-21.** Written and frozen BEFORE any number from this run was computed.
Null-type debt against a CLAUDE.md STANDING RESULT:

> "Axis 2 (maintenance): detailed-balance breaking = the γM term (estimator validated;
> macaque motor cortex |z|=8.8 coordinating, galaxy baryon cycle z≈0 bound)."

Frozen prior work (READ ONLY, not edited by this run):
`experiments/keff_saturation/spectral_spikes.py`, `spectral_results_spikes.json`,
`spectral_spikes_summary.md`, `entropy_production.py`, `spectral_test.py`.
Output of this run lives only in `experiments/keff_saturation/macaque_poisson_null/`.

---

## 0. The debt

The published |z| = 8.83 was computed on **20 ms spike counts**. Spike counts are
discrete Poisson-like draws; the frozen summary itself records that spike shot noise
inflates the correlation spectrum (PR 132 → 58 under smoothing). **K4** (2026-07-20,
`papers/notes/the_third_prenup.md`; method in
`experiments/cosmo_entropic_potential/thirdness/discriminator/`) established that
exactly this null-type mismatch — a continuous-field surrogate used against discrete
count data — can manufacture an apparently-robust multi-sigma signal. The correct null
for a count statistic is a **count-matched** null.

### 0.1 A methodological fact recorded before the run (read from the frozen code, not a result)

Reading `entropy_production.py`, the published `|z|` is **not** a surrogate-referenced
z at all. `_angvel_z` computes

    dθ_t = wrapped angular increment of the top mode-pair;  μ = mean(dθ)
    SE    = sd over 400 moving-block bootstrap resamples (block = 50) of mean(dθ)
    z     = μ / SE

i.e. a **block-bootstrap t-statistic for "mean winding rate ≠ 0"** on the data's own
increments. The phase-randomized surrogate in `spectral_spikes.py` is used for the
*saturation / effective-rank* readout only. So the "null ceiling ~1.5" quoted beside
|z| = 8.8 is the value this same bootstrap-t happens to take on synthetic
OU-equilibrium/relaxation trajectories at matched T — a **synthetic calibrator**, not a
null built from the macaque data. This makes the debt sharper, not weaker: the statistic
has never been referenced to any surrogate constructed from the real spike trains.

This run therefore reports **two levels** of statistic (§3).

---

## 1. Data

DANDI:000140 `MC_Maze_Small`, asset
`sub-Jenkins/sub-Jenkins_ses-small_desc-train_behavior+ecephys.nwb`
(asset_id `7821971e-c6a4-4568-8773-1bfa205c13f8`, 29,207,528 bytes), macaque M1+PMd,
sorted spikes, delayed-reach maze task. The file used by the frozen run lived in a
prior session scratchpad and is gone; it is **re-fetched from the DANDI REST API** for
this run. Real data only. Identity is confirmed by reproducing the frozen run's
reported load line (142 units, 131,669 spikes, ~293.7 s, 100 reaches) and the frozen
primary |z| = 8.83 — see §6 gate.

Primary matrix (the one carrying the standing result): **whole-session**, all ~293 s,
20 ms bins, Gaussian smoothing σ = 1 bin, 142 units × ~14,684 bins.

## 2. The estimator — UNCHANGED

The frozen estimator is used verbatim by import, no reimplementation:
`entropy_production.irreversibility_from_units(X, k=4)` — z-score units, SVD, take the
top 4 temporal modes, evaluate the block-bootstrap winding statistic on all
C(4,2) = 6 mode pairs, return the pair with the largest |z|. The max-over-pairs
selection is part of the estimator and is therefore applied **identically to every
surrogate** (no selection asymmetry).

Recorded per evaluation: `winding_rate` μ, bootstrap SE, inner `z = μ/SE`, chosen pair.

## 3. The two statistics

- **Inner |z|** (the published statistic): μ/SE, bootstrap-t. Reported for the real data
  and for every surrogate. The published claim's implicit content is that surrogates
  sit near ~1.5 while the data sits at 8.8.
- **Outer z** (the null-referenced statistic this run adds):
  `z_out = (|μ|_real − mean|μ|_null) / sd(|μ|_null)`, plus the exact empirical
  percentile / one-sided p of |μ|_real in the surrogate distribution. A companion
  `z_out(|z|)` is computed the same way on the inner-|z| statistic. **The outer z on
  |μ| is the primary adjudicator**; the outer z on inner-|z| is reported alongside
  because the published number is an inner |z|.

Sign convention: |μ| (magnitude of net winding) is used because the null has no
preferred rotation direction and the estimator already selects a pair by |z|.

## 4. The nulls — construction, frozen

All surrogates are generated at the **spike-count level**, then passed through the
*identical* smoothing and estimator path as the real data. N = 200 surrogates per null
at the primary configuration; N = 100 per null at each swept bin width (compute
budget, declared in advance).

- **NULL-P — phase-randomized (the original null type, for side-by-side).**
  `spectral_test.phase_randomize` applied to the smoothed real count matrix: preserves
  each unit's power spectrum, randomizes phases, destroys cross-unit alignment. Produces
  a continuous field — **does not reproduce count discreteness or Poisson shot noise.**
  This is the null the standing result was implicitly read against.

- **NULL-A — constant-rate Poisson (primary count-matched null).**
  For each unit i, counts in every bin drawn i.i.d. `Poisson(λ_i)` with
  `λ_i = (total spikes of unit i) / (number of bins)` — the measured per-unit firing
  rate. Reproduces: count discreteness, Poisson shot noise, the full per-unit rate
  heterogeneity (142 different λ). Contains: **zero** coordination and zero temporal
  structure. This is the direct test of "is |z| = 8.8 manufactured by shot noise."

- **NULL-B1 — rate-profile-matched Poisson, independently time-shifted (strict
  coordination null).**
  For each unit i, estimate a smooth time-varying rate `r_i(t)` by Gaussian-smoothing
  its binned counts with **σ_rate = 500 ms** (25× the 20 ms analysis bin, and 25× the
  σ = 1 bin analysis smoothing — chosen so the rate profile carries slow task-locked
  structure, not the fine structure the estimator reads). Each `r_i` is then **circularly
  shifted by an independent uniform random lag**, and counts are drawn `Poisson(r_i(t+φ_i))`.
  Preserves: shot noise, discreteness, each unit's own rate magnitude, non-stationarity
  and autocorrelation. Destroys: cross-unit temporal alignment, i.e. the coordination.
  σ_rate = 500 ms and the circular-shift construction are frozen here before any result.

- **NULL-B0 — rate-profile-matched Poisson, UNSHIFTED (diagnostic, non-adjudicating).**
  Identical to B1 but with no shift, so cross-unit coordination above the 500 ms scale
  is *retained*. B0 is **not** a null for coordination; it is a shot-noise-only
  resample and is reported purely as a diagnostic that isolates how much of the read is
  carried by the smooth rates versus by the individual spikes. **No pass/fail hangs on
  B0.** It is declared here so it cannot be introduced post hoc as a defense.

## 5. Bin-width sweep (the "smoothing defense" test)

The frozen summary's partial defense on record: the signal *strengthens* as shot noise
is smoothed away (|z| 4.6 at 10 ms → 44 at 50 ms/σ2.5), which is argued to show the
rotation is a rate-level phenomenon that shot noise works *against*.

Sweep: bin ∈ **{20, 50, 100, 200} ms**, smoothing σ = 1 bin throughout (one smoothing
setting, so bin width is the only varying factor — the frozen table confounded the two).
At each bin width, the real value **and all four nulls** are recomputed. This is the
load-bearing addition: the frozen defense observed only that the *real* |z| rises. If
the *null* |z| rises just as fast, the defense is empty.

Reading rule, frozen:
- Defense **VERIFIED** if the outer z (null-referenced) rises, or holds ≥ its 20 ms
  value, across the sweep.
- Defense **REFUTED** if the outer z falls with coarser bins while the inner |z| rises —
  that pattern means the rise is a property of the statistic/T, not of the signal.

## 6. Gate (must pass before any verdict is read)

The re-fetched file must reproduce the frozen run: 142 units, 131,669 spikes, 100
reaches, and whole-session 20 ms/σ1 inner |z| within 0.05 of the frozen 8.83. If the
gate fails, the run reports the discrepancy and does not issue a verdict on the standing
result.

## 7. Pass / fail — frozen before any number

Adjudicated at the **primary configuration** (whole-session, 20 ms, σ = 1 bin), on the
outer z / empirical p of |μ|_real against **NULL-A and NULL-B1**:

- **SURVIVES** — the |z| = 8.8 coordinating verdict stands against a Poisson-matched
  null: |μ|_real exceeds the null distribution at **p < 0.01 one-sided under BOTH
  NULL-A and NULL-B1** (equivalently outer z ≥ 2.58 with no surrogate breach at
  N = 200 → p < 0.005), **and** the bin sweep does not show the refutation pattern of §5.

- **SHOT-DRIVEN (KILL FIRES)** — the standing result is a null-type artifact:
  |μ|_real lies **inside the central 95%** of NULL-A (p > 0.05), i.e. a
  coordination-free Poisson count process at the measured firing rates reproduces the
  published statistic. Equivalently: NULL-A's inner |z| distribution brackets 8.8.

- **PARTIAL / WEAKENED** — anything between: p < 0.01 under one Poisson null but not
  the other; or 0.01 ≤ p ≤ 0.05; or survival at 20 ms with the §5 refutation pattern in
  the sweep. Reported as PARTIAL with the exact numbers, never rounded up to SURVIVES.

A separate, non-adjudicating note will be recorded if NULL-P (phase-randomized) itself
turns out not to sit near the quoted ~1.5 ceiling — that would be a fact about the
original null, reported plainly either way.

## 8. Prior expectation on record

The program's prior is **SURVIVES**, on the smoothing defense (§5): the directed
rotation in macaque M1/PMd during reaching is a textbook rate-level phenomenon
(Churchland et al. 2012 jPCA), so shot noise should work *against* it, not for it.
This prior is recorded so that a fired kill cannot be re-narrated afterwards as
expected. The run is executed blind to outcome and whatever comes is reported —
a fired kill on a CLAUDE.md standing result is reported as plainly as a survival.

## 9. Discipline

No synthetic *empirical* data: the Poisson surrogates are pre-committed NULL controls
generated from the real measured rates, never used as data. Results flush
incrementally to `results.json` / `run.log` so a wedge leaves recoverable partial work.
No edits to frozen `keff_saturation` files, no CLAUDE.md edit, no registration edit,
no git commit.
