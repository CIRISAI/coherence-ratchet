/-
CoherenceRatchet.StructuralClaims
=================================

The five EMPIRICAL structural commitments of the framework, stated so that what
each test is trying to prove or disprove — and how — is explicit and
machine-checked.

This file deliberately proves NONE of the five claims. They are empirical: they
are about what coordinated substrates actually do, and they could be false.
What this file DOES prove is the falsification logic — that each claim is
equivalent to the non-existence of a specific falsifying witness — so that an
experiment exhibiting such a witness disproves the claim by a checked step.

Contrast with the Kish identity (k_eff = k/(1+ρ(k-1)), Core.BaseIdentity, with
K1–K4 proven): that IS a theorem — true by construction given its definitions,
not falsifiable. The Kish identity is the COORDINATE SYSTEM. The five claims
below are the COMMITMENTS. A theorem is not an empirical claim and an empirical
claim is not a theorem; this file holds the empirical claims.

Each claim is recorded as `framework_asserts_N : ClaimN` — an axiom, an
ASSERTION the framework makes and experiment N tries to break. The axioms are
not proved and not provable; that is the point. Finding a falsifier witness
contradicts the corresponding axiom via `claimN_iff`.
-/

namespace CoherenceRatchet.StructuralClaims

/-! ## Abstract carriers -/

/-- Any coordinated system: gene-regulatory network, brain, LLM, OSS project,
    social group, CMB mode-space. -/
axiom Substrate : Type

/-- A level of the emergence hierarchy (Ph0 … A5). -/
axiom Rung : Type

/-! ## Operational predicates — each answered by MEASUREMENT, not by proof -/

axiom Coordinated  : Substrate → Prop   -- exhibits sustained coordination
axiom Persistent   : Substrate → Prop   -- survives on long timescales
axiom InCorridor   : Substrate → Prop   -- occupies the bounded band, not a pole
axiom Maintained   : Substrate → Prop   -- has identifiable active maintenance (γM) work
axiom ThermalClosed : Substrate → Prop  -- evolves by closed-system thermal dynamics
axiom GenericInitial : Substrate → Prop -- generic high-entropy initial conditions
axiom MultiRung    : Substrate → Prop   -- exhibits multi-rung corridor structure
axiom BackwardConditioned : Substrate → Prop -- structure delivered by P_ω post-selection
axiom Carries      : Rung → Prop        -- the rung carries coordinated structure
axiom ForwardErgodic     : Rung → Prop  -- forward generator: a unique steady state
axiom BackwardNonErgodic : Rung → Prop  -- backward generator: many conserved quantities
axiom RungInCorridor     : Rung → Prop  -- the rung occupies a corridor under some k_eff
axiom MaintenanceBreaksSymmetry : Rung → Prop -- the γM maintenance breaks the
                                              -- dynamical symmetries (Test E2)

/-! ## The falsification lemma — the one logical fact this file rests on -/

/-- A universally-quantified claim `∀ x, A x → B x` holds iff no falsifying
    witness `∃ x, A x ∧ ¬ B x` exists. Proven once; reused for all five. -/
theorem claim_iff_no_witness {α : Type} (A B : α → Prop) :
    (∀ x, A x → B x) ↔ ¬ ∃ x, A x ∧ ¬ B x := by
  constructor
  · intro h ⟨x, hA, hnB⟩
    exact hnB (h x hA)
  · intro h x hA
    apply Classical.byContradiction
    intro hnB
    exact h ⟨x, hA, hnB⟩

/-! ## Claim 1 — the corridor is a bounded attractor at every coordinated substrate

    A persistent coordinated substrate either occupies the corridor or pays
    identifiable maintenance work (Mode-(iii) absence).
    TEST E1: corridor-existence measurement on new A0+ substrates.
    FALSIFIER: a persistent coordinated substrate at a pole, unmaintained. -/

def Claim1 : Prop :=
  ∀ s, (Coordinated s ∧ Persistent s) → (InCorridor s ∨ Maintained s)

def Falsifier1 : Prop :=
  ∃ s, (Coordinated s ∧ Persistent s) ∧ ¬ (InCorridor s ∨ Maintained s)

theorem claim1_iff : Claim1 ↔ ¬ Falsifier1 :=
  claim_iff_no_witness _ _

axiom framework_asserts_1 : Claim1

