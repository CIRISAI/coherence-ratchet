# Robust re-run of v1's five-substrate corridor record — pre-registration

**Date:** 2026-05-21. **Purpose:** paper v2 (`papers/Corridor Dynamics.tex`,
§sec:corridor-empirical). v1 validated the corridor at five substrates, measured
2026-05-15..19 — before the 2026-05-21 structural series. v2 re-runs the
original five under the structural series' more robust framing so the flagship
paired-validation matrix (Figure 2) sits on uniform footing rather than mixing
pre- and post-structural-series methods. v1's record is **re-run, not
downgraded** — the structural series separately added fMRI + Allen and extended
cancer 5→12.

## The robust framing

Canonical estimator — `experiments/structural_series/data_fmri/fmri_corridor.py`,
function `subject_rho`:

- ρ = mean |off-diagonal| of the z-scored correlation matrix (`rho_raw`).
- **Debiased:** `rho_deb = sqrt(max(rho_raw² − floor², 0))`, where `floor` is the
  mean ρ of phase-randomized surrogates (phase randomization preserves each
  series' power spectrum, destroys cross-series correlation).
- **Canonical k_eff:** participation ratio of the covariance eigenvalues
  (`k_eff_emp`), not the mean-pairwise proxy — the Allen lesson.
- **Substrate-local corridor calibration:** the nominal GPU-anchored (0.10,
  0.43) band is not assumed to transfer; calibrate per substrate.
- Pre-register thresholds before recomputation.

## Substrates and verdicts

- **S1 neural in-corridor — C. elegans whole-brain calcium; Drosophila CX.**
  PASS: healthy operation occupies a bounded `rho_deb` band off both poles
  (neither ≈0 nor ≈1), reproducing v1's off-pole finding. FAIL: under
  debiasing, healthy `rho_deb` collapses to ≈0 (chaos) or pins ≈1 (rigidity).
- **S1 neural out-corridor — EEG (CHB-MIT seizure, I-CARE coma).** PASS:
  pathological displacement direction reproduces (rigidity-leaning) under
  debiased ρ.
- **S2 cancer, S3 LLM** — already re-run under the robust framing in the
  2026-05-21 structural series (TCGA 7 new cancers; LLM-internals). Recorded,
  not re-run here.
- **S4 OSS, S5 social** — non-ρ substrates (single-author-dominance proxy; AM
  checklist). The debiased-ρ upgrade does not apply. Robust framing here =
  pre-registration + the proxy/qualitative status stated explicitly as such.
  Re-run = recompute the proxy with pre-registered thresholds; verdict is
  whether v1's three-mode finding reproduces.

## Whole-wave falsifier

Any v1 in-corridor substrate whose healthy operation pins at a pole under
debiased ρ, or any out-corridor result that reverses direction, retracts or
amends that substrate's v1 finding for v2.

## Discipline

Real data only — no synthetic data. Incremental output: write per-unit results
as computed. If a dataset cannot be located on disk, report **BLOCKED** — do
not fabricate.
