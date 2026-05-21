# RESULT — Path 1 (τ-calibration): cross-rung vs within-rung coupling ratio

Post-measurement. Pre-registered design in `PREREGISTRATION.md`, committed in a
PRECEDING commit (git history is the proof). 2026-05-21.

## The question

Herbert Simon (*Architecture of Complexity*, 1962): stable complex hierarchies
are **near-decomposable** — coupling among constituents inside a subsystem
DOMINATES coupling between subsystems. The framework's Claim 6
(`StructuralClaims.lean`): the multi-rung corridor needs cross-rung coupling to
DOMINATE within-rung. Opposite polarity. Operationalised as a ratio at real
adjacent-rung pairs:

```
ratio = cross-rung coupling τ / within-rung coupling W_within
```

Pre-registered verdict rule: **ratio < 0.5** vindicates Simon and fails
Claim 6's premise; **ratio > 1.5** is framework-distinctive (Claim 6's premise
holds); **0.5 ≤ ratio ≤ 1.5** is the middle band, reported as such.

## What ran — pairs actually measured

**2 of the 3 candidate rung pairs were measured on real data.** Pair 3
(individual→community) needed an open org-psych dataset sourced and was not
reached; it is recorded as not-measured, not fabricated.

| Pair | rungs | substrate | data | units measured |
|------|-------|-----------|------|----------------|
| A | molecular → pathway | TCGA cellular | GDC public API, STAR-Counts, log2(TPM+1) | 6 cancers (healthy tissue) |
| B | internal → external | LLM (A3int→A3ext) | open HF weights, fixed text | 3 models |

Pair A: 7 TCGA cancers were attempted; the run was wall-clock-limited after 6
(THCA, LUSC, LIHC, HNSC, STAD, KIRP). KICH (the borderline-n cancer) did not
complete the GDC fetch within the time budget — it is omitted, not a result.
6 cancers each give one independent healthy-tissue measurement.

## Constructions (as pre-registered)

- **Within-rung coupling W**: mean |Pearson| over constituent pairs, shuffle-
  debiased by quadrature (the E1 `layer_rho` noise-floor procedure). Measured at
  both rungs; `W_within = sqrt(W_n · W_{n+1})`.
- **Cross-rung coupling τ**: normalised Gaussian mutual information
  `I(R_n;R_{n+1}) / min(H_n,H_{n+1})` (Piece 6) on PCA-reduced representations
  (`q = min(8, m//6)` components, fixed rule), debiased by a row-permutation
  shuffle null (mean subtraction).
- **Pair A only — gene-set-scramble correction**: pathway scores recomputed from
  50 random gene sets of matched sizes; `τ_corrected = τ_debiased − median τ
  against scrambled pathways`. This removes the cross-rung MI that is
  *mechanical* (a pathway score is an arithmetic function of its member genes)
  and isolates the *biological* cross-rung coupling.
- `ratio = τ (corrected, for A) / W_within`.

## Pair A — TCGA molecular → pathway (healthy tissue, the verdict pair)

| Cancer | m | W_n (gene) | W_{n+1} (pathway) | W_within | τ_raw | τ_debiased | τ_scramble | τ_corrected | **ratio** |
|--------|--:|-----------:|------------------:|---------:|------:|-----------:|-----------:|------------:|----------:|
| THCA | 59 | 0.309 | 0.639 | 0.445 | 0.932 | 0.874 | 0.296 | 0.578 | **1.299** |
| LUSC | 51 | 0.236 | 0.631 | 0.385 | 0.924 | 0.858 | 0.291 | 0.567 | **1.472** |
| LIHC | 50 | 0.312 | 0.830 | 0.509 | 0.800 | 0.732 | 0.245 | 0.488 | **0.958** |
| HNSC | 44 | 0.324 | 0.716 | 0.482 | 0.866 | 0.799 | 0.349 | 0.450 | **0.933** |
| STAD | 36 | 0.359 | 0.696 | 0.500 | 1.055 | 0.980 | 0.366 | 0.614 | **1.228** |
| KIRP | 32 | 0.373 | 0.815 | 0.551 | 1.011 | 0.943 | 0.356 | 0.588 | **1.066** |

