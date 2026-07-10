#!/usr/bin/env python3
"""
Volume test for the B-total halo-grain crossing epoch.

MANDATE: does a LARGER box tighten the crossing-epoch scatter (single-box peak-z
range 0.33-1.36 on the 25 Mpc/h CV suite) and move it TOWARD or AWAY from DESI's
CPL crossing ~0.35?

INDEPENDENT LARGE BOX -- REACHABILITY (checked 2026-07-10, logged below):
  * Quijote (1 Gpc/h FoF): access is Globus OR Binder ONLY. The Globus HTTPS
    guest-collection host does not resolve from here (DNS 000); Binder redirects
    to an OAuth login wall (and needs a signup form). No anonymous HTTP endpoint.
  * CAMELS-SAM (100 Mpc/h): not present on the public Flatiron ~camels mirror
    (404 at every CAMELS-SAM path).
  * CAMELS IllustrisTNG L50n512 (50 Mpc/h, SAME mass resolution as CV): listed
    on the mirror but PERMISSION-BLOCKED (dir 403 "Permission denied", file 404).
  => No independent larger-volume catalog is reachable. Per the brief we do NOT
     fake a volume test.

WHAT WE CAN DO HONESTLY (real data, labelled for what it is):
  S_total = -ln det C is EXTENSIVE, and the correlation between halos in two
  DISJOINT comoving sub-volumes is ~0, so C over the union of N independent-phase
  boxes is block-diagonal and
        S_pooled(a) = sum_over_boxes S_box(a).
  This is EXACTLY what a region of N x (25 Mpc/h)^3 built from N independent
  25-Mpc/h sub-volumes would measure. Pooling the 6 CV boxes is therefore a
  genuine VOLUME increase in the sampling / shot-noise sense: it reduces the
  cosmic-variance scatter on the crossing epoch as ~1/sqrt(N_box).

  LIMIT (stated, not buried): pooling independent 25-Mpc/h boxes adds volume but
  NOT Fourier modes larger than 25 Mpc/h. A true 50-100 Mpc/h box carries
  large-scale power the pooled construction lacks; that could shift the epoch
  beyond what variance-reduction alone shows. So this bounds the
  VARIANCE-REDUCTION direction of the volume effect, not the large-mode
  systematic. It answers "does the epoch sharpen, and toward what value" -- not
  "is the sharpened value the final large-box truth".

Config = the ADDENDUM reference point (thr=1e11, R=1.0, cap=1000).
Output: appends 'volume_test' to results.json (must run after sweep.py), figure.
"""
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HG = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HG))
sys.path.insert(0, str(HG.parent))
import halo_grain as hg   # noqa: E402
import s_of_a as S        # noqa: E402

HERE = Path(__file__).resolve().parent
NBOX = 6
THR, R, CAP = 1e11, 1.0, 1000
DESI_CROSSING_Z = 0.35


def probe_reachability():
    """Record the HTTP status of each large-volume option (documentation)."""
    import urllib.request
    import urllib.error
    targets = {
        "CAMELS_L50n512_dir": "https://users.flatironinstitute.org/~camels/Sims/IllustrisTNG/L50n512/",
        "CAMELS_L50n512_file": "https://users.flatironinstitute.org/~camels/Sims/IllustrisTNG/L50n512/CV/CV_0/groups_090.hdf5",
        "CAMELS_SAM": "https://users.flatironinstitute.org/~camels/Sims/CAMELS-SAM/",
        "Quijote_binder": "https://binder.flatironinstitute.org/~fvillaescusa/Quijote/Halos/FoF/fiducial/0/",
    }
    log = {}
    for name, url in targets.items():
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=15) as resp:
                log[name] = dict(status=resp.status, url=url)
        except urllib.error.HTTPError as e:
            log[name] = dict(status=int(e.code), url=url)
        except Exception as e:
            log[name] = dict(status="unreachable", detail=repr(e)[:80], url=url)
    return log


def box_trajectory(ps, snaps):
    recs = hg.op_B(ps, snaps, THR, R_smooth=R, cap=CAP, n_draw=8)
    a = np.array([r["a"] for r in recs])
    Sv = np.array([r["S"] for r in recs])
    return a, Sv


def peak_and_wtoday(a, Sv):
    ok = np.isfinite(Sv) & (Sv > 0)
    a2, S2 = a[ok], Sv[ok]
    o = np.argsort(a2)
    a2, S2 = a2[o], S2[o]
    peak_a = a2[int(np.argmax(S2))]
    late = (np.log(S2[-1]) - np.log(S2[-2])) / (np.log(a2[-1]) - np.log(a2[-2]))
    return 1.0 / peak_a - 1.0, -1.0 - late / 3.0


