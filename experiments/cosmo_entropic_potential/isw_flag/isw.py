#!/usr/bin/env python3
"""
ISW supervoid flag: our thawing background vs LambdaCDM.

Our frozen large-volume S(a) maps to E^2(a) = Om a^-3 + (1-Om) S(a)/S(1). Thawing
(w > -1 after z~0.6) => faster late-time potential decay => enhanced integrated
Sachs-Wolfe signal at supervoid redshifts. This computes OUR enhancement:

  potential  Phi(a) ∝ D(a)/a        (early-normalized D -> a; EdS => Phi const)
  ISW source Phi'   ∝ d(D/a)/deta = a^2 H d(D/a)/da,   H = H0 E(a)
  ratio      R_ISW(z) = Phi'_ours / Phi'_LCDM  (H0, Poisson prefactor cancel)
  window     A_ratio = ∫W(z)Phi'_ours / ∫W(z)Phi'_LCDM  over supervoid z-window

Verdict bands (DECISIONS.md, pre-stated): E* = A_ratio over [0.4,0.7].
  RELEVANT E*>=1.5 ; DISCRIMINANT 1.05<=E*<1.5 ; NEGLIGIBLE E*<1.05.

Growth ODE + E(a) + S->f_de mapping lifted verbatim from ../selfconsistency and
../epoch_check. CPU only. Incremental flush. No simulation reload.
"""
import json, time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
LV = HERE.parent / "large_volume" / "results.json"
RESULTS = HERE / "results.json"
OM = 0.300                     # TNG300/CAMELS box cosmology (the S(a) universe)

t0 = time.time()
out = {"date": "2026-07-11", "Om": OM,
       "mapping": "E^2 = Om a^-3 + (1-Om) S(a)/S(1)",
       "kernel": "Phi ∝ D/a ; ISW source ∝ d(D/a)/deta = a^2 E d(D/a)/da",
       "normalization": "D early-normalized (D->a as a->0); CMB-anchored primordial amplitude",
       "verdict_bands": {"RELEVANT": ">=1.5", "DISCRIMINANT": "1.05..1.5", "NEGLIGIBLE": "<1.05"}}

def flush():
    with open(RESULTS, "w") as fh:
        json.dump(out, fh, indent=2)

# ---------------------------------------------------------------------------
# 1. Backgrounds S(a): primary corner + complete-book (tiles 1e11) from frozen LV.
# ---------------------------------------------------------------------------
lv = json.load(open(LV))
recs = lv["stage2_primary"]["records"]
a_prim = np.array([r["a"] for r in recs])
S_prim = np.array([r["S"] for r in recs])
order = np.argsort(a_prim)
a_prim, S_prim = a_prim[order], S_prim[order]

a_cb = np.array(lv["stage4_tiles"]["a"])
S_cb = np.array(lv["stage4_tiles"]["S"])
order = np.argsort(a_cb)
a_cb, S_cb = a_cb[order], S_cb[order]

out["backgrounds"] = {
    "primary_corner": {"thr": "7.43e11", "a": a_prim.tolist(), "S": S_prim.tolist(),
                       "w_today": lv["stage5"]["primary"]["w_today"],
                       "S_peak_z": lv["stage5"]["primary"]["interior_peak_z"]},
    "complete_book_1e11": {"thr": "1e11 (tiled full box)", "a": a_cb.tolist(), "S": S_cb.tolist(),
                           "w_today": lv["stage5"]["tiles_1e11"]["w_today"],
                           "S_peak_z": lv["stage5"]["tiles_1e11"]["interior_peak_z"]}}
flush()

def make_f_de(a, Sa):
    """f_de(a) = rho_DE(a)/rho_DE(1) = S(a)/S(1); frozen (constant) below a_min."""
    sp = CubicSpline(np.log(a), np.log(Sa))
    S1 = np.exp(sp(0.0))
    amin = a.min(); lnSmin = sp(np.log(amin))
    def f(aa):
        aa = np.atleast_1d(np.asarray(aa, float))
        lnS = np.where(aa >= amin, sp(np.log(np.clip(aa, 1e-6, 1.0))), lnSmin)
        return np.exp(lnS) / S1
    return f

