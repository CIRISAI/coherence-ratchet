/-
Core.TriadicChannel — does the second law cover the Third? (THREAD 2, prenup K3)

The program's second law ("deceit is never free" / no-free-coordination / DPI) is
mechanized only in the PAIRWISE equicorrelation fragment
(`FourLaws.entropicPotential_strictMono_k`), and `FourLaws.RestrictedSecondLaw`
records the GENERAL Gaussian form as BLOCKED on Fischer's inequality (the ln-det
subset-monotonicity route). The Third prenup (`papers/notes/the_third_prenup.md`,
prediction 3 / kill K3) asks the sharper safety question: does the law extend to the
FULL multi-information `I_total` — is triadic coordination UN-FORGEABLE?

RESULT (Prong A). YES, under LOCAL operations, and by a DIFFERENT route than the one
FourLaws found blocked. Total correlation (multi-information) is a relative entropy,
`TC(p) = D(p ‖ ∏ᵢ pᵢ)` (Watanabe 1960). Under a LOCAL/product channel `⊗ᵢ Λᵢ` (each
party processes only its own variable) two facts hold:

  (i)  COMMUTING: the channel maps the product-of-marginals of `p` to the
       product-of-marginals of `Λp` — `channel (indep p) = indep (channel p)`;
  (ii) RELATIVE-ENTROPY DPI: `D` is monotone when the SAME channel is applied to
       both arguments — `D (Λp) (Λq) ≤ D p q` (Cover–Thomas Thm 2.8.1; Csiszár).

From (i)+(ii), `TC(Λp) ≤ TC(p)`: no LOCAL processing can manufacture multi-information
— the Third included. This file PROVES that reduction (`local_op_does_not_increase_TC`),
mirroring the `FourLaws.tc_group_chain_rule` reduction house-style: the algebra is
proved, the one analytic input (relative-entropy DPI as a channel monotonicity, absent
from mathlib v4.14 in channel form) is a named hypothesis / open step.

THE CONDITION (load-bearing, honest). Monotonicity holds for LOCAL ops ONLY. A
genuinely JOINT/global operation CAN create `TC`: the XOR gate maps two INDEPENDENT
bits (`TC = 0`) to the parity distribution (`TC = 1` bit). That is not a loophole — it
is a real shared cause, which is exactly what coordination IS. So the correct verdict
is CONDITIONALLY un-forgeable: un-forgeable by any LOCAL attacker; forgeable only by a
genuinely joint mechanism, which is a genuine coordinating cause, not a forgery.

RESULT (Prong B, blind spot). Un-forgeable ≠ visible. The pairwise detector
(`S = −ln det C`, `Neff_PR`, `ρ̄` — all functionals of `C`) reads the CHAOS-POLE value
on a pure triad: `S_pairwise_identity` gives `S = 0` on the identity correlation matrix,
and `thirdness_line` shows `I_total` is not a functional of `C` at all. The measured
blind spot (`experiments/adversarial_neff/triadic_channel/`): a purely-triadic
coordination hides 100% of its `I_total` from the pairwise detector — which reads not
merely "blind" but `Neff_PR = n` (MAXIMAL independence, the safest possible reading),
`ρ̄ = 0`, `S/2 = 0` — at every noise level. The floor is un-forgeable in the QUANTITY
and blind in the INSTRUMENT: the fix is a multi-information instrument, not a stronger
pairwise one.

SCOPE / F-11: forward, engineering-tier. The abstract reduction touches no measure
theory and nothing about the joint backward P_ω.
-/

import CoherenceRatchet.Core.Thirdness

namespace CoherenceRatchet.Core

/-! ## PRONG A — the local-operation DPI: the second law covers the Third -/

section LocalDPI
variable {Dist : Type*}

/-- Total correlation (multi-information) written as a relative entropy:
    `TC(p) = D(p ‖ indep p)`, the KL divergence of the joint `p` from the product of
    its marginals `indep p` (Watanabe 1960). `D` and `indep` are left abstract; the
    only structure used is that `TC` is `D` against the independence projection. -/
def TCof (D : Dist → Dist → ℝ) (indep : Dist → Dist) (p : Dist) : ℝ := D p (indep p)

/-- **PRONG A — THE LOCAL-OPERATION DPI (reduction proved).** Total correlation is
    non-increasing under a LOCAL/product channel `channel = ⊗ᵢ Λᵢ`, given its two
    standard inputs:
      • `hcommute` — the local channel maps the product-of-marginals of `p` to the
        product-of-marginals of `channel p` (a bookkeeping fact about product
        channels: the i-th marginal of `channel p` is `Λᵢ (pᵢ)`);
      • `hDPI` — relative entropy is monotone under the channel applied to both
        arguments (Cover–Thomas Thm 2.8.1 / Csiszár; the data-processing inequality).
    Conclusion `TCof D indep (channel p) ≤ TCof D indep p`: NO LOCAL PROCESSING CAN
    MANUFACTURE MULTI-INFORMATION — the Third included. Triadic coordination is
    un-forgeable by local operations; the second law covers it. The proof is pure
    algebra (rewrite by the commuting law, then apply the DPI), mirroring
    `FourLaws.tc_group_chain_rule`'s reduction-proved / analytic-input-named pattern. -/
