#!/usr/bin/env python3
"""
Defense check for the corner cap-step KILL: the corner RULE is itself cap-dependent
(thr_corner(cap) = max over snaps of the (cap+1)-th largest mass). corner_capstep.py held the
threshold fixed at corner(38000) and lowered the cap -> KILLED. This asks the fair follow-up:
if the RULE re-selects the threshold at each lower cap (so the cap again sits at the raw
count's max), is the RULE's output cap-stable (interior peak + ~1.36sigma recovered)?

Same 10-snap grid, machinery, analysis as corner_capstep.py. Writes under
corner_capstep.rule_reselect in challenge_results.json.
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
maha = lambda w0, wa: float(np.sqrt(np.array([w0+0.838, wa+0.62]) @ COVINV @ np.array([w0+0.838, wa+0.62])))
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
    k = len(pos); P = cp.asarray(pos, dtype=cp.float64); C = cp.empty((k, k), dtype=cp.float64)
    for i0 in range(0, k, tile):
        i1 = min(i0+tile, k); d2 = cp.zeros((i1-i0, k), dtype=cp.float64)
        for ax in range(3):
            dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax]); cp.minimum(dx, box-dx, out=dx); dx *= dx; d2 += dx
        cp.sqrt(d2, out=d2); cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2); C[i0:i1] = cp.interp(d2, xr, xv); del d2, dx
    idx = cp.arange(k); C[idx, idx] = 1.0 + jitter; cp.get_default_memory_pool().free_all_blocks()
    if not _chol(C): del C; cp.get_default_memory_pool().free_all_blocks(); return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum()); del C; cp.get_default_memory_pool().free_all_blocks()
    return dict(S=Sval, k=k)

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]; BOX = 205.0; SEED_BASE = 20260710
snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64), m200=d["m200"].astype(np.float64)))
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng); LCDM_CHI2 = lf.profile_fixedshape(lf.f_lcdm, use_cmb=True)["chi2"]
T0 = time.time(); log = lambda m: print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

def corner_thr(cap):
    return float(max(np.sort(sd["m200"])[-(cap+1)] if len(sd["m200"]) > cap else 0.0 for sd in snapdata))
def s_of(pos):
    if len(pos) < 3: return None
    g = S_gpu(pos, BOX, XR, XV)
    if g is None:
        g = S_gpu(pos, BOX, XR, XV, jitter=1e-8)
        if g is None: raise RuntimeError("chol fail")
    return g
def analyze(records):
    a = np.array([x["a"] for x in records], float); Sa = np.array([x["S"] for x in records], float)
    ok = np.isfinite(Sa) & (Sa > 0); a_ok, S_ok = a[ok], Sa[ok]; o = np.argsort(a_ok); a_ok, S_ok = a_ok[o], S_ok[o]
    imax = int(np.argmax(S_ok))
    w0, wa, c2 = project_distance(make_f_fw(a_ok, S_ok), Om=OM_PROJ, use_cmb=True)
    prof = lf.profile_fixedshape(lf.make_f_fw(a_ok, S_ok), use_cmb=True)
    return dict(z_peak_globalmax=float(1/a_ok[imax]-1), peak_at_endpoint=bool(imax in (0, len(a_ok)-1)),
                cpl=dict(w0=float(w0), wa=float(wa), cross_z=crossing_z(w0, wa), maha=maha(w0, wa)),
                likelihood=dict(chi2=float(prof["chi2"]), chi2_minus_lcdm=float(prof["chi2"]-LCDM_CHI2)))

RES = HERE / "challenge_results.json"; out = json.load(open(RES))
out["corner_capstep"]["rule_reselect"] = {}
def flush():
    with open(RES, "w") as fh: json.dump(out, fh, indent=1)

for cap in [38000, 30000, 20000]:
    thr = corner_thr(cap)
    recs = []
    for sd in snapdata:
        pos = sd["pos"][sd["m200"] > thr]; n = int(len(pos))
        if n > cap:
            pos = pos[np.random.RandomState(SEED_BASE + cap + sd["snap"]).choice(n, cap, replace=False)]
        g = s_of(pos); recs.append({"z": sd["z"], "a": sd["a"], "n_above": n, "k": int(len(pos)), "S": g["S"]})
        flush()
    r = {"cap": cap, "thr_corner_Msunh": thr, "log10_thr": float(np.log10(thr)),
         "k_of_a": [x["k"] for x in recs], "n_above_of_a": [x["n_above"] for x in recs], "records": recs}
    r.update(analyze(recs)); out["corner_capstep"]["rule_reselect"][str(cap)] = r; flush()
    log(f"RULE cap={cap}: thr=10^{np.log10(thr):.3f} z_peak={r['z_peak_globalmax']:.3f} "
        f"maha={r['cpl']['maha']:.3f} chi2dL={r['likelihood']['chi2_minus_lcdm']:+.3f} "
        f"w0={r['cpl']['w0']:+.3f} wa={r['cpl']['wa']:+.3f} endpt={r['peak_at_endpoint']} "
        f"n_above(a)={r['n_above_of_a']}")
log("RULE-RESELECT DONE"); flush()
