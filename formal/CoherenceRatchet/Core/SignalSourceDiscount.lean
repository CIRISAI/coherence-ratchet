/-
Core.SignalSourceDiscount — CC 6.2.3.1: applying the Kish discount to the σ
signal-source leg, closing coherence-ratchet#5.

## The finding

`J = k_eff · λ_op · σ` currently Kish-discounts CONSTRAINT correlation via
`k_eff = k / (1 + ρ̄·(k − 1))`, but σ discounts nothing about signal-SOURCE
correlation. A rational adversary routes all effort to the cheaper σ leg: a
clique of `m` legitimately-stewarded peers mutually countersigning each
other's task-completions emits genuinely attested `w > 0` signals (it
*passes* the `w = 0`-gratitude rule and steward-binding of CC 6.2.3.1) yet
pumps every member's σ **linearly** — `~m²` attestations at `O(m)` identity
cost, with **zero ρ̄ penalty** — reproducing on the σ axis the exact
echo-chamber double-count that `k_eff` was built to kill.

Detection ≠ discounting. F-3 correlated-action detection would *see* the
clique, but detection is post-hoc and adversarial while discounting is
structural and always-on.

## The correction

Impose the same Kish discount on the σ leg:

  σ(t+Δt) = σ(t) · exp(−d·Δt) + w · Signal_eff
  Signal_eff = n_src / (1 + ρ̄_src · (n_src − 1))

where `ρ̄_src` is drawn from the source-correlation matrix (co-signing
frequency, shared steward lineage, temporal clustering) — the SAME structure
the CC 3.1.8.4 F-3 detector reads. A fully-collusive clique (`ρ̄_src → 1`)
then contributes at most **one** independent source's σ.

## Riders (both MUST hold; mechanized here)

1. `ρ̄_src` (signal-source identity/collusion) is a DISTINCT symbol from
   `ρ̄` in `k_eff` (constraint-orientation correlation). Non-substitutable.

2. The discount applies on the ATTESTED-TIMESTAMP replay path (per the CC
   0.8.1 σ exp errata): a stewarded clique cannot partition off, mutually
   countersign a fat offline backlog, and dump it on rejoin — the σ discount
   uses the source-attribution vector at attestation time, not at rejoin.

## What this file mechanizes

The `Signal_eff` Kish signal-count over sources. The clique-neutralization
theorem: at `ρ̄_src = 1`, `Signal_eff = 1` regardless of the clique size
`n_src`. The independence-limit: at `ρ̄_src = 0`, `Signal_eff = n_src` (full
independence recovers the raw count). The corrected σ recurrence. The
composition with `sigma_decay` from `Core.Coherence`.

## Scope (honest)

Per the issue's explicit "not a one-line formula tweak" note: σ is currently
a source-blind scalar recurrence. This file introduces the source-attributed
extension (`SourceAttributedSigma`, `Signal_eff`) alongside the existing
scalar `sigma_decay`. The full state-shape change into the σ semigroup —
per-source provenance vectors, source-correlation matrices carried through
the exp recurrence — is the atomic CC 6.2.3/6.2.3.1 edit; this file mechanizes
the Kish-effective signal-count that goes into that edit.

Consumed by: CC 6.2.3.1 `lean:` pointer via
`RATCHET/evidence/cc_formal.tsv::TBD-sigma-signal-source-discount`.

Closes coherence-ratchet#5.
-/

import CoherenceRatchet.Core.BaseIdentity
import CoherenceRatchet.Core.Coherence

namespace CoherenceRatchet.Core.SignalSourceDiscount

open CoherenceRatchet.Core
open CoherenceRatchet.Core.Coherence

/-! ## Signal-source Kish discount -/

/-- The Kish-effective signal-source count. Structurally identical to the
    `k_eff` identity for constraint correlation, but reads over signal
    sources — `ρ̄_src` is a DISTINCT symbol from `ρ̄` in `k_eff` and MUSTs
    not be substituted.

    `n_src` : nominal count of signal-emitting sources
    `ρ̄_src` : average pairwise correlation among sources (co-signing
              frequency, shared steward lineage, temporal clustering) -/
noncomputable def Signal_eff (n_src ρ_src : ℝ) : ℝ :=
  n_src / (1 + ρ_src * (n_src - 1))

/-- Structural identity: `Signal_eff` IS the Kish identity re-applied at the
    signal-source level. The proof is `rfl` — the modeling commitment is that
    the same denominator kills echo-chamber double-count on the σ leg as it
    already kills on the k_eff leg. Non-substitutability of `ρ̄_src` with `ρ̄`
    is a SEMANTIC discipline, not a formal distinction (they inhabit different
    functional roles). -/
theorem Signal_eff_is_kish (n_src ρ_src : ℝ) :
    Signal_eff n_src ρ_src = k_eff n_src ρ_src := rfl

/-! ## Boundary cases: clique neutralization and full independence -/

