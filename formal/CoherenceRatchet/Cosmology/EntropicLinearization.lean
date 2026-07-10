/-
Cosmology.EntropicLinearization — the orthogonality theorem as a linearization limit

FORWARD CONTENT (F-11 discipline). Everything in this file is forward-tier: it
concerns the forward soft P_ω (the ρ_ss steady state) and the entropic potential
S(k, ρ) of `Core.EntropicPotential`. It does NOT touch, weaken, or reopen the
F-11 no-go on the joint multi-rung backward P_ω
(`Cosmology.CorridorProjector.F11_joint_backward_P_omega_no_go`). No backward
operator is constructed, asserted, or needed below.

-------------------------------------------------------------------------------
THE THESIS, AND WHAT IS HONESTLY PROVABLE

Bianconi's entropic action (arXiv:2408.14391, Eqs. 45–47) reduces EXACTLY to
Einstein–Hilbert with ZERO cosmological constant in the low-coupling limit
(α', β' ≪ 1). The lake separately proves an orthogonality theorem
(`CoherenceRatchet.CMBOrthogonality.framework_cmb_power_eq_lcdm`): the soft
post-selection operator P_ω leaves the bulk CMB power spectrum exactly
invariant, so the framework predicts exactly ΛCDM for the CMB.

The tempting claim is "these are the same statement". They are NOT, and this
file does not pretend otherwise. Read the actual hypotheses of the
orthogonality theorem:

    theorem framework_cmb_power_eq_lcdm {Ω : Type*}
        (E : (Ω → ℝ) → ℝ) (w S : Ω → ℝ)
        (indep : E (fun x => w x * S x) = E w * E S) (hw : E w ≠ 0) :
        E (fun x => w x * S x) / E w = E S

`E` is an arbitrary functional (not even assumed linear); `w` and `S` are
arbitrary. The entire physical content sits in the hypothesis `indep`, and the
conclusion is EXACT AT EVERY COUPLING β — there is no limit being taken. A
linearization statement is asymptotic (deviation → 0 as coupling → 0). So:

  * The orthogonality theorem is NOT literally a linearization limit.
  * `participation_scale_invariant` (Part A of that file, a real theorem) and
    `pomega_preserves_power` (Part B, one line of algebra from `indep`) are not
    formally connected there: nothing says `w` factors through `participation`.

What IS honestly provable, and is proved below, is a TWO-SECTOR statement that
does the work the thesis wanted:

  POWER SECTOR — deviation is exactly zero, at every coupling.
      Because the post-selection weight is a function of `participation`, which
      is scale-invariant, the weight is constant along the power ray. Formalized
      here as `entropicWeight_comp_participation_scale_invariant` and
      `shape_weight_preserves_power` — the missing bridge between Parts A and B
      of `CMBOrthogonality`, which shows the ONLY unproved input is `indep`
      (Gaussian shape ⊥ scale, Fisher; cited, not re-proved).

  SHAPE SECTOR — deviation is second order in the coupling ρ.
      The substrate ρ = 0 is a STATIONARY point of the entropic potential:
      S(k, 0) = 0 and S'(k, 0) = 0 (T-L1). Hence there is no first-order
      deviation, and the leading term is quadratic with an exact coefficient,
      S(k, ρ)/ρ² → k(k−1)/2 (T-L2). The induced post-selection weight inherits
      this: 1 − exp(−β S) is also second order, with coefficient β·k(k−1)/2
      (T-L3).

