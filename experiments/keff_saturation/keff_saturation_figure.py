#!/usr/bin/env python3
"""
k_eff saturation figure — the direct, convention-robust read of the Gate-0
(criticality vs low-rank) discriminator.

The discriminator (formalized in CoherenceRatchet/Cosmology/CriticalityDiscriminator.lean):
  - LOW-RANK (novel):  k_eff -> 1/rho_0, a bounded ceiling, as k grows.
  - CRITICALITY (trivial): k_eff ~ sqrt(k)/c, unbounded, as k grows.

Plotting the DIRECTLY-MEASURED k_eff against system size k sidesteps the
band-center-definition and log-log-slope fragility that make the rho*-vs-k
regression underpowered. If k_eff climbs like sqrt(k) it is criticality; if it
sits flat in a bounded band it is low-rank.

Per-substrate numbers are transcribed from the repo (citations in DATA below).
Estimator discipline: k_eff is the reported participation-ratio / empirical
k_eff where available. Where only rho* is reported, the Kish value 1/rho* is
shown as a hollow marker and labelled, and NOT mixed with measured k_eff in the
trend commentary.
"""
import numpy as np

# substrate, k (parts), k_eff_measured (participation-ratio/empirical; None if only rho*),
# rho_star (debiased band center; for the Kish fallback), citation
DATA = [
    ("Drosophila CX",     24,   7.9,  0.331, "robust_rerun/drosophila (EPG/FC2 16, FC3 32; k_eff 3.45-12.4)"),
    ("EEG interictal",    21,   6.5,  0.269, "robust_rerun/eeg (CHB-MIT; k_eff PR 6.5)"),
    ("TCGA (Hallmark)",   50,   7.0,  0.312, "tcga_debiased (pathways; k_eff PR 4.9-10.0)"),
    ("C. elegans",       100,   3.9,  0.312, "robust_rerun/celegans (imaged ~100; k_eff_emp 3.9)"),
    ("Allen mouse ctx",  126,   9.73, 0.10,  "allen_keff_retest (N median 126; k_eff_emp 9.73)"),
    ("fMRI (ABIDE)",     200,   8.0,  0.266, "data_fmri (CC200; k_eff_emp 8.0)"),
    ("LLM internals",    800,   None, 0.082, "band_calibration (768-896 units; rho* only -> Kish fallback)"),
]

def main():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"[no matplotlib: {e}] printing table instead")
        print(f"{'substrate':18s} {'k':>6s} {'k_eff':>7s} {'source':>8s}")
        for name, k, keff, rho, _ in DATA:
            v = keff if keff is not None else 1.0/rho
            src = "meas" if keff is not None else "Kish"
            print(f"{name:18s} {k:6d} {v:7.2f} {src:>8s}")
        return

    import matplotlib.pyplot as plt

    ks       = np.array([d[1] for d in DATA], float)
    measured = [d[2] for d in DATA]
    rhos     = np.array([d[3] for d in DATA], float)

    meas_mask = np.array([m is not None for m in measured])
    keff_meas = np.array([m if m is not None else np.nan for m in measured], float)
    keff_kish = 1.0 / rhos  # fallback / cross-check

    kgrid = np.logspace(np.log10(ks.min()*0.8), np.log10(ks.max()*1.2), 200)

    fig, ax = plt.subplots(figsize=(8.2, 5.4))

    # --- theoretical reference curves (both in MEASURED-k_eff units, apples-to-apples) ---
    # Low-rank: k_eff sits in a bounded, k-independent band. Reference = mean +/- std
    # of the MEASURED k_eff (not 1/rho*, which is a different estimator).
    keff_band = keff_meas[meas_mask]
    band_mean, band_sd = float(np.mean(keff_band)), float(np.std(keff_band))
    ax.axhspan(band_mean-band_sd, band_mean+band_sd, color="#2a7", alpha=0.15, zorder=1)
    ax.axhline(band_mean, ls="--", lw=1.6, color="#2a7", zorder=2,
               label=f"low-rank: bounded band  k_eff ≈ {band_mean:.1f} ± {band_sd:.1f}")

    # Criticality: k_eff = sqrt(k)/c, anchored to the smallest-k measured point so
    # the two references agree at low k and diverge as k grows.
    anchor_i = int(np.nanargmin(ks[meas_mask]))
    k_anchor = ks[meas_mask][anchor_i]
    keff_anchor = keff_meas[meas_mask][anchor_i]
    c = np.sqrt(k_anchor) / keff_anchor
    ax.plot(kgrid, np.sqrt(kgrid)/c, ls=":", lw=1.8, color="#c33", zorder=2,
            label=f"criticality  √k/c  (anchored at k={k_anchor:.0f}; ⟹ {keff_anchor*np.sqrt(ks[meas_mask].max()/k_anchor):.0f} at k={ks[meas_mask].max():.0f})")

    # --- data ---
    ax.scatter(ks[meas_mask], keff_meas[meas_mask], s=90, color="#124", zorder=5,
               label="measured k_eff (participation ratio)")
    for name, k, keff, rho, _ in DATA:
        if keff is not None:
            ax.annotate(name, (k, keff), textcoords="offset points", xytext=(6, 5),
                        fontsize=8, color="#124")
    # Kish-fallback points (hollow) — not part of the measured trend
    ax.scatter(ks[~meas_mask], keff_kish[~meas_mask], s=90, facecolors="none",
               edgecolors="#777", zorder=4, label="Kish 1/ρ* (ρ*-only substrate)")
    for name, k, keff, rho, _ in DATA:
        if keff is None:
            ax.annotate(name+" (Kish)", (k, 1.0/rho), textcoords="offset points",
                        xytext=(6, -12), fontsize=8, color="#777")

    ax.set_xscale("log")
    ax.set_xlabel("system size  k  (number of parts, log scale)")
    ax.set_ylabel("effective dimensionality  k_eff")
    ax.set_ylim(0, max(np.nanmax(keff_meas), band_mean+band_sd, np.sqrt(kgrid[-1])/c)*1.15)
    ax.set_title("k_eff saturation: measured k_eff stays bounded as k grows\n"
                 "(flat band ⟹ low-rank / not-trivial;  √k climb ⟹ criticality / trivial)")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.95)
    ax.grid(True, which="both", alpha=0.25)

    # honest caption
    span = np.log10(ks[meas_mask].max()/ks[meas_mask].min())
    cap = (f"n={int(meas_mask.sum())} measured substrates, k spans {span:.1f} decades. "
           f"Measured k_eff range {np.nanmin(keff_meas):.1f}–{np.nanmax(keff_meas):.1f}; "
           f"criticality would predict ≈{keff_anchor*np.sqrt(ks[meas_mask].max()/k_anchor):.0f} "
           f"at k={ks[meas_mask].max():.0f}. Directional (low-rank-leaning), not decisive: "
           f"under-powered on range, and a high-k engineered point under a fixed "
           f"static-ρ estimator is the cheapest way to make it decisive.")
    fig.text(0.5, -0.02, cap, ha="center", va="top", fontsize=7.5, wrap=True)

    out = __file__.rsplit("/", 1)[0] + "/keff_saturation.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")
    print(f"low-rank bounded band: measured k_eff ≈ {band_mean:.2f} ± {band_sd:.2f}")
    print(f"criticality would predict k_eff ≈ "
          f"{keff_anchor*np.sqrt(ks[meas_mask].max()/k_anchor):.1f} at k={ks[meas_mask].max():.0f}; "
          f"measured max is {np.nanmax(keff_meas):.1f}")

if __name__ == "__main__":
    main()
