# Results — C. elegans neural in-corridor substrate, robust re-run

**Wave:** S1 neural in-corridor (`experiments/structural_series/robust_rerun/`).
**Date:** 2026-05-21. Protocol fixed in `PREREGISTRATION.md` before computation.

## Verdict

**PASS.** v1's C. elegans whole-brain calcium in-corridor finding reproduces
under the robust framing. Healthy whole-brain calcium occupies a bounded
debiased-ρ band off both poles — it does not collapse to chaos (≈0) and does
not pin at rigidity (≈1) once the phase-randomized surrogate floor is
subtracted.

## Data

`qsimeon/celegans_neural_data` (`worm_data_short.parquet`), the same aggregated
whole-brain calcium corpus v1's `run_v15a` / `run_v15b` loaded. 42,798
labeled-and-unlabeled rows; 32,879 labeled-neuron rows; **919 (study, worm)
units** across **12 source studies**. After the pre-registered inclusion gate
(≥4 classified neurons, ≥1 functional class with a pair), **832 worms across
all 12 studies** entered the verdict statistics. Real data, on disk from prior
v15 work — no synthetic data.

(v1's headline was "337 worms, 11 studies." That count reflects v1's
per-functional-class inclusion gate, which is the per-class `command` count
here — exactly 337 worms have a usable command-interneuron pair. The robust
re-run reports the whole-brain count of 832 as the primary N and the per-class
counts alongside.)

## The estimator change

| | v1 (`run_v15a`/`run_v15b`) | robust re-run |
|---|---|---|
| ρ | raw mean \|pairwise Pearson\| per class | **debiased** ρ = √(max(ρ_raw²−floor², 0)), floor = mean ρ of 20 phase-randomized surrogates |
| k_eff | mean-pairwise Kish proxy | **canonical** participation ratio (Σλ)²/Σλ² of the covariance spectrum |

Canonical estimator: `experiments/structural_series/data_fmri/fmri_corridor.py::subject_rho`.

## Debiased vs raw — the headline numbers

**Whole-brain (832 worms):**

| quantity | value |
|---|---|
| ρ_raw median | 0.357  (range 0.088–0.921) |
| surrogate floor median | 0.176 |
| **ρ_debiased median** | **0.312**  (range 0.000–0.872) |
| ρ_deb percentiles | p5 0.157, p25 0.227, p75 0.423, p95 0.650 |
| ρ_deb IQR | 0.196 |
| k_eff_emp median | 3.9  (range 1.2–12.9) |

Debiasing removes a substantial surrogate floor (median 0.176) but does **not**
zero the correlation: median ρ drops 0.357 → 0.312, and the 5th percentile
stays at 0.157 — well above the chaos cutoff (0.05). The band stays bounded and
off both poles. The canonical k_eff median of 3.9 (with the population
nominally ~80–150 neurons) is the participation-ratio confirmation: a
rigidity-pole worm would collapse to k_eff ≈ 1; chaos would push k_eff toward
the nominal neuron count. 3.9 is squarely intermediate — the corridor signature.

**Per functional class (raw → floor → debiased median):**

| class | ρ_raw | floor | **ρ_deb** | ρ_deb range | n worms | off-chaos |
|---|---|---|---|---|---|---|
| sensory | 0.364 | 0.176 | **0.315** | 0.000–0.870 | 831 | 100% |
| interneuron | 0.406 | 0.191 | **0.358** | 0.116–0.824 | 342 | 100% |
| motor | 0.435 | 0.183 | **0.392** | 0.084–0.867 | 342 | 100% |
| command | 0.626 | 0.191 | **0.597** | 0.000–0.956 | 337 | 99% |

The v1 per-class **rank order survives debiasing**: command sits highest,
sensory/interneuron/motor cluster lower. Debiasing shifts every class down by
roughly its floor but preserves the banded structure. C4 (per-class structure
survives): 829 of 832 worms retain ≥1 class with ρ_deb > 0.05.

## Does v1's specific claim reproduce?

v1 (Corridor Dynamics §sec:corridor-empirical, Substrate 1, and Figure 1):
"command 0.52–0.75 and sensory/interneuron/motor 0.25–0.45 in 10/11 studies",
substrate-local band 0.25–0.75.

Under debiased ρ:

- **command band:** debiased median **0.597**, inside v1's 0.52–0.75 band.
  v1's raw figure was effectively unchanged here — the command floor (0.191) is
  small relative to its raw value (0.626), so debiasing barely moves it.
- **sensory/interneuron/motor:** debiased medians **0.315 / 0.358 / 0.392**.
  v1 quoted 0.25–0.45 for these three — the debiased medians all fall inside
  that band. Raw medians (0.364 / 0.406 / 0.435) were slightly higher;
  debiasing moves them down into the lower part of v1's stated band.
- **substrate-local 0.25–0.75 band:** the debiased per-class medians span
  0.315–0.597, comfortably inside it. The whole-brain debiased band
  (IQR 0.227–0.423, p5–p95 0.157–0.650) is bounded and off both poles.

v1's "Venkatachalam 2024 uniform-at-0.5" note: Venkatachalam2024 whole-brain
debiased median is 0.433 (raw 0.497) — still the highest-but-one study,
consistent with v1's characterization of it as a study-specific elevated
pattern rather than the cross-lab norm. Leifer2023 (0.531) and Nejatbakhsh2020
(0.560) are also elevated; the bulk of studies sit 0.21–0.33.

## Pre-registered criteria

| criterion | threshold | observed | verdict |
|---|---|---|---|
| C1 off chaos | whole-brain ρ_deb p5 > 0.05 | p5 = 0.157 | **PASS** |
| C2 off rigidity | ρ_deb p95 < 0.90 AND median k_eff > 1.5 | p95 = 0.650, k_eff median 3.9 | **PASS** |
| C3 bounded band | ρ_deb IQR ≤ 0.30 AND max < 0.95 | IQR 0.196, max 0.872 | **PASS** |
| C4 per-class survives | ≥60% worms keep a class with ρ_deb > 0.05 | 829/832 = 99.6% | **PASS** |

C1 ∧ C2 ∧ C3 → **PASS**. C4 confirms the per-class banded structure (the
specific shape of v1's finding) also survives, not just whole-brain occupancy.

## Reading

The robust framing strips a real surrogate floor (median 0.176 of the raw
0.357) — phase-randomized calcium traces, sharing only their slow GCaMP power
spectra, already produce ρ ≈ 0.18 of spurious cross-correlation. v1's raw
estimator did not subtract this. Even so, **genuine debiased correlation
survives at every level**: whole-brain median 0.312, every functional-class
median in 0.32–0.60, the command-vs-rest rank order intact, and not a single
study collapsing to the chaos pole. The canonical participation-ratio k_eff
(median 3.9, never near 1) independently rules out the rigidity pole.

v1's C. elegans neural in-corridor claim **stands under the robust framing**.
The debiased numbers are modestly lower than v1's raw numbers — the
sensory/interneuron/motor cluster moves into the lower part of v1's quoted
0.25–0.45 band rather than the middle — but the structural finding (bounded
band, off both poles, per-class banding with command highest) reproduces. No
amendment to v1's Substrate-1 in-corridor text is required for v2; the only
honest refinement is that the band centers sit slightly lower once the
surrogate floor is removed, which v2 can note as a footnote rather than a
retraction.

No whole-wave falsifier fired: healthy whole-brain calcium does not pin at a
pole under debiased ρ.
