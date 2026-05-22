# RESULTS — Cross-rung coupling, extension beyond n=2

Post-measurement. Pre-registered design in `PREREGISTRATION.md`, committed in a
preceding commit (git history is the proof). 2026-05-21.

## The question

`papers/Corridor Dynamics.tex` §sec:crossrung reports the cross-rung /
within-rung coupling ratio as $O(1)$ (order 0.3–3), anchored across 26
pre-registered cells but at only **n = 2 distinct rung pairs** (TCGA
molecular→pathway and LLM internal→external). The synthesis flagged n = 2 as the
cross-rung tier's weakest point. This experiment measures additional real rung
pairs from structural-series data on disk, with the **same method** as Path 1
(`crossrung_series/path1_tau/crossrung_lib.py`) so the numbers are comparable.

Pre-registered verdict rule, per pair:
- **$O(1)$ holds:** ratio stays in order 0.3–3 → the cross-rung corridor
  (Claim 6) is anchored at $n > 2$.
- **$O(1)$ breaks:** a pair sits decisively at $g/J \ll 1$ (Simon
  near-decomposability) or $g/J \gg 3$ → the $O(1)$ reading is
  rung-pair-specific, not general.

This is the coupling-**ratio** form only. The timescale form is out of scope.

## Candidate rung pairs and data availability

The pre-registration named three candidates, "subject to data availability".
Discipline: real on-disk data only; a pair whose data cannot be located is
reported **MISSING**, not fabricated.

| Candidate pair | Data on disk? | Outcome |
|----------------|---------------|---------|
| C. elegans neuron→functional-class | YES — `worm_data_short.parquet` (qsimeon/celegans_neural_data, calcium imaging) | **MEASURED** |
| cancer pathway→hallmark | NO | **MISSING** |
| fMRI region→network | NO | **MISSING** |

**cancer pathway→hallmark — MISSING.** A pathway→hallmark pair *distinct from*
Path 1's molecular→pathway needs a fine pathway layer below Hallmark
(Reactome / KEGG / GO) as rung $n$, plus the raw gene×sample expression
matrices. Only the MSigDB Hallmark GMT is on disk — no finer-grained GMT — and
the TCGA expression matrices are not on disk (Path 1's `measure_pairA_tcga.py`
fetches each per-cancer from the GDC API and deletes it after computing; the
host is disk-constrained). What remains on disk is per-pathway within-rung $\rho$
summaries only, not the matrices a cross-rung MI needs. (`results_cancer_pathway_hallmark.json`.)

**fMRI region→network — MISSING.** The on-disk ABIDE-PCP timeseries use the
CC200 (Craddock-2012, 200-cluster functional) parcellation. The $n+1$ rung needs
a fixed region→network membership map — the analog of TCGA gene-sets and the
C. elegans functional-class map. No CC200→network lookup is on disk, and the
CC200 atlas image (needed for a spatial-overlay assignment) is not cached and is
not fetchable (`cluster_roi.projects.nitrc.org` returns an SSL certificate
failure). A data-driven network partition would introduce a clustering method
choice absent from `crossrung_lib.py`, violating the pre-registered "same
method" constraint. (`results_fmri.json`.)

## Pair measured — C. elegans neuron → functional-class

The exact structural parallel of Path 1 Pair A (TCGA molecular→pathway): the
$n+1$ rung is an aggregate over member constituents of the $n$ rung.

- **Rung $n$** = individual labeled neurons (constituents).
- **Rung $n+1$** = functional-class aggregate traces — sensory / interneuron /
  motor / command, the canonical v15a/v15b prefix map (identical to the
  `robust_rerun/celegans` run). Class score = mean of z-scored member-neuron
  traces, parallel to Pair A's `pathway_scores`.
- **Observation axis** = calcium-imaging time-points of one worm.
- $W_n$ = within-rung coupling among neurons (mean over the 4 classes of the
  within-class mean $|$Pearson$|$, shuffle-debiased); $W_{n+1}$ = within-rung
  coupling among the 4 class-aggregate traces, debiased; $W_{\text{within}} =
  \sqrt{W_n \cdot W_{n+1}}$.
