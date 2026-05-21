"""
Age of the universe from CMB data — and why "max lifetime" is not computable.
=============================================================================

DIRECTION 2, tracked down honestly.

AGE. The age of the universe is a BULK observable: it is fixed by the ΛCDM
parameters, and those are fixed by the CMB power spectrum. The orthogonality
theorem (CMBOrthogonality.lean) proves the soft P_ω leaves every bulk observable
exactly invariant — so the framework's age equals ΛCDM's age, exactly, with
zero framework-distinctive content. "Calculating the age from CMB data" is
standard cosmology; the framework neither adds to it nor conflicts with it.

The honest calculation here: the age integral evaluated at the Planck 2018
CMB-fit ΛCDM parameters. (A from-scratch refit of the 6 parameters to the map
needs a Boltzmann code + MCMC — CAMB/CLASS — not reproduced here; the Planck
parameters ARE the CMB fit.)

  t_0 = (1/H0) ∫_0^1 da / (a · E(a)),   E(a) = √(Ω_r a^-4 + Ω_m a^-3 + Ω_Λ)

MAX LIFETIME / TIME TO FIDELITY. Tracked down, and the honest finding is a
negative: the data does not deliver it. Shown below by the future-time
integral.
"""
import numpy as np
from scipy.integrate import quad

# Planck 2018 (TT,TE,EE+lowE+lensing) — the CMB fit
H0 = 67.36                       # km/s/Mpc
Om = 0.3153                      # matter
OL = 0.6847                      # dark energy (cosmological constant)
Or = 9.1e-5                      # radiation (photons + neutrinos)
HUBBLE_TIME = 9.778 / (H0 / 100) # 1/H0 in Gyr

def E(a):
    return np.sqrt(Or * a ** -4 + Om * a ** -3 + OL)

print("=" * 78)
print("Age of the universe from CMB data (Planck 2018 ΛCDM fit)")
print("=" * 78)
integral, err = quad(lambda a: 1.0 / (a * E(a)), 1e-8, 1.0)
age = HUBBLE_TIME * integral
print(f"  H0 = {H0} km/s/Mpc  ->  Hubble time 1/H0 = {HUBBLE_TIME:.3f} Gyr")
print(f"  Ω_m = {Om}, Ω_Λ = {OL}, Ω_r = {Or:.1e}")
print(f"  age integral ∫_0^1 da/(a E) = {integral:.4f}")
print(f"  AGE OF THE UNIVERSE  t_0 = {age:.3f} Gyr")
print(f"  (Planck 2018 published value: 13.797 ± 0.023 Gyr — agreement)")
print()
print("  Framework content here: ZERO. The age is a bulk observable; the")
print("  orthogonality theorem makes the soft P_ω leave it exactly invariant.")
print("  Framework age == ΛCDM age. The framework reproduces, adds nothing.")

print()
print("=" * 78)
print("Max lifetime / time to fidelity — tracked down, and the finding is NO")
print("=" * 78)
# future proper time: ∫_1^A da/(a E(a)) as A -> ∞
for A in [10, 1e2, 1e4, 1e8, 1e16]:
    fut, _ = quad(lambda a: 1.0 / (a * E(a)), 1.0, A)
    print(f"  proper time from now to scale factor a={A:>8.0e}: "
          f"{HUBBLE_TIME * fut:8.1f} Gyr")
# analytic tail: for large a, E -> sqrt(OL), integrand -> 1/(a sqrt(OL))
print(f"  tail: for a -> ∞, E(a) -> √Ω_Λ, so the integrand -> 1/(a√Ω_Λ) and")
print(f"  ∫ da/(a√Ω_Λ) = ln(a)/√Ω_Λ -> ∞. The future proper time DIVERGES.")

print()
print("=" * 78)
print("READING")
print("=" * 78)
print(f"  AGE: {age:.2f} Gyr — real, standard, framework-neutral. Done.")
print()
print("  MAX LIFETIME: there is none to compute. Under ΛCDM with Ω_Λ > 0 the")
print("  universe expands forever — the future proper-time integral diverges")
print("  logarithmically (de Sitter asymptote). CMB data fixes Ω_Λ > 0 tightly,")
print("  so the CMB-derived cosmology has an INFINITE future, not a bounded")
print("  lifetime. There is no band to put because the quantity is not finite.")
print()
print("  TIME TO FIDELITY (framework reading): not computable either, for two")
print("  separate reasons, both honest:")
print("   1. A framework corridor-EXIT timescale at the cosmological scale is")
print("      downstream of P_ω as a constructed operator. P_ω is an axiom in")
print("      the lake (CorridorProjector.lean); MaximalClaim.lean tagged the")
print("      cosmological-time machinery as the BREAK. No operator -> no")
print("      corridor-exit time.")
print("   2. The shape-drift route is circular: the framework's CMB drift rate")
print("      was ESTIMATED as 'order unity over a Hubble time' (~10^-9/decade).")
print("      A 'time to fidelity' from that rate just returns ~one Hubble time")
print("      by construction — it is the input read back, not a measurement.")
print()
print("  Honest verdict: the age is yours, 13.8 Gyr. The max lifetime is not")
print("  in the data and not in the current framework. 'We have enough data'")
print("  is false for the second quantity — tracked down, reported as a null.")
