#!/usr/bin/env python3
"""Figures for the coupled cross-sector model. DISCOVERY MODE: plots the full
result-space, no winner-picking."""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
recs = R["records"]
BUD = R["meta"]["budget_levels"]
RHO_LO, RHO_HI = R["meta"]["corridor"]


def sel(**kw):
    out = []
    for r in recs:
        if all(r.get(k) == v for k, v in kw.items()):
            out.append(r)
    return out


RULES = [("A_equal", "na"), ("B_stock", "s1"), ("B_stock", "s2"),
         ("C_rate", "s1"), ("C_rate", "s2"), ("D_need", "na")]
Dgrid = [7, 14, 28, 56, 112, 224]

# ---- FIG 1: k_eff vs D per rule, curves by budget ----
fig, axes = plt.subplots(2, 3, figsize=(15, 9), sharex=True)
budsel = [0.15, 0.35, 0.55, 0.75, 0.95, 1.15, 1.35]
cmap = plt.cm.viridis(np.linspace(0, 1, len(budsel)))
for ax, (rule, split) in zip(axes.flat, RULES):
    for b, col in zip(budsel, cmap):
        xs, ys = [], []
        for D in Dgrid:
            rr = [r for r in sel(rule=rule, split=split, accounting="per_pair",
                                 alpha="lin", budget_b=b)
                  if int(r["D"]) == D and r["dim_name"].startswith("pair25")
                  and r["which_pole"] is None]
            if rr:
                xs.append(D); ys.append(rr[0]["keff"])
        if len(xs) >= 2:
            ax.plot(xs, ys, "o-", color=col, ms=4, label=f"b={b:.2f}")
    # extensive reference (independent-block parent: k_eff ~ 0.61 D)
    ax.plot(Dgrid, 0.61 * np.array(Dgrid), "k--", lw=1, alpha=0.5,
            label="0.61·D (indep. blocks)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_title(f"{rule}/{split}  (lin, per_pair)")
    ax.set_xlabel("D"); ax.set_ylabel("k_eff (participation ratio)")
    ax.grid(alpha=0.3)
axes.flat[0].legend(fontsize=7, ncol=2)
fig.suptitle("k_eff vs D — does coupling SATURATE the participation ratio?", fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1_keff_vs_D.png"), dpi=110)
plt.close(fig)

# ---- FIG 2: rho_g vs sector-rho competition (pair25_x8, lin, per_pair) ----
fig, axes = plt.subplots(2, 3, figsize=(15, 9), sharex=True, sharey=True)
for ax, (rule, split) in zip(axes.flat, RULES):
    rr = sorted([r for r in sel(rule=rule, split=split, accounting="per_pair",
                                alpha="lin", dim_name="pair25_x8")],
                key=lambda r: r["budget_b"])
    b = [r["budget_b"] for r in rr]
    rg = [r["rho_g"] for r in rr]
    d = np.array(rr[0]["dims"]) if rr else np.array([])
    r2 = [np.array(r["rho_sectors"])[d == 2].mean() for r in rr]
    r5 = [np.array(r["rho_sectors"])[d == 5].mean() for r in rr]
    ax.plot(b, rg, "s-", color="crimson", label="rho_g (global)")
    ax.plot(b, r2, "o-", color="steelblue", label="rho (d=2 sectors)")
    ax.plot(b, r5, "^-", color="seagreen", label="rho (d=5 sectors)")
    ax.axhspan(RHO_LO, RHO_HI, color="gold", alpha=0.15)
    # mark PSD-boundary cells
    for r in rr:
        if r["which_pole"] == "psd_boundary":
            ax.axvline(r["budget_b"], color="purple", ls=":", alpha=0.5)
    ax.set_title(f"{rule}/{split}")
    ax.set_xlabel("budget b"); ax.set_ylabel("rho*")
    ax.grid(alpha=0.3)
axes.flat[0].legend(fontsize=8)
fig.suptitle("Global vs sector channel — budget competition (pair25_x8, D=56, lin, per_pair)\n"
             "gold band = corridor; purple dotted = PSD boundary hit", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2_rho_competition.png"), dpi=110)
plt.close(fig)

# ---- FIG 3: phase map (budget x D), classification, per rule ----
CLS_COL = {"symmetric": 0, "broken": 1, "runaway_rigidity": 2,
           "collapse_chaos": 3, "psd_boundary": 4}
from matplotlib.colors import ListedColormap
cmap3 = ListedColormap(["#4575b4", "#91bfdb", "#d73027", "#fee090", "#762a83"])
fig, axes = plt.subplots(2, 3, figsize=(15, 9), sharex=True, sharey=True)
for ax, (rule, split) in zip(axes.flat, RULES):
    M = np.full((len(Dgrid), len(BUD)), np.nan)
    for i, D in enumerate(Dgrid):
        for j, b in enumerate(BUD):
            rr = [r for r in sel(rule=rule, split=split, accounting="per_pair",
                                 alpha="lin", budget_b=b)
                  if int(r["D"]) == D and r["dim_name"].startswith("pair25")]
            if rr:
                M[i, j] = CLS_COL[rr[0]["classification"]]
    ax.imshow(M, aspect="auto", origin="lower", cmap=cmap3, vmin=0, vmax=4,
              extent=[BUD[0], BUD[-1], -0.5, len(Dgrid) - 0.5])
    ax.set_yticks(range(len(Dgrid))); ax.set_yticklabels(Dgrid)
    ax.set_title(f"{rule}/{split}")
    ax.set_xlabel("budget b"); ax.set_ylabel("D")
fig.suptitle("Phase map (lin, per_pair): blue=symmetric cyan=broken red=rigidity "
             "yellow=chaos purple=PSD-boundary", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3_phase_map.png"), dpi=110)
plt.close(fig)

print("wrote fig1_keff_vs_D.png fig2_rho_competition.png fig3_phase_map.png")
