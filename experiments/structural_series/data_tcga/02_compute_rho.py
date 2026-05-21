#!/usr/bin/env python3
"""
02_compute_rho.py — within-rung |rho| per (cancer x pathway x sample-type).

For each cancer matrix from 01_fetch_gdc.py:
  - split columns into tumor (|01) and normal (|11);
  - per Hallmark pathway, within-rung |rho| = mean |Pearson| over
    gene-gene pairs in the pathway across the samples of one group;
  - bootstrap 95% CI (B=500) by resampling samples within group.

Construction identical to experiments/noncorr_cancer/02_compute_rho.py.
"""
import json, time, pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

B = 500
MIN_GENES = 10
MIN_NORMAL = 20
MIN_TUMOR = 100
SEED = 17


def load_hallmark(p):
    sets = {}
    for line in pathlib.Path(p).read_text().strip().split("\n"):
        parts = line.split("\t")
        sets[parts[0]] = parts[2:]
    return sets


def mean_abs_corr(M):
    """Mean |Pearson| over the upper triangle of corrcoef(M); M is
    variables (genes) x observations (samples)."""
    if M.shape[0] < 2 or M.shape[1] < 3:
        return np.nan
    var = M.var(axis=1)
    keep = var > 1e-10
    if keep.sum() < 2:
        return np.nan
    M = M[keep]
    C = np.corrcoef(M)
    if C.ndim == 0 or np.isnan(C).all():
        return np.nan
    iu = np.triu_indices_from(C, k=1)
    return float(np.nanmean(np.abs(C[iu])))


def bootstrap_rho(M, B, rng):
    n = M.shape[1]
    out = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        out[b] = mean_abs_corr(M[:, idx])
    return out


def main():
    t0 = time.time()
    sets = load_hallmark(DATA / "h.all.v2024.1.Hs.symbols.gmt")
    print(f"Loaded {len(sets)} Hallmark pathways")
    summary = json.loads((DATA / "fetch_summary.json").read_text())
    rng = np.random.default_rng(SEED)

    all_results = {}
    for cancer in summary:
        t1 = time.time()
        expr_path = DATA / f"{cancer}_expr.tsv.gz"
        if not expr_path.exists():
            print(f"\n{cancer}: no matrix; skip")
            continue
        print(f"\n=== {cancer} ===")
        df = pd.read_csv(expr_path, sep="\t", index_col=0)
        cols = list(df.columns)
        tcols = [c for c in cols if c.split("|")[1] == "01"]
        ncols = [c for c in cols if c.split("|")[1] == "11"]
        n_t, n_n = len(tcols), len(ncols)
        print(f"  tumor n={n_t}  normal n={n_n}")
        insufficient = (n_n < MIN_NORMAL or n_t < MIN_TUMOR)
        if insufficient:
            print(f"  below pre-reg minimum (>={MIN_NORMAL} normal, "
                  f">={MIN_TUMOR} tumor) -- recorded, flagged INSUFFICIENT")

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
            rho_t = mean_abs_corr(Tsub)
            rho_n = mean_abs_corr(Nsub)
            bt = bootstrap_rho(Tsub, B, rng)
            bn = bootstrap_rho(Nsub, B, rng)
            ci_t = (float(np.nanpercentile(bt, 2.5)),
                    float(np.nanpercentile(bt, 97.5)))
            ci_n = (float(np.nanpercentile(bn, 2.5)),
                    float(np.nanpercentile(bn, 97.5)))
            non_overlap = (ci_t[0] > ci_n[1]) or (ci_n[0] > ci_t[1])
            res["pathways"][p] = {
                "n_genes_in_pathway": len(genes),
                "n_genes_used": int(len(idx)),
                "rho_tumor": rho_t, "rho_normal": rho_n,
                "delta": float(rho_t - rho_n),
                "ci_tumor": ci_t, "ci_normal": ci_n,
                "non_overlap_95": bool(non_overlap),
            }
        all_results[cancer] = res
        print(f"  {len(res['pathways'])} pathways  [{time.time()-t1:.1f}s]")

    out = RESULTS / "rho_by_cancer_pathway.json"
    out.write_text(json.dumps(all_results, indent=2))
    print(f"\nWrote {out}  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
