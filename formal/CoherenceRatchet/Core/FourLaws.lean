/-
Core.FourLaws — the Lean pass on the "four laws of coordination thermodynamics"
(papers/notes/four_laws.md), run as a TAUTOLOGY AUDIT.

The program's own discipline (memory: tautology-vs-commitment) says an identity
masquerading as a law is a kill: elegant algebra is the shallowest commitment;
the test of depth is "could it have been otherwise." This file sticks the knife
into each of the four laws — formalizing what is provable, and LABELLING what
comes out as an identity (zero empirical content) versus a theorem-given-model
versus a genuine empirical claim. The full verdict table is in
papers/notes/lean_knives_report.md.

Knives, and where each lands:

  K1  FIRST-LAW TAUTOLOGY (the sharpest).  Total correlation obeys an exact
      GROUP CHAIN RULE: TC(all) = TC(between groups) + Σ TC(within group). We
      prove it here for ARBITRARY reals standing in for the entropies — it needs
      neither Gaussianity nor determinants nor even that the numbers are
      entropies. It is telescoping (`tc_group_chain_rule`). VERDICT: the STATIC
      "the books balance across the rungs" reading of the first law (X = 1 as a
      decomposition identity) is a TAUTOLOGY. The non-tautological first law is
      the DYNAMIC conservation claim, stated precisely in `firstLawDynamicContent`
      (comment): dTC_total/dt = 0 under the specific virialization dynamics — a
      claim no chain rule guarantees, and one that structure growth generically
      violates. four_laws.md must demote the static reading.

  K2  THE COUPLING IDENTITY  H_joint = Σ H_marginal − I  (`coupling_identity`).
      Load-bearing for the genus claim ("the classical books contain the
      coordination books"). It is the DEFINITION of I rearranged — an identity,
      LABELLED as such. It supports the coupling framing and earns no empirical
      weight. The Gaussian instance (I = −½ ln det C) is already mechanized in
      `Core.EntropicPotential` (`gaussianMultiInformation`, `kishMatrix_det`).

  K3  RESTRICTED SECOND LAW.  Full DPI (multi-information non-increasing under
      local processing) is BLOCKED: it needs Fischer's inequality
      det Σ ≤ Π det(principal blocks) (equivalently ln-det superadditivity /
      Oppenheim), which is ABSENT from mathlib v4.14.0 — recorded as a named
      open step (`RestrictedSecondLaw`). What IS provable now, and proved here,
      is the equicorrelation fragment: adding a coordinated unit never decreases
      S (`entropicPotential_strictMono_k`, `add_unit_increases_S`) — the first
      mechanized second-law fragment, THEOREM-GIVEN-MODEL (Kish family).

  K4  THE JARLSKOG BOUND.  |J| ≤ J_max(angles) with J_max → 0 at the aligned
      (no-mixing) pole (`abs_jarlskog_le_max`, `jarlskogMax_zero_at_no_mixing`).
      Pure trigonometry; the flavor-side instance of "coordination caps
      irreversibility" (CP violation is bounded by mixing and vanishes when the
      mixing is rigid). THEOREM.

SCOPE / F-11. Forward, engineering-tier content: finite algebra, real analysis
on a closed-form spectrum, and trigonometric bounds. Touches nothing about the
joint multi-rung backward P_ω (`Cosmology.CorridorProjector`).
-/

import CoherenceRatchet.Core.EntropicPotential
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

namespace CoherenceRatchet.Core

open Real Finset

/-! ## K1 — the first-law tautology knife: the total-correlation group chain rule

Total correlation (multi-information) of a family of variables is
    TC = (Σ marginal entropies) − (joint entropy).
Partition the variables into groups. Watanabe's group chain rule states
    TC(all) = TC(between groups) + Σ_g TC(within group g).
We prove it below with the entropies replaced by ARBITRARY reals `hMarg`,
`hGroup`, `hTotal`. Nothing about the proof uses that they are entropies, that
the distribution is Gaussian, or that any determinant identity holds: it is pure
telescoping. THAT is the knife — an accounting identity that balances for any
numbers whatsoever has no empirical content, exactly as "assets = liabilities +
equity" is bookkeeping, not a law of economics. -/

variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq κ]

/-- The set of variables assigned to group `g` by `grp`. -/
def groupMembers (grp : ι → κ) (g : κ) : Finset ι :=
  Finset.univ.filter (fun i => grp i = g)

