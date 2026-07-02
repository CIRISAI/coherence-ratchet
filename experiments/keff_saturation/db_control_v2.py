#!/usr/bin/env python3
"""Positive control v2 for the bound-vs-coordinating detector, using the
winding-based irreversibility estimator (entropy_production.py). Known
coordinating brains (C. elegans cyclic attractor, zebrafish) should now BREAK
detailed balance (z>>2); the calibrators set the null ceiling."""
import json, os, numpy as np, pandas as pd
import entropy_production as ep

HERE=os.path.dirname(os.path.abspath(__file__))
CEL=os.path.join(HERE,"../structural_series/corridor_dynamics/celegans/data/kato2015_whole_brain.parquet")

def worm_matrix(df,w):
    sub=df[df.worm==w]; tr=[np.asarray(r["calcium_data"],float) for _,r in sub.iterrows()]
    L=min(len(t) for t in tr); X=np.vstack([t[:L] for t in tr])
    g=np.isfinite(X).all(1)&(X.std(1)>1e-9); return X[g]

out={"estimator":"winding-rate irreversibility (block-bootstrap z), max over top-4 mode pairs"}
# null ceiling from calibrators
cal={}
for name,gen in [("OU-equilibrium",ep.ou_equilibrium),("relaxation",ep.relaxation),
                 ("limit-cycle",ep.limit_cycle),("OU-driven",ep.ou_driven)]:
    r=ep.entropy_production(gen(2500)); cal[name]=round(r["z"],2)
print("calibrators (null ceiling ~1.5; cycles >>2):",cal); out["calibration"]=cal

# C. elegans
df=pd.read_parquet(CEL)
worms=sorted(df.worm.unique(),key=lambda w:-df[df.worm==w].neuron.nunique())
cz=[]
for w in worms:
    X=worm_matrix(df,w)
    if X.shape[0]<20 or X.shape[1]<500: continue
    r=ep.irreversibility_from_units(X,k=4); cz.append((w,r["z"],r["pair"]))
    print(f"  {w:8s} z={r['z']:+.2f} pair={r['pair']} T={r['T']}")
zc=np.array([z for _,z,_ in cz])
out["celegans"]=dict(units=[dict(worm=w,z=z,pair=list(p)) for w,z,p in cz],
    median_abs_z=float(np.median(np.abs(zc))),frac_abs_z_gt2=float((np.abs(zc)>2).mean()),frac_abs_z_gt3=float((np.abs(zc)>3).mean()))
az=np.abs(zc)
print(f"C. elegans: median|z|={np.median(az):.2f}  |z|>2:{100*(az>2).mean():.0f}%  |z|>3:{100*(az>3).mean():.0f}%  (null ceiling ~1.5)")

# zebrafish
try:
    import spectral_zebrafish as sz
    X=np.memmap(sz.MEMMAP,dtype=np.float32,mode="r",shape=(sz.T_FULL,sz.N_FULL))
    Xr=np.asarray(X,np.float32); good=np.isfinite(Xr).all(0)&(Xr.std(0)>1e-9)
    rng=np.random.default_rng(0); cols=np.sort(rng.choice(np.where(good)[0],8000,replace=False))
    r=ep.irreversibility_from_units(Xr[:,cols].T,k=4)
    out["zebrafish"]=dict(z=r["z"],pair=list(r["pair"]),T=r["T"])
    print(f"zebrafish whole-brain: z={r['z']:+.2f} pair={r['pair']}")
except Exception as e:
    print("zebrafish skipped:",str(e)[:120]); out["zebrafish"]={"error":str(e)[:150]}

verdict=("REAL but WEAK DB-breaking (median|z|>2, above null ~1.5, but far below clean-cycle ~16; calcium-limited)"
    if np.median(np.abs(zc))>2 else "still weak/marginal")
out["verdict"]=verdict; print("VERDICT:",verdict)
json.dump(out,open(os.path.join(HERE,"db_control_v2_results.json"),"w"),indent=1)
print("wrote db_control_v2_results.json")
