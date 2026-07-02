#!/usr/bin/env python3
"""
BARYON-CYCLE test: does the GAS of the same complete galaxy COORDINATE?

The stellar component was bound / detailed-balance-satisfying -- expected, because
stars are ~collisionless/conservative. Coordination, if anywhere, lives in the
GAS: the baryon cycle (inflow -> star formation -> feedback -> outflow -> cool ->
re-inflow) is a dissipative, self-regulated loop. This runs the SAME two readouts
on PartType0 (gas) of CAMELS IllustrisTNG CV_0, main progenitor of subhalo 0.

EULERIAN construction (gas has NO persistent IDs -- Voronoi refinement, gas->stars
-- so no ParticleID tracking). Fixed cells in the galaxy's INSTANTANEOUS frame
(disk-aligned, star-tracked center); the natural frame for flows. A 3D grid of
disk-aligned cells within +/-R; per cell per snapshot:
   log rho   = log10(gas mass in cell / cell volume)      [density]
   logT      = mass-weighted log10 temperature (TNG formula)
   v_r       = mass-weighted galactocentric radial velocity (physical peculiar)
UNITS = grid cells populated in ALL snapshots; OBSERVATIONS = snapshots. The
cell x cell correlation over snapshots is a genuine collective-mode decomposition
(NOT the trivial cells x {few properties} table).

READOUTS
 (1) SATURATION: is gas dynamics low-rank (bounded k_eff) as cells are added?
 (2) DETAILED BALANCE (crux):
   (a) mode-circulation omega on top collective modes vs phase-randomized null
       (+ OU-equilibrium / OU-driven / relaxation calibrators);
   (b) DIRECT baryon-cycle signature: net circulation in a THERMODYNAMIC phase-
       plane. Per cell, trajectory in (log rho, logT) and in (log rho, v_r) over
       cosmic time; mean circulation <x dy - y dx> across cells vs phase-rand
       null. A LOOP (net circulation) = sustained self-regulated cycle = NESS =
       coordinating; a ONE-WAY drift (monotone depletion) = transient relaxation.
       Also the GLOBAL mass-weighted mean-state trajectory in (log rho, logT).

CAVEATS (load-bearing, in the summary): TNG gas has cooling+feedback BY
CONSTRUCTION, so SOME irreversibility is guaranteed -- the question is sustained
homeostatic CYCLE vs one-way depletion. Star-forming gas sits on TNG's effective
EOS (T not physical on the cold-dense branch) -> the (rho,T) cold branch is
model-imposed; flagged. T=26 snapshots is short; one simulated galaxy. And
"TNG-physics dissipation" is NOT automatically the framework's gamma*M -- flagged.

Real sim data only; synthetics only calibrate. Reuses analysis core + robust_center
from spectral_galaxy.py.
"""
import numpy as np, h5py, fsspec, json, os, time, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sg", os.path.join(HERE, "spectral_galaxy.py"))
sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)
RNG = np.random.default_rng(0)
SCRATCH = sg.SCRATCH; BASE = sg.BASE
# Gas test uses the ASSEMBLED-galaxy epoch only: at z>~1 the galaxy is still
# fragmented (main progenitor holds few of the z=0 stars), so "the galaxy's gas"
# and its frame are ill-defined. z<~1 is the quasi-steady baryon-cycle regime.
SNAPS = list(range(60, 91, 2))          # z = 1.05 -> 0.0, 16 snapshots
opn = sg.opn
corr_eig, participation_ratio, mp_edge = sg.corr_eig, sg.participation_ratio, sg.mp_edge
phase_randomize, subsample_pr, powerlaw_alpha = sg.phase_randomize, sg.subsample_pr, sg.powerlaw_alpha
synth_lowrank, synth_powerlaw, synth_noise = sg.synth_lowrank, sg.synth_powerlaw, sg.synth_noise

