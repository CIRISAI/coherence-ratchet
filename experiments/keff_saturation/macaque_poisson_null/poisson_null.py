#!/usr/bin/env python3
"""
Macaque motor-cortex detailed-balance |z| = 8.8 vs a POISSON-COUNT-MATCHED NULL.

Closes the null-type debt on the CLAUDE.md standing result
  "Axis 2 (maintenance): ... macaque motor cortex |z|=8.8 coordinating"
whose published value was computed on 20 ms spike COUNTS while the only surrogate in
the frozen pipeline was PHASE-RANDOMIZED (continuous; reproduces the power spectrum,
NOT Poisson spike shot noise). K4 (2026-07-20) showed exactly this null-type mismatch
can manufacture an apparently-robust multi-sigma signal on discrete count data.

Pre-registration: DECISIONS.md in this directory (frozen before any number).

The estimator is the FROZEN one, imported verbatim from ../entropy_production.py.
Nulls are built at the spike-COUNT level and pushed through the identical
smoothing + estimator path as the real data.

  NULL-P  phase-randomized (original null type, side-by-side)
  NULL-A  constant-rate Poisson at the measured per-unit rate   [primary count null]
  NULL-B1 rate-profile Poisson (sigma_rate = 500 ms), each unit independently
          circularly shifted -> destroys cross-unit coordination [strict null]
  NULL-B0 rate-profile Poisson, UNSHIFTED -> diagnostic only, non-adjudicating

Real data only (DANDI:000140 MC_Maze_Small). Poisson surrogates are pre-committed
null controls, never used as data.
"""
import os, sys, json, time, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, FROZEN)

import entropy_production as ep          # FROZEN estimator, unmodified
import spectral_test as st               # FROZEN phase_randomize

NWB = os.environ.get("MC_MAZE_NWB", os.path.join(
    "/tmp/claude-1000/-home-emoore-coherence-ratchet/"
    "047db89f-06e6-45f4-a014-34f932c0bc32/scratchpad/data", "mc_maze_small.nwb"))

SIGMA_RATE_S = 0.500                     # pre-registered rate-profile smoothing (NULL-B)
K_MODES      = 4                         # frozen estimator setting
SMOOTH_SIGMA = 1.0                       # frozen analysis smoothing, in bins


# ---------------------------------------------------------------- data & binning
def load_units(path):
    import h5py
    with h5py.File(path, "r") as f:
        u = f["units"]
        st_all = u["spike_times"][:]
        idx = u["spike_times_index"][:]
        bounds = np.concatenate([[0], idx])
        units = [st_all[bounds[i]:bounds[i + 1]] for i in range(len(idx))]
        move = f["intervals"]["trials"]["move_onset_time"][:]
        return units, move, float(st_all.max())


def bin_whole(units, t_end, dt):
    """identical to frozen spectral_spikes.bin_whole"""
    edges = np.arange(0, t_end + dt, dt)
    return np.vstack([np.histogram(s, edges)[0] for s in units]).astype(float)


def smooth(X, sigma_bins=SMOOTH_SIGMA):
    """identical to frozen spectral_spikes.smooth"""
    r = max(1, int(3 * sigma_bins))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_bins) ** 2); k /= k.sum()
    return np.vstack([np.convolve(row, k, mode="same") for row in X])


def gsmooth_rows(X, sigma_bins):
    """wider gaussian smoothing used only to build the NULL-B rate profiles"""
    r = max(1, int(4 * sigma_bins))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_bins) ** 2); k /= k.sum()
    return np.vstack([np.convolve(row, k, mode="same") for row in X])


# ---------------------------------------------------------------- surrogates
def surr_phase(counts, rng):
    """NULL-P: phase-randomize the SMOOTHED matrix (as the frozen pipeline does).
    Own rng so workers are independent (frozen st.phase_randomize uses a module RNG)."""
    Xs = smooth(counts)
    F = np.fft.rfft(Xs, axis=1)
    ph = np.exp(1j * rng.uniform(0, 2 * np.pi, F.shape))
    ph[:, 0] = 1
    return np.fft.irfft(F * ph, n=Xs.shape[1], axis=1)


def surr_poisson_const(counts, rng):
    """NULL-A: iid Poisson at each unit's measured mean count per bin."""
    lam = counts.mean(1, keepdims=True)
    return smooth(rng.poisson(np.broadcast_to(lam, counts.shape)).astype(float))


