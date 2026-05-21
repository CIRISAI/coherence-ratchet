# RESULT — Do the framework's corridors share a ~one-OOM width?

Post-measurement. Pre-registered design in `PREREGISTRATION.md`, committed in a
PRECEDING commit (git history is the proof). 2026-05-21.
Reproduce: `python3 compute_oom_widths.py`.

## The question

A prior session found the cross-rung coupling corridor is g/J ∈ (0.3, 3) —
exactly one decade. Hypothesis: one order of magnitude is the framework's
characteristic *corridor width* — every empirically measured corridor is
~one decade wide on its natural multiplicative (log) axis.

## Width definition (pre-registered, unchanged)

Natural multiplicative quantity is k_eff (effective dimensionality), not ρ.
For a corridor already on a multiplicative axis (g/J, k_eff):
`width = log10(upper/lower)`. For a ρ-band, the Kish asymptotic k_eff → 1/ρ
gives `width = log10(ρ_hi/ρ_lo)`. Disclosed in the prereg and confirmed here:
for a ρ-band this is numerically identical to the log-width of the ρ-band
itself — the "convert to k_eff" step changes the *interpretation* of the axis
(effective dimensionality, not raw correlation) but not the number. Finite-k
k_eff widths are reported as a companion; they are marginally *smaller* than
the asymptotic widths (k_eff saturates), so they do not rescue the hypothesis.

## Per-corridor log-widths (decades)

| Corridor | substrate | bounds | axis | **width (dec)** | source |
|---|---|---|---|---:|---|
| LLM within-layer ρ (E1) | LLM internals | ρ [0.046, 0.218] | ρ→k_eff | **0.676** | `structural_series/NOTES.md` |
| fMRI FC ρ | human neural | ρ p5–p95 [0.168, 0.464] | ρ→k_eff | **0.441** | `data_fmri/RESULTS.md` |
| TCGA healthy ρ | cellular | ρ [0.159, 0.625] | ρ→k_eff | **0.594** | `data_tcga/RESULT.md` |
| C. elegans ρ | whole-brain neural | ρ [0.264, 0.382] | ρ→k_eff | **0.161** | `corridor_dynamics/celegans/results_corridor_relaxation.json` |
| CMB shape-sector | cosmological | k_eff [2.8, 4.8] | k_eff direct | **0.234** | `open_system_pomega/cmb_corridor_prediction.py` |
| A3+ within-rung (recalibrated) | 5-substrate envelope | ρ [0.16, 0.35] | ρ→k_eff | **0.340** | `open_system_pomega/corridor_recalculation.py` |
| Cross-rung g/J | cross-rung coupling | g/J [0.3, 3.0] | g/J direct | **1.000** | `open_system_pomega/crossrung_oom_band.py` |
| GPU corridor (reference) | GPU | ρ [0.10, 0.43] / k_eff [2.33,10] | both | **0.633** | `CLAUDE.md` |
| Allen mouse cortex (FALSIFIER) | mouse neural | ρ [0.008, 0.161] | — | (1.304) | `data_allen/NOTES.md` |

Allen is excluded from the cluster statistic per pre-registration: it is a
falsifier — 60% of sessions pole-pinned at chaos, no corridor band. Its
"width" of 1.30 decades is the spread of a pole-pinned scatter, not a corridor.

## Verdict — SCATTER (hypothesis NOT supported)

Pre-registered criterion on the 7 coordinated corridors:

- **(a) every width in [0.6, 1.5] decades** — **FAIL.** 5 of 7 fall *below*
  0.6: fMRI 0.44, TCGA 0.59, C. elegans 0.16, CMB 0.23, A3+ recalibration
  0.34. Only the g/J corridor (1.00) and the LLM band (0.68) are in-band.
- **(b) sample std < 0.30 decade** — **PASS** (std 0.29), but only because the
  widths are all *small*, clustered low rather than at 1.0.

Both conditions are required. (a) fails decisively. **VERDICT: SCATTER.**

Width range [0.16, 1.00] decades, mean 0.49. The corridors are mostly
*sub-decade* — a factor of ~2–4× span, not a factor of ~10×.

## Honest reading — why one-OOM does not generalise

**1. The g/J corridor's clean decade is special, not representative.**
g/J ∈ (0.3, 3) is the *only* corridor that hits a full decade, and it was the
corridor that generated the hypothesis. It is also the only one of structural,
not empirical, origin: (0.3, 3) was *chosen* as "the natural width of a
non-fine-tuned band on a log axis centred on parity g/J = 1" — see
`crossrung_oom_band.py` header. It is one-OOM-wide because it was *defined* to
be. The empirically measured corridors, when read on the same log axis, come
out narrower. Generalising from g/J to a framework-wide law was reading the
definition back as a measurement.

**2. The measured corridors are sub-decade.** Mapped to the k_eff axis, the
biological/technological corridors span factors of ~1.4× (C. elegans) to ~4.7×
(LLM) — comfortably under one decade. The A3+ recalibration (ρ 0.16–0.35,
k_eff ~2.5–5) is 0.30–0.34 decade. The CMB k_eff band [2.8, 4.8] is 0.23
decade. Coordination, where it has actually been measured, lives in a band
*tighter* than one OOM.

**3. The corridors are not all the same kind of object — a real caveat.**
This is the load-bearing honesty point. The entries above mix two distinct
constructions:
  - **Criterion bands**: a pre-drawn corridor box (g/J band; A3+ recalibrated
    band; GPU anchor; CMB predicted band). These are *definitions* of where
    the corridor is.
  - **Measured spreads**: the empirical range of ρ across subjects/worms/
    layers (fMRI p5–p95; TCGA pooled range; C. elegans per-worm; LLM per-layer).
    These are *distributions of a measurement*, and their width depends on
    sample size, percentile cut, and substrate heterogeneity — not on an
    intrinsic corridor width.
  A measured-spread width and a criterion-band width are not the same
  physical quantity, and the prereg's single log-width definition flattens
  that distinction. Even granting the flattening, the numbers do not cluster
  at one OOM — so the hypothesis fails regardless. But the cleaner statement
  is: **the framework does not currently have a single, consistently
  constructed "corridor width" to test.** Some corridors are boxes drawn by a
  criterion; others are histograms of a measurement. One-OOM held for one box
  (g/J) that was drawn to be one OOM wide.

**4. The k_eff vs ρ axis choice.** For ρ-bands the choice is numerically
inert (log10(ρ_hi/ρ_lo) either way). It matters only for the two corridors
specified in *both* ρ and k_eff — the GPU anchor and the A3+ recalibration —
and there the two log-widths agree to within 0.04 decade (GPU 0.633 on both;
A3+ 0.340 in ρ vs 0.301 in stated k_eff). So the axis choice does not drive
the verdict. It would matter more if any corridor's k were small *and* its
band were near the rigidity pole, where k_eff saturation compresses the span;
none of the measured corridors is in that regime.

## Bottom line

**One order of magnitude is a rule of thumb for the cross-rung g/J corridor —
where it was put in by construction — not a measured characteristic width of
the framework's corridors.** The seven coordinated corridors scatter from 0.16
to 1.00 decade (mean 0.49); five are sub-decade. The pre-registered cluster
criterion returns SCATTER. The honest framework-level statement: corridors are
bounded bands, typically *narrower* than one decade on the k_eff axis, and the
framework does not yet have a uniformly constructed corridor-width quantity for
which "~1 OOM" could be a law.
