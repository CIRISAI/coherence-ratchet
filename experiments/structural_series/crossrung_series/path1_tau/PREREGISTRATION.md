# Pre-registration — Path 1 (τ-calibration): cross-rung vs within-rung coupling ratio

Committed BEFORE any results. See `../PROTOCOL.md` for the series ordering
(τ-calibration precedes g/J testing) and the standing discipline. This document
is committed in a SEPARATE commit that PRECEDES the results commit; git history
is the proof.

## 0. The question this Path 1 run settles

Herbert Simon (*The Architecture of Complexity*, 1962): stable complex
hierarchies are **near-decomposable** — coupling AMONG constituents inside a
subsystem DOMINATES coupling BETWEEN subsystems. The framework's Claim 6
(`StructuralClaims.lean`): the multi-rung corridor needs cross-rung coupling to
DOMINATE within-rung. Opposite polarity.

Operationalised as a **ratio** at a real adjacent-rung pair:

```
ratio = cross-rung coupling / within-rung coupling
```

- **ratio ≪ 1** — within dominates → vindicates Simon, fails Claim 6's premise.
- **ratio ≳ 1** — cross dominates → framework-distinctive (Claim 6 premise holds).
- **middle band (≈ 0.5 – 1.5)** — neither polarity is clean; reported as such.

This run does not pre-judge. It measures the ratio at every real, data-accessible
adjacent-rung pair it can source, and reports the numbers.

## 1. Rung pairs and data

### Pair A — MOLECULAR → PATHWAY (inside the cellular rung)
- Rung n = individual genes (molecular constituents).
- Rung n+1 = MSigDB Hallmark pathways (pathway-level aggregates).
- Data: TCGA gene-expression, GDC public API, STAR-Counts, log2(TPM+1) — the
  same `data_tcga` pipeline already used in the series. **Healthy / matched-
  normal (`|11`) tissue** is the coordinated, actively-maintained substrate;
  the measurement is on healthy tissue. Tumour is measured too as a contrast
  but does not enter the verdict.
- One independent measurement per cancer; cancers are the replication axis.
- Data-access status: GDC API reachable; matrices fetched per-cancer, computed,
  then deleted (disk-constrained). Number of cancers actually measured is
  reported in RESULT.md.

### Pair B — LLM INTERNAL → EXTERNAL (A3int → A3ext)
- Rung n = transformer hidden-state structure (internal representation).
- Rung n+1 = output-token / next-token logit-distribution structure (external).
- Data: open LLM weights from HuggingFace (`gpt2`, `EleutherAI/pythia-160m`,
  `Qwen/Qwen2.5-0.5B`), the same models used in Test E1, run on a fixed diverse
  text. Observation axis = token positions.
- Data-access status: HuggingFace reachable; `transformers` installed.

If a pair is not accessible it is recorded as not accessible and not fabricated.

## 2. Constructions (defined HERE, before results)

The observation axis (samples for Pair A, token positions for Pair B) is the
axis over which correlations and mutual information are estimated. Write the
observation count `m`.

### 2.1 Within-rung coupling
For a rung whose constituents at one observation form a vector `x ∈ R^d`:
- z-score each constituent across the `m` observations.
- within-rung coupling `W = mean over all pairs (i≠j) of |Pearson(x_i, x_j)|`.
This is the framework's within-rung ρ (the `02_compute_rho.py` construction,
mean |Pearson|). It is computed at BOTH rungs of a pair:
  - `W_n`  — among the rung-n constituents (genes within a pathway / hidden units).
  - `W_{n+1}` — among the rung-(n+1) constituents (Hallmark pathway scores /
    output-distribution summary features).
- The pair's **within-rung coupling** for the ratio is the geometric mean
  `W_within = sqrt(W_n · W_{n+1})` (debiased values; geometric mean because the
  two rungs are different scales and the ratio must not be dominated by whichever
  rung happens to be larger).

