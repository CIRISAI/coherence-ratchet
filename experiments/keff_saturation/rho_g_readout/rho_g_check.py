#!/usr/bin/env python3
"""
1/sqrt(L) global-correlation read-out check.

Prediction (coupled_model/SUMMARY.md sec 3): on any Gate-0 substrate whose
participation-ratio k_eff SATURATES at level L, the maintained global cross-unit
correlation should be rho_g ~ 1/sqrt(L), because the coupled two-level model's
saturation ceiling is exactly k_eff -> 1/rho_g^2.

Three observables per complete unit (all from the z-scored correlation matrix
C = ZZ^T/T, trace(C)=N, exactly the Gate-0 pipeline):
  L        = k_eff = participation ratio (sum lam)^2 / sum lam^2
  lam1     = top ("global") eigenvalue
  f        = lam1 / N          -- variance fraction of the global mode
  rho_spec = (lam1-1)/(N-1)    -- mean off-diagonal correlation IF top mode is
             the uniform mode (equicorrelation inversion; = rho_g in the toy)
  rho_dir  = actual mean off-diagonal correlation of C (raw data only)

Checks:
  (P) rho_g   ~ 1/sqrt(L)          (the prediction; rho_g = rho_dir where we have it)
  (S) f       ~ 1/sqrt(L)  <=>  L ~ 1/f^2   (spectral form; the toy gives 1/rho_g^2)
      vs the task-note's L ~ 1/f (reported too, to show which the data picks)

rho_dir is computed WITHOUT forming C for large N via
  sum_ij C_ij = || sum_i Z_i ||^2 / T,  mean_offdiag = (that - N)/(N(N-1)).
"""
import numpy as np, pandas as pd, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)


def corr_from_X(X):
    """X = N x T raw -> (eigs desc, N, T, rho_direct). z-score per unit."""
    N, T = X.shape
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    # rho_direct without forming NxN when N large: 1^T C 1 = ||sum_i Z_i||^2 / T
    s = Z.sum(0)                       # length-T
    ones_C_ones = float(s @ s) / T     # = sum_ij C_ij
    rho_dir = (ones_C_ones - N) / (N * (N - 1))
    if N <= 4000:
        C = (Z @ Z.T) / T
        ev = np.clip(np.linalg.eigvalsh(C)[::-1], 0, None)
    else:                              # T-space Gram (exact nonzero spectrum)
        G = (Z.T @ Z) / T              # T x T
        ev = np.clip(np.linalg.eigvalsh(G)[::-1], 0, None)
    return ev, N, T, rho_dir


def pr(ev):
    return float((ev.sum() ** 2) / (ev ** 2).sum())


def summarize(ev, N, rho_dir=None):
    L = pr(ev)
    lam1 = float(ev[0])
    f = lam1 / N
    rho_spec = (lam1 - 1) / (N - 1)
    return dict(L=L, lam1=lam1, N=int(N), f=f, rho_spec=rho_spec,
                rho_dir=(None if rho_dir is None else float(rho_dir)),
                pred_1_over_sqrtL=1.0 / np.sqrt(L),
                inv_f=1.0 / f, inv_f2=1.0 / f ** 2)


records = {}   # substrate -> list of per-unit dicts

# ---------- C. elegans (raw) ----------
cel = os.path.join(BASE, "../structural_series/corridor_dynamics/celegans/data/"
                         "kato2015_whole_brain.parquet")
if os.path.exists(cel):
    df = pd.read_parquet(cel)
    units = []
    for w in sorted(df.worm.unique()):
        sub = df[df.worm == w]
        traces = [np.asarray(r["calcium_data"], float) for _, r in sub.iterrows()]
        Lmin = min(len(t) for t in traces)
        X = np.vstack([t[:Lmin] for t in traces])
        good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
        X = X[good]
        if X.shape[0] < 20:
            continue
        ev, N, T, rd = corr_from_X(X)
        units.append(summarize(ev, N, rd) | dict(unit=w))
    records["celegans"] = units
    print(f"celegans: {len(units)} worms")

# ---------- Finance S&P-100 and full market (raw) ----------
for name, pq in [("finance_sp100", "finance_returns_cache.parquet"),
                 ("finance_fullmkt", "fullmarket_returns.parquet")]:
    p = os.path.join(BASE, pq)
    if not os.path.exists(p):
        continue
    R = pd.read_parquet(p).dropna(axis=1, how="any")
    X = R.to_numpy().T                       # units(stocks) x time(days)
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-12)
    X = X[good]
    ev, N, T, rd = corr_from_X(X)
    records[name] = [summarize(ev, N, rd) | dict(unit=name, T=int(T))]
    print(f"{name}: N={N} T={T}")

