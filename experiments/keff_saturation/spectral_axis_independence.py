#!/usr/bin/env python3
"""
AXIS-INDEPENDENCE: fill the two OPEN high-rank cells of the structure x maintenance 2x2.

Two orthogonal axes are claimed:
  (1) STRUCTURE      = effective dimensionality (LOW-rank/saturating vs HIGH-rank/scale-free)
  (2) MAINTENANCE    = detailed balance (BREAKS DB = actively coordinating/driven vs
                       DB-SATISFYING = bound/reversible/dead)

Two cells are already anchored elsewhere in this directory:
  - motor cortex (MC_Maze, spikes)  : LOW-rank + BREAKS DB   (coordinating)  |z|=8.8
  - galaxy baryon cycle (TNG)       : LOW-rank + DB-satisfying (bound)        z~0.5

This script fills the two OPEN cells and thereby tests axis-independence:

  CELL 1  TURBULENT (HIGH-rank + BREAKS DB):
      Allen Visual Coding NEUROPIXELS, visual-cortex spikes during NATURAL MOVIES.
      Fast spikes (not the DB-weak slow calcium). Prior Allen 2p calcium already read
      HIGH-rank / scale-free (power-law alpha~0.97, Stringer 2019 ~1.04, non-saturating);
      here we test on FAST spikes whether that SAME high-dimensional visual cortex ALSO
      BREAKS detailed balance. If HIGH-rank AND breaks-DB -> turbulent cell filled, and
      together with motor cortex (LOW-rank + breaks-DB) it shows the DB axis is
      INDEPENDENT of the rank axis (both break DB, different ranks).

  CELL 2  DEAD (HIGH-rank + DB-SATISFYING):
      (a) PRIMARY constructed control: PHASE-RANDOMIZE the SAME neuropixels data. Phase
          randomization destroys cross-unit structure (-> HIGH-rank) and the time-arrow
          (-> DB-satisfying) by construction. So the same data, scrambled, should read
          HIGH-rank + DB-satisfying: both axes flip when coordination is removed while
          the marginal power spectra are held fixed. (Labelled: CONSTRUCTED CONTROL.)
      (b) if reachable, a genuinely-equilibrium real anchor is sought separately.

Rank axis reuses spectral_test.py (corr_eig, participation_ratio, mp_edge,
phase_randomize, subsample_pr) + a debiased effective rank vs phase-randomized surrogate
+ a power-law exponent alpha (lambda_i ~ i^-alpha; alpha~1 scale-free/high-rank,
alpha~0 flat/noise). DB axis reuses BOTH validated estimators:
  - winding-rate z            (entropy_production.irreversibility_from_units)
  - direct circulation z      (spectral_galaxy_db.db_stats: omega vs phase-rand null)

Real data only; the phase-randomized "dead" cell is a CONSTRUCTED control, labelled as
such. No commit, no .lean edits.
"""
import os, sys, json, numpy as np, h5py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import entropy_production as ep
import spectral_test as st
import spectral_galaxy_db as gdb

NWB = os.environ.get("NPX_NWB",
    "/tmp/claude-1000/-home-emoore-coherence-ratchet/a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/npx_ses721123822.nwb")
OUT_JSON = os.path.join(HERE, "spectral_results_axis_independence.json")
BIN = 0.020            # 20 ms spike bins (fast)
RNG = np.random.default_rng(0)
VIS_PREFIXES = ("VIS",)   # cortical visual areas (VISp, VISl, VISal, VISpm, VISrl, VISam)


