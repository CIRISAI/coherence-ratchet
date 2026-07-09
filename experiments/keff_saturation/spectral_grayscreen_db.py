#!/usr/bin/env python3
"""
DECONFOUND: is the visual-cortex "breaks detailed balance" signal INTRINSIC (real
gamma*M active maintenance) or an artifact of the LOOPING natural-movie stimulus?

BACKGROUND. The "turbulent" 2x2 cell (HIGH-rank + BREAKS DB) was anchored on Allen
Neuropixels visual cortex during natural_movie_three (a LOOPING clip). A response
phase-locked to the movie's repeat period produces a rotation in the top covariance
modes that reads as "breaks DB" and survives phase-randomization -- but its SOURCE
is the external periodic drive, not the system's own gamma*M. In the prior run the
circulation z=4.0 was carried almost entirely by ONE mode-pair (0-2, z=-6.1; others
at null), and winding picked a different single carrier pair (0-3): the signature of
a single driven rotation, not distributed intrinsic irreversibility.

THE TEST. Recompute the DB axis on the SAME visual cortex, SAME units, SAME 20ms
bins, SAME estimators, across three stimulus conditions on one brain_observatory_1.1
session:
  1. SPONTANEOUS  -- longest continuous gray-screen block. NO external periodicity.
                     The clean intrinsic-gamma*M condition.
  2. NATURAL_MOVIE-- looping clip (the prior "turbulent" anchor). External period.
  3. DRIFTING_GRATINGS -- periodic but a DIFFERENT externally-imposed period than the
                     movie loop (2s grating + 1s blank cycle + internal TF drift).
                     If DB tracks whatever periodicity is present, gratings show it too.

For each condition, each null is a PHASE-RANDOMIZATION of that SAME condition's data
(never the movie null reused for spontaneous). We report, per condition:
  - k_eff (participation ratio) and debiased eff-rank
  - winding |z| (entropy_production.irreversibility_from_units, block-bootstrap null)
  - circulation |z| (spectral_galaxy_db.db_stats, per-pair phase-randomized null)
  - PER-MODE-PAIR circulation z  (directly tests "single driven pair" vs distributed)
  - the winding/circulation |z| ON the phase-randomized SAME data = the null CEILING
  - T and the T-limitation flag for winding

VERDICT logic:
  intrinsic gamma*M  -> spontaneous STILL breaks DB (|z| clearly above null ceiling and
                        above the ~1.5 winding null) -> turbulent cell holds, confound
                        rejected. The arrow of time is the system's own.
  stimulus-driven    -> spontaneous at null but movie present, and the single dominant
                        antisymmetric pair DISAPPEARS in spontaneous -> "breaks DB" was
                        external periodicity; turbulent-cell DB claim collapses (relabel
                        high-rank + externally-driven).
  unresolved         -> T too short for a stable winding at spontaneous; lean on direct
                        circulation which tolerates shorter T, and say so.

Real data only. Population held FIXED across conditions (VIS units active >0.5 Hz in
ALL three windows) so the stimulus is the only thing that changes. No commit.
"""
import os, sys, json, numpy as np, h5py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import entropy_production as ep
import spectral_test as st
import spectral_galaxy_db as gdb
from spectral_axis_independence import (load_units, bin_spikes, smooth,
                                        natural_movie_window, rank_readout)

NWB = os.environ.get("NPX_NWB",
    "/tmp/claude-1000/-home-emoore-coherence-ratchet/a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/npx_ses721123822.nwb")
OUT_JSON = os.path.join(HERE, "spectral_results_grayscreen_db.json")
BIN = 0.020
VIS_PREFIXES = ("VIS",)
KMODES = 4
RNG = np.random.default_rng(0)


