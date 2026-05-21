#!/usr/bin/env python3
"""
01_fetch_gdc.py — TCGA expression via the public NCI GDC API.

For each pre-registered cancer:
  - query the GDC /files endpoint for STAR-Counts gene-expression files,
    open access, primary-tumor + solid-tissue-normal;
  - download ALL matched-normal files plus a tumor pool capped at
    TUMOR_CAP (random, fixed seed) via the GDC bulk /data endpoint;
  - parse each augmented_star_gene_counts.tsv (gene_name + tpm_unstranded),
    assemble a genes x samples matrix, save as compressed TSV under data/.

Also fetches the MSigDB Hallmark v2024.1.Hs GMT.

Public HTTP, no credentials. GDC Data Release 45.0.
"""
import io, json, gzip, time, tarfile, pathlib, urllib.request
import numpy as np
import pandas as pd
import requests

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)

GDC_FILES = "https://api.gdc.cancer.gov/files"
GDC_DATA = "https://api.gdc.cancer.gov/data"
HALLMARK_URL = ("https://data.broadinstitute.org/gsea-msigdb/msigdb/"
                "release/2024.1.Hs/h.all.v2024.1.Hs.symbols.gmt")

# pre-registered target set (THCA..KIRP primary tier; KICH borderline)
CANCERS = ["TCGA-THCA", "TCGA-LUSC", "TCGA-LIHC", "TCGA-HNSC",
           "TCGA-STAD", "TCGA-KIRP", "TCGA-KICH"]
TUMOR_CAP = 150
BATCH = 40            # files per bulk-download POST
SEED = 17


def fetch_hallmark():
    out = DATA / "h.all.v2024.1.Hs.symbols.gmt"
    if out.exists() and out.stat().st_size > 0:
        print(f"  hallmark cached ({out.stat().st_size} bytes)")
        return
    with urllib.request.urlopen(HALLMARK_URL, timeout=60) as r:
        out.write_bytes(r.read())
    print(f"  hallmark downloaded ({out.stat().st_size} bytes)")


def query_manifest(project):
    """Return list of (file_id, file_name, sample_type, barcode)."""
    base = [
        {"op": "in", "content": {"field": "cases.project.project_id",
                                 "value": [project]}},
        {"op": "in", "content": {"field": "data_type",
                                 "value": ["Gene Expression Quantification"]}},
        {"op": "in", "content": {"field": "analysis.workflow_type",
                                 "value": ["STAR - Counts"]}},
        {"op": "in", "content": {"field": "access", "value": ["open"]}},
        {"op": "in", "content": {"field": "cases.samples.sample_type",
                                 "value": ["Primary Tumor",
                                           "Solid Tissue Normal"]}},
    ]
    filt = {"op": "and", "content": base}
    params = {
        "filters": json.dumps(filt), "size": 5000, "format": "json",
        "fields": ("file_id,file_name,"
                   "cases.samples.sample_type,"
                   "cases.samples.submitter_id"),
        "expand": "cases.samples",
    }
    r = requests.get(GDC_FILES, params=params, timeout=120).json()
    rows = []
    for h in r["data"]["hits"]:
        # one file -> one aliquot -> one sample; pick the first
        sts, bcs = [], []
        for c in h.get("cases", []):
            for s in c.get("samples", []):
                sts.append(s.get("sample_type"))
                bcs.append(s.get("submitter_id", ""))
        if not sts:
            continue
        rows.append((h["file_id"], h["file_name"], sts[0], bcs[0]))
    return rows


def bulk_download(ids):
    """POST a list of file ids to /data, return {file_id: bytes}."""
    out = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        for attempt in range(3):
            try:
                resp = requests.post(
                    GDC_DATA, data=json.dumps({"ids": chunk}),
                    headers={"Content-Type": "application/json"},
                    timeout=600)
                resp.raise_for_status()
                buf = io.BytesIO(resp.content)
                if len(chunk) == 1:
                    # single file: returned raw, not tarred
                    out[chunk[0]] = resp.content
                else:
                    with tarfile.open(fileobj=buf, mode="r:*") as tf:
                        for m in tf.getmembers():
                            if not m.isfile():
                                continue
                            # member path: <file_id>/<file_name>
                            fid = m.name.split("/")[0]
                            out[fid] = tf.extractfile(m).read()
                print(f"    batch {i//BATCH+1}: {len(chunk)} files, "
                      f"{len(resp.content)/1e6:.1f} MB")
                break
            except Exception as e:
                print(f"    batch {i//BATCH+1} attempt {attempt+1} "
                      f"failed: {type(e).__name__}: {str(e)[:70]}")
                time.sleep(5)
    return out


