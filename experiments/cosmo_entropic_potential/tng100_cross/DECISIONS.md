# TNG100-1 cross-check (independent-box replication of the large-volume test) — pipeline decisions, fixed BEFORE any S or w

**Date 2026-07-10. Status: decisions record, written before any S(a) or w value from
TNG100-1 existed.** This file is the TNG100-1 mirror of `../large_volume/DECISIONS.md`. Its
purpose is one question and one question only:

> Does the **frozen RULE** (not the lucky number 7.425e11) — "lowest mass threshold whose
> above-threshold count stays computable (max_a k(a) ≤ cap) while still resolving ≥200 halos
> at z=3, selected from count tables alone" — reproduce the DESI-quadrant curve (interior
> S(a) peak, w_today ≈ −0.83, CPL point ≈1.4σ from DESI) on an **independent simulation box
> at different volume and resolution**? Or was the TNG300 result volume/resolution-fragile?

Nothing in the frozen spec (`../PREREGISTRATION.md`, `a5beb57`) or the pipeline (estimator,
sign law, CPL machinery, cap value, jackknife design) is changed. Only the box changes.

## Box and cosmology (from the TNG API root, verified today)

- **TNG100-1**, BOX = **75.0 Mpc/h** (75000 ckpc/h). Volume = (75/205)³ = **0.049×** TNG300-1
  (≈20× smaller volume).