/-- Within-group total correlation of group `g`: (Σ marginal entropies of its
    members) − (its own joint entropy). -/
def TCwithin (grp : ι → κ) (hMarg : ι → ℝ) (hGroup : κ → ℝ) (g : κ) : ℝ :=
  (∑ i ∈ groupMembers grp g, hMarg i) - hGroup g

/-- Between-group total correlation: (Σ group joint entropies) − (grand joint
    entropy). The coordination "credited at the inter-group rung." -/
def TCbetween (hGroup : κ → ℝ) (hTotal : ℝ) : ℝ :=
  (∑ g, hGroup g) - hTotal

/-- Grand total correlation: (Σ all marginal entropies) − (grand joint entropy). -/
def TCtotal (hMarg : ι → ℝ) (hTotal : ℝ) : ℝ :=
  (∑ i, hMarg i) - hTotal

/-- **K1 — THE FIRST-LAW TAUTOLOGY, EXPOSED.** The total-correlation group chain
    rule holds for ARBITRARY reals in the entropy slots:
        TC(all) = TC(between) + Σ_g TC(within g).
    Proof: `∑_g (∑_{members of g} hMarg) = ∑_all hMarg` (fiberwise) and the
    per-group joint entropies telescope. No Gaussianity, no determinant, no
    positivity — the accounting balances by definition. Therefore the STATIC
    "the books balance across the rungs" reading of the first law is an identity,
    not a prediction: it could not have been otherwise. -/
theorem tc_group_chain_rule (grp : ι → κ) (hMarg : ι → ℝ) (hGroup : κ → ℝ)
    (hTotal : ℝ) :
    TCtotal hMarg hTotal
      = TCbetween hGroup hTotal + ∑ g, TCwithin grp hMarg hGroup g := by
  unfold TCtotal TCbetween TCwithin groupMembers
  rw [Finset.sum_sub_distrib, Finset.sum_fiberwise Finset.univ grp hMarg]
  ring

/-! The dynamic (non-tautological) first law — stated for the record, not
    formalizable as an identity because it is contingent on the dynamics.

    `firstLawDynamicContent`.  Let `t ↦ TC_within(t)`, `t ↦ TC_between(t)` be the
    within-halo and inter-halo total correlations of the matter field along the
    virialization flow, with the partition into halos itself evolving. The
    exchange rate is  X := −ΔTC_between / ΔTC_within  over a virialization epoch.
    The chain rule gives, at every instant and for the current partition,
        TC_total = TC_between + Σ TC_within,
    hence  ΔTC_total = ΔTC_between + Σ ΔTC_within.  The claim "X = 1" is exactly
    "ΔTC_between = −Σ ΔTC_within", i.e. **ΔTC_total = 0**: total coordination of
    the matter field is CONSERVED across the rung conversion. THIS is the
    empirical content — and it is not guaranteed by any chain rule. Gravitational
    clustering generically GROWS total correlation (structure forms), so the
    naive global form is expected to fail; the honest claim is the
    partition-relative one, that the coordination DEBITED from within-halo phase
    space is CREDITED, to within X = 1, at the inter-halo rung over the specific
    epoch — with the partition-change term made explicit. Kill: a precise
    X robustly ≠ 1 (the toy measurement X = 0.85 ± 0.30 is consistent with 1 but
    does not yet discriminate). See lean_knives_report.md §K1. -/

/-! ## K2 — the coupling identity  H_joint = Σ H_marginal − I

