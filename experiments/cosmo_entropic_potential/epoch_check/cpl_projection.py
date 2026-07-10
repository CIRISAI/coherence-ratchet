#!/usr/bin/env python3
"""
CPL-projection of the framework's halo-grain w(a) curve.

The question (operator, 2026-07-10): the framework's PHYSICAL phantom-divide
crossing sits at z ~ 0.77-1.05 (where the halo-grain B-total S(a) peaks). DESI's
CPL best fit crosses at z ~ 0.35. Is that "2x epoch miss" a real miss, or an
artifact of comparing a PHYSICAL crossing epoch to a CPL-FITTED crossing epoch?

DESI does not measure w(a) directly; it fits a 2-parameter CPL line w=w0+wa(1-a)
to distance data over z<~2.3. A curved w(a) run through that same linear fit gets
a DISTORTED (w0,wa) and a distorted crossing epoch (Wolf&Ferreira 2024;
Shlivko&Steinhardt 2024; arXiv:2504.16337).

So the fair test: take the framework's OWN w(a) (from halo S(a) via the sign law),
and FIT CPL TO IT the same way DESI fits CPL to data. Then compare the
CPL-projected crossing epoch to DESI's ~0.35, and the CPL-projected (w0,wa) to
DESI's (-0.84,-0.6). If the framework curve, once distorted by CPL the same way,
lands near DESI, the epoch "miss" was an apples-to-oranges comparison.

Framework physics used:  rho_DE(a) proportional to S(a)  (the stock mapping, eq.1 of
lambda_maintenance_wz.md), so E^2(a) = Om a^-3 + (1-Om) S(a)/S(1), EXACTLY. No
differentiation of S is needed for the distance-based fit (robust to S-noise).

Three independent projections, all over the DESI window z<2.3:
  (P-dist) distance-space chi^2 vs a mock DESI DR2 BAO + CMB theta* data vector
           -- the faithful mimic of what DESI actually fits.
  (P-rho)  DE-fraction-weighted fit of ln rho_DE(a): CPL to framework, no
           derivative -- matches the expansion history where DE has leverage.
  (P-w)    the literal "project w(a) onto {1,(1-a)}" fits: uniform-in-a (what the
           existing pipeline does) and DE-fraction-weighted.
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

HG = "/home/emoore/coherence-ratchet/experiments/cosmo_entropic_potential/halo_grain"
PARENT = "/home/emoore/coherence-ratchet/experiments/cosmo_entropic_potential"
sys.path.insert(0, HG); sys.path.insert(0, PARENT)
import halo_grain as hg
import s_of_a as S

C_KM = 299792.458
Z_STAR = 1089.0

# ---------------------------------------------------------------------------
# 1. Framework S(a): frozen B-total pipeline, all 6 CAMELS CV boxes.
# ---------------------------------------------------------------------------
ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)  # CAMELS cosmo
THR = 1e11
box_curves = []
for cv in range(6):
    snaps = [hg.load_snapshot(s, cv=cv) for s in hg.SNAPS]
    recs = hg.op_B(ps, snaps, THR)                 # frozen B-total
    a = np.array([r["a"] for r in recs]); Sa = np.array([r["S"] for r in recs])
    ok = np.isfinite(Sa) & (Sa > 0)
    box_curves.append((a[ok], Sa[ok]))

a_grid = box_curves[0][0]
# pooled S(a): S_total over the union of independent-phase boxes = sum (block-diag C),
# the framework's own volume-increase device (sweep/quijote.py). Sharpest single curve.
S_pooled = np.sum([c[1] for c in box_curves], axis=0)

def phys_crossing_z(a, Sa):
    """physical phantom-divide crossing = S peak (dlnS/dlna=0), via the frozen spline."""
    sp = CubicSpline(np.log(a), np.log(Sa))
    aa = np.linspace(a.min(), 1.0, 2000)
    d = sp(np.log(aa), 1)
    # last sign change of dlnS/dlna from + to - (peak)
    sgn = np.sign(d)
    idx = np.where((sgn[:-1] > 0) & (sgn[1:] <= 0))[0]
    if len(idx) == 0:
        return None
    ac = aa[idx[-1]]
    return 1.0 / ac - 1.0

# ---------------------------------------------------------------------------
# 2. Backgrounds.
# ---------------------------------------------------------------------------
def make_f_fw(a, Sa):
    """f_fw(a) = rho_DE(a)/rho_DE(1) = S(a)/S(1); constant (frozen) below a_min."""
    sp = CubicSpline(np.log(a), np.log(Sa))
    S1 = np.exp(sp(0.0))                       # S at a=1
    amin = a.min()
    lnSmin = sp(np.log(amin))
    def f(aa):
        aa = np.atleast_1d(np.asarray(aa, float))
        lnS = np.where(aa >= amin, sp(np.log(np.clip(aa, 1e-6, 1.0))), lnSmin)
        return np.exp(lnS) / S1
    return f

def f_cpl(a, w0, wa):
    a = np.asarray(a, float)
    return a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))

def E_of(f_de, Om):
    def E(a):
        a = np.asarray(a, float)
        return np.sqrt(Om * a ** -3.0 + (1.0 - Om) * f_de(a))
    return E

def comoving_DM(zt, Efunc):
    val, _ = quad(lambda z: 1.0 / float(np.ravel(Efunc(1.0 / (1.0 + z)))[0]),
                  0.0, zt, limit=200)
    return C_KM * val            # units of (c/H0) km/s ; H0 cancels in fw-vs-CPL ratios

def DH(zt, Efunc):
    return C_KM / float(np.ravel(Efunc(1.0 / (1.0 + zt)))[0])

# ---------------------------------------------------------------------------
# 3. Projections.
# ---------------------------------------------------------------------------
# DESI DR2 effective redshifts (BGS, LRG1, LRG2, LRG3+ELG1, ELG2, QSO, Lya) and
# representative fractional errors on D_M/r_d and D_H/r_d (DESI DR2 BAO; a couple of
# low-z tracers give D_V only -> approximated by giving both with looser errors).
DESI_Z   = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
SIG_DM   = np.array([0.030, 0.016, 0.011, 0.009, 0.013, 0.026, 0.030])   # frac err D_M/r_d
SIG_DH   = np.array([0.030, 0.021, 0.015, 0.012, 0.020, 0.035, 0.018])   # frac err D_H/r_d
SIG_CMB  = 3.0e-4     # theta* known to ~0.03% -> frac err on D_M(z*)

def project_distance(f_fw, Om=0.3155, float_H0=True, use_cmb=True):
    """Fit CPL (w0,wa) to the framework's distances the way DESI+CMB fits data.
    r_d and early physics identical (linear-era w=-1), so BAO -> match D_M,D_H;
    CMB -> match D_M(z*). float_H0 marginalizes an overall distance scale k."""
    Efw = E_of(f_fw, Om)
    zc = np.concatenate([DESI_Z, [Z_STAR]]) if use_cmb else DESI_Z
    DM_fw = np.array([comoving_DM(z, Efw) for z in zc])
    DH_fw = np.array([DH(z, Efw) for z in DESI_Z])
    def chi2(p):
        w0, wa = p
        fcpl = lambda a: f_cpl(a, w0, wa)
        Ecpl = E_of(fcpl, Om)
        DM_c = np.array([comoving_DM(z, Ecpl) for z in zc])
        DH_c = np.array([DH(z, Ecpl) for z in DESI_Z])
        # optional overall scale k (H0*r_d degeneracy): minimize analytically in ln-space
        if float_H0:
            # weighted mean log-offset across all points
            res_dm = np.log(DM_fw) - np.log(DM_c)
            res_dh = np.log(DH_fw) - np.log(DH_c)
            wdm = 1.0 / np.concatenate([SIG_DM, [SIG_CMB]]) ** 2 if use_cmb else 1.0 / SIG_DM ** 2
            wdh = 1.0 / SIG_DH ** 2
            k = (np.sum(res_dm * wdm) + np.sum(res_dh * wdh)) / (np.sum(wdm) + np.sum(wdh))
        else:
            k = 0.0
        sig_dm = np.concatenate([SIG_DM, [SIG_CMB]]) if use_cmb else SIG_DM
        c2 = np.sum(((np.log(DM_fw) - np.log(DM_c) - k) / sig_dm) ** 2)
        c2 += np.sum(((np.log(DH_fw) - np.log(DH_c) - k) / SIG_DH) ** 2)
        return c2
    r = minimize(chi2, [-0.85, -0.5], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-8, maxiter=4000))
    return float(r.x[0]), float(r.x[1]), float(r.fun)

def project_rho(f_fw, Om=0.3155, zmax=2.3):
    """DE-fraction-weighted fit of ln rho_DE(a): CPL to framework. No derivative."""
    aa = np.linspace(1.0 / (1.0 + zmax), 1.0, 400)
    lnf_fw = np.log(f_fw(aa))
    Efw = E_of(f_fw, Om)
    W = (1.0 - Om) * f_fw(aa) / Efw(aa) ** 2         # Omega_DE(a): leverage weight
    def loss(p):
        w0, wa = p
        return np.sum(W * (np.log(f_cpl(aa, w0, wa)) - lnf_fw) ** 2)
    r = minimize(loss, [-0.85, -0.5], method="Nelder-Mead",
                 options=dict(xatol=1e-5, fatol=1e-12, maxiter=4000))
    return float(r.x[0]), float(r.x[1]), float(r.fun)

def project_w(a, Sa, Om=0.3155, weight="uniform", zmax=2.3):
    """Literal 'project w(a) onto {1,(1-a)}' least squares over z<zmax."""
    sp = CubicSpline(np.log(a), np.log(Sa))
    aa = np.linspace(max(a.min(), 1.0 / (1.0 + zmax)), 1.0, 400)
    w = -1.0 - sp(np.log(aa), 1) / 3.0
    if weight == "uniform":
        W = np.ones_like(aa)
    else:  # DE-fraction
        f = make_f_fw(a, Sa)
        E = E_of(f, Om)
        W = (1.0 - Om) * f(aa) / E(aa) ** 2
    A = np.vstack([np.ones_like(aa), 1.0 - aa]).T
    WA = A * W[:, None]
    coef = np.linalg.solve(A.T @ WA, WA.T @ w)
    return float(coef[0]), float(coef[1])

def crossing_z(w0, wa):
    """z where CPL w=-1: a=1+(1+w0)/wa."""
    if wa == 0:
        return None
    a_c = 1.0 + (1.0 + w0) / wa
    if a_c <= 0:
        return None
    return 1.0 / a_c - 1.0

# ---------------------------------------------------------------------------
# 4. Run.
# ---------------------------------------------------------------------------
DESI = dict(w0=-0.838, wa=-0.62, cross_z=None)
DESI["cross_z"] = crossing_z(DESI["w0"], DESI["wa"])

def run_on(a, Sa, label):
    f = make_f_fw(a, Sa)
    zx_phys = phys_crossing_z(a, Sa)
    out = {"label": label, "phys_crossing_z": zx_phys}
    # distance-space (faithful)
    for tag, kw in [("dist_BAO+CMB", dict(use_cmb=True)),
                    ("dist_BAO_only", dict(use_cmb=False))]:
        w0, wa, c2 = project_distance(f, **kw)
        out[tag] = dict(w0=w0, wa=wa, cross_z=crossing_z(w0, wa), chi2=c2)
    # rho-space
    w0, wa, l = project_rho(f)
    out["rho_DEweighted"] = dict(w0=w0, wa=wa, cross_z=crossing_z(w0, wa))
    # w-space
    for wt in ("uniform", "DE"):
        w0, wa = project_w(a, Sa, weight=wt)
        out[f"w_{wt}"] = dict(w0=w0, wa=wa, cross_z=crossing_z(w0, wa))
    return out

results = {"desi": DESI, "note": "rho_DE ∝ S(a); E^2=Om a^-3+(1-Om)S/S1",
           "boxes": {}, "pooled": None, "per_box_summary": {}}

# per box
for cv, (a, Sa) in enumerate(box_curves):
    results["boxes"][f"CV_{cv}"] = run_on(a, Sa, f"CV_{cv}")
# pooled
results["pooled"] = run_on(a_grid, S_pooled, "pooled_6box")

# summarize across boxes for each method
methods = ["dist_BAO+CMB", "dist_BAO_only", "rho_DEweighted", "w_uniform", "w_DE"]
for m in methods:
    w0s = [results["boxes"][f"CV_{cv}"][m]["w0"] for cv in range(6)]
    was = [results["boxes"][f"CV_{cv}"][m]["wa"] for cv in range(6)]
    czs = [results["boxes"][f"CV_{cv}"][m]["cross_z"] for cv in range(6)]
    czs_ok = [z for z in czs if z is not None]
    results["per_box_summary"][m] = dict(
        w0_mean=float(np.mean(w0s)), w0_std=float(np.std(w0s)),
        wa_mean=float(np.mean(was)), wa_std=float(np.std(was)),
        cross_z_mean=float(np.mean(czs_ok)) if czs_ok else None,
        cross_z_std=float(np.std(czs_ok)) if czs_ok else None,
        cross_z_per_box=[None if z is None else round(z, 3) for z in czs])
phys_cz = [results["boxes"][f"CV_{cv}"]["phys_crossing_z"] for cv in range(6)]
phys_ok = [z for z in phys_cz if z is not None]
results["phys_crossing_summary"] = dict(
    per_box=[None if z is None else round(z, 3) for z in phys_cz],
    mean=float(np.mean(phys_ok)) if phys_ok else None,
    pooled=results["pooled"]["phys_crossing_z"])

with open(Path(HG).parent / "epoch_check" / "cpl_projection_results.json", "w") as fh:
    json.dump(results, fh, indent=2)

# ---- print ----
def fmt(d): return f"w0={d['w0']:+.3f} wa={d['wa']:+.3f} cross_z={('%.3f'%d['cross_z']) if d['cross_z'] is not None else 'none'}"
print("="*78)
print(f"DESI DR2 (Pantheon+):  w0={DESI['w0']:+.3f} wa={DESI['wa']:+.3f} "
      f"cross_z={DESI['cross_z']:.3f}")
print("="*78)
print(f"\nPHYSICAL crossing (S peak): per-box {results['phys_crossing_summary']['per_box']}")
print(f"  mean={results['phys_crossing_summary']['mean']:.3f}  "
      f"pooled={results['phys_crossing_summary']['pooled']}")
print("\n--- CPL-PROJECTED (per-box mean ± std across 6 boxes) ---")
for m in methods:
    s = results["per_box_summary"][m]
    cz = f"{s['cross_z_mean']:.3f}±{s['cross_z_std']:.3f}" if s['cross_z_mean'] is not None else "none"
    print(f"  {m:16s}: w0={s['w0_mean']:+.3f}±{s['w0_std']:.3f}  "
          f"wa={s['wa_mean']:+.3f}±{s['wa_std']:.3f}  cross_z={cz}")
    print(f"                     per-box cross_z={s['cross_z_per_box']}")
print("\n--- POOLED 6-box curve (sharpest; physical crossing z={:.2f}) ---".format(
    results['pooled']['phys_crossing_z']))
for m in methods:
    print(f"  {m:16s}: {fmt(results['pooled'][m])}")
print("\nwrote epoch_check/cpl_projection_results.json")
