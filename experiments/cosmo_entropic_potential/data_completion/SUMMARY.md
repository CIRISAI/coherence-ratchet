# Data completion — SNe joined, ISW checked, family tie broken: the preference survives everything added

**Date 2026-07-10.** Completes the data side of the DR2 comparison (`../desi_likelihood_v2/`):
real SNe likelihoods joined, the late-ISW prediction checked, and the within-family tie tested
against DESI's existing crossing posterior. Data: `results.json`, `des_results.json`,
`isw_results.json`, `family_results.json`.

## 1. The joint fits — the framework's preference GROWS with SNe, on both compilations

**Pantheon+** (1580 SNe after cuts, full 1701² STAT+SYS covariance, M_B/H₀ analytically
marginalized; Brout et al. 2022):

| config | framework | ΛCDM | CPL | Δχ² fw−ΛCDM | ΔAIC fw−CPL | ΔBIC fw−CPL |
|---|---|---|---|---|---|---|
| BAO+θ*+SNe | χ² = 1397.17 | 1401.22 | 1395.64 | **−4.05** | **−2.47** | **−13.21** |
| BAO+SNe (no CMB) | 1396.44 | 1400.37 | 1395.59 | **−3.93** | −3.15 | — |

**DES-SN5YR** (the K5 sensitivity check — the compilation whose calibration threatens DESI's
own evolving-DE significance):

| config | Δχ² fw−ΛCDM | ΔAIC fw−CPL | ΔBIC fw−CPL |
|---|---|---|---|
| BAO+θ*+DES | **−5.44** | −1.76 | −12.79 |
| BAO+DES (no CMB) | **−4.74** | −2.23 | −13.26 |

Three facts, plainly: (i) adding SNe **strengthened** the zero-shape-parameter preference over
ΛCDM (−1.46 → −4.05 Pantheon+, −5.44 DES); (ii) the framework now beats the 2-extra-parameter
CPL on **both** information criteria on the full cosmological data vector; (iii) **the
preference is SNe-compilation-robust** — K5 (the DES-Y5 calibration systematic) can move
DESI's evolving-DE significance but does not touch the framework-vs-ΛCDM comparison, which
holds on both compilations and without CMB. Note also the with-SNe CPL best fit
(w₀ = −0.888, wₐ = −0.274) moves toward the framework's curve relative to the BAO-only fit.

## 2. Late ISW — consistency pass, below current sensitivity

The frozen w(z) modifies the late-ISW signal relative to ΛCDM by **1–7%** across estimators
(net-decay, broad tomographic 0<z<2, Gaussian z_eff = 0.5 kernels; both Ω_m conventions).
Published A_ISW constraints sit at ~30% precision (unWISE×Planck: 0.96 ± 0.30 — fetched, not
re-derived). Verdict: **consistent; the framework's ISW deviation is an order of magnitude
below current sensitivity** — a pass, not a discriminant, and a future-survey target.

## 3. Within-family discrimination — present data already rank the variants

Against DESI DR2's own crossing posterior (median 0.35, 90% [0.19, 0.70]), CPL-projected
through the identical distance machinery:

| variant | projected crossing z | inside DESI 90%? |
|---|---|---|
| **extensive S (frozen)** | 0.458 | **yes** |
| intensive S/k | 0.756 | **no** |
| count k(a) | 0.385 | yes |

**The intensive variant — indistinguishable from the frozen choice by distance χ² — is
disfavored by the crossing epoch with data in hand.** The extensive convention gains its first
data-side (not convention-side) support; the count variant remains a live competitor (its
projected (w₀, wₐ) = (−0.839, −0.580) sits nearest DESI's point), which keeps the honest
statement from `../functional_falsification/`: the family's discriminating observable is the
crossing epoch, and DR3 sharpens exactly that.

## Caveats

θ*-compression approximation inherited (not the full CMB likelihood); Ω_m profiled;
SNe duplicates between compilations not cross-checked (each used separately, never jointly);
A_ISW numbers fetched-not-rederived; the family ranking uses DESI's CPL-space crossing
posterior, which is itself ill-conditioned (the reason it's a ranking, not a kill);
`sne_only` configuration degenerate (M_B marginalization absorbs the distinction) and reported
as null by design.

*(Summary written by the orchestrating session from the agent's completed results; the DES
sensitivity script was executed by the orchestrator after the agent idled — all numbers are
executed output.)*
