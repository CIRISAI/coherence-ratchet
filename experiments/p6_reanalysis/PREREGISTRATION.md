# P6 re-analysis — three-regime corridor in public qubit decoherence-sweep data — pre-registration

**Date:** 2026-05-22. A **weak-proxy** test of P6, honestly labelled — not the
clean decisive test.

## Context

P6 (corridor-boundary dynamics) predicts a goal-coupled substrate, swept on a
control parameter, exhibits the three-regime structure — rigidity (k_eff → 1),
corridor (bounded k_eff), chaos (k_eff → n). The *decisive* test is Exp 5
(Conjecture A): a new programmable-qubit-array experiment sweeping decoherence
rate γ. This is **not** that. This is a re-analysis of *already-published*
qubit decoherence-sweep data — the one P6 move available from public data. It
is a weak proxy: it inherits whatever the published experiment measured and
carries observable-choice caveats. Reported as a proxy, not as Exp 5.

## The observable

k_eff = 1 / Tr(ρ²) — the inverse purity / participation ratio of the measured
density matrix, the canonical quantum corridor observable Conjecture A specifies.
For an n-qubit system k_eff ∈ [1, 2ⁿ]: k_eff → 1 is rigidity (pure / single
effective state), k_eff → 2ⁿ is chaos (maximally mixed).

## Method

1. Find genuine **published, empirical** quantum-hardware data in which a
   decoherence or control parameter is swept and the density matrix (or enough
   to reconstruct purity) is measured — process/state tomography over a sweep,
   open quantum-hardware characterization datasets, paper supplementary data.
2. Compute k_eff = 1/Tr(ρ²) as a function of the swept control parameter.
3. Test for the three-regime structure: is there a control-parameter regime in
   which k_eff is bounded *away from both* the rigidity floor (≈1) and the chaos
   ceiling (≈2ⁿ) — a corridor — and does the Kish identity fit that regime
   (R² > 0.5)?

## Three-way verdict

- **PASS:** a genuine three-regime corridor — a bounded-k_eff regime off both
  poles, Kish-identity fit R² > 0.5. The corridor structure appears at the
  quantum substrate in public data (a weak-proxy positive for P6).
- **NULL:** k_eff runs monotonically from rigidity to chaos with no bounded
  corridor regime — no three-regime structure.
- **BLOCKED:** no suitable published empirical dataset (control-parameter sweep
  + tomography/purity) is found — report exactly what was searched.

## Discipline

Real **published empirical** data only. **No synthetic data, and no substituting
a quantum-simulator sweep** — simulating a Lindblad decoherence sweep is not a
re-analysis, it changes the experiment; if no empirical dataset is found, BLOCKED
is the honest outcome. The canonical observable is k_eff = 1/Tr(ρ²) — fixed here,
not chosen post hoc. This is a weak proxy for Exp 5 and is reported as one.
Two-sided; NULL and BLOCKED are valid results. Incremental output.
