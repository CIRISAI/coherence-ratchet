#!/usr/bin/env python3
"""
fine_grid: frozen B-total S(a) on the 26-snapshot dense grid at the FROZEN
threshold 7.425e11 Msun/h (NOT reselected), plus the 8-octant jackknife.

Estimator (S_gpu / _cholesky_inplace / make_xi_table) copied VERBATIM from
../run_test.py (run_test.py is NOT imported — it executes on import). CPL
projection defs lifted from ../epoch_check/cpl_projection.py (split at "# 4.
Run."). TNG cosmology patched into s_of_a after the CAMELS validation gate.

Resumable: every S eval is flushed to results.json immediately; on restart,
already-computed (curve, snap) pairs are skipped. Run under flock on the shared
GPU:  flock /tmp/claude-1000/gpu.lockfile -c "python3 compute_fine.py"
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
LV = HERE.parent
DATA = LV / "data"
CEP = LV.parent
HG = CEP / "halo_grain"
EPOCH = CEP / "epoch_check"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))

import halo_grain as hg          # patches s_of_a to CAMELS values (for the gate)
import s_of_a as S

# lift the published CPL-projection functions verbatim (defs only)
src = (EPOCH / "cpl_projection.py").read_text()
cpl = {}
exec(compile(src.split("# 4. Run.")[0], str(EPOCH / "cpl_projection.py"), "exec"), cpl)
make_f_fw = cpl["make_f_fw"]; project_distance = cpl["project_distance"]
project_rho = cpl["project_rho"]; crossing_z = cpl["crossing_z"]
phys_crossing_z = cpl["phys_crossing_z"]

# --- frozen grid & spec -----------------------------------------------------
ORIG = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
NEW  = [33, 39, 45, 47, 51, 53, 55, 59, 61, 63, 67, 70, 72, 74, 79, 82]
SNAPS = sorted(ORIG + NEW)
THR = 742530285568.0          # FROZEN corner threshold (NOT reselected)
BOX = 205.0
OM_PROJ = 0.3155
COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
maha = lambda w0, wa: float(np.sqrt(np.array([w0+0.838, wa+0.62]) @ COVINV
                                    @ np.array([w0+0.838, wa+0.62])))

RES = HERE / "results.json"
if RES.exists():
    out = json.load(open(RES))
else:
    out = {"date": "2026-07-10", "box": "TNG300-1 205 Mpc/h",
           "thr": THR, "grid": "26-snap dense (10 orig + 16 new)",
           "snaps": SNAPS, "orig": ORIG, "new": NEW,
           "primary": {}, "jackknife": {str(o): {} for o in range(8)}}
out.setdefault("primary", {})
out.setdefault("jackknife", {str(o): {} for o in range(8)})
def flush():
    tmp = RES.with_suffix(".json.tmp")
    with open(tmp, "w") as fh:
        json.dump(out, fh, indent=1)
    tmp.replace(RES)

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

# ---------------------------------------------------------------------------
# estimator (VERBATIM from ../run_test.py)
# ---------------------------------------------------------------------------
import cupy as cp

def make_xi_table(ps, R_smooth=1.0, rmin=0.02, rmax=180.0, n=400_000):
    xi = ps.xi_spline(R_smooth)
    sig2 = ps.sigma2_R(R_smooth)
    r = np.logspace(np.log10(rmin), np.log10(rmax), n)
    return cp.asarray(r), cp.asarray(xi(r) / sig2), float(sig2)

def _cholesky_inplace(C, bs=2048):
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
    if guards:
        x = cp.random.RandomState(0).rand(k)
        for _ in range(50):
            x = C @ x; x /= cp.linalg.norm(x)
        lam_max = float(x @ (C @ x))
        del x
    ok = _cholesky_inplace(C)
    if not ok:
        del C
        cp.get_default_memory_pool().free_all_blocks()
        return None
    Sval = float(-2.0 * cp.log(cp.diagonal(C)).sum())
    lam_min = None
    if guards:
        Lv = C.T
        y = cp.random.RandomState(1).rand(k)
        y /= cp.linalg.norm(y)
        for _ in range(50):
            z = solve_triangular(Lv, y, lower=False, trans="T")
            z = solve_triangular(Lv, z, lower=False, trans="N")
            y = z / cp.linalg.norm(z)
        z = solve_triangular(Lv, y, lower=False, trans="T")
        z = solve_triangular(Lv, z, lower=False, trans="N")
        lam_min = float(1.0 / (y @ z))
        del y, z
    del C
    cp.get_default_memory_pool().free_all_blocks()
    return dict(S=Sval, k=k, lam_min=lam_min, lam_max=lam_max)

def S_with_jitter(pos, box, xr, xv, guards):
    r = S_gpu(pos, box, xr, xv, guards=guards)
    if r is None:
        r = S_gpu(pos, box, xr, xv, jitter=1e-8, guards=guards)
        if r is None:
            raise RuntimeError(f"Cholesky failed even with jitter at k={len(pos)}")
        r["jitter"] = 1e-8
    return r

# ---------------------------------------------------------------------------
# load 26 snapshots
# ---------------------------------------------------------------------------
snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64),
                         m200=d["m200"].astype(np.float64)))
kcount = [int((sd["m200"] > THR).sum()) for sd in snapdata]
log(f"loaded {len(snapdata)} snaps; k at frozen thr = {kcount} (max {max(kcount)})")
out["k_at_frozen_thr"] = {str(sd["snap"]): kcount[i] for i, sd in enumerate(snapdata)}
flush()

# ---------------------------------------------------------------------------
# validation gate on CAMELS CV_0 (CPU op_B vs GPU) — same discipline as parent
# ---------------------------------------------------------------------------
if not out.get("gate", {}).get("pass"):
    ps_cam = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
    cam = hg.load_snapshot(90, cv=0)
    cpu_rec = hg.op_B(ps_cam, [cam], 1e11)[0]
    xr_c, xv_c, _ = make_xi_table(ps_cam)
    gpu_rec = S_gpu(cam["pos"][cam["m200"] > 1e11], 25.0, xr_c, xv_c)
    rel = abs(gpu_rec["S"] - cpu_rec["S"]) / abs(cpu_rec["S"])
    out["gate"] = {"S_cpu": cpu_rec["S"], "S_gpu": gpu_rec["S"],
                   "rel_diff": rel, "pass": bool(rel < 1e-6)}
    flush()
    log(f"GATE: rel={rel:.2e} pass={rel < 1e-6}")
    assert rel < 1e-6, "validation gate FAILED — abort before any TNG number"

# ---------------------------------------------------------------------------
# TNG cosmology (patch AFTER the gate)
# ---------------------------------------------------------------------------
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)

oct_of = lambda p: ((p[:, 0] > BOX/2).astype(int) + 2*(p[:, 1] > BOX/2)
                    + 4*(p[:, 2] > BOX/2))

# ---------------------------------------------------------------------------
# primary S(a) — full grid at frozen threshold (resumable)
# ---------------------------------------------------------------------------
for sd in snapdata:
    key = str(sd["snap"])
    if key in out["primary"]:
        continue
    pos = sd["pos"][sd["m200"] > THR]
    r = S_with_jitter(pos, BOX, XR, XV, guards=True)
    r.update(a=sd["a"], z=sd["z"], snap=sd["snap"])
    out["primary"][key] = r
    flush()
    log(f"primary snap {sd['snap']} a={sd['a']:.3f} z={sd['z']:.3f}: k={r['k']} "
        f"S={r['S']:.2f} cond={r['lam_max']/r['lam_min']:.3g}")

# ---------------------------------------------------------------------------
# 8-octant jackknife — full grid (resumable, guards off)
# ---------------------------------------------------------------------------
for o in range(8):
    jk = out["jackknife"][str(o)]
    for sd in snapdata:
        key = str(sd["snap"])
        if key in jk:
            continue
        pos = sd["pos"][sd["m200"] > THR]
        keep = oct_of(pos) != o
        r = S_with_jitter(pos[keep], BOX, XR, XV, guards=False)
        jk[key] = r["S"]
        flush()
    log(f"jackknife octant {o} done: S(a=1)={jk[str(SNAPS[-1])]:.2f}")

# ---------------------------------------------------------------------------
# analysis
# ---------------------------------------------------------------------------
def analyze(a, Sa, label, project=True):
    a = np.asarray(a, float); Sa = np.asarray(Sa, float)
    ok = np.isfinite(Sa) & (Sa > 0)
    a, Sa = a[ok], Sa[ok]
    order = np.argsort(a); a, Sa = a[order], Sa[order]
    d = S.dln_dlna(a, Sa)
    w = -1.0 - d / 3.0
    res = {"label": label, "w_today": float(w[-1]),
           "dlnS_dlna_today": float(d[-1]),
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

a_p = np.array([out["primary"][str(s)]["a"] for s in SNAPS])
S_p = np.array([out["primary"][str(s)]["S"] for s in SNAPS])
stage5 = {"primary": analyze(a_p, S_p, f"B-total dense grid thr {THR:.2e}")}

# jackknife on interior-peak z and w_today
jk_cross, jk_w = [], []
for o in range(8):
    Sj = np.array([out["jackknife"][str(o)][str(s)] for s in SNAPS])
    zj = phys_crossing_z(a_p, Sj)
    jk_cross.append(zj if zj is not None else np.nan)
    dj = S.dln_dlna(a_p, Sj)
    jk_w.append(-1.0 - dj[-1] / 3.0)
jk_cross = np.array(jk_cross, float); jk_w = np.array(jk_w)
n_ok = int(np.isfinite(jk_cross).sum())
jkf = lambda v: float(np.sqrt((len(v)-1)/len(v) * ((v - v.mean())**2).sum()))
stage5["jackknife"] = {
    "crossing_z_values": jk_cross.tolist(),
    "crossing_z_err68": jkf(jk_cross[np.isfinite(jk_cross)]) if n_ok == 8 else None,
    "n_replicates_with_peak": n_ok,
    "w_today_values": jk_w.tolist(), "w_today_err68": jkf(jk_w)}
out["stage5"] = stage5
flush()

p = stage5["primary"]; j = stage5["jackknife"]
log("=" * 70)
log(f"DENSE thr={THR:.2e} ({len(SNAPS)} snaps): "
    f"w_today={p['w_today']:+.3f}+-{j['w_today_err68']:.3f}  "
    f"interior_peak_z={p['interior_peak_z']} +- {j['crossing_z_err68']} "
    f"({j['n_replicates_with_peak']}/8 with peak)")
log(f"  dist CPL: {p['dist_BAO+CMB']}")
log(f"  rho  CPL: {p['rho_DEweighted']}")
log("wrote results.json")
