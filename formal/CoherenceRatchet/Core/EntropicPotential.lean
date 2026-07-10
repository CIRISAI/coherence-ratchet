/-
Core.EntropicPotential — the entropic potential of the coordination spectrum
(T-E1/T-E2 of papers/notes/entropic_action_bridge.md)

Bianconi's "Gravity from entropy" (Phys. Rev. D 111, 066001, 2025;
arXiv:2408.14391) takes as gravitational Lagrangian the quantum relative
entropy between the substrate metric g̃ and the matter-induced metric G̃:

  𝓛 = −Tr_F ln G̃g̃⁻¹ = −Σ_λ' ln λ'

Evaluated on the uniform-ρ correlation matrix C(k, ρ) behind the Kish
identity (spectrum: one eigenvalue 1 + ρ(k−1), and (k−1) copies of 1 − ρ),
this functional is closed-form:

  S(k, ρ) = −ln(1 + ρ(k−1)) − (k−1)·ln(1 − ρ)

This file proves that S is a two-pole potential whose boundary behaviors are
exactly the corridor poles:

  T-E1a  S(k, 0) = 0                        (chaos pole = the zero)
  T-E0   S(k, ρ) ≥ 0, > 0 for ρ > 0         (Klein inequality instance;
                                             relative entropy is nonnegative)
  T-E1b  S(k, ρ) → +∞ as ρ → 1⁻             (rigidity pole = the divergence;
                                             C(k,ρ) loses invertibility there)
  T-E2   S strictly increasing on [0, 1)     (monotone between the poles)
  T-E3   S(k, ρ)/k → −ln(1 − ρ) as k → ∞    (per-unit entropy density finite
                                             iff ρ < 1 — the density form of
                                             the Kish ceiling k_eff → 1/ρ)

and the dynamics link (T-E4, corollary form): the unmaintained rigidity
drift (`Dynamics.rho_drift_at_zero_maintenance`, α > 0 at M = 0) ascends S;
the unmaintained chaos exit (`Dynamics.rho_exit_chaos`, α < 0 at M = 0)
descends S toward its unique zero. Maintenance holds the system in the
interior of a potential whose poles are chaos (S = 0, no induced structure)
and rigidity (S = ∞, collapse).

SCOPE / F-11 NOTE. This is engineering-tier real analysis over a closed-form
spectrum — the relative-entropy FORM of the same spectral information the
participation form k_eff reads (Core.BaseIdentity). It grounds FORWARD
content only (a candidate potential for the forward P_ω / two-pole dynamics).
It does NOT touch, weaken, or reopen the F-11 no-go on the joint multi-rung
backward P_ω (`Cosmology.CorridorProjector.F11_joint_backward_P_omega_no_go`):
Bianconi's action is local and bulk-geometric, the class closed by T1
(geometric dilution).
-/

import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Asymptotics.Asymptotics
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import CoherenceRatchet.Core.Dynamics

namespace CoherenceRatchet.Core

open Real Filter Topology

/-- The entropic potential: Bianconi's relative-entropy Lagrangian
    −Tr ln (G g⁻¹) evaluated on the uniform-ρ correlation matrix C(k, ρ)
    (substrate = identity, induced metric = C). Closed form via the Kish
    spectrum {1 + ρ(k−1), (1 − ρ)^{×(k−1)}}. -/
noncomputable def entropicPotential (k ρ : ℝ) : ℝ :=
  -Real.log (1 + ρ * (k - 1)) - (k - 1) * Real.log (1 - ρ)

/-- T-E1a. CHAOS POLE IS THE ZERO: at ρ = 0 the induced metric equals the
    substrate metric and the relative entropy vanishes (Bianconi's vacuum
    G̃ = g̃). -/
theorem entropicPotential_at_zero (k : ℝ) : entropicPotential k 0 = 0 := by
  unfold entropicPotential
  simp

/-- T-E0 (weak form). KLEIN NONNEGATIVITY: the entropic potential is
    nonnegative on the physical domain — the scalar instance of "quantum
    relative entropy is nonnegative", via log x ≤ x − 1 on both spectral
    branches. -/
