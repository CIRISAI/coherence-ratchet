#!/usr/bin/env python3
"""Figures for the rent-tracks-stock neural replication. Reads results.json +
raw_window_metrics.json written by rent_stock.py.  No recomputation of estimators."""
import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from rent_stock import S_closed, rho_kish, _rank, _resid, PROXIES

RES = json.load(open(os.path.join(HERE, "results.json")))
RAW = json.load(open(os.path.join(HERE, "raw_window_metrics.json")))
SESS = ["chibi/propofol", "chibi/ketamine", "george/propofol", "george/ketamine"]
COL = {"propofol": "#C4462F", "ketamine": "#2F6FC4"}
EPC = {"awake": "#FFFFFF", "induction": "#F2E9D8", "deep": "#DFE3E8"}

def load_windows(nm):
    animal, agent = nm.split("/")
    tag = "" if animal == "chibi" else "_george"
    p = os.path.join(PARENT, f"trajectory_windows_{agent}{tag}.jsonl")
    rows = [json.loads(l) for l in open(p)]
    raw = RAW[nm]
    d = dict(t=np.array([r["t_center"] for r in rows]),
             epoch=[r["epoch"] for r in rows],
             k_eff=np.array([r["k_eff"] for r in rows]),
             z_circ=np.abs([r["db_z_circ_sum"] for r in rows]),
             z_wind=np.abs([r["db_z_winding"] for r in rows]),
             mag_circ=np.array([r["mag_circ_rad_per_s"] for r in raw]),
             mag_wind=np.array([r["mag_wind_rad_per_s"] for r in raw]),
             epr=np.array([r["epr_nats_per_s"] for r in raw]),
             S_direct=np.array([r["S_direct"] for r in raw]))
    d["S_closed"] = S_closed(rho_kish(d["k_eff"]))
    return d

def shade(ax, t, epoch):
    e = np.array(epoch)
    for lab in ["induction", "deep"]:
        m = e == lab
        if m.any():
            ax.axvspan(t[m].min(), t[m].max(), color=EPC[lab], zorder=0, lw=0)

# ---------------------------------------------------------------- Fig 1
def fig_trajectories():
    fig, axes = plt.subplots(4, 4, figsize=(17, 11), sharex="row")
    for i, nm in enumerate(SESS):
        d = load_windows(nm); agent = nm.split("/")[1]; t = d["t"]
        panels = [("S_direct", "STOCK  S = −ln det C", "#111111"),
                  ("z_circ", "|z| circulation (significance)", COL[agent]),
                  ("mag_circ", "Σ|ω| circulation  [rad/s]  (RATE)", COL[agent]),
                  ("epr", "plug-in EPR, debiased  [nats/s]  (RATE)", COL[agent])]
        for j, (key, lab, c) in enumerate(panels):
            ax = axes[i, j]; shade(ax, t, d["epoch"])
            ax.plot(t, d[key], lw=0.8, color=c)
            k = 9
            sm = np.convolve(d[key], np.ones(k) / k, mode="same")
            ax.plot(t[k:-k], sm[k:-k], lw=2.0, color="k", alpha=0.55)
            if key == "z_circ": ax.axhline(1.5, ls=":", c="0.35", lw=1)
            if key == "epr": ax.axhline(0.0, ls=":", c="0.35", lw=1)
            if j == 0:
                ax.set_ylabel(nm.replace("/", "\n"), fontsize=10, fontweight="bold")
            if i == 0: ax.set_title(lab, fontsize=9.5)
            if i == 3: ax.set_xlabel("t (s)")
            ax.tick_params(labelsize=8)
    fig.suptitle("Stock (S) and maintenance proxies through anesthetic induction — within-session only\n"
                 "shaded: induction (tan), deep (grey).  Absolute levels are field-confounded and are NOT compared across rows.",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(HERE, "fig1_trajectories.png"), dpi=140)
    plt.close(fig)

