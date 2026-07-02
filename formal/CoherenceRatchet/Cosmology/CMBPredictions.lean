/-
Cosmology.CMBPredictions — D4 RETRACTED: the CMB anomalies are not framework content

RETRACTION (2026-05-22, recorded in-lake 2026-07-01). This file once asserted
D4: that five large-angle CMB anomalies (axis of evil, cold spot, hemispherical
asymmetry, low-ℓ suppression, parity asymmetry) are TSVF post-selection
signatures of the joint multi-rung backward P_omega. D4 is retracted, on two
independent grounds:

1. F-11 fired (CorridorProjector.FelevenNoGo): the joint multi-rung backward
   P_omega operator is non-constructible at theorem strength (T1 geometric
   dilution; T2 holonomic area law). There is no operator for the anomalies
   to be a signature OF.

2. Direct test: the anomalies are within cosmic variance, and the CMB weight
   `w = exp(−β H_sum)` with `H_sum = Σ_ℓ (ρ_ℓ − ρ_mid)²` is additive over
   multipoles and factorizes, `w = Π_ℓ w_ℓ` — it does no joint cross-multipole
   work. The framework-distinctive prediction (a signed temporal drift of the
   shape profile via a time-dependent β(t)) lost its mechanism with the joint
   operator: no joint P_omega, no β(t), no drift. F-19 is moot.

What this file carried and no longer does: the axioms `C_l_TSVF` and
`prediction_low_l_suppression`, the four statement-only prediction theorems
(axis alignment, hemispherical asymmetry, cold spot, parity asymmetry), and
the conjunction `TSVF_predicts_all_CMB_anomalies`. All deleted; the retraction
record below replaces them, mirroring the `FelevenNoGo` pattern.

THE SURVIVING CMB CONTENT is the orthogonality theorem
(`CoherenceRatchet.CMBOrthogonality`): the soft forward P_omega leaves the
bulk CMB power spectrum exactly invariant, so the framework predicts EXACTLY
ΛCDM for the CMB — a provable consistency, not a distinctive prediction. The
framework is a strict extension of ΛCDM at the cosmological tier.

The anomaly catalog is retained below as documentation of what D4 claimed;
it is observational context, not framework content.

A1. Axis of evil — aligned ℓ=2/ℓ=3 preferred axis (~few permille under
    isotropic inflation).
A2. Cold spot — ~70 μK cold ~5° southern region (~1% under Gaussian inflation).
A3. Hemispherical asymmetry — north/south power difference (~1% under isotropy).
A4. Low-ℓ suppression — quadrupole power below ΛCDM expectation.
A5. Parity asymmetry — even-ℓ/odd-ℓ imbalance at low multipoles.

Individually few-percent flukes; the retracted claim was that collectively
they were post-selection signatures. Post-F-11 the framework reads them the
way standard cosmology does: within cosmic variance.
-/

import CoherenceRatchet.Cosmology.CorridorProjector
import CoherenceRatchet.Cosmology.PenrosePast

namespace CoherenceRatchet.Cosmology.CMB

/-- A CMB mode indexed by (l, m): spherical-harmonic decomposition of the
    temperature field on the cosmological 2-sphere. -/
structure CMBMode where
  l : Nat
  m : Int
  m_bound : Int.natAbs m ≤ l

/-- The power spectrum amplitude at multipole l (the standard observational
    C_l). Framework primitive; observationally measured (Planck 2018, ACT 2024). -/
axiom C_l : Nat → ℝ

/-- The standard inflationary ΛCDM prediction for C_l. Framework primitive
    (the theoretical baseline). Post-retraction this is also the framework's
    own CMB prediction: by the orthogonality theorem
    (`CMBOrthogonality.framework_cmb_power_eq_lcdm`) the framework predicts
    exactly ΛCDM. -/
axiom C_l_inflation : Nat → ℝ

/-- D4 retraction record. A flat fact with its evidence — the CMB-anomalies-as-
    TSVF-signatures claim is retracted. Not a `sorry`, not an axiom asserting
    a prediction: a recorded retraction, mirroring the `FelevenNoGo` pattern.
    The sole surviving CMB content is the orthogonality theorem
    (`CoherenceRatchet.CMBOrthogonality`). -/
structure DfourRetraction where
  /-- F-11: there is no joint multi-rung backward P_omega for the anomalies
      to be a signature of (`CorridorProjector.FelevenNoGo`). -/
  no_joint_operator : True
  /-- Direct test: the anomalies are within cosmic variance. -/
  anomalies_within_cosmic_variance : True
  /-- The CMB weight factorizes over multipoles (`w = Π_ℓ w_ℓ`); it does no
      joint cross-multipole work. -/
  weight_factorizes : True
  /-- The predicted temporal drift lost its mechanism: no joint P_omega,
      no β(t), no drift. F-19 is moot. -/
  no_drift_mechanism : True

/-- D4 is retracted: the retraction record is inhabited. -/
def D4_cmb_anomalies_retracted : DfourRetraction :=
  ⟨trivial, trivial, trivial, trivial⟩

end CoherenceRatchet.Cosmology.CMB