- m_DM = **5.06×10⁶ M⊙/h** (≈7.9× **finer** mass resolution than TNG300-1's 3.98×10⁷).
- Cosmology **identical Planck2015** to TNG300-1: Ωm=0.3089, ΩΛ=0.6911, Ωb=0.0486, h=0.6774,
  ns=0.9667, σ8=0.8159. (API root: omega_0=0.3089, omega_L=0.6911, hubble=0.6774.) The
  `s_of_a` globals are patched to these values (the SAME patch line as `run_test.py`), so the
  power spectrum, estimator, spline slope (`dln_dlna`), and sign law are byte-identical to the
  TNG300 run apart from BOX.

## Snapshot grid (fixed) — identical redshift table to TNG300-1

TNG100-1 shares TNG300-1's snapshot/redshift table exactly. The 10-snapshot grid is therefore
the **same snapshot numbers** and the **same redshifts** as `../large_volume`:
**[25, 30, 36, 42, 49, 56, 65, 76, 87, 99]** → z = 3.008, 2.316, 1.744, 1.358, 1.036, 0.791,
0.546, 0.329, 0.153, 0.000. This makes the TNG100↔TNG300 comparison exact at matched epochs.

## Where the box change collides with the frozen rule, and the resolutions (all fixed now)

1. **The rule self-selects a LOWER threshold here — stated in advance.** TNG100-1 has ≈20×
   smaller volume, so at any fixed mass threshold it holds ≈20× fewer halos than TNG300-1.
   The frozen corner rule ("lowest threshold with max_a k(a) ≤ cap") therefore lands at a
   **lower mass** on TNG100-1 than TNG300-1's 7.425e11 — pre-registered expectation ≈2–4e10
   M⊙/h (rough estimate from the TNG300 count table scaled by 0.049× volume and a ~6× per-dex
   mass-function factor). The finer resolution (m_DM=5.06e6) resolves that band cleanly
   (2e10 ≈ 4000 particles). **The number is not frozen; the RULE is** — exactly the point of
   the cross-check. The threshold is read from the k(a) count tables ALONE, before any S(a).
2. **Fetch mass floor = 1e10 M⊙/h** (lower than TNG300's, because the box mass floor is lower
   and the rule reaches deeper). This is comfortably below the expected corner and captures
   the (cap+1)-th largest halo needed to define the corner threshold.
3. **Cap = 38,000** (unchanged from TNG300; the invariant "the cap never bites at the analysis
   threshold" is preserved by the corner rule, which selects the threshold at which max_a k(a)
   equals the cap). GPU in-place blocked fp64 Cholesky, peak ≈13GB on the 16GB card, unchanged.
4. **Estimator unchanged.** GPU Cholesky log-det S = −2·Σ ln diag(L), C_ij = ξ_R(r_ij)/σ²_R
   from the same `xi_spline(R_smooth=1.0)`, C_ii=1, PBC minimum-image with **box=75.0**. The
   `S_gpu` / `_cholesky_inplace` / `make_xi_table` code is copied verbatim from
   `../large_volume/run_test.py` (NOT imported). VALIDATION GATE unchanged: the GPU path must
   reproduce a CAMELS-size CPU `op_B` S to |ΔS/S| < 1e-6 before any TNG100 number is accepted.
5. **Fetch stop-heuristic fix (numerical, not a spec change).** TNG100-1 group catalogs have
   448 chunk files with a highly non-uniform group distribution: massive-end chunks are nearly
   empty (chunk 0 holds the single most-massive halo; many early chunks have 0 groups), and the
   1e10 floor is crossed around chunk ~160 at z=0. The TNG300 fetch's "stop when the last-3-chunk
   max mass < THR/MARGIN" would **false-trigger on the empty massive-end chunks** (max=0). Fix:
   the tail is tracked over **non-empty** chunks only, and the stop is armed only **after** the
   first halo above the floor has been collected. This changes only which chunks are read, not
   which halos are kept (keep = all M200c > 1e10). Documented here before any fetch.

## What will be computed and reported (identical objects to TNG300, for direct comparison)

- **Primary (P1/P3/K3 object): frozen B-total S(a) at the rule-selected corner threshold.**
  Interior-peak verdict (K3), crossing epoch + 68% via the **8-octant jackknife** (octants of
  37.5 Mpc/h), w_today (P3/K7), CPL projections through the identical `cpl_projection.py`
  machinery (Om_proj=0.3155, DESI target (−0.838,−0.62), cov (0.055,0.20), ρ=−0.7,
  Mahalanobis).
- **Threshold ladder: 7.425e11 (the TNG300 corner, for a DIRECT same-threshold comparison)
  and 5e12** — reported alongside, never swapped in as headline.
- **Mechanism check:** S-peak epoch vs the epoch where above-threshold k(a) peaks.

## Registered expectations (from the frozen spec, restated before the numbers)

- P1: interior S peak exists; crossing epoch = above-threshold formation-peak epoch.
- P3: w_today ∈ [−1.22, −0.84]; expectation band −0.85 ± 0.05.
- K3: no interior peak → the extensive branch (the DESI-shape claim) is dead entirely.
- **Cross-check verdict criterion (the actual question):** the RULE is judged **robust** if
  the TNG100-1 rule-selected curve lands in the DESI quadrant — interior peak present (K3 does
  not fire), w_today in-band, CPL point of comparable Mahalanobis to TNG300's 1.36σ — with a
  peak epoch and (w0,wa) that agree with TNG300 within the octant-jackknife error. It is judged
  **volume/resolution-fragile** if the rule-selected curve loses the interior peak, or w_today /
  peak epoch / (w0,wa) move outside the TNG300 jackknife error.
- Honest caveat stated in advance: the 75 Mpc/h box has far larger cosmic variance than TNG300
  and (with only octant jackknife) the error bars UNDER-estimate the true box-to-box scatter;
  a modest disagreement with TNG300 is not by itself fatal, but a lost interior peak (K3) or a
  sign flip would be.

## Order of operations (enforced — no S computed before the threshold is fixed from counts)

1. Fetch halo fields (M200c, positions; M200c > 1e10) — no S computed.
2. Build k(a) tables → select corner threshold by the frozen rule — record it and k(a) BEFORE
   any S(a) at any threshold.
3. GPU-estimator validation gate on CAMELS-size data.
4. Compute S(a) at the selected + ladder thresholds; then w, peaks, projections.
5. SUMMARY.md with the cross-check verdict against this file, unedited.
