#!/usr/bin/env python
"""Figures for the Gaia phase-space ledger test (real data)."""
import warnings; warnings.filterwarnings("ignore")
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import astropy.coordinates as coord
import astropy.units as u
import gala.coordinates as gc
from astropy.table import Table

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
RNG = np.random.default_rng(20260710)


def gd1_arrays():
    t = Table.read(os.path.join(HERE, "gaia_gd1_raw.fits"))
    c = coord.SkyCoord(ra=np.asarray(t["ra"]) * u.deg, dec=np.asarray(t["dec"]) * u.deg,
                       pm_ra_cosdec=np.asarray(t["pmra"]) * u.mas / u.yr,
                       pm_dec=np.asarray(t["pmdec"]) * u.mas / u.yr,
                       frame="icrs").transform_to(gc.GD1Koposov10())
    phi1 = c.phi1.wrap_at(180 * u.deg).deg; phi2 = c.phi2.deg
    mu1 = c.pm_phi1_cosphi2.value; mu2 = c.pm_phi2.value
    box = (mu1 > -14) & (mu1 < -2) & (mu2 > -4) & (mu2 < 2)
    on = np.abs(phi2) < 0.8; off = (np.abs(phi2) > 1.5) & (np.abs(phi2) < 3.0)
    cand = on & box
    coef1 = np.polyfit(phi1[cand], mu1[cand], 2); coef2 = np.polyfit(phi1[cand], mu2[cand], 2)
    for _ in range(3):
        k = (np.abs(mu1[cand] - np.polyval(coef1, phi1[cand])) < 1.3) & \
            (np.abs(mu2[cand] - np.polyval(coef2, phi1[cand])) < 1.3)
        coef1 = np.polyfit(phi1[cand][k], mu1[cand][k], 2); coef2 = np.polyfit(phi1[cand][k], mu2[cand][k], 2)
    mem = on & box & (np.abs(mu1 - np.polyval(coef1, phi1)) < 1.0) & (np.abs(mu2 - np.polyval(coef2, phi1)) < 1.0)
    return phi1, mu1, mem, (off & box)


def orphan_arrays():
    from astroquery.vizier import Vizier
    Vizier.ROW_LIMIT = -1
    t = Vizier.get_catalogs("J/MNRAS/490/3508/s5dr1")[0]
    field = np.asarray(t["Field"]); rv = np.asarray(t["velcalib"], float)
    rverr = np.asarray(t["velcalib_std"], float)
    ra = np.asarray(t["RAJ2000"], float); de = np.asarray(t["DEJ2000"], float)
    good = np.isfinite(rv) & (np.abs(rv) < 500) & np.isfinite(rverr) & (rverr < 5)
    m = np.array(["Orphan-field" in f for f in field]) & good
    ra, de, rv, FLD = ra[m], de[m], rv[m], field[m]
    phi1 = coord.SkyCoord(ra=ra * u.deg, dec=de * u.deg).transform_to(
        gc.OrphanKoposov19()).phi1.wrap_at(180 * u.deg).deg
    mem = np.zeros(len(rv), bool); centers = []
    for f in set(FLD):
        idx = np.where(FLD == f)[0]
        if len(idx) < 25: continue
        v = rv[idx]; los = np.arange(v.min(), v.max(), 2.0)
        bn, bl = -1, los[0]
        for l in los:
            n = int(np.sum((v >= l) & (v < l + 16)))
            if n > bn: bn, bl = n, l
        cm = (v >= bl) & (v < bl + 16); mem[idx[cm]] = True
        centers.append((np.median(phi1[idx[cm]]), np.median(v[cm])))
    return phi1, rv, mem, np.array(centers)


def sfun(cols):
    C = np.corrcoef(np.vstack([np.asarray(c, float) for c in cols]))
    return -np.log(min(max(np.linalg.det(np.atleast_2d(C)), 1e-12), 1.0))


# --- Figure 1: GD-1 astrometric grain (selection-confounded) ---
p1, mu1, mem, field = gd1_arrays()
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].scatter(p1[field], mu1[field], s=3, c="0.7", label=f"field (S={sfun([p1[field],mu1[field]]):.2f})")
ax[0].scatter(p1[mem], mu1[mem], s=6, c="crimson", label=f"stream members (S={sfun([p1[mem],mu1[mem]]):.2f})")
ax[0].set_xlabel(r"$\phi_1$  (deg along GD-1)"); ax[0].set_ylabel(r"$\mu_{\phi_1}$ (mas/yr)")
ax[0].set_title("GD-1  (Gaia DR3, REAL 5D astrometry)"); ax[0].legend(fontsize=8); ax[0].set_ylim(-14, -2)
ax[1].text(0.02, 0.5,
           "PART A verdict: SELECTION-CONFOUNDED\n\n"
           "The stream track is real & tight, but members are\n"
           "SELECTED by a velocity-track band, which manufactures\n"
           "corr($\\phi_1,\\mu$).  A fake band through pure field stars\n"
           "gives S=1.10 >= the stream's 0.78.  Without the velocity\n"
           "selection the coherence dilutes to the field floor (0.06).\n"
           "Proper motion alone cannot separate real coherence from\n"
           "the selection filter.  -> see Part B (independent RV).",
           fontsize=9, va="center", family="monospace")
ax[1].axis("off")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "fig1_gd1_astrometry.png"), dpi=130); plt.close()

# --- Figure 2: Orphan RV grain (non-circular PASS) ---
ph, rv, mem, cen = orphan_arrays()
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].scatter(ph[~mem], rv[~mem], s=3, c="0.75", label=f"field / MW (S={sfun([ph[~mem],rv[~mem]]):.2f})")
ax[0].scatter(ph[mem], rv[mem], s=7, c="navy", label=f"cold-clump members (S={sfun([ph[mem],rv[mem]]):.2f})")
ax[0].scatter(cen[:, 0], cen[:, 1], s=70, marker="D", c="orange", edgecolor="k",
              zorder=5, label="per-field clump centers")
ax[0].set_xlabel(r"$\phi_1$ (deg along Orphan)"); ax[0].set_ylabel("radial velocity (km/s)")
ax[0].set_title("Orphan  (S5, REAL radial velocities)"); ax[0].legend(fontsize=8)

# permutation null of clump-center S
Sobs = sfun([cen[:, 0], cen[:, 1]])
Sperm = [sfun([cen[:, 0], RNG.permutation(cen[:, 1])]) for _ in range(2000)]
ax[1].hist(Sperm, bins=40, color="0.7", label="permuted (position-RV\nalignment destroyed)")
ax[1].axvline(Sobs, color="red", lw=2, label=f"observed S={Sobs:.2f}")
ax[1].set_xlabel("S of clump centers"); ax[1].set_ylabel("count")
ax[1].set_title(f"Non-circular permutation null (p={(np.sum(np.array(Sperm)>=Sobs)+1)/2001:.3f})")
ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(FIG, "fig2_orphan_rv.png"), dpi=130); plt.close()
print("wrote figures:", os.listdir(FIG))
