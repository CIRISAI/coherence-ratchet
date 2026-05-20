"""Exp 114-bis Lorenz variant: replicate Exp 114's actual dynamical model.

Exp 114 swept the Lorenz integration timestep `dt` and measured the
temporal autocorrelation of a k_eff observable derived from a coupled
chaotic dynamical system. The first OU-based run (run.py) gave flat ρ
across c — confirming that β=1.09 is NOT a generic property of any
coupled coordinator. This script uses the *correct* model:

  N coupled Lorenz oscillators with mean-field coupling on x,
  integrated forward with Euler timestep `dt`, sweeping dt across
  the Exp 114 range [0.018, 0.034].

Each oscillator:
  dx/dt = σ(y - x) + ε·(x̄ - x)
  dy/dt = x·(ρ_L - z) - y
  dz/dt = x·y - β_L·z

The k_eff observable: window-averaged off-diagonal cross-unit correlation
on x, fed through the Kish formula. AC1 of k_eff(t) is the framework's
ρ (the autocorrelation that Exp 114 fits a power law to).

Full statistics this time:
  - 50 dt values (Exp 114: 9)
  - 30 trials per dt (Exp 114: 5)
  - Bootstrap β CI from 2000 resamples (Exp 114: no CI)
  - AIC vs alternative functional forms
  - Susceptibility-exponent γ via Var(ρ) scaling
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import optimize, stats

OUT = Path(__file__).parent / "results_lorenz.json"

N_UNITS = 16
SIGMA_L = 10.0     # Lorenz σ
RHO_L   = 28.0     # Lorenz ρ (chaotic regime)
BETA_L  = 8.0/3.0  # Lorenz β
COUPLE_EPS = 0.5   # mean-field coupling on x
WINDOW = 40        # sliding window for instantaneous correlation
T_BURNIN = 200
T_MEASURE = 2000

DT_VALUES = np.linspace(0.015, 0.036, 50)
N_TRIALS = 30
N_BOOTSTRAP = 2000


def simulate_lorenz_array(dt: float, seed: int) -> np.ndarray:
    """Return x-trajectory of shape (T_MEASURE, N_UNITS)."""
    rng = np.random.default_rng(seed)
    state = rng.normal(0, 5, size=(N_UNITS, 3))  # (N, 3) for x,y,z
    state[:, 2] = np.abs(state[:, 2]) + 10.0      # z > 0 to avoid pathological start

    def step(s, dt):
        x, y, z = s[:, 0], s[:, 1], s[:, 2]
        xbar = x.mean()
        dx = SIGMA_L * (y - x) + COUPLE_EPS * (xbar - x)
        dy = x * (RHO_L - z) - y
        dz = x * y - BETA_L * z
        return s + dt * np.stack([dx, dy, dz], axis=1)

    for _ in range(T_BURNIN):
        state = step(state, dt)

    traj = np.empty((T_MEASURE, N_UNITS))
    for t in range(T_MEASURE):
        state = step(state, dt)
        traj[t] = state[:, 0]
    return traj


def compute_k_eff_trajectory(traj: np.ndarray, window: int = WINDOW) -> np.ndarray:
    T, N = traj.shape
    n_pts = T - window
    k_eff = np.empty(n_pts)
    for t in range(n_pts):
        w = traj[t:t+window]
        wm = w - w.mean(axis=0, keepdims=True)
        std = wm.std(axis=0, ddof=0) + 1e-12
        wn = wm / std
        corr = (wn.T @ wn) / window
        mask = ~np.eye(N, dtype=bool)
        r = np.abs(corr[mask]).mean()
        k_eff[t] = N / (1.0 + r * (N - 1))
    return k_eff


def ac1(x: np.ndarray) -> float:
    x = x - x.mean()
    s = x.std(ddof=0)
    if s == 0:
        return float("nan")
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def measure_rho(dt: float, seed: int) -> float:
    traj = simulate_lorenz_array(dt, seed)
    if not np.all(np.isfinite(traj)):
        return float("nan")
    k = compute_k_eff_trajectory(traj)
    if not np.all(np.isfinite(k)):
        return float("nan")
    return abs(ac1(k))


def run_sweep() -> list[dict]:
    records = []
    t0 = time.time()
    for i, dt in enumerate(DT_VALUES):
        rhos = []
        for trial in range(N_TRIALS):
            seed = 20_000 + i * 1000 + trial
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
        print(f"[{el:7.1f}s] dt={dt:.4f}  rho_mean={rec['rho_mean']:.4f}  "
              f"rho_std={rec['rho_std']:.4f}  n={rec['n_trials']}")
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
        return None, "insufficient points"
    p0 = [x[np.argmax(np.abs(np.diff(y)))] if len(x) > 1 else x.mean(),
          float(y.max() - y.min()), 1.0, float(y.min())]
    bounds = ([x.min() - 0.005, 0.001, 0.1, 0.0],
              [x.max() + 0.005, 100, 4.0, 1.0])
    try:
        popt, pcov = optimize.curve_fit(model_power, x, y, p0=p0, bounds=bounds, maxfev=20000)
        return popt, pcov
    except Exception as e:
        return None, str(e)


def fit_simple(model, x, y, p0):
    valid = np.isfinite(y)
    x, y = x[valid], y[valid]
    if len(x) < len(p0) + 1:
        return None, "insufficient points"
    try:
        popt, _ = optimize.curve_fit(model, x, y, p0=p0, maxfev=20000)
        return popt, None
    except Exception as e:
        return None, str(e)


def aic(rss: float, n: int, k_params: int) -> float:
    return n * np.log(rss / n) + 2 * k_params


def bootstrap_beta(x_arr, rho_mat, n_bootstrap=N_BOOTSTRAP) -> dict:
    n_x, n_trials_max = rho_mat.shape
    rng = np.random.default_rng(20260518)
    betas, cs = [], []
    fails = 0
    for _ in range(n_bootstrap):
        # resample trials within each x
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
        popt, _ = fit_power(x_arr, boot)
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
        "x_crit_median": float(np.median(cs)),
        "x_crit_ci95":   [float(np.quantile(cs, 0.025)), float(np.quantile(cs, 0.975))],
        "n_bootstrap": len(betas),
        "n_failed":    fails,
    }


def analyze(records):
    x_arr = np.array([r["dt"] for r in records])
    rho_means = np.array([r["rho_mean"] for r in records])
    rho_vars  = np.array([r["rho_var"]  for r in records])
    # pad rhos to common length
    max_trials = max(len(r["rhos"]) for r in records)
    rho_mat = np.full((len(records), max_trials), np.nan)
    for i, r in enumerate(records):
        rho_mat[i, :len(r["rhos"])] = r["rhos"]

    popt_pow, _ = fit_power(x_arr, rho_means)
    if popt_pow is None:
        return {"error": "power-law fit failed"}
    pred_pow = model_power(x_arr, *popt_pow)
    rss_pow = float(np.nansum((rho_means - pred_pow) ** 2))
    r2_pow = 1.0 - rss_pow / float(np.nansum((rho_means - np.nanmean(rho_means)) ** 2))
    aic_pow = aic(rss_pow, np.sum(np.isfinite(rho_means)), 4)

    def alt(model, p0, k):
        popt, _ = fit_simple(model, x_arr, rho_means, p0)
        if popt is None:
            return None
        pred = model(x_arr, *popt)
        rss = float(np.nansum((rho_means - pred) ** 2))
        r2 = 1.0 - rss / float(np.nansum((rho_means - np.nanmean(rho_means)) ** 2))
        return {"params": list(map(float, popt)),
                "r_squared": float(r2),
                "AIC": float(aic(rss, np.sum(np.isfinite(rho_means)), k))}

    alts = {
        "linear":  alt(model_linear,  [-1.0, rho_means[0]], 2),
        "exp":     alt(model_exp,     [1.0, 1.0, np.nanmin(rho_means)], 3),
        "sigmoid": alt(model_sigmoid, [np.nanmax(rho_means)-np.nanmin(rho_means),
                                       x_arr.mean(), 50.0, np.nanmin(rho_means)], 4),
    }

    boot = bootstrap_beta(x_arr, rho_mat)

    # γ
    c_c = popt_pow[0]
    mask = (rho_vars > 0) & (np.abs(x_arr - c_c) > 1e-4) & np.isfinite(rho_vars)
    if mask.sum() >= 5:
        log_dx = np.log(np.abs(x_arr[mask] - c_c))
        log_chi = np.log(rho_vars[mask])
        slope, _, rv, _, _ = stats.linregress(log_dx, log_chi)
        gamma_est, gamma_r2 = -slope, float(rv**2)
    else:
        gamma_est, gamma_r2 = float("nan"), float("nan")

    return {
        "n_x_values": len(x_arr),
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
        },
    }


def main() -> int:
    print(f"Exp 114-bis (Lorenz model)")
    print(f"  N={N_UNITS} Lorenz oscillators, dt sweep {DT_VALUES[0]:.3f}..{DT_VALUES[-1]:.3f}")
    print(f"  {len(DT_VALUES)} dt values x {N_TRIALS} trials, T_meas={T_MEASURE}")
    print()
    records = run_sweep()
    summary = analyze(records)
    out = {
        "config": {"N_units": N_UNITS, "sigma_L": SIGMA_L, "rho_L": RHO_L,
                   "beta_L": BETA_L, "couple_eps": COUPLE_EPS, "window": WINDOW,
                   "T_burnin": T_BURNIN, "T_measure": T_MEASURE,
                   "n_dt": len(DT_VALUES), "n_trials": N_TRIALS,
                   "n_bootstrap": N_BOOTSTRAP},
        "sweep": records,
        "analysis": summary,
    }
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
    print(f"  bootstrap dt_c 95% CI: [{b['x_crit_ci95'][0]:.5f}, {b['x_crit_ci95'][1]:.5f}]")
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