def parse_star_counts(raw):
    """augmented_star_gene_counts.tsv -> Series gene_name -> tpm_unstranded.
    Drops the 4 STAR summary rows (N_unmapped etc.) and unmapped genes."""
    txt = raw.decode("utf-8", errors="replace")
    df = pd.read_csv(io.StringIO(txt), sep="\t", comment="#")
    # summary rows have gene_id starting with 'N_'
    df = df[~df["gene_id"].astype(str).str.startswith("N_")]
    df = df[df["gene_name"].notna()]
    s = df.groupby("gene_name")["tpm_unstranded"].max()  # collapse dup symbols
    return s


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    print("=" * 70)
    print("01_fetch_gdc — TCGA expression via NCI GDC API")
    print("=" * 70)
    fetch_hallmark()

    summary = {}
    for proj in CANCERS:
        t1 = time.time()
        short = proj.replace("TCGA-", "")
        out_path = DATA / f"{short}_expr.tsv.gz"
        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"\n{short}: matrix cached, skip")
            df = pd.read_csv(out_path, sep="\t", index_col=0)
            cols = list(df.columns)
            nt = sum(1 for c in cols if c.split("|")[1] == "01")
            nn = sum(1 for c in cols if c.split("|")[1] == "11")
            summary[short] = {"n_tumor": nt, "n_normal": nn,
                              "n_genes": df.shape[0], "cached": True}
            continue

        print(f"\n=== {short} ===")
        manifest = query_manifest(proj)
        normals = [m for m in manifest if m[2] == "Solid Tissue Normal"]
        tumors = [m for m in manifest if m[2] == "Primary Tumor"]
        print(f"  manifest: {len(tumors)} tumor, {len(normals)} normal")
        if len(tumors) > TUMOR_CAP:
            sel = rng.choice(len(tumors), size=TUMOR_CAP, replace=False)
            tumors = [tumors[i] for i in sorted(sel)]
            print(f"  tumor pool capped to {TUMOR_CAP}")

        wanted = normals + tumors
        id2meta = {m[0]: m for m in wanted}
        print(f"  downloading {len(wanted)} STAR-Counts files ...")
        blobs = bulk_download([m[0] for m in wanted])
        print(f"  retrieved {len(blobs)}/{len(wanted)} files")

        # assemble matrix; column label = '<barcode-or-fid>|<01|11>'
        cols = {}
        st_map = {"Solid Tissue Normal": "11", "Primary Tumor": "01"}
        seen = set()
        for fid, raw in blobs.items():
            meta = id2meta.get(fid)
            if meta is None:
                continue
            try:
                s = parse_star_counts(raw)
            except Exception as e:
                print(f"    parse fail {fid[:8]}: {e}")
                continue
            st = st_map[meta[2]]
            label = f"{meta[3] or fid[:12]}|{st}"
            # de-dup barcodes (multiple aliquots of one sample)
            if label in seen:
                label = f"{label}|{fid[:6]}"
            seen.add(label)
            cols[label] = np.log2(s + 1.0)
        expr = pd.DataFrame(cols)
        expr = expr.dropna(how="any")
        expr.to_csv(out_path, sep="\t")
        nt = sum(1 for c in expr.columns if c.split("|")[1] == "01")
        nn = sum(1 for c in expr.columns if c.split("|")[1] == "11")
        summary[short] = {"n_tumor": nt, "n_normal": nn,
                          "n_genes": expr.shape[0], "cached": False,
                          "manifest_tumor": len(tumors),
                          "manifest_normal": len(normals)}
        print(f"  matrix: {expr.shape[0]} genes x {expr.shape[1]} samples "
              f"({nt} tumor / {nn} normal)  [{time.time()-t1:.0f}s]")

    (DATA / "fetch_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\ndone in {time.time()-t0:.0f}s")
    for c, s in summary.items():
        print(f"  {c}: {s['n_tumor']} tumor / {s['n_normal']} normal, "
              f"{s['n_genes']} genes")


if __name__ == "__main__":
    main()
