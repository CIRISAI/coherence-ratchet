/-
CoherenceRatchet.CMBOrthogonality
=================================

The orthogonality theorem. The soft post-selection operator P_ω leaves the bulk
CMB power spectrum exactly invariant; all of its content lives in the
within-multipole shape sector.

Demonstrated numerically in `experiments/open_system_pomega/
cmb_weak_value_spectrum.py`: with the linear low-ℓ CMB modes modelled as
Gaussian a_{ℓm} of variance C_ℓ (the ΛCDM forward prediction) and the soft
P_ω weight w = exp(-β H_sum), the per-multipole power C_ℓ and the penalty
H_sum have ensemble correlation 0.007 (MC noise floor 0.002), and the
reweighted C_ℓ equals the input C_ℓ at every β.

The two facts behind it, formalised here:

  PART A.  H_sum is built from ρ_ℓ, the per-multipole Kish correlation, read
  off the power participation ratio of the 2ℓ+1 mode amplitudes. The
  participation ratio is SCALE-INVARIANT — it depends only on the direction of
  the amplitude vector, not its length. Proved below.

  PART B.  For a Gaussian amplitude ensemble the length² (∝ C_ℓ, the power)
  and the direction (the shape) are statistically independent. Hence the
  weight w — a function of the scale-invariant shape — is independent of the
  power S, and the weak-value / reweighted expectation of S equals the
  unconditioned expectation. Proved below from the independence hypothesis;
  the hypothesis itself is the standard χ²-⊥-direction independence for
  Gaussian vectors (Fisher), cited not re-proved.

Corollary: C_ℓ^framework = C_ℓ^ΛCDM, exactly, at every multipole and every
coupling β. The framework is a strict extension of ΛCDM at the cosmological
tier — it cannot disagree with ΛCDM on the bulk power spectrum, and its
distinctive content is confined to the shape sector (ρ_ℓ drift).
-/
import Mathlib

namespace CoherenceRatchet.CMBOrthogonality

open Finset

/-! ## Part A — the participation ratio is scale-invariant -/

/-- The power participation ratio of an amplitude vector: `(Σ aᵢ²)² / (Σ aᵢ⁴)`.
    This is `k_eff` up to the Kish reparametrisation; ρ_ℓ is a function of it. -/
noncomputable def participation {n : ℕ} (a : Fin n → ℝ) : ℝ :=
  (∑ i, (a i) ^ 2) ^ 2 / (∑ i, (a i) ^ 4)

/-- The participation ratio depends only on the DIRECTION of the amplitude
    vector — rescaling every amplitude by a nonzero `c` leaves it unchanged.
    This is why H_sum (built from ρ_ℓ, a function of `participation`) carries
    no information about the overall power C_ℓ. -/
theorem participation_scale_invariant {n : ℕ} (c : ℝ) (hc : c ≠ 0)
    (a : Fin n → ℝ) :
    participation (fun i => c * a i) = participation a := by
  have h2 : ∑ i, (c * a i) ^ 2 = c ^ 2 * ∑ i, (a i) ^ 2 := by
    rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun i _ => by ring)
  have h4 : ∑ i, (c * a i) ^ 4 = c ^ 4 * ∑ i, (a i) ^ 4 := by
    rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun i _ => by ring)
  unfold participation
  rw [h2, h4]
  have hnum : (c ^ 2 * ∑ i, (a i) ^ 2) ^ 2 = c ^ 4 * (∑ i, (a i) ^ 2) ^ 2 := by
    ring
  rw [hnum, mul_div_mul_left _ _ (pow_ne_zero 4 hc)]

/-- Upper range bound. The participation ratio never exceeds the nominal mode
    count: `participation a ≤ n`. Cauchy–Schwarz on the vectors `(aᵢ²)` and
    `(1)` gives `(Σ aᵢ²)² ≤ n · Σ aᵢ⁴`. Together with `one_le_participation`
    this is the formal version of the corridor's outer wall: `participation`
    is the canonical k_eff shape observable, and k_eff lives between the
    rigidity floor 1 and the nominal constituent count n — "more constituents"
    caps, it does not escape. -/