# --------------------------------------------------------------------------- #
#  Allen Neuropixels loader (NWB = HDF5, read with h5py; no pynwb/allensdk)    #
# --------------------------------------------------------------------------- #
def load_units(path):
    """Return list of spike-time arrays (one per unit), unit region labels, session span."""
    f = h5py.File(path, "r")
    u = f["units"]
    st_all = u["spike_times"][:]
    idx = u["spike_times_index"][:]
    bounds = np.concatenate([[0], idx])
    units = [st_all[bounds[i]:bounds[i + 1]] for i in range(len(idx))]
    # region label per unit: units table -> electrodes table -> location
    region = None
    try:
        peak_ch = u["peak_channel_id"][:] if "peak_channel_id" in u else None
        el = f["general/extracellular_ephys/electrodes"]
        loc = np.array([x.decode() if isinstance(x, bytes) else str(x)
                        for x in el["location"][:]])
        el_ids = el["id"][:]
        id2loc = {int(i): l for i, l in zip(el_ids, loc)}
        if peak_ch is not None:
            region = np.array([id2loc.get(int(c), "?") for c in peak_ch])
    except Exception as e:
        print("  (region lookup failed:", str(e)[:80], ")")
    span = float(st_all.max())
    return f, units, region, span


def _largest_contiguous_block(s, e, max_gap=0.5):
    """Largest run of consecutive presentations with inter-presentation gap < max_gap."""
    order = np.argsort(s); s = s[order]; e = e[order]
    gaps = s[1:] - e[:-1]
    big = np.where(gaps > max_gap)[0]
    bounds = np.concatenate([[0], big + 1, [len(s)]])
    runs = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    lens = [e[b - 1] - s[a] for a, b in runs]
    k = int(np.argmax(lens))
    a, b = runs[k]
    return float(s[a]), float(e[b - 1]), int(b - a), float(lens[k])


def natural_movie_window(f):
    """Return (t0, t1, names) for the LARGEST CONTIGUOUS natural-movie block, else
    (None, None). Using a contiguous block (not min..max, which straddles other
    interleaved stimuli) gives the winding estimator a continuous time trajectory.
    Allen Visual Coding intervals live under /intervals/<name>_presentations."""
    iv = f.get("intervals")
    if iv is None:
        return None, None
    names = list(iv.keys())
    movie = [n for n in names if "natural_movie" in n.lower()] or \
            [n for n in names if "movie" in n.lower()]
    if not movie:
        return None, None
    best = None
    for n in movie:
        g = iv[n]
        if "start_time" not in g or "stop_time" not in g:
            continue
        t0, t1, npres, dur = _largest_contiguous_block(g["start_time"][:], g["stop_time"][:])
        if best is None or dur > best[3]:
            best = (t0, t1, dur, dur, [n], npres)
    if best is None:
        return None, None
    t0, t1, dur, _, name, npres = best
    return t0, t1, [f"{name[0]} (largest contiguous block: {npres} frames, {dur:.0f}s)"]


def bin_spikes(units, t0, t1, dt=BIN):
    edges = np.arange(t0, t1 + dt, dt)
    X = np.vstack([np.histogram(s, edges)[0] for s in units]).astype(float)
    return X                       # units x time


def smooth(X, sigma_bins=1.0):
    r = max(1, int(3 * sigma_bins))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_bins) ** 2); k /= k.sum()
    return np.vstack([np.convolve(row, k, mode="same") for row in X])


# --------------------------------------------------------------------------- #
#  RANK axis                                                                   #
# --------------------------------------------------------------------------- #
def powerlaw_alpha(ev, i0=2, frac=0.5):
    """alpha in lambda_i ~ i^-alpha, fit on a log-log mid range of the eigenspectrum.
    alpha~1 = Stringer-style scale-free (high-dimensional); alpha~0 = flat (noise)."""
    ev = np.sort(ev)[::-1]
    ev = ev[ev > 0]
    n = len(ev)
    hi = max(i0 + 3, int(frac * n))
    idx = np.arange(i0, hi)
    if len(idx) < 4:
        return float("nan")
    a = -np.polyfit(np.log10(idx + 1), np.log10(ev[idx]), 1)[0]
    return float(a)


