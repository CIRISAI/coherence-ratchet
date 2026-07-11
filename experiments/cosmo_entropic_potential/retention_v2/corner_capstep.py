#!/usr/bin/env python3
"""
Corner cap-step robustness test on the standing headline.

At the frozen corner threshold 7.4253e11 Msun/h, on the large_volume 10-snapshot grid,
rerun the full S(a) -> w(z) -> DESI-fit chain at cap = {38000 (reproduction anchor),
30000, 20000}, plus two fences:
  - P4 fence: ceiling k=20000 at all snaps, 2 seeds (== cap=20000 seed-repeats for the corner)
  - stronger intensive fence: CONSTANT k=8000 at all snaps, 2 seeds (isolates structure from count)

Only cap-dependence is tested; threshold, grid, and analysis are held fixed. GPU machinery and
analysis copied from challenge_compute.py (which copied it verbatim from ../large_volume/run_test.py).
Incremental flush. No synthetic data (random subsampling of the real TNG300 catalog only).
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

csrc = (EPOCH / "cpl_projection.py").read_text()
cpl_ns = {"np": np}
exec("import numpy as np\nfrom scipy.integrate import quad\n"
     "from scipy.interpolate import CubicSpline\nfrom scipy.optimize import minimize\n"
     "C_KM = 299792.458\nZ_STAR = 1089.0\n", cpl_ns)
body = csrc.split("# 2. Backgrounds.")[1].split("# 4. Run.")[0]
exec(compile(body, str(EPOCH / "cpl_projection.py"), "exec"), cpl_ns)
make_f_fw = cpl_ns["make_f_fw"]; project_distance = cpl_ns["project_distance"]
crossing_z = cpl_ns["crossing_z"]
sys.path.insert(0, str(DESIV2)); import likelihood_fit as lf

COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
maha = lambda w0, wa: float(np.sqrt(np.array([w0+0.838, wa+0.62]) @ COVINV
                                    @ np.array([w0+0.838, wa+0.62])))
OM_PROJ = 0.3155

import cupy as cp
def make_xi_table(ps, R_smooth=1.0, rmin=0.02, rmax=180.0, n=400_000):
    xi = ps.xi_spline(R_smooth); sig2 = ps.sigma2_R(R_smooth)
    r = np.logspace(np.log10(rmin), np.log10(rmax), n)
    return cp.asarray(r), cp.asarray(xi(r) / sig2), float(sig2)

def _cholesky_inplace(C, bs=2048):
    from cupyx.scipy.linalg import solve_triangular
    k = C.shape[0]
    for j in range(0, k, bs):
        je = min(j + bs, k); Cjj = C[j:je, j:je]
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

def S_gpu(pos, box, xr, xv, jitter=0.0, tile=1024):
    k = len(pos)
    P = cp.asarray(pos, dtype=cp.float64)
    C = cp.empty((k, k), dtype=cp.float64)
    for i0 in range(0, k, tile):
        i1 = min(i0 + tile, k)
        d2 = cp.zeros((i1 - i0, k), dtype=cp.float64)
        for ax in range(3):
            dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax])
            cp.minimum(dx, box - dx, out=dx); dx *= dx; d2 += dx
        cp.sqrt(d2, out=d2); cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2)
        C[i0:i1] = cp.interp(d2, xr, xv); del d2, dx
    idx = cp.arange(k); C[idx, idx] = 1.0 + jitter
    cp.get_default_memory_pool().free_all_blocks()
    if not _cholesky_inplace(C):
        del C; cp.get_default_memory_pool().free_all_blocks(); return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum())
    del C; cp.get_default_memory_pool().free_all_blocks()
    return dict(S=Sval, k=k)

# large_volume 10-snapshot grid + frozen corner
SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
SEED_BASE = 20260710
THR_CORNER = 742530285568.0   # 10^11.871 Msun/h, frozen large_volume corner

snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64), m200=d["m200"].astype(np.float64)))

S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)
LCDM = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True); LCDM_CHI2 = LCDM["chi2"]

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

def s_of(pos_use):
    if len(pos_use) < 3: return None
    g = S_gpu(pos_use, BOX, XR, XV)
    if g is None:
        g = S_gpu(pos_use, BOX, XR, XV, jitter=1e-8)
        if g is None: raise RuntimeError("Cholesky failed")
    return g

def analyze(records):
    a = np.array([x["a"] for x in records], float)
    Sa = np.array([x["S"] if x["S"] is not None else np.nan for x in records], float)
    ok = np.isfinite(Sa) & (Sa > 0)
    a_ok, S_ok = a[ok], Sa[ok]; order = np.argsort(a_ok); a_ok, S_ok = a_ok[order], S_ok[order]
    out = {"n_valid": int(len(a_ok))}
    if len(a_ok) < 4:
        out["z_peak_globalmax"] = None; return out
    imax = int(np.argmax(S_ok)); a_peak = float(a_ok[imax])
    out["z_peak_globalmax"] = float(1.0/a_peak - 1.0); out["S_max"] = float(S_ok[imax])
    out["peak_at_endpoint"] = bool(imax == 0 or imax == len(a_ok)-1)
    w0, wa, c2proj = project_distance(make_f_fw(a_ok, S_ok), Om=OM_PROJ, use_cmb=True)
    out["cpl"] = dict(w0=float(w0), wa=float(wa), cross_z=crossing_z(w0, wa),
                      maha=maha(w0, wa), proj_chi2=float(c2proj))
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    out["likelihood"] = dict(chi2=float(prof["chi2"]), Om=float(prof["Om"]),
                             chi2_minus_lcdm=float(prof["chi2"] - LCDM_CHI2))
    return out

def run(cap=None, const_k=None, seed_tag=0):
    """cap: subsample-ceiling (n_above > cap -> pick cap). const_k: fixed size at every snap."""
    recs = []
    for sd in snapdata:
        pos = sd["pos"][sd["m200"] > THR_CORNER]; n_above = int(len(pos))
        target = const_k if const_k is not None else cap
        if target is not None and n_above > target:
            seed = SEED_BASE + seed_tag + sd["snap"]
            pos_use = pos[np.random.RandomState(seed).choice(n_above, target, replace=False)]
            sub = True
        else:
            pos_use = pos; sub = False
        g = s_of(pos_use)
        recs.append({"a": sd["a"], "z": sd["z"], "n_above": n_above,
                     "k": int(len(pos_use)), "subsampled": bool(sub),
                     "S": None if g is None else g["S"]})
        flush()
    r = {"records": recs}; r.update(analyze(recs)); return r

RES = HERE / "challenge_results.json"
out = json.load(open(RES)) if RES.exists() else {}
out["corner_capstep"] = {
    "date": "2026-07-10", "grid": "large_volume 10-snap", "snaps": SNAPS,
    "thr_corner_Msunh": THR_CORNER, "log10_thr": float(np.log10(THR_CORNER)),
    "lcdm_chi2": LCDM_CHI2,
    "baseline_38k_existing": {"maha": 1.3626340790730724, "w0": -0.7666191523146305,
        "wa": -0.7423928100872467, "interior_peak_z": 0.5896633869209742,
        "w_today": -0.8332054965762254, "source": "large_volume/results.json stage5.primary"},
    "cap_runs": {}, "fence_k20000": [], "fence_const_k8000": []}
def flush():
    with open(RES, "w") as fh: json.dump(out, fh, indent=1)
flush()
log(f"LCDM chi2={LCDM_CHI2:.4f}; corner={THR_CORNER:.4e} (10^{np.log10(THR_CORNER):.3f})")

# ---- cap-step: 38000 (anchor), 30000, 20000 ----
for ci, cap in enumerate([38000, 30000, 20000]):
    r = run(cap=cap, seed_tag=1000*ci)
    r["cap"] = cap
    r["n_subsampled"] = int(sum(x["subsampled"] for x in r["records"]))
    out["corner_capstep"]["cap_runs"][str(cap)] = r; flush()
    log(f"CAP {cap}: z_peak={r.get('z_peak_globalmax'):.3f} "
        f"maha={r.get('cpl',{}).get('maha'):.3f} "
        f"chi2dL={r.get('likelihood',{}).get('chi2_minus_lcdm'):+.3f} "
        f"nsub={r['n_subsampled']}/10 endpt={r.get('peak_at_endpoint')}")

# ---- P4 fence: ceiling k=20000, 2 seeds ----
for rep in range(2):
    r = run(cap=20000, seed_tag=500000 + 100000*rep)
    r["rep"] = rep; r["ceiling"] = 20000
    out["corner_capstep"]["fence_k20000"].append(r); flush()
    log(f"FENCE k<=20000 rep{rep}: z_peak={r.get('z_peak_globalmax'):.3f} "
        f"maha={r.get('cpl',{}).get('maha'):.3f} "
        f"chi2dL={r.get('likelihood',{}).get('chi2_minus_lcdm'):+.3f}")

# ---- stronger intensive fence: constant k=8000, 2 seeds ----
for rep in range(2):
    r = run(const_k=8000, seed_tag=800000 + 100000*rep)
    r["rep"] = rep; r["const_k"] = 8000
    out["corner_capstep"]["fence_const_k8000"].append(r); flush()
    log(f"FENCE const-k=8000 rep{rep}: z_peak={r.get('z_peak_globalmax'):.3f} "
        f"maha={r.get('cpl',{}).get('maha'):.3f} "
        f"chi2dL={r.get('likelihood',{}).get('chi2_minus_lcdm'):+.3f}")

log("=" * 60); log("CORNER CAP-STEP DONE"); flush()
