# Baryon cycle (GAS) — does the galaxy COORDINATE?

Two-readout test on the **gas** (PartType0) of the same complete galaxy (CAMELS
IllustrisTNG L25n256 CV_0, main progenitor of subhalo 0). The stellar component
was bound / detailed-balance-satisfying — expected, because stars are
~collisionless/conservative. Coordination, if anywhere, lives in the **gas**: the
baryon cycle (inflow → star formation → feedback → outflow → cool → re-inflow) is
a dissipative, self-regulated loop. This is the real test of whether the galaxy
coordinates.

## Matrix construction (Eulerian — gas has no persistent IDs)

Gas cells have **no persistent IDs** (Voronoi refinement; gas→stars), so no
ParticleID tracking. Instead a fixed **Eulerian** grid in the galaxy's
instantaneous frame — the natural frame for flows:

- main-progenitor FOF halo selected per snapshot (nearest real halo, >5000 gas
  cells, to the star-tracked center); gas read via the group offset (contiguous
  slice — only the halo's gas, not the 15.7M-cell box).
- center = halo `GroupPos`; bulk velocity + disk axis from inner (<30 kpc) gas.
- disk-aligned **3D grid, ±60 kpc/h, 8³ = 512 cells**. Per cell per snapshot:
  `logρ` (mass/volume), `logT` (mass-weighted, TNG temperature), `v_r`
  (mass-weighted physical peculiar radial velocity).

      UNITS = grid cells populated in ALL snapshots   N = 511
      OBSERVATIONS = snapshots                         T = 16   (z = 1.05 → 0.0)

Restricted to z ≲ 1: at higher z the galaxy is still fragmented (main progenitor
holds few of the z=0 stars) so "the galaxy's gas" and its frame are ill-defined.
z ≲ 1 is exactly the quasi-steady "equilibrium/bathtub" baryon-cycle regime
(Bouché 2010 / Davé 2012 / Lilly 2013) — the right epoch to look for a sustained
cycle. The cell×cell correlation over snapshots is a genuine collective-mode
decomposition (not the trivial cells × few-properties table).

## Readout 1 — SATURATION: gas is LOW-RANK

| scalar | N | T | PR / k_eff | eff_rank (MP) | eff_rank (surrogate) | β_top | α | plateau |
|---|---|---|---|---|---|---|---|---|
| logρ | 511 | 16 | **5.83** | 2 | 2 | 0.02 | 0.95 | flat by N′≈100 |
| v_r  | 511 | 16 | 8.43 | 4 | 3 | 0.02 | 1.20 | flat by N′≈100 |
| logT | 511 | 16 | 4.84 | 2 | 2 | 0.00 | 0.88 | flat by N′≈100 |

PR plateaus well below the T=16 ceiling and stays flat as cells are added to the
full 511; only 2–3 modes clear the phase-randomized surrogate. **The gas dynamics
are low-rank / saturating**, like the stars (and like C. elegans; unlike the
zebrafish whole brain).

## Readout 2 — DETAILED BALANCE: does the gas break it?

**Estimator:** net cycling rate `ω = ⟨x dy − y dx⟩/⟨x²+y²⟩` vs a phase-randomized
null. **Calibration ruler (n_modes=4, T=16):** OU-equilibrium Σ|ω|=0.329 (z=−0.4),
OU-driven-NESS Σ|ω|=1.455 (**z=+3.0**), relaxation Σ|ω|=0.087 (z=−0.8).
*Note the ceiling:* even the injected **driven NESS only reaches z≈3.0** at T=16 —
this test has **low statistical power** at 16 snapshots.

**(2a) Mode-circulation** on the top collective modes:

| gas scalar | Σ|ω| | z |
|---|---|---|
| logρ | 0.556 | +1.66 |
| v_r  | 0.625 | +0.83 |
| logT | 0.613 | +1.15 |

All sit **between** the equilibrium (0.33) and driven (1.46) calibrators, closer
to equilibrium, none significant (z<2).

**(2b) Thermodynamic-plane circulation** (the direct baryon-cycle signature):

| plane | measure | mean ω | z | reading |
|---|---|---|---|---|
| **(logρ, logT)** per cell | config-space | +0.0072 | **+1.12** | not significant |
| global mean-state (logρ, logT) loop | config-space | +0.063 | **+0.35** | monotone drift, no loop |
| (logρ, v_r) per cell | position–velocity | −0.044 | **−6.39** | **CONFOUNDED** (see below) |

**The one strong signal, (logρ, v_r) z=−6.4, is not clean broken-DB evidence.**
That plane pairs a coordinate (density) with a **velocity**: a *reversible*
breathing oscillation — or a one-way inflow drift — circulates there just as a
driven cycle does, and the phase-randomized null (which only needs a ρ–v_r phase
lag, i.e. quadrature) cannot separate reversible from driven. It is the standard
position–momentum confound Battle et al. avoid by using **configuration-space**
coordinate pairs. The clean configuration-space tests are the (ρ, T) ones — a
directed thermodynamic loop needs a ρ↔T **phase lag** (compress→heat→expand→cool),
and those give **z = 1.1 and 0.35: not significant.**

## VERDICTS

- **Saturation: LOW-RANK (yes).** Gas effective dimensionality is bounded
  (k_eff ≈ 5–8), saturating, at/under the corridor ceiling.
- **Broken detailed balance / coordinating: NOT ESTABLISHED (inconclusive,
  leaning not-detected).** No significant configuration-space circulation
  ((ρ,T) z=1.1; global-loop z=0.35; mode-circulation z=1.7 — all below the
  already-weak driven ruler z=3.0). The only strong circulation is in a confounded
  position–velocity plane. So this test does **not** show the baryon cycle to be a
  sustained coordinating NESS distinguishable from one-way drift plus reversible
  oscillation.

## Honest bottom line — does the baryon cycle coordinate?

**Not demonstrated here.** The prediction was that the gas *should* break detailed
balance (dissipative, self-regulated), unlike the stars. The clean tests do not
detect it — the gas reads as low-rank but detailed-balance-**inconclusive**, with
the only strong signal sitting in a confounded plane. Three load-bearing reasons
this is "not detected" rather than "shown absent":

1. **Low power at T=16** — even an *injected* driven NESS only reaches z≈3.0 at
   this snapshot count, so a genuine but modest cycle would sit below detection. A
   real conclusion needs high-cadence snapshots (e.g. TNG subboxes), which are not
   a single bound galaxy.
2. **Eulerian, not Lagrangian** — the true baryon cycle is traced by gas *parcels*
   (which change radius, temperature, phase); fixed Eulerian cells partly average
   the loop out. Gas has no IDs, so Lagrangian tracking isn't available here.
3. **EOS confound** — star-forming gas sits on TNG's effective equation of state,
   so the cold-dense branch of the (ρ,T) plane is model-imposed, not physical.

And the framing caveat stands: **TNG cooling+feedback is dissipative by
construction, and that is not automatically the framework's active-maintenance
`γ·M`.** Even a clean broken-DB detection would show "an irreversible baryon
cycle," which would still need a separate argument to equate with corridor `γ·M`.

**Net across both components of this galaxy:** stars are low-rank **and**
detailed-balance-satisfying (bound, not coordinating); gas is low-rank but
detailed-balance-**inconclusive** (no clean sustained-cycle signal at T=16). So
the complete galaxy saturates throughout, but the stronger claim — that it
*coordinates* (sustained `γ·M` cycle) — is **not established** by these tests. The
coordinating-unit question remains open; the natural next step is a
high-time-cadence, Lagrangian-tracer baryon-cycle test.

Artifacts: `spectral_galaxy_gas.py`, `spectral_results_galaxy_gas.json`,
`spectral_galaxy_gas_run.log`.
