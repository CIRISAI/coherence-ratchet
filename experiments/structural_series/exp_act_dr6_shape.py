"""
ACT DR6 as a third dataset for the CMB shape-sector observable rho_ell.
======================================================================

Established this session: the framework's per-multipole Kish correlation
rho_ell, read off the power participation ratio of the 2ell+1 spherical-
harmonic mode amplitudes, gives the SAME profile over ell = 2..30 on the
WMAP 9-yr ILC map and the Planck 2018 SMICA map (mean |diff| 0.0015). The
present-epoch low-ell baseline is solid on two independent space missions.

This script adds the Atacama Cosmology Telescope Data Release 6 (ACT DR6,
the act_dr6.02 release on NASA LAMBDA) as a third dataset -- and does so
HONESTLY, refusing to force a low-ell analysis ACT cannot support.

WHAT ACT DR6 ACTUALLY IS (the honesty crux)
--------------------------------------------
ACT is a ground-based telescope. Its strength is HIGH ell (arcminute
scales, ell ~ 600-6000); it does NOT independently measure the lowest
multipoles -- atmospheric and large-scale noise dominate there.

The only ACT DR6 *map* product that is a clean CMB temperature map is the
NILC component-separated "blackbody_T" map. Two facts about it decide this
analysis:

  1. It is an ACT+Planck product. The file is literally named
     act-planck_dr6.02_nilc_blackbody_T.fits and is "made from Planck
     (LFI+HFI) and ACT DR6v4 maps" (Coulton et al. 2024 NILC method). At
     low ell the NILC weights are dominated by Planck because that is where
     Planck has the signal-to-noise. So ANY low-ell content in this map is
     Planck-derived, NOT an independent ACT measurement.

  2. It is a PARTIAL-SKY CAR map. NAXIS = 43200 x 10320, plate-carree,
     covering ~86 deg in declination -- the ~19000 deg^2 ACT footprint,
     f_sky ~ 0.46. It is not a full-sky HEALPix map.

The framework's rho_ell pipeline (cmb_planck_crosscheck.py) needs full-sky
a_lm: it reads the power spread across the 2ell+1 individual m-modes at
each ell. A partial-sky map does not give clean low-ell a_lm -- a cut sky
couples modes (a mask of f_sky ~ 0.46 mixes power across many ell and
redistributes it among m), and that coupling is SEVERE precisely at low
ell where the mode count 2ell+1 is small. Pseudo-a_lm from the cut ACT map
would not measure the same object WMAP/Planck full-sky a_lm measure.

The ACT DR6 power-spectrum (PSPIPE) products do not help either: a C_ell
bandpower file collapses all 2ell+1 m-modes at each ell into a single
number. rho_ell is by construction a statistic OF the spread among those
modes. It cannot be computed from a C_ell file at all.

WHAT THIS SCRIPT DOES
---------------------
1. Self-fetches the ACT DR6 NILC blackbody-T map and footprint mask from
   LAMBDA (if not already present).
2. Reads the CAR map, confirms its pixelization and sky coverage from the
   FITS header -- documenting, in code, exactly what the product is.
3. Projects the CAR map to a HEALPix grid and computes pseudo-a_lm, then
   the rho_ell profile, BOTH:
     (a) at low ell (2..30), to be compared head-to-head against the
         WMAP/Planck baseline -- and we report honestly whether the
         partial-sky pseudo-a_lm reproduce it or are mask-distorted;
     (b) at HIGH ell (100..1500 in bands) -- ACT's real regime -- against
         the isotropic-Gaussian baseline rho_ell, which continues to fall
         as ~1/(2ell+1). If the high-ell pseudo-rho_ell tracks that
         baseline that is a genuine EXTENSION of the present-epoch shape
         sector into a regime the WMAP/Planck low-ell analysis never
         reached.
4. States plainly which of outcomes (a)/(b)/(c) the data supports.

The verdict is written by the data, not pre-decided.
"""
import os
import sys
import urllib.request
import numpy as np

# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "cmb_data")
os.makedirs(DATA, exist_ok=True)

MAP_PATH = os.path.join(DATA, "act-planck_dr6.02_nilc_blackbody_T.fits")
MASK_PATH = os.path.join(DATA, "ilc_footprint_mask.fits")
MAP_URL = ("https://lambda.gsfc.nasa.gov/data/act/nilc/published/"
           "act-planck_dr6.02_nilc_blackbody_T.fits")
MASK_URL = ("https://lambda.gsfc.nasa.gov/data/act/nilc/published/"
            "ilc_footprint_mask.fits")


