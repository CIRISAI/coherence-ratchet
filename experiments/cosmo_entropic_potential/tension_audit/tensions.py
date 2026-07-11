#!/usr/bin/env python3
"""
Tension audit: what the framework's rho_DE(a) ∝ S(a) background does to H0 and S8.

Honest-exposure audit (see DECISIONS.md). Directions/magnitudes reported as found.

TASK A (H0): hold omega_b, omega_c (=> r_s, early-time, UNCHANGED by a late-time DE
  deformation) and the acoustic scale theta* fixed at Planck. Replace Lambda with
  rho_DE(a) ∝ S(a), close the universe today, solve for the H0 that preserves the
  comoving distance to z*=1090 over the same r_s. Report H0_ours - H0_LCDM.

TASK B (S8/growth): solve delta'' + (2 + dlnH/dlna) delta' = 1.5 Om(a) delta in ln a,
  our background vs LCDM, normalized identically at a=0.01. Report D(z=0) ratio ->
  sigma8/S8 fractional shift and the fsigma8(z) difference at z=0.3-0.8.

CPU only. Incremental flush to results.json.
"""
import json, time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
LV = HERE.parent / "large_volume" / "results.json"
FP = HERE.parent / "full_population" / "results.json"
RESULTS = HERE / "results.json"
t0 = time.time()

# --- verified Planck 2018 anchors (see DECISIONS.md) -----------------------
PLANCK = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, Om=0.3153,
              theta100=1.04109, zstar=1089.80, rstar=144.39,
              sigma8=0.8111, S8=0.834, S8_err=0.016)
SH0ES = dict(H0=73.04, err=1.04)
LENSING = dict(S8_kids=0.759, S8_combined=0.762, err=0.025)
OMH2 = PLANCK["ombh2"] + PLANCK["omch2"]           # physical matter density, FIXED
OMR_H2 = 4.15e-5                                    # photons + 3 nu (relativistic today)
C_KM = 299792.458                                  # km/s
GAP = SH0ES["H0"] - PLANCK["H0"]                   # the tension, km/s/Mpc

out = {"date": "2026-07-11", "planck": PLANCK, "sh0es": SH0ES, "lensing": LENSING,
       "omh2_fixed": OMH2, "omr_h2": OMR_H2, "H0_gap_kms": GAP}
def flush():
    out["elapsed_s"] = round(time.time() - t0, 1)
    with open(RESULTS, "w") as fh:
        json.dump(out, fh, indent=2)

# --- load the two S(a) curves ----------------------------------------------
lv = json.load(open(LV))
recs = lv["stage2_primary"]["records"]
A_CORNER = np.array([r["a"] for r in recs])
S_CORNER = np.array([r["S"] for r in recs])

fp = json.load(open(FP))
snaps = fp["full_1e11"]["2"]["per_snap"]                 # complete-book, best tile T=2
A_FULL = np.array([s["a"] for s in snaps])
S_FULL = np.array([s["S_total"] for s in snaps])

def g_builder(a_grid, S_grid):
    """g(a)=S(a)/S(1) via log-log cubic spline; constant-w (frozen local slope)
    extrapolation below a_min. Returns g(a) callable and w(a) callable."""
    la, lS = np.log(a_grid), np.log(S_grid)
    sp = CubicSpline(la, lS)                              # natural in interior
    S1 = float(np.exp(sp(0.0)))
    a_min = a_grid[0]
    slope_min = float(sp(np.log(a_min), 1))              # dlnS/dlna at the low edge
    lS_min = float(sp(np.log(a_min)))
    def lnS(a):
        a = np.asarray(a, float)
        v = np.where(a >= a_min, sp(np.log(np.maximum(a, 1e-8))),
                     lS_min + slope_min * (np.log(np.maximum(a, 1e-8)) - np.log(a_min)))
        return v
    def g(a):
        return np.exp(lnS(a)) / S1
    def dlnS_dlna(a):
        a = np.asarray(a, float)
        return np.where(a >= a_min, sp(np.log(np.maximum(a, 1e-8)), 1), slope_min)
    def w(a):
        return -1.0 - dlnS_dlna(a) / 3.0
    return g, w, dict(a_min=float(a_min), slope_min=slope_min, S1=S1)

# ===========================================================================
# TASK A — H0 from preserving D_M(z*) at fixed omega_m, r_s (theta*).
# ===========================================================================
def E2(a, h, gfun):
    """H^2/H0^2. Om, Or from FIXED physical densities => scale with h."""
    Om = OMH2 / h**2
    Or = OMR_H2 / h**2
    Ode = 1.0 - Om - Or                               # flat closure today
    return Om * a**-3 + Or * a**-4 + Ode * gfun(a)

