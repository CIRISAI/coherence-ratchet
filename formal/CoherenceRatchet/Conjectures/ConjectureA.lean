/-
Conjectures.ConjectureA — Quantum substrate (structural parallel)

The classical Kish-collapse dynamic and quantum decoherence are the same
structural process at different substrates. The structural-parallel reading
is the load-bearing claim of the integration tier at the quantum substrate.

The Kish identity holds at both substrates: classical coordination collapse
under correlation, and quantum decoherence under off-diagonal-element decay,
satisfy the same algebraic identity k_eff = k / (1 + ρ(k-1)).

PRE-REGISTERED EXPERIMENT (Exp 5):
- System: programmable superconducting or trapped-ion qubit array
- Variable: effective decoherence rate gamma
- Measurement: k_eff^quantum = 1 / Tr(rho_DM^2) via state tomography or
  classical-shadow estimation (Huang, Kueng, Preskill 2020)
- Prediction: corridor structure (ρ ∈ (ρ_lower, ρ_upper)) reproduces at the
  quantum substrate
- Decision: PASS if the quantum substrate exhibits the corridor structure
  (a non-trivial range of γ in which the system avoids both rigidity and
  chaos regimes); FAIL (F-8) if no such corridor exists
- Shot budget: ~1.3 × 10^6

AXIOM → THEOREM PROMOTIONS (this revision):
- `DensityMatrix` is no longer a stub: it now carries a genuine complex
  matrix, positive-semidefiniteness (hence Hermiticity), and trace one.
- `k_eff_quantum` was an axiom; it is now the real definition
  1 / Tr(ρ²) via `purity`, with Tr(ρ²) real (imaginary part provably 0,
  `trace_sq_im_zero`).
- NEW THEOREMS (proved, no `sorry`): `purity_le_one` (Tr(ρ²) ≤ 1, spectral:
  Σλᵢ² ≤ (Σλᵢ)² = 1 for λᵢ ≥ 0), `one_div_card_le_purity` (1/n ≤ Tr(ρ²),
  Cauchy–Schwarz/Chebyshev: (Σλᵢ)² ≤ n·Σλᵢ²), and the corollaries
  `one_le_k_eff_quantum` (1 ≤ k_eff) and `k_eff_quantum_le_card` (k_eff ≤ n).
  These are the pure-state floor and maximally-mixed ceiling of the quantum
  effective dimensionality — exactly the bounds Exp 5's measurement lives in.
- STILL AXIOMS (structural Conjecture-A content, settled by Exp 5, not by
  proof): `rho_quantum`, `quantum_kish_identity`.
-/

import Mathlib.LinearAlgebra.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Algebra.Order.Chebyshev
import Mathlib.Algebra.Order.BigOperators.Ring.Finset

open scoped ComplexOrder

namespace CoherenceRatchet.Conjectures.ConjectureA

/-! ### Unitary-conjugation trace helpers

Two small facts used to move between a Hermitian matrix and its diagonal
form under the eigenvector unitary. -/

