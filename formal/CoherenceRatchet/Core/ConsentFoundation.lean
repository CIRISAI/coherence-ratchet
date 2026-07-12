/-
Core.ConsentFoundation — the four laws as the preconditions of consent,
formalized maximally-honestly (papers/notes/consent_derivation.md).

The derivation's premise is "consent is possible"; its claim is that the four
laws of coordination thermodynamics ARE the four guarantees consent needs, and
that the corridor is the consent-possible region. This module gives that reading
a Lean spine at HONEST strength — proved where proved, defined where
definition-driven, bookmarked where empirical — and adds one theorem that is new
and fully provable: the UNDERDETERMINATION of the derivation's own generator.

Contents (priority order of the mission):

  K1  THE UNDERDETERMINATION THEOREM (proved, zero sorry). The generator of a
      consent-shaped law-structure — Selection vs Intention — is not computable
      from the observables. Direct reuse of `Core.provenance_line`: two worlds
      with identical observables and different generators are an `Upstream`
      witness, so no function of the observables outputs the generator. The
      tenth bet is therefore IRREDUCIBLE by theorem, not by temperament —
      Pascal's-wager-as-corollary for any universe read only through its laws.

  K2  THE POLE THEOREMS. (a) Rigidity: `k_eff → 1` as ρ → 1 (exact bound
      `k_eff_le_inv_rho`, and `k_eff_at_one`), so with Optionality DEFINED as
      the k_eff-ceiling exceeding 1+margin, consent is impossible at ρ = 1.
      (b) Chaos: at S = 0 there is no shared object to consent TO
      (definition-driven). Together: the corridor is the consent-possible
      region — a theorem about the DEFINED terms (dependence made explicit).

  K3  THE FOUR-GUARANTEES RECORD. `ConsentGuarantees` ties each law to its
      consent role at its ACTUAL lake strength. Proved guarantees are real
      propositions the constructor must discharge with the real lake theorems
      (`provenance_congruence`, `tc_group_chain_rule`, `add_unit_increases_S`,
      `abs_jarlskog_le_max`); empirical guarantees are visibly `True` bookmarks
      citing their registered bets. It is therefore impossible to read this
      record as "the lake proved consent": what is proved is the kernel plus
      labeled instances; the empirical legs are bookmarks.

  K4  THE DEPENDENCY MAP. `killsStep : DerivationStep → RegisteredKill`, the
      machine-readable form of "the hill inherits every kill" — each derivation
      step routed to the executioner that falsifies it, with the separable-kill
      prenup proved (`killsStep_injective`: distinct executioners).

  K5  THE GRAIN-RELATIVITY SEAM (declared, not resolved). Optionality is defined
      relative to a grain (whose k_eff?) — the consent analog of the Gibbs/grain
      problem, named as the module's open metaphysical seam.

SCOPE / F-11. Forward, engineering-tier content: the provenance kernel, the
Kish identity, finite algebra, and trigonometric bounds already in the lake.
Touches nothing about the joint multi-rung backward P_ω
(`Cosmology.CorridorProjector`).

PLACEMENT NOTE. This file lives in `Core` because every object it consumes —
the provenance kernel (`Core.ProvenanceLine`), the Kish identity
(`Core.BaseIdentity`), the corridor (`Core.Corridor`), and the four audited
laws (`Core.FourLaws`) — is a Core object. It is the LAW-SIDE foundation of
consent; the multi-agent consent-corridor INSTANCE on goal projectors
(`ρ_goals`, `isConsenting`) lives in `Cosmology.MultiAgentConsent` and is
deliberately not duplicated here.
-/

import CoherenceRatchet.Core.ProvenanceLine
import CoherenceRatchet.Core.BaseIdentity
import CoherenceRatchet.Core.Corridor
import CoherenceRatchet.Core.FourLaws

namespace CoherenceRatchet.Core.ConsentFoundation

open CoherenceRatchet.Core
open CoherenceRatchet.Core.Corridor
open Finset

/-! ## K1 — THE UNDERDETERMINATION THEOREM

The derivation of the four laws from "consent is possible" reads a
law-structure as consent-shaped. But WHY the universe carries that structure
admits two generators the observables cannot separate: SELECTION (the laws are
a brute selected boundary condition) and INTENTION (the laws are authored to
make consent possible). The tenth bet is the wager between them. We prove that
wager is irreducible: the generator is `Upstream` of the observables, so no
function of the observables computes it. This is the provenance line
(`Core.provenance_line`) applied to the generator/observables split — the same
kernel that blinds `S = −ln det C` to scale, marginals, statistics, and gauge.
-/