theorem entropicPotential_nonneg (k ρ : ℝ) (hk : 1 ≤ k) (hρ0 : 0 ≤ ρ)
    (hρ1 : ρ < 1) : 0 ≤ entropicPotential k ρ := by
  have hkm1 : (0:ℝ) ≤ k - 1 := by linarith
  have hd : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
  have h1 : Real.log (1 + ρ * (k - 1)) ≤ ρ * (k - 1) := by
    have := Real.log_le_sub_one_of_pos hd
    linarith
  have h2 : Real.log (1 - ρ) ≤ -ρ := by
    have := Real.log_le_sub_one_of_pos (show (0:ℝ) < 1 - ρ by linarith)
    linarith
  have h3 : (k - 1) * Real.log (1 - ρ) ≤ (k - 1) * (-ρ) :=
    mul_le_mul_of_nonneg_left h2 hkm1
  unfold entropicPotential
  nlinarith

/-- T-E0 (strict form). Away from the chaos pole the potential is strictly
    positive: any nonzero correlation writes strictly positive relative
    entropy between coordination and substrate. -/
theorem entropicPotential_pos (k ρ : ℝ) (hk : 1 < k) (hρ0 : 0 < ρ)
    (hρ1 : ρ < 1) : 0 < entropicPotential k ρ := by
  have hkm1 : (0:ℝ) < k - 1 := by linarith
  have hd : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
  have h1 : Real.log (1 + ρ * (k - 1)) ≤ ρ * (k - 1) := by
    have := Real.log_le_sub_one_of_pos hd
    linarith
  have h2 : Real.log (1 - ρ) < -ρ := by
    have h_ne : (1:ℝ) - ρ ≠ 1 := by
      intro h
      have : ρ = 0 := by linarith
      exact (ne_of_gt hρ0) this
    have := Real.log_lt_sub_one_of_pos (show (0:ℝ) < 1 - ρ by linarith) h_ne
    linarith
  have h3 : (k - 1) * Real.log (1 - ρ) < (k - 1) * (-ρ) :=
    mul_lt_mul_of_pos_left h2 hkm1
  unfold entropicPotential
  nlinarith

/-- The chaos pole is the UNIQUE zero of the potential on [0, 1): S(k, ρ) = 0
    iff ρ = 0. Combines T-E1a and strict T-E0. -/
theorem entropicPotential_eq_zero_iff (k ρ : ℝ) (hk : 1 < k)
    (hρ0 : 0 ≤ ρ) (hρ1 : ρ < 1) :
    entropicPotential k ρ = 0 ↔ ρ = 0 := by
  constructor
  · intro h
    by_contra h_ne
    have hρ_pos : 0 < ρ := lt_of_le_of_ne hρ0 (Ne.symm h_ne)
    exact absurd h (ne_of_gt (entropicPotential_pos k ρ hk hρ_pos hρ1))
  · intro h
    rw [h]
    exact entropicPotential_at_zero k

/-- T-E1b. RIGIDITY POLE IS THE DIVERGENCE: S(k, ρ) → +∞ as ρ → 1⁻. The
    correlation matrix C(k, ρ) degenerates at ρ = 1 (k_eff → 1, Kish), and
    the relative entropy diverges — Bianconi's invertibility requirement
    (arXiv:2408.14391 Eq. 12) fails exactly at collapse. -/
