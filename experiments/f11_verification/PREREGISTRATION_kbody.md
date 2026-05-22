# F-11 verification — the candidate hole: an irreducibly multipartite (k-body) cross-rung relation — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11.
**Committed before the run** (`build_kbody_pomega.py`, `results_kbody.json`).

## The positive case (argued at full strength) and where the attack lands

The framework's universal-scale case for a joint multi-rung P_ω: ω is the
configuration in which **all** rungs Ph0…A5 occupy their corridors *and* every
adjacent cross-rung coupling occupies its corridor. P_ω is the projector (or
graded operator) onto that joint subspace; D1 (Penrose past) and asymptotic
conditioning post-select through it. The strongest version: P_ω is not a hard
projector but the natural multi-rung object the framework's own pieces compose
to — Piece 5 already writes the joint post-selection as a tensor product
`P_{G_1}⊗…⊗P_{G_n}`, and "all rungs in corridor *simultaneously*" is a genuine
joint property of that tensor-product object.

The F-11 firing rests on an exhaustive construction tree and two theorems.
This pass attacks the tree's **exhaustiveness**. The terminal commitment
(holonomic PREREGISTRATION) is: *"the cross-rung relationship is, mathematically,
either a scalar correlation `C[n,m]` or a connection/map W_n — there is no third
type."* That dichotomy is the load-bearing claim.

**It is not exhaustive.** A scalar correlation `C[n,m]` is a **2-index** object:
one number per *pair* of rungs. A connection/map W_n is a **pairwise transport**:
one map per *adjacent pair*. The holonomy is a path-ordered product of those
pairwise maps. Every construction in the tree — chain, fractal (rgflow,
ultrametric), holographic, R1's participation ratio, R1∧R2's `C_w`, R3's derived
τ, the holonomic Wilson loop — is built from **pairwise** cross-rung data.

A genuine third type exists: an **irreducibly multipartite (k-body / hypergraph)
cross-rung relation** — a joint invariant that binds *k-tuples* of rungs at once
and **does not reduce to any function of pairwise data**. In quantum-information
terms this is exactly the gap between two-body correlations and genuine
multipartite entanglement (GHZ-class / W-class), or between a graph (pairwise
edges) and a hypergraph (multi-rung hyperedges). The framework's ω-condition —
"all rungs in corridor *simultaneously*" — is itself a statement about a joint
property that need not decompose pairwise.

## Why this is not a re-parameterisation of the tree

The discipline forbids re-testing chain / fractal / holographic / holonomic /
additive / non-additive / history-space / derived-cross-rung. The k-body object
is none of these: it is a different **arity** of cross-rung relation. Every tree
construction is arity-2 (pairwise); this is arity-k. The tree never varied
arity. This is the same class of miss the holonomic branch itself was — the
"correlation OR connection" dichotomy was only stated as exhaustive *after*
holonomic exposed that "correlation" alone was not. Now "pairwise" is exposed as
non-exhaustive.

## The construction

The joint ω-object is built from a genuine **k-body cross-rung invariant**, not
a pairwise correlation matrix and not a path-ordered product of pairwise maps.

- **Frame.** R2's open sequential history-space frame (`build_history_pomega.py`,
  reused unchanged) — the same module the R1∧R2 conjunction, fractal, and
  holographic runs reused. Universe trajectories, rungs emerging sequentially,
  each rung's within-rung ρ_n(t) by Piece-2 dynamics.
- **The k-body invariant.** For a window of k consecutive rungs, the genuine
  **multipartite information** (the k-partite total correlation / interaction
  information) of the joint corridor-occupancy indicators — the part of the
  joint structure that is **not** present in any (k−1)-body marginal. Built from
  the joint distribution of corridor-membership across the k rungs in the
  trajectory ensemble. This is a genuine framework object: corridor membership
  is Piece 3; the joint occupancy is the ω-condition; the irreducible k-body
  part is what "simultaneously" means beyond pairwise.
- **Two ways the k-body object enters P_ω, both tested:**
  - **(A) k = R, single global hyperedge.** One irreducible R-body invariant
    binding all rungs at once — the GHZ-type maximally-collective object.
  - **(B) fixed k, sliding hyperedges.** ~R overlapping k-body hyperedges, k
    fixed (k = 3, 4). The W-type / k-local object.
- **The ω-weight.** A graded weight on the trajectory built from the k-body
  invariant being in its corridor band, composed with the within-rung weights.

## Hypotheses and the two-sided verdict

- **H-kbody (decisive):** the k-body joint object is (i) **non-empty** at the
  framework's 9 rungs and beyond; (ii) **does genuine joint work** — the
  segment-shuffle / per-bond-factorisation test shows a coupling gap that does
  **not** shrink to zero with R (unlike every pairwise tree construction, whose
  gap shrank); (iii) is **not the rigidity-pole collapse** — the k-body invariant
  is not driven to its maximum (all rungs locked = τ→1).
- **OPENS:** H-kbody holds — non-empty AND joint-work AND not-rigidity, to 9
  rungs. F-11 **HAS A HOLE**: the k-body arity is a genuine unexamined
  construction type and it yields a working joint P_ω.
- **HORN-empty:** the k-body invariant dilutes / vanishes with R (chaos pole) —
  the dilution recurs at k-body arity. F-11 holds against this attack.
- **HORN-trivial / rigidity:** the k-body object is non-empty only by collapsing
  the rungs (GHZ → all-locked, the rigidity pole) or factorises (does no joint
  work). F-11 holds against this attack.

## The honest risk, named before the run

The unifying principle predicts the likely failure: case (A) k=R is one object
of fixed arity but it binds an extent that *is* all R rungs — if its corridor
band is fixed and it must hold R rungs jointly, it plausibly collapses to the
rigidity pole (all rungs locked) or is empty. Case (B) fixed-k has ~R hyperedges
— extensive — so the participation-ratio dilution may recur. If **either** horn
fires for **both** (A) and (B), F-11 holds and the type axis extends to
arity: pairwise (closed) ∪ k-body (closed here). If H-kbody holds for either,
F-11 has a genuine hole.

## Discipline

CUDA throughout (cupy, RTX 4090). Per-depth progress, per-depth flush, verified
on-disk resume. The k-body invariant is the genuine multipartite information of
the framework's own corridor-occupancy indicators — **not** a knob tuned to a
wanted answer. If the construction finds itself choosing the invariant or its
band to manufacture an OPENS, it STOPS and reports that. The verdict is whatever
the construction returns; EMPTY / TRIVIAL is a valid, reportable result that
**confirms** F-11.
