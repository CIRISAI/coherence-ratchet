#!/usr/bin/env python3
"""
POST-HOC SUPPLEMENTS (declared as such; they do NOT alter the frozen §7 verdict).

S-1  PRECISION: rerun the primary 20 ms configuration against NULL-A and NULL-B1 with
     N = 2000 surrogates instead of the pre-registered N = 200, so the marginal
     |mu| p-value (1/200 and 3/200 breaches) is measured rather than estimated from a
     handful of tail draws. The statistic, the estimator and the p < 0.01 threshold are
     unchanged; only the surrogate count grows. Reported SEPARATELY from the frozen call.

S-2  THE DEFENSE'S OWN HEADLINE CELL: the frozen summary's strongest number is
     50 ms bins with smoothing sigma = 2.5 bins -> |z| = 44.03, quoted against a
     "null ceiling ~1.5". The frozen bin sweep confounded bin width with smoothing
     width, so the pre-registered sweep here held sigma = 1. S-2 evaluates that exact
     frozen cell (50 ms, sigma = 2.5) against all four nulls, to test whether the
     "~1.5 ceiling" survives at the binning the headline number is quoted at.
"""
import os, sys, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import poisson_null as P

OUT = os.path.join(HERE, "supplement_results.json")
LOG = os.path.join(HERE, "supplement.log")
lf = open(LOG, "a", buffering=1)


def log(s):
    print(s, flush=True)
    lf.write(s + "\n")


def flush(d):
    tmp = OUT + ".tmp"
    json.dump(d, open(tmp, "w"), indent=1)
    os.replace(tmp, OUT)


_S = {}


def _init2(counts, srb, smooth_sigma):
    _S["c"] = counts
    _S["srb"] = srb
    _S["ss"] = smooth_sigma


def _work2(args):
    null, seed = args
    rng = np.random.default_rng(seed)
    c, srb, ss = _S["c"], _S["srb"], _S["ss"]
    if null == "P":
        Xs = P.smooth(c, ss)
        F = np.fft.rfft(Xs, axis=1)
        ph = np.exp(1j * rng.uniform(0, 2 * np.pi, F.shape)); ph[:, 0] = 1
        X = np.fft.irfft(F * ph, n=Xs.shape[1], axis=1)
    elif null == "A":
        lam = c.mean(1, keepdims=True)
        X = P.smooth(rng.poisson(np.broadcast_to(lam, c.shape)).astype(float), ss)
    else:
        rate = np.clip(P.gsmooth_rows(c, srb), 0, None)
        if null == "B1":
            T = rate.shape[1]
            lags = rng.integers(0, T, rate.shape[0])
            rate = np.vstack([np.roll(rate[i], int(lags[i])) for i in range(rate.shape[0])])
        X = P.smooth(rng.poisson(rate).astype(float), ss)
    return null, P.evaluate(X)


def block(units, t_end, dt, smooth_sigma, nulls, nsurr, tag, res):
    import multiprocessing as mp
    c = P.bin_whole(units, t_end, dt)
    srb = P.SIGMA_RATE_S / dt
    real = P.evaluate(P.smooth(c, smooth_sigma))
    log(f"\n=== {tag}: bin {int(dt*1000)} ms, smooth sigma {smooth_sigma} bins, "
        f"N x T = {c.shape}, {nsurr} surrogates/null ===")
    log(f"  REAL |z|_inner = {real['abs_z']:.3f}  |mu| = {real['abs_mu']:.6f}  "
        f"se = {real['se']:.6f}  pair = {real['pair']}")
    NOFF = {"P": 1, "A": 2, "B1": 3, "B0": 4}
    jobs = [(nl, 7_000_000 * NOFF[nl] + 13 * i + int(round(dt * 1000 + smooth_sigma * 10)))
            for nl in nulls for i in range(nsurr)]
    out = {nl: [] for nl in nulls}
    ctx = mp.get_context("fork")
    t0 = time.time(); done = 0
    with ctx.Pool(24, initializer=_init2, initargs=(c, srb, smooth_sigma)) as pool:
        for nl, r in pool.imap_unordered(_work2, jobs, chunksize=4):
            out[nl].append(r); done += 1
            if done % 200 == 0:
                log(f"    ... {done}/{len(jobs)} ({time.time()-t0:.0f}s)")
                res.setdefault(tag, {})["partial"] = {k: len(v) for k, v in out.items()}
                flush(res)
    entry = dict(bin_ms=int(dt * 1000), smooth_sigma=smooth_sigma, shape=list(c.shape),
                 n_surrogate=nsurr, real=real, nulls={})
    for nl in nulls:
        v = out[nl]
        az = np.array([x["abs_z"] for x in v]); am = np.array([x["abs_mu"] for x in v])
        entry["nulls"][nl] = dict(
            n=len(v),
            abs_z=dict(mean=float(az.mean()), sd=float(az.std(ddof=1)),
                       median=float(np.median(az)), p95=float(np.percentile(az, 95)),
                       p99=float(np.percentile(az, 99)), max=float(az.max())),
            abs_mu=dict(mean=float(am.mean()), sd=float(am.std(ddof=1)),
                        median=float(np.median(am)), p95=float(np.percentile(am, 95)),
                        p99=float(np.percentile(am, 99)), max=float(am.max())),
            outer_abs_mu=P.outer_stats(real, v, "abs_mu"),
            outer_abs_z=P.outer_stats(real, v, "abs_z"))
        om = entry["nulls"][nl]["outer_abs_mu"]; oz = entry["nulls"][nl]["outer_abs_z"]
        log(f"  NULL-{nl:2s}: inner|z| null {entry['nulls'][nl]['abs_z']['mean']:6.2f} "
            f"+- {entry['nulls'][nl]['abs_z']['sd']:5.2f} (p99 {entry['nulls'][nl]['abs_z']['p99']:6.2f}, "
            f"max {entry['nulls'][nl]['abs_z']['max']:6.2f}) | "
            f"|mu|: n_ge={om['n_null_ge_real']:4d}/{om['n_null']} p={om['p_onesided']:.5f} "
            f"zout={om['z_outer']:+7.2f} | |z|: n_ge={oz['n_null_ge_real']:4d}/{oz['n_null']} "
            f"p={oz['p_onesided']:.5f} zout={oz['z_outer']:+7.2f}")
    res[tag] = entry
    flush(res)


def main():
    units, move, t_end = P.load_units(P.NWB)
    log(f"\n######### supplement {time.strftime('%Y-%m-%d %H:%M:%S')} #########")
    log(f"loaded {len(units)} units, {sum(len(s) for s in units)} spikes")
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    block(units, t_end, 0.020, 1.0, ["A", "B1"], 2000, "S1_precision_20ms", res)
    block(units, t_end, 0.050, 2.5, ["P", "A", "B1", "B0"], 200, "S2_frozen_headline_50ms_sig2.5", res)
    log("\nsupplement done.")


if __name__ == "__main__":
    main()