# ---------- Stored-spectra substrates (top_eigs + PR + N) ----------
def from_stored(unitrec):
    te = unitrec.get("top_eigs")
    N = unitrec.get("N")
    L = unitrec.get("PR")
    if not te or not N:
        return None
    lam1 = float(te[0])
    f = lam1 / N
    return dict(L=float(L), lam1=lam1, N=int(N), f=f,
                rho_spec=(lam1 - 1) / (N - 1), rho_dir=None,
                pred_1_over_sqrtL=1.0 / np.sqrt(float(L)),
                inv_f=1.0 / f, inv_f2=1.0 / f ** 2)

# Drosophila (per fly-trial)
dro = json.load(open(os.path.join(BASE, "spectral_results_drosophila.json")))
records["drosophila"] = [r for r in (from_stored(u) for u in dro) if r]

# fMRI (per subject, roi_as_units)
tf = json.load(open(os.path.join(BASE, "spectral_results_tcga_fmri.json")))
records["fmri"] = [r for r in (from_stored(u) for u in tf["fmri"]["per_subject"]) if r]
# TCGA (per cancer, genes_as_units -- huge N; f/rho_spec still defined)
records["tcga"] = [r for r in (from_stored(u) for u in tf["tcga"]["per_cancer"]) if r]

# Zebrafish (single complete brain) -- stored top_eigs + PR_full_N
zf = json.load(open(os.path.join(BASE, "spectral_results_zebrafish.json")))
lam1 = float(zf["top_eigs"][0]); N = int(zf["N_neurons"])
for Lname, L in [("PR_full_N", zf["PR_full_N"]),
                 ("noise_free_keff", zf["cv"]["noise_free_keff"])]:
    records.setdefault("zebrafish", []).append(dict(
        L=float(L), lam1=lam1, N=N, f=lam1 / N, rho_spec=(lam1 - 1) / (N - 1),
        rho_dir=None, pred_1_over_sqrtL=1.0 / np.sqrt(float(L)),
        inv_f=1.0 / (lam1 / N), inv_f2=1.0 / (lam1 / N) ** 2, unit=Lname))

# ---------- aggregate + report ----------
def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None

print("\n" + "=" * 96)
print(f"{'substrate':16s} {'nU':>3s} {'L(k_eff)':>9s} {'1/sqrtL':>8s} "
      f"{'rho_dir':>8s} {'rho_spec':>9s} {'f':>7s} {'1/f^2':>7s} {'1/f':>6s} "
      f"{'rho/pred':>8s} {'f/pred':>7s}")
print("-" * 96)
agg = {}
for sub, units in records.items():
    L = med([u["L"] for u in units])
    pred = 1.0 / np.sqrt(L)
    rho_dir = med([u["rho_dir"] for u in units])
    rho_spec = med([u["rho_spec"] for u in units])
    f = med([u["f"] for u in units])
    invf2 = med([u["inv_f2"] for u in units])
    invf = med([u["inv_f"] for u in units])
    rho_use = rho_dir if rho_dir is not None else rho_spec
    agg[sub] = dict(n_units=len(units), L=L, pred_1_over_sqrtL=pred,
                    rho_dir=rho_dir, rho_spec=rho_spec, f=f,
                    inv_f2=invf2, inv_f=invf,
                    rho_over_pred=rho_use / pred, f_over_pred=f / pred,
                    L_over_inv_f2=L / invf2, L_over_inv_f=L / invf)
    print(f"{sub:16s} {len(units):3d} {L:9.2f} {pred:8.3f} "
          f"{('%.3f'%rho_dir) if rho_dir is not None else '   -  ':>8s} "
          f"{rho_spec:9.3f} {f:7.3f} {invf2:7.2f} {invf:6.2f} "
          f"{rho_use/pred:8.2f} {f/pred:7.2f}")

json.dump({"per_substrate": agg,
           "records": {k: v for k, v in records.items()}},
          open(os.path.join(HERE, "rho_g_results.json"), "w"), indent=1)
print("\nwrote rho_g_results.json")
print("\nCheck legend:  rho/pred and f/pred should be ~1 if rho_g,f ~ 1/sqrt(L).")
print("L_over_inv_f2 ~1 => k_eff ~ 1/f^2 (toy form); L_over_inv_f ~1 => k_eff ~ 1/f (task-note form).")
for sub, a in agg.items():
    print(f"  {sub:16s} L/(1/f^2)={a['L_over_inv_f2']:.2f}  L/(1/f)={a['L_over_inv_f']:.2f}")
