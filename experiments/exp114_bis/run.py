"""Exp 114-bis: clean dynamical-system test of the framework's β=1.09 claim.

Question: did Exp 114's β=1.09 emerge from the Kish dynamics, or was it an
artifact of GPU substrate noise on the CIRISArray rig?

This script replicates the Exp 114 measurement pattern on a clean
stochastic-dynamical model (no GPU, no kernel-timing observables), with the
statistics Exp 114 didn't do:

  - 50 control-parameter values (Exp 114: 9)
  - 30 trials per value (Exp 114: 5)
  - Bootstrap CI on β from 2000 resamples (Exp 114: no CI)
  - AIC comparison against alternative functional forms (Exp 114: no comparison)
  - Companion susceptibility-exponent γ measurement (Exp 114: not measured)

Model: N=16 all-to-all-coupled stochastic units (the simplest universality-
class testbed). Each unit obeys an Ornstein-Uhlenbeck-like SDE:

    dx_i = [-γ_relax · x_i + c · (x̄ - x_i)] dt + σ √dt · η_i

where x̄ = (1/N) Σ_j x_j is the mean field and η_i are i.i.d. standard
normal at each step. The control parameter is the coupling strength c
(analog of Exp 114's Lorenz dt sweep — varying coordination strength).

Measurement: at each step compute the instantaneous cross-unit correlation
r(t) = mean off-diagonal of the cross-unit correlation matrix over a sliding
window. Then k_eff(t) = N / (1 + r(t)·(N-1)). Sweep c, measure ρ as the
lag-1 autocorrelation of k_eff(t) over the trajectory, fit power law.

This matches Exp 114's measurement chain (sweep control parameter, measure
ρ_meas = AC1 of k_eff(t), fit ρ = A|c - c_c|^β + C) with the substrate
swapped out for a clean numerical model.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import optimize, stats

OUT_DIR = Path(__file__).parent
RESULTS_JSON = OUT_DIR / "results.json"

# --- Model parameters ---
N_UNITS = 16            # match CIRISArray rig
GAMMA_RELAX = 1.0       # local restoring rate
NOISE_SIGMA = 1.0       # per-unit noise amplitude
DT_SIM = 0.01           # integration timestep (held fixed)
T_BURNIN = 500          # steps discarded before measurement
T_MEASURE = 4000        # steps over which AC1 is computed
WINDOW = 40             # sliding window for instantaneous r(t)

# --- Sweep parameters ---
C_VALUES = np.linspace(0.0, 0.6, 50)  # 50 control values (Exp 114: 9)
N_TRIALS = 30                          # 30 trials per value (Exp 114: 5)

# --- Fit / bootstrap ---
N_BOOTSTRAP = 2000


def simulate_array(c: float, seed: int) -> np.ndarray:
    """Simulate the N-unit coupled OU array. Returns (T_MEASURE, N) trajectory."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, size=N_UNITS)
    sqrt_dt = np.sqrt(DT_SIM)
    coupling = c * DT_SIM
    decay = (1.0 - GAMMA_RELAX * DT_SIM)

    # burn-in
    for _ in range(T_BURNIN):
        xbar = x.mean()
        drift = decay * x + coupling * (xbar - x)
        x = drift + NOISE_SIGMA * sqrt_dt * rng.standard_normal(N_UNITS)

    # measurement
    traj = np.empty((T_MEASURE, N_UNITS))
    for t in range(T_MEASURE):
        xbar = x.mean()
        drift = decay * x + coupling * (xbar - x)
        x = drift + NOISE_SIGMA * sqrt_dt * rng.standard_normal(N_UNITS)
        traj[t] = x
    return traj


def compute_k_eff_trajectory(traj: np.ndarray, window: int = WINDOW) -> np.ndarray:
    """Compute k_eff(t) from instantaneous off-diagonal correlation over a
    sliding window. k_eff = N / (1 + r(t)(N-1)) — the Kish formula."""
    T, N = traj.shape
    n_pts = T - window
    k_eff = np.empty(n_pts)
    for t in range(n_pts):
        w = traj[t:t+window]  # (window, N)
        # demean per unit
        wm = w - w.mean(axis=0, keepdims=True)
        # correlation matrix via std-normalized covariance
        std = wm.std(axis=0, ddof=0) + 1e-12
        wn = wm / std
        corr = (wn.T @ wn) / window
        # average absolute off-diagonal
        mask = ~np.eye(N, dtype=bool)
        r = np.abs(corr[mask]).mean()
        # k_eff via Kish
        k_eff[t] = N / (1.0 + r * (N - 1))
    return k_eff


