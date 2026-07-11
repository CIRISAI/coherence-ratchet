#!/usr/bin/env python3
"""
Stage B (GPU): measured-C S(a) at the corner threshold via the SAME fp64 in-place
blocked Cholesky log-det used for the model run (S_gpu / _cholesky_inplace copied
verbatim from ../large_volume/run_test.py — NOT imported). The ONLY change from the
model run is the interpolation table: per-snapshot MEASURED xi_hat tables from
measured_tables.npz, instead of the single model xi table.

Primary = 1.0x normalization; also computes 0.5x/2.0x R_smooth normalization
(sensitivity). Holds the GPU flock for the whole GPU section (blocking acquire —
waits patiently if another job holds it). Flushes results_gpu.json incrementally.
"""
import json, sys, time, fcntl
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
LV = CEP / "large_volume" / "results.json"
LOCK = "/tmp/claude-1000/gpu.lockfile"

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
thr_corner = float(json.load(open(LV))["stage0"]["thr_corner_Msun_h"])
NORM = ["1.0x", "0.5x", "2.0x"]

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

# ---- measured tables (per snap, per R_smooth factor) ----
tab = np.load(HERE / "measured_tables.npz")

import cupy as cp

# ===== verbatim from run_test.py =====
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
# ===== end verbatim =====

def run_snapshot(pos, xr_np, xv_np):
    xr, xv = cp.asarray(xr_np), cp.asarray(xv_np)
    r = S_gpu(pos, BOX, xr, xv)
    if r is None:
        r = S_gpu(pos, BOX, xr, xv, jitter=1e-8)
        if r is not None:
            r["jitter"] = 1e-8
    del xr, xv
    cp.get_default_memory_pool().free_all_blocks()
    return r

out = {"stage": "s_measured_gpu", "thr_corner": thr_corner, "box": BOX,
       "note": "measured-C S(a); S_gpu verbatim from run_test.py; only xi table swapped",
       "records": {n: [] for n in NORM}}
RES = HERE / "results_gpu.json"
def flush(): RES.write_text(json.dumps(out, indent=1))

# preload positions
posmap = {}
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    sel = d["m200"] > thr_corner
    posmap[s] = d["pos"][sel].astype(np.float64)

log(f"acquiring GPU flock (blocking) at {LOCK} ...")
lf = open(LOCK, "w")
fcntl.flock(lf, fcntl.LOCK_EX)
log("GPU flock acquired.")
try:
    for name in NORM:
        for s in SNAPS:
            d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
            z, a = float(d["z"]), float(d["a"])
            xr_np = tab[f"xr_{s}_{name}"]; xv_np = tab[f"xv_{s}_{name}"]
            r = run_snapshot(posmap[s], xr_np, xv_np)
            if r is None:
                log(f"[{name}] snap {s} a={a:.3f}: PD FAILURE even with jitter")
                out["records"][name].append(dict(a=a, z=z, k=len(posmap[s]), S=None))
            else:
                r.update(a=a, z=z)
                out["records"][name].append(r)
                cond = r["lam_max"] / r["lam_min"] if r["lam_min"] else None
                log(f"[{name}] snap {s} a={a:.3f} k={r['k']} S={r['S']:.2f} "
                    f"lam_min={r['lam_min']:.4g} cond={cond:.3g}"
                    + (" [jitter]" if r.get('jitter') else ""))
            flush()
finally:
    fcntl.flock(lf, fcntl.LOCK_UN); lf.close()
    log("GPU flock released.")
log("Stage B done.")
