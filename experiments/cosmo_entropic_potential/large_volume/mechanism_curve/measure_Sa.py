#!/usr/bin/env python3
"""
Mechanism-curve GPU stage: frozen B-total S(a) + k(a) across a ladder of mass
thresholds on TNG300-1 (205 Mpc/h, 10 snapshots z=3..0).

The frozen B-total pipeline, identical to large_volume/run_test.py stage 2/3:
  C_ij = xi_R(r_ij) / sig2_R  at halo positions (R_smooth=1.0), S = -ln det C
  via GPU blocked Cholesky log-det.  guards off (mechanism curve needs S,k only).

S_gpu / _cholesky_inplace / make_xi_table are copied verbatim from run_test.py
(NOT imported: importing run_test.py executes its whole pipeline).

TNG cosmology (Planck2015): Om=0.3089 OL=0.6911 Ob=0.0486 h=0.6774 ns=0.9667
sigma8=0.8159 -- patched into s_of_a AFTER importing halo_grain.

Incremental flush to raw_Sa.json after every (threshold, snapshot).  The CPU
theory/analysis + figure live in analyze_curve.py (no GPU, no lock).
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
LV = HERE.parent                      # large_volume/
DATA = LV / "data"
CEP = LV.parent                       # cosmo_entropic_potential/
HG = CEP / "halo_grain"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))

import halo_grain as hg               # side-effect free; patches s_of_a to CAMELS
import s_of_a as S

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
CAP = 38000
# 12 log-spaced thresholds from the corner (7.4253e11) to 2e13 Msun/h.
THR_LO = 742530285568.0               # = large_volume corner threshold (reproduces z0.590 pt)
THR_HI = 2e13
THRESHOLDS = np.logspace(np.log10(THR_LO), np.log10(THR_HI), 12)

RAW = HERE / "raw_Sa.json"
out = {"date": "2026-07-10", "box": "TNG300-1 205 Mpc/h", "cap": CAP,
       "R_smooth": 1.0, "snaps": SNAPS,
       "cosmology": dict(Om=0.3089, OL=0.6911, Ob=0.0486, h=0.6774,
                         ns=0.9667, sigma8=0.8159),
       "thresholds_Msun_h": THRESHOLDS.tolist(), "per_threshold": {}}
def flush():
    with open(RAW, "w") as fh:
        json.dump(out, fh, indent=1)

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

# ---------------------------------------------------------------------------
# load snapshots
# ---------------------------------------------------------------------------
snapdata = []
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    snapdata.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                         pos=d["pos"].astype(np.float64),
                         m200=d["m200"].astype(np.float64)))
A_GRID = np.array([sd["a"] for sd in snapdata])
Z_GRID = np.array([sd["z"] for sd in snapdata])
out["a_grid"] = A_GRID.tolist(); out["z_grid"] = Z_GRID.tolist()
flush()

# ---------------------------------------------------------------------------
# GPU S: same number as op_B's -sum(log eig(C)), via Cholesky log-det.
# Copied verbatim from large_volume/run_test.py.
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
    del C
    cp.get_default_memory_pool().free_all_blocks()
    return dict(S=Sval, k=k)

# ---------------------------------------------------------------------------
# TNG cosmology power spectrum (patch s_of_a globals AFTER importing halo_grain)
# ---------------------------------------------------------------------------
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)
log(f"xi table built; sig2_R(1.0)={SIG2:.6g}; {len(THRESHOLDS)} thresholds")

# ---------------------------------------------------------------------------
# main loop: per threshold, S(a) + k(a) on the 10-snapshot grid
# ---------------------------------------------------------------------------
for ti, thr in enumerate(THRESHOLDS):
    key = f"{thr:.4e}"
    recs = []
    for sd in snapdata:
        sel = sd["m200"] > thr
        pos = sd["pos"][sel]
        k = int(len(pos))
        if k < 3:
            recs.append(dict(a=sd["a"], z=sd["z"], k=k, S=None, jitter=None))
            continue
        r = S_gpu(pos, BOX, XR, XV)
        jit = 0.0
        if r is None:                                  # PD failure -> jitter
            r = S_gpu(pos, BOX, XR, XV, jitter=1e-8)
            jit = 1e-8
            if r is None:
                recs.append(dict(a=sd["a"], z=sd["z"], k=k, S=None, jitter="fail"))
                out["per_threshold"][key] = {"thr": float(thr), "records": recs}
                flush()
                raise RuntimeError(f"Cholesky failed even with jitter at thr={thr:.3e} "
                                   f"a={sd['a']:.3f} k={k}")
        recs.append(dict(a=sd["a"], z=sd["z"], k=k, S=r["S"], jitter=jit))
        out["per_threshold"][key] = {"thr": float(thr), "records": recs}
        flush()
    ks = [r["k"] for r in recs]
    Ss = [None if r["S"] is None else round(r["S"], 2) for r in recs]
    log(f"thr[{ti+1}/12]={thr:.3e}: k={ks}")
    log(f"                 S={Ss}")

log("DONE — all thresholds measured; raw_Sa.json complete")
out["complete"] = True
flush()