def main():
    print("Volume test: reachability probe + pooled-volume convergence")
    reach = probe_reachability()
    for k, v in reach.items():
        print(f"  {k}: {v['status']}")

    print("\nComputing per-box reference trajectories (thr=1e11,R=1.0,cap=1000)...")
    ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
    # a-grid is identical across boxes (same snapshots); S per box aligned on it
    a_ref = None
    S_boxes = []
    for cv in range(NBOX):
        snaps = [hg.load_snapshot(s, cv=cv) for s in hg.SNAPS]
        a, Sv = box_trajectory(ps, snaps)
        if a_ref is None:
            a_ref = a
        S_boxes.append(Sv)
        pz, wt = peak_and_wtoday(a, Sv)
        print(f"  CV_{cv}: peak z={pz:.2f}  w_today={wt:+.3f}")
    S_boxes = np.array(S_boxes)          # (6, nsnap)

    # ---- pooled-volume convergence: S_pooled = sum over member boxes ----
    # For each N in {1,2,3,6}, enumerate box subsets, sum their S(a), extract
    # peak-z and w_today.  Scatter across subsets = cosmic variance at that volume.
    conv = {}
    for N in (1, 2, 3, 6):
        subsets = list(combinations(range(NBOX), N))
        pzs, wts = [], []
        for sub in subsets:
            Spool = S_boxes[list(sub)].sum(axis=0)
            pz, wt = peak_and_wtoday(a_ref, Spool)
            pzs.append(pz); wts.append(wt)
        pzs, wts = np.array(pzs), np.array(wts)
        conv[N] = dict(
            n_subsets=len(subsets),
            effective_volume_Mpc3=N * (hg.BOX ** 3),
            equiv_box_Mpc_h=round((N * hg.BOX ** 3) ** (1.0 / 3.0), 1),
            peak_z_mean=float(pzs.mean()), peak_z_std=float(pzs.std()),
            peak_z_min=float(pzs.min()), peak_z_max=float(pzs.max()),
            w_today_mean=float(wts.mean()), w_today_std=float(wts.std()),
        )
        print(f"  N={N} boxes (~{conv[N]['equiv_box_Mpc_h']} Mpc/h equiv): "
              f"peak z = {pzs.mean():.2f} +/- {pzs.std():.2f} "
              f"[{pzs.min():.2f},{pzs.max():.2f}]  w_today={wts.mean():+.3f}")

    # full 6-box pooled estimate (the tightest volume we can build)
    Spool6 = S_boxes.sum(axis=0)
    pz6, wt6 = peak_and_wtoday(a_ref, Spool6)

    # direction verdict: does peak-z move toward DESI 0.35 as volume grows?
    pz_single = conv[1]["peak_z_mean"]
    verdict = dict(
        single_box_peak_z_mean=round(pz_single, 3),
        single_box_peak_z_scatter=round(conv[1]["peak_z_std"], 3),
        single_box_peak_z_range=[round(conv[1]["peak_z_min"], 2), round(conv[1]["peak_z_max"], 2)],
        pooled6_peak_z=round(pz6, 3),
        pooled6_w_today=round(wt6, 3),
        scatter_shrinks_with_volume=bool(conv[6]["peak_z_std"] < conv[1]["peak_z_std"]),
        scatter_ratio_N6_over_N1=round(conv[6]["peak_z_std"] / max(conv[1]["peak_z_std"], 1e-9), 3),
        sqrtN_expectation=round(1.0 / np.sqrt(6), 3),
        moves_toward_desi=bool(abs(pz6 - DESI_CROSSING_Z) < abs(pz_single - DESI_CROSSING_Z)),
        desi_crossing_z=DESI_CROSSING_Z,
        note=("Pooled ~6x-volume estimate. Adds sampling volume (variance down "
              "~1/sqrt(N)) but NOT >25 Mpc/h modes; not an independent large box."),
    )
    print(f"\n  single-box peak z: {pz_single:.2f} +/- {conv[1]['peak_z_std']:.2f}"
          f"  ->  pooled 6-box: {pz6:.2f} (w_today {wt6:+.3f})")
    print(f"  scatter N6/N1 = {verdict['scatter_ratio_N6_over_N1']} "
          f"(1/sqrt6 = {verdict['sqrtN_expectation']}); "
          f"moves toward DESI 0.35: {verdict['moves_toward_desi']}")

    out = dict(reachability=reach, config=dict(thr=THR, R=R, cap=CAP),
               per_box_peak_z=[round(peak_and_wtoday(a_ref, S_boxes[i])[0], 3)
                               for i in range(NBOX)],
               convergence={str(k): v for k, v in conv.items()},
               verdict=verdict)

    # append to results.json
    rj = HERE / "results.json"
    if rj.exists():
        allres = json.load(open(rj))
    else:
        allres = {}
    allres["volume_test"] = out
    json.dump(allres, open(rj, "w"), indent=2)
    print(f"\nappended volume_test to {rj}")

    make_figure(conv, a_ref, S_boxes, Spool6, pz6)
    return out


def make_figure(conv, a_ref, S_boxes, Spool6, pz6):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    Ns = sorted(conv.keys())
    means = [conv[N]["peak_z_mean"] for N in Ns]
    stds = [conv[N]["peak_z_std"] for N in Ns]
    equiv = [conv[N]["equiv_box_Mpc_h"] for N in Ns]
    ax[0].errorbar(equiv, means, yerr=stds, fmt="o-", color="navy", capsize=3,
                   label="pooled peak z (mean +/- cosmic variance)")
    ax[0].axhline(DESI_CROSSING_Z, color="crimson", ls=":", label="DESI crossing ~0.35")
    ax[0].set_xlabel("effective box size [Mpc/h]  (N x 25^3)^(1/3)")
    ax[0].set_ylabel("B-total crossing epoch  z")
    ax[0].set_title("Does the epoch sharpen with volume?")
    ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)
    # scatter vs 1/sqrtN
    ax[1].plot(Ns, stds, "o-", color="navy", label="measured peak-z scatter")
    s1 = conv[1]["peak_z_std"]
    ax[1].plot(Ns, [s1 / np.sqrt(N) for N in Ns], "--", color="gray",
               label="1/sqrt(N) from N=1")
    ax[1].set_xlabel("N boxes pooled"); ax[1].set_ylabel("peak-z scatter")
    ax[1].set_title("Cosmic-variance reduction with volume")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HERE / "figures/fig_volume_convergence.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()
