#!/usr/bin/env python3
"""
Corridor-ceiling Part B: measured irreversibility (detailed-balance |z|) vs corridor
position (k_eff), assembled from the keff_saturation catalog. The ceiling mechanism
predicts an OCCUPANCY EDGE: no coordinating substrate with high sigma near the rigidity
pole (k_eff -> 1, rho -> 1). n is small; real found systems only (the phase-randomized
"dead" cell is a CONSTRUCTED reversible control — plotted separately, not evidence).

All numbers traced to source JSONs in ../keff_saturation/. NO synthetic data.
Seed 20260710.
"""
import json, os
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results.json")

# corridor position: k_eff = eff_rank_surr (saturating coordinating rank).
# rho_proxy = 1/k_eff is the global-mode reading (higher = closer to rigidity pole).
# irreversibility: circulation |z| (the trustworthy estimator; winding where noted).
# Each row: (name, k_eff, |z|, class, found?, source)
CATALOG = [
    # --- real FOUND systems (both axes measured) ---
    ("motor cortex (MC_Maze spikes)", 6.7, 12.5, "coordinating", True,
     "axis_independence head_to_head motor_MCmaze: eff_rank_surr 6-7, circ|z| 12.0-12.7"),
    ("visual cortex (Allen nat-movie)", 6.0, 5.0, "coordinating", True,
     "axis_independence turbulent/head_to_head: eff_rank_surr 5-8, circ|z| 4.0-7.0"),
    ("C. elegans (whole-brain calcium)", 9.0, 2.75, "coordinating(weak est.)", True,
     "rho_g_readout: k_eff~9; slow-calcium DB |z|~2.75 (winding, weak estimator)"),
    ("galaxy baryon cycle (TNG)", 2.5, 0.34, "bound", True,
     "galaxy detailed_balance: eff_rank_surr 2-3; circ|z| jz .03 / vr .34 / zheight .62"),
    # --- CONSTRUCTED control (reversible by construction) — NOT evidence for the edge ---
    ("phase-randomized dead cell", 1.0, 1.6, "constructed-reversible", False,
     "axis_independence dead_constructed: eff_rank_surr 1, circ|z| 1.6 (CONSTRUCTED)"),
]

rows = [dict(name=n, k_eff=k, abs_z=z, cls=c, found=f, rho_proxy=1.0/k, source=s)
        for (n, k, z, c, f, s) in CATALOG]

found = [r for r in rows if r["found"]]
kf = np.array([r["k_eff"] for r in found])
zf = np.array([r["abs_z"] for r in found])
# Spearman: the collapse/edge prediction => POSITIVE (lower k_eff => lower achievable sigma).
rho_s, p_s = stats.spearmanr(kf, zf)

partB = {
    "corridor_position": "k_eff = eff_rank_surr (saturating coordinating rank); rho_proxy=1/k_eff",
    "irreversibility": "circulation |z| (phase-randomized null); winding where noted",
    "catalog": rows,
    "n_found": len(found),
    "spearman_keff_vs_absz_found": {"rho": float(rho_s), "p": float(p_s),
        "note": "n=4 found systems; collapse/edge predicts POSITIVE (low k_eff -> low sigma)"},
    "occupancy_edge_read": (
        "No FOUND coordinating substrate sits near the pole: all coordinating systems have "
        "k_eff 6-9 (rho_proxy 0.11-0.17, INSIDE the corridor, nowhere near rho->1). The only "
        "near-pole point (k_eff=1) is the phase-randomized dead cell, reversible BY "
        "CONSTRUCTION, so it cannot test the mechanism. Within the populated band, k_eff and "
        "|z| are ~independent (program's own axis-independence result): the lowest-k_eff FOUND "
        "system (galaxy, k_eff~2.5) is BOUND, but for an independent reason (cosmic-assembly "
        "transient, no sustained drive), while motor cortex (k_eff~7) breaks DB hardest. The "
        "scatter neither confirms nor kills the ceiling: the pole region is simply unoccupied."),
}

# ---- plot ----
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    cmap = {"coordinating": "#1f77b4", "coordinating(weak est.)": "#6baed6",
            "bound": "#7f7f7f", "constructed-reversible": "#d62728"}
    for r in rows:
        mk = "x" if not r["found"] else "o"
        ax.scatter(r["k_eff"], r["abs_z"], s=140, marker=mk,
                   c=cmap.get(r["cls"], "#333"), edgecolor="k", zorder=3,
                   label=None)
        ax.annotate(r["name"], (r["k_eff"], r["abs_z"]),
                    textcoords="offset points", xytext=(8, 4), fontsize=7.5)
    ax.axhline(1.5, ls=":", c="gray", lw=1)
    ax.text(1.02, 1.55, "DB null ceiling |z|~1.5", fontsize=7, c="gray")
    ax.axvspan(1.0, 1.6, color="red", alpha=0.06)
    ax.text(1.02, 11, "rigidity pole\n(k_eff->1)", fontsize=7.5, c="red")
    ax.set_xscale("log")
    ax.set_xlabel("corridor position  k_eff = eff_rank_surr  (log; left = toward rigidity pole)")
    ax.set_ylabel("measured irreversibility  |z|  (broken detailed balance)")
    ax.set_title("Part B: irreversibility vs corridor position\n"
                 f"n={len(found)} found systems; Spearman(k_eff,|z|)={rho_s:+.2f} (p={p_s:.2f}, n.s.)"
                 "  — 'x' = constructed control", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "catalog_scatter.png"), dpi=130)
    partB["figure"] = "catalog_scatter.png"
    print("wrote catalog_scatter.png")
except Exception as e:
    partB["figure_error"] = str(e)
    print("plot skipped:", e)

res = json.load(open(OUT)) if os.path.exists(OUT) else {}
res["partB"] = partB
with open(OUT, "w") as f:
    json.dump(res, f, indent=2)
print(f"Spearman(k_eff,|z|) over {len(found)} found systems: rho={rho_s:+.3f} p={p_s:.3f}")
print("wrote partB to", OUT)
