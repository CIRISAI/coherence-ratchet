/-
Core.Dynamics — Piece 2: the dynamical equation for ρ(t)  [TWO-POLE form]

The Kish identity is kinematic. The dynamics that makes the corridor a
non-trivial MAINTAINED state is:

  dρ/dt = α(ρ, S) − γ·M(t)

Where:
- α(ρ, S) is the spontaneous correlation drift driven by shared environment
  or shared selection pressure S. Its SIGN is substrate/perturbation-specific:
  α > 0 drives toward the RIGIDITY pole (ρ → 1); α < 0 drives toward the CHAOS
  pole (ρ → 0).
- γ·M(t) is the active coherence-management work being done.
- The corridor is a MAINTAINED state, held by non-trivial M(t) AGAINST α
  (`corridor_requires_maintenance`: at equilibrium γM = α).
- At M = 0, ρ drifts OUT of the corridor toward the pole selected by sign(α)
  (`rho_drift_at_zero_maintenance` = the α>0 rigidity exit; `rho_exit_chaos`
  = the α<0 chaos exit).

CORRECTION (2026-07-02, from the arousal/dynamics probe). An earlier version of
this header claimed "at M=0, ρ drifts monotonically toward 1" — a SINGLE-pole
over-specification. The corridor has TWO exits: rigidity (ρ→1, e.g. seizure /
deep slow-wave anesthesia — the α>0 case) and chaos (ρ→0, e.g. burst-suppression
/ post-anoxic silence — the α<0 case). Both are corridor exits; consciousness =
corridor-occupation is corroborated by both poles being unconscious. Which pole a
given substrate+perturbation takes is set by the sign of α in the corridor — an
empirical, substrate-specific fact, NOT universally ρ→1.

HONEST FALSIFIABILITY CAVEAT. "M=0 → exit to *some* pole" is more defensible but
WEAKER than the single-pole claim — a system out of the corridor is at one pole
or the other almost by definition. The falsifiable content is QUANTITATIVE: for a
given substrate + graded perturbation, does ρ go to the SPECIFIC predicted pole?

EMPIRICAL STATUS (2026-07-03): tested cleanly — macaque ECoG (128-ch subdural,
right grain), propofol vs ketamine, matched awake baseline on the same implant.
RESULT: the framework's ORIGINAL single-pole direction (M=0 → ρ↑ toward RIGIDITY)
is SUPPORTED. Both anesthetics drove k_eff↓ / ρ↑ broadband — propofol 14.9→6.4
(ρ 0.062→0.153), ketamine 14.5→5.3 (ρ 0.064→0.185), large effects (d≈−5, p≈4e-5) —
REVERSING the earlier confounded scalp-EEG / post-anoxic arousal result (which had
shown the opposite; it was a grain + perturbation artifact). So maintenance
withdrawal drives toward rigidity at the coordinating grain, as originally claimed.

What is NOT supported is the stronger PREDICTIVE embellishment — that the
anesthetic's receptor mechanism selects the pole (propofol→rigidity vs
ketamine→chaos). Both agents went to rigidity; ketamine never reached chaos; and
the pole flips with analysis band (propofol → chaos in gamma). So the CHAOS exit
(`rho_exit_chaos`) is real MATHEMATICALLY (α<0) and at EXTREMES (burst-suppression /
isoelectric death), but it is NOT agent-selected; the empirically-supported default
under clean maintenance-withdrawal is RIGIDITY. Robustness caveats: one monkey
(Chibi), ECoG field (not single-unit), gamma-band flip. Net: the original
directional dynamics gains support at a second clean substrate; the two-pole
predictive speculation does not. (`experiments/keff_saturation/spectral_twopole_summary.md`.)

TRAJECTORY / ORDERING TEST (2026-07-03). The prior test compared two endpoints
(awake vs deep). This one slides a window across the CONTINUOUS induction to ask
the causal-ordering question this file's framing stakes a claim on: the corridor
is written as "a MAINTAINED state, held by non-trivial M(t)", which predicts that
under anesthesia the maintenance term γM (Axis 2, measured as broken detailed
balance) should withdraw BEFORE or WITH the structural k_eff collapse (Axis 1) —
maintenance withdrawal DRIVES the exit, so it cannot lag. Same macaque ECoG
(Chibi, 128-ch, continuous Session2), propofol and ketamine, broadband 1–100 Hz,
20 s / 5 s windows; DB via winding + phase-randomized circulation null.
RESULT: the ordering prediction is NOT supported.
  • k_eff (Axis 1) collapses under BOTH agents (propofol sharp, midpoint 142 s ±4 s;
    ketamine gradual, 176 s). ⚠ SUPERSEDED BY THE GEORGE REPLICATION (see below):
    this collapse is CHIBI-SPECIFIC and did not replicate; the earlier reading of it
    as "the robust correlate of fading consciousness" is RETRACTED.
  • Propofol: γM DOES eventually withdraw (circulation |z| 5.4→0.93, dropping below
    the ~1.5 null into the DB-satisfying "bound" cell) — but its transition is noisy
    and NOT resolvably before k_eff (winding −14 s, circ +41 s; wide CIs straddle the
    sharp k_eff time; the strong estimator if anything LAGS). Ordering: UNRESOLVED.
  • Ketamine (DECISIVE): k_eff collapses just as fully while detailed balance is
    PRESERVED (winding 3.3→4.3↑, circ 5.6→6.9↑, both far above null throughout deep).
    So structural corridor-exit occurs WITHOUT maintenance withdrawal — a clean
    counter-example in the NECESSITY direction to "the corridor structure is held by
    γM". Deep ketamine sits in the coordinating cell (low-rank + breaks DB) yet is
    unconscious: the 2×2 CELL does not determine consciousness; the k_eff DROP from
    the system's own baseline does.
