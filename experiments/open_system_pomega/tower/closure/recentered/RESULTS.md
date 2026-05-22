# P_ω closure — re-centred re-run — RESULTS

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.
**Verdict: TRIVIAL.** The pre-committed stopping rule fires: **F-11 fires.**

This is the bug-fix re-run of the forward–backward closure construction
(`../PREREGISTRATION.md`, `recentered/PREREGISTRATION.md`). It is not a new
recast — it stays inside the pre-committed final construction and its binding
stopping rule.

## The one change

The buggy closure run (`../results_tower_closure.json`, EXIT 0, script verdict
DISCOVERY) optimized a penalty centred at **τ_c = ρ_c = 0.5**, which sits
**outside** the corridor band (0.10, 0.43) the run itself records. Result:
`tau_in_band_count = 0` at all 14 depths — not one rung landed in the corridor.

The fix was exactly one change to `build_tower_closure.py`: the penalty centre
moved to the **actual corridor centre**, τ_c = ρ_c = **0.265** = (0.10+0.43)/2.
Band (0.10, 0.43), w = 0.165, β_pin = 18.365 — all unchanged (width was already
correct). The centre 0.265 is forced by the band; it is not a tunable knob.
Same forward–backward two-state tower, same 14-depth scan, same D1 coupling
test, same flat-boundary control, same selectivity test, same seed. Everything
recomputed at the corrected centre. CUDA throughout (cupy 13.6.0, float64,
RTX 4090). Runtime 2169 s. No CPU fallback.

## Verification requirement — PASSED

`tau_in_band_count` is now **non-zero at every depth**. Every bond's weak-joint
τ optimised into the corridor band (0.10, 0.43):

| R | h_min / R | bonds in band | R | h_min / R | bonds in band |
|---|-----------|---------------|---|-----------|---------------|
| 2 | 6.17e-08 | 1 / 1   | 11 | 3.78e-07 | 10 / 10 |
| 3 | 7.93e-07 | 2 / 2   | 13 | 3.39e-07 | 12 / 12 |
| 4 | 4.61e-07 | 3 / 3   | 20 | 5.88e-07 | 19 / 19 |
| 5 | 1.30e-06 | 4 / 4   | 30 | 1.18e-06 | 29 / 29 |
| 6 | 3.25e-07 | 5 / 5   | 40 | 4.73e-07 | 39 / 39 |
| 7 | 1.79e-07 | 6 / 6   | 56 | 6.54e-07 | 55 / 55 |
| 8 | 8.47e-07 | 7 / 7   |    |          |         |
| 9 | 4.35e-07 | 8 / 8   |    |          |         |

The recentred operator genuinely optimises corridor occupancy. The within-rung
ρ and cross-rung τ both pull to ≈ 0.265, and h_min/R stays ~1e-6 — small. The
construction is **non-empty**: it is satisfiable, and well inside the framework's
9 rungs and past R* = 56.

## The verdict — TRIVIAL

Three-horn pre-registered verdict. The corrected construction returns TRIVIAL.

| Criterion | Threshold | Result | Pass? |
|-----------|-----------|--------|-------|
| non-empty (e_inf) | e_inf < 0.01 | e_inf = 6.91e-07 | yes |
| well-defined to 9 rungs | h_min(9)/9 < 0.05 | 4.35e-07 | yes |
| selective | random-tower pass fraction < 0.5 | 0.000 at R=5,9,13 | yes |
| **D1 coupled & ω-specific** | **min ω-ratio > 3 AND > 3× max flat-ratio** | **min ω-ratio 0.76** | **NO** |

The decisive horn is **D1 coupling** — the same test the feed-forward recast
ran, the one that distinguishes a genuine joint P_ω from a decoupled chain.
D1 measures the joint optimum against the sum of independent per-bond optima.

**D1 — joint optimum vs sum of independent per-bond optima (the ratio):**

| R | ω-boundary joint/indep | flat-control joint/indep |
|---|------------------------|--------------------------|
| 5  | 3.09 | — |
| 9  | 1.32 | 0.46 |
| 13 | **0.76** | 0.49 |

