#!/usr/bin/env python3
"""
Stage A (CPU): measure xi_hat(r) per snapshot at the frozen corner threshold, build
ln(1+xi) splines + measured-C interpolation tables + normalization sigma2_hat (3 R_smooth),
and the PSD (negative-eigenvalue-mass) diagnostic.  Everything per DECISIONS.md, fixed first.

Writes proxy_upgrade/measured_tables.npz and flushes proxy_upgrade/results.json incrementally.
No S(a) / no w computed here (that is the GPU stage, s_measured_gpu.py).
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
DATA = CEP / "large_volume" / "data"
LV = CEP / "large_volume" / "results.json"

# ---- frozen grid + corner threshold (read, not reselected) ----
SNAPS = [25, 30, 36, 42, 49, 56, 65, 76, 87, 99]
BOX = 205.0
lv = json.load(open(LV))
THR = float(lv["stage0"]["thr_corner_Msun_h"])

# ---- estimator constants (DECISIONS.md, fixed) ----
R_MIN, R_MAX, NBINS = 0.1, BOX / 2.0, 32          # r_max = L/2 = 102.5 (exact inscribed RR)
TABLE_RMAX = 180.0                                 # xi tapered to 0 on [R_MAX, TABLE_RMAX]
R_SMOOTH = 1.0
NORM_FACTORS = {"0.5x": 0.5, "1.0x": 1.0, "2.0x": 2.0}   # sensitivity on sigma2_hat
K_SUB_PSD = 6000                                   # subsample for full-spectrum PSD diagnostic
TILE = 1500
SEED = 20260710

T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

RES = HERE / "results.json"
out = {"stage": "measure_xi (CPU)", "date": "2026-07-10", "box_Mpc_h": BOX,
       "thr_corner_Msun_h": THR, "snaps": SNAPS,
       "estimator": {"r_min": R_MIN, "r_max": R_MAX, "nbins": NBINS,
                     "table_rmax": TABLE_RMAX, "R_smooth": R_SMOOTH,
                     "RR": "periodic analytic, ordered: N(N-1)*Vshell/Vbox",
                     "xi_hat": "DD/RR - 1", "spline": "cubic on ln(1+xi) vs ln r",
                     "beyond_rmax": "xi=0 (uncorrelated)"},
       "decisions": "proxy_upgrade/DECISIONS.md (pre-committed)"}
def flush():
    with open(RES, "w") as fh:
        json.dump(out, fh, indent=1)

LOG_EDGES = np.logspace(np.log10(R_MIN), np.log10(R_MAX), NBINS + 1)
R_CENT = np.sqrt(LOG_EDGES[:-1] * LOG_EDGES[1:])   # geometric bin centers
VBOX = BOX ** 3
VSHELL = (4.0 / 3.0) * np.pi * (LOG_EDGES[1:] ** 3 - LOG_EDGES[:-1] ** 3)


def periodic_dd_counts(pos):
    """Ordered DD(r) log-bin counts via tiled minimum-image distances."""
    n = len(pos)
    counts = np.zeros(NBINS, dtype=np.int64)
    for i0 in range(0, n, TILE):
        i1 = min(i0 + TILE, n)
        d2 = np.zeros((i1 - i0, n), dtype=np.float64)
        for ax in range(3):
            dx = np.abs(pos[i0:i1, ax][:, None] - pos[None, :, ax])
            np.minimum(dx, BOX - dx, out=dx)
            dx *= dx
            d2 += dx
        r = np.sqrt(d2, out=d2).ravel()
        # only pairs within [R_MIN, R_MAX]; self (r=0) excluded by R_MIN
        m = (r >= R_MIN) & (r <= R_MAX)
        counts += np.bincount(np.digitize(r[m], LOG_EDGES) - 1,
                              minlength=NBINS + 1)[:NBINS].astype(np.int64)
    return counts


def xi_hat_of(pos):
    n = len(pos)
    dd = periodic_dd_counts(pos)
    rr = n * (n - 1) * VSHELL / VBOX
    xi = dd / rr - 1.0
    return dd, rr, xi


def build_table(r_cent, xi, sig2_hat):
    """(xr, xv) table for S_gpu: xv = xi_smooth(r)/sig2_hat on [R_MIN, TABLE_RMAX];
    xi tapered to 0 on [R_MAX, TABLE_RMAX] (uncorrelated beyond measured range)."""
    ok = np.isfinite(xi) & (xi > -1.0)
    rc, xc = r_cent[ok], xi[ok]
    sp = CubicSpline(np.log(rc), np.log1p(xc))     # ln(1+xi) vs ln r
    r_grid = np.logspace(np.log10(R_MIN), np.log10(TABLE_RMAX), 4000)
    xi_g = np.expm1(sp(np.log(np.clip(r_grid, rc.min(), rc.max()))))
    xi_g = np.where(r_grid > R_MAX, 0.0, xi_g)     # zero beyond measured range
    xv = xi_g / sig2_hat
    return r_grid, xv, sp


def sig2_from_spline(r_cent, xi, R):
    ok = np.isfinite(xi) & (xi > -1.0)
    sp = CubicSpline(np.log(r_cent[ok]), np.log1p(xi[ok]))
    return float(np.expm1(sp(np.log(R))))


# ---------------------------------------------------------------------------
# 1. measure per snapshot
# ---------------------------------------------------------------------------
rng = np.random.default_rng(SEED)
records = []
tables = {}       # snap -> dict of R_smooth-factor -> (r_grid, xv)
snap_pos = {}     # keep positions for the PSD diagnostic
for s in SNAPS:
    d = np.load(DATA / f"tng300_groups_{s:03d}.npz")
    z, a = float(d["z"]), float(d["a"])
    sel = d["m200"] > THR
    pos = d["pos"][sel].astype(np.float64)
    k = len(pos)
    snap_pos[s] = pos
    dd, rr, xi = xi_hat_of(pos)
    sig2 = {name: sig2_from_spline(R_CENT, xi, f * R_SMOOTH)
            for name, f in NORM_FACTORS.items()}
    tables[s] = {}
    for name, f in NORM_FACTORS.items():
        r_grid, xv, _ = build_table(R_CENT, xi, sig2[name])
        tables[s][name] = (r_grid, xv)
    rec = dict(snap=s, z=z, a=a, k=k,
               r_cent=R_CENT.tolist(), xi_hat=xi.tolist(),
               dd=dd.tolist(),
               sigma2_hat=sig2,
               xi_at_1Mpc=float(sig2["1.0x"]),
               xi_min=float(np.nanmin(xi)), xi_max=float(np.nanmax(xi)))
    records.append(rec)
    log(f"snap {s:03d} z={z:5.3f} k={k:6d}  xi_hat(1Mpc)={sig2['1.0x']:.3f}  "
        f"xi_hat range [{np.nanmin(xi):+.3f},{np.nanmax(xi):+.2f}]")
    out["measured"] = records
    flush()

# save tables (per snap, per R_smooth factor) for the GPU stage
np.savez(HERE / "measured_tables.npz",
         snaps=np.array(SNAPS),
         **{f"xr_{s}_{name}": tables[s][name][0]
            for s in SNAPS for name in NORM_FACTORS},
         **{f"xv_{s}_{name}": tables[s][name][1]
            for s in SNAPS for name in NORM_FACTORS})
log("wrote measured_tables.npz")

# ---------------------------------------------------------------------------
# 2. PSD diagnostic: full spectrum on a k_sub subsample at z~3 (first) and z~0 (last)
# ---------------------------------------------------------------------------
def build_C_cpu(pos, xr, xv):
    n = len(pos)
    C = np.empty((n, n), dtype=np.float64)
    for i0 in range(0, n, TILE):
        i1 = min(i0 + TILE, n)
        d2 = np.zeros((i1 - i0, n))
        for ax in range(3):
            dx = np.abs(pos[i0:i1, ax][:, None] - pos[None, :, ax])
            np.minimum(dx, BOX - dx, out=dx)
            dx *= dx
            d2 += dx
        r = np.sqrt(d2, out=d2)
        np.clip(r, xr[0], xr[-1], out=r)
        C[i0:i1] = np.interp(r, xr, xv)
    np.fill_diagonal(C, 1.0)
    return C

psd = {}
for tag, s in [("early_z3", SNAPS[0]), ("late_z0", SNAPS[-1])]:
    pos = snap_pos[s]
    ksub = min(K_SUB_PSD, len(pos))
    idx = rng.choice(len(pos), size=ksub, replace=False)
    xr, xv = tables[s]["1.0x"]
    C = build_C_cpu(pos[idx], xr, xv)
    ev = np.linalg.eigvalsh(C)
    neg_mass = float(np.abs(ev[ev < 0]).sum() / np.abs(ev).sum())
    psd[tag] = dict(snap=s, k_sub=ksub, lam_min=float(ev.min()), lam_max=float(ev.max()),
                    n_negative=int((ev < 0).sum()), neg_eig_mass=neg_mass,
                    flag_fail=bool(neg_mass > 0.01))
    log(f"PSD {tag} snap {s}: k_sub={ksub} lam_min={ev.min():.4g} "
        f"neg_mass={neg_mass:.4e} fail(>1%)={neg_mass>0.01}")
    out["psd_diagnostic"] = psd
    flush()

out["psd_gate_pass"] = bool(all(not v["flag_fail"] for v in psd.values()))
flush()
log(f"PSD gate pass (both epochs <1% neg mass): {out['psd_gate_pass']}")
log("Stage A done.")
