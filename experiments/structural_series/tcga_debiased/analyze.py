#!/usr/bin/env python3
"""Summarize the debiased TCGA run vs the raw run."""
import json
import pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
deb = json.loads((HERE / "results_debiased.json").read_text())
raw = json.loads((HERE.parent / "data_tcga" / "results"
                  / "rho_by_cancer_pathway.json").read_text())

PRIMARY = [c for c, v in deb.items() if not v["insufficient"]]

print("=" * 76)
print("DEBIASED TCGA — per-cancer healthy-tissue rho (vs raw)")
print("=" * 76)
print(f"{'cancer':6} {'n_n':>4} {'raw rho_n':>10} {'floor_n':>9} "
      f"{'DEB rho_n':>10} {'IQR_deb':>8} {'p10':>6} {'p90':>6} {'k_eff_n':>8}")
all_deb_n_primary = []
for c, v in deb.items():
    paths = v["pathways"]
    rn_raw = np.array([p["normal"]["rho_raw"] for p in paths.values()])
    fl_n = np.array([p["normal"]["floor"] for p in paths.values()])
    rn_deb = np.array([p["normal"]["rho_deb"] for p in paths.values()])
    keff_n = np.array([p["normal"]["k_eff_pr"] for p in paths.values()])
    iqr = np.percentile(rn_deb, 75) - np.percentile(rn_deb, 25)
    flag = "" if not v["insufficient"] else "  [insuff n]"
    print(f"{c:6} {v['n_normal']:>4} {np.median(rn_raw):>10.4f} "
          f"{np.median(fl_n):>9.4f} {np.median(rn_deb):>10.4f} "
          f"{iqr:>8.4f} {np.percentile(rn_deb,10):>6.3f} "
          f"{np.percentile(rn_deb,90):>6.3f} {np.median(keff_n):>8.1f}{flag}")
    if not v["insufficient"]:
        all_deb_n_primary.extend(rn_deb.tolist())

all_deb_n_primary = np.array(all_deb_n_primary)
print("-" * 76)
print(f"POOLED healthy debiased rho over {len(PRIMARY)} primary cancers "
      f"({len(all_deb_n_primary)} pathway-values):")
print(f"  median {np.median(all_deb_n_primary):.4f}  "
      f"IQR [{np.percentile(all_deb_n_primary,25):.4f}, "
      f"{np.percentile(all_deb_n_primary,75):.4f}]  "
      f"range [{all_deb_n_primary.min():.4f}, {all_deb_n_primary.max():.4f}]")
bio_lo, bio_hi = 0.27, 0.33
in_cluster = bio_lo <= np.median(all_deb_n_primary) <= bio_hi
print(f"  biological cluster ~[{bio_lo}, {bio_hi}]: "
      f"{'JOINS' if in_cluster else 'OUTSIDE'}")

print()
print("=" * 76)
print("DEBIASED TCGA — tumour drift (debiased rho_t vs rho_n)")
print("=" * 76)
print(f"{'cancer':6} {'npath':>6} {'chaos-ward':>11} {'rigid-ward':>11} "
      f"{'flat(=0)':>9} {'med dDEB':>9} {'med dRAW':>9}")
tot_chaos = tot_rigid = tot_flat = 0
tot_chaos_p = tot_rigid_p = tot_flat_p = 0
for c, v in deb.items():
    paths = v["pathways"]
    dd = np.array([p["delta_deb"] for p in paths.values()])
    dr = np.array([p["delta_raw"] for p in paths.values()])
    # tumour drift direction on the DEBIASED delta
    chaos = int(np.sum(dd < 0))      # tumour rho LOWER -> chaos-ward
    rigid = int(np.sum(dd > 0))      # tumour rho HIGHER -> rigidity-ward
    flat = int(np.sum(dd == 0))      # both floored to 0 -> no debiased signal
    tot_chaos += chaos; tot_rigid += rigid; tot_flat += flat
    if not v["insufficient"]:
        tot_chaos_p += chaos; tot_rigid_p += rigid; tot_flat_p += flat
    print(f"{c:6} {len(paths):>6} {chaos:>11} {rigid:>11} {flat:>9} "
          f"{np.median(dd):>9.4f} {np.median(dr):>9.4f}")
print("-" * 76)
n_all = tot_chaos + tot_rigid + tot_flat
print(f"ALL 7 cancers: {tot_chaos}/{n_all} chaos-ward, "
      f"{tot_rigid}/{n_all} rigidity-ward, {tot_flat}/{n_all} flat")
n_p = tot_chaos_p + tot_rigid_p + tot_flat_p
print(f"6 primary    : {tot_chaos_p}/{n_p} chaos-ward, "
      f"{tot_rigid_p}/{n_p} rigidity-ward, {tot_flat_p}/{n_p} flat")

# raw-run drift: non-overlapping 95% CI significant pathways, all chaos-ward
print()
print("RAW run reference (from data_tcga/RESULT.md): 201/201 significant "
      "(non-overlap 95% CI)\n  pathway-shifts chaos-ward, 0 rigidity-ward.")

# debiased significance via permutation surrogate: a pathway's debiased shift
# is "real" if BOTH groups have rho_deb > 0 (signal survived the floor) and
# sign of delta_deb is consistent with sign of delta_raw
print()
print("Sign-consistency of debiased vs raw delta:")
for c, v in deb.items():
    paths = v["pathways"]
    dd = np.array([p["delta_deb"] for p in paths.values()])
    dr = np.array([p["delta_raw"] for p in paths.values()])
    # only count pathways where debiased delta is non-zero
    nz = dd != 0
    same = int(np.sum(np.sign(dd[nz]) == np.sign(dr[nz])))
    print(f"  {c:6}: {same}/{int(nz.sum())} non-flat debiased deltas keep "
          f"the raw sign  (raw all-negative)")