Together these are the framework's exact analogue of Bianconi's Eqs. 45–47.
"Zero cosmological constant at low coupling" is, on her side, the statement that
the vacuum G̃ = g̃ is a stationary point of the relative-entropy action, so no
term survives at first order in the coupling. T-L1 is literally that statement
for S(k, ρ): the chaos pole is not merely the zero of the potential (T-E1a,
already proved) but its CRITICAL point. That is what upgrades the orthogonality
theorem from a fence ("we happen not to deviate") to a mechanism ("the deviation
is a second-order entropic quantity whose first-order term vanishes because the
substrate extremizes the action").

WHAT REMAINS INTERPRETATION. That the CMB weight `w = exp(−β H_sum)` is the
entropic weight of the coordination spectrum — i.e. that `H_sum` is (a
reparametrisation of) `S(k, ρ_ℓ)` summed over multipoles — is a MODELLING
COMMITMENT, recorded in `OrthogonalityIsLinearization` below, not a theorem.
What is a theorem is that ANY weight factoring through `participation` (which
the entropic weight does, since ρ_ℓ is read off the participation ratio via the
Kish inversion `kishRhoOfParticipation`) is power-orthogonal.
-------------------------------------------------------------------------------
-/

import CoherenceRatchet.Core.EntropicPotential
import CoherenceRatchet.CMBOrthogonality
import Mathlib.Analysis.Calculus.LHopital
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

namespace CoherenceRatchet.Cosmology.EntropicLinearization

open Real Filter Topology Set
open CoherenceRatchet.Core
open CoherenceRatchet.CMBOrthogonality

/-! ## 0. The weak-coupling predicates

`ρ` is the coordination coupling: the uniform correlation of the coordinating
units. `ρ = 0` is the substrate (Bianconi's vacuum `G̃ = g̃`), `ρ → 1⁻` the
rigidity pole. A "deviation functional" `D` measures how far the coordinated
system departs from the substrate. -/

/-- WEAK-COUPLING LIMIT. The deviation vanishes at the substrate and vanishes
    continuously as the coupling is switched off. This is the bare form of
    Bianconi's "reduces to Einstein–Hilbert at low coupling": at zero coupling
    there is nothing to see. -/
structure LowCouplingLimit (D : ℝ → ℝ) : Prop where
  /-- At the substrate the deviation is exactly zero (`G̃ = g̃`). -/
  vanishes_at_substrate : D 0 = 0
  /-- Switching the coupling off drives the deviation to zero. -/
  tendsto_zero : Tendsto D (𝓝[>] 0) (𝓝 0)

/-- SECOND-ORDER DEVIATION. The strong form, and the one that carries the
    mechanism: the substrate is not merely a zero of the deviation but a
    STATIONARY point of it, so the deviation has no first-order term and its
    leading behaviour is `c · ρ²`.

    This is the precise sense in which "the low-coupling limit has zero
    cosmological constant": a nonzero `D'(0)` would be exactly a term linear in
    the coupling surviving the limit. -/
structure SecondOrderDeviation (D : ℝ → ℝ) (c : ℝ) : Prop where
  /-- At the substrate the deviation is exactly zero. -/
  vanishes_at_substrate : D 0 = 0
  /-- THE SUBSTRATE IS A CRITICAL POINT: no first-order deviation. -/
  stationary_at_substrate : HasDerivAt D 0 0
  /-- The exact quadratic coefficient. -/
  curvature_limit : Tendsto (fun ρ => D ρ / ρ ^ 2) (𝓝[>] 0) (𝓝 c)

/-- A second-order deviation is a weak-coupling limit. (The stationarity gives
    continuity at the substrate, hence the limit.) -/
theorem SecondOrderDeviation.toLowCouplingLimit {D : ℝ → ℝ} {c : ℝ}
    (h : SecondOrderDeviation D c) : LowCouplingLimit D where
  vanishes_at_substrate := h.vanishes_at_substrate
  tendsto_zero := by
    have hc : Tendsto D (𝓝 0) (𝓝 (D 0)) := h.stationary_at_substrate.continuousAt.tendsto
    rw [h.vanishes_at_substrate] at hc
    exact hc.mono_left nhdsWithin_le_nhds

/-! ## 1. The first two derivatives of the entropic potential

`S(k, ρ) = −ln(1 + ρ(k−1)) − (k−1)·ln(1 − ρ)`, so

  `S'(k, ρ)  = (k−1)/(1−ρ) − (k−1)/(1 + ρ(k−1))`
  `S''(k, ρ) = (k−1)/(1−ρ)² + (k−1)²/(1 + ρ(k−1))²`

At the substrate `ρ = 0` these are `0` and `k(k−1)` respectively — the two facts
that carry the whole file. -/

/-- First derivative of the entropic potential in `ρ`. -/
noncomputable def entropicPotentialDeriv (k ρ : ℝ) : ℝ :=
  (k - 1) / (1 - ρ) - (k - 1) / (1 + ρ * (k - 1))

/-- Second derivative of the entropic potential in `ρ`. -/
noncomputable def entropicPotentialDeriv2 (k ρ : ℝ) : ℝ :=
  (k - 1) / (1 - ρ) ^ 2 + (k - 1) ^ 2 / (1 + ρ * (k - 1)) ^ 2

theorem hasDerivAt_entropicPotential (k ρ : ℝ) (h1 : 1 - ρ ≠ 0)
    (h2 : 1 + ρ * (k - 1) ≠ 0) :
    HasDerivAt (entropicPotential k) (entropicPotentialDeriv k ρ) ρ := by
  have hA : HasDerivAt (fun x : ℝ => 1 + x * (k - 1)) (k - 1) ρ := by
    simpa using ((hasDerivAt_id ρ).mul_const (k - 1)).const_add 1
  have hlogA : HasDerivAt (fun x : ℝ => Real.log (1 + x * (k - 1)))
      ((k - 1) / (1 + ρ * (k - 1))) ρ := hA.log h2
  have hB : HasDerivAt (fun x : ℝ => 1 - x) (-1) ρ := by
    simpa using (hasDerivAt_id ρ).const_sub 1
  have hlogB : HasDerivAt (fun x : ℝ => Real.log (1 - x)) ((-1) / (1 - ρ)) ρ :=
    hB.log h1
  have h := hlogA.neg.sub (hlogB.const_mul (k - 1))
  have hfun : (fun x : ℝ => -Real.log (1 + x * (k - 1)) - (k - 1) * Real.log (1 - x))
      = entropicPotential k := rfl
  rw [hfun] at h
  convert h using 1
  unfold entropicPotentialDeriv
  field_simp
  ring

theorem hasDerivAt_entropicPotentialDeriv (k ρ : ℝ) (h1 : 1 - ρ ≠ 0)
    (h2 : 1 + ρ * (k - 1) ≠ 0) :
    HasDerivAt (entropicPotentialDeriv k) (entropicPotentialDeriv2 k ρ) ρ := by
  have hB : HasDerivAt (fun x : ℝ => 1 - x) (-1) ρ := by
    simpa using (hasDerivAt_id ρ).const_sub 1
  have hA : HasDerivAt (fun x : ℝ => 1 + x * (k - 1)) (k - 1) ρ := by
    simpa using ((hasDerivAt_id ρ).mul_const (k - 1)).const_add 1
  have hq1 := (hasDerivAt_const ρ (k - 1)).div hB h1
  have hq2 := (hasDerivAt_const ρ (k - 1)).div hA h2
  have h := hq1.sub hq2
  have hfun : (fun x : ℝ => (k - 1) / (1 - x) - (k - 1) / (1 + x * (k - 1)))
      = entropicPotentialDeriv k := rfl
  rw [hfun] at h
  convert h using 1
  unfold entropicPotentialDeriv2
  field_simp
  ring

/-! ## 2. T-L1 — the substrate is a CRITICAL point of the entropic potential

This is the load-bearing new theorem. `Core.EntropicPotential` proved
`S(k, 0) = 0` (T-E1a: the chaos pole is the zero). Here: the chaos pole is also
the STATIONARY point. No hypothesis on `k` is needed — at `ρ = 0` both spectral
branches are at their regular value `1`.

Physically: the first-order response of the entropic action to switching on
coordination is identically zero. Any deviation from the substrate theory is
second order in the coupling. This is the framework's `Λ = 0 at low coupling`. -/

/-- T-L1a. `S'(k, 0) = 0` in closed form. -/
@[simp] theorem entropicPotentialDeriv_at_zero (k : ℝ) : entropicPotentialDeriv k 0 = 0 := by
  unfold entropicPotentialDeriv; simp

/-- T-L1b. `S''(k, 0) = k(k−1)` in closed form. -/
@[simp] theorem entropicPotentialDeriv2_at_zero (k : ℝ) :
    entropicPotentialDeriv2 k 0 = k * (k - 1) := by
  unfold entropicPotentialDeriv2; norm_num; ring

/-- **T-L1. THE SUBSTRATE IS A STATIONARY POINT OF THE ENTROPIC POTENTIAL.**
    `S` is differentiable at the chaos pole `ρ = 0` with derivative `0`.

    The two spectral branches of `C(k, ρ)` — the one stretched eigenvalue
    `1 + ρ(k−1)` and the `(k−1)` compressed ones `1 − ρ` — contribute
    `−(k−1)` and `+(k−1)` to `dS/dρ` at `ρ = 0` and cancel exactly. Bianconi's
    "zero cosmological constant at low coupling" is this cancellation. -/
theorem entropicPotential_hasDerivAt_zero (k : ℝ) :
    HasDerivAt (entropicPotential k) 0 0 := by
  have h := hasDerivAt_entropicPotential k 0 (by norm_num) (by norm_num)
  rwa [entropicPotentialDeriv_at_zero] at h

/-- T-L1c. The deviation is `o(ρ)`: there is no first-order term. Immediate
    from T-L1 + T-E1a via the definition of the derivative. -/
theorem entropicPotential_isLittleO_id (k : ℝ) :
    (fun ρ => entropicPotential k ρ) =o[𝓝 0] (fun ρ : ℝ => ρ) := by
  have h := hasDerivAt_iff_isLittleO.mp (entropicPotential_hasDerivAt_zero k)
  simpa [entropicPotential_at_zero] using h

/-! ## 3. T-L2 — the exact quadratic coefficient

`S(k, ρ)/ρ² → k(k−1)/2` as `ρ → 0⁺`. Two applications of L'Hôpital on `(0, 1)`,
where both spectral branches stay positive for `k ≥ 1`.

This mechanizes the small-ρ sensing law that `entropic_action_bridge.md` §T-E5
recorded as "documented, not mechanized": `S ≈ ½ k(k−1) ρ²`. -/

/-- Continuity of `S` at the substrate, as a one-sided limit. -/
private theorem tendsto_entropicPotential_zero (k : ℝ) :
    Tendsto (entropicPotential k) (𝓝[>] (0:ℝ)) (𝓝 0) := by
  have hc := (hasDerivAt_entropicPotential k 0 (by norm_num) (by norm_num)).continuousAt.tendsto
  rw [entropicPotential_at_zero] at hc
  exact hc.mono_left nhdsWithin_le_nhds

/-- Continuity of `S'` at the substrate, as a one-sided limit. Its value there
    is `0` (T-L1a). -/
private theorem tendsto_entropicPotentialDeriv_zero (k : ℝ) :
    Tendsto (entropicPotentialDeriv k) (𝓝[>] (0:ℝ)) (𝓝 0) := by
  have hc :=
    (hasDerivAt_entropicPotentialDeriv k 0 (by norm_num) (by norm_num)).continuousAt.tendsto
  rw [entropicPotentialDeriv_at_zero] at hc
  exact hc.mono_left nhdsWithin_le_nhds

/-- Continuity of `S''` at the substrate: `S''(k, ρ) → k(k−1)`. -/
private theorem tendsto_entropicPotentialDeriv2 (k : ℝ) :
    Tendsto (entropicPotentialDeriv2 k) (𝓝[>] (0:ℝ)) (𝓝 (k * (k - 1))) := by
  have hcont : ContinuousAt (entropicPotentialDeriv2 k) 0 := by
    unfold entropicPotentialDeriv2
    have h1 : ContinuousAt (fun x : ℝ => (1 - x) ^ 2) 0 := by fun_prop
    have h2 : ContinuousAt (fun x : ℝ => (1 + x * (k - 1)) ^ 2) 0 := by fun_prop
    have e1 : ((1 : ℝ) - 0) ^ 2 ≠ 0 := by norm_num
    have e2 : ((1 : ℝ) + 0 * (k - 1)) ^ 2 ≠ 0 := by norm_num
    exact (continuousAt_const.div h1 e1).add (continuousAt_const.div h2 e2)
  have := hcont.tendsto
  rw [entropicPotentialDeriv2_at_zero] at this
  exact this.mono_left nhdsWithin_le_nhds

/-- Both spectral branches are regular on `(0, 1)` when `k ≥ 1`. -/
private theorem branches_ne_zero {k x : ℝ} (hk : 1 ≤ k) (hx : x ∈ Ioo (0:ℝ) 1) :
    (1 - x ≠ 0) ∧ (1 + x * (k - 1) ≠ 0) := by
  obtain ⟨hx0, hx1⟩ := hx
  refine ⟨by linarith, ?_⟩
  have : 0 ≤ x * (k - 1) := mul_nonneg hx0.le (by linarith)
  linarith

/-- Intermediate: `S'(k, ρ)/(2ρ) → k(k−1)/2`. First L'Hôpital pass. -/
theorem entropicPotentialDeriv_div_tendsto (k : ℝ) (hk : 1 ≤ k) :
    Tendsto (fun ρ => entropicPotentialDeriv k ρ / (2 * ρ)) (𝓝[>] (0:ℝ))
      (𝓝 (k * (k - 1) / 2)) := by
  refine HasDerivAt.lhopital_zero_right_on_Ioo (a := 0) (b := 1) one_pos
    (f := entropicPotentialDeriv k) (f' := entropicPotentialDeriv2 k)
    (g := fun x => 2 * x) (g' := fun _ => 2)
    (fun x hx => hasDerivAt_entropicPotentialDeriv k x (branches_ne_zero hk hx).1
      (branches_ne_zero hk hx).2)
    (fun x _ => by simpa using (hasDerivAt_id x).const_mul (2:ℝ))
    (fun x _ => two_ne_zero)
    (tendsto_entropicPotentialDeriv_zero k) ?_ ?_
  · have : Tendsto (fun x : ℝ => 2 * x) (𝓝 (0:ℝ)) (𝓝 0) := by
      simpa using (continuous_const.mul continuous_id).tendsto (0:ℝ)
    exact this.mono_left nhdsWithin_le_nhds
  · have h := (tendsto_entropicPotentialDeriv2 k).div_const 2
    exact h

/-- **T-L2. THE DEVIATION IS EXACTLY SECOND ORDER.**
    `S(k, ρ)/ρ² → k(k−1)/2` as `ρ → 0⁺`. Second L'Hôpital pass.

    The coefficient `k(k−1)/2` is the number of coordinating PAIRS: the entropic
    cost of weak coordination is one half `ρ²` per pair. (Via T-E5c, `S = 2·I`,
    the Gaussian multi-information at small ρ is `¼ k(k−1) ρ²`.) -/
theorem entropicPotential_div_sq_tendsto (k : ℝ) (hk : 1 ≤ k) :
    Tendsto (fun ρ => entropicPotential k ρ / ρ ^ 2) (𝓝[>] (0:ℝ))
      (𝓝 (k * (k - 1) / 2)) := by
  refine HasDerivAt.lhopital_zero_right_on_Ioo (a := 0) (b := 1) one_pos
    (f := entropicPotential k) (f' := entropicPotentialDeriv k)
    (g := fun x => x ^ 2) (g' := fun x => 2 * x)
    (fun x hx => hasDerivAt_entropicPotential k x (branches_ne_zero hk hx).1
      (branches_ne_zero hk hx).2)
    (fun x _ => by simpa using hasDerivAt_pow 2 x)
    (fun x hx => by
      have : (0:ℝ) < x := hx.1
      positivity)
    (tendsto_entropicPotential_zero k) ?_ (entropicPotentialDeriv_div_tendsto k hk)
  · have : Tendsto (fun x : ℝ => x ^ 2) (𝓝 (0:ℝ)) (𝓝 0) := by
      simpa using (continuous_pow 2).tendsto (0:ℝ)
    exact this.mono_left nhdsWithin_le_nhds

/-- **The entropic potential is a second-order deviation.** The packaging of
    T-E1a + T-L1 + T-L2: the substrate is the zero AND the critical point of
    `S`, and the exact curvature there is `k(k−1)`. -/
theorem entropicPotential_secondOrderDeviation (k : ℝ) (hk : 1 ≤ k) :
    SecondOrderDeviation (entropicPotential k) (k * (k - 1) / 2) where
  vanishes_at_substrate := entropicPotential_at_zero k
  stationary_at_substrate := entropicPotential_hasDerivAt_zero k
  curvature_limit := entropicPotential_div_sq_tendsto k hk

/-- Corollary: the entropic potential has a weak-coupling limit. -/
theorem entropicPotential_lowCouplingLimit (k : ℝ) (hk : 1 ≤ k) :
    LowCouplingLimit (entropicPotential k) :=
  (entropicPotential_secondOrderDeviation k hk).toLowCouplingLimit

/-! ## 4. T-L3 — the induced post-selection weight is second order too

The soft P_ω weight is `w = exp(−β · S)`. Its deviation from the trivial
(identity) weight `1` is `1 − exp(−β S)`. This inherits stationarity from T-L1
— because `S` is stationary at the substrate and `exp` is smooth — and its
quadratic coefficient is `β · k(k−1)/2`.

This is the statement that at weak coordination the post-selection weight is
`1 + O(ρ²)`: to first order in the coupling, P_ω is the identity, so the theory
it post-selects is the unconditioned theory. Orthogonality in the power sector
(§5) is exact; here in the shape sector it is second-order-small. -/

/-- The entropic post-selection weight of the coordination spectrum. -/
noncomputable def entropicWeight (β k ρ : ℝ) : ℝ :=
  Real.exp (-β * entropicPotential k ρ)

@[simp] theorem entropicWeight_at_zero (β k : ℝ) : entropicWeight β k 0 = 1 := by
  unfold entropicWeight; simp [entropicPotential_at_zero]

/-- **T-L3. THE POST-SELECTION WEIGHT DEVIATES FROM UNITY ONLY AT SECOND ORDER.**
    `1 − exp(−β S(k, ρ))` is a second-order deviation with coefficient
    `β · k(k−1)/2`. To first order in the coordination coupling, the soft P_ω is
    the identity operator. -/
theorem entropicWeight_deviation_secondOrderDeviation (β k : ℝ) (hk : 1 ≤ k) :
    SecondOrderDeviation (fun ρ => 1 - entropicWeight β k ρ) (β * (k * (k - 1) / 2)) where
  vanishes_at_substrate := by simp
  stationary_at_substrate := by
    have hS := entropicPotential_hasDerivAt_zero k
    have hm : HasDerivAt (fun x => -β * entropicPotential k x) (-β * 0) 0 := hS.const_mul (-β)
    have he : HasDerivAt (fun x => Real.exp (-β * entropicPotential k x))
        (Real.exp (-β * entropicPotential k 0) * (-β * 0)) 0 := hm.exp
    have hD := he.const_sub 1
    have : -(Real.exp (-β * entropicPotential k 0) * (-β * 0)) = 0 := by ring
    rw [this] at hD
    exact hD
  curvature_limit := by
    -- L'Hôpital: numerator' = β·S'(ρ)·exp(−βS(ρ)), denominator' = 2ρ.
    refine HasDerivAt.lhopital_zero_right_on_Ioo (a := 0) (b := 1) one_pos
      (f := fun ρ => 1 - entropicWeight β k ρ)
      (f' := fun ρ => β * entropicPotentialDeriv k ρ * entropicWeight β k ρ)
      (g := fun x => x ^ 2) (g' := fun x => 2 * x)
      (fun x hx => ?_)
      (fun x _ => by simpa using hasDerivAt_pow 2 x)
      (fun x hx => by have : (0:ℝ) < x := hx.1; positivity)
      ?_ ?_ ?_
    · -- derivative of the weight deviation
      obtain ⟨h1, h2⟩ := branches_ne_zero hk hx
      have hS := hasDerivAt_entropicPotential k x h1 h2
      have hm := hS.const_mul (-β)
      have he := hm.exp
      have hD := he.const_sub 1
      have heq : -(Real.exp (-β * entropicPotential k x) * (-β * entropicPotentialDeriv k x))
          = β * entropicPotentialDeriv k x * entropicWeight β k x := by
        unfold entropicWeight; ring
      rw [heq] at hD
      exact hD
    · -- numerator → 0
      have hw : Tendsto (fun ρ => entropicWeight β k ρ) (𝓝[>] (0:ℝ)) (𝓝 1) := by
        have h := (tendsto_entropicPotential_zero k).const_mul (-β)
        rw [mul_zero] at h
        have := (Real.continuous_exp.tendsto 0).comp h
        simpa [entropicWeight, Function.comp] using this
      have := (tendsto_const_nhds (x := (1:ℝ)) (f := 𝓝[>] (0:ℝ))).sub hw
      simpa using this
    · -- denominator → 0
      have : Tendsto (fun x : ℝ => x ^ 2) (𝓝 (0:ℝ)) (𝓝 0) := by
        simpa using (continuous_pow 2).tendsto (0:ℝ)
      exact this.mono_left nhdsWithin_le_nhds
    · -- f'/g' = β · weight · (S'/(2ρ)) → β · 1 · k(k−1)/2
      have hw : Tendsto (fun ρ => entropicWeight β k ρ) (𝓝[>] (0:ℝ)) (𝓝 1) := by
        have h := (tendsto_entropicPotential_zero k).const_mul (-β)
        rw [mul_zero] at h
        have := (Real.continuous_exp.tendsto 0).comp h
        simpa [entropicWeight, Function.comp] using this
      have hq := entropicPotentialDeriv_div_tendsto k hk
      have hprod : Tendsto
          (fun ρ => β * entropicWeight β k ρ * (entropicPotentialDeriv k ρ / (2 * ρ)))
          (𝓝[>] (0:ℝ)) (𝓝 (β * 1 * (k * (k - 1) / 2))) :=
        ((tendsto_const_nhds.mul hw).mul hq)
      rw [mul_one] at hprod
      refine hprod.congr' ?_
      filter_upwards [self_mem_nhdsWithin] with x hx
      have hx0 : x ≠ 0 := ne_of_gt hx
      field_simp
      ring

/-! ## 5. The power sector — the missing bridge in `CMBOrthogonality`

`CMBOrthogonality` proves two things that it never joins:

  A. `participation_scale_invariant` — the shape observable is constant along
     the power ray.
  B. `pomega_preserves_power` — a weight independent of the power leaves the
     power expectation invariant.

Nothing there says the weight IS a function of `participation`. It is, and here
is why: `H_sum` is built from `ρ_ℓ`, and `ρ_ℓ` is read off the participation
ratio by inverting Kish, `k_eff = k/(1 + ρ(k−1))`. So the whole weight factors
through `participation`. The theorems below make that factorisation explicit,
so the remaining unproved input is isolated: the independence hypothesis
`indep`, i.e. Gaussian shape ⊥ scale (Fisher), cited not re-proved. -/

/-- The Kish inversion: recover the correlation `ρ` from the participation ratio
    `p = k_eff`. Inverse of `Core.k_eff k ρ = k / (1 + ρ(k−1))`. -/
noncomputable def kishRhoOfParticipation (k p : ℝ) : ℝ := (k - p) / (p * (k - 1))

/-- The inversion is correct: for `k > 1` and `ρ` in the physical range,
    `kishRhoOfParticipation k (k_eff k ρ) = ρ`. -/
theorem kishRhoOfParticipation_k_eff (k ρ : ℝ) (hk : 1 < k) (hρ0 : 0 ≤ ρ) (_hρ1 : ρ < 1) :
    kishRhoOfParticipation k (k_eff k ρ) = ρ := by
  have hkm1 : (0:ℝ) < k - 1 := by linarith
  have hden : (0:ℝ) < 1 + ρ * (k - 1) := by nlinarith
  have hk0 : (0:ℝ) < k := by linarith
  unfold kishRhoOfParticipation k_eff
  have hne : k / (1 + ρ * (k - 1)) ≠ 0 := by positivity
  field_simp
  ring

/-- The entropic weight, as a function of the amplitude vector: it factors
    through `participation` via the Kish inversion. This is the `w` of
    `CMBOrthogonality`, exhibited as a SHAPE function. -/
noncomputable def entropicWeightOfAmplitudes (β k : ℝ) {n : ℕ} (a : Fin n → ℝ) : ℝ :=
  entropicWeight β k (kishRhoOfParticipation k (participation a))

/-- **The entropic weight is scale-invariant.** Rescaling every amplitude by a
    nonzero `c` leaves the weight unchanged: the weight is constant along the
    power ray, so it carries no information about `C_ℓ`. Immediate from
    `participation_scale_invariant`. -/
theorem entropicWeightOfAmplitudes_scale_invariant (β k : ℝ) {n : ℕ} (c : ℝ) (hc : c ≠ 0)
    (a : Fin n → ℝ) :
    entropicWeightOfAmplitudes β k (fun i => c * a i) = entropicWeightOfAmplitudes β k a := by
  unfold entropicWeightOfAmplitudes
  rw [participation_scale_invariant c hc a]

/-- More generally: ANY weight factoring through `participation` is
    scale-invariant. This is the general shape-function statement; the entropic
    weight is the instance. -/
theorem shape_weight_scale_invariant {n : ℕ} (f : ℝ → ℝ) (c : ℝ) (hc : c ≠ 0)
    (a : Fin n → ℝ) :
    f (participation (fun i => c * a i)) = f (participation a) := by
  rw [participation_scale_invariant c hc a]

/-- **The power sector is exactly orthogonal, for any shape weight.**
    Instantiation of `pomega_preserves_power` with `w = f ∘ participation` and
    `S = Σ aᵢ²` (the power). Stating it this way isolates the ONE unproved
    input of the orthogonality theorem: `indep`, the Gaussian
    shape ⊥ scale independence (Fisher), which is cited, not re-proved.

    Note the conclusion is EXACT at every coupling — there is no limit here.
    The linearization content of this file lives entirely in the SHAPE sector
    (§2–§4), not in this sector. -/
theorem shape_weight_preserves_power {n : ℕ}
    (E : ((Fin n → ℝ) → ℝ) → ℝ) (f : ℝ → ℝ)
    (indep : E (fun a => f (participation a) * ∑ i, (a i) ^ 2)
      = E (fun a => f (participation a)) * E (fun a => ∑ i, (a i) ^ 2))
    (hw : E (fun a => f (participation a)) ≠ 0) :
    E (fun a => f (participation a) * ∑ i, (a i) ^ 2) / E (fun a => f (participation a))
      = E (fun a => ∑ i, (a i) ^ 2) :=
  pomega_preserves_power E _ _ indep hw

/-- The entropic instance: with the entropic weight in the shape sector, the
    framework's bulk power spectrum equals ΛCDM's, exactly, at every `β`. -/
theorem entropic_pomega_preserves_power {n : ℕ} (β k : ℝ)
    (E : ((Fin n → ℝ) → ℝ) → ℝ)
    (indep : E (fun a => entropicWeightOfAmplitudes β k a * ∑ i, (a i) ^ 2)
      = E (fun a => entropicWeightOfAmplitudes β k a) * E (fun a => ∑ i, (a i) ^ 2))
    (hw : E (fun a => entropicWeightOfAmplitudes β k a) ≠ 0) :
    E (fun a => entropicWeightOfAmplitudes β k a * ∑ i, (a i) ^ 2)
        / E (fun a => entropicWeightOfAmplitudes β k a)
      = E (fun a => ∑ i, (a i) ^ 2) :=
  shape_weight_preserves_power E
    (fun p => entropicWeight β k (kishRhoOfParticipation k p)) indep hw

/-! ## 6. The structural record — theorem vs interpretation

What is above is theorem. What follows is the reading, recorded in the lake's
record house pattern (cf. `Cosmology.CorridorProjector.FelevenNoGo`,
`OperationalCorridor`) rather than dressed as a theorem it is not. -/

/-- ORTHOGONALITY AS LINEARIZATION. The two-sector reading of the orthogonality
    theorem, with the modelling commitments named. A flat record of facts and
    their evidence — not an asserted operator, not a `sorry`. -/
structure OrthogonalityIsLinearization where
  /-- POWER SECTOR (theorem, exact at all β). The post-selection weight factors
      through `participation`, which is scale-invariant, so the weight is
      constant along the power ray and — given Gaussian shape ⊥ scale — the
      reweighted power equals the unreweighted power.
      Evidence: `entropicWeightOfAmplitudes_scale_invariant`,
      `entropic_pomega_preserves_power`, `CMBOrthogonality.framework_cmb_power_eq_lcdm`. -/
  power_sector_exact_at_all_coupling : True
  /-- SHAPE SECTOR (theorem, asymptotic). The substrate ρ = 0 is a STATIONARY
      point of the entropic potential, so the deviation has no first-order term
      and `S(k,ρ)/ρ² → k(k−1)/2`.
      Evidence: `entropicPotential_hasDerivAt_zero`, `entropicPotential_div_sq_tendsto`. -/
  shape_sector_second_order : True
  /-- THE MECHANISM. Bianconi's "exactly Einstein–Hilbert with Λ = 0 at low
      coupling" (arXiv:2408.14391 Eqs. 45–47) is, structurally, the statement
      that the vacuum extremizes the relative-entropy action. T-L1 is that
      statement for `S(k, ρ)`. The orthogonality theorem is therefore not
      merely a fence ("we happen not to deviate") but the power-sector face of
      a stationarity: the deviation is a second-order entropic quantity.
      Evidence: `entropicWeight_deviation_secondOrderDeviation` — the weight is
      `1 + O(ρ²)`, so to first order the soft P_ω is the identity. -/
  linearization_is_the_mechanism : True
  /-- NOT A THEOREM, AND NOT CLAIMED AS ONE. The orthogonality theorem is EXACT
      at every β and takes no limit; a linearization statement is asymptotic.
      They are not the same statement. What is proved is the conjunction of the
      two sector facts above, which is the framework's analogue of Eqs. 45–47 —
      not an identification of the two theorems. -/
  orthogonality_is_not_literally_a_limit : True
  /-- MODELLING COMMITMENT (documented, not mechanized). That the CMB weight
      `w = exp(−β H_sum)` with `H_sum = Σ_ℓ (ρ_ℓ − ρ_mid)²` IS the entropic
      weight `exp(−β Σ_ℓ S(k_ℓ, ρ_ℓ))` — i.e. that `H_sum` is a
      reparametrisation of the entropic potential — is a modelling choice.
      Both are shape functions (both factor through `participation`), so both
      are power-orthogonal; but they are not the same functional. The
      power-sector theorem holds for either; the second-order coefficient
      `k(k−1)/2` is specific to `S`. -/
  H_sum_equals_entropic_potential_is_a_modelling_commitment : True
  /-- MODELLING COMMITMENT (cited, not proved). The independence hypothesis
      `indep` — Gaussian shape ⊥ scale — is Fisher's χ²-⊥-direction result. It
      is a hypothesis of `pomega_preserves_power`, not a theorem of the lake. -/
  gaussian_shape_scale_independence_is_cited_not_proved : True
  /-- F-11 DISCIPLINE. All of the above is FORWARD content: the forward soft
      P_ω (ρ_ss steady state) and the entropic potential. The joint multi-rung
      backward P_ω remains a documented no-go
      (`CorridorProjector.F11_joint_backward_P_omega_no_go`). Bianconi's action
      is a local, bulk-geometric, forward variational principle — it enters the
      F-11 construction tree at the already-closed correlation/topology branch
      (T1 geometric dilution). Nothing here reopens it. -/
  forward_only_f11_untouched : True

/-- The two-sector reading is recorded. -/
def orthogonality_is_linearization : OrthogonalityIsLinearization :=
  ⟨trivial, trivial, trivial, trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Cosmology.EntropicLinearization