For Pair A, rung-n constituents = genes; to keep `W_n` a single number per
cancer it is the mean over the 50 Hallmark pathways of the within-pathway mean
|Pearson|. Rung n+1 constituents = the 50 Hallmark pathway scores (pathway score
per sample = mean of z-scored member genes); `W_{n+1}` = mean |Pearson| among
those 50 scores.

For Pair B, rung-n constituents = hidden units of a chosen mid-depth layer
(subsampled to a fixed `d`=256 units, fixed seed, for tractable MI); `W_n` =
mean |Pearson| among them across token positions. Rung n+1 = the next-token
logit vector projected to its top-`d`=256 highest-variance vocabulary
coordinates; `W_{n+1}` = mean |Pearson| among those.

### 2.2 Cross-rung coupling τ (Piece 6)
`τ = I(R_n ; R_{n+1}) / min(H_n, H_{n+1})`, the normalised cross-rung mutual
information. `R_n` and `R_{n+1}` are the rung-n and rung-(n+1) constituent
vectors observed jointly over the `m` observations.

Estimator — **Gaussian (parametric) mutual information**, the standard
closed-form for multivariate continuous data:
```
I(R_n;R_{n+1}) = 1/2 · log( det(Σ_n) det(Σ_{n+1}) / det(Σ_joint) )
H_n            = 1/2 · log( (2πe)^{d_n} det(Σ_n) )
```
where Σ are sample covariance matrices of z-scored, dimensionality-reduced
representations. To keep covariance estimation well-conditioned with `m`
observations, both `R_n` and `R_{n+1}` are reduced by PCA to `q` components,
`q = min(8, m//6)` — fixed by this rule, not tuned. τ is the MI normalised by
`min(H_n, H_{n+1})` of the SAME reduced representations, clipped to [0, 1+].
A small ridge `1e-3·I` is added to every covariance before `det`/inverse for
numerical stability (fixed, not tuned).

`R_n` for Pair A = the per-sample PCA of the gene-expression matrix restricted
to all Hallmark-pathway genes. `R_{n+1}` for Pair A = the per-sample PCA of the
50 pathway scores. For Pair B, `R_n` = PCA of the hidden-state matrix, `R_{n+1}`
= PCA of the logit matrix, over token positions.

### 2.3 The ratio
```
ratio = τ / W_within
```
Both numerator and denominator are debiased (§3). τ is normalised MI in [0,~1];
`W_within` is mean |Pearson| in [0,1]. Both are dimensionless coupling
strengths in a comparable [0,1] range, so their ratio is the cross-vs-within
quantity Simon and Claim 6 disagree about.

Uncertainty: per pair, the spread (min–max and IQR) ACROSS the replication
units (cancers for Pair A; models for Pair B) is the reported uncertainty on
the ratio. No parametric CI is claimed beyond that spread.

## 3. Finite-sample bias control (mandatory)

MI estimators and mean |Pearson| are BOTH positively biased at finite `m`.
Every estimate is debiased against a **shuffle null** that destroys real
cross/within structure while preserving the marginal distributions and the
sample count:

- **Within-rung W**: each constituent's values are independently permuted
  across the `m` observations (the E1 `layer_rho` noise-floor procedure).
  `W_debiased = sqrt(max(W_raw^2 − W_floor^2, 0))` (quadrature subtraction,
  identical to E1).
- **Cross-rung τ**: the observation-row ordering of `R_{n+1}` is permuted
  relative to `R_n` (destroys cross-rung dependence, keeps each rung's internal
  structure and entropies). `N_SHUFFLE = 50` permutations give a null mean
  `τ_floor`. `τ_debiased = max(τ_raw − τ_floor, 0)` (MI is non-negative and the
  Gaussian-MI bias is additive in log-det, so a mean-subtraction debias is the
  correct form, not quadrature).
- A pair's `τ_floor` being a large fraction of `τ_raw` is itself reported: if
  `τ_debiased / τ_raw < 0.3` the cross-rung estimate is flagged noise-dominated
  and that pair's ratio is reported with a noise-dominated caveat.