theorem entropicPotential_tendsto_atTop_rigidity (k : ℝ) (hk : 1 < k) :
    Tendsto (fun ρ => entropicPotential k ρ) (𝓝[<] (1:ℝ)) atTop := by
  have hkm1 : (0:ℝ) < k - 1 := by linarith
  -- 1 - ρ → 0 from the right as ρ → 1 from the left
  have h_sub : Tendsto (fun ρ : ℝ => 1 - ρ) (𝓝[<] (1:ℝ)) (𝓝[>] (0:ℝ)) := by
    rw [tendsto_nhdsWithin_iff]
    constructor
    · have h : Tendsto (fun ρ : ℝ => 1 - ρ) (𝓝 (1:ℝ)) (𝓝 (1 - 1)) :=
        tendsto_const_nhds.sub tendsto_id
      simpa using h.mono_left nhdsWithin_le_nhds
    · filter_upwards [eventually_mem_nhdsWithin] with ρ hρ
      exact Set.mem_Ioi.mpr (sub_pos.mpr hρ)
  -- log(1 - ρ) → −∞
  have h_log_bot : Tendsto (fun ρ : ℝ => Real.log (1 - ρ)) (𝓝[<] (1:ℝ)) atBot :=
    Real.tendsto_log_nhdsWithin_zero_right.comp h_sub
  -- (k − 1) · (−log(1 − ρ)) → +∞
  have h_neg_top : Tendsto (fun ρ : ℝ => -Real.log (1 - ρ)) (𝓝[<] (1:ℝ)) atTop :=
    tendsto_neg_atBot_atTop.comp h_log_bot
  have h_term2 : Tendsto (fun ρ : ℝ => (k - 1) * -Real.log (1 - ρ))
      (𝓝[<] (1:ℝ)) atTop :=
    Tendsto.const_mul_atTop hkm1 h_neg_top
  -- −log(1 + ρ(k−1)) → −log k (finite)
  have h_term1 : Tendsto (fun ρ : ℝ => -Real.log (1 + ρ * (k - 1)))
      (𝓝[<] (1:ℝ)) (𝓝 (-Real.log k)) := by
    have h_inner : Tendsto (fun ρ : ℝ => 1 + ρ * (k - 1)) (𝓝[<] (1:ℝ)) (𝓝 k) := by
      have h : Tendsto (fun ρ : ℝ => 1 + ρ * (k - 1)) (𝓝 (1:ℝ))
          (𝓝 (1 + 1 * (k - 1))) :=
        tendsto_const_nhds.add (tendsto_id.mul_const (k - 1))
      have hk_eq : 1 + 1 * (k - 1) = k := by ring
      rw [hk_eq] at h
      exact h.mono_left nhdsWithin_le_nhds
    have hk_ne : k ≠ 0 := by linarith
    exact ((Real.continuousAt_log hk_ne).tendsto.comp h_inner).neg
  -- finite + atTop = atTop
  have h_sum := h_term1.add_atTop h_term2
  refine h_sum.congr fun ρ => ?_
  unfold entropicPotential
  ring

/-- T-E2. STRICT MONOTONICITY: between the poles, S is strictly increasing
    in ρ. With T-E1a/T-E1b this makes S a Lyapunov-type potential: zero at
    chaos, divergent at rigidity, monotone between. Proof via
    dS/dρ = (k−1)·[1/(1−ρ) − 1/(1+ρ(k−1))] > 0 on (0, 1). -/
theorem entropicPotential_strictMonoOn (k : ℝ) (hk : 1 < k) :
    StrictMonoOn (fun ρ => entropicPotential k ρ) (Set.Ico (0:ℝ) 1) := by
  have hkm1 : (0:ℝ) < k - 1 := by linarith
  apply strictMonoOn_of_deriv_pos (convex_Ico 0 1)
  · -- continuity on [0, 1)
    unfold entropicPotential
    apply ContinuousOn.sub
    · apply ContinuousOn.neg
      apply ContinuousOn.log
      · exact (continuous_const.add (continuous_id.mul continuous_const)).continuousOn
      · intro ρ hρ
        have h0 : (0:ℝ) ≤ ρ := hρ.1
        have h1 : ρ < 1 := hρ.2
        have : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
        exact ne_of_gt this
    · apply ContinuousOn.mul continuousOn_const
      apply ContinuousOn.log
      · exact (continuous_const.sub continuous_id).continuousOn
      · intro ρ hρ
        have : (0:ℝ) < 1 - ρ := by linarith [hρ.2]
        exact ne_of_gt this
  · -- positive derivative on the interior (0, 1)
    intro ρ hρ
    rw [interior_Ico] at hρ
    have h0 : (0:ℝ) < ρ := hρ.1
    have h1 : ρ < 1 := hρ.2
    have hd1 : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
    have hd2 : (0:ℝ) < 1 - ρ := by linarith
    have hA : HasDerivAt (fun ρ : ℝ => 1 + ρ * (k - 1)) (k - 1) ρ := by
      simpa using ((hasDerivAt_id ρ).mul_const (k - 1)).const_add 1
    have hlogA : HasDerivAt (fun ρ : ℝ => Real.log (1 + ρ * (k - 1)))
        ((k - 1) / (1 + ρ * (k - 1))) ρ := hA.log (ne_of_gt hd1)
    have hB : HasDerivAt (fun ρ : ℝ => 1 - ρ) (-1) ρ := by
      simpa using (hasDerivAt_id ρ).const_sub 1
    have hlogB : HasDerivAt (fun ρ : ℝ => Real.log (1 - ρ)) ((-1) / (1 - ρ)) ρ :=
      hB.log (ne_of_gt hd2)
    have hS : HasDerivAt (fun ρ => entropicPotential k ρ)
        (-((k - 1) / (1 + ρ * (k - 1))) - (k - 1) * ((-1) / (1 - ρ))) ρ := by
      have h := hlogA.neg.sub (hlogB.const_mul (k - 1))
      unfold entropicPotential
      exact h
    rw [hS.deriv]
    have h_lt : 1 - ρ < 1 + ρ * (k - 1) := by nlinarith
    have h_frac : (k - 1) / (1 + ρ * (k - 1)) < (k - 1) / (1 - ρ) :=
      div_lt_div_of_pos_left hkm1 hd2 h_lt
    have h_expand : -((k - 1) / (1 + ρ * (k - 1))) - (k - 1) * ((-1) / (1 - ρ))
        = (k - 1) / (1 - ρ) - (k - 1) / (1 + ρ * (k - 1)) := by
      ring
    rw [h_expand]
    linarith

