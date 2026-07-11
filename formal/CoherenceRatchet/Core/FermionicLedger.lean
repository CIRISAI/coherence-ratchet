/-
Core.FermionicLedger — the fermionic coordination ledger and its EXCLUSION
DEFORMATION of the two-pole structure.

Companion to `Core.EntropicPotential`. There the bosonic ledger is
    S(k,ρ) = −ln det C(k,ρ) = −ln(1+ρ(k−1)) − (k−1)ln(1−ρ),
a two-pole potential whose rigidity pole DIVERGES (T-E1b: S → +∞ as ρ → 1⁻).

The fermionic ledger is the fermionic multi-information (total correlation) of a
uniform-coordination array of k fermionic modes. A fermionic Gaussian state is
fixed by its Majorana covariance (eigenvalues ±iν_j, ν_j ∈ [0,1]); the per-mode
entropy is
    h(ν) = −((1+ν)/2)ln((1+ν)/2) − ((1−ν)/2)ln((1−ν)/2) = binEntropy((1−ν)/2).
On the uniform half-filled family with collective polarization s = ν₀ ∈ [0,1]
(the exclusion-constrained order parameter; per-pair coherence c = s/(2(k−1)) is
capped by Pauli exclusion), the covariance spectrum is {ν₀ = s, ν₁ = s/(k−1)
with multiplicity k−1}, all single-mode marginals are maximally mixed (h = ln2),
so the multi-information is closed-form:

    I_F(k,s) = k·ln2 − h(s) − (k−1)·h(s/(k−1)).

The load-bearing contrast with the bosonic ledger (proved below):

  T-FL0   I_F(k,0) = 0                          chaos pole = the zero (as bosonic)
  T-FL1   0 ≤ I_F(k,s)                          nonnegativity (subadditivity)
  T-FL2   I_F(k,s) ≤ k·ln2                      **EXCLUSION CAP**: the rigidity end
                                                is FINITE — Pauli exclusion bounds
                                                the collective coherence at ν₀=1,
                                                so I_F cannot diverge. Contrast the
                                                bosonic T-E1b (S → +∞ at rigidity).
  T-FL3   I_F(k,1) = k·ln2 − (k−1)·h(1/(k−1))   exact value at the rigidity pole;
                                                → ln2 as k → ∞ (documented step).

Empirical/numerical companion: experiments/fermionic_ledger/ (search_log.md,
SUMMARY.md). There the cap I_F(k,1) → ln2 and the saturation law
dims_removed → (1 − h(s)/ln2)² are verified numerically and by sympy; the split
of the bosonic log-det/multi-information degeneracy is measured; and the bridge
to the classical instrument S = −ln det C is |Spearman| = 1.0 on the Kitaev chain.

SCOPE / F-11. Forward, engineering-tier content: a closed-form potential on a
closed-form spectrum. It does not touch the F-11 no-go on the joint multi-rung
backward P_ω. It is the fermionic-substrate reading of the SAME corridor object.
-/

import Mathlib.Analysis.SpecialFunctions.BinaryEntropy

namespace CoherenceRatchet.Core

open Real

/-- Per-mode fermionic (Majorana) entropy as a function of the covariance
    eigenvalue ν ∈ [0,1]: `h(ν) = binEntropy((1−ν)/2)`. `h(0)=ln2` (maximally
    mixed mode), `h(1)=0` (pure/frozen mode). -/
noncomputable def hFerm (ν : ℝ) : ℝ := binEntropy ((1 - ν) / 2)

/-- `h(0) = ln 2`: the maximally mixed mode carries one bit. -/
@[simp] theorem hFerm_zero : hFerm 0 = Real.log 2 := by
  unfold hFerm
  norm_num
  simp [binEntropy_two_inv]

/-- `h(1) = 0`: a pure (frozen) mode carries no entropy. -/
@[simp] theorem hFerm_one : hFerm 1 = 0 := by
  unfold hFerm
  norm_num

