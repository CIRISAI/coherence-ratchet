#!/usr/bin/env python3
"""
STIMULUS-CONFOUND control for the ZAPBench whole-brain saturation test.

The full recording is 9 successive visual conditions. Shared stimulus drive
across conditions could impose low dimensionality artificially (a discrete
9-regime block structure inflates the top eigenvalues and depresses PR). This
re-runs the saturation curve + block-interleaved CV WITHIN a single condition,
where the global stimulus regime is fixed, so between-condition shared drive is
removed. If PR still saturates at a similar level, the low-rank is intrinsic;
if it jumps up (toward power-law growth), the whole-recording saturation was a
stimulus artifact.

Reuses the analysis core from spectral_zebrafish.py; cached traces (no
re-download). Real data only; incremental JSON flush.
"""
import json
import os
import time

import numpy as np

import spectral_zebrafish as sz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "spectral_results_zebrafish_condition.json")
# ZAPBench condition boundaries and names (zapbench/constants.py); pad 1 frame.
OFFSETS = (0, 649, 2422, 3078, 3735, 5047, 5638, 6623, 7279, 7879)
NAMES = ("gain", "dots", "flash", "taxis", "turning", "position",
         "cond6", "cond7", "cond8")
PAD = 1


def main():
    t0 = time.time()
    X = np.memmap(sz.MEMMAP, dtype=np.float32, mode="r",
                  shape=(sz.T_FULL, sz.N_FULL))
    Xr = np.asarray(X, np.float32)

    # pick the longest conditions (most timepoints for a within-condition test)
    conds = []
    for i in range(len(OFFSETS) - 1):
        a, b = OFFSETS[i] + PAD, OFFSETS[i + 1] - PAD
        conds.append((i, NAMES[i], a, b, b - a))
    conds.sort(key=lambda c: -c[4])
    chosen = conds[:3]                      # three longest single conditions
    print("chosen single conditions (idx,name,frames):",
          [(c[0], c[1], c[4]) for c in chosen], flush=True)

    out = dict(dataset="ZAPBench whole-brain zebrafish, single-condition control",
               note="within-condition saturation+CV; between-condition shared "
                    "stimulus drive removed", conditions=[], status="running")
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)

    for idx, name, a, b, L in chosen:
        print(f"\n=== condition {idx} '{name}': frames [{a},{b}) T={L} ===",
              flush=True)
        Z = sz.zscore_cols(Xr[a:b].astype(np.float64)).astype(np.float32)
        N = Z.shape[1]
        sizes = [s for s in [50, 100, 200, 500, 1000, 2000, 4000, 8000,
                             16000, 32000, 50000, N] if s <= N]

        def ndraw(n, N=N):
            if n >= 32000:
                return 1
            if n >= 8000:
                return 2
            if n >= 2000:
                return 3
            return 6

        curve = sz.subsample_pr(Z, sizes, np.random.default_rng(10), ndraw)
        cn = np.array([c[0] for c in curve], float)
        cp = np.array([c[1] for c in curve])
        up = cn >= 5000
        beta = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]) \
            if up.sum() >= 2 else float("nan")
        up2 = cn >= 16000
        beta_top = float(np.polyfit(np.log10(cn[up2]), np.log10(cp[up2]), 1)[0]) \
            if up2.sum() >= 2 else float("nan")
        pr_full = float(cp[-1])
        print(f"  PR full N={pr_full:.2f}  beta(>=5000)={beta:.4f}  "
              f"beta(>=16000)={beta_top:.4f}", flush=True)

        cvr = sz.cv_readouts_fullN(Z, np.random.default_rng(7), n_surr=6)
        print(f"  CV: n_cv_pos={cvr['n_cv_pos']}  nf_keff="
              f"{cvr['noise_free_keff']:.2f}  n>surr={cvr['n_above_surr']}  "
              f"alpha={cvr['alpha']:.3f}", flush=True)

        rec = dict(cond_idx=idx, name=name, frames=[a, b], T=L, N=N,
                   saturation_curve=[dict(Np=c[0], PR=c[1], PR_std=c[2],
                                          draws=c[3]) for c in curve],
                   beta_upper=beta, beta_topdecade=beta_top, PR_full_N=pr_full,
                   cv=dict(n_cv_pos=cvr["n_cv_pos"],
                           noise_free_keff=cvr["noise_free_keff"],
                           n_above_surr=cvr["n_above_surr"],
                           alpha=cvr["alpha"],
                           cv_top=cvr["cv_top"]))
        out["conditions"].append(rec)
        with open(OUT, "w") as f:
            json.dump(out, f, indent=1)
            f.flush()
            os.fsync(f.fileno())

    out["status"] = "done"
    out["runtime_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {OUT}  ({out['runtime_s']}s)", flush=True)


if __name__ == "__main__":
    main()
