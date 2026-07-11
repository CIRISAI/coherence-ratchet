#!/usr/bin/env python3
"""
Adversarial controls C1 and C2 for the retention_v2 SHM-anchor hit.

C1: rerun {11.67,11.89,12.11,12.33} with the cap LOWERED to 20000 -> does the fit-quality
    extremum follow the cap boundary (artifact) or stay at 11.89 (SHM survives)?
C2: at 11.89, subsample each snapshot to 12.33's per-snapshot count (k-profile matched),
    3 seeds -> is the above-side degradation a k artifact or a population effect?

GPU machinery (S_gpu / _cholesky_inplace / make_xi_table) copied VERBATIM from
../large_volume/run_test.py, same as compute_retention.py. Analysis (z_peak, CPL projection,
real DESI likelihood) identical to compute_retention.py. Incremental flush. No synthetic data
(random subsampling of the real TNG300 catalog only).
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
HG = CEP / "halo_grain"
EPOCH = CEP / "epoch_check"
DESIV2 = CEP / "desi_likelihood_v2"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))

import s_of_a as S

# ---- exec-lift CPL projection (identical to compute_retention.py) ----
csrc = (EPOCH / "cpl_projection.py").read_text()
cpl_ns = {"np": np}
exec("import numpy as np\nfrom scipy.integrate import quad\n"
     "from scipy.interpolate import CubicSpline\nfrom scipy.optimize import minimize\n"
     "C_KM = 299792.458\nZ_STAR = 1089.0\n", cpl_ns)
body = csrc.split("# 2. Backgrounds.")[1].split("# 4. Run.")[0]
exec(compile(body, str(EPOCH / "cpl_projection.py"), "exec"), cpl_ns)
make_f_fw = cpl_ns["make_f_fw"]; project_distance = cpl_ns["project_distance"]
crossing_z = cpl_ns["crossing_z"]

sys.path.insert(0, str(DESIV2))
import likelihood_fit as lf

COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
maha = lambda w0, wa: float(np.sqrt(np.array([w0+0.838, wa+0.62]) @ COVINV
                                    @ np.array([w0+0.838, wa+0.62])))
OM_PROJ = 0.3155

# ---- GPU machinery copied verbatim from ../large_volume/run_test.py ----
import cupy as cp

def make_xi_table(ps, R_smooth=1.0, rmin=0.02, rmax=180.0, n=400_000):
    xi = ps.xi_spline(R_smooth); sig2 = ps.sigma2_R(R_smooth)
    r = np.logspace(np.log10(rmin), np.log10(rmax), n)
    return cp.asarray(r), cp.asarray(xi(r) / sig2), float(sig2)

def _cholesky_inplace(C, bs=2048):
    from cupyx.scipy.linalg import solve_triangular
    k = C.shape[0]
    for j in range(0, k, bs):
        je = min(j + bs, k)
        Cjj = C[j:je, j:je]
        if j > 0:
            Lp = C[j:je, :j]; Cjj -= Lp @ Lp.T
        try:
            Ld = cp.linalg.cholesky(Cjj)
        except Exception:
            return False
        if bool(cp.isnan(cp.diagonal(Ld)).any()) or bool((cp.diagonal(Ld) <= 0).any()):
            return False
        C[j:je, j:je] = Ld
        if je < k:
            panel = C[je:, j:je]
            if j > 0:
                panel -= C[je:, :j] @ C[j:je, :j].T
            C[je:, j:je] = solve_triangular(Ld, panel.T, lower=True).T
    return True

def S_gpu(pos, box, xr, xv, jitter=0.0, guards=False, tile=1024):
    from cupyx.scipy.linalg import solve_triangular
    k = len(pos)
    P = cp.asarray(pos, dtype=cp.float64)
    C = cp.empty((k, k), dtype=cp.float64)
    for i0 in range(0, k, tile):
        i1 = min(i0 + tile, k)
        d2 = cp.zeros((i1 - i0, k), dtype=cp.float64)
        for ax in range(3):
            dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax])
            cp.minimum(dx, box - dx, out=dx); dx *= dx; d2 += dx
        cp.sqrt(d2, out=d2)
        cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2)
        C[i0:i1] = cp.interp(d2, xr, xv)
        del d2, dx
    idx = cp.arange(k); C[idx, idx] = 1.0 + jitter
    cp.get_default_memory_pool().free_all_blocks()
    ok = _cholesky_inplace(C)
    if not ok:
        del C; cp.get_default_memory_pool().free_all_blocks(); return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum())
    del C; cp.get_default_memory_pool().free_all_blocks()
    return dict(S=Sval, k=k)

# ---- data + power spectrum (identical setup) ----
SNAPS = [25, 30, 33, 36, 39, 42, 45, 47, 49, 51, 53, 55, 56, 59, 61,
         63, 65, 67, 70, 72, 74, 76, 79, 82, 87, 99]
BOX = 205.0
SEED_BASE = 20260710

snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64),
                         m200=d["m200"].astype(np.float64)))

S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)

THRESHOLDS = np.logspace(11.0, 13.0, 10)   # identical grid; indices 3,4,5,6 used here
LCDM = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)
LCDM_CHI2 = LCDM["chi2"]

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

def s_curve_S(pos_use):
    if len(pos_use) < 3:
        return None
    g = S_gpu(pos_use, BOX, XR, XV)
    if g is None:
        g = S_gpu(pos_use, BOX, XR, XV, jitter=1e-8)
        if g is None:
            raise RuntimeError("Cholesky failed")
    return g

def analyze(records):
    a = np.array([x["a"] for x in records], float)
    Sa = np.array([x["S"] if x["S"] is not None else np.nan for x in records], float)
    ok = np.isfinite(Sa) & (Sa > 0)
    a_ok, S_ok = a[ok], Sa[ok]
    order = np.argsort(a_ok); a_ok, S_ok = a_ok[order], S_ok[order]
    out = {"n_valid": int(len(a_ok))}
    if len(a_ok) < 4:
        out["z_peak_globalmax"] = None
        return out
    imax = int(np.argmax(S_ok)); a_peak = float(a_ok[imax])
    out["z_peak_globalmax"] = float(1.0/a_peak - 1.0)
    out["S_max"] = float(S_ok[imax])
    out["peak_at_endpoint"] = bool(imax == 0 or imax == len(a_ok)-1)
    f = make_f_fw(a_ok, S_ok)
    w0, wa, c2proj = project_distance(f, Om=OM_PROJ, use_cmb=True)
    out["cpl"] = dict(w0=float(w0), wa=float(wa), cross_z=crossing_z(w0, wa),
                      maha=maha(w0, wa), proj_chi2=float(c2proj))
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    out["likelihood"] = dict(chi2=float(prof["chi2"]), Om=float(prof["Om"]),
                             chi2_minus_lcdm=float(prof["chi2"] - LCDM_CHI2))
    return out

RES = HERE / "challenge_results.json"
out = {"date": "2026-07-10", "purpose": "adversarial controls C1,C2 for retention_v2 hit",
       "lcdm_chi2": LCDM_CHI2, "box": "TNG300-1 205 Mpc/h",
       "reference_from_main_run": {
           "11.89": {"cap": 38000, "maha": 1.1561782774507192, "chi2_minus_lcdm": -1.4454477136793766,
                     "z_peak": 0.5463921831410221},
           "12.33": {"cap": 38000, "maha": 2.104667532028569, "chi2_minus_lcdm": 4.027376458361385,
                     "z_peak": 0.2733533465784399}},
       "C1_cap20000": [], "C2_kmatched_11p89": []}
def flush():
    with open(RES, "w") as fh:
        json.dump(out, fh, indent=1)
flush()
log(f"LCDM baseline chi2 = {LCDM_CHI2:.4f}")

# =====================================================================
# C1: cap lowered to 20000, thresholds {11.67,11.89,12.11,12.33} (indices 3,4,5,6)
# =====================================================================
CAP_C1 = 20000
for ti in [3, 4, 5, 6]:
    thr = THRESHOLDS[ti]
    rec = {"log10_thr": float(np.log10(thr)), "thr_Msunh": float(thr), "cap": CAP_C1,
           "records": []}
    n_capped = 0
    for sd in snapdata:
        sel = sd["m200"] > thr
        pos = sd["pos"][sel]; n_above = int(len(pos))
        capped = n_above > CAP_C1
        if capped:
            n_capped += 1
            seed = SEED_BASE + 1000*ti + sd["snap"]      # DECISIONS seed formula
            rs = np.random.RandomState(seed)
            pos_use = pos[rs.choice(n_above, CAP_C1, replace=False)]
        else:
            pos_use = pos
        r = {"a": sd["a"], "z": sd["z"], "n_above": n_above, "capped": bool(capped)}
        g = s_curve_S(pos_use)
        r["S"] = None if g is None else g["S"]
        r["k"] = int(len(pos_use)) if g is None else g["k"]
        rec["records"].append(r); flush()
    rec["n_capped_snaps"] = n_capped
    rec["cap_limited"] = bool(n_capped > 0)
    rec.update(analyze(rec["records"]))
    out["C1_cap20000"].append(rec); flush()
    log(f"C1 thr={np.log10(thr):.2f} cap=20000 n_capped={n_capped}/26 "
        f"z_peak={rec.get('z_peak_globalmax')} maha={rec.get('cpl',{}).get('maha')} "
        f"chi2dL={rec.get('likelihood',{}).get('chi2_minus_lcdm')}")

# =====================================================================
# C2: 11.89 subsampled to 12.33's per-snapshot count, 3 seeds
# =====================================================================
thr_1189 = THRESHOLDS[4]
thr_1233 = THRESHOLDS[6]
k_target = []
for sd in snapdata:
    k_target.append(int((sd["m200"] > thr_1233).sum()))
out["C2_k_target_profile"] = k_target; flush()

for rep in range(3):
    rec = {"rep": rep, "log10_thr": float(np.log10(thr_1189)),
           "k_matched_to": "12.33 per-snap counts", "records": []}
    for i, sd in enumerate(snapdata):
        sel = sd["m200"] > thr_1189
        pos = sd["pos"][sel]; n_above = int(len(pos))
        kt = k_target[i]
        seed = SEED_BASE + 100000*rep + sd["snap"]
        rs = np.random.RandomState(seed)
        if n_above > kt:
            pos_use = pos[rs.choice(n_above, kt, replace=False)]
        else:
            pos_use = pos
        r = {"a": sd["a"], "z": sd["z"], "n_above": n_above, "k_target": kt}
        g = s_curve_S(pos_use)
        r["S"] = None if g is None else g["S"]
        r["k"] = int(len(pos_use)) if g is None else g["k"]
        rec["records"].append(r); flush()
    rec.update(analyze(rec["records"]))
    out["C2_kmatched_11p89"].append(rec); flush()
    log(f"C2 rep={rep} kmatched-11.89 z_peak={rec.get('z_peak_globalmax')} "
        f"maha={rec.get('cpl',{}).get('maha')} "
        f"chi2dL={rec.get('likelihood',{}).get('chi2_minus_lcdm')}")

log("=" * 60); log("C1+C2 DONE"); flush()