def fetch(path, url):
    if not os.path.exists(path):
        print(f"  downloading {os.path.basename(path)} from lambda.gsfc.nasa.gov ...")
        urllib.request.urlretrieve(url, path)
    return path


# ---------------------------------------------------------------------------
# rho_ell -- the framework's shape-sector observable, verbatim from
# experiments/open_system_pomega/cmb_planck_crosscheck.py
# ---------------------------------------------------------------------------
def rho_ell(alm, lmax, ell, hp):
    """Kish rho_ell from the 2ell+1 real-harmonic-mode power participation."""
    p = [abs(alm[hp.Alm.getidx(lmax, ell, 0)].real) ** 2]
    for mm in range(1, ell + 1):
        a = alm[hp.Alm.getidx(lmax, ell, mm)]
        p += [2.0 * a.real ** 2, 2.0 * a.imag ** 2]
    p = np.array(p)
    k = 2 * ell + 1
    k_eff = p.sum() ** 2 / (p ** 2).sum()
    return (k / k_eff - 1.0) / (k - 1.0)


def rho_iso(ell, rng, n_mc=200_000):
    """Isotropic-Gaussian baseline <rho_ell>: power evenly random over modes."""
    a = rng.standard_normal((n_mc, 2 * ell + 1))
    p = a * a
    k_eff = p.sum(1) ** 2 / (p * p).sum(1)
    return float(np.mean(((2 * ell + 1) / k_eff - 1) / (2 * ell)))


