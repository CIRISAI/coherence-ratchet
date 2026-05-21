"""
Allen Brain Observatory corridor test — Claims 1 & 4, real neural data.
========================================================================

StructuralClaims.lean Claim 1 (the corridor is a bounded interior attractor at
every coordinated substrate — off rigidity rho->1, off chaos rho->0) and
Claim 4 (it recurs at every coordinated rung). A mouse visual cortex IS a
coordinated rung, so the corridor IS expected here if Claims 1 & 4 hold.

Substrate: Allen Brain Observatory, mouse visual cortex, two-photon calcium
imaging. One imaging session = one rung instance; its simultaneously-recorded
neurons (ROIs) = the constituents. Within-rung rho = mean off-diagonal
|Pearson correlation| of the dF/F traces on the SPONTANEOUS epoch (grey
screen, no stimulus) so the correlation is intrinsic coordination, not a
shared stimulus drive.

Confound controls (pre-registered in PREREGISTRATION.md):
  - finite-sample noise floor: circular-time-shift shuffle baseline, debias
    in quadrature (E1's method, circular shift because calcium is
    autocorrelated; plain permutation would understate the floor).
  - neuropil: Allen dF/F is already neuropil-subtracted; also run the test on
    the detected-events traces (neuropil-insensitive) as a cross-check.
  - session/area heterogeneity: rho reported per session with covariates;
    recurrence tested per area, not pooled.

FALSIFIER: sessions pinned at a pole (debiased rho > 0.90 or < 0.03), or no
bounded band at all. Reported as a partial falsification of Claims 1 & 4 if so.

Independent of the framework's existing neural result (C. elegans whole-brain
calcium, within-class bands rho ~ 0.25-0.75).

Run with the Python 3.10 venv that has allensdk:  /tmp/allenenv/bin/python
"""
import json
import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")

from allensdk.core.brain_observatory_cache import BrainObservatoryCache

MANIFEST = "/tmp/allen_data/boc/manifest.json"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

# corridor band, pre-registered. poles are the falsifier-relevant thresholds.
RIGIDITY_POLE = 0.90
CHAOS_POLE = 0.03
MIN_ROIS = 10            # too few constituents to define a within-rung corr
N_PER_AREA = 8           # sessions per cortical area
AREAS = ["VISp", "VISl", "VISpm", "VISal"]
SESSION_TYPE = "three_session_A"   # carries a spontaneous (grey-screen) epoch


def mean_abs_offdiag(C):
    d = C.shape[0]
    return float(np.mean(np.abs(C[~np.eye(d, dtype=bool)])))


def participation_ratio(X):
    """Effective dimensionality of the neuron x neuron covariance:
    k_eff = (sum lambda)^2 / sum lambda^2, lambda the covariance eigenvalues."""
    C = np.cov(X)
    w = np.linalg.eigvalsh(C)
    w = np.clip(w, 0, None)
    s = w.sum()
    if s <= 0:
        return float("nan")
    return float(s * s / np.sum(w * w))


def session_rho(traces, rng, n_shuffle=20):
    """Within-rung rho on a (neurons x frames) trace block.
    Returns (raw, noise_floor, debiased, k_eff, n_neurons, n_frames).

    raw      : mean |Pearson corr| over neuron pairs.
    floor    : same statistic after independently circular-shifting each
               neuron's trace by a random lag (kills cross-neuron correlation,
               keeps each neuron's autocorrelation and amplitude).
    debiased : sqrt(max(raw^2 - floor^2, 0)) -- genuine correlation above the
               finite-sample / autocorrelation noise floor.
    """
    X = np.asarray(traces, dtype=np.float64)
    # drop flat neurons (no variance -> undefined correlation)
    sd = X.std(axis=1)
    X = X[sd > 1e-9]
    n, T = X.shape
    if n < MIN_ROIS:
        return None
    Xz = (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True)
    C = (Xz @ Xz.T) / T
    raw = mean_abs_offdiag(C)
    keff = participation_ratio(X)
    floors = []
    for _ in range(n_shuffle):
        Xs = np.empty_like(Xz)
        for j in range(n):
            lag = rng.integers(1, T)
            Xs[j] = np.roll(Xz[j], lag)
        Cs = (Xs @ Xs.T) / T
        floors.append(mean_abs_offdiag(Cs))
    floor = float(np.mean(floors))
    floor_sd = float(np.std(floors))
    debiased = float(np.sqrt(max(raw ** 2 - floor ** 2, 0.0)))
    return dict(raw=raw, floor=floor, floor_sd=floor_sd, debiased=debiased,
                k_eff=keff, n_neurons=int(n), n_frames=int(T))


