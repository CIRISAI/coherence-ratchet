"""
CMB temporal drift from the soft P_omega -- the framework-distinctive signature.
================================================================================

The paper's corrected claim (Corridor Dynamics.tex, CMB temporal drift): with
P_omega reformulated as a soft graded operator, CMB modes drift along the
GRADIENT of the corridor-compatibility weight on the 2-sphere mode space.
Standard cosmology predicts zero pattern drift after last scattering; generic
post-selection predicts some unsigned drift; the soft-P_omega reading predicts
drift in a SPECIFIC SIGNED direction. That signed direction is the framework's
fingerprint -- pure anthropic conditioning has no weight function, hence no
gradient, hence predicts exactly zero drift.

This computes the signed direction.

Mode space. Multipoles ell = 2..L_MAX; the constituents at ell are the
2*ell+1 real spherical-harmonic coefficients a_{ell,m}. Statistical isotropy
(standard cosmology) = the a_{ell,m} i.i.d. Gaussian.

Rung observable. Within multipole ell, the framework's correlation rho_ell is
read off the Kish identity from the power participation ratio:
  k = 2*ell+1 constituents;  power p_m = a_{ell,m}^2;
  k_eff = (sum p)^2 / sum(p^2)  in [1, k];
  rho_ell = (k/k_eff - 1)/(k - 1)  in [0, 1].
Power spread evenly over all modes -> k_eff = k -> rho = 0 (chaos, isotropy).
Power concentrated in one mode -> k_eff = 1 -> rho = 1 (rigidity, a preferred
axis). The named CMB anomalies (axis of evil, hemispherical asymmetry) are
concentration anomalies: rho_ell pushed up off the isotropic floor.

Soft P_omega. H_sum = sum_ell (rho_ell - rho_mid)^2, the total corridor
penalty; the backward weight on a configuration is E_omega(beta) =
exp(-beta * H_sum). As cosmic time t advances toward the universal future
boundary t_f, the post-selection sharpens -- beta increases monotonically in t.

Drift. The drift of any observable A is d<A>/dt = (d<A>/dbeta)(dbeta/dt), with
dbeta/dt > 0. At beta -> 0 (we are far from t_f today),
  d<A>/dbeta |_0  =  -Cov_iso(A, H_sum),
an exact covariance over the isotropic ensemble -- no free parameter. Its SIGN
is the framework-distinctive prediction. Standard cosmology: beta frozen at 0,
zero drift. Soft-P_omega: drift = -Cov(A, H_sum), signed by corridor geometry.
"""
import numpy as np

rng = np.random.default_rng(20260521)

L_MIN, L_MAX = 2, 12
ELLS = list(range(L_MIN, L_MAX + 1))
N = 400_000                                  # Monte Carlo realizations
RHO_MID_VALS = [0.15, 0.25, 0.35]            # corridor centre (free parameter)

print("=" * 80)
print("CMB temporal drift from the soft P_omega")
print("=" * 80)
print(f"  multipoles ell = {L_MIN}..{L_MAX}; {N:,} isotropic realizations")
print(f"  rung observable rho_ell from the Kish identity on power participation")


def rho_of(a):
    """rho_ell for an (N, 2ell+1) array of real harmonic coefficients."""
    k = a.shape[1]
    p = a * a
    s1 = p.sum(axis=1)
    s2 = (p * p).sum(axis=1)
    k_eff = s1 * s1 / np.maximum(s2, 1e-300)         # in [1, k]
    return (k / k_eff - 1.0) / (k - 1.0)             # in [0, 1]


# isotropic ensemble: rho_ell per realization, and per-ell total power
rho = np.zeros((N, len(ELLS)))
power = np.zeros((N, len(ELLS)))
for j, ell in enumerate(ELLS):
    a = rng.standard_normal((N, 2 * ell + 1))        # statistical isotropy
    rho[:, j] = rho_of(a)
    power[:, j] = (a * a).sum(axis=1)

rho_iso = rho.mean(axis=0)                           # standard-cosmology baseline
print()
print("  standard-cosmology baseline (beta = 0): mean rho_ell per multipole")
for j, ell in enumerate(ELLS):
    print(f"    ell={ell:2d} (k={2*ell+1:2d}):  rho_ell = {rho_iso[j]:.4f}")


def drift(A, Hsum):
    """d<A>/dbeta at beta=0  =  -Cov(A, Hsum)  over the isotropic ensemble."""
    return -float(np.mean((A - A.mean()) * (Hsum - Hsum.mean())))


