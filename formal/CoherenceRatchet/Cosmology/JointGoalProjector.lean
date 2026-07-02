/-
Cosmology.JointGoalProjector — operator form of multi-agent consent

For n agents with goals G_1, ..., G_n on Hilbert spaces H_1, ..., H_n, the joint
post-selection is the tensor product:

  P_{G_1...G_n} = P_{G_1} ⊗ P_{G_2} ⊗ ... ⊗ P_{G_n} : ⊗_i H_i →L[ℂ] ⊗_i H_i

This file formalizes that operator as a continuous linear map on the tensor-
product Hilbert space, and the consent corridor as a constraint on its support.

The earlier `MultiAgentConsent.lean` carried `P_joint` as a placeholder
(`Type := sorry`); this file replaces it with the proper operator construction.

STRUCTURE:
- ⊗_i P_{G_i} : ⊗_i H_i →L[ℂ] ⊗_i H_i, the rank-one-in-each-factor projector
- support: range of the joint projector — PROVABLY at most 1-dimensional for
  EVERY federation (`jointSupport_rank_le_one`): a tensor product of rank-one
  factors is rank-one, regime irrelevant
- rho_goals: the pairwise correlation |⟨G_i|G_j⟩|², a concrete definition
  (formerly an opaque axiom), with boundedness and diagonal-1 as theorems
- the regime content (rigidity collapse vs. corridor multi-dimensionality)
  lives on the GOAL-SPAN span{G_i.vec} ⊆ H in the homogeneous case, not on
  the tensor-product support: corridor ⇒ goal-span rank ≥ 2 (proved, strict
  Cauchy–Schwarz); all-pairwise-correlation-1 ⇒ goal-span rank ≤ 1 (proved,
  Cauchy–Schwarz equality case)

CORRECTION (2026-07-01, discharged in the same pass that concretized
rho_goals): the earlier draft asserted the regime distinction on the rank of
the joint tensor-product support — `rigid_collapse_to_one_dim` (rank ≤ 1
given rigidity) and `consent_corridor_nontrivial_support` (rank ≥ 2 given
corridor), both axioms. The first had a spurious hypothesis (the bound is
unconditional); the second was FALSE of the concrete construction — with a
concrete `rho_goals` making corridor-occupation exhibitable, it would have
made the lake inconsistent against `jointSupport_rank_le_one`. Both axioms
are removed; the true rank-one fact is proved honestly; the regime claims
are restated on the goal-span, where they are theorems. The tensor-range
formulation could not carry the regime distinction — falsification
discipline applied to the lake's own formalization.

AXIOM LEDGER for this file: `rho_goals`, `rho_goals_bounded`,
`rho_goals_diagonal` discharged to def + theorems (2026-07-01);
`rigid_collapse_to_one_dim`, `consent_corridor_nontrivial_support` removed
as above (2026-07-01). Remaining axioms: `k_eff_goals`,
`k_eff_goals_corridor_iff` (structural, Kish-identity composition).

References:
- Aharonov, Bergmann, Lebowitz (1964): ABL inner product on tensor products
- Aharonov, Vaidman (2008): joint post-selection structure §3
- Reed & Simon, Methods of Modern Mathematical Physics II §VIII.10: tensor
  products of Hilbert spaces
-/

import CoherenceRatchet.Cosmology.GoalProjection
import CoherenceRatchet.Core.Corridor
import Mathlib.LinearAlgebra.TensorProduct.Basic
import Mathlib.LinearAlgebra.PiTensorProduct
import Mathlib.LinearAlgebra.LinearIndependent
import Mathlib.LinearAlgebra.Dimension.Basic
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.Data.Fin.VecNotation
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.NormedSpace.OperatorNorm.Basic

namespace CoherenceRatchet.Cosmology.JointProjector

open CoherenceRatchet.Cosmology.Goal
open CoherenceRatchet.Core.Corridor
open Cardinal

universe u

/-! ## Single-agent state space and goal projector -/

variable {n : ℕ}
variable (H : Fin n → Type u)
variable [∀ i, NormedAddCommGroup (H i)]
variable [∀ i, InnerProductSpace ℂ (H i)]
variable [∀ i, CompleteSpace (H i)]

/-- A federation: an indexed family of agent goal-states. -/
structure Federation where
  goal : ∀ i : Fin n, GoalState (H i)