def ac1(x: np.ndarray) -> float:
    """Lag-1 autocorrelation, the same statistic Exp 114 used."""
    x = x - x.mean()
    s = x.std(ddof=0)
    if s == 0:
        return float("nan")
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def measure_rho(c: float, seed: int) -> dict:
    traj = simulate_array(c, seed)
    k_eff = compute_k_eff_trajectory(traj)
    r = abs(ac1(k_eff))
    return {
        "c": float(c),
        "seed": seed,
        "rho": r,
        "k_eff_mean": float(k_eff.mean()),
        "k_eff_var": float(k_eff.var()),
    }


def run_sweep() -> list[dict]:
    records = []
    t0 = time.time()
    for i, c in enumerate(C_VALUES):
        rhos = []
        for trial in range(N_TRIALS):
            seed = 10_000 + i * 1000 + trial
            r = measure_rho(c, seed)
            rhos.append(r["rho"])
        rec = {
            "c": float(c),
            "rho_mean": float(np.mean(rhos)),
            "rho_std":  float(np.std(rhos, ddof=1)),
            "rho_var":  float(np.var(rhos, ddof=1)),
            "n_trials": N_TRIALS,
            "rhos":     [float(x) for x in rhos],
        }
        records.append(rec)
        elapsed = time.time() - t0
        print(f"[{elapsed:7.1f}s] c={c:.4f}  rho_mean={rec['rho_mean']:.4f}  "
              f"rho_std={rec['rho_std']:.4f}  rho_var={rec['rho_var']:.6f}")
    return records


# --- Model fitting ---

def model_power(x, x_c, A, beta, C):
    return A * np.abs(x - x_c)**beta + C

def model_linear(x, m, b):
    return m * x + b

def model_exp(x, A, k, C):
    return A * np.exp(-k * x) + C

def model_sigmoid(x, A, x_c, k, C):
    return A / (1.0 + np.exp(k * (x - x_c))) + C


def fit_power(c_arr, rho_arr):
    p0 = [c_arr[np.argmin(np.abs(np.diff(rho_arr)))], 1.0, 1.0, rho_arr.min()]
    bounds = ([0.0, 0.001, 0.1, 0.0], [c_arr.max() * 1.5, 100, 4.0, 1.0])
    try:
        popt, pcov = optimize.curve_fit(model_power, c_arr, rho_arr,
                                        p0=p0, bounds=bounds, maxfev=20000)
        return popt, pcov
    except Exception as e:
        return None, str(e)


def fit_simple(model, c_arr, rho_arr, p0):
    try:
        popt, pcov = optimize.curve_fit(model, c_arr, rho_arr, p0=p0, maxfev=20000)
        return popt, pcov
    except Exception as e:
        return None, str(e)


def aic(rss: float, n: int, k_params: int) -> float:
    return n * np.log(rss / n) + 2 * k_params


def bootstrap_beta(c_arr, rho_arr_mat, n_bootstrap=N_BOOTSTRAP) -> dict:
    """Bootstrap β by resampling trials within each c, refitting each time.

    rho_arr_mat: shape (n_c, n_trials).
    """
    n_c, n_trials = rho_arr_mat.shape
    rng = np.random.default_rng(20260518)
    betas = []
    cc = []
    fails = 0
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n_trials, size=(n_c, n_trials))
        boot_rhos = np.take_along_axis(rho_arr_mat, idx, axis=1).mean(axis=1)
        popt, _ = fit_power(c_arr, boot_rhos)
        if popt is None:
            fails += 1
            continue
        betas.append(popt[2])
        cc.append(popt[0])
    betas = np.array(betas)
    cc = np.array(cc)
    return {
        "beta_median": float(np.median(betas)),
        "beta_mean":   float(betas.mean()),
        "beta_ci95":   [float(np.quantile(betas, 0.025)), float(np.quantile(betas, 0.975))],
        "beta_ci80":   [float(np.quantile(betas, 0.10)), float(np.quantile(betas, 0.90))],
        "beta_std":    float(betas.std(ddof=1)),
        "c_crit_median": float(np.median(cc)),
        "c_crit_ci95":   [float(np.quantile(cc, 0.025)), float(np.quantile(cc, 0.975))],
        "n_bootstrap": len(betas),
        "n_failed":    fails,
    }


