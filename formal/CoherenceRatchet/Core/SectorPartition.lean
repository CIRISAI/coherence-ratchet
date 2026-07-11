/-
Core.SectorPartition — the entropic potential of a BLOCK-STRUCTURED (sectored)
correlation spectrum, and the sector-symmetric shared-budget steady state.

This file is the lake-side companion to the forced-partition computation
(experiments/cosmo_entropic_potential/forced_partition/). It formalizes the two
pieces of algebra that the numerics rest on and separates the DERIVABLE content
from the genuinely OPEN (dynamical) content.

SEEDED vs FORCED — the load-bearing honesty (papers/notes/entropic_matter_sector.md,
Q3/Candidate-B, and the referee paragraph). The block structure itself is an
INPUT: we PARTITION the units into sectors of dimension d_k by hand. Nothing in
this file (or the numerics) claims the sectors are discovered. What is legitimate
to read off is only what the DYNAMICS does with a seeded block structure — the
steady-state partition of S across sectors, and its stability. Additivity of S
over blocks is a theorem about the seeded structure; the partition RATIO at the
maintained steady state is the thing the numerics measure.

TWO FORMS OF S, and where proportionality-to-dimension is EXACT vs ASYMPTOTIC:

  * FULL form  S_k = entropicPotential d_k ρ_k
               = −ln(1 + ρ_k(d_k−1)) − (d_k−1)·ln(1−ρ_k)     (Core.EntropicPotential)
    Additive over blocks EXACTLY (log-det of a block-diagonal matrix). But at a
    common ρ* it is NOT exactly proportional to d_k — the −ln(1+ρ(d−1)) head term
    breaks proportionality at finite d.

  * DENSITY form  S_k = d_k · s(ρ_k),  s(ρ) = −ln(1−ρ)        (T-E3 large-d limit)
    This is the per-unit density the brief and the numerics use. At a common ρ*
    it is EXACTLY proportional to d_k: S_k = d_k · s̄. So the clean
    "partition ∝ dimension" statement is a DENSITY-form fact; the full form
    carries an O(1)-per-sector correction. This distinction is real content and
    the numerics report both.

SCOPE / F-11 NOTE. Forward/steady-state real analysis over a seeded block
spectrum. No backward operator, no joint multi-rung P_ω; does not touch
`Cosmology.CorridorProjector.F11_joint_backward_P_omega_no_go`.
-/

import CoherenceRatchet.Core.EntropicPotential
import CoherenceRatchet.Core.Dynamics

namespace CoherenceRatchet.Core

open Real

/-! ## 1. A sectored spectrum and blockwise additivity (DERIVABLE) -/

/-- One sector of a block-structured correlation spectrum: a block of `dim`
    coordinating units at within-sector correlation `rho`. `dim` is real to match
    `entropicPotential`'s signature (the matrix bridge below uses a `ℕ` dimension). -/
structure Sector where
  dim : ℝ
  rho : ℝ

/-- The entropic potential carried by one sector (FULL form). -/
noncomputable def Sector.S (s : Sector) : ℝ := entropicPotential s.dim s.rho

/-- The entropic potential of a sectored (block-diagonal) spectrum: the sum of
    the per-sector potentials. This is the object whose steady-state partition
    across sectors the numerics measure. -/
noncomputable def sectoredPotential (secs : List Sector) : ℝ :=
  (secs.map Sector.S).sum

/-- BLOCKWISE ADDITIVITY (list form). The entropic potential of a sectored
    spectrum splits additively over any partition of the sector list. Near-trivial
    at the list level — the content is that `S` is a sum over blocks — and it is
    the spectrum-level shadow of log-det additivity (matrix bridge below). -/
theorem sectoredPotential_append (a b : List Sector) :
    sectoredPotential (a ++ b) = sectoredPotential a + sectoredPotential b := by
  simp [sectoredPotential, List.map_append, List.sum_append]

/-- Blockwise additivity, cons form: peeling one sector off the front. -/
theorem sectoredPotential_cons (s : Sector) (rest : List Sector) :
    sectoredPotential (s :: rest) = s.S + sectoredPotential rest := by
  simp [sectoredPotential]

/-- Empty spectrum carries no potential. -/
@[simp] theorem sectoredPotential_nil : sectoredPotential [] = 0 := by
  simp [sectoredPotential]

/-! ## 2. The matrix bridge — additivity IS log-det factorization (DERIVABLE)