print()
print("=" * 80)
print("DRIFT DIRECTION  d<rho_ell>/dbeta = -Cov(rho_ell, H_sum)  per multipole")
print("=" * 80)
for rho_mid in RHO_MID_VALS:
    Hsum = ((rho - rho_mid) ** 2).sum(axis=1)
    print()
    print(f"  corridor centre rho_mid = {rho_mid}")
    print(f"  {'ell':>4} {'rho_iso':>9} {'baseline vs mid':>16} "
          f"{'d<rho>/dbeta':>14} {'drift':>10}")
    for j, ell in enumerate(ELLS):
        d = drift(rho[:, j], Hsum)
        side = "below mid" if rho_iso[j] < rho_mid else "above mid"
        arrow = "UP  (toward concentration)" if d > 0 else "down (toward isotropy)"
        print(f"  {ell:>4} {rho_iso[j]:>9.4f} {side:>16} {d:>14.2e}   {arrow}")
    # aggregate observables
    A_conc = rho.mean(axis=1)                         # mean concentration
    tot = power.sum(axis=1)
    even = sum(power[:, j] for j, e in enumerate(ELLS) if e % 2 == 0)
    A_par = (2 * even - tot) / tot                    # parity asymmetry
    A_low = power[:, 0] + power[:, 1]                 # ell=2,3 power (suppression)
    print(f"    aggregate  d<concentration>/dbeta = {drift(A_conc, Hsum):+.2e}")
    print(f"               d<parity asym>/dbeta   = {drift(A_par, Hsum):+.2e}")
    print(f"               d<low-ell power>/dbeta = {drift(A_low, Hsum):+.2e}")

# finite-beta robustness check (rho_mid = 0.25): is the linear sign stable?
print()
print("=" * 80)
print("FINITE-beta CHECK (rho_mid = 0.25): <rho_ell>_beta vs beta")
print("=" * 80)
rho_mid = 0.25
Hsum = ((rho - rho_mid) ** 2).sum(axis=1)
print(f"  {'ell':>4}" + "".join(f"{'b='+str(b):>11}" for b in [0, 2, 8, 20]))
for j, ell in enumerate(ELLS):
    row = f"  {ell:>4}"
    for beta in [0, 2, 8, 20]:
        w = np.exp(-beta * (Hsum - Hsum.min()))
        row += f"{np.average(rho[:, j], weights=w):>11.4f}"
    print(row)
ess = (np.exp(-20 * (Hsum - Hsum.min())).sum() ** 2
       / np.exp(-2 * 20 * (Hsum - Hsum.min())).sum())
print(f"  effective sample size at beta=20: {ess:,.0f} of {N:,}")

print()
print("=" * 80)
print("READING")
print("=" * 80)
print("  Standard cosmology: beta frozen at 0, the CMB pattern frozen after last")
print("  scattering -- d<A>/dt = 0. Pure anthropic conditioning: no weight")
print("  function, no H_sum, no gradient -- also exactly zero drift.")
print()
print("  The soft P_omega predicts a NON-ZERO, SIGNED, MULTIPOLE-RESOLVED drift:")
print("  d<rho_ell>/dbeta = -Cov(rho_ell, H_sum). A structured drift profile")
print("  where both null theories predict a flat zero -- that structure is the")
print("  framework-distinctive signature.")
print()
print("  But it is NOT a uniform 'anomalies strengthen.' The isotropic baseline")
print("  rho_ell is itself ell-dependent: high at ell=2 (~0.29 -- few modes, so")
print("  small-number statistics concentrate the power) falling to ~0.07 at")
print("  ell=12 (many modes, power spreads). Statistical isotropy is thus")
print("  rigidity-side at the quadrupole and chaos-side at high ell.")
print()
print("  For a mid-range corridor centre (rho_mid ~ 0.25-0.35) the generic")
print("  pattern: the QUADRUPOLE (ell=2) drifts DOWN toward isotropy while")
print("  higher multipoles drift UP toward concentration. The crossover")
print("  multipole and the aggregate sign depend on rho_mid. This corrects the")
print("  paper's parenthetical guess ('probably toward stronger anomaly")
print("  amplitude'): the drift is signed and ell-resolved, not uniformly")
print("  amplitude-increasing, and at ell=2 it generically runs toward isotropy.")
print()
print("  The sign pivots on rho_mid, the corridor centre -- uncalibrated. The")
print("  CMB drift PROFILE is computable; its hard sign is gated on pinning")
print("  rho_mid. Same master-parameter dependence the rung-budget calibration")
print("  found: the corridor centre/width controls the universal-scale")
print("  predictions, and is the empirical target that converts this signed")
print("  profile into a falsifiable direction.")
print()
print("  Scope: this v1 toy couples to within-ell concentration (the axis-of-")
print("  evil / hemispherical-asymmetry family). Parity drift is ~null (-1e-6)")
print("  and low-ell-power drift small -- they couple only if encoded into the")
print("  rung observable; a cross-ell H_sum carrying Piece-6 cross-rung coupling")
print("  is the named extension.")
