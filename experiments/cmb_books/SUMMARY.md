# Bet 11 — DISSOLVED: the low-ell CMB anomalies are jointly typical of one isotropic Gaussian sky

**Verdict: DISSOLVED.** Date 2026-07-11. Registration (`REGISTRATION.md`, frozen + committed
before any data touch, plus a documented pre-data amendment to one functional) is the sole
scorer. Data: Planck 2018 SMICA full-sky temperature (I_STOKES, K_CMB, Galactic, Nside=2048),
`map2alm` to l_max=60. Null: 100,000 isotropic Gaussian skies from the Planck best-fit LCDM TT
spectrum, seeded, per-index reproducible. Code+data: `run_cmb.py`, `results.json`,
`discovery_panel.py`, `discovery_panel.json`; null battery `null_battery.npz` (reproducible).

The seven-functional battery, scored jointly by the three registered depth statistics with the
look-elsewhere effect computed on the null ensemble, places the real low-ell sky **inside the
central 99%** of the isotropic-Gaussian ensemble — at the primary l_max=30 and robustly across
l_max in {10, 60}. The famous individual anomalies each reproduce their known direction and
significance, but they **do not conspire**: taken together they are what one isotropic Gaussian
sky looks like once you count how many ways it could have looked odd. The KILL did not fire.

## The scored result (frozen decision rule)

Joint outlyingness percentile of the 7-vector `(align_23, A_hemi, S_half, Q_amp, axis_conc,
S_logdet, pr_lowell)` in the null cloud — three depths, all must be <= 99.0 to DISSOLVE:

| l_max | Mahalanobis | normal-scores rank | spatial (L1) | tier |
|------:|------------:|-------------------:|-------------:|:-----|
| 10 | 88.18 | 96.69 | 89.30 | DISSOLVE |
| **30 (primary)** | **94.84** | **98.22** | **93.68** | **DISSOLVE** |
| 60 | 81.71 | 96.76 | 75.78 | DISSOLVE |

All three depths agree at all three l_max; none reaches the 99.0 flag line, let alone the
99.73 (3sigma-equivalent) SURVIVE threshold. The Mahalanobis empirical percentile (94.84)
matches its chi^2_7-theory percentile (94.71) — the joint-depth distribution is near-Gaussian,
no hidden non-Gaussian tail. **DISSOLVED, robustly.**

## Per-anomaly sanity reproductions (l_max=30) — each in the literature-expected direction

| functional | data | percentile | tail | reproduces |
|---|---:|---:|:--|:--|
| `align_23` (quad-octopole alignment, \|n2.n3\|) | 0.9994 | **99.95** (upper) | U | the alignment anomaly (~2deg, ~99.9% CL) OK |
| `Q_amp` (quadrupole power) | 200.98 uK^2 | **3.60** (lower) | L | the low quadrupole OK |
| `S_half` (S_1/2 lack of correlation) | 5803 uK^4 | **5.88** (lower) | L | the missing large-angle correlations OK |
| `A_hemi` (hemispherical asymmetry) | 0.291 | 93.1 (upper) | U | the asymmetry, mild (~1.5sigma full-sky) OK |
| `axis_conc` (multi-l preferred-axis conc.) | 0.539 | 77.2 | U | ledger functional — mildly elevated |
| `S_logdet` (cross-l power-map coordination) | 1.917 | 97.9 | U | ledger functional — mildly elevated at l<=30 |
| `pr_lowell` (within-l m-power PR) | 0.389 | 59.5 | L | typical |

The three canonical anomalies (alignment, low quadrupole, S_1/2) reproduce sharply and in the
right tails — the pipeline measures the real sky correctly. The two directional-coordination
ledger functionals (`axis_conc`, `S_logdet`) pick up the known low-l directional structure
mildly at l_max=30 (S_logdet 97.9th) and wash out by l_max=60 (76th) — the coordination that
exists is a large-scale, few-l effect, exactly where the alignment lives.

## Look-elsewhere, reported both ways (honest, incl. the one adverse number)

- **Registered union** (P any of 7 marginals >= as extreme as the data in its tail): 0.68–0.89
  across l_max. This **saturates by construction** — several data marginals sit mid-distribution
  (e.g. `pr_lowell` at the 60th pct), so "at least one marginal beyond the data's least-extreme
  one" is near-certain. It conveys only that the marginal pattern is unremarkable; not the sharp
  statistic.
