# Bet 11 — REGISTRATION (frozen before any data touch)

**Date frozen: 2026-07-11.** No Planck anomaly-data value has been inspected at the time this
file is written. Null-model inputs (the Planck best-fit LCDM C_ell, a theory spectrum) and the
ensemble machinery are not anomaly data; everything that reads the actual sky is specified here
*before* it is computed. This registration is the sole scorer. The claim stands or falls only by
the pre-committed decision rule below.

---

## The bet (stated against ourselves)

The coordination **past hypothesis** (mystery_map.md §1: the primordial arrangement books
opened empty, `S_coord ≈ 0`, read off Planck Gaussianity `f_NL = −0.9 ± 5.1`) together with the
**orthogonality theorem** (CLAUDE.md: the framework is *exactly* ΛCDM in the
conditioning/perturbation sector — the CMB fence) make a joint, pre-stated prediction:

> **The famous low-ell CMB anomalies (quadrupole–octopole alignment, hemispherical/dipolar
> power asymmetry, the S_{1/2} lack of large-angle correlations, the low quadrupole) are
> individually a-posteriori selections from one isotropic Gaussian sky. Treated JOINTLY, with
> the look-elsewhere effect computed on the null ensemble, they should DISSOLVE — the CMB's own
> "θ₁₃": one soft marginal that is an expected fluctuation once you count how many ways the sky
> could have looked odd.**

This is the CMB analog of the flavor-sector result (`sm_escalator_mixing/`): one pre-registered
functional battery, one structureless null ensemble, joint depth statistics, ensemble-computed
look-elsewhere. There the leptonic sector dissolved into Haar-typicality; here the low-ell
temperature sky should dissolve into isotropic-Gaussian-typicality.

### KILL (the real bet)

**If the joint atypicality of the low-ell temperature sky SURVIVES the battery at ≥ 3σ-equivalent
(joint outlyingness ≥ 99.73rd ensemble percentile), robustly across the pre-committed ell_max
choices — then the books did NOT open empty.** A jointly-significant coordination structure in
the primordial temperature field is primordial coordination the past hypothesis says should be
absent, and it is coordination sitting in the exact linear/perturbation sector the orthogonality
theorem fences off as pure ΛCDM. Both the past-hypothesis answer (mystery_map.md §1) and the
orthogonality fence (CLAUDE.md CMB row) are wounded. This is staked now, before the data.

A partial/ambiguous outcome (below) wounds nothing but earns nothing (Discipline rule 2: a
dissolved anomaly is a consistency check / retrodiction — Gaussianity and these anomalies were
already known — not novel support).

---

## 1. UNITS

The **low-ell temperature multipoles** of the CMB: real spherical-harmonic coefficients
`a_{ℓm}` for `ℓ ∈ [2, ℓ_max]`, evaluated in the **Galactic frame** (fixed for data and
ensemble alike — several battery functionals are frame-dependent per realization but
frame-fixed in distribution; a common fixed frame makes data and null directly comparable).

- **ℓ_max = 30 primary.** Robustness re-runs at **ℓ_max = 10 and ℓ_max = 60**, decided now.
- ℓ = 0 (monopole) and ℓ = 1 (dipole) are excluded (kinematic/removed), standard.

## 2. NULL ENSEMBLE (the method; labelled synthetic, not data)

Isotropic Gaussian skies drawn from the **Planck 2018 best-fit ΛCDM temperature spectrum**
`C_ℓ^{TT}` (base_plikHM_TTTEEE_lowl_lowE_lensing minimum-theory, or the released best-fit
`COM_PowerSpect_CMB` TT theory column; whichever downloads — both are the same base-ΛCDM
prediction). This is the standard isotropy-null choice: the data's departures (e.g. low S_{1/2},
low quadrupole) then appear as departures from the isotropic-Gaussian-theory expectation, which
is the correct comparison and reproduces the literature significances.

- **N = 100,000 realizations.** `numpy.random.default_rng(20260711)`. `healpy.synalm(C_ℓ,
  lmax=ℓ_max, new=True)` per realization → `a_{ℓm}`; map-based functionals use
  `healpy.alm2map(alm, nside=64)` (ℓ_max ≤ 60 ≪ 3·64, no aliasing).
