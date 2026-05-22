# Robust re-run — Substrate 4: OSS contribution — pre-registration

**Date:** 2026-05-21. **Written before inspecting any v1 verdict.** Paper v2,
`papers/Corridor Dynamics.tex` §sec:corridor-empirical, Substrate 4.

## What this substrate is — and is NOT

OSS contribution is a **non-ρ substrate**. There is no correlation matrix, no
z-scoring, no phase-randomized surrogate, no debiased ρ. The wave
pre-registration (`../PREREGISTRATION.md`, S4/S5 paragraph) states explicitly
that the debiased-ρ upgrade **does not apply here**.

The OSS metric is a **proxy for regime position**: a single-author-dominance
weekly fraction built from per-week commit-author distributions. It is reported
AS a proxy, never as a ρ measurement. The corridor concepts (rigidity / chaos /
corridor) are mapped onto commit-authorship concentration, which is a
defensible operationalization but a proxy nonetheless.

## The robust upgrade for this substrate

Per the wave pre-registration: for a non-ρ proxy substrate the robust framing
is (a) pre-registering thresholds before looking, (b) stating the proxy
explicitly as a proxy, (c) checking the v1 verdict survives that discipline.
It is **not** a debiased-ρ recomputation. This file delivers (a) and (b);
RESULTS.md delivers (c).

## Data

Real GitHub REST API commit history, fetched 2026-05-19, 15 repositories
(10 JSON files in the v1 worktree `data/`; some files hold two aliases via the
fork's shared early history). Each commit record: `{sha, author, date}`.
Source of record:
`.../agent-aed109995f1888fa3/experiments/noncorr_oss/data/*.json` and
`results/01_fetch_summary.json`. No synthetic data; no data added or removed
relative to v1.

15 aliases in 3 pre-assigned classes:
- **Rigidity-pole candidates** (single-committer dominance expected): R1 jquery,
  R2 colors.js orig (Marak), R2b colors.js fork (DABH), R3 faker-js successor,
  R4 left-pad mirror (stevemao).
- **Chaos-pole / hostile-fork candidates**: C1a Audacity orig, C1b Tenacity
  fork, C2a Elasticsearch orig, C2b OpenSearch fork, C3a CyanogenMod, C3b
  LineageOS.
- **Corridor controls**: K1 Kubernetes, K2 Rust, K3 Django, K4 Redis.

Class assignment is fixed by documented project history (BDFL status,
foundation backing, hostile-fork events) and is not revised by the metric.

## Proxy definitions (fixed before re-run)

Per repo, group commits by ISO-week and by author. For each active week
(>= 1 commit):
- `S1` = top-1 author's share of that week's commits.
- `n_authors` = distinct authors that week.

Per-segment proxy metrics (segment = lifetime, or pre-/post-event split at the
documented event date, or trailing 104 weeks):
- **`rigid_w`** = fraction of active weeks with `S1 >= 0.80` (one author wrote
  >= 80% of that week's commits). Proxy for rigidity-pole occupation.
- **`multi_w`** = fraction of active weeks with `n_authors >= 5`. Proxy for
  corridor-style distributed authorship.

These are the v1 definitions (`02_compute_corridor_metrics.py`,
`03_period_analysis.py`). They are re-stated here, unchanged, as the
pre-registered proxy — the robust upgrade is declaring them in advance and
labelling them as a proxy, not redefining them.

## Active maintenance γM(t) — documented, not computed

Each alias carries a documented active-maintenance flag set (foundation
backing, corporate sponsorship, BDFL, public rescue event, dependency bot)
from incident reports and project history. AM is **documentary evidence**, not
a metric. "Heavy maintenance" = any AM flag present that constitutes ongoing
institutional γM(t) (foundation, corporate, or active community-org backing).

## Three-mode classification rubric (fixed before re-run)

A non-corridor repo (rigidity- or chaos-class) is assigned exactly one mode:

- **Mode (i)** — non-corridor occupation AND no active maintenance AND short
  functional lifetime (project dormant: trailing window inactive / `silence_w`
  large). Framework-consistent (γM(t) removed → dissolution).
- **Mode (ii)** — non-corridor occupation AND documented active maintenance
  γM(t), repo still active. Framework-consistent (maintenance cost visible).
- **Mode (iii)** — non-corridor occupation (rigid commit pattern) AND no
  identifiable active maintenance AND long persistence while still active.
  **This mode falsifies the corridor-as-attractor reading at the OSS
  substrate.**

A repo whose proxy returns it to corridor occupation after a rescue
(`rigid_w <= 0.50` and `multi_w >= 0.50` post-event) is recorded as
**back-in-corridor**, not as a non-corridor mode.

## PASS / FAIL / BLOCKED

- **PASS** — v1's three-mode finding reproduces under this discipline: the
  proxy metrics recomputed from raw data match v1 within rounding, the
  rigidity / corridor proxy bands are distinguishable
  (median `rigid_w` rigidity-class clearly above corridor-class; median
  `multi_w` clearly below), and **Mode (iii) count = 0**.
- **FAIL** — Mode (iii) count >= 1 (a long-lived, actively-developed,
  unmaintained, rigid-pattern repo), or the proxy bands for rigidity vs
  corridor class are not distinguishable.
- **BLOCKED** — raw commit data cannot be located or re-read.

## Pre-registered expectation

v1 reported: Mode (i) 4/15, Mode (ii) 7/15, Mode (iii) 0/15, with the
remaining repos either corridor controls or back-in-corridor rescues. We
expect this to reproduce exactly, because the proxy is a deterministic
function of the raw data and the v1 computation is being re-executed, not
re-specified. If it does not reproduce, that is the finding.
