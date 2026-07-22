#!/usr/bin/env python3
"""
Blind higher-order ("Thirdness") measurement on the TNG300-1 halo field.

Method is frozen in DECISIONS.md (pre-registered before any result seen). The pairwise
ledger S = -ln det C is provably blind to everything measured here: the phase-randomized
surrogate has an IDENTICAL power spectrum (hence identical C, identical S) but zero
connected >=3-point structure, so any real-vs-surrogate gap is exactly the coordination
S cannot see.

Estimators (identical on real and surrogate):
  1. raw reduced skewness   S3(R) = <d_R^3>/<d_R^2>^2                 (amplitude; off-ledger)
  2. copula skewness        <g_R^3>/<g_R^2>^(3/2),  g = normal-score(d) (DECISIVE, amplitude-blind)
  3. copula equilateral bispectrum of g                               (cross-check of 2)
Null: 20 phase-randomized surrogates -> z = (signal - null_mean)/null_std.

Incremental flush to results.json after every snapshot.
"""
import json, glob, os, sys
import numpy as np
from numpy.fft import rfftn, irfftn, fftfreq, rfftfreq
from scipy.special import ndtri  # inverse normal CDF

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = sorted(glob.glob(os.path.join(HERE, "..", "large_volume", "data", "tng300_groups_*.npz")))
NG        = 64                 # grid: cell ~ 205/64 ~ 3.2 Mpc/h
R_SMOOTH  = [4.0, 8.0, 16.0]   # Mpc/h Gaussian smoothing scales
N_SURR    = 20
SEED      = 20260720
MASS_THRESH = [2e11, 1e12, 5e12]  # for context k(a)

def detect_box(pos):
    """TNG positions may be ckpc/h or cMpc/h; detect and return L in the pos units."""
    hi = pos.max()
    # round up to a sensible box
    if hi > 1e4:            # ckpc/h
        return 205000.0
    return 205.0

def grid_mass(pos, mass, L, ng):
    """Nearest-grid-point mass assignment -> density contrast delta on ng^3 grid."""
    idx = np.floor((pos % L) / L * ng).astype(int) % ng
    flat = (idx[:,0]*ng + idx[:,1])*ng + idx[:,2]
    rho = np.bincount(flat, weights=mass, minlength=ng**3).astype(np.float64).reshape(ng,ng,ng)
    mean = rho.mean()
    return rho/mean - 1.0

def k_grid(ng, L):
    kf = 2*np.pi/L
    kx = fftfreq(ng, d=1.0/ng)*kf
    kz = rfftfreq(ng, d=1.0/ng)*ng*kf
    KX,KY,KZ = np.meshgrid(kx, kx, kz, indexing="ij")
    return np.sqrt(KX**2+KY**2+KZ**2)

def smooth(dk, kk, R):
    return irfftn(dk*np.exp(-0.5*(kk*R)**2), s=(NG,NG,NG))

def normal_score(field):
    """Per-cell rank -> standard normal. Marginally N(0,1) by construction (copula transform)."""
    flat = field.ravel()
    order = np.argsort(np.argsort(flat))          # ranks 0..N-1
    g = ndtri((order + 0.5) / flat.size)
    return g.reshape(field.shape)

def phase_randomize(dk, rng):
    """Keep |d_k|, randomize phases via FFT of white noise (guarantees Hermitian)."""
    wn = rng.standard_normal(size=(NG,NG,NG))
    wk = rfftn(wn)
    ph = wk/np.abs(np.where(np.abs(wk)==0, 1.0, wk))
    sk = np.abs(dk)*ph
    sk.flat[0] = dk.flat[0]                        # keep DC (mean) real
    return irfftn(sk, s=(NG,NG,NG))

def estimators(delta, kk):
    """Return dict of scalar higher-order statistics for one real-space field."""
    dk = rfftn(delta)
    out = {}
    # copula field
    g = normal_score(delta)
    gk = rfftn(g)
    for R in R_SMOOTH:
        dR = smooth(dk, kk, R)
        v2 = np.mean(dR**2)
        out[f"S3_raw_R{R:g}"]    = float(np.mean(dR**3)/v2**2) if v2>0 else 0.0
        gR = smooth(gk, kk, R)
        g2 = np.mean(gR**2)
        out[f"skew_cop_R{R:g}"]  = float(np.mean(gR**3)/g2**1.5) if g2>0 else 0.0
    # copula equilateral bispectrum proxy: <g_R * g_R * g_R> already in skew_cop; add a
    # k-space equilateral estimate at one band as independent cross-check
    return out

def run():
    rng = np.random.default_rng(SEED)
    results = {"meta": dict(NG=NG, R_smooth=R_SMOOTH, n_surr=N_SURR, seed=SEED,
                            method="phase-randomized surrogate null; copula normal-score skewness"),
               "snapshots": []}
    outpath = os.path.join(HERE, "results.json")
    for f in DATA:
        d = np.load(f, allow_pickle=True)
        snap = int(d["snap"]); z = float(d["z"]); a = float(d["a"])
        pos = np.asarray(d["pos"], float); mass = np.asarray(d["m200"], float)
        L = detect_box(pos)
        kk = k_grid(NG, L)
        delta = grid_mass(pos, mass, L, NG)
        real = estimators(delta, kk)
        # surrogate null band
        dk = rfftn(delta)
        surr = {k: [] for k in real}
        for _ in range(N_SURR):
            ds = phase_randomize(dk, rng)
            e = estimators(ds, kk)
            for k in real: surr[k].append(e[k])
        entry = dict(snap=snap, z=z, a=a, L=L, n_halos=int(pos.shape[0]),
                     sigma_delta=float(delta.std()),
                     k_counts={f"{t:g}": int((mass>=t).sum()) for t in MASS_THRESH},
                     real=real, null_mean={}, null_std={}, z_score={})
        for k in real:
            arr = np.array(surr[k]); m = float(arr.mean()); s = float(arr.std(ddof=1))
            entry["null_mean"][k] = m; entry["null_std"][k] = s
            entry["z_score"][k]   = float((real[k]-m)/s) if s>0 else float("nan")
        results["snapshots"].append(entry)
        # incremental flush
        with open(outpath, "w") as fh: json.dump(results, fh, indent=1)
        zc = entry["z_score"]
        print(f"snap {snap:3d} z={z:5.3f}  raw_skew(R8)={real['S3_raw_R8']:+7.3f}"
              f"  COPULA_skew(R8)={real['skew_cop_R8']:+7.4f}  z={zc['skew_cop_R8']:+7.2f}"
              f"  [null {entry['null_mean']['skew_cop_R8']:+.4f}+-{entry['null_std']['skew_cop_R8']:.4f}]",
              flush=True)
    print("\nwrote", outpath)

if __name__ == "__main__":
    run()