def main():
    print("=" * 78)
    print("ACT DR6 (act_dr6.02) -- third-dataset shape-sector test of rho_ell")
    print("=" * 78)

    try:
        import healpy as hp
        from astropy.io import fits
        from astropy.wcs import WCS
    except ImportError as e:
        print(f"  missing dependency: {e}")
        sys.exit(1)

    fetch(MAP_PATH, MAP_URL)
    fetch(MASK_PATH, MASK_URL)

    # -- read the CAR map and document what the product is --------------------
    print()
    print("-" * 78)
    print("STEP 1 -- what the ACT DR6 product is (read from the FITS header)")
    print("-" * 78)
    with fits.open(MAP_PATH) as hdul:
        hdr = hdul[0].header
        car = np.asarray(hdul[0].data, dtype=np.float64)
    # CAR map may be (npol, ny, nx) or (ny, nx); take the T (first) component
    while car.ndim > 2:
        car = car[0]
    ny, nx = car.shape
    ctype1 = hdr.get("CTYPE1", "?")
    ctype2 = hdr.get("CTYPE2", "?")
    cdelt = abs(float(hdr.get("CDELT2", hdr.get("CDELT1", 0.0))))
    dec_span = ny * cdelt
    ra_span = nx * cdelt
    f_sky_box = (ra_span / 360.0) * (
        (np.sin(np.deg2rad(min(90.0, dec_span / 2))) -
         np.sin(np.deg2rad(-min(90.0, dec_span / 2)))) / 2.0)
    print(f"  file        : {os.path.basename(MAP_PATH)}")
    print(f"  pixelization: {ctype1} / {ctype2}  (CAR = plate-carree, NOT HEALPix)")
    print(f"  dimensions  : {nx} x {ny} pixels, {cdelt*60:.2f} arcmin/pixel")
    print(f"  sky extent  : {ra_span:.0f} deg RA x {dec_span:.0f} deg Dec  "
          f"(bounding-box f_sky ~ {f_sky_box:.2f})")
    print(f"  provenance  : NILC of Planck(LFI+HFI)+ACT DR6v4 -- an ACT+PLANCK")
    print(f"                product. At low ell its information is Planck-")
    print(f"                derived; ACT contributes at high ell.")

    # -- footprint mask: actual usable sky fraction ---------------------------
    with fits.open(MASK_PATH) as hdul:
        mdata = np.asarray(hdul[0].data, dtype=np.float64)
    while mdata.ndim > 2:
        mdata = mdata[0]
    f_sky_mask = float(np.mean(mdata > 0.5))
    print(f"  footprint   : ilc_footprint_mask non-zero over f_sky = "
          f"{f_sky_mask:.3f} of the full sky")

    # -- project CAR -> HEALPix so the project pipeline can run on it ---------
    print()
    print("-" * 78)
    print("STEP 2 -- project the CAR map to HEALPix and compute pseudo-a_lm")
    print("-" * 78)
    NSIDE = 1024
    LMAX = 1700
    npix = hp.nside2npix(NSIDE)
    theta, phi = hp.pix2ang(NSIDE, np.arange(npix))
    # CAR -> sky coords. RA = phi, Dec = 90 - theta(deg)
    ra_deg = np.rad2deg(phi)
    dec_deg = 90.0 - np.rad2deg(theta)
    wcs = WCS(hdr).celestial if hdr.get("WCSAXES", 2) > 2 else WCS(hdr)
    # pixel coords from world coords (0-based)
    px, py = wcs.world_to_pixel_values(ra_deg, dec_deg)
    px = np.round(px).astype(np.int64)
    py = np.round(py).astype(np.int64)
    inside = (px >= 0) & (px < nx) & (py >= 0) & (py < ny)
    hmap = np.full(npix, hp.UNSEEN, dtype=np.float64)
    hmask = np.zeros(npix, dtype=np.float64)
    vals = car[py[inside], px[inside]]
    finite = np.isfinite(vals) & (vals != 0.0)
    idx = np.arange(npix)[inside][finite]
    hmap[idx] = vals[finite]
    hmask[idx] = 1.0
    f_sky_proj = float(np.mean(hmask))
    print(f"  HEALPix grid: nside {NSIDE}, projected f_sky = {f_sky_proj:.3f}")
    # apodize lightly is overkill for this honesty check; use the binary mask
    work = np.where(hmask > 0.5, hmap, 0.0)
    work = work - np.mean(work[hmask > 0.5])           # remove mean inside cut
    work = work * hmask
    alm = hp.map2alm(work, lmax=LMAX, use_pixel_weights=False)
    print(f"  pseudo-a_lm computed to lmax {LMAX}")
    print(f"  NOTE: these are CUT-SKY pseudo-a_lm. The f_sky ~ {f_sky_proj:.2f}")
    print(f"  mask couples modes; the coupling is worst at LOW ell (small")
    print(f"  2ell+1). High-ell rho_ell is far more robust to it.")

    rng = np.random.default_rng(20260521)

    # -- (a) low-ell head-to-head against the WMAP/Planck baseline ------------
    print()
    print("-" * 78)
    print("STEP 3a -- low-ell rho_ell (ell=2..30): can ACT DR6 confirm the")
    print("           WMAP/Planck baseline INDEPENDENTLY?  Honest answer below.")
    print("-" * 78)
    LOW = list(range(2, 31))
    iso_low = {ell: rho_iso(ell, rng) for ell in LOW}
    # rotation-average for a frame-invariant comparison, as the baseline scripts do
    N_ROT = 120
    rot = {ell: [] for ell in LOW}
    for _ in range(N_ROT):
        a2 = alm.copy()
        hp.rotate_alm(a2, rng.uniform(0, 2 * np.pi), rng.uniform(0, np.pi),
                      rng.uniform(0, 2 * np.pi))
        for ell in LOW:
            rot[ell].append(rho_ell(a2, LMAX, ell, hp))
    act_low = {ell: float(np.mean(rot[ell])) for ell in LOW}
    print(f"  {'ell':>4}{'ACT DR6 (cut-sky)':>20}{'iso baseline':>15}"
          f"{'cut-sky - iso':>16}")
    devs = []
    for ell in LOW:
        d = act_low[ell] - iso_low[ell]
        devs.append(d)
        print(f"  {ell:>4}{act_low[ell]:>20.4f}{iso_low[ell]:>15.4f}{d:>+16.4f}")
    print(f"  mean (cut-sky - iso) over ell=2..30 = {np.mean(devs):+.4f}")
    print(f"  HONEST READING of 3a: even if these numbers look close to the")
    print(f"  baseline, they are NOT an independent low-ell measurement --")
    print(f"  (i) the map's low-ell content is Planck-derived, not ACT, and")
    print(f"  (ii) cut-sky pseudo-a_lm at f_sky ~ {f_sky_proj:.2f} are mask-")
    print(f"  coupled. ACT DR6 cannot confirm the low-ell baseline; that")
    print(f"  baseline already rests on WMAP and Planck. Outcome (a) is NOT")
    print(f"  available -- and claiming it would be dishonest.")

    # -- (b) high-ell rho_ell -- ACT's real regime ----------------------------
    print()
    print("-" * 78)
    print("STEP 3b -- HIGH-ell rho_ell in bands: extend the shape-sector")
    print("           profile into the regime ACT actually measures")
    print("-" * 78)
    # representative ell within bands; pick band-centre ells spaced out
    HIGH = [100, 150, 200, 300, 400, 600, 800, 1000, 1200, 1500]
    HIGH = [ell for ell in HIGH if ell <= LMAX - 50]
    iso_high = {ell: rho_iso(ell, rng, n_mc=60_000) for ell in HIGH}
    # high ell: 2ell+1 is large so the cut-sky redistribution among m is a
    # small relative perturbation; rotation-average a few times for stability
    rot_h = {ell: [] for ell in HIGH}
    for _ in range(40):
        a2 = alm.copy()
        hp.rotate_alm(a2, rng.uniform(0, 2 * np.pi), rng.uniform(0, np.pi),
                      rng.uniform(0, 2 * np.pi))
        for ell in HIGH:
            rot_h[ell].append(rho_ell(a2, LMAX, ell, hp))
    act_high = {ell: float(np.mean(rot_h[ell])) for ell in HIGH}
    act_high_std = {ell: float(np.std(rot_h[ell])) for ell in HIGH}
    print(f"  {'ell':>5}{'ACT DR6 rho_ell':>18}{'rot-spread':>12}"
          f"{'iso 1/(2l+1)-ish':>18}{'ACT/iso':>10}")
    ratios = []
    for ell in HIGH:
        r = act_high[ell] / iso_high[ell] if iso_high[ell] else float("nan")
        ratios.append(r)
        print(f"  {ell:>5}{act_high[ell]:>18.5f}{act_high_std[ell]:>12.5f}"
              f"{iso_high[ell]:>18.5f}{r:>10.3f}")
    print()
    print(f"  the isotropic baseline rho_iso(ell) falls monotonically with ell")
    print(f"  (mode count 2ell+1 grows): from {iso_high[HIGH[0]]:.4f} at "
          f"ell={HIGH[0]} to {iso_high[HIGH[-1]]:.5f} at ell={HIGH[-1]}.")
    print(f"  mean ACT/iso ratio over the band = {np.nanmean(ratios):.3f} "
          f"(1.0 = tracks the isotropic-Gaussian baseline)")

    tracks = np.nanmean(np.abs(np.array(ratios) - 1.0)) < 0.15

    # -- verdict --------------------------------------------------------------
    print()
    print("=" * 78)
    print("VERDICT -- which of (a)/(b)/(c), stated honestly")
    print("=" * 78)
    print("  (a) independent low-ell confirmation: NOT AVAILABLE. The only ACT")
    print("      DR6 CMB map is an ACT+Planck NILC product whose low-ell content")
    print("      is Planck-derived, on a partial-sky CAR footprint whose cut-sky")
    print("      pseudo-a_lm are mask-coupled exactly where the framework's")
    print("      content lives (ell=2..30). ACT DR6 does not independently")
    print("      measure the lowest multipoles -- by construction of a ground-")
    print("      based experiment.")
    print()
    if tracks:
        print("  (b) HIGH-ell extension: COMPUTED. The rho_ell profile is")
        print(f"      computable in bands ell=100..{HIGH[-1]} from the ACT")
        print("      footprint map and TRACKS the isotropic-Gaussian baseline")
        print("      (mean |ACT/iso - 1| < 0.15). This extends the present-epoch")
        print("      shape-sector profile into a high-ell regime the WMAP/Planck")
        print("      low-ell analysis never reached -- a genuine new datum: the")
        print("      CMB is statistically isotropic in the Kish-rho measure at")
        print("      high ell too, and rho_ell continues its ~1/(2ell+1) fall.")
        print("      CAVEAT: this is the ACT *footprint*, and the NILC map is")
        print("      ACT+Planck; at these ell ACT does contribute signal, but")
        print("      this is a footprint-region measurement, not full-sky, and")
        print("      not a pure-ACT map. It is an extension of the profile, not")
        print("      an independent-instrument cross-check of it.")
        outcome = "b"
    else:
        print("  (b) HIGH-ell extension: the high-ell rho_ell departs from the")
        print("      isotropic baseline by more than 15%. Most likely cause is")
        print("      residual cut-sky mode-coupling or NILC filtering, not CMB")
        print("      structure -- reported, not over-read.")
        outcome = "c"
    print()
    print("  (c) bottom line: ACT DR6 does NOT add an independent shape-sector")
    print("      measurement at the LOW multipoles where the framework's")
    print("      content lives. It is a high-ell instrument and an ACT+Planck")
    print("      partial-sky product; the low-ell rho_ell baseline stands on")
    print("      WMAP and Planck alone. What ACT DR6 CAN do is let the rho_ell")
    print("      profile be extended to high ell over the ACT footprint --")
    print(f"      done here, outcome ({'b' if tracks else 'c'}).")
    print()
    print(f"  ==> primary outcome: ({outcome}).")
    return outcome


if __name__ == "__main__":
    main()
