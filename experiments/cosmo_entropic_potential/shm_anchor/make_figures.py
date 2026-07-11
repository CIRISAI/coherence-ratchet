#!/usr/bin/env python3
"""
Figures for the SHM retention-anchor scan. Reads analysis.json + results.json.
  fig_money_overlay.png : DESI-fit-quality vs unit mass scale (both boxes), overlaid on
                          the SHM efficiency curve epsilon(M) (Moster/Behroozi) + peak band.
  fig_peak_epoch.png    : S-peak epoch (global max) vs unit mass scale, plateau breadth.
  fig_curves_S.png      : the raw S(a) curves per bin (diagnostic).
Idempotent.
"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shm_models as SHM

A = json.load(open(HERE / "analysis.json"))
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)

def ok_bins(store):
    xs, out = [], []
    for c, b in store.items():
        if b.get("ok"):
            xs.append(b["center"]); out.append(b)
    o = np.argsort(xs)
    return np.array(xs)[o], [out[i] for i in o]

# SHM efficiency curves in Msun/h axis, at z=0 and z=0.5 (S-peak epoch)
Mh_Msun = np.linspace(10.6, 13.4, 400)
Mh_axis = SHM.Msun_to_Msunh(Mh_Msun)   # convert x to Msun/h
eff_mos0 = SHM.moster_ratio(Mh_Msun, 0.0)
eff_mos5 = SHM.moster_ratio(Mh_Msun, 0.5)
eff_beh0 = SHM.behroozi_ratio(Mh_Msun, 0.0)
eff_beh5 = SHM.behroozi_ratio(Mh_Msun, 0.5)
peak = A["shm"]["peaks_z0"]; peak5 = A["shm"]["peaks_z0p5"]
band_lo = min(peak["moster_Msunh"], peak["behroozi_Msunh"])
band_hi = max(peak5["moster_Msunh"], peak5["behroozi_Msunh"])

# =====================================================================
# MONEY FIGURE
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 6.2))
ax2 = ax.twinx()
# SHM efficiency band + curves (right axis)
ax2.axvspan(band_lo, band_hi, color="gold", alpha=0.25, zorder=0,
            label=f"SHM efficiency peak (z=0->0.5): {band_lo:.2f}-{band_hi:.2f}")
ax2.plot(Mh_axis, eff_mos0, color="darkgoldenrod", lw=1.3, ls="-", alpha=0.8, label="Moster+2013 eps(M) z=0")
ax2.plot(Mh_axis, eff_mos5, color="darkgoldenrod", lw=1.3, ls="--", alpha=0.8, label="Moster+2013 z=0.5")
ax2.plot(Mh_axis, eff_beh0, color="olive", lw=1.3, ls="-", alpha=0.8, label="Behroozi+2013 eps(M) z=0")
ax2.plot(Mh_axis, eff_beh5, color="olive", lw=1.3, ls="--", alpha=0.8, label="Behroozi+2013 z=0.5")
ax2.set_ylabel("SHM efficiency  m*/M_halo   (fetched, not re-derived)", color="olive")
ax2.tick_params(axis="y", labelcolor="olive")

# DESI-fit-quality Mahalanobis (left axis, lower = better fit)
for store, color, marker, lab in [("tng300_bins", "C0", "o", "TNG300 (box 205)"),
                                   ("tng100_bins", "C3", "s", "TNG100 (box 75)")]:
    xs, bs = ok_bins(A[store])
    if len(xs) == 0:
        continue
    mah = [b["cpl_dist"]["maha"] for b in bs]
    ax.plot(xs, mah, color=color, marker=marker, ms=7, lw=2, label=f"{lab}: Mahalanobis to DESI")
    # mark the minimum
    imin = int(np.argmin(mah))
    ax.annotate(f"min {xs[imin]:.2f}", (xs[imin], mah[imin]),
                textcoords="offset points", xytext=(0, -16), color=color, fontsize=9)
ax.set_ylabel("DESI-fit quality: Mahalanobis distance to DESI (w0,wa)  [lower = better]")
ax.set_xlabel("unit mass scale  log10 M_halo  [Msun/h]  (bin center, width 0.4 dex)")
ax.set_title("Retention-anchor test: does DESI-fit quality extremize at the SHM efficiency peak?")
ax.grid(alpha=0.25)
# top axis in Msun
axt = ax.twiny()
axt.set_xlim(ax.get_xlim());
def to_msun(x): return x - np.log10(SHM.H_TNG)
ticks = ax.get_xticks()
axt.set_xticks(ticks); axt.set_xticklabels([f"{to_msun(t):.1f}" for t in ticks])
axt.set_xlabel("log10 M_halo  [Msun]")
# combined legend
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper right", framealpha=0.9)
fig.tight_layout()
fig.savefig(FIG / "fig_money_overlay.png", dpi=130)
plt.close(fig)

# also a version with the real-likelihood chi2-LCDM (TNG300)
fig, ax = plt.subplots(figsize=(10, 6.2))
ax2 = ax.twinx()
ax2.axvspan(band_lo, band_hi, color="gold", alpha=0.25, zorder=0,
            label=f"SHM efficiency peak: {band_lo:.2f}-{band_hi:.2f} Msun/h")
ax2.plot(Mh_axis, eff_beh5, color="olive", lw=1.4, ls="-", label="Behroozi+2013 eps(M) z=0.5")
ax2.plot(Mh_axis, eff_mos5, color="darkgoldenrod", lw=1.4, ls="-", label="Moster+2013 eps(M) z=0.5")
ax2.set_ylabel("SHM efficiency m*/M_halo", color="olive"); ax2.tick_params(axis="y", labelcolor="olive")
xs, bs = ok_bins(A["tng300_bins"])
have = [(b["center"], b["likelihood"]["chi2_minus_LCDM"]) for b in bs if "likelihood" in b]
if have:
    hx = [h[0] for h in have]; hy = [h[1] for h in have]
    ax.plot(hx, hy, color="C0", marker="o", ms=7, lw=2, label="TNG300 real DESI DR2 chi2 - LCDM")
    ax.axhline(0, color="gray", ls=":", lw=1)
ax.set_ylabel("real DESI DR2 likelihood  chi2(framework) - chi2(LCDM)   [<0 = beats LCDM]")
ax.set_xlabel("unit mass scale  log10 M_halo  [Msun/h]")
ax.set_title("Retention-anchor test (real DESI DR2 likelihood): TNG300 bins")
ax.grid(alpha=0.25)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="best")
fig.tight_layout(); fig.savefig(FIG / "fig_money_likelihood.png", dpi=130); plt.close(fig)

# =====================================================================
# PEAK-EPOCH vs MASS
# =====================================================================
fig, ax = plt.subplots(figsize=(9.5, 6))
for store, color, marker, lab in [("tng300_bins", "C0", "o", "TNG300"),
                                  ("tng100_bins", "C3", "s", "TNG100")]:
    xs, bs = ok_bins(A[store])
    if len(xs) == 0:
        continue
    zp = np.array([b["z_peak"] for b in bs])
    plo = np.array([b["z_plateau_lo"] for b in bs])
    phi = np.array([b["z_plateau_hi"] for b in bs])
    ax.errorbar(xs, zp, yerr=[zp - plo, phi - zp], color=color, marker=marker,
                ms=7, lw=2, capsize=3, label=f"{lab}: global-max z (bars=5% plateau)")
ax.axvspan(band_lo, band_hi, color="gold", alpha=0.25, label="SHM efficiency peak")
ax.set_xlabel("unit mass scale  log10 M_halo  [Msun/h]")
ax.set_ylabel("S(a) global-max epoch  z_peak")
ax.set_title("S-peak epoch vs unit mass scale")
ax.grid(alpha=0.25); ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig(FIG / "fig_peak_epoch.png", dpi=130); plt.close(fig)

# =====================================================================
# RAW S(a) CURVES (diagnostic)
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
for store, ax, title in [("tng300_bins", axes[0], "TNG300"),
                         ("tng100_bins", axes[1], "TNG100")]:
    xs, bs = ok_bins(A[store])
    cmap = plt.cm.viridis(np.linspace(0, 1, max(len(bs), 1)))
    for b, col in zip(bs, cmap):
        z = np.array(b["z"]); Sa = np.array(b["S"])
        ax.plot(z, Sa / Sa.max(), color=col, marker=".", ms=4, lw=1.2,
                label=f"c={b['center']:.2f}")
    ax.set_xlabel("z"); ax.set_ylabel("S(a) / S_max"); ax.set_title(f"{title} S(a), normalized")
    ax.invert_xaxis(); ax.grid(alpha=0.25); ax.legend(fontsize=7, ncol=2)
fig.tight_layout(); fig.savefig(FIG / "fig_curves_S.png", dpi=120); plt.close(fig)

print("wrote figures to", FIG)