**Median healthy ratio = 1.147, range [0.933, 1.472].** All 6 cancers land
inside the pre-registered middle band [0.5, 1.5]. None is below 0.5 (Simon);
none is above 1.5 (framework). The verdict for Pair A is **MIDDLE BAND**.

Noise control: every τ estimate is well above its shuffle floor — the floor is
6–9% of τ_raw at every cancer, debiased τ retains 91–94% of raw. No cancer is
noise-dominated. The gene-set-scramble correction is doing real work: it removes
~30% of τ (the mechanical-aggregation floor, τ_scramble ≈ 0.25–0.37), and what
remains (τ_corrected ≈ 0.45–0.61) is genuine biological cross-rung coupling, not
the arithmetic of averaging.

Tumour contrast (NOT in the verdict, pre-registered as contrast only): tumour
ratios median 1.218, range [0.793, 1.499] — also middle band, no systematic
move of the cross/within polarity between healthy and tumour tissue.

## Pair B — LLM internal → external (A3int → A3ext)

| Model | m | W_n (hidden) | W_{n+1} (logits) | W_within | τ_raw | τ_debiased | **ratio** |
|-------|--:|-------------:|-----------------:|---------:|------:|-----------:|----------:|
| gpt2 | 268 | 0.080 | 0.993 | 0.281 | 0.212 | 0.201 | **0.716** |
| pythia-160m | 275 | 0.172 | 0.944 | 0.403 | 0.200 | 0.189 | **0.470** |
| Qwen2.5-0.5B | 268 | 0.143 | 0.362 | 0.228 | 0.179 | 0.168 | **0.738** |

