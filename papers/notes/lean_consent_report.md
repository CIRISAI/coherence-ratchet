# Lean pass on the consent derivation — what is proved, defined, bookmarked

**Date 2026-07-11.** Formalization of `papers/notes/consent_derivation.md` in
`formal/CoherenceRatchet/Core/ConsentFoundation.lean` (additive to the lake;
`lake build` green top to bottom). The mission was to give the "four laws are the
preconditions of consent" reading a Lean spine at HONEST strength — proved where
proved, defined where definition-driven, bookmarked where empirical — plus the
one genuinely new provable result (K1). Below: the strength ledger, then the K1
statement verbatim.

## Placement

`Core/ConsentFoundation.lean`, namespace `CoherenceRatchet.Core.ConsentFoundation`.
Core (not Consciousness/Cosmology) because every object consumed is a Core object:
the provenance kernel (`Core.ProvenanceLine`), the Kish identity
(`Core.BaseIdentity`), the corridor (`Core.Corridor`), the four audited laws
(`Core.FourLaws`). This is the LAW-SIDE foundation of consent; the multi-agent
consent-corridor INSTANCE on goal projectors (`ρ_goals`, `isConsenting`) already
lives in `Cosmology.MultiAgentConsent` and is deliberately not duplicated.

## Axiom audit (`#print axioms`)

- `generator_underdetermined` (K1): **depends on NO axioms** — purely constructive.
- `consent_guarantees` (K3 inhabitant): only `propext, Classical.choice, Quot.sound`
  (Mathlib standard trio) — NO framework axioms; the four proved guarantees are
  genuinely discharged by the real lake theorems.
- `killsStep_injective` (K4): only `propext`.
- `corridor_is_consent_possible` (K2): standard trio + `Core.Corridor.corridorBounds`
  — the existing corridor primitive, appropriately (this is a theorem about the
  corridor). No new framework axioms are introduced anywhere in the file.

Zero `sorry` in code (the two "sorry" hits are the phrase "zero sorry" in docstrings).

## What is PROVED

| Item | Statement | Lake object reused |
|---|---|---|
| K1 generator underdetermination | no function of the observables computes the generator (Selection vs Intention) | `Core.provenance_line` verbatim |
| K2 k_eff ceiling | `k_eff k ρ ≤ 1/ρ` for `1≤k`, `0<ρ≤1` (`k_eff_le_inv_rho`) | `Core.k_eff`; matches `k_eff_asymptotic_ceiling` |
| K2 rigidity pole | consent impossible at ρ=1 (ceiling = 1, no margin clearable) | `Core.k_eff_at_one` cited |
| K2 corridor = consent-possible region | `inCorridor ρ ∧ 0<S ⇒ ConsentPossible ρ 0 S` | `Core.Corridor.corridor_bounds_well_formed` |
| K3 zeroth/definability | congruence of a coordination functional | `Core.provenance_congruence` |
| K3 first/attributability (identity half) | total-correlation group chain rule | `Core.tc_group_chain_rule` (labeled: identity, zero empirical content) |
| K3 second/securability (fragment) | adding a coordinated unit strictly increases S | `Core.add_unit_increases_S` (theorem-given-model, Kish family) |
| K3 third/recoverability (flavor) | `|J| ≤ J_max`, vanishing at the rigid pole | `Core.abs_jarlskog_le_max` |
| K4 separable-kill prenup | `killsStep` injective (distinct executioners) | — |

## What is DEFINITION-DRIVEN (theorems about defined terms, not derivations of the definitions)

- `OptionalityAchievable ρ margin := 1 + margin < optionalityCeiling ρ` — the Step-1
  identification optionality = k_eff, made precise. The rigidity-pole impossibility
  is a theorem GIVEN this definition, flagged as such in its docstring.
- `ConsentPossible ρ margin S := OptionalityAchievable ρ margin ∧ 0 < S`. Clause (ii)
  is why the chaos pole (S=0) fails — definition-driven, flagged. The physical fact
  ρ=0 ⇒ S=0 is cited (`Cosmology.EntropicInitialCondition`), not reproved.

## What is BOOKMARKED (honest `True` fields; NOT proved)

Inside `ConsentGuarantees`, three fields are visibly `True`, each citing its
registered bet — so the record cannot be read as "the lake proved consent":

- `first_lossless_conversion_bet` — lossless conversion X=1 (bet 6/10).
- `second_general_dpi_open` — full DPI, NAMED OPEN (Fischer's inequality absent from
  mathlib v4.14.0; `Core.RestrictedSecondLaw`).
- `third_ceiling_conditional_bet` — `σ_max ∝ (1−ρ)`, tyranny unmaintainable (bet 7).

Plus `grain_relativity_open_seam` (K5): Optionality is grain-relative through ρ (whose
k_eff?) — the consent analog of the Gibbs/grain problem, DECLARED open, not resolved.

## The K4 dependency map (machine-readable)

`killsStep : DerivationStep → RegisteredKill` routes each of the six derivation steps
to the kill that falsifies it (optionality→rigidity pole, deceitVoids→DPI failure,
persistenceRented→rent-free persistence, revocability→bet 7, commonAccount→no
substrate-independent S, attributability→bet 6). `killsStep_injective` proves the
executioners are distinct: one law falling falsifies exactly its own step — the hill
degrades leg-by-leg, not all-or-nothing.

## K1 — the theorem statement, verbatim

```lean
theorem generator_underdetermined {L : Type*} (obs : L) :
    ¬ ∃ g : L → Generator, ∀ w : World L, w.generator = g w.observables :=
  provenance_line (fun w : World L => w.observables) (fun w : World L => w.generator)
    (generator_upstream obs)
```

with `Generator := selection | intention` and `World L := { generator : Generator,
observables : L }`. Docstring corollary: the tenth bet (Selection vs Intention) is
IRREDUCIBLE — a wager by theorem, not by temperament; Pascal's-wager-as-corollary for
any universe whose laws are read only through their observables. Depends on no axioms.

## One-sentence honest summary

The lake now carries the four laws' consent-preconditions at their true strengths — a
provenance kernel, an accounting identity, an equicorrelation second-law fragment, a
Jarlskog flavor instance, and a genuinely new axiom-free theorem that the derivation's
own generator (Selection vs Intention) is uncomputable from the observables — but it
does NOT prove "consent," which rests additionally on three registered empirical bets
and a declared grain-relativity seam, all bookmarked as such.