def surr_poisson_rate(counts, rng, sigma_rate_bins, shift):
    """NULL-B1 (shift=True) / NULL-B0 (shift=False)."""
    rate = np.clip(gsmooth_rows(counts, sigma_rate_bins), 0, None)
    if shift:
        T = rate.shape[1]
        lags = rng.integers(0, T, rate.shape[0])
        rate = np.vstack([np.roll(rate[i], int(lags[i])) for i in range(rate.shape[0])])
    return smooth(rng.poisson(rate).astype(float))


# ---------------------------------------------------------------- one evaluation
def evaluate(X):
    r = ep.irreversibility_from_units(X, k=K_MODES)
    return dict(mu=float(r["winding_rate"]), se=float(r["se"]),
                z=float(r["z"]), abs_z=float(abs(r["z"])),
                abs_mu=float(abs(r["winding_rate"])),
                pair=list(map(int, r["pair"])), T=int(r["T"]))


_G = {}


def _init(counts, sigma_rate_bins):
    _G["counts"] = counts
    _G["srb"] = sigma_rate_bins


def _work(args):
    null, seed = args
    rng = np.random.default_rng(seed)
    c, srb = _G["counts"], _G["srb"]
    if null == "P":
        X = surr_phase(c, rng)
    elif null == "A":
        X = surr_poisson_const(c, rng)
    elif null == "B1":
        X = surr_poisson_rate(c, rng, srb, True)
    elif null == "B0":
        X = surr_poisson_rate(c, rng, srb, False)
    else:
        raise ValueError(null)
    return null, evaluate(X)


# ---------------------------------------------------------------- statistics
def outer_stats(real, nulls, key):
    v = np.asarray([n[key] for n in nulls], float)
    r = float(real[key])
    m, s = float(v.mean()), float(v.std(ddof=1))
    n_ge = int((v >= r).sum())
    n = len(v)
    return dict(stat=key, real=r, null_mean=m, null_sd=s,
                z_outer=float((r - m) / s) if s > 0 else float("nan"),
                null_median=float(np.median(v)),
                null_p95=float(np.percentile(v, 95)),
                null_p99=float(np.percentile(v, 99)),
                null_max=float(v.max()), n_null=n, n_null_ge_real=n_ge,
                p_onesided=float((n_ge + 1) / (n + 1)))


# ---------------------------------------------------------------- driver
def run_config(units, t_end, dt, nsurr, pool, log, results, tag):
    counts = bin_whole(units, t_end, dt)
    Xreal = smooth(counts)
    real = evaluate(Xreal)
    srb = SIGMA_RATE_S / dt
    log(f"\n=== bin = {int(dt*1000)} ms  ({tag})  N x T = {counts.shape}  "
        f"sigma_rate = {srb:.1f} bins ===")
    log(f"  REAL: |z|_inner = {real['abs_z']:.3f}  mu = {real['mu']:+.6f}  "
        f"se = {real['se']:.6f}  pair = {real['pair']}  T = {real['T']}")

    _init(counts, srb)  # for the serial path
    NOFF = {"P": 1, "A": 2, "B1": 3, "B0": 4}   # deterministic seeds (no hash())
    jobs = [(nl, 1_000_000 * NOFF[nl] + 1_000 * i + int(round(dt * 1000)))
            for nl in ("P", "A", "B1", "B0") for i in range(nsurr)]
    out = {"P": [], "A": [], "B1": [], "B0": []}
    t0 = time.time()
    done = 0
    for null, res in pool.imap_unordered(_work, jobs, chunksize=1):
        out[null].append(res)
        done += 1
        if done % 25 == 0:
            log(f"    ... {done}/{len(jobs)} surrogates  ({time.time()-t0:.0f}s)")
            results[tag] = dict(bin_ms=int(dt * 1000), real=real,
                                partial={k: len(v) for k, v in out.items()})
            flush(results)

    entry = dict(bin_ms=int(dt * 1000), dt_s=dt, shape=list(counts.shape),
                 sigma_rate_bins=float(srb), n_surrogate=nsurr, real=real, nulls={})
    for nl in ("P", "A", "B1", "B0"):
        v = out[nl]
        entry["nulls"][nl] = dict(
            n=len(v),
            abs_z=dict(mean=float(np.mean([x["abs_z"] for x in v])),
                       sd=float(np.std([x["abs_z"] for x in v], ddof=1)),
                       median=float(np.median([x["abs_z"] for x in v])),
                       p95=float(np.percentile([x["abs_z"] for x in v], 95)),
                       max=float(np.max([x["abs_z"] for x in v]))),
            abs_mu=dict(mean=float(np.mean([x["abs_mu"] for x in v])),
                        sd=float(np.std([x["abs_mu"] for x in v], ddof=1)),
                        median=float(np.median([x["abs_mu"] for x in v])),
                        p95=float(np.percentile([x["abs_mu"] for x in v], 95)),
                        max=float(np.max([x["abs_mu"] for x in v]))),
            outer_abs_mu=outer_stats(real, v, "abs_mu"),
            outer_abs_z=outer_stats(real, v, "abs_z"),
            samples_abs_z=[float(x["abs_z"]) for x in v],
            samples_abs_mu=[float(x["abs_mu"]) for x in v],
        )
        o = entry["nulls"][nl]["outer_abs_mu"]
        oz = entry["nulls"][nl]["outer_abs_z"]
        log(f"  NULL-{nl:2s}: |z|_inner null = {entry['nulls'][nl]['abs_z']['mean']:6.2f} "
            f"+- {entry['nulls'][nl]['abs_z']['sd']:5.2f} (max {entry['nulls'][nl]['abs_z']['max']:6.2f})"
            f" | outer z(|mu|) = {o['z_outer']:+7.2f}  p = {o['p_onesided']:.4f}"
            f" | outer z(|z|) = {oz['z_outer']:+7.2f}  p = {oz['p_onesided']:.4f}")
    results[tag] = entry
    flush(results)
    return entry


