#!/usr/bin/env python3
"""Figures for the quantum-corridor calibration (SPEC.md §4.4). Imported by calibrate.py."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# canonical band edges from the calibration branches (SPEC §4.4 / §5)
CRIT_LO, CRIT_HI = 0.30, 0.80


def build(out, here):
    _beta_separation(out["grid"], here)
    _ramp_overlay(out["ramp"], here)


def _beta_separation(grid, here):
    """beta with bootstrap CI for every class, one panel per (N,S) cell."""
    cells = []
    for r in grid:
        key = (r["cell"], r["N"], r["S"])
        if key not in cells:
            cells.append(key)
    fig, axes = plt.subplots(1, len(cells), figsize=(4.2 * len(cells), 4.6), sharey=True)
    if len(cells) == 1:
        axes = [axes]
    for ax, key in zip(axes, cells):
        rows = [r for r in grid if (r["cell"], r["N"], r["S"]) == key]
        names = [r["name"] for r in rows]
        y = np.arange(len(rows))
        betas = np.array([r["beta"] for r in rows])
        lo = np.array([r["beta_lo"] for r in rows])
        hi = np.array([r["beta_hi"] for r in rows])
        ax.axvspan(CRIT_LO, CRIT_HI, color="tab:orange", alpha=0.12, label="criticality band")
        ax.axvline(0.0, color="tab:blue", ls=":", lw=1)
        ax.axvline(1.0, color="tab:red", ls=":", lw=1)
        colors = ["tab:green" if r["verdict"] in ("CORRIDOR", "RIGIDITY")
                  else "tab:orange" if r["verdict"] == "CRITICAL"
                  else "tab:blue" for r in rows]
        # point beta uses full ndraw; bootstrap CI uses reduced ndraw, so the CI can
        # sit marginally off the point -> clip the whisker lengths to non-negative.
        xerr = np.vstack([np.clip(betas - lo, 0, None), np.clip(hi - betas, 0, None)])
        ax.errorbar(betas, y, xerr=xerr, fmt="o",
                    ecolor="0.5", elinewidth=1.4, capsize=3,
                    mfc="none", mec="0.3", zorder=3)
        ax.scatter(betas, y, c=colors, s=60, zorder=4)
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=8)
        ax.set_xlim(-0.25, 1.25)
        ax.set_xlabel(r"$\beta$ (subsample PR exponent)")
        ax.set_title(f"{key[0]}  N={key[1]}  S={key[2]:,}", fontsize=9)
        ax.grid(axis="x", alpha=0.25)
    axes[0].set_ylabel("state class")
    fig.suptitle("N5 calibration: does $\\beta$ separate the state classes at each (N,S)?",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = os.path.join(here, "beta_separation.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)


def _ramp_overlay(ramp, here):
    """C3: measured S vs the parameter-free -(k-1)ln(1-rho) curve along the ramp."""
    r = [x for x in ramp if np.isfinite(x["S_measured"])]
    rho = np.array([x["rho_bar"] for x in r])
    Sm = np.array([x["S_measured"] for x in r])
    Sc = np.array([x["S_c3"] for x in r])
    dev = np.array([x["deviation"] for x in r])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.5))
    order = np.argsort(rho)
    ax1.plot(rho[order], Sc[order], "-", color="tab:blue",
             label=r"parameter-free  $-(k-1)\ln(1-\bar\rho)$")
    ax1.plot(rho[order], Sm[order], "o", color="tab:red",
             label=r"measured  $S(k,\bar\rho)$")
    ax1.set_xlabel(r"$\bar\rho$  (mean off-diagonal correlation)")
    ax1.set_ylabel("potential  S")
    ax1.set_title("C3: S tracks the parameter-free rigidity-pole curve")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.25)
    ax2.plot(rho[order], dev[order], "o-", color="tab:purple")
    ax2.axhline(0, color="0.5", lw=1)
    ax2.set_xlabel(r"$\bar\rho$")
    ax2.set_ylabel(r"deviation  $S_{meas}-S_{C3}\;=\;-\ln(1+\bar\rho(k-1))$")
    ax2.set_title("C3 deviation band (bounded first term)")
    ax2.grid(alpha=0.25)
    fig.suptitle("Depolarized-GHZ maintenance ramp (C2/C3 surrogate)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p = os.path.join(here, "c3_ramp_overlay.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