def rank_readout(X, label, size_grid=None):
    """Debiased effective rank, PR, power-law alpha, PR-subsampling beta."""
    good = X.std(1) > 1e-9
    X = X[good]
    ev, N, T = st.corr_eig(X)
    pr = st.participation_ratio(ev)
    edge = st.mp_edge(N, T)
    eff_mp = int((ev > edge).sum())
    Xs = st.phase_randomize(X); evs, *_ = st.corr_eig(Xs)
    eff_surr = int((ev > evs.max()).sum())
    alpha = powerlaw_alpha(ev)
    alpha_surr = powerlaw_alpha(evs)
    if size_grid is None:
        size_grid = [10, 15, 20, 30, 40, 60, 80, 100, 150, 200, 300, 400]
    sizes = [s for s in size_grid if s <= N]
    curve = st.subsample_pr(X, sizes, ndraw=20)
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    up = cn >= max(20, cn.max() // 3)
    beta = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]) if up.sum() >= 3 else float("nan")
    # HIGH-rank if debiased eff-rank is large AND spectrum is scale-free (alpha~1, well above surrogate)
    highrank = (eff_surr >= 15) and (alpha > 0.5) and (alpha > alpha_surr + 0.3)
    verdict = "HIGH-rank / scale-free" if highrank else \
              ("LOW-rank / bounded" if (eff_surr <= 12 and beta < 0.3) else "intermediate")
    print(f"  [RANK {label}] N={N} T={T}  PR={pr:.1f}  eff_rank(surr)={eff_surr}  "
          f"eff_rank(MP)={eff_mp}  alpha={alpha:.2f}(surr {alpha_surr:.2f})  beta={beta:.3f}  -> {verdict}")
    return dict(label=label, N=int(N), T=int(T), PR=float(pr), eff_rank_surr=int(eff_surr),
                eff_rank_mp=int(eff_mp), mp_edge=float(edge), alpha=alpha, alpha_surr=alpha_surr,
                beta_sub=beta, top_eigs=[float(x) for x in ev[:8]],
                subsample=[[int(a), float(b), float(c)] for a, b, c in curve],
                verdict=verdict, high_rank=bool(highrank))


# --------------------------------------------------------------------------- #
#  DB axis (two estimators)                                                    #
# --------------------------------------------------------------------------- #
def db_readout(X, label, kmodes=4):
    good = X.std(1) > 1e-9
    Xg = X[good]
    # estimator 1: winding-rate z on top-k SVD modes (block-bootstrap null)
    w = ep.irreversibility_from_units(Xg, k=kmodes)
    # estimator 2: direct circulation omega vs phase-randomized null
    A = gdb.modes(Xg, kmodes)
    pr, cs = gdb.db_stats(A, npair=min(3, kmodes))
    print(f"  [DB   {label}] winding|z|={abs(w['z']):.2f}  circulation|z|={abs(cs['z']):.2f}  "
          f"(winding pair {w['pair']}, T={w['T']})")
    return dict(label=label,
                winding_rate=float(w['winding_rate']), winding_z=float(w['z']),
                winding_abs_z=float(abs(w['z'])), winding_pair=list(w['pair']), T=int(w['T']),
                circulation_sum=float(cs['circulation_sum']), circulation_z=float(cs['z']),
                circulation_abs_z=float(abs(cs['z'])),
                circulation_pairs={k: dict(omega=float(v['omega']), z=float(v['z']))
                                   for k, v in pr.items()})


def db_calibrators(T):
    out = {}
    for name, gen in [("OU_equilibrium(null)", ep.ou_equilibrium),
                      ("relaxation(null)", ep.relaxation),
                      ("noisy_limit_cycle", ep.limit_cycle),
                      ("OU_driven(NESS)", ep.ou_driven)]:
        r = ep.entropy_production(gen(min(T, 5000)))
        out[name] = float(abs(r['z']))
    return out