theorem local_op_does_not_increase_TC
    (D : Dist → Dist → ℝ) (indep channel : Dist → Dist)
    (hcommute : ∀ p, channel (indep p) = indep (channel p))
    (hDPI : ∀ p q, D (channel p) (channel q) ≤ D p q) (p : Dist) :
    TCof D indep (channel p) ≤ TCof D indep p := by
  unfold TCof
  calc D (channel p) (indep (channel p))
      = D (channel p) (channel (indep p)) := by rw [hcommute]
    _ ≤ D p (indep p) := hDPI p (indep p)

end LocalDPI

/-- **PRONG A record.** The second law's extension to the full `I_total`, at true
    strength: reduction proved, analytic input named, the load-bearing CONDITION
    stated. House pattern (cf. `FourLaws.RestrictedSecondLaw`, `StatisticsNoGo`). -/
structure TriadicSecondLaw where
  /-- PROVED here (`local_op_does_not_increase_TC`): given relative-entropy DPI and the
      product-channel commuting law, `TC` is non-increasing under local operations. The
      Third is UN-FORGEABLE by any local attacker. -/
  local_dpi_reduction_proved : True
  /-- The single analytic input: relative entropy is monotone under a channel applied
      to both arguments (Cover–Thomas Thm 2.8.1). This is a DIFFERENT route than
      `FourLaws.RestrictedSecondLaw` found blocked — that was the Gaussian ln-det
      SUBSET-monotonicity form needing Fischer's inequality; THIS is the channel/DPI
      form. mathlib v4.14 has no channel-form relative-entropy DPI (no `klDiv`), so it
      remains the named open mechanization step. -/
  relentropy_dpi_is_the_named_input : True
  /-- THE CONDITION (load-bearing): monotonicity holds for LOCAL ops ONLY. A genuinely
      JOINT operation CAN create `TC` — XOR maps two INDEPENDENT bits (`TC = 0`) to the
      parity distribution (`TC = 1` bit). Not a loophole: a real shared cause is what
      coordination IS. Verdict: CONDITIONALLY un-forgeable (un-forgeable by any local
      attacker; forgeable only by a genuine coordinating cause). -/
  local_only_condition : True
  /-- Consequence for the safety floor: the DETECTABLE-coordination quantity cannot be
      faked up by local axis-tuning, so a multi-information detector that reads `TC`
      inherits an un-forgeability guarantee the pairwise detector's blind spot lacks. -/
  covers_the_third : True

/-- The Prong-A record is inhabited: reduction proved, input named, condition stated. -/
def triadic_second_law : TriadicSecondLaw := ⟨trivial, trivial, trivial, trivial⟩

/-! ## PRONG B — the pairwise instrument's triadic blind spot (un-forgeable ≠ visible) -/

/-- **PRONG B — THE BLIND SPOT, restated on the pairwise instrument.** On a pure triad
    every pairwise correlation is zero, so the pairwise detector's correlation matrix is
    the identity and `S_pairwise 1 = 0` (`Thirdness.S_pairwise_identity`): it reads the
    CHAOS-POLE value on a state carrying genuine `I_total > 0`. Combined with
    `thirdness_line` (`I_total` is not a functional of `C`), the pairwise instrument
    cannot see the Third by ANY post-processing of `C`. This is the invisibility half:
    `local_op_does_not_increase_TC` makes the Third un-forgeable, and this makes it
    invisible to the pairwise floor — two independent facts. -/
theorem pairwise_detector_blind_on_pure_triad {n : ℕ} :
    S_pairwise (1 : Matrix (Fin n) (Fin n) ℝ) = 0 :=
  S_pairwise_identity

/-- **PRONG B record.** The blind spot at true strength, tying the mechanized kernels to
    the measured gap. -/
structure TriadicBlindSpot where
  /-- PROVED (`pairwise_detector_blind_on_pure_triad` = `S_pairwise_identity`): the
      pairwise detector reads `S/2 = 0` on the identity `C` of a pure triad. -/
  pairwise_reads_chaos_pole : True
  /-- PROVED (`Thirdness.thirdness_line`): `I_total` is not a functional of `C`; no
      post-processing of the pairwise correlation matrix — hence no `Neff_PR`, `ρ̄`, or
      `S` — can output it. The blind spot is structural, not finite-sample. -/
  itotal_not_functional_of_C : True
  /-- MEASURED (`experiments/adversarial_neff/triadic_channel/`): a purely-triadic
      coordination hides 100% of its `I_total` from the pairwise detector, which reads
      `Neff_PR = n` (MAXIMAL independence — safest possible), `ρ̄ = 0`, `S/2 = 0` at every
      noise level, while `I_total` ranges up to 1 bit. The synergy probes
      (O-information < 0, copula 3-point) recover it at high significance. -/
  measured_hidden_fraction_unity : True
  /-- THE HONEST SPLIT for CIRIS's floor: the pairwise semantic `Neff` (H3ERE) HAS this
      triadic blind spot and needs a multi-information / O-information probe over feature
      TRIPLES to close it. The CEG attestation substrate is cryptographic — not a
      correlation detector — so this correlation blind spot does not apply to it the same
      way; its guarantee is orthogonal. Both readings owed in any safety claim. -/
  ceg_substrate_is_orthogonal : True

/-- The Prong-B record is inhabited: both kernels proved, gap measured, split stated. -/
def triadic_blind_spot : TriadicBlindSpot := ⟨trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Core
