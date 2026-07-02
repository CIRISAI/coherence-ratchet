# Fast-spike positive control for the detailed-balance (bound-vs-coordinating) detector

**Bottom line: YES — fast spike-train data gives a CLEAN detailed-balance positive
control.** Macaque motor cortex during reaching breaks detailed balance strongly
(winding-rate |z| = 8.8 at the primary 20 ms binning, rising to 44 once spike-count
shot noise is smoothed away), far above the null ceiling (~1.5) and far above the
weak ~1 s calcium C. elegans result (median |z| = 2.75). The detailed-balance axis
works — the earlier weak calcium signal was a slow-substrate/measurement limitation,
not the detector failing.

## Dataset

- **DANDI:000140 — MC_Maze_Small**, `sub-Jenkins_ses-small_desc-train_behavior+ecephys.nwb`
  (29.2 MB). Macaque primary motor (M1) + dorsal premotor (PMd) cortex, sorted
  spikes, delayed-reach maze task. Churchland/Kaufman/Shenoy lineage — THE textbook
  system for directed **rotational population dynamics** (jPCA; Churchland et al.
  2012, *Nature*). During movement the population state traces consistent directed
  loops in its top principal plane; a directed loop breaks detailed balance by
  construction, so this is a maximally clean positive control.
- Fetched directly from the DANDI REST API; NWB is HDF5, read with `h5py` (no
  pynwb/dandi needed). Real data only; synthetics only calibrate the ruler.
- **142 sorted units, 131,669 spikes, 293.7 s continuous, 100 successful reaches**
  with absolute `move_onset_time`.

## units × time construction

Spikes binned into neurons × time-bins histograms, lightly Gaussian-smoothed along
time (σ = 1 bin primary). Two matrices:

| matrix | binning | shape (N × T) | rationale |
|---|---|---|---|
| whole-session | 20 ms, full 293 s | 142 × 14,684 | conservative; idle inter-trial periods included |
| move-aligned | 20 ms, [−100, +500] ms per reach, concatenated | 142 × 3,000 | rotation-rich movement epoch |

## (1) Saturation — is k_eff bounded / low-rank?

**Low-rank / bounded, once shot noise is accounted for.** The debiased effective
rank (eigenvalues above the phase-randomized surrogate floor) is **small: 2–8**
across every binning/smoothing setting. Raw 20 ms spike counts give an inflated
participation ratio (PR ≈ 117) and a PR-subsampling exponent β ≈ 0.85 (looks
"extensive") — but that inflation is **Poisson spike-count shot noise**, not signal:
as smoothing suppresses shot noise the PR collapses 132 → 58 and the effective rank
holds at 5–6. So β on raw counts is not a usable saturation readout for spikes; the
surrogate-debiased effective rank (5–8) is, and it says bounded/low-rank — consistent
with the calcium C. elegans low-rank verdict.

## (2) Detailed balance — winding-rate |z|

| system | T | winding-rate |z| |
|---|---|---|
| **whole-session (M1/PMd, 20 ms)** | 14,684 | **8.83** |
| **move-aligned (M1/PMd, 20 ms)** | 3,000 | **5.81** |
| null ceiling (OU-equilibrium / relaxation) | — | ~0.6–2.3 |
| calcium C. elegans (prior, ~1 s substrate) | — | 2.75 |
| clean-cycle synthetic reference | — | ~16 |

Both spike matrices sit **well above the null and above the calcium reference**.
The move-aligned run is lower than whole-session only because it has ~5× fewer bins
(larger bootstrap SE); the per-step winding rate is comparable.

**Ruler check (calibrators re-run at matched T):** OU-equilibrium |z| ≈ 0.6, relaxation
≈ 1.2–2.3 (nulls); noisy limit cycle ≈ 11–35; OU-driven NESS ≈ 50–92. The detector's
null floor and cycle ceiling reproduce at the data's T, so the M1 value is read on a
validated scale.

## Robustness — not a binning artifact

The directed cycle is a **firing-rate-level** phenomenon, so suppressing spike-count
shot noise should *strengthen* it. It does:

| bin | smooth σ | |z| | eff_rank(surr) | PR |
|---|---|---|---|---|
| 10 ms | 1.0 | 4.64 | 8 | 131.8 |
| 10 ms | 2.5 | 10.26 | 8 | 110.7 |
| 20 ms | 1.0 | 8.83 | 8 | 117.2 |
| 20 ms | 2.5 | 17.34 | 6 | 87.0 |
| 50 ms | 1.0 | 23.13 | 6 | 87.1 |
| 50 ms | 2.5 | 44.03 | 5 | 58.1 |

|z| rises monotonically with better rate estimation (4.6 → 44, approaching the
OU-driven NESS regime) while effective rank falls to 5 — i.e. the system is
simultaneously **strongly detailed-balance-breaking and low-rank**. A binning
artifact would not behave this way; a real rate-level rotation does.

## Verdict

Fast spike data delivers the clean positive control the slow calcium recording could
not. Motor cortex during reaching — a coordinating system with a known directed
population rotation — breaks detailed balance decisively (|z| = 8.8 primary, up to 44
with rate smoothing) versus a ~1.5 null and a 2.75 calcium signal, and is
low-rank/bounded on the debiased effective-rank readout. The detailed-balance axis of
the bound-vs-coordinating detector is confirmed to work on good (fast, coordinating)
data.

*Outputs: `spectral_results_spikes.json` (all numbers), `spectral_spikes.py` (analysis;
NWB kept out of the repo tree, path via `MC_MAZE_NWB` env or beside the script).
No commit, no `.lean` edits.*