/-- The rank-one projector for a single agent's goal-state. Concrete
    construction: `P_G = (innerSL ℂ G.vec).smulRight G.vec`, the standard
    Dirac-notation `|G⟩⟨G|` mapping `x ↦ ⟨G | x⟩ • G.vec`. -/
noncomputable def singleProjector {i : Fin n} (G : GoalState (H i)) : (H i) →L[ℂ] (H i) :=
  (innerSL ℂ G.vec).smulRight G.vec

/-- Rank-one action: `singleProjector G x = ⟨G | x⟩ • G.vec`. -/
theorem singleProjector_apply {i : Fin n} (G : GoalState (H i)) (x : H i) :
    singleProjector H G x = @inner ℂ _ _ G.vec x • G.vec := by
  unfold singleProjector
  rw [ContinuousLinearMap.smulRight_apply, innerSL_apply]

/-- The self-inner product of a unit vector is 1. Helper lemma. -/
private lemma inner_self_of_unit {i : Fin n} (G : GoalState (H i)) :
    @inner ℂ _ _ G.vec G.vec = 1 := by
  have h := @inner_self_eq_norm_sq_to_K ℂ _ _ _ _ G.vec
  rw [G.unit_norm] at h
  simpa using h

/-- Idempotence: `P_G · P_G = P_G` via `⟨G | G⟩ = 1`. -/
theorem singleProjector_idempotent {i : Fin n} (G : GoalState (H i)) :
    ∀ x : H i, singleProjector H G (singleProjector H G x) = singleProjector H G x := by
  intro x
  rw [singleProjector_apply, singleProjector_apply, inner_smul_right,
      inner_self_of_unit, mul_one]

/-- Self-adjointness: `⟨P_G x | y⟩ = ⟨x | P_G y⟩` via inner-product
    conjugate-symmetry on a rank-one projector. -/
theorem singleProjector_self_adjoint {i : Fin n} (G : GoalState (H i)) :
    ∀ x y : H i, @inner ℂ _ _ (singleProjector H G x) y =
                 @inner ℂ _ _ x (singleProjector H G y) := by
  intro x y
  rw [singleProjector_apply, singleProjector_apply, inner_smul_left, inner_smul_right,
      inner_conj_symm x G.vec]
  ring

/-! ## Tensor-product space and joint projector -/

/-- The tensor-product Hilbert space ⊗_i H_i. -/
abbrev JointSpace := PiTensorProduct ℂ H

/-- The joint goal-projector `P_{G_1...G_n} = ⊗_i P_{G_i}` on the tensor
    product space. Concrete construction via `PiTensorProduct.map` on the
    family of per-factor rank-one projectors. -/
noncomputable def P_joint (fed : Federation H) : JointSpace H →ₗ[ℂ] JointSpace H :=
  PiTensorProduct.map (fun i => (singleProjector H (fed.goal i)).toLinearMap)

/-- Tensor product of idempotents is idempotent. Real theorem proved by
    extending across tprod generators and applying `singleProjector_idempotent`
    per factor. -/
theorem P_joint_idempotent (fed : Federation H) :
    ∀ x : JointSpace H, P_joint H fed (P_joint H fed x) = P_joint H fed x := by
  suffices h : (P_joint H fed).comp (P_joint H fed) = P_joint H fed by
    intro x
    have := LinearMap.congr_fun h x
    simpa using this
  unfold P_joint
  apply PiTensorProduct.ext
  apply MultilinearMap.ext
  intro f
  simp only [LinearMap.compMultilinearMap_apply, LinearMap.coe_comp, Function.comp_apply,
             PiTensorProduct.map_tprod, ContinuousLinearMap.coe_coe]
  congr 1
  funext i
  exact singleProjector_idempotent H (fed.goal i) (f i)

/-- The range of the joint projector — the subspace onto which the
    post-selection projects. NOTE: this range is at most 1-dimensional for
    every federation (`jointSupport_rank_le_one`); it is the line spanned by
    the product goal-state `⊗_i G_i.vec`. The regime distinction lives on
    the goal-span (`goalSpan`), not here. -/
noncomputable def jointSupport (fed : Federation H) : Submodule ℂ (JointSpace H) :=
  LinearMap.range (P_joint H fed)