- $\tau$ = normalised cross-rung Gaussian MI (`crossrung_lib.cross_rung_tau`),
  shuffle-debiased, then **class-scramble corrected** — subtract the median
  $\tau$ against random neuron groups of matched sizes, the mechanical-
  aggregation floor removal, exactly parallel to Pair A's gene-set scramble.
- **ratio** = $\tau_{\text{corrected}} / W_{\text{within}}$.

**Data:** `worm_data_short.parquet` on disk, 919 (study, worm) units with
labeled neurons across 11 source datasets. Inclusion: a worm needs ≥ 3 of the 4
functional classes populated with ≥ 3 classified neurons each, aligned trace
length ≥ 12. **340 of 919 worms** clear inclusion and yield a usable ratio; 579
are excluded (492 have < 3 usable functional classes — too few labeled neurons
spread across the classes — and 87 have < 4 classified neurons). All exclusions
are inclusion-criterion misses, not failures.

### Per-study ratios (340 worms, 11 datasets)

| Source dataset | n worms | median ratio | range |
|----------------|--------:|-------------:|-------|
| Dag2023        |   7 | 0.308 | 0.151–0.764 |
| Flavell2023    |  40 | 0.520 | 0.156–1.038 |
| Kaplan2020     |  19 | 0.402 | 0.056–1.185 |
| Kato2015       |  12 | 0.435 | 0.120–0.800 |
| Leifer2023     | 108 | 0.242 | 0.000–0.555 |
| Nejatbakhsh2020|  21 | 0.161 | 0.000–0.476 |
| Nichols2017    |  44 | 0.447 | 0.000–2.401 |
| Skora2018      |  12 | 0.466 | 0.264–0.680 |
| Uzel2022       |   6 | 0.087 | 0.000–0.380 |
| Venkatachalam2024 | 22 | 0.227 | 0.111–0.414 |
| Yemini2021     |  49 | 0.468 | 0.000–1.630 |

**Worm-level: median ratio 0.313, range [0.000, 2.401].** Percentiles
5/25/50/75/95 = 0.056 / 0.186 / 0.313 / 0.492 / 0.819. 184 of 340 worms (54%)
land inside the pre-registered O(1) band [0.3, 3]; 156 (46%) fall below 0.3; **0
worms exceed 3**. Study-level median-of-study-medians 0.402, range across the
11 study medians [0.087, 0.520]. No worm is noise-dominated (every $\tau$
estimate clears its shuffle floor).

The class-scramble correction is doing heavy work: debiased $\tau$ median 0.904,
$\tau_{\text{scramble}}$ median 0.736, $\tau_{\text{corrected}}$ median 0.175 —
~80% of the cross-rung MI at this pair is mechanical (a class score is an
arithmetic mean of its member neurons), and what survives is a small genuine
biological residual. $W_{\text{within}}$ median 0.564 ($W_n$ 0.472, $W_{n+1}$
0.717).

## Verdict — flat

| Pair | n units | median ratio | range | verdict |
|------|--------:|-------------:|-------|---------|
| C. elegans neuron→functional-class | 340 worms (11 datasets) | **0.313** | [0.000, 2.401] | **O(1), lower edge** |
| cancer pathway→hallmark | — | — | — | MISSING (no on-disk data) |
| fMRI region→network | — | — | — | MISSING (no on-disk data) |

**The C. elegans pair lands inside the pre-registered O(1) band, but at its
lower edge.** The worm-level median 0.313 and the study-level median 0.402 both
sit just inside [0.3, 3]. By the pre-registered rule the pair does **not** break
O(1) — the median is not decisively $\ll 1$ — so O(1) holds and the cross-rung
anchor extends to **n = 3 distinct rung pairs**. But the result is honestly a
*soft* pass, not a clean confirmation, and three things qualify it:

