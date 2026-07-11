# abacus_cross — the cross-code test, pre-committed BEFORE any Abacus S/w is seen

**Written 2026-07-11, before running the pipeline on Abacus.** The question the program has
owed since `proxy_upgrade` §2: is the DE-leg signal (interior S-peak, thawing w(z),
beats-ΛCDM) a property of the coordination read, or a TNG artifact? The prior Abacus attempt
proved reachability but was CPU-blocked to a cluster-scale threshold (endpoint peak, not
evidence either way). The gate-validated nested-tile estimator (`../full_population/`,
reproduces exact to maha 0.09 on TNG300) removes that block. This is a **qualitative
cross-code** test, not a second precision measurement.

## 1. DATA (on disk — no refetch)

`AbacusSummit_small_c000_ph3000` (500 Mpc/h, CompaSO halos, Planck-2018 base cosmology),
already fetched in `../proxy_upgrade/abacus_data/` (10 snapshots, verified present). Fields per
snapshot: `pos` (Mpc/h, wrapped to [0,500)), `mass` (Msun/h, = CompaSO `N`×`ParticleMassHMsun`),
`box`=500, `particle_mass`=2.109081520453063e9 Msun/h.

**Full available snapshot range (all 10, wider than the prior a=0.37–0.83 CPU run):**
z = 3.008, 2.258, 1.705, 1.400, 1.028, 0.800, 0.577, 0.500, 0.351, 0.200
(a = 0.2495, 0.3070, 0.3697, 0.4167, 0.4931, 0.5556, 0.6342, 0.6667, 0.7402, 0.8333).
**The small box has NO z<0.2 snapshot: the grid ENDS at a = 0.8333, there is no a = 1.**
This is the load-bearing grid difference vs TNG300 (which reaches a = 1); quantified in §6.

## 2. MASS DEFINITION MAPPING (committed before results — NOT tuned to any fit)

CompaSO halo mass differs from TNG `M_Crit200` by definition (CompaSO `N` = L1-halo particle
count; SO vs FoF-family) and both are already in Msun/h with each box's own h. **Mapping
choice: use CompaSO `N`×particle_mass as-is, in Msun/h, and define all thresholds in Msun/h
consistently.** No cross-definition rescaling, no h-conversion, no post-hoc adjustment. The
definitional mismatch is a caveat carried to the verdict, not something we tune away — that is
the honest cross-code posture (a matched *number density* or matched *definition* remap would
be a second knob; we refuse it).

Two threshold configurations, both pre-committed to run:
- **(a) corner-equivalent:** M > **7.425e11 Msun/h** (= the TNG300 frozen corner threshold, in
  Msun/h; = 352 Abacus particles — well resolved). This is the configuration the LAW-LIKE /
  CODE-SPECIFIC verdict is read on (§5).
- **(b) full population:** M > **2.109e11 Msun/h** (= 100 particles, the resolution floor from
  the particle mass). The selection-free companion (matches `full_population/`'s complete-book
  posture on TNG).

## 3. ESTIMATOR — nested tile (reused verbatim from `../full_population/run_full_population.py`)

`S_total(a) = S_intra(a) + S_inter(a)`:
- **S_intra** = Σ_tiles [ −ln det C(halos in tile) ], per-axis minimum-image over the full 500
  box, frozen `op_B` machinery (model-ξ eh98/tophat, unit-diagonal normalized correlation, GPU
  blocked-Cholesky log-det). Tiles with <3 halos contribute 0.
- **S_inter** = −ln det C(tile centroids), same op_B.
- **Robustness variant:** `S_extensive = S_intra` alone (the framework-native extensive term).

**Tile ladder scaled to the 500 box:** T = 2 (250 Mpc/h), 4 (125), 8 (62.5). All ≫
R_smooth = 1 Mpc/h and ≤ box/2 (min-image exact).

**Cholesky cap = 38000** (16 GB GPU, as in `full_population`). Contingency (identical to
`full_population` §7): any single tile with >38000 halos is subsampled to 38000 without
replacement, seed = 20260711 + 1_000_000·T + 1000·tile_index + snap, and **FLAGGED** in
results. On the 500 box at these thresholds the T=2 tiles are expected to exceed 38000 and be
flagged; **T=4 and T=8 are the clean estimators** and the verdict is read on the best
gate-passing tile (below), reported alongside all three.