def _largest_single_block(s, e, max_gap=0.5):
    """Largest contiguous run of presentations (inter-presentation gap < max_gap).
    Returns (t0, t1, npres, dur)."""
    order = np.argsort(s); s = s[order]; e = e[order]
    gaps = s[1:] - e[:-1]
    big = np.where(gaps > max_gap)[0]
    bounds = np.concatenate([[0], big + 1, [len(s)]])
    runs = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    lens = [e[b - 1] - s[a] for a, b in runs]
    k = int(np.argmax(lens))
    a, b = runs[k]
    return float(s[a]), float(e[b - 1]), int(b - a), float(lens[k])


def interval_window(f, name, max_gap):
    g = f["intervals"][name]
    return _largest_single_block(g["start_time"][:], g["stop_time"][:], max_gap=max_gap)


def db_readout(X, label, kmodes=KMODES):
    """winding |z| + circulation |z| + per-pair circulation z on top-k modes."""
    good = X.std(1) > 1e-9
    Xg = X[good]
    w = ep.irreversibility_from_units(Xg, k=kmodes)
    A = gdb.modes(Xg, kmodes)
    pr, cs = gdb.db_stats(A, npair=min(3, kmodes))
    per_pair = {k: dict(omega=float(v['omega']), z=float(v['z'])) for k, v in pr.items()}
    max_pair_absz = max(abs(v['z']) for v in per_pair.values())
    return dict(label=label,
                winding_rate=float(w['winding_rate']), winding_abs_z=float(abs(w['z'])),
                winding_pair=list(w['pair']), T=int(w['T']),
                circulation_sum=float(cs['circulation_sum']),
                circulation_abs_z=float(abs(cs['z'])),
                circulation_pairs=per_pair,
                max_pair_abs_z=float(max_pair_absz))


def condition_readout(X, label):
    """rank (k_eff) + DB on real data; DB null CEILING on phase-randomized SAME data."""
    r = rank_readout(X, label)
    d = db_readout(X, label)
    Xnull = st.phase_randomize(X)
    dnull = db_readout(Xnull, label + "_PHASERAND(null_ceiling)")
    print(f"  [{label}] N={r['N']} T={r['T']}  k_eff(PR)={r['PR']:.1f} "
          f"eff_rank_surr={r['eff_rank_surr']}  || winding|z|={d['winding_abs_z']:.2f} "
          f"(pair {d['winding_pair']})  circ|z|={d['circulation_abs_z']:.2f} "
          f"max_pair|z|={d['max_pair_abs_z']:.2f}")
    print(f"        NULL CEILING (phase-rand same data): winding|z|={dnull['winding_abs_z']:.2f}"
          f"  circ|z|={dnull['circulation_abs_z']:.2f}  max_pair|z|={dnull['max_pair_abs_z']:.2f}")
    print(f"        per-pair circ z: " +
          "  ".join(f"{k}:z={v['z']:+.2f}" for k, v in d['circulation_pairs'].items()))
    return dict(rank=r, db=d, db_null_ceiling=dnull)


