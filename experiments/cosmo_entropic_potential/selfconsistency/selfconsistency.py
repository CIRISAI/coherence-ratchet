#!/usr/bin/env python3
"""
Self-consistency loop for the halo-grain dark-energy mapping.

THE GAP THIS CLOSES (one_ledger pressure test, 2026-07-10): the pipeline's S(a)
was measured in CAMELS boxes evolved under a FIXED LambdaCDM background, then
mapped to rho_DE = kappa*S(a) -- i.e. E^2(a) = Om a^-3 + (1-Om) S(a)/S(1). But
that E(a) is NOT LambdaCDM: the mapping's own dark energy changes H(a), which
changes linear growth, which changes halo formation, which changes the halo
count k(a) that drives the extensive B-total S(a). First-order pipeline, open
loop. Here we close it:

    S_0(a)  = measured pooled B-total (LambdaCDM background)
    E_i(a)  = background implied by S_i(a)
    D_i(a)  = linear growth under E_i  (ODE, smooth DE, no DE perturbations)
    R_i(a)  = N_ST(>M_thr; sigma*g_i(a)) / N_ST(>M_thr; sigma)   [Sheth-Tormen
              cumulative-count response; g_i = D_i/D_ref, both early-normalized
              (fixed primordial amplitude / CMB-anchored)]
    S_{i+1}(a) = S_0(a) * R_i(a)^eta      [eta = dlnS/dlnk channel; T-E3
              extensive S ~ k*sbar => eta = 1 headline; 0.5/1.5 sensitivity]
    iterate to the fixed point S* = S_0 * R(background(S*))^eta.

The response model perturbs ONLY the halo-formation channel (k via the mass
function). The geometric per-unit factor sbar (normalized C at halo positions)
is held fixed: linear bias and growth cancel in C exactly (halo_grain SUMMARY,
"governing theoretical point"), so its background response is second order.
The late-time ~9% merger-driven k decline is NOT modeled (ST is monotone in D);
only the DIFFERENTIAL response to the background enters, and it is
formation-dominated. Flagged in SUMMARY.

Pre-stated question: does the fixed-point (w0,wa), CPL-projected exactly as in
epoch_check/cpl_projection.py, move TOWARD or AWAY from DESI's (-0.838,-0.62)?
Published open-loop pooled numbers to beat: dist_BAO+CMB (-0.784,-0.442) 2.42sig;
rho_DEweighted (-0.777,-0.531) 2.03sig; w_DE (-0.786,-0.519) 1.89sig; LCDM 3.28sig.

Incremental writes to results.json after every stage (house discipline).
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
HG = str(HERE.parent / "halo_grain")
PARENT = str(HERE.parent)
EPOCH = HERE.parent / "epoch_check"
sys.path.insert(0, HG); sys.path.insert(0, PARENT); sys.path.insert(0, str(EPOCH))

import halo_grain as hg          # patches s_of_a globals to CAMELS cosmology
import s_of_a as S

# reuse the published projection machinery verbatim
import importlib.util
spec = importlib.util.spec_from_file_location("cplproj", EPOCH / "cpl_projection.py")
# cpl_projection.py runs its whole pipeline on import; we only want its functions.
# Extract them by executing up to the "4. Run" section: simplest robust route is to
# reimplement nothing and instead lift the functions by reading the module source
# and exec'ing only the definitions (everything above the RUN marker).
src = (EPOCH / "cpl_projection.py").read_text()
defs_src = src.split("# 4. Run.")[0]
cpl = {}
exec(compile(defs_src, str(EPOCH / "cpl_projection.py"), "exec"), cpl)
make_f_fw = cpl["make_f_fw"]; E_of = cpl["E_of"]
project_distance = cpl["project_distance"]; project_rho = cpl["project_rho"]
crossing_z = cpl["crossing_z"]; phys_crossing_z = cpl["phys_crossing_z"]
f_cpl = cpl["f_cpl"]

OM = 0.300                      # CAMELS box cosmology (the loop's universe)
OM_PROJ = 0.3155                # cpl_projection.py's projection convention (kept)
DELTA_C = 1.686
ETA_HEAD = 1.0
RESULTS = HERE / "results.json"
out = {"date": "2026-07-10", "eta_headline": ETA_HEAD, "Om_loop": OM,
       "Om_projection": OM_PROJ,
       "desi": {"w0": -0.838, "wa": -0.62, "sig_w0": 0.055, "sig_wa": 0.20, "rho": -0.7},
       "published_openloop_pooled": {
           "dist_BAO+CMB": {"w0": -0.784, "wa": -0.442, "maha": 2.42},
           "rho_DEweighted": {"w0": -0.777, "wa": -0.531, "maha": 2.03},
           "w_DE": {"w0": -0.786, "wa": -0.519, "maha": 1.89},
           "LCDM_maha": 3.28}}

def flush():
    with open(RESULTS, "w") as fh:
        json.dump(out, fh, indent=2)

COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
def maha(w0, wa):
    d = np.array([w0 + 0.838, wa + 0.62])
    return float(np.sqrt(d @ COVINV @ d))

# ---------------------------------------------------------------------------
# 1. Measured S_0(a): pooled B-total, all 6 boxes (identical to cpl_projection).
# ---------------------------------------------------------------------------
t0 = time.time()
ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
THR = 1e11
box_curves = []
for cv in range(6):
    snaps = [hg.load_snapshot(s, cv=cv) for s in hg.SNAPS]
    recs = hg.op_B(ps, snaps, THR)
    a = np.array([r["a"] for r in recs]); Sa = np.array([r["S"] for r in recs])
    ok = np.isfinite(Sa) & (Sa > 0)
    box_curves.append((a[ok], Sa[ok]))
A_GRID = box_curves[0][0]
S0_POOL = np.sum([c[1] for c in box_curves], axis=0)
out["S0_pooled"] = {"a": A_GRID.tolist(), "S": S0_POOL.tolist()}
out["timing_load_s"] = round(time.time() - t0, 1)
flush()
print(f"[{time.time()-t0:6.1f}s] S0 pooled loaded: S(a=0.25)={S0_POOL[0]:.1f} "
      f"S(a=1)={S0_POOL[-1]:.1f} phys_cross_z={phys_crossing_z(A_GRID, S0_POOL):.3f}")

# ---------------------------------------------------------------------------
# 2. Growth under an arbitrary smooth-DE background (ODE in ln a).
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

# reference: LambdaCDM, the background the boxes were actually evolved under
f_lcdm = lambda a: np.ones_like(np.asarray(a, float))
D_ref = growth_of(f_lcdm)

# ---------------------------------------------------------------------------
# 3. Sheth-Tormen cumulative count N(>M_thr) and its response to growth ratio g.
# ---------------------------------------------------------------------------
LNM = np.linspace(np.log(THR), np.log(1e16), 400)
RHO_M = 2.775e11 * S.OM                                   # Msun/h / (Mpc/h)^3
R_L = (3.0 * np.exp(LNM) / (4.0 * np.pi * RHO_M)) ** (1.0 / 3.0)
SIG_M1 = np.array([np.sqrt(ps._sigma2(r, S.W_tophat)) for r in R_L])  # sigma(M, a=1), LCDM norm
DLNSIG_DLNM = np.gradient(np.log(SIG_M1), LNM)

def N_ST(sigma_of_M):
    """Cumulative ST count above THR (arbitrary normalization; only ratios used)."""
    nu = DELTA_C / sigma_of_M
    q, p, A = 0.707, 0.3, 0.3222
    nufnu = A * np.sqrt(2.0 * q * nu**2 / np.pi) * (1.0 + (q * nu**2) ** -p) \
            * np.exp(-q * nu**2 / 2.0)
    dn_dlnM = nufnu * np.abs(DLNSIG_DLNM) / np.exp(LNM)   # rho_m/M^2 * M -> 1/M; const dropped
    return float(np.trapezoid(dn_dlnM, LNM))

Dref_a = D_ref(A_GRID); Dref_1 = float(D_ref(1.0))
N_ref = np.array([N_ST(SIG_M1 * D / Dref_1) for D in Dref_a])

# validation: ST k(a) shape vs the measured pooled k(a)
k_meas = None
try:
    krec = json.load(open(Path(HG) / "results.json"))["mass_function_k_of_a"]["1e11"]
    k_meas = np.array([r["k"] for r in krec])  # CV_0
except Exception:
    pass
out["validation_ST_vs_measured_k"] = {
    "a": A_GRID.tolist(),
    "N_ST_norm_to_a1": (N_ref / N_ref[-1]).tolist(),
    "k_measured_CV0_norm_to_a1": (k_meas / k_meas[-1]).tolist() if k_meas is not None else None,
    "note": "ST is monotone in D: captures formation channel, misses the ~9% late merger decline."}
flush()
print(f"[{time.time()-t0:6.1f}s] ST validation: N_ST(a)/N_ST(1) = "
      + " ".join(f"{x:.2f}" for x in N_ref / N_ref[-1]))
if k_meas is not None:
    print(f"          measured k(a)/k(1) (CV_0) = "
          + " ".join(f"{x:.2f}" for x in k_meas / k_meas[-1]))

# ---------------------------------------------------------------------------
# 4. The loop.
# ---------------------------------------------------------------------------
def response(f_de):
    """R(a) on A_GRID for a background f_de, vs the LCDM reference."""
    D_fw = growth_of(f_de)
    g = D_fw(A_GRID) / Dref_a                    # early-normalized ratio (both D->a)
    N_fw = np.array([N_ST(SIG_M1 * Da * gi / Dref_1)
                     for Da, gi in zip(Dref_a, g)])
    return N_fw / N_ref, g

def run_loop(eta, max_iter=15, tol=1e-4, track_dist=False):
    S_i = S0_POOL.copy()
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
        S_new = S0_POOL * R_new ** eta
        dmax = float(np.max(np.abs(np.log(S_new / S_new[-1]) - np.log(S_i / S_i[-1]))))
        R = R_new
        S_i = S_new
        if it > 0 and dmax < tol:
            history.append({"converged_at_iter": it, "dmax_lnshape": dmax})
            print(f"  converged: max|dln f| = {dmax:.2e}")
            break
    return S_i, history

print(f"\n[{time.time()-t0:6.1f}s] === LOOP eta={ETA_HEAD} (headline) ===")
S_star, hist = run_loop(ETA_HEAD)
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
out["openloop_projection"] = full_projection(A_GRID, S0_POOL, "open-loop S0")
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
show("OPEN LOOP (reproduces published)", out["openloop_projection"])
show("FIXED POINT (eta=1)", out["fixedpoint_projection"])

# ---------------------------------------------------------------------------
# 6. Sensitivity: eta in {0.5, 1.5}; per-box fixed points (dist projection only).
# ---------------------------------------------------------------------------
out["sensitivity_eta"] = {}
for eta in (0.5, 1.5):
    print(f"\n[{time.time()-t0:6.1f}s] === LOOP eta={eta} (sensitivity) ===")
    S_e, h_e = run_loop(eta)
    f = make_f_fw(A_GRID, S_e)
    w0, wa, _ = project_distance(f, Om=OM_PROJ, use_cmb=True)
    out["sensitivity_eta"][str(eta)] = {
        "history_tail": h_e[-3:], "dist_BAO+CMB": {"w0": w0, "wa": wa,
        "cross_z": crossing_z(w0, wa), "maha": maha(w0, wa)}}
    print(f"  eta={eta}: dist w0={w0:+.4f} wa={wa:+.4f} maha={maha(w0, wa):.2f}")
    flush()

out["per_box_fixedpoint"] = {}
print(f"\n[{time.time()-t0:6.1f}s] === per-box fixed points (eta=1, dist proj) ===")
for cv, (a_b, S_b) in enumerate(box_curves):
    S0_save, A_save = S0_POOL, A_GRID
    # rebind loop globals to this box
    globals()["S0_POOL"], globals()["A_GRID"] = S_b, a_b
    Dref_a_b = D_ref(a_b)
    globals()["Dref_a"] = Dref_a_b
    globals()["N_ref"] = np.array([N_ST(SIG_M1 * D / Dref_1) for D in Dref_a_b])
    S_fp, _ = run_loop(ETA_HEAD, max_iter=10, tol=3e-4)
    f = make_f_fw(a_b, S_fp)
    w0, wa, _ = project_distance(f, Om=OM_PROJ, use_cmb=True)
    out["per_box_fixedpoint"][f"CV_{cv}"] = {"w0": w0, "wa": wa,
                                             "maha": maha(w0, wa)}
    print(f"  CV_{cv}: w0={w0:+.4f} wa={wa:+.4f} maha={maha(w0, wa):.2f}")
    globals()["S0_POOL"], globals()["A_GRID"] = S0_save, A_save
    globals()["Dref_a"] = D_ref(A_save)
    globals()["N_ref"] = np.array([N_ST(SIG_M1 * D / Dref_1) for D in D_ref(A_save)])
    flush()

pb = out["per_box_fixedpoint"]
out["per_box_summary"] = {
    "w0_mean": float(np.mean([v["w0"] for v in pb.values()])),
    "w0_std": float(np.std([v["w0"] for v in pb.values()])),
    "wa_mean": float(np.mean([v["wa"] for v in pb.values()])),
    "wa_std": float(np.std([v["wa"] for v in pb.values()]))}
out["timing_total_s"] = round(time.time() - t0, 1)
flush()
print(f"\n[{time.time()-t0:6.1f}s] done. per-box fixed point: "
      f"w0={out['per_box_summary']['w0_mean']:+.3f}±{out['per_box_summary']['w0_std']:.3f} "
      f"wa={out['per_box_summary']['wa_mean']:+.3f}±{out['per_box_summary']['wa_std']:.3f}")
print("wrote", RESULTS)