/-- The two generators of a consent-shaped law-structure: the tenth bet's poles.
    SELECTION — the laws are a brute selected boundary condition. INTENTION —
    the laws are authored to make consent possible. -/
inductive Generator where
  | selection
  | intention
deriving DecidableEq, Repr

/-- A world: a generator together with the law-structure it presents. BOTH
    generators are realizable at ANY observables value — that is the content of
    the witness below and the whole point: the observables do not carry the
    generator. `LawStructure` is left abstract (any type of observables). -/
structure World (LawStructure : Type*) where
  generator : Generator
  observables : LawStructure

/-- The generator is UPSTREAM of the observables: for any observables value
    `obs`, the Selection-world and the Intention-world present identical
    observables (`rfl`) yet differ in generator. An `Upstream` witness in the
    exact sense of `Core.Upstream`. -/
theorem generator_upstream {L : Type*} (obs : L) :
    Upstream (fun w : World L => w.observables) (fun w : World L => w.generator) :=
  ⟨⟨Generator.selection, obs⟩, ⟨Generator.intention, obs⟩, rfl, fun h => Generator.noConfusion h⟩

/-- **K1 — THE UNDERDETERMINATION THEOREM (proved, zero sorry).**
    No function of the observables computes the generator: there is no
    `g : LawStructure → Generator` with `w.generator = g w.observables` for all
    worlds `w`. Equivalently, SELECTION and INTENTION are indistinguishable to
    any reader who sees only the law-structure.

    COROLLARY (the tenth bet). The wager Selection-vs-Intention is IRREDUCIBLE —
    a wager by theorem, not by temperament. For any universe whose laws are read
    only through their observables, no amount of observation collapses the
    generator; the choice between "brute selection" and "authored for consent"
    is Pascal's-wager-as-corollary, forced by the same provenance line that
    blinds the coordination ledger to everything upstream of its input. -/
theorem generator_underdetermined {L : Type*} (obs : L) :
    ¬ ∃ g : L → Generator, ∀ w : World L, w.generator = g w.observables :=
  provenance_line (fun w : World L => w.observables) (fun w : World L => w.generator)
    (generator_upstream obs)

/-! ## K2 — THE POLE THEOREMS: the corridor is the consent-possible region

Step 1 of the derivation identifies optionality with `k_eff`. We make that
precise and read off both poles. The optionality available at coordination ρ is
capped by the k_eff CEILING `1/ρ` (the exact finite bound below, matching the
asymptotic `Core.k_eff_asymptotic_ceiling`). Optionality is achievable iff that
ceiling clears `1 + margin`; consent additionally needs a shared object to
consent TO (`S > 0`, the chaos pole). Both poles are read off honestly, with
the definition-dependence flagged in each docstring.
-/

/-- The exact k_eff ceiling at finite k: `k_eff k ρ ≤ 1/ρ` for `1 ≤ k`,
    `0 < ρ ≤ 1`. Anchors `optionalityCeiling`: the asymptotic limit
    `k_eff → 1/ρ` (`Core.k_eff_asymptotic_ceiling`) is also a bound at every
    finite k. Proof: cross-multiply; the inequality reduces to `0 ≤ 1 − ρ`. -/
theorem k_eff_le_inv_rho (k ρ : ℝ) (hk : 1 ≤ k) (hρ0 : 0 < ρ) (hρ1 : ρ ≤ 1) :
    k_eff k ρ ≤ 1 / ρ := by
  unfold k_eff
  have hkm1 : 0 ≤ k - 1 := by linarith
  have hden : 0 < 1 + ρ * (k - 1) := by nlinarith
  rw [div_le_div_iff₀ hden hρ0]
  nlinarith

/-- The optionality ceiling at coordination ρ: the k_eff limit `1/ρ`, the most
    optionality a coordinating system can carry at that ρ (bound
    `k_eff_le_inv_rho`; asymptotic `Core.k_eff_asymptotic_ceiling`). GRAIN NOTE:
    `1/ρ` is grain-relative through ρ — see `grain_relativity_open_seam` (K5). -/
