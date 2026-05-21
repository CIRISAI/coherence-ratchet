#!/usr/bin/env python3
"""
03_corridor_test.py — C1/C2/C3 evaluation against PREREGISTRATION.md.

C1  per-cancer bounded-band test on the 50 healthy-tissue |rho| values:
      (a) off rigidity   90th pctile < 0.55
      (b) off chaos      10th pctile > 0.10
      (c) bounded width  IQR <= 0.15
      (d) median in the recalibrated A3+ band [0.17, 0.35]
    BAND-CONSISTENT iff all four; BROAD-SPREAD if a,b,d but not c;
    POLE-PILED if a or b fails.
C2  recurrence verdict across the 6 primary-tier cancers.
C3  tumor drift direction (chaos-ward expected).
Plus the sample-size confound control: tumor subsampled to normal-n.
"""
import json, time, pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
RESULTS = HERE / "results"

PRIMARY = ["THCA", "LUSC", "LIHC", "HNSC", "STAD", "KIRP"]   # KICH borderline
A3_BAND = (0.17, 0.35)
IQR_CEIL = 0.15
RIG_90 = 0.55
CHAOS_10 = 0.10
N_REPS = 50
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
    M = M[keep]
    C = np.corrcoef(M)
    iu = np.triu_indices_from(C, k=1)
    return float(np.nanmean(np.abs(C[iu])))


def classify_band(rho_normal_vals):
    v = np.array([x for x in rho_normal_vals if np.isfinite(x)])
    p10, p25, p75, p90 = np.percentile(v, [10, 25, 75, 90])
    med = float(np.median(v))
    iqr = float(p75 - p25)
    a = p90 < RIG_90                       # off rigidity
    b = p10 > CHAOS_10                     # off chaos
    c = iqr <= IQR_CEIL                    # bounded width
    d = A3_BAND[0] <= med <= A3_BAND[1]    # median in A3+ band
    if not (a and b):
        verdict = "POLE-PILED"
    elif a and b and c and d:
        verdict = "BAND-CONSISTENT"
    else:
        verdict = "BROAD-SPREAD"
    return {"median": med, "iqr": iqr, "p10": float(p10),
            "p25": float(p25), "p75": float(p75), "p90": float(p90),
            "off_rigidity": bool(a), "off_chaos": bool(b),
            "bounded_iqr": bool(c), "median_in_A3band": bool(d),
            "verdict": verdict}


def sample_size_control():
    """Tumor subsampled to normal-n; fraction of pathways whose chaos-drift
    is preserved (same sign, >=50% magnitude)."""
    sets = load_hallmark(DATA / "h.all.v2024.1.Hs.symbols.gmt")
    summary = json.loads((DATA / "fetch_summary.json").read_text())
    rng = np.random.default_rng(SEED)
    out = {}
    for cancer in summary:
        expr_path = DATA / f"{cancer}_expr.tsv.gz"
        if not expr_path.exists():
            continue
        df = pd.read_csv(expr_path, sep="\t", index_col=0)
        cols = list(df.columns)
        tidx = [i for i, c in enumerate(cols) if c.split("|")[1] == "01"]
        nidx = [i for i, c in enumerate(cols) if c.split("|")[1] == "11"]
        E = df.values
        gene_index = df.index
        gset = set(gene_index)
        nn = len(nidx)
        preserved, total = 0, 0
        deltas_full, deltas_sub = [], []
        for p, genes in sets.items():
            gs = [g for g in genes if g in gset]
            idx = gene_index.get_indexer(gs)
            idx = idx[idx >= 0]
            if len(idx) < 10:
                continue
            Tf = E[np.ix_(idx, tidx)]
            Ns = E[np.ix_(idx, nidx)]
            rho_n = mean_abs_corr(Ns)
            rho_tf = mean_abs_corr(Tf)
            subs = []
            for _ in range(N_REPS):
                si = rng.choice(Tf.shape[1], size=nn, replace=False)
                subs.append(mean_abs_corr(Tf[:, si]))
            rho_ts = float(np.mean(subs))
            df_ = rho_tf - rho_n
            ds_ = rho_ts - rho_n
            deltas_full.append(df_)
            deltas_sub.append(ds_)
            total += 1
            if np.sign(df_) == np.sign(ds_) and abs(ds_) >= 0.5 * abs(df_):
                preserved += 1
        out[cancer] = {
            "n_normal": nn, "n_paths": total,
            "preserved": preserved,
            "preservation_rate": preserved / total if total else 0.0,
            "median_delta_full": float(np.median(deltas_full)),
            "median_delta_subsampled": float(np.median(deltas_sub)),
        }
        print(f"  {cancer}: median dfull={out[cancer]['median_delta_full']:+.4f}"
              f"  dsub={out[cancer]['median_delta_subsampled']:+.4f}"
              f"  preserved {preserved}/{total}")
    return out