1. **The pair leans Simon-ward, not centred.** 46% of worms fall below the 0.3
   O(1) floor; the worm-level median 0.313 grazes that floor. Cross-rung
   coupling at this pair is the *minority* term — comparable to but distinctly
   smaller than within-rung coupling — which is the near-decomposability
   direction. The two earlier pairs straddled parity (Pair A median 1.15 above,
   Pair B median 0.72 below); this third pair sits clearly on the
   within-dominated side.

2. **Two whole studies fall below the O(1) floor.** Uzel2022 (median 0.087, n=6)
   and Nejatbakhsh2020 (median 0.161, n=21) sit decisively at $g/J \ll 1$ — the
   Simon near-decomposable regime. Per the pre-registered "O(1) breaks" branch,
   *within these two datasets* the cross-rung coupling is a weak residual, not
   O(1). The pair median survives because the other 9 studies (medians
   0.23–0.52) pull it back into band, but the dataset-level spread is real and
   reportable: the ratio is not uniform across acquisition setups.

3. **The mechanical-aggregation floor is large here.** ~80% of the raw
   cross-rung MI is removed by the class-scramble correction. The O(1)-edge
   result rests on the small biological residual $\tau_{\text{corrected}}
   \approx 0.18$; had the correction been omitted (as a naive measurement
   would), the ratio would read $\gg 1$ spuriously. The correction is the same
   one Path 1 Pair A applied, so the comparison is fair — but it means the
   genuine cross-rung signal at this biological pair is modest.

**Bottom line.** The new total is **n = 3 distinct rung pairs** with a measured
cross-rung / within-rung coupling ratio (TCGA molecular→pathway ≈ 1.15; LLM
internal→external ≈ 0.72; C. elegans neuron→functional-class ≈ 0.31). All three
medians lie within order 0.3–3, so **O(1) holds across the expanded set** and
§sec:crossrung's n = 2 caveat is relieved by one pair. The honest qualification:
the three medians span an order of magnitude (1.15 / 0.72 / 0.31), trending
*down* as the substrate gets biologically finer-grained, and the C. elegans pair
specifically sits at the lower O(1) edge with two of its eleven constituent
datasets below the floor. O(1) is confirmed as a band, not as a tight value; the
cross-rung corridor is wide, and at the finest pair measured it is closer to
Simon's near-decomposable end than to parity.

The two MISSING pairs (cancer pathway→hallmark, fMRI region→network) are
recorded as not-measured because the required on-disk data — a finer pathway
GMT plus TCGA expression matrices, and a CC200→network membership map
respectively — could not be located. They are not fabricated and not estimated.

## Files

- `measure_celegans.py` — the measurement (same `crossrung_lib` estimators as
  Path 1; class-scramble correction parallel to Pair A's gene-set scramble).
- `results_celegans.json` — per-worm records, flushed incrementally as computed.
- `results_cancer_pathway_hallmark.json`, `results_fmri.json` — MISSING stubs
  with the specific on-disk-data reason.

## Honest limits

- **One of three candidate pairs measured.** The other two are MISSING for
  concrete, stated data reasons — the extension adds one rung pair, not three.
- The Gaussian-MI estimator assumes the PCA-reduced representations are
  approximately jointly Gaussian; calcium traces are non-negative and
  autocorrelated. The shuffle null debiases the estimator's bias, not its form.
  This is the same estimator caveat Path 1 carries.
- C. elegans has only 4 functional classes, so the $n+1$ rung is low-dimensional
  ($W_{n+1}$ and the cross-rung MI are computed on ≤ 4 aggregate series). Path 1
  Pair A's $n+1$ rung had 50 Hallmark pathways. The smaller $n+1$ rung makes the
  C. elegans cross-rung MI noisier per worm; the 340-worm sample is what gives
  the median its stability.
- 340 of 919 worms measured; the 579 exclusions are all inclusion-criterion
  misses (too few labeled neurons across classes), not silent failures.
