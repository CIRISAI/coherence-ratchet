"""
Planck cross-check of the WMAP CMB rho_ell profile.
===================================================

corridor_calibration_and_cmb_drift.py computed the present-epoch rho_ell
profile from the WMAP 9-yr ILC map and found one clean departure from the
isotropic baseline: the octupole, ell=3, rotation-averaged concentration
+0.033 above isotropic. WMAP ILC carries residual foreground; the test of
whether that excess is real CMB structure or ILC residual is whether it
reproduces in an independent map.

This recomputes the same Kish-rho profile on the Planck 2018 SMICA
component-separated CMB map (COM_CMB_IQU-smica_2048_R3.00, ESA Planck Legacy
Archive) and puts the two profiles side by side. At ell = 2..30 the CMB is
cosmic-variance-limited: WMAP and Planck measure the same sky and the low-ell
rho_ell values must agree if the measure is tracking CMB structure rather than
instrument/pipeline residual.
"""
import os
import urllib.request
import numpy as np
import healpy as hp

LMAX = 32
ELLS = list(range(2, 31))

MAPS = {
    "WMAP ILC 9yr": (
        "cmb_data/wmap_ilc_9yr_v5.fits",
        "https://lambda.gsfc.nasa.gov/data/map/dr5/dfp/ilc/wmap_ilc_9yr_v5.fits"),
    "Planck SMICA R3": (
        "cmb_data/planck_smica_R3.fits",
        "https://pla.esac.esa.int/pla/aio/product-action"
        "?MAP.MAP_ID=COM_CMB_IQU-smica_2048_R3.00_full.fits"),
}


def rho_ell(alm, lmax, ell):
    """Kish rho_ell from the 2ell+1 real-harmonic-mode power participation."""
    p = [abs(alm[hp.Alm.getidx(lmax, ell, 0)].real) ** 2]
    for mm in range(1, ell + 1):
        a = alm[hp.Alm.getidx(lmax, ell, mm)]
        p += [2.0 * a.real ** 2, 2.0 * a.imag ** 2]
    p = np.array(p)
    k = 2 * ell + 1
    k_eff = p.sum() ** 2 / (p ** 2).sum()
    return (k / k_eff - 1.0) / (k - 1.0)


def profile(path, url):
    if not os.path.exists(path):
        os.makedirs("cmb_data", exist_ok=True)
        urllib.request.urlretrieve(url, path)
    m = hp.read_map(path)
    m = hp.remove_dipole(m)
    alm = hp.map2alm(m, lmax=LMAX)
    gal = {ell: rho_ell(alm, LMAX, ell) for ell in ELLS}
    rng = np.random.default_rng(20260521)
    rot = {ell: [] for ell in ELLS}
    for _ in range(200):
        a2 = alm.copy()
        hp.rotate_alm(a2, rng.uniform(0, 2 * np.pi), rng.uniform(0, np.pi),
                      rng.uniform(0, 2 * np.pi))
        for ell in ELLS:
            rot[ell].append(rho_ell(a2, LMAX, ell))
    return gal, {ell: float(np.mean(rot[ell])) for ell in ELLS}, \
        {ell: float(np.std(rot[ell])) for ell in ELLS}


print("=" * 78)
print("Planck cross-check of the WMAP rho_ell profile")
print("=" * 78)
prof = {}
for label, (path, url) in MAPS.items():
    gal, rot, std = profile(path, url)
    prof[label] = (gal, rot, std)
    print(f"  {label}: nside-read OK, alm to lmax {LMAX}")

# isotropic-Gaussian baseline
rng = np.random.default_rng(7)
rho_iso = {}
for ell in ELLS:
    a = rng.standard_normal((200_000, 2 * ell + 1))
    p = a * a
    k_eff = p.sum(1) ** 2 / (p * p).sum(1)
    rho_iso[ell] = float(np.mean(((2 * ell + 1) / k_eff - 1) / (2 * ell)))

w_gal, w_rot, w_std = prof["WMAP ILC 9yr"]
p_gal, p_rot, p_std = prof["Planck SMICA R3"]

print()
print("  rotation-averaged (frame-invariant) rho_ell, WMAP vs Planck:")
print(f"  {'ell':>4}{'WMAP':>9}{'Planck':>9}{'iso':>9}{'W-P diff':>10}"
      f"{'W excess':>10}{'P excess':>10}")
agree = []
for ell in ELLS:
    diff = w_rot[ell] - p_rot[ell]
    agree.append(abs(diff))
    wex, pex = w_rot[ell] - rho_iso[ell], p_rot[ell] - rho_iso[ell]
    flag = "  <- octupole" if ell == 3 else ""
    print(f"  {ell:>4}{w_rot[ell]:>9.4f}{p_rot[ell]:>9.4f}{rho_iso[ell]:>9.4f}"
          f"{diff:>+10.4f}{wex:>+10.4f}{pex:>+10.4f}{flag}")

print()
print("=" * 78)
print("READING")
print("=" * 78)
print(f"  mean |WMAP - Planck| over ell=2..30 = {np.mean(agree):.4f}; "
      f"max = {np.max(agree):.4f}")
oc_w = w_rot[3] - rho_iso[3]
oc_p = p_rot[3] - rho_iso[3]
print(f"  octupole (ell=3) concentration excess over isotropic:")
print(f"    WMAP ILC   : {oc_w:+.4f}")
print(f"    Planck SMICA: {oc_p:+.4f}")
if oc_p > 0.015 and oc_w > 0.015:
    print(f"  The octupole excess REPRODUCES in Planck -- it is CMB structure,")
    print(f"  not WMAP ILC residual. The Kish-rho measure flags the octupole as")
    print(f"  a concentration anomaly in both independent maps.")
elif oc_p < 0.005:
    print(f"  The octupole excess does NOT reproduce in Planck -- the WMAP")
    print(f"  signal was ILC residual, not CMB structure.")
else:
    print(f"  The octupole excess is partial in Planck -- intermediate; the")
    print(f"  measure is sensitive to map/pipeline choices at this multipole.")