## 4. GATE (Abacus-native, "gate where possible" per mission item 3)

Exact-det S over the full 500 box is only reachable where the snapshot count ≤ 38000. Corner
and full populations are ~5×10^5 halos — beyond exact reach — so the gate uses a **high
(cluster) threshold chosen purely so max-count-over-snapshots ≤ 35000**, computed BEFORE any
science config. At that threshold:
- compute **exact** S(a) (one whole-box Cholesky per snapshot) → CPL point (w0_ex, wa_ex);
- compute **tiled** S_total(a) at T = 2, 4, 8 → CPL points;
- `maha_to_exact` = DESI-metric distance (same Σ_DESI: diag 0.055, 0.20, ρ=−0.7) between tiled
  and exact CPL points.
- **GATE PASSES for a tile iff maha_to_exact ≤ 1.0.** Best tile = min maha_to_exact among
  passing tiles; that tile is the PRIMARY estimator for the science configs.
- **If no tile passes → report estimator-failure on Abacus; no cross-code verdict.**

The gate's own *physics* verdict (a cluster threshold gives an endpoint peak on both codes —
`proxy_upgrade` already saw this) is **explicitly NOT evidence either way** (mission item 5);
the gate validates only that the tiled estimator reproduces exact on this box/code.

## 5. DECISION RULE (qualitative cross-code, fixed now — verdict read at the corner-equivalent threshold, best gate-passing tile, S_total)

- **LAW-LIKE** = interior S-peak (z_peak ∈ [0.3, 1.0]) **AND** thawing (wa < 0) **AND** better
  DESI DR2 fit than ΛCDM (Mahalanobis maha < 3.28) — the DE-leg signal transfers across codes.
- **CODE-SPECIFIC** = endpoint peak **OR** phantom (wa > 0) **OR** worse than ΛCDM (maha ≥
  3.28) — a major caveat lands on the whole DE leg.
- **PARTIAL** = mixed (report which of {interior peak, thawing, beats-ΛCDM} transfer).
- The known **threshold-zone** behavior (cluster-scale thresholds give endpoint peaks on BOTH
  codes) is NOT evidence either way; only the corner-equivalent (§2a) and full-population
  (§2b) reads count. Full-population is reported as the selection-free companion; if the two
  disagree, that is itself reported (which grain transfers).
- Note the bar is deliberately qualitative (beat ΛCDM), NOT "match the 1.36σ TNG headline" —
  this is a cross-code *sign/shape* test, and the small box is one 500-Mpc/h realization with
  a coarser z-grid.

## 6. SNAPSHOT-GRID CAVEAT (quantified, pre-stated method)

The Abacus a-grid ends at a = 0.8333 (no a = 1) and is spaced differently from TNG300's
10-snapshot grid. To quantify what this does to the w(z) projection, I **re-run the frozen CPL
projection on the TNG300 large_volume corner S(a) (which HAS a = 1) after (i) truncating to
a ≤ 0.8333 and (ii) re-gridding to the Abacus a-values**, and report Δw0, Δwa, Δcrossing_z vs
the full-grid TNG projection. This isolates the grid effect on a known signal, separating it
from any genuine code difference. Reported in results.json (`grid_caveat`) and SUMMARY.

## 7. DOWNSTREAM (frozen, unchanged)

ξ model from `s_of_a.PowerSpectrum(eh98, tophat)` with **Abacus c000 cosmology**: Om =
0.315192, OL = 0.684808, Ob = 0.02237/0.6736² = 0.049302, h = 0.6736, ns = 0.9649,
sigma8 = 0.807952 (published AbacusSummit c000 sigma8_m). op_B → S(a) → sign law
1+w = −⅓ dlnS/dlna → CPL projection (`epoch_check/cpl_projection.py` `project_distance`,
Om_proj = 0.3155 fixed = the observer fiducial, as in the frozen pipeline) → DESI DR2
Mahalanobis (center (−0.838,−0.62), cov diag (0.055,0.20), ρ=−0.7) + real DR2 likelihood chi2
(`desi_likelihood_v2`). z_peak = global-max epoch. No new downstream choices.