Fixed seeds throughout (`SEED = 17`, matching the existing pipeline).

## 4. Confounds (control specified before the result is seen)

- **Aggregation-induced coupling (Pair A).** The pathway score is a deterministic
  function of its member genes, so molecular and pathway layers are NOT
  independent by construction — some cross-rung MI is mechanical. Control: the
  shuffle null in §3 does NOT remove this (shuffle breaks the sample pairing,
  not the construction), so a SECOND null is computed — **gene-set scramble**:
  pathway scores are recomputed from RANDOM gene sets of the same sizes (50
  random sets, fixed seed). The cross-rung τ against scrambled pathways is the
  "mechanical-aggregation floor"; the reported Pair-A τ is
  `τ_real − τ_scramble` where `τ_scramble` is the median scramble τ. This
  isolates the BIOLOGICAL cross-rung coupling from the arithmetic of averaging.
- **Sample-size imbalance (Pair A).** Healthy `m` ranges ~25–59 across cancers;
  MI bias grows as `m` shrinks. Controlled by the per-cancer shuffle null
  (computed at each cancer's own `m`) and by reporting τ vs `m` so any `m`-trend
  is visible. PCA component count `q` is tied to `m` by the fixed §2.2 rule.
- **Dimensionality (both pairs).** Raw gene/hidden-unit/logit dimensions are
  >>`m`; covariance is rank-deficient. Controlled by the fixed PCA reduction to
  `q` components (§2.2) — the same `q` for both rungs of a pair, set by `m`.
- **Token-position autocorrelation (Pair B).** Adjacent tokens are not
  independent. Controlled by the shuffle null operating on the same token set
  (the null inherits the autocorrelation), and by reporting whether a
  block-permuted null (permute contiguous 8-token blocks) changes τ_floor
  materially.

## 5. Pre-registered interpretation (the verdict rule)

Per pair, compute the median ratio across its replication units.

- **ratio < 0.5** — within-rung coupling dominates. This **vindicates Simon's
  near-decomposability** at that pair and **fails Claim 6's premise** there:
  the multi-rung corridor cannot need cross-rung dominance if cross-rung
  coupling is the minority term. Recorded as a Simon result.
- **ratio > 1.5** — cross-rung coupling dominates. **Framework-distinctive**:
  Claim 6's premise (cross-rung coupling dominates within-rung) holds at that
  pair. Recorded as a framework result.
- **0.5 ≤ ratio ≤ 1.5** — middle band. Neither polarity is clean; the rungs are
  comparably coupled within and across. Recorded honestly as a middle result —
  it neither vindicates Simon nor confirms Claim 6's strong form.

Series-level verdict: if every measured pair lands the same side, that side
wins on the data measured. If pairs split, the split is reported pair-by-pair
with no aggregate spin.

This Path 1 run does NOT test the g/J ≳ 3 gate value (that is Paths 2 & 3 and
needs the relaxation-timescale measurements). It tests the **polarity**: which
of cross-rung and within-rung coupling is the larger term at real rung pairs.
The polarity is exactly where Simon and Claim 6 disagree, so the polarity alone
adjudicates the head-to-head.

## 6. Honest prior

Pair A (molecular→pathway) is a genuine coordinated rung pair: gene-regulatory
coordination within pathways is actively maintained in healthy tissue. The
honest prior is uncertain. Simon's near-decomposability is a 60-year-old
empirically grounded principle and gene modules ARE the textbook example of
near-decomposability (modular biology). So the honest prior leans Simon for
Pair A — a ratio ≳ 1 there would be a genuine surprise and genuinely
framework-distinctive. Pair B (LLM internal→external) has a strong mechanical
link (logits are a learned readout of the final hidden state), so a higher
cross-rung ratio there would be partly architectural, not free evidence for
Claim 6 — hence the prior treats Pair B as the weaker pair and Pair A as the
decisive one. The numbers are reported either way.
