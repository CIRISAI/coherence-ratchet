# Pre-registration — Claims 1 & 4 at the human-neural substrate (resting-state fMRI)

Pre-registered 2026-05-21, BEFORE any results were computed or inspected.
Part of the structural-claims test series (see `../NOTES.md`).

## Claim under test

`StructuralClaims.lean` Claim 1 (the corridor is a bounded attractor at every
coordinated substrate — off the rigidity pole ρ→1, off the chaos pole ρ→0) and
Claim 4 (the corridor recurs at every coordinated rung under some
effective-dimensionality coordinate).

The human brain at rest IS a coordinated rung — a maintained, non-thermal
system, unlike the particle-physics substrates (E4, pp_*) that returned nulls.
The corridor IS therefore expected here if Claims 1 & 4 hold. **A null at the
human-neural substrate is a genuine partial falsifier and will be reported as
one.** The relevant `FalsifierN` witness (StructuralClaims.lean) is a
coordinated, persistent substrate sitting AT a pole.

## Data — assessed before pre-registration

- HCP (Human Connectome Project): the ideal source, but HCP open-access fMRI
  requires a data-use agreement / ConnectomeDB credentials. Not usable in this
  environment without credentials. **Not used.**
- **CHOSEN: ABIDE Preprocessed (ABIDE-PCP)**, fetched via `nilearn.datasets.
  fetch_abide_pcp`. Fully open, no credentials, no DUA — served from the public
  `fcp-indi` S3 bucket. Pre-computed parcellated ROI timeseries.
  - Pipeline: `cpac`, `filt_noglobal` (band-pass filtered, **no** global signal
    regression — GSR is a confound we control rather than apply, see below).
  - Parcellation: **CC200** (Craddock 200-region functional atlas). k = 200
    nominal constituents (brain regions).
  - `quality_checked=True` (vendor QC pass only).
  - **Subjects: typically-developing CONTROLS only** (`DX_GROUP == 2`). The
    claim is about a *healthy* coordinated rung; the autism group is excluded so
    a clinical-population effect cannot be mistaken for a pole.
  - n: the first **100** quality-checked control subjects returned by the
    fetcher (fixed cap, set before results; if fewer are returned, all of them).

## ρ construction (fixed before results)

Per subject, the ROI timeseries is a (T timepoints × 200 regions) matrix.

1. Each region's timeseries is z-scored across time.
2. Discard regions with zero variance or with fewer than `T` valid samples.
3. The within-rung correlation matrix C is the 200×200 Pearson correlation
   among regions.
4. **ρ_raw = mean of |C_ij| over the off-diagonal entries** — the mean absolute
   pairwise functional connectivity. (Absolute value: anti-correlated regions
   are still coordinated, consistent with the E1 LLM `mean|corr|` measure.)
5. **Finite-timeseries noise floor.** A short BOLD timeseries gives a non-zero
   |correlation| even between independent signals. Floor is measured per
   subject by phase-randomizing each region's timeseries independently (FFT,
   randomize phases, invert) — this destroys cross-region correlation while
   preserving each region's autocorrelation/power spectrum, then recomputing
   mean|C_ij|. Averaged over 5 surrogate draws.
   **ρ_debiased = sqrt(max(ρ_raw² − floor², 0))** (quadrature subtraction, as in
   E1).
6. Secondary coordinate — **effective dimensionality**:
   `k_eff = (Σλ_i)² / Σλ_i²` (participation ratio of the eigenvalues of C),
   and the Kish prediction `k_eff_Kish = k / (1 + ρ(k−1))` with k = 200.
   Reported for the Claim-4 "under some k_eff coordinate" clause.

The primary reported quantity is the **distribution of ρ_debiased across
subjects**.

## Corridor criterion (fixed before results — E1's lesson: a BAND, not a wide window)

The framework's A3+ corridor band, recomputed from five A3+ substrates in
`../../open_system_pomega/corridor_recalculation.py`, is **ρ ∈ ≈ (0.17, 0.35)**,
centre ≈ 0.25. The GPU-substrate envelope (0.10, 0.43) is the wider, retired
number and is NOT the criterion.

CORRIDOR CONFIRMED (Claims 1 & 4 supported at the human-neural substrate) iff
ALL of:
- **C1 — off the rigidity pole:** the upper tail stays clear of ρ→1.
  Operationally: 95th-percentile ρ_debiased < 0.60, and no subject above 0.80.
- **C2 — off the chaos pole:** the lower tail stays clear of ρ→0.
  Operationally: 5th-percentile ρ_debiased > 0.05, i.e. the debiased signal is
  resolvably non-zero for the bulk of subjects.
- **C3 — a bounded band, not a broad spread:** the subject distribution is
  unimodal and concentrated — interquartile range ≤ 0.15, and the median sits
  inside the recalculated A3+ band (0.17, 0.35). A broad spread spanning most of
  (0,1), or a bimodal pile-up at the poles, FAILS C3 even if C1/C2 pass.

PARTIAL: C1 and C2 pass (off both poles) but C3 fails (median outside the A3+
band, or IQR too wide) — corridor exists as "off the poles" but the human-neural
band does not coincide with the framework's calibrated A3+ band. Reported as
weakly-supported, mirroring E1's verdict.

FALSIFIER (Claims 1 & 4 partially falsified at this substrate): C1 fails (pile-up
toward rigidity) OR C2 fails (debiased ρ within noise of zero for the bulk) —
a coordinated, persistent substrate sitting at a pole.

## Confound controls (fixed before results)

1. **Motion artifact.** Head motion inflates short-range functional
   correlation. Control: (a) report Spearman correlation between ρ_debiased and
   `func_mean_fd` (mean framewise displacement) across subjects; (b) re-test the
   corridor criterion on the low-motion subset (`func_mean_fd` < 0.20 mm). If
   the corridor verdict flips between the full and low-motion sets, motion is
   driving it and the result is reported as motion-confounded.
2. **Global-signal effects.** GSR is contested and itself shifts the
   correlation distribution negative. We use the `filt_noglobal` (no-GSR)
   pipeline as primary. As a sensitivity check the no-GSR result is the
   reported one; we additionally note that the noise-floor subtraction and the
   |·| absolute-value measure make the result less GSR-sensitive than a signed
   mean-FC would be. (A full GSR-pipeline re-fetch is noted as owed if the
   primary result is borderline.)
3. **Finite-timeseries noise floor.** Handled in the ρ construction (step 5):
   phase-randomized surrogates, quadrature subtraction. Without this a short
   run produces spurious non-zero ρ and a false "off-chaos" pass.
4. **Site heterogeneity.** ABIDE pools ~17 acquisition sites with different
   scanners and TRs. Control: report the per-site median ρ_debiased; if the
   corridor verdict depends on which sites are included, report as
   site-heterogeneous. The primary verdict uses all sites pooled.

## What would make this a null

- Debiased ρ within noise of zero for most subjects (chaos pole) — C2 fails.
- ρ piled up near 1 (rigidity pole) — C1 fails.
- ρ spread broadly across most of (0,1) with no concentration — C3 fails, no
  band.
Any of these is reported as a partial falsifier of Claims 1 & 4 at the
human-neural substrate, exactly as the particle-physics nulls were reported.

## Files

- `fmri_corridor.py` — the test script.
- `RESULTS.md` — written after, committed in a separate commit AFTER this file.