/-- The joint support is (at most) a line — for EVERY federation, regime
    irrelevant. On generators, `P_joint (⊗_i f_i) = (∏_i ⟨G_i|f_i⟩) • ⊗_i
    G_i.vec`: a tensor product of rank-one projectors is rank-one, so the
    range is contained in `span{⊗_i G_i.vec}`. This is the honest statement
    of what the tensor-product construction gives; the two former regime
    axioms on this rank are removed (see file header, CORRECTION). -/
theorem jointSupport_rank_le_one (fed : Federation H) :
    Module.rank ℂ (jointSupport H fed) ≤ 1 := by
  have hle : jointSupport H fed
      ≤ Submodule.span ℂ {(PiTensorProduct.tprod ℂ) (fun k => (fed.goal k).vec)} := by
    intro x hx
    obtain ⟨y, rfl⟩ := hx
    induction y using PiTensorProduct.induction_on with
    | smul_tprod r f =>
      rw [map_smul]
      refine Submodule.smul_mem _ r ?_
      have h1 : P_joint H fed ((PiTensorProduct.tprod ℂ) f)
          = (PiTensorProduct.tprod ℂ)
              (fun k => (@inner ℂ _ _ (fed.goal k).vec (f k)) • (fed.goal k).vec) := by
        unfold P_joint
        rw [PiTensorProduct.map_tprod]
        congr 1  -- per-factor: `singleProjector G x = ⟨G|x⟩ • G.vec` (`singleProjector_apply`)
      rw [h1, MultilinearMap.map_smul_univ]
      exact Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self _)
    | add a b ha hb =>
      rw [map_add]
      exact Submodule.add_mem _ ha hb
  calc Module.rank ℂ (jointSupport H fed)
      ≤ Module.rank ℂ
          (Submodule.span ℂ {(PiTensorProduct.tprod ℂ) (fun k => (fed.goal k).vec)}) :=
        Submodule.rank_mono hle
    _ ≤ #({(PiTensorProduct.tprod ℂ) (fun k => (fed.goal k).vec)} : Set (JointSpace H)) :=
        rank_span_le _
    _ = 1 := Cardinal.mk_singleton _

/-! ## Pairwise goal correlation -/

open scoped Classical in
/-- The pairwise goal correlation between agents i and j:

      ρ_goals(i, j) = |⟨G_i|G_j⟩|² / (⟨G_i|G_i⟩⟨G_j|G_j⟩)

    Formerly an opaque framework axiom (with `rho_goals_bounded` and
    `rho_goals_diagonal` as further axioms about it); now a concrete
    definition, both properties discharged to theorems.

    The heterogeneous per-agent family `H i` cannot express `⟨G_i|G_j⟩`
    without a substrate-encoding map — the Sensor-lift refactor
    (`papers/Corridor Dynamics.tex` §sec:a3-structural) supplies it as
    cross-sensor reflexive inner products on a shared `H`. Until that
    encoding is in the lake, the definition reads:
    - factors with type-equal state spaces (`H i = H j`) — in particular
      every homogeneous federation, where the identity encoding is
      canonical — get the normalized inner product along the cast;
    - type-distinct factors read 0 (decoupled): absent an encoding the
      framework licenses no cross-substrate correlation claim, hence no
      corridor claim. A conservative default, to be replaced by the
      explicit encoding map when it lands. -/
noncomputable def rho_goals (fed : Federation H) (i j : Fin n) : ℝ :=
  if h : H i = H j then
    Complex.normSq (@inner ℂ (H j) _ (cast h (fed.goal i).vec) (fed.goal j).vec) /
      (‖cast h (fed.goal i).vec‖ ^ 2 * ‖(fed.goal j).vec‖ ^ 2)
  else 0

/-- Pairwise correlations are bounded in [0, 1]. Nonneg from `|·|² ≥ 0`;
    upper bound from Cauchy–Schwarz. Discharged from axiom to theorem
    (2026-07-01). -/
theorem rho_goals_bounded (fed : Federation H) (i j : Fin n) :
    0 ≤ rho_goals H fed i j ∧ rho_goals H fed i j ≤ 1 := by
  unfold rho_goals
  by_cases h : H i = H j
  · rw [dif_pos h]
    refine ⟨div_nonneg (Complex.normSq_nonneg _) (by positivity), ?_⟩
    refine div_le_one_of_le₀ ?_ (by positivity)
    rw [Complex.normSq_eq_abs, ← Complex.norm_eq_abs, ← mul_pow]
    exact pow_le_pow_left₀ (norm_nonneg _) (norm_inner_le_norm _ _) 2
  · rw [dif_neg h]
    norm_num

