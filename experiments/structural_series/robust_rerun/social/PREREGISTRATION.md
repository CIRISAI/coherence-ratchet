# Robust re-run — Substrate 5: social groups — pre-registration

**Date:** 2026-05-21. **Written before inspecting any v1 verdict.** Paper v2,
`papers/Corridor Dynamics.tex` §sec:corridor-empirical, Substrate 5.

## What this substrate is — and is NOT

Organized social groups are a **non-ρ substrate**. There is no correlation
matrix, no time series, no z-scoring, no debiased ρ. The wave pre-registration
(`../PREREGISTRATION.md`, S4/S5 paragraph) states explicitly that the
debiased-ρ upgrade **does not apply here**.

The social-substrate instrument is a **qualitative checklist**: an
active-maintenance (AM) score from 0 to 5, plus a coarse ordinal `rho_analog`
(1–5) assigned from documented governance structure, plus a persistence time
`T_persist` in years from documented founding/dissolution dates. None of these
is a ρ measurement. `rho_analog` is a hand-assigned ordinal label, NOT a
correlation; it is reported as such and is not load-bearing for the verdict.

## The robust upgrade for this substrate

Per the wave pre-registration: for a non-ρ qualitative substrate the robust
framing is (a) pre-registering thresholds before looking, (b) stating the
checklist status explicitly as a qualitative instrument (not a ρ
measurement), (c) checking the v1 verdict survives that discipline. It is
**not** a debiased-ρ recomputation. This file delivers (a) and (b);
RESULTS.md delivers (c).

## Data

9 social groups, real historical record (founding dates, leadership history,
membership figures, dissolution events) compiled in the v1 worktree from
documented public sources (`01_compile_dataset.py` header cites the BITE-model
literature, PSIA reports, denominational records). Source of record:
`.../agent-ab3971bf4bb503603/experiments/noncorr_social/results/dataset.csv`
and `dataset.json`. No synthetic data.

3 pre-assigned classes:
- **Rigidity** (R1–R4): Peoples Temple/Jonestown, Heaven's Gate, NXIVM, Aum
  Shinrikyo/Aleph.
- **Chaos** (C1–C2): Occupy Wall Street encampment phase, Tahrir / Coalition
  of Youth of the Revolution.
- **Corridor** (K1–K3): Quakers, Trappists, Mennonites.

## Instrument definitions (fixed before re-run)

- **`T_persist`** — years from documented founding to documented
  dissolution, or to 2026 if ongoing.
- **`AM_total`** — count (0–5) of documented active-maintenance practices:
  AM1 required charismatic leader, AM2 escalating commitment rituals,
  AM3 information control, AM4 defection punishment, AM5 financial sunk-cost
  coercion. Each flag is a documentary boolean from the public record.
- **`LD`** — months from leader removal to group dissolution (rigidity class
  only); null if the group persists past leader removal.
- **`rho_analog`** — ordinal 1–5, hand-assigned governance label. Reported
  for completeness; **not** used in any PASS/FAIL test.

These are the v1 definitions, re-stated unchanged. The robust upgrade is
declaring them in advance and labelling the instrument as a qualitative
checklist, not redefining it.

## Pre-registered hypothesis tests (fixed before re-run)

- **H1** — corridor-class median `T_persist` >= 250 years.
- **H2** — rigidity-class median `T_persist` <= 50 years.
- **H3** — chaos-class median `T_persist` <= 5 years.
- **H4** — rigidity-class leader-dependence: `LD` <= 24 months in >= 3 of 4
  rigidity groups.
- **H5** — every rigidity-class group with non-trivial persistence carries
  `AM_total >= 3` (heavy maintenance present wherever a non-corridor group
  persists at all).

## Three-mode classification rubric (fixed before re-run)

A non-corridor (rigidity- or chaos-class) group is assigned one mode:

- **Mode (i)** — non-corridor AND `AM_total <= 1` AND short persistence.
  Framework-consistent.
- **Mode (ii)** — non-corridor AND `AM_total >= 3`, persisting with the
  maintenance cost visible. Framework-consistent.
- **Mode (iii)** — non-corridor AND `AM_total <= 1` AND long persistence
  (`T_persist > 50` years). **This mode falsifies the corridor-as-attractor
  reading at the social substrate.**

## PASS / FAIL / BLOCKED

- **PASS** — v1's three-mode finding reproduces: H1–H5 all hold,
  **Mode (iii) count = 0**, and the four-orders-of-magnitude persistence
  spread between corridor and non-corridor classes is present.
- **FAIL** — Mode (iii) count >= 1, or any of H1–H5 fails such that the
  three-mode pattern no longer holds.
- **BLOCKED** — the dataset cannot be located or re-read.

## Pre-registered expectation

v1 reported: 5/5 hypothesis tests PASS, 0 Mode-iii, persistence spread of
four orders of magnitude (corridor median 374y vs chaos median ~0.83y). We
expect this to reproduce, because the instrument is a deterministic function
of the documented dataset and we are re-executing, not re-specifying it. If
it does not reproduce, that is the finding.