RES_PATH = os.path.join(HERE, "results.json")
LOG_PATH = os.path.join(HERE, "run.log")


def flush(results):
    tmp = RES_PATH + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(results, fh, indent=1)
    os.replace(tmp, RES_PATH)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nsurr-primary", type=int, default=200)
    ap.add_argument("--nsurr-sweep", type=int, default=100)
    ap.add_argument("--procs", type=int, default=16)
    a = ap.parse_args()

    lf = open(LOG_PATH, "a", buffering=1)

    def log(s):
        print(s, flush=True)
        lf.write(s + "\n")

    log(f"\n########## run {time.strftime('%Y-%m-%d %H:%M:%S')} ##########")
    units, move, t_end = load_units(NWB)
    nsp = int(sum(len(s) for s in units))
    log(f"loaded {len(units)} units, {nsp} spikes, span {t_end:.1f}s, {len(move)} reaches")

    results = {}
    if os.path.exists(RES_PATH):
        try:
            results = json.load(open(RES_PATH))
        except Exception:
            results = {}

    # ---- GATE: reproduce the frozen primary -------------------------------
    counts20 = bin_whole(units, t_end, 0.020)
    real20 = evaluate(smooth(counts20))
    gate = dict(n_units=len(units), n_spikes=nsp, n_reaches=int(len(move)),
                span_s=t_end, frozen_abs_z=8.83, reproduced_abs_z=real20["abs_z"],
                delta=abs(real20["abs_z"] - 8.83))
    gate["pass"] = bool(gate["delta"] < 0.05 and len(units) == 142
                        and nsp == 131669 and len(move) == 100)
    results["gate"] = gate
    flush(results)
    log(f"GATE: frozen |z| = 8.83, reproduced = {real20['abs_z']:.3f} "
        f"(delta {gate['delta']:.4f})  units={len(units)} spikes={nsp} "
        f"reaches={len(move)}  -> {'PASS' if gate['pass'] else 'FAIL'}")
    if not gate["pass"]:
        log("GATE FAILED - no verdict issued on the standing result.")
        json.dump(results, open(RES_PATH, "w"), indent=1)
        return

    import multiprocessing as mp
    ctx = mp.get_context("fork")
    sweep = [(0.020, a.nsurr_primary, "primary_20ms"),
             (0.050, a.nsurr_sweep, "sweep_50ms"),
             (0.100, a.nsurr_sweep, "sweep_100ms"),
             (0.200, a.nsurr_sweep, "sweep_200ms")]
    for dt, ns, tag in sweep:
        if tag in results and isinstance(results[tag], dict) and "nulls" in results[tag]:
            log(f"skip {tag} (already complete)")
            continue
        cts = bin_whole(units, t_end, dt)
        with ctx.Pool(a.procs, initializer=_init,
                      initargs=(cts, SIGMA_RATE_S / dt)) as pool:
            run_config(units, t_end, dt, ns, pool, log, results, tag)

    log("\ndone.")
    lf.close()


if __name__ == "__main__":
    main()
