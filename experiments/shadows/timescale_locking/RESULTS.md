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

Computed by `02_measure_gj.py`; raw values in `results_gj.json`.

**Dimensional note.** `J` is a *time* (weeks for OSS, years for social) and `g`
is a *rate* (per year). The dimensionless quantity that expresses "environmental
demand `g` comparable to the internal relaxation rate `1/J`" is the **lock
number `g·J`** (= `g / (1/J)`). The pre-registration writes "g/J"; the O(1)
test is the same quantity once `J` is correctly a time. We report `g·J` and
apply the pre-registered O(1) band [0.3, 3] to it. This is a notation
clarification, not a redefinition of the test or the band.

### 2.1 OSS (15 repos), `J` in weeks, `g` in transitions/year

| repo | label (prior) | J (wk) | g (/yr) | g·J |
|------|---------------|-------:|--------:|----:|
| K1 kubernetes | corridor | 13.84 | 0.654 | 0.174 |
| K2 rust | corridor | 5.05 | 0.870 | 0.085 |
| K3 django | corridor | 118.61 | 0.104 | 0.236 |
| K4 redis | corridor | 47.02 | 0.618 | 0.559 |
| R1 jquery | noncorridor | 66.68 | 1.029 | 1.319 |
| R2 colors_orig | noncorridor | 2.96 | 0.259 | 0.015 |
| R2b colors_dabh | noncorridor | 2.89 | 0.211 | 0.012 |
| R3 faker_succ | noncorridor | 11.23 | 1.396 | 0.302 |
| R4 leftpad | noncorridor | 1.93 | 0.200 | 0.007 |
| C1a audacity_orig | noncorridor | 18.41 | 0.735 | 0.260 |
| C1b tenacity_fork | noncorridor | 17.03 | 1.546 | 0.506 |
| C2a elastic_orig | noncorridor | 1.22 | 5.882 | 0.138 |
| C2b opensearch_fork | noncorridor | 3.25 | 0.877 | 0.055 |
| C3a cm_orig | noncorridor | 2.55 | 0.762 | 0.037 |
| C3b lineage_fork | noncorridor | 3.75 | 0.749 | 0.054 |

- In-corridor (n=4): g·J = {0.085, 0.174, 0.236, 0.559}; median **0.205**.
- Out-of-corridor (n=11): g·J = {0.007, 0.012, 0.015, 0.037, 0.054, 0.055,
  0.138, 0.260, 0.302, 0.506, 1.319}; median **0.055**.
- In O(1) band [0.3, 3]: in-corridor **1/4**; out-of-corridor **3/11**.

### 2.2 Social (9 groups), `J` in years, `g` in shifts/year (coded proxy)

| group | label (prior) | J (yr) | g (/yr) | g·J |
|-------|---------------|-------:|--------:|----:|
| K1 Quakers | corridor | 1.0 | 0.05 | 0.050 |
| K2 Trappists | corridor | 3.0 | 0.04 | 0.120 |
| K3 Mennonites | corridor | 1.0 | 0.05 | 0.050 |
| R1 Jonestown | noncorridor | 0.02 | 0.30 | 0.006 |
| R2 Heaven's Gate | noncorridor | 0.05 | 0.20 | 0.010 |
| R3 NXIVM | noncorridor | 0.05 | 0.40 | 0.020 |
| R4 Aum / Aleph | noncorridor | 0.10 | 0.50 | 0.050 |
| C1 Occupy | noncorridor | 0.02 | 4.00 | 0.080 |
| C2 Tahrir Coalition | noncorridor | 0.08 | 2.00 | 0.160 |

- In-corridor (n=3): g·J = {0.050, 0.050, 0.120}; median **0.050**.
- Out-of-corridor (n=6): g·J = {0.006, 0.010, 0.020, 0.050, 0.080, 0.160};
  median **0.035**.
- In O(1) band [0.3, 3]: in-corridor **0/3**; out-of-corridor **0/6**.

## 3. Verdict

### VERDICT: NULL

`g·J` does not separate the corridor / non-corridor prior label, and
in-corridor groups do **not** cluster in the O(1) band [0.3, 3]. The
pre-registered PASS condition — in-corridor at g·J ~ O(1) AND out-of-corridor
not — fails on both halves.

**OSS.** There is a weak *direction*: the in-corridor median (0.205) sits above
the out-of-corridor median (0.055), and all four in-corridor repos exceed the
out-of-corridor median. But (a) the populations overlap heavily — four
out-of-corridor repos (R1 1.32, C1b 0.51, R3 0.30, C1a 0.26) lie at or above
the in-corridor range, and (b) **neither** population is centred in the O(1)
band: only 1/4 in-corridor repos and 3/11 out-of-corridor repos fall in
[0.3, 3]. The in-corridor cluster sits an order of magnitude *below* O(1)
(~0.08–0.56). The PASS condition requires in-corridor *clustering at O(1)*;
the in-corridor cluster is at ~0.2, and out-of-corridor repos are *more*
likely to land in the O(1) band than in-corridor ones. No PASS.

**Social.** No separation at all: in-corridor median 0.050 vs out-of-corridor
median 0.035, fully overlapping, and 0/9 groups in the O(1) band. The social
g·J is dominated by the coded-proxy choices for J and g (§1.2–1.3) and the
absolute scale is therefore not interpretable; the most that can be read is
that the lock number, as coded, carries no corridor signal.

### Honest assessment

1. **Is the cross-rung timescale ratio measurable classically?** Partially.
   `J` (the autocorrelation time of the contribution series) is a clean,
   non-circular on-disk measurement for OSS — it ranges over two orders of
   magnitude (1.9 wk for left-pad to 119 wk for django) and is a genuine
   internal-relaxation-time read. `g` is the weak link: the regime-change
   rate is a *stated proxy* (RESULTS.md §1.3) extracted from the same commit
   series, so it is not fully independent of J, and no independent
   ecosystem-churn series is on disk. For social, both J and g are
   hand-coded proxies. So: the *internal* timescale is classically
   measurable; the *external* timescale, at these substrates, is not, with
   on-disk data alone.

2. **Does it land in the O(1) band?** No. The OSS in-corridor lock numbers
   cluster around ~0.2, an order of magnitude below O(1). If anything the
   data hints that the corridor sits *below* O(1) on this proxy, not at it —
   but with n=4 in-corridor and a proxy-dependent `g`, that is not a claim,
   only the absence of the predicted O(1) clustering.

3. **What this NULL means.** This is a genuine two-sided NULL, not a failed
   measurement: `J` was measured cleanly and the prior labels were never used
   to set g or J. The NULL says the classical macroscopic shadow of the
   cross-rung timescale ratio, *as operationalised here*, does not reproduce
   the O(1) timescale-locking prediction and does not discriminate corridor
   from non-corridor groups. The most likely methodological reason is the
   `g` proxy: the regime-change rate is a coarse and partly-circular stand-in
   for true environmental shift rate. A cleaner test would require an
   independent external-churn series (dependency-break dates for OSS;
   a coded political-shock timeline validated against an external source for
   social). Until such a series exists, the cross-rung timescale ratio g/J
   is **not** shown to be classically measurable in a way that lands in the
   O(1) band. The quantum route (w3) was observable-blocked; this classical
   route returns NULL. The cross-rung *coupling ratio* (Path 1) remains the
   only O(1) cross-rung result; the cross-rung *timescale ratio* is, after
   this shadow, still unmeasured.

4. **n.** 15 OSS + 9 social = 24, with only 4 + 3 = 7 in-corridor. Small.
   No quantitative claim is made beyond the medians and band counts above.

