"""
measure_pairA_tcga.py — Pair A: MOLECULAR -> PATHWAY (inside the cellular rung).

Rung n   = individual genes (molecular constituents).
Rung n+1 = MSigDB Hallmark pathways (pathway-level aggregates).
Observation axis = TCGA samples. Verdict is on HEALTHY / matched-normal tissue
(the coordinated, actively-maintained substrate). Tumour is computed as a
contrast and does NOT enter the verdict.

Per cancer:
  W_n      within-rung coupling among genes (mean over the 50 pathways of the
           within-pathway mean |Pearson|), shuffle-debiased.
  W_{n+1}  within-rung coupling among the 50 pathway scores, shuffle-debiased.
  W_within = sqrt(W_n * W_{n+1}).
  tau      normalised cross-rung Gaussian MI between the gene layer and the
           pathway layer, shuffle-debiased, then gene-set-scramble corrected
           (subtract the median tau against random gene sets of matched sizes).
  ratio    = tau_corrected / W_within.

Data is fetched per-cancer from the public NCI GDC API (no credentials),
computed, then the matrix is deleted — the host is disk-constrained. Only
healthy/normal samples plus a capped tumour pool are downloaded.

Constructions and debiasing are exactly as in PREREGISTRATION.md §2-4.
"""
import io
import json
import pathlib
import sys
import tarfile
import time

import numpy as np
import pandas as pd
import requests

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from crossrung_lib import within_rung_W, cross_rung_tau, mean_abs_corr  # noqa

SEED = 17
TUMOR_CAP = 60
BATCH = 40
MIN_GENES = 10
N_SCRAMBLE = 50

GDC_FILES = "https://api.gdc.cancer.gov/files"
GDC_DATA = "https://api.gdc.cancer.gov/data"
GMT = (HERE / ".." / ".." / "data_tcga" / "data"
       / "h.all.v2024.1.Hs.symbols.gmt").resolve()

CANCERS = ["TCGA-THCA", "TCGA-LUSC", "TCGA-LIHC", "TCGA-HNSC",
           "TCGA-STAD", "TCGA-KIRP", "TCGA-KICH"]


def load_hallmark(p):
    sets = {}
    for line in pathlib.Path(p).read_text().strip().split("\n"):
        parts = line.split("\t")
        sets[parts[0]] = parts[2:]
    return sets


def query_manifest(project, sample_type):
    filt = {"op": "and", "content": [
        {"op": "in", "content": {"field": "cases.project.project_id",
                                 "value": [project]}},
        {"op": "in", "content": {"field": "data_type",
                                 "value": ["Gene Expression Quantification"]}},
        {"op": "in", "content": {"field": "analysis.workflow_type",
                                 "value": ["STAR - Counts"]}},
        {"op": "in", "content": {"field": "access", "value": ["open"]}},
        {"op": "in", "content": {"field": "cases.samples.sample_type",
                                 "value": [sample_type]}},
    ]}
    params = {"filters": json.dumps(filt), "size": 5000, "format": "json",
              "fields": "file_id,file_name,cases.samples.submitter_id",
              "expand": "cases.samples"}
    r = requests.get(GDC_FILES, params=params, timeout=120).json()
    rows = []
    for h in r["data"]["hits"]:
        bcs = [s.get("submitter_id", "")
               for c in h.get("cases", []) for s in c.get("samples", [])]
        rows.append((h["file_id"], bcs[0] if bcs else h["file_id"][:12]))
    return rows


def bulk_download(ids):
    out = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        for attempt in range(3):
            try:
                resp = requests.post(
                    GDC_DATA, data=json.dumps({"ids": chunk}),
                    headers={"Content-Type": "application/json"}, timeout=600)
                resp.raise_for_status()
                if len(chunk) == 1:
                    out[chunk[0]] = resp.content
                else:
                    with tarfile.open(fileobj=io.BytesIO(resp.content),
                                      mode="r:*") as tf:
                        for m in tf.getmembers():
                            if m.isfile():
                                out[m.name.split("/")[0]] = \
                                    tf.extractfile(m).read()
                break
            except Exception as e:
                print(f"      batch attempt {attempt+1} failed: "
                      f"{type(e).__name__}: {str(e)[:60]}")
                time.sleep(5)
    return out


