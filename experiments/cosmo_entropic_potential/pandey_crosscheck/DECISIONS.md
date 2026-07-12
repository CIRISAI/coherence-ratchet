# Pandey MI-minimum vs. our S-peak — pre-registered cross-check (DECISIONS, before results)

**Date 2026-07-12.** Registered in Corridor Dynamics v5 (§registered-bets, "A registered
cross-check: Pandey's mutual-information minimum vs. our S-peak"). This file fixes the method
and the verdict criterion **before** any number from this box is computed.

## STEP 1 — Pandey's estimator, VERIFIED (not guessed)

Source read in full: B. Pandey, *"Time evolution of the mutual information between disjoint
regions in the Universe,"* arXiv:2307.12959 = *Entropy* **25**(7) 1094 (2023). Companion:
Pandey & Nandi, arXiv:2601.02351 (finite-volume coherence ceiling). PDF text extracted locally
(`pdftotext`), Eqs. 1–14 read.

**The load-bearing fact about his method: the 2023 paper is ANALYTIC, not a simulation
measurement.** Pandey never grids a field, never bins densities, never runs an N-body MI
histogram. He *derives* the time evolution of the mutual information from two objects:

1. **Configuration entropy** (his Eq. 1, root object, from his 2016/2019 programme):
   `S_c(t) = -∫ ρ(r,t) log ρ(r,t) dV`, ρ = matter density in comoving subvolumes.
2. **Mutual information between two large disjoint regions A, B** (his Eqs. 4–6):
   `I_AB(t) = ∫∫ ρ_AB log[ρ_AB/(ρ_A ρ_B)] dV_A dV_B`,
   with the joint density `ρ_AB = ρ̄_A ρ̄_B [1 + ξ(r_AB,t)]` and `ρ_A ρ_B = ρ̄_A ρ̄_B`, so
   `I_AB(t) = ∫∫ ρ̄²(t) [1+ξ(r_AB,t)] log[1+ξ(r_AB,t)] dV_A dV_B`  (ξ = two-point correlation).

**His central result (Eqs. 7–14, §3, §4), verbatim in substance:**
- Matter-dominated (Ω_m=1): `dI/dt < 0` — MI decreases (`ρ̄ ∝ a^{-3}` diluting, growth
  `D∝a`). Λ-dominated (Ω_Λ=1): `dI/dt = 0` — MI constant.
- ΛCDM and dynamical/holographic DE: **MI decreases to a minimum, then increases.** He states
  it explicitly: *"The location of the minimum precisely indicates the epoch of dark energy
  domination"* and *"the time evolution of the mutual information ... [is] entirely determined
  by the behaviour of the configuration entropy rate."* The joint-entropy term is negligible;
  the driver is `dS_c/dt`.

So **Pandey's "MI-minimum epoch" = the epoch where the configuration-entropy dissipation rate
`dS_c/dt` turns (reaches its extremum and heads back toward zero)**, which he identifies with
DE-domination onset. That is the quantity we must locate on the TNG field.

**No exact binning/grid/region-size to recover** (there is none in the paper). Faithful
reconstruction stated below and flagged as such.

### A subtlety that IS the physics (recorded before results)
The standard information-theoretic MI between two cells is invariant under any per-marginal
monotone transform, including the physical-density scale `ρ̄(a)` — a copula functional, like our
own S. Such an MI grows monotonically with clustering and **cannot host Pandey's minimum.**
Pandey's minimum is a feature of the *un-normalized configuration-entropy* MI, whose
physical-density weighting `ρ̄²(a) ∝ a^{-6}` supplies the expansion/dilution that competes with
correlation growth. We therefore implement his actual (density-weighted, configuration-entropy)
object, **not** a copula-invariant MI. The copula-invariant binned MI is computed only as a
documented tertiary control (expected monotone).

## STEP 2 — Reconstruction committed BEFORE compute

**Field (same field as our S-peak, "two functionals on one field"):**
- Tracer: TNG300-1 FoF groups (halos), **mass-weighted by M200** — the same halo grain the
  S-peak B-total pipeline reads. Robustness tracer: galaxies/subhalos (denser, 566k vs 213k).
- CIC deposit (`copula_stress/copula_lib.cic_grid`) onto a periodic `Ng³` mesh, box
  L = 205 Mpc/h. **Primary Ng = 128** (cell 1.60 Mpc/h). Robustness: Ng ∈ {64, 256}.
- Physical density `ρ_i = ρ̄(a)(1+δ_i)`, comoving `ρ̄(a) ∝ a^{-3}` (comoving mass fixed; the
  overall constant `ρ̄_0` cancels in the epoch, the `a^{-3}` evolution does not and is kept).
- 26 snapshots, z = 3.008 → 0 (all group snapshots on disk).

**O1 — PRIMARY: configuration entropy and its rate (Pandey's Eq. 1 + his named driver).**
`S_c(a) = -Σ_i ρ_i ln ρ_i · ΔV`. Algebraically (⟨δ⟩=0, M=total mass, N=Ng³):
`S_c(a) = const + 3M ln a - M·G(a)`, where `G(a) ≡ ⟨(1+δ) ln(1+δ)⟩` (the density-field
negentropy / configuration information). Then `dS_c/d ln a = 3M - M·dG/d ln a`, so the
config-entropy-rate extremum ⇔ **the peak of the clustering-growth rate `dG/d ln a`.**
**Pandey MI-minimum epoch (O1) ≡ argmax_a (dG/d ln a).** `G(a)` fit with a smoothing spline in
ln a; derivative peak located on a fine grid.

**O2 — SECONDARY: Pandey MI functional (his literal Eq. 4–6).**
`I(a) = ρ̄²(a) ∫_{rmin}^{rmax} 4π r² [1+ξ(r,a)] ln[1+ξ(r,a)] dr`, `ρ̄(a) ∝ a^{-3}`, ξ(r,a) from
the CIC field via FFT `P(k) → ξ(r)`. r-range = **[5, 50] Mpc/h** (quasi-linear "large regions":
above the deeply nonlinear scale, below the box/homogeneity limit; note L/4 ≈ 51). Locate
argmin_a I(a). **Flag:** the absolute density-weighting convention is the key reconstruction
choice; O2 is corroboration for O1, not independent.

**O3 — TERTIARY control: copula-invariant binned Shannon MI (team-lead's literal recipe).**
Bin `ln(1+δ)` into Nb=16 equal-count bins; 2-D histogram of (cell_i, cell_{i+lag}) at fixed
lag; `I(X;Y)=ΣΣ p ln(p/p_x p_y)`, lags r ∈ {12.8, 25.6, 51.2 Mpc/h}. **Expected monotone**
(copula-invariant) — reported to document that the standard MI cannot reproduce Pandey's
minimum, i.e. the minimum lives in the density weighting.

**Uncertainty:** octant jackknife — split the box into 8 (2³) sub-cubes, drop one, recompute
the epoch; error = std over 8 replicates (same scheme as the S-peak 8/8 jackknife). Reported
±1σ. Incremental flush to `results.json` after every snapshot/observable.

## STEP 2b — Box-adequacy statement (honest, before results)
TNG300 (205 Mpc/h) is **modest** for a large-scale MI measure; Pandey used larger sims / SDSS
volumes. The homogeneity scale (70–150 Mpc) is a large fraction of L, so only ~1–2 independent
homogeneity-scale regions fit — the box can only marginally host the "disjoint distant large
regions" his formalism assumes. Pandey–Nandi (arXiv:2601.02351) bound retained coherence at MI
peak ≈ **L/8 = 25.6 Mpc/h**, declining beyond; our O2 r-range [5,50] straddles that ceiling, so
the large-separation end is already in the regime his own bound flags as volume-limited. If the
observable is monotone in z, or its minimum sits at the z-range edge, or the jackknife error
spans most of (0,3), the honest verdict is INCONCLUSIVE-BY-BOX, not a forced agreement/divergence.

## STEP 4 — Verdict criterion (committed BEFORE results)
Our S-peak crossing (registered DR3 prediction): **z = 0.59 ± 0.03** (physical peak).
Let z_P ± σ_P be Pandey's MI-minimum epoch (O1 primary; O2 corroborating).
- **AGREEMENT** — z_P and 0.59 coincide within combined 1σ (`|z_P − 0.59| ≤ √(σ_P² + 0.03²)`).
  Reading: two independent functionals (his configuration-entropy MI, our copula S) on the same
  TNG field name the same DE-onset epoch. **Rule-2 support** — genuine, independent, at exactly
  that weight (a confirmed independent prediction), no more: it corroborates the *mechanism*
  (matter-field information extremum marks DE onset), which is Pandey's with 2019 priority, not
  ours; it does not confirm the copula functional, the sign law, or the DR3 magnitude.
- **DIVERGENCE** — disagree beyond combined 1σ. Then at least one functional misreads the
  field; we state which is more likely and why.
- **INCONCLUSIVE-BY-BOX** — no clean/robust minimum locatable (see Step 2b). Reported honestly.

This cross-check does **not** touch the frozen DR3 bet or the anti-hedging commitment (bet 9).
