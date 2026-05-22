# Robust re-run — Substrate 5: social groups — RESULTS

**Date:** 2026-05-21. Pre-registration: `PREREGISTRATION.md` (written before
any verdict was inspected). Verification script: `verify_checklist.py`.
Machine output: `results/verify_results.json`.

## Verdict: **PASS**

v1's three-mode finding reproduces under pre-registration discipline.

## Recomputation vs re-labeling — honest call

**This was a re-labeling, not a recomputation, and that is the correct
outcome.** The social substrate is a non-ρ substrate. Its instrument is a
**qualitative checklist**: an active-maintenance score `AM_total` (0–5,
counted from five documentary booleans), a persistence time `T_persist` (years,
from documented founding/dissolution dates), and a leader-dependence lag `LD`
(months). None of these is a measurement that can be "re-derived" from a raw
signal — they are documentary values read off the public historical record.

There is no raw time series to recompute, no correlation matrix, no
phase-randomized surrogate, no debiased ρ. Manufacturing a "recomputation"
here would have been theatre. The honest robust upgrade for this substrate is
exactly what the wave pre-registration specifies: (a) pre-register the
thresholds before looking, (b) state the instrument explicitly as a
qualitative checklist rather than a ρ measurement, (c) check the v1 verdict
survives that discipline. That is what was done.

**The one genuine computation performed** is an internal-consistency check:
re-deriving `AM_total` from its five component booleans for all 9 groups.
Result: **all 9 consistent** (`AM_total_internally_consistent: true`). The
dataset's `AM_total` field is not a free-floating number; it equals the sum of
its documented components in every row.

## What reproduced

All five pre-registered hypothesis tests pass, re-run from the dataset:

| Test | Pre-reg threshold | Value | Verdict |
|------|-------------------|-------|---------|
| H1 corridor median `T_persist` | ≥ 250 y | 374 y | PASS |
| H2 rigidity median `T_persist` | ≤ 50 y | 23 y | PASS |
| H3 chaos median `T_persist` | ≤ 5 y | 0.83 y | PASS |
| H4 rigidity `LD` ≤ 24 mo | ≥ 3 of 4 groups | 3/4 (LD = 0, 0, 3, NA) | PASS |
| H5 rigidity `AM_total` ≥ 3 | all rigidity groups | 5, 4, 5, 4 | PASS |

Three-mode classification: Mode (i) 2 (C1 Occupy, C2 Tahrir — chaos, AM = 0,
short-lived), Mode (ii) 4 (R1–R4 — rigidity, AM ≥ 4, persisting with
maintenance cost visible), **Mode (iii) 0**. Framework-contradicting cases: 0
(no rigidity group with T > 100 y and AM ≤ 1; no chaos group with T > 20 y
unconsolidated).

## One honest correction to v1's narrative

v1's NOTES and the v1 paragraph in `Corridor Dynamics.tex` describe the
persistence spread as "four orders of magnitude" between corridor and
non-corridor populations. The corridor-vs-chaos **median** ratio is
374 y / 0.83 y ≈ 450×, i.e. **2.7 orders of magnitude**. The "four orders"
figure compares the corridor maximum (Mennonites, 501 y) against the chaos
minimum (Occupy, 0.17 y) ≈ 2950×, i.e. ~3.5 orders. Neither framing is wrong,
but they are different statistics. v2 should state the **median-to-median
spread of ~2.7 orders of magnitude** as the headline, with the extremes-ratio
noted separately if used. The qualitative finding — a very large,
unambiguous separation between corridor and non-corridor persistence — is
unaffected.

## The instrument is a qualitative checklist — stated explicitly

`AM_total` is a count of documented practices, not a ρ. `rho_analog` is a
hand-assigned ordinal governance label (1–5), not a correlation — it is
reported in the dataset for completeness and is **not used in any PASS/FAIL
test** in this re-run. `T_persist` is read from the historical record. The
verdict rests on documented persistence times and a documented maintenance
checklist, and v2 must carry it with that status attached: this is qualitative
historical evidence consistent with the three-mode reading, not a quantitative
ρ measurement.

## Bottom line for v2

The social substrate's v1 three-mode finding **stands** under pre-registration
discipline: all five hypothesis tests pass, `AM_total` is internally
consistent, Mode (iii) — the corridor-as-attractor falsifier — is empty (0/6
non-corridor groups), and no framework-contradicting case appears. The robust
upgrade was a re-labeling: pre-registration plus explicit qualitative-checklist
status. The only edit owed to v2 is the persistence-spread figure (2.7 orders
of magnitude median-to-median, not four).
