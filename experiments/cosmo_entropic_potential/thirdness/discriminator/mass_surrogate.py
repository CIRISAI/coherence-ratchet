#!/usr/bin/env python3
"""
K4 discriminator -- the null for the ACTUAL frozen (mass-weighted) measurement.

The frozen thirdness measurement is MASS-weighted (m200). Its proper discreteness null is a
Poisson point process (matched n_bar and pairwise power) whose points carry masses drawn from
the REAL halo mass function but placed INDEPENDENTLY of environment -- i.e. same discreteness,
same mass distribution, same pairwise clustering, but NO mass-environment coupling and no
genuine connected >=3-point.  If real_mass survives above this (S1m), the frozen copula Third
requires genuine coordination; if it collapses to S1m, K4 fires on the frozen measurement.

  S0m  phase-randomize the mass field directly (continuous, matched mass P(k))     N=10  (~0 expected)
  S1m  compound-Poisson mass surrogate (random masses, no environment coupling)    N=20  (the null)

Same grain NG=64, identical copula estimator, positional tie-break (frozen behaviour).
Incremental flush per snapshot to mass_results.json.
"""
import json, glob, os
import numpy as np
from numpy.fft import rfftn, irfftn, fftfreq, rfftfreq
from scipy.special import ndtri

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = sorted(glob.glob(os.path.join(HERE, "..", "..", "large_volume", "data", "tng300_groups_*.npz")))
NG=64; R_SMOOTH=[4.0,8.0,16.0]; N_S0M=10; N_S1M=20; SEED=20260720

def detect_box(pos): return 205000.0 if pos.max()>1e4 else 205.0
def k_grid(ng,L):
    kf=2*np.pi/L; kx=fftfreq(ng,d=1.0/ng)*kf; kz=rfftfreq(ng,d=1.0/ng)*ng*kf
    KX,KY,KZ=np.meshgrid(kx,kx,kz,indexing="ij"); return np.sqrt(KX**2+KY**2+KZ**2)
def grid_ngp(pos,w,L,ng):
    idx=np.floor((pos%L)/L*ng).astype(int)%ng
    flat=(idx[:,0]*ng+idx[:,1])*ng+idx[:,2]
    rho=np.bincount(flat,weights=w,minlength=ng**3).astype(np.float64).reshape(ng,ng,ng)
    return rho/rho.mean()-1.0
def normal_score(field):
    flat=field.ravel(); order=np.argsort(np.argsort(flat)); return ndtri((order+0.5)/flat.size).reshape(field.shape)
def smooth(fk,kk,R): return irfftn(fk*np.exp(-0.5*(kk*R)**2), axes=(0,1,2), s=(NG,NG,NG))
def copula_skew(field,kk):
    gk=rfftn(normal_score(field)); out={}
    for R in R_SMOOTH:
        gR=smooth(gk,kk,R); g2=np.mean(gR**2); out[R]=float(np.mean(gR**3)/g2**1.5) if g2>0 else np.nan
    return out
def phase_rand_amp(amp,rng):
    wk=rfftn(rng.standard_normal((NG,NG,NG))); ph=wk/np.abs(np.where(np.abs(wk)==0,1.0,wk))
    sk=amp*ph; sk.flat[0]=0.0; return irfftn(sk, axes=(0,1,2), s=(NG,NG,NG))

def run():
    rng=np.random.default_rng(SEED+1); kk=k_grid(NG,205.0); M=NG**3
    res={"meta":dict(NG=NG,R=R_SMOOTH,N_S0m=N_S0M,N_S1m=N_S1M,seed=SEED,
                     note="mass-weighted discreteness null for the frozen measurement"),
         "snapshots":[]}
    outpath=os.path.join(HERE,"mass_results.json")
    for f in DATA:
        d=np.load(f,allow_pickle=True)
        snap=int(d["snap"]); z=float(d["z"]); a=float(d["a"])
        pos=np.asarray(d["pos"],float); mass=np.asarray(d["m200"],float)
        L=detect_box(pos); N=pos.shape[0]; nbar=N/M
        fld_mass=grid_ngp(pos,mass,L,NG)
        real=copula_skew(fld_mass,kk)
        amp_count=np.abs(rfftn(grid_ngp(pos,np.ones(N),L,NG)))   # matched count P(k)
        amp_mass =np.abs(rfftn(fld_mass))
        b0={R:[] for R in R_SMOOTH}; b1={R:[] for R in R_SMOOTH}
        for _ in range(N_S0M):                    # continuous mass null
            cs=copula_skew(phase_rand_amp(amp_mass,rng),kk)
            for R in R_SMOOTH: b0[R].append(cs[R])
        for _ in range(N_S1M):                    # compound-Poisson mass surrogate
            dG=phase_rand_amp(amp_count,rng)
            mu=np.clip(nbar*(1.0+dG),0,None)
            n=rng.poisson(mu); nflat=n.ravel().astype(np.int64); Ntot=int(nflat.sum())
            masses=rng.choice(mass,size=Ntot,replace=True)      # real MF, no environment coupling
            cell=np.repeat(np.arange(M),nflat)
            rho=np.bincount(cell,weights=masses,minlength=M).astype(np.float64).reshape(NG,NG,NG)
            surr=rho/rho.mean()-1.0
            cs=copula_skew(surr,kk)
            for R in R_SMOOTH: b1[R].append(cs[R])
        entry=dict(snap=snap,z=z,a=a,N=N,nbar=nbar,real=real,
                   S0m_mean={R:float(np.mean(b0[R])) for R in R_SMOOTH},
                   S0m_std ={R:float(np.std(b0[R],ddof=1)) for R in R_SMOOTH},
                   S1m_mean={R:float(np.mean(b1[R])) for R in R_SMOOTH},
                   S1m_std ={R:float(np.std(b1[R],ddof=1)) for R in R_SMOOTH},
                   z_vs_S1m={})
        for R in R_SMOOTH:
            s=entry["S1m_std"][R]; m=entry["S1m_mean"][R]
            entry["z_vs_S1m"][R]=float((real[R]-m)/s) if s>0 else float("nan")
        res["snapshots"].append(entry)
        with open(outpath,"w") as fh: json.dump(res,fh,indent=1)
        print(f"snap {snap:3d} z={z:5.3f}  R8: real_mass={real[8.0]:+.4f}  "
              f"S0m={entry['S0m_mean'][8.0]:+.4f} S1m={entry['S1m_mean'][8.0]:+.4f}"
              f"(+-{entry['S1m_std'][8.0]:.4f})  z_vs_S1m={entry['z_vs_S1m'][8.0]:+.2f}",flush=True)
    print("\nwrote",outpath)

if __name__=="__main__":
    run()
