# Large-volume test (P1/P3/K3/K7) — pipeline decisions, fixed BEFORE computing S or w

**Date 2026-07-10. Status: decisions record, written before any S(a) or w value from the
large box existed.** Data: TNG300-1 (205 Mpc/h, Planck2015: Ωm=0.3089, ΩΛ=0.6911, Ωb=0.0486,
h=0.6774; API access granted by operator today). Frozen spec being executed:
`../PREREGISTRATION.md` (`a5beb57`). This file exists because the frozen spec's own terms
require any big-box pipeline choice to be stated before the resulting w is seen.

## Snapshot grid (fixed)

TNG300-1 snapshots [25, 30, 36, 42, 49, 56, 65, 76, 87, 99] — z = 3.008, 2.316, 1.744,
1.358, 1.036, 0.791, 0.546, 0.329, 0.153, 0.000 — the closest available match to the frozen
CAMELS lever arm (a = 0.25 → 1.0, 10 points).

## Where the frozen spec collides with the big box, and the resolutions (all fixed now)

1. **Resolved-corner rule vs computability.** The frozen rule ("lowest threshold with ≥200
   halos at z=3"; the RULE is frozen, not the number 1e11) was written for a box where
   resolution binds. On TNG300-1 (m_DM = 3.98e7 M⊙/h) the literal rule selects ~8e9 M⊙/h with
   k ~ 10⁷ — `−ln det C` is not computable there by any means available.
   **Resolution: the binding constraint is documented as computability, and the rule is
   applied as: the lowest threshold such that (a) ≥200 halos at z=3 [the frozen rule] and
   (b) k(a) ≤ cap at every snapshot [feasibility].** The threshold is selected from the k(a)
   count tables ALONE, before any S(a) is computed at any threshold.
2. **Cap.** Frozen `cap=1000` was a numerical guard, spec-documented as *inert by design*
   ("the count never reaches the cap") at the analysis threshold. Keeping it at 1000 on the
   big box would make it bite everywhere, silently converting B-total into a fixed-k variant —
   the opposite of the frozen intent. **Resolution: cap = 38,000**, preserving the invariant
   *the cap never bites at the analysis threshold*. `n_draw` paths therefore never trigger at
   the analysis threshold. *(Correction, same day, before any S at the corner threshold was
   seen: the GPU is a 16GB laptop 4090, not 24GB; cap=38,000 stands, made feasible by an
   in-place blocked Cholesky — peak ~13GB — rather than by headroom.)*
3. **Estimator numerics.** Frozen estimator is exact: S = −Σ ln λ(C). At k ~ 4×10⁴ a full
   `eigvalsh` is infeasible; **Cholesky log-det computes the SAME number** (C is PSD by
   construction — ξ_R is the FT of a non-negative P(k)). **Resolution: GPU (fp64) Cholesky
   log-det; guards (min-eig / cond) replaced by Cholesky success + extremal eigenvalues via
   power iteration. VALIDATION GATE: the GPU path must reproduce a CAMELS-size CPU `op_B`
   S value to |ΔS/S| < 1e-6 before any TNG300 number is accepted.** ξ_R evaluated on GPU by
   dense-grid interpolation of the same `xi_spline` (validated in the same gate).
4. **Cosmology.** `PowerSpectrum` monkeypatched to TNG300 Planck2015 (σ8 = 0.8159,
   ns = 0.9667); BOX = 205 Mpc/h; positions ckpc/h → cMpc/h. R_smooth = 1.0 (frozen),
   estimator, spline slope (`dln_dlna`), and sign law all unchanged.

## What will be computed and reported, regardless of outcome

- **Primary (the P1/P3 object): frozen B-total S(a) at the corner threshold** selected by
  rule (1b). Interior-peak verdict (K3), crossing epoch + 68% via the six-fold subvolume
  jackknife below (P1), `w_today` (P3/K7), CPL projections through the identical
  `cpl_projection.py` machinery.
- **Threshold ladder: 5e12, 1e13 M⊙/h** — the dominant-dial sensitivity on the big box.
  Reported alongside, never swapped in as headline.
- **CAMELS-continuity variant: threshold 1e11 on 512 disjoint (25.6 Mpc/h)³ tiles,
  block-extensive sum** (the pooling device of `sweep/quijote.py`, 512 tiles instead of 6
  boxes). Tests whether the published pooled curve was 25-Mpc/h-box-biased at matched
  threshold and shrinks its cosmic variance ~9×. This variant contains no super-tile modes
  by construction and cannot answer P1's large-mode question; labeled accordingly.
- **Mechanism check (ADDENDUM §mechanism):** the S-peak epoch vs the epoch where
  above-threshold k(a) peaks (if it peaks). If k(a) is monotone rising at the corner
  threshold and S has no interior peak, **K3 fires and is logged as fired** — this is
  stated now, in advance.
- **Uncertainty:** 68% intervals from an octant jackknife (8 disjoint (102.5)³ half-box
  octants... corrected: 8 octants of 102.5 Mpc/h each) on the primary threshold: recompute
  S(a) dropping one octant at a time (delete-1 jackknife on the extensive sum is not exact
  for cross-octant pairs; the jackknife is on the FULL C restricted to surviving halos, so
  cross-terms are retained). This is the closest big-box analog of the 6-box scatter.

## Registered expectations (from the frozen spec, restated before the numbers)

- P1: interior S peak exists; crossing epoch = above-threshold formation-peak epoch.
  Current registered value to be replaced: z ≈ 1.05 (pooled small-volume).
- P3: `w_today ∈ [−1.22, −0.84]`; expectation band −0.85 ± 0.05. Outside the interval in a
  resolved cell → K7 fires.
- K3: no interior peak → the extensive branch (the DESI-shape claim) is dead entirely.
- Threshold-dependence caveat, stated in advance: the corner threshold on this box lands
  ~1.5–3e12 M⊙/h (set by counts, not yet computed at time of writing) — massive halos form
  late and their k(a) likely rises monotonically to z=0, which is exactly the configuration
  in which K3 CAN fire. The test has real teeth; that is the point of running it.

## Order of operations (enforced)

1. Fetch halo fields (M200c, positions; M200c > 1e11) — no S computed.
2. Build k(a) tables → select corner threshold by rule (1b) — no S computed.
3. GPU-estimator validation gate on CAMELS-size data.
4. Compute S(a) at the selected + ladder + tile thresholds; then w, peaks, projections.
5. SUMMARY.md with P1/P3/K3/K7 verdicts against this file, unedited.
