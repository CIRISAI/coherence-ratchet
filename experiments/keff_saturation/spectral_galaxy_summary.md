# Complete bound galaxy — k_eff saturation verdict

SATURATION test of the criticality-vs-low-rank discriminator on a COMPLETE,
GRAVITATIONALLY-BOUND galaxy at astrophysical scale — a legitimate complete-unit
test (unlike the cosmic web, which is a finite past-light-cone subsample of the
universe, or Gaia's partial internal view of the Milky Way).

## GRAVITY CAVEAT (read first — do not gloss)

This galaxy is bound by **gravity**, a conservative binding force. In the
framework's dynamics `dρ/dt = α(ρ,S) − γ·M`, a shared gravitational potential is
the **spontaneous α-term** (shared environment / shared selection), **not** the
active-maintenance `γ·M` that defines corridor *coordination*. So this measures
**"does a complete BOUND unit saturate,"** which is adjacent to — but not
identical to — **"does a complete COORDINATING unit saturate."** The result below
does **not** settle the coordinating-unit question. It is reported as a
bound-unit datapoint only.

## Dataset + where

- **CAMELS · IllustrisTNG · L25n256 · CV_0** (fiducial cosmology+astrophysics),
  pulled by remote partial-HDF5 reads from the public CAMELS mirror
  `https://users.flatironinstitute.org/~camels/Sims/IllustrisTNG/CV/CV_0/`
  (26 snapshots `snapshot_040…090.hdf5` + SUBFIND catalog `groups_090.hdf5`).
- **Target = SUBFIND subhalo 0** — the central galaxy of FOF group 0, the most
  star-rich bound galaxy in the box: **47,736 star particles at z=0**
  (M⋆ ≈ 4.3×10¹¹ M⊙/h — a massive, merger-built central; a non-cherry-picked,
  if anything adversarial, choice for a *low*-rank test). Because we hold **every
  star particle of the bound unit**, subsampling runs up to the full constituent
  count and **"wrong grain" cannot be invoked**.
- Real simulation data only. Synthetics (low-rank / power-law / noise) are used
  **solely** to calibrate the estimator at this (N,T); they never enter the verdict.

## The matrix (N, T) — the crux, avoids the trivial rank≤6 trap

**Time-resolved.** Units = star particles tracked by `ParticleID`; observations =
snapshots. Entry `X[i,t]` = a kinematic scalar of star *i* at snapshot *t*,
measured in the galaxy's **own instantaneous frame** (robust iterative
periodic-aware center; bulk velocity removed; disk axis = angular-momentum
direction of the bound core, sign-aligned across snapshots; comoving→physical):

| scalar | meaning |
|---|---|
| **z-height** (primary) | height above the instantaneous principal plane (physical kpc) |
| j_z | specific angular momentum about the disk axis |
| v_r | galactocentric radial velocity (physical peculiar km/s) |

    UNITS (rows, subsampled)   N = 25,579  stars present in ALL 26 snapshots
    OBSERVATIONS (cols)        T = 26      snapshots, z = 2.3 → 0.0

The **star × star correlation over snapshots** asks whether the galaxy's dynamics
collapse to a **few collective modes** (rotation / bar / bending+breathing waves /
coherent settling = LOW-RANK) or are high-dimensional (each star an independent
oscillator). This is NOT the trivial `stars × {x,y,z,vx,vy,vz}` table (rank ≤ 6 by
construction); it is a genuine collective-mode decomposition over cosmic time.

**Interpretation guard.** Because rank ≤ T−1 = 25, PR is capped at ~26, so the
PR-vs-N′ curve *flattening* is partly structural and is **not** itself the signal.
The discriminating quantities are (i) the plateau **level** vs the matched-(N,T)
synthetic calibrators, (ii) the effective rank above a phase-randomized surrogate,
(iii) the steepness of the eigenvalue spectrum. T=26 is modest — a stronger test
needs higher snapshot cadence for one galaxy (e.g. TNG subbox), which is not a
single bound unit; noted as a limitation.

## Calibration at N=5000, T=26 (the ruler works here)

