# P_ω tower — the forward–backward closure — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12. Formal
construction. **This is the pre-committed final construction** (see Stopping
rule below).

## Where we are

Two tower constructions, two horns of the empty/trivial squeeze:

- `build_tower_pomega.py` — cross-rung corridor as an **additive operator
  penalty** Σ(τ_n−τ_c)²: adjacent terms frustrate, soft E_ω dead-zoned
  (the *empty* horn). The ≈0.19/rung frustration was since shown to be an
  artifact of this modeling — retracted.
- `tower/recast/` — cross-rung corridor as a constraint on the **feed-forward
  maps** W_n: the frustration dissolves (≈7×10⁻⁸/rung) but the tower
  *decouples* — each W_n independently satisfies its corridor, the cross-rung
  corridor does no joint work (the *trivial* horn).

Both constructions are **forward-only**. P_ω was never a forward object: it is
the framework's **backward boundary** ⟨Φ_ω| — a post-selection from t_f. Both
prior constructions simplified that away. This construction restores it.

## The construction

A genuine tower H₀ → … → H_R with forward coarse-graining maps W_n, **plus** a
backward boundary post-selection at the top rung R (the ω-condition). The
backward state ⟨φ_n| propagates *down* from the boundary through the maps;
the forward state |ψ_n| propagates *up* from the base. Each rung carries the
two-state pair (⟨φ_n|, |ψ_n|); the within-rung and cross-rung corridor
conditions are conditions on the **weak values** ⟨φ_n|·|ψ_n|/⟨φ_n|ψ_n|, not on
forward operators alone.

The hypothesis: a backward boundary closing the top of the tower is a **global**
constraint — every rung is then constrained from *both* ends, so the chain
cannot decouple the way the feed-forward recast did. That coupling is where a
non-trivial joint P_ω could live.

## Method

Build the forward–backward closure. CUDA. Test, across tower depth (framework's
9 rungs and past R\*): is the set of towers consistent with the backward
boundary *and* all rungs' corridors (a) non-empty, (b) non-trivial — does the
constraint *couple* the rungs (joint optimum ≠ sum of independent per-bond
optima; fixing W_n changes what W_{n+1} may do, once the boundary is in), and
(c) selective (measure-concentrated on a special subset of towers, not all).

## Three-horn pre-registered verdict

- **DISCOVERY:** the closure yields a joint object that is non-empty **and**
  non-trivial (the cross-rung corridor does genuine joint work — the backward
  boundary couples the chain) **and** well-defined to the framework's rung count.
  Then P_ω is constructed as the forward–backward closure, and that is the
  genuine form the forward-only constructions missed.
- **EMPTY:** the two-arm constraint is over-determined — no tower satisfies both
  the forward corridors and the backward-propagated boundary. Dead-zone horn.
- **TRIVIAL:** the closure still decouples / the backward boundary does no work.
  Trivial horn.

## Stopping rule (pre-committed)

This is the **final** construction in the recast chain. If the verdict is EMPTY
or TRIVIAL, the multi-rung P_ω squeeze is the genuine result: **F-11 fires**,
and v2's §sec:open-research records the documented no-go (which the framework's
own F-12 language says it welcomes). No further recast. If DISCOVERY, P_ω is
constructed and v2 records *that*.

## Discipline

CUDA mandatory (cupy). Incremental output. The backward boundary must be the
genuine ω-post-selection condition, not a boundary hand-tuned to produce
coupling — if the construction finds itself choosing the boundary to manufacture
non-triviality, stop and report it (that is the self-sealing move and it voids
the test). The verdict is whatever the construction returns; EMPTY or TRIVIAL is
a valid, reportable result that fires F-11.
