"""Exp 114-bis rig version: actual CIRISArray GPU Sentinel, expanded protocol.

Replicates the original Exp 114 measurement chain (CIRISArray
ciris_sentinel.Sentinel + step_and_measure_full + AC1 of k_eff) but with:

  - 50 dt values across [0.018, 0.034] (Exp 114: 9 values)
  - 30 trials per dt value (Exp 114: 5)
  - Bootstrap β CI from 2000 resamples (Exp 114: no CI)
  - AIC comparison against sigmoid / exp / linear (Exp 114: only power)
  - Susceptibility-exponent γ via Var(ρ) scaling

This is the apples-to-apples test of whether β = 1.09 holds on the actual
rig with proper statistics, and whether power-law beats sigmoid on AIC.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Import the actual CIRISArray Sentinel
sys.path.insert(0, "/home/emoore/CIRISArray")

import numpy as np
import cupy as cp
from scipy import optimize, stats

from ciris_sentinel import Sentinel, SentinelConfig

OUT = Path(__file__).parent / "results_rig.json"

DT_VALUES = np.linspace(0.018, 0.034, 50)  # Exp 114 used 0.018..0.034 step 0.002 (9 pts)
N_TRIALS  = 30                              # Exp 114: 5
N_SAMPLES = 100                             # Exp 114: 100 (kept same)
SAMPLE_SLEEP = 0.005                        # Exp 114 used time.sleep(0.005)

N_BOOTSTRAP = 2000


def measure_rho(dt: float, seed: int) -> float:
    """Run one trial: Sentinel with the given lorenz_dt, return AC1 of k_eff."""
    cp.random.seed(seed)
    config = SentinelConfig(lorenz_dt=float(dt))
    sentinel = Sentinel(config)
    k_effs = []
    for _ in range(N_SAMPLES):
        state = sentinel.step_and_measure_full(auto_reset=False)
        k_effs.append(state["k_eff"])
        time.sleep(SAMPLE_SLEEP)
    k_effs = np.array(k_effs)
    if np.std(k_effs) == 0 or not np.all(np.isfinite(k_effs)):
        return float("nan")
    r = np.corrcoef(k_effs[:-1], k_effs[1:])[0, 1]
    if not np.isfinite(r):
        return float("nan")
    return float(abs(r))


def run_sweep() -> list[dict]:
    records = []
    t0 = time.time()
    for i, dt in enumerate(DT_VALUES):
        rhos = []
        for trial in range(N_TRIALS):
            seed = 30_000 + i * 1000 + trial
            r = measure_rho(dt, seed)
            if np.isfinite(r):
                rhos.append(r)
        rec = {
            "dt": float(dt),
            "rho_mean": float(np.mean(rhos)) if rhos else float("nan"),
            "rho_std":  float(np.std(rhos, ddof=1)) if len(rhos) > 1 else float("nan"),
            "rho_var":  float(np.var(rhos, ddof=1)) if len(rhos) > 1 else float("nan"),
            "n_trials": len(rhos),
            "rhos":     [float(x) for x in rhos],
        }
        records.append(rec)
        el = time.time() - t0
        eta = el / (i + 1) * (len(DT_VALUES) - i - 1)
        print(f"[{el:8.1f}s] dt={dt:.4f}  rho_mean={rec['rho_mean']:.4f}  "
              f"rho_std={rec['rho_std']:.4f}  n={rec['n_trials']}  ETA={eta:.0f}s",
              flush=True)
        # checkpoint
        with open(OUT.with_suffix(".inprogress.json"), "w") as f:
            json.dump({"sweep": records, "config": _config_dict()}, f, indent=2)
    return records


def model_power(x, x_c, A, beta, C):
    return A * np.abs(x - x_c)**beta + C

def model_linear(x, m, b):
    return m * x + b

def model_exp(x, A, k, C):
    return A * np.exp(-k * x) + C

def model_sigmoid(x, A, x_c, k, C):
    return A / (1.0 + np.exp(k * (x - x_c))) + C


def fit_power(x, y):
    valid = np.isfinite(y)
    x, y = x[valid], y[valid]
    if len(x) < 5:
        return None
    p0 = [float(np.median(x)), float(y.max() - y.min()), 1.0, float(y.min())]
    bounds = ([x.min() - 0.005, 0.001, 0.1, 0.0],
              [x.max() + 0.005, 100.0, 4.0, 1.0])
    try:
        popt, _ = optimize.curve_fit(model_power, x, y, p0=p0, bounds=bounds, maxfev=20000)
        return popt
    except Exception:
        return None


def fit_simple(model, x, y, p0):
    valid = np.isfinite(y)
    x, y = x[valid], y[valid]
    if len(x) < len(p0) + 1:
        return None
    try:
        popt, _ = optimize.curve_fit(model, x, y, p0=p0, maxfev=20000)
        return popt
    except Exception:
        return None


def aic(rss: float, n: int, k_params: int) -> float:
    return n * np.log(rss / n) + 2 * k_params


def bootstrap_beta(x_arr, rho_mat, n_bootstrap=N_BOOTSTRAP) -> dict:
    rng = np.random.default_rng(20260518)
    betas, cs = [], []
    fails = 0
    n_x = len(x_arr)
    for _ in range(n_bootstrap):
        boot = np.zeros(n_x)
        for i in range(n_x):
            row = rho_mat[i]
            valid = ~np.isnan(row)
            if valid.sum() == 0:
                boot[i] = np.nan
                continue
            v = row[valid]
            idx = rng.integers(0, len(v), size=len(v))
            boot[i] = v[idx].mean()
        popt = fit_power(x_arr, boot)
        if popt is None:
            fails += 1
            continue
        cs.append(popt[0])
        betas.append(popt[2])
    betas = np.array(betas)
    cs = np.array(cs)
    return {
        "beta_median": float(np.median(betas)),
        "beta_mean":   float(betas.mean()),
        "beta_ci95":   [float(np.quantile(betas, 0.025)), float(np.quantile(betas, 0.975))],
        "beta_ci80":   [float(np.quantile(betas, 0.10)), float(np.quantile(betas, 0.90))],
        "beta_std":    float(betas.std(ddof=1)),
        "dt_c_median": float(np.median(cs)),
        "dt_c_ci95":   [float(np.quantile(cs, 0.025)), float(np.quantile(cs, 0.975))],
        "n_bootstrap": len(betas),
        "n_failed":    fails,
    }


def analyze(records) -> dict:
    x = np.array([r["dt"] for r in records])
    rho_means = np.array([r["rho_mean"] for r in records])
    rho_vars  = np.array([r["rho_var"]  for r in records])
    max_t = max(len(r["rhos"]) for r in records)
    rho_mat = np.full((len(records), max_t), np.nan)
    for i, r in enumerate(records):
        rho_mat[i, :len(r["rhos"])] = r["rhos"]

    popt_pow = fit_power(x, rho_means)
    if popt_pow is None:
        return {"error": "power-law fit failed"}
    pred = model_power(x, *popt_pow)
    rss = float(np.nansum((rho_means - pred) ** 2))
    n = int(np.sum(np.isfinite(rho_means)))
    r2_pow = 1.0 - rss / float(np.nansum((rho_means - np.nanmean(rho_means)) ** 2))
    aic_pow = aic(rss, n, 4)

    def alt(model, p0, k):
        popt = fit_simple(model, x, rho_means, p0)
        if popt is None:
            return None
        pred = model(x, *popt)
        rss = float(np.nansum((rho_means - pred) ** 2))
        r2 = 1.0 - rss / float(np.nansum((rho_means - np.nanmean(rho_means)) ** 2))
        return {"params": list(map(float, popt)), "r_squared": float(r2), "AIC": float(aic(rss, n, k))}

    alts = {
        "linear":  alt(model_linear, [-1.0, float(rho_means[0])], 2),
        "exp":     alt(model_exp,    [1.0, 1.0, float(np.nanmin(rho_means))], 3),
        "sigmoid": alt(model_sigmoid,
                       [float(np.nanmax(rho_means) - np.nanmin(rho_means)),
                        float(x.mean()), 200.0, float(np.nanmin(rho_means))], 4),
    }

    boot = bootstrap_beta(x, rho_mat)

    c_c = popt_pow[0]
    mask = (rho_vars > 0) & (np.abs(x - c_c) > 1e-4) & np.isfinite(rho_vars)
    if mask.sum() >= 5:
        log_dx = np.log(np.abs(x[mask] - c_c))
        log_chi = np.log(rho_vars[mask])
        slope, _, rv, _, _ = stats.linregress(log_dx, log_chi)
        gamma_est, gamma_r2 = -slope, float(rv ** 2)
    else:
        gamma_est, gamma_r2 = float("nan"), float("nan")

    return {
        "n_x_values": int(n),
        "main_fit_power_law": {
            "form": "rho = A * |dt - dt_c|^beta + C",
            "dt_c": float(popt_pow[0]),
            "A": float(popt_pow[1]),
            "beta": float(popt_pow[2]),
            "C": float(popt_pow[3]),
            "r_squared": float(r2_pow),
            "AIC": float(aic_pow),
        },
        "bootstrap_beta": boot,
        "alternatives": alts,
        "susceptibility_exponent_gamma": {
            "gamma": gamma_est, "r_squared_of_log_fit": gamma_r2,
            "n_points_used": int(mask.sum()),
        },
        "compare_to_exp114": {
            "exp114_beta_point": 1.0921,
            "exp114_r_squared": 0.9784,
            "exp114_dt_c": 0.03279,
            "exp114_A": 39.64,
            "exp114_C": 0.331,
            "exp114_n_points": 9,
            "exp114_n_trials": 5,
            "exp114_no_CI": True,
        },
    }


def _config_dict() -> dict:
    return {
        "n_dt": len(DT_VALUES),
        "n_trials_per_dt": N_TRIALS,
        "n_samples_per_trial": N_SAMPLES,
        "sample_sleep_s": SAMPLE_SLEEP,
        "dt_min": float(DT_VALUES.min()),
        "dt_max": float(DT_VALUES.max()),
        "n_bootstrap": N_BOOTSTRAP,
        "substrate": "CIRISArray GPU Sentinel (cupy) on RTX 4090",
    }


def main() -> int:
    print("Exp 114-bis RIG version")
    print(f"  GPU substrate: NVIDIA RTX 4090 Laptop, driver 580.142")
    print(f"  sweep: {len(DT_VALUES)} dt values [{DT_VALUES[0]:.4f}, {DT_VALUES[-1]:.4f}]")
    print(f"         {N_TRIALS} trials per dt, {N_SAMPLES} samples per trial")
    print(f"         estimated runtime: ~{len(DT_VALUES) * N_TRIALS * N_SAMPLES * SAMPLE_SLEEP / 60:.0f} min")
    print()
    records = run_sweep()
    summary = analyze(records)
    out = {"config": _config_dict(), "sweep": records, "analysis": summary}
    OUT.write_text(json.dumps(out, indent=2))
    print()
    print(f"Wrote {OUT}")
    print()
    if "error" in summary:
        print(summary)
        return 1
    m = summary["main_fit_power_law"]
    b = summary["bootstrap_beta"]
    print("=== HEADLINE ===")
    print(f"  beta point: {m['beta']:.4f}    (Exp 114: 1.0921)")
    print(f"  bootstrap beta median: {b['beta_median']:.4f}")
    print(f"  bootstrap beta 95% CI: [{b['beta_ci95'][0]:.4f}, {b['beta_ci95'][1]:.4f}]")
    print(f"  bootstrap beta 80% CI: [{b['beta_ci80'][0]:.4f}, {b['beta_ci80'][1]:.4f}]")
    print(f"  dt_c point: {m['dt_c']:.5f}    (Exp 114: 0.03279)")
    print(f"  bootstrap dt_c 95% CI: [{b['dt_c_ci95'][0]:.5f}, {b['dt_c_ci95'][1]:.5f}]")
    print()
    print(f"  R^2 (power law): {m['r_squared']:.4f}    (Exp 114: 0.978)")
    print(f"  R^2 (linear):    {summary['alternatives']['linear']['r_squared']:.4f}")
    print(f"  R^2 (exp):       {summary['alternatives']['exp']['r_squared']:.4f}")
    print(f"  R^2 (sigmoid):   {summary['alternatives']['sigmoid']['r_squared']:.4f}")
    print()
    print(f"  AIC power:   {m['AIC']:.2f}")
    print(f"  AIC linear:  {summary['alternatives']['linear']['AIC']:.2f}")
    print(f"  AIC exp:     {summary['alternatives']['exp']['AIC']:.2f}")
    print(f"  AIC sigmoid: {summary['alternatives']['sigmoid']['AIC']:.2f}")
    print()
    g = summary["susceptibility_exponent_gamma"]
    print(f"  gamma (susceptibility): {g['gamma']:.4f}  (R^2 of log fit: {g['r_squared_of_log_fit']:.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
