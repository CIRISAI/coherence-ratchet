# Dense snapshot grid (26 snaps) — headline robust and improved; two frozen estimators exposed as wiggle-fragile

**Date 2026-07-10.** 16 snapshots added to the frozen 10 (peak region z ∈ 0.15–2.0 densified),
same frozen B-total pipeline at the corner threshold 7.425×10¹¹, same octant jackknife.
Estimator gate re-passed. Decisions pre-committed in `DECISIONS.md`. Data: `results.json`.

## The likelihood-level result: robust, slightly improved

| quantity | 10-snap (frozen grid) | **26-snap (dense)** |
|---|---|---|
| dist CPL (w₀, wₐ) | (−0.767, −0.742) | **(−0.774, −0.711)** |
| Mahalanobis from DESI | 1.36σ | **1.26σ** |
| projected crossing z | 0.458 | **0.465** |
| ρ-weighted maha | 1.95σ | 1.92σ |

Densifying the grid moved the DESI-projected point by ~0.03 in wₐ and *improved* the tension.
**The distance-level quantities are grid-robust.**

## The S(a) shape: a clean global peak on a broad plateau

The dense curve rises monotonically to a **global maximum at z = 0.503** (S = 9945.8), within
one grid step of the coarse grid's 0.546–0.59, then declines to z = 0 — with S staying within
**5.7% of the maximum across the whole range z ∈ (0.10, 0.65)**. The peak is real, interior
(8/8 jackknife), and BROAD. That breadth is the physical finding: the crossing epoch is not a
sharp point, and quoting it as one overstates the pipeline's resolution.

## The estimator lesson (report it loudly, it's the honest yield of this run)

Two frozen-spec estimators are **fragile to sub-0.1% wiggles** once the grid resolves them:

1. **The last-sign-change spline peak finder** reported "interior peak z = 0.239 ± 0.017" —
   an artifact: it latched onto a +0.06% uptick between z = 0.273 (S = 9632.8) and z = 0.226
   (S = 9638.4). The jackknife's tiny ±0.017 is misleading — all replicates share the same
   correlated wiggle. The **global-max epoch (z = 0.503)** is the robust physical-peak
   statistic on a dense grid.
2. **The endpoint-slope w_today** moved from −0.833 ± 0.057 (coarse) to −1.152 ± 0.172
   (dense) — the coarse grid's tight error bar was itself a resolution artifact, and the
   endpoint derivative is simply not a well-measured quantity at this box's noise level.
   The dense error bar spans −1. **w_today should be retired as a headline number** in favor
   of the projected (w₀, wₐ), which is what data can actually constrain.

## Consequence for the registered DR3 prediction

Per the confirmation-mode discipline, the registered comparison quantities update as a
documented refinement, not a silent swap: the frozen 10-snap spec's value (z = 0.59) stands as
what the frozen spec produced; the dense measurement refines the physical peak to
**z ≈ 0.50 on a broad (≈±0.25) plateau**, and the grid-robust DR3-facing quantity is the
**CPL-projected crossing z = 0.46–0.47** (stable across grids, both of which sit inside DESI
DR2's 90% interval [0.19, 0.70]). Recorded in `../..​/PREREGISTRATION.md` update block.

## Caveats

Dense snapshots are a data-quantity increase through the frozen pipeline (documented in
DECISIONS before results); the wiggle at z ≈ 0.23 is at the box's shot/cosmic-variance floor
and not physical; octant jackknife shares large modes; all prior caveats (2-point proxy, one
simulation, θ* convention) unchanged.

*(Fetch by the fine-grid agent; compute executed by the orchestrating session under the GPU
lock after the agent idled; summary by the orchestrator from executed output.)*