def main():
    print("=" * 78)
    print("Allen Brain Observatory corridor test -- Claims 1 & 4 (real neural data)")
    print("=" * 78)
    boc = BrainObservatoryCache(manifest_file=MANIFEST)
    rng = np.random.default_rng(0)

    # pick sessions: N_PER_AREA per area, session type with a spontaneous epoch
    targets = []
    for area in AREAS:
        exps = boc.get_ophys_experiments(targeted_structures=[area],
                                         session_types=[SESSION_TYPE])
        for e in exps[:N_PER_AREA]:
            targets.append(e)
    print(f"  selected {len(targets)} sessions across {len(AREAS)} areas, "
          f"type {SESSION_TYPE}")

    results = []
    for i, e in enumerate(targets):
        sid = e["id"]
        area = e["targeted_structure"]
        try:
            ds = boc.get_ophys_experiment_data(sid)
            ts, dff = ds.get_dff_traces()
            spont = ds.get_stimulus_table("spontaneous")
            # spontaneous epoch (grey screen) -- intrinsic coordination
            seg = max(((r.start, r.end) for r in spont.itertuples()),
                      key=lambda ab: ab[1] - ab[0])
            s0, s1 = int(seg[0]), int(seg[1])
            dff_spont = dff[:, s0:s1]
            r_dff = session_rho(dff_spont, rng)

            # neuropil cross-check: detected events on the same epoch
            r_ev = None
            try:
                ev = boc.get_ophys_experiment_events(sid)
                r_ev = session_rho(ev[:, s0:s1], rng)
            except Exception as ee:
                r_ev = {"error": f"{type(ee).__name__}"}

            if r_dff is None:
                print(f"  [{i+1:2d}/{len(targets)}] {sid} {area:6s}  EXCLUDED "
                      f"(< {MIN_ROIS} valid ROIs)")
                results.append(dict(id=sid, area=area, cre_line=e["cre_line"],
                                    imaging_depth=e["imaging_depth"],
                                    excluded="too_few_rois"))
                continue
            rec = dict(id=sid, area=area, cre_line=e["cre_line"],
                       imaging_depth=e["imaging_depth"],
                       spont_frames=s1 - s0, dff=r_dff, events=r_ev)
            results.append(rec)
            ev_db = (f"{r_ev['debiased']:.3f}"
                     if isinstance(r_ev, dict) and "debiased" in r_ev else "n/a")
            print(f"  [{i+1:2d}/{len(targets)}] {sid} {area:6s} "
                  f"n={r_dff['n_neurons']:3d}  raw={r_dff['raw']:.3f} "
                  f"floor={r_dff['floor']:.3f}  DEBIASED rho={r_dff['debiased']:.3f}"
                  f"  k_eff={r_dff['k_eff']:.2f}  (events rho={ev_db})")
        except Exception as ex:
            print(f"  [{i+1:2d}/{len(targets)}] {sid} {area:6s}  FAILED: "
                  f"{type(ex).__name__}: {str(ex)[:70]}")
            results.append(dict(id=sid, area=area, failed=str(ex)[:120]))

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  wrote {OUT}")

    analyse(results)