# --------------------------------------------------------------------------- #
MC_MAZE = os.environ.get("MC_MAZE_NWB",
    "/tmp/claude-1000/-home-emoore-coherence-ratchet/a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/mc_maze_small.nwb")


def load_mc_maze(path):
    """Macaque M1/PMd spikes (whole session), units x spike-time arrays + span."""
    f = h5py.File(path, "r")
    u = f["units"]; st_all = u["spike_times"][:]; idx = u["spike_times_index"][:]
    bounds = np.concatenate([[0], idx])
    units = [st_all[bounds[i]:bounds[i + 1]] for i in range(len(idx))]
    span = float(st_all.max()); f.close()
    return units, span


def smoothing_sweep(units, t0, t1, label, sigmas=(1.0, 2.5, 5.0), size_grid=None):
    """Shot-noise is suppressed by rate smoothing; a genuine high-rank (scale-free)
    system keeps a large non-saturating rank as sigma grows, while a low-rank system's
    rank collapses. Report rank + DB across smoothing to separate signal from shot noise."""
    rows = []
    X0 = bin_spikes(units, t0, t1)
    for sig in sigmas:
        X = smooth(X0, sigma_bins=sig)
        r = rank_readout(X, f"{label}_sig{sig}", size_grid=size_grid)
        d = db_readout(X, f"{label}_sig{sig}")
        rows.append(dict(sigma_bins=sig, rank=r, db=d))
    return rows


