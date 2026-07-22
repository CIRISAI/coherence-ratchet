# K4 discriminator — is the copula Third real coordination or a halo/discreteness artifact? (PRE-REGISTRATION)

**Date 2026-07-20. Method frozen BEFORE any discriminator number is seen.**
The frozen `thirdness/` measurement is untouched. This directory holds the CONTROLS that
try to kill the ~20% copula-Third detection as an artifact. Kill K4 (the Third prenup,
`papers/notes/the_third_prenup.md`): *if the copula Third collapses to a shot-noise-matched
surrogate, the "physical measured Third" leg dies and only the pure-math theorem survives.*

## What the frozen null does and does NOT control

The frozen phase-randomized surrogate keeps `|δ_k|` of the **gridded** field (identical P(k),
identical C, identical S) and randomizes phases → a **continuous Gaussian** field with zero
connected ≥3-point. It controls the grid, the marginals (via normal-score), and all pairwise
power. It does **NOT** control:

1. **Discreteness / shot noise.** The real field is a discrete point catalog (mass on cells);
   the frozen surrogate is a smooth Gaussian. Poisson sampling of a point process injects
   connected ≥3-point structure purely from discreteness (the 1/n̄ terms) — invisible to the
   continuous null.
2. **Tie-spreading in the normal-score.** ~44% of NG=64 cells are empty (all at δ=−1, a tie);
   `argsort(argsort)` assigns them a deterministic, position-correlated block of low-Gaussian
   values. A continuous Gaussian surrogate has no exact ties, so it cannot expose a
   tie-break artifact.
3. **Halo bias / exclusion.** Nonlinear bias (b2, b3) and halo exclusion generate genuine
   tracer ≥3-point structure that is a property of the tracer, not necessarily of the matter
   field. Only the DM particle field fully separates these (prenup prediction 4) — not on
   disk; see §DM.

## Surrogates (pre-committed NULL controls, not synthetic data standing in for measurement)

Same status as the frozen phase-randomized null and the CMB null ensembles.

- **S0 — phase-randomized continuous Gaussian** (reproduce the frozen null): matched `|δ_k|`,
  no HOC, no discreteness. Expected copula-skew ≈ 0. Baseline / pipeline validation.
- **S1 — Poisson-clipped-Gaussian (DECISIVE shot-noise null).** Phase-randomize the real δ to a
  Gaussian field with matched `|δ_k|`; form intensity μ = n̄·(1+δ_G), clip at 0; draw counts
  `n_cell ~ Poisson(μ_cell)`; grid identically (count field). Matched n̄, matched pairwise
  power, pure Poisson discreteness + non-negativity, **no genuine connected HOC** (only the
  mild clipping nonlinearity, which if anything pushes the null TOWARD the real negative skew
  → conservative for claiming survival). Poisson resampling adds one extra 1/n̄ of shot on top
  of the shot already baked into `|δ_k|` — this makes S1 slightly noisier than real
  (conservative). N=20 realizations/snapshot → null band.
- **S1b — shot-subtracted Poisson-Gaussian (brackets the double-shot).** Same as S1 but the
  input amplitudes are shot-subtracted (`|δ_k|² → max(|δ_k|²−P_shot, 0)`, P_shot=V/N for the
  count field) before phase randomization, so that after Poisson sampling the TOTAL P(k)
  matches real. S1 and S1b bracket the true matched-discreteness null.
- **S2 — Poisson-lognormal reference (standard nonlinear clustering + discreteness).** Intensity
  from a lognormal transform of the matched-power Gaussian; Poisson-sampled. Has a calibrated,
  hierarchical HOC = the "mundane nonlinear clustering" model. NOT a null — a reference rung.
  N=10/snapshot.

## The interpretation ladder (pre-committed, read against S0/S1/S2)

Let `|k|_real`, `|k|_S1`, `|k|_S2` be |copula-skew| at R=8 (the clean scale).

- **real ≈ S1** (within the S1 band, gap < 30% of the real signal): the Third is discreteness +
  non-negativity. **K4 FIRES** — the ~20% was a shot/discreteness artifact.
- **S1 < real ≈ S2**: the Third is standard nonlinear clustering (real but mundane; the
  b2/b3/exclusion regime). **K4 PARTIALLY FIRES** — it is a tracer-clustering effect, not
  coordination beyond standard structure formation.
- **real ≫ S1 and real ≥ S2** (real above the S1 band by ≫3σ, gap a large fraction of the
  signal): the Third is **not** discreteness and exceeds the standard-clustering rung. **K4
  does NOT fire on the discreteness leg** — survives-above-surrogate = coordination (still on
  tracers, not DM particles; the halo-bias leg remains open pending §DM).

## Cuts / robustness (descriptive; report trends, no self-support)

- **PRIMARY field for the S0/S1/S2 comparison:** count-weighted, NGP, all halos ≥1e11,
  positional tie-break, R∈{4,8,16} — matched to the Poisson surrogates' construction. R=8 is
  the verdict scale (SUMMARY flagged R=4 as near the NGP cell ≈ 3.2 Mpc/h).
- **Tie-break control:** positional (frozen) vs random tie-break on the real field. If random
  tie-break moves |skew| to ≈0 while positional retains it → the signal is a raster/positional
  tie artifact (an artifact; report as K4-adjacent).
- **Assignment control:** NGP vs CIC (anti-aliasing) at R∈{4,8,16}. Confirm the R=8 detection
  and the S1 gap are assignment-independent; treat R=4 magnitude cautiously.
- **Weighting:** count vs mass (m200) weighting. The frozen measurement is mass-weighted; the
  discreteness null is count-based. Report both; the count result is the conservative core.
  Random-mass Poisson variant (masses drawn from the real mass function, no mass–environment
  correlation) tests whether mass-weighting's contribution needs genuine mass–environment
  correlation.
- **Mass threshold / bias:** copula Third across m200 ∈ {≥1e11, ≥1e12, ≥5e12} (groups). A
  nonlinear-bias artifact scales with bias (mass); genuine matter coordination should be more
  stable. Report the trend (no hard cut — the bias leg is not cleanly killable without DM).
- **Tracer:** groups (m200) vs galaxies (count, mstar-weighted). Bias artifacts differ between
  tracers; genuine coordination should be more stable across tracers.

## DM particle field (§DM — attempt ONLY if the S1 result is AMBIGUOUS)

The true K4 discriminator is the DM **particle** field (prenup prediction 4). On disk we have
only halo/galaxy catalogs. A TNG300-1 DM particle pull is the full `snapshot-{snap}.{c}.hdf5`
PartType1 Coordinates — billions of particles, many GB, ~230 s/chunk — not a spot-check-sized
download. It will be attempted (ONE snapshot, subsampled) ONLY if S1 leaves real within ~2–3σ
of the surrogate (ambiguous). If S1 is decisive either way, the DM pull is not run; the
tracer-only limit is stated plainly. The API key stays at `~/.tng_api_key`, never written to
the repo.

## Discipline

No synthetic data (S0–S2 are pre-committed nulls/reference rungs, same status as the CMB null
ensembles). Grain fixed before spectrum. Method frozen at this write; the verdict statistic
(|skew|_real vs |skew|_S1 at R=8) and the ladder are committed here and not tuned after seeing
numbers. Incremental flush per snapshot. If K4 fires, that is a clean, important result to
report plainly, not a disappointment. The frozen `thirdness/` files are not modified.