XH=0.76; GAMMA=5/3.; MP=1.6726e-24; KB=1.3807e-16
RGRID = 60.0     # half-box of the disk-aligned cube, physical kpc/h
NGRID = 8        # cells per side -> up to 512 cells

def gas_temperature(u, xe):
    mu = 4.0/(1+3*XH+4*XH*xe)*MP
    return (GAMMA-1)*(u*1e10)*mu/KB          # Kelvin

def fetch_group_gas(snap, center_hint):
    """Read ONLY the main-progenitor FOF halo's gas (nearest group to the star
    center) via the group offset -- a contiguous snapshot slice. Cached."""
    cache = f"{SCRATCH}/gal_gas_{snap:03d}.npz"
    if os.path.exists(cache):
        d = np.load(cache); return {k: d[k] for k in d.files}
    with opn(f"{BASE}/groups_{snap:03d}.hdf5") as f:
        GLT = f['Group/GroupLenType'][:]; GPos = f['Group/GroupPos'][:]
    box = 25000.0
    dd = GPos - center_hint; dd -= box*np.round(dd/box)
    dist = np.linalg.norm(dd, axis=1)
    real = np.where(GLT[:, 0] > 5000)[0]              # nearest REAL halo (ignore spurious tiny groups)
    g = int(real[np.argmin(dist[real])]) if real.size else int(np.argmin(dist))
    off = int(GLT[:g, 0].sum()); n = int(GLT[g, 0])
    with opn(f"{BASE}/snapshot_{snap:03d}.hdf5") as f:
        a = float(f['Header'].attrs['Time'])
        sl = slice(off, off+n)
        pos = f['PartType0/Coordinates'][sl].astype(np.float64)
        vel = f['PartType0/Velocities'][sl].astype(np.float64)
        mass = f['PartType0/Masses'][sl].astype(np.float64)
        u = f['PartType0/InternalEnergy'][sl].astype(np.float64)
        xe = f['PartType0/ElectronAbundance'][sl].astype(np.float64)
        sfr = f['PartType0/StarFormationRate'][sl].astype(np.float64)
    d = dict(a=a, gpos=GPos[g], pos=pos, vel=vel, mass=mass,
             T=gas_temperature(u, xe), sfr=sfr)
    np.savez(cache, **d); return d

def star_frame(snap, keep_ids):
    """galaxy center, bulk velocity, disk axis from tracked stars at this snap."""
    d = sg.fetch_snapshot_stars(snap)
    order = np.argsort(d['ids']); sid = d['ids'][order]
    pin = np.searchsorted(sid, keep_ids); idx = order[pin]
    pos = d['pos'][idx]; vel = d['vel'][idx]; a = d['a']
    p, c, V, core = sg.robust_center(pos, vel)
    r = (p-c)*a; vv = vel*np.sqrt(a)-V
    L = np.cross(r[core], vv[core]).sum(0); Lh = L/(np.linalg.norm(L)+1e-30)
    return c, V, Lh, a