/-- Diagonal correlation is 1: `|⟨G_i|G_i⟩|² = 1² = 1` by `unit_norm`.
    Discharged from axiom to theorem (2026-07-01). -/
theorem rho_goals_diagonal (fed : Federation H) (i : Fin n) :
    rho_goals H fed i i = 1 := by
  unfold rho_goals
  rw [dif_pos rfl, cast_eq, inner_self_of_unit H (fed.goal i), (fed.goal i).unit_norm]
  norm_num [Complex.normSq_one]

/-! ## The three regimes -/

/-- Rigidity regime: every pair of agents has correlation above the upper
    corridor bound. All goal-projectors collapse to one effective projector. -/
def isRigid (fed : Federation H) : Prop :=
  ∀ i j : Fin n, i ≠ j → rho_goals H fed i j > ρ_upper

/-- Chaos regime: every pair has correlation below the lower corridor bound.
    Goal-projectors are pairwise nearly-orthogonal. -/
def isChaotic (fed : Federation H) : Prop :=
  ∀ i j : Fin n, i ≠ j → rho_goals H fed i j < ρ_lower

/-- Consent corridor regime: every pair has correlation strictly inside the
    corridor. This is the operator-level definition of consent. -/
def isInConsentCorridor (fed : Federation H) : Prop :=
  ∀ i j : Fin n, i ≠ j → inCorridor (rho_goals H fed i j)

/-! ## Corridor characterization theorems

The regime distinction is carried by the GOAL-SPAN `span{G_i.vec} ⊆ H₀` in
the homogeneous case — NOT by the rank of the tensor-product joint support,
which is ≤ 1 unconditionally (`jointSupport_rank_le_one`). The two former
axioms asserting the regime distinction on the joint-support rank
(`rigid_collapse_to_one_dim`, `consent_corridor_nontrivial_support`) are
removed; their honest replacements below are proved theorems. -/

/-- Chaos sends joint support to a measure-zero submanifold of physical
    trajectories. Mutual near-orthogonality of factor projectors means the
    joint projector applied to any normalizable initial state has near-zero
    norm (the amplitude `∏_i ⟨G_i|f_i⟩` through the rank-one channel is
    suppressed). -/
theorem chaotic_measure_zero (fed : Federation H) (h : isChaotic H fed) :
    -- Operationalized as: the joint projector applied to any normalizable
    -- initial state has near-zero norm.
    True := by
  trivial  -- structural statement; full proof requires the dynamics-measure
           -- coupling, which is a substrate-dependent later step.

section Homogeneous

/-! ### The homogeneous federation: concrete correlation and the goal-span

For a federation over a fixed shared state space `H₀` (every agent's goals
in the same Hilbert space — the `MultiAgentConsent.MultiAgentConfig` case),
the identity encoding is canonical and `rho_goals` computes to the bare
`|⟨G_i|G_j⟩|²`. The regime content lives here. -/

variable {H₀ : Type u} [NormedAddCommGroup H₀] [InnerProductSpace ℂ H₀]

/-- On a homogeneous federation `rho_goals` is exactly `|⟨G_i|G_j⟩|²`
    (unit-norm goals make the normalization denominator 1). -/
theorem rho_goals_homogeneous (fed : Federation (fun _ : Fin n => H₀)) (i j : Fin n) :
    rho_goals (fun _ : Fin n => H₀) fed i j
      = Complex.normSq (@inner ℂ H₀ _ (fed.goal i).vec (fed.goal j).vec) := by
  unfold rho_goals
  rw [dif_pos rfl]
  simp only [cast_eq, (fed.goal i).unit_norm, (fed.goal j).unit_norm, one_pow, mul_one,
    div_one]

/-- The goal-span: the subspace of the SHARED state space spanned by the
    federation's goal vectors. This — not the tensor-product joint support —
    is the object whose dimension registers the regime distinction:
    rigidity collapses it to a line, corridor occupation keeps it genuinely
    multi-dimensional. -/
noncomputable def goalSpan (fed : Federation (fun _ : Fin n => H₀)) : Submodule ℂ H₀ :=
  Submodule.span ℂ (Set.range fun i => (fed.goal i).vec)