def analyze(records: list[dict]) -> dict:
    c_arr = np.array([r["c"] for r in records])
    rho_means = np.array([r["rho_mean"] for r in records])
    rho_vars  = np.array([r["rho_var"] for r in records])
    rho_mat   = np.array([r["rhos"] for r in records])  # (n_c, n_trials)
    n = len(c_arr)

    # main power-law fit
    popt_pow, pcov_pow = fit_power(c_arr, rho_means)
    if popt_pow is None:
        return {"error": "power-law fit failed", "detail": pcov_pow}
    pred_pow = model_power(c_arr, *popt_pow)
    rss_pow = float(np.sum((rho_means - pred_pow) ** 2))
    r2_pow  = 1.0 - rss_pow / float(np.sum((rho_means - rho_means.mean()) ** 2))
    aic_pow = aic(rss_pow, n, 4)

    # alternative models
    popt_lin, _ = fit_simple(model_linear, c_arr, rho_means, [-1.0, rho_means[0]])
    pred_lin = model_linear(c_arr, *popt_lin) if popt_lin is not None else None
    rss_lin = float(np.sum((rho_means - pred_lin) ** 2)) if pred_lin is not None else float("inf")
    r2_lin  = 1.0 - rss_lin / float(np.sum((rho_means - rho_means.mean()) ** 2)) if pred_lin is not None else float("nan")
    aic_lin = aic(rss_lin, n, 2)

    popt_exp, _ = fit_simple(model_exp, c_arr, rho_means, [1.0, 1.0, rho_means.min()])
    pred_exp = model_exp(c_arr, *popt_exp) if popt_exp is not None else None
    rss_exp = float(np.sum((rho_means - pred_exp) ** 2)) if pred_exp is not None else float("inf")
    r2_exp  = 1.0 - rss_exp / float(np.sum((rho_means - rho_means.mean()) ** 2)) if pred_exp is not None else float("nan")
    aic_exp = aic(rss_exp, n, 3)

    popt_sig, _ = fit_simple(model_sigmoid, c_arr, rho_means,
                              [rho_means[0] - rho_means[-1], c_arr.mean(), 10.0, rho_means[-1]])
    pred_sig = model_sigmoid(c_arr, *popt_sig) if popt_sig is not None else None
    rss_sig = float(np.sum((rho_means - pred_sig) ** 2)) if pred_sig is not None else float("inf")
    r2_sig  = 1.0 - rss_sig / float(np.sum((rho_means - rho_means.mean()) ** 2)) if pred_sig is not None else float("nan")
    aic_sig = aic(rss_sig, n, 4)

    # bootstrap β
    boot = bootstrap_beta(c_arr, rho_mat)

    # susceptibility-exponent γ: χ(c) ~ |c - c_c|^(-γ), where χ ∝ Var(ρ).
    # Use bootstrap c_crit as a hint. Fit log(rho_var) ~ -γ log|c - c_c| over
    # the half-sweep nearer to c_c.
    c_c = popt_pow[0]
    mask = (rho_vars > 0) & (np.abs(c_arr - c_c) > 1e-3)
    log_dx = np.log(np.abs(c_arr[mask] - c_c))
    log_chi = np.log(rho_vars[mask])
    if log_dx.size >= 3:
        slope, intercept, r_val, _, _ = stats.linregress(log_dx, log_chi)
        gamma_est = -slope
        gamma_r2 = float(r_val ** 2)
    else:
        gamma_est = float("nan")
        gamma_r2 = float("nan")

    return {
        "n_c_values": n,
        "n_trials_per_c": rho_mat.shape[1],
        "main_fit_power_law": {
            "form": "rho = A * |c - c_c|^beta + C",
            "c_c": float(popt_pow[0]),
            "A": float(popt_pow[1]),
            "beta": float(popt_pow[2]),
            "C": float(popt_pow[3]),
            "r_squared": float(r2_pow),
            "AIC": float(aic_pow),
            "RSS": rss_pow,
        },
        "bootstrap_beta": boot,
        "alternatives": {
            "linear":  {"params": list(map(float, popt_lin)) if popt_lin is not None else None,
                         "r_squared": float(r2_lin), "AIC": float(aic_lin)},
            "exp":     {"params": list(map(float, popt_exp)) if popt_exp is not None else None,
                         "r_squared": float(r2_exp), "AIC": float(aic_exp)},
            "sigmoid": {"params": list(map(float, popt_sig)) if popt_sig is not None else None,
                         "r_squared": float(r2_sig), "AIC": float(aic_sig)},
        },
        "susceptibility_exponent_gamma": {
            "form": "log Var(rho) ~ -gamma * log|c - c_c|",
            "gamma": float(gamma_est),
            "r_squared_of_log_fit": gamma_r2,
            "n_points_used": int(mask.sum()),
        },
        "compare_to_exp114": {
            "exp114_beta_point": 1.0921,
            "exp114_r_squared": 0.9784,
            "exp114_n_points": 9,
            "exp114_n_trials_per_point": 5,
            "exp114_published_beta_CI": "NONE",
        },
    }