**Median ratio = 0.716, range [0.470, 0.738].** All 3 models land in (or, for
pythia, a hair below the edge of) the pre-registered middle band. The verdict
for Pair B is **MIDDLE BAND** (the median 0.716 is unambiguously middle;
pythia's 0.470 grazes the Simon side but the pair median does not).

Noise control: τ shuffle floors are ~0.011, ~5% of raw τ — cross-rung signal is
well above noise at all 3 models. The pre-registered caveat applies: the logit
layer is a learned linear readout of the final hidden state, so some cross-rung
coupling at this pair is architectural; Pair B was pre-registered as the weaker
pair for exactly this reason.

## Verdict — Simon vs the framework, on the data measured

| Pair | n units | median ratio | range | verdict |
|------|--------:|-------------:|-------|---------|
| A — TCGA molecular→pathway | 6 cancers | **1.147** | [0.933, 1.472] | MIDDLE BAND |
| B — LLM internal→external | 3 models | **0.716** | [0.470, 0.738] | MIDDLE BAND |

**Both measured pairs land in the middle band. The data adjudicates for
NEITHER Simon's near-decomposability NOR the framework's Claim 6 strong form.**

What the numbers say plainly:

1. **Simon's strong near-decomposability is not seen.** A near-decomposable
   hierarchy would show cross-rung coupling as a small minority term —
   ratio ≪ 1, e.g. < 0.5. No pair, and no individual unit (cancer or model),
   came in below 0.47. Cross-rung coupling is NOT a negligible residual at
   either real rung pair. The framework's premise that cross-rung coupling is
   *substantial* is supported; Simon's premise that it is *dominated to the
   point of near-decomposability* is not.

2. **The framework's Claim 6 strong form (cross-rung DOMINATES, ratio ≳ 1, the
   abstract tower's g/J ≳ 3) is also not seen.** Cross-rung coupling is
   comparable to within-rung coupling, not several times larger. At Pair A it
   edges slightly above parity (median 1.15); at Pair B it edges slightly below
   (median 0.72). Neither is dominance.

3. **The honest reading is the middle band: at real coordinated rung pairs,
   cross-rung and within-rung coupling are the same order of magnitude.** This
   is the pre-registered "middle" outcome. It is informative: it rules out the
   clean version of BOTH the 60-year-old baseline and the framework's
   distinctive claim. The corridor — if it is the right object — sits at
   *intermediate decomposability*, not at Simon's near-decomposable end and not
   at a cross-rung-dominant end.

This matches the `crossrung_simon_headtohead.py` toy's "partially-coupled
middle" branch — but now on real data at real rung pairs, not a degenerate toy.

## Consequence for Claim 6

Path 1 calibrates the cross-rung scale; it does not by itself fire
`Falsifier6`. `Falsifier6` is "the multi-rung corridor satisfied AND coupling
NOT dominating" — and "dominating" is the g/J gate, which Paths 2 & 3 measure
via relaxation timescales, not Path 1. But Path 1 delivers a sharp constraint
the gate calibration must now respect: **at the two real rung pairs measured,
cross-rung coupling does not dominate within-rung coupling — the ratio is ≈ 1,
not ≳ 3.** If Claim 6's gate is the abstract tower's g/J ≳ 3, these two pairs
are on track to be `Falsifier6` witnesses once their g/J is measured, because a
cross/within coupling RATIO near 1 is hard to reconcile with a g/J several times
above 1. The framework owes either (a) a demonstration that the relaxation-
timescale g/J can be ≳ 3 while the coupling-strength ratio is ≈ 1 — i.e. that
the two operationalisations of "dominance" come apart — or (b) a retraction of
the strong g/J ≳ 3 gate in favour of the calibrated value, which Path 1 now
constrains to the parity region, not the dominance region.

The cross-rung τ band itself, which Path 1 set out to calibrate: at the
data-accessible pairs the *debiased, scramble-corrected* τ is **0.45–0.61**
(Pair A) and the debiased τ is **0.17–0.20** (Pair B). The two pairs do NOT
share a common τ band — Pair A's biological cross-rung MI is ~3× Pair B's. Per
the PROTOCOL, a τ band that varies across pairs is rung-specific, and the
framework owes an explanation; the calibration is NOT structural across these
two substrates. (Part of the gap is the Pair-B architectural caveat; part is
genuine.)

## Honest limits

- 2 of 3 candidate pairs measured; the org-psych pair was not sourced. The
  series' six-pair ambition is not met here — Path 1 measured the two
  data-accessible pairs.
- 6 of 7 TCGA cancers; KICH (borderline n) was cut by the wall-clock budget.
  The 6 that ran are the 6 primary-tier cancers and all clear the pre-reg
  `m ≥ 12` minimum.
- The Gaussian-MI estimator assumes the PCA-reduced representations are
  approximately jointly Gaussian; non-Gaussian dependence is not captured. The
  shuffle null debiases the *bias* of this estimator but does not fix its
  *form*. A k-NN MI estimator (KSG) re-run is owed as a robustness check.
- Pair B's cross-rung link is partly architectural (logits = linear readout of
  the final hidden state); its ratio is a soft data point, not free evidence.
  Pair A is the decisive measurement and it is the cleaner one.
- `W_within` is the geometric mean of two rungs whose raw within-coupling
  differs (Pair A pathway W ≈ 2× gene W; Pair B logit W ≈ 5–12× hidden W). The
  geometric mean is the pre-registered choice. Robustness to that choice:
  recomputing with the ARITHMETIC mean of the two rungs leaves Pair A in the
  middle band (median ratio 1.077, range [0.85, 1.31]) but pushes Pair B to the
  Simon side (median ratio 0.376) — because the logit rung's within-coupling is
  so large (W ≈ 0.94–0.99 for gpt2/pythia) that an arithmetic mean lets it
  dominate the denominator. This is exactly the architectural caveat: Pair B's
  external rung is a near-rigid linear readout, and the verdict for Pair B is
  estimator-sensitive. Pair A — the decisive pair — is robust to the mean
  choice and stays middle band either way.
- Path 1 measures coupling-strength polarity, not the relaxation-timescale g/J.
  The g/J gate test is Paths 2 & 3 and is not run here.
