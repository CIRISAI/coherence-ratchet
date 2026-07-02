#!/usr/bin/env python3
"""
CLEAN POSITIVE CONTROL for the bound-vs-coordinating (detailed-balance) detector,
on FAST spike-train data — macaque primary motor + dorsal premotor cortex during
a delayed-reach maze task (DANDI 000140, MC_Maze_Small; Churchland/Kaufman/Shenoy
lineage). This is THE textbook system for directed rotational population dynamics
(jPCA, Churchland et al. 2012, Nature): during movement the population state
traces consistent directed loops in its top principal plane. A directed loop
breaks detailed balance by construction -> the winding-rate detector must fire
STRONGLY here, unlike the ~1 s calcium C. elegans case (median |z|=2.75).

Data: 142 sorted units, 293 s continuous recording, 100 successful reaches with
absolute move_onset_time. NWB (=HDF5) read directly with h5py (no pynwb needed).

Two units x time matrices:
  (A) WHOLE SESSION  : bin all 293 s at 20 ms -> 142 x ~14680 (conservative;
                       inter-trial idle periods included, dilutes the signal).
  (B) MOVEMENT-ALIGNED: for each reach concatenate [move_onset-100ms,+500ms] at
                       20 ms -> 142 x (100*30=3000). This is the rotation-rich
                       regime where the directed cycle lives.

Readouts:
  1. SATURATION  (spectral_test core): correlation-eigenvalue participation ratio,
     effective rank vs phase-randomized surrogate floor, PR subsampling exponent
     beta. beta~0 & small rank = low-rank/bounded k_eff.
  2. DETAILED BALANCE (entropy_production.irreversibility_from_units, k=4): net
     winding rate z of the top-4 SVD modes. |z| >> 2 = broken detailed balance =
     coordinating. Null ceiling ~1.5; calcium C. elegans reference = 2.75.
  3. Synthetic calibrators re-run at the data's T to confirm the ruler.

Real data only; synthetics only calibrate. No commit, no .lean edits.
"""
import os, json, numpy as np, h5py
import entropy_production as ep
import spectral_test as st   # corr_eig, participation_ratio, mp_edge, phase_randomize, subsample_pr

HERE = os.path.dirname(os.path.abspath(__file__))
# NWB kept out of the repo tree; set MC_MAZE_NWB or drop mc_maze_small.nwb beside this script.
NWB  = os.environ.get("MC_MAZE_NWB",
    "/tmp/claude-1000/-home-emoore-coherence-ratchet/a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/mc_maze_small.nwb")
if not os.path.exists(NWB) and os.path.exists(os.path.join(HERE, "mc_maze_small.nwb")):
    NWB = os.path.join(HERE, "mc_maze_small.nwb")
BIN  = 0.020          # 20 ms bins
RNG  = np.random.default_rng(0)

# ---- load spikes -----------------------------------------------------------
def load_units(path):
    f = h5py.File(path, "r")
    u = f["units"]
    st_all = u["spike_times"][:]
    idx    = u["spike_times_index"][:]
    bounds = np.concatenate([[0], idx])
    units  = [st_all[bounds[i]:bounds[i+1]] for i in range(len(idx))]
    tr = f["intervals"]["trials"]
    move = tr["move_onset_time"][:]
    return units, move, float(st_all.max())

def bin_whole(units, t_end, dt=BIN):
    edges = np.arange(0, t_end + dt, dt)
    X = np.vstack([np.histogram(s, edges)[0] for s in units]).astype(float)
    return X                                   # units x time

def bin_aligned(units, move, dt=BIN, pre=0.10, post=0.50):
    nb = int(round((pre + post) / dt))
    cols = []
    for m in move:
        edges = m - pre + dt * np.arange(nb + 1)
        block = np.vstack([np.histogram(s, edges)[0] for s in units]).astype(float)
        cols.append(block)
    return np.concatenate(cols, axis=1), nb     # units x (n_trial*nb)

def smooth(X, sigma_bins=1.0):
    """light gaussian smoothing along time (kernel radius 3 sigma)."""
    r = max(1, int(3 * sigma_bins))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_bins) ** 2); k /= k.sum()
    return np.vstack([np.convolve(row, k, mode="same") for row in X])

# ---- saturation readout ----------------------------------------------------
def saturation(X, label):
    good = (X.std(1) > 1e-9)
    X = X[good]
    ev, N, T = st.corr_eig(X)
    pr   = st.participation_ratio(ev)
    edge = st.mp_edge(N, T)
    eff_mp = int((ev > edge).sum())
    Xs = st.phase_randomize(X); evs, *_ = st.corr_eig(Xs)
    eff_surr = int((ev > evs.max()).sum())
    sizes = [s for s in [10,15,20,30,40,60,80,100,120,140] if s <= N]
    curve = st.subsample_pr(X, sizes, ndraw=25)
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    up = cn >= max(20, cn.max()//3)
    beta = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]) if up.sum()>=3 else float("nan")
    verdict = ("LOW-RANK (bounded k_eff)" if (beta < 0.2 and eff_surr <= 12)
               else "power-law/critical" if 0.2 <= beta <= 0.9
               else "extensive/noise")
    print(f"  [{label}] N={N} T={T}  PR={pr:.2f}  eff_rank(surr)={eff_surr}  "
          f"eff_rank(MP)={eff_mp}  beta_sub={beta:.3f}  -> {verdict}")
    return dict(label=label, N=N, T=T, PR=float(pr), eff_rank_surr=eff_surr,
                eff_rank_mp=eff_mp, mp_edge=float(edge), beta_sub=beta,
                top_eigs=[float(x) for x in ev[:6]],
                subsample=[[int(a),float(b),float(c)] for a,b,c in curve],
                verdict=verdict)

