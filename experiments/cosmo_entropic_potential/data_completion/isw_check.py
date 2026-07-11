#!/usr/bin/env python3
"""
Late-time ISW amplitude prediction for the FROZEN halo-grain w(z), relative to LCDM.

Physics
-------
Linear growth D(a) under a smooth (unclustered) dark energy, solved from deep matter
domination (D ∝ a, early-normalised so both models share the primordial amplitude):
    d2D/dN2 + (2 + dlnH/dN) dD/dN - (3/2) Om(N) D = 0 ,  N=ln a,
    Om(N) = Om a^-3 / E(a)^2 ,  dlnH/dN = (1/2) dln E^2/dN.

The late-ISW effect is sourced by the decay of the gravitational potential
    Phi(z) ∝ D(z) (1+z)            (Poisson: k^2 Phi ∝ Om a^-2 delta ∝ Om D/a)
so the ISW source is  dPhi/dz  (== 0 in matter domination where D∝a).

The galaxy×CMB cross-power that measures A_ISW is
    C_l^{Tg} ∝ ∫ dz W_g(z) (dPhi/dz) × (geometry, matter power),
and observers report A_ISW = (measured amplitude)/(LCDM-template amplitude). For two DE
models with identical primordial power and nearly identical low-z geometry, the geometric
factors cancel to leading order, so the framework's PREDICTED amplitude relative to the
LCDM template is
    A_ISW(fw) ≈ ∫ dz W(z) (dPhi_fw/dz) / ∫ dz W(z) (dPhi_LCDM/dz).

Reported three ways (robustness): net potential decay 0<z<z_hi (window-free), a broad
tomographic window (0<z<2), and a z_eff≈0.5 Gaussian tracer window (where ISW×galaxy
signal peaks). Both models evaluated at matched Om (clean w(z) effect) AND each at its own
joint-fit Om.
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
LV = CEP / "large_volume" / "results.json"
OM_R = 9.2e-5

# --- frozen framework S(a) -> f_de(a)=S/S1, and w(a) ---------------------------
lv = json.load(open(LV))
recs = lv["stage2_primary"]["records"]
A_S = np.array([r["a"] for r in recs]); S_S = np.array([r["S"] for r in recs])
o = np.argsort(A_S); A_S, S_S = A_S[o], S_S[o]
_sp_lnS = CubicSpline(np.log(A_S), np.log(S_S))
S1 = np.exp(_sp_lnS(0.0)); AMIN = A_S.min(); LNSMIN = _sp_lnS(np.log(AMIN))

def f_fw(a):
    a = np.atleast_1d(np.asarray(a, float))
    lnS = np.where(a >= AMIN, _sp_lnS(np.log(np.clip(a, 1e-6, 1.0))), LNSMIN)
    return np.exp(lnS) / S1

def dlnf_dlna_fw(a):
    a = np.atleast_1d(np.asarray(a, float))
    d = np.where(a >= AMIN, _sp_lnS(np.log(np.clip(a, 1e-6, 1.0)), 1), 0.0)
    return d

def w_fw(a):
    return -1.0 - dlnf_dlna_fw(a) / 3.0

def f_lcdm(a):
    return np.ones_like(np.atleast_1d(np.asarray(a, float)))

def dlnf_dlna_lcdm(a):
    return np.zeros_like(np.atleast_1d(np.asarray(a, float)))

# --- background E(a) and dln E^2/dN -------------------------------------------
def make_bg(f_de, dlnf, Om):
    Ode = 1.0 - Om - OM_R
    def E2(a):
        a = np.asarray(a, float)
        return OM_R * a**-4 + Om * a**-3 + Ode * f_de(a)
    def dlnE2_dN(a):   # dln E^2/dln a = (dE^2/dln a)/E^2
        a = np.asarray(a, float)
        dE2 = -4*OM_R*a**-4 - 3*Om*a**-3 + Ode * f_de(a) * dlnf(a)
        return dE2 / E2(a)
    return E2, dlnE2_dN

# --- linear growth ODE in N=ln a ----------------------------------------------
def growth(f_de, dlnf, Om, a_eval):
    E2, dlnE2_dN = make_bg(f_de, dlnf, Om)
    N0, N1 = np.log(1e-3), 0.0
    def rhs(N, y):
        a = np.exp(N); D, dD = y
        Om_a = Om * a**-3 / float(np.ravel(E2(a))[0])
        dlnH = 0.5 * float(np.ravel(dlnE2_dN(a))[0])
        ddD = -(2.0 + dlnH) * dD + 1.5 * Om_a * D
        return [dD, ddD]
    a0 = np.exp(N0)
    sol = solve_ivp(rhs, [N0, N1], [a0, a0], t_eval=np.log(a_eval),
                    rtol=1e-9, atol=1e-12, dense_output=True)
    return sol.y[0]   # D(a_eval)

# --- ISW amplitude relative to LCDM -------------------------------------------
def isw_amplitudes(Om_fw, Om_lcdm, z_hi=3.0):
    zg = np.linspace(0.0, z_hi, 1200)
    a = 1.0 / (1.0 + zg)
    ai = a[::-1]                                  # increasing a for the ODE
    D_fw = growth(f_fw, dlnf_dlna_fw, Om_fw, ai)[::-1]
    D_lc = growth(f_lcdm, dlnf_dlna_lcdm, Om_lcdm, ai)[::-1]
    # normalised potential P(z) = D(z)(1+z)/D(0)
    P_fw = D_fw * (1.0 + zg) / D_fw[0]
    P_lc = D_lc * (1.0 + zg) / D_lc[0]
    dP_fw = np.gradient(P_fw, zg)
    dP_lc = np.gradient(P_lc, zg)

    def ratio(W):
        num = np.trapezoid(W * dP_fw, zg)
        den = np.trapezoid(W * dP_lc, zg)
        return float(num / den)

    windows = {
        "net_decay_0_to_zhi": np.ones_like(zg),                       # window-free
        "broad_tomographic_0_2": (zg <= 2.0).astype(float),           # 0<z<2 uniform
        "gauss_zeff0.5": np.exp(-0.5 * ((zg - 0.5) / 0.3) ** 2),      # tracer-like
    }
    out = {k: ratio(W) for k, W in windows.items()}
    out["_note_net"] = "net_decay ratio == [P_fw(0)-P_fw(zhi)]/[P_lc(0)-P_lc(zhi)]"
    # growth suppression today (fsigma8-relevant sanity): D(0)/a normalised early
    out["D0_over_early_fw"] = float(D_fw[0])
    out["D0_over_early_lcdm"] = float(D_lc[0])
    return out

if __name__ == "__main__":
    # matched Om (isolate the w(z) effect) and each-at-own joint-fit Om
    OM_PLANCK = 0.3153
    OM_FW_FIT, OM_LC_FIT = 0.3160, 0.2980   # from joint_fit.py BAO+CMB+SNe
    res = {
        "w_today_framework": float(w_fw(1.0)[0]),
        "w_of_a_grid": {"a": A_S.tolist(), "w": w_fw(A_S).tolist()},
        "matched_Om_0.3153": isw_amplitudes(OM_PLANCK, OM_PLANCK),
        "each_own_jointfit_Om": isw_amplitudes(OM_FW_FIT, OM_LC_FIT),
        "published_A_ISW": {
            "unWISE_x_Planck_2110.13959": [0.96, 0.30],
            "RACS_ASKAP_2204.13436": [0.94, 0.42],
            "earlier_concordance": [1.14, 0.38],
            "note": "A_ISW measured relative to LCDM template; consistent with 1.0+/-0.3",
        },
    }
    (HERE / "isw_results.json").write_text(json.dumps(res, indent=2))
    print(f"framework w_today = {res['w_today_framework']:+.4f}")
    print("\nA_ISW(framework relative to LCDM):")
    for label in ("matched_Om_0.3153", "each_own_jointfit_Om"):
        print(f"  [{label}]")
        for k, v in res[label].items():
            if k.startswith("_") or k.startswith("D0"):
                continue
            print(f"      {k:24s}: {v:.4f}")
    print("\npublished A_ISW: unWISE 0.96+/-0.30, RACS 0.94+/-0.42, earlier 1.14+/-0.38")
