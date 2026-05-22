# Cross-rung coupling — extension beyond n=2 — pre-registration

**Date:** 2026-05-21. **Addresses:** the n=2 limitation of the cross-rung
anchor (`papers/Corridor Dynamics.tex` §sec:crossrung — the coupling ratio is
measured at two rung pairs, TCGA molecular→pathway and LLM internal→external).

## Why

§sec:crossrung reports the cross-rung / within-rung coupling ratio as $O(1)$,
anchored across 26 pre-registered cells but at only **n=2 distinct rung pairs**.
The synthesis flagged n=2 as the cross-rung tier's weakest point. More real rung
pairs are extractable from structural-series data already on disk; this
experiment measures them.

## Method

Use the existing cross-rung machinery (`crossrung_series/path1_tau/crossrung_lib.py`).
Identify every additional real rung pair extractable from on-disk structural-series
data — candidates, subject to data availability:

- cancer **pathway→hallmark** (a distinct pair from the measured molecular→pathway);
- fMRI **region→network**;
- C. elegans **neuron→functional-class**.

For each pair with data on disk, measure the cross-rung / within-rung coupling
ratio with the same pre-registered method as Path 1. Report per pair.

## Pre-registered verdict

- **$O(1)$ holds:** the coupling ratio at the new rung pairs stays $O(1)$
  (order $0.3$–$3$) → the cross-rung corridor claim (Claim 6) is anchored at
  $n>2$ distinct rung pairs; §sec:crossrung's n=2 caveat is relieved in
  proportion to the pairs added.
- **$O(1)$ breaks:** a new rung pair sits decisively at $g/J \ll 1$ (Simon
  near-decomposability) or $g/J \gg 3$ → the $O(1)$ reading is rung-pair-specific,
  not general; report which pair and the value.

This concerns the coupling-**ratio** form only. The canonical **timescale** form
remains measured at no substrate (§sec:crossrung) and is out of scope here.

## Discipline

Real structural-series data on disk only — no synthetic data. A rung pair whose
data cannot be located is reported MISSING, not fabricated. Incremental output.
Verdict flat — a broken-$O(1)$ result is as reportable as a confirmation.