The genus/species claim ("the classical entropy books contain the coordination
books as an unitemized line-item") rests on H_joint = Σ H_marginal − I. This is
the definition of the multi-information I rearranged: an identity. We state and
LABEL it. It supports the coupling FRAMING; it earns no empirical weight (rule
2). The Gaussian realization I = −½ ln det C is already mechanized in
`Core.EntropicPotential`. -/

/-- **K2 — THE COUPLING IDENTITY (labelled: identity, zero empirical content).**
    With the multi-information defined as `I = (Σ marginals) − joint`, the joint
    entropy is `joint = (Σ marginals) − I`. This is the sole load-bearing algebra
    under "the classical books contain the coordination books": true by
    definition, hence bookkeeping, not physics. -/
theorem coupling_identity (hMarg : ι → ℝ) (hJoint I : ℝ)
    (hI : I = (∑ i, hMarg i) - hJoint) :
    hJoint = (∑ i, hMarg i) - I := by
  rw [hI]; ring

/-- The same identity read on the mechanized Gaussian instance: for the
    equicorrelation (Kish) array `Core.EntropicPotential` already establishes
    `S = 2·I` with `I = gaussianMultiInformation`. Here we record the coupling
    form directly: the array's joint-entropy DEFICIT `S/2` is exactly the
    multi-information, so `H_joint = Σ H_marginal − S/2`. This ties K2's abstract
    identity to a concrete correlation matrix (no new empirical content — it is
    the same identity on a named model). -/
theorem coupling_identity_gaussian (k ρ : ℝ) (hk : 1 ≤ k) (hρ0 : 0 ≤ ρ)
    (hρ1 : ρ < 1) :
    gaussianMultiInformation k ρ = entropicPotential k ρ / 2 := by
  rw [entropicPotential_eq_two_mul_multiInformation k ρ hk hρ0 hρ1]; ring

/-! ## K3 — the restricted second law

Full DPI is blocked. The equicorrelation fragment is provable and proved:
adding a coordinated unit never decreases the coordination potential S. This is
the first mechanized second-law fragment — a THEOREM-GIVEN-MODEL (the Kish
family), the honest label. -/

/-- **K3 — RESTRICTED SECOND LAW (equicorrelation fragment).** On the Kish family
    the entropic potential is STRICTLY INCREASING in the number of units `k` at
    any fixed coordination `ρ ∈ (0,1)`: adding a coordinated unit strictly
    increases total coordination. Proof: dS/dk = −ρ/(1+ρ(k−1)) − ln(1−ρ) > 0,
    because −ln(1−ρ) > ρ (strict log bound) ≥ ρ/(1+ρ(k−1)) (denominator ≥ 1). -/
theorem entropicPotential_strictMono_k (ρ : ℝ) (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    StrictMonoOn (fun k => entropicPotential k ρ) (Set.Ici (1:ℝ)) := by
  apply strictMonoOn_of_deriv_pos (convex_Ici 1)
  · -- continuity on [1, ∞)
    unfold entropicPotential
    apply ContinuousOn.sub
    · apply ContinuousOn.neg
      apply ContinuousOn.log
      · exact (continuous_const.add
          (continuous_const.mul (continuous_id.sub continuous_const))).continuousOn
      · intro k hk
        have hk1 : (1:ℝ) ≤ k := hk
        have : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
        exact ne_of_gt this
    · exact ((continuous_id.sub continuous_const).mul continuous_const).continuousOn
  · -- positive derivative on the interior (1, ∞)
    intro k hk
    rw [interior_Ici] at hk
    have hk1 : (1:ℝ) < k := hk
    have hd1 : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
    have hd2 : (0:ℝ) < 1 - ρ := by linarith
    -- d/dk of −log(1 + ρ(k−1))
    have hA : HasDerivAt (fun k : ℝ => 1 + ρ * (k - 1)) ρ k := by
      simpa using (((hasDerivAt_id k).sub_const 1).const_mul ρ).const_add 1
    have hlogA : HasDerivAt (fun k : ℝ => Real.log (1 + ρ * (k - 1)))
        (ρ / (1 + ρ * (k - 1))) k := hA.log (ne_of_gt hd1)
    -- d/dk of (k−1)·log(1−ρ)
    have hB : HasDerivAt (fun k : ℝ => (k - 1) * Real.log (1 - ρ))
        (Real.log (1 - ρ)) k := by
      simpa using ((hasDerivAt_id k).sub_const 1).mul_const (Real.log (1 - ρ))
    have hS : HasDerivAt (fun k => entropicPotential k ρ)
        (-(ρ / (1 + ρ * (k - 1))) - Real.log (1 - ρ)) k := by
      have h := hlogA.neg.sub hB
      unfold entropicPotential
      exact h
    rw [hS.deriv]
    -- −ln(1−ρ) > ρ ≥ ρ/(1+ρ(k−1))
    have hlog : Real.log (1 - ρ) < -ρ := by
      have h_ne : (1:ℝ) - ρ ≠ 1 := by intro h; nlinarith
      have := Real.log_lt_sub_one_of_pos hd2 h_ne
      linarith
    have hfrac : ρ / (1 + ρ * (k - 1)) ≤ ρ := by
      rw [div_le_iff₀ hd1]
      nlinarith [mul_pos hρ0 (mul_pos hρ0 (show (0:ℝ) < k - 1 by linarith))]
    linarith

/-- **K3 corollary — the discrete "add a unit" second law.** For `1 ≤ k` and
    `ρ ∈ (0,1)`, `S(k, ρ) < S(k+1, ρ)`: appending one coordinated unit strictly
    increases the coordination potential. The mechanized second-law fragment in
    its physical (discrete) form, on the equicorrelation model. -/
theorem add_unit_increases_S (k ρ : ℝ) (hk : 1 ≤ k) (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    entropicPotential k ρ < entropicPotential (k + 1) ρ :=
  entropicPotential_strictMono_k ρ hρ0 hρ1 hk (by simp; linarith) (by linarith)

/-- **K3 open step — the GENERAL data-processing inequality (BLOCKED).** The full
    second law (multi-information non-increasing under local processing; and its
    subset-monotonicity corollary TC(X_{A∪B}) ≥ TC(X_A) for general Gaussian TC)
    reduces, via the chain rule `tc_group_chain_rule`, to the nonnegativity of
    every inter-group term I(A;B) ≥ 0 — equivalently to **Fischer's inequality**
    det Σ ≤ Π_g det(principal block Σ_g) for positive-definite Σ (equivalently
    ln-det superadditivity / Oppenheim). This inequality is ABSENT from mathlib
    v4.14.0 (no `Matrix.det_le_prod_diagonal`, no Hadamard/Fischer determinant
    bound; `Mathlib.LinearAlgebra.Matrix.PosDef` has only `det_pos`). This record
    marks the gap precisely; it is NOT a claim that DPI is proved. -/
structure RestrictedSecondLaw where
  /-- PROVED here: the equicorrelation fragment (adding a unit increases S). -/
  equicorrelation_fragment_proved : True
  /-- PROVED here: the chain-rule reduction of subset-monotonicity to
      inter-group nonnegativity (`tc_group_chain_rule`). -/
  chain_rule_reduction_proved : True
  /-- OPEN / BLOCKED: the inter-group term nonnegativity I(A;B) ≥ 0 for general
      Gaussian TC needs Fischer's inequality det Σ ≤ Π det(blocks), absent from
      mathlib v4.14.0. This is the single missing lemma. -/
  fischer_inequality_missing : True
  /-- Consequently the GENERAL DPI is an open Lean step, not a theorem. -/
  general_dpi_open : True

/-- The restricted-second-law record is inhabited: fragment proved, general DPI
    open on the named missing lemma. -/
def restricted_second_law : RestrictedSecondLaw := ⟨trivial, trivial, trivial, trivial⟩

/-! ## K4 — the Jarlskog bound (flavor instance: coordination caps irreversibility)

The Jarlskog invariant J is the reparametrization-invariant measure of CP
violation (T-symmetry breaking / irreversibility) in the quark mixing matrix. In
the standard parametrization
    J = c₁₂ s₁₂ c₂₃ s₂₃ c₁₃² s₁₃ sin δ,
with cᵢⱼ = cos θᵢⱼ, sᵢⱼ = sin θᵢⱼ. We prove |J| ≤ J_max(angles) := the same
product with |sin δ| dropped, and that J_max → 0 at the aligned (no-mixing) pole
θᵢⱼ → 0. This pins, at Lean strength, "coordination (mixing) caps irreversibility
(CP violation), and irreversibility vanishes where the mixing is rigid." -/

/-- The Jarlskog invariant in the standard parametrization. -/
noncomputable def jarlskog (θ12 θ23 θ13 δ : ℝ) : ℝ :=
  cos θ12 * sin θ12 * cos θ23 * sin θ23 * (cos θ13) ^ 2 * sin θ13 * sin δ

/-- The angle-only Jarlskog magnitude bound (the `|sin δ| ≤ 1` envelope). -/
noncomputable def jarlskogMax (θ12 θ23 θ13 : ℝ) : ℝ :=
  cos θ12 * sin θ12 * cos θ23 * sin θ23 * (cos θ13) ^ 2 * sin θ13

/-- `J_max ≥ 0` on the physical octant `[0, π/2]³`: a product of nonnegative sines
    and cosines. -/
theorem jarlskogMax_nonneg {θ12 θ23 θ13 : ℝ}
    (h12 : θ12 ∈ Set.Icc 0 (π/2)) (h23 : θ23 ∈ Set.Icc 0 (π/2))
    (h13 : θ13 ∈ Set.Icc 0 (π/2)) : 0 ≤ jarlskogMax θ12 θ23 θ13 := by
  have hpi : (0:ℝ) ≤ π/2 := by positivity
  have hc12 : 0 ≤ cos θ12 := cos_nonneg_of_mem_Icc ⟨by linarith [h12.1], h12.2⟩
  have hs12 : 0 ≤ sin θ12 := sin_nonneg_of_mem_Icc ⟨h12.1, by linarith [h12.2, pi_pos]⟩
  have hc23 : 0 ≤ cos θ23 := cos_nonneg_of_mem_Icc ⟨by linarith [h23.1], h23.2⟩
  have hs23 : 0 ≤ sin θ23 := sin_nonneg_of_mem_Icc ⟨h23.1, by linarith [h23.2, pi_pos]⟩
  have hc13 : 0 ≤ cos θ13 := cos_nonneg_of_mem_Icc ⟨by linarith [h13.1], h13.2⟩
  have hs13 : 0 ≤ sin θ13 := sin_nonneg_of_mem_Icc ⟨h13.1, by linarith [h13.2, pi_pos]⟩
  unfold jarlskogMax
  have hc13sq : 0 ≤ (cos θ13) ^ 2 := sq_nonneg _
  positivity

/-- **K4 — THE JARLSKOG BOUND.** `|J| ≤ J_max(angles)` on the physical octant:
    the CP-violation magnitude is bounded by the mixing-angle envelope, saturated
    only at maximal CP phase `|sin δ| = 1`. Proof: `|J| = J_max · |sin δ|` and
    `|sin δ| ≤ 1` with `J_max ≥ 0`. -/
theorem abs_jarlskog_le_max {θ12 θ23 θ13 δ : ℝ}
    (h12 : θ12 ∈ Set.Icc 0 (π/2)) (h23 : θ23 ∈ Set.Icc 0 (π/2))
    (h13 : θ13 ∈ Set.Icc 0 (π/2)) :
    |jarlskog θ12 θ23 θ13 δ| ≤ jarlskogMax θ12 θ23 θ13 := by
  have hmax : 0 ≤ jarlskogMax θ12 θ23 θ13 := jarlskogMax_nonneg h12 h23 h13
  have hfactor : jarlskog θ12 θ23 θ13 δ = jarlskogMax θ12 θ23 θ13 * sin δ := by
    unfold jarlskog jarlskogMax; ring
  rw [hfactor, abs_mul, abs_of_nonneg hmax]
  calc jarlskogMax θ12 θ23 θ13 * |sin δ|
      ≤ jarlskogMax θ12 θ23 θ13 * 1 :=
        mul_le_mul_of_nonneg_left (abs_sin_le_one δ) hmax
    _ = jarlskogMax θ12 θ23 θ13 := by ring

/-- **K4 — THE ALIGNED POLE.** `J_max = 0` whenever any mixing angle vanishes
    (θᵢⱼ = 0 ⇒ sin θᵢⱼ = 0): at the no-mixing / rigid-alignment pole the CP
    violation is forced to zero. The coordination analog: irreversibility cannot
    be posted where the coordinating structure (mixing) is trivial. -/
theorem jarlskogMax_zero_at_no_mixing (θ12 θ23 θ13 : ℝ)
    (h : θ12 = 0 ∨ θ23 = 0 ∨ θ13 = 0) : jarlskogMax θ12 θ23 θ13 = 0 := by
  unfold jarlskogMax
  rcases h with h | h | h <;> subst h <;> simp

/-- **K4 — the opposite (maximal-mixing) endpoint** also kills J via the 1–3
    cosine: at `θ13 = π/2`, `cos θ13 = 0`, so `J_max = 0`. Together with
    `jarlskogMax_zero_at_no_mixing`, the CP violation vanishes at BOTH ends of
    each mixing angle's range — it lives only strictly between the poles, the
    same corridor shape the whole program reads. -/
theorem jarlskogMax_zero_at_max_13mixing (θ12 θ23 : ℝ) :
    jarlskogMax θ12 θ23 (π/2) = 0 := by
  unfold jarlskogMax
  rw [cos_pi_div_two]; ring

end CoherenceRatchet.Core
