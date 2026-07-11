#!/usr/bin/env python3
"""
Stellar-to-halo-mass (SHM) efficiency curves epsilon(M_halo, z), implemented from the
published fitted forms. FETCHED-NOT-REDERIVED: parameter values are transcribed from the
source papers (verified against the arXiv PDFs), not re-fit here.

All halo masses below are in SOLAR MASSES (Msun), the units of the source papers. The
TNG scan axis is in Msun/h (h=0.6774); convert with  M[Msun/h] = M[Msun] * h  (so
1.09e12 Msun = 7.4e11 Msun/h). Papers used slightly different h in their own halo
definitions (Moster+2013 WMAP7 h~0.70; Behroozi+2013 h=0.7); that ~0.15 dex convention
ambiguity is smaller than our 0.4-dex bin width and is flagged, not corrected.

Sources:
  Moster, Naab & White 2013, MNRAS 428, 3121 (arXiv:1205.5807), Eqs. 2 & 11-14, Table 1.
  Behroozi, Wechsler & Conroy 2013, ApJ 770, 57 (arXiv:1207.6105), Eqs. 3-4 & Sec. 5
    best-fit parameters (transcribed from the PDF parameter block).
  Behroozi et al. 2019 (UniverseMachine), MNRAS 488, 3143: peak ~10^12 Msun, drifting up
    with z; used only as a cited cross-check value, form not re-implemented.
"""
import numpy as np

# ============================================================================
# Moster, Naab & White 2013  (double power law; X(z) = X10 + X11 * z/(z+1))
# ============================================================================
MOSTER = dict(M10=11.590, M11=1.195, N10=0.0351, N11=-0.0247,
              b10=1.376, b11=-0.826, g10=0.608, g11=0.329)   # b=beta, g=gamma

def moster_ratio(logMh_Msun, z):
    """m*/Mhalo (efficiency) from Moster+2013 Eq.2 with z-evolution Eqs.11-14."""
    x = z / (z + 1.0)
    logM1 = MOSTER["M10"] + MOSTER["M11"] * x
    N = MOSTER["N10"] + MOSTER["N11"] * x
    beta = MOSTER["b10"] + MOSTER["b11"] * x
    gamma = MOSTER["g10"] + MOSTER["g11"] * x
    r = 10.0 ** (logMh_Msun - logM1)
    return 2.0 * N / (r ** (-beta) + r ** gamma)

def moster_peak_logMh(z):
    """log10 M_halo [Msun] where m*/Mh is maximal at redshift z (analytic:
    M_peak = M1 (beta/gamma)^(1/(beta+gamma)))."""
    x = z / (z + 1.0)
    logM1 = MOSTER["M10"] + MOSTER["M11"] * x
    beta = MOSTER["b10"] + MOSTER["b11"] * x
    gamma = MOSTER["g10"] + MOSTER["g11"] * x
    return logM1 + np.log10(beta / gamma) / (beta + gamma)

# ============================================================================
# Behroozi, Wechsler & Conroy 2013  (Eqs. 3-4; nu(a)=exp(-4a^2))
# ============================================================================
BEHROOZI = dict(
    logeps0=-1.777, eps_a=-0.006, eps_z=-0.000, eps_a2=-0.119,
    logM1_0=11.514, M1_a=-1.793, M1_z=-0.251,
    alpha0=-1.412, alpha_a=0.731,
    delta0=3.508, delta_a=2.608, delta_z=-0.043,
    gamma0=0.316, gamma_a=1.319, gamma_z=0.279)

def _behroozi_params(z):
    a = 1.0 / (1.0 + z)
    nu = np.exp(-4.0 * a * a)
    B = BEHROOZI
    logM1 = B["logM1_0"] + (B["M1_a"] * (a - 1) + B["M1_z"] * z) * nu
    logeps = (B["logeps0"] + (B["eps_a"] * (a - 1) + B["eps_z"] * z) * nu
              + B["eps_a2"] * (a - 1))
    alpha = B["alpha0"] + (B["alpha_a"] * (a - 1)) * nu
    delta = B["delta0"] + (B["delta_a"] * (a - 1) + B["delta_z"] * z) * nu
    gamma = B["gamma0"] + (B["gamma_a"] * (a - 1) + B["gamma_z"] * z) * nu
    return logM1, logeps, alpha, delta, gamma

def _behroozi_f(x, alpha, delta, gamma):
    return (-np.log10(10.0 ** (alpha * x) + 1.0)
            + delta * (np.log10(1.0 + np.exp(x))) ** gamma / (1.0 + np.exp(10.0 ** (-x))))

def behroozi_logMstar(logMh_Msun, z):
    logM1, logeps, alpha, delta, gamma = _behroozi_params(z)
    x = logMh_Msun - logM1
    return (logeps + logM1 + _behroozi_f(x, alpha, delta, gamma)
            - _behroozi_f(0.0, alpha, delta, gamma))

def behroozi_ratio(logMh_Msun, z):
    """M*/Mh efficiency."""
    return 10.0 ** (behroozi_logMstar(logMh_Msun, z) - logMh_Msun)

def behroozi_peak_logMh(z, grid=None):
    if grid is None:
        grid = np.linspace(10.5, 14.0, 1400)
    r = behroozi_ratio(grid, z)
    return float(grid[np.argmax(r)])

# ============================================================================
# convenience
# ============================================================================
H_TNG = 0.6774
def Msun_to_Msunh(logM_Msun):   # M[Msun/h] = M[Msun]*h
    return logM_Msun + np.log10(H_TNG)
def Msunh_to_Msun(logM_Msunh):
    return logM_Msunh - np.log10(H_TNG)

if __name__ == "__main__":
    for z in (0.0, 0.5, 1.0, 2.0):
        mp = moster_peak_logMh(z); bp = behroozi_peak_logMh(z)
        print(f"z={z:.1f}  Moster peak log10Mh = {mp:.3f} Msun ({Msun_to_Msunh(mp):.3f} Msun/h)"
              f"   Behroozi peak = {bp:.3f} Msun ({Msun_to_Msunh(bp):.3f} Msun/h)")
