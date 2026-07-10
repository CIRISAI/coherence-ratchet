/-
Core.EntropicContraction — the entropic-potential contraction (DPI) inequality,
clause (4) of the coordination law.

This module mechanizes the matrix backbone of the "no-phantom" theorem
(`experiments/cosmo_entropic_potential/SUMMARY.md` §5; `results.json` key
`general_theorem`). The physics claim there is:

  For a Gaussian linear field with normalized correlation matrix c and ANY
  pointwise (local) transform g, the transformed correlation matrix C_g
  satisfies S(C_g) ≤ S(c), where S = −ln det. Since S → S_linear (constant) as
  a → 0 and S ≤ S_linear always, S can only fall, so 1 + w = −⅓ dlnS/dlna ≥ 0:
  no local model of nonlinear growth can produce a phantom (w < −1) epoch.

The numerical proof chain (SUMMARY §5) has four clauses:
  (1) MEHLER/HERMITE: C_g = Σ_{n≥1} w_n c^{∘n}, a convex combination of Hadamard
      powers (w_n ≥ 0, Σ w_n = 1);
  (2) SCHUR PRODUCT THEOREM: Hadamard products of PSD matrices are PSD, so each
      c^{∘n} is PSD with unit diagonal;
  (3) OPPENHEIM: det(A ∘ B) ≥ det A · Π_i B_ii, hence det(c^{∘n}) ≥ det c for
      unit-diagonal c, so S(c^{∘n}) ≤ S(c);
  (4) CONVEXITY of −ln det on the PSD cone, to pass from the powers to the
      convex combination: S(Σ w_n c^{∘n}) ≤ Σ w_n S(c^{∘n}) ≤ S(c).

This file mechanizes the DEFINITIONAL layer (T-C0) and the general
arbitrary-matrix Klein/nonnegativity theorem (T-C1) — the base inequality
S(C) ≥ 0 for every PSD unit-diagonal C, which generalizes the uniform-ρ
`entropicPotential_nonneg` (T-E0 in Core.EntropicPotential) to ARBITRARY
correlation matrices — plus the 2×2 explicit case of Oppenheim (T-C3₂). The
Schur product theorem (2), general Oppenheim (3), and the −ln det convexity (4)
are ABSENT from mathlib v4.14 and are recorded as a precise roadmap below.

================================================================================
MATHLIB v4.14 SURVEY (checked against .lake/packages/mathlib @ v4.14.0)
================================================================================

PRESENT and used:
  • `Matrix.PosSemidef` / `Matrix.PosDef`               (LinearAlgebra/Matrix/PosDef.lean)
  • `Matrix.PosSemidef.eigenvalues_nonneg`               — 0 ≤ eigenvalue          (PosDef.lean:160)
  • `Matrix.PosDef.det_pos`                              — 0 < det for PosDef       (PosDef.lean:447)
  • `Matrix.IsHermitian.det_eq_prod_eigenvalues`         — det = ∏ λ                (Spectrum.lean:125)
  • `Matrix.IsHermitian.spectral_theorem`                — A = U diag(λ) Uˣ         (Spectrum.lean:108)
  • `Matrix.mem_unitaryGroup_iff` / `_iff'`              — U Uˣ = 1 / Uˣ U = 1      (UnitaryGroup.lean:63,67)
  • `Matrix.trace_diagonal`, `Matrix.trace_mul_comm`     (LinearAlgebra/Matrix/Trace.lean)
  • `Real.log_prod`, `Real.log_le_sub_one_of_pos`,
    `Real.log_lt_sub_one_of_pos`                          (Analysis/SpecialFunctions/Log/Basic.lean)
  • `RCLike.ofReal_real_eq_id`                            — ofReal = id over ℝ      (RCLike/Basic.lean:918)

DERIVED here (mathlib has no direct statement):
  • `IsHermitian.trace_eq_sum_eigenvalues` — trace A = Σ λ_i, for a real Hermitian
    matrix, via the spectral theorem + trace cyclicity. (mathlib has trace = Σ
    roots-of-charpoly over an algebraically closed field in Charpoly/Eigs.lean,
    but nothing linking `IsHermitian.eigenvalues` to the trace.)