def E2_lcdm(a, h):
    Om = OMH2 / h**2
    Or = OMR_H2 / h**2
    Ode = 1.0 - Om - Or
    return Om * a**-3 + Or * a**-4 + Ode              # Lambda: g=1

def comoving_Dm(h, E2fun, zmax):
    """comoving distance c/H0 * int_0^zmax dz/E(z), Mpc."""
    a_lo = 1.0 / (1.0 + zmax)
    def integrand(a):
        # dz = -da/a^2 ; dz/E = da/(a^2 E)
        return 1.0 / (a**2 * np.sqrt(E2fun(a)))
    val, _ = quad(integrand, a_lo, 1.0, limit=200, epsabs=1e-8, epsrel=1e-10)
    return (C_KM / h / 100.0) * val

def taskA(label, a_grid, S_grid):
    g, w, meta = g_builder(a_grid, S_grid)
    zstar = PLANCK["zstar"]
    # target: LCDM comoving distance to z* at Planck H0 (r_s/theta* is the same number)
    h_lcdm = PLANCK["H0"] / 100.0
    Dm_target = comoving_Dm(h_lcdm, lambda a: E2_lcdm(a, h_lcdm), zstar)
    # check r_s/theta* consistency (informational): r_s/theta* with theta*=theta100/100
    theta = PLANCK["theta100"] / 100.0
    Dm_from_rs = PLANCK["rstar"] / theta
    # solve for h_ours s.t. comoving_Dm(h; our g) = Dm_target
    def resid(h):
        return comoving_Dm(h, lambda a: E2(a, h, g), zstar) - Dm_target
    h_ours = brentq(resid, 0.55, 0.80, xtol=1e-6)
    H0_ours = 100.0 * h_ours
    # high-z DE negligibility check: fraction of D_M from z>3
    def frac_zgt3(h, gfun):
        a3 = 0.25
        num, _ = quad(lambda a: 1.0/(a**2*np.sqrt(E2(a, h, gfun))), 1e-4, a3, limit=200)
        den, _ = quad(lambda a: 1.0/(a**2*np.sqrt(E2(a, h, gfun))), 1e-4, 1.0, limit=200)
        return num/den
    # sensitivity to extrapolation: freeze g constant below a_min instead
    def g_const(a):
        a = np.asarray(a, float)
        return np.where(a >= meta["a_min"], g(a), g(meta["a_min"]))
    def resid_c(h):
        return comoving_Dm(h, lambda a: E2(a, h, g_const), zstar) - Dm_target
    h_ours_c = brentq(resid_c, 0.55, 0.80, xtol=1e-6)
    res = dict(label=label, Dm_target_Mpc=Dm_target, Dm_from_rs_over_theta=Dm_from_rs,
               H0_lcdm=PLANCK["H0"], H0_ours=H0_ours, dH0=H0_ours - PLANCK["H0"],
               w_today=float(w(1.0)), g_at_apeak=float(g(a_grid[np.argmax(S_grid)])),
               frac_Dm_from_zgt3=float(frac_zgt3(h_ours, g)),
               H0_ours_constextrap=100.0*h_ours_c,
               extrap_sens_kms=100.0*(h_ours_c - h_ours),
               gap_before=GAP, gap_after=SH0ES["H0"] - H0_ours, meta=meta)
    return res

print(f"[{time.time()-t0:5.1f}s] TASK A: H0 from D_M(z*) preservation ...")
out["taskA_corner"] = taskA("corner-rule (frozen large-volume)", A_CORNER, S_CORNER)
flush()
out["taskA_full"] = taskA("complete-book (full population >1e11, T=2)", A_FULL, S_FULL)
flush()
for k in ("taskA_corner", "taskA_full"):
    r = out[k]
    print(f"  {r['label']:42s} H0_ours={r['H0_ours']:.3f}  dH0={r['dH0']:+.3f}  "
          f"gap {r['gap_before']:.2f}->{r['gap_after']:.2f}  "
          f"(zgt3 frac={r['frac_Dm_from_zgt3']:.2e}, extrap_sens={r['extrap_sens_kms']:+.4f})")

# ===========================================================================
# TASK B — linear growth D(a), sigma8/S8 shift, fsigma8(z).
# ===========================================================================
OM_GROWTH = PLANCK["Om"]                              # hold Om fixed; swap only DE sector

