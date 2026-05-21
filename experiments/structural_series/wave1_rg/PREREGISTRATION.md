# PREREGISTRATION — Wave 1 RG: does the cross-rung OOM band constrain the dead-zone rung budget R*?

Pre-registered 2026-05-21, BEFORE results. Committed in a PRECEDING commit; git
history is the proof.

## Background

Two pieces of this session's work, to be confronted:

1. **Dead-zone RG tower** (`experiments/open_system_pomega/deadzone_rung_scaling.py`,
   `deadzone_rg_calibration.py`). A backward-soft P_omega
   `E_omega = exp(-beta * sum_n (rho_n - rho_c)^2)` survives a finite number of
   rungs R before the corridor penalty `h_min` exponentially suppresses it. The
   "rung budget" R* is the death rung (e^-1 soft weight). The calibrated value is
   **R* ≈ 25–56**. The calibration coordinate is the directly-measured `h_min`
   slope (≈ 0.00081/rung) on genuine RG-nested operators; the random-operator
   model reaches that slope at a non-commutativity knob value **ε ≈ 0.20**.

2. **Cross-rung coupling corridor** (`crossrung_series/path1_tau/RESULT.md`,
   Claim 6 in `formal/CoherenceRatchet/StructuralClaims.lean`). Real-data Path 1
   put the cross-rung/within-rung coupling RATIO at **g/J ∈ (0.3, 3)** — one OOM
   around parity g/J = 1.

ε ≈ 0.20 sits just below the OOM band's lower edge (0.3). Suggestive. The task
is to determine whether that proximity is meaningful.

## THE CRUX — assessment criterion: "is ε the cross-rung coupling g/J?"

ε and g/J are declared THE SAME KIND OF QUANTITY only if ALL of the following hold:

- **(C1) Same role in the model.** ε must parametrise the strength of
  *coupling between adjacent rungs* relative to *within-rung structure*. g/J is,
  by construction, exactly that ratio (`g·Σ Z Z` cross-rung term over `J`
  within-rung Heisenberg term).
- **(C2) Dimensional/structural commensurability.** Both must be dimensionless
  ratios of the SAME two physical scales (cross-rung vs within-rung), OR there
  must be an explicit, monotone, model-independent map ε ↔ g/J that is more than
  "both are dimensionless numbers near 0.2–3".
- **(C3) Shared mechanism.** The quantity ε controls in the dead-zone model
  (the `h_min` corridor penalty / rung-operator non-commutativity) must be the
  SAME mechanism that g/J controls in the cross-rung tower (the energy-scale
  ratio setting cross-rung mutual information τ).

If C1–C3 all hold → ε IS (or maps to) the cross-rung coupling. Proceed to the
recomputation step.

If ANY of C1–C3 fails → ε is NOT the cross-rung coupling. **Report that plainly.
"The OOM band does not constrain ε" is a valid honest outcome and the
experiment STOPS there** — no recomputation, honest negative.

### Prior expectation (stated before running, not binding)

Reading the two scripts: ε is the non-commutativity knob in `U_n = exp(i·ε·A_n)`
— it tunes how much adjacent rung *correlation operators* `rho_n` fail to
commute. The dead-zone model has NO within-rung Hamiltonian J at all (rungs are
abstract random Hermitian operators on a fixed shared Hilbert space). g/J is a
ratio of two Hamiltonian energy scales in a model with NO ε knob. The honest
prior is that C1 and C3 likely FAIL and this is an honest negative. The
pre-registered work is to VERIFY that against the actual code, not to assume it.

## IF ε is the cross-rung coupling — the recomputation

Only executed if C1–C3 pass.

- Restrict ε to the band-equivalent range — the sub-range of ε that corresponds
  to g/J ∈ (0.3, 3) under the C2 map.
- Recompute R* (the e^-1 death rung) using only ε values inside that range.
- Re-run the dead-zone rung scan (`deadzone_rung_scaling.py` machinery, reused —
  not rebuilt) restricted to the band.

### What a changed vs unchanged R* would mean

- **R* TIGHTENS** (narrower interval, e.g. the 25–56 spread shrinks): the OOM
  band excludes part of the ε range the original budget averaged over; the
  cross-rung corridor genuinely constrains the dead-zone budget. The two pieces
  of the framework lock together.
- **R* UNCHANGED** (still ≈ 25–56): the OOM-band-equivalent ε range already
  contains the operative ε ≈ 0.20, so the constraint is non-binding. Honest
  negative on "tighter R*", but a positive consistency check (the calibrated ε
  sits inside the band).
- **R* SHIFTS** (e.g. lower-bounded away from 25, or pushed up): the OOM band
  forces ε away from the calibrated 0.20; would indicate tension between the
  dead-zone calibration and the cross-rung corridor — reported as such.

## Discipline

- Real computation, GPU, reuse `deadzone_rung_scaling.py` machinery.
- Honest negative is a valid and expected outcome at the C1–C3 gate.
- Results written to `RESULT.md` in a commit AFTER this one.
