# P_ω — the R1 ∧ R2 conjunction — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12. **Status:** an
author-authorized **protocol extension** of the assumption audit — not a
continuation. Two-sided, with the terminal commitment below.

## Why this is the one conjunction

The single-assumption audit found three horns by three *distinct* mechanisms:

- **R1** (non-additive corridor functional, but static/simultaneous): HORNED by
  chaos-pole **dilution** — the joint participation ratio ran ρ_joint ~ 4/K → 0
  with depth, under nearest-neighbour locality and raw constituent count K → ∞.
- **R2** (history-space / sequential frame, but additive weight): HORNED by
  **factorization** — the joint log-weight `Σ_n log soft(ρ_n)` is additive,
  exponentiates to a product, decomposes (segment-shuffle gap ≈ 0).
- R3 (derived cross-rung): HORNED by within/cross **antagonism** — a separate
  geometric mechanism.

R1's failure and R2's failure are **mutually curing**: R2's frame (sequential
emergence, each rung maintained inside its within-rung corridor, which caps
k_eff ≈ 10) removes the raw-K→∞ dilution that killed R1; R1's non-additive
functional removes the additive-weight factorization that killed R2. R3's
mechanism is not curative of either and is not in scope. **R1 ∧ R2 is therefore
the one principled conjunction** — the others (R1∧R3, R2∧R3, …) are the
combinatorial regress and are explicitly out of scope.

## The construction

A non-additive corridor functional carried on the open, sequential
history-space frame:

- **Frame (from R2):** simulate universe trajectories — rungs emerging
  sequentially over cosmic time, each rung's within-rung ρ_n(t) maintained in
  its corridor after emergence (Piece 2 dynamics). Reuse `R2_history`'s
  `build_history_pomega.py` simulator.
- **Functional (from R1):** the ω-weight is **not** `Σ_n log soft(ρ_n)`. It is
  a genuinely non-additive functional of the trajectory's *joint* rung
  structure — the joint Kish participation ratio / k_eff of the joint
  rung-correlation across the trajectory (the R1 object, evaluated on the
  history rather than a static config). It must not decompose into a sum of
  per-rung terms.

## Re-injected proven constraints

- The within-rung corridor **caps k_eff ≈ 10** (Kish asymptotic + corridor;
  band calibration this session). The joint functional must be evaluated with
  each rung corridor-capped — this is the structure hypothesised to prevent R1's
  dilution.
- Rungs emerge **sequentially** (Piece 6 timescales) — the frame is open, new
  degrees of freedom per emergence.
- Cross-rung coupling is **O(1)** (measured, n=3 this session).

## Hypotheses under test

- **H1 — non-decomposability (cures R2):** the non-additive functional does not
  factorize. Segment-shuffle gap is real **and grows with R** — not flat near
  zero as in R2.
- **H2 — no dilution (cures R1):** the joint effective dimensionality stays
  bounded with depth — the corridor-capped sequential frame prevents the joint
  participation ratio running to the chaos pole.
- **H3 — joint work (OPENS):** given H1 and H2, the joint object is non-empty,
  selective, genuinely couples the trajectory (R2's Test-B timing coupling now
  *reaches the weight*), and is well-defined to the framework's 9 rungs.

## Three-way verdict

- **OPENS:** H1 ∧ H2 ∧ H3 — non-empty, non-decomposable (shuffle gap grows),
  non-diluting (joint k_eff bounded), selective, well-defined to 9 rungs. Then
  P_ω is constructed: a non-additive corridor functional on the open sequential
  history is the genuine form. F-11 does not fire.
- **EMPTY:** H2 fails — the joint functional dilutes to the chaos pole even on
  the corridor-capped sequential frame.
- **TRIVIAL:** H1 fails — the non-additive functional on the history still
  factorizes under segment-shuffle.

## Terminal commitment (binding)

This is the **final** P_ω construction. If the verdict is OPENS, P_ω is
constructed and v2 records it. If EMPTY or TRIVIAL, the multi-rung backward P_ω
is a documented no-go across the additive ansatz, R1, R2, R3, and the R1 ∧ R2
conjunction — **F-11 fires**, v2's §sec:open-research records it, and there are
**no further conjunctions** (R1∧R3, R1∧R2∧R3, …): that is the combinatorial
regress, and the line is drawn here.

## Discipline

- CUDA mandatory (cupy). The build script **must** print per-depth progress,
  flush interim results to JSON after each depth, and **resume from on-disk
  partial results** — verified before the run, not after.
- Two-sided: EMPTY or TRIVIAL is a valid, reportable result that fires F-11.
- The non-additive functional must be a genuine framework object (the joint
  Kish/participation-ratio functional), not reverse-engineered to OPEN. If the
  construction finds itself tuning the functional to a wanted verdict, it stops
  and reports that.
