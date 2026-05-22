# Per-substrate corridor-band calibration — pre-registration

**Date:** 2026-05-21. **Addresses:** the open "per-substrate corridor
calibration" / cross-substrate "consistency-of-bounds" question
(`papers/Corridor Dynamics.tex` §sec:engineering, §sec:open).

## Why

The 2026-05-21 structural series and robust re-run measured debiased ρ at
multiple coordinated substrates. Those distributions are on disk. This
experiment characterises, per substrate, the band that healthy / in-corridor
operation occupies, and asks whether the bands cluster across substrates or are
substrate-specific.

## Scope — stated honestly

This calibrates the **static band**: where healthy operation's debiased ρ sits.
It does **not** calibrate the corridor-as-attractor dynamical bounds (the ρ at
which dρ/dt changes regime) — those require per-substrate dρ/dt, measured so far
only at the GPU substrate. The static band yields a *first estimate* of the
corridor centre ρ_mid and half-width w; tightening these to true attractor
bounds is gated on per-substrate dρ/dt and is not claimed here.

## Method

Gather the healthy / in-corridor debiased-ρ distributions already computed:
fMRI (`data_fmri/`), TCGA healthy tissue (`data_tcga/`), C. elegans, Drosophila,
EEG-interictal (`robust_rerun/`), LLM internals (`exp_E1_llm_corridor.py`), GPU.
OSS and social are non-ρ proxy substrates and are excluded.

Per substrate report: ρ_mid (median), IQR, [p5, p95]; band half-width
w ≈ (p95 − p5)/2; effective k_eff range the band implies via the Kish identity.

## Pre-registered cross-substrate read

- **Bounds cluster:** the per-substrate ρ_mid values fall within a factor of ~2
  of each other and the w values are comparable — a cross-substrate corridor
  with a shared centre is supported as a first estimate.
- **Substrate-specific:** ρ_mid spans more than a factor of ~2 — the corridor is
  substrate-local in centre, not just in mechanism; report the per-substrate
  values as the calibration and the spread as the result.

Either way, report the pooled ρ_mid and w as the first empirical estimate of
P_ω's master parameters, flagged as static-band estimates.

## Discipline

Analysis only on debiased-ρ values already computed and on disk — no new data
collection, no synthetic data. If a substrate's per-unit ρ values cannot be
located, report it MISSING and proceed with the rest. Incremental output.