| synthetic | PR | eff_rank (vs surrogate) | β_top | α |
|---|---|---|---|---|
| low-rank r=3    |  4.05 | 3 | −0.001 | 0.93 |
| low-rank r=6    |  5.96 | 5 |  0.007 | 2.13 |
| power-law α=1.0 | 20.93 | 5 |  0.032 | 0.45 |
| power-law α=0.6 | 24.57 | 3 |  0.030 | 0.15 |
| pure noise      | 24.87 | 0 |  0.029 | 0.09 |

At this T, the **PR level** cleanly separates the regimes: low-rank sits at PR≈r
(4–6), while power-law and noise sit near the T-ceiling (PR≈21–25). Estimator
validated at this grain.

## Result on the complete bound galaxy

| scalar | N | T | PR / k_eff | eff_rank (MP) | eff_rank (surrogate) | β_top | α | plateau onset |
|---|---|---|---|---|---|---|---|---|
| **z-height** | 25,579 | 26 | **4.26** | 3 | 2 | 0.000 | 1.20 | N′≈300 |
| j_z          | 25,579 | 26 | 10.70 | 10 | 3 | 0.001 | 2.01 | N′≈300 |
| v_r          | 25,579 | 26 | 10.94 |  4 | 2 | 0.000 | 0.50 | N′≈300 |

Saturation curve (primary z-height), PR vs N′ — **flat from a few hundred stars up
to the full 25,579:**

| N′ | 10 | 20 | 50 | 100 | 300 | 1000 | 3000 | 10000 | 25579 |
|----|----|----|----|-----|-----|------|------|-------|-------|
| PR | 3.18 | 3.81 | 4.04 | 4.08 | 4.22 | 4.24 | 4.26 | 4.26 | 4.26 |

- z-height top eigenvalues: **9547, 7493**, 1784, 884, 738, 635, … — **two
  dominant collective modes** then a steep fall. j_z: 4239, 3443, 2562, … (α=2.0,
  the steepest — most low-rank). All three scalars land **far below** the
  noise/power-law PR ceiling (~21–25) and **at or near the low-rank synthetics**.
- Adding constituents from 10 → 25,579 (all the way to the complete bound unit)
  **does not add effective dimensions**: k_eff ≈ 4 (z-height) / ≈ 11 (j_z, v_r),
  bounded, at/under the framework's ~10 corridor ceiling.

## VERDICT: SATURATES (bounded k_eff / few collective modes) — LOW-RANK

A **complete gravitationally-bound galaxy saturates**. Its stellar phase-space
dynamics over cosmic time collapse to a handful of collective modes (k_eff ≈ 4–11,
bounded, at/under the ~10 ceiling), with only 2–3 modes clearing a phase-
randomized surrogate and a steep eigenvalue spectrum. On a complete unit where
"wrong grain" cannot be invoked, effective dimensionality **does not grow with
constituent count** — the low-rank / corridor-consistent signature.

## Readout 2 — broken detailed balance (bound vs COORDINATING)

Saturation says low-rank; it does **not** say whether the low rank is
actively-maintained. The deeper `dρ/dt = α − γ·M` question: a **coordinating**
system is a non-equilibrium steady state sustained by `γ·M` that **breaks detailed
balance** (net probability currents / circulation in its collective coordinates,
positive entropy production); a merely **bound** system (gravity = conservative
`α`, no `γ·M`) satisfies detailed balance (≈zero net circulation) for the
collisionless stellar component (Battle et al. 2016, Science; Gnesotto 2018).

Test: project each scalar's star×snapshot matrix onto its top collective (SVD)
modes; for each mode pair estimate the mean cycling rate
`ω = ⟨x dy − y dx⟩ / ⟨x²+y²⟩` (net circulation; E[ω]=0 under detailed balance),
significance vs a **phase-randomized** null (preserves each mode's power spectrum,
destroys the cross-mode phase relations that produce net rotation). Summed |ω|
over the top-3 pairs is an entropy-production proxy.

**Calibration ruler (n_modes=4, T=26):**

| synthetic | Σ|ω| | z (Σ) | top-pair z |
|---|---|---|---|
| OU-equilibrium (reversible) | 0.125 | −1.4 (≈0) | −1.1 |
| **OU-driven (NESS, breaks DB)** | **1.232** | **+4.35** | +3.1 |
| relaxation (transient) | 0.093 | +0.5 | −1.5 |

