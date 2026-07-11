#!/usr/bin/env python3
"""
Phase-diagram figures for the forced-partition sweep. One figure per allocation
rule (per-unit accounting): rows = alpha forms, cols = dimension vectors; each
panel shows steady-state ρ_k vs budget b (one line per sector), the corridor band
(0.10, 0.43) shaded, and the two poles. A companion partition figure per rule
shows the S-partition fraction per sector vs budget with the dimension fractions
as dashed references.
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "results.json")) as f:
    data = json.load(f)
meta = data["meta"]
recs = data["records"]

DIMS = list(meta["dim_vectors"].keys())
ALPHAS = meta["alpha_forms"]
RULES = meta["alloc_rules"]
LO, HI = meta["corridor"]


def sel(rule, acc, dim, form):
    rs = [r for r in recs if r["rule"] == rule and r["accounting"] == acc
          and r["dim_name"] == dim and r["alpha"] == form]
    return sorted(rs, key=lambda r: r["budget_b"])


def phase_fig(rule, acc):
    fig, axes = plt.subplots(len(ALPHAS), len(DIMS), figsize=(4.2 * len(DIMS), 3.2 * len(ALPHAS)),
                             squeeze=False)
    for i, form in enumerate(ALPHAS):
        for j, dim in enumerate(DIMS):
            ax = axes[i][j]
            rs = sel(rule, acc, dim, form)
            if not rs:
                continue
            b = np.array([r["budget_b"] for r in rs])
            rho = np.array([r["rho_star"] for r in rs])  # (nb, nsec)
            dims = rs[0]["dims"]
            n = len(dims)
            cmap = plt.cm.viridis(np.linspace(0, 0.9, n))
            for k in range(n):
                ax.plot(b, rho[:, k], "-o", ms=2.5, color=cmap[k],
                        label=f"d={int(dims[k])}")
            ax.axhspan(LO, HI, color="green", alpha=0.10)
            ax.axhline(1.0, color="red", lw=0.7, ls="--")
            ax.axhline(0.0, color="blue", lw=0.7, ls="--")
            ax.set_ylim(-0.05, 1.05)
            ax.set_title(f"{form} | {dim}", fontsize=8)
            if i == len(ALPHAS) - 1:
                ax.set_xlabel("budget b")
            if j == 0:
                ax.set_ylabel(r"$\rho_k^\ast$")
            # dedupe legend entries
            h, l = ax.get_legend_handles_labels()
            uniq = dict(zip(l, h))
            ax.legend(uniq.values(), uniq.keys(), fontsize=6, loc="upper right")
    fig.suptitle(f"Steady-state rho per sector — rule {rule} ({acc})", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = os.path.join(HERE, f"phase_rho_{rule}_{acc}.png")
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def partition_fig(rule, acc):
    fig, axes = plt.subplots(len(ALPHAS), len(DIMS), figsize=(4.2 * len(DIMS), 3.2 * len(ALPHAS)),
                             squeeze=False)
    for i, form in enumerate(ALPHAS):
        for j, dim in enumerate(DIMS):
            ax = axes[i][j]
            rs = sel(rule, acc, dim, form)
            if not rs:
                continue
            b = np.array([r["budget_b"] for r in rs])
            pf = np.array([r["partition_frac"] for r in rs])  # (nb, nsec)
            dims = rs[0]["dims"]
            dimfrac = np.array(dims) / np.sum(dims)
            n = len(dims)
            cmap = plt.cm.plasma(np.linspace(0, 0.9, n))
            for k in range(n):
                ax.plot(b, pf[:, k], "-", color=cmap[k], label=f"d={int(dims[k])}")
                ax.axhline(dimfrac[k], color=cmap[k], lw=0.8, ls=":")
            ax.set_ylim(0, 1)
            ax.set_title(f"{form} | {dim}", fontsize=8)
            if i == len(ALPHAS) - 1:
                ax.set_xlabel("budget b")
            if j == 0:
                ax.set_ylabel(r"$S_k/S_{tot}$")
            h, l = ax.get_legend_handles_labels()
            uniq = dict(zip(l, h))
            ax.legend(uniq.values(), uniq.keys(), fontsize=6, loc="upper right")
    fig.suptitle(f"S-partition fraction vs dimension fraction (dotted) — rule {rule} ({acc})",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = os.path.join(HERE, f"partition_{rule}_{acc}.png")
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def main():
    outs = []
    for rule in RULES:
        outs.append(phase_fig(rule, "per_unit"))
        outs.append(partition_fig(rule, "per_unit"))
    for o in outs:
        print("wrote", o)


if __name__ == "__main__":
    main()
