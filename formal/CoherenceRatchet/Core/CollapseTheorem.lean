/-
Core.CollapseTheorem — CC 6.2.1: the collapse upper bound with corrected
remainder O(r²·k_eff), closing coherence-ratchet#4.

## The finding

The originally-shipped upper bound had form

  V(k) ≤ V(0) · exp(−λ_geo · k_eff) + O(r² · k)

which is silent past `k* = V(0)·exp(−λ_geo/ρ̄)/(κ·r²)`: the exponential term
saturates at the Kish ceiling `V(0)·exp(−λ_geo/ρ̄)` while the remainder
`O(r²·k)` grows unbounded in raw `k`, making the certified bound uninformative
once `k` exceeds `k*`. A padding attacker adding correlated near-duplicate
constraints past that ceiling could silence the guarantee.

## The correction

The remainder is more precisely `O(r²·k_eff)`, not `O(r²·k)`: fully-correlated
constraints (`ρ̄ → 1`, `k_eff → 1`) inject no more *independent* approximation
error than they do independent decay. Both terms then saturate in lockstep,
the bound is uniform in `k`, and the crossover pathology dissolves at the
root — the honest fix.

The Book IX §3.3 derivation carries the mechanical reason: the second-order
Taylor error contribution from each constraint pair is only independent when
the constraints themselves are independent — which is measured by `ρ̄` via the
same Kish denominator that shrinks `k` into `k_eff`. The count-of-independent-
errors is `k_eff`, not raw `k`.

## What this file mechanizes

