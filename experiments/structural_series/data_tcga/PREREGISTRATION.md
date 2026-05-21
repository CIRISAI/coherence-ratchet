# PREREGISTRATION — TCGA cellular-substrate corridor test (extension)

Structural-claims series. Tests **Claim 1** (the corridor is a bounded
attractor at every coordinated substrate) and **Claim 4** (it recurs at
every coordinated rung), per `formal/CoherenceRatchet/StructuralClaims.lean`.

This is committed BEFORE any result is computed. No edits after the first
data run; results go in `RESULT.md` and `NOTES.md`, never here.

## Background — what is already known

The framework's existing 5-cancer TCGA work (`experiments/noncorr_cancer/`,
LUAD / BRCA / COAD / KIRC / PRAD; UCSC-Xena HiSeqV2 matrices, 50 MSigDB
Hallmark gene sets) found:

- healthy / matched-normal Hallmark-pathway within-rung |ρ| clusters at
  **median ≈ 0.27 ± 0.07** — a bounded band;
- tumor tissue drifts **chaos-ward to median ≈ 0.18 ± 0.06**, uniformly
  across all 5 cancers (0/176 FDR-significant pathway-shifts went rigidity-ward);
- the effect survived a tumor-subsampled-to-normal-n control in 4/5 cancers
  (PRAD's collapsed — flagged as small-sample bias).

The A3+ recalibrated corridor (`experiments/open_system_pomega/
corridor_recalculation.py`) puts the coordinated-substrate band at
**|ρ| ≈ 0.17–0.35, centre ≈ 0.25**, with the cellular substrate's healthy
median at 0.27. This is the band this test holds the additional cancers to.

## The claim under test

The cellular gene-regulatory substrate IS a coordinated rung (each Hallmark
pathway = constituents that must co-regulate). Claims 1 & 4 say a bounded
corridor band — off the rigidity pole (ρ→1, clonal lock) and off the chaos
pole (ρ→0, decoherent regulation) — IS expected here. The particle-physics
substrates returned nulls *because they are not coordinated rungs*; the
cellular substrate is the positive test.

A null here — healthy tissue NOT occupying a bounded band — is a genuine
**partial falsifier of Claim 4** (a coordinated rung with no corridor).

## Data

**Source: NCI GDC public API** (`api.gdc.cancer.gov`, open-access HTTP, no
credentials). Per-sample STAR-Counts gene-expression quantification files
(`augmented_star_gene_counts.tsv`), GDC Data Release 45.0. This is the
canonical NCI primary source; the existing 5-cancer work used the Xena
re-host of the same TCGA data.

**Cancers — pre-specified target set.** TCGA projects DISJOINT from the
existing 5, with adequate matched-normal sampling, ranked by
Solid-Tissue-Normal STAR-Counts file count (queried from GDC before this
preregistration was committed):

| Project | Primary Tumor | Solid Tissue Normal | Tier |
|---------|--------------:|--------------------:|------|
| TCGA-THCA (thyroid) | 505 | 59 | primary |
| TCGA-LUSC (lung squamous) | 511 | 51 | primary |
| TCGA-LIHC (liver) | 371 | 50 | primary |
| TCGA-HNSC (head & neck) | 520 | 44 | primary |
| TCGA-STAD (stomach) | 412 | 36 | primary |
| TCGA-KIRP (kidney papillary) | 290 | 32 | primary |
| TCGA-KICH (kidney chromophobe) | 66 | 25 | borderline (tumor n<100) |

The 6 primary-tier cancers all clear the existing-work thresholds (≥20
normal, ≥100 tumor). KICH is included as a borderline case (25 normal but
only 66 tumor) and is reported separately; it does NOT count toward the
recurrence verdict if its tumor n stays under 100 after filtering.

Cancers excluded for inadequate matched-normal: BLCA (19), UCEC (35 but
endometrium has no true matched normal — adjacent myometrium), ESCA (13),
PAAD (4), CHOL (9), READ (10).

**Feasibility scope.** GDC bulk download runs ~1.3 MB/s; a full cancer is
~570 × 4 MB ≈ 2.3 GB. To stay feasible the run downloads ALL matched-normal
samples plus a tumor pool capped at 150 per cancer (random, fixed seed).
The capped tumor pool is sufficient: the analysis is a group-level
correlation, and the sample-size control (below) sub-samples tumor to
normal-n regardless. If download throughput forces a smaller cancer count,
the count actually completed is reported honestly in RESULT.md; no cancer
is fabricated or partially run then reported as complete.

**Gene sets.** MSigDB Hallmark v2024.1.Hs (`h.all.v2024.1.Hs.symbols.gmt`,
50 gene sets, Liberzon 2015) — identical to the existing 5-cancer work.

## Construction (identical to the existing 5-cancer pipeline)

1. STAR-Counts `unstranded` column → genes × samples matrix per cancer;
   Ensembl IDs mapped to HGNC symbols via the `gene_name` column in the
   STAR-Counts file itself. Expression transformed `log2(TPM-equivalent
   + 1)` using the STAR-Counts `tpm_unstranded` column (the Xena HiSeqV2
   matrices were log2(norm_count+1); TPM log is the closest STAR analogue
   and is the GDC-recommended within-sample-normalized quantity).
2. Sample type from the TCGA barcode 4th block: `01` = primary tumor,
   `11` = solid tissue normal. Retain `01` and `11` only.
3. For each Hallmark pathway p (genes intersected with the expression
   matrix, ≥10 genes required): within-rung |ρ| = mean |Pearson
   correlation| over gene–gene pairs in p, computed across the samples of
   one sample-type group (genes = variables, samples = observations).
   This is the framework's group-level within-rung correlation.
4. Bootstrap 95% CI on each |ρ| by resampling samples within group
   (B = 500).

## Pre-registered corridor criterion — a BOUNDED BAND, not a wide window

E1's lesson: "off both poles" inside a 0.4-wide window is NOT a corridor.
The corridor claim requires the healthy-tissue |ρ| values to be
**concentrated in a bounded band**, not merely non-polar.

Operationalized, decided before results:

**C1 — bounded band (Claim 4 recurrence).** For each cancer, take the 50
healthy-tissue per-pathway |ρ| values. The cancer's healthy tissue
"occupies a bounded band" iff ALL of:

  (a) **off rigidity**: 90th-percentile pathway |ρ| < 0.55;
  (b) **off chaos**: 10th-percentile pathway |ρ| > 0.10;
  (c) **bounded width**: the interquartile range (IQR, 25th–75th
      percentile) of the 50 healthy |ρ| values is **≤ 0.15**. This is
      the band-tightness test — an IQR wider than 0.15 is a broad spread,
      not a corridor. (For reference: the existing 5-cancer healthy
      median was 0.27 ± 0.07; a healthy IQR of ~0.10 is the expectation.
      0.15 is a deliberately generous ceiling.)
  (d) **central tendency in the A3+ band**: the median healthy |ρ| lies
      in the recalibrated coordinated-substrate corridor [0.17, 0.35].

A cancer is **BAND-CONSISTENT** iff (a)–(d) all hold; **BROAD-SPREAD** if
(a),(b),(d) hold but (c) fails (off both poles but not concentrated);
**POLE-PILED** if (a) or (b) fails.

**C2 — recurrence verdict (Claim 4).** Across the 6 primary-tier cancers:

  - **RECURS**: ≥ 5 of 6 are BAND-CONSISTENT.
  - **WEAKLY RECURS**: 3–4 of 6 BAND-CONSISTENT, the rest BROAD-SPREAD
    (off poles, loose band).
  - **PARTIAL FALSIFIER of Claim 4**: ≥ 2 of 6 are POLE-PILED, OR ≥ 4 of
    6 are BROAD-SPREAD. A coordinated rung that does not produce a bounded
    band is the Falsifier4 witness — reported as such.

**C3 — tumor drift direction (Claim 1, the attractor reading).** For each
cancer, per-pathway Δ = |ρ|_tumor − |ρ|_normal. Pre-registered
expectation, inherited from the existing 5-cancer result: tumor drifts
**chaos-ward** (Δ < 0) in the large majority of pathways.

  - **CHAOS-DRIFT CONFIRMED**: in ≥ 5 of 6 cancers, ≥ 70% of pathways
    with non-overlapping 95% bootstrap CIs have Δ < 0.
  - **MIXED**: drift direction not consistent across cancers.
  - **RIGIDITY-DRIFT**: ≥ 3 of 6 cancers drift Δ > 0 — would contradict
    the existing 5-cancer finding and is reported as a discrepancy.

## Confound controls (mandatory, pre-registered)

1. **Sample-size imbalance.** Tumor n ≫ normal n; mean-|Pearson| is
   upward-biased at small n. Control: subsample tumor to normal-n
   (50 reps, fixed seed), recompute Δ. A cancer's chaos-drift is counted
   as **real** only if it is preserved (same sign, ≥50% magnitude) in
   ≥ 60% of pathways under n-matching. The existing work flagged PRAD
   as a small-sample artifact by exactly this test; the same control is
   binding here.
2. **Batch effects.** STAR-Counts files carry no plate/batch field
   directly usable per-sample without clinical join; the mitigation is
   that within-cancer tumor-vs-normal is the contrast and both groups are
   drawn from the same project's processing pipeline. The within-sample
   TPM normalization removes library-depth differences. Cross-cancer
   |ρ| comparison is descriptive only — the corridor-band test (C1) is
   evaluated per cancer, not pooled, precisely so a batch offset in one
   cancer cannot manufacture a pooled band.
3. **Gene-coverage imbalance.** Pathways with < 10 mapped genes dropped
   with an explicit log; n_genes_used recorded per pathway.

## Falsifier — stated explicitly

The **Falsifier4 witness** for this test: a TCGA cancer whose
matched-normal (healthy) tissue is **not** in a bounded band — either
POLE-PILED (criterion (a) or (b) fails) or BROAD-SPREAD with an IQR
> 0.15. The cellular regulatory substrate is a coordinated rung; if its
healthy state does not occupy a bounded corridor, Claim 4 has a witness
and is falsified at this substrate. Per C2, ≥ 2 POLE-PILED or ≥ 4
BROAD-SPREAD cancers triggers the PARTIAL FALSIFIER verdict.

A secondary, weaker concern: if healthy tissue IS in a band but tumor
does NOT drift chaos-ward (C3 = RIGIDITY-DRIFT or MIXED), the existing
5-cancer chaos-drift finding does not generalize — reported as a
discrepancy, not a falsifier of Claims 1/4 themselves.

## Scripts

- `01_fetch_gdc.py` — GDC API: per-cancer STAR-Counts manifest, bulk
  download of all matched-normal + capped tumor pool, assemble
  genes×samples expression matrices. Hallmark GMT fetch.
- `02_compute_rho.py` — within-rung |ρ| per (cancer × pathway ×
  sample-type), bootstrap CIs.
- `03_corridor_test.py` — C1/C2/C3 evaluation, sample-size control,
  verdict against the pre-registered thresholds.

— committed before the results commit, 2026-05-21.
