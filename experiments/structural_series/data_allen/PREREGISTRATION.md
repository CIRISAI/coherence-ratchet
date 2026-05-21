# PRE-REGISTRATION — Allen Brain Observatory corridor test (Claims 1 & 4)

Pre-registered 2026-05-21, BEFORE any correlation results were computed. The
feasibility probe (one session downloaded, ΔF/F trace shape inspected, API
confirmed accessible) was done first; the analysis proper had not been run when
this file was committed.

## What is under test

`StructuralClaims.lean` Claim 1 (the corridor is a bounded attractor at every
coordinated substrate — off rigidity ρ→1, off chaos ρ→0) and Claim 4 (the
corridor recurs at every coordinated rung). A mouse visual cortex is a
coordinated rung in the framework's sense (A2/A3 neural substrate), unlike the
particle-physics observables that returned nulls. So the corridor IS expected
here if Claims 1 & 4 hold. The framework's existing neural result is C. elegans
whole-brain calcium (within-class bands ρ ≈ 0.25–0.75); the Allen mouse
visual-cortex two-photon dataset is an INDEPENDENT neural substrate.

## Substrate and data

Allen Brain Observatory — mouse visual cortex, two-photon calcium imaging,
public, via the AllenSDK `BrainObservatoryCache`. Within-rung correlation ρ =
the mean pairwise activity correlation among simultaneously-recorded neurons in
one imaging session (ΔF/F traces). One imaging session = one "rung instance".
Effective dimensionality k_eff is reported alongside.

## The rung and the constituents

- Rung instance: one ophys imaging session (one cortical area, one mouse, one
  imaging plane). Constituents: the simultaneously recorded neurons (ROIs) in
  that session, n typically 20–250.
- Within-rung ρ: mean off-diagonal |Pearson correlation| of the ΔF/F traces,
  computed on the SPONTANEOUS-activity epoch only (grey screen, no stimulus) —
  so the measured correlation is intrinsic coordination, not a shared
  stimulus drive. This is the analogue of E1's within-layer ρ.
- k_eff: the participation-ratio effective dimensionality of the
  neuron×neuron covariance, k_eff = (Σλ)² / Σλ², computed on the same epoch.

## Corridor criterion (the operational definition — fixed BEFORE results)

E1's lesson: a corridor is a BOUNDED INTERIOR BAND, not a wide window. The
A3+-recalibrated band (corridor_recalculation.py) is ρ ≈ 0.17–0.35, centre
~0.25. The criteria, in descending strength:

- POLE TEST (the falsifier-relevant test). Rigidity pole: debiased ρ > 0.90.
  Chaos pole: debiased ρ < 0.03 (within finite-sample noise of zero). A
  coordinated, persistent neural substrate pinned at either pole, with no
  identifiable active maintenance, is a Claim-1 FALSIFIER witness.
- BAND TEST (corridor confirmation, the stronger positive result). The
  per-session debiased ρ distribution sits as a bounded band — interquartile
  range width ≤ 0.25 AND the band lies strictly interior (both quartiles in
  (0.03, 0.90)). A confirmation requires the band, not merely "off the poles".
- RECURRENCE (Claim 4). The band must reproduce across sessions AND across
  the ≥3 distinct cortical areas sampled — same interior band, no area pinned
  at a pole. A single area at a pole while others are mid-band is a partial
  Claim-4 failure.

Verdict ladder, fixed in advance:
- CONFIRMED: no pole pile-up; debiased ρ forms a bounded interior band
  (IQR ≤ 0.25, interior); band recurs across areas.
- WEAKLY SUPPORTED: off both poles but the spread is broad (IQR > 0.25) or
  the band sits at a corridor EDGE (E1-style chaos-edge result).
- FALSIFIER: ≥ 20% of sessions pinned at a pole, OR an entire cortical area
  pole-pinned, with the substrate coordinated+persistent+unmaintained.
- NULL / NO CORRIDOR: debiased ρ shows no band — broad uniform spread across
  (0, 0.9) with no concentration, or bimodal pole-and-mid split.

A null or falsifier here is a GENUINE partial falsifier of Claims 1 & 4 and
will be reported as such, not explained away. A brain is the substrate the
framework most expects the corridor at; failure here matters.

## Confound controls (fixed BEFORE results)

1. FINITE-SAMPLE NOISE FLOOR. The pairwise-correlation estimate is biased away
   from zero by finite samples. Control by E1's shuffle-baseline debiasing:
   independently circularly time-shift each neuron's trace (preserving each
   neuron's autocorrelation but destroying cross-neuron correlation), recompute
   mean |corr| as the noise floor, debias in quadrature:
   ρ_debiased = sqrt(max(ρ_raw² − ρ_floor², 0)).
   Circular shift (not plain permutation) because calcium traces are
   strongly autocorrelated; plain permutation would understate the floor.
2. NEUROPIL CONTAMINATION. Two-photon ΔF/F has contamination from out-of-cell
   neuropil signal, which inflates pairwise correlation spuriously and
   uniformly. The Allen pipeline already applies neuropil subtraction to the
   published ΔF/F traces. As an additional control, the analysis is also run
   on the events traces (`get_demixed_traces` / detected-events where
   available), which are far less neuropil-sensitive; if ρ collapses toward
   zero on events, the ΔF/F result is contamination-driven and reported so.
3. SESSION / AREA HETEROGENEITY. Sessions vary in n (neuron count), cre line,
   imaging depth, area. Report ρ per session with these covariates; test
   recurrence as a per-area distribution, not a pooled mean. Compute ρ as the
   mean of |corr| (k-independent within reasonable n) and report n alongside.
4. EPOCH. Use the spontaneous epoch so the correlation is not a shared
   stimulus drive. If the spontaneous epoch is too short for a stable floor,
   report the floor's own variability.
5. MOTION / NEURON COUNT FLOOR. Sessions with < 10 valid ROIs after QC are
   excluded (too few constituents to define a within-rung correlation);
   exclusions are counted and reported.

## Scope and feasibility

The full dataset is ~2534 sessions; each NWB file is ~hundreds of MB and
downloads in ~1–2 min. Honest scope: a few tens of sessions across ≥ 3
cortical areas (VISp, VISl, VISpm, plus others if time permits), one session
type (`three_session_A`, which carries a spontaneous epoch). Final session
count is reported. If downloads stall, the count is whatever completed; a
partial result with an honest n is preferred over none.

## Falsifier (single sentence)

If the Allen mouse visual-cortex neural populations are pinned at a pole
(debiased ρ > 0.90 or < 0.03) across sessions, or show no bounded band at all
(broad featureless spread), that is a witness against Claims 1 & 4 at the
neural substrate and will be reported as a partial falsification.
