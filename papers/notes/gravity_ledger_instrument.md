# The gravity ledger vs the light ledger — S on the dark matter field carries no coordination the light field misses, beyond a bias factor

**Date 2026-07-10. Companion to `dm_phasespace_grain.md`, `gaia_phasespace_test.md`, and
the README "dark ledger" section.** Those read the LIGHT ledger (galaxy light, baryons,
phase-space of stars) on real sky. This note puts the instrument on the field dark matter
actually lives on — the GRAVITY ledger, the total-matter field — in a simulation where
BOTH the dark and the luminous fields are known with ground truth (IllustrisTNG). Code:
`experiments/dm_coherence/gravity_ledger/{gravity_ledger.py, results.json, figures}`
(seed 20260710; every number below is executed output).

**The idea.** S = -ln det C is ledger-agnostic — it reads whatever correlation matrix you
feed it. Every prior test fed it the electromagnetic ledger (galaxy light, baryons). Dark
matter lives on the gravity ledger (total matter, dark-dominated). So feed the instrument
the DARK MATTER field and compare to S on the STELLAR/gas field over the SAME comoving
volume. The two-ledger difference S(gravity) - S(light) is, by our own definition, the dark
sector's coordination structure — now directly measurable.

---

## Bottom line up front

**VERDICT: BIAS-ONLY (the honest NULL).** On the gravity ledger the dark-matter field reads
a real, robust coordination S(DM); the two-ledger difference from the stellar light ledger is
large. But it is *entirely a tracer effect* — shot, peakedness, and the linear bias factor b.
The light field is the dark field, rescaled: at large scales the stellar field is predicted
from the dark field up to a single bias with cross-correlation **r = 0.986 ± 0.003** (gas:
0.999), and what survives bias-matching is small (2.8% stochasticity), lives at small scales,
and is the *known* galaxy-formation / discreteness residual — not a new large-scale dark
coordination. The one candidate for a distinct dark higher-order signal (a non-Gaussian excess
in the stellar residual) **fails its control**: it appears only in the sparse, threshold-selected
stellar tracer and vanishes in the dense gas tracer, marking it as the star-formation threshold
(known nonlinear bias), not dark structure. **The gravity ledger carries no NEW coordination the
instrument can read, even on the right ledger.**

| | Gravity ledger (DM) | Light ledger (stars) | Light ledger (gas) |
|---|---|---|---|
| S = -ln det C (z~0, CV mean) | **4.53 ± 0.76** | **0.98 ± 0.21** | 13.28 |
| what sets S | dense, mildly nonlinear | sparse + spiky (shot 0.44) | smooth (pressure) |
| linear bias b vs DM | 1 | 1.78 ± 0.03 | 0.94 |
| cross-corr r(k), large scale | 1 | **0.986 ± 0.003** | **0.999** |
| stochasticity 1-r², large / small scale | 0 | 0.028 / 0.097 | 0.002 / 0.36 |
| residual non-Gaussian excess (nats/pair) | 0.36 (its own web) | 0.47 | 0.38 |
| distinct dark higher-order (residual - DM) | — | 0.12 (stars only) | **0.03 (control: null)** |

The raw ledger ordering is **gas (13.3) > DM (3.5) > star (0.9)** — the *opposite* of "the
gravity ledger carries the most structure." It is set purely by each tracer's smoothing,
peakedness, and shot, and all three collapse onto one field at r ~ 1. That inversion is the
whole result: *S-value differences across ledgers are tracer bookkeeping, not independent
coordination.*

---

## 1. Fields — both real, ground-truth, same volume

IllustrisTNG CV (Cosmic-Variance) set, 25 Mpc/h box, public CAMELS Flatiron mirror (the TNG
www API is gated/403, as in `../cosmo_entropic_potential/halo_grain`). Ranged HDF5 reads of the
particle snapshots, CIC-deposited to a matched 64³ comoving grid (cell 0.391 Mpc/h):

- **Gravity ledger** = PartType1 dark matter, 16 777 216 equal-mass particles (256³). Dense,
  shot on the contrast = 0.016 — negligible.
- **Light ledger (primary)** = PartType4 stars, 636 474 particles (z~0). Sparse and spiky;
  shot on the contrast = 0.44.
- **Light ledger (control)** = PartType0 gas, 15.6 M particles. Dense and smooth (pressure
  support), shot = 0.018 — the zero-inflation-free tracer used to control the higher-order test.

No mock was needed. Three snapshots (z = 0.00, 1.05, 2.30) for evolution; CV_0..CV_2 at z~0 for
cosmic-variance error bars.

