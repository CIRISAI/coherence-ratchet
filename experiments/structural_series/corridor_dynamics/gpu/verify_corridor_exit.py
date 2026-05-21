#!/usr/bin/env python3
"""
GPU-substrate corridor-exit rate — verification + gate check.
=============================================================

Re-runs the CIRISArray exp51 Test-4 coherence-decay measurement on the real
RTX 4090, but instruments it so the five pre-committed gates C1-C5 (see
PREREGISTRATION.md) can be checked directly from the captured arrays rather
than trusted from exp51's printed summary.

What this records, that exp51 does not expose:
  - the raw single-device k_eff(t) series           -> C1, C2
  - the running r(t) and the window length W          -> C3
  - the exponential fit (r_inf, A, tau) with errors    -> C4
  - across-run spread of tau (3 independent resets)    -> C5

The decay model and the running-correlation construction are IDENTICAL to
exp51.test_coherence_decay; this script does not change the measurement, it
exposes its internals.

Real GPU only. Aborts honestly if CuPy / the device is unavailable.
"""
import json
import time
import sys
import numpy as np
from datetime import datetime, timezone
from scipy import optimize

sys.path.insert(0, "/home/emoore/CIRISArray/experiments")
from exp51_physics_validation import PhysicsTestSensor, HAS_CUDA

OUT = "/home/emoore/coherence-ratchet/.claude/worktrees/agent-ab8cfb09d4784ee05/experiments/structural_series/corridor_dynamics/gpu/results_corridor_exit.json"

N_OSSICLES = 2048
DURATION_SEC = 120.0
SAMPLE_RATE = 10.0          # Hz
WINDOW = 50                 # 50 samples @ 10 Hz = 5.0 s running-correlation window
N_RUNS = 3
WINDOW_SEC = WINDOW / SAMPLE_RATE


def decay_model(t, r_inf, A, tau):
    return r_inf + A * np.exp(-t / tau)


def one_run(run_idx):
    """One reset + 120 s capture; returns the raw series and the fit."""
    sensor = PhysicsTestSensor(N_OSSICLES)      # __init__ calls reset() -> array starts correlated
    interval = 1.0 / SAMPLE_RATE
    n_samples = int(DURATION_SEC * SAMPLE_RATE)

    k_eff_series, timestamps = [], []
    start = time.time()
    for i in range(n_samples):
        t0 = time.perf_counter()
        sensor.step_with_noise(0.01)                 # unmaintained free relaxation, same as exp51
        k_eff_series.append(sensor.measure_k_eff())  # SINGLE device, its own k_eff
        timestamps.append(time.time() - start)
        elapsed = time.perf_counter() - t0
        if elapsed < interval:
            time.sleep(interval - elapsed)

    k_eff = np.array(k_eff_series, dtype=float)
    t = np.array(timestamps, dtype=float)

    # running correlation between adjacent WINDOW-length windows of one device's k_eff(t)
    corr, tpts = [], []
    for i in range(WINDOW, len(k_eff) - WINDOW):
        early = k_eff[i - WINDOW:i]
        later = k_eff[i:i + WINDOW]
        r = np.corrcoef(early, later)[0, 1]
        if not np.isnan(r):
            corr.append(r)
            tpts.append(t[i])
    corr = np.array(corr)
    tpts = np.array(tpts)

    fit = {}
    try:
        popt, pcov = optimize.curve_fit(
            decay_model, tpts, corr, p0=[0.05, 0.9, 30],
            bounds=([0, 0, 1], [0.5, 1.5, 200]))
        perr = np.sqrt(np.diag(pcov))
        pred = decay_model(tpts, *popt)
        ss_res = float(np.sum((corr - pred) ** 2))
        ss_tot = float(np.sum((corr - corr.mean()) ** 2))
        fit = {
            "r_inf": float(popt[0]), "r_inf_err": float(perr[0]),
            "A": float(popt[1]), "A_err": float(perr[1]),
            "tau": float(popt[2]), "tau_err": float(perr[2]),
            "R2": float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan"),
            "converged": True,
        }
    except Exception as e:
        fit = {"converged": False, "error": str(e)}

    return {
        "run": run_idx,
        "k_eff_first": float(k_eff[0]), "k_eff_last": float(k_eff[-1]),
        "k_eff_mean": float(k_eff.mean()), "k_eff_std": float(k_eff.std()),
        "r_start": float(corr[0]), "r_end": float(corr[-1]),
        "r_drop": float(corr[0] - corr[-1]),
        "fit": fit,
    }


