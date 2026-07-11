#!/usr/bin/env python3
"""Print the load-bearing numbers from results.json for SUMMARY.md.
DISCOVERY MODE: reports the full result-space; no winner-picking."""
import json
import os
import numpy as np
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
recs = R["records"]
print(f"# {len(recs)} cells\n")

# ---- validation ----
vals = [r["validation"] for r in recs if r["validation"]]
if vals:
    mk = max(v["keff_absdiff"] for v in vals)
    ml = max(v["neglogdet_absdiff"] for v in vals)
    mc = min(v["min_eig_C"] for v in vals)
    print(f"## Closed-form validation ({len(vals)} cells, D<=60)")
    print(f"max |keff_closed-numpy|      = {mk:.2e}")
    print(f"max |neglogdet_closed-numpy| = {ml:.2e}")
    print(f"min eig(C) over validated    = {mc:.4f}\n")

# ---- global classification counts ----
print("## Classification counts (all cells)")
for k, v in Counter(r["classification"] for r in recs).most_common():
    print(f"  {k:20s} {v}")
print()

# ---- PSD-boundary encounters ----
psd = [r for r in recs if r["which_pole"] == "psd_boundary"]
print(f"## PSD-boundary encounters: {len(psd)} cells")
byrule = Counter((r["rule"], r["alpha"]) for r in psd)
for k, v in byrule.most_common():
    print(f"  {k}: {v}")
if psd:
    ex = psd[0]
    print(f"  example: {ex['dim_name']} {ex['alpha']} {ex['rule']}/{ex['split']} "
          f"{ex['accounting']} b={ex['budget_b']} rho_g={ex['rho_g']:.3f} "
          f"min_eig_G={ex['min_eig_G']:.2e}")
print()

# ---- k_eff vs D (pair25 series), per (rule,split,acc,alpha,budget) ----
print("## k_eff vs D  (pair25 series: D = 7,14,28,56,112,224)")
Dgrid = [7, 14, 28, 56, 112, 224]
def series(rule, split, acc, alpha, b):
    out = {}
    for r in recs:
        if (r["dim_name"].startswith("pair25") and r["rule"] == rule
                and r["split"] == split and r["accounting"] == acc
                and r["alpha"] == alpha and abs(r["budget_b"] - b) < 1e-6):
            out[int(r["D"])] = r
    return out

for alpha in ("lin",):
    for acc in ("per_pair", "per_channel"):
        for rule, split in (("A_equal", "na"), ("B_stock", "s1"), ("B_stock", "s2"),
                            ("C_rate", "s1"), ("C_rate", "s2"), ("D_need", "na")):
            for b in (0.35, 0.75, 1.15):
                s = series(rule, split, acc, alpha, b)
                if len(s) < 4:
                    continue
                row = []
                for D in Dgrid:
                    if D in s and s[D]["which_pole"] is None:
                        row.append(f"{s[D]['keff']:6.2f}")
                    elif D in s:
                        row.append(f"{s[D]['which_pole'][:4]:>6s}")
                    else:
                        row.append("   -  ")
                # fit exponent on interior cells
                Ds = [D for D in Dgrid if D in s and s[D]["which_pole"] is None]
                ks = [s[D]["keff"] for D in Ds]
                slope = np.nan
                if len(Ds) >= 3 and min(ks) > 0:
                    slope = np.polyfit(np.log(Ds), np.log(ks), 1)[0]
                print(f"  {acc:11s} {rule:8s}/{split} b={b:.2f} | "
                      + " ".join(row) + f" | dln keff/dln D = {slope:+.2f}")
    print()

# ---- rho_g vs rho_sector competition (pair25_x8, lin, per_pair) ----
print("## rho_g vs sector-rho competition (pair25_x8 D=56, lin, per_pair)")
for rule, split in (("A_equal", "na"), ("B_stock", "s1"), ("B_stock", "s2"),
                    ("C_rate", "s1"), ("C_rate", "s2"), ("D_need", "na")):
    print(f"  {rule}/{split}:")
    for r in recs:
        if (r["dim_name"] == "pair25_x8" and r["rule"] == rule and r["split"] == split
                and r["accounting"] == "per_pair" and r["alpha"] == "lin"
                and r["budget_b"] in (0.35, 0.65, 0.95, 1.25)):
            rs = np.array(r["rho_sectors"])
            # d=2 sectors even idx, d=5 odd idx
            d = np.array(r["dims"])
            r2 = rs[d == 2].mean() if (d == 2).any() else np.nan
            r5 = rs[d == 5].mean() if (d == 5).any() else np.nan
            print(f"    b={r['budget_b']:.2f} rho_g={r['rho_g']:.3f} "
                  f"rho(d=2)={r2:.3f} rho(d=5)={r5:.3f} "
                  f"class={r['classification']:16s} jac={r['jac_max_real_eig']:+.3f} "
                  f"pole={r['which_pole']}")
print()

# ---- stability classes ----
print("## Stability (jac max real eig) — interior cells only")
inter = [r for r in recs if r["which_pole"] is None]
byrule = defaultdict(list)
for r in inter:
    byrule[(r["rule"], r["split"])].append(r["jac_max_real_eig"])
for k in sorted(byrule):
    a = np.array(byrule[k])
    marg = int(np.sum(np.abs(a) < 1e-6))
    print(f"  {k[0]:8s}/{k[1]:2s}: n={len(a):4d} "
          f"max_re in [{a.min():+.3f},{a.max():+.3f}] median={np.median(a):+.3f} "
          f"marginal(|.|<1e-6)={marg}")