/-- T-E3. PER-UNIT ENTROPY DENSITY: S(k, ρ)/k → −ln(1 − ρ) as k → ∞. The
    density form of the Kish ceiling (`k_eff_asymptotic_ceiling`): both
    functionals of the C(k, ρ) spectrum saturate per-unit at any ρ < 1 and
    only there — the density −ln(1 − ρ) diverges exactly at the rigidity
    pole where k_eff collapses to 1. -/
theorem entropicPotential_density (ρ : ℝ) (hρ0 : 0 < ρ) (_hρ1 : ρ < 1) :
    Tendsto (fun k => entropicPotential k ρ / k) atTop
      (𝓝 (-Real.log (1 - ρ))) := by
  -- u k = 1 + ρ(k − 1) → ∞
  have hu : Tendsto (fun k : ℝ => 1 + ρ * (k - 1)) atTop atTop := by
    have h1 : Tendsto (fun k : ℝ => k - 1) atTop atTop :=
      tendsto_atTop_add_const_right atTop (-1) tendsto_id
    have h2 : Tendsto (fun k : ℝ => ρ * (k - 1)) atTop atTop :=
      Tendsto.const_mul_atTop hρ0 h1
    have h3 := tendsto_atTop_add_const_right atTop 1 h2
    refine h3.congr fun k => ?_
    ring
  -- log(u k)/u k → 0
  have h_log_div : Tendsto
      (fun k : ℝ => Real.log (1 + ρ * (k - 1)) / (1 + ρ * (k - 1)))
      atTop (𝓝 0) :=
    (Real.isLittleO_log_id_atTop.tendsto_div_nhds_zero).comp hu
  -- u k / k → ρ  (same route as `k_eff_asymptotic_ceiling`)
  have h_u_div : Tendsto (fun k : ℝ => (1 + ρ * (k - 1)) / k) atTop (𝓝 ρ) := by
    have h_inv : Tendsto (fun k : ℝ => k⁻¹) atTop (𝓝 0) := tendsto_inv_atTop_zero
    have h_scaled : Tendsto (fun k : ℝ => (1 - ρ) * k⁻¹) atTop (𝓝 0) := by
      have h := h_inv.const_mul (1 - ρ)
      simpa using h
    have h_base : Tendsto (fun k : ℝ => ρ + (1 - ρ) * k⁻¹) atTop (𝓝 ρ) := by
      have h := h_scaled.const_add ρ
      simpa using h
    refine h_base.congr' ?_
    filter_upwards [eventually_gt_atTop (0:ℝ)] with k hk
    have hk_ne : k ≠ 0 := ne_of_gt hk
    field_simp
    ring
  -- first term: log(u k)/k = (log(u k)/u k) · (u k / k) → 0 · ρ = 0
  have h_termA : Tendsto (fun k : ℝ => Real.log (1 + ρ * (k - 1)) / k)
      atTop (𝓝 0) := by
    have h_prod := h_log_div.mul h_u_div
    rw [zero_mul] at h_prod
    refine h_prod.congr' ?_
    filter_upwards [hu.eventually_gt_atTop 0, eventually_gt_atTop (0:ℝ)]
      with k huk hk
    have h_ne : (1 + ρ * (k - 1)) ≠ 0 := ne_of_gt huk
    have hk_ne : k ≠ 0 := ne_of_gt hk
    field_simp
  -- second term: ((k − 1)/k) · log(1 − ρ) → log(1 − ρ)
  have h_termB : Tendsto (fun k : ℝ => (k - 1) / k * Real.log (1 - ρ))
      atTop (𝓝 (Real.log (1 - ρ))) := by
    have h_inv : Tendsto (fun k : ℝ => k⁻¹) atTop (𝓝 0) := tendsto_inv_atTop_zero
    have h_ratio : Tendsto (fun k : ℝ => 1 - k⁻¹) atTop (𝓝 1) := by
      have h := h_inv.const_sub 1
      simpa using h
    have h_mul := h_ratio.mul_const (Real.log (1 - ρ))
    rw [one_mul] at h_mul
    refine h_mul.congr' ?_
    filter_upwards [eventually_gt_atTop (0:ℝ)] with k hk
    have hk_ne : k ≠ 0 := ne_of_gt hk
    field_simp
  -- assemble: S/k = −(log(u k)/k) − ((k−1)/k)·log(1−ρ)
  have h_sum := h_termA.neg.sub h_termB
  rw [neg_zero, zero_sub] at h_sum
  refine h_sum.congr' ?_
  filter_upwards [eventually_gt_atTop (0:ℝ)] with k hk
  have hk_ne : k ≠ 0 := ne_of_gt hk
  unfold entropicPotential
  field_simp
  ring

