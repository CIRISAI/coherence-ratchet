# Results — corridor-exit rate from the paired Mode-(i) record

Extraction run 2026-05-21, against the criteria pre-registered in
`PREREGISTRATION.md` (committed 2026-05-21, commit 01b4287, before this file).

## Headline

**The paired non-corridor record classifies Modes but does not record
extractable per-case unmaintained non-corridor lifetimes. No corridor-exit
rate is extractable from it.** This is the pre-registered honest negative.

Zero of the five paired substrates yields a Mode-(i) case that passes all four
inclusion criteria. The crux finding the task anticipated — the paper's wording
"short lifetime where observed" being qualitative — is confirmed, and the
failure is sharper than that wording alone suggests: in addition to the cases
that carry no number, several substrates' Mode-(i) cases carry numbers that
measure the wrong quantity, and the LLM substrate's one numeric non-corridor
case is a Mode-(ii) case, not Mode (i).

## Per-substrate extraction

Criteria (from PREREGISTRATION.md): (1) per-case real-unit number; (2) it is
the lifetime of the non-corridor STATE, not of the system; (3) maintenance
absent/removed for the interval; (4) the non-corridor regime independently
established for that case.

### Neural — CHB-MIT seizures (`noncorr_biology/NOTES.md`)

Mode-(i) cases: 6 generalized seizures, chb01. Per-case durations recorded:
**27, 40, 51, 90, 93, 101 s** (median 70.5 s). Maintenance: recorded during
anti-epileptic-medication washout — maintenance genuinely removed.

- Criterion 1 — PASS. Six per-case durations in seconds.
- Criterion 2 — PASS. The duration is the ictal-episode duration; the ictal
  state is the candidate non-corridor state, and it self-terminates.
- Criterion 3 — PASS. Drug-resistant epilepsy, recorded during AED washout.
- **Criterion 4 — FAIL.** The NOTES measured ictal whole-brain |ρ| at mean
  0.316 (PLV 0.305) — *inside* the corridor band, never reaching the rigidity
  threshold. Verbatim: *"ictal whole-brain |rho| stays in the corridor band ...
  the framework's quantitative rigidity-pole-entry reading of seizures is not
  supported by this metric."* The seizure was *predicted* non-corridor but
  *measured* in-corridor. Its 70.5 s is therefore the lifetime of an
  in-corridor episode, not a corridor-exit time. No exit occurred.

Verdict: numeric, but FAILS criterion 4. Not a corridor-exit datum.

### Cellular regulatory — TCGA tumor tissue (`noncorr_cancer/NOTES.md`)

Mode-(i) cell in the paper's Figure 2: **"N/A (no off-treatment cohort)."**

- Criterion 1 — FAIL. TCGA is cross-sectional bulk RNA-seq: one expression
  vector per tumor, no time axis. There is no duration of any kind to extract.

Verdict: no time axis at all. Not a corridor-exit datum.

### LLM internals — Qwen2.5-1.5B mode-collapse (`noncorr_tech/NOTES.md`)

Two numeric facts about the non-corridor LLM state exist:
(a) the one clear non-corridor state, collapse-2 ("a b a b" greedy), crosses
the rigidity threshold |ρ|>0.7 at ≈ token 80 of a 200-token run;
(b) the paper's Figure 2 Mode-(i) cell reads *"non-greedy or non-periodic
input: |ρ| stays in corridor"*.

- For (b): criterion 1 FAIL — the Mode-(i) "observation" at the LLM substrate
  is precisely that those runs *stay in corridor*. There is no exit, hence no
  exit time. It is a no-event, not a short-lifetime event.
- For (a): criterion 1 PASS (token-80 crossing, on the substrate-intrinsic
  token axis), criterion 4 PASS (|ρ|→0.71, regime independently established).
  **Criterion 3 — FAIL.** The NOTES are explicit that greedy decoding *is* the
  active maintenance: *"γ·M(t) at the LLM substrate IS something like 'argmax +
  repetitive input pattern' combined"*, and the three-modes verdict for this
  case is *"Reading (ii) is the best fit"* — the non-corridor state is
  maintained, not unmaintained. The token-80 crossing is the onset of a
  Mode-(ii) state, not a Mode-(i) lifetime. The trajectory is *AWAY* from
  corridor for the full 200-token runway; no decay, hence not even an upper
  bound on an unmaintained lifetime.

Verdict: the no-exit cases are qualitative; the one numeric exit is Mode (ii),
fails criterion 3. Not a corridor-exit datum.

### OSS contribution — 15 repos (`noncorr_oss/NOTES.md`)

Mode-(i) cases (4/15): colors.js original (228 weeks dormant), left-pad mirror
(375 weeks), CyanogenMod (492 weeks), DABH colors.js fork (91 weeks dormant).
These numbers are *silence_w* — weeks since last commit, ref date 2026-05-19.

- Criterion 1 — PASS (numeric, in weeks).
- **Criterion 2 — FAIL.** `silence_w` is time-since-last-commit: it measures
  how long an *already-dead* project has stayed dead, with no defined endpoint
  (the count grows by one each week the repo stays dormant). It is not the
  duration of a live non-corridor state. PREREGISTRATION.md exclusion criterion
  explicitly names this: *"a 'time since last commit / dormancy' count ...
  measures how long a dead project has been dead, not the duration of a live
  non-corridor state, and has no defined endpoint."* The OSS NOTES record no
  per-case interval between non-corridor *entry* (single-committer dominance
  setting in) and non-corridor *exit* (dissolution); the rigid_w / multi_w
  metrics are lifetime fractions, not dated transitions.

Verdict: numeric, but the number is a dormancy count, FAILS criterion 2. Not a
corridor-exit datum.

