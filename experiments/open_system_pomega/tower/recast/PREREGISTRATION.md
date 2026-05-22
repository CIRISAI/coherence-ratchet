# P_ω tower — recast: cross-rung corridor as a map-constraint — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12. Formal
construction — attempt, report honestly.

## The hypothesis under test

`build_tower_pomega.py` found a documented obstruction: adjacent cross-rung
penalty terms H_{n,n+1} = (τ_n − τ_c)² frustrate (they share rung n+1),
h_min ≈ 0.19/rung, soft E_ω dead-zoned at R\* ≈ 0.2.

**The hypothesis:** that obstruction is a symptom of a misread, not a real wall.
The construction modeled the cross-rung corridor as an **additive operator
penalty** — Σ_n (τ_n − τ_c)² as terms in a joint Hamiltonian, τ_n an operator,
adjacent τ_n and τ_{n+1} competing for rung n+1's degrees of freedom. But the
framework's cross-rung coupling τ_(n,n+1) is **relational** — a normalized
mutual information, the degree to which rung n+1 *emerges from* rung n — and in
the tower that relation is already carried by the coarse-graining map W_n.
Penalizing τ as an independent additive term double-counts a structural
relationship; the frustration is the artifact of that double-count.

## The recast

The cross-rung corridor is a corridor on the tower's connecting **maps** W_n
(the emergence relations): τ(W_n) ∈ (τ_lower, τ_upper), with τ(W_n) the
*actual* normalized mutual information the map realizes (the framework's own
definition of τ). Each W_n joins a distinct pair of levels — no shared-rung
competition. Multi-rung structure lives in the **composability/consistency of
the map-tower** (W_{n+1}∘W_n), not in additive operator frustration.

## Method

Rebuild the tower with the cross-rung corridor as a constraint on the W_n maps.
Within-rung penalty stays as the soft H_n = (ρ_n − ρ_c)². Cross-rung: compute
τ(W_n) as the genuine normalized mutual information realized by W_n; constrain
it to the corridor; carry the composition constraints. Test whether the joint
object (the corrected E_ω, or whatever the relational form yields) is
well-defined across tower depth, at the framework's 9 rungs and past R\*. CUDA.

## Two-sided pre-registered verdict

- **DISCOVERY (recast confirmed):** the frustration dissolves — h_min does *not*
  grow ≈0.19/rung — **and** the multi-rung object stays non-trivial: the
  cross-rung corridor still does work (it does not collapse to the finest-rung
  projector, nor to an unconstrained product of independent map-constraints).
  *Both* required. Then the correct mathematical form of the cross-rung corridor
  is the map-tower constraint — a genuine structural finding.
- **OBSTRUCTION STANDS:** the frustration persists under the relational form
  too — the misread hypothesis fails; `build_tower_pomega.py`'s obstruction
  holds.
- **TRIVIAL:** the frustration dissolves only because each W_n independently
  satisfies its corridor with no joint constraint — the other horn of the
  empty/trivial squeeze. Reported as such, **not** as a discovery.

## Discipline

CUDA mandatory (cupy). Incremental output. The recast is a hypothesis being
tested — a self-sealing "the framework cannot be obstructed" adoption is
explicitly **not** permitted. The verdict is whatever the construction returns;
a persisting obstruction is a valid, reportable result. No synthetic data — the
honesty constraint is that the relational form be the genuine framework
definition of τ, not a penalty hand-tuned to vanish.
