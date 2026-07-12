# THICKENER 3 — MEPP cross-rung selection consistency: PRE-REGISTRATION

**Date 2026-07-12. Frozen BEFORE any result was computed.** (Pandey-run lesson: no post-hoc
estimator fixes. The σ-observable, the nulls, and the "selects" threshold below are fixed here;
whatever comes out is reported against them.)

## The claim under test

The sister run (`experiments/mepp_flavor/`, in flight) proposes that the FORCED
entropy-production functional σ (the bench-validated `experiments/corridor_ceiling/sigma_max.py`
object) *selects* the observed flavor copula (CKM-comonotone / PMNS-anarchic) as a
maximum-entropy-production steady state. **THICKENER 3 asks whether the SAME functional selects
observed structure at OTHER rungs against their nulls.** A selection principle that fires at one
rung is an epicycle; one functional selecting observed copulas across markets, galaxy fields (and
flavor) is a candidate LAW (the parked fourth-law/Onsager slot, `papers/notes/four_laws.md`).

This is Class-V selection (`sm_from_thermodynamics.md` §4) and a THICKENER of a still-uncrowned
claim: by rule 2 it earns NOTHING until the flavor δ-fork it supports is confirmed. The only
verdicts available here are **cross-rung-consistent (candidate law)** vs **flavor-only (epicycle)**
vs **k_eff-in-disguise (no independent content)**.

## σ-OBSERVABLE (frozen)

The bench functional from `corridor_ceiling/sigma_max.py`, generalized from the equicorrelation
two-eigenvalue case to a general observed correlation matrix C (the copula) with eigenvalues
λ₁ ≥ … ≥ λ_N (Σλ = N):

- σ = Σ_{i<j} Q_ij² (1/λ_i + 1/λ_j) is the OU steady-state entropy production
  (Godrèche–Luck 2019); σ_max maximizes over antisymmetric circulation Q under a power budget P.
- **PRIMARY: N1 (bounded actuation, the corridor_ceiling PHYSICAL pick).** Budget
  ‖QC⁻¹‖_F² ≤ P. Closed form: σ_max^N1 = P · max_{i<j} (1/λ_i+1/λ_j)/(1/λ_i²+1/λ_j²).
- **SECONDARY (reported, not decisive): N3 (bare stirring).** Budget Tr[QᵀQ] ≤ P.
  σ_max^N3 = (P/2)·max_{i<j}(1/λ_i+1/λ_j) = (P/2)(1/λ_N + 1/λ_{N-1}).
- P = 1 throughout (percentiles are scale-free in P).

**Pre-registered structural note (NOT a result, a property of the functional):** both σ_max forms
are functions of the eigenvalue multiset ONLY — the maximization over Q reduces to a best
eigenvalue-pair. σ_max is therefore eigenvector-blind. This is *why* the null design below is what
it is, and it is the crux of the confound check.

## NULLS (frozen — three, each answering a distinct question)

- **NULL-A — phase-randomized (coordination baseline).** Per-channel Fourier phase randomization
  of the raw time series (preserves each channel's power spectrum / marginal, destroys
  cross-channel dependence), rebuild C, recompute σ_max. M = 500 surrogates. Question answered:
  *is observed σ_max above a DECORRELATED baseline?* Requires raw series (finance, fullmarket,
  galaxy×3). **Expected to be near-tautological** (a coordinating system has more spectral spread
  than its decorrelated self) — included precisely so the tautology is measured, not assumed.

- **NULL-B — k_eff-matched random spectra (THE confound-controlling null).** Random eigenvalue
  multisets of size N, Σλ = N, with participation ratio PR = (Σλ)²/Σλ² held to the OBSERVED k_eff
  (±2% tolerance, rejection-sampled from Dirichlet(α) spectra with α swept for shape diversity),
  eigenvalue SHAPE otherwise random. M = 500. Question answered: *given its coordination LEVEL
  (k_eff), does the observed spectral SHAPE sit at a σ-extremum?* This is the only null that is
  not k_eff-in-disguise. Requires only the observed spectrum → all substrates.

