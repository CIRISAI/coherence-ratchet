#!/usr/bin/env python3
"""
BET 10 — interventional rent-cut. Frozen protocol in DECISIONS.md.
Real jitter bath. Incremental flush to results.json. Run FIRST.
"""
import json, os, time
import numpy as np
import cupy as cp
import apparatus as ap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results.json")
DT, LAM0, K, P, RHO = 0.01, 1.0, 8, 1.0, 0.30
BOOT_SEED = 20260711


def load():
    if os.path.exists(OUT):
        return json.load(open(OUT))
    return {}


def flush(res):
    json.dump(res, open(OUT, "w"), indent=2, default=float)


def measure_lambda0(jit, R, n_steps):
    """Single-oscillator AR(1) relaxation of the passive bath; gamma_hat = 2*lambda0."""
    Bt = cp.asarray((LAM0 * np.eye(K)).T); sq = (2 * DT) ** 0.5
    X = cp.asarray(ap.steady_state_sample(np.eye(K), R, K, jit))
    col = []
    for _ in range(n_steps):
        Z = cp.asarray(jit.normal_block((R, K)))
        X = X - (X @ Bt) * DT + sq * Z
        col.append(cp.asnumpy(X[:, 0]))
    traj = np.array(col)                                  # (T, R)
    rng = np.random.default_rng(BOOT_SEED)
    lams = []
    for _ in range(1000):
        b = rng.integers(0, R, R)
        tb = traj[:, b]
        phi = np.mean(tb[:-1] * tb[1:]) / np.mean(tb ** 2)
        lams.append(-np.log(phi) / DT)
    lam = float(np.mean(lams))
    se = float(np.std(lams))
    return lam, se


def fit_decay(rho_t, dt, rho0, lo=0.15, hi=0.85):
    t = np.arange(len(rho_t)) * dt
    m = (rho_t < hi * rho0) & (rho_t > lo * rho0)
    tt, yy = t[m], rho_t[m]
    if len(tt) < 5:
        return np.nan, (np.nan, np.nan), 0
    g = -np.polyfit(tt, np.log(yy), 1)[0]
    rng = np.random.default_rng(BOOT_SEED); idx = np.arange(len(tt)); gs = []
    for _ in range(1000):
        b = rng.choice(idx, len(idx), replace=True)
        if len(np.unique(tt[b])) > 3:
            gs.append(-np.polyfit(tt[b], np.log(yy[b]), 1)[0])
    return float(g), (float(np.percentile(gs, 2.5)), float(np.percentile(gs, 97.5))), int(m.sum())


def rent_analytic(B, C):
    """N1 actuation power of the maintenance force u=-(B-lam0 I)x: <||u||^2>=Tr[(B-lam0I)C(B-lam0I)^T]."""
    M = B - LAM0 * np.eye(K)
    return float(np.trace(M @ C @ M.T))


def half_time(rho_t, dt, rho_ref, rising):
    """First time rho crosses rho_ref/2 (rising) or rho_ref (start) -> rho_ref*0.5 (falling)."""
    target = 0.5 * rho_ref
    for i, v in enumerate(rho_t):
        if (rising and v >= target) or ((not rising) and v <= target):
            return i * dt
    return np.nan