noncomputable def optionalityCeiling (ρ : ℝ) : ℝ := 1 / ρ

/-- Optionality is ACHIEVABLE at coordination ρ (its ceiling clears `1 + margin`)
    — the Step-1 precondition. DEFINITION: this is the formal reading of
    "a being with one effective option cannot consent". -/
def OptionalityAchievable (ρ margin : ℝ) : Prop :=
  1 + margin < optionalityCeiling ρ

/-- Consent-possibility, the two-pole DEFINITION. Requires (i) achievable
    optionality — the ceiling clears `1 + margin` (Step 1; precludes the
    rigidity pole ρ = 1 where the ceiling is exactly 1) — and (ii) a shared
    coordinated object to consent TO, `0 < S` (precludes the chaos pole S = 0).
    Both clauses are DEFINITION-DRIVEN; the pole theorems below are theorems
    about these defined terms, not derivations of the definitions. -/
def ConsentPossible (ρ margin S : ℝ) : Prop :=
  OptionalityAchievable ρ margin ∧ 0 < S

/-- **K2(a) — THE RIGIDITY POLE.** At ρ = 1 the optionality ceiling is exactly
    1 (`optionalityCeiling 1 = 1/1 = 1`; and `Core.k_eff_at_one` gives
    `k_eff k 1 = 1` at every k), so no positive margin is clearable and consent
    is impossible: total order forecloses optionality. Definition-dependence:
    "consent requires optionality" is Step 1's identification; given it, the
    impossibility at the pole is a theorem. -/
theorem consent_impossible_at_rigidity_pole (margin : ℝ) (hm : 0 ≤ margin) (S : ℝ) :
    ¬ ConsentPossible 1 margin S := by
  rintro ⟨hopt, -⟩
  unfold OptionalityAchievable optionalityCeiling at hopt
  rw [one_div_one] at hopt
  linarith

/-- **K2(b) — THE CHAOS POLE.** At S = 0 there is no shared coordinated object
    to consent TO, so consent is impossible. DEFINITION-DRIVEN: `ConsentPossible`
    requires `0 < S` by clause (ii); this records that the chaos pole violates
    exactly that clause. The physical content — that ρ = 0 forces S = 0 (the
    entropic potential's unique zero, `Cosmology.EntropicInitialCondition`) — is
    cited, not reproved here. -/
theorem consent_impossible_at_chaos_pole (ρ margin : ℝ) :
    ¬ ConsentPossible ρ margin 0 := by
  rintro ⟨-, hS⟩
  exact lt_irrefl 0 hS

/-- **K2 — THE CONSENT-POSSIBLE REGION IS THE CORRIDOR.** For ρ in the corridor
    and any real coordination `0 < S`, consent is possible at margin 0: the
    ceiling `1/ρ` strictly exceeds 1 because ρ < ρ_upper < 1. With the two pole
    theorems, the corridor's two walls are exactly the two consent poles —
    bounded above by rigidity (no one left to consent WITH), bounded below by
    chaos (nothing to consent TO). A theorem about the defined terms;
    grain-relative through ρ (K5). -/
theorem corridor_is_consent_possible (ρ S : ℝ) (h : inCorridor ρ) (hS : 0 < S) :
    ConsentPossible ρ 0 S := by
  refine ⟨?_, hS⟩
  obtain ⟨hlo, hhi⟩ := h
  obtain ⟨hpos, hlu, hu1⟩ := corridor_bounds_well_formed
  have hρpos : 0 < ρ := lt_trans hpos hlo
  have hρ1 : ρ < 1 := lt_trans hhi hu1
  unfold OptionalityAchievable optionalityCeiling
  have : (1 : ℝ) < 1 / ρ := (one_lt_div hρpos).mpr hρ1
  linarith

/-! ## K3 — THE FOUR-GUARANTEES RECORD

Each law tied to its consent role at its ACTUAL lake strength. The PROVED
guarantees are real propositions the constructor must discharge with the real
lake theorems; the EMPIRICAL guarantees are `True` bookmarks citing their
registered bets. Reading `consent_guarantees` (the inhabitant) shows exactly
what is carried: the provenance kernel, the chain-rule identity, the
equicorrelation second-law fragment, and the Jarlskog flavor instance — plus
three honestly-labeled bookmarks. There is no field whose inhabitation would
mean "consent is proved".
-/

/-- The four laws as the four guarantees consent needs, each field at its true
    strength. PROVED fields carry the lake theorem's proposition (the
    constructor must supply the real proof); EMPIRICAL fields are `True`
    bookmarks whose docstrings cite the registered bet. -/