**Galaxy:**

| scalar | Σ|ω| | z (Σ) | mode-pair z's |
|---|---|---|---|
| z-height | 0.357 | **+0.62** | (0,1): **−2.0**;  (0,2): +0.4;  (1,2): 0.0 |
| j_z      | 0.278 | +0.03 | (0,1): +0.2; (0,2): +0.3; (1,2): −1.4 |
| v_r      | 0.286 | +0.34 | (0,1): −1.0; (0,2): −1.2; (1,2): +0.7 |

The galaxy's **summed circulation is not significant** (z = 0.0–0.6 for all three
scalars) and sits **far below the driven-NESS ruler** (Σ|ω| ≈ 0.3 vs 1.23; z ≈ 0
vs +4.35). Only a single z-height mode pair reaches |z|≈2 — the one-way arc of the
top assembly mode, i.e. the **transient cosmic-assembly drift**, not a sustained
cycle (the relaxation calibrator behaves the same way: modest, one-pair).

**Readout-2 verdict: DETAILED-BALANCE-SATISFYING → BOUND, NOT COORDINATING.**
Exactly the theoretical prediction for a ~collisionless/conservative stellar
system. Caveats that bound this readout: **T=26 is a short, non-stationary
trajectory** (a proper NESS test wants a long stationary segment), and any
residual irreversibility is most plausibly transient gravitational relaxation, not
`γ·M`.

## How this sits against the other complete-unit tests

| complete unit | verdict | k_eff / PR |
|---|---|---|
| C. elegans whole brain | **LOW-RANK (saturates)** | small, bounded |
| **this bound galaxy** | **LOW-RANK (saturates)** | **≈4–11, bounded** |
| zebrafish whole brain (ZAPBench) | **FALSIFICATION — high-dim, does NOT saturate** | PR≈34, 1592 CV dims, α≈1.36 |
| mouse-V1 cortex (subsample) | grain-inconclusive | α≈0.97 |
| cosmic web (survey subsample) | power-law, grain-inconclusive | α≈0.75, PR≈52 climbing |

**Correction to the task framing:** the request described zebrafish as a complete
brain that *saturates* (α≈1.5). The repo's own `spectral_zebrafish_summary.md`
records the **opposite** — the complete zebrafish brain was a **falsification**
(high-dimensional, PR≈34, 1592 cross-validated dims, does not saturate). So this
galaxy lands with **C. elegans (low-rank)**, i.e. on the *opposite* side from the
zebrafish whole-brain result, not alongside it.

## Honest bottom line — TWO separated readouts

**(1) Saturation: YES.** A whole gravitationally-bound galaxy's stellar dynamics
are low-rank (k_eff ≈ 4–11, bounded, at/under the ~10 corridor ceiling), robust
across three independent kinematic scalars, on the full ~25.6k-star constituent
set where the grain objection is unavailable. (Load-bearing evidence is the
plateau **level** vs matched-(N,T) calibrators and the small surrogate rank, not
curve-flatness — T=26 rank-caps PR at ~26.)

**(2) Coordinating? NO.** The same modes are **detailed-balance-satisfying** —
near-zero net circulation, far below the driven-NESS ruler — so the low rank is a
**conservatively BOUND** structure, not an actively-maintained (`γ·M`) coordinating
one. Gravity is the α-term, as the caveat said; this readout confirms it
empirically rather than just asserting it.

**The two readouts together are the real result:** low-dimensionality alone does
**not** imply coordination. A complete bound galaxy saturates *and* is bound-not-
coordinating — showing that the saturation test and the detailed-balance test
measure different things, and that "complete bound unit saturates" ≠ "complete
coordinating unit saturates." The coordinating-unit question stays open; the two
complete *brain* tests (C. elegans low-rank vs zebrafish high-dim) remain split,
and neither has yet been run through the detailed-balance detector.

Artifacts: `spectral_galaxy.py`, `spectral_galaxy_db.py`,
`spectral_results_galaxy.json`, `spectral_results_galaxy_db.json`,
`spectral_galaxy_run.log`.
