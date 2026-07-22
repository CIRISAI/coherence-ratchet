#!/usr/bin/env python3
"""
K4 discriminator (DECISIVE leg): is the copula Third real coordination or a
discreteness/shot-noise artifact?  Method frozen in DECISIONS.md before any number seen.

For each of the 26 TNG300-1 snapshots, on the SAME grain (NG=64) as the frozen measurement,
compute the copula skewness (normal-score -> Fourier Gaussian smooth -> standardized skew,
IDENTICAL estimator to measure_thirdness.py) on:

  REAL field variants:  {count, mass} weight  x  {NGP, CIC} assignment  x  {positional, random}
                        tie-break,  R in {4,8,16}.  (real_mass_ngp_pos must reproduce results.json)

  SURROGATE bands (count field, NGP, positional -- matched to the surrogate construction):
    S0  phase-randomized continuous Gaussian (frozen null; expect ~0)          N=20
    S1  Poisson-clipped-Gaussian (DECISIVE shot null; matched n_bar, |d_k|)     N=20
    S1b shot-subtracted Poisson-Gaussian (brackets the double-shot)            N=20
    S2  lognormal-Poisson reference (standard nonlinear clustering+discreteness) N=10

Verdict statistic (pre-registered): |skew|_real(count,NGP,pos) vs the S1 band at R=8.
Incremental flush per snapshot to poisson_results.json.
"""
import json, glob, os
import numpy as np
from numpy.fft import rfftn, irfftn, fftfreq, rfftfreq
from scipy.special import ndtri

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = sorted(glob.glob(os.path.join(HERE, "..", "..", "large_volume", "data", "tng300_groups_*.npz")))
NG      = 64
R_SMOOTH= [4.0, 8.0, 16.0]
N_S0    = 20
N_S1    = 20
N_S1B   = 20
N_S2    = 10
SEED    = 20260720

# ---------- gridding ----------
def detect_box(pos):
    return 205000.0 if pos.max() > 1e4 else 205.0

def grid_ngp(pos, w, L, ng):
    idx = np.floor((pos % L)/L*ng).astype(int) % ng
    flat = (idx[:,0]*ng+idx[:,1])*ng+idx[:,2]
    rho = np.bincount(flat, weights=w, minlength=ng**3).astype(np.float64).reshape(ng,ng,ng)
    return rho/rho.mean() - 1.0

def grid_cic(pos, w, L, ng):
    """Cloud-in-cell assignment (anti-aliased)."""
    x = (pos % L)/L*ng
    i0 = np.floor(x).astype(int)
    d  = x - i0
    rho = np.zeros(ng**3, np.float64)
    for dx in (0,1):
        wx = (1-d[:,0]) if dx==0 else d[:,0]
        ix = (i0[:,0]+dx) % ng
        for dy in (0,1):
            wy = (1-d[:,1]) if dy==0 else d[:,1]
            iy = (i0[:,1]+dy) % ng
            for dz in (0,1):
                wz = (1-d[:,2]) if dz==0 else d[:,2]
                iz = (i0[:,2]+dz) % ng
                flat = (ix*ng+iy)*ng+iz
                rho += np.bincount(flat, weights=w*wx*wy*wz, minlength=ng**3)
    rho = rho.reshape(ng,ng,ng)
    return rho/rho.mean() - 1.0

# ---------- estimator (identical to frozen) ----------
def k_grid(ng, L):
    kf = 2*np.pi/L
    kx = fftfreq(ng, d=1.0/ng)*kf
    kz = rfftfreq(ng, d=1.0/ng)*ng*kf
    KX,KY,KZ = np.meshgrid(kx, kx, kz, indexing="ij")
    return np.sqrt(KX**2+KY**2+KZ**2)

def normal_score(field, tie="positional", rng=None):
    flat = field.ravel()
    if tie == "positional":
        order = np.argsort(np.argsort(flat))           # frozen behaviour
    elif tie == "random":
        # random tie-break: jitter equal values before ranking
        jit = rng.standard_normal(flat.size)*1e-9*(np.abs(flat).mean()+1e-30)
        order = np.argsort(np.argsort(flat + jit))
    g = ndtri((order + 0.5)/flat.size)
    return g.reshape(field.shape)

def smooth(fk, kk, R):
    return irfftn(fk*np.exp(-0.5*(kk*R)**2), s=(NG,NG,NG))

def copula_skew(field, kk, tie="positional", rng=None):
    g = normal_score(field, tie, rng)
    gk = rfftn(g)
    out = {}
    for R in R_SMOOTH:
        gR = smooth(gk, kk, R); g2 = np.mean(gR**2)
        out[R] = float(np.mean(gR**3)/g2**1.5) if g2>0 else np.nan
    return out

# ---------- surrogates ----------
def phase_randomize_amp(amp, rng):
    """Given a real-space amplitude spectrum |d_k| (rfftn shape), return a Gaussian field."""
    wk = rfftn(rng.standard_normal(size=(NG,NG,NG)))
    ph = wk/np.abs(np.where(np.abs(wk)==0, 1.0, wk))
    sk = amp*ph
    sk.flat[0] = 0.0                                   # zero mean overdensity
    return irfftn(sk, s=(NG,NG,NG))