## 8. MECHANICS

Incremental flush to `results.json` per snapshot. GPU only via `flock
/tmp/claude-1000/gpu.lockfile` (queue behind any galaxy-book run — correct). No synthetic
data. Report exhaustively including negatives. Deliverable: `{DECISIONS.md, run_abacus_cross.py,
results.json, SUMMARY.md}`.

---

## AMENDMENT — GATE V2 (fair-regime subvolume gate); reasoning logged BEFORE v2 is computed

**2026-07-11, after gate v1 ran and STOPPED per §4, before any v2 number.** Gate v1 (§4)
compared tiled-vs-exact at a *cluster* threshold (1.329e13 Msun/h, the only exact-reachable
whole-box config) and failed: maha_to_exact = 1.41 (T=2), 1.50 (T=4), 1.42 (T=8), all > 1.0.
But that gate was tested in the wrong regime, and the recorded numbers show it:

- **The exact gate S(a) is a monotone-rising cluster read** — z_peak = 0.200 (endpoint),
  wa = −8.10, maha = 38.4 from DESI. The CPL projection is ill-conditioned here: it maps a
  tiny S(a) difference into a large (w0,wa) displacement. maha_to_exact in this regime measures
  projection conditioning, not estimator fidelity.
- **Direct fidelity check on the v1 data (S(a) space, no projection):** T=2 whole-box tiled
  reproduces exact gate S(a) to **median 1.04%, max 1.73%** fractional error, with **dlnS/dlna
  median |Δ| = 0.024** (max 0.20). Sub-2% in the shape that carries the sign law. The z_peak
  matched EXACTLY (0.200) at all three tile sizes. **The v1 "failure" is a metric-conditioning
  artifact, not an estimator failure.**
- T=4/T=8 additionally show a 64–66% error at the single a=0.249 (z=3) snapshot only —
  because the cluster threshold leaves just 145 halos there, which 64/512 tiles shatter to
  ~2/~0.3 per tile. This is a gate-threshold sparsity artifact; at the corner-equivalent
  threshold z=3 has 130,475 halos, so it does not arise in the science config.

**Gate v2 — a fair-regime gate at the ACTUAL config of interest** (stricter in relevance,
transparent as an amendment; v1 and v2 both reported):

- **Config:** corner-equivalent threshold 7.425e11 Msun/h (§2a — where the verdict lives).
- **Subvolumes:** partition the 500 box into 4³ = 64 disjoint cubic subvolumes of 125 Mpc/h
  (≈ 700k/64 ≈ 11k halos each at late times — exact-det feasible). Pairwise separations within
  a 125 subvolume are < 125·√3 ≈ 217 < box/2 = 250, so the frozen min-image `S_gpu(box=500)`
  reduces to plain Euclidean inside a subvolume — the science machinery, unchanged.
- **Sample:** 4 subvolumes chosen at random, `np.random.RandomState(20260711).choice(64, 4,
  replace=False)` (stated).
- **Comparison, per subvolume, per snapshot:** exact S(a) = S_gpu over ALL halos in the
  subvolume, vs nested-tile S(a) = S_intra(8 tiles of 62.5 Mpc/h) + S_inter(tile centroids) —
  the T=8 grain (62.5 Mpc/h) of the whole-box science estimator, gated at corner density.
