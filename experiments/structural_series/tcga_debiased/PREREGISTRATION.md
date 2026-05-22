# Debiased TCGA re-run — pre-registration

**Date:** 2026-05-21. **Owed by:** the per-substrate band calibration
(`band_calibration/RESULTS.md`), which excluded TCGA because its on-disk ρ
(`data_tcga/02_compute_rho.py`) is raw `mean_abs_corr` with no surrogate-floor
subtraction — raw ρ, not debiased ρ.

## Why

Every other structural-series substrate has debiased ρ (raw² − floor², floored
at 0). TCGA does not. The TCGA healthy-tissue band centre quoted in
§sec:robust-rerun (0.27 / 0.34) is therefore a raw figure, not comparable with
the debiased biological cluster. This re-run debiases it.

## The surrogate — stated explicitly

TCGA Hallmark-pathway ρ is computed over **samples × pathways**, not a time
series. Phase randomization (the fMRI/EEG floor) does not apply — TCGA samples
are not temporally ordered. The correct null here is a **per-pathway permutation
surrogate**: independently permute each pathway's values across samples, which
destroys cross-pathway correlation while exactly preserving each pathway's
marginal distribution. The floor is the mean ρ over such surrogates;
`rho_deb = sqrt(max(rho_raw² − floor², 0))`. The estimator otherwise matches
`data_fmri/fmri_corridor.py` in spirit (debiased ρ + participation-ratio k_eff).

## Method

Same TCGA data on disk (`data_tcga/data/`, the twelve-cancer healthy + tumour
Hallmark-pathway record). Recompute, per cancer: healthy-tissue debiased ρ,
tumour debiased ρ, and the canonical participation-ratio k_eff. Compare against
the raw figures.

## Pre-registered verdict

- **Healthy band:** debiased TCGA healthy-tissue ρ_mid sits off both poles and
  within the biological cluster (≈0.27–0.33 from `band_calibration/`) → TCGA
  joins the debiased pool; §sec:robust-rerun's "debiased TCGA re-run is owed" is
  discharged.
- **Tumour drift:** the chaos-ward tumour drift (201/201 in the raw run)
  survives debiasing → directional result robust. If the drift sign weakens or
  reverses under debiasing, report it — that would be a real finding.

## Discipline

Real TCGA data on disk only — no synthetic data, no new GDC fetch unless the
on-disk data is incomplete. Incremental output: per-cancer results flushed as
computed. If the on-disk data cannot be read, report BLOCKED. Verdict flat.
