#!/usr/bin/env python3
"""CALIBRATION micro-check: does the bet-10 decay estimator recover the known
passive rate 2*lambda0 = 2.01 (discrete) from a real-jitter passive relaxation?
Tests R and the fit window. No bet-relevant numbers."""
import numpy as np, apparatus as ap
DT, LAM, K = 0.01, 1.0, 8
jit = ap.JitterSource()


def fit_decay(rho_t, dt, rho0, lo=0.10, hi=0.85):
    """Fit rho(t)=rho0*exp(-g t) on the window rho in [lo*rho0, hi*rho0]
    (above the finite-ensemble floor, below the initial transient). Weighted
    log-linear; bootstrap CI over the window points."""
    t = np.arange(len(rho_t)) * dt
    m = (rho_t < hi * rho0) & (rho_t > lo * rho0)
    tt, yy = t[m], rho_t[m]
    if len(tt) < 5:
        return np.nan, (np.nan, np.nan), 0
    g = -np.polyfit(tt, np.log(yy), 1)[0]
    # bootstrap
    idx = np.arange(len(tt)); gs = []
    rng = np.random.default_rng(0)
    for _ in range(500):
        b = rng.choice(idx, len(idx), replace=True)
        if len(np.unique(tt[b])) > 3:
            gs.append(-np.polyfit(tt[b], np.log(yy[b]), 1)[0])
    return float(g), (float(np.percentile(gs, 2.5)), float(np.percentile(gs, 97.5))), int(m.sum())


for R in (256, 1024, 4096):
    Bpass = LAM * np.eye(K)
    X0 = ap.steady_state_sample(ap.C_kish(0.5, K), R, K, jit)
    out = ap.integrate(Bpass, np.eye(K), X0, jit, n_steps=150, dt=DT, R=R, k=K, record_rho=True)
    rt = out["rho_t"]
    g, ci, npts = fit_decay(rt, DT, rho0=rt[0])
    floor = 1.0 / np.sqrt(R)
    print(f"R={R:5d}  rho0={rt[0]:.3f}  floor~{floor:.3f}  npts={npts:3d}  "
          f"rate={g:.3f}  CI=({ci[0]:.3f},{ci[1]:.3f})  [true=2.01]")