def build_gas_cells():
    """cells x snapshot matrices for logrho, logT, v_r (disk-aligned 3D grid)."""
    # persistent tracked stars -> consistent per-snapshot galaxy frame
    tids = np.load(f"{SCRATCH}/target_ids.npy"); tids = tids[tids > 0]
    present = None
    for s in SNAPS:
        d = sg.fetch_snapshot_stars(s)
        present = np.isin(tids, d['ids']) if present is None else (present & np.isin(tids, d['ids']))
    keep_ids = tids[present]
    box = 25000.0; edges = np.linspace(-RGRID, RGRID, NGRID+1)
    vol = ((2*RGRID/NGRID))**3           # (kpc/h)^3, constant per cell
    ncell = NGRID**3
    LR = np.full((ncell, len(SNAPS)), np.nan)
    LT = np.full((ncell, len(SNAPS)), np.nan)
    VR = np.full((ncell, len(SNAPS)), np.nan)
    prevLh = None
    for ti, s in enumerate(SNAPS):
        c_hint, _, _, a = star_frame(s, keep_ids)        # only to identify the main halo
        g = fetch_group_gas(s, c_hint)
        c = g['gpos']                                    # center on the halo potential min (robust)
        dp = g['pos'] - c; dp -= box*np.round(dp/box)
        r = (dp*a)                                       # physical kpc/h
        vgas = g['vel']*np.sqrt(a)                       # physical peculiar km/s
        rn = np.linalg.norm(r, axis=1)
        inner = rn < 30.0                                # bulk velocity + disk axis from inner gas
        m = g['mass']; T = g['T']
        wV = m[inner][:, None]
        V = (wV*vgas[inner]).sum(0)/ (m[inner].sum()+1e-30)
        vv = vgas - V
        Lg = (m[inner][:, None]*np.cross(r[inner], vv[inner])).sum(0)
        Lh = Lg/(np.linalg.norm(Lg)+1e-30)
        if prevLh is not None and np.dot(Lh, prevLh) < 0: Lh = -Lh
        prevLh = Lh
        tmp = np.array([0,0,1.0]) if abs(Lh[2]) < 0.9 else np.array([1.0,0,0])
        e1 = np.cross(Lh, tmp); e1 /= np.linalg.norm(e1); e2 = np.cross(Lh, e1)
        R = np.vstack([e1, e2, Lh])
        xyz = r @ R.T
        rn = np.linalg.norm(r, axis=1); rhat = r/(rn[:,None]+1e-30)
        vr = np.sum(vv*rhat, axis=1)
        m = g['mass']; T = g['T']
        inside = np.all(np.abs(xyz) < RGRID, axis=1)
        ix = np.clip(np.floor((xyz[:,0]+RGRID)/(2*RGRID)*NGRID).astype(int),0,NGRID-1)
        iy = np.clip(np.floor((xyz[:,1]+RGRID)/(2*RGRID)*NGRID).astype(int),0,NGRID-1)
        iz = np.clip(np.floor((xyz[:,2]+RGRID)/(2*RGRID)*NGRID).astype(int),0,NGRID-1)
        cell = (ix*NGRID + iy)*NGRID + iz
        cell = np.where(inside, cell, -1)
        mass_cell = np.zeros(ncell); mT = np.zeros(ncell); mvr = np.zeros(ncell)
        sel = cell >= 0
        np.add.at(mass_cell, cell[sel], m[sel])
        np.add.at(mT, cell[sel], (m*np.log10(T))[sel])
        np.add.at(mvr, cell[sel], (m*vr)[sel])
        pop = mass_cell > 0
        LR[pop, ti] = np.log10(mass_cell[pop]/vol)
        LT[pop, ti] = mT[pop]/mass_cell[pop]
        VR[pop, ti] = mvr[pop]/mass_cell[pop]
        print(f"  gas snap {s:03d} z={1/a-1:4.2f}: halo gas cells {sel.sum():6d}, populated grid cells {pop.sum():4d}", flush=True)
    return LR, LT, VR

# ---- detailed-balance estimators (same omega as spectral_galaxy_db.py) ------
def omega(x, y):
    dx=np.diff(x); dy=np.diff(y); xm=x[:-1]; ym=y[:-1]
    den=np.mean(xm**2+ym**2); return float(np.mean(xm*dy-ym*dx)/den) if den>0 else 0.0
def phaserand(v):
    F=np.fft.rfft(v); ph=np.exp(1j*RNG.uniform(0,2*np.pi,F.shape)); ph[0]=1
    return np.fft.irfft(F*ph, n=len(v))
def modes(X, k=4):
    good=np.isfinite(X).all(1)&(X.std(1)>1e-12); Z=X[good]
    Z=(Z-Z.mean(1,keepdims=True))/Z.std(1,keepdims=True)
    U,S,Vt=np.linalg.svd(Z, full_matrices=False); return (S[:,None]*Vt)[:k]
