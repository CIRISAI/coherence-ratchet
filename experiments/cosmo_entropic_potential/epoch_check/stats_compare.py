#!/usr/bin/env python3
"""
Two decisive statistics on top of cpl_projection.py:

(1) Mahalanobis distance of the framework's CPL-PROJECTED (w0,wa) point from DESI's
    (w0,wa) posterior. The desi_thawing_likelihood note did this for the PHYSICAL /
    uniform-fit point (-0.90,-0.10) and got ~3-4 sigma. Here we redo it for the point
    DESI would actually assign the framework's curve -- the CPL projection -- which is
    the fair comparison.

(2) Crossing-epoch uncertainty. z_cross = 1/(1+(1+w0)/wa) - 1 is an ill-conditioned
    function of (w0,wa). Propagate DESI's own posterior to get the uncertainty on
    DESI's "z~0.35", and compare to the framework's projected crossing distribution.
    Tests whether "0.8 physical vs 0.35 DESI, a 2x miss" survives once BOTH sides
    carry their real error bars.
"""
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
res = json.load(open(HERE / "cpl_projection_results.json"))

# DESI DR2 + CMB + Pantheon+ CPL posterior (arXiv:2503.14738)
DESI_W0, DESI_WA = -0.838, -0.62
SIG_W0, SIG_WA, RHO = 0.055, 0.20, -0.7      # marginal errors + standard w0-wa anticorr
COV = np.array([[SIG_W0**2, RHO*SIG_W0*SIG_WA],
                [RHO*SIG_W0*SIG_WA, SIG_WA**2]])
COVINV = np.linalg.inv(COV)

def maha(w0, wa):
    d = np.array([w0 - DESI_W0, wa - DESI_WA])
    return float(np.sqrt(d @ COVINV @ d))

def cross_z(w0, wa):
    if wa == 0: return np.nan
    a = 1.0 + (1.0 + w0) / wa
    return 1.0/a - 1.0 if a > 0 else np.nan

print("="*74)
print("(1) MAHALANOBIS distance of framework CPL-projected point from DESI ellipse")
print(f"    DESI (w0,wa)=({DESI_W0},{DESI_WA})  sig=({SIG_W0},{SIG_WA}) rho={RHO}")
print("="*74)
print(f"    {'method':16s} {'pooled (w0,wa)':>22s} {'Maha sigma':>11s}")
methods = ["dist_BAO+CMB", "dist_BAO_only", "rho_DEweighted", "w_uniform", "w_DE"]
for m in methods:
    d = res["pooled"][m]
    print(f"    {m:16s} ({d['w0']:+.3f},{d['wa']:+.3f})   {maha(d['w0'],d['wa']):8.2f}")
# per-box mean point too
print("    --- per-box-mean points ---")
for m in methods:
    s = res["per_box_summary"][m]
    print(f"    {m:16s} ({s['w0_mean']:+.3f},{s['wa_mean']:+.3f})   "
          f"{maha(s['w0_mean'],s['wa_mean']):8.2f}")
# anchors for calibration
print("    --- calibration anchors ---")
for name,(w0,wa) in [("LCDM",(-1.0,0.0)),
                     ("cell-grain/thawing",(-0.897,-0.099)),
                     ("halo w_today only (-0.841, wa=? use -0.5)",(-0.841,-0.5))]:
    print(f"    {name:40s} ({w0:+.3f},{wa:+.3f}) Maha={maha(w0,wa):.2f}")

print()
print("="*74)
print("(2) CROSSING-EPOCH uncertainty (z_cross is ill-conditioned in (w0,wa))")
print("="*74)
rng = np.random.default_rng(0)
L = np.linalg.cholesky(COV)
samp = np.array([DESI_W0, DESI_WA])[None,:] + (rng.standard_normal((200000,2)) @ L.T)
zc = np.array([cross_z(w0,wa) for w0,wa in samp[:20000]])  # subsample for speed
zc = zc[np.isfinite(zc)]
# only physical crossings in (0, ~3)
zc_phys = zc[(zc>-0.0)&(zc<3.0)]
frac_nocross = np.mean(~np.isfinite([cross_z(w0,wa) for w0,wa in samp[:20000]]) |
                       (np.array([cross_z(w0,wa) for w0,wa in samp[:20000]])<=0))
print(f"  DESI best-fit crossing z = {cross_z(DESI_W0,DESI_WA):.3f}")
print(f"  DESI posterior crossing z: median={np.median(zc_phys):.3f}  "
      f"16-84%=[{np.percentile(zc_phys,16):.3f}, {np.percentile(zc_phys,84):.3f}]  "
      f"5-95%=[{np.percentile(zc_phys,5):.3f}, {np.percentile(zc_phys,95):.3f}]")
print(f"  (fraction of DESI posterior with NO real crossing / a_c<=0: {frac_nocross:.2f})")

# framework projected crossings
print("\n  Framework CPL-projected crossing z (per-box, dist_BAO+CMB & rho methods):")
for m in ["dist_BAO+CMB","rho_DEweighted"]:
    s = res["per_box_summary"][m]
    vals = [v for v in s["cross_z_per_box"] if v is not None]
    print(f"    {m:16s}: per-box {s['cross_z_per_box']}  "
          f"mean={np.mean(vals):.3f} pooled={res['pooled'][m]['cross_z']:.3f}")
print(f"\n  Framework PHYSICAL crossing: per-box {res['phys_crossing_summary']['per_box']}"
      f"  mean={res['phys_crossing_summary']['mean']:.3f} "
      f"pooled={res['phys_crossing_summary']['pooled']:.3f}")

# does framework projected crossing sit inside DESI's crossing posterior?
lo,hi = np.percentile(zc_phys,5), np.percentile(zc_phys,95)
print(f"\n  DESI crossing 90% interval: [{lo:.2f}, {hi:.2f}]")
for m in ["dist_BAO+CMB","rho_DEweighted","w_DE"]:
    p = res['pooled'][m]['cross_z']
    inside = lo <= p <= hi
    print(f"    framework pooled {m:16s} crossing z={p:.3f}  inside 90%: {inside}")
