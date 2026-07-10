#!/usr/bin/env python3
"""
Large-volume test of the frozen B-total pipeline on TNG300-1 (205 Mpc/h).
Executes the order-of-operations in DECISIONS.md (written before any S/w here):
  0. k(a) tables -> corner-threshold selection (counts only, no S)
  1. GPU-estimator validation gate on CAMELS CV_0 (|dS/S| < 1e-6 or abort)
  2. primary S(a) + guards + octant jackknife (GPU Cholesky log-det)
  3. threshold ladder (5e12, 1e13)
  4. CAMELS-continuity tiled variant (1e11, 512 tiles, original CPU op_B)
  5. frozen analysis: w(a), w_today, interior peak (K3), crossing epoch + 68%
     (P1), CPL projections + Mahalanobis (identical machinery), P3/K7 verdicts
Incremental writes to results.json after every stage.
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
CEP = HERE.parent
HG = CEP / "halo_grain"
EPOCH = CEP / "epoch_check"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))

import halo_grain as hg          # patches s_of_a to CAMELS values (used for the gate)
import s_of_a as S

# lift the published CPL-projection functions verbatim (defs only)
src = (EPOCH / "cpl_projection.py").read_text()
cpl = {}
exec(compile(src.split("# 4. Run.")[0], str(EPOCH / "cpl_projection.py"), "exec"), cpl)
make_f_fw = cpl["make_f_fw"]; project_distance = cpl["project_distance"]
project_rho = cpl["project_rho"]; crossing_z = cpl["crossing_z"]
phys_crossing_z = cpl["phys_crossing_z"]; E_of = cpl["E_of"]

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
CAP = 38000
LADDER = [5e12, 1e13]
OM_PROJ = 0.3155
COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
maha = lambda w0, wa: float(np.sqrt(np.array([w0+0.838, wa+0.62]) @ COVINV
                                    @ np.array([w0+0.838, wa+0.62])))

RES = HERE / "results.json"
out = {"date": "2026-07-10", "box": "TNG300-1 205 Mpc/h", "cap": CAP,
       "decisions": "DECISIONS.md (pre-committed)"}
def flush():
    with open(RES, "w") as fh:
        json.dump(out, fh, indent=1)

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

# ---------------------------------------------------------------------------
# Stage 0: load, k(a) tables, corner threshold (counts only)
# ---------------------------------------------------------------------------
snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64),
                         m200=d["m200"].astype(np.float64)))
A_GRID = np.array([sd["a"] for sd in snapdata])

# corner threshold: max over snapshots of the (CAP+1)-th largest mass
thr_corner = max(np.sort(sd["m200"])[-(CAP + 1)] if len(sd["m200"]) > CAP else 0.0
                 for sd in snapdata)
k_corner = [int((sd["m200"] > thr_corner).sum()) for sd in snapdata]
k_z3 = k_corner[0]
out["stage0"] = {
    "k_tables": {f"{t:.0e}": [int((sd['m200'] > t).sum()) for sd in snapdata]
                 for t in (1e11, 2e11, 5e11, 1e12, 2e12, 5e12, 1e13)},
    "thr_corner_Msun_h": float(thr_corner), "k_at_corner": k_corner,
    "k_z3_at_corner": k_z3, "rule_z3_ok": bool(k_z3 >= 200)}
flush()
log(f"corner threshold = {thr_corner:.3e} Msun/h; k(a) = {k_corner}; "
    f"k(z=3) = {k_z3} (rule >=200: {k_z3 >= 200})")
assert k_z3 >= 200, "corner threshold violates the z=3 rule — stop"

# ---------------------------------------------------------------------------
# GPU S: same number as op_B's -sum(log eig(C)), via Cholesky log-det
# ---------------------------------------------------------------------------
import cupy as cp

def make_xi_table(ps, R_smooth=1.0, rmin=0.02, rmax=180.0, n=400_000):
    xi = ps.xi_spline(R_smooth)
    sig2 = ps.sigma2_R(R_smooth)
    r = np.logspace(np.log10(rmin), np.log10(rmax), n)
    return cp.asarray(r), cp.asarray(xi(r) / sig2), float(sig2)

def _cholesky_inplace(C, bs=2048):
    """Left-looking blocked Cholesky, in place (lower triangle). Peak mem ~n^2
    + one panel, vs 2n^2 for cp.linalg.cholesky's copy. Returns False if a
    diagonal block is not PD."""
    from cupyx.scipy.linalg import solve_triangular
    k = C.shape[0]
    for j in range(0, k, bs):
        je = min(j + bs, k)
        Cjj = C[j:je, j:je]
        if j > 0:
            Lp = C[j:je, :j]
            Cjj -= Lp @ Lp.T
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

def S_gpu(pos, box, xr, xv, jitter=0.0, guards=True, tile=1024):
    # tile=1024 keeps C-build temporaries ~1GB: 16GB card, C alone is 11.6GB at k=38000
    from cupyx.scipy.linalg import solve_triangular
    k = len(pos)
    P = cp.asarray(pos, dtype=cp.float64)
    C = cp.empty((k, k), dtype=cp.float64)
    for i0 in range(0, k, tile):
        i1 = min(i0 + tile, k)
        d2 = cp.zeros((i1 - i0, k), dtype=cp.float64)
        for ax in range(3):
            dx = cp.abs(P[i0:i1, ax][:, None] - P[None, :, ax])
            cp.minimum(dx, box - dx, out=dx)
            dx *= dx
            d2 += dx
        cp.sqrt(d2, out=d2)
        cp.clip(d2, float(xr[0]), float(xr[-1]), out=d2)
        C[i0:i1] = cp.interp(d2, xr, xv)
        del d2, dx
    idx = cp.arange(k)
    C[idx, idx] = 1.0 + jitter
    cp.get_default_memory_pool().free_all_blocks()
    lam_max = None
    if guards:                                   # lam_max BEFORE C is destroyed
        x = cp.random.RandomState(0).rand(k)
        for _ in range(50):
            x = C @ x; x /= cp.linalg.norm(x)
        lam_max = float(x @ (C @ x))
        del x
    ok = _cholesky_inplace(C)                    # C's lower triangle becomes L
    if not ok:
        del C
        cp.get_default_memory_pool().free_all_blocks()
        return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum())
    lam_min = None
    if guards:                                   # inverse iteration, solves only
        # C is C-order; C.T is an F-order VIEW (no 9.6GB copy inside
        # solve_triangular). L z = b == solve(C.T, b, lower=False, trans='T');
        # L^T z = b == solve(C.T, b, lower=False, trans='N').
        Lv = C.T
        y = cp.random.RandomState(1).rand(k)
        y /= cp.linalg.norm(y)
        for _ in range(50):
            z = solve_triangular(Lv, y, lower=False, trans="T")
            z = solve_triangular(Lv, z, lower=False, trans="N")
            y = z / cp.linalg.norm(z)
        # converged unit y: lam_min = 1 / (y . C^-1 y)
        z = solve_triangular(Lv, y, lower=False, trans="T")
        z = solve_triangular(Lv, z, lower=False, trans="N")
        lam_min = float(1.0 / (y @ z))
        del y, z
    del C
    cp.get_default_memory_pool().free_all_blocks()
    return dict(S=Sval, k=k, lam_min=lam_min, lam_max=lam_max)

# ---------------------------------------------------------------------------
# Stage 1: validation gate on CAMELS CV_0 (CPU op_B vs GPU path)
# ---------------------------------------------------------------------------
ps_cam = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
cam = hg.load_snapshot(90, cv=0)          # z=0, k=364 at 1e11
cpu_rec = hg.op_B(ps_cam, [cam], 1e11)[0]
xr_c, xv_c, _ = make_xi_table(ps_cam)
gpu_rec = S_gpu(cam["pos"][cam["m200"] > 1e11], 25.0, xr_c, xv_c)
rel = abs(gpu_rec["S"] - cpu_rec["S"]) / abs(cpu_rec["S"])
out["stage1_gate"] = {"S_cpu": cpu_rec["S"], "S_gpu": gpu_rec["S"],
                      "rel_diff": rel, "pass": bool(rel < 1e-6),
                      "lam_min_gpu": gpu_rec["lam_min"],
                      "lam_min_cpu": cpu_rec["min_eig"]}
flush()
log(f"GATE: S_cpu={cpu_rec['S']:.10f} S_gpu={gpu_rec['S']:.10f} rel={rel:.2e} "
    f"pass={rel < 1e-6}")
assert rel < 1e-6, "validation gate FAILED — abort before any TNG number"

# ---------------------------------------------------------------------------
# TNG cosmology power spectrum (patch AFTER the gate)
# ---------------------------------------------------------------------------
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)
hg.BOX = BOX                                    # for the tiled CPU variant

# ---------------------------------------------------------------------------
# Stage 2: primary S(a) + octant jackknife
# ---------------------------------------------------------------------------
out["stage2_primary"] = {"thr": float(thr_corner), "records": [],
                         "jackknife": {}}
for sd in snapdata:
    sel = sd["m200"] > thr_corner
    pos = sd["pos"][sel]
    r = S_gpu(pos, BOX, XR, XV)
    if r is None:                                # PD failure -> jitter (=op_B clip)
        r = S_gpu(pos, BOX, XR, XV, jitter=1e-8)
        if r is None:
            raise RuntimeError(f"Cholesky failed even with jitter at a={sd['a']:.3f} "
                               f"k={len(pos)} — investigate before proceeding")
        r["jitter"] = 1e-8
    r.update(a=sd["a"], z=sd["z"])
    out["stage2_primary"]["records"].append(r)
    flush()
    log(f"primary a={sd['a']:.3f}: k={r['k']} S={r['S']:.2f} "
        f"lam_min={r['lam_min']:.4g} cond={r['lam_max']/r['lam_min']:.3g}")

oct_of = lambda p: ((p[:, 0] > BOX/2).astype(int) + 2*(p[:, 1] > BOX/2)
                    + 4*(p[:, 2] > BOX/2))
for o in range(8):
    Sjk = []
    for sd in snapdata:
        sel = sd["m200"] > thr_corner
        pos = sd["pos"][sel]
        keep = oct_of(pos) != o
        r = S_gpu(pos[keep], BOX, XR, XV, guards=False)
        if r is None:
            r = S_gpu(pos[keep], BOX, XR, XV, jitter=1e-8, guards=False)
        Sjk.append(r["S"])
    out["stage2_primary"]["jackknife"][str(o)] = Sjk
    flush()
    log(f"jackknife octant {o}: S(a=1)={Sjk[-1]:.2f}")

# ---------------------------------------------------------------------------
# Stage 3: ladder
# ---------------------------------------------------------------------------
out["stage3_ladder"] = {}
for thr in LADDER:
    recs = []
    for sd in snapdata:
        pos = sd["pos"][sd["m200"] > thr]
        if len(pos) < 3:
            recs.append(dict(a=sd["a"], k=len(pos), S=None)); continue
        r = S_gpu(pos, BOX, XR, XV, guards=False)
        r.update(a=sd["a"])
        recs.append(r)
    out["stage3_ladder"][f"{thr:.0e}"] = recs
    flush()
    log(f"ladder {thr:.0e}: k = {[r['k'] for r in recs]}")

# ---------------------------------------------------------------------------
# Stage 4: CAMELS-continuity tiles (1e11, 8^3 tiles, original CPU op_B)
# ---------------------------------------------------------------------------
NT = 8; TS = BOX / NT
tile_S = np.zeros(len(snapdata)); tile_k = np.zeros(len(snapdata), int)
for i, sd in enumerate(snapdata):
    sel = sd["m200"] > 1e11
    pos = sd["pos"][sel]; m = sd["m200"][sel]
    ti = (np.minimum((pos[:, 0]/TS).astype(int), NT-1) +
          NT*np.minimum((pos[:, 1]/TS).astype(int), NT-1) +
          NT*NT*np.minimum((pos[:, 2]/TS).astype(int), NT-1))
    tot = 0.0; ktot = 0
    for t in range(NT**3):
        pt = pos[ti == t]
        if len(pt) < 3: continue
        rec = hg.op_B(ps_tng, [dict(a=sd["a"], z=sd["z"], pos=pt, m200=np.full(len(pt), 1e12))],
                      1e11)[0]
        if np.isfinite(rec["S"]):
            tot += rec["S"]; ktot += rec["k"]
    tile_S[i] = tot; tile_k[i] = ktot
    log(f"tiles a={sd['a']:.3f}: k_total={ktot} S_total={tot:.1f}")
    out["stage4_tiles"] = {"a": A_GRID.tolist(), "S": tile_S.tolist(),
                           "k": tile_k.tolist()}
    flush()

# ---------------------------------------------------------------------------
# Stage 5: frozen analysis + verdicts
# ---------------------------------------------------------------------------
def analyze(a, Sa, label, project=True):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float)
    ok = np.isfinite(Sa) & (Sa > 0)
    a, Sa = a[ok], Sa[ok]
    d = S.dln_dlna(a, Sa)
    w = -1.0 - d / 3.0
    ols = np.polyfit(np.log(a), np.log(Sa), 1)[0]
    res = {"label": label, "w_today": float(w[-1]),
           "dlnS_dlna_today": float(d[-1]), "ols_global_slope": float(ols),
           "interior_peak_z": phys_crossing_z(a, Sa),
           "S_first_last": [float(Sa[0]), float(Sa[-1])]}
    if project:
        f = make_f_fw(a, Sa)
        w0, wa, _ = project_distance(f, Om=OM_PROJ, use_cmb=True)
        res["dist_BAO+CMB"] = dict(w0=w0, wa=wa, cross_z=crossing_z(w0, wa),
                                   maha=maha(w0, wa))
        w0, wa, _ = project_rho(f, Om=OM_PROJ)
        res["rho_DEweighted"] = dict(w0=w0, wa=wa, cross_z=crossing_z(w0, wa),
                                     maha=maha(w0, wa))
    return res

prim = out["stage2_primary"]["records"]
a_p = [r["a"] for r in prim]; S_p = [r["S"] for r in prim]
out["stage5"] = {"primary": analyze(a_p, S_p, f"B-total corner {thr_corner:.2e}")}
flush()

# jackknife on crossing epoch and w_today
jk_cross, jk_w = [], []
for o in range(8):
    Sj = out["stage2_primary"]["jackknife"][str(o)]
    zj = phys_crossing_z(np.array(a_p), np.array(Sj))
    jk_cross.append(zj if zj is not None else np.nan)
    dj = S.dln_dlna(np.array(a_p), np.array(Sj))
    jk_w.append(-1.0 - dj[-1] / 3.0)
jk_cross = np.array(jk_cross, float); jk_w = np.array(jk_w)
n_ok = np.isfinite(jk_cross).sum()
jkf = lambda v: float(np.sqrt((len(v)-1)/len(v) * ((v - v.mean())**2).sum()))
out["stage5"]["jackknife"] = {
    "crossing_z_values": jk_cross.tolist(),
    "crossing_z_err68": jkf(jk_cross[np.isfinite(jk_cross)]) if n_ok == 8 else None,
    "n_replicates_with_peak": int(n_ok),
    "w_today_values": jk_w.tolist(), "w_today_err68": jkf(jk_w)}
for thr in LADDER:
    recs = out["stage3_ladder"][f"{thr:.0e}"]
    aa = [r["a"] for r in recs if r["S"] is not None]
    ss = [r["S"] for r in recs if r["S"] is not None]
    out["stage5"][f"ladder_{thr:.0e}"] = analyze(aa, ss, f"ladder {thr:.0e}",
                                                 project=False)
out["stage5"]["tiles_1e11"] = analyze(A_GRID, tile_S, "tiled 1e11 x512")
# mechanism check: epoch of k(a) peak vs S peak (primary)
kk = np.array(k_corner, float)
out["stage5"]["mechanism"] = {
    "k_of_a_primary": k_corner,
    "k_peak_interior": bool(np.argmax(kk) < len(kk) - 1),
    "k_peak_z": float(1/A_GRID[np.argmax(kk)] - 1)}
flush()

p = out["stage5"]["primary"]; j = out["stage5"]["jackknife"]
log("=" * 70)
log(f"PRIMARY thr={thr_corner:.2e}: w_today={p['w_today']:+.3f}±{j['w_today_err68']:.3f}"
    f"  interior_peak_z={p['interior_peak_z']}  (replicates with peak: "
    f"{j['n_replicates_with_peak']}/8)")
log(f"  dist CPL: {p['dist_BAO+CMB']}")
log(f"  K3 (no interior peak -> extensive branch dead): "
    f"{'FIRES' if p['interior_peak_z'] is None else 'does not fire'}")
log(f"  P3/K7: w_today in [-1.22,-0.84]: "
    f"{-1.22 <= p['w_today'] <= -0.84}")
log(f"  tiles 1e11: w_today={out['stage5']['tiles_1e11']['w_today']:+.3f} "
    f"peak_z={out['stage5']['tiles_1e11']['interior_peak_z']}")
log("wrote results.json")