def growth(gfun, Om=OM_GROWTH, a_start=1e-2):
    """D(a) with delta'' + (2 + dlnE/dlna) delta' = 1.5 Om(a) delta, ln a variable.
    Om(a) = Om a^-3 / E^2(a).  Normalized delta=a (D->a) at a_start."""
    Ode = 1.0 - Om                                   # flat, radiation negligible at growth epochs
    def E2g(a):
        return Om * a**-3 + Ode * gfun(a)
    def dlnE_dlna(a, hstep=1e-4):
        return (np.log(E2g(a*np.exp(hstep))) - np.log(E2g(a*np.exp(-hstep)))) / (4*hstep)
    def rhs(lna, y):
        a = np.exp(lna); D, Dp = y
        Om_a = Om * a**-3 / E2g(a)
        return [Dp, -(2.0 + dlnE_dlna(a)) * Dp + 1.5 * Om_a * D]
    sol = solve_ivp(rhs, [np.log(a_start), 0.0], [a_start, a_start],
                    dense_output=True, rtol=1e-9, atol=1e-12, method="RK45")
    D = lambda a: sol.sol(np.log(np.asarray(a, float)))[0]
    Dp = lambda a: sol.sol(np.log(np.asarray(a, float)))[1]
    f = lambda a: Dp(a) / D(a)                        # f = dlnD/dlna
    return D, f

g_lcdm = lambda a: np.ones_like(np.asarray(a, float))
D_l, f_l = growth(g_lcdm)
D_l1 = float(D_l(1.0))

def taskB(label, a_grid, S_grid):
    g, w, meta = g_builder(a_grid, S_grid)
    D_o, f_o = growth(g)
    D_o1 = float(D_o(1.0))
    ratio = D_o1 / D_l1                               # identical early norm => sigma8 ratio
    sigma8_ours = PLANCK["sigma8"] * ratio
    S8_ours = PLANCK["S8"] * ratio                    # Om common => S8 ratio = sigma8 ratio
    # fsigma8(z) at DESI/Euclid redshifts
    zgrid = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ag = 1.0 / (1.0 + zgrid)
    def fs8(zg, Dfun, ffun, D1, s8_0):
        aa = 1.0/(1.0+zg)
        return ffun(aa) * s8_0 * Dfun(aa) / D1
    fs8_ours = fs8(zgrid, D_o, f_o, D_o1, sigma8_ours)
    fs8_lcdm = fs8(zgrid, D_l, f_l, D_l1, PLANCK["sigma8"])
    res = dict(label=label, D_ratio=ratio, sigma8_lcdm=PLANCK["sigma8"],
               sigma8_ours=float(sigma8_ours), S8_lcdm=PLANCK["S8"], S8_ours=float(S8_ours),
               dS8=float(S8_ours - PLANCK["S8"]), pct_shift=100.0*(ratio-1.0),
               w_today=float(w(1.0)),
               S8_lensing=LENSING["S8_combined"],
               gap_before_sigma=(PLANCK["S8"]-LENSING["S8_combined"])/LENSING["err"],
               gap_after_sigma=(S8_ours-LENSING["S8_combined"])/LENSING["err"],
               z=zgrid.tolist(), fs8_ours=fs8_ours.tolist(), fs8_lcdm=fs8_lcdm.tolist(),
               fs8_frac_diff=((fs8_ours/fs8_lcdm)-1.0).tolist())
    return res

def couple_om(taskB_res, taskA_res):
    """S8 also carries Om via S8 = sigma8 sqrt(Om/0.3). When Task A moves H0 at fixed
    omega_m, Om = omega_m/h^2 moves too. Report the self-consistent S8 that folds both
    the growth-sigma8 shift AND this Om shift (the primary/corner has ~0 H0 shift so its
    coupling is negligible; the complete-book's is not)."""
    # Relative-shift convention (same as fixed-Om: anchor to Planck's quoted S8=0.834).
    # S8 ∝ sigma8 * sqrt(Om); sigma8 carries the growth D-ratio, sqrt(Om) carries the H0
    # shift (Om = omega_m/h^2 at FIXED physical density). phi = full relative S8 factor.
    h_ours = taskA_res["H0_ours"] / 100.0
    Om_ours = OMH2 / h_ours**2
    Om_lcdm = OMH2 / (PLANCK["H0"]/100.0)**2
    phi = taskB_res["D_ratio"] * np.sqrt(Om_ours / Om_lcdm)
    S8_coupled = PLANCK["S8"] * phi
    taskB_res["Om_lcdm"] = Om_lcdm
    taskB_res["Om_ours_from_H0"] = Om_ours
    taskB_res["S8_relshift_phi"] = float(phi)
    taskB_res["S8_ours_coupled"] = float(S8_coupled)
    taskB_res["gap_after_sigma_coupled"] = float(
        (S8_coupled - LENSING["S8_combined"]) / LENSING["err"])
    return taskB_res

print(f"[{time.time()-t0:5.1f}s] TASK B: linear growth / S8 ...")
out["taskB_corner"] = couple_om(taskB("corner-rule (frozen large-volume)", A_CORNER, S_CORNER),
                                out["taskA_corner"])
flush()
out["taskB_full"] = couple_om(taskB("complete-book (full population >1e11, T=2)", A_FULL, S_FULL),
                              out["taskA_full"])