def analyse(results):
    ok = [r for r in results if "dff" in r and isinstance(r["dff"], dict)]
    print()
    print("=" * 78)
    print("READING")
    print("=" * 78)
    if not ok:
        print("  No session yielded a valid within-rung rho -- test could not run.")
        return
    deb = np.array([r["dff"]["debiased"] for r in ok])
    raw = np.array([r["dff"]["raw"] for r in ok])
    floor = np.array([r["dff"]["floor"] for r in ok])
    keff = np.array([r["dff"]["k_eff"] for r in ok])
    nn = np.array([r["dff"]["n_neurons"] for r in ok])

    q1, med, q3 = np.percentile(deb, [25, 50, 75])
    iqr = q3 - q1
    at_rigid = int(np.sum(deb > RIGIDITY_POLE))
    at_chaos = int(np.sum(deb < CHAOS_POLE))
    interior = (q1 > CHAOS_POLE) and (q3 < RIGIDITY_POLE)

    print(f"  {len(ok)} sessions with a valid within-rung rho "
          f"(of {len(results)} attempted).")
    print(f"  neuron counts n: [{nn.min()}, {nn.max()}], median {int(np.median(nn))}.")
    print(f"  raw mean|corr|:   [{raw.min():.3f}, {raw.max():.3f}], "
          f"mean {raw.mean():.3f}")
    print(f"  noise floor:      [{floor.min():.3f}, {floor.max():.3f}], "
          f"mean {floor.mean():.3f}  (circular-shift shuffle baseline)")
    print(f"  DEBIASED rho:     [{deb.min():.3f}, {deb.max():.3f}], "
          f"median {med:.3f}, IQR [{q1:.3f}, {q3:.3f}] width {iqr:.3f}")
    print(f"  k_eff (partic.):  [{keff.min():.2f}, {keff.max():.2f}], "
          f"median {np.median(keff):.2f}")
    print(f"  at rigidity pole (debiased>{RIGIDITY_POLE}): {at_rigid}/{len(ok)}; "
          f"at chaos pole (<{CHAOS_POLE}): {at_chaos}/{len(ok)}")
    print()

    # per-area recurrence (Claim 4)
    print("  PER-AREA (Claim 4 -- recurrence):")
    areas = sorted(set(r["area"] for r in ok))
    area_meds = {}
    for a in areas:
        d = np.array([r["dff"]["debiased"] for r in ok if r["area"] == a])
        area_meds[a] = np.median(d)
        print(f"    {a:7s} n_sess={len(d):2d}  debiased rho "
              f"[{d.min():.3f}, {d.max():.3f}]  median {np.median(d):.3f}")
    area_spread = max(area_meds.values()) - min(area_meds.values())
    print(f"    spread of per-area medians: {area_spread:.3f}")
    print()

    # neuropil cross-check
    ev_ok = [r for r in ok if isinstance(r.get("events"), dict)
             and "debiased" in r["events"]]
    if ev_ok:
        ev_deb = np.array([r["events"]["debiased"] for r in ev_ok])
        dff_deb_match = np.array([r["dff"]["debiased"] for r in ev_ok])
        print(f"  NEUROPIL CROSS-CHECK ({len(ev_ok)} sessions with events):")
        print(f"    dF/F debiased rho   median {np.median(dff_deb_match):.3f}")
        print(f"    events debiased rho median {np.median(ev_deb):.3f}")
        ratio = np.median(ev_deb) / max(np.median(dff_deb_match), 1e-9)
        print(f"    events/dF/F ratio {ratio:.2f}  -- if << 1, the dF/F signal")
        print(f"    is neuropil-inflated; if ~comparable, it is genuine.")
        print()

    # verdict (pre-registered ladder)
    print("  VERDICT (pre-registered ladder in PREREGISTRATION.md):")
    pole_frac = (at_rigid + at_chaos) / len(ok)
    if pole_frac >= 0.20:
        print(f"    FALSIFIER: {at_rigid+at_chaos}/{len(ok)} sessions pinned at a")
        print(f"    pole (>= 20%). Partial falsification of Claims 1 & 4 at the")
        print(f"    neural substrate.")
    elif interior and iqr <= 0.25 and area_spread <= 0.15:
        print(f"    CONFIRMED: no pole pile-up; debiased rho forms a bounded")
        print(f"    interior band (IQR width {iqr:.3f} <= 0.25, both quartiles")
        print(f"    interior) that recurs across {len(areas)} cortical areas")
        print(f"    (per-area median spread {area_spread:.3f} <= 0.15).")
    elif at_rigid == 0 and at_chaos == 0:
        print(f"    WEAKLY SUPPORTED: off both poles (0 sessions at either),")
        print(f"    but the band is not tight enough for a clean confirmation")
        print(f"    (IQR width {iqr:.3f}, area-median spread {area_spread:.3f}).")
    else:
        print(f"    NULL / NO CLEAN CORRIDOR: some pole occupancy or no bounded")
        print(f"    band. {at_rigid+at_chaos}/{len(ok)} at a pole, IQR {iqr:.3f}.")
    print()
    print(f"  Scope: {len(ok)} sessions, {SESSION_TYPE}, spontaneous (grey-screen)")
    print(f"  epoch only. rho = mean |Pearson corr| of neuropil-subtracted dF/F,")
    print(f"  debiased by a circular-shift shuffle floor. Independent neural")
    print(f"  substrate vs the framework's C. elegans calcium result.")


if __name__ == "__main__":
    main()
