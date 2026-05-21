"""
C. elegans corridor relaxation rate — condition 2, the C. elegans angle.
========================================================================

The framework (Piece 2, dρ/dt = α − γM; Claim 1, the corridor) asserts a
DYNAMICS for the within-rung correlation ρ. Every prior measurement — including
v15_celegans — measured only the STATIC ρ. This script measures the corridor's
local RATE CONSTANT: how fast ρ(t) relaxes back toward its mean after a
fluctuation, from real C. elegans whole-brain calcium-imaging time series.

Data: Kato et al. 2015, Cell 163:656 — the canonical whole-brain imaging
dataset — via the qsimeon/celegans_neural_data aggregation. 12 worms.

Pipeline is fixed by PREREGISTRATION.md (committed before this script ran):
  1. ρ(t) = Kish-inverted k_eff on a 30 s sliding window of the neuron×time
     covariance.
  2. relaxation rate from (2a) autocorrelation e-folding time τ_ac and
     (2b) OU mean-reversion coefficient θ.
  3. dimensionless: rate ÷ global-brain-state cycle period T_global (PC1
     spectral peak).
  4. controls: 200 phase-randomised surrogates, window-length sweep
     {20,30,45}s, across-worm spread; all 12 worms, no dropping.

Real data only. Honest nulls. Error bars reported.
"""
import functools
import json
import os
from pathlib import Path

# single-threaded numpy: the per-window covariances are small matrices, and
# BLAS thread oversubscription makes them dramatically SLOWER. Parallelism is
# instead taken across worms via a process pool below.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy.signal import welch

print = functools.partial(print, flush=True)
HERE = Path(__file__).parent

DATA = HERE / "data" / "kato2015_whole_brain.parquet"
WINDOWS_SEC = [20.0, 30.0, 45.0]   # window-length sweep
W_HEADLINE = 30.0                  # headline window
N_SURROGATE = 200
GLOBAL_BAND = (1 / 300.0, 1 / 8.0)  # Hz search band for the global cycle


# ----------------------------------------------------------------------
# corridor observable
# ----------------------------------------------------------------------
def keff_rho(window):
    """k_eff (participation ratio) and Kish ρ of an (N x W) window.

    Covariance over time within the window, neurons as variables.
    k_eff = (Σλ)²/Σλ²; ρ = (N/k_eff − 1)/(N − 1) inverting the Kish identity
    k_eff = N/(1 + ρ(N−1)).

    The participation ratio is computed via the trace identities
    Σλ = tr(C) and Σλ² = tr(C²) = ||C||_F² — these hold exactly for the
    (PSD) covariance matrix, so k_eff = tr(C)² / ||C||_F² is identical to
    the eigenvalue form (Σλ)²/Σλ², and needs no eigendecomposition.
    Verified numerically to identical to 6 decimals against eigvalsh.
    """
    N = window.shape[0]
    Wc = window - window.mean(1, keepdims=True)
    W = window.shape[1]
    C = (Wc @ Wc.T) / (W - 1)                # N x N covariance over the window
    tr = np.trace(C)
    fro2 = np.dot(C.ravel(), C.ravel())      # ||C||_F^2 = Σλ²
    if tr <= 0 or fro2 <= 0:
        return 1.0, 1.0
    k_eff = (tr * tr) / fro2
    rho = (N / k_eff - 1.0) / (N - 1.0)
    return float(k_eff), float(rho)


def rho_trajectory(X, W):
    """ρ(t) over a sliding window of W samples, step 1 sample."""
    N, T = X.shape
    out = np.empty(T - W)
    for t in range(T - W):
        _, out[t] = keff_rho(X[:, t:t + W])
    return out


