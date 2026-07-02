#!/usr/bin/env python3
"""
POSITIVE CONTROL for the bound-vs-coordinating (broken-detailed-balance) detector.

The galaxy (bound) read detailed-balance-SATISFYING. That reading only means
something if a KNOWN COORDINATING system reads detailed-balance-BREAKING on the
identical estimator. Prediction (Lynn et al. 2021 PNAS found broken DB in human
brain activity): C. elegans and zebrafish whole-brain — actively-maintained
coordinating units — should show significant net circulation in their top
collective modes, like the driven-NESS calibrator and UNLIKE the galaxy.

Reuses the IDENTICAL estimator from spectral_galaxy_db.py (omega circulation,
phase-randomized null, OU calibrators). Same 2-axis logic: saturation says
low-rank; detailed balance says bound-vs-coordinating.
"""
import json, os, numpy as np, pandas as pd
import spectral_galaxy_db as gdb   # identical estimator

HERE = os.path.dirname(os.path.abspath(__file__))
CEL = os.path.join(HERE, "../structural_series/corridor_dynamics/celegans/data/kato2015_whole_brain.parquet")

def worm_matrix(df, worm):
    sub = df[df.worm == worm]; traces = [np.asarray(r["calcium_data"], float) for _, r in sub.iterrows()]
    L = min(len(t) for t in traces); X = np.vstack([t[:L] for t in traces])
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
    return X[good]

def run_system(name, mats, T_cal):
    # calibrators at this system's T
    print(f"\n=== {name}: calibration at T={T_cal} ===")
    cal = {}
    for cname, gen in [("OU-equilibrium(reversible)", gdb.ou_equilibrium),
                       ("OU-driven(NESS,breaks DB)", gdb.ou_driven),
                       ("relaxation(transient)", gdb.relaxation)]:
        A = gen(4, T_cal); pr, cs = gdb.db_stats(A)
        cal[cname] = cs
        print(f"  {cname:28s} sum|omega|={cs['circulation_sum']:.3f}  z={cs['z']:+.2f}")
    print(f"  (equilibrium z~0; DRIVEN z>>2; relaxation modest)")
    recs = []
    for i, (label, X) in enumerate(mats):
        A = gdb.modes(X, 4)                       # top-4 collective mode trajectories a_k(t)
        pr, cs = gdb.db_stats(A)
        recs.append(dict(unit=label, N=int(X.shape[0]), T=int(X.shape[1]),
                         circ_sum=cs['circulation_sum'], z=cs['z'],
                         pairs={k: dict(omega=v['omega'], z=v['z']) for k, v in pr.items()}))
        print(f"  [{label:8s}] sum|omega|={cs['circulation_sum']:.3f}  z={cs['z']:+.2f}  "
              + " ".join(f"{k}:z{v['z']:+.1f}" for k, v in pr.items()))
    zs = np.array([r['z'] for r in recs])
    med = float(np.median(zs)); frac_sig = float((zs > 2).mean())
    driven_z = cal["OU-driven(NESS,breaks DB)"]['z']
    verdict = ("BREAKS DETAILED BALANCE -> COORDINATING (like driven-NESS, unlike the bound galaxy)"
               if med > 2 else "detailed-balance-satisfying (bound-like)" if med < 1 else "MARGINAL")
    print(f"  --> median z={med:+.2f} across {len(recs)} units; {100*frac_sig:.0f}% with z>2; "
          f"driven ruler z={driven_z:+.2f}")
    print(f"  VERDICT: {verdict}")
    return dict(system=name, T_cal=T_cal, calibration=cal, units=recs,
                median_z=med, frac_z_gt2=frac_sig, verdict=verdict)

def main():
    out = {}
    # C. elegans
    df = pd.read_parquet(CEL)
    worms = sorted(df.worm.unique(), key=lambda w: -df[df.worm == w].neuron.nunique())
    mats = []
    for w in worms:
        X = worm_matrix(df, w)
        if X.shape[0] >= 20 and X.shape[1] >= 500: mats.append((w, X))
    T_cal = int(np.median([X.shape[1] for _, X in mats]))
    out["celegans"] = run_system("C. elegans whole-brain (coordinating?)", mats, T_cal)

    # zebrafish (memmap; top modes over full time, subsample neurons for speed)
    try:
        import spectral_zebrafish as sz
        X = np.memmap(sz.MEMMAP, dtype=np.float32, mode="r", shape=(sz.T_FULL, sz.N_FULL))
        Xr = np.asarray(X, np.float32)
        good = np.isfinite(Xr).all(0) & (Xr.std(0) > 1e-9)
        rng = np.random.default_rng(0)
        cols = np.sort(rng.choice(np.where(good)[0], 8000, replace=False))
        Zt = Xr[:, cols].T                                    # neurons x time
        out["zebrafish"] = run_system("zebrafish whole-brain (coordinating?)", [("zf_whole", Zt)], sz.T_FULL)
    except Exception as e:
        print("zebrafish DB skipped:", str(e)[:150]); out["zebrafish"] = {"error": str(e)[:200]}

    json.dump(out, open(os.path.join(HERE, "db_positive_control_results.json"), "w"), indent=1)
    print("\nwrote db_positive_control_results.json")

if __name__ == "__main__":
    main()
