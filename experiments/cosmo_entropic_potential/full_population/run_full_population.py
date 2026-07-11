#!/usr/bin/env python3
"""
Full-population tiled S(a): the aperture law's pre-registered decider (DECISIONS.md).
Two-level nested estimator S_total = S_intra (Sigma tile log-dets) + S_inter (tile-centroid
log-det). Continuity gate at the corner threshold vs the exact cap=38000 result; if a tile
size passes, run the full m200>1e11 population (no cap). GPU op_B machinery copied verbatim
from ../large_volume/run_test.py. Incremental flush. No synthetic data; no subsampling unless
a tile exceeds 38000 (contingency, DECISIONS.md §7).
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
HG = CEP / "halo_grain"; EPOCH = CEP / "epoch_check"; DESIV2 = CEP / "desi_likelihood_v2"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))
import s_of_a as S
csrc = (EPOCH / "cpl_projection.py").read_text(); cpl_ns = {"np": np}
exec("import numpy as np\nfrom scipy.integrate import quad\n"
     "from scipy.interpolate import CubicSpline\nfrom scipy.optimize import minimize\n"
     "C_KM = 299792.458\nZ_STAR = 1089.0\n", cpl_ns)
exec(compile(csrc.split("# 2. Backgrounds.")[1].split("# 4. Run.")[0],
             str(EPOCH / "cpl_projection.py"), "exec"), cpl_ns)
make_f_fw = cpl_ns["make_f_fw"]; project_distance = cpl_ns["project_distance"]; crossing_z = cpl_ns["crossing_z"]
sys.path.insert(0, str(DESIV2)); import likelihood_fit as lf
COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]]); COVINV = np.linalg.inv(COV)
def maha_pt(w0, wa, c0=-0.838, c1=-0.62):
    d = np.array([w0-c0, wa-c1]); return float(np.sqrt(d @ COVINV @ d))
maha = lambda w0, wa: maha_pt(w0, wa)
def maha_to(w0, wa, w0e, wae):  # DESI-metric distance from the exact point
    d = np.array([w0-w0e, wa-wae]); return float(np.sqrt(d @ COVINV @ d))
OM_PROJ = 0.3155

import cupy as cp
def make_xi_table(ps, R_smooth=1.0, rmin=0.02, rmax=180.0, n=400_000):
    xi = ps.xi_spline(R_smooth); sig2 = ps.sigma2_R(R_smooth)
    r = np.logspace(np.log10(rmin), np.log10(rmax), n); return cp.asarray(r), cp.asarray(xi(r)/sig2), float(sig2)
def _chol(C, bs=2048):
    from cupyx.scipy.linalg import solve_triangular
    k = C.shape[0]
    for j in range(0, k, bs):
        je = min(j+bs, k); Cjj = C[j:je, j:je]
        if j > 0: Lp = C[j:je, :j]; Cjj -= Lp @ Lp.T
        try: Ld = cp.linalg.cholesky(Cjj)
        except Exception: return False
        if bool(cp.isnan(cp.diagonal(Ld)).any()) or bool((cp.diagonal(Ld) <= 0).any()): return False
        C[j:je, j:je] = Ld
        if je < k:
            panel = C[je:, j:je]
            if j > 0: panel -= C[je:, :j] @ C[j:je, :j].T
            C[je:, j:je] = solve_triangular(Ld, panel.T, lower=True).T
    return True
def S_gpu(pos, box, xr, xv, jitter=0.0, tile=1024):
    k = len(pos)
    if k < 3: return None
    P = cp.asarray(pos, dtype=cp.float64); C = cp.empty((k, k), dtype=cp.float64)
    for i0 in range(0, k, tile):
        i1 = min(i0+tile, k); d2 = cp.zeros((i1-i0, k), dtype=cp.float64)
        for ax in range(3):
            dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax]); cp.minimum(dx, box-dx, out=dx); dx *= dx; d2 += dx
        cp.sqrt(d2, out=d2); cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2); C[i0:i1] = cp.interp(d2, xr, xv); del d2, dx
    idx = cp.arange(k); C[idx, idx] = 1.0 + jitter; cp.get_default_memory_pool().free_all_blocks()
    if not _chol(C):
        del C; cp.get_default_memory_pool().free_all_blocks()
        P = cp.asarray(pos, dtype=cp.float64); C = cp.empty((k, k), dtype=cp.float64)
        for i0 in range(0, k, tile):
            i1 = min(i0+tile, k); d2 = cp.zeros((i1-i0, k), dtype=cp.float64)
            for ax in range(3):
                dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax]); cp.minimum(dx, box-dx, out=dx); dx *= dx; d2 += dx
            cp.sqrt(d2, out=d2); cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2); C[i0:i1] = cp.interp(d2, xr, xv); del d2, dx
        idx = cp.arange(k); C[idx, idx] = 1.0 + 1e-8
        if not _chol(C): del C; cp.get_default_memory_pool().free_all_blocks(); return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum()); del C; cp.get_default_memory_pool().free_all_blocks()
    return Sval

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]; BOX = 205.0; SEED_BASE = 20260710
TILE_MAX = 38000
snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64), m200=d["m200"].astype(np.float64)))
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng); LCDM_CHI2 = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)["chi2"]
T0 = time.time(); log = lambda m: print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)
GATE_W0E, GATE_WAE = -0.7666191523146305, -0.7423928100872467

def tiled_S(pos, T, seed0):
    """Return dict with S_intra, S_inter, S_total, occupancy, n_flagged."""
    side = BOX / T
    idx = np.clip(np.floor(pos / side).astype(int), 0, T-1)
    tid = idx[:, 0]*T*T + idx[:, 1]*T + idx[:, 2]
    S_intra = 0.0; reps = []; occ = []; nflag = 0
    for t in range(T**3):
        sel = pos[tid == t]; n = len(sel); occ.append(int(n))
        if n == 0: continue
        reps.append(sel.mean(axis=0))
        if n > TILE_MAX:
            nflag += 1
            sel = sel[np.random.RandomState(seed0 + t).choice(n, TILE_MAX, replace=False)]
        s = S_gpu(sel, BOX, XR, XV)
        if s is not None: S_intra += s
    reps = np.array(reps)
    S_inter = S_gpu(reps, BOX, XR, XV) if len(reps) >= 3 else 0.0
    return dict(S_intra=float(S_intra), S_inter=float(S_inter or 0.0),
                S_total=float(S_intra + (S_inter or 0.0)),
                occ_min=int(min(occ)), occ_max=int(max(occ)), n_tiles=int(sum(o > 0 for o in occ)),
                n_flagged=int(nflag))

def analyze(a, Sa):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float)
    ok = np.isfinite(Sa) & (Sa > 0); a_ok, S_ok = a[ok], Sa[ok]; o = np.argsort(a_ok); a_ok, S_ok = a_ok[o], S_ok[o]
    if len(a_ok) < 4: return {"z_peak": None}
    imax = int(np.argmax(S_ok))
    w0, wa, c2 = project_distance(make_f_fw(a_ok, S_ok), Om=OM_PROJ, use_cmb=True)
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    return dict(z_peak=float(1/a_ok[imax]-1), peak_at_endpoint=bool(imax in (0, len(a_ok)-1)),
                w0=float(w0), wa=float(wa), cross_z=crossing_z(w0, wa), maha=maha(w0, wa),
                maha_to_exact=maha_to(w0, wa, GATE_W0E, GATE_WAE),
                chi2=float(prof["chi2"]), chi2_minus_lcdm=float(prof["chi2"]-LCDM_CHI2))

RES = HERE / "results.json"
out = {"date": "2026-07-10", "grid_snaps": SNAPS, "lcdm_chi2": LCDM_CHI2,
       "gate_exact": {"w0": GATE_W0E, "wa": GATE_WAE, "maha": 1.3626, "z_peak": 0.546},
       "jackknife_yardstick": {"w_today_err68": 0.057, "crossing_z_err68": 0.025},
       "gate": {}, "full_1e11": {}, "full_2e11": {}}
def flush():
    with open(RES, "w") as fh: json.dump(out, fh, indent=1)
flush()
log(f"LCDM chi2={LCDM_CHI2:.4f}. Gate target (w0,wa)=({GATE_W0E:.4f},{GATE_WAE:.4f}) maha=1.363")

def run_pop(mass_cut, tag, Tlist):
    res = {}
    for T in Tlist:
        rec = {"T": T, "tile_size_Mpch": BOX/T, "per_snap": []}
        a_arr, Sint, Stot = [], [], []
        for si, sd in enumerate(snapdata):
            pos = sd["pos"][sd["m200"] > mass_cut]
            r = tiled_S(pos, T, SEED_BASE + 1000000*T + 1000*si)
            r.update(a=sd["a"], z=sd["z"], n=int(len(pos)))
            rec["per_snap"].append(r); a_arr.append(sd["a"]); Sint.append(r["S_intra"]); Stot.append(r["S_total"])
            flush()
        rec["S_total_analysis"] = analyze(a_arr, Stot)
        rec["S_extensive_analysis"] = analyze(a_arr, Sint)
        res[str(T)] = rec; flush()
        at = rec["S_total_analysis"]; ae = rec["S_extensive_analysis"]
        log(f"  [{tag}] T={T}: TOTAL z_peak={at['z_peak']:.3f} maha={at['maha']:.3f} "
            f"m2exact={at['maha_to_exact']:.3f} chi2dL={at['chi2_minus_lcdm']:+.3f} | "
            f"EXT z_peak={ae['z_peak']:.3f} maha={ae['maha']:.3f} m2exact={ae['maha_to_exact']:.3f} "
            f"| occ[{rec['per_snap'][5]['occ_min']},{rec['per_snap'][5]['occ_max']}] flagged={sum(p['n_flagged'] for p in rec['per_snap'])}")
    return res

# ---- CONTINUITY GATE (corner threshold, all three T) ----
log("=== CONTINUITY GATE (corner threshold 7.4253e11) ===")
out["gate"] = run_pop(7.4253e11, "GATE", [2, 4, 8]); flush()

def gate_pass(analysis):
    return (analysis["z_peak"] is not None and 0.35 <= analysis["z_peak"] <= 0.85
            and analysis["maha_to_exact"] <= 1.0)
passed = {}
for T, rec in out["gate"].items():
    p_tot = gate_pass(rec["S_total_analysis"]); p_ext = gate_pass(rec["S_extensive_analysis"])
    passed[T] = {"total": p_tot, "extensive": p_ext,
                 "m2e_total": rec["S_total_analysis"]["maha_to_exact"],
                 "m2e_ext": rec["S_extensive_analysis"]["maha_to_exact"]}
out["gate_pass"] = passed; flush()
log(f"GATE results: {json.dumps(passed)}")

# best passing tile = min maha_to_exact among tiles that pass on the PRIMARY (total) estimator
best = [(T, p["m2e_total"]) for T, p in passed.items() if p["total"]]
if not best:
    # fall back: any tile passing on extensive (report but flag)
    best_ext = [(T, p["m2e_ext"]) for T, p in passed.items() if p["extensive"]]
    out["gate_verdict"] = "ESTIMATOR-FAILURE (no tile passes on PRIMARY S_total)"
    out["gate_pass_extensive_only"] = best_ext
    flush(); log(f"GATE FAILED on primary. extensive-passing: {best_ext}. STOPPING per DECISIONS.md.")
    log("=" * 60); log("DONE (gate failure)"); sys.exit(0)
best_T = sorted(best, key=lambda x: x[1])[0][0]
out["best_tile"] = best_T; flush()
log(f"GATE PASSED. best tile T={best_T} (min maha_to_exact={dict(best)[best_T]:.3f})")

# ---- FULL POPULATION >=1e11, all three T (verdict on best_T) ----
log("=== FULL POPULATION m200>1e11 (all three T) ===")
out["full_1e11"] = run_pop(1e11, "1e11", [2, 4, 8]); flush()
# ---- robustness >=2e11 at best_T ----
log(f"=== ROBUSTNESS m200>2e11 (best tile T={best_T}) ===")
out["full_2e11"] = run_pop(2e11, "2e11", [int(best_T)]); flush()

# ---- verdict ----
v = out["full_1e11"][str(best_T)]["S_total_analysis"]
def verdict(a):
    if a["z_peak"] is None or not (0.35 <= a["z_peak"] <= 0.85): return "FAIL/ARTIFACT-REASSERTS"
    if a["maha"] <= 1.36: return "PASS/APERTURE-CONFIRMED"
    if a["maha"] >= 1.86: return "FAIL/ARTIFACT-REASSERTS"
    return "AMBIGUOUS"
out["VERDICT"] = {"word": verdict(v), "best_tile": best_T, "estimator": "S_total (primary)",
                  "maha": v["maha"], "z_peak": v["z_peak"], "w0": v["w0"], "wa": v["wa"],
                  "chi2_minus_lcdm": v["chi2_minus_lcdm"],
                  "extensive_variant": verdict(out["full_1e11"][str(best_T)]["S_extensive_analysis"]),
                  "robustness_2e11": verdict(out["full_2e11"][str(best_T)]["S_total_analysis"])}
flush()
log(f"VERDICT: {out['VERDICT']['word']}  maha={v['maha']:.3f} z_peak={v['z_peak']:.3f} "
    f"(w0={v['w0']:.3f} wa={v['wa']:.3f})")
log("=" * 60); log("FULL-POPULATION DONE"); flush()