def E_of(f_de, Om=OM):
    return lambda a: np.sqrt(Om * np.asarray(a, float)**-3.0 + (1.0 - Om) * f_de(np.asarray(a, float)))

# ---------------------------------------------------------------------------
# 2. Growth under a smooth-DE background (ODE in ln a), early-normalized D->a.
#    D'' + (2 + dlnE/dlna) D' - 1.5 Om a^-3 / E^2 D = 0 ;  D -> a  (a -> 0).
#    (verbatim from selfconsistency.growth_of)
# ---------------------------------------------------------------------------
def growth_of(f_de, Om=OM, a_start=1e-3):
    E2 = lambda a: Om * a**-3 + (1.0 - Om) * float(np.ravel(f_de(a))[0])
    def dlnE_dlna(a, h=1e-4):
        return (np.log(E2(a * np.exp(h))) - np.log(E2(a * np.exp(-h)))) / (4 * h)
    def rhs(lna, y):
        a = np.exp(lna); D, Dp = y
        return [Dp, -(2.0 + dlnE_dlna(a)) * Dp + 1.5 * Om * a**-3 / E2(a) * D]
    sol = solve_ivp(rhs, [np.log(a_start), 0.0], [a_start, a_start],
                    dense_output=True, rtol=1e-9, atol=1e-13, method="RK45")
    return lambda a: sol.sol(np.log(np.asarray(a, float)))[0]

f_lcdm = lambda a: np.ones_like(np.asarray(a, float))
D_lcdm = growth_of(f_lcdm)
E_lcdm = E_of(f_lcdm)

# ---------------------------------------------------------------------------
# 3. ISW source Phi'(a) ∝ a^2 E(a) d(D/a)/da, on a fine a-grid. H0 cancels in ratios.
# ---------------------------------------------------------------------------
def isw_source(D_fun, E_fun, a):
    """Phi'(a) up to the common constant 4 pi G rho_m0 / H0 (cancels in ratios)."""
    a = np.asarray(a, float)
    da = a * 1e-4
    P = lambda x: D_fun(x) / x                    # potential ∝ D/a
    dP_da = (P(a + da) - P(a - da)) / (2 * da)    # central difference
    return a**2 * E_fun(a) * dP_da                # = d(D/a)/deta up to H0

# fine z-grid over (0,2); a in (1/3, 1)
z_grid = np.linspace(0.01, 2.0, 400)
a_grid = 1.0 / (1.0 + z_grid)

src_lcdm = isw_source(D_lcdm, E_lcdm, a_grid)

def run_variant(name, a_bg, S_bg):
    f_de = make_f_de(a_bg, S_bg)
    E_fun = E_of(f_de)
    D_fun = growth_of(f_de)
    src = isw_source(D_fun, E_fun, a_grid)
    ratio = src / src_lcdm                          # R_ISW(z), both sources negative
    # sanity: growth-suppression at z=0
    g0_ours = float(D_fun(1.0) / 1.0)
    g0_lcdm = float(D_lcdm(1.0) / 1.0)
    rec = {"name": name,
           "z": z_grid.tolist(),
           "R_ISW_z": ratio.tolist(),
           "src_ours_z": src.tolist(),
           "src_lcdm_z": src_lcdm.tolist(),
           "D_over_a_today_ours": g0_ours,
           "D_over_a_today_lcdm": g0_lcdm}
    # window integrals: A_ratio = ∫W Phi'_ours / ∫W Phi'_LCDM (same voids => W cancels no)
    def A_ratio(W):
        num = np.trapezoid(W * src, z_grid)
        den = np.trapezoid(W * src_lcdm, z_grid)
        return float(num / den)
    W_gns = ((z_grid >= 0.4) & (z_grid <= 0.7)).astype(float)          # GNS top-hat
    W_des = np.exp(-0.5 * ((z_grid - 0.52) / 0.15)**2)                 # DES/BOSS Gaussian
    W_broad = ((z_grid >= 0.2) & (z_grid <= 0.9)).astype(float)        # broad top-hat
    rec["A_ratio"] = {
        "primary_GNS_tophat_0.4_0.7": A_ratio(W_gns),
        "robust_DES_gauss_0.52_0.15": A_ratio(W_des),
        "broad_tophat_0.2_0.9": A_ratio(W_broad)}
    # point ratios at representative void redshifts
    rec["R_ISW_points"] = {f"z={z:.2f}": float(np.interp(z, z_grid, ratio))
                           for z in (0.2, 0.35, 0.5, 0.55, 0.7, 0.9, 1.2)}
    return rec

