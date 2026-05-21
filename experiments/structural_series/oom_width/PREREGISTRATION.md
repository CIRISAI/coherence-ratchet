# PRE-REGISTRATION — Do the framework's corridors share a ~one-OOM width?

Committed BEFORE the corridor numbers were collected or the widths computed.
Git history is the proof: this commit precedes the RESULT commit.
2026-05-21.

## Hypothesis

A prior session found the cross-rung coupling corridor is g/J ∈ (0.3, 3) —
exactly one decade, centred on parity. The hypothesis under test:

> ONE order of magnitude is the framework's characteristic *corridor width*.
> Every corridor the framework has empirically measured is ~one decade wide
> on its natural multiplicative (log) axis.

This is a regularity claim about corridor *width*, distinct from any claim
about corridor *location* (the framework already says location is
substrate-local). If true, it says corridors are non-fine-tuned bounded bands
of a characteristic scale. If false (the widths scatter), one-OOM is a rule of
thumb for the g/J case only, not a law.

## Corridors to be collected

Every corridor the framework has *empirically measured* (real data, already in
the repo). Sources fixed in advance:

1. LLM within-layer ρ band — `exp_E1_llm_corridor.py` / `structural_series/NOTES.md`.
2. fMRI functional-connectivity ρ band — `data_fmri/RESULTS.md`.
3. TCGA healthy-tissue ρ band — `data_tcga/RESULT.md` (pooled primary cancers).
4. Allen mouse-cortex ρ — `data_allen/NOTES.md`.
5. C. elegans ρ — `corridor_dynamics/celegans/results_corridor_relaxation.json`.
6. CMB shape-sector ρ_ℓ band — `open_system_pomega/cmb_corridor_prediction.py`.
7. A3+ within-rung corridor (recalibrated) — `open_system_pomega/corridor_recalculation.py`.
8. Cross-rung g/J band — `open_system_pomega/crossrung_oom_band.py` /
   `crossrung_series/path1_tau/RESULT.md`.
9. GPU substrate corridor (the original anchor) — `CLAUDE.md`.

A corridor enters the cluster test only if it has two cleanly extractable
bounds [lower, upper] on a *coordinated* substrate. A falsifier result
(substrate pinned at a pole, no band) does NOT supply a corridor width — it is
reported but excluded from the cluster statistic, with the exclusion stated.

## Per-corridor log-width definition (fixed before collection)

The natural multiplicative quantity is **k_eff**, not ρ. ρ is a correlation
(bounded [0,1], not multiplicative); k_eff = k/(1+ρ(k-1)) is an effective
dimensionality (a count — a genuine multiplicative quantity). The Kish
asymptotic is the bridge: as k → ∞ at fixed ρ, k_eff → 1/ρ. So a corridor's
multiplicative span is the span of k_eff.

Definition. For a corridor:

- **If the corridor is stated as a coupling/dimensionality ratio already
  multiplicative** (g/J; k_eff directly): width = log10(upper / lower).

- **If the corridor is stated as a ρ-band [ρ_lo, ρ_hi]**: convert to k_eff and
  take the log-width. Use the **substrate-independent asymptotic**
  k_eff ≈ 1/ρ (the k → ∞ Kish limit), so

  ```
  width = log10( k_eff(ρ_lo) / k_eff(ρ_hi) ) = log10( (1/ρ_lo) / (1/ρ_hi) )
        = log10( ρ_hi / ρ_lo )
  ```

  i.e. the log-width of a ρ-band, read on the k_eff axis via the asymptotic
  Kish map, is just log10(ρ_hi/ρ_lo). This is the **primary** width measure:
  it is k-free and therefore the only substrate-independent choice (constituent
  counts k are estimated, not measured, for most substrates — see
  `corridor_recalculation.py`).

- **Robustness companion (reported, not primary)**: for any ρ-band where a
  substrate k is available, also compute the finite-k k_eff width
  log10(k_eff(k,ρ_lo)/k_eff(k,ρ_hi)). Finite k makes k_eff *less* spread than
  1/ρ (k_eff saturates), so the finite-k width is a LOWER bound on the
  asymptotic width. Reporting both brackets the answer.

Where it matters, and disclosed now: log10(ρ_hi/ρ_lo) is identical to the
log-width of the ρ-band itself. So the "convert to k_eff" step does not change
the number for ρ-band corridors — it only changes the *interpretation* (the
axis is effective-dimensionality, not raw correlation). The honest statement
is: the primary measure is log10(upper/lower) of whatever multiplicative
quantity the corridor most naturally lives on, and for ρ-bands the Kish
asymptotic certifies that ρ_hi/ρ_lo IS the k_eff ratio. The finite-k companion
is where a real numerical difference can appear, and it is reported.

For a ρ-band, the bounds used are the **measured corridor edges** as reported
by each source. Where a source gives both a full range and a percentile band
(e.g. fMRI p5–p95), the percentile band is used as primary (it is the
source's own corridor-criterion band, robust to single-subject tails), and the
full range is reported as a width-upper-bound companion.

## Cluster criterion (fixed before collection)

The hypothesis is "~one OOM". Pre-registered decision rule, on the **primary**
log-widths of the coordinated-substrate corridors:

- **CLUSTERED at ~1 OOM** (hypothesis supported) iff BOTH:
  (a) every primary log-width lies in [0.6, 1.5] decades, AND
  (b) the sample standard deviation of the primary log-widths is < 0.30 decade.

- **SCATTER** (hypothesis not supported) iff either (a) or (b) fails.

Justification of the bounds. A "characteristic width of one OOM" should mean
the corridors land within roughly a factor-of-2-to-3 of one decade — [0.6, 1.5]
is "between ~4× and ~30× span", a band centred near 1.0 on a log scale (its
geometric centre is 10^((0.6+1.5)/2) ≈ 0.95 decade). A std < 0.30 decade means
the widths agree to within a factor of ~2 of each other — tight enough that
"one OOM" is a real shared scale rather than an average over a wide spread.
If the widths range over, say, [0.3, 2.5] decades, that is an 8×-to-300×
span — no characteristic width, and the criterion correctly returns SCATTER.

Both conditions are required: (a) catches individual outliers, (b) catches the
case where every corridor is in-band but the distribution still fills the band.

## What would falsify / what would confirm

- CONFIRM: all coordinated corridors 0.6–1.5 decades, std < 0.30. One OOM is a
  real characteristic corridor width of the framework.
- FALSIFY: widths scatter outside [0.6, 1.5] or std ≥ 0.30. One-OOM is then a
  property of the g/J corridor specifically, not a framework-wide law, and
  should be stated as such.

Either outcome is reported. A null is as informative as a positive: it tells
the framework whether "corridor width" is a transferable quantity.

## Honesty commitments

- Real, already-measured numbers only; each width cites its source file.
- If a corridor's bounds are not cleanly extractable, that is stated and the
  corridor is excluded with the reason given.
- The verdict is whatever the criterion returns, computed mechanically.
