"""
Figures for the C. elegans corridor relaxation measurement.

Run run_corridor_relaxation.py first (produces results_corridor_relaxation.json).
This script reloads the data, recomputes the headline-window rho(t) for one
representative worm to show the corridor trajectory and its ACF, and draws the
across-worm rate distribution from the saved JSON.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from run_corridor_relaxation import (rho_trajectory, acf, tau_ac,
                                     global_cycle_period, W_HEADLINE)

HERE = Path(__file__).parent
res = json.load(open(HERE / "results_corridor_relaxation.json"))
hl_key = f"{W_HEADLINE:.0f}s"
hl = res["windows"][hl_key]

df = pd.read_parquet(HERE / "data" / "kato2015_whole_brain.parquet")

# representative worm = the one whose r* is closest to the across-worm mean
agg = hl["aggregate"]
pw = hl["per_worm"]
target = agg["r_star_mean"]
cand = {w: v for w, v in pw.items()
        if isinstance(v["r_star"], (int, float)) and np.isfinite(v["r_star"])}
rep = min(cand, key=lambda w: abs(cand[w]["r_star"] - target))

g = df[df.worm == rep]
X = np.array([np.asarray(c, float) for c in g["calcium_data"]])
X = X[X.std(1) > 1e-9]
t = np.asarray(g["time_in_seconds"].iloc[0], float)
dt = float(np.median(np.diff(t)))
W = int(round(W_HEADLINE / dt))
rho = rho_trajectory(X, W)
tac, tint, fit_lag = tau_ac(rho, dt)
Tg, _ = global_cycle_period(X, dt)
a = acf(rho - rho.mean(), len(rho) // 4)
lags_s = np.arange(len(a)) * dt

fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# (a) rho(t) corridor trajectory
ax = axes[0, 0]
tt = np.arange(len(rho)) * dt + W_HEADLINE / 2
ax.plot(tt, rho, lw=0.8, color="C0")
ax.axhline(rho.mean(), color="k", ls="--", lw=1,
           label=f"mean ρ̄ = {rho.mean():.3f}")
ax.axhspan(0.1, 0.43, color="C2", alpha=0.12, label="framework corridor (0.1, 0.43)")
ax.set_xlabel("time (s)")
ax.set_ylabel("ρ(t)  (Kish-inverted k_eff)")
ax.set_title(f"(a) corridor trajectory — {rep}, {W_HEADLINE:.0f}s window")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (b) ACF + exponential fit
ax = axes[0, 1]
ax.plot(lags_s, a, color="C0", label="ACF of ρ(t)")
if np.isfinite(tac):
    fit = np.exp(-lags_s / tac)
    ax.plot(lags_s, fit, "r--", label=f"exp fit, τ_ac = {tac:.1f}s")
ax.axhline(0, color="k", lw=0.5)
ax.axvline(W_HEADLINE, color="C3", ls=":", label=f"window = {W_HEADLINE:.0f}s")
ax.set_xlim(0, min(lags_s[-1], 6 * (tac if np.isfinite(tac) else 30)))
ax.set_xlabel("lag (s)")
ax.set_ylabel("autocorrelation")
ax.set_title("(b) ρ(t) autocorrelation and relaxation-time fit")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (c) across-worm tau_ac vs surrogate
ax = axes[1, 0]
worms = sorted(pw.keys())
real_tac = [pw[w]["tau_ac_s"] for w in worms]
sur_m = [pw[w]["surrogate_tau_ac_mean"] for w in worms]
sur_p95 = [pw[w]["surrogate_tau_ac_p95"] for w in worms]
x = np.arange(len(worms))
ax.bar(x - 0.2, real_tac, 0.4, color="C0", label="real τ_ac")
ax.bar(x + 0.2, sur_m, 0.4, color="0.6", label="surrogate τ_ac (mean)")
ax.plot(x + 0.2, sur_p95, "kx", ms=7, label="surrogate p95")
ax.axhline(W_HEADLINE, color="C3", ls=":", label=f"window {W_HEADLINE:.0f}s")
ax.set_xticks(x)
ax.set_xticklabels(worms, rotation=45, ha="right", fontsize=7)
ax.set_ylabel("τ_ac (s)")
ax.set_title("(c) real vs phase-randomised-surrogate relaxation time")
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis="y")

# (d) dimensionless r* across worms + window sweep
ax = axes[1, 1]
rstar = [pw[w]["r_star"] for w in worms]
ax.bar(x, rstar, 0.6, color="C4", label="r* = T_global / τ_ac")
ax.axhline(agg["r_star_mean"], color="k", ls="--",
           label=f"mean r* = {agg['r_star_mean']:.1f} ± {agg['r_star_std']:.1f}")
ax.axhline(1.0, color="C3", ls=":", label="r* = 1 (relax = global cycle)")
ax.set_xticks(x)
ax.set_xticklabels(worms, rotation=45, ha="right", fontsize=7)
ax.set_ylabel("dimensionless rate r*")
ws = res["w_stability_rstar_means"]
ax.set_title("(d) dimensionless relaxation rate per worm\n"
             f"W-sweep r*: " +
             ", ".join(f"{k}={float(v):.1f}" for k, v in ws.items()))
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis="y")

plt.tight_layout()
out = HERE / "corridor_relaxation.png"
plt.savefig(out, dpi=120)
print(f"Figure: {out}")
