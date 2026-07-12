# Bench suite — bets 7, 8, 10 on the CIRISArray substrate: ALL THREE PASS

**Date 2026-07-12.** The second species' three registered bench experiments, run on coupled
oscillators whose noise source is REAL GPU timing jitter (no PRNG in the dynamics; ~84 million
physical jitter samples across the suite). Pre-registration in `DECISIONS.md` (apparatus,
estimators, thresholds, and the tautology-guards C2–C4, all frozen before bet-relevant runs);
data in `results.json` (incremental flush); verdicts computed by the frozen rules. Summary by
the orchestrator from the executed output.

## Bet 10 — the rent-cut (first causal test of dρ/dt = α − γM): **PASS**

The registered curve was written BEFORE the cut: from steady-state fluctuations alone,
γ̂ = 2.061, registered band [1.972, 2.149]. Then the maintenance was cut, five independent
physical realizations: measured decay γ_cut = **1.965 ± 0.084**, mean 2SE CI [1.889, 2.040] —
**inside the registered band**. The books decayed at the pre-measured rate. Rent while held:
3.14 (budget units), σ̂_held = 0.83 vs analytic 0.816.

**The tautology-guard (C2) and the control that carries the epistemics:** on a linear
substrate, decay-to-fixed-point after a cut is structurally guaranteed — so the genuine
content is (a) the RATE matching the independently pre-measured bath γ̂, and (b) the rent
certificate. The **conservative control** (symmetric coupling: holds the same ρ* WITH detailed
balance) decays identically when cut but pays **~zero housekeeping** — proving the decay test
alone cannot distinguish rented from conservative maintenance, and that σ̂/rent is the
discriminating observable. The kept-vs-bound distinction (Axis 2) is now demonstrated
interventionally on hardware: same structure, same decay, different books.

## Bet 7 — the ceiling (third law): **PASS**

Nine-point sweep ρ* = 0.1 → 0.9 at fixed actuation budget: maintainable σ collapses
monotonically; fitted exponent **β = 1.075 ± 0.066** against the predicted 1; measured/analytic
ratio 0.91–1.05 across the sweep with no anomalous high-ρ growth; σ(0.9) < σ(0.1) by 10×.
(C3 guard: under N1 the ideal exponent is analytically 1 — the bench's content is that the
REAL-jitter substrate reproduces the collapse, where flatness or inversion was the pre-stated
kill and was physically available.) You cannot stir a rigidly-clamped system: measured.

## Bet 8 — the equality form (single-κ fluctuation theorem): **PASS**

The exact integral FT ⟨e^(−ΔS_tot)⟩ = 1 holds at **κ = 1** at both operating points
(0.988 [0.974, 1.003] and 1.002 [0.989, 1.018]); Crooks slopes agree (0.95, 1.04, overlapping
CIs). One state-independent κ across ρ* — the cross-condition consistency that WAS the test.
(C4 guard: the direct exponential estimator is ill-conditioned and the Gaussian-form κ_var is
skew-biased (1.20, 1.09; skews 1.21, 0.86) — reported as diagnostics; the well-conditioned
estimators decide, per the frozen addendum.)

## What this does and does not establish

Three registered executioners of the second species arrived and none fired: the maintenance
law holds causally (the pawl lets go at the predicted rate), the capacity ceiling collapses
with the predicted exponent, and the second law's equality form holds with a single κ — all
on physical noise, all pre-registered, with the structurally-guaranteed parts explicitly
fenced off from the measured content (C2–C4 + the conservative control). Per rule 2 these are
theorem-given-model confirmations on an ENGINEERED substrate — they open the lab channel
(repeatable, σ-scalable) and they do not, by themselves, say anything about cosmology. The
laws' natural-substrate executioners (DR3 and the rest of the deposit) are unchanged and
still scheduled.
