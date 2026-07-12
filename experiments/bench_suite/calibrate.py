#!/usr/bin/env python3
"""
CALIBRATION (no bet-relevant numbers). Validates the instrument before DECISIONS
are frozen:
  1. real-jitter normals: whiteness + normality (the bath must be white Gaussian-ish).
  2. sigma_hat estimator: measured housekeeping heat vs the analytic
     sigma = Tr[Q^T D^{-1} Q C^{-1}] on a known drift (reuses corridor_ceiling form).
  3. passive relaxation lambda0: (a) single-oscillator lag-autocorr of the passive
     array; (b) correlation-decay rate of a correlated start under the passive drift.
     Confirms the FDT identity used by bet 10: correlation decays at 2*lambda0, and
     2*lambda0 is recoverable from equilibrium single-oscillator fluctuations alone.
  4. wall-clock timing of one ensemble step (sizes the bet runs).
Writes calibration.json.
"""
import json, time, os
import numpy as np
import apparatus as ap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "calibration.json")
DT = 0.01
LAMBDA0 = 1.0
K = 8
R = 256
res = {"role": "CALIBRATION", "dt": DT, "lambda0": LAMBDA0, "k": K, "R": R}


def flush():
    with open(OUT, "w") as f:
        json.dump(res, f, indent=2, default=float)


def fit_exp_rate(t, y, y_inf):
    """Fit y(t) = y_inf + A exp(-r t) by linear regression on log|y - y_inf|."""
    d = y - y_inf
    good = d > 1e-4
    t, d = t[good], d[good]
    slope, intercept = np.polyfit(t, np.log(d), 1)
    return -float(slope), float(np.exp(intercept))


t_start = time.perf_counter()
jit = ap.JitterSource()

# ---- 1. jitter normals validation -----------------------------------------
print("[cal 1/4] validating real-jitter normals ...")
z = jit.normals(300000)
res["jitter_validation"] = ap.validate_normals(z)
v = res["jitter_validation"]
print(f"    mean={v['mean']:+.4f} std={v['std']:.4f} skew={v['skew']:+.3f} "
      f"kurt={v['kurtosis']:+.3f} ac1={v['autocorr_lags_1_2_3_5_10'][0]:+.4f} "
      f"KS_p={v['ks_p']:.3f}")
flush()

# ---- 2. sigma_hat estimator vs analytic ------------------------------------
print("[cal 2/4] sigma_hat estimator vs analytic (rho=0.3, k=8, P=1) ...")
rho = 0.3
Q, sig_analytic = ap.optimal_Q_N1(rho, K, P=1.0)
B, C, D, _ = ap.build_drift(rho, K, Q=Q)
X0 = ap.steady_state_sample(C, R, K, jit)
out = ap.integrate(B, D, X0, jit, n_steps=1500, dt=DT, R=R, k=K, accum_heat=True)
res["sigma_estimator_check"] = dict(rho=rho, sigma_analytic=sig_analytic,
                                    sigma_hat=out["sigma_hat"],
                                    rel_err=abs(out["sigma_hat"] - sig_analytic) / sig_analytic)
print(f"    analytic={sig_analytic:.4f}  measured={out['sigma_hat']:.4f}  "
      f"rel_err={res['sigma_estimator_check']['rel_err']*100:.1f}%")
flush()

# ---- 3. passive relaxation lambda0 -----------------------------------------
print("[cal 3/4] passive lambda0 two ways ...")
Bpass = LAMBDA0 * np.eye(K)                        # bare relaxation, no coupling
Dpass = np.eye(K)
# (a) single-oscillator autocorrelation from an equilibrium passive trajectory
X0eq = ap.steady_state_sample(np.eye(K), R, K, jit)   # passive NESS = identity cov
traj = []
Xg = X0eq
import cupy as cp
Bt = cp.asarray(Bpass.T); sq = (2 * DT) ** 0.5
Xg = cp.asarray(X0eq)
for t in range(400):
    Z = cp.asarray(jit.normal_block((R, K)))
    Xg = Xg - (Xg @ Bt) * DT + sq * Z
    traj.append(cp.asnumpy(Xg[:, 0]))             # oscillator 0 across replicas
traj = np.array(traj)                              # (T, R)
# lag-L autocorr; process is zero-mean stationary OU, so do NOT subtract a
# finite-sample time mean (that biases high-phi ACF downward). Pool over t,replicas.
var0 = np.mean(traj ** 2)
def acf_lag(L):
    return np.mean(traj[:-L] * traj[L:]) / var0
lags = np.array([1, 2, 3, 5, 8, 12])
acf = np.array([acf_lag(L) for L in lags])
lam_acf = -np.polyfit(lags * DT, np.log(np.clip(acf, 1e-6, None)), 1)[0]
# (b) correlation decay of a correlated start under passive drift
rho0 = 0.5
Ccorr = ap.C_kish(rho0, K)
X0c = ap.steady_state_sample(Ccorr, R, K, jit)
outc = ap.integrate(Bpass, Dpass, X0c, jit, n_steps=200, dt=DT, R=R, k=K, record_rho=True)
rt = outc["rho_t"]
tt = np.arange(len(rt)) * DT
rate_corr, _ = fit_exp_rate(tt, rt, y_inf=0.0)
res["passive_lambda0"] = dict(
    lambda0_set=LAMBDA0,
    lambda0_from_single_osc_acf=float(lam_acf),
    corr_decay_rate_measured=float(rate_corr),
    corr_decay_rate_predicted_2lambda=float(2 * lam_acf),
    rho0=rho0)
print(f"    lambda0 set={LAMBDA0}  from single-osc ACF={lam_acf:.3f}")
print(f"    corr-decay rate measured={rate_corr:.3f}  predicted 2*lambda0={2*lam_acf:.3f}")
flush()

# ---- 4. wall-clock per step ------------------------------------------------
print("[cal 4/4] timing one ensemble step ...")
t0 = time.perf_counter()
_ = ap.integrate(Bpass, Dpass, X0eq, jit, n_steps=50, dt=DT, R=R, k=K)
dt_step = (time.perf_counter() - t0) / 50
res["timing"] = dict(sec_per_step=dt_step, n_timings=jit.n_timings,
                     n_normals=jit.n_normals,
                     total_wall_sec=time.perf_counter() - t_start)
print(f"    {dt_step*1000:.2f} ms/step (incl real-jitter harvest); "
      f"{jit.n_normals} normals used")
flush()
print(f"\nwrote {OUT}")
