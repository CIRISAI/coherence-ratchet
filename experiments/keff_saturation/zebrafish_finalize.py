#!/usr/bin/env python3
"""
Lean finalizer for the ZAPBench complete-brain test: the two checks the agent's
full-N runs kept stalling on. Reuses spectral_zebrafish.py's core + cached memmap.

(1) STIMULUS CONFOUND: saturation curve (PR vs N' up to full N) WITHIN each of the
    3 longest single visual conditions. If PR still saturates at a similar level
    with between-condition drive removed, the low-rank is INTRINSIC.
(2) CV-alpha on a 15k-neuron random subsample per condition (NOT full N -> tractable;
    alpha is scale-free so a subsample suffices), few surrogates.
"""
import json, os, time
import numpy as np
import spectral_zebrafish as sz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "spectral_results_zebrafish_condition.json")
OFFSETS = (0, 649, 2422, 3078, 3735, 5047, 5638, 6623, 7279, 7879)
NAMES = ("gain","dots","flash","taxis","turning","position","cond6","cond7","cond8")
PAD = 1
CVSUB = 15000   # neuron subsample for CV-alpha (tractable; alpha is scale-free)

def main():
    t0 = time.time()
    X = np.memmap(sz.MEMMAP, dtype=np.float32, mode="r", shape=(sz.T_FULL, sz.N_FULL))
    Xr = np.asarray(X, np.float32)
    good = np.isfinite(Xr).all(0) & (Xr.std(0) > 1e-9)
    conds = [(i, NAMES[i], OFFSETS[i]+PAD, OFFSETS[i+1]-PAD, OFFSETS[i+1]-OFFSETS[i]-2*PAD)
             for i in range(len(OFFSETS)-1)]
    conds.sort(key=lambda c: -c[4])
    chosen = conds[:3]
    print("longest single conditions (idx,name,T):", [(c[0],c[1],c[4]) for c in chosen], flush=True)

    out = dict(dataset="ZAPBench whole-brain zebrafish — single-condition stimulus control",
               note="within-condition saturation removes between-condition shared drive; "
                    "CV-alpha on 15k-neuron subsample",
               full_recording=dict(PR_full=34.19, beta=-0.0015, eff_rank_surr=10,
                                    note="whole-recording reference"),
               conditions=[], status="running")
    json.dump(out, open(OUT,"w"), indent=1)

    rng = np.random.default_rng(10)
    for idx, name, a, b, L in chosen:
        print(f"\n=== condition {idx} '{name}': frames [{a},{b}) T={L} ===", flush=True)
        Zc = sz.zscore_cols(Xr[a:b][:, good].astype(np.float64)).astype(np.float32)
        N = Zc.shape[1]
        sizes = [s for s in [50,100,200,500,1000,2000,4000,8000,16000,32000,50000,N] if s <= N]
        ndraw = lambda n: 1 if n>=32000 else (2 if n>=8000 else (3 if n>=2000 else 6))
        curve = sz.subsample_pr(Zc, sizes, np.random.default_rng(10), ndraw)
        cn = np.array([c[0] for c in curve], float); cp = np.array([c[1] for c in curve])
        up = cn >= 5000
        beta = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]),1)[0]) if up.sum()>=2 else float("nan")
        pr_full = float(cp[-1])
        print(f"  saturation: PR(full N={N})={pr_full:.2f}  beta(>=5000)={beta:.4f}", flush=True)
        # CV-alpha on a 15k subsample
        sub = np.sort(rng.choice(N, min(CVSUB, N), replace=False))
        try:
            cvr = sz.cv_readouts_fullN(Zc[:, sub], np.random.default_rng(7), n_surr=3)
            cvline = dict(N_sub=len(sub), n_cv_pos=cvr["n_cv_pos"],
                          noise_free_keff=cvr["noise_free_keff"],
                          n_above_surr=cvr["n_above_surr"], alpha=cvr["alpha"])
            print(f"  CV(15k): n_cv_pos={cvr['n_cv_pos']}  nf_keff={cvr['noise_free_keff']:.2f}  "
                  f"n>surr={cvr['n_above_surr']}  alpha={cvr['alpha']:.3f}", flush=True)
        except Exception as e:
            cvline = dict(error=str(e)[:200]); print("  CV error:", e, flush=True)
        out["conditions"].append(dict(cond_idx=idx, name=name, frames=[a,b], T=L, N=N,
                                      saturation_curve=[dict(Np=c[0],PR=c[1],draws=c[3]) for c in curve],
                                      beta_upper=beta, PR_full_N=pr_full, cv=cvline))
        json.dump(out, open(OUT,"w"), indent=1)
    out["status"]="done"; out["runtime_s"]=round(time.time()-t0,1)
    json.dump(out, open(OUT,"w"), indent=1)
    print(f"\nwrote {OUT} ({out['runtime_s']}s)", flush=True)

if __name__ == "__main__":
    main()
