#!/usr/bin/env python
"""Fetch real Gaia DR3 astrometry in the GD-1 stream corridor and cache to FITS.

Data path: direct Gaia DR3 TAP query via astroquery (galstreams is installed but
its MWStreams init is broken against the local gala/astropy versions, so we use
gala's built-in GD1Koposov10 frame + a direct archive query instead). This is
REAL public Gaia DR3 data, not a mock.

Union of circular cones along the published GD-1 track (Koposov et al. 2010 frame),
with only distance/quality/broad-PM cuts that are NOT specific to GD-1's velocity,
so the same table serves as both the stream sample and the field sample.
"""
import warnings; warnings.filterwarnings('ignore')
import time
import numpy as np
import gala.coordinates as gc
import astropy.coordinates as coord
import astropy.units as u
from astroquery.gaia import Gaia
from astropy.table import vstack, unique

Gaia.ROW_LIMIT = -1
OUT = "gaia_gd1_raw.fits"


def fetch():
    phi1_c = np.arange(-85, 6, 3.5)
    cen = gc.GD1Koposov10(phi1=phi1_c * u.deg, phi2=np.zeros_like(phi1_c) * u.deg)
    ci = coord.SkyCoord(cen).transform_to(coord.ICRS())
    rad = 2.0
    tabs = []
    for i, (ra, dec) in enumerate(zip(ci.ra.deg, ci.dec.deg)):
        adql = f"""SELECT source_id, ra, dec, parallax, parallax_error, pmra, pmdec,
         pmra_error, pmdec_error, phot_g_mean_mag, bp_rp, radial_velocity, ruwe
         FROM gaiadr3.gaia_source
         WHERE 1=CONTAINS(POINT('ICRS',ra,dec), CIRCLE('ICRS',{ra:.4f},{dec:.4f},{rad}))
         AND phot_g_mean_mag BETWEEN 15.0 AND 20.5 AND parallax < 1.0 AND ruwe < 1.4
         AND sqrt(pmra*pmra+pmdec*pmdec) < 25 AND astrometric_params_solved > 3"""
        t = None
        for attempt in range(4):
            try:
                t = Gaia.launch_job_async(adql).get_results()  # async respects ROW_LIMIT=-1
                break
            except Exception as e:
                print(f"  cone {i} attempt {attempt} err: {str(e)[:70]}")
                time.sleep(3)
        if t is None:
            raise RuntimeError(f"cone {i} failed after retries")
        tabs.append(t)
        if i % 5 == 0:
            print(f"cone {i}/{len(phi1_c)} ra={ra:.1f} dec={dec:.1f} rows={len(t)}")
    allt = unique(vstack(tabs), keys="source_id")
    print("TOTAL unique rows:", len(allt))
    allt.write(OUT, overwrite=True)
    rv = allt["radial_velocity"]
    nrv = int(np.sum(~rv.mask)) if hasattr(rv, "mask") else int(np.sum(np.isfinite(rv)))
    print("rows with Gaia RV:", nrv)
    print("cached", OUT)


if __name__ == "__main__":
    fetch()
