#!/usr/bin/env python3
"""
SHM retention-anchor scan: frozen B-total S(a) as a function of the UNIT MASS SCALE.

Hypothesis (operator, 2026-07-10): the cosmological ledger's units are the halos that
can STORE HISTORY (maximal record retention). The independently measured retention
scale is the stellar-to-halo-mass (SHM) efficiency peak, M_halo ~ 10^11.9-12.0 Msun
(Moster 2013; Behroozi 2013/2019). If true, DESI-fit quality vs unit mass scale should
EXTREMIZE near the SHM peak -- two independently measured curves aligning, no dial.

This script computes, resumably, the frozen B-total S(a) for a LADDER OF MASS BINS
(bins isolate a scale; thresholds run as a sensitivity) on TNG300-1 (26 snaps, box 205)
and TNG100-1 (10 snaps, box 75, extends below 1e11). GPU estimator (S_gpu /
_cholesky_inplace / make_xi_table) copied VERBATIM from ../large_volume/run_test.py
(NOT imported). CPL projection / likelihood are done in analyze_scan.py (CPU).

Cap per bin/snap at 38000 (compute limit: C is 11.6 GB at k=38000 on a 16 GB card);
subsample with a fixed deterministic seed if exceeded -- documented as B-fixedk-like for
dense bins. Flush after every eval; resumable.

Run under the GPU lock:
  flock /tmp/claude-1000/gpu.lockfile -c "python3 compute_scan.py"
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
LV_DATA = CEP / "large_volume" / "data"
T100_DATA = CEP / "tng100_cross" / "data"
HG = CEP / "halo_grain"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))

import halo_grain as hg          # patches s_of_a to CAMELS values (used for the gate)
import s_of_a as S

# --- frozen grid & spec -----------------------------------------------------
ORIG = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
NEW  = [33, 39, 45, 47, 51, 53, 55, 59, 61, 63, 67, 70, 72, 74, 79, 82]
SNAPS300 = sorted(ORIG + NEW)                 # 26 dense-grid snaps
SNAPS100 = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]   # TNG100 fetched grid

CAP = 38000
WIDTH_DEX = 0.4                               # bin full width; center +- 0.2 dex
CENTERS300 = [11.0, 11.25, 11.5, 11.75, 12.0, 12.25, 12.5, 12.75, 13.0]  # log10 Msun/h
CENTERS100 = [10.2, 10.4, 10.6, 10.8, 11.0]                              # log10 Msun/h
# threshold sensitivity (cumulative >M), coarse 10-snap grid, TNG300 only:
THRESH300 = [1e11, 2e11, 5e11, 7.425e11, 1e12, 2e12, 5e12, 1e13]

RES = HERE / "results.json"
if RES.exists():
    out = json.load(open(RES))
else:
    out = {"date": "2026-07-10",
           "hypothesis": "retention anchor: DESI-fit quality vs unit mass scale peaks "
                         "at the SHM efficiency peak (~10^11.9-12.0 Msun ~ 10^11.78-11.83 "
                         "Msun/h at h=0.6774)",
           "spec": {"cap": CAP, "width_dex": WIDTH_DEX,
                    "centers_tng300_log10Msunh": CENTERS300,
                    "centers_tng100_log10Msunh": CENTERS100,
                    "thresholds_tng300": THRESH300,
                    "snaps_tng300": SNAPS300, "snaps_tng100": SNAPS100,
                    "h": 0.6774,
                    "note": "bins are center +- 0.2 dex (0.4 dex full, overlapping, "
                            "spacing 0.25 dex on TNG300 / 0.2 dex on TNG100); "
                            "subsample seed = 20260710 + round(center*100) + snap"},
           "tng300_bins": {}, "tng100_bins": {},
           "tng300_bins_jackknife": {}, "tng300_thresholds": {}}
for k in ("tng300_bins", "tng100_bins", "tng300_bins_jackknife", "tng300_thresholds"):
    out.setdefault(k, {})

def flush():
    tmp = RES.with_suffix(".json.tmp")
    with open(tmp, "w") as fh:
        json.dump(out, fh, indent=1)
    tmp.replace(RES)

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

# ---------------------------------------------------------------------------
# estimator (VERBATIM from ../large_volume/run_test.py)
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

def S_with_jitter(pos, box, xr, xv, guards=True):
    r = S_gpu(pos, box, xr, xv, guards=guards)
    if r is None:
        r = S_gpu(pos, box, xr, xv, jitter=1e-8, guards=guards)
        if r is None:
            raise RuntimeError(f"Cholesky failed even with jitter at k={len(pos)}")
        r["jitter"] = 1e-8
    return r

def subsample(pos, n_target, seed):
    if len(pos) <= n_target:
        return pos, len(pos), False
    idx = np.random.RandomState(seed).choice(len(pos), n_target, replace=False)
    return pos[idx], n_target, True

# ---------------------------------------------------------------------------
# load snapshots
# ---------------------------------------------------------------------------
def load_box(data_dir, prefix, snaps):
    sd = []
    for s in snaps:
        d = np.load(data_dir / f"{prefix}_{s:03d}.npz")
        sd.append(dict(snap=s, z=float(d["z"]), a=float(d["a"]),
                       pos=d["pos"].astype(np.float64),
                       m200=d["m200"].astype(np.float64)))
    return sd

snap300 = load_box(LV_DATA, "tng300_groups", SNAPS300)
snap100 = load_box(T100_DATA, "tng100_groups", SNAPS100)
log(f"loaded TNG300 {len(snap300)} snaps, TNG100 {len(snap100)} snaps")

# ---------------------------------------------------------------------------
# validation gate on CAMELS CV_0 (CPU op_B vs GPU) -- same discipline as parent
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
    assert rel < 1e-6, "validation gate FAILED -- abort before any TNG number"

# ---------------------------------------------------------------------------
# TNG cosmology (patch AFTER the gate); same Planck2015 for both boxes
# ---------------------------------------------------------------------------
S.OM, S.OL, S.OB, S.H0H, S.NS, S.SIGMA8 = 0.3089, 0.6911, 0.0486, 0.6774, 0.9667, 0.8159
ps_tng = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)
XR, XV, SIG2 = make_xi_table(ps_tng)

def bin_key(center): return f"{center:.3f}"

# ---------------------------------------------------------------------------
# Stage A: TNG300 mass-BIN S(a) (resumable)
# ---------------------------------------------------------------------------
def run_bins(snapdata, centers, box, store, tag):
    for c in centers:
        lo, hi = 10.0 ** (c - WIDTH_DEX / 2), 10.0 ** (c + WIDTH_DEX / 2)
        rec = store.setdefault(bin_key(c), {"center": c, "lo": lo, "hi": hi,
                                            "box": box, "records": {}})
        recs = rec["records"]
        for sd in snapdata:
            key = str(sd["snap"])
            if key in recs:
                continue
            sel = (sd["m200"] >= lo) & (sd["m200"] < hi)
            pos = sd["pos"][sel]
            n_in = int(sel.sum())
            if n_in < 3:
                recs[key] = dict(a=sd["a"], z=sd["z"], k=n_in, n_in_bin=n_in,
                                 S=None, capped=False)
                flush(); continue
            seed = 20260710 + int(round(c * 100)) + sd["snap"]
            pos_s, n_used, capped = subsample(pos, CAP, seed)
            r = S_with_jitter(pos_s, box, XR, XV, guards=True)
            r.update(a=sd["a"], z=sd["z"], n_in_bin=n_in, capped=bool(capped))
            recs[key] = r
            flush()
            log(f"{tag} c={c} a={sd['a']:.3f} z={sd['z']:.3f}: n_in={n_in} k={r['k']} "
                f"cap={capped} S={r['S']:.2f} cond={r['lam_max']/r['lam_min']:.2g}")
        log(f"{tag} bin c={c} DONE")

log("=== Stage A: TNG300 bins ===")
run_bins(snap300, CENTERS300, 205.0, out["tng300_bins"], "T300")

log("=== Stage B: TNG100 bins ===")
run_bins(snap100, CENTERS100, 75.0, out["tng100_bins"], "T100")

# ---------------------------------------------------------------------------
# Stage C: 8-octant jackknife on the galaxy-host anchor bin c=12.0 (TNG300)
#          (representative epoch/fit error bar; full-grid jackknife on every bin
#           is ~7 h, so we anchor one bin and use plateau breadth elsewhere)
# ---------------------------------------------------------------------------
ANCHOR = 12.0
oct_of = lambda p, box: ((p[:, 0] > box/2).astype(int) + 2*(p[:, 1] > box/2)
                         + 4*(p[:, 2] > box/2))
log("=== Stage C: octant jackknife on TNG300 anchor bin c=12.0 ===")
jstore = out["tng300_bins_jackknife"].setdefault(bin_key(ANCHOR), {str(o): {} for o in range(8)})
c = ANCHOR
lo, hi = 10.0 ** (c - WIDTH_DEX / 2), 10.0 ** (c + WIDTH_DEX / 2)
for o in range(8):
    jk = jstore.setdefault(str(o), {})
    for sd in snap300:
        key = str(sd["snap"])
        if key in jk:
            continue
        sel = (sd["m200"] >= lo) & (sd["m200"] < hi)
        pos = sd["pos"][sel]
        seed = 20260710 + int(round(c * 100)) + sd["snap"]
        pos_s, n_used, capped = subsample(pos, CAP, seed)
        keep = oct_of(pos_s, 205.0) != o
        r = S_with_jitter(pos_s[keep], 205.0, XR, XV, guards=False)
        jk[key] = r["S"]
        flush()
    log(f"jackknife octant {o} done")

# ---------------------------------------------------------------------------
# Stage D: TNG300 threshold sensitivity (cumulative >M), coarse 10-snap grid
# ---------------------------------------------------------------------------
log("=== Stage D: TNG300 threshold sensitivity (coarse 10-snap) ===")
snap300_coarse = [sd for sd in snap300 if sd["snap"] in ORIG]
for thr in THRESH300:
    tk = f"{thr:.3e}"
    rec = out["tng300_thresholds"].setdefault(tk, {"thr": thr, "box": 205.0, "records": {}})
    recs = rec["records"]
    for sd in snap300_coarse:
        key = str(sd["snap"])
        if key in recs:
            continue
        sel = sd["m200"] > thr
        pos = sd["pos"][sel]
        n_in = int(sel.sum())
        if n_in < 3:
            recs[key] = dict(a=sd["a"], z=sd["z"], k=n_in, n_in_bin=n_in, S=None, capped=False)
            flush(); continue
        seed = 77000000 + int(round(np.log10(thr) * 100)) + sd["snap"]
        pos_s, n_used, capped = subsample(pos, CAP, seed)
        r = S_with_jitter(pos_s, 205.0, XR, XV, guards=False)
        r.update(a=sd["a"], z=sd["z"], n_in_bin=n_in, capped=bool(capped))
        recs[key] = r
        flush()
        log(f"thr {tk} a={sd['a']:.3f}: n_in={n_in} k={r['k']} cap={capped} S={r['S']:.2f}")
    log(f"threshold {tk} DONE")

log("ALL STAGES COMPLETE")