/-- `0 ≤ h(ν)` for ν ∈ [0,1]. -/
theorem hFerm_nonneg {ν : ℝ} (h0 : 0 ≤ ν) (h1 : ν ≤ 1) : 0 ≤ hFerm ν := by
  unfold hFerm
  apply binEntropy_nonneg <;> linarith

/-- `h(ν) ≤ ln 2`: no mode carries more than one bit — the fermionic bound that
    becomes the exclusion cap on coordination. -/
theorem hFerm_le_log_two (ν : ℝ) : hFerm ν ≤ Real.log 2 := by
  unfold hFerm; exact binEntropy_le_log_two

/-- The fermionic multi-information on the uniform-coordination family of `k`
    modes at collective polarization `s = ν₀ ∈ [0,1]`:
    `I_F(k,s) = k·ln2 − h(s) − (k−1)·h(s/(k−1))`. -/
noncomputable def fermionicMultiInfo (k s : ℝ) : ℝ :=
  k * Real.log 2 - hFerm s - (k - 1) * hFerm (s / (k - 1))

/-- T-FL0. CHAOS POLE IS THE ZERO: at `s = 0` the array is uncorrelated and the
    multi-information vanishes — the fermionic chaos pole, matching the bosonic
    `entropicPotential_at_zero`. -/
theorem fermionicMultiInfo_at_zero (k : ℝ) : fermionicMultiInfo k 0 = 0 := by
  unfold fermionicMultiInfo
  rw [zero_div, hFerm_zero]
  ring

/-- T-FL1. NONNEGATIVITY (subadditivity of entropy): `0 ≤ I_F(k,s)`. The joint
    entropy `h(s) + (k−1)h(s/(k−1))` never exceeds the marginal total `k·ln2`
    because each per-mode entropy is `≤ ln2`. -/
theorem fermionicMultiInfo_nonneg (k s : ℝ) (hk : 2 ≤ k)
    (_hs0 : 0 ≤ s) (_hs1 : s ≤ 1) : 0 ≤ fermionicMultiInfo k s := by
  have hkm1 : (0:ℝ) ≤ k - 1 := by linarith
  have h1 : hFerm s ≤ Real.log 2 := hFerm_le_log_two s
  have h2 : hFerm (s / (k - 1)) ≤ Real.log 2 := hFerm_le_log_two _
  have h3 : (k - 1) * hFerm (s / (k - 1)) ≤ (k - 1) * Real.log 2 :=
    mul_le_mul_of_nonneg_left h2 hkm1
  unfold fermionicMultiInfo
  nlinarith [h1, h3]

/-- T-FL2. **THE EXCLUSION CAP.** `I_F(k,s) ≤ k·ln2` for every `s ∈ [0,1]`,
    INCLUDING the rigidity end `s = 1`. Pauli exclusion bounds the collective
    coherence at `ν₀ = 1` (one frozen mode), so the fermionic ledger is finite on
    the whole domain — the sharp contrast with the bosonic rigidity pole, where
    `entropicPotential k ρ → +∞` as `ρ → 1⁻` (T-E1b). The fermionic rigidity pole
    is a finite frozen mode, not a divergence. -/
theorem fermionicMultiInfo_le_k_log_two (k s : ℝ) (hk : 2 ≤ k)
    (hs0 : 0 ≤ s) (hs1 : s ≤ 1) : fermionicMultiInfo k s ≤ k * Real.log 2 := by
  have hkm1 : (0:ℝ) ≤ k - 1 := by linarith
  have hsk0 : 0 ≤ s / (k - 1) := by positivity
  have hsk1 : s / (k - 1) ≤ 1 := by
    rw [div_le_one (by linarith)]; linarith
  have h_hs : 0 ≤ hFerm s := hFerm_nonneg hs0 hs1
  have h_hsk : 0 ≤ hFerm (s / (k - 1)) := hFerm_nonneg hsk0 hsk1
  have h_term : 0 ≤ (k - 1) * hFerm (s / (k - 1)) :=
    mul_nonneg hkm1 h_hsk
  unfold fermionicMultiInfo
  linarith

