# galaxy_book — does physical rung-membership select the DE grain?

**Pre-committed 2026-07-11, BEFORE any pipeline run.** Confirmation-mode at the claim boundary.
The grain problem (`papers/notes/the_grain_problem.md`): the 1.36σ headline is conditional on an
underived grain (~7.4e11 corner). Both escapes died — DERIVE the grain (SHM anchor: C1/C2 kills)
and DISSOLVE it (complete book / aperture law: full-population FAIL, 2.21σ). This run tests the
third route: define the unit population by **physical membership at the galactic rung** — halos
hosting a well-resolved galaxy — fixed from independent physics BEFORE any fit, then run the
frozen pipeline with zero threshold freedom. This is NOT the killed SHM-extremum claim (which
tuned a threshold to fit quality post hoc); it is a resolution-standard definition, made once.

## 1. Membership (fixed now, from independent physics — the whole point)

- **PRIMARY unit definition:** FoF group whose stellar mass **GroupMassType[:,4] ≥ 1.1e9 Msun/h**
  = 100 × m_baryon(TNG300-1) (≈1.1e7 Msun/h) — the simulation-standard ≥100-star-particle
  "well-resolved galaxy" criterion. Committed as THE definition.
- **Robustness ladder (reported, NEVER promoted):** M* ≥ 10^8.5, 10^9.5, 10^10 Msun/h.
- **Per-snapshot selection:** at each snapshot a group is a unit iff its M*(a) clears the floor
  (a group counts once its hosted galaxy is resolved at that epoch — physical, evolving membership).
- GroupMassType is read in code units (1e10 Msun/h); floor 1.1e9 Msun/h = 0.11 code units.

## 2. Grain / positions (frozen)

Unit position = group position (GroupPos/1e3, Mpc/h), exactly as the frozen pipeline uses it.
NOTHING else changes: frozen op_B (model-ξ eh98/tophat, sigma8=0.8159, unit-diagonal normalized
correlation, GPU blocked-Cholesky log-det) → S(a) → sign law 1+w=−⅓ dlnS/dlna → CPL projection
(Om_proj=0.3155, use_cmb) → DESI DR2 Mahalanobis (center (−0.838,−0.62), cov diag (0.055,0.20),
ρ=−0.7) + real DR2 likelihood chi2. z_peak = global-max epoch. No new choices.

## 3. Estimator (gate-validated in full_population/)

Nested two-level tile: S_total = Σ_tiles S_intra + S_inter(tile centroids). **T=2 primary**
(best gate score, maha_to_exact 0.087), **T=4 reported**. No cap, no subsampling. Also report the
pure-extensive variant (Σ S_intra) — it was ≡ S_total to 3 decimals in full_population.

## 4. Grid and self-consistent reference cuts

- **Grid:** the **26-snapshot dense grid** (all `../large_volume/data/tng300_groups_*.npz` snaps:
  25/30/33/36/39/42/45/47/49/51/53/55/56/59/61/63/65/67/70/72/74/76/79/82/87/99), per team-lead.
- The prior anchors (corner 1.363, ≥2e11 1.889, complete-book 2.21) were on the 10-snap grid. To
  keep the decision threshold (maha<1.89 ≡ "beat the ≥2e11 mass-cut at matched selection-freedom",
  `the_grain_problem.md` §4) valid on THIS grid, I **recompute on the same 26-snap grid + same
  tiled estimator** the halo-mass reference cuts: **≥2e11, ≥1e11 (complete book), and the corner
  ≥7.4253e11**. The galaxy-book verdict is then read BOTH ways: (a) absolute vs the pre-registered
  maha thresholds, and (b) relative — does the galaxy book beat the ≥2e11 cut on the same grid
  (the note's actual intent). If the 26-snap ≥2e11 maha departs materially from 1.889, I report the
  grid sensitivity explicitly and lead with the relative comparison.

## 5. Decision rule (from `the_grain_problem.md` §4 + team-lead task; fixed now)

Verdict on the **PRIMARY M*≥1.1e9, T=2, S_total**:

- **PASS:** `maha < 1.89` AND z_peak interior (0.35–0.85). → Physical rung-membership selects the
  grain; the grain problem resolves (the epoch's coordinating rung is galactic, as piece-6 predicts).
- **KILL:** `maha ≥ 2.0` OR z_peak exits the interior. → Rung membership does NOT select the grain;
  the grain is a second free constant of the theory alongside κ, and `dimensional_line_kB.md` §5's
  pre-staked one-marriage kill takes its hit.
- **AMBIGUOUS:** `maha ∈ [1.89, 2.0)` with interior peak → unresolved-with-direction, no spin.

Report the verdict word FIRST. Ladder + T=4 + extensive variant + relative-vs-≥2e11 reported for
context; the headline verdict is primary/M*≥1.1e9/T=2/S_total.

## 6. Descriptive output (not an input)

The effective halo-mass (M200) distribution of the member population — median and 16–84% range per
snapshot — so we can see how the stellar criterion maps onto the mass axis (expected near the
galaxy-host scale ~10^11.5–12, but that is an OUTPUT here, not a tuned input).

## 7. Fetch and mechanics

- Fetch TNG300-1 group catalogs (all 26 snaps): GroupPos, Group_M_Crit200, **GroupMassType[:,4]**
  (stellar), fsspec ranged HDF5 reads, API key from `~/.tng_api_key` (chmod 600, **never written to
  the repo or any committed file**). New files `data/tng300_galaxies_*.npz`; do NOT overwrite the
  halo npz. Groups are ~total-mass ordered; **keep M200 > 3e10 Msun/h** (a floor low enough that all
  four stellar rungs incl. 10^8.5 are complete — M*≥3e8 needs M200≳6e10, so 3e10 has margin), stop
  scanning when the last-3-chunk max M200 < 1e10. Parallelize connections (one process per snap).
- **Completeness check (post-fetch, pre-verdict):** confirm the min M200 among the selected
  M*≥1.1e9 population sits well above the 3e10 fetch floor (no galaxy-hosting group cut). Report it.
- No synthetic data, no cap, no subsampling (densest 2³ tile stays < the proven 38k Cholesky limit;
  contingency only: a tile >38000 is subsampled to 38000, seed 20260711+1e6·T+1e3·tile+snap, flagged).
- Incremental flush; GPU via `flock /tmp/claude-1000/gpu.lockfile`.