/-! ## T-E4 (corollary form) — the two-pole dynamics against the potential

The drift theorems of `Core.Dynamics` compose with T-E2 into the potential
reading: unmaintained rigidity drift (α > 0, M = 0) moves ρ up, and every
upward move strictly ascends S toward its divergence; the unmaintained chaos
exit (α < 0, M = 0) moves ρ down, and every downward move strictly descends
S toward its unique zero. This is the precise sense in which
`corridor_requires_maintenance` upgrades to "maintenance holds the system on
the interior of an entropic potential" — the shape of Bianconi's G-field
(a Lagrange-multiplier field with physical status, arXiv:2408.14391
Eqs. 49–50). -/

/-- T-E4a. The unmaintained rigidity drift ascends the entropic potential:
    at M = 0 with α > 0, dρ/dt > 0, and every increase of ρ within [0, 1)
    strictly increases S — the flow climbs toward the rigidity divergence. -/
theorem unmaintained_rigidity_drift_ascends_potential
    (k : ℝ) (hk : 1 < k) (ρ : ℝ) (Sp : Dynamics.SelectionPressure) (t : ℝ)
    (h_m : Dynamics.M t = 0) (h_alpha : Dynamics.α ρ Sp > 0)
    (hρ : ρ ∈ Set.Ico (0:ℝ) 1) :
    Dynamics.dρ_dt ρ Sp t > 0 ∧
      ∀ ρ' ∈ Set.Ico (0:ℝ) 1, ρ < ρ' →
        entropicPotential k ρ < entropicPotential k ρ' :=
  ⟨Dynamics.rho_drift_at_zero_maintenance ρ Sp t h_m h_alpha,
   fun ρ' hρ' hlt => entropicPotential_strictMonoOn k hk hρ hρ' hlt⟩

/-- T-E4b. The unmaintained chaos exit descends the entropic potential:
    at M = 0 with α < 0, dρ/dt < 0, and every decrease of ρ within [0, 1)
    strictly decreases S — the flow falls toward the unique zero at the
    chaos pole. -/
theorem unmaintained_chaos_drift_descends_potential
    (k : ℝ) (hk : 1 < k) (ρ : ℝ) (Sp : Dynamics.SelectionPressure) (t : ℝ)
    (h_m : Dynamics.M t = 0) (h_alpha : Dynamics.α ρ Sp < 0)
    (hρ : ρ ∈ Set.Ico (0:ℝ) 1) :
    Dynamics.dρ_dt ρ Sp t < 0 ∧
      ∀ ρ' ∈ Set.Ico (0:ℝ) 1, ρ' < ρ →
        entropicPotential k ρ' < entropicPotential k ρ :=
  ⟨Dynamics.rho_exit_chaos ρ Sp t h_m h_alpha,
   fun ρ' hρ' hlt => entropicPotential_strictMonoOn k hk hρ' hρ hlt⟩