/-! ## Claim 2 — forward and backward generators in different ergodicity classes

    At every rung carrying coordinated structure WHOSE MAINTENANCE BREAKS THE
    DYNAMICAL SYMMETRIES, the forward generator is ergodic (a unique steady
    state) and the backward generator is non-ergodic (many conserved
    quantities) — operator-level distinct.
    TEST E2: ergodicity-class measurement on each operational instantiation.
    FALSIFIER: a rung with symmetry-breaking maintenance where the split fails.
    STATUS: tested at n = 6 instances (exp_E2_ergodicity_split.py). The split
    holds for symmetry-breaking maintenance (4/6); it FAILS for symmetric
    maintenance (2/6: Heisenberg + symmetric bit-flip → non-ergodic forward).
    The `MaintenanceBreaksSymmetry` antecedent is the amendment E2 forced — the
    original unqualified Claim 2 was falsified as stated. γM ("injects
    distinction", Piece 2) is generically symmetry-breaking. -/

def Claim2 : Prop :=
  ∀ r, (Carries r ∧ MaintenanceBreaksSymmetry r) →
       (ForwardErgodic r ∧ BackwardNonErgodic r)

def Falsifier2 : Prop :=
  ∃ r, (Carries r ∧ MaintenanceBreaksSymmetry r) ∧
       ¬ (ForwardErgodic r ∧ BackwardNonErgodic r)

theorem claim2_iff : Claim2 ↔ ¬ Falsifier2 :=
  claim_iff_no_witness _ _

axiom framework_asserts_2 : Claim2

/-! ## Claim 3 — closed-system thermal dynamics cannot sustain a corridor unmaintained

    If a closed-system thermal substrate persistently occupies the corridor, it
    must be maintained. (Contrapositive: closed thermal + unmaintained ⇒ no
    persistent corridor.)
    TEST E3: closed-system thermalization simulation.
    FALSIFIER: a verifiably thermal closed system persistently in-corridor and
    unmaintained. -/

def Claim3 : Prop :=
  ∀ s, (ThermalClosed s ∧ InCorridor s ∧ Persistent s) → Maintained s

def Falsifier3 : Prop :=
  ∃ s, (ThermalClosed s ∧ InCorridor s ∧ Persistent s) ∧ ¬ Maintained s

theorem claim3_iff : Claim3 ↔ ¬ Falsifier3 :=
  claim_iff_no_witness _ _

axiom framework_asserts_3 : Claim3

/-! ## Claim 4 — the corridor recurs at every coordinated rung (fractal recurrence)

    Every rung carrying coordinated structure occupies a corridor under some
    effective-dimensionality coordinate.
    TEST E4: corridor-existence per rung, chemistry through cosmology.
    FALSIFIER: a coordinated rung with no corridor under any reasonable k_eff. -/

def Claim4 : Prop :=
  ∀ r, Carries r → RungInCorridor r

def Falsifier4 : Prop :=
  ∃ r, Carries r ∧ ¬ RungInCorridor r

theorem claim4_iff : Claim4 ↔ ¬ Falsifier4 :=
  claim_iff_no_witness _ _

axiom framework_asserts_4 : Claim4

/-! ## Claim 5 — multi-rung structure from generic initial conditions needs backward conditioning

    A substrate that reaches multi-rung corridor structure FROM GENERIC
    high-entropy initial conditions did so via backward conditioning (P_ω
    post-selection). Scope is cosmological ORIGIN — not corridor occupation in
    general, which forward dissipative dynamics with maintenance does produce
    (construct_pomega_lindblad.py).
    TEST E6: under the constructed soft P_ω, the forward amplitude from generic
    high-entropy initial conditions to multi-rung corridor structure.
    FALSIFIER: multi-rung corridor structure reached from generic initial
    conditions by purely forward dynamics. -/

def Claim5 : Prop :=
  ∀ s, (GenericInitial s ∧ MultiRung s) → BackwardConditioned s

def Falsifier5 : Prop :=
  ∃ s, (GenericInitial s ∧ MultiRung s) ∧ ¬ BackwardConditioned s

theorem claim5_iff : Claim5 ↔ ¬ Falsifier5 :=
  claim_iff_no_witness _ _

axiom framework_asserts_5 : Claim5

/-! ## Summary

    Five empirical claims, each `ClaimN ↔ ¬ FalsifierN` machine-checked above.
    The framework asserts each (`framework_asserts_N`). An experiment exhibits a
    `FalsifierN` witness ⇒ `¬ ClaimN` ⇒ contradiction with `framework_asserts_N`
    ⇒ the framework is wrong at claim N. That is the whole test logic, and it is
    checked here. The corridor is the empirical object; the Kish algebra
    (Core.BaseIdentity) is the coordinate system it is stated in.

    ## Test ledger (2026-05-21 structural series; experiments/structural_series/)

    Claim 1 — E1 (LLM substrate, real weights: gpt2 / Pythia-160m / Qwen2.5-0.5B)
      WEAKLY SUPPORTED. Decisively off the rigidity pole; debiased within-layer
      ρ low (~0.05–0.22), at the chaos-side edge. No falsifier; not a clean
      confirmation. Owed: real-data campaign across more substrates.
    Claim 2 — E2 (6 Lindbladian instances)
      FALSIFIED AS STATED → AMENDED. 2/6 (Heisenberg + symmetric bit-flip) had
      non-ergodic forward generators. The `MaintenanceBreaksSymmetry` antecedent
      above is the amendment the test forced.
    Claim 3 — E3 (closed chaotic chain, energy-swept)
      CONSISTENT. A closed system conserves energy ⇒ late-time ρ is energy-
      indexed, a one-parameter family, no corridor attractor without
      maintenance.
    Claim 4 — E1 (3 architectures)
      WEAKLY SUPPORTED (with Claim 1).
    Claim 5 — E6 (Penrose-scope: 200 generic high-entropy ICs)
      CONSISTENT at the cosmological-origin scope. 0/200 forward-evolve to the
      multi-rung corridor.

    Plus the orthogonality theorem (CMBOrthogonality.lean): the soft P_ω leaves
    the bulk CMB power spectrum exactly invariant — the framework is a strict
    extension of ΛCDM at the cosmological tier. PROVED, not an empirical claim.

    The spec is live: a test (E2) already amended a claim. -/

end CoherenceRatchet.StructuralClaims
