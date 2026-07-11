# Self-consistency loop — TNG300-1 large-volume primary curve

**Date 2026-07-10.** Big-box replicate of `../selfconsistency/` (which closed the loop on the
pooled 6-box CAMELS 25 Mpc/h curve). Same machinery, same pre-stated question: **does closing
the gravity<->ledger loop move the fixed point toward or away from DESI?**

## Verdict

**The loop closes, converges in 2 iterations, and the fixed point sits essentially on top of the
open loop — a <=0.1% perturbation to S(a), ~0.015 in wa, 0 in w0.** The published big-box
~1.4 sigma (distance-space) result is **not** an artifact of the open loop.

**Direction is projection-dependent at this box** (unlike CAMELS, where all three moved toward):

| projection | open loop (published) | fixed point (eta=1) | d_maha | direction |
|---|---|---|---|---|
| **dist BAO+CMB** (faithful) | (-0.767, -0.742) **1.363 sig** | (-0.767, -0.727) **1.400 sig** | **+0.037** | **AWAY** |
| rho_DE-weighted | (-0.738, -0.977) 1.952 sig | (-0.739, -0.961) 1.912 sig | -0.045 | toward |
| w-space (DE-wtd) | (-0.762, -0.917) 1.563 sig | (-0.762, -0.903) 1.520 sig | -0.043 | toward |

Open-loop row reproduces `large_volume/results.json` stage5.primary **exactly**
(dist (-0.7666,-0.7424) maha 1.363) — pipeline-identity check passed.

- **eta-sensitivity (dist):** 1.381 sig (eta=0.5) / 1.400 sig (eta=1) / 1.417 sig (eta=1.5) — monotone, ~0.02 sig span.
- **Jackknife (8 spatial replicates, dist):** d_maha = **+0.038 +/- 0.007**, all 8 positive. The
  "away" sign in the distance projection is **robust to spatial subsampling** — small but not noise.
- **Physical crossing** (S peak) unmoved: z = 0.590 -> 0.603.

## Why the sign differs from CAMELS (honest mechanics, not a rescue)

The correction itself is the same physics in both boxes: the framework background suppresses/mildly
enhances late growth (here **g(a=1) = 1.007**, ~0.7% *more* growth by today — opposite sign to
CAMELS's 0.987, because TNG300's S(a)/S(1) sits *below* the constant-DE LCDM reference at the
epochs that dominate integrated growth), giving **R(1) = 0.999** and nudging the late-time S rise
down by <0.2% -> **wa rises by +0.015** (less negative) in every projection.

The *direction* then depends on geometry + the DESI covariance, not on the physics:
- TNG300's open-loop wa (-0.742) already sits **more negative than DESI** (-0.62). Raising it is
  toward DESI in raw wa.
- But the **distance fit pins w0 = -0.767** (off-center high vs DESI -0.838), and under DESI's
  **rho = -0.7** correlated covariance a pure less-negative-wa move at fixed high-w0 crosses the
  penalized correlation axis -> dist-maha *rises* by 0.037 sig.
- The rho- and w-space fits let w0,wa float together, so they read the same +0.015 wa shift as toward.

CAMELS differed only in that its open-loop wa (-0.44) sat *inside* DESI and its w0 improved under
the loop, so all three projections agreed on "toward."

## Response-model validation (load-bearing check)

ST cumulative-count shape N_ST(>thr; sig*g)/N_ST(>thr) vs the **measured** k(a)/k(1) at the corner
threshold (7.43e11 Msun/h), both normalized to a=1:

```
a           :  0.25  0.30  0.36  0.42  0.49  0.56  0.65  0.75  0.87  1.00
N_ST/N_ST(1):  0.30  0.50  0.70  0.83  0.92  0.97  1.00  1.01  1.01  1.00
k_meas/k(1) :  0.24  0.46  0.69  0.86  0.97  1.03  1.06  1.06  1.04  1.00
```

Global log-slopes 0.75 (ST) vs 0.89 (measured). ST tracks the rise and the interior turnover
location (a ~ 0.65) but **under-predicts the interior-peak amplitude (1.01 vs 1.06) and the late
merger-driven decline** — the expected formation-channel-only shortfall. At this high (corner)
threshold the ST fit is looser than at CAMELS's 1e11 (where it caught the peak to ~0.02); only the
*differential* background response enters the loop, and it is sub-percent regardless.

## Caveats (honest)

- **Formation-channel only.** R is the ST cumulative-count ratio on the extensive k-channel; the
  per-unit geometry sbar is held fixed (second order by the bias-cancellation argument, not measured).
  The measured k(a) has a stronger interior peak + late decline than ST reproduces — ST is monotone
  in D and misses mergers. This is a *model* for the response, validated only on shape.
- **eta is an assumption** (headline 1; 0.5/1.5 band spans 0.02 sig), not a measurement.
- **Smooth DE** in the growth ODE (no DE perturbations, c_s^2 unexamined); radiation omitted
  (cancels in g to first order). Same open flank as `lambda_maintenance_wz.md` sec 7c.
- **Single box, single background.** The loop background is Planck2015 (Om=0.3089), the projection
  convention Om=0.3155 (kept identical to the published pipeline). No cosmic-variance average
  across independent phases — jackknife bounds sampling noise within the one box, not the CV error.
- **Direction is not robust to projection choice here.** The honest one-line reading: the big-box
  self-consistency correction is **negligible (~0.04 sig, << the 1.4 sig headline and << box error)
  and its sign flips between the distance-space fit (away) and the derivative-space fits (toward).**
  What *is* robust and shared with CAMELS: the loop is stable, converges immediately, and does not
  move the result — the coupled gravity<->ledger system is already near its fixed point.

## Open questions

- Does the sign flip survive a full multi-box CV average at large volume (independent-phase TNG
  or the pre-registered large-volume ensemble)? The jackknife says the dist-away sign is robust
  *within* this box; across independent phases it may wash out.
- Why g(1)>1 here vs <1 in CAMELS: is it the S(a)-shape difference (corner vs 1e11 threshold,
  interior-peak amplitude) or the cosmology (Planck2015 vs CAMELS Om)? Separable by rerunning the
  TNG300 curve under the CAMELS background and vice versa.
- A measured (not ST-modeled) k-response — re-run the box's halo counts under the framework
  background directly — would remove the formation-channel-only caveat.

## Files

`selfconsistency_tng300.py` . `results.json` (incremental writes: S0 curve + measured k, ST
validation, per-iteration history, eta-headline + fixed-point projections, shift summary,
eta-sensitivity, per-jackknife fixed points). Runtime ~6 s.
