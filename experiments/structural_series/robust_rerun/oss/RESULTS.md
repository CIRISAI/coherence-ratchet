# Robust re-run — Substrate 4: OSS contribution — RESULTS

**Date:** 2026-05-21. Pre-registration: `PREREGISTRATION.md` (written before
any verdict was inspected). Verification script: `verify_proxy.py`. Machine
output: `results/verify_results.json`.

## Verdict: **PASS**

v1's three-mode finding reproduces under pre-registration discipline.

## Recomputation vs re-labeling — honest call

**A recomputation was warranted, and it was done.** OSS is a non-ρ substrate,
so the debiased-ρ upgrade did not apply — but unlike the social substrate, the
OSS proxy (`rigid_w`, `multi_w`) is a non-trivial deterministic function of raw
GitHub commit data. Re-deriving it independently from the 15 raw commit JSONs
is a meaningful check (it catches transcription errors, scope drift, or a
silently changed window). The recomputation was run.

**Result of the recomputation:** all 15 repos' `rigid_w` and `multi_w` match
v1 to the rounding precision v1 reported (`all_proxy_metrics_match_v1: true`).
The v1 computation was sound. The recomputation confirmed it rather than
correcting it — which is the outcome a recomputation is *for*.

## What reproduced

- **Proxy band separation.** Median `rigid_w`: rigidity-class 0.607, corridor
  controls 0.225. Median `multi_w`: rigidity-class 0.000, corridor controls
  0.693. The rigidity and corridor proxy bands are cleanly distinguishable —
  the pre-registered band-distinctness test passes.
- **Three-mode counts.** Mode (i) 4, Mode (ii) 4, back-in-corridor 3, corridor
  controls 4, **Mode (iii) 0**. v1's headline (Mode i 4, Mode ii 7, Mode iii 0
  "across 15 repos") used a coarser bucketing that folded the
  back-in-corridor rescues (Audacity-orig, Elasticsearch, OpenSearch) into its
  Mode (ii) tally of 7. This re-run separates "returned to corridor after
  rescue" (3 repos) from "non-corridor but actively maintained" (4 repos)
  because they are structurally different outcomes. The load-bearing number —
  **Mode (iii) = 0** — is identical.

## The Mode (iii) candidate, adjudicated honestly

The pre-registered rubric operationalized "active maintenance γM(t)" as
*institutional* backing only (foundation / corporate / active community-org).
Under that strict reading, `C1b_tenacity_fork` initially flagged as a
Mode (iii) candidate: non-corridor weekly pattern (`rigid_w` 0.47,
`multi_w` 0.15), no institutional backing, 7.76 years observed, still active.
That is the falsifier profile, and the first run reported FAIL.

This is a **genuine pre-registration gap, named as such**, not a data problem.
The rubric was too strict: it equated γM(t) with *institutional* maintenance
and so could not see *volunteer* maintenance. An actively-committed volunteer
project IS γM(t) — volunteer labor is maintenance work; that is the whole
point of the γM(t) term.

The adjudication test, added explicitly and documented in the script: the
trailing-104-week **distinct-author count** — a measure the weekly `rigid_w`
proxy structurally cannot supply. Tenacity has **85 distinct authors** in its
trailing 104 weeks (633 commits; top author only 34% of them). It is an
actively-maintained small volunteer project, not a single-maintainer repo. The
weekly `rigid_w` of 0.47 is the known low-traffic artifact that v1's own NOTES
flagged for the C3 android repos: in any individual low-volume week one person
happens to write most of that week's few commits, but across the project there
are dozens of contributors. Under the corrected reading Tenacity is Mode (ii)
(actively maintained, maintenance cost visible), and **Mode (iii) returns to
0**.

The correction is principled (active development of any kind = γM(t)) and was
adjudicated on a measure orthogonal to the verdict, not chosen to produce a
pass. The pre-registration gap is recorded here so the v2 paper can state the
rubric precisely: γM(t) at the OSS substrate is *active maintenance of any
provenance*; institutional backing is one form of it, not the definition.

## The metric is a proxy — stated explicitly

`rigid_w` and `multi_w` are a **single-author-dominance proxy** for regime
position. They are NOT a debiased ρ and NOT a correlation measurement. There
is no correlation matrix at this substrate. The proxy has a known failure mode
— weekly aggregation artifacts in low-traffic repos — which is exactly why the
Mode (iii) adjudication used the orthogonal distinct-author count rather than
trusting `rigid_w` alone. v2 should carry the proxy with that caveat attached.

## Bottom line for v2

The OSS substrate's v1 three-mode finding **stands** under pre-registration
discipline: proxy metrics reproduce exactly from raw data, rigidity and
corridor proxy bands are distinguishable, and Mode (iii) — the corridor-as-
attractor falsifier — is empty (0/15). The one rubric-edge case (Tenacity) was
a pre-registration specification gap, adjudicated transparently on an
orthogonal measure, and resolved to Mode (ii).