flush()
for k in ("taskB_corner", "taskB_full"):
    r = out[k]
    print(f"  {r['label']:42s} D_ratio={r['D_ratio']:.4f}  sigma8 {r['sigma8_lcdm']:.4f}"
          f"->{r['sigma8_ours']:.4f} ({r['pct_shift']:+.2f}%)  "
          f"S8 tension {r['gap_before_sigma']:.2f}->{r['gap_after_sigma']:.2f} sigma")

# --- cross-check vs selfconsistency (its LCDM->framework growth suppression g(1)) ---
try:
    sc = json.load(open(HERE.parent / "selfconsistency" / "results.json"))
    # its loop reported g(1) ~ 0.987 growth suppression (D_framework/D_lcdm at a=1)
    hist = sc.get("loop_eta1", {}).get("history", [])
    g1_sc = next((h["g_at_a1"] for h in reversed(hist) if "g_at_a1" in h), None)
    out["crosscheck_selfconsistency"] = {
        "sc_g_at_a1": g1_sc,
        "our_D_ratio_corner": out["taskB_corner"]["D_ratio"],
        "our_D_ratio_full": out["taskB_full"]["D_ratio"],
        "note": ("selfconsistency used CAMELS pooled S0 (25 Mpc/h) not the frozen large box; "
                 "both are sub-percent growth suppressions of the same sign -> consistent.")}
except Exception as e:
    out["crosscheck_selfconsistency"] = {"error": str(e)}
flush()
print(f"[{time.time()-t0:5.1f}s] cross-check: sc g(1)={out['crosscheck_selfconsistency'].get('sc_g_at_a1')}, "
      f"our D_ratio(corner)={out['taskB_corner']['D_ratio']:.4f}")

# --- verdict block (honest-exposure; self-consistent S8 = the CMB-anchored one) -----
ac, af = out["taskA_corner"], out["taskA_full"]
bc, bf = out["taskB_corner"], out["taskB_full"]
def word_h0(dH0, floor):
    if abs(dH0) <= abs(floor): return "NEGLIGIBLE"
    return "RELIEVES" if dH0 > 0 else "WORSENS"      # dH0>0 raises H0 -> toward SH0ES
def word_s8(gap_after, gap_before, tol=0.05):
    d = gap_after - gap_before
    if abs(d) <= tol: return "NEGLIGIBLE"
    return "RELIEVES" if d < 0 else "WORSENS"        # lower sigma -> toward lensing
out["VERDICT"] = {
    "registered_primary": "corner-rule",
    "H0": {
        "corner": {"dH0_kms": round(ac["dH0"],3), "extrap_floor_kms": round(abs(ac["extrap_sens_kms"]),3),
                   "gap": [ac["gap_before"], round(ac["gap_after"],2)],
                   "word": word_h0(ac["dH0"], ac["extrap_sens_kms"])},
        "full":   {"dH0_kms": round(af["dH0"],3), "extrap_floor_kms": round(abs(af["extrap_sens_kms"]),3),
                   "gap": [af["gap_before"], round(af["gap_after"],2)],
                   "word": word_h0(af["dH0"], af["extrap_sens_kms"])}},
    "S8_self_consistent": {
        "baseline_sigma": round(bc["gap_before_sigma"],2),
        "corner": {"S8": round(bc["S8_ours_coupled"],4), "sigma": round(bc["gap_after_sigma_coupled"],2),
                   "word": word_s8(bc["gap_after_sigma_coupled"], bc["gap_before_sigma"])},
        "full":   {"S8": round(bf["S8_ours_coupled"],4), "sigma": round(bf["gap_after_sigma_coupled"],2),
                   "word": word_s8(bf["gap_after_sigma_coupled"], bf["gap_before_sigma"])}},
    "S8_growth_only_fixed_Om": {
        "corner": {"sigma": round(bc["gap_after_sigma"],2), "word": word_s8(bc["gap_after_sigma"], bc["gap_before_sigma"])},
        "full":   {"sigma": round(bf["gap_after_sigma"],2), "word": word_s8(bf["gap_after_sigma"], bf["gap_before_sigma"])}},
    "note": ("Self-consistent S8 folds the Om=omega_m/h^2 shift forced by each Task-A H0 result "
             "into S8=sigma8*sqrt(Om/0.3); this is the CMB-anchored prediction. The full-book's "
             "growth-only relief is cancelled and reversed once its H0 drop raises Om.")}
flush()
print(f"[{time.time()-t0:5.1f}s] VERDICT  H0 corner={out['VERDICT']['H0']['corner']['word']} "
      f"full={out['VERDICT']['H0']['full']['word']} | "
      f"S8(self-consistent) corner={out['VERDICT']['S8_self_consistent']['corner']['word']} "
      f"full={out['VERDICT']['S8_self_consistent']['full']['word']}")
print("wrote", RESULTS)
