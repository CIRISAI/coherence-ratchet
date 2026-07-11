# retention_v2 — is the dark-energy unit mass scale fixed by information-retention physics?

**Pre-registered 2026-07-10, BEFORE computing.** NEUTRAL DISCOVERY MODE: a null (fit
quality flat in mass, or extremum far from the SHM peak) and a hit (extremum at the SHM
peak) are equally reportable. Run it to find the truth.

## The question

The coherence-ratchet dark-energy pipeline maps rho_DE(a) ∝ S(a), the frozen B-total
log-det of the halo two-point covariance. S(a) is computed on a **unit set** of halos —
all halos above a mass threshold. That threshold is currently an **underived input**
(the "corner" 7.4e11 Msun/h chosen by a counting rule). This experiment asks whether the
unit mass scale is instead **fixed by independently-measured retention physics**: the
stellar-to-halo-mass (SHM) efficiency peak, the halo mass at which baryons are maximally
converted to stars, i.e. where a halo maximally "stores history."

If DESI-fit quality of the frozen S(a) curve **extremizes at the SHM peak**, the unit
scale is derived from retention physics. If fit quality is flat in mass, or extremizes
far from the SHM peak, the unit scale is not retention-anchored and stays an input.

## Why this re-runs shm_anchor/ (what broke before)

The prior attempt used narrow **mass BINS** (center ± 0.2 dex). Two failures:
1. Narrow bins are **not a monotone unit set**: halos grow out of the bin between
   snapshots, breaking the "same book accumulating history" premise the mapping needs.
2. The lowest bins **saturated the cap** (38000) at every snapshot → a degenerate
   fixed-k series, and the analysis only ever populated one bin cleanly.

## The fix (this run)

Use the pipeline's **native object: CUMULATIVE THRESHOLDS** — all halos ABOVE a
threshold, a monotone unit set (a halo above threshold stays above it as it grows).
Scan the threshold across the mass axis; do NOT bin. For each threshold compute the
frozen B-total S(a) and its DESI-fit quality, and ask whether fit quality extremizes
near the SHM efficiency peak.

## Pre-committed spec

- **Thresholds:** `np.logspace(11.0, 13.0, 10)` Msun/h =
  {11.00, 11.22, 11.44, 11.67, 11.89, 12.11, 12.33, 12.56, 12.78, 13.00} (log10 Msun/h).
- **Data:** TNG300-1 (box 205 Mpc/h, TNG cosmology Om=0.3089), the **26-snapshot dense
  grid** in `../large_volume/data/tng300_groups_*.npz`.
- **Cap:** 38000. Above cap, subsample WITHOUT replacement using a fixed seed
  `seed = 20260710 + 1000*threshold_index + snap`. A threshold is flagged **cap-limited**
  (effectively fixed-k) at any snapshot where n_above > 38000; a threshold capped at ALL
  26 snaps is flagged **fully-capped** (fully fixed-k → the k-channel of the signal is
  frozen; the shm_anchor degeneracy). Predicted from `../large_volume` k-tables: 11.00
  and 11.22 fully-capped; 11.44, 11.67 partially; 11.89 borderline; ≥12.11 clean.
- **S(a):** frozen B-total via the GPU Cholesky log-det (`S_gpu`/`_cholesky_inplace`/
  `make_xi_table` copied verbatim from `../large_volume/run_test.py`, NOT imported), TNG
  power spectrum (eh98, tophat, sigma8=0.8159). PD failure → retry with jitter=1e-8.
- **Peak epoch:** GLOBAL-max epoch z_peak = 1/a_peak − 1 at argmax S(a). NOT the
  last-sign-change spline finder (shown wiggle-fragile in `../large_volume/fine_grid`).
- **CPL projection:** exec-lift `../epoch_check/cpl_projection.py` (`make_f_fw`,
  `project_distance`, `crossing_z`), Om_proj=0.3155 → (w0,wa) → **Mahalanobis** to DESI
  DR2 (−0.838,−0.62), cov diag (0.055,0.20), rho=−0.7 (same `maha` as run_test.py).
- **Real likelihood chi2:** reuse `../desi_likelihood_v2/likelihood_fit.py`
  `profile_fixedshape(make_f_fw(a,S), use_cmb=True)`; LCDM baseline chi2 from
  `profile_fixedshape(f_lcdm)` (≈10.32). Report chi2 and chi2−LCDM per threshold.

## SHM peak reference (FETCHED-NOT-REDERIVED; `../shm_anchor/shm_models.py`)

Moster+2013 (arXiv:1205.5807) & Behroozi+2013 (arXiv:1207.6105) fitted forms. Peak halo
mass where m*/M_halo is maximal, in Msun/h at h=0.6774:

| z | Moster peak (log10 Msun/h) | Behroozi peak (log10 Msun/h) |
|---|---|---|
| 0.0 | 11.60 | 11.80 |
| 0.5 | 11.92 | 11.86 |

**Reference SHM peak = 10^11.8 Msun/h** (task-specified; the S(a) crossing epoch sits at
z≈0.5, where both models give ~11.86–11.92, so the effective target band is **11.80–11.92**).

## The two outcomes (both fully reportable)

- **HIT (retention-anchored):** the best-fit threshold — the extremum of fit quality
  (min Mahalanobis and/or min chi2) as a function of threshold mass — lies **within ~0.3
  dex of 10^11.8 Msun/h** (i.e. in ~11.5–12.1). Then the unit scale is derived from
  independently-measured retention physics.
- **KILL / NULL:** fit quality is **flat in mass** (no clear extremum), OR the extremum
  lies **>0.5 dex from 10^11.8** (e.g. best fit at 10^13 or 10^11). Then the unit scale
  is not retention-anchored and stays an underived input.

Verdict stated plainly as **aligned / null / anti-aligned**, with the extremum location
vs the SHM peak reported explicitly and cap-limited thresholds flagged.

## Honest caveats (pre-stated)

- Cap-limited thresholds are fixed-k; their fit quality is not a clean function of the
  unit set. Flagged, not excluded.
- The S(a)→w(a) map is a 2-point proxy (log-det of the covariance), not full dynamics.
- Single box (TNG300-1); no cosmic-variance ensemble here (octant jackknife not repeated
  per threshold — this is a scan, not a per-point error budget).
- The SHM peak evolves with z (~0.3 dex from z=0 to z=2); we quote the z≈0–0.5 band.
- Very high thresholds (≥12.8) have small k at high z (few halos) → noisy S(a) there;
  the global-max peak may sit at the low-z end by default.