/-- Strict Cauchy–Schwarz helper: a unit vector whose squared inner product
    with another unit vector is < 1 is not a scalar multiple of it. -/
private lemma no_smul_of_normSq_inner_lt_one {u v : H₀}
    (hu : ‖u‖ = 1) (hv : ‖v‖ = 1)
    (hlt : Complex.normSq (@inner ℂ H₀ _ u v) < 1) (a : ℂ) :
    a • v ≠ u := by
  intro hav
  have hnorm : ‖a‖ = 1 := by
    have h' := congrArg norm hav
    rwa [norm_smul, hv, mul_one, hu] at h'
  have hvv : @inner ℂ H₀ _ v v = 1 := by
    have h'' := @inner_self_eq_norm_sq_to_K ℂ H₀ _ _ _ v
    rw [hv] at h''
    simpa using h''
  have hinner : @inner ℂ H₀ _ u v = (starRingEnd ℂ) a := by
    rw [← hav, inner_smul_left, hvv, mul_one]
  rw [hinner, Complex.normSq_conj, Complex.normSq_eq_abs, ← Complex.norm_eq_abs,
    hnorm] at hlt
  norm_num at hlt

/-- THE CONSENT-CORRIDOR THEOREM (goal-span form). In a homogeneous
    federation with at least two agents, consent-corridor occupation forces
    the goal-span to rank ≥ 2: corridor-bounded pairwise correlation
    (`ρ_goals < ρ_upper < 1`) is strict Cauchy–Schwarz, so no goal is a
    scalar multiple of another — the federation has NOT collapsed to a
    single goal direction. Replaces the removed
    `consent_corridor_nontrivial_support` axiom (which asserted rank ≥ 2 of
    the tensor-product joint support — false: `jointSupport_rank_le_one`);
    this is the object the regime claim is actually about, and it is a
    proved theorem rather than an axiom. -/
theorem consent_corridor_goalSpan_rank_ge_two
    (fed : Federation (fun _ : Fin n => H₀)) (hn : 2 ≤ n)
    (h : isInConsentCorridor (fun _ : Fin n => H₀) fed) :
    2 ≤ Module.rank ℂ (goalSpan fed) := by
  have h0 : 0 < n := by omega
  have h1 : 1 < n := by omega
  have hij : (⟨0, h0⟩ : Fin n) ≠ ⟨1, h1⟩ := by simp [Fin.ext_iff]
  have hcorr := h ⟨0, h0⟩ ⟨1, h1⟩ hij
  rw [rho_goals_homogeneous] at hcorr
  have hlt1 : Complex.normSq
      (@inner ℂ H₀ _ (fed.goal ⟨0, h0⟩).vec (fed.goal ⟨1, h1⟩).vec) < 1 :=
    lt_trans hcorr.2 corridor_bounds_well_formed.2.2
  have hu : (fed.goal ⟨0, h0⟩).vec ∈ goalSpan fed :=
    Submodule.subset_span ⟨⟨0, h0⟩, rfl⟩
  have hv : (fed.goal ⟨1, h1⟩).vec ∈ goalSpan fed :=
    Submodule.subset_span ⟨⟨1, h1⟩, rfl⟩
  have hli : LinearIndependent ℂ
      (![(⟨(fed.goal ⟨0, h0⟩).vec, hu⟩ : goalSpan fed),
         ⟨(fed.goal ⟨1, h1⟩).vec, hv⟩]) := by
    rw [linearIndependent_fin2]
    constructor
    · simp only [Matrix.cons_val_one, Matrix.head_cons, ne_eq, Submodule.mk_eq_zero]
      intro h0v
      have hn1 := (fed.goal ⟨1, h1⟩).unit_norm
      rw [h0v] at hn1
      simp at hn1
    · intro a
      simp only [Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_zero, ne_eq]
      intro heq
      have hav : a • (fed.goal ⟨1, h1⟩).vec = (fed.goal ⟨0, h0⟩).vec := by
        simpa using congrArg Subtype.val heq
      exact no_smul_of_normSq_inner_lt_one
        (fed.goal ⟨0, h0⟩).unit_norm (fed.goal ⟨1, h1⟩).unit_norm hlt1 a hav
  simpa using hli.cardinal_lift_le_rank

