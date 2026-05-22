# P_ω — the R1 ∧ R2 conjunction — results

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.
**Pre-registration:** `R1xR2_conjunction/PREREGISTRATION.md` (committed before
this run). **Build:** `build_R1xR2.py` (reuses `build_history_pomega.py`,
R2's sequential-emergence simulator). **Raw:** `results_R1xR2.json`,
`run_R1xR2.log`.

---

## VERDICT: EMPTY — H2 fails (the joint functional dilutes)

The R1 ∧ R2 conjunction — R1's genuinely non-additive joint Kish
participation-ratio functional, carried on R2's open sequential history-space
frame, with the proven within-rung corridor cap (k_eff ≈ 10 per rung)
re-injected — **horns EMPTY**. The joint effective dimensionality runs to the
chaos pole with depth: `ρ_joint` falls as `R^-1.09`, the band lower edge 0.10
is crossed downward at R ≈ 5–6, and the ω-set is empty (no all-emerged history
in band) from R = 13. This is **R1's dilution mechanism recurring** — the
mutually-curing hypothesis failed. Per the binding terminal commitment, **F-11
fires**: the multi-rung backward P_ω is a documented no-go across the additive
ansatz, R1, R2, R3, and the R1 ∧ R2 conjunction. There are no further
conjunctions. The line is drawn here.

Reported flat, per the pre-registration. EMPTY is a valid two-sided result.

---

## The construction

**Frame (from R2), reused unchanged.** `build_history_pomega.py` —
universe trajectories, rungs Ph0…A5 emerging sequentially over cosmic time,
each rung's within-rung ρ_n(t) evolving by Piece 2 dynamics
`dρ/dt = α − γM` and held in its corridor by active management. The all-emerged
sub-ensemble is the histories the post-selection acts on.

**Functional (from R1), with the pre-registered dilution cure.** R1's object
verbatim — the Kish-inverse of a participation ratio `(Tr C)²/Tr(C²)` — with
the one change the pre-registration mandates. R1 built `C_joint` over the
**raw constituents** K = R·m, so the Kish "constituent count" blew up with
depth and `ρ_joint ~ 4/K → 0`. The pre-registration's re-injected proven
constraint: the within-rung corridor caps each rung's k_eff ≈ 10, so the joint
object's constituents are the **R corridor-capped rungs**, not the R·m raw
spins. The joint correlation object is the R×R **rung-level** correlation
matrix `C_w`:

- diagonal 1 (each rung a unit);
- adjacent off-diagonal = the cross-rung correlation read off the trajectory —
  how corridor-aligned rung n was at the step rung n+1 emerged (R2's
  sequential-emergence timing coupling, the signal R2's Test B found);
- non-adjacent 0 (nearest-neighbour topology kept — the conjunction drops
  R1's assumptions 2 and 3 and R2's 4 and 8, not assumption 5);
- each rung row/column scaled by `√w_n`, `w_n = soft(ρ_n at t_f)` — the
  re-injected within-rung corridor cap as a soft TSVF post-selection factor.

The ω-weight: `k_eff_joint = (Tr C_w)²/Tr(C_w²)`,
`ρ_joint = (R/k_eff_joint − 1)/(R − 1)` (Kish inverse on the **rung count R**),
`log w_ω = log smooth_band_indicator(ρ_joint)`.

**Why it is framework-faithful, not reverse-engineered.** The functional is
R1's Kish participation ratio; Piece 1 (Kish), the participation-ratio reading
of k_eff (NOTES / exp5), Piece 3 (the band) — nothing invented. The only change
from R1 is the re-injection named explicitly in the pre-registration. The
functional was fixed before the run; it was not re-chosen to chase a verdict.
The construction is genuinely two-sided — `ρ_joint` is a ratio of traces of one
matrix, so it could equally have stayed bounded (H2 holds) or factorized
(H1 fails). It did neither cleanly: H2 failed.

CUDA throughout (cupy 13.6.0, RTX 4090, float64). Per-depth progress printed;
results flushed to `results_R1xR2.json` after every rung-depth; resume from
on-disk partials **verified before the long run** (dropped R=5 from the JSON,
re-ran, confirmed R=3,4 skipped and R=5 recomputed bit-identical). Total
runtime 831 s; depths 3–20, N up to 20 M histories.

---

## The three hypotheses

| R  | ρ_joint(ps) | ρ_joint(max) | k_eff(ps) | in-band frac | shuffle_gap | gap/rung |
|----|-------------|--------------|-----------|--------------|-------------|----------|
| 3  | 0.1694 | 0.974 | 2.26 | 0.736 | 0.1071 | 0.0357 |
| 4  | 0.1286 | 0.773 | 2.91 | 0.475 | 0.0789 | 0.0197 |
| 5  | 0.1007 | 0.379 | 3.60 | 0.221 | 0.0692 | 0.0138 |
| 6  | 0.0810 | 0.271 | 4.31 | 0.075 | 0.0659 | 0.0110 |
| 7  | 0.0670 | 0.302 | 5.03 | 0.022 | 0.0574 | 0.0082 |
| 8  | 0.0568 | 0.200 | 5.77 | 0.006 | 0.0534 | 0.0067 |
| 9  | 0.0498 | 0.148 | 6.48 | 0.0022 | 0.0500 | 0.0056 |
| 11 | 0.0402 | 0.152 | 7.90 | 0.00005 | 0.0609 | 0.0055 |
| 13 | 0.0339 | 0.0996 | 9.30 | **0.0000** | 0.0458 | 0.0035 |
| 20 | 0.0228 | 0.0503 | 14.03 | **0.0000** | 0.0355 | 0.0018 |

### H2 — no dilution (the cure for R1): **FAILS**

`ρ_joint(ps)` falls monotonically: 0.169 → 0.101 (R=5) → 0.050 (R=9) →
0.034 (R=13) → 0.023 (R=20). It crosses the band lower edge 0.10 downward at
R ≈ 5–6 — **before the framework's 9 rungs**. The post-selected ensemble's
joint correlation is **chaos-side at R=9** (0.050, half the band floor). The
band-reachability extreme `ρ_joint(max)` clears the floor to R = 11 and is
unreachable (`n_in_band = 0`) from **R = 13** out to R = 20. `k_eff_joint`
runs *up* monotonically and passes the framework's k_eff ≈ 10 ceiling at R = 13.

The decisive diagnostic: a power-law fit gives **`ρ_joint(ps) ~ R^-1.09`**, and
`ρ_joint(ps)·R` is roughly constant (0.51, 0.45, 0.46 at R = 3, 9, 20). This is
**R1's `ρ_joint ~ const/K → 0` dilution law**, recurring at the rung level. The
corridor-cap re-injection changed the *constant* (R1's raw-spin functional hit
the floor at R ≈ 12 for the best-case tower; here the corridor-capped rung
functional's post-selected mean clears the floor only to R ≈ 5, the best-case
to R ≈ 11) — but it did **not** change the **law**. The functional still
dilutes to the chaos pole.

Mechanism, confirmed by the same arithmetic R1 documented: the rung-level
matrix `C_w` has unit diagonal and only adjacent off-diagonal entries, so
`Tr(C_w) ≈ R` while `Tr(C_w²) ≈ R + (cross terms) ≈ R + cR`. Then
`k_eff_joint ≈ R²/((1+c)R) = R/(1+c)` grows linearly in R, and
`ρ_joint = (R/k_eff − 1)/(R−1) ≈ c/(R−1) → 0`. The within-rung corridor cap
shrinks `c` (it down-weights rungs and caps the cross entries) but cannot make
`c` grow with R — and only a `c` growing with R would hold `ρ_joint` off the
floor. Re-indexing the joint object from raw spins to rungs replaced K with R
in the same dilution formula; it did not escape it. The chaos-pole dilution is
**structural to the joint participation ratio of any locally-coupled tower**,
whatever the granularity of the "constituents."

### H1 — non-decomposability (the cure for R2): **also fails**

The segment-shuffle gap does **not** grow with R — it **falls**:
0.107 (R=3) → 0.069 (R=5) → 0.050 (R=9) → 0.046 (R=13) → 0.036 (R=20). Per-rung
it falls an order of magnitude, 0.036 → 0.0018. The H1 criterion (gap real
**and growing with R**, unlike R2's flat-near-zero) is not met: the gap is real
but **shrinking**. The non-additive functional does carry *some* joint
structure the shuffle destroys at low R — more than R2's additive weight, whose
gap was ≈ 0 — but that structure dilutes away exactly as the dilution sets in.
Once `ρ_joint` is pinned near the chaos floor, the smooth-band-indicator weight
is flat (its argument is far below the band), every history scores the same
near-zero weight, and shuffling rungs changes nothing. H1's decomposability
question is moot under H2's failure: a functional that has diluted to a
constant is trivially decomposable.

### H3 — joint work: moot (H2 forecloses it)

The cross-rung structure is non-inert at low R (`cross_delta_mean` 0.085 at
R=3, the joint weight responds to turning the cross entries off) and the band
is selective where it is reachable. But H3 requires the joint object
**non-empty** and well-defined to 9 rungs, and it is empty at 9 (in-band frac
0.0022, effectively zero) and exactly empty from 13. There is no joint object
left to do work on. `cross_delta` itself dilutes with depth (0.085 → 0.011),
tracking the same `1/R` decay.

---

## Verdict against the pre-registration

The three-way verdict:

- **OPENS** requires H1 ∧ H2 ∧ H3. H2 fails; H1 fails. Not OPENS.
- **EMPTY** is H2 failing — the joint functional dilutes to the chaos pole
  even on the corridor-capped sequential frame. **This is what happened.**
- **TRIVIAL** is H1 failing while H2 holds. H1 also fails, but H2's failure is
  the primary, decisive one (the shuffle gap is moot once the functional has
  diluted to a constant). The verdict is **EMPTY**, with the note that H1 would
  not have rescued it either.

**EMPTY fires F-11** per the binding terminal commitment.

---

## Honest assessment — is R1 ∧ R2 the genuine P_ω form?

No. **The conjunction horns too**, and it horns on R1's side.

The pre-registration's hypothesis was that R1's failure (dilution under raw
K → ∞) and R2's failure (additive-weight factorization) are *mutually curing*:
R2's frame caps each rung at k_eff ≈ 10 and so removes R1's raw-K blow-up;
R1's non-additive functional removes R2's additive factorization. The run shows
**the cure does not hold**. The reason is precise and was visible in R1's own
diagnosis: R1 did not dilute *because* it used raw constituents — it diluted
because the joint Kish participation ratio of **any locally-coupled tower**
obeys `ρ_joint ~ c/(count − 1)`, where the count is whatever you take the
joint object's constituents to be. R1's count was R·m; the conjunction's count
is R. Smaller, so the constant is friendlier and the floor is hit later — but
the *law* is `1/count`, and `count` still grows with depth. The corridor cap
re-injection is a multiplicative down-weighting of the matrix; it cannot
manufacture the `count`-growing off-diagonal mass that would be needed to hold
`ρ_joint` bounded. R1's control already showed what would: an **all-to-all**
coupled tower does not dilute — but that is dropping the nearest-neighbour
topology (assumption 5 / R4), which the conjunction, like R1, explicitly keeps.

So the conjunction inherits R1's dilution because the dilution was never
specific to additivity *or* to raw-constituent indexing — it is the trace-ratio
structure of `k_eff` meeting locality. R2's history frame supplied a genuine
open sequential object and a real (if weak) timing coupling, but it cannot
change the arithmetic of the participation ratio. The two failures are **not**
mutually curing; they are, with R3's antagonism, three faces of one obstruction:
the multi-rung joint corridor object, built faithfully to the framework's
k_eff, its band, and its nearest-neighbour rung topology, **cannot be
simultaneously non-empty, non-diluting, and non-factorizing as depth grows to
the framework's rung count.**

This is the EMPTY horn — the same horn the hard-projector dead zone (3 models)
and R1 returned, by the dilution route. It is reached here by a construction
the audit specifically built to escape it, holding every framework constraint.
That is the strongest available statement of the no-go.

**Scope — unchanged from R1 and R2.** Touched: the multi-rung *joint backward*
P_ω, the object D1 (Penrose past) and asymptotic conditioning post-select
through. **Not** touched: the within-rung corridor (F-10, single-rung,
empirically supported on five A3+ substrates), the engineering tier, or the
soft *forward* P_ω (ρ_ss, the open-system Lindblad steady state, which exists
and is non-empty independently — it is not a joint participation ratio and does
not dilute). F-11's firing is specific to the multi-rung joint backward
construction, the universal-scale tier's open formal step.

**Limits of this construction.** (1) The cross-rung entry is the
soft-corridor-scaled timing coupling; a different cross-rung observable would
change the constant `c` but not the `1/R` law (the law is the diagonal-dominant
structure of `C_w`, which any nearest-neighbour rung matrix has). (2) m = R2's
simulator's within-rung resolution; the rung-level functional is m-independent
by construction (the rungs are the constituents). (3) The all-to-all escape is
real but is assumption 5 / R4 — out of scope for R1 ∧ R2, and the
pre-registration's terminal commitment forbids pursuing it: R4 and the further
conjunctions are the combinatorial regress, and the line is drawn.

---

## Bottom line for the audit

**R1 ∧ R2 horns — EMPTY.** The non-additive joint Kish functional on the open
sequential history frame, with the within-rung corridor cap re-injected,
dilutes to the chaos pole exactly as R1 did: `ρ_joint ~ R^-1.09`, band floor
crossed at R ≈ 5–6, ω-set empty from R = 13 — before and past the framework's
9 rungs. The mutually-curing hypothesis is refuted: R2's corridor-capped frame
does not escape R1's dilution, because the dilution is the trace-ratio
arithmetic of the Kish participation ratio under locality, not an artifact of
raw-constituent indexing. H1 also fails (the shuffle gap shrinks with R rather
than growing), but H2's dilution is the decisive horn.

Per the binding terminal commitment in the pre-registration: **F-11 fires.**
The multi-rung backward P_ω is a documented no-go across the additive ansatz,
R1, R2, R3, and the R1 ∧ R2 conjunction. There are no further conjunctions —
R1∧R3, R1∧R2∧R3, R4 — that is the combinatorial regress, and the line is drawn
here. v2's §sec:open-research records the no-go. The within-rung corridor, the
engineering tier, and the forward open-system P_ω are untouched.
