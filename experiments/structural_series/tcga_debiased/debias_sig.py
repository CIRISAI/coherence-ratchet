#!/usr/bin/env python3
"""
debias_sig.py — significance gate for the DEBIASED TCGA tumour drift.

The raw run (data_tcga/RESULT.md) reports 201/201 significant pathway-shifts
chaos-ward, where "significant" = non-overlapping bootstrap 95% CI of raw rho_t
vs raw rho_n. To compare the debiased tumour drift on the SAME footing, this
re-runs the bootstrap on the DEBIASED rho: for each pathway, B bootstrap
resamples of the samples within each group, debiased rho per resample (raw rho
of the resample minus the same per-pathway permutation floor), and a pathway is
"significant" if the debiased-rho 95% CIs of the two groups do not overlap.

Incremental flush to results_debiased_sig.json. Real on-disk TCGA data only.
"""
import json
import time
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data_tcga" / "data"
OUT = HERE / "results_debiased_sig.json"

MIN_GENES = 10
N_SURROGATE = 20
B = 500               # bootstrap resamples, matches 02_compute_rho.py
SEED = 17


def load_hallmark(p):
    sets = {}
    for line in pathlib.Path(p).read_text().strip().split("\n"):
        parts = line.split("\t")
        sets[parts[0]] = parts[2:]
    return sets


def mean_abs_corr(M):
    if M.shape[0] < 2 or M.shape[1] < 3:
        return np.nan
    var = M.var(axis=1)
    keep = var > 1e-10
    if keep.sum() < 2:
        return np.nan
    C = np.corrcoef(M[keep])
    if C.ndim == 0 or np.isnan(C).all():
        return np.nan
    iu = np.triu_indices_from(C, k=1)
    return float(np.nanmean(np.abs(C[iu])))


def permutation_floor(M, rng):
    floors = []
    n_samp = M.shape[1]
    for _ in range(N_SURROGATE):
        Ms = np.empty_like(M)
        for g in range(M.shape[0]):
            Ms[g] = M[g, rng.permutation(n_samp)]
        v = mean_abs_corr(Ms)
        if not np.isnan(v):
            floors.append(v)
    return float(np.mean(floors)) if floors else np.nan


def bootstrap_deb(M, floor, rng):
    """Bootstrap debiased rho: per resample, sqrt(max(raw^2 - floor^2, 0))."""
    n = M.shape[1]
    out = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        raw = mean_abs_corr(M[:, idx])
        out[b] = np.sqrt(max(raw ** 2 - floor ** 2, 0.0)) \
            if not np.isnan(raw) else np.nan
    return out


def main():
    t0 = time.time()
    sets = load_hallmark(DATA / "h.all.v2024.1.Hs.symbols.gmt")
    summary = json.loads((DATA / "fetch_summary.json").read_text())
    rng = np.random.default_rng(SEED)

    all_results = {}
    if OUT.exists():
        try:
            all_results = json.loads(OUT.read_text())
            print(f"Resuming: {len(all_results)} cancers done")
        except Exception:
            all_results = {}

    for cancer in summary:
        if cancer in all_results:
            print(f"{cancer}: already done — skip")
            continue
        t1 = time.time()
        expr_path = DATA / f"{cancer}_expr.tsv.gz"
        if not expr_path.exists():
            print(f"{cancer}: no matrix — skip")
            continue
        print(f"=== {cancer} ===")
        df = pd.read_csv(expr_path, sep="\t", index_col=0)
        cols = list(df.columns)
        tcols = [c for c in cols if c.split("|")[1] == "01"]
        ncols = [c for c in cols if c.split("|")[1] == "11"]
        n_t, n_n = len(tcols), len(ncols)
        insufficient = (n_n < 20 or n_t < 100)
        T = df[tcols].values
        N = df[ncols].values
        gene_index = df.index
        gset = set(gene_index)

        res = {"n_tumor": n_t, "n_normal": n_n,
               "insufficient": bool(insufficient), "pathways": {}}
        for p, genes in sets.items():
            gs = [g for g in genes if g in gset]
            if len(gs) < MIN_GENES:
                continue
            idx = gene_index.get_indexer(gs)
            idx = idx[idx >= 0]
            Tsub, Nsub = T[idx, :], N[idx, :]
            fl_t = permutation_floor(Tsub, rng)
            fl_n = permutation_floor(Nsub, rng)
            if np.isnan(fl_t) or np.isnan(fl_n):
                continue
            bt = bootstrap_deb(Tsub, fl_t, rng)
            bn = bootstrap_deb(Nsub, fl_n, rng)
            ci_t = (float(np.nanpercentile(bt, 2.5)),
                    float(np.nanpercentile(bt, 97.5)))
            ci_n = (float(np.nanpercentile(bn, 2.5)),
                    float(np.nanpercentile(bn, 97.5)))
            non_overlap = (ci_t[0] > ci_n[1]) or (ci_n[0] > ci_t[1])
            rho_t = float(np.nanmedian(bt))
            rho_n = float(np.nanmedian(bn))
            res["pathways"][p] = {
                "rho_t_deb": rho_t, "rho_n_deb": rho_n,
                "ci_tumor": ci_t, "ci_normal": ci_n,
                "delta_deb": rho_t - rho_n,
                "non_overlap_95": bool(non_overlap),
            }
        all_results[cancer] = res
        nsig = sum(1 for x in res["pathways"].values()
                   if x["non_overlap_95"])
        print(f"  {len(res['pathways'])} pathways, {nsig} significant  "
              f"[{time.time()-t1:.1f}s]")
        OUT.write_text(json.dumps(all_results, indent=2))

    print(f"\nDone. Wrote {OUT}  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
