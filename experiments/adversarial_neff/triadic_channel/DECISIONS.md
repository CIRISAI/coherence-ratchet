# Triadic-deception channel — does the second law cover the Third, and is the Third invisible? (PRE-REGISTRATION)

**Date 2026-07-20. Method + thresholds frozen BEFORE any number was computed.**
THREAD 2 of the Third prenup (`papers/notes/the_third_prenup.md`), prediction 3 / kill K3:
the safety blind-spot leg. Discovery run under program discipline — blind, exhaustive
reporting, incremental flush, shuffled nulls for every estimate.

## The claim under test

Coordination is ONE quantity, the full multi-information `I_total`. The pairwise instrument
reads `S = −ln det C = 2·I⁽²⁾`, its second-order truncation (`I_total ≥ S/2`,
`Core/Thirdness.lean`). The Neff/CEG deception detector (`experiments/adversarial_neff/SPEC.md`,
`trace_harness/harness_neff.py`) is built on the **pairwise** correlation matrix: `Neff_PR`,
`ρ̄`, and the equicorrelation `k_eff` are all functionals of `C`. So the safety floor inherits
`S`'s blind spot. K3 asks two separable questions:

- **PRONG A (un-forgeable?):** does the program's second law ("deceit is never free" /
  no-free-coordination / DPI) extend from the mechanized PAIRWISE fragment
  (`FourLaws.entropicPotential_strictMono_k`, equicorrelation) to the FULL `I_total`? If yes,
  triadic coordination cannot be manufactured — the law covers the Third. Name the exact
  operation class for which it holds; name any condition under which it fails.
- **PRONG B (invisible?):** construct explicit purely-triadic coordinations and MEASURE the
  gap between what `I_total` sees and what the pairwise detector reads. Quantify how much
  genuine coordination hides at `S/2 ≈ 0`.

## PRONG A — the law-extension question (analysis + Lean stub)

Not a data run. Establish, with citation and precise operation class, whether `I_total` is
monotone non-increasing under local operations, and mechanize the reduction in Lean 4 /
Mathlib v4.14 to the extent the library allows (house style of `Core/Thirdness.lean` and
`FourLaws.RestrictedSecondLaw`: proved kernel + named open analytic step). The Lean file ships
ONLY if `lake build` is green.

**Decision rule (pre-committed):**
- **UN-FORGEABLE** iff `I_total` is provably monotone non-increasing under the class of
  operations relevant to a *local* attacker (each party/axis processed by its own channel,
  i.e. a product channel `⊗ᵢ Λᵢ`), from a standard theorem with citation.