- **Mask treatment: full sky, no mask** for both data and ensemble (primary). Data primary is
  the released full-sky component-separated low-ℓ map (below); the residual-foreground caveat at
  the largest scales is stated as a known limitation, not modelled. (A mask would couple ℓ and
  is deferred; the full-sky treatment is the honest primary given the fallback-map option.)

## 3. THE OBSERVABLE VECTOR (exact functionals, frozen)

Computed identically on the data sky and on every ensemble realization. Two groups.

### Group A — classic anomaly statistics (PRIOR ART; recomputed only for the sanity
reproduction, must reproduce their known individual significances):

1. **`align_23`** — quadrupole–octopole alignment. Angular-momentum-dispersion (AMD) preferred
   axis (de Oliveira-Costa, Tegmark, Zaldarriaga & Hamilton 2004, *PRD* 69, 063516): for ℓ=2,3
   the preferred axis `n_ℓ` maximizes `Σ_m m² |a_{ℓm}(n)|²` over rotations (evaluated on a fixed
   HEALPix Nside=32 direction grid; the max-power axis). Statistic = `|n_2 · n_3|` (1 = aligned).
   Literature: aligned at ≈ 3°, |n_2·n_3| ≈ 0.99, quoted ≈ 99% CL. Sanity target: high percentile.
2. **`A_hemi`** — hemispherical power asymmetry (Eriksen et al. 2004, *ApJ* 605, 14). Map from
   ℓ=2..ℓ_max at Nside=64; over each axis `d` in a fixed HEALPix Nside=8 direction set (768
   axes), power ratio `(σ²_{+d} − σ²_{−d})/(σ²_{+d} + σ²_{−d})`; `A_hemi` = the maximum over `d`.
   Literature: A ≈ 0.07, ≈ 2–3σ. Sanity target: upper tail.
3. **`S_half`** — the S_{1/2} lack-of-correlation statistic (Spergel et al. 2003; Copi, Huterer,
   Schwarz & Starkman 2009, *MNRAS* 399, 295): `S_{1/2} = ∫_{-1}^{1/2} [C(θ)]² d(cosθ)` with
   `C(θ) = Σ_{ℓ=2}^{ℓ_max} (2ℓ+1)/(4π) Ĉ_ℓ P_ℓ(cosθ)`, `Ĉ_ℓ = (1/(2ℓ+1))Σ_m a_{ℓm}²`.
   Literature: observed LOW, p ≈ 0.3–3%. Sanity target: LOWER tail (low-percentile).
4. **`Q_amp`** — quadrupole power `Q = ℓ(ℓ+1)Ĉ_ℓ/2π` at ℓ=2 (the low-quadrupole anomaly).
   Sanity target: LOWER tail.

### Group B — the ledger / coordination functionals (the mixing battery adapted; dependence
across ℓ-blocks and across m within ℓ — these carry the JOINT bet):

5. **`axis_conc`** — multi-ℓ preferred-axis concentration (the alignment anomaly generalized to
   ALL low ℓ, an across-ℓ directional-dependence read). For each ℓ ∈ [2, ℓ_max] the AMD
   preferred axis `n_ℓ` and weight `w_ℓ = (2ℓ+1)Ĉ_ℓ`; form the dyadic `T = Σ_ℓ w_ℓ n_ℓ n_ℓᵀ /
   Σ_ℓ w_ℓ`; `axis_conc` = largest eigenvalue λ_max(T) ∈ [1/3, 1]. Isotropy → axes uniform on
   the sphere → λ_max near its null bulk; coordinated (all ℓ sharing an axis) → λ_max → 1.
