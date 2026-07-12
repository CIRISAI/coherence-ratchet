#!/usr/bin/env python3
"""
BET 7 — third-law ceiling: maintainable (capacity) sigma collapses ∝(1−ρ) under
fixed N1 actuation budget P. Frozen protocol in DECISIONS.md. Real jitter bath.
"""
import json, os, time
import numpy as np
import apparatus as ap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results.json")
DT, K, P = 0.01, 8, 1.0
RHOS = [0.10, 0.20, 0.30, 0.43, 0.50, 0.60, 0.70, 0.80, 0.90]
R, BURN, MEAS = 256, 800, 2000
BOOT_SEED = 20260711


def load():
    return json.load(open(OUT)) if os.path.exists(OUT) else {}


def flush(res):
    json.dump(res, open(OUT, "w"), indent=2, default=float)


def run():
    res = load()
    t0 = time.perf_counter()
    jit = ap.JitterSource()
    b7 = {"bet": 7, "dt": DT, "k": K, "P": P, "R": R,
          "caveat": "C3 (DECISIONS.md): under N1 the collapse exponent is analytically 1; "
          "bench MEASURES sigma_hat (capacity, optimal-Q at budget P) on the real-jitter "
          "trajectory and checks it reproduces the collapse with no anomalous high-rho growth.",
          "sweep": []}
    res["bet7"] = b7; flush(res)

    for rho in RHOS:
        Q, sig_an = ap.optimal_Q_N1(rho, K, P)
        B, C, D, _ = ap.build_drift(rho, K, Q=Q)
        X0 = ap.steady_state_sample(C, R, K, jit)
        # burn-in (discard), then measure
        burn = ap.integrate(B, D, X0, jit, n_steps=BURN, dt=DT, R=R, k=K, record_rho=True)
        meas = ap.integrate(B, D, burn["X"], jit, n_steps=MEAS, dt=DT, R=R, k=K,
                            accum_heat=True, record_rho=True)
        rho_hat = float(np.mean(meas["rho_t"][-500:]))
        keff = ap.keff_from_rho(rho_hat, K)
        # per-replica sigma for a CI
        spr = meas["sigma_hat_per_replica"]
        rng = np.random.default_rng(BOOT_SEED)
        boot = [np.mean(spr[rng.integers(0, len(spr), len(spr))]) for _ in range(500)]
        row = dict(rho_target=rho, rho_hat=rho_hat, keff=keff,
                   sigma_hat=meas["sigma_hat"], sigma_analytic=sig_an,
                   sigma_hat_ci=[float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
                   ratio_measured_over_analytic=meas["sigma_hat"] / sig_an,
                   holdable=bool(abs(rho_hat - rho) < 0.06 and np.isfinite(meas["sigma_hat"])),
                   one_minus_rho=1 - rho)
        b7["sweep"].append(row)
        res["bet7"] = b7; flush(res)
        print(f"    rho={rho:.2f} rho_hat={rho_hat:.3f} keff={keff:.2f} "
              f"sigma_hat={meas['sigma_hat']:.4f} (analytic {sig_an:.4f}, "
              f"ratio {row['ratio_measured_over_analytic']:.2f}) hold={row['holdable']}")

    # fit exponent beta in sigma = A (1-rho)^beta  (log-log), jackknife CI
    om = np.array([r["one_minus_rho"] for r in b7["sweep"]])
    sg = np.array([r["sigma_hat"] for r in b7["sweep"]])
    good = sg > 0
    lx, ly = np.log(om[good]), np.log(sg[good])
    beta = float(np.polyfit(lx, ly, 1)[0])         # slope of log sigma vs log(1-rho)
    # jackknife
    betas = []
    idx = np.arange(len(lx))
    for i in idx:
        j = idx != i
        betas.append(np.polyfit(lx[j], ly[j], 1)[0])
    beta_se = float(np.std(betas) * np.sqrt(len(idx) - 1))
    monotone = all(b7["sweep"][i]["sigma_hat"] >= b7["sweep"][i + 1]["sigma_hat"] - 1e-6
                   for i in range(len(b7["sweep"]) - 1))
    collapse = b7["sweep"][-1]["sigma_hat"] < b7["sweep"][0]["sigma_hat"]
    if not collapse or beta <= 0:
        verdict = "KILL"
    elif 0.6 <= beta <= 1.4 and monotone:
        verdict = "PASS"
    else:
        verdict = "AMBIGUOUS"
    b7["exponent_beta"] = beta
    b7["exponent_beta_se"] = beta_se
    b7["monotone_collapse"] = bool(monotone)
    b7["collapses_pole_below_floor"] = bool(collapse)
    b7["verdict"] = verdict
    b7["verdict_detail"] = (f"beta={beta:.3f}+/-{beta_se:.3f} (predicted 1). "
                            f"monotone={monotone}, sigma(0.9)<sigma(0.1)={collapse}. "
                            f"PASS if collapse & beta in [0.6,1.4] & monotone; "
                            f"KILL if flat/increasing (beta<=0).")
    b7["wall_sec"] = time.perf_counter() - t0
    b7["n_jitter_normals"] = jit.n_normals
    res["bet7"] = b7; flush(res)
    print(f"\n[bet7] beta={beta:.3f}+/-{beta_se:.3f}  monotone={monotone}  "
          f"collapse={collapse}  VERDICT: {verdict}  wall={b7['wall_sec']:.0f}s")


if __name__ == "__main__":
    run()