# ----------------------------------------------------------------------
# relaxation-rate estimators
# ----------------------------------------------------------------------
def acf(x, maxlag):
    """Biased autocorrelation function of mean-subtracted x, lags 0..maxlag."""
    x = x - x.mean()
    n = len(x)
    v = np.dot(x, x)
    if v <= 0:
        return np.zeros(maxlag + 1)
    out = np.empty(maxlag + 1)
    for k in range(maxlag + 1):
        out[k] = np.dot(x[:n - k], x[k:]) / v
    return out


def tau_ac(x, dt):
    """(2a) autocorrelation e-folding time, in seconds.

    Fit ACF(lag)=exp(−lag/τ) on lags up to the first zero-crossing (capped at
    T/4). Returns (tau_ac_seconds, tau_int_seconds, fit_maxlag_samples).
    tau_int = 1 + 2 Σ_{lag>0} ACF, summed to first zero-crossing — fit-free.
    """
    n = len(x)
    maxlag = n // 4
    a = acf(x, maxlag)
    # first zero crossing
    zc = np.where(a <= 0)[0]
    fit_lag = int(zc[0]) if len(zc) else maxlag
    fit_lag = max(fit_lag, 2)
    # integrated AC time (fit-free), to first zero crossing
    tau_int = 1.0 + 2.0 * a[1:fit_lag].sum()
    # exponential fit via log-linear regression on the positive part
    lags = np.arange(fit_lag)
    pos = a[:fit_lag]
    mask = pos > 1e-6
    if mask.sum() >= 3:
        slope, _ = np.polyfit(lags[mask], np.log(pos[mask]), 1)
        tau_samples = -1.0 / slope if slope < 0 else np.nan
    else:
        tau_samples = np.nan
    return (tau_samples * dt if np.isfinite(tau_samples) else np.nan,
            tau_int * dt, fit_lag)


def ou_theta(x, dt):
    """(2b) OU mean-reversion rate θ (1/s).

    dρ = −θ(ρ−ρ̄)dt + σdW.  Regress Δρ on (ρ−ρ̄); slope = −θ·dt.
    """
    xm = x - x.mean()
    dx = np.diff(x)
    slope, _ = np.polyfit(xm[:-1], dx, 1)
    theta = -slope / dt
    return float(theta)