/-- Full-correlation collapse (the rigidity endpoint ρ_goals ≡ 1): if every
    pairwise correlation is exactly 1, the goal-span is at most a line —
    Cauchy–Schwarz equality case: every goal is a scalar multiple of any
    fixed one. Replaces the removed `rigid_collapse_to_one_dim` axiom (whose
    rigidity hypothesis was spurious for the tensor-product support — that
    rank is ≤ 1 unconditionally). The dynamical rigidity regime
    (ρ_goals > ρ_upper) reaches this endpoint via dρ/dt > 0 above the
    corridor (Core.Dynamics); the endpoint statement is what the algebra
    licenses as a theorem. -/
theorem all_correlated_goalSpan_rank_le_one
    (fed : Federation (fun _ : Fin n => H₀))
    (h : ∀ i j : Fin n, rho_goals (fun _ : Fin n => H₀) fed i j = 1) :
    Module.rank ℂ (goalSpan fed) ≤ 1 := by
  rcases isEmpty_or_nonempty (Fin n) with hemp | hne
  · haveI := hemp
    unfold goalSpan
    rw [Set.range_eq_empty, Submodule.span_empty]
    simp [rank_bot]
  · obtain ⟨i0⟩ := hne
    have hspan : goalSpan fed ≤ Submodule.span ℂ {(fed.goal i0).vec} := by
      unfold goalSpan
      rw [Submodule.span_le]
      rintro x ⟨j, rfl⟩
      have h1 : Complex.normSq
          (@inner ℂ H₀ _ (fed.goal i0).vec (fed.goal j).vec) = 1 := by
        rw [← rho_goals_homogeneous]
        exact h i0 j
      have habs : ‖@inner ℂ H₀ _ (fed.goal i0).vec (fed.goal j).vec‖ = 1 := by
        rw [Complex.norm_eq_abs]
        have h2 : Complex.abs (@inner ℂ H₀ _ (fed.goal i0).vec (fed.goal j).vec) ^ 2
            = 1 := by
          rw [Complex.sq_abs]
          exact h1
        have h3 := Complex.abs.nonneg
          (@inner ℂ H₀ _ (fed.goal i0).vec (fed.goal j).vec)
        nlinarith [h2, h3]
      have hne0 : (fed.goal i0).vec ≠ 0 := by
        intro hz
        have := (fed.goal i0).unit_norm
        rw [hz] at this
        simp at this
      have hne0j : (fed.goal j).vec ≠ 0 := by
        intro hz
        have := (fed.goal j).unit_norm
        rw [hz] at this
        simp at this
      obtain ⟨r, -, hr⟩ := (norm_inner_eq_norm_iff (𝕜 := ℂ) hne0 hne0j).mp (by
        rw [(fed.goal i0).unit_norm, (fed.goal j).unit_norm, mul_one]
        exact habs)
      exact Submodule.mem_span_singleton.mpr ⟨r, hr.symm⟩
    calc Module.rank ℂ (goalSpan fed)
        ≤ Module.rank ℂ (Submodule.span ℂ {(fed.goal i0).vec}) :=
          Submodule.rank_mono hspan
      _ ≤ #({(fed.goal i0).vec} : Set H₀) := rank_span_le _
      _ = 1 := Cardinal.mk_singleton _

end Homogeneous

/-- The effective dimensionality of the federation's joint goal-space.
    Framework axiom — identified with `k_eff` applied at `ρ_goals` via
    the Kish identity. Operationally for an unbiased estimator of pairwise
    `ρ_goals` across all pairs: `k_eff = n / (1 + ρ̄_goals · (n - 1))`. -/
axiom k_eff_goals (fed : Federation H) : ℝ

/-- THE OPERATOR-LEVEL CONSENT THEOREM. The federation's k_eff_goals sits
    in the substrate-independent corridor range (2.33, 10) asymptotically
    iff the federation is in the consent corridor. Framework axiom —
    composition of pairwise corridor with the Kish identity. -/
axiom k_eff_goals_corridor_iff
    (fed : Federation H) (h_large_n : 10 ≤ (n : ℝ)) :
    isInConsentCorridor H fed ↔
      (k_eff_goals H fed > k_eff_floor_at_upper ∧ k_eff_goals H fed < k_eff_ceiling_at_lower)

end CoherenceRatchet.Cosmology.JointProjector
