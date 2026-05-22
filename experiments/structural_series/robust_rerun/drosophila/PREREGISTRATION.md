# Robust re-run — Drosophila central-complex neural in-corridor substrate

**Date:** 2026-05-21. Written and committed BEFORE the recomputation.
**Parent wave:** `experiments/structural_series/robust_rerun/PREREGISTRATION.md`
(Substrate S1 neural in-corridor). **Paper target:** `papers/Corridor
Dynamics.tex` §sec:corridor-empirical, Substrate 1 (neural), in-corridor anchor.

## What v1 claimed

v1's Drosophila line (Figure 1 / §"Substrate 1: neural"): the Drosophila
central complex (CX) dual-color simultaneous imaging shows **both rungs
corridor-occupying with bounded within-rung correlation under matched-activity
controls**. Cited datasets: Ishida 2025 same-fly EPG+FC3, Dan et al EPG-only,
Mussells Pires 2024 EPG vs FC2. The substrate-local band reported in the
Figure-1 table is 0.25--0.75. v1's within-rung |rho| was a raw mean-absolute
off-diagonal Pearson with matched-activity / matched-bump-concentration nulls
but **no phase-randomized debiasing and no canonical participation-ratio
k_eff**. This re-run applies the structural-series robust framing.

## Datasets located on disk (real data, no synthetic)

Two independent CX datasets, both already downloaded by v1 sub-agents:

1. **Mussells Pires 2024** (v18) — Zenodo `processed_data.zip`, paired HDF5.
   `.../agent-acdef895a126f5e14/experiments/v18_biology/data/shared_data/EPG_FC2_imaging/`
   - EPG rung (genotype `60D05`): 16 recordings, 9 flies. ROIs
     `pb_c1_roi_2..17_F` — 16 protocerebral-bridge glomerulus ROIs, raw F.
   - FC2 rung (genotype `VT065306-AD-VT029306-DBD`): 27 recordings, 15 flies.
     ROIs `fb_c1_roi_1..16_F` — 16 fan-shaped-body column ROIs, raw F.
   - Between-fly design: EPG and FC2 imaged in different flies.
2. **Ishida et al 2025** (v19) — Zenodo record 17555687, folder 6
   (`6-FC3-EPG_12E04-LexALexAop-GC7f_60D05-Gal4UAS-RGECO1a`), CSV.
   `.../agent-a4753b36bf926c6d6/experiments/v19_biology/data/ishida_folder6/`
   - 7 same-fly dual-color recordings (dates 2023_03_06/21/22).
   - `*_im.csv`: 96 columns. EPG rung = `ROI_01..16_eb_c1` (ellipsoid-body,
     16 ROIs, GC7f channel). FC3 rung = `ROI_01..16_fb2_c1` and
     `ROI_01..16_fb5_c1` (fan-shaped-body layers 2 and 5, RGECO1a channel).
   - `*_beh.csv`: behavior at imaging timebase, incl. `im_walking`.
   - This is the same-fly two-rung dataset; the strongest single anchor.

Channel `c1` is used as the analysis channel for every genotype/layer (the raw
fluorescence channel); `c2` is the structural/reference channel and is not
analyzed, matching v1's `02b_fc2_vs_epg_h5.py` convention.

## Robust estimator (fixed — canonical, from `data_fmri/fmri_corridor.py`)

Per recording, per rung, the ROI time-series matrix `X` is `[T timepoints x N
ROIs]`. Raw fluorescence is converted to dF/F per ROI (`F0` = 5th percentile of
F over the recording; `dFF = (F - F0)/F0`) — identical to v1's
`raw_F_to_dFF`. Then, on the z-scored dF/F matrix:

- `rho_raw` = mean |off-diagonal| of the ROI x ROI correlation matrix.
- **Debiased rho:** `rho_deb = sqrt(max(rho_raw^2 - floor^2, 0))`, where
  `floor` = mean `rho_raw` over `N_SURROGATE = 20` phase-randomized surrogate
  matrices. Phase randomization (`np.fft.rfft`, randomize non-DC/non-Nyquist
  phases independently per ROI column) preserves each ROI's power spectrum and
  autocorrelation, destroys cross-ROI correlation. This is the floor a
  finite-T, autocorrelated multi-ROI matrix produces by chance.
- **Canonical k_eff:** participation ratio of the dF/F covariance eigenvalues,
  `k_eff_emp = (sum ev)^2 / sum(ev^2)` — NOT the mean-pairwise Kish proxy.
  `k_eff_kish = N / (1 + rho_deb (N-1))` reported alongside for comparison.

Computed for the unconditioned recording AND for the walking-only subset
(v18: derived fixation mask from `02b`; v19: `im_walking` column) — the
"matched-activity" analogue, so the re-run answers the same conditioned
question v1 answered. Recordings with < 100 usable imaging samples or < 3
usable ROIs after dropping zero-variance columns are excluded.

## Substrate-local corridor calibration

The GPU-anchored (0.10, 0.43) band is NOT assumed to transfer. v1's own
Figure-1 substrate-local neural band was 0.25--0.75 (raw, C. elegans-driven).
This re-run reports the debiased band the CX data actually produces and asks
the structural question — off both poles — rather than band-coincidence.

## Pre-registered PASS / FAIL (fixed before computation)

The structural claim is: both CX rungs occupy the corridor — bounded
within-rung correlation, off rigidity and off chaos.

- **PASS** if, under debiased rho, EVERY CX rung tested (v18 EPG, v18 FC2,
  v19 EPG, v19 FC3) has its per-recording-median `rho_deb` in a bounded band
  strictly off both poles, operationalized as:
  - **off chaos:** rung-median `rho_deb >= 0.05` (debiased correlation does
    not collapse to the surrogate floor), AND
  - **off rigidity:** rung-median `rho_deb <= 0.80` and 95th-percentile across
    recordings `< 0.90` (does not pin near 1).
- **FAIL** if any CX rung pins at a pole under debiasing: rung-median
  `rho_deb < 0.05` (chaos pin — genuine correlation was an artifact of the
  noise floor) OR rung-median `rho_deb > 0.80` (rigidity pin).
- **BLOCKED** if the imaging time-series cannot be loaded from disk.

A rung that is off-pole but lands outside v1's stated 0.25--0.75 band is still
a PASS for the structural claim; the band shift is reported as a calibration
correction, named honestly, exactly as the cancer substrate did.

## Whole-wave falsifier (inherited)

If a CX rung's healthy operation pins at a pole under debiased rho, v1's
Drosophila in-corridor finding is amended/retracted for paper v2.

## Discipline

Real data only. Incremental output: per-recording results flushed to
`results.json` as computed. If data cannot be located, report BLOCKED with the
exact paths searched — no fabrication.
