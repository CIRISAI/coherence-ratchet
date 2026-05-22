# Debiased TCGA re-run — RESULTS

Post-measurement. Pre-registered design in `PREREGISTRATION.md` (committed
before this run). 2026-05-21.

## What ran

The raw TCGA run (`data_tcga/`) computed within-rung ρ as raw `mean_abs_corr`
with no surrogate-floor subtraction. Every other structural-series substrate
carries debiased ρ. This run debiases TCGA so it is comparable with the
debiased biological cluster, discharging the item §sec:robust-rerun flagged as
owed.

Data: the same 7-cancer on-disk TCGA record (`data_tcga/data/*_expr.tsv.gz`,
STAR-Counts log2(TPM+1) matrices, 59,427 genes, TCGA barcodes with `|01`/`|11`
sample-type suffix), fetched from the public NCI GDC API by `01_fetch_gdc.py`.
The matrices are gitignored (~335 MB, regenerable); they were recovered intact
from disk and re-used — **no synthetic data, no new GDC fetch**. The fetch
record is 7 cancers (THCA, LUSC, LIHC, HNSC, STAD, KIRP, KICH), not twelve; the
"twelve-cancer" phrasing combines this run with a prior disjoint 5-cancer set.
This run debiases the 7 on-disk cancers.

The surrogate, per pre-registration: TCGA Hallmark-pathway ρ is over
samples × pathways, **not** a time series. Phase randomization does not apply.
The floor is a **per-pathway permutation surrogate** — each gene's values are
independently permuted across samples (N=20 draws), destroying cross-gene
correlation while exactly preserving each gene's marginal. Debiased
ρ = `sqrt(max(rho_raw² − floor², 0))`. k_eff is the canonical
participation-ratio of the gene-gene correlation eigenvalues, matching
`data_fmri/fmri_corridor.py`.

Scripts: `debias_tcga.py` (per-cancer debiased ρ + k_eff, incremental flush to
`results_debiased.json`), `debias_sig.py` (bootstrap 95% CI on the *debiased*
delta — B=500 — so the tumour-drift significance gate matches the raw run's
non-overlapping-CI gate; flush to `results_debiased_sig.json`),
`analyze.py` (summary).

## Healthy-tissue debiased ρ — per cancer (vs raw)

| Cancer | n_n | raw ρ_n | floor_n | **debiased ρ_n** | IQR_deb | p10 | p90 | k_eff_n (PR) |
|--------|----:|--------:|--------:|-----------------:|--------:|----:|----:|-------------:|
| THCA | 59 | 0.317 | 0.105 | **0.299** | 0.084 | 0.231 | 0.390 | 6.2 |
| LUSC | 51 | 0.239 | 0.113 | **0.210** | 0.092 | 0.170 | 0.328 | 10.0 |
| LIHC | 50 | 0.329 | 0.114 | **0.308** | 0.134 | 0.215 | 0.436 | 6.1 |
| HNSC | 44 | 0.328 | 0.122 | **0.305** | 0.092 | 0.241 | 0.452 | 6.4 |
| STAD | 36 | 0.374 | 0.136 | **0.348** | 0.084 | 0.299 | 0.452 | 4.9 |
| KIRP | 32 | 0.377 | 0.144 | **0.349** | 0.105 | 0.295 | 0.510 | 4.9 |
| KICH | 25 | 0.342 | 0.164 | **0.300** | 0.098 | 0.257 | 0.425 | 5.4 [insuff. n] |

Pooled healthy debiased ρ over the 6 primary cancers (300 pathway-values):
**median 0.312, IQR [0.261, 0.367], range [0.112, 0.608]**.

The permutation floor is modest (0.10–0.16) and remarkably uniform across
cancers — it shifts each cancer's healthy ρ down by ≈0.02–0.04, not enough to
move any cancer to a pole. Every healthy IQR stays tight (0.084–0.134, all
≤0.15); no p90 near rigidity (max 0.51), no p10 near chaos (min 0.17). The
bounded-band signature is unchanged by debiasing.