**The instrument, made exact.** For a stationary field with autocovariance ξ(r), sampling at a
fixed set of comoving cells gives *exactly* C_ij = ξ(r_ij)/ξ(0), C_ii = 1 — a principal submatrix
of the field's circulant covariance, hence **PSD by construction** (the FFT power spectrum
P(k) ≥ 0). We measure ξ on the 64³ lattice by FFT, sample 512 lattice cells (averaged over 12
drawings), and take S = -ln det C using exact periodic lattice lags. Conditioning is benign
throughout (cond 1.8–7.7; min-eig 0.29–0.71). A full-grid spectral cross-check S = -Σ ln λ_k
(λ = P_k/⟨P_k⟩) reproduces the ordering (per-mode 2.41 gas > 1.35 DM > 0.74 star).

**The theoretical point that governs everything (same as the halo grain).** In the *normalized*
correlation matrix, **linear bias b cancels exactly**: if δ_star = b·δ_DM then Cov ~ b²ξ_DM and
the diagonal also carries b², so C_star = C_DM identically and S(star) = S(DM). A Gaussian
two-ledger difference can arise ONLY through (1) shot/discreteness, (2) scale-dependent bias
b(k), (3) stochasticity beyond linear bias. Only (3) could be a genuine independent dark-sector
coordination. P3 isolates it.

## 2. S(DM) vs S(light) — a big difference, and it is all tracer

S(DM) = 4.53 ± 0.76 ≫ S(star) = 0.98 ± 0.21 (two-ledger difference DM - star = 2.6, sign robust
in every CV box). Naively "the gravity ledger carries 4× the coordination of the light ledger."
But S(gas) = 13.3 ≫ S(DM): the *smooth* light ledger reads *more* than the dark ledger. S is
reading tracer smoothing/peakedness, not a hierarchy of fundamental coordination:

- **stars** are a sparse, spiky, threshold-selected tracer — most cells hold no stars, so at
  random cell separations most pairs are near-zero → suppressed off-diagonal → **low S**;
- **gas** is smooth (pressure erases small-scale power) → high cell-cell correlation at fixed
  separation → **high S**;
- **DM** sits between.

The clustering-fraction-deconvolved S (shot removed from the diagonal) is identical to the
field S to 3 decimals — the difference is not even shot in the normalization; it is the shape/
smoothing of each tracer. None of this is independent coordination.

## 3. The discriminator (P3) — the light field IS the dark field, rescaled

Fit the linear bias b from the cross-power at large scales, form the bias residual
ε = δ_light - b·δ_DM, and read the cross-correlation coefficient r(k):

```
              b (large-scale)   r(k) large   r(k) small   stochasticity 1-r²
  stars       1.78 ± 0.03       0.986         0.951        0.028 -> 0.097
  gas         0.94              0.999         0.801        0.002 -> 0.36
```

At large scales the dark field predicts BOTH light fields to r ~ 0.99: **97–99.99% of the light
ledger's structure is the dark ledger up to one number b.** What survives bias-matching (the
stochasticity 1-r²) is 2.8% for stars, 0.2% for gas at large scales, and it *grows toward small
scales* (9.7%, 36%) — i.e. the residual is a small-scale effect (Poisson shot for stars, pressure
support for gas), not a coherent large-scale dark structure the light misses. The residual S is
correspondingly small and small-scale (S_ε = 0.48 ± 0.13, driven by sub-Mpc modes).

**Evolution — the one place the ledgers decorrelate, and why it is not a signal.**

```
  z      b        r(k) large   S(DM)   S(star)   S(residual)
  0.00   1.74     0.982        3.52    0.92      0.52
  1.05   2.39     0.939        5.59    1.25      0.74
  2.30   3.55     0.863        6.71    1.12      0.85
```

At z = 2.3 the large-scale cross-correlation falls to r = 0.863 (stochasticity 26%) — the closest
thing to a two-ledger decorrelation anywhere in the run. But it tracks the tracer getting *rarer
and more biased* (b climbs 1.7 → 3.5 as star-forming peaks become sparse): this is the textbook
high-redshift galaxy stochasticity of a rare-peak tracer, not an emergent dark coordination. At
z ~ 0 — where real weak-lensing and galaxy surveys operate — it is unambiguously BIAS-ONLY
(r = 0.986 ± 0.003, tight across three boxes).

## 4. Two-point vs higher-order — nothing distinct in the non-Gaussian sector

The Gaussian S depends only on ξ(r) (2-point). To probe beyond it we measure the pairwise copula
mutual information MI(r) (rank-transformed, Miller-Madow corrected) and subtract the Gaussian value
MI_G = -½ ln(1-ρ²); the excess flags non-Gaussian *pairwise* (2-variable) dependence. (Genuine
order ≥ 3 remains the framework's known blind spot; this captures full 2-variable dependence, not
triplets.)