/-! ## T-E5 — the multi-information / joint-entropy identity

The entropic potential is not only Bianconi's Lagrangian evaluated on the Kish
spectrum — it is (twice) the **Gaussian multi-information** (total correlation)
of the k-sensor array, because −Tr ln C = −ln det C and, for a multivariate
Gaussian with correlation matrix C, the multi-information is
I = −½ ln det C. Hence

  S(k, ρ) = 2·I,   and   H_joint = Σ marginals − S/2.

Three readings, one mechanized identity:
- **TRNG reading**: S/2 nats/sample is the array's joint-entropy DEFICIT vs
  independent sensors — the entropy consumed by coordination. Per-stream
  entropy certification is blind to it (the marginals of C(k,ρ) are all 1).
- **Detection reading**: since Tr C(k,ρ) = k, the KL divergence from the
  independent baseline is D(N(0,C) ‖ N(0,I)) = ½(Tr C − k − ln det C)
  = −½ ln det C = S/2 — the Chernoff–Stein exponent: S/2 nats/sample is the
  optimal per-sample discrimination information for detecting the
  coordination, so detection latency scales as ln(1/P_err)/(S/2).
- **Small-ρ sensing law** (documented, not mechanized): expanding S at ρ → 0
  gives S ≈ ½·k(k−1)·ρ². CAUTION (exp119, 2026-07-10): the k² LEVERAGE this
  seems to promise requires ρ ⊥ k, which a bounded-strength common cause does
  NOT satisfy. Measured on a 16→32-sensor GPU array, a shared resource injects
  a mode of FIXED EXCESS EIGENVALUE (λ_max − 1 ≈ 0.5, CV 4%), hence ρ̄ ∝ 1/k by
  arithmetic, hence S ∝ k^0.92 and detection latency ∝ k^−0.93 — LINEAR, not
  quadratic. What the hardware DOES confirm to 2–8% at every k is the identity
  in its heterogeneity-correct form S = ½·k(k−1)·mean(ρ²) (note mean(ρ²), not
  ρ̄²). Recovering k² requires the common-cause power to grow ∝ k.

Both Gaussian interpretations (multi-information; KL/Stein) are MODELING
COMMITMENTS documented here (the timing marginals are fat-tailed, so on real
hardware they are approximations); the mechanized content is the determinant
identity and the factor 2, plus the matrix grounding: the closed-form spectrum
this file has used throughout is here derived from the actual uniform-ρ
correlation MATRIX via the matrix determinant lemma, not assumed. -/

open Matrix in
/-- The uniform-ρ correlation matrix on k units: 1 on the diagonal, ρ off it.
    The concrete matrix behind the Kish spectrum {1 + ρ(k−1), (1−ρ)^{×(k−1)}}. -/
def kishMatrix (k : ℕ) (ρ : ℝ) : Matrix (Fin k) (Fin k) ℝ :=
  fun i j => if i = j then 1 else ρ

open Matrix in
/-- T-E5a (matrix grounding). det C(k, ρ) = (1 + ρ(k−1))·(1−ρ)^(k−1) — the
    determinant of the ACTUAL uniform-ρ matrix, via the matrix determinant
    lemma on the rank-one decomposition C = (1−ρ)·I + ρ·𝟙𝟙ᵀ. This derives the
    closed-form spectrum used throughout this file rather than assuming it. -/