def main():
    t0 = time.time()
    rho = json.loads((RESULTS / "rho_by_cancer_pathway.json").read_text())

    print("=" * 74)
    print("C1 — per-cancer bounded-band test (healthy / matched-normal |rho|)")
    print("=" * 74)
    c1 = {}
    for cancer, res in rho.items():
        rn = [pd["rho_normal"] for pd in res["pathways"].values()]
        rt = [pd["rho_tumor"] for pd in res["pathways"].values()]
        band = classify_band(rn)
        band["n_pathways"] = len(rn)
        band["tumor_median"] = float(np.median([x for x in rt
                                                if np.isfinite(x)]))
        band["insufficient"] = res.get("insufficient", False)
        c1[cancer] = band
        flag = " [INSUFFICIENT n]" if band["insufficient"] else ""
        print(f"  {cancer:<6} healthy med={band['median']:.3f} "
              f"IQR={band['iqr']:.3f} "
              f"[p10={band['p10']:.2f} p90={band['p90']:.2f}]  "
              f"tumor med={band['tumor_median']:.3f}  "
              f"{band['verdict']}{flag}")

    print()
    print("=" * 74)
    print("C2 — Claim 4 recurrence verdict (6 primary-tier cancers)")
    print("=" * 74)
    prim = {c: c1[c] for c in PRIMARY if c in c1}
    n_band = sum(1 for v in prim.values() if v["verdict"] == "BAND-CONSISTENT")
    n_broad = sum(1 for v in prim.values() if v["verdict"] == "BROAD-SPREAD")
    n_pole = sum(1 for v in prim.values() if v["verdict"] == "POLE-PILED")
    print(f"  of {len(prim)} primary-tier: {n_band} BAND-CONSISTENT, "
          f"{n_broad} BROAD-SPREAD, {n_pole} POLE-PILED")
    if n_band >= 5:
        c2 = "RECURS"
    elif n_band >= 3 and n_pole == 0:
        c2 = "WEAKLY RECURS"
    elif n_pole >= 2 or n_broad >= 4:
        c2 = "PARTIAL FALSIFIER of Claim 4"
    else:
        c2 = "AMBIGUOUS"
    print(f"  C2 VERDICT: {c2}")

    print()
    print("=" * 74)
    print("C3 — tumor drift direction (chaos-ward = delta<0 expected)")
    print("=" * 74)
    c3 = {}
    for cancer, res in rho.items():
        sig = [pd for pd in res["pathways"].values()
               if pd["non_overlap_95"]]
        neg = sum(1 for pd in sig if pd["delta"] < 0)
        frac = neg / len(sig) if sig else 0.0
        med_d = float(np.median([pd["delta"]
                                 for pd in res["pathways"].values()]))
        c3[cancer] = {"n_sig": len(sig), "n_neg_of_sig": neg,
                      "frac_neg": frac, "median_delta": med_d}
        print(f"  {cancer:<6} {len(sig)} sig pathways, "
              f"{neg} chaos-ward ({frac:.0%}), median delta={med_d:+.3f}")
    prim_chaos = sum(1 for c in PRIMARY
                     if c in c3 and c3[c]["n_sig"] >= 5
                     and c3[c]["frac_neg"] >= 0.70)
    if prim_chaos >= 5:
        c3v = "CHAOS-DRIFT CONFIRMED"
    elif sum(1 for c in PRIMARY if c in c3
             and c3[c]["median_delta"] > 0) >= 3:
        c3v = "RIGIDITY-DRIFT"
    else:
        c3v = "MIXED"
    print(f"  C3 VERDICT: {c3v} ({prim_chaos}/6 cancers >=70% chaos-ward)")

    print()
    print("=" * 74)
    print("Confound control — tumor subsampled to normal-n")
    print("=" * 74)
    ssc = sample_size_control()

    out = {"C1_band": c1,
           "C2_recurrence": {"verdict": c2, "n_band_consistent": n_band,
                             "n_broad_spread": n_broad,
                             "n_pole_piled": n_pole,
                             "primary_tier": PRIMARY},
           "C3_drift": {"per_cancer": c3, "verdict": c3v,
                        "n_cancers_chaos_drift": prim_chaos},
           "sample_size_control": ssc}
    (RESULTS / "corridor_test.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {RESULTS/'corridor_test.json'}  [{time.time()-t0:.0f}s]")
    print()
    print(f"SUMMARY: C2 {c2}  |  C3 {c3v}")


if __name__ == "__main__":
    main()
