# Allen mouse visual cortex — canonical k_eff re-test — pre-registration

**Date:** 2026-05-21. **Owed by:** `papers/Corridor Dynamics.tex` §sec:robust-rerun
("the k_eff re-test on the same data is owed").

## Why

The 2026-05-21 structural series measured Allen mouse visual cortex (25 two-photon
sessions, spontaneous epoch) at mean pairwise neuron ρ ≈ 0.023 — a chaos-pole
reading. But the framework's canonical shape observable is **not** the mean
pairwise correlation: it is the participation-ratio k_eff of the activity
covariance. Cortex is the named case where the two diverge — cortical population
activity is well documented as low-dimensional (low participation ratio) despite
low pairwise correlation. The chaos-pole datum may therefore be an
observable-choice artifact. This re-test settles it.

## Method

Same Allen data as the structural-series run (`data_allen/exp_allen_corridor.py`
locates it). For each session, on the spontaneous-epoch neuron × time activity
matrix, compute:

- `k_eff_emp` = participation ratio of the covariance eigenvalues,
  `(Σλ)² / Σλ²` — the canonical observable.
- For comparison: debiased ρ (phase-randomized surrogate floor) and the Kish
  `k_eff = N / (1 + ρ(N−1))`.

Report per session and aggregated; N = neuron count per session stated.

## Pre-registered verdict

- **Corridor:** `k_eff_emp` sits in a bounded range well below N and well above 1
  — cortex occupies the corridor on the canonical observable, and the
  mean-pairwise chaos-pole reading was an observable-choice artifact.
- **Chaos pole confirmed:** `k_eff_emp` ≈ N (within a small factor) — cortex
  genuinely sits at the chaos pole even on the canonical observable; a real
  chaos-pole substrate, and §sec:robust-rerun stands as written.

## Discipline

Real Allen data only — no synthetic data. Incremental output: write per-session
results as computed. If the data cannot be re-accessed, report BLOCKED with what
was tried. Verdict stated flat — a chaos-pole confirmation is as reportable as a
corridor result.