# ---- detailed balance ------------------------------------------------------
def db(X, label):
    r = ep.irreversibility_from_units(X, k=4)
    print(f"  [{label}] winding_rate={r['winding_rate']:+.4f}  |z|={abs(r['z']):.2f}  "
          f"pair={r['pair']}  T={r['T']}")
    return dict(label=label, winding_rate=float(r['winding_rate']),
                z=float(r['z']), abs_z=float(abs(r['z'])),
                pair=list(r['pair']), T=int(r['T']))

def calibrators(T):
    print(f"  ruler @ T={T}:")
    out = {}
    for name, gen in [("OU_equilibrium(null)", ep.ou_equilibrium),
                      ("relaxation(null)", ep.relaxation),
                      ("noisy_limit_cycle", ep.limit_cycle),
                      ("OU_driven(NESS)", ep.ou_driven)]:
        r = ep.entropy_production(gen(T)); out[name] = float(abs(r['z']))
        print(f"    {name:22s} |z|={abs(r['z']):.2f}")
    return out

# ---- main ------------------------------------------------------------------
def main():
    units, move, t_end = load_units(NWB)
    print(f"loaded {len(units)} units, {sum(len(s) for s in units)} spikes, "
          f"span {t_end:.1f}s, {len(move)} reaches\n")

    Xw = smooth(bin_whole(units, t_end))
    Xa, nb = bin_aligned(units, move)
    Xa = smooth(Xa)
    print(f"whole-session  matrix: {Xw.shape} (20ms bins)")
    print(f"move-aligned   matrix: {Xa.shape} ({nb} bins/reach x {len(move)} reaches, [-100,+500]ms)\n")

    print("=== SATURATION (is k_eff bounded / low-rank?) ===")
    sat_w = saturation(Xw, "whole-session")
    sat_a = saturation(Xa, "move-aligned")

    print("\n=== DETAILED BALANCE (winding-rate |z|; null~1.5, calcium C.elegans=2.75) ===")
    db_w = db(Xw, "whole-session")
    db_a = db(Xa, "move-aligned")

    print("\n=== CALIBRATORS (confirm the ruler at matched T) ===")
    cal_w = calibrators(Xw.shape[1])
    cal_a = calibrators(Xa.shape[1])

    # robustness: is the positive control an artifact of one bin/smoothing choice?
    print("\n=== ROBUSTNESS (whole-session |z| and eff_rank across bin/smoothing) ===")
    robust = []
    for dt in (0.010, 0.020, 0.050):
        for sig in (1.0, 2.5):
            Xr = smooth(bin_whole(units, t_end, dt=dt), sigma_bins=sig)
            good = Xr.std(1) > 1e-9
            r = ep.irreversibility_from_units(Xr[good], k=4)
            ev, N, T = st.corr_eig(Xr[good])
            Xs = st.phase_randomize(Xr[good]); evs, *_ = st.corr_eig(Xs)
            effr = int((ev > evs.max()).sum())
            print(f"  bin={int(dt*1000):>2d}ms smooth={sig:>3} : |z|={abs(r['z']):5.2f}  "
                  f"eff_rank(surr)={effr:>2d}  PR={st.participation_ratio(ev):6.1f}  T={T}")
            robust.append(dict(bin_ms=int(dt*1000), smooth_sigma=sig,
                               abs_z=float(abs(r['z'])), eff_rank_surr=effr,
                               PR=float(st.participation_ratio(ev)), T=int(T)))

    results = dict(
        dataset="DANDI:000140 MC_Maze_Small sub-Jenkins (macaque M1+PMd, delayed reach)",
        source_asset="sub-Jenkins_ses-small_desc-train_behavior+ecephys.nwb (29.2 MB)",
        n_units=len(units), n_reaches=len(move), span_s=t_end, bin_s=BIN,
        reference_nulls=dict(winding_null_ceiling=1.5, calcium_celegans_median_absz=2.75,
                             clean_cycle_synthetic_absz=16.0),
        saturation=dict(whole_session=sat_w, move_aligned=sat_a),
        detailed_balance=dict(whole_session=db_w, move_aligned=db_a),
        calibrators=dict(whole_session=cal_w, move_aligned=cal_a),
        robustness=robust,
    )
    with open(os.path.join(HERE, "spectral_results_spikes.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    print("\nwrote spectral_results_spikes.json")
    return results

if __name__ == "__main__":
    main()