IMPLICATION for the theorems below. `rho_drift_at_zero_maintenance` (M=0 → drift)
is a conditional and is NOT contradicted — ketamine never sets M=0. What is undercut
is the stronger EXPLANATORY reading that structural corridor-exit IMPLIES maintenance
failure: real loss of consciousness (ketamine) exits the k_eff corridor with γM
fully intact. Maintenance withdrawal is (at most) sufficient, NOT necessary, for
structural collapse. POSITIVE by-product: the two agents land in DIFFERENT 2×2 cells
(propofol→bound, ketamine→coordinating), the dynamical echo of the static
axis-independence result — Axis 1 collapses while Axis 2 does (propofol) or does not
(ketamine), independently. Caveats: ECoG field grain, weak/noisy DB signal (ordering
limited by the DB estimator, not k_eff), one monkey, broadband only.
(`experiments/keff_saturation/spectral_anesthesia_trajectory_summary.md`.)

GEORGE REPLICATION (2026-07-04) — the structural claim does NOT survive a second
animal; the maintenance claim does. Same pipeline, second macaque (George), both
anesthetics, within-session contrasts against George's own awake baseline.
  • ⚠ k_eff COLLAPSE FAILS TO REPLICATE, and reverses sign. George: propofol
    7.10→7.88, ketamine 5.83→6.94 — both RISE (Cliff's δ 0.51 / 0.44, p≈1e-3 /
    3e-7), against Chibi's 13.9→6.2 and 13.8→5.25 (δ=1.0 both). This is not mere
    dynamic-range compression (George's absolute k_eff ≈6–7 vs Chibi ≈14, a
    field/reference confound): the DIRECTION is opposite. Therefore "k_eff collapse
    is the robust dynamical correlate of fading consciousness" is FALSIFIED as a
    cross-animal claim; it was preparation-specific. Absolute ECoG-field k_eff is
    not portable across animals, and its within-session sign is not stable either.
  • ✓ THE MAINTENANCE SPLIT REPLICATES 2/2, on the trustworthy phase-randomized
    circulation null: deep propofol falls BELOW the ~1.5 null (Chibi 0.93, George
    1.07) = the BOUND cell; deep ketamine stays ABOVE it (Chibi 6.9, George 4.62)
    = the COORDINATING cell. The cell is fixed by the deep level vs the null, so it
    is baseline-independent. This is a drug-specific signature (GABAergic quiescence
    vs dissociative activation), NOT a consciousness correlate — both agents render
    the animal unconscious yet land in DIFFERENT cells.
  • ⚠ THE KETAMINE COUNTER-EXAMPLE IS CHIBI-ONLY (n=1), not replicated. The
    counter-example requires structure to collapse WHILE maintenance persists;
    George has no structural collapse, so the configuration never arises there. Only
    its "ketamine preserves DB" half replicates. The necessity-direction refutation
    of "the corridor is held by γM" therefore rests on a single animal.
  • ✓ BUT George supplies the BEST axis-independence evidence in the program, and it
    is NATURAL rather than constructed: at deep, in the SAME animal, same electrodes,
    same band, same estimator, the two agents are MATCHED on rank (k_eff 7.88 vs
    6.94) while differing 4.3× on maintenance (circ |z| 1.07 vs 4.62, straddling the
    null). Two real conditions matched on one axis and differing on the other — which
    the phase-randomized scramble in the static run could not provide (scrambling
    destroys both axes at once). Structure and maintenance are independent knobs.
NET: neither axis is a validated consciousness correlate. What reproduces across
animals is a drug-specific MAINTENANCE signature and the INDEPENDENCE of the two
axes. Caveats: ECoG field grain; one session per agent per animal; broadband only
(band-lability shown by the two-pole test); winding is the weak estimator, direct
circulation the trustworthy one; ketamine George had a top-up injection.
(`experiments/keff_saturation/spectral_anesthesia_george_summary.md`.)

