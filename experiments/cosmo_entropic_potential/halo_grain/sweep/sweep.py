#!/usr/bin/env python3
"""
Sensitivity sweep of the B-total halo-grain S(a) result over the FREE CHOICES.

The ADDENDUM headline (w_today = -0.841 +/- 0.050, DESI w0 = -0.838; interior S
peak 6/6 boxes) was measured at ONE point in a choice space: mass threshold 1e11
Msun/h, R_smooth = 1.0 Mpc/h, cap = 1000, on the CAMELS CV 25 Mpc/h suite.  This
script varies those choices on a grid and reports how far w_today and the peak
epoch move -- the honest spread, "w_today in [x,y] robustly", and whether the
qualitative DESI shape (interior peak, w>-1 today) survives everywhere or only in
a corner.

Exact same code path as halo_grain.op_B (B-total; k grows).  Nothing tuned.

Grid:
  mass threshold : {5e10, 1e11, 3e11, 1e12}   Msun/h on M200c
  R_smooth       : {0.5, 1.0, 2.0}            Mpc/h
  cap            : {500, 1000}                numerical cap on halos
Over all 6 CAMELS CV boxes (independent-phase), 10 snapshots z=3->0.

Outputs: results.json (this dir), figures/*.png.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HG = Path(__file__).resolve().parent.parent            # .../halo_grain
sys.path.insert(0, str(HG))
sys.path.insert(0, str(HG.parent))                      # .../cosmo_entropic_potential
import halo_grain as hg          # noqa: E402
import s_of_a as S               # noqa: E402

HERE = Path(__file__).resolve().parent
NBOX = 6
THRESHOLDS = [5e10, 1e11, 3e11, 1e12]
R_SMOOTHS = [0.5, 1.0, 2.0]
CAPS = [500, 1000]
DESI_W0 = -0.838

# reference config = the ADDENDUM headline point
REF = dict(thr=1e11, R=1.0, cap=1000)


def w_today_from_trajectory(av, Sa):
    """Late-time log-slope -> w_today under 1+w = -(1/3) dlnS/dlna.
    Uses the last two (a-ordered, finite, positive-S) points, matching
    btotal_multibox.py exactly."""
    ok = np.isfinite(Sa) & (Sa > 0)
    av, Sa = av[ok], Sa[ok]
    order = np.argsort(av)
    av, Sa = av[order], Sa[order]
    if len(av) < 3:
        return np.nan, np.nan, np.nan
    late = (np.log(Sa[-1]) - np.log(Sa[-2])) / (np.log(av[-1]) - np.log(av[-2]))
    w_today = -1.0 - late / 3.0
    peak_a = av[int(np.argmax(Sa))]
    return w_today, peak_a, float(Sa[-1] / Sa.max())


def run_cell(ps, boxes_snaps, thr, R, cap):
    """One grid cell over all boxes.  Returns per-box (w_today, peak_a, S_end/S_peak)
    and the trajectories (for the reference figure)."""
    per_box = []
    trajectories = []
    for snaps in boxes_snaps:
        recs = hg.op_B(ps, snaps, thr, R_smooth=R, cap=cap, n_draw=8)
        av = np.array([r["a"] for r in recs])
        Sa = np.array([r["S"] for r in recs])
        kk = np.array([r["k"] for r in recs])
        w_t, peak_a, ratio = w_today_from_trajectory(av, Sa)
        per_box.append(dict(w_today=w_t, peak_a=peak_a, s_end_over_peak=ratio,
                            k_z3=int(kk[0]), k_z0=int(kk[-1])))
        trajectories.append(dict(a=av.tolist(), S=Sa.tolist(), k=kk.tolist()))
    return per_box, trajectories


def summarize_cell(per_box):
    w = np.array([b["w_today"] for b in per_box], float)
    pk = np.array([b["peak_a"] for b in per_box], float)
    wok = w[np.isfinite(w)]
    pkok = pk[np.isfinite(pk)]
    interior = pkok < 0.999            # peak not at a=1 (today)
    peak_z = 1.0 / pkok - 1.0
    return dict(
        n_boxes=int(np.isfinite(w).sum()),
        w_today_mean=float(wok.mean()) if len(wok) else np.nan,
        w_today_std=float(wok.std()) if len(wok) else np.nan,
        w_today_min=float(wok.min()) if len(wok) else np.nan,
        w_today_max=float(wok.max()) if len(wok) else np.nan,
        w_today_gt_minus1_frac=float((wok > -1).mean()) if len(wok) else np.nan,
        interior_peak_frac=float(interior.mean()) if len(pkok) else np.nan,
        interior_peak_count=int(interior.sum()),
        peak_z_median=float(np.median(peak_z[peak_z > 1e-6])) if (peak_z > 1e-6).any() else np.nan,
        peak_z_min=float(peak_z.min()) if len(peak_z) else np.nan,
        peak_z_max=float(peak_z.max()) if len(peak_z) else np.nan,
        per_box_w_today=[round(float(x), 3) if np.isfinite(x) else None for x in w],
        per_box_peak_z=[round(float(1.0 / p - 1.0), 3) if np.isfinite(p) else None for p in pk],
    )


def main():
    t0 = time.time()
    print("Loading 6 CAMELS CV boxes (cached fields)...")
    boxes_snaps = [[hg.load_snapshot(s, cv=cv) for s in hg.SNAPS] for cv in range(NBOX)]
    ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)

    results = dict(
        description="B-total halo-grain S(a) sensitivity sweep over free choices",
        data="CAMELS IllustrisTNG CV_0..CV_5, 25 Mpc/h, 10 snaps z=3->0 (cached)",
        cosmology=dict(Om=S.OM, OL=S.OL, h=S.H0H, ns=S.NS, sigma8=S.SIGMA8),
        sign_law="1 + w(a) = -(1/3) dlnS/dlna",
        desi_w0=DESI_W0,
        reference_config=REF,
        grid=dict(threshold=THRESHOLDS, R_smooth=R_SMOOTHS, cap=CAPS),
        cells=[],
    )

    ref_trajs = None
    for thr in THRESHOLDS:
        for R in R_SMOOTHS:
            for cap in CAPS:
                tc = time.time()
                per_box, trajs = run_cell(ps, boxes_snaps, thr, R, cap)
                summ = summarize_cell(per_box)
                cell = dict(threshold=thr, R_smooth=R, cap=cap, **summ)
                results["cells"].append(cell)
                if abs(thr - REF["thr"]) < 1 and R == REF["R"] and cap == REF["cap"]:
                    ref_trajs = trajs
                    results["reference_cell"] = cell
                print(f"thr={thr:.0e} R={R:<3} cap={cap:<4}  "
                      f"w_today={summ['w_today_mean']:+.3f}+/-{summ['w_today_std']:.3f}  "
                      f"interior_peak={summ['interior_peak_count']}/6  "
                      f"peak_z_med={summ['peak_z_median']:.2f}  ({time.time()-tc:.1f}s)")

    # ---- honest spread across the WHOLE grid ----
    wm = np.array([c["w_today_mean"] for c in results["cells"]], float)
    ip = np.array([c["interior_peak_frac"] for c in results["cells"]], float)
    n_cells = len(results["cells"])
    results["spread"] = dict(
        n_cells=n_cells,
        w_today_mean_over_grid=float(np.nanmean(wm)),
        w_today_range=[float(np.nanmin(wm)), float(np.nanmax(wm))],
        cells_with_w_gt_minus1=int(np.sum(wm > -1)),
        interior_peak_survives_frac=float(np.nanmean(ip)),
        cells_all6_interior=int(np.sum(ip >= 0.999)),
        cells_majority_interior=int(np.sum(ip >= 0.5)),
    )

    # ---- biggest mover: marginal effect of each free choice on w_today_mean ----
    def marginal(param, values):
        means = []
        for v in values:
            sub = [c["w_today_mean"] for c in results["cells"]
                   if (abs(c[param] - v) < max(1e-30, 1e-6 * abs(v)))
                   and np.isfinite(c["w_today_mean"])]
            means.append(np.mean(sub) if sub else np.nan)
        means = np.array(means)
        return dict(values=[float(v) for v in values],
                    w_today_by_value=[round(float(m), 3) for m in means],
                    span=float(np.nanmax(means) - np.nanmin(means)))
    movers = dict(
        threshold=marginal("threshold", THRESHOLDS),
        R_smooth=marginal("R_smooth", R_SMOOTHS),
        cap=marginal("cap", CAPS),
    )
    movers_ranked = sorted(movers.items(), key=lambda kv: -kv[1]["span"])
    results["biggest_mover"] = dict(
        ranking=[dict(param=k, span=round(v["span"], 3)) for k, v in movers_ranked],
        detail=movers,
    )

    with open(HERE / "results.json", "w") as f:
        json.dump(_san(results), f, indent=2)
    print(f"\nwrote {HERE/'results.json'}  ({time.time()-t0:.0f}s total)")

    make_figures(results, ref_trajs)
    print_report(results)
    return results


def _san(o):
    if isinstance(o, dict):
        return {k: _san(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_san(x) for x in o]
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o


def make_figures(results, ref_trajs):
    cells = results["cells"]
    # Fig 1: w_today across the grid (heatmap-ish, faceted by cap)
    fig, axes = plt.subplots(1, len(CAPS), figsize=(11, 4.4), sharey=True)
    for ci, cap in enumerate(CAPS):
        ax = axes[ci]
        M = np.full((len(THRESHOLDS), len(R_SMOOTHS)), np.nan)
        for c in cells:
            if c["cap"] != cap:
                continue
            i = THRESHOLDS.index(c["threshold"])
            j = R_SMOOTHS.index(c["R_smooth"])
            M[i, j] = c["w_today_mean"]
        im = ax.imshow(M, aspect="auto", cmap="RdBu_r", vmin=-1.1, vmax=-0.6,
                       origin="lower")
        ax.set_xticks(range(len(R_SMOOTHS)))
        ax.set_xticklabels([str(r) for r in R_SMOOTHS])
        ax.set_yticks(range(len(THRESHOLDS)))
        ax.set_yticklabels([f"{t:.0e}" for t in THRESHOLDS])
        ax.set_xlabel("R_smooth [Mpc/h]")
        if ci == 0:
            ax.set_ylabel("mass threshold [Msun/h]")
        ax.set_title(f"cap={cap}")
        for i in range(len(THRESHOLDS)):
            for j in range(len(R_SMOOTHS)):
                if np.isfinite(M[i, j]):
                    ax.text(j, i, f"{M[i,j]:+.2f}", ha="center", va="center",
                            fontsize=8, color="k")
    fig.colorbar(im, ax=axes, label="mean w_today", fraction=0.046)
    fig.suptitle(f"Sensitivity of w_today (DESI w0={DESI_W0}); "
                 f"grid mean {results['spread']['w_today_mean_over_grid']:+.3f}")
    fig.savefig(HERE / "figures/fig_w_today_grid.png", dpi=110,
                bbox_inches="tight")
    plt.close(fig)

    # Fig 2: interior-peak survival + peak-z across grid
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    labels = [f"{c['threshold']:.0e}\nR{c['R_smooth']} c{c['cap']}" for c in cells]
    ipc = [c["interior_peak_count"] for c in cells]
    ax[0].bar(range(len(cells)), ipc, color="steelblue")
    ax[0].axhline(6, color="green", ls="--", lw=1, label="all 6 boxes")
    ax[0].set_ylabel("boxes with interior S peak (/6)")
    ax[0].set_xticks(range(len(cells)))
    ax[0].set_xticklabels(labels, rotation=90, fontsize=5)
    ax[0].legend(); ax[0].set_title("Interior-peak survival across grid")
    ax[0].grid(alpha=0.3, axis="y")
    pz = [c["peak_z_median"] for c in cells]
    pzlo = [c["peak_z_median"] - c["peak_z_min"] if np.isfinite(c["peak_z_median"]) else 0 for c in cells]
    pzhi = [c["peak_z_max"] - c["peak_z_median"] if np.isfinite(c["peak_z_median"]) else 0 for c in cells]
    ax[1].errorbar(range(len(cells)), pz, yerr=[pzlo, pzhi], fmt="o",
                   color="crimson", ms=4, capsize=2)
    ax[1].axhline(0.35, color="k", ls=":", label="DESI CPL crossing ~0.35")
    ax[1].set_ylabel("peak z (median, box range)")
    ax[1].set_xticks(range(len(cells)))
    ax[1].set_xticklabels(labels, rotation=90, fontsize=5)
    ax[1].legend(); ax[1].set_title("Peak epoch across grid")
    ax[1].grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(HERE / "figures/fig_peak_survival.png", dpi=110)
    plt.close(fig)

    # Fig 3: reference-config S(a) trajectories, all 6 boxes
    if ref_trajs is not None:
        fig, ax = plt.subplots(figsize=(6.5, 4.6))
        for cv, tr in enumerate(ref_trajs):
            a = np.array(tr["a"]); Sv = np.array(tr["S"])
            ok = np.isfinite(Sv)
            ax.plot(1 / a[ok] - 1, Sv[ok], "o-", ms=3, label=f"CV_{cv}", alpha=0.8)
        ax.set_xlabel("z"); ax.set_ylabel("S_total = -ln det C")
        ax.invert_xaxis()
        ax.set_title(f"Reference config (thr={REF['thr']:.0e}, R={REF['R']}, "
                     f"cap={REF['cap']}): B-total S(z)")
        ax.legend(fontsize=7); ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(HERE / "figures/fig_reference_trajectories.png", dpi=110)
        plt.close(fig)


def print_report(results):
    print("\n=== SENSITIVITY SWEEP REPORT ===")
    sp = results["spread"]
    print(f"grid cells: {sp['n_cells']}")
    print(f"w_today range across grid: [{sp['w_today_range'][0]:+.3f}, "
          f"{sp['w_today_range'][1]:+.3f}]  (grid mean {sp['w_today_mean_over_grid']:+.3f})")
    print(f"cells with w_today>-1 (non-phantom today): "
          f"{sp['cells_with_w_gt_minus1']}/{sp['n_cells']}")
    print(f"interior peak: all-6-boxes in {sp['cells_all6_interior']}/{sp['n_cells']} "
          f"cells, majority in {sp['cells_majority_interior']}/{sp['n_cells']}")
    print("\nbiggest mover (span of mean w_today):")
    for r in results["biggest_mover"]["ranking"]:
        print(f"  {r['param']:10s} span={r['span']:.3f}")


if __name__ == "__main__":
    main()