# ----------------------------------------------------------------------
# intrinsic timescale
# ----------------------------------------------------------------------
def global_cycle_period(X, dt):
    """Dominant period of the global brain-state dynamics (PC1), in seconds.

    PC1 of the whole-brain neuron×time matrix; Welch periodogram; peak
    frequency in GLOBAL_BAND. Returns (T_global_seconds, peak_ok_bool).
    """
    Xc = X - X.mean(axis=1, keepdims=True)
    # PC1 via SVD of the (time x neuron) matrix
    u, s, vt = np.linalg.svd(Xc.T, full_matrices=False)
    pc1 = u[:, 0] * s[0]
    nper = min(len(pc1), max(256, len(pc1) // 4))
    f, P = welch(pc1, fs=1.0 / dt, nperseg=nper)
    band = (f >= GLOBAL_BAND[0]) & (f <= GLOBAL_BAND[1])
    if not band.any():
        return np.nan, False
    fb, Pb = f[band], P[band]
    fpeak = fb[np.argmax(Pb)]
    # peak_ok: the in-band peak stands above the in-band median
    peak_ok = Pb.max() > 3.0 * np.median(Pb)
    return (1.0 / fpeak, bool(peak_ok))


# ----------------------------------------------------------------------
# surrogates
# ----------------------------------------------------------------------
def phase_randomise(X, rng):
    """Independently phase-randomise each neuron's trace (preserves each
    neuron's power spectrum, destroys cross-neuron structure)."""
    N, T = X.shape
    F = np.fft.rfft(X, axis=1)
    nf = F.shape[1]
    phases = rng.uniform(0, 2 * np.pi, size=(N, nf))
    phases[:, 0] = 0.0
    if T % 2 == 0:
        phases[:, -1] = 0.0
    Fs = np.abs(F) * np.exp(1j * phases)
    return np.fft.irfft(Fs, n=T, axis=1)


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def load_kato():
    df = pd.read_parquet(DATA)
    worms = {}
    for w, g in df.groupby("worm"):
        X = np.array([np.asarray(c, float) for c in g["calcium_data"]])
        t = np.asarray(g["time_in_seconds"].iloc[0], float)
        dt = float(np.median(np.diff(t)))
        # drop any degenerate (constant) neurons
        good = X.std(axis=1) > 1e-9
        worms[w] = (X[good], dt)
    return worms


def analyse_worm(X, dt, W_sec, seed):
    """Full per-worm pipeline at one window length. Returns a dict.

    `seed` makes the surrogate draw reproducible inside each pool worker.
    """
    wrng = np.random.default_rng(seed)
    W = int(round(W_sec / dt))
    rho = rho_trajectory(X, W)
    tac, tint, fit_lag = tau_ac(rho, dt)
    theta = ou_theta(rho, dt)
    Tg, peak_ok = global_cycle_period(X, dt)
    # surrogate null on τ_ac and θ
    sur_tac, sur_theta = [], []
    for _ in range(N_SURROGATE):
        Xs = phase_randomise(X, wrng)
        rs = rho_trajectory(Xs, W)
        ts, _, _ = tau_ac(rs, dt)
        if np.isfinite(ts):
            sur_tac.append(ts)
        sur_theta.append(ou_theta(rs, dt))
    sur_tac = np.array(sur_tac)
    sur_theta = np.array(sur_theta)
    return dict(
        W_sec=W_sec, W_samples=W, dt=dt, n_neurons=int(X.shape[0]),
        T=int(X.shape[1]), n_rho=int(len(rho)),
        rho_mean=float(rho.mean()), rho_std=float(rho.std()),
        tau_ac_s=tac, tau_int_s=tint, fit_lag_samples=int(fit_lag),
        ou_theta_per_s=theta,
        k_relax_per_s=(1.0 / tac if np.isfinite(tac) and tac > 0 else np.nan),
        T_global_s=Tg, global_peak_ok=peak_ok,
        r_star=(Tg / tac if np.isfinite(tac) and np.isfinite(Tg) and tac > 0
                else np.nan),
        theta_star=(theta * Tg if np.isfinite(Tg) else np.nan),
        surrogate_tau_ac_mean=float(np.nanmean(sur_tac)) if len(sur_tac) else np.nan,
        surrogate_tau_ac_std=float(np.nanstd(sur_tac)) if len(sur_tac) else np.nan,
        surrogate_tau_ac_p95=float(np.nanpercentile(sur_tac, 95)) if len(sur_tac) else np.nan,
        surrogate_theta_mean=float(np.nanmean(sur_theta)),
        surrogate_theta_std=float(np.nanstd(sur_theta)),
        # positive-result gates: real τ_ac exceeds window AND surrogate 95th pct
        tau_exceeds_window=bool(np.isfinite(tac) and tac > W_sec),
        tau_exceeds_surrogate=bool(np.isfinite(tac) and len(sur_tac) and
                                   tac > np.nanpercentile(sur_tac, 95)),
    )


def main():
    print("=" * 78)
    print("C. elegans corridor relaxation rate — Kato2015 whole-brain imaging")
    print("=" * 78)
    if not DATA.exists():
        print(f"DATA NOT ACCESSIBLE: {DATA} missing. Aborting (no fabrication).")
        return
    worms = load_kato()
    print(f"Loaded {len(worms)} Kato2015 worms.")
    for w, (X, dt) in sorted(worms.items()):
        print(f"  {w}: N={X.shape[0]} neurons, T={X.shape[1]}, dt={dt:.3f}s, "
              f"dur={X.shape[1]*dt:.0f}s")

    results = {"data_source": "Kato et al. 2015 (qsimeon/celegans_neural_data)",
               "n_surrogates": N_SURROGATE, "headline_window_sec": W_HEADLINE,
               "windows": {}}

    worm_list = sorted(worms.items())
    for wi, W_sec in enumerate(WINDOWS_SEC):
        print(f"\n{'='*78}\nWINDOW = {W_sec:.0f} s\n{'='*78}")
        per_worm = {}
        hdr = (f"{'worm':<9} {'rho_mean':>9} {'tau_ac/s':>9} {'theta/s':>9} "
               f"{'T_glob/s':>9} {'r*':>7} {'theta*':>8} {'sur_tau':>9} "
               f"{'>W':>4} {'>sur':>5}")
        print(hdr)
        # worms are independent — dispatch across a process pool. Each worker
        # gets a distinct, deterministic seed (window index, worm index).
        with ProcessPoolExecutor(max_workers=min(12, os.cpu_count() or 4)) as ex:
            futs = {ex.submit(analyse_worm, X, dt, W_sec, 20260521 + wi * 100 + i):
                    w for i, (w, (X, dt)) in enumerate(worm_list)}
            done = {}
            for fut in futs:
                done[futs[fut]] = fut.result()
        for w, _ in worm_list:
            r = done[w]
            per_worm[w] = r
            print(f"{w:<9} {r['rho_mean']:>9.3f} {r['tau_ac_s']:>9.2f} "
                  f"{r['ou_theta_per_s']:>9.4f} {r['T_global_s']:>9.1f} "
                  f"{r['r_star']:>7.2f} {r['theta_star']:>8.2f} "
                  f"{r['surrogate_tau_ac_mean']:>9.2f} "
                  f"{'Y' if r['tau_exceeds_window'] else 'n':>4} "
                  f"{'Y' if r['tau_exceeds_surrogate'] else 'n':>5}")

        # across-worm aggregates
        def agg(key, ok_only=False):
            v = [r[key] for r in per_worm.values()
                 if np.isfinite(r[key]) and (not ok_only or r["global_peak_ok"])]
            v = np.array(v, float)
            return v
        tac_v = agg("tau_ac_s")
        krelax_v = agg("k_relax_per_s")
        theta_v = agg("ou_theta_per_s")
        rstar_v = agg("r_star", ok_only=True)
        thetastar_v = agg("theta_star", ok_only=True)
        Tg_v = agg("T_global_s", ok_only=True)
        n_exc_w = sum(r["tau_exceeds_window"] for r in per_worm.values())
        n_exc_s = sum(r["tau_exceeds_surrogate"] for r in per_worm.values())

        print(f"\n  across-worm (N={len(per_worm)}):")
        print(f"    tau_ac      = {tac_v.mean():.2f} +/- {tac_v.std():.2f} s "
              f"  range [{tac_v.min():.2f}, {tac_v.max():.2f}]")
        print(f"    k_relax     = {krelax_v.mean():.4f} +/- {krelax_v.std():.4f} /s")
        print(f"    OU theta    = {theta_v.mean():.4f} +/- {theta_v.std():.4f} /s")
        print(f"    T_global    = {Tg_v.mean():.1f} +/- {Tg_v.std():.1f} s "
              f"(N={len(Tg_v)} with clear peak)")
        print(f"    r* = T_g/tau_ac = {rstar_v.mean():.2f} +/- {rstar_v.std():.2f}"
              f"  range [{rstar_v.min():.2f}, {rstar_v.max():.2f}]  (N={len(rstar_v)})")
        print(f"    theta* = theta*T_g = {thetastar_v.mean():.2f} +/- "
              f"{thetastar_v.std():.2f}  (N={len(thetastar_v)})")
        print(f"    gate: tau_ac > window in {n_exc_w}/{len(per_worm)} worms;"
              f"  tau_ac > surrogate-p95 in {n_exc_s}/{len(per_worm)} worms")

        results["windows"][f"{W_sec:.0f}s"] = {
            "per_worm": per_worm,
            "aggregate": {
                "tau_ac_s_mean": float(tac_v.mean()), "tau_ac_s_std": float(tac_v.std()),
                "tau_ac_s_range": [float(tac_v.min()), float(tac_v.max())],
                "k_relax_per_s_mean": float(krelax_v.mean()),
                "k_relax_per_s_std": float(krelax_v.std()),
                "ou_theta_per_s_mean": float(theta_v.mean()),
                "ou_theta_per_s_std": float(theta_v.std()),
                "T_global_s_mean": float(Tg_v.mean()), "T_global_s_std": float(Tg_v.std()),
                "n_with_clear_peak": int(len(Tg_v)),
                "r_star_mean": float(rstar_v.mean()), "r_star_std": float(rstar_v.std()),
                "r_star_range": [float(rstar_v.min()), float(rstar_v.max())],
                "r_star_n": int(len(rstar_v)),
                "theta_star_mean": float(thetastar_v.mean()),
                "theta_star_std": float(thetastar_v.std()),
                "n_tau_exceeds_window": int(n_exc_w),
                "n_tau_exceeds_surrogate": int(n_exc_s),
            },
        }

    # ---- verdict ----
    hl = results["windows"][f"{W_HEADLINE:.0f}s"]["aggregate"]
    print(f"\n{'='*78}\nVERDICT (headline window {W_HEADLINE:.0f} s)\n{'='*78}")
    n_worms = len(worms)
    window_dominated = hl["n_tau_exceeds_window"] < n_worms / 2
    surrogate_null = hl["n_tau_exceeds_surrogate"] < n_worms / 2
    rstar_cv = hl["r_star_std"] / hl["r_star_mean"] if hl["r_star_mean"] else np.inf
    # W-stability
    rstars = [results["windows"][f"{w:.0f}s"]["aggregate"]["r_star_mean"]
              for w in WINDOWS_SEC]
    w_stable = (np.std(rstars) / np.mean(rstars)) < 0.5 if np.mean(rstars) else False

    if window_dominated:
        verdict = ("WINDOW-DOMINATED NULL: tau_ac does not exceed the window in "
                   "a majority of worms. The observable is window-correlated; "
                   "no relaxation rate is claimed.")
    elif surrogate_null:
        verdict = ("SURROGATE NULL: tau_ac is inside the phase-randomised "
                   "surrogate distribution. rho(t)-dynamics is not "
                   "distinguishable from windowed independent noise.")
    elif rstar_cv > 1.0 or not w_stable:
        verdict = (f"INCONCLUSIVE: r* spread is wide (CV={rstar_cv:.2f}) or "
                   f"W-unstable. Reported with error bars; no headline number.")
    else:
        verdict = "POSITIVE: a corridor relaxation rate is measured."
    results["verdict"] = verdict
    results["w_stability_rstar_means"] = {f"{w:.0f}s": rstars[i]
                                          for i, w in enumerate(WINDOWS_SEC)}
    print(verdict)
    print(f"\n  Corridor relaxation rate (headline):")
    print(f"    tau_ac        = {hl['tau_ac_s_mean']:.2f} +/- {hl['tau_ac_s_std']:.2f} s")
    print(f"    k_relax       = {hl['k_relax_per_s_mean']:.4f} +/- "
          f"{hl['k_relax_per_s_std']:.4f} /s")
    print(f"    T_global      = {hl['T_global_s_mean']:.1f} +/- "
          f"{hl['T_global_s_std']:.1f} s")
    print(f"    DIMENSIONLESS r* = T_global / tau_ac = "
          f"{hl['r_star_mean']:.2f} +/- {hl['r_star_std']:.2f}")
    print(f"    DIMENSIONLESS theta* = theta * T_global = "
          f"{hl['theta_star_mean']:.2f} +/- {hl['theta_star_std']:.2f}")
    print(f"  W-stability of r*: {results['w_stability_rstar_means']}")

    with open(HERE / "results_corridor_relaxation.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults: {HERE / 'results_corridor_relaxation.json'}")


if __name__ == "__main__":
    main()
