#!/usr/bin/env python3
"""
P4 intensive fence, Task 2: fixed-k geometry.
Hold the count fixed at k = 8606 (the z=3 count at the corner threshold). At each
snapshot draw n_draw=8 seeded random subsamples of the above-corner-threshold halos
and compute S = -log det C on the GPU (identical S_gpu machinery as run_test.py).
This removes k(a) entirely: only the point-set geometry evolves. Report S(a),
per-draw std, spline dlnS/dlna slope, global OLS slope. Verdict: rising or falling.

GPU-guarded: run under flock /tmp/claude-1000/gpu.lockfile.
Incremental flush to p4_fence/results.json (merges Task 1's keys if present).
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
LV = HERE.parent
CEP = LV.parent
DATA = LV / "data"
HG = CEP / "halo_grain"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))

import halo_grain as hg   # noqa: patches s_of_a to CAMELS; we re-patch to TNG below
import s_of_a as S

SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
THR = 742530285568.0    # corner threshold (Msun/h), from stage0
K_FIX = 8606            # z=3 count at corner threshold
N_DRAW = 8
SEED = 20260710

import cupy as cp

# ---- machinery copied verbatim from run_test.py (do NOT import run_test) ------
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
# ------------------------------------------------------------------------------

def Sval(pos, jitter=0.0):
    r = S_gpu(pos, BOX, XR, XV, guards=False)
    if r is None:
        r = S_gpu(pos, BOX, XR, XV, jitter=1e-8, guards=False)
        if r is None:
            raise RuntimeError(f"Cholesky failed even with jitter at k={len(pos)}")
    return r["S"]

# TNG cosmology power spectrum (patch AFTER importing halo_grain, as instructed)
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)

RES = HERE / "results.json"
out = json.load(open(RES)) if RES.exists() else {}
T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

records = []
rng = np.random.default_rng(SEED)
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    a = float(d["a"]); z = float(d["z"])
    pos_all = d["pos"].astype(np.float64)[d["m200"].astype(np.float64) > THR]
    k_avail = len(pos_all)
    if k_avail < K_FIX:
        raise RuntimeError(f"snap {s}: only {k_avail} above threshold < K_FIX={K_FIX}")
    draws = []
    if k_avail == K_FIX:
        draws.append(Sval(pos_all))          # only one possible draw (z=3 anchor)
    else:
        for di in range(N_DRAW):
            idx = rng.choice(k_avail, size=K_FIX, replace=False)
            draws.append(Sval(pos_all[idx]))
    rec = dict(snap=s, a=a, z=z, k=K_FIX, k_avail=k_avail,
               n_draw=len(draws), S_mean=float(np.mean(draws)),
               S_std=float(np.std(draws, ddof=1)) if len(draws) > 1 else 0.0,
               S_draws=[float(x) for x in draws])
    records.append(rec)
    out["fixedk_geometry"] = {
        "k_fixed": K_FIX, "n_draw": N_DRAW, "seed": SEED, "thr": THR,
        "records": records}
    with open(RES, "w") as fh:
        json.dump(out, fh, indent=1)
    log(f"a={a:.3f} k_avail={k_avail} S_mean={rec['S_mean']:.2f} "
        f"S_std={rec['S_std']:.2f} (n_draw={rec['n_draw']})")

# slopes on the fixed-k mean curve
a = np.array([r["a"] for r in records])
Sm = np.array([r["S_mean"] for r in records])
o = np.argsort(a); a, Sm = a[o], Sm[o]
dsp = S.dln_dlna(a, Sm)
ols = float(np.polyfit(np.log(a), np.log(Sm), 1)[0])
verdict = {
    "dlnS_dlna_spline": dsp.tolist(),
    "w_spline": (-1.0 - dsp / 3.0).tolist(),
    "dlnS_dlna_today": float(dsp[-1]),
    "w_today": float(-1.0 - dsp[-1] / 3.0),
    "ols_global_slope": ols,
    "w_from_ols": float(-1.0 - ols / 3.0),
    "S_first_last": [float(Sm[0]), float(Sm[-1])],
    "peak_a": float(a[np.argmax(Sm)]),
    "peak_interior": bool(0 < np.argmax(Sm) < len(Sm) - 1),
    "n_rising_nodes": int((dsp > 0).sum()),
    "max_spline_slope": float(dsp.max()),
    "phantom_anywhere_ols": bool(ols > 0),
    "phantom_any_node": bool((dsp > 0).any()),
}
out["fixedk_geometry"]["verdict"] = verdict
with open(RES, "w") as fh:
    json.dump(out, fh, indent=1)

log("=" * 68)
log(f"FIXED-k={K_FIX}: S {Sm[0]:.2f} -> {Sm[-1]:.2f}, peak a={verdict['peak_a']:.3f} "
    f"(interior={verdict['peak_interior']})")
log(f"  global OLS slope = {ols:+.4f} -> w={verdict['w_from_ols']:+.3f}  "
    f"(rising={verdict['phantom_anywhere_ols']})")
log(f"  spline slope today = {dsp[-1]:+.4f} -> w_today={verdict['w_today']:+.3f}")
log(f"  rising nodes {verdict['n_rising_nodes']}/{len(a)}  "
    f"max slope {verdict['max_spline_slope']:+.4f}")
log("wrote p4_fence/results.json")
