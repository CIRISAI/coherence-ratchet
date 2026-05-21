# Pre-registration — corridor-exit rate from the framework's paired Mode-(i) record

Pre-registered 2026-05-21, BEFORE any extraction or numbers are stated.
Condition 2 of the computable cosmological time-to-fidelity: a corridor-exit-rate
calibration INDEPENDENT of the CMB shape-drift definition.

## The question

The framework's dynamics is `dρ/dt = α(ρ, S) − γ·M(t)` (CLAUDE.md Piece 2,
`formal/CoherenceRatchet/StructuralClaims.lean` Claim 1). The corridor-exit rate
is the rate at which a system, with active maintenance `γM` removed, leaves the
corridor. It has never been measured directly — only the static corridor band ρ
has been measured at the five paired substrates.

The framework's paired non-corridor work (CCA v3 / paired-substrate datasets,
`papers/Corridor Dynamics.tex` §sec:corridor-empirical, §sec:paired-validation)
classifies every non-corridor case into three modes:

- **Mode (i)** — non-corridor state, no active maintenance, **short lifetime**.
- **Mode (ii)** — non-corridor state, documented `γM`, persists.
- **Mode (iii)** — non-corridor state, no maintenance, persists long (falsifier;
  claimed absent at 5/5 substrates).

IF the Mode-(i) cases carry **quantitative observed lifetimes** — durations of
unmaintained non-corridor states, per case, in real physical units — then the
corridor-exit rate is `≈ 1 / lifetime`, extractable from already-collected data.

## What counts as a QUANTITATIVE lifetime (the inclusion criterion)

A datum qualifies as a quantitative Mode-(i) lifetime, usable for an exit rate,
ONLY IF all four of the following hold:

1. **Per-case real-unit number.** A numeric duration, in physical time units
   (seconds, days, years) or a substrate-intrinsic surrogate axis (generated
   tokens), attached to a specific named case — not a median quoted without the
   per-case values, not a verbal label.

2. **It is the lifetime of the NON-CORRIDOR state itself**, not of the system.
   The clock must start when the system enters the non-corridor regime (rigidity
   or chaos pole) and stop when it leaves it (dissolves, self-terminates, or
   returns to corridor). A founding-to-dissolution span of an *organisation* is
   NOT this number unless the organisation was measured to be in the non-corridor
   regime for that entire span.

3. **Maintenance is absent or removed for the measured interval** — this is what
   makes it a Mode-(i), not Mode-(ii), datum. If documented `γM` (life support,
   foundation funding, charismatic leader, greedy-decoding steering) was active
   during the interval, the case is Mode (ii) and the lifetime does not measure
   an unmaintained corridor-exit rate.

4. **The non-corridor regime is independently established for that case** — i.e.
   the paired record actually measured ρ (or its substrate analog) outside the
   corridor band for that case, OR the case is non-corridor by an independent,
   pre-registered structural criterion in the source NOTES. A case that was
   *predicted* non-corridor but *measured* in-corridor does not qualify (its
   "lifetime" would not be a corridor-exit time).

## What counts as a QUALITATIVE label (the exclusion criterion)

A datum is qualitative-only — NOT usable for an exit rate — if any of:

- It is the Mode classification itself ("Mode (i)", "short lifetime where
  observed") with no per-case number.
- It is a number, but for the system/organisation, not for the non-corridor
  *state* (fails criterion 2).
- The interval had documented active maintenance (fails criterion 3 — it is a
  Mode-(ii) datum).
- The case was measured inside the corridor band so there is no "exit" (fails
  criterion 4).
- It is a "time since last commit / dormancy" count — this measures how long a
  *dead* project has been dead, not the duration of a live non-corridor state,
  and has no defined endpoint (fails criterion 2).

## Extraction method (locked before extraction)

For each of the five paired substrates (neural / cellular / LLM / OSS / social):

1. Read the substrate's `noncorr_*/NOTES.md` results section.
2. List every case the NOTES classify as Mode (i).
3. For each, apply criteria 1–4 above. Record PASS or, if FAIL, which criterion
   it fails, with the verbatim source quote.
4. For PASS cases: record the per-case lifetime, its unit, and the exact source
   line. Corridor-exit rate `r = 1 / lifetime` in (1/unit).
5. Where the substrate has a known **intrinsic timescale** (e.g. a characteristic
   relaxation, oscillation, or turnover time independently measured), report the
   rate dimensionless as `r / r_intrinsic`. If no such intrinsic timescale is
   independently available, report the rate dimensional and say so — do NOT
   invent an intrinsic scale.

## Honesty constraints

- Real data only. Every extracted lifetime is traced to a source file + line.
- No lifetime is inferred from a qualitative Mode label. If the record says
  "short" without a number, that is qualitative — reported as such.
- No fabrication. If a substrate's Mode-(i) cases are all qualitative, that
  substrate yields no rate, stated plainly.
- A fully-qualitative outcome is a valid result: it tells the framework that
  condition 2 needs new time-series measurement, not the existing record.

## Pre-registered decision rule

- IF ≥1 substrate yields ≥1 PASS case → extract rates per substrate, report with
  provenance, dimensionless where an intrinsic scale exists.
- IF 0 substrates yield a PASS case → report the honest negative: "the paired
  record classifies Modes but does not record extractable per-case unmaintained
  non-corridor lifetimes; no corridor-exit rate is extractable from it."

## Data locations (sister-worktree paths, read-only)

- Neural: `.../agent-a5a5cfc9f224f29b0/experiments/noncorr_biology/NOTES.md`
- Cellular: `.../agent-ae618976841275d76/experiments/noncorr_cancer/NOTES.md`
- LLM: `.../agent-adac93ab2d2bdd8ba/experiments/noncorr_tech/NOTES.md`
- OSS: `.../agent-aed109995f1888fa3/experiments/noncorr_oss/NOTES.md`
- Social: `.../agent-ab3971bf4bb503603/experiments/noncorr_social/NOTES.md`
- Paper synthesis: `papers/Corridor Dynamics.tex` §sec:corridor-empirical.