def poisson_count_field(intensity_field, rng):
    """intensity_field = expected counts per cell (>=0). Return delta of a Poisson draw."""
    n = rng.poisson(np.clip(intensity_field, 0, None))
    m = n.mean()
    return n/m - 1.0 if m>0 else n*0.0

def run():
    rng = np.random.default_rng(SEED)
    res = {"meta": dict(NG=NG, R=R_SMOOTH, N_S0=N_S0, N_S1=N_S1, N_S1B=N_S1B, N_S2=N_S2,
                        seed=SEED, note="K4 discriminator: Poisson shot-noise surrogates"),
           "snapshots": []}
    outpath = os.path.join(HERE, "poisson_results.json")
    kk = k_grid(NG, 205.0)
    M = NG**3
    for f in DATA:
        d = np.load(f, allow_pickle=True)
        snap=int(d["snap"]); z=float(d["z"]); a=float(d["a"])
        pos=np.asarray(d["pos"],float); mass=np.asarray(d["m200"],float)
        L = detect_box(pos); N = pos.shape[0]; nbar = N/M
        ones = np.ones(N)

        # ---- REAL variants
        real = {}
        fields = {
            "count_ngp": grid_ngp(pos, ones, L, NG),
            "mass_ngp" : grid_ngp(pos, mass, L, NG),
            "count_cic": grid_cic(pos, ones, L, NG),
            "mass_cic" : grid_cic(pos, mass, L, NG),
        }
        for name, fld in fields.items():
            real[name+"_pos"] = copula_skew(fld, kk, "positional")
        # random tie-break only where it matters most (count NGP, mass NGP)
        real["count_ngp_rand"] = copula_skew(fields["count_ngp"], kk, "random", rng)
        real["mass_ngp_rand"]  = copula_skew(fields["mass_ngp"],  kk, "random", rng)

        # ---- measure the count-field shot level empirically (uniform Poisson, same N)
        pshot_samples = []
        for _ in range(5):
            nu = rng.poisson(nbar, size=(NG,NG,NG)).astype(float)
            du = nu/nu.mean()-1.0
            pshot_samples.append(np.mean(np.abs(rfftn(du))**2))
        P_shot = float(np.mean(pshot_samples))

        # count-field amplitude spectrum (for S0/S1/S2) and shot-subtracted (S1b)
        dk_count = rfftn(fields["count_ngp"])
        amp = np.abs(dk_count)
        power = amp**2
        amp_sub = np.sqrt(np.clip(power - P_shot, 0, None))

        # ---- SURROGATE bands (count field, NGP, positional)
        bands = {k: {R: [] for R in R_SMOOTH} for k in ("S0","S1","S1b","S2")}
        def collect(key, fld):
            cs = copula_skew(fld, kk, "positional")
            for R in R_SMOOTH: bands[key][R].append(cs[R])

        for _ in range(N_S0):                       # S0 continuous Gaussian null
            collect("S0", phase_randomize_amp(amp, rng))
        for _ in range(N_S1):                       # S1 Poisson-clipped-Gaussian
            dG = phase_randomize_amp(amp, rng)
            collect("S1", poisson_count_field(nbar*(1.0+dG), rng))
        for _ in range(N_S1B):                      # S1b shot-subtracted Poisson-Gaussian
            dG = phase_randomize_amp(amp_sub, rng)
            collect("S1b", poisson_count_field(nbar*(1.0+dG), rng))
        for _ in range(N_S2):                       # S2 lognormal-Poisson reference
            g = phase_randomize_amp(amp, rng)       # linear power = real count power
            lam = nbar*np.exp(g - 0.5*np.var(g))
            collect("S2", poisson_count_field(lam, rng))

        entry = dict(snap=snap, z=z, a=a, N=N, nbar=nbar, P_shot=P_shot, real=real,
                     surr_mean={}, surr_std={}, z_vs={})
        for key in bands:
            entry["surr_mean"][key] = {R: float(np.nanmean(bands[key][R])) for R in R_SMOOTH}
            entry["surr_std"][key]  = {R: float(np.nanstd(bands[key][R], ddof=1)) for R in R_SMOOTH}
        # verdict z-scores: real count_ngp_pos vs each surrogate band
        rc = real["count_ngp_pos"]
        for key in bands:
            entry["z_vs"][key] = {}
            for R in R_SMOOTH:
                s = entry["surr_std"][key][R]; m = entry["surr_mean"][key][R]
                entry["z_vs"][key][R] = float((rc[R]-m)/s) if s>0 else float("nan")
        res["snapshots"].append(entry)
        with open(outpath,"w") as fh: json.dump(res, fh, indent=1)
        print(f"snap {snap:3d} z={z:5.3f}  R8: real_count={rc[8.0]:+.3f} "
              f"real_mass={real['mass_ngp_pos'][8.0]:+.3f}  "
              f"S0={entry['surr_mean']['S0'][8.0]:+.3f} S1={entry['surr_mean']['S1'][8.0]:+.3f}"
              f"(+-{entry['surr_std']['S1'][8.0]:.3f}) S1b={entry['surr_mean']['S1b'][8.0]:+.3f} "
              f"S2={entry['surr_mean']['S2'][8.0]:+.3f}  z_vsS1={entry['z_vs']['S1'][8.0]:+.1f}",
              flush=True)
    print("\nwrote", outpath)

if __name__ == "__main__":
    run()