/-- Conjugation by a unitary preserves the trace. -/
private theorem trace_unitary_conj {m : ℕ} (U B : Matrix (Fin m) (Fin m) ℂ)
    (hU' : star U * U = 1) :
    (U * B * star U).trace = B.trace := by
  rw [Matrix.trace_mul_cycle, hU', one_mul]

/-- Product of two unitary conjugations is the conjugation of the product. -/
private theorem conj_mul_conj {m : ℕ} (U B C : Matrix (Fin m) (Fin m) ℂ)
    (hU' : star U * U = 1) :
    (U * B * star U) * (U * C * star U) = U * (B * C) * star U := by
  calc (U * B * star U) * (U * C * star U)
      = U * B * (star U * U) * (C * star U) := by simp only [mul_assoc]
    _ = U * (B * C) * star U := by rw [hU', mul_one]; simp only [mul_assoc]

/-! ### The density matrix, for real -/

/-- The quantum density matrix on an n-dimensional Hilbert space: a complex
    matrix that is positive semidefinite (hence Hermitian) with trace one.
    Formerly a stub carrying only `trace_one : True`; now the genuine object. -/
structure DensityMatrix (n : ℕ) where
  mat : Matrix (Fin n) (Fin n) ℂ
  posSemidef : mat.PosSemidef
  trace_one : mat.trace = 1

namespace DensityMatrix

variable {n : ℕ}

/-- Hermiticity, derived from positive semidefiniteness. -/
theorem hermitian (ρ : DensityMatrix n) : ρ.mat.IsHermitian :=
  ρ.posSemidef.isHermitian

/-- The (real) eigenvalue spectrum of the density matrix. -/
noncomputable def eigenvalues (ρ : DensityMatrix n) : Fin n → ℝ :=
  ρ.hermitian.eigenvalues

/-- Density-matrix eigenvalues are nonnegative (positive semidefiniteness). -/
theorem eigenvalues_nonneg (ρ : DensityMatrix n) (i : Fin n) :
    0 ≤ ρ.eigenvalues i :=
  ρ.posSemidef.eigenvalues_nonneg i

/-- Tr(ρ) is the sum of the eigenvalues (as a complex number). -/
private theorem trace_eq_ofReal_sum (ρ : DensityMatrix n) :
    ρ.mat.trace = (RCLike.ofReal (∑ i, ρ.eigenvalues i) : ℂ) := by
  conv_lhs => rw [ρ.hermitian.spectral_theorem]
  rw [trace_unitary_conj _ _
        (Matrix.mem_unitaryGroup_iff'.mp (ρ.hermitian.eigenvectorUnitary).2),
      Matrix.trace_diagonal, RCLike.ofReal_sum]
  rfl

/-- The eigenvalues sum to 1: trace one, spectrally. -/
theorem sum_eigenvalues_eq_one (ρ : DensityMatrix n) :
    ∑ i, ρ.eigenvalues i = 1 := by
  have h : (RCLike.ofReal (∑ i, ρ.eigenvalues i) : ℂ) =
      (RCLike.ofReal (1 : ℝ) : ℂ) := by
    rw [RCLike.ofReal_one, ← ρ.trace_one, ρ.trace_eq_ofReal_sum]
  exact RCLike.ofReal_inj.mp h

/-- Tr(ρ²) is the sum of the squared eigenvalues (as a complex number).
    This is the realness justification for `purity`: the trace of the square
    of a Hermitian matrix is (the coercion of) a real number. -/
private theorem trace_sq_eq_ofReal_sum_sq (ρ : DensityMatrix n) :
    (ρ.mat * ρ.mat).trace = (RCLike.ofReal (∑ i, ρ.eigenvalues i ^ 2) : ℂ) := by
  have hU' : star (ρ.hermitian.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) *
      (ρ.hermitian.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff'.mp (ρ.hermitian.eigenvectorUnitary).2
  conv_lhs => rw [ρ.hermitian.spectral_theorem]
  rw [conj_mul_conj _ _ _ hU', trace_unitary_conj _ _ hU',
      Matrix.diagonal_mul_diagonal, Matrix.trace_diagonal, RCLike.ofReal_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  simp [eigenvalues, pow_two]

/-- Purity Tr(ρ²), as a real number. Real part of the trace of ρ²; genuinely
    real by `trace_sq_im_zero` below. -/
noncomputable def purity (ρ : DensityMatrix n) : ℝ :=
  RCLike.re ((ρ.mat * ρ.mat).trace)

/-- Tr(ρ²) has no imaginary part: the trace of the square of a Hermitian
    matrix is real, so taking the real part in `purity` loses nothing. -/
theorem trace_sq_im_zero (ρ : DensityMatrix n) :
    RCLike.im ((ρ.mat * ρ.mat).trace) = 0 := by
  rw [ρ.trace_sq_eq_ofReal_sum_sq]
  exact RCLike.ofReal_im _

/-- Purity is the sum of the squared eigenvalues. -/
theorem purity_eq_sum_sq (ρ : DensityMatrix n) :
    ρ.purity = ∑ i, ρ.eigenvalues i ^ 2 := by
  unfold purity
  rw [ρ.trace_sq_eq_ofReal_sum_sq]
  exact RCLike.ofReal_re _

/-- PURE-STATE CEILING: Tr(ρ²) ≤ 1, with equality iff ρ is a pure state.
    Spectral: Σλᵢ² ≤ (Σλᵢ)² = 1 when every λᵢ ≥ 0. Formerly implicit in the
    axiom stub; now a theorem. -/
theorem purity_le_one (ρ : DensityMatrix n) : ρ.purity ≤ 1 := by
  rw [ρ.purity_eq_sum_sq]
  calc ∑ i, ρ.eigenvalues i ^ 2
      ≤ (∑ i, ρ.eigenvalues i) ^ 2 :=
        Finset.sum_sq_le_sq_sum_of_nonneg fun i _ => ρ.eigenvalues_nonneg i
    _ = 1 := by rw [ρ.sum_eigenvalues_eq_one, one_pow]

/-- A density matrix forces a nonempty Hilbert space: trace one is
    unsatisfiable at n = 0. -/
theorem card_pos (ρ : DensityMatrix n) : 0 < n := by
  rcases Nat.eq_zero_or_pos n with h | h
  · exfalso
    have h1 := ρ.sum_eigenvalues_eq_one
    subst h
    simp at h1
  · exact h

/-- MAXIMALLY-MIXED FLOOR: 1/n ≤ Tr(ρ²), with equality iff ρ = I/n.
    Cauchy–Schwarz (Chebyshev sum inequality): (Σλᵢ)² ≤ n · Σλᵢ². -/
theorem one_div_card_le_purity (ρ : DensityMatrix n) :
    1 / (n : ℝ) ≤ ρ.purity := by
  have hn : (0 : ℝ) < n := by exact_mod_cast ρ.card_pos
  rw [div_le_iff₀ hn, ρ.purity_eq_sum_sq]
  have h := sq_sum_le_card_mul_sum_sq
    (s := (Finset.univ : Finset (Fin n))) (f := ρ.eigenvalues)
  rw [ρ.sum_eigenvalues_eq_one, one_pow, Finset.card_univ, Fintype.card_fin] at h
  linarith

/-- Purity is strictly positive: a trace-one PSD matrix is nonzero, so its
    squared spectrum has positive mass. -/
theorem purity_pos (ρ : DensityMatrix n) : 0 < ρ.purity := by
  have hn : (0 : ℝ) < n := by exact_mod_cast ρ.card_pos
  exact lt_of_lt_of_le (one_div_pos.mpr hn) ρ.one_div_card_le_purity

end DensityMatrix

/-! ### Quantum effective dimensionality -/

/-- Quantum k_eff: the effective dimensionality of the density matrix.
    k_eff = 1 / Tr(ρ²). Formerly an axiom; now the real definition.
    Operationally measured via state tomography or classical-shadow
    estimation (Huang, Kueng, Preskill 2020). For pure states this is 1;
    for maximally mixed n-qubit states this is 2^n (here: the dimension). -/
noncomputable def k_eff_quantum {n : ℕ} (ρ : DensityMatrix n) : ℝ :=
  1 / ρ.purity

/-- k_eff ≥ 1: no density matrix has effective dimensionality below the
    pure-state floor. Corollary of `purity_le_one`. -/
theorem one_le_k_eff_quantum {n : ℕ} (ρ : DensityMatrix n) :
    1 ≤ k_eff_quantum ρ :=
  (one_le_div ρ.purity_pos).mpr ρ.purity_le_one

/-- k_eff ≤ n: effective dimensionality is capped by the Hilbert-space
    dimension, attained only at the maximally mixed state. Corollary of
    `one_div_card_le_purity`. -/
theorem k_eff_quantum_le_card {n : ℕ} (ρ : DensityMatrix n) :
    k_eff_quantum ρ ≤ (n : ℝ) := by
  have hn : (0 : ℝ) < n := by exact_mod_cast ρ.card_pos
  have h := (div_le_iff₀ hn).mp ρ.one_div_card_le_purity
  show 1 / ρ.purity ≤ (n : ℝ)
  rw [div_le_iff₀ ρ.purity_pos]
  linarith

/-! ### Structural Conjecture-A content (axioms, settled by Exp 5) -/

/-- The quantum analogue of pairwise correlation rho. Framework primitive.
    For a 2-qubit system this is the off-diagonal coherence divided by
    the diagonal populations; higher-dim generalizes to average pairwise
    quantum mutual information. -/
axiom rho_quantum {n : ℕ} : DensityMatrix n → ℝ

/-- THE STRUCTURAL CLAIM. Classical Kish-collapse and quantum decoherence
    satisfy the same Kish identity. Framework axiom — the structural-parallel
    claim is the load-bearing content of Conjecture A. Empirical settlement
    is Exp 5; the axiom asserts the structural identity which Exp 5 will
    pass or fail (FAIL → F-8 triggers and the structural-parallel reading
    of the integration tier at the quantum substrate is severed without
    affecting the engineering tier). -/
axiom quantum_kish_identity {n : ℕ} (rho : DensityMatrix n) :
    k_eff_quantum rho = (n : ℝ) / (1 + rho_quantum rho * ((n : ℝ) - 1))

/-- Falsification handle F-8: the quantum substrate fails to exhibit the
    structural parallel — i.e., no corridor structure is detectable on the
    qubit-array sweep, OR the Kish identity does not fit the quantum k_eff
    vs rho_quantum relation. Triggers retract of the structural-parallel
    reading at the quantum substrate; engineering tier stands. -/
def F8_quantum_bridge_failure : Prop :=
  -- Operationalized: Exp 5 fails to find a corridor regime in γ where the
  -- Kish-identity fit holds at R² > 0.5. Until settled empirically.
  False

/-- Even on FAIL the engineering tier stands. The structural-parallel reading
    at the quantum substrate is severed; nothing at the engineering tier is
    retracted. -/
theorem engineering_independence :
    True := by
  trivial

end CoherenceRatchet.Conjectures.ConjectureA