The DM field has a modest, physical small-scale non-Gaussian excess (0.36 → 0.005 nats/pair as
separation grows 0.39 → 3.1 Mpc/h): the nonlinear cosmic web, Gaussian at large scales. The gas
field is similar (0.27 → 0.01). The stellar residual shows an excess *above* the DM web (0.47 vs
0.36 at the smallest lag, a distinct 0.12) — a candidate "dark higher-order" signal. **It fails
its control.** A distinct dark higher-order coordination must be tracer-independent, so it must
appear in the dense, threshold-free GAS residual too — but the gas residual excess is 0.03 above
DM, consistent with the shared web (null). The stellar excess is therefore the star-formation
threshold: where a cell has no stars, ε = -1 - b·δ_DM is a deterministic (nonlinear) function of
δ_DM — known nonlinear stellar bias, not dark structure. The raw stellar MI (1.4–2.0 nats/pair) is
larger still and is a pure empty-cell-tie artifact; we flag and discard it.

## 5. Honesty gates

- **(i) Galaxy bias is a known, large effect — and it is the whole two-ledger difference.** Most
  of S(DM) vs S(light) is bias + shot + smoothing; the test was whether *anything* survives
  bias-matching, and at z ~ 0 essentially nothing does (r = 0.986; residual = small-scale
  stochasticity). We did not tune to STRUCTURE; BIAS-ONLY is the pre-registered honest outcome.
- **(ii) At 2-point this reduces to the known matter-vs-galaxy P(k)/cross-spectrum ratio.** Stated
  plainly: b(k) and r(k) here *are* the standard galaxy-bias and stochasticity functions. We went
  to the non-Gaussian pairwise sector to look for non-trivial content and found none that is
  tracer-independent — the only excess is the stellar star-formation threshold, killed by the gas
  control. Genuine order ≥ 3 (bispectrum / true multi-information) is untested and is the framework's
  acknowledged blind spot; a dark signal could in principle hide there, and our instrument cannot
  read it.
- **(iii) This is a simulation with ground truth.** The real-data version is the natural extension
  (§6) and carries systematics this test does not.
- **(iv) Grain and scale.** One box (25 Mpc/h), one grain (0.39 Mpc/h cells, 512 sampled). The
  conclusion is a large-scale (≳ Mpc) statement; we do not probe the deeply nonlinear sub-100-kpc
  regime, and the stellar tracer is shot-limited there regardless.

## 6. The real-data extension (named, with its systematics)

The simulation says: on the gravity ledger, the dark field's readable coordination is the light
field's, rescaled. The real-sky test of the *same* two-ledger difference replaces the two
simulated fields with two observed maps over one sky patch:

- **gravity ledger** = a weak-lensing convergence map κ (total matter, dark-dominated) — DES/KiDS/
  HSC, or CMB lensing (Planck/ACT/SO) for the linear, high-z gravity ledger;
- **light ledger** = the galaxy number-density map over the same footprint.

Compute S = -ln det C on each, fit the galaxy bias and the galaxy-convergence cross-correlation
r(ℓ), and ask whether a residual survives bias-matching. Added systematics absent here: shape
noise and intrinsic alignments in κ; photo-z and magnification in the galaxy map; mask/geometry;
and the projection to 2D (lensing is a line-of-sight integral, not the 3D field). The prediction
this note licenses is concrete and falsifiable: **r(ℓ) → 1 at large scales and a bias-only null**,
matching galaxy-galaxy-lensing stochasticity measurements — unless the gravity ledger carries
independent coordination, which on the ground-truth simulation it does not.

## 7. Verdict

**BIAS-ONLY.** Put on the correct ledger — the gravitating dark-matter field, with ground truth —
the instrument reads real coordination S(DM), but the two-ledger difference from the light ledger
is entirely tracer bookkeeping (shot, smoothing, and a linear bias b), and the light field is the
dark field rescaled to r = 0.986 ± 0.003 at large scales (z ~ 0). Nothing large-scale survives
bias-matching; the small residual is known small-scale galaxy-formation stochasticity; the one
non-Gaussian candidate is the star-formation threshold, killed by the gas control. This is the
clean, valuable NULL the brief anticipated: **the gravity ledger's coordination is the light
ledger's, and dark matter carries no NEW coordination our instrument can read — even on the field
it lives on.** Consistent, grain-independent, with the dark-matter verdicts already on record:
*direction revived (Bullet, phase-space), magnitude dead, dwarf pair fatal* — and now, *gravity
ledger = light ledger up to bias.*