6. **`S_logdet`** — the program's native copula functional `S = −ln det Ĉ` transferred to the
   sky, phase-sensitive, across ℓ-blocks. Build the per-ℓ maps `m_ℓ(n̂) = Σ_m a_{ℓm} Y_{ℓm}(n̂)`
   (ℓ = 2..ℓ_max), each sampled on a fixed HEALPix Nside=8 direction set (768 points); stack into
   a (768 × L) matrix (L = ℓ_max−1), demean each column, form the (L×L) sample correlation matrix
   `Ĉ` across the directions; `S_logdet = −ln det Ĉ` (= −Σ ln(eigenvalues)). Isotropy → distinct
   ℓ-maps are independent random fields → `Ĉ ≈ I` → `S_logdet ≈ 0`; shared spatial structure
   across ℓ (a common preferred pattern) → off-diagonal correlation → `S_logdet > 0`. This is the
   direct `−ln det C` effective-rank / coordination read used everywhere in the program.
7. **`pr_lowell`** — within-ℓ m-power participation ratio (across-m dependence read, fixed frame):
   for each ℓ, `PR_ℓ = (Σ_m a_{ℓm}²)² / Σ_m a_{ℓm}⁴` (participation ratio of power over the 2ℓ+1
   m-modes in the Galactic frame); `pr_lowell` = mean over ℓ ∈ [2, ℓ_max] of `PR_ℓ / (2ℓ+1)`
   (normalized so 1 = power spread evenly across m, low = concentrated in few m = a preferred
   frame / m-coordination). Frame-dependent per realization, frame-fixed in distribution — the
   null ensemble supplies the correct reference in the same Galactic frame.

**Observable vector = (align_23, A_hemi, S_half, Q_amp, axis_conc, S_logdet, pr_lowell)** — 7
components. Dimension is deliberately modest so the 100k-null Mahalanobis covariance is very well
estimated.

## 4. THE JOINT TEST (rigor-pass depth statistics; look-elsewhere ON THE ENSEMBLE)

The full 7-vector's depth in the null cloud, three depths (as in `rigor/rigor.py`), each
percentiled against the empirical null (outlyingness percentile: ~50 typical, >99 flagged, >99.73
= 3σ-equiv):

- **(a) Mahalanobis** `D² = (x−μ)ᵀ Σ⁻¹ (x−μ)` on the empirical null mean/cov of the 7-vector;
  outlyingness pct = fraction of null with `D² < D²_data`; report also the χ²₇ CDF (the
  Gaussian-theory percentile) — their gap = non-Gaussianity of the depth.
- **(b) Normal-scores rank Mahalanobis** — rank-transform each component to its empirical uniform,
  inverse-normal (van der Waerden), Mahalanobis in that space (robust to marginal non-Gaussianity,
  keeps correlation).
- **(c) Spatial (L1) depth** on a null subsample (cross-check), standardized by null std.

**Explicit look-elsewhere number (analog of the θ₁₃ union in STAT2):** compute directly on the
ensemble `P(at least one of the 7 marginals is at least as extreme as the data's, in that
marginal's flagged tail)`, using each marginal's pre-declared tail direction (align_23, A_hemi,
axis_conc, S_logdet: UPPER; S_half, Q_amp, pr_lowell: LOWER). ≳ 10% ⇒ the individual "anomalies"
are an expected look-elsewhere fluctuation; ≲ 1% ⇒ flagged.

## 5. DECISION RULE (frozen — the sole scorer)

Let `J` = the joint outlyingness percentile (require the three depths to agree; if they disagree
by more than one tier, verdict = AMBIGUOUS).

- **DISSOLVED** — `J` inside the central 99% (joint outlyingness ≤ 99.0) for the primary
  ℓ_max = 30, i.e. the low-ell sky is jointly typical of an isotropic Gaussian ensemble once
  look-elsewhere is accounted for by the joint depth. (Consistent with, but not requiring, the
  marginal-union ≳ 10%.)
- **SURVIVES** — `J ≥ 99.73` (3σ-equivalent) at ℓ_max = 30 **and** robust (still ≥ 99.73) across
  ℓ_max ∈ {10, 60}. → fires the KILL above.
- **AMBIGUOUS** — anything between (99.0 < J < 99.73), or depth disagreement, or a verdict that
  flips across the ℓ_max robustness choices.

## 6. DATA