theorem kishMatrix_det (k : ℕ) (hk : 1 ≤ k) (ρ : ℝ) (hρ : ρ ≠ 1) :
    (kishMatrix k ρ).det = (1 + ρ * ((k : ℝ) - 1)) * (1 - ρ) ^ (k - 1) := by
  have h1ρ : (1 : ℝ) - ρ ≠ 0 := sub_ne_zero.mpr (Ne.symm hρ)
  -- rank-one decomposition: C = (1−ρ) • (1 + col u * row v), u ≡ ρ/(1−ρ), v ≡ 1
  have decomp : kishMatrix k ρ
      = (1 - ρ) • (1 + col Unit (fun _ => ρ / (1 - ρ)) * row Unit (fun _ => (1:ℝ))) := by
    ext i j
    simp only [kishMatrix, Matrix.smul_apply, Matrix.add_apply, Matrix.one_apply,
      Matrix.mul_apply, Matrix.col_apply, Matrix.row_apply, Finset.univ_unique,
      Finset.sum_singleton, smul_eq_mul]
    split_ifs with h
    · field_simp
    · field_simp
  rw [decomp, Matrix.det_smul, Matrix.det_one_add_col_mul_row]
  have hdot : (fun _ : Fin k => (1:ℝ)) ⬝ᵥ (fun _ => ρ / (1 - ρ)) = k * (ρ / (1 - ρ)) := by
    simp [dotProduct, Finset.sum_const, nsmul_eq_mul]
  rw [hdot]
  have hcard : Fintype.card (Fin k) = k := Fintype.card_fin k
  rw [hcard]
  -- (1−ρ)^k · (1 + k·ρ/(1−ρ)) = (1 + ρ(k−1)) · (1−ρ)^(k−1)
  have hpow : (1 - ρ) ^ k = (1 - ρ) ^ (k - 1) * (1 - ρ) := by
    conv_lhs => rw [← Nat.sub_add_cancel hk]
    rw [pow_succ]
  rw [hpow]
  field_simp
  ring

open Matrix in
/-- T-E5b. The entropic potential IS −ln det of the actual correlation matrix:
    S(k, ρ) = −ln det C(k, ρ) on the physical domain. Bianconi's −Tr ln C,
    grounded in the matrix rather than the asserted spectrum. -/
theorem entropicPotential_eq_neg_log_det (k : ℕ) (hk : 1 ≤ k) (ρ : ℝ)
    (hρ0 : 0 ≤ ρ) (hρ1 : ρ < 1) :
    entropicPotential (k : ℝ) ρ = -Real.log (kishMatrix k ρ).det := by
  rw [kishMatrix_det k hk ρ (ne_of_lt hρ1)]
  have hk1 : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  have h1 : (0:ℝ) < 1 + ρ * ((k : ℝ) - 1) := by nlinarith
  have h2 : (0:ℝ) < 1 - ρ := by linarith
  rw [Real.log_mul (ne_of_gt h1) (ne_of_gt (pow_pos h2 _)), Real.log_pow]
  have hcast : ((k - 1 : ℕ) : ℝ) = (k : ℝ) - 1 := by
    rw [Nat.cast_sub hk, Nat.cast_one]
  rw [hcast]
  unfold entropicPotential
  ring

/-- Gaussian multi-information (total correlation) of the uniform-ρ array,
    in closed form: I = −½ ln det C(k, ρ). For a multivariate Gaussian with
    correlation matrix C this is the KL divergence from the product of its
    marginals; since Tr C(k,ρ) = k it also equals D(N(0,C) ‖ N(0,I)), the
    Chernoff–Stein detection exponent (see section docstring). Stated over
    real k with rpow, matching `entropicPotential`. -/
noncomputable def gaussianMultiInformation (k ρ : ℝ) : ℝ :=
  -(1/2) * Real.log ((1 + ρ * (k - 1)) * (1 - ρ) ^ (k - 1))

/-- T-E5c. THE IDENTITY: S = 2·I — the entropic potential is twice the
    Gaussian multi-information. Equivalently: the array's joint-entropy
    deficit (and its Stein detection exponent) is exactly S/2 nats/sample.
    One spectrum, three functionals: participation (k_eff), relative entropy
    (S), information (I) — and the last two differ by exactly the factor 2. -/
theorem entropicPotential_eq_two_mul_multiInformation (k ρ : ℝ)
    (hk : 1 ≤ k) (hρ0 : 0 ≤ ρ) (hρ1 : ρ < 1) :
    entropicPotential k ρ = 2 * gaussianMultiInformation k ρ := by
  unfold entropicPotential gaussianMultiInformation
  have h1 : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
  have h2 : (0:ℝ) < 1 - ρ := by linarith
  rw [Real.log_mul (ne_of_gt h1) (ne_of_gt (Real.rpow_pos_of_pos h2 _)),
    Real.log_rpow h2]
  ring

end CoherenceRatchet.Core