def parse_star(raw):
    df = pd.read_csv(io.StringIO(raw.decode("utf-8", errors="replace")),
                     sep="\t", comment="#")
    df = df[~df["gene_id"].astype(str).str.startswith("N_")]
    df = df[df["gene_name"].notna()]
    return df.groupby("gene_name")["tpm_unstranded"].max()


def build_matrix(project, sample_type, cap, rng):
    man = query_manifest(project, sample_type)
    if cap and len(man) > cap:
        sel = rng.choice(len(man), size=cap, replace=False)
        man = [man[i] for i in sorted(sel)]
    blobs = bulk_download([m[0] for m in man])
    cols = {}
    for fid, bc in man:
        if fid not in blobs:
            continue
        try:
            s = parse_star(blobs[fid])
        except Exception:
            continue
        label = bc if bc not in cols else f"{bc}|{fid[:6]}"
        cols[label] = np.log2(s + 1.0)
    return pd.DataFrame(cols).dropna(how="any")


def pathway_scores(expr_genes_x_samples, sets):
    """expr is genes x samples (DataFrame). Return (samples x pathways) score
    matrix: pathway score = mean of z-scored member genes per sample."""
    gset = set(expr_genes_x_samples.index)
    X = expr_genes_x_samples.values            # genes x samples
    gz = (X - X.mean(axis=1, keepdims=True))
    sd = gz.std(axis=1, keepdims=True)
    gz = np.divide(gz, sd, out=np.zeros_like(gz), where=sd > 1e-10)
    gidx = {g: i for i, g in enumerate(expr_genes_x_samples.index)}
    names, score_cols = [], []
    for p, genes in sets.items():
        idx = [gidx[g] for g in genes if g in gset]
        if len(idx) < MIN_GENES:
            continue
        names.append(p)
        score_cols.append(gz[idx, :].mean(axis=0))      # per sample
    return np.array(score_cols).T, names                # samples x pathways


def measure_group(expr, sets, rng, label):
    """expr: genes x samples DataFrame. Returns the Pair-A measurement dict."""
    m = expr.shape[1]
    gset = set(expr.index)
    gidx = {g: i for i, g in enumerate(expr.index)}
    Xgenes = expr.values.T                              # samples x genes

    # --- W_n: mean over pathways of within-pathway gene mean|Pearson| ---
    wn_raw, wn_db = [], []
    pw_gene_idx = {}
    for p, genes in sets.items():
        idx = [gidx[g] for g in genes if g in gset]
        if len(idx) < MIN_GENES:
            continue
        pw_gene_idx[p] = idx
        sub = Xgenes[:, idx]
        r = within_rung_W(sub, rng)
        if np.isfinite(r[0]):
            wn_raw.append(r[0])
        if np.isfinite(r[2]):
            wn_db.append(r[2])
    W_n_raw = float(np.mean(wn_raw))
    W_n = float(np.mean(wn_db))

    # --- rung n+1: pathway scores, W_{n+1} ---
    P, pnames = pathway_scores(expr, sets)              # samples x pathways
    wm = within_rung_W(P, rng)
    W_np1_raw, W_np1 = wm[0], wm[2]
    W_within = float(np.sqrt(max(W_n, 0.0) * max(W_np1, 0.0)))

    # --- cross-rung tau: gene layer vs pathway layer ---
    # gene layer R_n = expression restricted to all Hallmark-pathway genes
    all_pw_genes = sorted({g for genes in sets.values()
                           for g in genes if g in gset})
    Rn = expr.loc[all_pw_genes].values.T                # samples x genes
    tau = cross_rung_tau(Rn, P, m, rng)

    # --- confound: gene-set scramble (mechanical-aggregation floor) ---
    sizes = [len(v) for v in pw_gene_idx.values()]
    all_genes = list(expr.index)
    scramble_taus = []
    sr = np.random.default_rng(SEED + 1)
    for _ in range(N_SCRAMBLE):
        rand_scores = []
        for sz in sizes:
            pick = sr.choice(len(all_genes), size=sz, replace=False)
            sub = Xgenes[:, pick]
            subz = sub - sub.mean(axis=0, keepdims=True)
            sd = subz.std(axis=0, keepdims=True)
            subz = np.divide(subz, sd, out=np.zeros_like(subz),
                             where=sd > 1e-10)
            rand_scores.append(subz.mean(axis=1))
        Pscr = np.array(rand_scores).T                  # samples x pathways
        t = cross_rung_tau(Rn, Pscr, m, sr)
        if np.isfinite(t["tau_debiased"]):
            scramble_taus.append(t["tau_debiased"])
    tau_scramble = float(np.median(scramble_taus)) if scramble_taus else 0.0
    tau_corrected = max(tau["tau_debiased"] - tau_scramble, 0.0)

    ratio = tau_corrected / W_within if W_within > 1e-9 else np.nan
    return dict(
        label=label, m_samples=int(m), n_pathways=len(pnames),
        W_n_raw=W_n_raw, W_n=W_n, W_np1_raw=float(W_np1_raw),
        W_np1=float(W_np1), W_within=W_within,
        tau_raw=tau["tau_raw"], tau_floor=tau["tau_floor"],
        tau_debiased=tau["tau_debiased"], tau_scramble=tau_scramble,
        tau_corrected=float(tau_corrected), q_pca=tau["q"],
        tau_noise_dominated=bool(
            tau["tau_raw"] > 1e-9
            and tau["tau_debiased"] / tau["tau_raw"] < 0.3),
        ratio=float(ratio),
    )