ABSENT — the reason the chain stops at T-C1 (see ROADMAP):
  • SCHUR PRODUCT THEOREM. `Mathlib/Data/Matrix/Hadamard.lean` has ONLY the
    algebra of `⊙` (comm/assoc/distrib/smul), NO positivity. `PosSemidef.hadamard`
    does not exist. `Mathlib/LinearAlgebra/Matrix/SchurComplement.lean` is the
    Schur COMPLEMENT (block matrices), a different object.
  • KRONECKER POSITIVITY. `Mathlib/Data/Matrix/Kronecker.lean` has no PosSemidef
    lemma, so the "Hadamard = principal submatrix of Kronecker" route to Schur is
    not short either.
  • OPPENHEIM'S INEQUALITY. Absent (as expected).
  • ln-det CONCAVITY / (−ln det) CONVEXITY on the PSD cone. Absent. No
    `StrictConcaveOn … Matrix.det` of any kind.

================================================================================
WHAT IS PROVED (this module), zero sorries / zero new axioms (audited below):
================================================================================
  T-C0   definitions: `IsUnitDiag`, `entropicPotentialM C := −ln det C`; the
         bridge `entropicPotentialM (kishMatrix k ρ) = entropicPotential k ρ`
         (grounds the closed-form potential in the actual matrix functional).
  T-C1   KLEIN, GENERAL MATRIX FORM: for PSD unit-diagonal C with det C > 0,
         0 ≤ entropicPotentialM C, with equality iff C = 1. This is the first
         ARBITRARY-matrix entropic-potential theorem in the tier — it generalizes
         `entropicPotential_nonneg` (uniform-ρ only) to every correlation matrix.
         Route: eigenvalues positive (PSD + det>0), Σ λ = trace = k (unit diag),
         and log λ ≤ λ − 1 per eigenvalue ⟹ Σ log λ ≤ Σ(λ−1) = 0 ⟹ det ≤ 1.
  T-C3₂  OPPENHEIM, k = 2 explicit: for the 2×2 unit-diagonal matrices C(a), C(b)
         with |a|,|b| ≤ 1, det(C(a) ∘ C(b)) ≥ det C(a). The concrete base case of
         clause (3); det(C(a)∘C(a)) ≥ det C(a) (the Hadamard-square step of the
         C_g pipeline) is the b = a instance.

================================================================================
ROADMAP for the remaining clauses (honest tags — not attempted here):
================================================================================
  T-C2  (Schur product theorem: A,B PosSemidef ⟹ A ∘ B PosSemidef). REAL PROJECT.
        Cleanest self-contained route over ℝ: spectrally decompose B = Σ_k λ_k
        u_k u_kᵀ (λ_k ≥ 0 via `spectral_theorem` + `eigenvalues_nonneg`); then for
        any x, xᵀ(A∘B)x = Σ_k λ_k (x ⊙ u_k)ᵀ A (x ⊙ u_k) ≥ 0 since A is PSD. The
        Lean cost is the quadratic-form bookkeeping (reindexing the double sum and
        the entrywise product x_i u_{k,i}); ~a day. Alternative (also unsupported
        today): add Kronecker PSD (A,B PSD ⟹ A ⊗ B PSD) then `PosSemidef.submatrix`
        on the diagonal embedding — but Kronecker PSD is itself absent.
  T-C3  (Oppenheim general: det(A∘B) ≥ det A · Π B_ii for A,B PSD, B unit-diagonal).
        HARD CORE. Standard proof is induction on dimension via Schur complements
        (`SchurComplement.lean` provides the block infrastructure); depends on T-C2.
        The k = 2 case is proved here (T-C3₂); the induction is the open work.
  T-C4  (convex-combination / DPI closure: −ln det(Σ wₙ Cₙ) ≤ Σ wₙ (−ln det Cₙ)).
        Needs CONCAVITY of ln det on the PD cone — absent from mathlib. Standard
        route: ln det is concave because its Hessian −C⁻¹ ⊗ C⁻¹ is negative
        semidefinite; mechanizing this needs matrix-calculus infrastructure not
        present in v4.14. This is the largest single gap. With T-C2+T-C3+T-C4 the
        full no-phantom inequality S(C_g) ≤ S(c) closes by the SUMMARY §5 chain.

