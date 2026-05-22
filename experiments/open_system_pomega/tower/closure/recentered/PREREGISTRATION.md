# P_ω closure — re-centred re-run — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12. This is a
**bug-fix re-run** of the forward–backward closure construction
(`../PREREGISTRATION.md`), not a new recast — it stays inside the
pre-committed final construction and its stopping rule.

## The bug being fixed

The closure run (`../results_tower_closure.json`, EXIT 0, script verdict
DISCOVERY) optimized a penalty centred at **τ_c = ρ_c = 0.5**. That centre sits
**outside the corridor band (0.10, 0.43)** the run itself records. The tell:
`tau_in_band_count = 0` at all 14 depths — every τ and ρ was driven to ~0.50,
**not one rung landed in the actual corridor**. The run took the band's
half-width (w = 0.165, β_pin = 18.37) but not its centre — internally
inconsistent. So the "non-empty / well-defined / e_inf tiny" half of the verdict
is computed for a mis-centred operator and does not yet stand.

## The fix

Re-run the *identical* closure construction with the penalty centre at the
**actual corridor centre**: τ_c = ρ_c = **0.265** (= (0.10 + 0.43)/2), band
(0.10, 0.43), w = 0.165, β_pin = 18.37 (unchanged — width was already right).
Everything else identical: same forward–backward two-state tower, same depth
scan, same D1 coupling test, same flat-boundary control, same selectivity test
— all recomputed at the corrected centre.

## Verification requirement

`tau_in_band_count` must now be **non-zero** — rungs landing inside (0.10, 0.43).
If it is still 0 at the corrected centre, the construction is optimizing
something other than corridor occupancy, and that is itself a reportable
finding.

## Verdict — unchanged three horns

- **DISCOVERY:** at the corrected centre the closure is non-empty, the
  ω-boundary still couples the chain (D1 ω-specific vs the flat control), the
  operator does not dead-zone to the framework's rung count, and rungs land
  in-band. P_ω constructed — banked.
- **EMPTY / TRIVIAL:** re-centring kills the survival or the coupling. It lands
  on a horn.

## Stopping rule (still in force)

If EMPTY or TRIVIAL → the multi-rung P_ω squeeze is the genuine result, **F-11
fires**, v2's §sec:open-research records the documented no-go. If DISCOVERY,
P_ω is constructed and v2 records that. No further recast either way.

## Discipline

CUDA mandatory (cupy). Incremental output. The centre 0.265 is forced by the
band (0.10, 0.43) — it is not a tunable knob; do not adjust it to chase a
verdict. The verdict is whatever the corrected construction returns.