- **NULL-C — spectrum-matched, Haar eigenvectors (diagnostic).** Same eigenvalues as observed,
  random orthogonal eigenvectors (Haar). M = 200. Because σ_max is eigenvector-blind, this MUST
  return percentile ≈ 50 (σ_max identical). Included as an executable proof of the structural
  note above; a deviation from ~50 would falsify my own understanding of the functional.

## "SELECTS" CRITERION (frozen thresholds)

Per substrate, percentile of observed σ_max within each null's distribution (fraction of null
draws with σ_max ≤ observed; 0–100).

1. **Rung-selection (per substrate, NULL-B):** "σ selects the observed copula" iff observed sits
   at **≥ 90th percentile** (near a σ-MAX extremum, MEPP reading) OR **≤ 10th percentile** (near a
   σ-MIN extremum, anti-MEPP) of NULL-B. Between 10 and 90 = σ does not select this copula.
   MEPP specifically predicts the HIGH tail.

2. **Class split (THE thickener content):** across substrates, coordinating/maintained systems
   (finance, fullmarket, galaxy density, galaxy temp) sit near a NULL-B σ-extremum (criterion 1)
   AND constructed/decorrelated controls (iid, phase-randomized) do NOT. Verdict YES iff the
   coordinating median NULL-B extremity (|percentile − 50|) exceeds the control median by a gap
   with rank-sum separation (one-sided Mann–Whitney p < 0.05, small-n caveated).

3. **Confound (k_eff-in-disguise) — decisive:** (a) NULL-C percentile must be ≈ 50 (proves
   eigenvector-blindness). (b) Regress NULL-A percentile on k_eff across substrates; if NULL-A
   extremity is fully explained by k_eff (Spearman |r|(NULL-A pct, k_eff) high AND the class-split
   in NULL-A vanishes after conditioning on k_eff), the NULL-A "signal" is coordination-detection,
   not σ-selection. **THICKENER 3 HOLDS only if NULL-B (which already controls k_eff) shows the
   class split.** If NULL-B gives ≈ 50 for everyone, σ-selection carries no content beyond k_eff →
   report "k_eff-in-disguise", THICKENER FAILS.

## SUBSTRATES (real data only; constructed controls labeled)

Recoverable full spectra + raw series (this is the honest scope — most catalog JSONs store only
truncated top_eigs, unusable for σ_max which needs the small eigenvalues):

| substrate | source | N × T | class |
|---|---|---|---|
| finance S&P-100 | `finance_returns_cache.parquet` | 98 × 2010 | coordinating |
| fullmarket S&P-500 | `fullmarket_returns.parquet` | 487 × 1504 | coordinating (overlaps finance — non-independent, noted) |
| galaxy density (TNG) | `tngsubbox_checkpoint_T30.npz` SR_lr | 12 × ~47 | coordinating/bound |
| galaxy temperature (TNG) | SR_lt | 12 × ~47 | coordinating/bound |
| galaxy velocity (TNG) | SR_vr | 12 × ~47 | bound (weaker — the low anchor among real) |
| iid Gaussian | CONSTRUCTED (labeled) | 98 × 2010 | dead control |
| phase-randomized finance | CONSTRUCTED (labeled) | 98 × 2010 | reversible control |

Constructed controls are NOT "found systems" (corridor_ceiling Part-B precedent); they anchor the
low end of the class split and are flagged in every table. Neurons/immune are named in the mission
but their raw series are not in this directory and the stored top_eigs are truncated → cannot
compute σ_max honestly → excluded rather than faked.

## DISCIPLINE

Real catalog data only; the sole synthetic objects are the pre-committed null ensembles (NULL-A/B/C),
labeled as such. Seed 20260712, CPU. Incremental flush. No estimator changes after this file.