/-- T-FL3. RIGIDITY-POLE VALUE (exact): `I_F(k,1) = k·ln2 − (k−1)·h(1/(k−1))`.
    The collective mode freezes (`h(ν₀=1) = 0`) while the `k−1` residual modes,
    forced by exclusion to coherence `1/(k−1)`, carry the rest. Numerically (see
    experiments/fermionic_ledger) this tends to `ln2` as `k → ∞`: the maximal
    fermionic coordination of a single collective mode is one bit — the whole
    array cannot condense, exactly the Pauli statement. -/
theorem fermionicMultiInfo_at_one (k : ℝ) :
    fermionicMultiInfo k 1 = k * Real.log 2 - (k - 1) * hFerm (1 / (k - 1)) := by
  unfold fermionicMultiInfo
  rw [hFerm_one]
  ring

/-- The normalized coordination fraction of the collective mode,
    `μ(s) = 1 − h(s)/ln2 ∈ [0,1]`: `μ(0)=0` (chaos), `μ(1)=1` (rigidity). The
    fermionic Kish-analog saturation law (numerically + sympy verified in
    experiments/fermionic_ledger) is
        lim_{k→∞} [ k − k_eff(k,s) ] = μ(s)²  ≤ 1,
    i.e. exclusion caps the coordinative dimensional collapse at ONE effective
    dimension per collective mode — versus the bosonic Kish `k_eff → 1/ρ`, which
    removes `k − 1/ρ → ∞`. Stated here; the analytic limit is the named open step. -/
noncomputable def coordinationFraction (s : ℝ) : ℝ := 1 - hFerm s / Real.log 2

/-- `μ(0) = 0`: the chaos pole coordinates nothing. -/
@[simp] theorem coordinationFraction_zero : coordinationFraction 0 = 0 := by
  unfold coordinationFraction
  rw [hFerm_zero, div_self (by positivity)]
  ring

/-- `μ(1) = 1`: the rigidity pole fully coordinates the collective mode (which,
    by exclusion, removes exactly one effective dimension: `μ(1)² = 1`). -/
@[simp] theorem coordinationFraction_one : coordinationFraction 1 = 1 := by
  unfold coordinationFraction
  rw [hFerm_one, zero_div]
  ring

/-- The fermionic Kish-analog saturation law: the number of effective dimensions
    removed by coordination on the uniform family saturates (large `k`) at
    `μ(s)² ≤ 1` per collective mode. NAMED OPEN STEP: the `k → ∞` limit of the
    participation-ratio effective dimension `k_eff` equals `k − μ(s)²`; verified
    numerically to 5 digits and symbolically (sympy) in
    experiments/fermionic_ledger (`uniform_family.py`), not yet mechanized here.
    The bound `μ(s)² ≤ 1` — the exclusion cap on dimensional collapse — is
    immediate from `0 ≤ μ(s) ≤ 1`. -/
theorem coordinationFraction_sq_le_one (s : ℝ) (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    coordinationFraction s ^ 2 ≤ 1 := by
  have hb : hFerm s ≤ Real.log 2 := hFerm_le_log_two s
  have hn : 0 ≤ hFerm s := hFerm_nonneg hs0 hs1
  have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have h0 : 0 ≤ coordinationFraction s := by
    unfold coordinationFraction
    rw [sub_nonneg, div_le_one hl]; exact hb
  have h1 : coordinationFraction s ≤ 1 := by
    unfold coordinationFraction
    have : 0 ≤ hFerm s / Real.log 2 := div_nonneg hn (le_of_lt hl)
    linarith
  nlinarith [h0, h1]

end CoherenceRatchet.Core
