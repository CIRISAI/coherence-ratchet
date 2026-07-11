#!/usr/bin/env python3
"""
Pantheon+ SNe Ia likelihood module for the frozen halo-grain S(a) dark-energy test.

Provenance
----------
Data:  PantheonPlusSH0ES/DataRelease (github, main branch), files
  data/Pantheon+SH0ES.dat                    (1701 SNe light-curve params + zHD, m_b_corr)
  data/Pantheon+SH0ES_STAT+SYS.cov           (1701x1701 STAT+SYS covariance, magnitudes^2)
reproducing Brout et al. 2022 (ApJ 938, 110; arXiv:2202.04077), the Pantheon+ compilation.

Cosmology use (NOT H0):
  - drop Cepheid calibrators (IS_CALIBRATOR==1),
  - z_HD > 0.01 cut (peculiar-velocity floor; the standard Pantheon+ cosmology cut),
  - data vector = m_b_corr (Tripp/BBC-corrected apparent magnitude, mag),
  - model mu_shape(z) = 5 log10[(1+z) * Int_0^z dz'/E(z')]  (offset-free; the additive
    constant = M_B + 25 + 5 log10(c/H0) is marginalised ANALYTICALLY -> absorbs both the
    SN absolute magnitude M_B and H0). So SNe constrain the DE SHAPE (Om, and w0,wa for
    CPL) via the shape of the distance-redshift relation only.

Analytic offset marginalisation (flat prior on the constant offset), full covariance C:
    Delta = m_b_corr - mu_shape
    chi2  = Delta^T Cinv Delta - (1^T Cinv Delta)^2 / (1^T Cinv 1)
which is the profiled (== flat-prior-marginalised up to a constant) minimum over the offset.
"""
import numpy as np
from pathlib import Path
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
C_KM = 299792.458

# ---------------------------------------------------------------------------
# Load Pantheon+ (cosmology sample).
# ---------------------------------------------------------------------------
def load_pantheon(zmin=0.01):
    dat = DATA / "Pantheon+SH0ES.dat"
    lines = dat.read_text().splitlines()
    hdr = lines[0].split()
    ix = {name: i for i, name in enumerate(hdr)}
    rows = [ln.split() for ln in lines[1:] if ln.strip()]
    n_full = len(rows)                     # 1701, matches covariance dimension
    zHD = np.array([float(r[ix["zHD"]]) for r in rows])
    mb = np.array([float(r[ix["m_b_corr"]]) for r in rows])
    iscal = np.array([int(float(r[ix["IS_CALIBRATOR"]])) for r in rows])

    # full covariance: first line is N, then N*N entries row-major.
    cov_txt = (DATA / "Pantheon+SH0ES_STAT+SYS.cov").read_text().split()
    n_cov = int(cov_txt[0])
    assert n_cov == n_full, (n_cov, n_full)
    C_full = np.array(cov_txt[1:], dtype=np.float64).reshape(n_cov, n_cov)

    mask = (iscal == 0) & (zHD > zmin)
    z = zHD[mask]
    mu_obs = mb[mask]
    C = C_full[np.ix_(mask, mask)]
    return dict(z=z, mu_obs=mu_obs, cov=C, n=int(mask.sum()), n_full=n_full,
                zmin=zmin, zmax=float(z.max()))

_SNE = None
def sne():
    global _SNE
    if _SNE is None:
        _SNE = load_pantheon()
        _SNE["cinv"] = np.linalg.inv(_SNE["cov"])
        _SNE["ones"] = np.ones(_SNE["n"])
        _SNE["oCo"] = float(_SNE["ones"] @ _SNE["cinv"] @ _SNE["ones"])
    return _SNE

# ---------------------------------------------------------------------------
# mu_shape(z) from a background E(a). E_func takes scale factor a.
# Uses a cumulative-trapezoid comoving-distance spline for speed (1590 SNe).
# ---------------------------------------------------------------------------
def mu_shape(E_of_a, zmax):
    zg = np.linspace(0.0, zmax * 1.001 + 1e-3, 4000)
    a = 1.0 / (1.0 + zg)
    invE = 1.0 / E_of_a(a)                                 # E_of_a vectorised in a
    Dc = np.concatenate([[0.0], np.cumsum(0.5 * (invE[1:] + invE[:-1]) * np.diff(zg))])
    Dc_spl = CubicSpline(zg, Dc)
    def mu(zsn):
        dc = Dc_spl(zsn)
        return 5.0 * np.log10((1.0 + zsn) * dc)            # offset-free
    return mu

def chi2_sne(E_of_a):
    s = sne()
    mu = mu_shape(E_of_a, s["zmax"])(s["z"])
    delta = s["mu_obs"] - mu
    cinv = s["cinv"]
    b = float(s["ones"] @ cinv @ delta)
    c2 = float(delta @ cinv @ delta) - b * b / s["oCo"]
    return c2

if __name__ == "__main__":
    # Validation: LCDM chi2/dof against Pantheon+ published Om ~ 0.334 should be ~1.
    s = sne()
    print(f"loaded {s['n']} SNe (of {s['n_full']}), z in [{s['z'].min():.4f}, {s['zmax']:.4f}]")
    OM_R = 9.2e-5
    def E_lcdm(Om):
        def E(a):
            a = np.asarray(a, float)
            return np.sqrt(OM_R * a**-4 + Om * a**-3 + (1 - Om - OM_R))
        return E
    for Om in [0.30, 0.315, 0.334, 0.35]:
        c2 = chi2_sne(E_lcdm(Om))
        print(f"  LCDM Om={Om:.3f}: chi2={c2:.2f}  chi2/dof={c2/(s['n']-1):.4f}")
    # scan for SNe-preferred Om
    oms = np.linspace(0.28, 0.42, 71)
    c2s = [chi2_sne(E_lcdm(o)) for o in oms]
    j = int(np.argmin(c2s))
    print(f"  SNe-only LCDM best Om={oms[j]:.3f} chi2={c2s[j]:.2f}")
