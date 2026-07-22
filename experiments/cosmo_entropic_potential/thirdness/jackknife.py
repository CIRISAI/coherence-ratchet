#!/usr/bin/env python3
"""
Sub-volume jackknife for the copula-Thirdness epoch structure.

Splits the 205 Mpc/h box into 3^3 = 27 sub-cubes, runs the IDENTICAL copula-skewness
estimator (normal-score -> real-space Gaussian smooth -> standardized skewness on the
trimmed interior) in each, on the real field and on one phase-randomized surrogate.

Two questions:
  (A) Detection robustness: is the box-mean copula skew negative and inconsistent with the
      surrogate, per snapshot, with a cosmic-variance error bar?
  (B) Epoch structure: is |copula skew| genuinely larger near the DE epoch (z~0.5-0.65) than
      at z~0 and z~2.5?  Tested PAIRED across the 27 sub-cubes (same regions across time ->
      cosmic variance cancels in the difference).  Stores the full (snap x subcube) matrix.

Incremental flush. Real-space smoothing (mode='reflect') so sub-cubes don't wrap.
"""
import json, glob, os
import numpy as np
from scipy.special import ndtri
from scipy.ndimage import gaussian_filter
from numpy.fft import rfftn, irfftn

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = sorted(glob.glob(os.path.join(HERE, "..", "large_volume", "data", "tng300_groups_*.npz")))
NG    = 96                  # full grid, divisible by 3 -> 27 sub-cubes of 32^3
NSUB  = 3
SUB   = NG // NSUB          # 32
R_MPC = [4.0, 8.0]
SEED  = 20260720

def detect_box(pos):
    return 205000.0 if pos.max() > 1e4 else 205.0

def grid_mass(pos, mass, L, ng):
    idx = np.floor((pos % L)/L*ng).astype(int) % ng
    flat = (idx[:,0]*ng+idx[:,1])*ng+idx[:,2]
    rho = np.bincount(flat, weights=mass, minlength=ng**3).astype(np.float64).reshape(ng,ng,ng)
    return rho/rho.mean() - 1.0

def phase_randomize(delta, rng):
    dk = rfftn(delta)
    wk = rfftn(rng.standard_normal(size=delta.shape))
    ph = wk/np.abs(np.where(np.abs(wk)==0,1.0,wk))
    sk = np.abs(dk)*ph; sk.flat[0] = dk.flat[0]
    return irfftn(sk, s=delta.shape)

def copula_skew_cube(block, sig_cells):
    """normal-score within the sub-cube, real-space smooth, standardized skew on trimmed interior."""
    order = np.argsort(np.argsort(block.ravel()))
    g = ndtri((order+0.5)/block.size).reshape(block.shape)
    gR = gaussian_filter(g, sig_cells, mode='reflect')
    t = int(np.ceil(2*sig_cells))
    gi = gR[t:-t, t:-t, t:-t] if (t>0 and 2*t < block.shape[0]) else gR
    v2 = np.mean(gi**2)
    return float(np.mean(gi**3)/v2**1.5) if v2>0 else np.nan

def all_subcubes(delta, cell_mpc):
    """Return {R: [27 skew values]} over the 3^3 sub-cubes."""
    out = {R: [] for R in R_MPC}
    for i in range(NSUB):
        for j in range(NSUB):
            for k in range(NSUB):
                blk = delta[i*SUB:(i+1)*SUB, j*SUB:(j+1)*SUB, k*SUB:(k+1)*SUB]
                for R in R_MPC:
                    out[R].append(copula_skew_cube(blk, R/cell_mpc))
    return out

def run():
    rng = np.random.default_rng(SEED)
    res = {"meta": dict(NG=NG, nsub=NSUB, sub=SUB, R_mpc=R_MPC, seed=SEED), "snapshots": []}
    outpath = os.path.join(HERE, "jackknife_results.json")
    for f in DATA:
        d = np.load(f, allow_pickle=True)
        snap=int(d["snap"]); z=float(d["z"]); a=float(d["a"])
        pos=np.asarray(d["pos"],float); mass=np.asarray(d["m200"],float)
        L=detect_box(pos); cell = L/NG / (1000.0 if L>1e4 else 1.0)  # Mpc/h per cell
        delta = grid_mass(pos, mass, L, NG)
        real = all_subcubes(delta, cell)
        surr = all_subcubes(phase_randomize(delta, rng), cell)
        entry = dict(snap=snap, z=z, a=a, cell_mpc=cell)
        for R in R_MPC:
            r=np.array(real[R]); s=np.array(surr[R])
            entry[f"real_R{R:g}"]=r.tolist(); entry[f"surr_R{R:g}"]=s.tolist()
            entry[f"mean_R{R:g}"]=float(np.nanmean(r))
            entry[f"err_R{R:g}"]=float(np.nanstd(r,ddof=1)/np.sqrt(np.sum(~np.isnan(r))))
            entry[f"surr_mean_R{R:g}"]=float(np.nanmean(s))
        res["snapshots"].append(entry)
        with open(outpath,"w") as fh: json.dump(res, fh)
        print(f"snap {snap:3d} z={z:5.3f}  R8 mean={entry['mean_R8']:+.4f}+-{entry['err_R8']:.4f}"
              f" (surr {entry['surr_mean_R8']:+.4f})   R4 mean={entry['mean_R4']:+.4f}+-{entry['err_R4']:.4f}",
              flush=True)
    print("\nwrote", outpath)

if __name__ == "__main__":
    run()