- **Primary:** a released Planck full-sky component-separated CMB temperature map (SMICA or
  Commander, whichever downloads from the PLA / NASA LAMBDA), read with healpy, `map2alm` to
  ℓ_max=60 in the Galactic frame. If a low-resolution (Nside≤64) component-separated map is
  available it is preferred for the low-ℓ analysis and downloads faster.
- **Fallback (if map download infeasible):** the published low-ℓ `a_{ℓm}` / `C_ℓ` products or
  multipole tables from the Planck 2018 isotropy paper. Group-A statistics computable from
  published `Ĉ_ℓ`; Group-B (phase-sensitive) functionals need the `a_{ℓm}` and are reported only
  if the fallback provides them. Any fallback cited precisely in SUMMARY.md.
- **Masking documented honestly** per §2 (full-sky primary; caveat stated).

## 7. PRIOR ART (positioned honestly)

- The individual anomalies and their significances: Planck 2018 results VII, *Isotropy and
  statistics of the CMB* (*A&A* 641, A7, 2020); Planck 2015 XVI. Review: Schwarz, Copi, Huterer &
  Starkman, *CMB anomalies after Planck* (*Class. Quantum Grav.* 33, 184001, 2016). Individual
  statistics: de Oliveira-Costa et al. 2004 (alignment); Eriksen et al. 2004 (asymmetry); Copi,
  Huterer, Schwarz & Starkman 2009 (S_{1/2}); Spergel et al. 2003 (WMAP S_{1/2}).
- The look-elsewhere / a-posteriori critique: Bennett et al. 2011, *Are There Cosmic Microwave
  Background Anomalies?* (*ApJS* 192, 17) — the WMAP team's a-posteriori-selection argument.
- **OURS is exactly one thing, no more:** the single, pre-registered JOINT battery — the seven
  functionals scored together by depth statistics with the look-elsewhere effect computed on the
  null ensemble. Every individual statistic is prior art; the pre-registered joint verdict with
  ensemble look-elsewhere is the transferred method. Citations to be re-verified in the
  prior-art pass before SUMMARY.

---

## AMENDMENT (2026-07-11, pre-data — no sky value seen; reasoned from mathematics only)

**Correction to functional 6 (`S_logdet`), made before any anomaly datum is touched** (the
Planck map is still downloading; nothing has been computed on it). The originally-frozen
definition — the (L×L) correlation of the per-ℓ *field* maps `m_ℓ(n̂)` across directions — is
**degenerate by spherical-harmonic orthogonality**: distinct-ℓ real fields obey
`∫ m_ℓ m_{ℓ'} dΩ = 0`, so their demeaned across-direction correlation is ≈ 0 by identity for
both data and null, carrying only quadrature-sampling noise. It would read no coordination by
construction. This is a pre-data mathematical defect, so it is corrected here (documented, not
silently), keeping the same intent — a native `−ln det C` across-ℓ-block coordination read:

- **`S_logdet` (corrected)** = `−ln det Ĉ`, where `Ĉ` is the (L×L) sample **correlation matrix,
  across the 768 fixed HEALPix Nside=8 directions, of the per-ℓ POWER maps**
  `p_ℓ(n̂) = m_ℓ(n̂)²` (m_ℓ the ℓ-map as before), ℓ = 2..ℓ_max, L = ℓ_max−1. Power maps are NOT
  orthogonal across ℓ: a spatial region hot/cold across several ℓ (common concentration) makes
  `p_ℓ, p_{ℓ'}` covary → off-diagonal `Ĉ` → `S_logdet > 0`; isotropic independent ℓ →
  `Ĉ ≈ I` → `S_logdet ≈ 0`. UPPER tail = coordination. This reads cross-scale common structure
  (the native content the degenerate version could not). All other functionals unchanged.

The two directional Group-B functionals are thus: `axis_conc` = λ_max of the axis dyadic
(alignment amplitude), `S_logdet` = −ln det of the cross-ℓ power-map correlation (cross-scale
coordination). `pr_lowell` unchanged.

---

**Frozen. Data touch begins only after this file is committed.**