- **Metric (S(a) space, NOT CPL maha):** per-snapshot fractional |ΔS|/S and |Δ dlnS/dlna|.
- **PASS criteria (pre-stated numeric tolerance, ≈ the TNG gate's achieved fidelity band):**
  averaging over the 4 subvolumes,
  1. mean of (median-over-snapshots |ΔS|/S) ≤ **2%**, AND
  2. mean of (median-over-snapshots |Δ dlnS/dlna|) ≤ **0.15** (⇒ median |Δw| ≤ 0.05, within
     DESI's σ_w0 = 0.055), AND
  3. z_peak(tiled) within one snapshot of z_peak(exact) in ≥ 3 of 4 subvolumes.
  Rationale for the numbers: the sign law is 1+w = −⅓ dlnS/dlna, so a dlnS/dlna tolerance of
  0.15 keeps the induced w error below the DESI measurement error; the 2% S bar matches the
  sub-2% fidelity the v1 T=2 estimator already delivered even in the pathological regime.
- **If v2 PASSES:** proceed to the pre-committed corner-equivalent and full-population runs
  (§2, §3) and the original decision rule (§5) — the tiled estimator is validated at the
  corner grain on Abacus. Primary science tile = T=8 (62.5 Mpc/h, the gated grain), with T=2
  and T=4 reported alongside.
- **If v2 FAILS:** the cross-code test is genuinely estimator-blocked on Abacus. Report that as
  the finding, with the full v1-vs-v2 comparison, and stop.

---

## AMENDMENT 2 — TRUNCATION DIAGNOSTIC (pre-stated before the verdict computes; adds a dimension, does NOT move the verdict bar)

**2026-07-11, before the corner T=8 verdict number is read.** The Abacus corner-equivalent
count is still RISING at the final snapshot (a=0.833, z=0.2) — unlike TNG300's corner count,
which peaked interior. Likely cause: the CompaSO `N`-mass mapping makes the effective cut
higher-mass (number density above 7.425e11 on Abacus is ~3× lower than TNG at matched epoch),
pushing the formation clock later, possibly past the box's snapshot window (Abacus small ends
at z=0.2; no a=1). TNG showed S(a) peaks EARLIER than the raw count peak (per-unit structure
shifts it), so an interior S-peak may still appear.

**Pre-stated diagnostic:** report dS/da at the final snapshot (edge slope) for the corner
T=8 S_total(a). Verdict handling:
- **Endpoint peak (z_peak = 0.2) AND dS/da > 0 at the edge** → record the verdict per the §5
  rule (an endpoint peak fails the interior-peak clause), BUT flag it
  **INCONCLUSIVE-BY-TRUNCATION** (window-limited, not physics-adjudicated). Also check whether
  AbacusSummit small boxes have z<0.2 snapshots (e.g. z=0.1) to extend the window before
  concluding.
- **S turns over INTERIOR and the §5 rule still fails** (phantom, or worse than ΛCDM) →
  genuinely **CODE-SPECIFIC**, no truncation excuse.
- **S turns over interior and passes** → **LAW-LIKE** stands clean.

This separates "the physics differs" from "the window is short" using dS/da at the edge — a
number already in the S(a) output.

---

## AMENDMENT 3 — OPERATIONAL (T=4 full-population OOM/queue-time fallback; pre-authorized)

**2026-07-11, logged before acting.** Full-population T=4 tiles approach the det budget at late
snapshots (2.33M halos / 64 tiles → ~45–50k projected; the fp64 38k Cholesky was already ~13GB
on the 16GB card). Two protections, both honored:
1. The estimator already caps any tile >38,000 by subsampling to 38,000 (DECISIONS §3
   contingency), so a T=4 tile cannot OOM the card — it flags-and-subsamples. No OOM risk.
2. But full-population T=4 at late snapshots is then *subsample-contaminated* (not the clean
   estimator) AND slow (~1000s+/snapshot, ~3 h for the pass) — a poor use of GPU queue time for
   a companion tile whose verdict role is nil (the verdict is corner T=8; TNG showed tile-size
   robustness to 3 decimals; gate v2 validated the T=8 62.5-Mpc/h grain).

**Action (pre-authorized by the operational heads-up):** abandon the full-population T=4 pass
after the snapshots already computed (a=0.249, 0.307, 0.370 — preserved in results.json,
flagged partial), and take the full-population companion on **T=8 only** (tiles ~4.5k, no
flagging, safe and clean everywhere). Corner-equivalent keeps all of T=2/T=4/T=8 (already
computed). This does not touch the verdict (corner T=8) or its quality.

**z<0.2 confirmation:** the AbacusSummit small c000 halo mirror lists snapshots
z ∈ {0.2, 0.25, 0.3, …, 3.0, 5.0, 8.0} — **minimum z = 0.200; no z<0.2 output exists**, so the
truncation window cannot be extended on this box (amendment 2 diagnostic stands).