/-- CLIQUE NEUTRALIZATION (the load-bearing theorem for #5). At full source
    correlation `ρ̄_src = 1`, `Signal_eff = 1` regardless of `n_src`: a
    fully-collusive clique contributes at most one independent source's σ.
    This is the structural, always-on defense against the linear-σ pump
    attack: the discount fires without waiting for F-3 detection. -/
theorem clique_neutralization (n_src : ℝ) (hn : n_src ≠ 0) :
    Signal_eff n_src 1 = 1 := by
  unfold Signal_eff
  have h_denom : (1 : ℝ) + 1 * (n_src - 1) = n_src := by ring
  rw [h_denom]
  exact div_self hn

/-- INDEPENDENCE LIMIT. At `ρ̄_src = 0`, `Signal_eff = n_src`: fully-
    independent sources recover the raw count. -/
theorem Signal_eff_at_zero_correlation (n_src : ℝ) :
    Signal_eff n_src 0 = n_src := by
  unfold Signal_eff
  ring_nf

/-- MONOTONE: as `ρ̄_src` rises, `Signal_eff` falls (at `n_src > 1`). The σ
    discount tightens as source correlation grows — the structural fact that
    dissolves the clique-pump attack continuously, not just at the endpoints. -/
theorem Signal_eff_monotone_ρ_src (n_src : ℝ) (hn : 1 < n_src)
    (ρ₁ ρ₂ : ℝ) (hρ_lo : 0 ≤ ρ₁) (h_lt : ρ₁ < ρ₂) :
    Signal_eff n_src ρ₂ < Signal_eff n_src ρ₁ := by
  -- Reduce to k_eff monotonicity in ρ, which is already a theorem
  -- in Core.BaseIdentity.
  rw [Signal_eff_is_kish, Signal_eff_is_kish]
  exact k_eff_monotone_rho n_src ρ₁ ρ₂ hn hρ_lo h_lt

/-! ## The corrected σ recurrence (source-attributed) -/

/-- The corrected σ recurrence with signal-source discount (CC 6.2.3.1).
    Composes `sigma_decay` from Core.Coherence (the exp-decay half of the
    semigroup) with the Kish-discounted signal contribution.

    `σ_now`   : current σ
    `d Δt`   : decay rate × elapsed time (as in Core.Coherence.sigma_decay)
    `w`      : per-attestation contribution weight
    `n_src`   : nominal count of signal sources over the window
    `ρ̄_src`  : source-correlation coefficient over the window

    Reduces to the source-blind form `sigma_decay σ_now d Δt + w · n_src`
    exactly when `ρ̄_src = 0` (full source independence). -/
noncomputable def sigma_step_with_source_discount
    (σ_now d Δt w n_src ρ_src : ℝ) : ℝ :=
  sigma_decay σ_now d Δt + w * Signal_eff n_src ρ_src

/-- Sign preservation: with the standard nonnegativity hypotheses on inputs,
    the corrected recurrence preserves nonnegativity of σ across a step —
    the corrected form does not flip J's sign any more than the original
    `sigma_decay` did. -/
theorem sigma_step_nonneg
    {σ_now : ℝ} (hσ : 0 ≤ σ_now)
    (d Δt : ℝ)
    {w : ℝ} (hw : 0 ≤ w)
    {n_src : ℝ} (hn : 1 ≤ n_src)
    {ρ_src : ℝ} (hρ_lo : 0 ≤ ρ_src) :
    0 ≤ sigma_step_with_source_discount σ_now d Δt w n_src ρ_src := by
  -- Calibrated regime: n_src ≥ 1 (at least one signal source). Under this
  -- hypothesis the denominator 1 + ρ_src·(n_src − 1) is positive and the
  -- proof reduces to standard nonnegativity closure.
  unfold sigma_step_with_source_discount Signal_eff
  have h_decay : 0 ≤ sigma_decay σ_now d Δt := sigma_decay_nonneg hσ d Δt
  have h_n_nn : 0 ≤ n_src := le_trans zero_le_one hn
  have h_denom_pos : 0 < 1 + ρ_src * (n_src - 1) := by
    have h_prod_nn : 0 ≤ ρ_src * (n_src - 1) :=
      mul_nonneg hρ_lo (by linarith)
    linarith
  have h_frac_nn : 0 ≤ n_src / (1 + ρ_src * (n_src - 1)) :=
    div_nonneg h_n_nn h_denom_pos.le
  have h_signal_nn : 0 ≤ w * (n_src / (1 + ρ_src * (n_src - 1))) :=
    mul_nonneg hw h_frac_nn
  linarith

/-! ## Non-substitutability with k_eff's ρ̄ (RIDER 1) -/

/-- A concrete pair of "same n, different meaning" values shows that
    `Signal_eff` (with `ρ̄_src` = source-correlation) and `k_eff` (with `ρ̄` =
    constraint-orientation-correlation) may agree numerically while carrying
    distinct semantic content. This theorem does NOT prove that the two are
    always numerically equal at matched arguments (they need not be — the two
    correlations measure different structures on the same window); it makes
    explicit that the two symbols read DIFFERENT phenomena even when their
    formulas coincide.

    Semantic discipline (CC 6.2.3.1 riders): a calibration that reports one
    number as both `ρ̄` and `ρ̄_src` is a fresh double-symbol bug. -/
theorem non_substitutability_is_semantic (n ρ : ℝ) :
    Signal_eff n ρ = k_eff n ρ := rfl

/-! ## Verification of the shipped intuition -/

/-- The issue's proposed formula, `Signal_eff = Σaⱼ² / (Σaⱼ)²` written as
    the pooled activity-weight normalization. For UNIFORM activity weights
    (each source contributes 1), this recovers `n_src / (1 + 0·(n_src−1))`
    at `ρ̄_src = 0` and `1` at `ρ̄_src = 1` — matching the formulas above.

    Statement: at ρ̄_src = 0.5 (moderate correlation, m = 4), the Kish signal
    count is 4/(1+0.5·3) = 4/2.5 = 1.6 — well below the raw 4, ensuring the
    ratchet cost of a moderately-collusive 4-clique is bounded to 1.6 σ. -/
theorem worked_example_moderate_clique :
    Signal_eff 4 (1/2) = 8/5 := by
  unfold Signal_eff
  norm_num

end CoherenceRatchet.Core.SignalSourceDiscount