The corridor's bounds are substrate-specific (the earlier universal ρ_c ≈ 0.43 is
retracted); the framework asserts the corridor as the structural object.
-/

import Mathlib.Analysis.SpecialFunctions.Pow.Real
import CoherenceRatchet.Core.BaseIdentity

namespace CoherenceRatchet.Core.Dynamics

/-- Shared environment / selection pressure. Abstract; substrate-specific
    instantiations include thermal coupling (GPU), shared training corpus
    (foundation models), shared political pressure (institutions), etc. -/
structure SelectionPressure where
  intensity : ℝ
  nonneg : 0 ≤ intensity

/-- The spontaneous correlation drift function α(ρ, S). Framework primitive.
    Monotone in S. Its SIGN is substrate- and perturbation-specific: α > 0 drives
    ρ up toward the rigidity pole (ρ → 1); α < 0 drives ρ down toward the chaos
    pole (ρ → 0). The earlier assertion "positive at ρ < 1 is the default" is
    RETRACTED (single-pole over-specification). Functional form substrate-specific;
    the framework asserts existence and uses properties via dρ/dt = α − γM.
    Declared as `axiom` to make the framework-primitive status explicit. -/
axiom α (ρ : ℝ) (S : SelectionPressure) : ℝ

/-- The active coherence-management coefficient γ. Framework primitive set
    by the substrate's capacity to do anti-correlation work. Empirically
    measured per-substrate; not derivable internally. -/
axiom γ : ℝ

/-- The active coherence-management function M(t). Framework primitive.
    Concrete instantiations: audit pressure on a cascade, federation
    diversity, redundancy with independent failure modes, etc. -/
axiom M : ℝ → ℝ

/-- The full ρ-dynamics. -/
noncomputable def dρ_dt (ρ : ℝ) (S : SelectionPressure) (t : ℝ) : ℝ :=
  α ρ S - γ * M t

/-- RIGIDITY EXIT (α > 0 case). At M = 0 with α > 0, ρ increases — the system
    drifts toward the rigidity pole (ρ → 1). This is ONE of the two corridor
    exits; the other is `rho_exit_chaos`. Together they are the structural
    argument for why coherence management is necessary work, not optional polish.
    (Reused by `Cosmology.RecursiveLifecycle`.) -/
theorem rho_drift_at_zero_maintenance
    (ρ : ℝ) (S : SelectionPressure) (t : ℝ)
    (h : M t = 0) (h_alpha_pos : α ρ S > 0) :
    dρ_dt ρ S t > 0 := by
  unfold dρ_dt
  rw [h]
  linarith

/-- CHAOS EXIT (α < 0 case). At M = 0 with α < 0, ρ decreases — the system drifts
    toward the chaos pole (ρ → 0). The second corridor exit, missing from the
    earlier single-pole formulation. Empirically the post-anoxic-coma direction:
    maintenance withdrawal that suppresses/fragments rather than homogenizes. -/
theorem rho_exit_chaos
    (ρ : ℝ) (S : SelectionPressure) (t : ℝ)
    (h : M t = 0) (h_alpha_neg : α ρ S < 0) :
    dρ_dt ρ S t < 0 := by
  unfold dρ_dt
  rw [h]
  linarith

/-- CORRIDOR REQUIRES MAINTENANCE. At any equilibrium (dρ/dt = 0) the active
    maintenance exactly balances the spontaneous drift: γ·M(t) = α(ρ, S). Hence
    whenever α ≠ 0, holding the corridor requires non-trivial maintenance
    (γ·M ≠ 0) — the corridor is a MAINTAINED state, not a passive attractor. -/
theorem corridor_requires_maintenance
    (ρ : ℝ) (S : SelectionPressure) (t : ℝ)
    (h_eq : dρ_dt ρ S t = 0) :
    γ * M t = α ρ S := by
  unfold dρ_dt at h_eq
  linarith

/-- The upper corridor bound ρ_c (= ρ_upper). Substrate-specific framework
    primitive. Previously asserted as 0.43 based on CCA v3 cross-substrate
    measurement; that universal-value claim does not survive the
    cross-substrate ρ distribution observed in RATCHET (substrate means
    span the (0, 1) interval). Now axiomatized as substrate-specific;
    per-substrate value determined by the substrate's engine and data. -/
axiom ρ_c : ℝ

/-- The order parameter φ as deviation from the local upper corridor bound. -/
noncomputable def φ (ρ : ℝ) : ℝ :=
  (ρ_c - ρ) / ρ_c

end CoherenceRatchet.Core.Dynamics
