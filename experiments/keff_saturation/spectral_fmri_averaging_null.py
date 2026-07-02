#!/usr/bin/env python3
"""
AVERAGING-NULL control for the ABIDE CC200 region-level low-rank result.

Question: is region-level low k_eff GENUINE cross-region coordination, or a
mechanical artifact of coarse-graining (averaging independent sources into 200
regions + finite-T spurious correlation)?

k_eff := participation ratio of the signed correlation matrix (same definition
as the prior fMRI corridor read, data_fmri/RESULTS.md).

Three quantities per control subject (reuse the SAME loaded ROI x time data):
  real          : PR of the real 200-ROI correlation matrix.
  phase_rand    : PR after per-region FFT phase-randomization -- destroys
                  cross-region structure, preserves each region's EXACT power
                  spectrum. Spectrum-matched independent null.
  avg_null      : PR of 200 INDEPENDENT AR(1) signals, each matched to a real
                  region's lag-1 autocorr + variance, same T. The "no-coordination
                  brain": what averaging independent autocorrelated sources into
                  200 regions gives with ZERO coupling.

If real k_eff << null k_eff  -> genuine brain-wide low-rank coordination.
If real k_eff ~= null k_eff  -> the low-rank is just averaging (trivial).

Synthetics are the NULL, clearly labeled. Real data never fabricated.
"""
import numpy as np, json, os
from spectral_test_tcga_fmri import (load_abide_controls, load_1d, corr_eig,
                                      participation_ratio, phase_randomize)

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(1)

def keff(X):
    ev, *_ = corr_eig(X)
    return participation_ratio(ev)

def ar1_null(X):
    """200 independent AR(1) series matched to each region's lag-1 autocorr &
    variance, same T. Zero cross-region coordination by construction."""
    N, T = X.shape
    Z = X - X.mean(1, keepdims=True)
    Y = np.empty((N, T))
    for i in range(N):
        x = Z[i]
        v = x.var()
        denom = (x[:-1] ** 2).sum()
        phi = float((x[:-1] * x[1:]).sum() / denom) if denom > 1e-12 else 0.0
        phi = np.clip(phi, -0.999, 0.999)
        eps_sd = np.sqrt(max(v * (1 - phi ** 2), 1e-12))
        y = np.empty(T)
        y[0] = RNG.standard_normal() * np.sqrt(max(v, 1e-12))
        e = RNG.standard_normal(T) * eps_sd
        for t in range(1, T):
            y[t] = phi * y[t - 1] + e[t]
        Y[i] = y
    return Y

def boot_ci(vals, nboot=5000):
    vals = np.asarray(vals)
    meds = [np.median(RNG.choice(vals, vals.size, replace=True)) for _ in range(nboot)]
    return float(np.median(vals)), float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))

def main():
    subs = load_abide_controls()
    NDRAW = 5
    rows = []
    print(f"{'subject':16s} {'N':>3s} {'T':>4s} {'real':>6s} {'phase':>6s} {'avgnull':>7s} "
          f"{'null/real':>9s}")
    for fid, f in subs:
        X = load_1d(f)
        if X.shape[0] < 50 or X.shape[1] < 40:
            continue
        N, T = X.shape
        k_real = keff(X)
        k_phase = float(np.mean([keff(phase_randomize(X)) for _ in range(NDRAW)]))
        k_avg = float(np.mean([keff(ar1_null(X)) for _ in range(NDRAW)]))
        rows.append(dict(subject=fid, N=int(N), T=int(T),
                         k_real=float(k_real), k_phase=k_phase, k_avg=k_avg,
                         ratio_phase=k_phase / k_real, ratio_avg=k_avg / k_real))
        print(f"{fid:16s} {N:3d} {T:4d} {k_real:6.2f} {k_phase:6.2f} {k_avg:7.2f} "
              f"{k_avg / k_real:9.2f}")

    real = np.array([r["k_real"] for r in rows])
    phase = np.array([r["k_phase"] for r in rows])
    avg = np.array([r["k_avg"] for r in rows])
    rp = np.array([r["ratio_phase"] for r in rows])
    ra = np.array([r["ratio_avg"] for r in rows])

    agg = {}
    for name, v in [("k_real", real), ("k_phase_surrogate", phase),
                    ("k_avg_null", avg), ("ratio_phase_over_real", rp),
                    ("ratio_avgnull_over_real", ra)]:
        m, lo, hi = boot_ci(v)
        agg[name] = dict(median=m, ci95=[lo, hi],
                         p5=float(np.percentile(v, 5)), p95=float(np.percentile(v, 95)))

    # corridor placement of REAL k_eff (2.3-10)
    in_corr = int(((real >= 2.3) & (real <= 10)).sum())
    corridor = dict(band=[2.3, 10.0], frac_in_band=in_corr / len(real),
                    n_in_band=in_corr, n=len(real),
                    real_median=float(np.median(real)),
                    real_p5=float(np.percentile(real, 5)),
                    real_p95=float(np.percentile(real, 95)))

    # verdict
    ratio_med = agg["ratio_avgnull_over_real"]["median"]
    ratio_lo = agg["ratio_avgnull_over_real"]["ci95"][0]
    if ratio_lo > 1.5:
        verdict = ("GENUINE cross-region coordination: real k_eff is far below the "
                   "averaging null (independent AR(1)-matched sources). The low-rank "
                   "is NOT a coarse-graining artifact.")
    elif ratio_lo > 1.1:
        verdict = "GENUINE but modest: real k_eff below null, margin small."
    else:
        verdict = ("AVERAGING ARTIFACT: real k_eff ~= null; low-rank explained by "
                   "coarse-graining + finite-T, not coordination.")

    out = dict(substrate="ABIDE-PCP CC200 resting-state fMRI (controls)",
               keff_definition="participation ratio of signed 200x200 correlation matrix",
               n_subjects=len(rows), ndraw_per_null=NDRAW,
               nulls=dict(
                   phase_rand="per-region FFT phase-randomization (exact power spectrum, independent)",
                   avg_null="200 independent AR(1) series matched to per-region lag-1 autocorr+variance"),
               aggregate=agg, corridor=corridor, verdict=verdict, per_subject=rows)
    json.dump(out, open(os.path.join(HERE, "spectral_fmri_averaging_null.json"), "w"), indent=1)

    print(f"\n=== AGGREGATE (median [95pct CI], n={len(rows)} controls) ===")
    for k in ["k_real", "k_phase_surrogate", "k_avg_null",
              "ratio_phase_over_real", "ratio_avgnull_over_real"]:
        a = agg[k]
        print(f"  {k:26s} {a['median']:6.2f}  CI[{a['ci95'][0]:.2f},{a['ci95'][1]:.2f}]  "
              f"p5-95[{a['p5']:.2f},{a['p95']:.2f}]")
    print(f"\n  REAL k_eff in corridor (2.3-10): {in_corr}/{len(real)} "
          f"= {100*in_corr/len(real):.0f}%  (median {np.median(real):.2f})")
    print(f"\n  VERDICT: {verdict}")
    print("\nwrote spectral_fmri_averaging_null.json")

if __name__ == "__main__":
    main()