The list-level additivity above is the shadow of the honest matrix fact: the
correlation matrix of a two-sector block-diagonal spectrum has determinant equal
to the product of the block determinants, so `S = −ln det` adds. We prove the
two-block version explicitly (`Matrix.det_fromBlocks_zero₂₁`) and state that the
general block-diagonal case iterates it. -/

/-- The Kish block determinant is strictly positive on the physical domain. -/
theorem kishMatrix_det_pos (k : ℕ) (hk : 1 ≤ k) (ρ : ℝ) (hρ0 : 0 ≤ ρ) (hρ1 : ρ < 1) :
    0 < (kishMatrix k ρ).det := by
  rw [kishMatrix_det k hk ρ (ne_of_lt hρ1)]
  have hk1 : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  have h1 : (0:ℝ) < 1 + ρ * ((k : ℝ) - 1) := by nlinarith
  have h2 : (0:ℝ) < 1 - ρ := by linarith
  exact mul_pos h1 (pow_pos h2 _)

open Matrix in
/-- MATRIX BRIDGE (two sectors). The entropic potential of the block-diagonal
    correlation matrix of two sectors equals the sum of the two per-sector
    potentials — because `det (block-diag) = det₁ · det₂` and `−ln` turns the
    product into a sum. This grounds `sectoredPotential_append` in the actual
    correlation matrix rather than in the abstracted spectrum. The general
    n-sector case iterates this over the block-diagonal decomposition. -/
theorem sectoredPotential_two_eq_neg_log_det
    (k₁ k₂ : ℕ) (hk₁ : 1 ≤ k₁) (hk₂ : 1 ≤ k₂)
    (ρ₁ ρ₂ : ℝ) (hρ₁0 : 0 ≤ ρ₁) (hρ₁1 : ρ₁ < 1) (hρ₂0 : 0 ≤ ρ₂) (hρ₂1 : ρ₂ < 1) :
    entropicPotential (k₁ : ℝ) ρ₁ + entropicPotential (k₂ : ℝ) ρ₂
      = -Real.log (fromBlocks (kishMatrix k₁ ρ₁) 0 0 (kishMatrix k₂ ρ₂)).det := by
  rw [Matrix.det_fromBlocks_zero₂₁]
  have hd₁ : 0 < (kishMatrix k₁ ρ₁).det := kishMatrix_det_pos k₁ hk₁ ρ₁ hρ₁0 hρ₁1
  have hd₂ : 0 < (kishMatrix k₂ ρ₂).det := kishMatrix_det_pos k₂ hk₂ ρ₂ hρ₂0 hρ₂1
  rw [Real.log_mul (ne_of_gt hd₁) (ne_of_gt hd₂),
      entropicPotential_eq_neg_log_det k₁ hk₁ ρ₁ hρ₁0 hρ₁1,
      entropicPotential_eq_neg_log_det k₂ hk₂ ρ₂ hρ₂0 hρ₂1]
  ring

/-! ## 3. The sector-symmetric steady state and its partition (DENSITY form)

At a shared maintenance budget with EQUAL per-unit maintenance across sectors,
every sector relaxes toward a common correlation ρ* (identical per-unit drift ⇒
identical fixed point). At that symmetric state the density-form potential is
EXACTLY proportional to sector dimension: S_k = d_k · s̄ with s̄ = s(ρ*). This is
the "partition proportional to dimensions" claim, proved by algebra. -/

/-- Per-unit entropic density (the T-E3 large-`d` limit of `entropicPotential/d`). -/
noncomputable def sDensity (ρ : ℝ) : ℝ := -Real.log (1 - ρ)

/-- Density-form potential of a sector of dimension `d` at correlation `ρ`:
    `d · s(ρ)`. Exactly proportional to `d` at fixed `ρ` (this is the content the
    full form only approaches as `d → ∞`). -/
noncomputable def sectorDensity (d ρ : ℝ) : ℝ := d * sDensity ρ

/-- SECTOR-SYMMETRIC PARTITION (density form). When every sector shares the common
    correlation ρ*, the total density-form potential is `(Σ d_k) · s̄`, i.e. the
    potential partitions across sectors in EXACT proportion to their dimensions.
    Proved by induction over the sector-dimension list. -/
theorem symmetric_density_partition (dims : List ℝ) (ρ : ℝ) :
    (dims.map (fun d => sectorDensity d ρ)).sum = dims.sum * sDensity ρ := by
  induction dims with
  | nil => simp
  | cons d rest ih =>
      simp only [List.map_cons, List.sum_cons]
      rw [ih]
      simp only [sectorDensity]
      ring

