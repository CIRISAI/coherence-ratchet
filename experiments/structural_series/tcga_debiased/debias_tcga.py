#!/usr/bin/env python3
"""
debias_tcga.py — debiased within-rung rho for the TCGA cellular substrate.

Owed by band_calibration/RESULTS.md, pre-registered in this directory's
PREREGISTRATION.md. The on-disk TCGA rho (data_tcga/02_compute_rho.py) is raw
mean_abs_corr with no surrogate-floor subtraction. Every other structural-series
substrate has debiased rho (sqrt(rho_raw^2 - floor^2), floored at 0). This run
debiases TCGA so it is comparable with the debiased biological cluster.

THE SURROGATE (pre-registered, stated explicitly):
  TCGA Hallmark-pathway rho is computed over samples x pathways, NOT a time
  series. Phase randomization (the fMRI/EEG floor) does not apply -- TCGA
  samples are not temporally ordered. The correct null is a per-pathway
  PERMUTATION surrogate: independently permute each gene's values across
  samples, which destroys cross-gene correlation while exactly preserving each
  gene's marginal distribution. The floor is the mean rho over such surrogates;
  rho_deb = sqrt(max(rho_raw^2 - floor^2, 0)).

  (Within a Hallmark pathway, the "constituents" whose correlation builds rho
  are the genes; the surrogate independently shuffles each gene-column across
  samples, exactly the analogue of the per-series shuffle.)

k_eff: canonical participation-ratio of the gene-gene correlation matrix
eigenvalues, matching data_fmri/fmri_corridor.py.

Incremental output: per-cancer results flushed to results_debiased.json as
computed, so a wedge/restart leaves recoverable partial work.

Real TCGA data on disk only (data/*_expr.tsv.gz, fetched from the public NCI
GDC API by 01_fetch_gdc.py). No synthetic data.
"""
import json
import time
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data_tcga" / "data"
OUT = HERE / "results_debiased.json"

MIN_GENES = 10        # matches 02_compute_rho.py
N_SURROGATE = 20      # per-pathway permutation surrogate draws for the floor
SEED = 17             # matches 02_compute_rho.py


def load_hallmark(p):
    sets = {}
    for line in pathlib.Path(p).read_text().strip().split("\n"):
        parts = line.split("\t")
        sets[parts[0]] = parts[2:]
    return sets


def corr_matrix(M):
    """M is genes x samples. Returns the gene-gene Pearson matrix over the
    kept (non-constant) genes, or None if fewer than 2 genes survive."""
    if M.shape[0] < 2 or M.shape[1] < 3:
        return None
    var = M.var(axis=1)
    keep = var > 1e-10
    if keep.sum() < 2:
        return None
    C = np.corrcoef(M[keep])
    if C.ndim == 0 or np.isnan(C).all():
        return None
    return C


def mean_abs_corr_from_C(C):
    iu = np.triu_indices_from(C, k=1)
    return float(np.nanmean(np.abs(C[iu])))


def participation_ratio(C):
    """Canonical k_eff: participation ratio of the correlation-matrix
    eigenvalues (sum(ev)^2 / sum(ev^2)). Matches fmri_corridor.py."""
    ev = np.linalg.eigvalsh(C)
    ev = ev[ev > 1e-9]
    if ev.size == 0:
        return float("nan")
    return float((ev.sum() ** 2) / (ev ** 2).sum())


def permutation_floor(M, rng, n_surrogate=N_SURROGATE):
    """Per-pathway permutation surrogate: independently permute each gene's
    values across samples. Destroys cross-gene correlation, exactly preserves
    each gene's marginal. Returns mean rho over surrogates."""
    floors = []
    n_samp = M.shape[1]
    for _ in range(n_surrogate):
        Ms = np.empty_like(M)
        for g in range(M.shape[0]):
            Ms[g] = M[g, rng.permutation(n_samp)]
        Cs = corr_matrix(Ms)
        if Cs is not None:
            floors.append(mean_abs_corr_from_C(Cs))
    return float(np.mean(floors)) if floors else float("nan")


def debias_group(M, rng):
    """M: genes x samples for one sample-type group. Returns dict with
    rho_raw, floor, rho_deb, k_eff (participation ratio), n_genes_used."""
    C = corr_matrix(M)
    if C is None:
        return None
    rho_raw = mean_abs_corr_from_C(C)
    floor = permutation_floor(M, rng)
    rho_deb = float(np.sqrt(max(rho_raw ** 2 - floor ** 2, 0.0)))
    k_eff = participation_ratio(C)
    return {
        "rho_raw": rho_raw,
        "floor": floor,
        "rho_deb": rho_deb,
        "k_eff_pr": k_eff,
        "n_genes_used": int(C.shape[0]),
    }


def main():
    t0 = time.time()
    sets = load_hallmark(DATA / "h.all.v2024.1.Hs.symbols.gmt")
    print(f"Loaded {len(sets)} Hallmark pathways")
    summary = json.loads((DATA / "fetch_summary.json").read_text())
    rng = np.random.default_rng(SEED)

    # incremental: reload any partial result so a restart resumes
    all_results = {}
    if OUT.exists():
        try:
            all_results = json.loads(OUT.read_text())
            print(f"Resuming: {len(all_results)} cancers already done")
        except Exception:
            all_results = {}

    for cancer in summary:
        if cancer in all_results:
            print(f"\n{cancer}: already in results — skip")
            continue
        t1 = time.time()
        expr_path = DATA / f"{cancer}_expr.tsv.gz"
        if not expr_path.exists():
            print(f"\n{cancer}: no matrix on disk — skip")
            continue
        print(f"\n=== {cancer} ===")
        df = pd.read_csv(expr_path, sep="\t", index_col=0)
        cols = list(df.columns)
        tcols = [c for c in cols if c.split("|")[1] == "01"]
        ncols = [c for c in cols if c.split("|")[1] == "11"]
        n_t, n_n = len(tcols), len(ncols)
        insufficient = (n_n < 20 or n_t < 100)
        print(f"  tumor n={n_t}  normal n={n_n}  insufficient={insufficient}")

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
            d_t = debias_group(Tsub, rng)
            d_n = debias_group(Nsub, rng)
            if d_t is None or d_n is None:
                continue
            res["pathways"][p] = {
                "n_genes_in_pathway": len(genes),
                "tumor": d_t,
                "normal": d_n,
                "delta_deb": float(d_t["rho_deb"] - d_n["rho_deb"]),
                "delta_raw": float(d_t["rho_raw"] - d_n["rho_raw"]),
            }
        all_results[cancer] = res
        print(f"  {len(res['pathways'])} pathways debiased  "
              f"[{time.time()-t1:.1f}s]")
        # incremental flush
        OUT.write_text(json.dumps(all_results, indent=2))
        print(f"  flushed -> {OUT.name}")

    print(f"\nDone. Wrote {OUT}  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
