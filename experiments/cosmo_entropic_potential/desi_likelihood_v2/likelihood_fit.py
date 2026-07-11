#!/usr/bin/env python3
"""
Likelihood-grade DESI DR2 BAO comparison of the frozen halo-grain S(a) curve.

Upgrade of epoch_check/cpl_projection.py from REPRESENTATIVE fractional errors to
the REAL DESI DR2 BAO data vector + full covariance (the official Cobaya likelihood
file desi_gaussian_bao_ALL_GCcomb, 13 measurements over 7 tracers).

Program physics: rho_DE(a) proportional to S(a)  =>  E^2(a) = Om a^-3 + Om_r a^-4
+ (1-Om-Om_r) S(a)/S(1). The framework has NO free (w0,wa); its DE shape is FROZEN
from the TNG300-1 halo-grain B-total pipeline. Free parameters for the framework fit
are only (Om, beta) where beta = c/(H0 r_d) is the single distance-scale nuisance that
ALL BAO observables (DM/rd, DH/rd, DV/rd) are exactly linear in.

Models compared, all against the SAME real DESI vector + covariance (+ optional CMB
theta* anchor):
  (a) framework  : f_DE(a) = S(a)/S(1)   -> free (Om, beta)             [0 shape params]
  (b) CPL        : f_DE(a) = CPL(w0,wa)   -> free (Om, beta, w0, wa)     [2 shape params]
  (c) LCDM       : f_DE(a) = 1            -> free (Om, beta)             [0 shape params]

beta is profiled analytically at each grid point (linear); Om (and w0,wa for CPL) are
profiled on a grid. Outputs Delta chi2, AIC, BIC with matched parameter counts.

CMB theta* anchor (task-specified, frac err 3e-4): adds DM(z*)/rd at z*=1089.80 with a
target computed from Planck-2018 base-LCDM. This is an APPROXIMATION of the CMB prior:
it uses only the acoustic-scale distance to last scattering, folds the fixed early-
physics ratio rs*/rd into the target, includes radiation in E(z), and is Gaussian. It
does NOT carry the full CMB covariance or the sound-horizon (rs) uncertainty.
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
DATA = HERE / "desi_dr2_data"
LV = HERE.parent / "large_volume" / "results.json"

C_KM = 299792.458
# Planck 2018 base-LCDM (TT,TE,EE+lowE+lensing) for the CMB anchor target + radiation.
PLANCK = dict(Om=0.3153, H0=67.36, rd=147.09, zstar=1089.80)
OM_R = 9.2e-5          # Omega_r today (photons + massless nu, Neff=3.046, h~0.674)

# ---------------------------------------------------------------------------
# 1. REAL DESI DR2 BAO data vector + covariance (official Cobaya file).
#    Source: CobayaSampler/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_*.txt
#    which reproduces DESI DR2 Results II (arXiv:2503.14738) Table.
# ---------------------------------------------------------------------------
def load_desi():
    zs, vals, quants = [], [], []
    for line in (DATA / "desi_gaussian_bao_ALL_GCcomb_mean.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        z, v, q = line.split()
        zs.append(float(z)); vals.append(float(v)); quants.append(q)
    cov = np.loadtxt(DATA / "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    return np.array(zs), np.array(vals), quants, cov

DZ, DVAL, DQ, DCOV = load_desi()
DCOVINV = np.linalg.inv(DCOV)
N_BAO = len(DVAL)

# ---------------------------------------------------------------------------
# 2. Framework S(a): frozen TNG300-1 B-total corner curve.
# ---------------------------------------------------------------------------
lv = json.load(open(LV))
recs = lv["stage2_primary"]["records"]
A_S = np.array([r["a"] for r in recs])
S_S = np.array([r["S"] for r in recs])
order = np.argsort(A_S)
A_S, S_S = A_S[order], S_S[order]

def make_f_fw(a, Sa):
    sp = CubicSpline(np.log(a), np.log(Sa))
    S1 = np.exp(sp(0.0))
    amin = a.min(); lnSmin = sp(np.log(amin))
    def f(aa):
        aa = np.atleast_1d(np.asarray(aa, float))
        lnS = np.where(aa >= amin, sp(np.log(np.clip(aa, 1e-6, 1.0))), lnSmin)
        return np.exp(lnS) / S1
    return f

F_FW = make_f_fw(A_S, S_S)

def f_cpl(a, w0, wa):
    a = np.asarray(a, float)
    return a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))

def f_lcdm(a):
    return np.ones_like(np.atleast_1d(np.asarray(a, float)))

# ---------------------------------------------------------------------------
# 3. Backgrounds. E(a) INCLUDES radiation (matters only for the z* anchor).
# ---------------------------------------------------------------------------
def E_of(f_de, Om):
    Ode = 1.0 - Om - OM_R
    def E(a):
        a = np.asarray(a, float)
        return np.sqrt(OM_R * a ** -4.0 + Om * a ** -3.0 + Ode * f_de(a))
    return E

def _invE(z, Efunc):
    return 1.0 / float(np.ravel(Efunc(1.0 / (1.0 + z)))[0])

def dc_over_rd_unit(zt, Efunc):
    """comoving distance integral ∫_0^z dz/E  (multiply by beta for DM/rd)."""
    val, _ = quad(lambda z: _invE(z, Efunc), 0.0, zt, limit=200)
    return val

def template_vector(f_de, Om):
    """model vector at beta=1, in the EXACT row order of the DESI mean file."""
    E = E_of(f_de, Om)
    # cache comoving integrals per unique z
    uz = sorted(set(DZ))
    Dc = {z: dc_over_rd_unit(z, E) for z in uz}
    t = np.empty(N_BAO)
    for i, (z, q) in enumerate(zip(DZ, DQ)):
        dm = Dc[z]                       # DM/rd per beta = ∫dz/E
        dh = _invE(z, E)                 # = 1/E(z)  -> DH/rd per beta
        if q == "DM_over_rs":
            t[i] = dm
        elif q == "DH_over_rs":
            t[i] = dh
        elif q == "DV_over_rs":
            t[i] = (z * dm ** 2 * dh) ** (1.0 / 3.0)
        else:
            raise ValueError(q)
    return t

# ---------------------------------------------------------------------------
# 4. CMB theta* anchor target from Planck LCDM (DM(z*)/rd).
# ---------------------------------------------------------------------------
def cmb_anchor_target():
    E = E_of(f_lcdm, PLANCK["Om"])
    beta = C_KM / (PLANCK["H0"] * PLANCK["rd"])
    dm_star = beta * dc_over_rd_unit(PLANCK["zstar"], E)
    return dm_star

R_STAR = cmb_anchor_target()      # DM(z*)/rd Planck target
SIG_R = 3.0e-4 * R_STAR           # frac err 3e-4 (task-specified theta* precision)

def cmb_template(f_de, Om):
    E = E_of(f_de, Om)
    return dc_over_rd_unit(PLANCK["zstar"], E)   # DM(z*)/rd per beta

# ---------------------------------------------------------------------------
# 5. chi2 with analytic beta (all observables linear in beta).
# ---------------------------------------------------------------------------
def chi2_at(f_de, Om, use_cmb=True):
    t = template_vector(f_de, Om)
    if use_cmb:
        tc = cmb_template(f_de, Om)
        # stack BAO (correlated) + CMB (independent) into one GLS beta solve
        # A = t^T Cinv t + tc^2/sig^2 ; B = t^T Cinv d + tc*R/sig^2
        A = t @ DCOVINV @ t + tc * tc / SIG_R ** 2
        B = t @ DCOVINV @ DVAL + tc * R_STAR / SIG_R ** 2
        beta = B / A
        r = DVAL - beta * t
        c2 = r @ DCOVINV @ r + ((beta * tc - R_STAR) / SIG_R) ** 2
    else:
        A = t @ DCOVINV @ t
        B = t @ DCOVINV @ DVAL
        beta = B / A
        r = DVAL - beta * t
        c2 = r @ DCOVINV @ r
    return float(c2), float(beta)

# ---------------------------------------------------------------------------
# 6. Profiles.
# ---------------------------------------------------------------------------
OM_GRID = np.linspace(0.26, 0.37, 111)

def profile_fixedshape(f_de, use_cmb=True):
    best = (np.inf, None, None)
    prof = []
    for Om in OM_GRID:
        c2, beta = chi2_at(f_de, Om, use_cmb)
        prof.append((float(Om), c2))
        if c2 < best[0]:
            best = (c2, float(Om), beta)
    return dict(chi2=best[0], Om=best[1], beta=best[2],
                profile=prof)

def profile_cpl(use_cmb=True):
    """profile over (Om, w0, wa). Coarse grid -> local Nelder-Mead refine."""
    w0g = np.linspace(-1.2, -0.4, 17)
    wag = np.linspace(-2.2, 1.0, 17)
    best = (np.inf, None, None, None, None)
    for Om in OM_GRID[::5]:                # coarse in Om for the grid scan
        for w0 in w0g:
            for wa in wag:
                c2, beta = chi2_at(lambda a: f_cpl(a, w0, wa), Om, use_cmb)
                if c2 < best[0]:
                    best = (c2, float(Om), float(w0), float(wa), beta)
    # refine (Om,w0,wa) locally
    def nll(p):
        Om, w0, wa = p
        if not (0.2 < Om < 0.45):
            return 1e6
        c2, _ = chi2_at(lambda a: f_cpl(a, w0, wa), Om, use_cmb)
        return c2
    r = minimize(nll, [best[1], best[2], best[3]], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-6, maxiter=8000))
    Om, w0, wa = r.x
    c2, beta = chi2_at(lambda a: f_cpl(a, w0, wa), Om, use_cmb)
    return dict(chi2=float(c2), Om=float(Om), w0=float(w0), wa=float(wa), beta=beta)

# ---------------------------------------------------------------------------
# 7. Run + stats.
# ---------------------------------------------------------------------------
def aic_bic(chi2, k, n):
    return chi2 + 2 * k, chi2 + k * np.log(n)

def run(use_cmb):
    n = N_BAO + (1 if use_cmb else 0)
    fw = profile_fixedshape(F_FW, use_cmb)
    lc = profile_fixedshape(f_lcdm, use_cmb)
    cpl = profile_cpl(use_cmb)
    # param counts: Om + beta shared (=2); CPL adds w0,wa (=4)
    k_fw, k_lc, k_cpl = 2, 2, 4
    out = {}
    for name, res, k in [("framework", fw, k_fw), ("LCDM", lc, k_lc), ("CPL", cpl, k_cpl)]:
        aic, bic = aic_bic(res["chi2"], k, n)
        out[name] = {**{kk: vv for kk, vv in res.items() if kk != "profile"},
                     "k_params": k, "AIC": float(aic), "BIC": float(bic)}
    out["n_data"] = n
    out["deltas"] = {
        "chi2_framework_minus_LCDM": fw["chi2"] - lc["chi2"],
        "chi2_framework_minus_CPL": fw["chi2"] - cpl["chi2"],
        "chi2_LCDM_minus_CPL": lc["chi2"] - cpl["chi2"],
        "dAIC_framework_minus_CPL": out["framework"]["AIC"] - out["CPL"]["AIC"],
        "dAIC_framework_minus_LCDM": out["framework"]["AIC"] - out["LCDM"]["AIC"],
        "dBIC_framework_minus_CPL": out["framework"]["BIC"] - out["CPL"]["BIC"],
        "dBIC_framework_minus_LCDM": out["framework"]["BIC"] - out["LCDM"]["BIC"],
    }
    out["framework_profile_Om"] = fw["profile"]
    return out

if __name__ == "__main__":
  results = {
    "provenance": {
        "desi_data": "DESI DR2 BAO, official Cobaya likelihood file "
                     "desi_gaussian_bao_ALL_GCcomb (mean+cov), from "
                     "CobayaSampler/bao_data/desi_bao_dr2/, reproducing "
                     "DESI DR2 Results II arXiv:2503.14738; 13 measurements / 7 tracers.",
        "desi_z": DZ.tolist(), "desi_value": DVAL.tolist(), "desi_quantity": DQ,
        "cov_shape": list(DCOV.shape),
        "framework_curve": "TNG300-1 205 Mpc/h B-total corner 7.43e11, frozen S(a) from "
                           "large_volume/results.json stage2_primary.records (10 pts).",
        "S_of_a": {"a": A_S.tolist(), "S": S_S.tolist()},
        "cmb_anchor": {
            "target_DM_zstar_over_rd": R_STAR, "frac_err": 3.0e-4, "sigma": SIG_R,
            "zstar": PLANCK["zstar"], "planck_ref": PLANCK,
            "note": "theta*-compression approximation; uses acoustic-scale distance only, "
                    "folds fixed rs*/rd into the target, includes radiation, Gaussian; "
                    "NOT the full CMB covariance and NO rs uncertainty."},
        "Om_r_fixed": OM_R,
    },
    "with_cmb": run(True),
    "bao_only": run(False),
  }

  (HERE / "results.json").write_text(json.dumps(results, indent=2))

  # ---- print verdict ----
  def show(tag, r):
    print("=" * 76)
    print(f"{tag}   (n_data={r['n_data']})")
    print("-" * 76)
    for name in ("framework", "LCDM", "CPL"):
        d = r[name]
        extra = ""
        if name == "CPL":
            extra = f" w0={d['w0']:+.3f} wa={d['wa']:+.3f}"
        print(f"  {name:10s} chi2={d['chi2']:8.3f}  Om={d['Om']:.4f}  "
              f"k={d['k_params']}  AIC={d['AIC']:8.3f}  BIC={d['BIC']:8.3f}{extra}")
    dl = r["deltas"]
    print(f"  Dchi2 framework-LCDM = {dl['chi2_framework_minus_LCDM']:+.3f}  "
          f"framework-CPL = {dl['chi2_framework_minus_CPL']:+.3f}  "
          f"LCDM-CPL = {dl['chi2_LCDM_minus_CPL']:+.3f}")
    print(f"  dAIC fw-CPL={dl['dAIC_framework_minus_CPL']:+.2f}  fw-LCDM={dl['dAIC_framework_minus_LCDM']:+.2f}  "
          f"| dBIC fw-CPL={dl['dBIC_framework_minus_CPL']:+.2f}  fw-LCDM={dl['dBIC_framework_minus_LCDM']:+.2f}")

  print(f"\nCMB anchor target DM(z*)/rd = {R_STAR:.3f} +/- {SIG_R:.4f} (Planck LCDM)\n")
  show("WITH CMB theta* anchor", results["with_cmb"])
  print()
  show("BAO ONLY (no CMB)", results["bao_only"])
  print("\nwrote results.json")
