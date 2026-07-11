#!/usr/bin/env python3
"""
DES-SN5YR (Dovekie recalibration) SNe likelihood — the SENSITIVITY compilation.

Provenance: des-science/DES-SN5YR (github, main), 4_DISTANCES_COVMAT/
  DES-Dovekie_HD.csv   (1820 SNe: zHD, MU distance modulus)
  STAT+SYS.npz         (upper-triangular STAT+SYS INVERSE covariance, 1820x1820, mag^-2)
DES-SN5YR: DES Collaboration 2024 (arXiv:2401.02929); Dovekie cross-calibration recalib.
This is the compilation DESI's evolving-DE preference leans on, and the one at the centre
of the DES-Y5 vs Pantheon+ low-z calibration debate (K5). Used here as an independent SNe
sensitivity test of the framework's joint preference.

Same offset-marginalised likelihood as the DES team's own code (marginalise M analytically):
  chi2 = delta^T Cinv delta - (1^T Cinv delta)^2 / (1^T Cinv 1)      [+ const dropped]
delta = MU_obs - mu_shape ; mu_shape(z) = 5 log10[(1+z) Int dz'/E] (offset-free).
Cinv is used DIRECTLY (the npz stores the inverse of STAT+SYS).
"""
import numpy as np
from pathlib import Path
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

def load_des():
    npz = np.load(DATA / "DES_STATSYS.npz")
    n = int(npz["nsn"][0])
    cinv = np.zeros((n, n))
    cinv[np.triu_indices(n)] = npz["cov"]
    il = np.tril_indices(n, -1)
    cinv[il] = cinv.T[il]                       # symmetric inverse covariance
    lines = (DATA / "DES-Dovekie_HD.csv").read_text().splitlines()
    hdr = [l for l in lines if l.startswith("VARNAMES")][0].split()[1:]
    ix = {c: i for i, c in enumerate(hdr)}
    rows = [l.split() for l in lines if l.startswith("SN:")]
    z = np.array([float(r[1 + ix["zHD"]]) for r in rows])
    mu = np.array([float(r[1 + ix["MU"]]) for r in rows])
    assert len(z) == n, (len(z), n)
    return dict(z=z, mu_obs=mu, cinv=cinv, n=n, zmax=float(z.max()))

_DES = None
def des():
    global _DES
    if _DES is None:
        _DES = load_des()
        _DES["ones"] = np.ones(_DES["n"])
        _DES["oCo"] = float(_DES["ones"] @ _DES["cinv"] @ _DES["ones"])
    return _DES

def mu_shape(E_of_a, zmax):
    zg = np.linspace(0.0, zmax * 1.001 + 1e-3, 4000)
    a = 1.0 / (1.0 + zg)
    invE = 1.0 / E_of_a(a)
    Dc = np.concatenate([[0.0], np.cumsum(0.5 * (invE[1:] + invE[:-1]) * np.diff(zg))])
    spl = CubicSpline(zg, Dc)
    return lambda zsn: 5.0 * np.log10((1.0 + zsn) * spl(zsn))

def chi2_sne(E_of_a):
    d = des()
    mu = mu_shape(E_of_a, d["zmax"])(d["z"])
    delta = d["mu_obs"] - mu
    cinv = d["cinv"]
    b = float(d["ones"] @ cinv @ delta)
    c2 = float(delta @ cinv @ delta) - b * b / d["oCo"]
    return c2

if __name__ == "__main__":
    d = des()
    OM_R = 9.2e-5
    def E_lcdm(Om):
        return lambda a: np.sqrt(OM_R * np.asarray(a, float)**-4 + Om * np.asarray(a, float)**-3 + (1 - Om - OM_R))
    print(f"loaded {d['n']} DES-Dovekie SNe, z in [{d['z'].min():.4f}, {d['zmax']:.4f}]")
    oms = np.linspace(0.26, 0.44, 91)
    c2s = [chi2_sne(E_lcdm(o)) for o in oms]
    j = int(np.argmin(c2s))
    print(f"DES-only LCDM best Om={oms[j]:.3f} chi2={c2s[j]:.2f} chi2/dof={c2s[j]/(d['n']-1):.4f}")
    for Om in (0.30, 0.315, 0.35, 0.40):
        print(f"  LCDM Om={Om:.3f}: chi2={chi2_sne(E_lcdm(Om)):.2f}")
