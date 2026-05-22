# P_ω — assumption audit — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.

## Why this exists

The recast chain (`tower/`, `tower/recast/`, `tower/closure/`) documented a
no-go across four constructions — but all four are parameterizations of **one
ansatz**: P_ω as a soft Gibbs operator E_ω = exp(−β H_sum), with H_sum an
**additive** sum of **quadratic** per-rung and per-bond penalties on a **static
simultaneous** rung-tower configuration space. Four parameterizations, four
horns of the empty/trivial squeeze.

That is a documented no-go **for that ansatz family** — not a proof that P_ω has
no construction. The load-bearing assumptions were never questioned. This audit
questions them. It is **bounded**: the assumptions are a finite, definite list;
each genuinely-distinct relaxation is tested once. Exhaustion is the terminal
condition.

## The load-bearing assumptions of the failed ansatz

1. **Form** — P_ω is a soft exponential exp(−βH).
2. **Additive** — the corridor penalty is a sum of per-rung + per-bond local terms.
3. **Quadratic** — each term is a well at a centre (a proxy for band-membership).
4. **Object type** — P_ω is a *static* operator on a *simultaneous* configuration
   space (all rungs at once).
5. **Topology** — rungs are a 1D chain, cross-rung = nearest-neighbour.
6. **Independence** — the cross-rung corridor is its own independent penalty term.
7. **Coupling** — β = 1/2w².
8. **The ω condition** — ω = all rungs in corridor *simultaneously*.

## The relaxations under test

- **R1 — non-additive / global corridor functional** (drops 2, 3). The corridor
  condition is a non-local functional of the joint state — a band-indicator, a
  rank/determinant condition, a free-energy — not a sum of local quadratic wells.
- **R2 — history-space / sequential-trajectory object** (drops 4, 8). P_ω as a
  constraint on the universe's *trajectory* through rung-space over cosmic time —
  each rung entering its corridor as it emerges (Ph0 → … → A5) — not a static
  operator on a simultaneous configuration space. The TSVF-native form: a
  boundary condition on histories.
- **R3 — derived-not-independent cross-rung** (drops 6). The cross-rung corridor
  is not its own penalty term — τ is a *function* of (ρ_n, ρ_{n+1}, the emergence
  map), so there is no independent cross-rung degree of freedom to frustrate or
  to trivially satisfy.

(R4 topology and R5 β-renormalisation are noted assumptions; R5 was partly
addressed by prior work — β ∝ 1/R widens the corridor without bound, vacuous —
and R4 is lower priority. They are auditable if R1–R3 all horn.)

## Two-sided verdict — per relaxation

- **OPENS:** the relaxation yields a construction that is non-empty, does
  genuine joint work (the cross-rung / multi-rung structure is not vacuous —
  it concentrates measure, it couples), and is well-defined to the framework's
  9 rungs. That relaxation identifies the genuine P_ω form.
- **HORNS:** the relaxation lands empty or trivial, like the ansatz.

## Terminal condition (the real stopping rule)

The assumption set is finite. When the enumerated relaxations R1–R3 (and R4 if
reached) are exhausted: if **every** relaxation HORNS, F-11 fires at the
ansatz-independent level — a documented no-go for P_ω as such, recorded in v2's
§sec:open-research. If **any** relaxation OPENS, that is the genuine P_ω
construction; F-11 does not fire and v2 records the construction.

This audit is the assumptions, once each. It is **not** a licence for unbounded
recasts — a relaxation that horns is recorded as horned and not re-parameterised.

## Discipline

Each relaxation: pre-registered, two-sided, CUDA where numerical. The relaxation
must be a genuine structural change faithful to the framework's own definitions
— not a knob tuned to a wanted answer. If a construction finds itself choosing
its structure to manufacture an OPENS verdict, it stops and reports that (the
self-sealing move voids the test). The verdict is whatever the construction
returns; a HORN is a valid, reportable result.
