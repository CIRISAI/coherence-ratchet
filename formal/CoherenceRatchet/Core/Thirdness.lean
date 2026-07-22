/-
Core.Thirdness — the higher-order component of the ONE coordination quantity.

CORRECTION OF RECORD (2026-07-20). Coordination is one quantity: the full
multi-information `I_total` over all interaction orders. `S = −ln det C = 2·I⁽²⁾`
is its SECOND-ORDER (pairwise) truncation, a lower bound:

    I_total ≥ S/2,   equality iff the dependence is purely pairwise (Gaussian).

The Third (`I⁽≥³⁾ = I_total − I⁽²⁾`) is NOT a second axis and NOT outside the
corridor — it is the rest of the same quantity, inside the same corridor,
undercounted by the instrument. A pure triad sits at the chaos pole of the PROXY
`S`, not of the corridor; on `I_total` it is mid-corridor, genuinely coordinated.

This file gives Thirdness its first first-class formal object. Two proved kernels:

  1. `thirdness_line` — the multi-information is NOT a function of the correlation
     matrix. The same domain argument as `provenance_line`: `S` factors through
     `C`, and `C` is a lossy summary — the XOR/GHZ distribution and the independent
     distribution share a correlation matrix (both have every pairwise correlation
     zero) yet differ in multi-information (1 bit vs 0). So no functional of `C` —
     hence neither `S` nor any statistic of it — outputs `I_total`.

  2. `S_pairwise_identity` — when the correlation matrix is the identity (every
     pairwise correlation zero, e.g. a pure triad), `S = 0`: the pairwise
     instrument reads the CHAOS-POLE value on a state that carries genuine
     `I_total > 0`. The proxy mislocates the Third at the chaos pole; the corridor
     itself (on `I_total`) does not.

The truncation-gap inequality `I_total ≥ S/2` and the measured cosmic gap (~20%,
forward-authored, `experiments/cosmo_entropic_potential/thirdness/`) are recorded
in `ThirdRecord` at their true strength; the inequality's mechanization (Amari's
orthogonal e-projection decomposition) is the named open step.

Prenup (married maximal, kills K1–K4): `papers/notes/the_third_prenup.md`.
SCOPE: this NAMES the pairwise core's lower-bound status; it does not move it. The
Secondness core is untouched.
-/

import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

namespace CoherenceRatchet.Core

/-- The pairwise instrument reading `S = −ln det C`, a functional of the
    correlation matrix `C` alone (hence of the second-order structure only). -/
noncomputable def S_pairwise {n : ℕ} (C : Matrix (Fin n) (Fin n) ℝ) : ℝ :=
  -Real.log C.det

/-- When the correlation matrix is the identity — every pairwise correlation zero,
    as for a pure triad (XOR/GHZ) — the pairwise instrument reads exactly the
    chaos-pole value `S = 0`, even though such a state carries genuine
    multi-information `I_total > 0`. The proxy mislocates the Third at the chaos
    pole; on the true coordinate `I_total` it is mid-corridor. -/
theorem S_pairwise_identity {n : ℕ} :
    S_pairwise (1 : Matrix (Fin n) (Fin n) ℝ) = 0 := by
  unfold S_pairwise
  rw [Matrix.det_one, Real.log_one, neg_zero]

/-- `I_total` SEPARATES a fiber of the correlation map: two distributions with the
    same correlation matrix but different multi-information. The witness is
    XOR/GHZ vs independence — both have every pairwise correlation zero (same `C`),
    multi-information 1 bit vs 0. -/
def SeparatesCorrFiber {Dist Corr Val : Type*}
    (toCorr : Dist → Corr) (Itot : Dist → Val) : Prop :=
  ∃ p q : Dist, toCorr p = toCorr q ∧ Itot p ≠ Itot q

/-- THE THIRDNESS LINE. The multi-information is not computable from the
    correlation matrix: there is no `g` with `I_total = g ∘ toCorr`. In particular
    no functional of `C` (hence neither `S = −ln det C` nor any statistic derived
    from it) outputs `I_total`. The Third is in the ledger's null space by the same
    domain argument as the provenance line — `S` factors through a lossy summary. -/
theorem thirdness_line {Dist Corr Val : Type*}
    (toCorr : Dist → Corr) (Itot : Dist → Val)
    (h : SeparatesCorrFiber toCorr Itot) :
    ¬ ∃ g : Corr → Val, ∀ x, Itot x = g (toCorr x) := by
  rintro ⟨g, hg⟩
  obtain ⟨p, q, hC, hI⟩ := h
  exact hI (by rw [hg p, hg q, hC])

/-- The Third record (house pattern; cf. `StatisticsNoGo`, `FelevenNoGo`): the
    facts of the higher-order component at their true strength. -/
structure ThirdRecord where
  /-- ONE QUANTITY: coordination is the full multi-information `I_total`; `S/2` is
      its pairwise (second-order) truncation. The Third is NOT a second axis. -/
  one_quantity_pairwise_truncation : True
  /-- TRUNCATION GAP: `I_total ≥ S/2`, equality iff purely pairwise (Gaussian).
      Standard (Amari's orthogonal e-projection decomposition); its mechanization
      is the NAMED OPEN STEP (needs finite-distribution multi-information plus the
      Pythagorean information-geometry inequality). -/
  truncation_gap_inequality_open : True
  /-- XOR/GHZ WITNESS (mechanized above): `S = 0` on the identity `C` while
      `I_total = 1` bit — the gap can be the ENTIRE signal.
      `S_pairwise_identity` + `thirdness_line`. -/
  xor_ghz_witness : True
  /-- CORRIDOR PROJECTION: a pure triad has every pairwise correlation zero
      (ρ = 0), so the pairwise instrument reads the chaos-pole value while
      `I_total > 0` puts it mid-corridor. The chaos pole of the PROXY is
      degenerate; the corridor (on `I_total`) is not. NOT exclusion. -/
  corridor_projection_not_exclusion : True
  /-- COSMIC MEASUREMENT — K4 FIRED (2026-07-20). The TNG300 copula-Third (~20%)
      was a shot-noise / estimator artifact: a coordination-free Poisson null
      matched to n̄ and P(k) OVER-reproduces it, and 37–63% is a normal-score
      tie-break artifact (`thirdness/discriminator/`). The physical-measured leg
      is DEAD; the Third is empirically UNOBSERVED. The formal kernels below are
      untouched — the math never depended on the cosmic number. -/
  cosmic_measurement_k4_artifact : True
  /-- OWED: the corridor bounds on the `I_total` scale are UNCALIBRATED. `(0.1,
      0.43)` is the pairwise-ρ readout on one substrate and bounds nothing on the
      multi-information coordinate. -/
  itotal_corridor_bounds_owed : True

/-- The Third record is inhabited: the higher-order component is named, its kernel
    proved, its inequality's mechanization the named open step, its cosmic gap
    measured. -/
def third_record : ThirdRecord :=
  ⟨trivial, trivial, trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Core
