#!/usr/bin/env python3
"""Fit-quality-vs-threshold-mass overlaid on the SHM efficiency curve. Reads results.json."""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "shm_anchor"))
import shm_models as sm

res = json.load(open(HERE / "results.json"))
pt = [r for r in res["per_threshold"] if r.get("z_peak_globalmax") is not None
      and "cpl" in r]
logM = np.array([r["log10_thr"] for r in pt])
maha = np.array([r["cpl"]["maha"] for r in pt])
chi2 = np.array([r["likelihood"]["chi2"] for r in pt])
dlcdm = np.array([r["likelihood"]["chi2_minus_lcdm"] for r in pt])
zpeak = np.array([r["z_peak_globalmax"] for r in pt])
capped = np.array([r["cap_limited"] for r in pt])
fully = np.array([r["fully_capped"] for r in pt])
lcdm = res["lcdm_chi2"]
shm_ref = res["shm_peak_ref_log10Msunh"]

# SHM efficiency curve epsilon(M) at z=0 and z=0.5, in Msun/h
grid_h = np.linspace(11.0, 13.0, 300)
grid_msun = grid_h - np.log10(sm.H_TNG)
eps0 = np.array([sm.moster_ratio(m, 0.0) for m in grid_msun])
eps05 = np.array([sm.moster_ratio(m, 0.5) for m in grid_msun])
epsb0 = np.array([sm.behroozi_ratio(m, 0.0) for m in grid_msun])

fig, axes = plt.subplots(2, 1, figsize=(9, 9), sharex=True)

# ---- top: fit quality (Mahalanobis + chi2) vs threshold, SHM overlay ----
ax = axes[0]
mk = lambda c: ["s" if x else "o" for x in c]
for i in range(len(logM)):
    m = "D" if fully[i] else ("s" if capped[i] else "o")
    ax.plot(logM[i], maha[i], m, color="C0", ms=9, mec="k",
            mfc=("none" if capped[i] else "C0"), zorder=5)
ax.plot(logM, maha, "-", color="C0", lw=1.3, alpha=0.6, label="Mahalanobis to DESI (σ)")
ax.set_ylabel("Mahalanobis distance to DESI DR2 (σ)", color="C0")
ax.tick_params(axis="y", labelcolor="C0")
imin = int(np.argmin(maha))
ax.annotate(f"min at {logM[imin]:.2f}", (logM[imin], maha[imin]),
            textcoords="offset points", xytext=(6, 10), color="C0", fontsize=9)

ax2 = ax.twinx()
ax2.plot(logM, chi2, "-", color="C3", lw=1.3, alpha=0.6)
for i in range(len(logM)):
    mfc = "none" if capped[i] else "C3"
    ax2.plot(logM[i], chi2[i], ("D" if fully[i] else ("s" if capped[i] else "o")),
             color="C3", ms=8, mec="k", mfc=mfc, zorder=5)
ax2.axhline(lcdm, color="C3", ls=":", lw=1, alpha=0.7)
ax2.text(logM.max(), lcdm, " LCDM", color="C3", va="bottom", fontsize=8)
ax2.set_ylabel("real DESI DR2 likelihood χ²", color="C3")
ax2.tick_params(axis="y", labelcolor="C3")
ci = int(np.argmin(chi2))
ax2.annotate(f"min at {logM[ci]:.2f}", (logM[ci], chi2[ci]),
             textcoords="offset points", xytext=(6, -14), color="C3", fontsize=9)

ax.axvspan(shm_ref - 0.3, shm_ref + 0.3, color="green", alpha=0.10, zorder=0)
ax.axvline(shm_ref, color="green", ls="--", lw=1.5, label=f"SHM peak {shm_ref:.2f}")
ax.axvline(11.92, color="green", ls=":", lw=1, alpha=0.6)
ax.set_title("Fit quality vs cumulative-threshold mass  (open/diamond = cap-limited)")
ax.legend(loc="upper right", fontsize=8)
ax.grid(alpha=0.25)

# ---- bottom: SHM efficiency + peak epoch vs threshold ----
ax = axes[1]
ax.plot(grid_h, eps0 / eps0.max(), color="green", lw=2, label="Moster+2013 ε(M) z=0")
ax.plot(grid_h, eps05 / eps05.max(), color="green", lw=1.3, ls="--",
        label="Moster+2013 ε(M) z=0.5")
ax.plot(grid_h, epsb0 / epsb0.max(), color="darkgreen", lw=1.0, ls=":",
        label="Behroozi+2013 ε(M) z=0")
ax.axvspan(shm_ref - 0.3, shm_ref + 0.3, color="green", alpha=0.10)
ax.axvline(shm_ref, color="green", ls="--", lw=1.5)
ax.set_ylabel("SHM efficiency ε(M) (normalized)", color="green")
ax.set_xlabel("cumulative threshold mass  log10(M / Msun h⁻¹)")
ax.legend(loc="upper right", fontsize=8)
ax.grid(alpha=0.25)

ax3 = ax.twinx()
ax3.plot(logM, zpeak, "-", color="C1", lw=1.2, alpha=0.6)
for i in range(len(logM)):
    ax3.plot(logM[i], zpeak[i], ("D" if fully[i] else ("s" if capped[i] else "o")),
             color="C1", ms=7, mec="k", mfc=("none" if capped[i] else "C1"))
ax3.set_ylabel("S(a) global-max peak epoch  z_peak", color="C1")
ax3.tick_params(axis="y", labelcolor="C1")

fig.tight_layout()
fig.savefig(HERE / "figures" / "retention_fit_vs_shm.png", dpi=130)
print("wrote figures/retention_fit_vs_shm.png")
print(f"Mahalanobis min at log10M = {logM[imin]:.3f} (SHM ref {shm_ref}); "
      f"chi2 min at {logM[ci]:.3f}")