/-- The per-sector share equals the dimension share: `S_k / S_total = d_k / D`.
    The clean "forced partition proportional to d" statement, in the density form
    where it is exact. Requires the common maintained state to be off the chaos
    pole (`s̄ ≠ 0`) and a nonzero total dimension. -/
theorem symmetric_partition_ratio (d Dtot ρ : ℝ)
    (hs : sDensity ρ ≠ 0) (hD : Dtot ≠ 0) :
    sectorDensity d ρ / (Dtot * sDensity ρ) = d / Dtot := by
  unfold sectorDensity
  field_simp
  ring

/-! ## 4. The shared-budget dynamics: fixed point (DERIVABLE) and stability (OPEN)

Per sector the drift is `α(ρ_k, S) − γ·m_k` (the `Core.Dynamics` object with a
per-sector maintenance `m_k` in place of the single global `M`; this is the honest
generalization to a sectored budget). "Equal per-unit maintenance" means all
`m_k = m̄`; the shared-budget constraint is `Σ d_k · m̄ = M_total`. -/

/-- Per-sector drift with an explicit sector maintenance `m` (generalizes
    `Dynamics.dρ_dt`, which fixes one global `M t`). -/
noncomputable def sectorDrift (ρ m : ℝ) (S : Dynamics.SelectionPressure) : ℝ :=
  Dynamics.α ρ S - Dynamics.γ * m

/-- A sector is at a fixed point iff its maintenance balances its drift:
    `α(ρ, S) = γ·m`. The per-sector form of `Dynamics.corridor_requires_maintenance`. -/
theorem sectorDrift_zero_iff (ρ m : ℝ) (S : Dynamics.SelectionPressure) :
    sectorDrift ρ m S = 0 ↔ Dynamics.α ρ S = Dynamics.γ * m := by
  unfold sectorDrift
  constructor <;> intro h <;> linarith

/-- SHARED-BUDGET SYMMETRIC FIXED POINT (DERIVABLE). Under EQUAL per-unit
    maintenance `m̄`, if the drift balances at the common correlation ρ*
    (`α(ρ*, S) = γ·m̄`) then EVERY sector's drift vanishes simultaneously,
    regardless of the sector dimensions: the sector-symmetric configuration is a
    joint fixed point of the shared-budget dynamics. (The drift does not depend on
    `d`, so equal per-unit maintenance forces a common fixed point — this is why
    the symmetric partition is the natural steady state to test.) -/
theorem sharedBudget_symmetric_fixedPoint
    (dims : List ℝ) (ρstar mbar : ℝ) (S : Dynamics.SelectionPressure)
    (hbalance : Dynamics.α ρstar S = Dynamics.γ * mbar) :
    ∀ _d ∈ dims, sectorDrift ρstar mbar S = 0 := by
  intro _d _
  exact (sectorDrift_zero_iff ρstar mbar S).mpr hbalance

/-- OPEN — LOCAL LINEAR STABILITY (named open step). Guarded statement, TRUE when
    the self-drift derivative at the fixed point is restoring (`L < 0`): a fixed
    point ρ* of the per-sector drift with negative slope is locally attracting —
    drift opposes displacement on both sides. Left `sorry` deliberately:

      * the SCALAR fact (a `C¹` zero with negative derivative is locally
        restoring) is standard real analysis;
      * the LOAD-BEARING object is the MULTI-SECTOR Jacobian — once the shared
        budget couples the sectors, `L` becomes a matrix whose eigenvalue signs
        (and hence whether the symmetric partition is an attractor or breaks) are
        allocation-rule-dependent and are COMPUTED, not asserted, in
        experiments/cosmo_entropic_potential/forced_partition/ (per-rule Jacobian
        eigenvalues). Stability is genuinely substrate/rule-specific here — the
        rigidity pole is UNstable — so it is correctly a numeric deliverable, not
        a blanket lake theorem. -/
theorem sectorDrift_locally_restoring
    (m : ℝ) (S : Dynamics.SelectionPressure) (ρstar L : ℝ)
    (_hfix : sectorDrift ρstar m S = 0)
    (_hderiv : HasDerivAt (fun ρ => sectorDrift ρ m S) L ρstar)
    (_hL : L < 0) :
    ∀ᶠ ρ in nhds ρstar,
      (ρstar < ρ → sectorDrift ρ m S < 0) ∧ (ρ < ρstar → 0 < sectorDrift ρ m S) := by
  sorry

end CoherenceRatchet.Core