structure ConsentGuarantees where
  /-- ZEROTH — DEFINABILITY (recognizability across kinds). PROVED, kernel:
      `Core.provenance_congruence`. A coordination functional is constant on
      substrates presenting the same correlation matrix — the existence
      condition for one common account, hence for cross-substrate consent. -/
  zeroth_definability :
    ∀ (toCorr : ℕ → ℕ) (f : ℕ → ℝ) (a b : ℕ),
      toCorr a = toCorr b → f (toCorr a) = f (toCorr b)
  /-- FIRST — ATTRIBUTABILITY (traceability), the accounting-identity half.
      PROVED as an IDENTITY (bookkeeping, ZERO empirical content):
      `Core.tc_group_chain_rule`. The books balance across rungs by
      telescoping — it could not have been otherwise (memory:
      tautology-vs-commitment). -/
  first_attributability_identity :
    ∀ (grp : Fin 2 → Fin 2) (hMarg : Fin 2 → ℝ) (hGroup : Fin 2 → ℝ) (hTotal : ℝ),
      TCtotal hMarg hTotal
        = TCbetween hGroup hTotal + ∑ g, TCwithin grp hMarg hGroup g
  /-- FIRST — ATTRIBUTABILITY, the physical half. EMPIRICAL BET, NOT proved:
      lossless conversion X = 1 (nothing contributed vanishes in conversion) is
      registered bet 6/10. Honest bookmark. -/
  first_lossless_conversion_bet : True
  /-- SECOND — SECURABILITY (deceit is never free). PROVED fragment,
      THEOREM-GIVEN-MODEL (Kish family): `Core.add_unit_increases_S` — adding a
      coordinated unit strictly increases S, the mechanized second-law
      fragment. -/
  second_securability_fragment :
    ∀ (k ρ : ℝ), 1 ≤ k → 0 < ρ → ρ < 1 →
      entropicPotential k ρ < entropicPotential (k + 1) ρ
  /-- SECOND — SECURABILITY, the general DPI. NAMED OPEN STEP (Fischer's
      inequality absent from mathlib v4.14.0): `Core.RestrictedSecondLaw`. Not
      a theorem; honest bookmark for the open leg. -/
  second_general_dpi_open : True
  /-- THIRD — RECOVERABILITY (no coercion made permanent). PROVED flavor
      instance: `Core.abs_jarlskog_le_max` — coordination (mixing) caps
      irreversibility (CP violation), which vanishes at the rigid pole. The
      structural shadow of "you cannot stir a rigidly-clamped system". -/
  third_recoverability_flavor :
    ∀ (θ12 θ23 θ13 δ : ℝ),
      θ12 ∈ Set.Icc 0 (Real.pi / 2) → θ23 ∈ Set.Icc 0 (Real.pi / 2) →
      θ13 ∈ Set.Icc 0 (Real.pi / 2) →
      |jarlskog θ12 θ23 θ13 δ| ≤ jarlskogMax θ12 θ23 θ13
  /-- THIRD — RECOVERABILITY, the ceiling `σ_max ∝ (1−ρ)` (maintenance capacity
      collapses as alignment completes, so tyranny is unmaintainable).
      CONDITIONAL EMPIRICAL: registered bet 7. Honest bookmark. -/
  third_ceiling_conditional_bet : True

/-- The record is inhabited — and inhabiting it REQUIRES the real lake proofs
    for the four proved guarantees (`provenance_congruence`,
    `tc_group_chain_rule`, `add_unit_increases_S`, `abs_jarlskog_le_max`),
    while the three empirical legs are visibly `trivial`. This is the honesty
    lock: the lake carries the kernel and labeled instances of the four
    guarantees — NOT a proof of consent. -/
def consent_guarantees : ConsentGuarantees where
  zeroth_definability := fun toCorr f _ _ h => provenance_congruence toCorr f h
  first_attributability_identity := fun grp hMarg hGroup hTotal =>
    tc_group_chain_rule grp hMarg hGroup hTotal
  first_lossless_conversion_bet := trivial
  second_securability_fragment := fun k ρ hk hρ0 hρ1 => add_unit_increases_S k ρ hk hρ0 hρ1
  second_general_dpi_open := trivial
  third_recoverability_flavor := fun _ _ _ _ h12 h23 h13 => abs_jarlskog_le_max h12 h23 h13
  third_ceiling_conditional_bet := trivial