- **Discovery-panel count metric (auxiliary, NOT the scorer):** the data has **3 of 7** marginals
  beyond their 95th-percentile tail at l_max=30; on the ensemble `P(a random isotropic sky shows
  >= 3 such) = 0.0069` (~2.7sigma), vs a null mean of 0.35 flagged marginals. **This coarse count
  statistic is the one adverse number** — it reads the sky as mildly atypical (~2.7sigma). It
  discards magnitude and the null covariance geometry (the flagged functionals are positively
  correlated — directional-coordination reads co-vary), which is exactly what the registered
  Mahalanobis/spatial depths account for and why they land at ~94–98th, not 99.3rd. Reported for
  transparency; the frozen scorer is the joint depth, and it clears the DISSOLVE bar.

**Positioning (honest):** the dissolution is comfortable on the registered joint-depth scorer
(the most powerful, covariance-aware statistic) and robust across l_max; it is *not* overwhelming
— the normal-scores depth (98.2) is closest to the flag line, and the coarse anomaly-count sits
at 2.7sigma. "Jointly typical, mildly unusual," not "perfectly ordinary."

## What the verdict does to the stance

- **The KILL did not fire.** The joint atypicality does **not** survive at >=3sigma-equivalent —
  the registered kill (joint SURVIVES => the books did not open empty; past-hypothesis answer and
  orthogonality fence both wounded) is **not triggered**. Both the coordination past hypothesis
  (`mystery_map.md` sec.1: the primordial arrangement books opened empty, `S_coord ~ 0`) and the
  orthogonality fence (CLAUDE.md: exactly LCDM in the linear/perturbation sector) **pass this
  test**: a real primordial coordination structure that would sit in the fenced sector is absent
  at the level the battery can see.
- **But it earns nothing beyond consistency (Discipline rule 2).** These anomalies and the sky's
  Gaussianity were already known; a dissolved anomaly is a retrodiction / consistency check, not
  novel confirmed risk. No residual-first rights accrue. The result is a passed self-imposed bet,
  logged as such — the framework staked a real way to be wounded here and was not wounded.
- **Dated debt / live tension:** the ~2.7sigma coarse anomaly-count is a named, non-scoring
  adverse reading. Kill-adjacent condition: were a Planck-independent low-l dataset to push the
  *joint depth* — not the count — past 99.73 robustly, the KILL fires after all. On present Planck
  SMICA it does not.

## Method transferred (one line, no more)

The flavor-sector method (`sm_escalator_mixing/`) moved to the CMB: one pre-registered functional
battery vs one structureless null ensemble, joint depth statistics (Mahalanobis + rank + spatial),
look-elsewhere on the ensemble. Every individual anomaly statistic is prior art (de Oliveira-Costa
et al. 2004; Eriksen et al. 2004; Copi, Huterer, Schwarz & Starkman 2009; Spergel et al. 2003;
Planck 2018 results VII, A&A 641 A7; review Schwarz, Copi, Huterer & Starkman, "CMB anomalies
after Planck", CQG 33, 184001, 2016 — verified). The look-elsewhere / a-posteriori point is
Bennett, Hill & Hinshaw 2011 (ApJS 192, 17, arXiv:1001.4758 — verified). **Ours is exactly the
pre-registered JOINT verdict with ensemble look-elsewhere, nothing more** — and it lands on
Bennett et al.'s side: the low-l anomalies are jointly an a-posteriori selection from one
isotropic Gaussian sky.

## Caveats (stated plainly)

- **Full-sky, no mask** (registered primary): the SMICA full-sky component-separated map carries
  residual foreground at the largest scales; a masked re-analysis (which couples l) is deferred.
  The full-sky treatment applies identically to data and null.
- One functional's frozen definition was **corrected pre-data** (documented amendment): the
  original `S_logdet` (field-map correlation across l) is ~0 by spherical-harmonic orthogonality;
  it was replaced, before any sky value was seen, with the cross-l **power**-map correlation, the
  intended native `-ln det C` cross-scale read. Reasoned from mathematics, not data.