def db_modepairs(A, npair=3, nnull=3000):
    pairs=[(i,j) for i in range(npair) for j in range(i+1,npair)]
    res={}; obs_sum=0.0; null_sum=np.zeros(nnull)
    for (i,j) in pairs:
        obs=omega(A[i],A[j]); null=np.array([omega(phaserand(A[i]),phaserand(A[j])) for _ in range(nnull)])
        res[f"{i}-{j}"]=dict(omega=obs,z=float((obs-null.mean())/(null.std()+1e-12)))
        obs_sum+=abs(obs); null_sum+=np.abs(null)
    return res, dict(circ=float(obs_sum), z=float((obs_sum-null_sum.mean())/(null_sum.std()+1e-12)))

def thermo_circulation(Xa, Xb, nnull=2000):
    """Per-cell circulation in the (Xa,Xb) plane over snapshots, averaged; std-normalized per axis."""
    good=np.isfinite(Xa).all(1)&np.isfinite(Xb).all(1)&(Xa.std(1)>1e-9)&(Xb.std(1)>1e-9)
    A=Xa[good]; B=Xb[good]
    # normalize each axis globally so circulation is dimensionless & comparable
    A=(A-A.mean())/ (A.std()+1e-12); B=(B-B.mean())/(B.std()+1e-12)
    om=np.array([omega(A[i],B[i]) for i in range(A.shape[0])])
    obs=float(om.mean())
    null=np.empty(nnull)
    for k in range(nnull):
        oo=np.array([omega(phaserand(A[i]),phaserand(B[i])) for i in range(A.shape[0])])
        null[k]=oo.mean()
    z=float((obs-null.mean())/(null.std()+1e-12))
    return dict(mean_omega=obs, z=z, ncells=int(A.shape[0]))

