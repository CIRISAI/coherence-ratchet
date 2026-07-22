#!/usr/bin/env python3
import json, os
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
S=json.load(open(os.path.join(HERE,"tracer_results.json")))["snapshots"]

def col(key, field="real", R="8.0"):
    return np.array([s["configs"][key][R][field] for s in S if key in s["configs"]])
def kcol(key):
    return np.array([s["configs"][key]["k"] for s in S if key in s["configs"]])

print("="*78); print("K4 BIAS / TRACER LEG  (copula skew R8, across 26 snaps)"); print("="*78)
print("\nA nonlinear-bias artifact should GROW with bias (mass threshold);")
print("genuine matter-field coordination should be stable across cut and tracer.\n")

cfgs = [
 ("grp_mass_m1e11","groups mass-wt   m200>=1e11"),
 ("grp_mass_m1e12","groups mass-wt   m200>=1e12"),
 ("grp_mass_m5e12","groups mass-wt   m200>=5e12"),
 ("grp_count_m1e11","groups count-wt m200>=1e11"),
 ("grp_count_m1e12","groups count-wt m200>=1e12"),
 ("grp_count_m5e12","groups count-wt m200>=5e12"),
 ("gal_count_msall","galaxies count  mstar>0"),
 ("gal_count_ms1e9","galaxies count  mstar>=1e9"),
 ("gal_count_ms1e10","galaxies count mstar>=1e10"),
 ("gal_mstar_msall","galaxies mstar-wt mstar>0"),
]
print(f"{'config':32s} {'<skew>':>8s} {'std':>7s} {'<z_vsS0>':>9s} {'<k>':>8s}")
for key,lab in cfgs:
    r=col(key); z=col(key,"z"); k=kcol(key)
    if len(r)==0:
        print(f"{lab:32s}  (missing)"); continue
    print(f"{lab:32s} {np.mean(r):+8.3f} {np.std(r):7.3f} {np.mean(z):+9.1f} {np.mean(k):8.0f}")

print("\nKEY TRENDS:")
gm=[np.mean(col(f"grp_mass_m{t}")) for t in ("1e11","1e12","5e12")]
gc=[np.mean(col(f"grp_count_m{t}")) for t in ("1e11","1e12","5e12")]
print(f"  groups mass-wt  |skew| vs threshold 1e11->1e12->5e12: {gm[0]:+.3f} {gm[1]:+.3f} {gm[2]:+.3f}"
      f"  ({'FALLS' if abs(gm[2])<abs(gm[0]) else 'RISES'} with bias)")
print(f"  groups count-wt |skew| vs threshold 1e11->1e12->5e12: {gc[0]:+.3f} {gc[1]:+.3f} {gc[2]:+.3f}")
gms=col("gal_mstar_msall")
print(f"  galaxies mstar-wt skew: mean {np.mean(gms):+.3f}  std {np.std(gms):.3f}  "
      f"range [{np.min(gms):+.3f},{np.max(gms):+.3f}]  (instability = sampling-dominated)")
print(f"  count-wt >> mass-wt: groups count {np.mean(col('grp_count_m1e11')):+.3f} vs "
      f"mass {np.mean(col('grp_mass_m1e11')):+.3f}  (weighting-dependent => not a field invariant)")
print("="*78)
