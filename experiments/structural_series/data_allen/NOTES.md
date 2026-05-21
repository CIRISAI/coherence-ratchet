# Allen Brain Observatory corridor test — Claims 1 & 4 — RESULT

Run 2026-05-21. `exp_allen_corridor.py`, real Allen Brain Observatory data via
AllenSDK 2.16.2 (`BrainObservatoryCache`). Pre-registration in
`PREREGISTRATION.md`, committed before any result. This file written after.

## Data tested

- 32 imaging sessions selected, `three_session_A` (carries a spontaneous
  grey-screen epoch), 8 per cortical area across VISp / VISl / VISpm / VISal.
- 7 excluded by the pre-registered QC floor (< 10 valid ROIs). 25 sessions
  yielded a valid within-rung ρ.
- Two-photon calcium ΔF/F, neuropil-subtracted (Allen pipeline). Within-rung
  ρ = mean off-diagonal |Pearson correlation| of the ΔF/F traces on the
  spontaneous epoch only (~5 min, ~9k frames at 30 Hz) — intrinsic
  coordination, not a shared stimulus drive.
- Noise floor by circular-time-shift shuffle (preserves each neuron's
  autocorrelation, destroys cross-neuron correlation), debiased in quadrature.

## Result — debiased within-rung ρ distribution

| area  | n_sess | debiased ρ range | median |
|-------|--------|------------------|--------|
| VISp  | 6      | 0.012 – 0.161    | 0.066  |
| VISl  | 7      | 0.020 – 0.065    | 0.022  |
| VISpm | 6      | 0.008 – 0.064    | 0.027  |
| VISal | 6      | 0.022 – 0.063    | 0.023  |

Pooled (25 sessions): debiased ρ [0.008, 0.161], **median 0.023**, IQR
[0.022, 0.044]. Noise floor mean 0.012 (small — debiased ρ ≈ raw ρ, so the
low value is NOT a noise-floor artifact). k_eff (participation ratio) median
9.7, range 2.7–59 (k_eff tracks neuron count, not a corridor coordinate here).

At the rigidity pole (debiased ρ > 0.90): **0 / 25**.
At the chaos pole (debiased ρ < 0.03): **15 / 25** (60%).

## Verdict — FALSIFIER (per the pre-registered ladder)

The pre-registered falsifier threshold was ≥ 20% of sessions pole-pinned.
**60% of sessions sit at the chaos pole.** This is a clean, decisive
falsifier-direction result, not a marginal one.

- The rigidity pole is clean — not one mouse-visual-cortex session shows the
  neurons collapsing to a single synchronised voice. That half matches the
  framework.
- The chaos side is NOT clean and NOT marginal. Spontaneous-activity pairwise
  correlation in mouse V1/LM/PM/AL is genuinely tiny: median ρ ≈ 0.023, with
  most sessions within noise of zero. The mouse visual-cortex population in
  grey-screen rest is a near-decorrelated substrate, not a corridor occupant.
- The neuropil cross-check makes it worse, not better. On detected-events
  traces (neuropil-insensitive) the median ρ is 0.006 — events/ΔF/F ratio
  0.28. The small ΔF/F correlation is partly residual neuropil; the genuine
  spike-level correlation is lower still. So the chaos-pole reading is
  conservative — the true coordination signal is even weaker.

## Honest reading vs the framework's prior neural result

The framework's existing neural anchor is C. elegans whole-brain calcium
(within-class bands ρ ≈ 0.25–0.75) — mid-corridor to rigidity-side. The Allen
mouse visual cortex, an independent neural substrate, returns ρ ≈ 0.02 —
**an order of magnitude below the A3+-recalibrated corridor band (0.17–0.35,
`corridor_recalculation.py`)**, sitting at the chaos pole.

This is a genuine partial falsifier of Claims 1 & 4 at the neural substrate,
and is reported as such per the pre-registration — it is not explained away.
A brain is the substrate the framework most expects the corridor at; mouse
visual cortex does not deliver it under this operationalisation.

Two readings, both honest, neither rescues the claim as stated:

1. **The claim is wrong at this rung.** Sustained coordination need not show
   up as bounded *pairwise* correlation. Mouse visual cortex is famously
   low-dimensional in its *shared variability* (a few global modes) yet
   low in mean pairwise correlation — the coordination lives in structured
   low-rank covariance, not in a mid-band mean |corr|. The within-rung ρ
   defined as mean |pairwise corr| simply does not detect it. If so, Claim 1's
   operationalisation (not its spirit) fails here: the corridor coordinate
   has to be a covariance-structure measure, not mean pairwise correlation.

2. **The substrate genuinely sits at chaos.** Spontaneous grey-screen cortex
   is near-asynchronous by design (efficient coding decorrelates); the
   "coordinated rung" is the stimulus-evoked / task regime, not rest. The
   spontaneous epoch was chosen to control the stimulus confound, but it may
   have selected the substrate's least-coordinated state.

Either way, the pre-registered measure returned a chaos-pole pile-up, and the
recurrence test (Claim 4) shows the SAME chaos-pole result across all four
cortical areas — recurrence of the *null*, not of a corridor.

## Recurrence (Claim 4)

The result recurs across all four areas: every per-area median is 0.02–0.07,
all four at or near the chaos pole. The spread of per-area medians is 0.044.
So Claim 4 is "satisfied" only in the degenerate sense that the chaos-pole
result is reproducible — there is no corridor band to recur.

## Confound controls — all applied

1. Noise floor: circular-shift shuffle, debiased in quadrature. Floor ~0.012,
   far below the result; debiasing changed ρ by < 0.003. The low ρ is real.
2. Neuropil: ΔF/F is Allen-neuropil-subtracted; events cross-check (ratio
   0.28) shows the ΔF/F ρ is itself partly residual neuropil — the true
   correlation is lower. The chaos verdict is conservative.
3. Heterogeneity: ρ reported per session with n / area / cre-line / depth in
   `results.json`; recurrence tested per area, not pooled. No area escapes
   the chaos pole.
4. Epoch: spontaneous (grey-screen) only — correlation is intrinsic, not a
   shared stimulus drive.
5. QC: 7 sessions with < 10 ROIs excluded and counted.

## Scope and what is owed

25 sessions, one mouse-line-mixed dataset, one session type, one epoch, one
operationalisation (mean |pairwise corr| of ΔF/F). The honest claim: under the
framework's published within-rung-ρ operationalisation, mouse visual cortex at
spontaneous rest is at the chaos pole — a partial falsifier of Claims 1 & 4.
What this run cannot settle: whether a covariance-structure k_eff coordinate
(reading 1) or the evoked regime (reading 2) would place the substrate in a
band. Those are the two follow-ups the result points to; neither is run here,
and neither is assumed to rescue the claim.
