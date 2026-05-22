# R2 — P_ω as a history-space object — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.
**Audit relaxation:** R2 of `../PREREGISTRATION.md` — drops assumptions 4
(P_ω a *static* operator on a *simultaneous* all-rungs-at-once configuration
space) and 8 (ω = all rungs in corridor *simultaneously*).

This pre-registration is committed **before** the construction is run. The
verdict criteria below are binding. A HORN is a valid result.

## The relaxation

Every failed construction (`p_omega_construction/NOTES.md`,
`tower/`, `tower/recast/`, `tower/closure/recentered/`) built P_ω as a static
operator requiring **all rungs in corridor at one time**. The empty horn
(shared-rung frustration) and the trivial horn (feed-forward decoupling) are
both artifacts of the *simultaneous* configuration space.

But the framework's own Piece 6 says the rungs **emerge sequentially over
cosmic time** (A2→A3 ~540 Myr, A3→A4 ~310 kyr, A4→A5 ~6.7 kyr). And TSVF
(Piece 4) is natively a **histories** formalism: the backward state
⟨φ(t)| = ⟨φ(t_f)|U(t_f,t) is a *boundary condition on trajectories*, not an
operator on a configuration space.

R2 builds P_ω as a constraint on the universe's **history**: its trajectory
through rung-space over cosmic time, where each rung enters its corridor *as it
emerges* (Ph0 → Ph1 → … → A5), with the ω-condition a **two-time boundary
condition** on that path (forward state from t_0, backward post-selection at
t_f).

## The construction (committed form)

A history is a trajectory `x(t)` over cosmic time discretised into T steps. At
each step the universe has a set of *already-emerged* rungs; each emerged rung n
carries a within-rung correlation `ρ_n(t)` evolving by the framework's own
dynamics `dρ/dt = α − γM` (Piece 2). Rungs emerge sequentially: rung n+1's
emergence event is a step at which rung n is in its corridor (the
substrate-readiness gate — Piece 6's cross-rung condition, in trajectory form).

- **Forward state** |ψ⟩: the Big-Bang boundary at t_0 — chaos regime, no rungs
  instantiated, ρ → 0 (Piece 8's `|Ψ_α^high⟩`).
- **Backward state** ⟨φ_ω| at t_f: the ω-condition as a TSVF post-selection on
  the *whole trajectory* — the universe is observed, at t_f, to have all 9
  rungs emerged and each within corridor *at t_f*, AND each rung was in corridor
  at the moment its successor emerged (sequential-emergence viability).
- **P_ω** = the post-selection that reweights the path measure by the
  trajectory's compatibility with that two-time boundary. It is a functional on
  histories, NOT a static operator on a config space.

The path measure is over forward-dynamics-generated trajectories (a stochastic
`dρ/dt` per rung + emergence-gate events). P_ω = the weight on each history; the
post-selected ensemble is the reweighted set of histories.

CUDA (cupy) — histories sampled in GPU-parallel batches. Incremental output:
results flushed per trajectory-length.

## Verdict criteria (binding, three-way)

Tested across trajectory length to 9 rungs and beyond (R ∈ {2,…,13, and a
deep-tail point}).

- **OPENS** — all three:
  1. **Non-empty.** The post-selected set of histories has non-zero measure:
     post-selection weight `Z = E[w] > 0`, not vanishing with R.
  2. **Genuine joint work.** The ω-boundary *couples the trajectory* — it
     concentrates measure on a non-trivial subset of histories rather than
     being satisfied by every history. Decisive test (committed before run):
     a **joint-vs-factorised** ratio. Compute the post-selected ensemble's
     log-weight; compare the *joint* ω-boundary against a **factorised
     surrogate** that post-selects each rung's final state and each emergence
     event *independently* (product of per-rung / per-event marginals). If the
     joint weight equals the factorised-surrogate weight, the boundary does no
     joint work (TRIVIAL). Genuine joint work = a **selectivity gap**: the
     joint post-selection accepts a *strictly smaller, structured* fraction of
     histories than the factorised surrogate. Quantified two ways:
     (a) **selectivity** — joint acceptance fraction `f_joint` vs a flat
     (no-ω) baseline: require `f_joint < 0.5 × f_flat` and not → 1 with R;
     (b) **non-factorisation** — KL divergence / log-ratio between the joint
     post-selected path distribution and the factorised-surrogate path
     distribution; require it **non-zero and R-stable or R-growing** (a genuine
     temporal coupling does not wash out with trajectory length). And a
     **flat-boundary control**: a boundary that constrains only the endpoint
     (no sequential-emergence requirement) must show *no* such gap — if the
     flat control shows the same gap, the gap is not ω-specific.
  3. **Well-defined to 9 rungs.** The construction is well-posed and computable
     at R = 9 (the framework's Ph0…A5) and past it — Z and the joint-work
     metrics finite and stable at R = 9 and the deep-tail point.

- **HORNS** — any of:
  - **EMPTY:** post-selected set has vanishing measure (Z → 0 with R; the
    sequential-emergence boundary is unsatisfiable past some R < 9).
  - **TRIVIAL:** non-empty but the ω-boundary does no joint work — joint
    post-selection equals the factorised surrogate (no selectivity gap, or the
    flat control reproduces the gap). The history object factorises over
    time-steps / rungs just as the static constructions factorised over the
    config space.

## Discipline

The history-space object must be a genuine TSVF boundary condition on the
framework's real sequential rung-emergence — the emergence sequence Ph0→…→A5,
the within-rung `dρ/dt` dynamics, the corridor band — are the framework's, not
chosen to manufacture a verdict. The factorised surrogate and flat control are
the committed decisive tests; the verdict is whatever they return. If the
construction finds itself choosing structure to force OPENS, it stops and
reports that. A HORN is valid and reportable.