### Social groups — cults and leaderless movements (`noncorr_social/NOTES.md`)

Rigidity-pole T_persist: Jonestown 23.0 yr, Heaven's Gate 23.0 yr, NXIVM 20.0
yr, Aum/Aleph 39.0 yr. Chaos-pole T_persist: Occupy 0.2 yr, Tahrir 1.5 yr.

- Criterion 1 — PASS (numeric, in years).
- **Criterion 2 — FAIL.** T_persist is defined in the source as founding-to-
  dissolution of the *organisation*. The NOTES do not establish that the group
  occupied the non-corridor regime for that entire span; ρ_analog is an
  investigator-assigned ordinal (the NOTES say so: *"the rho_analog ordinal is
  investigator-assigned from qualitative source readings, not measured"*) with
  one value per group, not a dated trajectory. There is no measured non-corridor
  *entry* date, so the duration of the non-corridor *state* cannot be isolated.
- **Criterion 3 — FAIL (independently).** All four rigidity groups score AM
  (active-maintenance checklist) ∈ {4,4,5,5} — heavy documented maintenance for
  the whole span. The pre-registered Mode-(i) rubric cell (rigidity, T≤50 yr,
  AM≤1) had **0 of 4** cases. By the social NOTES' own three-modes rubric,
  zero rigidity cases are Mode (i). The chaos cases (Occupy, Tahrir) have AM=0
  but T_persist is again the organisation span, not a measured non-corridor-
  state lifetime (fails criterion 2), and re-corridorization — not corridor
  *exit-to-dissolution* — is what the NOTES document for both.

Verdict: numeric, but FAILS criteria 2 and 3. Not a corridor-exit datum.

## Summary table

| Substrate | Mode-(i) numbers in record | Crit 1 | Crit 2 | Crit 3 | Crit 4 | Usable? |
|-----------|----------------------------|:------:|:------:|:------:|:------:|:-------:|
| Neural    | seizure durations 27–101 s | PASS | PASS | PASS | **FAIL** | No |
| Cellular  | none (cross-sectional)     | **FAIL** | — | — | — | No |
| LLM       | token-80 rigidity crossing | PASS | PASS | **FAIL** | PASS | No |
| OSS       | dormancy 91–492 weeks      | PASS | **FAIL** | n/a | n/a | No |
| Social    | T_persist 0.2–39 yr        | PASS | **FAIL** | **FAIL** | n/a | No |

0 / 5 substrates yield a usable unmaintained-non-corridor lifetime.

## Why this is the honest negative, not a measurement failure of this run

Each substrate fails for a structural reason, not for want of effort here:

- **The numbers that exist measure the wrong quantity.** Seizure durations are
  in-corridor episode lengths (the predicted pole-entry was not observed).
  OSS dormancy counts are how long a corpse has lain. Social T_persist is an
  organisation's whole life, not a dated non-corridor interval.
- **The one numeric corridor exit (LLM, token 80) is a maintained exit.** Greedy
  decoding is the maintenance; it is a Mode-(ii) onset. An *unmaintained*
  corridor-exit rate is exactly what is not in the record.
- **The paired record was designed as a Mode *classifier*, not a *rate meter*.**
  Its pre-registered persistence measure at every substrate is "short / long"
  against a threshold, plus a qualitative maintenance checklist. It answers
  "Mode (i), (ii) or (iii)?" — a category — and answers it well (Mode (iii)
  absent at 5/5). It was never instrumented to record the *entry time* and
  *exit time* of a non-corridor state on a common clock, which is what a rate
  needs. The paper's own phrase "short lifetime where observed" is, on
  inspection of the data behind it, a category label: "observed to be short"
  relative to a threshold, with no per-case unmaintained-state duration.

## What condition 2 needs instead

A corridor-exit rate independent of the CMB shape-drift definition requires a
*new* time-series measurement, not re-mining the paired record:

1. A substrate where ρ (or its analog) is measured *as a trajectory* through
   the corridor boundary, with a clean non-corridor *entry* event and a clean
   *exit* event (dissolution, self-termination, or corridor return) on the same
   clock, with maintenance verifiably absent for the interval.
2. The substrate's intrinsic timescale independently measured, so the rate can
   be reported dimensionless (`r / r_intrinsic`) — without which the rate
   cannot be transported toward a cosmological scale.

Neither the paired non-corridor datasets nor the failed LLM-greedy attempt
(`experiments/open_system_pomega/corridor_exit_rate_llm.py`) supplies this. The
honest status of condition 2: **the corridor-exit rate has not been measured at
any substrate, and the framework's existing paired record cannot supply it.**
The "real path" note in the failed LLM script — "the paired non-corridor data
records Mode-(i) cases with OBSERVED LIFETIMES, the exit rate is ≈ 1/lifetime"
— is, on direct inspection of that data, **not available**: the lifetimes it
refers to are qualitative Mode labels and wrong-quantity numbers, not
extractable per-case unmaintained non-corridor durations.

## Provenance

Every datum above is quoted or counted from:
- `.../agent-a5a5cfc9f224f29b0/experiments/noncorr_biology/NOTES.md`
- `.../agent-ae618976841275d76/experiments/noncorr_cancer/NOTES.md`
- `.../agent-adac93ab2d2bdd8ba/experiments/noncorr_tech/NOTES.md`
- `.../agent-aed109995f1888fa3/experiments/noncorr_oss/NOTES.md`
- `.../agent-ab3971bf4bb503603/experiments/noncorr_social/NOTES.md`
- `papers/Corridor Dynamics.tex` §sec:corridor-empirical, §sec:paired-validation
  (Figure 2 paired-validation matrix).

No lifetime was fabricated or inferred from a qualitative label.
