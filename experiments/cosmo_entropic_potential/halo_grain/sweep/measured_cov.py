#!/usr/bin/env python3
"""
Measured-covariance variant (direction-of-effect check, one config).

The B-total headline builds C from a MODELED matter correlation xi_R(r_ij)
evaluated at real halo positions (PSD-safe, but model-ial). Question: if we
replace that with a covariance MEASURED from the halo field itself, does the
S(a) trajectory keep the same shape (rise-then-peak)?

Construction (as the brief specifies):
  * Coarse-grid the halo field (counts above threshold) into n^3 FIXED comoving
    cells, per snapshot, per box -> overdensity vector delta (length Ncell).
  * Treat the 6 CV boxes as 6 REALIZATIONS. Estimate the Ncell x Ncell cell-cell
    covariance across the 6 boxes at each snapshot. This is a small-sample problem
    (6 realizations << Ncell), so we regularize with Ledoit-Wolf linear shrinkage
    toward the diagonal and REPORT the shrinkage intensity delta per snapshot.
  * C = shrunk CORRELATION matrix; S(a) = -ln det C. Track the trajectory shape.

WHAT THIS IS / IS NOT (labelled):
  * This is a FIXED-dimension measure (Ncell constant across snapshots), so it
    probes the same channel as op_A (fixed units), NOT the extensive B-total
    k-growth channel. It cannot reproduce the k-driven amplitude of B-total.
  * Its job is narrow: does swapping MODEL-xi for MEASURED covariance change the
    DIRECTION (sign of dlnS/dlna, presence of an interior peak)? Direction only.
  * 6 realizations is a very small ensemble; shrinkage does heavy lifting. The
    magnitude of S is not interpretable, only the trajectory shape/sign.

Config: threshold 1e11, n_side=3 (27 cells) headline, n_side=4 (64) cross-check.
Output: appends 'measured_cov' to results.json; figure.
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.covariance import LedoitWolf

HG = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HG))
sys.path.insert(0, str(HG.parent))
import halo_grain as hg   # noqa: E402
import s_of_a as S        # noqa: E402

HERE = Path(__file__).resolve().parent
NBOX = 6
THR = 1e11


def coarse_field(pos, n_side, box):
    """Halo-count overdensity delta = N/mean - 1 in n^3 fixed comoving cells."""
    edges = np.linspace(0.0, box, n_side + 1)
    ix = np.clip(np.digitize(pos[:, 0], edges) - 1, 0, n_side - 1)
    iy = np.clip(np.digitize(pos[:, 1], edges) - 1, 0, n_side - 1)
    iz = np.clip(np.digitize(pos[:, 2], edges) - 1, 0, n_side - 1)
    flat = (ix * n_side + iy) * n_side + iz
    cnt = np.bincount(flat, minlength=n_side ** 3).astype(float)
    mean = cnt.mean()
    return cnt / mean - 1.0 if mean > 0 else cnt


def measured_S_trajectory(boxes_snaps, n_side):
    """S(a) from Ledoit-Wolf-shrunk measured cell covariance across the 6 boxes."""
    box = hg.BOX
    nsnap = len(hg.SNAPS)
    recs = []
    for si in range(nsnap):
        # 6-realization field matrix X: (6, Ncell)
        X = np.array([coarse_field(bs[si]["pos"][bs[si]["m200"] > THR], n_side, box)
                      for bs in boxes_snaps])
        a = boxes_snaps[0][si]["a"]
        z = boxes_snaps[0][si]["z"]
        # standardize columns (unit-variance) so shrinkage target = diagonal/identity
        mu = X.mean(0)
        sd = X.std(0, ddof=1)
        sd[sd < 1e-12] = 1e-12
        Xs = (X - mu) / sd
        lw = LedoitWolf(assume_centered=True).fit(Xs)
        C = lw.covariance_.copy()
        d = np.sqrt(np.diag(C))
        C = C / np.outer(d, d)          # -> correlation matrix, unit diagonal
        ev = np.linalg.eigvalsh(C)
        ev = np.clip(ev, 1e-12, None)
        S_val = float(-np.log(ev).sum())
        recs.append(dict(a=float(a), z=float(z), S=S_val,
                         shrinkage=float(lw.shrinkage_),
                         min_eig=float(ev.min()), cond=float(ev.max() / ev.min())))
    return recs


def slope_and_peak(recs):
    a = np.array([r["a"] for r in recs])
    Sv = np.array([r["S"] for r in recs])
    o = np.argsort(a)
    a, Sv = a[o], Sv[o]
    gslope = float(np.polyfit(np.log(a), np.log(Sv), 1)[0])
    late = (np.log(Sv[-1]) - np.log(Sv[-2])) / (np.log(a[-1]) - np.log(a[-2]))
    peak_a = a[int(np.argmax(Sv))]
    return dict(global_slope=gslope, w_global=-1 - gslope / 3,
                w_today=-1 - late / 3,
                peak_z=float(1 / peak_a - 1), interior_peak=bool(peak_a < 0.999),
                S_rises_globally=bool(gslope > 0))


def main():
    print("Measured-covariance variant (Ledoit-Wolf shrinkage across 6 boxes)")
    boxes_snaps = [[hg.load_snapshot(s, cv=cv) for s in hg.SNAPS] for cv in range(NBOX)]

    out = dict(config=dict(threshold=THR, n_realizations=NBOX,
                           estimator="Ledoit-Wolf linear shrinkage -> correlation"),
               variants={})
    for n_side in (3, 4):
        recs = measured_S_trajectory(boxes_snaps, n_side)
        sp = slope_and_peak(recs)
        deltas = [r["shrinkage"] for r in recs]
        out["variants"][f"n_side_{n_side}"] = dict(
            n_cells=n_side ** 3, records=recs,
            shrinkage_mean=float(np.mean(deltas)),
            shrinkage_range=[float(min(deltas)), float(max(deltas))],
            **sp)
        print(f"  n_side={n_side} ({n_side**3} cells): "
              f"global slope={sp['global_slope']:+.3f} (w={sp['w_global']:+.3f}), "
              f"S rises={sp['S_rises_globally']}, interior peak={sp['interior_peak']} "
              f"(z={sp['peak_z']:.2f}), shrinkage delta in "
              f"[{min(deltas):.2f},{max(deltas):.2f}]")

    head = out["variants"]["n_side_3"]
    out["direction_verdict"] = (
        f"Measured covariance (n_side=3, delta~{head['shrinkage_mean']:.2f}): "
        f"S {'RISES' if head['S_rises_globally'] else 'FALLS'} globally "
        f"(w_global={head['w_global']:+.3f}); interior peak "
        f"{'present' if head['interior_peak'] else 'absent'}. "
        "Fixed-dimension measure (op_A-like), so it cannot show the extensive "
        "B-total k-growth; it checks only whether MEASURED vs MODEL-xi flips the "
        "sign. Small ensemble (6) -> shrinkage dominant; magnitude not interpretable.")
    print("\n  " + out["direction_verdict"])

    rj = HERE / "results.json"
    allres = json.load(open(rj)) if rj.exists() else {}
    allres["measured_cov"] = out
    json.dump(allres, open(rj, "w"), indent=2)
    print(f"\nappended measured_cov to {rj}")

    # figure
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for n_side in (3, 4):
        recs = out["variants"][f"n_side_{n_side}"]["records"]
        z = [r["z"] for r in recs]; Sv = [r["S"] for r in recs]
        dl = [r["shrinkage"] for r in recs]
        ax[0].plot(z, Sv, "o-", label=f"n_side={n_side} ({n_side**3} cells)")
        ax[1].plot(z, dl, "s-", label=f"n_side={n_side}")
    ax[0].set_xlabel("z"); ax[0].set_ylabel("S = -ln det C (measured, shrunk)")
    ax[0].invert_xaxis(); ax[0].legend(); ax[0].grid(alpha=0.3)
    ax[0].set_title("Measured-covariance S(z) [fixed grid]")
    ax[1].set_xlabel("z"); ax[1].set_ylabel("Ledoit-Wolf shrinkage delta")
    ax[1].invert_xaxis(); ax[1].legend(); ax[1].grid(alpha=0.3)
    ax[1].set_title("Shrinkage intensity per snapshot")
    fig.tight_layout()
    fig.savefig(HERE / "figures/fig_measured_cov.png", dpi=110)
    plt.close(fig)
    return out


if __name__ == "__main__":
    main()
