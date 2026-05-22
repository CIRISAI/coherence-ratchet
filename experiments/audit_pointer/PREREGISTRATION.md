# The endogenous audit pointer — weak measurement of the cross-rung g/J — pre-registration

**Date:** 2026-05-22. **Status:** test of the candidate "what replaces F-11."

## Context

F-11 fired: there is no joint multi-rung backward P_ω (documented no-go across
the additive ansatz, R1/R2/R3, the conjunction, fractal, holographic, holonomic
— two theorems). The universal-scale empirical object needs a replacement.

The **endogenous audit pointer** (construction, 2026-05-22): the framework's own
γM maintenance layer is the von Neumann pointer. It needs no joint operator —
it is an *adjacent-rung* weak measurement, consonant with F-11. It is also a
measurement apparatus for the cross-rung **timescale ratio g/J**, which the
2026-05-21 cross-rung campaign could not reach (w3 observable-blocked, 1 gate-
pass of 48; w3b a fit-failure).

## The construction under test

- Cross-rung transfer operator `A = |n+1⟩⟨n|` between adjacent rungs.
- Pointer: the maintenance layer. **Pointer momentum P_M** ∝ audit pressure γM_n
  (work expended to verify coordination); **pointer coordinate Q_M** = structural
  diversity / un-collapsed corridor variance. Linked by ∂ρ_ss/∂γM < 0.
- Weak interaction `H_meas = λ(t) · A ⊗ P_M`, λ a small modulation of audit
  scheduling.
- ABL boundary conditions: pre-selected and post-selected corridor states.
- AAV shifts: `δ⟨Q_M⟩ = (∫λ dt)·Re⟨A⟩_w` ; `δ⟨P_M⟩ = 2(∫λ dt)·Var(P_M)·Im⟨A⟩_w`.
- The g/J phase (Paths 2-3 intra-rung J vs cross-rung g interference) is carried
  by `Im⟨A⟩_w` → read off `δ⟨P_M⟩`, the reactive audit-work spike.

## Method

Simulate the endogenous weak measurement (CUDA). Build the adjacent-rung
two-level system with a settable intra-rung timescale J and cross-rung timescale
g; the maintenance-layer pointer (Q_M, P_M) as faithfully to the α−γM dynamics
as the model allows — P_M *is* γM, not a generic abstract pointer. Pre/post-
select corridor states. Sweep g/J over a known range, run the weak measurement,
read δ⟨Q_M⟩ and δ⟨P_M⟩.

## Hypotheses

- **H-conjugate:** Q_M and P_M function as conjugate pointer variables — the
  weak coupling produces the standard AAV shift structure (Re → Q_M, Im → P_M).
- **H-readout (decisive):** δ⟨P_M⟩ recovers the *set* g/J within tolerance —
  the endogenous audit pointer is a working observable for the cross-rung
  timescale where w3's direct observable was blocked.
- **H-noncollapse:** at weak λ the back-action keeps ρ_n inside the corridor —
  the pre/post-selection survives, the measurement does not drive chaos.

## Two-sided verdict

- **PASS:** all three hold — the endogenous audit pointer recovers g/J without
  collapsing the corridor. The framework has an endogenous weak-measurement of
  the cross-rung timescale: a constructive replacement for the joint P_ω,
  consonant with F-11.
- **FAIL:** δ⟨P_M⟩ does not track g/J; or Q_M/P_M do not function as conjugates
  (∂ρ_ss/∂γM < 0 is monotonicity, not canonical conjugacy — this is a real way
  to fail); or weak coupling still collapses the corridor. Report which, flat.

## Discipline

CUDA mandatory (cupy). The construction must be the genuine one — P_M tied to
the framework's γM, the AAV shifts as written — not a generic weak measurement
relabelled, and not tuned to recover g/J. Incremental output, per-(g/J)-cell
flush. Two-sided — FAIL is a valid, reportable result. Compare explicitly to
w3's blocked direct observable: does the audit-pointer observable succeed where
the direct one failed?