# ---------------------------------------------------------------- Fig 2
def fig_partial_scatter():
    keys = ["z_circ", "mag_circ", "epr"]
    fig, axes = plt.subplots(4, 3, figsize=(11.5, 13))
    for i, nm in enumerate(SESS):
        d = load_windows(nm); agent = nm.split("/")[1]
        rt = _rank(d["t"]); X = np.column_stack([np.ones(len(rt)), rt])
        es = _resid(_rank(d["S_direct"]), X)
        for j, key in enumerate(keys):
            ax = axes[i, j]
            em = _resid(_rank(d[key]), X)
            r = RES["sessions"][nm]["partials"][f"{key}|S_direct"]["r_partial_time"]
            ci = RES["sessions"][nm]["partials"][f"{key}|S_direct"]["ci95"]
            ax.scatter(es, em, s=7, alpha=0.45, color=COL[agent], lw=0)
            b = np.polyfit(es, em, 1)
            xs = np.linspace(es.min(), es.max(), 10)
            ax.plot(xs, np.polyval(b, xs), color="k", lw=1.6)
            ax.axhline(0, c="0.8", lw=0.6); ax.axvline(0, c="0.8", lw=0.6)
            ax.set_title(f"{nm}  {key}\nr={r:+.3f}  CI[{ci[0]:+.2f},{ci[1]:+.2f}]",
                         fontsize=9, color=("#1a7a35" if ci[0] > 0 else "#a51d2d" if ci[1] < 0 else "0.3"))
            if j == 0: ax.set_ylabel("maintenance rank resid.", fontsize=8)
            if i == 3: ax.set_xlabel("STOCK rank resid. (S_direct)", fontsize=8)
            ax.tick_params(labelsize=7)
    fig.suptitle("Rent-tracks-stock: maintenance vs stock, both residualised on rank(time)\n"
                 "PREDICTION: positive slope in every panel.  green title = CI excludes 0 positive, red = negative",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(HERE, "fig2_partial_scatter.png"), dpi=140)
    plt.close(fig)

# ---------------------------------------------------------------- Fig 3
def fig_forest():
    proxies = [p[0] for p in PROXIES]
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 7), sharey=True)
    for a, stock in enumerate(["S_direct", "S_closed"]):
        ax = axes[a]; y = 0; ticks, labs = [], []
        for key in proxies:
            for nm in SESS:
                p = RES["sessions"][nm]["partials"].get(f"{key}|{stock}")
                if p is None: continue
                agent = nm.split("/")[1]
                lo, hi = p["ci95"]; r = p["r_partial_time"]
                ax.plot([lo, hi], [y, y], color=COL[agent], lw=2.2, alpha=0.8)
                ax.plot([r], [y], "o", color=COL[agent], ms=6,
                        mec="k" if (lo > 0 or hi < 0) else "none", mew=1.0)
                ticks.append(y); labs.append(f"{key} · {nm}")
                y -= 1
            pl = RES["pooled"].get(f"{key}|{stock}")
            if pl:
                ax.plot(pl["fe_ci"], [y, y], color="k", lw=3.0)
                ax.plot([pl["fe_r"]], [y], "D", color="k", ms=7)
                ticks.append(y); labs.append(f"{key} · POOLED (FE)   I²={pl['I2_pct']:.0f}%")
                y -= 1.6
        ax.axvline(0, color="0.25", lw=1.2)
        ax.set_yticks(ticks); ax.set_yticklabels(labs, fontsize=8)
        ax.set_xlabel("Spearman partial r  (maintenance, STOCK | time)")
        ax.set_title(f"STOCK = {stock}", fontsize=11)
        ax.set_xlim(-1, 1)
        ax.grid(axis="x", alpha=0.25)
    fig.suptitle("Rent-tracks-stock forest: prediction is r > 0 everywhere.\n"
                 "red = propofol, blue = ketamine.  Black outline = CI excludes 0.  "
                 "Block-bootstrap CIs (autocorrelated windows).", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(os.path.join(HERE, "fig3_forest.png"), dpi=140)
    plt.close(fig)

# ---------------------------------------------------------------- Fig 4
def fig_proxy_disagreement():
    """|z| vs rate: does the significance score track the magnitude at all?"""
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.2))
    for i, nm in enumerate(SESS):
        d = load_windows(nm); agent = nm.split("/")[1]; ax = axes[i]
        sc = ax.scatter(d["mag_circ"], d["z_circ"], s=8, alpha=0.5,
                        c=d["t"], cmap="viridis", lw=0)
        rho = np.corrcoef(_rank(d["mag_circ"]), _rank(d["z_circ"]))[0, 1]
        ax.axhline(1.5, ls=":", c="0.4")
        ax.set_title(f"{nm}\nSpearman(|z|, rate) = {rho:+.2f}", fontsize=9,
                     color=COL[agent])
        ax.set_xlabel("Σ|ω| circulation rate [rad/s]", fontsize=8)
        if i == 0: ax.set_ylabel("|z| circulation (significance)", fontsize=8)
        ax.set_xscale("log"); ax.tick_params(labelsize=7)
        plt.colorbar(sc, ax=ax, label="t (s)" if i == 3 else "")
    fig.suptitle("Caveat (i) made visible: the published |z| is a SIGNIFICANCE score, not a rate. "
                 "Where these two disagree, the |z| result is about the surrogate noise floor, not about γM.",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(os.path.join(HERE, "fig4_proxy_disagreement.png"), dpi=140)
    plt.close(fig)

if __name__ == "__main__":
    fig_trajectories(); fig_partial_scatter(); fig_forest(); fig_proxy_disagreement()
    print("figures written")