## Tumour drift under debiasing (debiased ρ, matched to the raw significance gate)

The raw run reports **201/201** significant pathway-shifts chaos-ward, where
"significant" = non-overlapping bootstrap 95% CI of raw ρ_t vs raw ρ_n. The
debiased re-run applies the identical gate to the **debiased** ρ (B=500
bootstrap, debiased per resample):

| Cancer | debiased-significant pathways | chaos-ward | rigidity-ward |
|--------|------------------------------:|-----------:|--------------:|
| THCA | 2 | 2 | 0 |
| LUSC | 35 | 35 | 0 |
| LIHC | 22 | 22 | 0 |
| HNSC | 31 | 31 | 0 |
| STAD | 44 | 44 | 0 |
| KIRP | 33 | 33 | 0 |
| KICH | 6 | 6 | 0 [insuff. n] |

**Debiased total: 173/173 chaos-ward, 0 rigidity-ward** (167/167 over the 6
primary cancers).

The count of significant pathways drops from 201 to 173: floor subtraction
shrinks some shifts below the CI-significance threshold (e.g. LIHC 28→22,
HNSC 37→31). But **every single surviving significant shift is chaos-ward —
zero rigidity-ward, exactly as in the raw run**. Across all 350 pathways
(significant or not) the all-cancer chaos-ward share of debiased deltas is
296/350 (264/300 primary); the directional signal is dominant even before the
significance gate. Sign-consistency of the debiased delta against the
all-negative raw delta is 43–50/50 per cancer.

## Verdict (flat, per the pre-registration)

**(a) Healthy band — does debiased TCGA healthy ρ_mid sit off both poles and
within the biological cluster (≈0.27–0.33)?**

YES. Pooled debiased healthy ρ_mid = **0.312**, inside the [0.27, 0.33]
biological cluster. Per-cancer debiased healthy ρ_mid spans 0.210–0.349: four
of seven (THCA 0.299, LIHC 0.308, HNSC 0.305, KICH 0.300) land squarely in the
cluster; LUSC (0.210) sits below it but still decisively off both poles;
STAD (0.348) and KIRP (0.349) sit a hair above 0.33 — the same two cancers
flagged "BROAD-SPREAD / rigidity-side" in the raw run, and debiasing pulls them
*toward* the cluster (raw 0.374/0.377 → debiased 0.348/0.349), not away.
Every cancer's healthy tissue stays in a tight band (IQR 0.084–0.134) off both
poles. **TCGA joins the debiased biological pool**; §sec:robust-rerun's
"debiased TCGA re-run is owed" is discharged.

**(b) Tumour drift — does the chaos-ward drift (201/201 raw) survive
debiasing?**

YES, directionally intact. Under the identical non-overlapping-95%-CI gate
applied to debiased ρ, **173/173 significant pathway-shifts are chaos-ward,
zero rigidity-ward**. The significant-pathway count falls from 201 to 173 —
floor subtraction removes the weakest ~14% of shifts from significance — but
the directional uniformity is exactly preserved: not one shift reverses to
rigidity-ward. The raw run's headline result is robust to debiasing.

## Honest limits

- The raw-vs-debiased count comparison (201 → 173) is a change in *how many*
  shifts clear the significance bar, not a change in *direction*; the
  directional finding (chaos-ward, 0 rigidity-ward) is identical.
- KICH is below the pre-registered tumour-n minimum (66 < 100); reported,
  flagged, excluded from the primary pool — as in the raw run.
- The permutation floor preserves each gene's marginal but not its
  cross-sample structure; for non-temporal sample×pathway data this is the
  correct null (per pre-registration) and the floor it yields is modest and
  uniform, consistent with genuine — not spurious — pathway co-expression.
- Bulk RNA-seq: ρ is the group-level pathway correlation, not a per-sample
  quantity. Unchanged from the raw run's limits.