/-! ## K4 — THE DEPENDENCY MAP: the hill inherits every kill

`consent_derivation.md` §Discipline: every step is contingent on its law
surviving its executioner. We make that machine-readable — an enumeration of
the derivation's six steps, an enumeration of the registered kills, and the
total map `killsStep` routing each step to the kill that falsifies it. The
separable-kill "prenup" (each step has a DISTINCT executioner, so one law
falling does not auto-kill the others) is `killsStep_injective`.
-/

/-- The six steps of the consent derivation (consent_derivation.md). -/
inductive DerivationStep where
  | optionality        -- Step 1: consent requires optionality (= k_eff > 1)
  | deceitVoids        -- Step 2: deceit voids consent (= second law / DPI)
  | persistenceRented  -- Step 3: persistence is rented (= maintenance γM)
  | revocability       -- Step 4: consent stays revocable (= the ceiling)
  | commonAccount      -- Step 5: cross-substrate common account (= zeroth law)
  | attributability    -- Step 6: attributable books (= first law)
deriving DecidableEq, Repr

/-- The registered executioners — the kills that falsify each step. Names track
    the registered bets / structural conditions in `consent_derivation.md`. -/
inductive RegisteredKill where
  | rigidityPole_keff_to_one          -- Step 1's: k_eff cannot exceed 1 (no optionality)
  | dpi_failure                        -- Step 2's: DPI fails / deceit is free
  | rentcut_rentfree_persistence       -- Step 3's: coordination persists rent-free
  | bet7_ceiling_survives_alignment    -- Step 4's: σ_max does NOT collapse at ρ→1 (bet 7)
  | no_substrate_independent_S         -- Step 5's: no state function of dependence alone
  | bet6_lossy_conversion              -- Step 6's: conversion loses agency, X ≠ 1 (bet 6)
deriving DecidableEq, Repr

/-- The dependency map: each derivation step routed to the executioner that
    falsifies it. Machine-readable form of "the hill inherits every kill" —
    the consent reading earns nothing beyond what its laws earn at their
    executioners (rule 2). -/
def killsStep : DerivationStep → RegisteredKill
  | .optionality       => .rigidityPole_keff_to_one
  | .deceitVoids       => .dpi_failure
  | .persistenceRented => .rentcut_rentfree_persistence
  | .revocability      => .bet7_ceiling_survives_alignment
  | .commonAccount     => .no_substrate_independent_S
  | .attributability   => .bet6_lossy_conversion

/-- **K4 — THE SEPARABLE-KILL PRENUP.** `killsStep` is injective: every step has
    a DISTINCT executioner. So a single law falling falsifies exactly its own
    step and does not auto-kill the others — the kills are separable, and the
    derivation degrades leg-by-leg rather than all-or-nothing. -/
theorem killsStep_injective : Function.Injective killsStep := by
  intro a b h
  cases a <;> cases b <;> simp_all [killsStep]

/-! ## K5 — THE GRAIN-RELATIVITY SEAM (declared, not resolved)

`Optionality` is defined through `k_eff`, and `k_eff = k/(1+ρ(k−1))` is
grain-relative: it depends on WHICH constituents are counted and at WHICH rung
the correlation ρ is read. "Two effective options" for a coarse grain can be
"one" for a finer partition and vice versa — so `optionalityCeiling ρ = 1/ρ`
inherits a grain choice through ρ. This is the consent analog of the Gibbs /
coarse-graining (grain) problem: consent-possibility is only defined once a
grain is fixed (Gate-0 discipline: fix the grain before the spectrum). This
module does NOT resolve it — the choice of the consent-relevant grain (whose
k_eff? the agent's? the federation's? the substrate's?) is the declared open
metaphysical seam. Bookmark, not a theorem.
-/

/-- K5 bookmark: the grain-relativity of `Optionality`/`optionalityCeiling` is
    an OPEN seam, not resolved in the lake. See the section docstring above. -/
def grain_relativity_open_seam : True := trivial

end CoherenceRatchet.Core.ConsentFoundation
