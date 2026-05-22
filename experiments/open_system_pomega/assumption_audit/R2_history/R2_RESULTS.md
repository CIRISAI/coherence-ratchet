# P_ω assumption audit — R2: history-space construction — results

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.
**Pre-registration:** `assumption_audit/PREREGISTRATION.md` (R2) and
`R2_history/PREREGISTRATION.md`. **Build:** `build_history_pomega.py` (stage-1
depth scan), `jointwork_test.py` (stage-2 decisive joint-work test).
**Raw:** `results_history.json`, `results_jointwork.json`.

## VERDICT: HORNS — trivial side

R2 dropped assumptions 4 and 8: P_ω built not as a static operator on a
simultaneous configuration space but as a boundary condition on the universe's
**trajectory** through sequential rung-emergence. The construction is non-empty
and well-defined to the framework's 9 rungs (and to 13). But the decisive test
shows the joint object **factorizes** — it does no genuine joint work.

## The three tests (R = 5, 9, 13)

- **Test A — flat control.** `sel(joint/flat)` = 0.285 / 0.257 / 0.190: the
  joint boundary's sequential-viability term (each rung in-band at its
  successor's emergence step) is a genuine extra constraint over a flat
  endpoint-only boundary, and tightens with depth. (A measures that the
  viability term is non-vacuous — not that it couples.)
- **Test B — adjacent emergence-gap correlation, prior → post-selected.**
  prior +0.07…−0.02 → post −0.11…−0.17. The ω-boundary induces a weak
  anti-correlation in adjacent rungs' emergence *timing* — a real but small
  coupling signal in the trajectory's pacing.
- **Test C — segment-shuffle (the decisive non-decomposability test).**
  `shuffle_gap` = −0.006 / +0.007 / +0.011; per-rung −0.0012 / +0.0007 /
  +0.0009 — flat near zero, not growing with R, sign-changing. Rebuilding
  histories by drawing each rung independently from the post-selected marginals
  reproduces the joint weight. **The joint object factorizes.**

Reconciliation: B finds a weak timing correlation; C finds the joint *weight*
decomposes. The decisive test horns. The stage-1 KL-growth
(`kl_joint_fact` 8.6 at R=9 → 21.9 at R=20) is hereby confirmed as the *trivial
additive accumulation* the test was built to catch — C's flat per-rung gap is
its signature.

## Diagnosed cause

R2's joint log-weight is `Σ_n log soft(ρ_n)` — **additive over rungs**. An
additive log-weight exponentiates to a product, and a product is decomposable
by construction. R2 dropped assumptions 4 and 8 but **kept assumption 2
(additive)**. The history-space frame did not escape the squeeze because the
weight stayed additive.

## Verdict against the pre-registration

OPENS requires non-empty AND genuine joint work AND well-defined to 9 rungs.
Non-empty ✓, well-defined to 9 (and 13) ✓, genuine joint work ✗ (Test C:
factorizes). Two of three needed; **HORNS**, trivial side.

## Audit status

R1 (non-additive) HORNS — chaos-pole dilution. R2 (history-space) HORNS —
factorization. R3 (derived cross-rung) HORNS — within/cross antagonism. Three of
three enumerated relaxations horn, each by a **distinct, characterized**
mechanism. Per the audit's terminal condition, F-11 fires at the
ansatz-independent level (R4 — topology — remains as a formality; the synthesis
showed it is closed-static and not framework-faithful, so it cannot close F-11).

**Observation, recorded as fact:** the three failures are *separable* — each
relaxation drops different assumptions and fails for a different reason. The
conjunction R1 ∧ R2 — a non-additive corridor functional carried on the
history-space frame — is the one combination the single-assumption audit did
not test. Pursuing it would be a deliberate protocol extension, not a
continuation of this audit.