def main() -> int:
    print(f"Exp 114-bis: clean dynamical-system test of beta")
    print(f"  N={N_UNITS} units, c sweep over {len(C_VALUES)} values, "
          f"{N_TRIALS} trials each, {T_MEASURE} measurement steps each")
    print()
    records = run_sweep()
    summary = analyze(records)

    out = {
        "config": {
            "N_units": N_UNITS, "gamma_relax": GAMMA_RELAX, "noise_sigma": NOISE_SIGMA,
            "dt_sim": DT_SIM, "T_burnin": T_BURNIN, "T_measure": T_MEASURE,
            "window": WINDOW, "n_c_values": len(C_VALUES), "n_trials": N_TRIALS,
            "c_min": float(C_VALUES.min()), "c_max": float(C_VALUES.max()),
            "n_bootstrap": N_BOOTSTRAP,
        },
        "sweep": records,
        "analysis": summary,
    }
    with open(RESULTS_JSON, "w") as f:
        json.dump(out, f, indent=2)
    print()
    print(f"Wrote {RESULTS_JSON}")
    print()
    print("=== HEADLINE ===")
    if "error" in summary:
        print(summary)
        return 1
    mfp = summary["main_fit_power_law"]
    boot = summary["bootstrap_beta"]
    print(f"  beta point estimate (mean-curve fit): {mfp['beta']:.4f}")
    print(f"  bootstrap beta median: {boot['beta_median']:.4f}")
    print(f"  bootstrap beta 95% CI: [{boot['beta_ci95'][0]:.4f}, {boot['beta_ci95'][1]:.4f}]")
    print(f"  bootstrap beta 80% CI: [{boot['beta_ci80'][0]:.4f}, {boot['beta_ci80'][1]:.4f}]")
    print(f"  R^2 (power law): {mfp['r_squared']:.4f}")
    print(f"  R^2 (linear):    {summary['alternatives']['linear']['r_squared']:.4f}")
    print(f"  R^2 (exp):       {summary['alternatives']['exp']['r_squared']:.4f}")
    print(f"  R^2 (sigmoid):   {summary['alternatives']['sigmoid']['r_squared']:.4f}")
    print(f"  AIC power:  {mfp['AIC']:.2f}")
    print(f"  AIC linear: {summary['alternatives']['linear']['AIC']:.2f}")
    print(f"  AIC exp:    {summary['alternatives']['exp']['AIC']:.2f}")
    print(f"  AIC sigmoid:{summary['alternatives']['sigmoid']['AIC']:.2f}")
    g = summary["susceptibility_exponent_gamma"]
    print(f"  gamma (susceptibility exponent): {g['gamma']:.4f}  (R^2 of log fit: {g['r_squared_of_log_fit']:.3f})")
    print(f"  Exp 114 baseline: beta=1.0921, R^2=0.978 (n=9 points, 5 trials, no CI)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