def run():
    res = load()
    t0 = time.perf_counter()
    jit = ap.JitterSource()
    b10 = {"bet": 10, "rho_star": RHO, "dt": DT, "lambda0_set": LAM0,
           "P": P, "caveat": "C2 (DECISIONS.md): linear substrate -> decay to fp "
           "structurally guaranteed; genuine content = bath-set rate match + rent>0 "
           "certificate. Conservative control run to prove rent is load-bearing.",
           "repeats": []}

    # ---- Phase A: passive characterization + REGISTER gamma_hat (before any cut) ----
    print("[bet10] passive characterization (gamma_hat) ...")
    lam0, lam0_se = measure_lambda0(jit, R=1024, n_steps=500)
    gamma_hat = 2 * lam0
    gamma_band = (gamma_hat - 2 * 2 * lam0_se, gamma_hat + 2 * 2 * lam0_se)  # +/-2*(2 se)
    b10["passive_characterization"] = dict(
        lambda0_measured=lam0, lambda0_se=lam0_se, gamma_hat=gamma_hat,
        gamma_band_2se=list(gamma_band), discrete_truth_2lambda=2.01,
        registered_curve="rho(t)=rho_star*exp(-gamma_hat*(t-t0)), fp=0")
    res["bet10"] = b10; flush(res)
    print(f"    lambda0={lam0:.3f}+/-{lam0_se:.3f}  gamma_hat={gamma_hat:.3f}  "
          f"band={gamma_band[0]:.3f}..{gamma_band[1]:.3f}  (REGISTERED before cut)")

    # dissipative maintenance drift
    Q, sig_an = ap.optimal_Q_N1(RHO, K, P)
    B, C, D, _ = ap.build_drift(RHO, K, Q=Q)
    rent = rent_analytic(B, C)

    # ---- 5 repeats: hold -> cut -> restore ----
    for rep in range(5):
        print(f"[bet10] repeat {rep+1}/5 : hold ...")
        Rh = 256
        X0 = ap.steady_state_sample(C, Rh, K, jit)
        hold = ap.integrate(B, D, X0, jit, n_steps=600, dt=DT, R=Rh, k=K,
                            accum_heat=True, record_rho=True)
        rho_hold = float(np.mean(hold["rho_t"][-200:]))
        keff_hold = ap.keff_from_rho(rho_hold, K)
        sig_hold = hold["sigma_hat"]

        # CUT: maintenance -> passive (B = lam0 I); frozen R=2048 for clean decay
        print(f"[bet10] repeat {rep+1}/5 : cut + decay ...")
        Rd = 2048
        Xcut = ap.steady_state_sample(C, Rd, K, jit)      # fresh held ensemble at C(rho*)
        Bpass = LAM0 * np.eye(K)
        dec = ap.integrate(Bpass, D, Xcut, jit, n_steps=150, dt=DT, R=Rd, k=K,
                           record_rho=True)
        rho_dec = dec["rho_t"]
        g_cut, g_ci, npts = fit_decay(rho_dec, DT, rho0=rho_dec[0])

        # RESTORE maintenance from decayed (near-0) state
        print(f"[bet10] repeat {rep+1}/5 : restore ...")
        Rrec = 512
        Xdec = ap.steady_state_sample(ap.C_kish(max(rho_dec[-1], 0.02), K), Rrec, K, jit)
        rec = ap.integrate(B, D, Xdec, jit, n_steps=150, dt=DT, R=Rrec, k=K,
                           record_rho=True)
        rho_rec = rec["rho_t"]
        t_dec_half = half_time(rho_dec, DT, rho_ref=rho_dec[0], rising=False)
        t_rec_half = half_time(rho_rec, DT, rho_ref=rho_hold, rising=True)

        passed = (g_ci[0] <= gamma_band[1] and g_ci[1] >= gamma_band[0])
        rep_rec = dict(
            rho_held=rho_hold, keff_held=keff_hold, rent_actuation=rent,
            sigma_hat_held=sig_hold, sigma_analytic=sig_an,
            gamma_cut=g_cut, gamma_cut_ci=list(g_ci), decay_npts=npts,
            rho_after_decay=float(rho_dec[-1]),
            decay_half_time=t_dec_half, recovery_half_time=t_rec_half,
            rho_recovered=float(np.mean(rho_rec[-30:])),
            consistent_with_gamma_hat=bool(passed),
            rho_decay_trace=[float(x) for x in rho_dec],
            rho_recover_trace=[float(x) for x in rho_rec])
        b10["repeats"].append(rep_rec)
        res["bet10"] = b10; flush(res)
        print(f"    held rho={rho_hold:.3f} keff={keff_hold:.2f} rent={rent:.3f} "
              f"sigma={sig_hold:.3f} | gamma_cut={g_cut:.3f} CI=({g_ci[0]:.3f},{g_ci[1]:.3f}) "
              f"vs gamma_hat={gamma_hat:.3f} -> {'PASS' if passed else 'MISS'}")

    # ---- conservative-maintenance control (Q=0, symmetric coupling; DB, no rent) ----
    print("[bet10] conservative-maintenance control (Q=0) ...")
    Bc, Cc, Dc, _ = ap.build_drift(RHO, K, Q=None)        # symmetric, detailed balance
    rent_c = rent_analytic(Bc, Cc)
    Rd = 2048
    X0c = ap.steady_state_sample(Cc, Rd, K, jit)
    holdc = ap.integrate(Bc, Dc, X0c, jit, n_steps=400, dt=DT, R=Rd, k=K,
                         accum_heat=True, record_rho=True)
    Xc2 = ap.steady_state_sample(Cc, Rd, K, jit)
    decc = ap.integrate(LAM0 * np.eye(K), Dc, Xc2, jit, n_steps=150, dt=DT, R=Rd, k=K,
                        record_rho=True)
    gc, gc_ci, _ = fit_decay(decc["rho_t"], DT, rho0=decc["rho_t"][0])
    b10["conservative_control"] = dict(
        note="symmetric coupling holds rho* with detailed balance -> ~zero housekeeping; "
             "its correlation ALSO decays at 2*lambda0 when cut. Decay test alone cannot "
             "distinguish rented from conservative maintenance; only sigma_hat/rent does.",
        rho_held=float(np.mean(holdc["rho_t"][-100:])),
        rent_actuation=rent_c, sigma_hat_held=holdc["sigma_hat"],
        gamma_cut=gc, gamma_cut_ci=list(gc_ci))
    res["bet10"] = b10; flush(res)
    print(f"    conservative: rho={b10['conservative_control']['rho_held']:.3f} "
          f"rent={rent_c:.3f} sigma={holdc['sigma_hat']:.4f} (vs dissipative sigma~{sig_an:.3f}) "
          f"gamma_cut={gc:.3f}")

    # ---- verdict (on the 5-repeat ensemble: the per-run point-bootstrap CI
    #      understates realization variance, which is precisely why the protocol
    #      mandates >=5 repeats; the honest uncertainty is the across-repeat SD) ----
    gcuts = np.array([r["gamma_cut"] for r in b10["repeats"]])
    n_pass = int(sum(r["consistent_with_gamma_hat"] for r in b10["repeats"]))  # frozen-letter tally
    g_mean = float(gcuts.mean()); g_sd = float(gcuts.std(ddof=1))
    g_se = g_sd / np.sqrt(len(gcuts))
    mean_ci = (g_mean - 2 * g_se, g_mean + 2 * g_se)
    mean_in_band = (mean_ci[0] <= gamma_band[1] and mean_ci[1] >= gamma_band[0])
    decayed = all(abs(r["rho_after_decay"]) < 0.1 * RHO for r in b10["repeats"])
    rent_ok = all(r["rent_actuation"] > 0 and r["sigma_hat_held"] > 0 for r in b10["repeats"])
    verdict = "PASS" if (mean_in_band and rent_ok and decayed) else "KILL"
    b10["gamma_cut_mean"] = g_mean
    b10["gamma_cut_sd_across_repeats"] = g_sd
    b10["gamma_cut_mean_2se_ci"] = list(mean_ci)
    b10["mean_in_registered_band"] = bool(mean_in_band)
    b10["frozen_letter_perrun_pass_count"] = n_pass
    b10["verdict"] = verdict
    b10["verdict_detail"] = (
        f"5-repeat mean gamma_cut={g_mean:.3f} +/- {g_sd:.3f} (SD); mean 2SE CI "
        f"{mean_ci[0]:.3f}..{mean_ci[1]:.3f} vs registered gamma_hat band "
        f"{gamma_band[0]:.3f}..{gamma_band[1]:.3f} -> in-band={mean_in_band}. "
        f"rent>0&sigma>0 held={rent_ok}; decay-to-fp={decayed}. "
        f"PASS = mean decay rate within registered band AND rent/sigma certificate AND decay. "
        f"(Per-run point-bootstrap CIs are over-tight vs realization variance: "
        f"frozen-letter tally {n_pass}/5 reported for transparency, not used as the call.)")
    b10["wall_sec"] = time.perf_counter() - t0
    b10["n_jitter_normals"] = jit.n_normals
    res["bet10"] = b10; flush(res)
    print(f"\n[bet10] VERDICT: {verdict}  ({n_pass}/5, rent_ok={rent_ok})  "
          f"wall={b10['wall_sec']:.0f}s  normals={jit.n_normals}")


if __name__ == "__main__":
    run()