SCOPE. Everything here is FORWARD, engineering-tier linear algebra grounding the
candidate potential S = −ln det; like Core.EntropicPotential it does not touch the
F-11 no-go on the joint backward P_ω.
-/

import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Hadamard
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import CoherenceRatchet.Core.EntropicPotential

namespace CoherenceRatchet.Core

open Matrix Real

variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ## T-C0 — definitions and the matrix bridge -/

/-- A correlation matrix has unit diagonal: `C i i = 1` for every index. -/
def IsUnitDiag (C : Matrix n n ℝ) : Prop := ∀ i, C i i = 1

/-- The entropic potential of a general correlation matrix: `S(C) = −ln det C`.
    Bianconi's `−Tr ln C`, the matrix functional behind the closed-form
    `Core.EntropicPotential.entropicPotential` on the uniform-ρ family. -/
noncomputable def entropicPotentialM (C : Matrix n n ℝ) : ℝ := -Real.log C.det

/-- Helper (mathlib has no direct statement): the trace of a real Hermitian
    matrix is the sum of its eigenvalues. Via the spectral theorem
    `A = U diag(λ) Uˣ` and cyclicity of the trace (`Uˣ U = 1`). -/
theorem trace_eq_sum_eigenvalues {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    A.trace = ∑ i, hA.eigenvalues i := by
  have hU : star (Matrix.IsHermitian.eigenvectorUnitary hA : Matrix n n ℝ)
      * (Matrix.IsHermitian.eigenvectorUnitary hA : Matrix n n ℝ) = 1 :=
    (mem_unitaryGroup_iff').mp (Matrix.IsHermitian.eigenvectorUnitary hA).2
  conv_lhs => rw [hA.spectral_theorem]
  rw [Matrix.trace_mul_comm, ← Matrix.mul_assoc, hU, Matrix.one_mul, Matrix.trace_diagonal]
  simp only [Function.comp_apply, RCLike.ofReal_real_eq_id, id_eq]

/-! ## T-C1 — Klein nonnegativity for an arbitrary correlation matrix -/

/-- T-C1 (nonnegativity). KLEIN INEQUALITY, GENERAL MATRIX FORM: for any PSD
    unit-diagonal `C` with `det C > 0`, the entropic potential is nonnegative,
    `0 ≤ S(C)`. Generalizes `entropicPotential_nonneg` (uniform-ρ only) to an
    ARBITRARY correlation matrix. Proof: the eigenvalues are positive (PSD +
    det > 0), sum to the trace `= k` (unit diagonal), and `log λ ≤ λ − 1` per
    eigenvalue gives `Σ log λ ≤ Σ(λ − 1) = 0`, i.e. `det C ≤ 1`. -/
theorem entropicPotentialM_nonneg {C : Matrix n n ℝ} (hC : C.PosSemidef)
    (hdiag : IsUnitDiag C) (hdet : 0 < C.det) : 0 ≤ entropicPotentialM C := by
  set e := hC.1.eigenvalues with he
  have hdet_eq : C.det = ∏ i, e i := by simpa using hC.1.det_eq_prod_eigenvalues
  have hev_ne : ∀ i, e i ≠ 0 := by
    intro i hi
    have hz : ∏ j, e j = 0 := Finset.prod_eq_zero (Finset.mem_univ i) hi
    rw [← hdet_eq] at hz; exact absurd hz (ne_of_gt hdet)
  have hev_pos : ∀ i, 0 < e i := fun i =>
    lt_of_le_of_ne (hC.eigenvalues_nonneg i) (Ne.symm (hev_ne i))
  have hlog : Real.log C.det = ∑ i, Real.log (e i) := by
    rw [hdet_eq, Real.log_prod _ _ (fun i _ => hev_ne i)]
  have hsum_le : ∑ i, Real.log (e i) ≤ ∑ i, (e i - 1) :=
    Finset.sum_le_sum (fun i _ => Real.log_le_sub_one_of_pos (hev_pos i))
  have htraceC : C.trace = (Fintype.card n : ℝ) := by
    have htr : C.trace = ∑ i, C i i := rfl
    have hd : ∀ i, C i i = (1 : ℝ) := hdiag
    rw [htr]
    simp only [hd, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
  have htrace : ∑ i, e i = (Fintype.card n : ℝ) := by
    rw [he, ← trace_eq_sum_eigenvalues hC.1, htraceC]
  have hsum_zero : ∑ i, (e i - 1) = 0 := by
    rw [Finset.sum_sub_distrib, htrace]
    simp [Finset.card_univ]
  unfold entropicPotentialM
  rw [hlog]
  linarith [hsum_le, hsum_zero]

/-- T-C1 (equality). The entropic potential of a PSD unit-diagonal correlation
    matrix vanishes IFF the matrix is the identity: `S(C) = 0 ↔ C = 1`. The chaos
    pole (zero correlation) is the unique zero of `S` on the correlation manifold,
    now for arbitrary `C` (cf. `entropicPotential_eq_zero_iff` for uniform-ρ).
    Forward: equality in `log λ ≤ λ − 1` forces every eigenvalue to `1`, and the
    spectral theorem reconstructs `C = U · 1 · Uˣ = 1`. -/
theorem entropicPotentialM_eq_zero_iff {C : Matrix n n ℝ} (hC : C.PosSemidef)
    (hdiag : IsUnitDiag C) (hdet : 0 < C.det) : entropicPotentialM C = 0 ↔ C = 1 := by
  constructor
  · intro h0
    set e := hC.1.eigenvalues with he
    have hdet_eq : C.det = ∏ i, e i := by simpa using hC.1.det_eq_prod_eigenvalues
    have hev_ne : ∀ i, e i ≠ 0 := by
      intro i hi
      have hz : ∏ j, e j = 0 := Finset.prod_eq_zero (Finset.mem_univ i) hi
      rw [← hdet_eq] at hz; exact absurd hz (ne_of_gt hdet)
    have hev_pos : ∀ i, 0 < e i := fun i =>
      lt_of_le_of_ne (hC.eigenvalues_nonneg i) (Ne.symm (hev_ne i))
    have hlog : Real.log C.det = ∑ i, Real.log (e i) := by
      rw [hdet_eq, Real.log_prod _ _ (fun i _ => hev_ne i)]
    have hlog_zero : ∑ i, Real.log (e i) = 0 := by
      have : Real.log C.det = 0 := by
        have := h0; unfold entropicPotentialM at this; linarith
      rw [hlog] at this; exact this
    have htraceC : C.trace = (Fintype.card n : ℝ) := by
      have htr : C.trace = ∑ i, C i i := rfl
      have hd : ∀ i, C i i = (1 : ℝ) := hdiag
      rw [htr]
      simp only [hd, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
    have htrace : ∑ i, e i = (Fintype.card n : ℝ) := by
      rw [he, ← trace_eq_sum_eigenvalues hC.1, htraceC]
    have hsum_zero : ∑ i, (e i - 1) = 0 := by
      rw [Finset.sum_sub_distrib, htrace]; simp [Finset.card_univ]
    -- g i := (e i − 1) − log (e i) ≥ 0, and Σ g = 0, so each g i = 0
    have hg_nonneg : ∀ i ∈ Finset.univ, 0 ≤ (e i - 1) - Real.log (e i) := by
      intro i _; linarith [Real.log_le_sub_one_of_pos (hev_pos i)]
    have hg_sum : ∑ i, ((e i - 1) - Real.log (e i)) = 0 := by
      rw [Finset.sum_sub_distrib, hsum_zero, hlog_zero, sub_zero]
    have hg_each := (Finset.sum_eq_zero_iff_of_nonneg hg_nonneg).mp hg_sum
    have hev1 : ∀ i, e i = 1 := by
      intro i
      by_contra hne
      have hlt := Real.log_lt_sub_one_of_pos (hev_pos i) hne
      have := hg_each i (Finset.mem_univ i)
      linarith
    -- spectral reconstruction: diag(ofReal ∘ e) = 1, so C = U · 1 · Uˣ = 1
    rw [hC.1.spectral_theorem]
    have hdiag1 : (diagonal (RCLike.ofReal ∘ hC.1.eigenvalues) : Matrix n n ℝ) = 1 := by
      have hfun : (RCLike.ofReal ∘ hC.1.eigenvalues) = (fun _ => (1 : ℝ)) := by
        funext i; simp [Function.comp, RCLike.ofReal_real_eq_id, ← he, hev1 i]
      rw [hfun]; exact diagonal_one
    rw [hdiag1, Matrix.mul_one]
    exact (mem_unitaryGroup_iff).mp (Matrix.IsHermitian.eigenvectorUnitary hC.1).2
  · intro h
    subst h
    simp [entropicPotentialM, Matrix.det_one]

/-! ## T-C0 bridge — the general functional restricted to the Kish family -/

/-- T-C0 (bridge). On the uniform-ρ family the general functional `entropicPotentialM`
    reduces to the closed form `entropicPotential`: `S(C(k,ρ)) = S(k, ρ)`. Grounds
    the closed-form two-pole potential of `Core.EntropicPotential` in the genuine
    matrix determinant (via the already-mechanized `entropicPotential_eq_neg_log_det`). -/
theorem entropicPotentialM_kishMatrix (k : ℕ) (hk : 1 ≤ k) (ρ : ℝ)
    (hρ0 : 0 ≤ ρ) (hρ1 : ρ < 1) :
    entropicPotentialM (kishMatrix k ρ) = entropicPotential (k : ℝ) ρ := by
  unfold entropicPotentialM
  exact (entropicPotential_eq_neg_log_det k hk ρ hρ0 hρ1).symm

/-! ## T-C3₂ — Oppenheim's inequality, the 2×2 explicit case -/

/-- T-C3₂. OPPENHEIM AT k = 2: for 2×2 unit-diagonal correlation matrices
    `C(a) = !![1,a;a,1]` and `C(b)` with `|a|, |b| ≤ 1`,
    `det(C(a) ∘ C(b)) ≥ det C(a)` — the Hadamard product contracts the
    off-diagonal, raising the determinant. `det(C(a)∘C(a)) ≥ det C(a)` (the
    Hadamard-SQUARE step of the C_g pipeline, clause (3) at n = 2) is `b = a`.
    General Oppenheim (any k, via Schur-complement induction) is roadmapped. -/
theorem oppenheim_two (a b : ℝ) (_ha : |a| ≤ 1) (hb : |b| ≤ 1) :
    (!![1, a; a, 1] ⊙ !![1, b; b, 1] : Matrix (Fin 2) (Fin 2) ℝ).det
      ≥ (!![1, a; a, 1] : Matrix (Fin 2) (Fin 2) ℝ).det := by
  obtain ⟨hb1, hb1'⟩ := abs_le.mp hb
  have hb2 : b ^ 2 ≤ 1 := by nlinarith [hb1, hb1']
  have hprod : (!![1, a; a, 1] ⊙ !![1, b; b, 1] : Matrix (Fin 2) (Fin 2) ℝ)
      = !![1, a * b; a * b, 1] := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.hadamard_apply]
  rw [hprod, Matrix.det_fin_two_of, Matrix.det_fin_two_of]
  nlinarith [sq_nonneg a, mul_nonneg (sq_nonneg a) (sub_nonneg.mpr hb2)]

end CoherenceRatchet.Core
