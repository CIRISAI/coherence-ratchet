/-
Cosmology.CriticalityDiscriminator — the formal core of the
"criticality vs low-rank" discriminator.

  k_eff(k, ρ) = k / (1 + ρ(k-1))        (the Kish identity, Piece 1)

THE QUESTION. The corridor is an empirical band on the correlation ρ. Two rival
readings of *why* a coordinating system sits in that band make OPPOSITE
predictions about how the band-center ρ* scales with the system size k, and hence
about the large-k limit of the effective dimensionality k_eff:

  • LOW-RANK (the framework's claim, and the non-trivial one).
    The band-center is a genuine property of shared low-rank structure: ρ* does
    NOT shrink as k grows — it is pinned at some constant ρ₀ > 0. Then

        k_eff(k, ρ₀) → 1/ρ₀      (SATURATES / BOUNDED).

    Effective dimensionality has a hard ceiling — the Kish ceiling — no matter how
    many nominal constituents k you add. "More constituents" is a non-solution to
    coordination failure. This is the fingerprint of real shared structure.
    (Already proved in the lake: `k_eff_asymptotic_ceiling`, reused below.)

  • CRITICALITY (the trivial alternative, to be ruled out).
    The band is just the neighborhood of a critical point, where the correlation
    length diverges and correlations decay as a power law. Then the band-center
    dilutes with size, ρ*(k) ~ c/√k, and

        k_eff(k, c/√k) → +∞       (DIVERGES / UNBOUNDED).

    There is no ceiling: effective dimensionality grows without bound with k. This
    is the fingerprint of a critical point, NOT of low-rank shared structure.

THE DISCRIMINATOR is exactly the boundedness of the large-k limit of k_eff:
saturating (⟨ nhds (1/ρ₀) ⟩, this file's low-rank branch) versus divergent
(atTop, this file's criticality branch). Equivalently, in the empirical protocol:
the log-log slope of the band-center ρ* against k is 0 under low-rank (constant
ρ*) and -1/2 under criticality (ρ* ∝ k^{-1/2}). Measuring that slope decides
between the two.

This file is the formal core of ruling out the "corridor = criticality (trivial)"
hypothesis. The low-rank saturation branch is imported from the lake; the
criticality divergence branch (`criticality_scaling_diverges`) is proved here.

Empirical status (2026-07-02): the discriminator is proved AND the branch is now
read at TWO independent substrates — DECISIVELY, low-rank at both (C. elegans
whole-brain calcium; Drosophila EPG compass). See the two determination records
at the foot of this file. The earlier proxy reads were
inconclusive: a log-log fit of band-center ρ* against k over the clean substrates
is UNDERPOWERED (k spans ~1.7 decades; slope CI contains both 0 and -1/2) and
flips with the LLM-outlier and TCGA k-axis conventions; the directly-measured
k_eff stays bounded (~4-10) across the biological cluster, which only *leans*
low-rank. The decisive read goes at the mechanism instead of the proxy: the
covariance eigenvalue spectrum on raw C. elegans whole-brain calcium (Kato 2015,
12 worms, N up to 151 — the one in-tree substrate with raw traces). Through a
pipeline calibrated on synthetic controls (injected low-rank r=3 → β≈0.03;
power-law α=1.0 → 0.25; α=0.6 → 0.65; pure noise → 0.96), the measured
subsampling exponent is β = 0.10 ± 0.02 — its 95% CI excludes the entire
criticality band — with effective rank 1-3 across all 12 worms. The LOW-RANK
branch is selected; the criticality (trivial) reading is ruled out at C. elegans.
The determination is recorded below as `gate0_c_elegans_low_rank`. Scope is honest:
this is ONE substrate; the same spectral test on each substrate's raw data is the
cross-substrate verdict (`experiments/keff_saturation/spectral_test.py` is the
template). This theorem is the `if-then`; the spectral test reads the branch.
-/

import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Mathlib.Analysis.SpecialFunctions.Sqrt
import CoherenceRatchet.Core.BaseIdentity

open Filter Topology

namespace CoherenceRatchet.Cosmology

open CoherenceRatchet.Core

/-! ## The low-rank branch (imported)

Saturation is `k_eff_asymptotic_ceiling` from `CoherenceRatchet.Core.BaseIdentity`:
for fixed ρ₀ > 0, `Tendsto (fun k => k_eff k ρ₀) atTop (nhds (1/ρ₀))`. We restate
it here under the discriminator's name so both branches sit side by side. -/

/-- LOW-RANK BRANCH. Band-center pinned at a constant ρ₀ > 0 ⟹ k_eff saturates at
    the Kish ceiling 1/ρ₀. This is the bounded limit; the fingerprint of genuine
    low-rank shared structure. Direct reuse of the lake's asymptotic-ceiling
    theorem. -/
theorem lowrank_scaling_saturates (ρ₀ : ℝ) (hρ₀ : 0 < ρ₀) :
    Tendsto (fun k : ℝ => k_eff k ρ₀) atTop (nhds (1 / ρ₀)) :=
  k_eff_asymptotic_ceiling ρ₀ hρ₀

/-! ## The criticality branch (proved here)

Auxiliary: `Real.sqrt` tends to atTop, via `√x = x ^ (1/2)` and `tendsto_rpow_atTop`. -/

/-- `√·` diverges to +∞. -/
theorem tendsto_sqrt_atTop : Tendsto (fun k : ℝ => Real.sqrt k) atTop atTop := by
  have h : Tendsto (fun x : ℝ => x ^ (1 / 2 : ℝ)) atTop atTop :=
    tendsto_rpow_atTop (by norm_num)
  exact h.congr (fun x => (Real.sqrt_eq_rpow x).symm)

/-- CRITICALITY BRANCH. With the band-center diluting as ρ(k) = c/√k (c > 0),
    k_eff(k, c/√k) diverges to +∞ — no ceiling. This is the unbounded limit; the
    fingerprint of a critical point, ruling out low-rank structure.

    Proof. For k ≥ 1 the denominator 1 + (c/√k)(k-1) is at most (1+c)·√k, because
    1 ≤ √k and (c/√k)(k-1) ≤ (c/√k)(√k·√k) = c·√k. Hence

        k_eff(k, c/√k) = k / (1 + (c/√k)(k-1)) ≥ k / ((1+c)√k) = √k / (1+c),

    and √k/(1+c) → +∞. Combine the eventual lower bound with `tendsto_atTop_mono'`. -/
theorem criticality_scaling_diverges (c : ℝ) (hc : 0 < c) :
    Filter.Tendsto (fun k : ℝ => k_eff k (c / Real.sqrt k)) Filter.atTop Filter.atTop := by
  -- The eventual lower bound √k/(1+c) ≤ k_eff(k, c/√k).
  have key : ∀ᶠ k : ℝ in atTop,
      Real.sqrt k / (1 + c) ≤ k_eff k (c / Real.sqrt k) := by
    filter_upwards [Filter.eventually_ge_atTop (1 : ℝ)] with k hk
    have hk0 : (0 : ℝ) < k := lt_of_lt_of_le zero_lt_one hk
    have hs_pos : (0 : ℝ) < Real.sqrt k := Real.sqrt_pos.mpr hk0
    have hs_sq : Real.sqrt k * Real.sqrt k = k := Real.mul_self_sqrt (le_of_lt hk0)
    have hs_ge1 : (1 : ℝ) ≤ Real.sqrt k := by
      have h1 : Real.sqrt 1 ≤ Real.sqrt k := Real.sqrt_le_sqrt hk
      rwa [Real.sqrt_one] at h1
    have hcs : (0 : ℝ) ≤ c / Real.sqrt k := le_of_lt (div_pos hc hs_pos)
    have hkm1 : (0 : ℝ) ≤ k - 1 := by linarith
    -- Denominator D and its bounds.
    have hD_pos : (0 : ℝ) < 1 + (c / Real.sqrt k) * (k - 1) := by
      have : (0 : ℝ) ≤ (c / Real.sqrt k) * (k - 1) := mul_nonneg hcs hkm1
      linarith
    -- (c/√k)(k-1) ≤ c·√k.
    have step1 : (c / Real.sqrt k) * (k - 1)
        ≤ (c / Real.sqrt k) * (Real.sqrt k * Real.sqrt k) :=
      mul_le_mul_of_nonneg_left (by rw [hs_sq]; linarith) hcs
    have step2 : (c / Real.sqrt k) * (Real.sqrt k * Real.sqrt k) = c * Real.sqrt k := by
      field_simp
      linear_combination (-c) * hs_sq
    have h3 : (c / Real.sqrt k) * (k - 1) ≤ c * Real.sqrt k :=
      le_trans step1 (le_of_eq step2)
    have hD_le : 1 + (c / Real.sqrt k) * (k - 1) ≤ (1 + c) * Real.sqrt k := by
      calc 1 + (c / Real.sqrt k) * (k - 1)
          ≤ 1 + c * Real.sqrt k := by linarith [h3]
        _ ≤ Real.sqrt k + c * Real.sqrt k := by linarith [hs_ge1]
        _ = (1 + c) * Real.sqrt k := by ring
    -- Assemble: √k/(1+c) ≤ k/D.
    have h1c : (0 : ℝ) < 1 + c := by linarith
    have hb : Real.sqrt k * (1 + (c / Real.sqrt k) * (k - 1))
        ≤ Real.sqrt k * ((1 + c) * Real.sqrt k) :=
      mul_le_mul_of_nonneg_left hD_le hs_pos.le
    have hrw : Real.sqrt k * ((1 + c) * Real.sqrt k) = k * (1 + c) := by
      have h : Real.sqrt k * ((1 + c) * Real.sqrt k)
          = (1 + c) * (Real.sqrt k * Real.sqrt k) := by ring
      rw [h, hs_sq]; ring
    unfold k_eff
    rw [div_le_div_iff₀ h1c hD_pos]
    calc Real.sqrt k * (1 + (c / Real.sqrt k) * (k - 1))
        ≤ Real.sqrt k * ((1 + c) * Real.sqrt k) := hb
      _ = k * (1 + c) := hrw
  -- The lower bound √k/(1+c) diverges.
  have h_lb : Tendsto (fun k : ℝ => Real.sqrt k / (1 + c)) atTop atTop :=
    Tendsto.atTop_div_const (by linarith : (0 : ℝ) < 1 + c) tendsto_sqrt_atTop
  exact tendsto_atTop_mono' atTop key h_lb

/-! ## The discriminator

The two scaling regimes are distinguished by the boundedness of the large-k limit
of k_eff. The `Prop`-level statement below packages both branches: for any
constant band-center ρ₀ > 0 the low-rank branch saturates at nhds (1/ρ₀) (a
BOUNDED limit), while for any dilution constant c > 0 the criticality branch
diverges to atTop (an UNBOUNDED limit). Because a filter cannot converge to both
a point of nhds and to atTop, the observed limit type decides between the two
hypotheses.

Empirical reading: fit the band-center ρ* against system size k on a log-log axis.
Slope 0 (constant ρ*)  ⟺ low-rank / saturation branch (Kish ceiling 1/ρ₀).
Slope -1/2 (ρ* ∝ k^{-1/2}) ⟺ criticality / divergence branch (no ceiling). -/

/-- DISCRIMINATOR. Both branches, side by side: the low-rank band-center gives a
    bounded (point) limit `nhds (1/ρ₀)`; the criticality band-center gives an
    unbounded limit `atTop`. The boundedness of the k_eff limit is the test. -/
theorem discriminator (ρ₀ : ℝ) (hρ₀ : 0 < ρ₀) (c : ℝ) (hc : 0 < c) :
    Tendsto (fun k : ℝ => k_eff k ρ₀) atTop (nhds (1 / ρ₀)) ∧
    Tendsto (fun k : ℝ => k_eff k (c / Real.sqrt k)) atTop atTop :=
  ⟨lowrank_scaling_saturates ρ₀ hρ₀, criticality_scaling_diverges c hc⟩

/-! ## Empirical determination (2026-07-02): the branch is read at C. elegans

The discriminator above is an `if-then`. The record below is a flat fact with its
evidence — the first DECISIVE read of the branch, at the mechanism level, on raw
data. It follows the lake's no-go/record house pattern (cf. `FelevenNoGo` in
`Cosmology.CorridorProjector`): a `structure` whose fields name the load-bearing
evidence, inhabited by a `def`. It is NOT a proof that the world is low-rank
everywhere — it is one substrate, and the fields include that scope explicitly.
The proxy reads (ρ*-vs-k slope, cross-session k_eff) were inconclusive; this goes
at the covariance eigenvalue spectrum directly. See
`experiments/keff_saturation/{spectral_test.py, spectral_results.json,
spectral_discriminator.png}`. -/

/-- Gate-0 spectral determination. The criticality (trivial) hypothesis is ruled
    out at C. elegans; the low-rank (novel) branch is selected. -/
structure SpectralDetermination where
  /-- Raw whole-brain calcium traces are in-tree (Kato 2015, 12 worms, N ≤ 151):
      the spectrum is measured on data, not on a cross-substrate proxy. -/
  substrate_has_raw_traces : True
  /-- The β (PR-subsampling exponent) estimator is calibrated through the
      IDENTICAL pipeline on synthetic controls: low-rank r=3 → β≈0.03; power-law
      α=1.0 → 0.25; α=0.6 → 0.65; pure noise → 0.96. The hypotheses separate
      cleanly at the real data's (N, T). -/
  pipeline_calibrated_on_synthetic_controls : True
  /-- Measured β = 0.10 ± 0.02; the 95% CI excludes the entire criticality band
      (β ≳ 0.25). The divergent-k_eff / criticality branch is refuted here. -/
  beta_ci_excludes_criticality_band : True
  /-- Effective rank 1-3 across all 12 worms — small and size-independent: a few
      spikes over a flat noise bulk, the low-rank fingerprint (the bounded-k_eff /
      Kish-ceiling branch of `discriminator`). -/
  effective_rank_small_and_size_independent : True
  /-- Scope, stated in the record itself: ONE substrate (the in-tree raw one).
      The cross-substrate verdict needs the same test on each substrate's raw
      data; `spectral_test.py` is the template. -/
  scope_single_substrate : True

/-- Gate 0 is read at C. elegans: the low-rank determination record is inhabited.
    Low-rank (novel), not criticality (trivial) — by mechanism, calibrated, on raw
    data. β = 0.10 ± 0.02, effective rank 1-3 (Kato 2015, 12 worms, N ≤ 151). -/
def gate0_c_elegans_low_rank : SpectralDetermination :=
  ⟨trivial, trivial, trivial, trivial, trivial⟩

/-- SECOND substrate, independent phylum and mechanism: Drosophila EPG compass
    (ring-attractor) neurons, Mussells Pires 2024 (60D05, 20 flies × 9 trials,
    N = 32 EB-wedge ROIs). Same pipeline, calibrated at N=32 (where the low-rank
    synthetic control gives β≈0.12, the power-law controls 0.42/0.78, noise 0.99).
    Measured β = 0.122 ± 0.077 — 95% CI [0.110, 0.133], sitting on top of the
    low-rank control and far below the criticality band — with effective rank
    median 1 (range 0-2), the ring-attractor fingerprint. Low-rank, not
    criticality. The insect-compass read replicates the nematode whole-brain read
    at a mechanistically unrelated substrate.
    (`experiments/keff_saturation/spectral_drosophila.py`,
    `spectral_results_drosophila.json`.) -/
def gate0_drosophila_epg_low_rank : SpectralDetermination :=
  ⟨trivial, trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Cosmology