- **CONDITIONALLY un-forgeable** iff monotonicity holds only under a named restriction — in
  which case the restriction is the load-bearing content and MUST be stated (e.g. "local ops
  only; a genuinely joint/global operation can create `I_total`").
- **FORGEABLE** iff no such monotonicity holds even for local ops.

## PRONG B — the blind-spot quantification (constructed distributions, no empirical data)

Constructed distributions demonstrating a mathematical fact (the XOR/GHZ witness generalized)
— explicitly permitted (not synthetic empirical data), same status as the CMB null ensembles
and the cosmic-thirdness phase-randomized surrogate.

### Scenario 1 — discrete parity family (exact, no estimation)

`n ∈ {3, 4, 5}` bits, uniform over the EVEN-PARITY subset (2ⁿ⁻¹ strings), then independent
symmetric bit-flip noise `ε ∈ {0, 0.05, 0.1, 0.2, 0.3, 0.5}` on each bit. Marginals stay
uniform; every pair stays independent uniform for all ε (bit-flip is a local channel that
preserves pairwise independence). Compute EXACTLY from the pmf:
- (i) `I_total` = TC = Σ H(Xᵢ) − H(joint), in bits.
- (ii) `S/2` = −½ ln det C on the Pearson correlation matrix C (nats; report bits too).
- (iii) pairwise detector: `Neff_PR` = (Σλ)²/Σλ² of C, `ρ̄` = mean off-diagonal, equicorr
  `k_eff`.
- (iv) synergy detectors: O-information sign (Rosas 2019; negative = synergy-dominated) and
  the triple-sign statistic ⟨s₁s₂s₃⟩ with sᵢ = 2Xᵢ−1 (a discrete copula 3-point), vs all
  pairwise ⟨sᵢsⱼ⟩.

### Scenario 2 — continuous sign-parity × amplitude (estimated, shuffle-null controlled)

`n = 3`. Signs `Uᵢ ∈ {±1}` drawn with a parity constraint held with probability `p ∈ {1.0,
0.9, 0.75, 0.6, 0.5}` (p=1 pure triad, p=0.5 independent); amplitudes `Aᵢ` iid half-normal;
`Xᵢ = Uᵢ·Aᵢ`. `Xᵢ` are pairwise independent by construction (so both linear-C AND copula-C are
identity). Sample `N = 200_000`. Compute:
- (i) `I_total` via binned plug-in (equal-frequency bins, `b = 8`/axis) with a per-column
  SHUFFLE NULL (independently permute each column, 200 shuffles) → report as z vs null and as
  bias-subtracted `I_total − null_mean`.
- (ii) `S/2` on the linear (Pearson) correlation matrix, and copula `S/2` on the normal-scored
  field (the exact object `S` reads).
- (iii) `Neff_PR`, `ρ̄`.
- (iv) copula 3-point ⟨g₁g₂g₃⟩ with `gᵢ` = normal score of `Xᵢ` (the cosmic-thirdness
  estimator, `experiments/cosmo_entropic_potential/thirdness/`), and all pairwise ⟨gᵢgⱼ⟩, each
  z-scored against the same shuffle null.

### Scenario 3 — the detector sketch

State and demonstrate the minimal upgrade that catches Scenarios 1–2: a multi-information /
higher-order-interaction probe over feature triples (`I_total` estimate + O-information sign +
copula 3-point), with shuffle nulls, added alongside the pairwise `Neff`. Map to a
reasoning-constraint trace: describe what a purely-triadic deception looks like across
constraint axes and which probe fires. State honestly whether the CEG *attestation* substrate
(cryptographic, not a correlation detector) is subject to the same blind spot.

## Decision rules (pre-committed)

- **INVISIBLE** (blind spot real) iff there exist constructed distributions with `I_total`
  bounded away from 0 (discrete: ≥ 0.1 bit exact; continuous: shuffle-null z ≥ 5) for which the
  pairwise detector is statistically indistinguishable from the independent baseline —
  operationally `|S/2| < 0.01` nat, `|ρ̄| < 0.02`, and `Neff_PR` within 2% of full rank n.
  Report the HIDDEN FRACTION `(I_total − S/2)/I_total`; invisible if ≥ 0.90 while `I_total` is
  non-vacuous.
- **VISIBLE** iff the pairwise detector departs from the independent baseline (by the above
  thresholds) whenever `I_total > 0` — i.e. the Third leaves an indirect pairwise signature.
  A VISIBLE result FIRES K3's blind-spot leg in the program's favour and is reported as such.
- **CATCHABLE** iff the Scenario-3 probe separates the coordinated (`I_total > 0`) from the
  independent case at z ≥ 5 where the pairwise detector reads zero. (Determines whether the
  floor can be *repaired*, distinct from whether it is currently blind.)

## Reading sideways (no outcome predicted)

- If the pairwise detector DOES catch the triadic deception (e.g. a determinant/eigenvalue
  perturbation at finite sample, or the copula-C picking up a signature), that VISIBLE result
  is the real finding — report it, K3's blind-spot leg does not fire.
- If PRONG A shows `I_total` is un-forgeable AND the Scenario-3 probe is catchable, the blind
  spot is a fixable *instrument* gap (build the probe), not an un-closeable hole — the honest
  and most likely truth. Both readings given in SUMMARY.

## Discipline

No synthetic empirical data — constructed distributions demonstrate a math fact only. Every
information estimate carries a shuffle null. Thresholds above are frozen at this commit;
nothing below is tuned after seeing the numbers. Incremental flush to `results.json`.