theorem participation_le_card {n : ℕ} (a : Fin n → ℝ) :
    participation a ≤ n := by
  unfold participation
  rcases eq_or_lt_of_le (Finset.sum_nonneg fun i _ => by positivity :
      (0 : ℝ) ≤ ∑ i, (a i) ^ 4) with h | hpos
  · rw [← h, div_zero]
    exact Nat.cast_nonneg n
  · rw [div_le_iff₀ hpos]
    have h := sq_sum_le_card_mul_sum_sq (s := Finset.univ) (f := fun i => (a i) ^ 2)
    simpa [← pow_mul] using h

/-- Lower range bound. For a nonzero amplitude vector, `1 ≤ participation a`:
    since every `aᵢ⁴ = (aᵢ²)²` and the `aᵢ²` are nonnegative,
    `Σ aᵢ⁴ ≤ (Σ aᵢ²)²`. This is the rigidity floor — a single surviving mode
    (k_eff = 1) is the degenerate minimum of the k_eff shape observable, met
    exactly when all power concentrates in one amplitude. -/
theorem one_le_participation {n : ℕ} (a : Fin n → ℝ) (ha : a ≠ 0) :
    1 ≤ participation a := by
  have hpos : (0 : ℝ) < ∑ i, (a i) ^ 4 := by
    obtain ⟨j, hj⟩ := Function.ne_iff.mp ha
    have hj' : a j ≠ 0 := hj
    exact Finset.sum_pos' (fun i _ => by positivity)
      ⟨j, Finset.mem_univ j, (even_iff_two_dvd.mpr ⟨2, rfl⟩).pow_pos hj'⟩
  rw [participation, le_div_iff₀ hpos, one_mul]
  have h := sum_sq_le_sq_sum_of_nonneg (s := Finset.univ)
    (f := fun i => (a i) ^ 2) (fun i _ => sq_nonneg _)
  simpa [← pow_mul] using h

/-! ## Part B — reweighting by a shape-function preserves the power expectation -/

/-- Orthogonality theorem. If the post-selection weight `w` is statistically
    independent of the power observable `S` under the configuration ensemble
    `E` — `E (w·S) = E w · E S` — then the weak-value / reweighted expectation
    of `S` equals its unconditioned expectation.

    In the CMB application: `S` is the per-multipole power C_ℓ; `w = exp(-β
    H_sum)` is the soft P_ω weight; `H_sum` is a function of the scale-
    invariant `participation` (Part A), so `w` depends only on the shape; for
    a Gaussian amplitude ensemble shape ⊥ scale, which is exactly the
    independence hypothesis. The conclusion: P_ω leaves ⟨C_ℓ⟩ invariant. -/
theorem pomega_preserves_power {Ω : Type*}
    (E : (Ω → ℝ) → ℝ) (w S : Ω → ℝ)
    (indep : E (fun x => w x * S x) = E w * E S) (hw : E w ≠ 0) :
    E (fun x => w x * S x) / E w = E S := by
  rw [indep, mul_comm (E w) (E S), mul_div_assoc, div_self hw, mul_one]

/-- The framework's bulk CMB power spectrum equals ΛCDM's. With `C_lcdm := E S`
    the forward (ΛCDM) power and `C_framework := E (w·S) / E w` the soft-P_ω
    weak value, the orthogonality theorem gives them equal — no tuning, a
    consequence of `participation` being scale-invariant. -/
theorem framework_cmb_power_eq_lcdm {Ω : Type*}
    (E : (Ω → ℝ) → ℝ) (w S : Ω → ℝ)
    (indep : E (fun x => w x * S x) = E w * E S) (hw : E w ≠ 0) :
    E (fun x => w x * S x) / E w = E S :=
  pomega_preserves_power E w S indep hw

end CoherenceRatchet.CMBOrthogonality
