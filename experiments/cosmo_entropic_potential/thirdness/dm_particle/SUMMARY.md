# Prediction 4 — the copula-Third on the dark-matter particle field: NO DETECTION

**Date 2026-07-22.** The prenup's unrun prediction 4, and the decisive test of whether a
physical Third exists in the matter field at all. Method frozen in `DECISIONS.md` before any
number was seen. Estimator identical to `thirdness/measure_thirdness.py` with both K4 fixes
baked in (**random** tie-breaking, not `argsort∘argsort`; **CIC** primary).

## What was run

Full **94,196,375 DM particles**, IllustrisTNG **TNG100-3 snapshot 99 (z = 0)**, box 75 Mpc/h,
streamed via HTTP Range requests and reduced on the fly to count grids (nothing stored at
particle level). Density ladder spanning **four decades**: random subsamples at
f = 4.3e-4 → 1.0, i.e. **n̄ = 0.019 → 359 particles/cell**, on CIC ng=64, CIC ng=128 and NGP
ng=64, each against four pre-committed nulls — N1 lognormal-Poisson (**primary shot null**;
a lognormal is a monotone transform of a Gaussian so its copula is *exactly* Gaussian, and
whatever copula-skew it shows at finite n̄ **is** the discreteness contribution), N1a
clipped-Gaussian-Poisson, N0 continuous phase-randomized (must give ~0), N2 cell-shuffle
(must give ~0).

## The decisive result — the signal is a function of the empty-cell fraction

CIC ng=128, verdict scale R = 2.93 Mpc/h:

| n̄ (per cell) | 0.019 | 0.045 | 0.135 | 0.450 | 1.347 | 4.490 | 13.47 |
|---|---|---|---|---|---|---|---|
| **empty-cell fraction** | 0.915 | 0.844 | 0.684 | 0.422 | 0.174 | 0.024 | 0.000 |
| **copula skew** | +0.504 | +0.411 | +0.287 | +0.171 | +0.108 | +0.088 | +0.040 |

NGP ng=64 reaches full density: at **n̄ = 359, skew = +0.0039** — consistent with zero.
The copula-Third is a **monotonic function of the empty/tied-cell fraction**, not of anything
physical. This independently reproduces, on a completely different dataset and across four
decades, the tied-fraction law inferred from the `copula_stress` and macaque re-nulls.

## Pre-registered verdict: **(c) AMBIGUOUS** by the letter — **NO DETECTION** in content

| criterion | NGP ng=64 | CIC ng=128 |
|---|---|---|
| monotone decline | **True** | **True** |
| \|G_N1\| < 3 at top two densities (no excess over shot null) | **True** (−1.92, −0.44) | **True** (−0.55, −0.27) |
| \|G\| > 5 vs BOTH shot nulls (a detection) | False | False |
| saturation to a plateau (a genuine Third) | **False** | **False** |
| A_inf (extrapolated asymptote) | −0.031 ± 0.008 (3.8σ) | −0.053 ± 0.014 (3.8σ) |
| decline exponent p (pure Poisson ⇒ 0.5) | 0.414 ± 0.013 | 0.275 ± 0.014 |

**There is no significant excess over the shot null at any density**, the signal declines
monotonically toward zero, and it never saturates to a positive plateau. Prediction 4 is
answered, and the answer is **no**.

It misses a clean "(a) pure shot artifact" only on two counts, both of which point away from
coordination: the decline exponent is **slower than pure Poisson** (p ≈ 0.28–0.41 vs 0.5), and
the extrapolated asymptote is **negative** (−0.03 to −0.05 at 3.8σ) — the wrong sign for
coordination. Both read as residual estimator/extrapolation systematics, not signal. Recorded
as AMBIGUOUS because that is what the frozen rule returns; the content is no detection.

## Both readings

- **No physical Third (the evidence).** This was the measurement that could have found it —
  the true matter field, full resolution, the estimator's own preferred statistic, both K4
  fixes applied. Nothing above shot noise anywhere. The Third remains **empirically
  unobserved**, now on the field itself rather than a sparse tracer.
- **Not a clean null (honesty).** p ≠ 0.5 and A_inf < 0 at 3.8σ are unexplained. They are the
  wrong sign to be the Third, but they are not nothing, and a future estimator audit should
  account for them rather than wave them off.

## Scope

One simulation, one redshift (TNG100-3, z=0). The formal object (`Core/Thirdness.lean`) and
the DPI un-forgeability (`Core/TriadicChannel.lean`) are untouched — neither ever depended on
a cosmic measurement. Per the prenup this closes prediction 4 / kill K4's remaining leg; the
`S`/pairwise-shadow results are unaffected (K4 was staked as separable).

**Note:** `analyze.py` raises `KeyError: 'snap'` in its final print after the verdicts compute
— a reporting-line bug, not a result bug. Numbers in `results.json`.