def main():
    print("=" * 78)
    print("Pair A — TCGA molecular -> pathway: cross-rung vs within-rung coupling")
    print("=" * 78)
    sets = load_hallmark(GMT)
    print(f"  loaded {len(sets)} Hallmark pathways from {GMT.name}")
    results = {}
    for proj in CANCERS:
        short = proj.replace("TCGA-", "")
        t0 = time.time()
        rng = np.random.default_rng(SEED)
        print(f"\n=== {short} ===")
        try:
            expr_n = build_matrix(proj, "Solid Tissue Normal", None, rng)
            expr_t = build_matrix(proj, "Primary Tumor", TUMOR_CAP, rng)
        except Exception as e:
            print(f"  fetch FAILED {type(e).__name__}: {str(e)[:80]}")
            continue
        print(f"  healthy: {expr_n.shape[0]} genes x {expr_n.shape[1]} samples"
              f"   tumour: {expr_t.shape[0]} genes x {expr_t.shape[1]} samples"
              f"   [{time.time()-t0:.0f}s fetch]")
        if expr_n.shape[1] < 12:
            print(f"  healthy n={expr_n.shape[1]} < 12 -- skip (too few "
                  f"samples for PCA-MI)")
            continue
        rh = measure_group(expr_n, sets, np.random.default_rng(SEED),
                           "healthy")
        rt = measure_group(expr_t, sets, np.random.default_rng(SEED),
                           "tumour") if expr_t.shape[1] >= 12 else None
        del expr_n, expr_t
        results[short] = {"healthy": rh, "tumour": rt}
        print(f"  HEALTHY  W_n={rh['W_n']:.3f}  W_n+1={rh['W_np1']:.3f}  "
              f"W_within={rh['W_within']:.3f}")
        print(f"           tau raw {rh['tau_raw']:.3f} floor "
              f"{rh['tau_floor']:.3f} -> debiased {rh['tau_debiased']:.3f}"
              f"  scramble {rh['tau_scramble']:.3f} -> "
              f"corrected {rh['tau_corrected']:.3f}"
              f"{'  [NOISE-DOM]' if rh['tau_noise_dominated'] else ''}")
        print(f"           ratio = tau_corrected / W_within = "
              f"{rh['ratio']:.3f}")
        if rt:
            print(f"  tumour   W_within={rt['W_within']:.3f}  "
                  f"tau_corrected={rt['tau_corrected']:.3f}  "
                  f"ratio={rt['ratio']:.3f}  (contrast only)")
        (HERE / "results_pairA.json").write_text(
            json.dumps(results, indent=2))

    healthy_ratios = [v["healthy"]["ratio"] for v in results.values()
                      if v["healthy"] and np.isfinite(v["healthy"]["ratio"])]
    if healthy_ratios:
        med = float(np.median(healthy_ratios))
        print("\n" + "=" * 78)
        print(f"  Pair A median HEALTHY ratio over {len(healthy_ratios)} "
              f"cancers = {med:.3f}")
        verdict = ("Simon (within dominates)" if med < 0.5 else
                   "framework (cross dominates)" if med > 1.5 else
                   "middle band")
        print(f"  ratio range [{min(healthy_ratios):.3f}, "
              f"{max(healthy_ratios):.3f}]  -> verdict: {verdict}")
    print(f"\n  wrote {HERE / 'results_pairA.json'}")


if __name__ == "__main__":
    main()
