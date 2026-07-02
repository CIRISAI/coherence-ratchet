# Collective motion (midge swarms) — covariance-saturation vs criticality

Adversarial breadth test on the criticality camp's **flagship living system**:
collective animal motion. Cavagna/Attanasi's "scale-free correlations in a living
system" (starling flocks, PNAS 2010; wild midge swarms, PNAS 2014) is *the*
canonical claim that a natural collective sits at a critical point — the
velocity-fluctuation correlation length grows with group size. A complete swarm at
an instant is a **complete unit** (all individuals tracked, no grain escape), so
this is a clean test on their home turf.

## Dataset

**Chironomus riparius laboratory midge swarms** — Sinhuber, van der Vaart, Ni,
Puckett, Kelley, Ouellette (2019), *"Three-dimensional time-resolved trajectories
from laboratory insect swarms"*, figshare **doi:10.6084/m9.figshare.11546013**
(open, CC-BY; `_fixed.csv` files). Columns: `id,t,x,y,z,vx,vy,vz`; 3D tracking at
**100 Hz**. Used the **unperturbed** takes (pure spontaneous coordination, no
external forcing). Midges are the same system class as Attanasi 2014's wild-swarm
criticality result — squarely on-turf.

- 5 unperturbed takes analyzed, each 160–200 s (16k–20k frames).
- **Co-present individuals: N = 8–14** at any instant. These are small lab swarms;
  tracks turn over, so only ~10–15 midges are simultaneously tracked. This caps the
  covariance-subsampling leverage — stated honestly below.

Larger *complete-group* datasets were sought and are **gated**: COBBS/CNR starling
flocks (on-request only); Pseudomugil schooling-fish coordinates on Dryad
(doi:10.5061/dryad.8g0d0 — files exist, 0.16–0.9 GB, but the download API returns
401/403 without an OAuth bearer token); Oregon State golden-shiner school
(ScholarsArchive `zk51vq07c` — Cloudflare 403). The midge set is the largest
openly fetchable complete-unit collective-motion data.

## Observable distinction (stated up front)

Two *different* observables, both computed:

- **(A) Covariance eigenspectrum k_eff** — the RATCHET discriminator. Effective
  number of collective velocity-fluctuation modes; does it saturate (bounded /
  low-rank) or grow with N?
- **(B) Correlation length ξ vs system size L** — **Cavagna's actual observable**,
  a *spatial* quantity (first zero-crossing of the connected correlation C(r)).
  Related to but **not identical** to the covariance PR. Scale-free/critical
  prediction: ξ ∝ L.

Velocity fluctuation everywhere = `δv_i = v_i − ⟨v⟩_swarm` (bulk swarm translation
removed; the coordination signal is the fluctuation, not the drift).

## Results

### (A) Covariance saturation — does NOT read low-rank

Pipeline calibrated first: a synthetic rank-3 collective field returns PR≈3,
eff_rank=3; an independent field returns PR≈N, eff_rank≈0. Separation is clean.

| take | N | k_eff (PR) | eff_rank vs surrogate | subsample β |
|------|---|-----------|-----------------------|-------------|
| 7  | 13 | 8.51 | **0** | 0.75 |
| 10 | 14 | 8.91 | 1 | 0.74 |
| 14 | 11 | 4.04 | 1 | 0.42 |
| 22 |  8 | 5.08 | 1 | 0.64 |
| 27 | 13 | 7.63 | 1 | 0.69 |

- **k_eff / N ≈ 0.65** (median PR 7.6 at mean N 11.8). Not low-rank.
- **Effective rank above the phase-randomized surrogate ≈ 0–1.** Phase-randomizing
  each midge's own velocity (preserving its power spectrum, destroying inter-midge
  phase relations) barely changes PR (real 8.9 vs surrogate 9.2). There is **at
  most one collective mode above the independence null, often zero.**
- Subsampling β ≈ 0.65 (limited leverage at N≤14), consistent with near-extensive.

The velocity-fluctuation covariance of a complete midge swarm is **near-independent
/ high-dimensional — the chaos corner, not a bounded low-rank attractor.** This
matches the biology: midge swarms are "collective behaviour *without* collective
order" (polarization ≈ 0). The RATCHET low-rank-saturation reading **does not win
here.**

### (B) Correlation length ξ ∝ L — reproduced, then shown to be an artifact

Pooled over **19,179 frames** (L = 154–1004 mm from the swarm's frame-to-frame
breathing; n = 6–19):

- ξ/L median = **0.347**, `d log ξ / d log L = 0.949` (r=0.51). Naively this
  **reproduces Cavagna's scale-free signature**: ξ tracks L almost linearly.

**Adversarial control — spatial shuffle.** Randomly permute the velocity vectors
among positions within each frame (destroys all real position↔velocity spatial
correlation; preserves the point cloud and the sum-rule Σφ=0):

| | n frames | ξ/L median | ξ median | slope d logξ/d logL |
|--|---------|-----------|----------|---------------------|
| **REAL**    | 19179 | 0.347 | 150.8 mm | 0.949 |
| **SHUFFLE** | 19168 | 0.358 | 152.4 mm | 0.941 |

**Identical.** The ξ∝L scaling survives complete spatial scrambling → on this
dataset it is a **definitional / finite-size artifact** of the zero-crossing
correlation length under the mean-subtraction sum rule (Σδv=0 forces C(r) positive
at small r and a zero-crossing that scales with L for *any* spatial arrangement),
**not evidence of genuine scale-free correlation.** The criticality camp's flagship
observable, applied here, does not distinguish a real swarm from spatially-scrambled
velocities.

### (C) Detailed balance — broken (the one robust signal)

Winding-based irreversibility on the collective velocity modes: **|z| median ≈ 3.1**
(per-take 2.0–3.4). Broken detailed balance, as expected for an actively
self-propelled swarm far from equilibrium. This is the real, non-artifactual
signature — active coordination, but *not* low-dimensional and *not* critical.

## Bottom line

On the criticality camp's flagship system, a **complete midge swarm**:

1. **Does not saturate to a bounded low-rank covariance.** Its velocity-fluctuation
   covariance is near-independent / high-dimensional (eff_rank 0–1 above the
   independence null, k_eff ≈ 0.65 N). The RATCHET low-rank reading is **not**
   supported — this is a place where it does not win.
2. **Does not carry a robust scale-free correlation length.** ξ∝L reproduces
   Cavagna's number (slope 0.95) but is **identical under spatial shuffle** → a
   sum-rule/finite-size artifact, not genuine criticality, on this dataset.
3. **Is genuinely far-from-equilibrium** (broken detailed balance, |z|≈3) — the
   only observable that survives adversarial controls.

So neither camp's headline reading survives cleanly here: the swarm is neither a
low-rank bounded attractor nor a demonstrably critical one on this data. Honest
scope limits: N≤14 co-present caps covariance-subsampling leverage, and the L-range
is the swarm's own breathing rather than a population of different-sized swarms
(Cavagna's cross-swarm test needs the gated wild-swarm / starling data). The
shuffle control is definition-level and does not depend on N.
