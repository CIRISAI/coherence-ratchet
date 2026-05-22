# Robust re-run — S1 neural OUT-corridor (EEG): pre-registration

**Date:** 2026-05-21. **Wave:** `experiments/structural_series/robust_rerun/`
(see parent `PREREGISTRATION.md`). **Substrate:** S1 neural out-corridor —
scalp EEG, CHB-MIT (seizure vs interictal) and I-CARE (post-cardiac-arrest
coma). **Status: pre-registered BEFORE recomputation.**

## What v1 claimed (paper v1, §sec:corridor-empirical, "Substrate 1: neural"
out-of-corridor paragraph)

- Healthy interictal EEG (CHB-MIT, 1322 windows, 10-s windows, 1–40 Hz
  band-pass, chb01): mean raw |ρ| = 0.282.
- Generalized seizures (CHB-MIT, 39 ictal windows / 6 events, chb01): mean
  raw |ρ| = 0.316.
- Comatose post-cardiac-arrest EEG (I-CARE v2.1, 6 patients, 179 windows):
  mean raw |ρ| ≈ 0.49 (Poor, n=4) / 0.50 (Good, n=2).
- **Displacement direction: toward RIGIDITY** (seizure > interictal; coma ≫
  interictal). Strict 0.7 mean-pairwise-Pearson pole-entry threshold NOT
  reached — qualitative direction supported, quantitative pole-entry not.

## Why re-run

v1's |ρ| is the raw mean absolute pairwise correlation. Raw |ρ| carries a
finite-window noise floor: even uncorrelated channels produce a positive
mean |off-diagonal| at finite window length. The structural series'
canonical estimator (`data_fmri/fmri_corridor.py::subject_rho`) debiases
against a phase-randomized surrogate floor. The re-run asks whether v1's
out-corridor finding — pathological displacement rigidity-ward of healthy
interictal — survives debiasing, and reports how debiasing shifts the
magnitude story.

## Data — same as v1, real data only

- CHB-MIT: `data/chbmit/` in the v1 worktree
  `/home/emoore/coherence-ratchet/.claude/worktrees/agent-a5a5cfc9f224f29b0/experiments/noncorr_biology/`.
  Patient chb01, 6 EDF files with seizures (chb01_03,04,15→16,18,21,26 per
  summary), `chb01-summary.txt` for seizure intervals.
- I-CARE: `data/icare/` in the same worktree. v1 used exactly 6 patients,
  one `_EEG.mat` file each: 0342, 0364, 0411, 0474 (Poor / CPC 5);
  0549, 0571 (Good / CPC 1–2). Those 6 files are the re-run set, to keep
  the window set identical to v1. (4 further valid-outcome patients —
  0284, 0432, 0501, 0526 — are present on disk; recorded here, not used,
  so the re-run is a strict like-for-like comparison with v1.)

## Windowing — IDENTICAL to v1 (no change)

- 10-s non-overlapping windows.
- 1–40 Hz band-pass, 4th-order Butterworth, zero-phase (`sosfiltfilt`).
- CHB-MIT: bipolar montage, first 23 channels; native sfreq (256 Hz).
  Ictal windows = marked seizure intervals; interictal = windows >600 s
  from any seizure, same recording.
- I-CARE: all valid (non-zero, non-NaN) channels; first 5 min per file;
  sfreq from `.hea` (256 Hz). ≥4 valid channels required.

## The robust computation (per window) — canonical estimator

Per 10-s window, channel matrix X (n_ch × n_t), z-scored per channel:

1. `rho_raw` = mean |off-diagonal| of the correlation matrix C = XᵀX / T
   — the v1 metric, recomputed here for direct comparison.
2. **Debiased ρ.** Phase-randomize each channel (rfft, randomize non-DC /
   non-Nyquist phases independently per channel — preserves each channel's
   power spectrum, destroys cross-channel correlation). N_SURROGATE = 20
   draws; `floor` = mean |off-diagonal| over surrogate correlation
   matrices. `rho_deb = sqrt(max(rho_raw² − floor², 0))`.
3. **Canonical k_eff.** Participation ratio of the covariance eigenvalues:
   `k_eff_emp = (Σλ)² / Σλ²`. (Also report Kish k_eff
   `k/(1+rho_deb·(k−1))` for cross-reference.)

Surrogate seed fixed (SEED = 0). Phase randomization identical to
`fmri_corridor.py::phase_randomize`.

## Groups compared

- Healthy interictal (CHB-MIT chb01 interictal windows) — the baseline.
- Seizure (CHB-MIT chb01 ictal windows).
- Coma Good-outcome (I-CARE CPC 1–2).
- Coma Poor-outcome (I-CARE CPC 3–5).

Headline statistic per group: mean and median `rho_deb`; same for
`rho_raw`. Displacement = group mean `rho_deb` − interictal mean `rho_deb`.

## PASS / FAIL — pre-registered

**PASS:** under debiased ρ, the pathological displacement direction
reproduces — BOTH seizure AND coma (each outcome group) have mean
`rho_deb` strictly greater than healthy interictal mean `rho_deb`
(displaced rigidity-ward). The v1 out-corridor finding stands.

**FAIL:** the direction reverses (a pathological group falls at or below
interictal under debiasing) or vanishes (displacement within ±0.005,
i.e. indistinguishable). Either fires a v1 amendment for v2.

**Magnitude is reported, not gated.** v1 already stated the strict 0.7
pole-entry threshold is not reached on this metric; the re-run reports
where debiased ρ sits relative to that threshold and relative to v1's raw
numbers, but the PASS/FAIL verdict turns only on displacement DIRECTION,
matching the parent pre-registration ("PASS: pathological displacement
direction reproduces (rigidity-leaning) under debiased ρ").

**BLOCKED:** if the EEG data cannot be read. Report the exact paths
searched; do not fabricate.

## Output

- `results_eeg_robust.json` — written incrementally, flushed per record
  (per EDF / per I-CARE patient), per-window arrays retained.
- `RESULTS.md` — verdict PASS / FAIL / BLOCKED stated flat; debiased vs
  raw numbers compared explicitly; whether the v1 claim stands.

## Discipline

Real data only. No synthetic data. Incremental flushed output. Thresholds
above are fixed before the computation runs.