The ω-boundary ratio is **not consistently above 1**. It is 3.1 at R=5, 1.3 at
R=9, and **0.76 at R=13** — i.e. at R=13 the joint optimum is *below* the sum of
the per-bond optima. A genuine coupling produces a positive, R-stable (ideally
R-growing) gap; this is the opposite — the "gap" shrinks and goes negative as R
grows, which is the signature of a **decoupled chain plus per-bond solver
noise**, not a backward boundary doing joint work. The per-bond isolated solves
simply land at slightly different (sometimes worse) local optima than the
joint solve; the differences are search residual, not structure.

The flat-boundary control confirms this: its ratios (0.46, 0.49) are also ~1
and also wander below 1 — the flat boundary "decouples" exactly the way the ω
boundary does. There is **no ω-specific excess**. The minimum ω-ratio (0.76) is
not above the flat-control maximum (0.49) by the required 3×; it is barely
above it at all, and below the absolute coupling threshold.

D2 (secondary, noisy) corroborates: median fix-W_n conditional-shift ratio 1.18,
no signal. The post-sweep-1 gain is non-zero (3.34e-2 deep), but with D1 flat
that is consistent with a noisy non-convex landscape, not coupling — and D1 is
the decisive, recast-comparable test, so the verdict follows D1.

## Honest assessment — did re-centring confirm or collapse the closure?

**Re-centring collapsed the closure onto the TRIVIAL horn.** The buggy run's
DISCOVERY was an artifact of the mis-centred operator. At τ_c = 0.5 — outside
the corridor — the forward and backward legs were both being driven toward an
*infeasible* target (no qutrit weak state can sit at ρ = 0.5 while every bond's
τ also sits at 0.5 in a way the corridor permits), and the large, R-growing
joint/indep gaps (14.7, 46.0, 20.6) were the cost of fighting that
over-constraint — frustration, not coupling. Re-centred onto the real corridor,
the construction becomes easily satisfiable: every bond drops into the band,
h_min/R falls to ~1e-6, and the joint optimum is just the sum of what each bond
can do on its own. The backward ω-boundary then does **no joint work** — fixing
one map does not change what its neighbours may do, the joint optimum is the
sum of independent per-bond optima, and the flat control behaves identically.

This is the **TRIVIAL horn**: the same decoupling the feed-forward recast hit.
The backward boundary, once the corridor is actually reachable, adds no
constraint that couples the rungs. P_ω as a forward–backward closure is **not**
the genuine joint object — it factorises over bonds.

The construction *is* non-empty, well-defined to 9 rungs and past R*, and
selective (0 / 6000 random towers near the optimum at every depth — random
towers do not satisfy the corridor). But selectivity without coupling is just
"the corridor is a narrow target," not "P_ω is an irreducible joint operator."
The pre-registration requires non-empty **AND coupled** for DISCOVERY. Coupling
fails. Verdict TRIVIAL.

## Stopping rule — F-11 fires

Per the binding, pre-committed stopping rule (`../PREREGISTRATION.md`,
`recentered/PREREGISTRATION.md`): this was the **final** construction in the
recast chain. EMPTY or TRIVIAL fires **F-11**. The verdict is TRIVIAL.

**F-11 fires.** The multi-rung P_ω squeeze is the genuine result. The
forward-only constructions decoupled (TRIVIAL) or frustrated (EMPTY); the
forward–backward closure, evaluated at the corrected corridor centre,
**also decouples**. No further recast. `papers/Corridor Dynamics.tex` v2's
`§sec:open-research` records the documented no-go — which the framework's own
F-12 language says it welcomes: a multi-rung joint P_ω operator is not
constructed by this route, and the construction has told the program exactly
where the universal-scale operator definition breaks.

## Files

- `build_tower_closure.py` — recentred build script (one-line centre change)
- `results_tower_closure.json` — full results, all stages, this run
- `run.log` — full stdout, EXIT 0
- `PREREGISTRATION.md` — the re-centred re-run pre-registration