def main():
    if not os.path.exists(NWB):
        print("NWB not found:", NWB); sys.exit(2)
    print(f"loading {NWB} ({os.path.getsize(NWB)/1e9:.2f} GB)")
    f, units, region, span = load_units(NWB)
    print(f"loaded {len(units)} units, session span {span:.0f}s")

    if region is not None:
        is_vis = np.array([str(r).startswith(VIS_PREFIXES) for r in region])
        vis_regions = sorted(set(region[is_vis]))
        print(f"visual-cortex units: {is_vis.sum()} / {len(units)}  regions={vis_regions}")
        vis_idx = np.where(is_vis)[0]
    else:
        print("no region labels -> using all units"); vis_idx = np.arange(len(units))
    units_vis = [units[i] for i in vis_idx]

    # ---- define the three windows -------------------------------------------
    # spontaneous: gray screen, single largest continuous block (no periodicity)
    sp_t0, sp_t1, sp_np, sp_dur = interval_window(f, "spontaneous_presentations", max_gap=0.5)
    # natural movie: reuse the same helper the prior anchor used (largest contiguous loop block)
    nm = natural_movie_window(f); nm_t0, nm_t1, nm_names = nm[0], nm[1], nm[2]
    # drifting gratings: bridge the ~1s inter-trial blanks (max_gap 1.5) -> continuous driven epoch
    dg_t0, dg_t1, dg_np, dg_dur = interval_window(f, "drifting_gratings_presentations", max_gap=1.5)

    windows = {
        "spontaneous":      dict(t0=sp_t0, t1=sp_t1, desc=f"gray screen, single {sp_dur:.0f}s block",
                                 periodicity="NONE (intrinsic condition)"),
        "natural_movie":    dict(t0=nm_t0, t1=nm_t1, desc=nm_names[0],
                                 periodicity="LOOPING clip (prior turbulent anchor)"),
        "drifting_gratings":dict(t0=dg_t0, t1=dg_t1, desc=f"{dg_np} gratings, {dg_dur:.0f}s block",
                                 periodicity="periodic, DIFFERENT period than movie loop"),
    }
    for k, w in windows.items():
        print(f"  window {k:18s} [{w['t0']:.0f},{w['t1']:.0f}]s ({w['t1']-w['t0']:.0f}s)  {w['periodicity']}")
    f.close()

    # ---- hold the population FIXED: VIS units active >0.5 Hz in ALL windows --
    def frates(t0, t1):
        return np.array([len(s[(s >= t0) & (s <= t1)]) for s in units_vis]) / (t1 - t0)
    active_all = np.ones(len(units_vis), bool)
    for w in windows.values():
        active_all &= (frates(w["t0"], w["t1"]) > 0.5)
    idx_act = np.where(active_all)[0]
    units_act = [units_vis[i] for i in idx_act]
    print(f"\nFIXED population: {len(units_act)} VIS units active >0.5 Hz in ALL three windows\n")

    results = dict(
        test="grayscreen deconfound of the turbulent-cell DB signal",
        dataset="DANDI:000021 Allen Visual Coding Neuropixels, session 721123822 (brain_observatory_1.1)",
        source_asset=os.path.basename(NWB), bin_s=BIN, kmodes=KMODES,
        population="VIS cortical units active >0.5 Hz in ALL three windows (held fixed)",
        n_units_fixed=int(len(units_act)),
        winding_null_ceiling_reference=1.5,
        prior_movie_anchor=dict(winding_abs_z=4.15, circulation_abs_z=4.01,
                                carrier_pair="0-2 z=-6.1 (single dominant), winding pair 0-3"),
        windows={k: {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv)
                     for kk, vv in v.items()} for k, v in windows.items()},
        conditions={},
    )

    for cond, w in windows.items():
        print(f"=== {cond.upper()} ({w['periodicity']}) ===")
        X = smooth(bin_spikes(units_act, w["t0"], w["t1"]))
        results["conditions"][cond] = condition_readout(X, cond)
        results["conditions"][cond]["periodicity"] = w["periodicity"]
        print()

    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"wrote {OUT_JSON}")

    # ---- compact verdict table ---------------------------------------------
    print("\n" + "=" * 100)
    print(f"{'condition':18s} {'T':>6s} {'k_eff':>7s} {'effR':>5s} "
          f"{'wind|z|':>8s} {'circ|z|':>8s} {'maxpair|z|':>10s} {'NULLwind':>9s} {'NULLcirc':>9s}")
    for cond in ["spontaneous", "natural_movie", "drifting_gratings"]:
        c = results["conditions"][cond]; r, d, n = c["rank"], c["db"], c["db_null_ceiling"]
        print(f"{cond:18s} {d['T']:>6d} {r['PR']:>7.1f} {r['eff_rank_surr']:>5d} "
              f"{d['winding_abs_z']:>8.2f} {d['circulation_abs_z']:>8.2f} {d['max_pair_abs_z']:>10.2f} "
              f"{n['winding_abs_z']:>9.2f} {n['circulation_abs_z']:>9.2f}")
    print("=" * 100)
    return results


if __name__ == "__main__":
    main()