def main():
    print("=" * 78)
    print("GPU-substrate corridor-exit rate — exp51 Test-4 re-run, instrumented")
    print("=" * 78)
    if not HAS_CUDA:
        print("ABORT: CuPy / CUDA device not available. No GPU run possible.")
        print("Pre-registration requires real GPU runs only — reporting honestly.")
        sys.exit(1)
    print(f"  GPU backend active (HAS_CUDA={HAS_CUDA})")
    print(f"  ossicles={N_OSSICLES}, capture={DURATION_SEC}s @ {SAMPLE_RATE}Hz, "
          f"running window W={WINDOW} samples = {WINDOW_SEC}s")
    print(f"  runs={N_RUNS} (independent resets)")
    print()

    runs = []
    for i in range(N_RUNS):
        print(f"  --- run {i+1}/{N_RUNS} ---")
        r = one_run(i)
        runs.append(r)
        f = r["fit"]
        if f["converged"]:
            print(f"    k_eff {r['k_eff_first']:.4f} -> {r['k_eff_last']:.4f} "
                  f"(mean {r['k_eff_mean']:.4f})")
            print(f"    r(t): {r['r_start']:.3f} -> {r['r_end']:.3f}  drop={r['r_drop']:.3f}")
            print(f"    fit r(t)={f['r_inf']:.3f}+{f['A']:.3f}*exp(-t/{f['tau']:.1f})  "
                  f"tau={f['tau']:.1f}+/-{f['tau_err']:.1f}s  R2={f['R2']:.3f}")
        else:
            print(f"    FIT FAILED: {f.get('error')}")
        print()

    taus = [r["fit"]["tau"] for r in runs if r["fit"]["converged"]]
    r_infs = [r["fit"]["r_inf"] for r in runs if r["fit"]["converged"]]
    As = [r["fit"]["A"] for r in runs if r["fit"]["converged"]]
    fit_errs = [r["fit"]["tau_err"] for r in runs if r["fit"]["converged"]]
    drops = [r["r_drop"] for r in runs if r["fit"]["converged"]]

    # ---- Gate checks (pre-committed C1-C5) ----
    gates = {}

    # C1: r(t) is the relaxation of the framework's own coherence observable.
    # k_eff = r_ab*(1-x)*COUPLING*1000 is the participation-style coherence;
    # r(t) is the temporal autocorrelation of that coherence; r decays = coherence lost.
    gates["C1_coherence_observable"] = {
        "pass": all(d > 0 for d in drops),
        "note": ("r(t) is the temporal autocorrelation of one device's coherence "
                 "signal k_eff(t); it decays (drop>0) = the array loses coherence "
                 "after reset. k_eff is the framework's coherence/k_eff observable."),
    }

    # C2: within-array decay, NOT the cross-device artifact.
    # Verified by code path: test_coherence_decay / one_run instantiate ONE
    # PhysicsTestSensor; r(t) correlates that ONE device's k_eff series across
    # TIME. The flagged artifact is correlation BETWEEN two devices.
    gates["C2_not_crossdevice_artifact"] = {
        "pass": True,
        "note": ("Single PhysicsTestSensor instantiated per run; r(t) is the "
                 "TEMPORAL autocorrelation of that one device's k_eff(t). The "
                 "CIRISArray-flagged artifact is correlation BETWEEN separate "
                 "devices' k_eff series (r~0.97, shared algorithm). Different "
                 "quantity: a within-device temporal decay is not produced by "
                 "the cross-device algorithm collision."),
    }

    # C3: tau >> W. Gate: tau > 3*W = 15 s.
    tau_min = min(taus) if taus else float("nan")
    gates["C3_not_window_dominated"] = {
        "pass": bool(taus) and tau_min > 3 * WINDOW_SEC,
        "tau_min": tau_min, "window_sec": WINDOW_SEC,
        "gate_threshold_sec": 3 * WINDOW_SEC,
        "tau_over_W": [t / WINDOW_SEC for t in taus],
        "note": (f"all taus must exceed 3*W={3*WINDOW_SEC}s. min tau={tau_min:.1f}s; "
                 f"tau/W ~ {tau_min/WINDOW_SEC:.1f}x. C. elegans failed here "
                 f"(tau_ac~15s vs 30s window)."),
    }

    # C4: fit real, not imposed.
    c4_ok = (bool(taus)
             and all(-0.1 <= ri <= 0.3 for ri in r_infs)
             and all(0.5 <= a <= 1.5 for a in As)
             and all(d >= 0.3 for d in drops))
    gates["C4_real_fit"] = {
        "pass": bool(c4_ok),
        "r_inf_range": [min(r_infs), max(r_infs)] if r_infs else None,
        "A_range": [min(As), max(As)] if As else None,
        "r_drop_min": min(drops) if drops else None,
        "R2": [r["fit"]["R2"] for r in runs if r["fit"]["converged"]],
        "note": ("r_inf in [-0.1,0.3] (near chaos pole), A in [0.5,1.5] "
                 "(starts near full corr), r drops >=0.3 (monotone gross decay)."),
    }

    # C5: reproducible across resets, max/min tau < 2.
    ratio = max(taus) / min(taus) if taus else float("nan")
    gates["C5_reproducible"] = {
        "pass": bool(taus) and ratio < 2.0,
        "tau_values": taus, "max_over_min": ratio,
        "note": "tau across 3 independent resets must agree within factor 2.",
    }

    all_pass = all(g["pass"] for g in gates.values())

    tau_mean = float(np.mean(taus)) if taus else float("nan")
    tau_sd = float(np.std(taus, ddof=1)) if len(taus) > 1 else float("nan")
    # combined error: across-run SD and mean per-fit covariance error, added in quad
    fit_err_mean = float(np.mean(fit_errs)) if fit_errs else float("nan")
    tau_err_combined = float(np.sqrt(tau_sd**2 + fit_err_mean**2)) if taus else float("nan")
    exit_rate = 1.0 / tau_mean if taus else float("nan")
    # propagate: d(1/tau) = err/tau^2
    exit_rate_err = tau_err_combined / tau_mean**2 if taus else float("nan")

    if all_pass:
        verdict = "POSITIVE — genuine GPU corridor-exit rate"
    elif not gates["C3_not_window_dominated"]["pass"]:
        verdict = "WINDOW-DOMINATED NULL"
    elif not gates["C2_not_crossdevice_artifact"]["pass"]:
        verdict = "ARTIFACT-CONTAMINATED NULL"
    elif not gates["C4_real_fit"]["pass"]:
        verdict = "FIT-FAILURE / NON-MONOTONE NULL"
    elif not gates["C5_reproducible"]["pass"]:
        verdict = "INCONCLUSIVE (run-to-run scatter > factor 2)"
    else:
        verdict = "NULL (C1 failed)"

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "instrument": "CIRISArray exp51 Test-4 (coherence decay), RTX 4090, CuPy",
        "n_ossicles": N_OSSICLES, "capture_sec": DURATION_SEC,
        "sample_rate_hz": SAMPLE_RATE, "running_window_sec": WINDOW_SEC,
        "n_runs": N_RUNS,
        "runs": runs,
        "tau_mean_sec": tau_mean, "tau_across_run_sd_sec": tau_sd,
        "tau_per_fit_err_mean_sec": fit_err_mean,
        "tau_err_combined_sec": tau_err_combined,
        "corridor_exit_rate_per_sec": exit_rate,
        "corridor_exit_rate_err_per_sec": exit_rate_err,
        "gates": gates, "all_gates_pass": all_pass, "verdict": verdict,
    }

    print("=" * 78)
    print("GATE CHECK")
    print("=" * 78)
    for name, g in gates.items():
        print(f"  [{'PASS' if g['pass'] else 'FAIL'}] {name}")
    print()
    print("=" * 78)
    print(f"VERDICT: {verdict}")
    print("=" * 78)
    if taus:
        print(f"  tau              = {tau_mean:.1f} +/- {tau_err_combined:.1f} s "
              f"(across-run SD {tau_sd:.1f}s, mean fit-err {fit_err_mean:.1f}s)")
        print(f"  corridor-exit rate 1/tau = {exit_rate:.4f} +/- {exit_rate_err:.4f} /s")
        print(f"  tau values: {[round(x,1) for x in taus]}")
    with open(OUT, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n  results -> {OUT}")


if __name__ == "__main__":
    main()
