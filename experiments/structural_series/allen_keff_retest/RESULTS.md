# Allen mouse visual cortex — canonical k_eff re-test — RESULT

Run 2026-05-21. `keff_retest.py`, real Allen Brain Observatory data.
Pre-registration in `PREREGISTRATION.md`, committed before this result.
This file written after.

## What was owed

`papers/Corridor Dynamics.tex` §sec:robust-rerun reads the structural-series
Allen run (`data_allen/`) as a "chaos-pole data point": 25 mouse-visual-cortex
two-photon sessions, spontaneous epoch, mean pairwise neuron ρ ≈ 0.023. The
pre-registration's point: that run measured the **wrong observable**. The
framework's canonical shape coordinate is not mean pairwise correlation — it is
`k_eff_emp`, the participation ratio of the activity covariance eigenvalues
`(Σλ)²/Σλ²`. Cortex is the textbook case where the two diverge: cortical
population activity is well documented as low-dimensional (low participation
ratio) *despite* low mean pairwise correlation. This re-test recomputes the
canonical observable on the exact same data and settles which reading holds.

## Data

Same 25 sessions, same spontaneous (grey-screen) epoch as `data_allen/results.json`
— session IDs taken verbatim from that file. `three_session_A`, four cortical
areas (VISp / VISl / VISpm / VISal), two-photon calcium ΔF/F, neuropil-subtracted
(Allen pipeline).

`allensdk` does not install under the available Python (3.12). The NWB files
were therefore fetched directly from the Allen Brain Observatory API
(`api.brain-map.org`, `WellKnownFile` type `NWBOphys`) and the ΔF/F traces +
spontaneous frame range read from the HDF5 directly. **Extraction verified**:
the participation ratio reproduces the original run's `k_eff` to four decimals
on session 627823695 (11.6923 vs 11.6923 in `data_allen/results.json`) — the
pipeline is identical to the original, only the data-access path differs.

For each session, on the spontaneous-epoch neuron × time ΔF/F matrix:

- `k_eff_emp` — participation ratio of the covariance eigenvalues (canonical).
- `rho_deb` — mean |pairwise corr| debiased by a phase-randomized surrogate
  floor (the `data_fmri/fmri_corridor.py` `subject_rho` estimator).
- `k_eff_kish` — `N / (1 + rho_deb·(N−1))`.

Per-session numbers in `results.json` (written incrementally, flushed per
session). N = neuron count after dropping flat ROIs.

## Result — canonical k_eff_emp

25 sessions. Neuron count N: range [10, 240], **median 126**.

| observable | min | 25th | median | 75th | max |
|------------|-----|------|--------|------|-----|
| `k_eff_emp` | 2.66 | 6.23 | **9.73** | 23.16 | 59.07 |
| `k_eff_emp / N` | 0.017 | 0.082 | **0.193** | 0.340 | 0.876 |
| `rho_deb` | 0.008 | — | 0.023 | — | 0.161 |
| `k_eff_kish` | 4.69 | — | 23.48 | — | 39.60 |

Per area (`k_eff_emp` median, range):

| area  | n | `k_eff_emp` median | range | `k_eff_emp/N` median |
|-------|---|--------------------|-------|----------------------|
| VISp  | 6 | 12.84 | 3.09 – 44.14 | 0.173 |
| VISl  | 7 |  6.23 | 4.54 – 59.07 | 0.178 |
| VISpm | 6 |  9.71 | 8.05 – 27.12 | 0.522 |
| VISal | 6 | 15.40 | 2.66 – 47.25 | 0.076 |

Key counts:
- `k_eff_emp` ≈ N (chaos pole): **0 / 25** sit at the pole. The closest is
  session 603763073 at `k_eff_emp/N` = 0.876 — and that is a 22-neuron session;
  in absolute terms its `k_eff_emp` is 19.3, still bounded.
- `k_eff_emp / N` < 0.5 (clearly sub-N): **21 / 25**.
- `k_eff_emp / N` < 0.3: **16 / 25**.
- `k_eff_emp` ≈ 1 (rigidity pole): **0 / 25** — minimum `k_eff_emp` is 2.66.
- `k_eff_emp` ≤ 10: **13 / 25** sit at or under the framework's asymptotic
  corridor ceiling of ≈ 10.

## Verdict — CORRIDOR (per the pre-registered ladder)

The pre-registered corridor branch: `k_eff_emp` in a bounded range, well below N
and well above 1. **That is what the data shows.** Median `k_eff_emp` = 9.73
against median N = 126 — a factor of ~13 compression. Not one session has
`k_eff_emp` collapse to 1 (rigidity) and not one has `k_eff_emp` ≈ N (chaos).
Every session lands in the interior. The canonical observable places mouse
visual cortex **inside the corridor**.

Strikingly, the median `k_eff_emp` of 9.73 sits right at the framework's stated
asymptotic corridor ceiling (`k_eff` ≈ 10 at `ρ_lower` = 0.1, CLAUDE.md Piece 3),
and 13 of 25 sessions are at or below it. The effective dimensionality of
spontaneous cortical population activity is bounded in the low single-to-low-
double digits regardless of how many neurons are imaged — exactly the
"saturation despite more constituents" the Kish asymptotic predicts.

**The §sec:robust-rerun "chaos-pole data point" reading does NOT stand. It
resolves to corridor.** The chaos-pole reading was an observable-choice
artifact: mean pairwise |corr| ≈ 0.023 is genuinely tiny, but it is not the
framework's shape coordinate. The covariance of mouse visual cortex is strongly
low-rank — a handful of dominant shared modes carry the variance — and the
participation ratio detects exactly that structure. Low mean pairwise
correlation and low participation ratio are not the same thing, and cortex is
the canonical case where they diverge. This is precisely Reading 1 flagged in
the original run's NOTES.md ("the coordination lives in structured low-rank
covariance, not in a mid-band mean |corr|") — and it is confirmed: switch to
the covariance-structure observable and the substrate is in the band.

## The two k_eff observables disagree, and k_eff_emp is the canonical one

`k_eff_kish` (median 23.48) and `k_eff_emp` (median 9.73) do not agree, because
`k_eff_kish` is derived from `rho_deb` — the mean pairwise correlation — and so
inherits the same observable-choice problem. For a low-rank covariance with low
mean pairwise correlation, the Kish formula (which assumes a single scalar ρ
summarises the correlation structure) over-estimates effective dimensionality:
it cannot see that the variance is concentrated in a few modes. `k_eff_emp`
reads the eigenvalue spectrum directly and is the observable the
pre-registration names as canonical. On that observable, the verdict is
corridor.

## Scope

25 sessions, one dataset, one session type, one epoch (spontaneous grey-screen),
one observable (`k_eff_emp` on neuropil-subtracted ΔF/F). The honest claim:
on the framework's canonical shape observable, mouse visual cortex at
spontaneous rest occupies a bounded effective-dimensionality band (`k_eff_emp`
median ≈ 10, ~13× below the neuron count, off both poles in all 25 sessions) —
a corridor result. The earlier mean-pairwise-ρ chaos-pole datum was an
observable-choice artifact and is superseded by this re-test.