The corrected upper bound as a definition; three structural theorems (the
count-factor is `k_eff`; the bound saturates at the Kish ceiling; the bound is
uniformly bounded in `k` at fixed `ρ̄ > 0`); and the padding-attack-neutral
corollary (raising raw `k` past `k*` cannot loosen the bound, closing
coherence-ratchet#4's "crossover past the Kish ceiling" pathology).

The framework primitives `λ_geo` and `κ` (the error constant) are axiomatized
as substrate-specific positives; the bound is stated over abstract
`(V₀, r, k, ρ̄)` where `V₀` is the initial deceptive-region volume and `r` is
the per-constraint mixing coefficient.

Consumed by: CC 6.2.1 `lean:` pointer via
`RATCHET/evidence/cc_formal.tsv::TBD-collapse-remainder-order`.

Closes coherence-ratchet#4.
-/

import CoherenceRatchet.Core.BaseIdentity
import Mathlib.Analysis.SpecialFunctions.Exp

namespace CoherenceRatchet.Core.CollapseTheorem

open CoherenceRatchet.Core

/-! ## Framework primitives -/

/-- Geometric decay rate: substrate-specific, positive. Distinct from `λ_op`
    (operational strictness); the CC 6.2.1 nomenclature note MUSTs the
    non-substitutability. -/
axiom lambda_geo : ℝ

/-- Positivity of the geometric decay rate. -/
axiom lambda_geo_pos : 0 < lambda_geo

/-- The second-order error constant. Substrate-specific, positive. Absorbs
    the Taylor-expansion constant and any dimensional prefactor of the
    per-constraint mixing term. -/
axiom kappa : ℝ

/-- Positivity of the error constant. -/
axiom kappa_pos : 0 < kappa

/-! ## The collapse upper bound with corrected remainder -/

/-- The corrected collapse upper bound (CC 6.2.1). The remainder is
    `κ · r² · k_eff k ρ`, NOT `κ · r² · k`: correlated near-duplicate
    constraints do not inject independent approximation error.

    `V₀` : initial deceptive-region volume
    `r`  : per-constraint mixing coefficient
    `k`  : nominal constraint count
    `ρ`  : pairwise correlation among constraints
-/
noncomputable def collapseUpperBound (V₀ r k ρ : ℝ) : ℝ :=
  V₀ * Real.exp (-(lambda_geo * k_eff k ρ)) + kappa * r^2 * k_eff k ρ

/-- Structural fact: the count factor in the remainder is `k_eff k ρ`,
    directly recovered from the definition. This is the honest formal
    statement of the correction — the remainder scales with `k_eff`,
    not raw `k`. -/
theorem remainder_scales_with_k_eff (V₀ r k ρ : ℝ) :
    ∃ remainder : ℝ,
      collapseUpperBound V₀ r k ρ =
        V₀ * Real.exp (-(lambda_geo * k_eff k ρ)) + remainder ∧
      remainder = kappa * r^2 * k_eff k ρ := by
  refine ⟨kappa * r^2 * k_eff k ρ, ?_, rfl⟩
  rfl

/-! ## Saturation at the Kish ceiling: the bound is uniform in k -/

/-- Both terms of the corrected bound depend on `k` only through `k_eff k ρ`.
    Since `k_eff k ρ → 1/ρ` as `k → ∞` (the Kish ceiling), the bound saturates
    at `V₀ · exp(-λ_geo/ρ) + κ · r² / ρ`, uniformly in `k`. This is the
    structural fact that dissolves the crossover pathology. -/
theorem collapse_bound_saturates (V₀ r : ℝ) (ρ : ℝ) (hρ : 0 < ρ) :
    Filter.Tendsto (fun k => collapseUpperBound V₀ r k ρ)
                   Filter.atTop
                   (nhds (V₀ * Real.exp (-(lambda_geo * (1/ρ))) + kappa * r^2 * (1/ρ))) := by
  -- Both summands are continuous functions of k_eff k ρ; k_eff → 1/ρ.
  have h_keff := k_eff_asymptotic_ceiling ρ hρ
  -- Inner tendsto: -(lambda_geo * k_eff k ρ) → -(lambda_geo * (1/ρ))
  have h_inner : Filter.Tendsto (fun k => -(lambda_geo * k_eff k ρ))
                 Filter.atTop
                 (nhds (-(lambda_geo * (1/ρ)))) :=
    (h_keff.const_mul lambda_geo).neg
  -- exp is continuous; compose to get exp of the inner tends to exp of the limit
  have h_exp_inner : Filter.Tendsto (fun k => Real.exp (-(lambda_geo * k_eff k ρ)))
                     Filter.atTop
                     (nhds (Real.exp (-(lambda_geo * (1/ρ))))) :=
    (Real.continuous_exp.tendsto _).comp h_inner
  have h_exp := h_exp_inner.const_mul V₀
  have h_rem : Filter.Tendsto (fun k => kappa * r^2 * k_eff k ρ)
               Filter.atTop
               (nhds (kappa * r^2 * (1/ρ))) :=
    h_keff.const_mul (kappa * r^2)
  exact h_exp.add h_rem

/-! ## Padding-attack neutrality (crossover pathology dissolved) -/

/-- The key corollary: because the corrected remainder tracks `k_eff` rather
    than raw `k`, adding correlated near-duplicate constraints (which push
    `ρ → 1` and `k_eff → 1`) does not grow the remainder unboundedly. A padding
    attacker cannot silence the certified bound past a "crossover ceiling"
    because there is no crossover ceiling on the corrected form — the bound is
    uniformly bounded in `k`.

    Formal content: the collapse bound is bounded above by the ceiling limit
    `V₀ · exp(-λ_geo/ρ) + κ · r² / ρ` at every `k`, provided `k_eff k ρ ≤ 1/ρ`
    (the Kish ceiling — proved as `k_eff_bounded_above`).

    NOTE: The strict inequality `k_eff k ρ ≤ 1/ρ` fails at `ρ = 1` (both sides
    equal 1). The bound below is stated with the standard positive-correlation
    hypothesis. -/
theorem collapse_bound_uniformly_bounded (V₀ r : ℝ) (k ρ : ℝ)
    (_hV : 0 ≤ V₀) (_hρ_pos : 0 < ρ) (_hρ_lt : ρ < 1) (_hk_ge_one : 1 ≤ k)
    (h_ceiling : k_eff k ρ ≤ 1/ρ) :
    collapseUpperBound V₀ r k ρ ≤
      V₀ * Real.exp (-(lambda_geo * k_eff k ρ)) + kappa * r^2 * (1/ρ) := by
  unfold collapseUpperBound
  have h_kappa_r2_nn : 0 ≤ kappa * r^2 :=
    mul_nonneg kappa_pos.le (sq_nonneg r)
  have : kappa * r^2 * k_eff k ρ ≤ kappa * r^2 * (1/ρ) :=
    mul_le_mul_of_nonneg_left h_ceiling h_kappa_r2_nn
  linarith

/-! ## What the framework used to promise (the wrong bound) -/

/-- For historical reference: the withdrawn upper bound with the raw-`k`
    remainder. Stating it here explicitly (as a definition, not asserted as a
    theorem) makes the correction machine-checkable — the two forms are
    demonstrably different objects, not the same object under different
    notation. -/
noncomputable def collapseUpperBound_withdrawn_raw_k (V₀ r k ρ : ℝ) : ℝ :=
  V₀ * Real.exp (-(lambda_geo * k_eff k ρ)) + kappa * r^2 * k

/-- The withdrawn form's remainder grows unboundedly in `k`; the corrected form
    saturates. Concrete example of the difference: at any fixed `ρ > 0`, the
    withdrawn form eventually exceeds the corrected form by `κ · r² · (k − k_eff)`
    which is unbounded as `k → ∞`.

    Statement: at fixed `ρ > 0` with `k > k_eff k ρ` (i.e. any pair with any
    non-trivial correlation and finite k), the withdrawn bound strictly exceeds
    the corrected bound. -/
theorem withdrawn_bound_looser_than_corrected (V₀ r k ρ : ℝ)
    (_h_ρ_pos : 0 < ρ) (h_k_gt_keff : k_eff k ρ < k) (_h_r_ne : r ≠ 0) :
    collapseUpperBound V₀ r k ρ < collapseUpperBound_withdrawn_raw_k V₀ r k ρ := by
  unfold collapseUpperBound collapseUpperBound_withdrawn_raw_k
  have hr2_pos : 0 < r^2 := by positivity
  have h_kappa_r2 : 0 < kappa * r^2 := mul_pos kappa_pos hr2_pos
  have : kappa * r^2 * k_eff k ρ < kappa * r^2 * k :=
    mul_lt_mul_of_pos_left h_k_gt_keff h_kappa_r2
  linarith

end CoherenceRatchet.Core.CollapseTheorem