def analyze_saturation(X, scalar):
    good=np.isfinite(X).all(1)&(X.std(1)>1e-12); Z=X[good]; N,T=Z.shape
    ev,N,T=corr_eig(Z); pr=participation_ratio(ev); edge=mp_edge(N,T)
    Xs=phase_randomize(Z); evs,*_=corr_eig(Xs); surr_top=float(evs.max())
    eff_mp=int((ev>edge).sum()); eff_surr=int((ev>surr_top).sum()); alpha=powerlaw_alpha(ev)
    sizes=sorted(set([s for s in [8,12,16,24,32,48,64,100,150,200,300,N] if s<=N]))
    curve=subsample_pr(Z, sizes, ndraw=20)
    cn=np.array([c[0] for c in curve]); cp=np.array([c[1] for c in curve])
    up=cn>=max(24,cn.max()//4)
    beta=float(np.polyfit(np.log10(cn[up]),np.log10(cp[up]),1)[0]) if up.sum()>=3 else float('nan')
    return dict(scalar=scalar,N=N,T=T,PR_keff=float(pr),mp_edge=float(edge),eff_rank_mp=eff_mp,
                eff_rank_surr=eff_surr,beta_top=beta,alpha=alpha,
                top_eigs=[float(x) for x in ev[:12]],
                subsample=[(int(a),float(b),float(c)) for a,b,c in curve])

def ou_eq(m,T):
    x=np.zeros((m,T))
    for t in range(1,T): x[:,t]=0.7*x[:,t-1]+RNG.standard_normal(m)
    return x
def ou_driven(m,T,w=0.8):
    x=np.zeros((m,T)); Ad=-0.3*np.eye(m)
    for i in range(0,m-1,2): Ad[i,i+1]=-w; Ad[i+1,i]=w
    for t in range(1,T): x[:,t]=x[:,t-1]+Ad@x[:,t-1]+0.5*RNG.standard_normal(m)
    return x
def relaxation(m,T):
    tt=np.linspace(0,1,T); x=np.array([np.exp(-(k+1)*tt) for k in range(m)])*3
    return x+0.3*RNG.standard_normal((m,T))

def main():
    t0=time.time()
    LR,LT,VR=build_gas_cells()
    np.savez(f"{SCRATCH}/gal_gas_cells.npz", LR=LR, LT=LT, VR=VR)
    T=LR.shape[1]
    # (1) SATURATION
    print("\n=== (1) SATURATION (gas) ===", flush=True)
    sat={}
    for name,X in [("logrho",LR),("v_r",VR),("logT",LT)]:
        r=analyze_saturation(X,name); sat[name]=r
        print(f"  [{name}] N={r['N']} T={r['T']} PR/k_eff={r['PR_keff']:.2f} "
              f"eff_rank(MP)={r['eff_rank_mp']} eff_rank(surr)={r['eff_rank_surr']} "
              f"beta_top={r['beta_top']:.3f} alpha={r['alpha']:.3f}", flush=True)
        print("    curve: "+"  ".join(f"{n}:{m:.1f}" for n,m,_ in r['subsample']), flush=True)
    # (2a) mode circulation + calibrators
    print("\n=== (2a) MODE-CIRCULATION detailed balance (gas) ===", flush=True)
    cal={}
    for name,A in [("OU-equilibrium",ou_eq(4,T)),("OU-driven",ou_driven(4,T)),("relaxation",relaxation(4,T))]:
        pr,cs=db_modepairs(A); cal[name]=dict(pairs=pr,circ=cs)
        print(f"  cal {name:16s}: sum|omega|={cs['circ']:.3f} z={cs['z']:+.2f}", flush=True)
    modecirc={}
    for name,X in [("logrho",LR),("v_r",VR),("logT",LT)]:
        A=modes(X,4); pr,cs=db_modepairs(A); modecirc[name]=dict(pairs=pr,circ=cs)
        print(f"  gas [{name}] sum|omega|={cs['circ']:.3f} z={cs['z']:+.2f}  "
              +"  ".join(f"{k}:z{v['z']:+.1f}" for k,v in pr.items()), flush=True)
    # (2b) thermodynamic-plane circulation (the direct baryon-cycle signature)
    print("\n=== (2b) THERMODYNAMIC-PLANE circulation (baryon cycle) ===", flush=True)
    thermo={}
    thermo['logrho_logT_percell']=thermo_circulation(LR,LT)
    thermo['logrho_vr_percell']  =thermo_circulation(LR,VR)
    for k,v in thermo.items():
        print(f"  per-cell {k}: mean_omega={v['mean_omega']:+.4f} z={v['z']:+.2f} (ncells={v['ncells']})", flush=True)
    # global mass-weighted mean-state trajectory in (logrho,logT)
    gm_lr=np.nanmean(LR,axis=0); gm_lt=np.nanmean(LT,axis=0)
    a=(gm_lr-gm_lr.mean())/(gm_lr.std()+1e-12); b=(gm_lt-gm_lt.mean())/(gm_lt.std()+1e-12)
    gobs=omega(a,b); gnull=np.array([omega(phaserand(a),phaserand(b)) for _ in range(5000)])
    thermo['global_meanstate_logrho_logT']=dict(omega=float(gobs),
        z=float((gobs-gnull.mean())/(gnull.std()+1e-12)),
        traj_logrho=[float(x) for x in gm_lr], traj_logT=[float(x) for x in gm_lt])
    print(f"  GLOBAL mean-state (logrho,logT) loop: omega={gobs:+.4f} "
          f"z={thermo['global_meanstate_logrho_logT']['z']:+.2f}", flush=True)

    # verdicts.
    # CLEAN broken-DB evidence must come from CONFIGURATION-space planes: (logrho,logT)
    # pairs two thermodynamic STATE variables, so a phase LAG = a directed thermodynamic
    # loop = broken detailed balance. The (logrho, v_r) plane pairs a coordinate with a
    # VELOCITY: even a REVERSIBLE breathing oscillation (or one-way inflow) circulates
    # there, and the phase-randomized null cannot separate reversible from driven -> that
    # signal is CONFOUNDED and is reported but NOT used as broken-DB evidence.
    prim=sat['logrho']
    saturates=(prim['PR_keff']<0.5*prim['T']) and (prim['eff_rank_surr']<=12)
    z_config=max(abs(thermo['logrho_logT_percell']['z']),
                 abs(thermo['global_meanstate_logrho_logT']['z']),
                 abs(modecirc['logrho']['circ']['z']))
    z_posvel=abs(thermo['logrho_vr_percell']['z'])
    driven_z=abs(cal['OU-driven']['circ']['z'])
    if z_config>3:
        db_verdict=("BREAKS DETAILED BALANCE in a configuration-space plane: significant directed "
                    "thermodynamic loop -> SUSTAINED self-regulated NESS = COORDINATING, unlike the "
                    "collisionless stars. (TNG cooling+feedback is not automatically gamma*M.)")
    elif z_config>2:
        db_verdict=("MARGINAL configuration-space circulation (2<|z|<3): weak/ambiguous sustained-cycle "
                    "evidence at T=16.")
    else:
        db_verdict=("NO significant CONFIGURATION-SPACE circulation ((logrho,logT) z=%.1f, global (logrho,logT) "
                    "z=%.1f, mode-circulation z=%.1f, all <2, far below the driven-NESS ruler z=%.1f): no "
                    "cleanly detected sustained thermodynamic cycle. The one strong signal is (logrho,v_r) "
                    "z=%.1f, but that is a position-VELOCITY plane where reversible breathing / one-way "
                    "inflow circulate trivially (CONFOUNDED, not broken-DB evidence). NET: the gas is "
                    "low-rank but this test does NOT establish that the baryon cycle is a sustained "
                    "coordinating NESS distinguishable from one-way drift + reversible oscillation."
                    %(abs(thermo['logrho_logT_percell']['z']),
                      abs(thermo['global_meanstate_logrho_logT']['z']),
                      abs(modecirc['logrho']['circ']['z']), driven_z, z_posvel))
    thermo['logrho_vr_percell']['confounded']=("position-velocity plane: reversible breathing / one-way "
        "inflow also circulate here; null cannot separate reversible from driven -> NOT broken-DB evidence")
    print(f"\nSATURATION verdict (gas): {'LOW-RANK (saturates)' if saturates else 'HIGH-DIM'} "
          f"(PR={prim['PR_keff']:.1f}, T={prim['T']})")
    print(f"DETAILED-BALANCE verdict (gas): {db_verdict}", flush=True)

    out=dict(substrate="CAMELS IllustrisTNG L25n256 CV_0, main progenitor of subhalo 0 -- GAS (PartType0)",
             construction=("Eulerian disk-aligned 3D grid (+/-%g kpc/h, %d^3 cells) in the star-tracked "
                           "galaxy frame; cells x snapshots; scalars logrho / logT / v_r; halo gas read "
                           "via FOF-group offset (main progenitor by nearest center)."%(RGRID,NGRID)),
             snapshots=SNAPS, z_range=[2.3,0.0], T=int(T),
             saturation=sat, saturation_verdict=("LOW-RANK" if saturates else "HIGH-DIM"),
             mode_circulation=dict(calibration=cal, gas=modecirc),
             thermodynamic_circulation=thermo,
             detailed_balance_verdict=db_verdict,
             caveats=["TNG has cooling+feedback by construction -> some irreversibility guaranteed; "
                      "question is sustained CYCLE vs one-way depletion (the loop/circulation).",
                      "star-forming gas on TNG effective EOS -> cold-dense branch of (rho,T) is model-imposed.",
                      "T=26 snapshots is short; one simulated galaxy.",
                      "TNG-physics dissipation is NOT automatically the framework's gamma*M."],
             elapsed_sec=round(time.time()-t0,1))
    json.dump(out, open(f"{HERE}/spectral_results_galaxy_gas.json","w"), indent=1)
    print(f"\nwrote spectral_results_galaxy_gas.json ({out['elapsed_sec']}s)", flush=True)

if __name__=="__main__":
    main()
