# Shadow 2 — timescale-locking shadow (classical g/J) — RESULTS

Two-sided, pre-registered. NULL is a valid result. This file's operational
definitions (§1) were written and committed **before** any g/J number was
computed; the verdict (§3) was appended afterward. Git history is the proof.

Pre-registration: `PREREGISTRATION.md` (this directory).

---

## 1. Operational definitions — FIXED BEFORE THE NUMBERS

The test: a coordinated group with internal relaxation time `J`, facing an
environment demanding adaptive response at rate `g`, survives in-corridor only
if `g/J ≈ O(1)`. We measure `J` and `g` identically for surviving (in-corridor)
and failed (out-of-corridor) groups, compute `g/J`, and ask whether `g/J`
separates the prior corridor label.

### 1.1 The PRIOR label (not a new measurement)

The corridor / non-corridor label is the v1 classification from
`papers/Corridor Dynamics.tex` §sec:corridor-empirical (the ρ-proxy + the
active-maintenance checklist). It is **not** derived from g or J. g/J is a
genuinely new measurement and therefore a genuine test.

- **OSS (15 repos).** In-corridor = the four stable foundation-backed controls
  K1 kubernetes, K2 rust, K3 django, K4 redis (paper: within-rung
  `|Δρ| ≤ 0.10`, all stable rungs inside (0.10,0.43)). Out-of-corridor = the 11
  pole-event repos: rigidity pole — R1 jquery, R2 colors_orig, R2b colors_dabh,
  R3 faker_succ, R4 leftpad; chaos pole — C1a audacity_orig, C1b tenacity_fork,
  C2a elastic_orig, C2b opensearch_fork, C3a cm_orig, C3b lineage_fork. Repos
  are labelled by the *pole event*, per the paper's line-280 three-pole split,
  not by their post-rescue current state.
- **Social (9 groups).** In-corridor = `pole == corridor`: K1 Quakers,
  K2 Trappists, K3 Mennonites. Out-of-corridor = `pole in {rigidity, chaos}`:
  R1 Jonestown, R2 Heaven's Gate, R3 NXIVM, R4 Aum/Aleph, C1 Occupy,
  C2 Tahrir Coalition.

### 1.2 J — internal relaxation time

The autocorrelation time of the group's coordination signal.

- **OSS.** The coordination signal is the **weekly commit-count series** over
  the on-disk window (`results/02_weekly_series.json`, regular weekly grid,
  zero-filled for inactive weeks). `J` = integrated autocorrelation time of the
  mean-subtracted weekly series, in **weeks**:
  `J = 1 + 2·Σ_{k≥1} r(k)`, summed until the first `r(k) ≤ 0` (initial
  positive sequence), where `r(k)` is the lag-`k` Pearson autocorrelation.
  Interpretation: how many weeks the contribution rhythm "remembers" — the
  relaxation time of internal coordination. `J ≥ 1` by construction.
- **Social.** The coordination signal is the **organisational decision /
  response cycle**: the documented interval between binding collective
  decisions. `J` is read in **years** from documented governance:
  corridor groups — distributed consensus governance with a named periodic
  body (e.g. Quaker Yearly Meeting ~1 yr; Trappist General Chapter every 3 yr;
  Mennonite congregational/conference cycle ~1 yr); rigidity groups — the
  leader's directive cycle, treated as effectively continuous / very short
  (single-voice command, `J → small`); chaos groups — the assembly /
  consensus-process cycle (Occupy GA daily-to-weekly; Tahrir coalition
  ad-hoc). Values are coded from the dataset's documented governance, stated
  as a coded proxy.

### 1.3 g — external environmental shift rate

The rate at which the environment forces an adaptive response.

- **OSS.** Proxy (stated as a proxy): the **regime-change rate** of the
  project's activity — the count of active⇄dormant transitions of the weekly
  series per year of observed span. An active⇄dormant transition is a crossing
  of the median-activity threshold sustained ≥4 weeks. Rationale: a project
  re-coordinating (entering or leaving an activity regime) is the on-disk
  footprint of the project responding to an external ecosystem shift (a
  dependency break, a security advisory, a downstream-demand surge, a
  governance change). `g` is in **transitions per year**.
  *Limitation, stated up front:* the only on-disk signal is the commit series
  itself; a fully independent ecosystem-churn series (npm/crates/PyPI
  dependency-break dates) is not on disk. The regime-change rate is the
  least-circular external proxy extractable from on-disk data — it counts
  *changes of regime* (response events), not raw commit volume (which feeds J).
  This circularity risk is logged and weighed in the verdict.
- **Social.** Proxy: the **rate of major external political-environment shifts**
  the group was exposed to per decade of its existence — wars, regime changes,
  legal/regulatory shocks, host-society upheavals documented in the dataset's
  `ended_or_status` / sources. `g` is in **shifts per year**, coded from the
  documented record, stated as a coded proxy.

### 1.4 The quantity and the verdict rule

`g/J` is dimensionless within each substrate (both in the substrate's natural
time unit — weeks for OSS, years for social). Per the pre-registration:

- **PASS** — in-corridor (surviving) groups cluster at `g/J ~ O(1)` (≈ 0.3–3)
  AND out-of-corridor (failed) groups do not.
- **NULL** — `g/J` does not separate corridor from non-corridor.

n is small (15 OSS + 9 social = 24). Reported honestly; no over-claim.

---

## 2. Measured values

<!-- appended by 02_measure_gj.py — incremental -->

## 3. Verdict

<!-- appended after §2 is complete -->
