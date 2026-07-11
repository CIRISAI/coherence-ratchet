#!/usr/bin/env python3
"""
Self-consistency loop for the halo-grain dark-energy mapping -- TNG300-1 (205 Mpc/h)
LARGE-VOLUME primary curve. Companion / big-box replicate of
../selfconsistency/selfconsistency.py (which closed the loop on the pooled 6-box
CAMELS 25 Mpc/h curve). Same machinery, same pre-stated question:

    does the fixed point move TOWARD or AWAY from DESI?

WHAT CHANGES vs the CAMELS run:
  * S_0(a), k(a) come DIRECTLY from the measured primary B-total curve
    (large_volume/results.json -> stage2_primary.records, 10 snapshots at the
    corner threshold thr = 7.4253e11 Msun/h). No snapshot re-load; the curve is
    the published headline object for the big box.
  * Box cosmology is Planck2015 (the TNG300 background), NOT CAMELS: the
    s_of_a globals are patched to Om=0.3089, OL=0.6911, Ob=0.0486, h=0.6774,
    ns=0.9667, sigma8=0.8159 so sigma(M) is the box's own transfer/normalization.
  * The loop background Om = 0.3089 (Planck2015). Projection convention Om=0.3155
    is kept identical to the published pipeline (cpl_projection.py).

Everything else -- growth ODE (smooth DE, D->a early, fixed primordial amplitude),
Sheth-Tormen cumulative-count response R(a)=N_ST(>thr; sigma*g)/N_ST(>thr; sigma),
S_{i+1}=S_0*R^eta (eta=1 headline; 0.5/1.5 sensitivity), and the CPL projection
(lifted verbatim from cpl_projection.py) -- is identical.

Open-loop reference to reproduce (large_volume/results.json stage5.primary):
    dist_BAO+CMB (w0,wa)=(-0.7666,-0.7424) maha 1.363.

House rules: incremental flush to results.json after every stage.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
CEP = HERE.parent                                   # cosmo_entropic_potential/
HG = str(CEP / "halo_grain")
EPOCH = CEP / "epoch_check"
sys.path.insert(0, HG); sys.path.insert(0, str(CEP)); sys.path.insert(0, str(EPOCH))

import halo_grain as hg          # patches s_of_a globals to CAMELS; we override below
import s_of_a as S

# --- patch s_of_a globals to the TNG300 box (Planck2015) BEFORE building PowerSpectrum ---
S.OM     = 0.3089
S.OL     = 0.6911
S.OB     = 0.0486
S.H0H    = 0.6774
S.NS     = 0.9667
S.SIGMA8 = 0.8159

# reuse the published projection machinery verbatim (same lift pattern as the CAMELS run)
src = (EPOCH / "cpl_projection.py").read_text()
defs_src = src.split("# 4. Run.")[0]
cpl = {}
exec(compile(defs_src, str(EPOCH / "cpl_projection.py"), "exec"), cpl)
make_f_fw = cpl["make_f_fw"]; E_of = cpl["E_of"]
project_distance = cpl["project_distance"]; project_rho = cpl["project_rho"]
crossing_z = cpl["crossing_z"]; phys_crossing_z = cpl["phys_crossing_z"]

OM = 0.3089                     # TNG300 box cosmology (the loop's universe)
OM_PROJ = 0.3155                # cpl_projection.py's projection convention (kept)
DELTA_C = 1.686
ETA_HEAD = 1.0
LV_RESULTS = CEP / "large_volume" / "results.json"
RESULTS = HERE / "results.json"

out = {"date": "2026-07-10", "box": "TNG300-1 205 Mpc/h (Planck2015)",
       "eta_headline": ETA_HEAD, "Om_loop": OM, "Om_projection": OM_PROJ,
       "cosmology": {"Om": S.OM, "OL": S.OL, "Ob": S.OB, "h": S.H0H,
                     "ns": S.NS, "sigma8": S.SIGMA8},
       "desi": {"w0": -0.838, "wa": -0.62, "sig_w0": 0.055, "sig_wa": 0.20, "rho": -0.7},
       "openloop_reference_from_large_volume": {
           "dist_BAO+CMB": {"w0": -0.7666, "wa": -0.7424, "maha": 1.363},
           "rho_DEweighted": {"w0": -0.7383, "wa": -0.9774, "maha": 1.952}},
       "camels_comparison": {
           "note": "CAMELS pooled 6-box fixed point moved +0.05 sigma TOWARD DESI (dist).",
           "dist_open": {"w0": -0.784, "wa": -0.442, "maha": 2.42},
           "dist_fixed": {"w0": -0.788, "wa": -0.436, "maha": 2.37}}}

def flush():
    with open(RESULTS, "w") as fh:
        json.dump(out, fh, indent=2)

COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
def maha(w0, wa):
    d = np.array([w0 + 0.838, wa + 0.62])
    return float(np.sqrt(d @ COVINV @ d))

# ---------------------------------------------------------------------------
# 1. Measured S_0(a), k(a): TNG300 primary B-total curve at the corner threshold.
# ---------------------------------------------------------------------------
t0 = time.time()
lv = json.load(open(LV_RESULTS))
prim = lv["stage2_primary"]
THR = float(prim["thr"])                                   # 7.4253e11 Msun/h corner
recs = prim["records"]
A_GRID = np.array([r["a"] for r in recs])
S0 = np.array([r["S"] for r in recs])
K_MEAS = np.array([r["k"] for r in recs], dtype=float)
order = np.argsort(A_GRID)
A_GRID, S0, K_MEAS = A_GRID[order], S0[order], K_MEAS[order]

ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)   # Planck2015
out["THR_corner_Msun_h"] = THR
out["S0"] = {"a": A_GRID.tolist(), "S": S0.tolist(), "k": K_MEAS.tolist()}
out["timing_load_s"] = round(time.time() - t0, 1)
flush()
print(f"[{time.time()-t0:6.1f}s] TNG300 primary curve loaded (THR={THR:.3e}): "
      f"S(a={A_GRID[0]:.3f})={S0[0]:.1f}  S(a=1)={S0[-1]:.1f}  "
      f"phys_cross_z={phys_crossing_z(A_GRID, S0):.3f}")

# ---------------------------------------------------------------------------
# 2. Growth under a smooth-DE background (ODE in ln a). Same as CAMELS run.
#    D'' + (2 + dlnE/dlna) D' - 1.5 Om a^-3 / E^2 D = 0 ;  D -> a  (a -> 0).
# ---------------------------------------------------------------------------
def growth_of(f_de, Om=OM, a_start=1e-3):
    E2 = lambda a: Om * a**-3 + (1.0 - Om) * float(np.ravel(f_de(a))[0])
    def dlnE_dlna(a, h=1e-4):
        return (np.log(E2(a * np.exp(h))) - np.log(E2(a * np.exp(-h)))) / (4 * h)
    def rhs(lna, y):
        a = np.exp(lna)
        D, Dp = y
        return [Dp, -(2.0 + dlnE_dlna(a)) * Dp + 1.5 * Om * a**-3 / E2(a) * D]
    sol = solve_ivp(rhs, [np.log(a_start), 0.0], [a_start, a_start],
                    dense_output=True, rtol=1e-8, atol=1e-12, method="RK45")
    return lambda a: sol.sol(np.log(np.asarray(a, float)))[0]

f_lcdm = lambda a: np.ones_like(np.asarray(a, float))
D_ref = growth_of(f_lcdm)

# ---------------------------------------------------------------------------
# 3. Sheth-Tormen cumulative count N(>THR) and its response to growth ratio g.
# ---------------------------------------------------------------------------
LNM = np.linspace(np.log(THR), np.log(1e16), 400)
RHO_M = 2.775e11 * S.OM                                   # Msun/h / (Mpc/h)^3
R_L = (3.0 * np.exp(LNM) / (4.0 * np.pi * RHO_M)) ** (1.0 / 3.0)
SIG_M1 = np.array([np.sqrt(ps._sigma2(r, S.W_tophat)) for r in R_L])  # sigma(M, a=1)
DLNSIG_DLNM = np.gradient(np.log(SIG_M1), LNM)

def N_ST(sigma_of_M):
    """Cumulative ST count above THR (arbitrary normalization; only ratios used)."""
    nu = DELTA_C / sigma_of_M
    q, p, A = 0.707, 0.3, 0.3222
    nufnu = A * np.sqrt(2.0 * q * nu**2 / np.pi) * (1.0 + (q * nu**2) ** -p) \
            * np.exp(-q * nu**2 / 2.0)
    dn_dlnM = nufnu * np.abs(DLNSIG_DLNM) / np.exp(LNM)
    return float(np.trapezoid(dn_dlnM, LNM))

Dref_a = D_ref(A_GRID); Dref_1 = float(D_ref(1.0))
N_ref = np.array([N_ST(SIG_M1 * D / Dref_1) for D in Dref_a])

# validation: ST k(a) shape vs the MEASURED k(a) at the corner threshold
out["validation_ST_vs_measured_k"] = {
    "a": A_GRID.tolist(),
    "N_ST_norm_to_a1": (N_ref / N_ref[-1]).tolist(),
    "k_measured_norm_to_a1": (K_MEAS / K_MEAS[-1]).tolist(),
    "N_ST_global_lnslope": float(np.polyfit(np.log(A_GRID), np.log(N_ref/N_ref[-1]), 1)[0]),
    "k_measured_global_lnslope": float(np.polyfit(np.log(A_GRID), np.log(K_MEAS/K_MEAS[-1]), 1)[0]),
    "note": "ST is monotone in D: captures the formation channel; measured k adds "
            "the late merger decline (both curves peak interior at a~0.6)."}
flush()
print(f"[{time.time()-t0:6.1f}s] ST validation at corner threshold:")
print("   a           : " + " ".join(f"{x:5.2f}" for x in A_GRID))
print("   N_ST/N_ST(1): " + " ".join(f"{x:5.2f}" for x in N_ref / N_ref[-1]))
print("   k_meas/k(1) : " + " ".join(f"{x:5.2f}" for x in K_MEAS / K_MEAS[-1]))

# ---------------------------------------------------------------------------
# 4. The loop.
# ---------------------------------------------------------------------------
def response(f_de):
    D_fw = growth_of(f_de)
    g = D_fw(A_GRID) / Dref_a                    # early-normalized ratio (both D->a)
    N_fw = np.array([N_ST(SIG_M1 * Da * gi / Dref_1)
                     for Da, gi in zip(Dref_a, g)])
    return N_fw / N_ref, g

def run_loop(eta, S0curve, max_iter=15, tol=1e-4):
    S_i = S0curve.copy()
    history = []
    R = np.ones_like(S_i); g = np.ones_like(S_i)
    for it in range(max_iter + 1):
        f_i = make_f_fw(A_GRID, S_i)
        w0r, war, _ = project_rho(f_i, Om=OM_PROJ)
        rec = {"iter": it, "w0_rho": round(w0r, 4), "wa_rho": round(war, 4),
               "maha_rho": round(maha(w0r, war), 3),
               "phys_cross_z": (lambda z: None if z is None else round(z, 3))(
                   phys_crossing_z(A_GRID, S_i)),
               "R_min": round(float(R.min()), 4), "R_at_a1": round(float(R[-1]), 4),
               "g_min": round(float(g.min()), 4), "g_at_a1": round(float(g[-1]), 4)}
        history.append(rec)
        print(f"  it{it:2d}: w0={w0r:+.4f} wa={war:+.4f} maha={rec['maha_rho']:.2f} "
              f"cross_z={rec['phys_cross_z']} g(1)={rec['g_at_a1']:.3f} R(1)={rec['R_at_a1']:.3f}")
        R_new, g = response(f_i)
        S_new = S0curve * R_new ** eta
        dmax = float(np.max(np.abs(np.log(S_new / S_new[-1]) - np.log(S_i / S_i[-1]))))
        R = R_new; S_i = S_new
        if it > 0 and dmax < tol:
            history.append({"converged_at_iter": it, "dmax_lnshape": dmax})
            print(f"  converged: max|dln f| = {dmax:.2e}")
            break
    return S_i, history

print(f"\n[{time.time()-t0:6.1f}s] === LOOP eta={ETA_HEAD} (headline) ===")
S_star, hist = run_loop(ETA_HEAD, S0)
out["loop_eta1"] = {"history": hist, "S_star": S_star.tolist()}
flush()

# ---------------------------------------------------------------------------
# 5. Fixed point, projected exactly as the published pipeline projects.
# ---------------------------------------------------------------------------
def full_projection(a, Sa, label):
    f = make_f_fw(a, Sa)
    res = {"label": label, "phys_crossing_z": phys_crossing_z(a, Sa)}
    w0, wa, c2 = project_distance(f, Om=OM_PROJ, use_cmb=True)
    res["dist_BAO+CMB"] = {"w0": w0, "wa": wa, "cross_z": crossing_z(w0, wa),
                           "maha": maha(w0, wa)}
    w0, wa, _ = project_rho(f, Om=OM_PROJ)
    res["rho_DEweighted"] = {"w0": w0, "wa": wa, "cross_z": crossing_z(w0, wa),
                             "maha": maha(w0, wa)}
    sp = CubicSpline(np.log(a), np.log(Sa))
    aa = np.linspace(max(a.min(), 1/3.3), 1.0, 400)
    w = -1.0 - sp(np.log(aa), 1) / 3.0
    fE = E_of(f, OM_PROJ)
    W = (1 - OM_PROJ) * f(aa) / fE(aa) ** 2
    A2 = np.vstack([np.ones_like(aa), 1 - aa]).T
    coef = np.linalg.solve(A2.T @ (A2 * W[:, None]), (A2 * W[:, None]).T @ w)
    res["w_DE"] = {"w0": float(coef[0]), "wa": float(coef[1]),
                   "cross_z": crossing_z(float(coef[0]), float(coef[1])),
                   "maha": maha(float(coef[0]), float(coef[1]))}
    return res

print(f"\n[{time.time()-t0:6.1f}s] projecting open-loop (iter-0 reproduction) ...")
out["openloop_projection"] = full_projection(A_GRID, S0, "open-loop S0 (TNG300 primary)")
flush()
print(f"[{time.time()-t0:6.1f}s] projecting fixed point ...")
out["fixedpoint_projection"] = full_projection(A_GRID, S_star, "fixed point eta=1")
flush()

def show(tag, r):
    print(f"  {tag}: phys_cross_z={r['phys_crossing_z']:.3f}" if r['phys_crossing_z']
          else f"  {tag}: no crossing")
    for m in ("dist_BAO+CMB", "rho_DEweighted", "w_DE"):
        d = r[m]
        cz = f"{d['cross_z']:.3f}" if d["cross_z"] is not None else "none"
        print(f"    {m:15s} w0={d['w0']:+.4f} wa={d['wa']:+.4f} cross_z={cz} "
              f"maha={d['maha']:.2f}")
show("OPEN LOOP (reproduces large_volume stage5)", out["openloop_projection"])
show("FIXED POINT (eta=1)", out["fixedpoint_projection"])

# shift summary (headline)
ol = out["openloop_projection"]; fp = out["fixedpoint_projection"]
out["shift_eta1"] = {m: {"d_w0": round(fp[m]["w0"] - ol[m]["w0"], 4),
                         "d_wa": round(fp[m]["wa"] - ol[m]["wa"], 4),
                         "d_maha": round(fp[m]["maha"] - ol[m]["maha"], 4),
                         "toward_desi": bool(fp[m]["maha"] < ol[m]["maha"])}
                     for m in ("dist_BAO+CMB", "rho_DEweighted", "w_DE")}
flush()

# ---------------------------------------------------------------------------
# 6. Sensitivity: eta in {0.5, 1.5} (dist projection).
# ---------------------------------------------------------------------------
out["sensitivity_eta"] = {}
for eta in (0.5, 1.5):
    print(f"\n[{time.time()-t0:6.1f}s] === LOOP eta={eta} (sensitivity) ===")
    S_e, h_e = run_loop(eta, S0)
    f = make_f_fw(A_GRID, S_e)
    w0, wa, _ = project_distance(f, Om=OM_PROJ, use_cmb=True)
    out["sensitivity_eta"][str(eta)] = {
        "history_tail": h_e[-3:], "dist_BAO+CMB": {"w0": w0, "wa": wa,
        "cross_z": crossing_z(w0, wa), "maha": maha(w0, wa)}}
    print(f"  eta={eta}: dist w0={w0:+.4f} wa={wa:+.4f} maha={maha(w0, wa):.2f}")
    flush()

# ---------------------------------------------------------------------------
# 7. Jackknife spread on the fixed-point shift (8 spatial replicates, eta=1).
#    Bounds the shift against the box's own sampling noise.
# ---------------------------------------------------------------------------
jk = prim.get("jackknife", {})
if jk:
    print(f"\n[{time.time()-t0:6.1f}s] === jackknife fixed points (eta=1, dist proj) ===")
    out["jackknife_fixedpoint"] = {}
    for key in sorted(jk, key=lambda s: int(s)):
        S0_jk = np.array(jk[key], dtype=float)[order]
        # open loop
        f_o = make_f_fw(A_GRID, S0_jk)
        w0o, wao, _ = project_distance(f_o, Om=OM_PROJ, use_cmb=True)
        # fixed point
        S_fp, _ = run_loop(ETA_HEAD, S0_jk, max_iter=10, tol=3e-4)
        f_f = make_f_fw(A_GRID, S_fp)
        w0f, waf, _ = project_distance(f_f, Om=OM_PROJ, use_cmb=True)
        out["jackknife_fixedpoint"][key] = {
            "open": {"w0": w0o, "wa": wao, "maha": maha(w0o, wao)},
            "fixed": {"w0": w0f, "wa": waf, "maha": maha(w0f, waf)},
            "d_maha": round(maha(w0f, waf) - maha(w0o, wao), 4)}
        print(f"  jk{key}: open maha={maha(w0o,wao):.3f} -> fixed maha={maha(w0f,waf):.3f} "
              f"(d={out['jackknife_fixedpoint'][key]['d_maha']:+.4f})")
        flush()
    dmahas = [v["d_maha"] for v in out["jackknife_fixedpoint"].values()]
    out["jackknife_summary"] = {"d_maha_mean": float(np.mean(dmahas)),
                                "d_maha_std": float(np.std(dmahas)),
                                "n": len(dmahas)}
    flush()

out["timing_total_s"] = round(time.time() - t0, 1)
flush()
d = out["shift_eta1"]["dist_BAO+CMB"]
print(f"\n[{time.time()-t0:6.1f}s] done. dist shift (eta=1): "
      f"d_maha={d['d_maha']:+.4f} ({'TOWARD' if d['toward_desi'] else 'AWAY FROM'} DESI)")
print("wrote", RESULTS)
