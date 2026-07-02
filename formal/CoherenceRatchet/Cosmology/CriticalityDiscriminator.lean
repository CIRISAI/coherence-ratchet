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
read across several substrates — with a CRUCIAL grain qualification that is the
real content of this update.

  LOW-RANK, read at COMPLETE coordinating units (records at the foot of this file):
  C. elegans whole-brain calcium (~50% of the 302-neuron nervous system),
  Drosophila EPG compass (the whole ring-attractor circuit), the S&P-100 return
  correlation spectrum (the non-neural adversarial case; criticality/power-law was
  the competing prediction, the measured spectrum is instead the RMT
  market-mode-plus-noise-bulk), and — THE DECISIVE TEST — a COMPLETE larval
  zebrafish brain (ZAPBench, all 71,721 neurons of an entire vertebrate brain,
  where grain cannot be invoked). Its k_eff saturates dead-flat to the full N
  (β≈0), WITHIN single visual conditions as well as whole-recording (so intrinsic,
  not stimulus-driven), with CV power-law α≈1.4-1.6 (steep = saturating/low-rank,
  decisively distinct from cortex's shallow α≈0.97) and genuine coordination (4-10
  modes above the autocorrelation floor, vs cortex's ~0). A complete unit that
  fails to saturate would have falsified the corridor claim for vertebrate brains;
  it saturates. Corroborating, agent-run through the identical
  pipeline: resting-state fMRI at a complete ~200-region cortical partition
  (β≈0.06) and TCGA transcriptomes (spectrum-only) — both low-rank. The fMRI
  result is averaging-null-controlled: real region k_eff (median 8.0) is 4.3× below
  an independent-AR(1) averaging null (≈35), 139/139 subjects — the region-level
  low-rank is genuine cross-region coordination, NOT a coarse-graining artifact
  (67% strictly in the (2.3,10) corridor).

  NOT low-rank, at an INCOMPLETE subsample: mouse V1 two-photon (~200 of ~1e8
  neurons, a sparse field-of-view of a sensory representational patch — NOT a
  complete coordinating unit). The RAW k_eff (up to 44-59, above the corridor
  ceiling) is noise-inflated; after cross-validation (block-interleaved, validated
  rank-3→3 / noise→0) the noise-free k_eff median is only ~4.8 (21 sessions,
  even BELOW a pure-noise null's ~11), so a few dominant modes carry the variance
  and by LEVEL it looks corridor-sized. But the SATURATION reads reveal the truth
  the level hides: the CV eigenspectrum is a power law with exponent α median 0.97
  (95% CI [0.88, 1.22] over 16 fittable sessions — matching Stringer 2019 mouse-V1
  α≈1.04), whose participation ratio GROWS with N (β=0.83), i.e. NON-saturating. So
  cortex-at-neuron-grain is a few dominant modes over a non-saturating scale-free
  tail = genuinely HIGH-DIMENSIONAL, NOT low-rank — the participation-ratio LEVEL
  (~5) MISLEADS (PR is a poor discriminator for a power law) and only saturation/α
  classifies it (a live validation of "saturation not level"). It is distinguishable
  from pure noise (α≈1 vs the noise null's α≈0), so it is genuine scale-free
  structure, not noise. Caveat: ~0 CV dims exceed the per-neuron autocorrelation
  surrogate floor, so cross-neuron coordination above single-neuron structure is
  weak; and the CV dim COUNT is method- and N-sensitive — α is the stable readout.
  (A parallel agent verdict of "low-rank, rescue holds" is a level-trap misread,
  annotated as superseded in spectral_allen_cv_summary.md.)
  Recorded below as a SCOPE finding (`cortex_grain_and_objective_measure`), NOT a
  low-rank determination and NOT a falsification — see that record for why the
  disqualification is outcome-independent and what the objective measure is. The earlier proxy reads were
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

/-- THIRD substrate, and the first that is BOTH non-neural AND adversarial: the
    S&P-100 daily-return cross-correlation spectrum (N=101 stocks × T=1506 trading
    days, yfinance). Financial markets carry a "criticality" reputation, so a
    power-law spectrum was the live competing prediction here. Instead the measured
    spectrum is the textbook random-matrix-theory structure (Laloux/Bouchaud 1999;
    Plerou 2002): ONE giant market mode (largest eigenvalue = 28% of total
    variance) + a handful of sector modes above the Marchenko-Pastur edge + a noise
    bulk holding 92% of the eigenvalues. Effective rank 8 (small), β = 0.153 —
    between the N=101 low-rank control (0.049) and the α=1.0 power-law control
    (0.243), far below the α=0.6 criticality control (0.657). Low-rank, not
    criticality. This substrate doubles as a pipeline validation: the discriminator
    recovers the KNOWN published spectrum of a non-neural system.
    (`experiments/keff_saturation/spectral_finance.py`,
    `spectral_results_finance.json`.) -/
def gate0_sp500_low_rank : SpectralDetermination :=
  ⟨trivial, trivial, trivial, trivial, trivial⟩

/-- THE DECISIVE COMPLETE-UNIT TEST: a complete larval zebrafish brain (ZAPBench,
    Immer 2025 / Ahrens-Engert data; all 71,721 neurons of an entire vertebrate
    brain). This is the one case where the grain escape is unavailable — you cannot
    subsample a bigger unit than the whole brain — so it can CONFIRM or FALSIFY
    without the grain caveat that neutralized mouse-V1. Result: k_eff SATURATES.
    The subsampling PR is dead flat at ~34 (whole-recording) from N'=500 to the full
    71,721 (β≈0); a power law would have grown (α=1 predicts ~3× growth over this
    range). WITHIN each of the 3 longest single visual conditions it still saturates
    (β≈0, PR flat), so the low-rank is INTRINSIC, not an artifact of switching among
    the 9 stimulus conditions. CV (noise-removed) power-law α = 1.42/1.63/1.56 across
    conditions — STEEP (>1 ⇒ PR converges ⇒ saturating/low-rank), decisively unlike
    cortex's shallow α≈0.97 (borderline, non-saturating). Noise-free k_eff ~6-16
    (2 of 3 conditions inside the (2.3,10) corridor); 4-10 modes above the
    per-neuron autocorrelation floor (genuine coordination; cortex had ~0). Honest
    caveat: the saturation LEVEL is state/substrate-specific (raw 17-46, noise-free
    6-16) — the universal invariant is SATURATION + steep α, not the specific band.
    (`experiments/keff_saturation/zebrafish_finalize.py`,
    `spectral_results_zebrafish{,_condition}.json`.) -/
def gate0_zebrafish_complete_vertebrate_low_rank : SpectralDetermination :=
  ⟨trivial, trivial, trivial, trivial, trivial⟩

/-! ## The objective measure, and the grain qualification (2026-07-02)

The mouse-V1 read (high-dimensional, dimensionality growing with the number of
neurons sampled) forced the question: if a high-dimensional read can be set aside
as "the wrong grain," what stops that from being an unfalsifiable escape hatch?
The answer is an OBJECTIVE, PRE-SPECTRAL criterion for what counts as a valid test.

THE OBJECTIVE MEASURE is SATURATION, not level. The framework's own claim (Piece 1)
is that effective dimensionality SATURATES at the Kish ceiling 1/ρ as constituents
are added — that IS the low-rank branch of `discriminator`, and empirically it is
the subsampling exponent β→0 (the PR-vs-N curve flattens). So the test for "is this
a genuine coordinating unit occupying the corridor?" is: does k_eff SATURATE as you
add constituents? The LEVEL of k_eff is grain-tunable and proves nothing on its own;
the SATURATION of k_eff is intrinsic. β→0 = saturating = the unit's dimensionality
is captured and bounded (low-rank). β bounded away from 0 = not saturating = either
a fragment of a larger system OR genuinely high-dimensional/critical.

WHY THIS IS NOT CIRCULAR. Saturation must be tested on a COMPLETE unit — all or a
large fraction of the constituents of a bounded, functionally-closed system, or a
complete partition of it. Completeness is a STRUCTURAL, pre-spectral property, fixed
before any spectrum is computed. It admits worm whole-brain, fly compass, market,
fMRI region-partition; it excludes the mouse-V1 subsample REGARDLESS of what that
subsample's spectrum says (a subsample's k_eff is not the unit's — Stringer 2019:
V1 dimensionality is sample-size-dependent, no saturation to 10^4 neurons). The
disqualification is outcome-independent: a low-rank read on that subsample would
have been rejected for the same reason.

THE FALSIFICATION PATH that keeps it honest: a system that IS a complete unit and
whose k_eff FAILS to saturate (β high up to the full constituent count) falsifies
the corridor claim for that substrate. Larval zebrafish whole-brain light-sheet
(~all ~10^5 neurons of an entire vertebrate brain) is the clean decisive case: it
is complete, so grain cannot be invoked. Saturation ⇒ strong confirmation;
non-saturation ⇒ falsification. This is the highest-value next dataset.

TWO CONTROLS this criterion still owes (open):
  (i) coarse-grained substrates (fMRI regions = averages of ~10^3 neurons) must
      beat an AVERAGING NULL — random-neuron-averaging into the same region count —
      to show the low-rank is structure, not a mechanical consequence of averaging.
  (ii) "complete" for an open/large system (the S&P-100 is 100 of ~4000 US equities)
      is a matter of degree; the airtight version subsamples the full constituent
      set. S&P-100 saturation is suggestive, not airtight, by this same criterion. -/

/-- Grain qualification + the objective measure. A flat fact with its evidence:
    the valid-test criterion is k_eff SATURATION on a COMPLETE coordinating unit
    (β→0), a structural pre-spectral property — not the level of k_eff, which is
    grain-tunable. The mouse-V1 subsample is high-dimensional but is the wrong grain
    (outcome-independently); the region-grain fMRI partition is low-rank. Kept
    honest by a falsification path (a complete unit that fails to saturate) and two
    owed controls (averaging-null; full-constituent completeness). -/
structure GrainAndObjectiveMeasure where
  /-- The objective measure is SATURATION of k_eff under subsampling (β→0), the
      low-rank branch of `discriminator` — NOT the level of k_eff. Validated by
      cortex: its noise-free k_eff LEVEL is ~5 (looks corridor) yet its CV spectrum
      is a Stringer power law α≈1.0 (β high) — the level misleads, saturation does
      not. Participation ratio is a POOR discriminator for a power-law spectrum. -/
  measure_is_saturation_not_level : True
  /-- Validity requires a COMPLETE unit (all/most constituents of a bounded
      functionally-closed system, or a complete partition): structural, pre-spectral. -/
  completeness_is_structural_and_pre_spectral : True
  /-- Mouse-V1 2p is a sparse subsample → high-dimensional (CV power law α≈1.0,
      Stringer; level-k_eff ~5 misleads) → excluded as wrong grain,
      OUTCOME-INDEPENDENTLY, whatever the subsample's dimensionality reads. -/
  cortex_neuron_subsample_wrong_grain : True
  /-- The coordinating grain of a large brain is regions; fMRI at a complete
      ~200-region partition reads low-rank (corroborating, agent-run). -/
  region_grain_partition_low_rank : True
  /-- Falsifiable: a COMPLETE unit whose k_eff fails to saturate falsifies the
      corridor at that substrate. RUN on larval zebrafish whole-brain (all 71,721
      neurons) — it SATURATES (β≈0 to full N, intrinsic within single conditions,
      CV α≈1.5 steep), so the decisive complete-vertebrate-unit test CONFIRMS rather
      than falsifies. See `gate0_zebrafish_complete_vertebrate_low_rank`. -/
  falsification_path_complete_unit_no_saturation : True
  /-- Controls: (i) DISCHARGED for ABIDE fMRI — real region k_eff (median 8.0) is
      4.3× below an averaging null (200 independent AR(1) region signals matched to
      per-region autocorrelation+variance, k_eff≈35), 139/139 subjects below the
      null: genuine cross-region coordination, not a coarse-graining artifact.
      (ii) still open: "complete" is a matter of degree (S&P-100 ⊂ full market). -/
  owed_controls_averaging_null_and_full_completeness : True

/-- The grain qualification is recorded: the objective measure is complete-unit
    k_eff saturation, kept falsifiable and with its controls named. -/
def cortex_grain_and_objective_measure : GrainAndObjectiveMeasure :=
  ⟨trivial, trivial, trivial, trivial, trivial, trivial⟩

/-! ## The cosmological grain limit (2026-07-02)

The adversarial cosmic-structure probe (SDSS DR17, 389,751 galaxies; the unit×unit
matrix is the two-point density covariance whose eigenvalues are the discrete P(k)
modes) reads NON-SATURATING / POWER-LAW: PR climbs to 52 with no plateau, β≈0.57,
α≈0.75 (smooth power-law decay, robust across grid scales) — the near-scale-invariant
P(k) (n_s≈0.96) showing through, exactly the adversarial signature for this substrate.
This is NOT the CMB (orthogonality theorem stands — the framework is exactly ΛCDM
there); it is emergent large-scale structure.

The honest reading is a two-part epistemic limit, NOT a falsification and NOT a
confirmation:
  (1) The power-law read is GRAIN-INCONCLUSIVE, outcome-independently: a galaxy
      survey is a finite past-light-cone subsample of the universe, and a subsample's
      k_eff is not the whole's (a low-rank read would have been equally inconclusive).
  (2) DEEPER: for cosmology a COMPLETE-unit test is impossible IN PRINCIPLE — the
      universe cannot be observed whole — so the corridor claim is cosmologically
      UNTESTABLE by the saturation criterion. The measure that decisively confirmed
      the corridor up to a complete vertebrate brain cannot reach the universal
      scale. This is consistent with F-11 having already closed the joint multi-rung
      backward P_ω; the surviving forward P_ω corridor is operationally defined
      (`CorridorProjector.OperationalCorridorOccupation`) but, at the cosmological
      rung, unmeasurable. -/

/-- Cosmological grain limit. A flat fact with its evidence: the corridor claim is
    empirically decisive at complete units up to a whole vertebrate brain, but at the
    universal scale it is untestable by the saturation criterion — a complete-unit
    test is impossible in principle, and the one measurable subsample (the cosmic web)
    reads adversarially power-law (grain-inconclusive, not a falsification). -/
structure CosmologicalGrainLimit where
  /-- Emergent cosmic structure (SDSS density covariance = P(k) modes) reads
      power-law/non-saturating (α≈0.75, β≈0.57) — the scale-invariance signature. -/
  cosmic_web_reads_power_law : True
  /-- Grain-inconclusive, OUTCOME-INDEPENDENTLY: a survey is a past-light-cone
      subsample; a low-rank read would have been equally inconclusive. -/
  power_law_is_grain_inconclusive_not_falsification : True
  /-- A COMPLETE-unit test is impossible in principle for the universe ⇒ the corridor
      claim is cosmologically UNTESTABLE by saturation. An honest limit, not a dodge. -/
  complete_unit_test_impossible_in_principle : True
  /-- NOT the CMB (orthogonality/ΛCDM stands); consistent with F-11 closing the joint
      backward P_ω. The forward P_ω corridor is defined but unmeasurable at this rung. -/
  not_cmb_and_consistent_with_f11 : True

/-- The cosmological grain limit is recorded. -/
def cosmological_grain_limit : CosmologicalGrainLimit :=
  ⟨trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Cosmology
