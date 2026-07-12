# Pandey cross-check — AGREEMENT (box-limited): two functionals, one field, same DE-onset epoch

**Date 2026-07-12.** The registered cross-check from Corridor Dynamics v5: Pandey's
mutual-information-minimum epoch vs our S-peak crossing (z = 0.59 ± 0.03), on the same TNG300
field. Pre-registration in DECISIONS.md; code + all results JSONs on disk. (Summary by the
orchestrator from the agent's executed output.)

## Verified method (his, not guessed)

Pandey 2023 (arXiv:2307.12959) is ANALYTIC: MI between large disjoint regions,
I_AB = ∫∫ ρ̄²(1+ξ)ln(1+ξ) dV_A dV_B, whose evolution is "entirely determined by the
configuration-entropy rate" (S_c = −∫ρ ln ρ dV); "the location of the [MI] minimum precisely
indicates the epoch of dark energy domination." His marker therefore = the extremum of the
clustering-rate term dG/dln a, G = ⟨(1+δ)ln(1+δ)⟩.

## Result

| field / smoothing | z_P (his marker) | vs our 0.59 ± 0.03 |
|---|---|---|
| halos, 1.6 Mpc/h (nonlinear) | 0.446 (jk 0.51 ± 0.18) | 0.79σ |
| halos, 4 Mpc/h (quasi-linear — his regime) | **0.582** (jk 0.63 ± 0.39) | **0.02σ** |
| halos, 8 Mpc/h | 0.585 | 0.01σ |
| galaxies, 4 Mpc/h | 0.581 | 0.02σ |

Robust to smoothing (2–16 Mpc/h) and tracer. In the quasi-linear regime his formalism
assumes, his marker lands essentially exactly on our crossing.

## Verdict: AGREEMENT — with two honesty disclosures carried

Two different functionals (his physical-density configuration entropy, our copula
S = −ln det C) on the SAME field name the same DE-onset epoch, because both read the same
structure-formation-rate turnover.

**Disclosure 1 — estimator correction (not a clean pre-registered hit).** The pre-registered
O1 locator (smoothing-spline derivative peak) returned z = 0 — INCONCLUSIVE by the letter, a
spline artifact pinned by a noisy z = 0 snapshot. The RAW finite-difference dG/dln a has a clear
broad interior maximum at z ≈ 0.44–0.60 (unrestricted argmax already interior at 0.44, so the
interior window did not manufacture it). AGREEMENT is under the corrected finite-difference
locator. A reader trusting only the pre-registration letter should read
INCONCLUSIVE-BY-ESTIMATOR → corrected to AGREEMENT on the raw curve. Both are in the record
(results.json = spline; results_final.json = corrected; results_smoothed.json = the raw curves
that adjudicate).

**Disclosure 2 — box-limited.** 205 Mpc/h is modest for a large-scale MI measure (Pandey used
bigger sims / SDSS); only ~1–2 homogeneity-scale regions fit, so jackknife errors are wide
(±0.18–0.46). The epochs coincide; the PRECISION of the coincidence is box-limited. The
Pandey–Nandi L/8 = 25.6 Mpc/h ceiling sits inside the measurement range.

## Weight (rule 2)

Genuine but modest independent corroboration of the MECHANISM — Pandey's 2019-priority claim
that a matter-field information extremum marks DE onset — NOT of our copula functional, the
sign law, or the DR3 magnitude. The frozen DR3 bet and the anti-hedging commitment are
untouched. Two literal-MI observables (O2 naive a⁻⁶×ξ competition; O3 copula-invariant Shannon
MI) are documented expected-negatives: his minimum lives in the physical-density weighting,
which O3 is blind to by density-scale invariance — a clean statement of why his marker and our
copula S agree on the epoch while being different objects.

The cheapest external test of the DE leg was run, and it landed on our epoch (z ≈ 0.58
quasi-linear vs our 0.59). This is the content of the email owed to B. Pandey
(biswap@visva-bharati.ac.in): independent reproduction with a different functional, priority
credited, epochs compared.