out["variants"] = {}
print(f"[{time.time()-t0:5.1f}s] LCDM: D/a(z=0) = {D_lcdm(1.0):.4f}")
for name, a_bg, S_bg in [("primary_corner", a_prim, S_prim),
                         ("complete_book_1e11", a_cb, S_cb)]:
    rec = run_variant(name, a_bg, S_bg)
    out["variants"][name] = rec
    E_star = rec["A_ratio"]["primary_GNS_tophat_0.4_0.7"]
    band = ("RELEVANT" if E_star >= 1.5 else
            "DISCRIMINANT" if E_star >= 1.05 else "NEGLIGIBLE")
    print(f"[{time.time()-t0:5.1f}s] {name}: E*(GNS 0.4-0.7) = {E_star:.3f}  -> {band}")
    print(f"           R_ISW at z=0.5 = {rec['R_ISW_points']['z=0.50']:.3f}, "
          f"z=0.55 = {rec['R_ISW_points']['z=0.55']:.3f}")
    print(f"           A_ratio DES-gauss = {rec['A_ratio']['robust_DES_gauss_0.52_0.15']:.3f}, "
          f"broad = {rec['A_ratio']['broad_tophat_0.2_0.9']:.3f}")
    flush()

# ---------------------------------------------------------------------------
# 4. Verdict (primary background, primary window).
# ---------------------------------------------------------------------------
E_star = out["variants"]["primary_corner"]["A_ratio"]["primary_GNS_tophat_0.4_0.7"]
band = ("RELEVANT" if E_star >= 1.5 else
        "DISCRIMINANT" if E_star >= 1.05 else "NEGLIGIBLE")
pct = 100.0 * (E_star - 1.0)
out["verdict"] = {
    "E_star_primary": E_star,
    "enhancement_pct": pct,
    "band": band,
    "complete_book_E_star": out["variants"]["complete_book_1e11"]["A_ratio"]["primary_GNS_tophat_0.4_0.7"]}

# Discriminant precision: our model predicts the LCDM ISW template amplitude is E* higher
# at the void window, so a measured A_ISW (obs/LCDM-expected) reads A_ISW/E* against our
# background. To SEPARATE the two backgrounds at n-sigma you need frac error on A_ISW
# below (E*-1)/n. Literature A_ISW fractional errors: Kovacs2019 5.2+/-1.6 (~0.31);
# Hang2021 voids -0.10+/-0.69 (undetected); NadathurCrittenden2016 1.64+/-0.53 (~0.32).
frac = E_star - 1.0
out["discriminant"] = {
    "template_shift_frac": frac,
    "sigmaA_over_A_needed_2sigma": frac / 2.0,
    "sigmaA_over_A_needed_1sigma": frac,
    "current_best_fracerr_examples": {"Kovacs2019_5.2pm1.6": 1.6/5.2,
                                      "NadathurCrittenden2016_1.64pm0.53": 0.53/1.64},
    "precision_improvement_factor_needed_vs_Kovacs2019_2sigma": (1.6/5.2)/(frac/2.0),
    "note": ("our background moves the expected supervoid ISW template up ~%.0f%%, so a "
             "measured A_ISW vs LCDM reads ~%.0f%% lower against our model; separating the "
             "two at 2sigma needs sigma(A_ISW)/A_ISW < %.3f, vs ~0.3 today." )
            % (100*frac, 100*frac, frac/2.0)}
flush()
print(f"\n[{time.time()-t0:5.1f}s] VERDICT: {band}  E* = {E_star:.3f} "
      f"({pct:+.1f}% at the supervoid window)")
print("wrote", RESULTS)
