#!/usr/bin/env python3
"""
Task 4: quantify the projection-method spread as a systematic on (w0,wa).

The framework has no intrinsic (w0,wa) -- a curved w(a) gets a DIFFERENT CPL point
depending on HOW you project it (distance-space vs rho-weighted vs w-space). The old
epoch_check pipeline reported distance-space wa=-0.74 vs rho-weighted wa=-0.98. Here we
recompute the distance-space projection through the REAL DESI DR2 covariance (not
representative errors) and report the spread across methods as the method systematic.

We also report each projected point's Mahalanobis distance from DESI's PUBLISHED
(w0,wa) posterior (the 1.36-sigma-class headline object), now with the real-covariance
projection replacing the representative-error one.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import CubicSpline
import likelihood_fit as L

HERE = Path(__file__).resolve().parent

# DESI DR2 published w0waCDM posterior (BAO+CMB+DESY5 SNe), arXiv:2503.14738.
DESI_W0, DESI_WA = -0.838, -0.62
SIG_W0, SIG_WA, RHO = 0.055, 0.20, -0.7
COV_WW = np.array([[SIG_W0**2, RHO*SIG_W0*SIG_WA],
                   [RHO*SIG_W0*SIG_WA, SIG_WA**2]])
COVINV_WW = np.linalg.inv(COV_WW)

def maha(w0, wa):
    d = np.array([w0 - DESI_W0, wa - DESI_WA])
    return float(np.sqrt(d @ COVINV_WW @ d))

def cross_z(w0, wa):
    if wa == 0: return None
    a = 1.0 + (1.0 + w0) / wa
    return 1.0/a - 1.0 if a > 0 else None

# ---------------------------------------------------------------------------
# (A) distance-space projection THROUGH THE REAL DESI COVARIANCE.
# framework distances become pseudo-data; fit CPL to them with metric = DCOV.
# ---------------------------------------------------------------------------
def framework_pseudodata(use_cmb):
    # framework best-fit (Om,beta) from the real fit
    r = L.profile_fixedshape(L.F_FW, use_cmb)
    Om, beta = r["Om"], r["beta"]
    t = L.template_vector(L.F_FW, Om)
    m = beta * t                        # framework DM/DH/DV vector (real units)
    tc = beta * L.cmb_template(L.F_FW, Om) if use_cmb else None
    return m, tc, Om

def project_distance_realcov(use_cmb=True):
    m_fw, mc_fw, Om_fw = framework_pseudodata(use_cmb)
    def chi2(p):
        w0, wa = p
        f = lambda a: L.f_cpl(a, w0, wa)
        def inner(Om):
            t = L.template_vector(f, Om)
            if use_cmb:
                tc = L.cmb_template(f, Om)
                A = t @ L.DCOVINV @ t + tc*tc/L.SIG_R**2
                B = t @ L.DCOVINV @ m_fw + tc*mc_fw/L.SIG_R**2
                beta = B/A
                rr = m_fw - beta*t
                return rr @ L.DCOVINV @ rr + ((beta*tc - mc_fw)/L.SIG_R)**2
            else:
                A = t @ L.DCOVINV @ t; B = t @ L.DCOVINV @ m_fw
                beta = B/A; rr = m_fw - beta*t
                return rr @ L.DCOVINV @ rr
        # profile Om quickly
        best = min(inner(Om) for Om in np.linspace(0.28, 0.40, 25))
        return best
    r = minimize(chi2, [-0.80, -0.6], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-8, maxiter=6000))
    return float(r.x[0]), float(r.x[1]), float(r.fun)

# ---------------------------------------------------------------------------
# (B) rho-weighted projection (Omega_DE(a)-weighted ln rho_DE fit; no covariance).
#     Reproduces epoch_check/cpl_projection.py project_rho.
# ---------------------------------------------------------------------------
def project_rho(Om=0.3155, zmax=2.3):
    aa = np.linspace(1.0/(1.0+zmax), 1.0, 400)
    lnf = np.log(L.F_FW(aa))
    E = L.E_of(L.F_FW, Om)
    W = (1.0 - Om) * L.F_FW(aa) / E(aa)**2
    def loss(p):
        w0, wa = p
        return np.sum(W * (np.log(L.f_cpl(aa, w0, wa)) - lnf)**2)
    r = minimize(loss, [-0.85, -0.5], method="Nelder-Mead",
                 options=dict(xatol=1e-5, fatol=1e-12, maxiter=4000))
    return float(r.x[0]), float(r.x[1])

# ---------------------------------------------------------------------------
# (C) w-space projection (literal project w(a) onto {1,(1-a)}).
# ---------------------------------------------------------------------------
def project_w(weight="DE", Om=0.3155, zmax=2.3):
    sp = CubicSpline(np.log(L.A_S), np.log(L.S_S))
    aa = np.linspace(max(L.A_S.min(), 1.0/(1.0+zmax)), 1.0, 400)
    w = -1.0 - sp(np.log(aa), 1)/3.0
    if weight == "uniform":
        Wt = np.ones_like(aa)
    else:
        E = L.E_of(L.F_FW, Om)
        Wt = (1.0 - Om) * L.F_FW(aa) / E(aa)**2
    A = np.vstack([np.ones_like(aa), 1.0 - aa]).T
    WA = A * Wt[:, None]
    coef = np.linalg.solve(A.T @ WA, WA.T @ w)
    return float(coef[0]), float(coef[1])

# ---------------------------------------------------------------------------
# Run.
# ---------------------------------------------------------------------------
pts = {}
w0, wa, c2 = project_distance_realcov(use_cmb=True)
pts["dist_realcov_BAO+CMB"] = dict(w0=w0, wa=wa, cross_z=cross_z(w0, wa), maha=maha(w0, wa))
w0, wa, c2 = project_distance_realcov(use_cmb=False)
pts["dist_realcov_BAO_only"] = dict(w0=w0, wa=wa, cross_z=cross_z(w0, wa), maha=maha(w0, wa))
w0, wa = project_rho()
pts["rho_weighted"] = dict(w0=w0, wa=wa, cross_z=cross_z(w0, wa), maha=maha(w0, wa))
w0, wa = project_w("DE")
pts["w_DE_weighted"] = dict(w0=w0, wa=wa, cross_z=cross_z(w0, wa), maha=maha(w0, wa))
w0, wa = project_w("uniform")
pts["w_uniform"] = dict(w0=w0, wa=wa, cross_z=cross_z(w0, wa), maha=maha(w0, wa))

w0s = [p["w0"] for p in pts.values()]
was = [p["wa"] for p in pts.values()]
spread = {
    "w0_min": min(w0s), "w0_max": max(w0s), "w0_range": max(w0s)-min(w0s),
    "w0_std": float(np.std(w0s)),
    "wa_min": min(was), "wa_max": max(was), "wa_range": max(was)-min(was),
    "wa_std": float(np.std(was)),
    "maha_min": min(p["maha"] for p in pts.values()),
    "maha_max": max(p["maha"] for p in pts.values()),
}

out = {
    "desi_published_posterior": dict(w0=DESI_W0, wa=DESI_WA, sig_w0=SIG_W0,
                                     sig_wa=SIG_WA, rho=RHO,
                                     note="w0waCDM BAO+CMB+DESY5, arXiv:2503.14738"),
    "projected_points": pts,
    "method_systematic": spread,
    "lcdm_maha": maha(-1.0, 0.0),
}
(HERE / "projection_spread.json").write_text(json.dumps(out, indent=2))

print("="*74)
print("PROJECTION-METHOD SPREAD (framework -> CPL), real DESI DR2 covariance")
print(f"DESI published (w0,wa)=({DESI_W0},{DESI_WA}) sig=({SIG_W0},{SIG_WA}) rho={RHO}")
print("="*74)
print(f"  {'method':24s} {'w0':>8s} {'wa':>8s} {'cross_z':>8s} {'Maha_sig':>9s}")
for k, p in pts.items():
    cz = f"{p['cross_z']:.3f}" if p['cross_z'] is not None else "none"
    print(f"  {k:24s} {p['w0']:+8.3f} {p['wa']:+8.3f} {cz:>8s} {p['maha']:9.2f}")
print(f"  {'LCDM (anchor)':24s} {-1.0:+8.3f} {0.0:+8.3f} {'none':>8s} {maha(-1.0,0.0):9.2f}")
print("-"*74)
print(f"  method systematic: w0 range={spread['w0_range']:.3f} (std {spread['w0_std']:.3f}); "
      f"wa range={spread['wa_range']:.3f} (std {spread['wa_std']:.3f})")
print(f"  Mahalanobis spans {spread['maha_min']:.2f}-{spread['maha_max']:.2f} sigma from DESI")
print("\nwrote projection_spread.json")
