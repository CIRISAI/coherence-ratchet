# full_population — the aperture law's pre-registered decider

**Pre-committed 2026-07-10, BEFORE any full-population S is computed.** Confirmation-mode at
the claim boundary. The cap-step audit (`../retention_v2/CHALLENGES.md`) left one decider: does
the frozen DE pipeline, read on the COMPLETE halo book with NO cap, meet or beat the cap=38000
headline (1.36σ)? Aperture law → complete-book fit ≥ 1.36σ; if the full read degrades, the
artifact reading reasserts. This file fixes the whole design before results are seen.

## 1. Population (no cap anywhere)

- **Primary:** all halos in the fetched TNG300 catalogs, m200 > 1e11 Msun/h
  (`../large_volume/data/tng300_groups_*.npz`; n = 122k–233k per snapshot).
- **Robustness:** m200 > 2e11 Msun/h (n = 54k–127k).
- **Grid:** the large_volume **10-snapshot** grid (snaps 25/30/36/42/49/56/65/76/87/99;
  z = 3.008 → 0), the grid the 1.36σ headline lives on.
- **No cap. No subsampling** of the population. (Memory contingency, §7 — not expected to fire.)

## 2. Estimator — two-level nested (NestedKish) decomposition

Partition the periodic box (205 Mpc/h) into T³ equal cubic tiles. Tile assignment:
`tile = floor(pos / (205/T))` per axis, clipped to [0,T−1]. All ops use the frozen `op_B`
machinery — model-ξ (eh98/tophat, sigma8=0.8159), normalized correlation with unit diagonal,
GPU blocked-Cholesky log-det — copied verbatim from `../large_volume/run_test.py` (as in
`../retention_v2/challenge_compute.py`). No new estimator choices at either level.

- **Intra (framework-native, extensive):**
  `S_intra(a) = Σ_tiles [ −ln det C(halos in tile) ]`. Per-axis minimum-image over the full
  box (exact for tile_size ≤ box/2 = 102.5, satisfied at all three T since per-axis halo
  separation within a tile ≤ tile_size ≤ box/2). Tiles with <3 halos contribute 0.
- **Inter (the correction):** each non-empty tile → one representative = **the mean position
  (centroid) of its halos at snapshot a** (evolves with a). `S_inter(a) = −ln det C(tile
  representatives)`, same op_B, same ξ evaluated between representatives, unit diagonal.
- **Primary estimator:** `S_total(a) = S_intra(a) + S_inter(a)`.
- **Robustness (pure block-extensive, framework-native normalization):** `S_extensive(a) =
  S_intra(a)` alone. (The stance normalizes ρ_DE extensive per comoving volume, so the
  extensive term is native and the inter term is the correction.)

## 3. Tile ladder

T = 2 (102.5 Mpc/h), 4 (51.25), 8 (25.6). All ≫ R_smooth = 1 Mpc. Report S(a) and the full
downstream fit at each, for both estimator variants.

## 4. Continuity gate (MUST pass before any full-population claim)

At the corner threshold (m200 > 7.4253e11; the EXACT det answer exists —
`../retention_v2/challenge_results.json` `corner_capstep.rule_reselect["38000"]`:
(w0,wa) = (−0.7666, −0.7424), maha = 1.363, z_peak = 0.546), compute the tiled S(a) at all
three T on the SAME corner population and run it through the identical downstream chain.

- **Yardstick:** the large_volume octant jackknife scatter — w_today err68 = 0.057,
  crossing_z err68 = 0.025.
- **GATE (primary, pre-stated): a tile size PASSES iff `maha_to_exact ≤ 1.0` AND
  `z_peak ∈ [0.35, 0.85]`**, where `maha_to_exact = sqrt(Δ^T Σ_DESI^{-1} Δ)`,
  Δ = (w0_tiled − w0_exact, wa_tiled − wa_exact), Σ_DESI the same cov used everywhere
  (diag 0.055, 0.20; ρ = −0.7). Rationale: DESI σ_w0 = 0.055 ≈ jackknife w_today σ = 0.057, so
  1σ in the DESI metric ≈ the jackknife spread — "lands within the exact run's jackknife spread."
- **Secondary reporting (not gating):** |Δw_today| vs 0.057, |Δcrossing_z| vs 0.025.
- **Best passing tile = min maha_to_exact.** The gate is applied to the PRIMARY estimator
  (S_total); the extensive variant is reported alongside.
- **If NO tile size passes at either estimator variant → STOP.** Report estimator-failure; NO
  full-population verdict; do not proceed to interpretation.

## 5. Downstream (frozen, unchanged)

op_B → S(a) → sign law `1+w = −⅓ dlnS/dlna` → CPL projection (`../epoch_check/cpl_projection.py`
`project_distance`, Om_proj=0.3155, use_cmb) → DESI DR2 Mahalanobis (center (−0.838,−0.62), cov
diag (0.055,0.20), ρ=−0.7) + real DR2 likelihood chi2 (`../desi_likelihood_v2`). z_peak =
global-max epoch. No new choices.

## 6. Decision rule (fixed now; verdict on the best gate-passing tile, PRIMARY estimator, m200>1e11)

- **PASS / APERTURE-CONFIRMED:** `maha ≤ 1.36` AND z_peak interior (0.35–0.85).
- **FAIL / ARTIFACT-REASSERTS:** `maha ≥ 1.86` (0.5 worse than baseline) OR z_peak leaves
  interior.
- **AMBIGUOUS:** maha ∈ (1.36, 1.86) with interior peak — reported as unresolved-with-direction,
  no spin.
- Report the verdict word first. Also report the extensive-variant verdict and the ≥2e11
  robustness verdict for context (the headline verdict is primary/≥1e11/best-tile).

## 7. Mechanics

- Incremental flush per snapshot to `results.json`. GPU via `flock /tmp/claude-1000/gpu.lockfile`.
- No synthetic data. **No subsampling** (densest 2³ tile at ≥1e11 is ~32k < the proven 38k
  Cholesky limit, verified before writing this). **Contingency only:** if any single tile
  exceeds 38000 halos, subsample THAT tile to 38000 without replacement, seed =
  20260710 + 1000000·T + 1000·tile_index + snap, and FLAG it in results. Not expected to fire.
- Seeds are needed only under the §7 contingency; otherwise the computation is deterministic.
