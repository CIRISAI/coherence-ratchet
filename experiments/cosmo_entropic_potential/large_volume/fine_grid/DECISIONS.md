# fine_grid — DECISIONS (pre-committed, written before any S/w computation)

Date: 2026-07-10
Parent: `../` (TNG300-1 205 Mpc/h large-volume frozen B-total pipeline)

## Purpose

Sharpen the large-volume dark-energy result by running the **same frozen
B-total pipeline** on a **denser snapshot grid**. This is a data-quantity
increase (more sampling of the S(a) curve), **NOT a spec change**. Nothing in
the estimator, the threshold, the cosmology, or the analysis machinery moves.

The 10-snapshot run found: corner threshold 7.425e11 Msun/h, interior S(a) peak
z = 0.590 +- 0.025 (octant jackknife), w_today = -0.833 +- 0.057, CPL-projected
(w0,wa) = (-0.767, -0.742) at 1.36 sigma from DESI. The peak region z ~ 0.3-1.0
was sampled by only ~4 points. More snapshots through the identical pipeline
give a sharper dlnS/dlna and a sharper crossing epoch.

## Frozen (do NOT touch)

1. **Threshold stays 7.425e11 Msun/h** (exactly 742530285568.0, the corner
   threshold selected from the 10-snapshot grid, CAP=38000). It is **NOT
   reselected** on the dense grid. Reselecting would let the denser grid move
   the threshold and is forbidden — the threshold is frozen from the original
   selection.
2. Estimator: GPU Cholesky log-det S_gpu, identical to `../run_test.py`
   (`S_gpu`, `_cholesky_inplace`, `make_xi_table` copied verbatim, run_test.py
   NOT imported).
3. TNG cosmology patched into `s_of_a`: OM=0.3089, OL=0.6911, OB=0.0486,
   H0H=0.6774, NS=0.9667, SIGMA8=0.8159; BOX=205.0. Power spectrum
   eh98 / tophat.
4. CPL-projection machinery lifted verbatim from `../epoch_check/cpl_projection.py`
   (source split at "# 4. Run.", defs only). Om_proj = 0.3155. DESI anchor
   (w0,wa) = (-0.838, -0.62), sigma (0.055, 0.20), rho = -0.7.
5. Octant jackknife: the SAME 8-octant spatial jackknife, **recomputed on the
   dense grid** (all 26 snapshots), for the interior-peak z and w_today error
   bars.

## Added snapshots (this run)

The dense grid = 10 original + 16 new snapshots, concentrated in the peak
region z in [0.2, 1.5] with two fillers in [1.5, 3].

Original 10 (frozen): 25, 30, 36, 42, 49, 56, 65, 76, 87, 99

New 16:
| snap | z      | region     |
|------|--------|------------|
| 33   | 2.002  | fill [1.5,3] |
| 39   | 1.531  | fill [1.5,3] |
| 45   | 1.206  | peak [0.2,1.5] |
| 47   | 1.114  | peak |
| 51   | 0.951  | peak |
| 53   | 0.887  | peak |
| 55   | 0.817  | peak |
| 59   | 0.700  | peak |
| 61   | 0.645  | peak |
| 63   | 0.599  | peak (near old crossing z=0.590) |
| 67   | 0.503  | peak |
| 70   | 0.440  | peak |
| 72   | 0.400  | peak |
| 74   | 0.361  | peak |
| 79   | 0.273  | peak |
| 82   | 0.226  | peak |

Combined 26-snapshot grid (by number): 25, 30, 33, 36, 39, 42, 45, 47, 49, 51,
53, 55, 56, 59, 61, 63, 65, 67, 70, 72, 74, 76, 79, 82, 87, 99. The peak region
z in [0.3, 1.0] now carries 14 points (was ~4).

## Threshold-count / memory note

At the frozen threshold, snapshot 65 (z=0.546) carried exactly k=38000 halos in
the 10-snapshot run (that snapshot defined the corner threshold via its
38001-th largest mass). The count above a fixed mass threshold is a smooth,
broad function of z peaking near z~0.5, so a new snapshot adjacent to 65 could
carry marginally more than 38000. The frozen pipeline uses the **threshold**,
not a per-snapshot cap, so all halos above 7.425e11 are included at each
snapshot; k is reported as measured. GPU matrices scale k^2*8 bytes (38000 ->
11.6 GB on the 16 GB card); counts are checked after fetch and the locked GPU
run is sized accordingly.

## Order of operations

0. Write this file (done, before any S/w).
1. Fetch group-catalog fields (GroupPos, Group_M_Crit200) for the 16 new
   snapshots via `fetch_fine.py` (adapted from `../fetch_tng300.py`, fields-only
   ranged HDF5 reads, npz_compressed into `../data/`, no full-file caching,
   disk-tight). Original 10 npz are reused as-is.
2. Frozen S(a) at threshold 7.425e11 on the full 26-snapshot grid (GPU,
   one flock-locked invocation, incremental flush to `results.json`).
3. 8-octant jackknife on the dense grid.
4. Analysis: interior peak z +- jk, w_today +- jk, CPL projections
   (dist BAO+CMB and rho-weighted), Mahalanobis to DESI. Compared directly
   against the 10-snapshot values.

Incremental flush to `fine_grid/results.json`; verdict-first `fine_grid/SUMMARY.md`.
Do NOT commit. API key never written into any repo file or output.
