/-
Core.Coherence — CC 6.2.4: the coherence functional and the J = F identity

Book IX (Part VI) of the CIRIS Constitution defines two three-factor functionals:

  J = k_eff · λ_op · σ    (defense / justice: the cost imposed on deception)   [CC 6.2.4, l.253]
  F = k_eff · λ_op · σ    (flourishing: the capacity created)                  [CC 6.2.4, l.301]

"the same equation as J, term for term: the cost imposed on deception and the
capacity created for flourishing are one geometry seen from two sides."

Principle mapping: scale k → Community; pluralism = the correlation discount
inside k_eff → Humility; strictness λ_op → Conscience; sustainability σ → Love.
- k_eff is the Kish effective dimensionality (`Core.k_eff`).
- λ_op is operator-tunable operational strictness, DISTINCT from the geometric
  λ_geo of the collapse theorem (CC 6.2.1 nomenclature note: they carry no default
  mapping; λ_op MUST NOT be substituted into the collapse bound).
- σ is the sustainability integral, an exp-decay semigroup (CC 6.2.3); its
  exponential form is load-bearing for the SIGN of J.

HONESTY NOTE (per the "tautology vs commitment" discipline). `J_eq_F` is a
DEFINITIONAL identity — J and F are the same functional, so the proof is `rfl`.
The content is not the proof but the MODELING COMMITMENT that defense and
flourishing are the same geometry. What earns mechanization is (a) pinning that
both objectives ARE this one functional, so the Constitution's CC 6.2.4 `lean:`
pointer resolves to a real object rather than to prose, and (b) the structural
facts that DO carry proof obligations: nonnegativity, factor-monotonicity, and
the σ semigroup + sign-preservation that Book IX makes load-bearing for J's sign
(the withdrawn linear form σ₀·(1−d·Δt) goes negative and would flip J's sign;
the exponential cannot).

This is the `lean:` anchor for CC 6.2.4 (CLM-math-JF) and, via `sigma_decay_*`,
for the σ-semigroup content of CC 6.2.3 (CLM-sigma-semigroup).
-/

import CoherenceRatchet.Core.BaseIdentity
import Mathlib.Analysis.SpecialFunctions.Exp

namespace CoherenceRatchet.Core.Coherence

open CoherenceRatchet.Core

/-- The Book IX coherence functional: the single three-factor geometry
    C(k_eff, λ_op, σ) = k_eff · λ_op · σ (CC 6.2.4). -/
noncomputable def coherence (k_eff lam_op σ : ℝ) : ℝ := k_eff * lam_op * σ

/-- Defense / justice functional `J = k_eff · λ_op · σ` (CC 6.2.4). -/
noncomputable def J (k_eff lam_op σ : ℝ) : ℝ := coherence k_eff lam_op σ

/-- Flourishing functional `F = k_eff · λ_op · σ` (CC 6.2.4). -/
noncomputable def F (k_eff lam_op σ : ℝ) : ℝ := coherence k_eff lam_op σ

/-- THE identity: J = F, term for term — defense and flourishing are one geometry.
    Definitional (the content is the modeling commitment, not the proof); this pins
    the CC 6.2.4 `lean:` anchor to a real object. -/
theorem J_eq_F (k_eff lam_op σ : ℝ) : J k_eff lam_op σ = F k_eff lam_op σ := rfl

/-- Grounding: with the first factor instantiated at the Kish effective
    dimensionality (`Core.k_eff k ρ`), J = F still holds — the functional's scale
    factor is the real Kish object from Piece 1, not a free scalar. -/
theorem J_eq_F_kish (k ρ lam_op σ : ℝ) :
    J (k_eff k ρ) lam_op σ = F (k_eff k ρ) lam_op σ := rfl

/-- Nonnegativity: with all three factors nonnegative the coherence is
    nonnegative (a well-formed state cannot have negative defense capacity). -/
theorem coherence_nonneg {k_eff lam_op σ : ℝ}
    (hk : 0 ≤ k_eff) (hl : 0 ≤ lam_op) (hs : 0 ≤ σ) :
    0 ≤ coherence k_eff lam_op σ :=
  mul_nonneg (mul_nonneg hk hl) hs

/-- Monotone in strictness: raising operational strictness λ_op (Conscience) at
    fixed nonnegative k_eff and σ does not decrease coherence. -/
theorem coherence_mono_strictness {k_eff σ : ℝ} (hk : 0 ≤ k_eff) (hs : 0 ≤ σ)
    {l₁ l₂ : ℝ} (h : l₁ ≤ l₂) :
    coherence k_eff l₁ σ ≤ coherence k_eff l₂ σ :=
  mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left h hk) hs

/-- Monotone in effective dimensionality: raising k_eff (Community × Humility) at
    fixed nonnegative λ_op and σ does not decrease coherence. -/
theorem coherence_mono_keff {lam_op σ : ℝ} (hl : 0 ≤ lam_op) (hs : 0 ≤ σ)
    {k₁ k₂ : ℝ} (h : k₁ ≤ k₂) :
    coherence k₁ lam_op σ ≤ coherence k₂ lam_op σ :=
  mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_right h hl) hs

/-! ## σ as an exp-decay semigroup (CC 6.2.3), load-bearing for J's sign -/

/-- The sustainability decay (CC 6.2.3): `σ(Δt) = σ₀ · exp(−d·Δt)`. -/
noncomputable def sigma_decay (σ₀ d Δt : ℝ) : ℝ := σ₀ * Real.exp (-(d * Δt))

/-- Semigroup law: decaying over `a + b` equals decaying over `a` then over `b`.
    This is exactly what makes σ cadence-invariant — the decimation-recovery rejoin
    (one peer taking a single large Δt step) computes an identical σ. The exponential
    is the only form with this property; the withdrawn linear form is not a
    semigroup. -/
theorem sigma_decay_semigroup (σ₀ d a b : ℝ) :
    sigma_decay σ₀ d (a + b) = sigma_decay (sigma_decay σ₀ d a) d b := by
  unfold sigma_decay
  have hsplit : -(d * (a + b)) = -(d * a) + -(d * b) := by ring
  rw [hsplit, Real.exp_add]
  ring

/-- Sign preservation: for `σ₀ ≥ 0` the exponential decay stays nonnegative for ALL
    Δt. The withdrawn linear form `σ₀·(1 − d·Δt)` goes negative past `Δt = 1/d` and
    would flip the sign of `J = k_eff·λ_op·σ`; the semigroup form cannot. -/
theorem sigma_decay_nonneg {σ₀ : ℝ} (h : 0 ≤ σ₀) (d Δt : ℝ) :
    0 ≤ sigma_decay σ₀ d Δt :=
  mul_nonneg h (Real.exp_pos _).le

/-- Corollary tying σ's sign to J: with nonnegative k_eff, λ_op and a nonnegative
    initial σ₀, the defense functional evaluated on the decayed σ is nonnegative for
    every elapsed Δt — J never changes sign under sustainability decay. -/
theorem J_nonneg_under_decay {k_eff lam_op σ₀ : ℝ}
    (hk : 0 ≤ k_eff) (hl : 0 ≤ lam_op) (hσ : 0 ≤ σ₀) (d Δt : ℝ) :
    0 ≤ J k_eff lam_op (sigma_decay σ₀ d Δt) :=
  coherence_nonneg hk hl (sigma_decay_nonneg hσ d Δt)

end CoherenceRatchet.Core.Coherence
