/-
Cosmology.EntropicInitialCondition — the entropic-vacuum initial condition:
S = 0 at t = 0, the chaos pole as the potential's unique zero and global minimum,
and the maintained ascent that never attains the rigidity divergence.

THE READING (interpretive; see the record at the bottom of this file, and
papers/notes/penrose_entropic_past.md). Penrose's Weyl Curvature Hypothesis
(1979; The Road to Reality, 2004, ch. 27) says the initial state of the universe
had vanishing Weyl curvature: an extraordinarily special, gravitationally
UNSTRUCTURED initial condition, which he takes to be the origin of the
thermodynamic arrow and treats as an unexplained boundary condition.

In the potential form of the corridor (`Core.EntropicPotential`, T-E0–T-E5),
"gravitationally unstructured" reads as ρ₀ = 0, equivalently S(k, ρ₀) = 0: the
universe begins at the CHAOS POLE, where no coordination-induced structure has
been written into the substrate and the induced metric equals the substrate
metric (Bianconi's vacuum G̃ = g̃, arXiv:2408.14391). Cosmic history is then a
MAINTAINED ASCENT of S which, per the corridor, must never reach the rigidity
pole where S diverges and the correlation matrix loses invertibility.

WHAT THIS FILE PROVES. Only the potential-theoretic content, which is real
analysis over the closed-form Kish spectrum and carries no framework axiom:

  T-P1  ρ₀ = 0  ↔  S(k, ρ₀) = 0        (the chaos pole IS the potential's
                                        unique zero — `entropicPotential_eq_zero_iff`)
  T-P2  S(k, 0) ≤ S(k, ρ) on [0, 1)    (the initial condition is the global
                                        minimum; strict off the pole)
  T-P3  a trajectory with ρ(0) = 0, strictly increasing, ranging in [0, 1),
        has S(k, ρ(0)) = 0, strictly increasing S, and S > 0 at every later
        time; and it is bounded by S(k, b) whenever ρ is bounded by b < 1
        (the rigidity divergence is approached only as ρ → 1⁻).

WHAT THIS FILE DOES NOT DO — F-11 STAYS CLOSED, AND PENROSE STAYS UNEXPLAINED.

1. This is FORWARD content. It is a statement about an initial condition and
   about the minimum of a potential on the physical domain. It involves no
   backward joint amplitude, no multi-rung post-selection operator, and no
   P_ω of any kind. It therefore does not touch, weaken, or reopen
   `Cosmology.CorridorProjector.F11_joint_backward_P_omega_no_go`, and it does
   NOT resurrect the retracted strong framing of D1 ("Penrose's WCH is
   structurally derived"). The schematic argument in `Cosmology.PenrosePast`
   is the argument this file replaces with a theorem about the potential, and
   the theorem it proves is strictly weaker than what D1 once claimed.

2. "S = 0 at t = 0" is a RESTATEMENT of specialness in the framework's
   variable, not an explanation of WHY the initial condition was special. The
   framework does not solve Penrose's puzzle; it relocates it. Nothing below
   derives ρ₀ = 0 — it is a hypothesis in every theorem that uses it.

3. The identification of vanishing Weyl curvature with ρ = 0 is an
   INTERPRETATION, unproved: gravitational-clustering correlation is not
   literally the Kish ρ of a coordinating unit. It is recorded as a record
   (`WeylCurvatureReading`), not as a theorem.

The one honest structural gain: the potential has a UNIQUE zero and a single
divergence, and is strictly monotone between them. So "begin at the zero,
ascend, never attain the pole" is the only history the potential permits — a
weak explanatory gain, stated precisely as T-P1/T-P2/T-P3 and no more.

REFERENCES:
- Penrose, R. Singularities and time-asymmetry. In Hawking & Israel (eds.),
  General Relativity: An Einstein Centenary Survey, 1979.
- Penrose, R. The Road to Reality. Knopf, 2004, ch. 27.
- Bianconi, G. Gravity from entropy. Phys. Rev. D 111, 066001 (2025).
- papers/notes/entropic_action_bridge.md (the T-E theorem series).
- papers/notes/penrose_entropic_past.md (this file's exposition and limits).
-/

import CoherenceRatchet.Core.EntropicPotential

namespace CoherenceRatchet.Cosmology.EntropicInitial

open Real Set
open CoherenceRatchet.Core

/-! ## The entropic-vacuum initial condition -/

/-- The ENTROPIC VACUUM INITIAL CONDITION: the coordinating unit begins with
    zero correlation. In the potential reading this is the chaos pole — no
    coordination-induced structure has been written into the substrate, so the
    induced metric equals the substrate metric (Bianconi's `G̃ = g̃`).

    `k` is carried for uniformity with `entropicPotential k ρ`; the condition
    itself constrains only ρ₀, since the potential's zero is `k`-independent
    (`entropicPotential_at_zero`). -/
def entropicVacuumInitial (_k : ℝ) (ρ₀ : ℝ) : Prop := ρ₀ = 0

/-- T-P1. THE INITIAL CONDITION IS EXACTLY THE VANISHING OF THE POTENTIAL.
    On the physical domain [0, 1), the entropic vacuum condition ρ₀ = 0 holds
    iff S(k, ρ₀) = 0. A direct instance of `entropicPotential_eq_zero_iff`: the
    chaos pole is the potential's UNIQUE zero, so "starts unstructured" and
    "starts at zero entropic potential" are the same hypothesis, not two.

    This is the precise sense in which the framework's variable expresses
    Penrose-style specialness. It does not explain it: ρ₀ = 0 remains a
    hypothesis, here and everywhere below. -/
theorem entropicVacuumInitial_iff_potential_eq_zero
    (k ρ₀ : ℝ) (hk : 1 < k) (hρ0 : 0 ≤ ρ₀) (hρ1 : ρ₀ < 1) :
    entropicVacuumInitial k ρ₀ ↔ entropicPotential k ρ₀ = 0 :=
  (entropicPotential_eq_zero_iff k ρ₀ hk hρ0 hρ1).symm

/-! ## The initial condition is the potential's global minimum -/

/-- T-P2a. GLOBAL MINIMUM: the entropic vacuum minimizes the potential over the
    whole physical domain. Immediate from Klein nonnegativity
    (`entropicPotential_nonneg`) plus `entropicPotential_at_zero`: the potential
    is a relative entropy, so it is nonnegative, and it vanishes at the pole. -/
theorem entropicVacuum_le_potential (k : ℝ) (hk : 1 ≤ k) :
    ∀ ρ ∈ Ico (0:ℝ) 1, entropicPotential k 0 ≤ entropicPotential k ρ := by
  intro ρ hρ
  rw [entropicPotential_at_zero]
  exact entropicPotential_nonneg k ρ hk hρ.1 hρ.2

/-- T-P2b. The same fact in `IsMinOn` form: `0` is a minimizer of the entropic
    potential on `[0, 1)`. -/
theorem entropicVacuum_isMinOn (k : ℝ) (hk : 1 ≤ k) :
    IsMinOn (fun ρ => entropicPotential k ρ) (Ico (0:ℝ) 1) 0 :=
  isMinOn_iff.mpr (entropicVacuum_le_potential k hk)

/-- T-P2c. STRICT global minimum away from the pole: every structured state
    costs strictly positive entropic potential. Any departure from the
    unstructured initial condition is a strict ascent. -/
theorem entropicVacuum_lt_potential (k : ℝ) (hk : 1 < k) :
    ∀ ρ ∈ Ioo (0:ℝ) 1, entropicPotential k 0 < entropicPotential k ρ := by
  intro ρ hρ
  rw [entropicPotential_at_zero]
  exact entropicPotential_pos k ρ hk hρ.1 hρ.2

/-! ## The maintained ascent

A cosmic history is modeled, in the framework's single dynamical variable, as a
trajectory `ρ : ℝ → ℝ` of the coordinating unit's correlation. The reading of
the arrow of time is the ascent of `S` along such a trajectory. This is
CONSISTENT WITH but NOT DERIVED FROM the second law: strict monotonicity of `ρ`
is a hypothesis of `EntropicAscent`, not a consequence of anything proved here. -/

/-- An ASCENT TRAJECTORY from the entropic vacuum: a correlation history that
    stays in the physical domain, starts at the chaos pole, and is strictly
    increasing on forward time.

    Each field is a hypothesis. In particular `strictly_ascending` is assumed,
    not derived — the framework does not prove the second law. -/
structure EntropicAscent (ρ : ℝ → ℝ) : Prop where
  /-- The trajectory stays on the physical domain: ρ(t) ∈ [0, 1) for t ≥ 0.
      In particular the rigidity pole ρ = 1 is never attained. -/
  physical : ∀ t, 0 ≤ t → ρ t ∈ Ico (0:ℝ) 1
  /-- The entropic-vacuum initial condition: ρ(0) = 0 (the chaos pole). -/
  vacuum_start : ρ 0 = 0
  /-- Forward time strictly increases correlation. ASSUMED. -/
  strictly_ascending : StrictMonoOn ρ (Ici (0:ℝ))

/-- T-P3a. The ascent begins at zero potential — the trajectory starts at the
    potential's unique zero. -/
theorem ascent_potential_at_start (k : ℝ) (ρ : ℝ → ℝ) (h : EntropicAscent ρ) :
    entropicPotential k (ρ 0) = 0 := by
  rw [h.vacuum_start, entropicPotential_at_zero]

/-- T-P3b. THE ASCENT: along an ascent trajectory the entropic potential is
    strictly increasing in forward time. Composition of the trajectory's
    strict monotonicity with `entropicPotential_strictMonoOn` (T-E2). -/
theorem ascent_potential_strictMono (k : ℝ) (hk : 1 < k) (ρ : ℝ → ℝ)
    (h : EntropicAscent ρ) {s t : ℝ} (hs : 0 ≤ s) (hst : s < t) :
    entropicPotential k (ρ s) < entropicPotential k (ρ t) := by
  have ht : 0 ≤ t := le_of_lt (lt_of_le_of_lt hs hst)
  exact entropicPotential_strictMonoOn k hk (h.physical s hs) (h.physical t ht)
    (h.strictly_ascending (mem_Ici.mpr hs) (mem_Ici.mpr ht) hst)

/-- T-P3c. Every later state carries strictly positive entropic potential: once
    the universe leaves the unstructured initial condition, the relative entropy
    between coordination and substrate is strictly positive and never returns to
    zero. The framework's reading of the thermodynamic arrow — again, a
    consequence of the ASSUMED strict ascent, not a derivation of it. -/
theorem ascent_potential_pos (k : ℝ) (hk : 1 < k) (ρ : ℝ → ℝ)
    (h : EntropicAscent ρ) {t : ℝ} (ht : 0 < t) :
    0 < entropicPotential k (ρ t) := by
  have h0 := ascent_potential_strictMono k hk ρ h (le_refl 0) ht
  rwa [ascent_potential_at_start k ρ h] at h0

/-- T-P3d. THE RIGIDITY POLE IS NEVER ATTAINED IN FINITE TIME: the trajectory's
    correlation stays strictly below 1 at every time, so the potential is finite
    all along the ascent. (Immediate from `physical`; recorded because it is the
    corridor's standing requirement on any admissible history.) -/
theorem ascent_below_rigidity (ρ : ℝ → ℝ) (h : EntropicAscent ρ)
    {t : ℝ} (ht : 0 ≤ t) : ρ t < 1 := (h.physical t ht).2

/-- T-P3e. THE DIVERGENCE IS APPROACHED ONLY AS ρ → 1⁻. If the ascent is bounded
    away from the rigidity pole by some `b < 1`, then the entropic potential is
    bounded above by `S(k, b)` for all time: an eternally maintained history has
    bounded entropic cost. Contrapositive: `S` can diverge along the trajectory
    only if `ρ(t) → 1`, i.e. only by reaching the rigidity pole in the limit. -/
theorem ascent_potential_le_of_bounded (k : ℝ) (hk : 1 < k) (ρ : ℝ → ℝ)
    (h : EntropicAscent ρ) (b : ℝ) (hb1 : b < 1) (hb : ∀ t, 0 ≤ t → ρ t ≤ b) :
    ∀ t, 0 ≤ t → entropicPotential k (ρ t) ≤ entropicPotential k b := by
  intro t ht
  have hb0 : (0:ℝ) ≤ b := by
    have := hb 0 (le_refl 0)
    rwa [h.vacuum_start] at this
  exact (entropicPotential_strictMonoOn k hk).monotoneOn
    (h.physical t ht) ⟨hb0, hb1⟩ (hb t ht)

/-! ## The only history the potential permits

Combining T-P1, T-P2 and T-P3: the potential has a unique zero (the chaos pole)
and a single divergence (the rigidity pole), and is strictly monotone between
them. A history that starts at the zero and ascends therefore has nowhere else
to start and no other direction to go, and the divergence bounds it from above
without ever being attained. That is the whole of the structural gain. -/

/-- T-P3f. THE PERMITTED HISTORY, assembled. An ascent trajectory (i) starts at
    the potential's unique zero, (ii) sits at the potential's global minimum at
    t = 0, (iii) strictly ascends thereafter, and (iv) never attains the
    rigidity pole. Nothing here explains WHY the history starts at the zero:
    `EntropicAscent.vacuum_start` is an assumption. -/
theorem permitted_history (k : ℝ) (hk : 1 < k) (ρ : ℝ → ℝ) (h : EntropicAscent ρ) :
    entropicPotential k (ρ 0) = 0 ∧
    (∀ σ ∈ Ico (0:ℝ) 1, entropicPotential k (ρ 0) ≤ entropicPotential k σ) ∧
    (∀ s t : ℝ, 0 ≤ s → s < t →
      entropicPotential k (ρ s) < entropicPotential k (ρ t)) ∧
    (∀ t : ℝ, 0 ≤ t → ρ t < 1) := by
  refine ⟨ascent_potential_at_start k ρ h, ?_, ?_, fun t ht => ascent_below_rigidity ρ h ht⟩
  · intro σ hσ
    rw [ascent_potential_at_start k ρ h, ← entropicPotential_at_zero k]
    exact entropicVacuum_le_potential k (le_of_lt hk) σ hσ
  · intro s t hs hst
    exact ascent_potential_strictMono k hk ρ h hs hst

/-! ## The Penrose reading — recorded, not proved -/

/-- WEYL-CURVATURE READING. A flat record of the interpretive claim, following
    the lake's record house pattern (cf. `Cosmology.CorridorProjector.FelevenNoGo`,
    `Cosmology.CorridorProjector.OperationalCorridor`). NOT a theorem: the fields
    are `True`, and the content lives in the docstrings. What is mechanized is
    T-P1–T-P3 above; what is recorded here is only how to read them. -/
structure WeylCurvatureReading where
  /-- THE MAPPING. Penrose's Weyl Curvature Hypothesis (vanishing Weyl curvature
      at t = 0) is read as ρ₀ = 0, equivalently S(k, ρ₀) = 0 (T-P1), equivalently
      occupation of the chaos pole, equivalently Bianconi's vacuum G̃ = g̃ (no
      coordination-induced structure on the substrate). -/
  wch_reads_as_entropic_vacuum : True
  /-- THE IDENTIFICATION IS INTERPRETIVE AND UNPROVED. Gravitational-clustering
      correlation is not literally the Kish ρ of a coordinating unit. No theorem
      in this lake connects the Weyl tensor to `entropicPotential`. -/
  weyl_to_rho_identification_unproved : True
  /-- RESTATEMENT, NOT EXPLANATION. "S = 0 at t = 0" expresses Penrose's
      specialness in the framework's variable; it does not explain why the
      initial condition was special. The framework RELOCATES Penrose's puzzle,
      it does not solve it. ρ₀ = 0 is a hypothesis in every theorem above. -/
  restatement_not_explanation : True
  /-- THE ARROW IS ASSUMED, NOT DERIVED. The thermodynamic arrow reads as the
      ascent of S under maintenance (T-P3b/T-P3c), but strict ascent is the
      hypothesis `EntropicAscent.strictly_ascending`. Consistent with the second
      law; not a derivation of it. -/
  arrow_consistent_not_derived : True
  /-- THE STRUCTURAL GAIN, PRECISELY. The potential has a unique zero
      (`entropicPotential_eq_zero_iff`) and one divergence
      (`entropicPotential_tendsto_atTop_rigidity`), monotone between
      (`entropicPotential_strictMonoOn`). So "start at the zero, ascend, never
      attain the pole" is the only history the potential permits (T-P3f). This
      is a weak explanatory gain: it constrains the SHAPE of any history, not
      the CHOICE of its initial condition. -/
  unique_zero_and_pole_constrain_history : True
  /-- FORWARD ONLY — F-11 UNTOUCHED. This is a statement about a forward initial
      condition and the minimum of a potential. It involves no backward joint
      P_ω, no post-selection operator, and no multi-rung amplitude. It does not
      reopen `CorridorProjector.F11_joint_backward_P_omega_no_go`, and it does
      not resurrect the retracted strong framing of D1 (`Cosmology.PenrosePast`:
      "WCH structurally derived" — retracted; the schematic argument survives). -/
  forward_only_untouched_by_f11 : True

/-- The Penrose reading of the entropic-vacuum initial condition is recorded.
    Inhabiting this record asserts nothing beyond the docstrings: the theorems
    are T-P1–T-P3f; this is their interpretation. -/
def penrose_entropic_initial_condition_reading : WeylCurvatureReading :=
  ⟨trivial, trivial, trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Cosmology.EntropicInitial