def main():
    if not os.path.exists(NWB):
        print("NWB not found:", NWB); sys.exit(2)
    print(f"loading {NWB} ({os.path.getsize(NWB)/1e9:.2f} GB)")
    f, units, region, span = load_units(NWB)
    print(f"loaded {len(units)} units, session span {span:.0f}s")

    # select cortical visual units
    if region is not None:
        is_vis = np.array([str(r).startswith(VIS_PREFIXES) for r in region])
        vis_regions = sorted(set(region[is_vis]))
        print(f"visual-cortex units: {is_vis.sum()} / {len(units)}  regions={vis_regions}")
        vis_idx = np.where(is_vis)[0]
    else:
        print("no region labels -> using all units")
        vis_idx = np.arange(len(units))
    units_vis = [units[i] for i in vis_idx]

    # natural-movie window
    nm = natural_movie_window(f)
    if nm[0] is not None:
        t0, t1, movie_names = nm
        print(f"natural-movie window [{t0:.0f}, {t1:.0f}]s ({t1-t0:.0f}s)  from {movie_names}")
    else:
        # fall back to full session
        t0, t1, movie_names = 0.0, span, ["<full session>"]
        print("no natural-movie interval found -> full session")
    f.close()

    X = smooth(bin_spikes(units_vis, t0, t1))
    # drop silent units
    fr = np.array([len(s[(s >= t0) & (s <= t1)]) for s in units_vis]) / (t1 - t0)
    active = fr > 0.5      # >0.5 Hz
    Xact = X[active]
    print(f"turbulent-cell matrix (natural movie, active>0.5Hz): {Xact.shape}")

    results = dict(
        dataset="DANDI:000021 Allen Visual Coding Neuropixels, session 721123822",
        source_asset=os.path.basename(NWB),
        stimulus=movie_names, window_s=[float(t0), float(t1)], bin_s=BIN,
        n_units_total=len(units), n_units_visual=int(len(units_vis)),
        n_units_active=int(active.sum()),
        reference_nulls=dict(winding_null_ceiling=1.5, calcium_celegans_median_absz=2.75,
                             clean_cycle_synthetic_absz=16.0),
        anchored_cells=dict(
            motor_cortex="LOW-rank (eff_rank 5-8) + BREAKS DB (winding|z|=8.8) [MC_Maze spikes]",
            galaxy="LOW-rank + DB-satisfying (circulation z~0.5) [TNG baryon cycle]"),
    )

    # ---- CELL 1: TURBULENT (high-rank + breaks DB) --------------------------
    print("\n=== CELL 1: TURBULENT (expect HIGH-rank + BREAKS DB) ===")
    c1_rank = rank_readout(Xact, "neuropixels_visual_naturalmovie")
    c1_db = db_readout(Xact, "neuropixels_visual_naturalmovie")

    # ---- CELL 2a: DEAD constructed control (phase-randomize the SAME data) ---
    print("\n=== CELL 2a: DEAD constructed control (phase-randomized SAME data) ===")
    Xdead = st.phase_randomize(Xact)
    c2_rank = rank_readout(Xdead, "neuropixels_PHASE_RANDOMIZED(control)")
    c2_db = db_readout(Xdead, "neuropixels_PHASE_RANDOMIZED(control)")

    # ---- calibrators at the data T -----------------------------------------
    print("\n=== DB calibrators at data T ===")
    cal = db_calibrators(Xact.shape[1])
    for k, v in cal.items():
        print(f"  {k:22s} |z|={v:.2f}")

    results["cells"] = dict(
        turbulent=dict(rank=c1_rank, db=c1_db,
                       target="HIGH-rank + BREAKS DB", source="real spikes (natural movie)"),
        dead_constructed=dict(rank=c2_rank, db=c2_db,
                       target="HIGH-rank + DB-satisfying",
                       source="CONSTRUCTED CONTROL: phase-randomized turbulent data"),
    )
    results["db_calibrators"] = cal

    # ---- HEAD-TO-HEAD vs motor cortex through the IDENTICAL pipeline ---------
    # The axis-independence crux: two DB-breaking systems at DIFFERENT rank. Spike
    # shot noise confounds naive rank, so we run a smoothing sweep on BOTH: a genuine
    # scale-free (high-rank) system keeps a large non-saturating rank as sigma rises;
    # a low-rank system's rank collapses toward a few modes.
    print("\n=== SMOOTHING SWEEP: visual cortex (natural movie) ===")
    idx_act = np.where(active)[0]
    units_act = [units_vis[i] for i in idx_act]
    vis_sweep = smoothing_sweep(units_act, t0, t1, "visual_naturalmovie")

    if os.path.exists(MC_MAZE):
        print("\n=== SMOOTHING SWEEP: motor cortex (MC_Maze whole session) — head-to-head ===")
        mc_units, mc_span = load_mc_maze(MC_MAZE)
        # match the visual epoch duration so N/T and shot-noise regimes are comparable
        mc_t1 = min(mc_span, t1 - t0)
        mc_sweep = smoothing_sweep(mc_units, 0.0, mc_span, "motor_MCmaze",
                                   size_grid=[10, 15, 20, 30, 40, 60, 80, 100, 120, 140])
        results["head_to_head"] = dict(
            note="identical pipeline; visual vs motor spikes across rate smoothing",
            visual_visualcortex=vis_sweep, motor_MCmaze=mc_sweep)
        print("\n  sigma | VISUAL eff_rank(surr)/alpha/beta/PR | MOTOR eff_rank(surr)/alpha/beta/PR")
        for vr, mr in zip(vis_sweep, mc_sweep):
            v, m = vr["rank"], mr["rank"]
            print(f"   {vr['sigma_bins']:>4} | vis rk={v['eff_rank_surr']:>2} a={v['alpha']:.2f} "
                  f"b={v['beta_sub']:.2f} PR={v['PR']:.0f}  |z|={vr['db']['winding_abs_z']:.1f}"
                  f"  ||  mot rk={m['eff_rank_surr']:>2} a={m['alpha']:.2f} b={m['beta_sub']:.2f} "
                  f"PR={m['PR']:.0f}  |z|={mr['db']['winding_abs_z']:.1f}")
    else:
        results["head_to_head"] = dict(note="MC_Maze not found", visual_visualcortex=vis_sweep)

    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"\nwrote {OUT_JSON}")
    return results


if __name__ == "__main__":
    main()
