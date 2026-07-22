#!/usr/bin/env python3
"""
K4 discriminator (bias/tracer leg): does the copula Third scale with bias (mass threshold)
and change between tracers?  A nonlinear-halo-bias artifact scales with bias; genuine matter
coordination should be more stable.  Descriptive trend (pre-registered in DECISIONS.md, no
hard cut -- the bias leg is not cleanly killable without the DM particle field).

Same grain (NG=64) and IDENTICAL copula estimator as the frozen measurement.
For each snapshot, copula skew at R in {4,8} for:
  groups  mass-weighted   thresholds m200 >= {1e11, 1e12, 5e12}
  groups  count-weighted  thresholds m200 >= {1e11, 1e12, 5e12}
  galaxies count-weighted mstar >= {0, 1e9, 1e10}
  galaxies mstar-weighted mstar >= 0
Each with a small phase-randomized S0 null band (N=10) for a z-score.
Incremental flush per snapshot to tracer_results.json.
"""
import json, glob, os
import numpy as np
from numpy.fft import rfftn, irfftn, fftfreq, rfftfreq
from scipy.special import ndtri

HERE = os.path.dirname(os.path.abspath(__file__))
DDIR = os.path.join(HERE, "..", "..", "large_volume", "data")
GRP  = sorted(glob.glob(os.path.join(DDIR, "tng300_groups_*.npz")))
NG   = 64
R_SMOOTH = [4.0, 8.0]
N_NULL = 10
SEED = 20260720

def detect_box(pos): return 205000.0 if pos.max() > 1e4 else 205.0
def k_grid(ng, L):
    kf=2*np.pi/L; kx=fftfreq(ng,d=1.0/ng)*kf; kz=rfftfreq(ng,d=1.0/ng)*ng*kf
    KX,KY,KZ=np.meshgrid(kx,kx,kz,indexing="ij"); return np.sqrt(KX**2+KY**2+KZ**2)
def grid_ngp(pos, w, L, ng):
    idx=np.floor((pos%L)/L*ng).astype(int)%ng
    flat=(idx[:,0]*ng+idx[:,1])*ng+idx[:,2]
    rho=np.bincount(flat,weights=w,minlength=ng**3).astype(np.float64).reshape(ng,ng,ng)
    return rho/rho.mean()-1.0
def normal_score(field):
    flat=field.ravel(); order=np.argsort(np.argsort(flat)); return ndtri((order+0.5)/flat.size).reshape(field.shape)
def smooth(fk,kk,R): return irfftn(fk*np.exp(-0.5*(kk*R)**2), s=(NG,NG,NG))
def copula_skew(field, kk):
    gk=rfftn(normal_score(field)); out={}
    for R in R_SMOOTH:
        gR=smooth(gk,kk,R); g2=np.mean(gR**2); out[R]=float(np.mean(gR**3)/g2**1.5) if g2>0 else np.nan
    return out
def phase_rand(dk, rng):
    wk=rfftn(rng.standard_normal((NG,NG,NG))); ph=wk/np.abs(np.where(np.abs(wk)==0,1.0,wk))
    sk=np.abs(dk)*ph; sk.flat[0]=dk.flat[0]; return irfftn(sk,s=(NG,NG,NG))

def measure(fld, kk, rng):
    real = copula_skew(fld, kk)
    dk = rfftn(fld); nb = {R: [] for R in R_SMOOTH}
    for _ in range(N_NULL):
        cs = copula_skew(phase_rand(dk, rng), kk)
        for R in R_SMOOTH: nb[R].append(cs[R])
    out = {}
    for R in R_SMOOTH:
        m=float(np.mean(nb[R])); s=float(np.std(nb[R],ddof=1))
        out[str(R)] = dict(real=real[R], null_mean=m, null_std=s,
                           z=float((real[R]-m)/s) if s>0 else float("nan"))
    return out

def run():
    rng = np.random.default_rng(SEED)
    kk = k_grid(NG, 205.0)
    res = {"meta": dict(NG=NG, R=R_SMOOTH, N_null=N_NULL, seed=SEED,
                        note="copula Third vs mass threshold (bias) and tracer"),
           "snapshots": []}
    outpath = os.path.join(HERE, "tracer_results.json")
    for gf in GRP:
        d = np.load(gf, allow_pickle=True)
        snap=int(d["snap"]); z=float(d["z"]); a=float(d["a"])
        pos=np.asarray(d["pos"],float); mass=np.asarray(d["m200"],float)
        L=detect_box(pos)
        entry=dict(snap=snap, z=z, a=a, configs={})
        # groups: mass-weighted and count-weighted across mass thresholds
        for thr,lbl in [(1e11,"1e11"),(1e12,"1e12"),(5e12,"5e12")]:
            sel = mass>=thr
            if sel.sum() < 500: continue
            p=pos[sel]; m=mass[sel]
            entry["configs"][f"grp_mass_m{lbl}"] = dict(k=int(sel.sum()),
                **measure(grid_ngp(p, m, L, NG), kk, rng))
            entry["configs"][f"grp_count_m{lbl}"]= dict(k=int(sel.sum()),
                **measure(grid_ngp(p, np.ones(sel.sum()), L, NG), kk, rng))
        # galaxies
        gxf = gf.replace("groups","galaxies")
        if os.path.exists(gxf):
            g=np.load(gxf, allow_pickle=True)
            gp=np.asarray(g["pos"],float); ms=np.asarray(g["mstar"],float)
            Lg=detect_box(gp)
            for thr,lbl in [(0.0,"all"),(1e9,"1e9"),(1e10,"1e10")]:
                sel = ms>=thr if thr>0 else ms>0  # mstar>0 removes dark subhalos
                if sel.sum() < 500: continue
                p=gp[sel]
                entry["configs"][f"gal_count_ms{lbl}"] = dict(k=int(sel.sum()),
                    **measure(grid_ngp(p, np.ones(sel.sum()), Lg, NG), kk, rng))
            selm = ms>0
            entry["configs"]["gal_mstar_msall"] = dict(k=int(selm.sum()),
                **measure(grid_ngp(gp[selm], ms[selm], Lg, NG), kk, rng))
        res["snapshots"].append(entry)
        with open(outpath,"w") as fh: json.dump(res, fh, indent=1)
        c=entry["configs"]
        def g8(key): return c[key]["8.0"]["real"] if key in c else float("nan")
        print(f"snap {snap:3d} z={z:5.3f}  R8 copula skew: "
              f"grp_mass[1e11]={g8('grp_mass_m1e11'):+.3f} [1e12]={g8('grp_mass_m1e12'):+.3f} "
              f"[5e12]={g8('grp_mass_m5e12'):+.3f} | grp_count[1e11]={g8('grp_count_m1e11'):+.3f} | "
              f"gal_count[all]={g8('gal_count_msall'):+.3f} gal_mstar={g8('gal_mstar_msall'):+.3f}",
              flush=True)
    print("\nwrote", outpath)

if __name__ == "__main__":
    run()
