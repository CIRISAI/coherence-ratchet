# Pre-registration — C. elegans neural in-corridor substrate, robust re-run

**Wave:** `experiments/structural_series/robust_rerun/PREREGISTRATION.md` (S1
neural in-corridor). **Date pre-registered:** 2026-05-21. Committed BEFORE any
debiased-ρ result is computed.

## What v1 claimed

Paper v1 (`papers/Corridor Dynamics.tex`, §sec:corridor-empirical,
"Substrate 1: neural"): C. elegans whole-brain calcium imaging, 337 worms across
11 published studies, "within-rung correlation in a bounded band per functional
class; the Venkatachalam 2024 uniform-at-0.5 pattern was study-specific;
cross-lab the bands sit at command 0.52–0.75 and sensory/interneuron/motor
0.25–0.45 in 10/11 studies." Figure 1 records the substrate-local band as
0.25–0.75.

The v1 estimator (`experiments/v15_celegans/run_v15a_methodology.py`,
`run_v15b_epochs_replication.py`) was the **raw** mean absolute pairwise
Pearson correlation within each functional class — no surrogate floor, no
participation-ratio k_eff. The robust re-run re-measures the same data under the
structural series' debiased estimator.

## Data

- **Source:** `qsimeon/celegans_neural_data` (HuggingFace), the aggregated
  whole-brain calcium-imaging corpus already on disk at
  `experiments/v15_celegans/celegans_neural_data/worm_data_short.parquet`
  (42,798 rows, 12 source studies, 919 (study, worm) units; this is the same
  parquet `run_v15a` / `run_v15b` load). The 12 studies are Kato2015,
  Skora2018, Nichols2017, Kaplan2020, Yemini2021, Uzel2022, Flavell2023,
  Leifer2023, Lin2023, Dag2023, Venkatachalam2024, Nejatbakhsh2020. v1's "11
  studies" reflects whichever subset cleared its inclusion gate; we report
  whatever clears ours and state the count.
- Calcium traces are provider-preprocessed (standard z-score normalization,
  moving-average smoothing) via the `calcium_data` column; `time_in_seconds`
  gives the real sampling grid. **Real data only.** If the parquet is
  unreadable we report BLOCKED and stop.

## Inclusion gate (fixed before computing)

A (study, worm) unit is **included** if, after restricting to labeled neurons
(`is_labeled_neuron == True`, the basis for v1's functional-class
stratification) and to traces of length ≥ 100 timepoints with non-zero
variance:

- it has ≥ 4 classified neurons total (matches v1's `load_worm_X` minimum), AND
- at least one functional class (sensory / interneuron / motor / command) has
  ≥ 2 neurons in it (a within-class ρ needs a pair).

Functional classification uses the **same** prefix map as v15a/v15b
(`classify_neuron`: SENSORY / COMMAND_INT / MOTOR / INTERNEURON sets). Units
failing the gate are recorded with `included: false` and excluded from verdict
statistics.

## The robust estimator (canonical — `data_fmri/fmri_corridor.py::subject_rho`)

For a given neuron set (a functional class within one worm), with the
time × neuron matrix `Z` (z-scored per column):

1. `C = (Z.T @ Z) / T` — the correlation matrix.
2. `rho_raw` = mean |off-diagonal| of `C`.
3. **Debiased ρ.** Draw `N_SURROGATE = 20` phase-randomized surrogates of `Z`
   (phase randomization preserves each trace's power spectrum / autocorrelation,
   destroys cross-trace correlation — `phase_randomize` from the canonical
   estimator). `floor` = mean `rho_raw` of the surrogates.
   `rho_deb = sqrt(max(rho_raw^2 - floor^2, 0))`.
   - Surrogate count is raised from the fMRI default 5 to 20 because C. elegans
     calcium traces are strongly autocorrelated (slow GCaMP kinetics, ~0.3 s
     sampling) — the surrogate floor is large and needs a stable mean. This is
     the only deviation from the fMRI defaults; it strictly tightens the floor
     estimate, it does not change the estimator.
4. **Canonical k_eff.** Participation ratio of the covariance eigenvalues:
   `k_eff_emp = (Σλ)^2 / Σλ^2` over the positive eigenvalues of `C`. Reported
   per worm at the whole-brain (all-labeled-neuron) level and per class.
   `k_eff_kish = k / (1 + rho_deb·(k−1))` reported alongside as the
   identity-implied value.

Stratification mirrors v1: per worm, debiased ρ is computed (a) at the
**whole-brain** level over all labeled neurons, and (b) **per functional class**
(sensory / interneuron / motor / command) over the neurons in that class.

## Substrate-local PASS / FAIL thresholds (fixed before computing)

The wave pre-registration's S1 in-corridor criterion: PASS = healthy whole-brain
calcium occupies a bounded `rho_deb` band off both poles; FAIL = pins at a pole
under debiasing. Operationalized substrate-locally:

- **C1 — off the chaos pole.** The across-worm 5th-percentile of whole-brain
  `rho_deb` is > 0.05. (Debiasing subtracts a noise floor; if genuine
  correlation survives at the 5th percentile, the substrate is not at chaos.)
- **C2 — off the rigidity pole.** The across-worm 95th-percentile of whole-brain
  `rho_deb` is < 0.90, AND across-worm median `k_eff_emp` > 1.5 (a rigidity-pole
  population collapses to k_eff ≈ 1).
- **C3 — bounded band.** The across-worm whole-brain `rho_deb` distribution is a
  bounded band: IQR ≤ 0.30 and the band does not touch either pole
  (max < 0.95, min off zero is already C1).
- **C4 — per-class structure survives debiasing.** In ≥ 60% of included worms,
  at least one functional class retains `rho_deb` > 0.05 after debiasing (the
  v1 finding was a per-class banded structure; if debiasing zeroes every class
  the per-class claim is gone even if whole-brain survives).

**Verdict:**

- **PASS** — C1 and C2 and C3 hold (off both poles, bounded band). v1's
  in-corridor finding reproduces under the robust framing. C4 reported as the
  per-class-structure rider.
- **FAIL** — C1 fails (debiased ρ collapses to ≈ 0 across worms → the v1 band
  was surrogate-floor artifact) OR C2 fails (pins at rigidity).
- **BLOCKED** — calcium time-series data not readable on disk.

Whole-wave falsifier (from the wave pre-registration): if healthy whole-brain
calcium pins at a pole under debiased ρ, v1's C. elegans in-corridor finding is
retracted/amended for v2.

## Reporting

- `results_celegans.json` — written incrementally, one record per (study, worm)
  flushed as computed: raw ρ, floor, debiased ρ, k_eff_emp, k_eff_kish, at
  whole-brain and per-class level; inclusion flag.
- `RESULTS.md` — verdict PASS / FAIL / BLOCKED stated flat; debiased-vs-raw ρ
  compared explicitly per class and whole-brain; per-study breakdown so the
  "10/11 studies" v1 claim can be checked.

## Discipline

Real data only — no synthetic data. Incremental output: every (study, worm)
record is written and flushed before the next is computed, so a crash leaves
recoverable partial work.
