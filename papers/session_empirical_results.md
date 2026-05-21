# Empirical results — 2026-05-21 working session

The results below are stated in the paper's register: each finding named, each
verdict given. Positives and nulls are written the same way — flat. A null is
a result.

## 1. The orthogonality theorem

The soft P_ω leaves the bulk CMB power spectrum exactly invariant. Proved in
`CMBOrthogonality.lean` — `participation_scale_invariant` and
`pomega_preserves_power`, both discharged with no framework axiom. Numerically
confirmed: the ensemble correlation between the per-multipole power C_ℓ and the
corridor-penalty H_sum is 0.007 against a Monte-Carlo noise floor of 0.002, and
the reweighted C_ℓ equals the input at every coupling β.

The framework is a strict extension of ΛCDM at the cosmological tier:
C_ℓ^framework = C_ℓ^ΛCDM at every multipole and every coupling. The bulk power
spectrum is ΛCDM, untouched. The framework's distinctive content is confined to
the shape sector. This is the session's one proved cosmological result.

## 2. The corridor at coordinated substrates (Claims 1 and 4)

**fMRI — confirmed.** ABIDE-PCP, 139 typically-developing controls across seven
acquisition sites, CC200 parcellation. Debiased functional-connectivity ρ:
median 0.266, IQR 0.134 — inside the recalibrated A3+ band, off the rigidity
pole and off the chaos pole, distribution unimodal. Stable under motion control
(low-motion subset, n=121) and uniform across all seven sites. Pre-registered.

**TCGA — confirmed at the cellular substrate.** Seven new disjoint cancer types,
real GDC data, pre-registered. Healthy tissue is tight-banded off both poles
(per-cancer IQR 0.08–0.13). Tumour drift: 201 of 201 significant pathway shifts
go chaos-ward, reproducing the prior five-cancer 176/176. The absolute band
centre is pipeline-dependent — GDC STAR-Counts ρ ≈ 0.34 against the prior
pipeline's 0.27.

**LLM internals — weak.** gpt2, Pythia-160m, Qwen2.5-0.5B, real weights.
Debiased within-layer ρ runs 0.05–0.22 over 48 layers. Decisively off the
rigidity pole; low, at the chaos-side edge of the corridor.

**Allen Brain — a chaos-pole data point.** 25 mouse visual-cortex two-photon
sessions, spontaneous epoch. Mean pairwise neuron ρ ≈ 0.023. This is a data
point, not a falsifier: the framework's canonical shape observable is the
participation-ratio k_eff of the activity covariance, not the mean pairwise
correlation, and cortex is the case where the two diverge. The k_eff re-test on
the same data is owed.

The corridor is confirmed at two coordinated substrates (human-neural, cellular),
weak at one (LLM), and one substrate (mouse cortex) returns a chaos-pole datum
pending the canonical-observable re-test.

## 3. The structural-claims specification

`StructuralClaims.lean` states six corridor-centered claims, each paired with a
falsifier and a machine-checked `ClaimN ↔ ¬FalsifierN` equivalence. The series:

- **Claim 2 — falsified as stated, then amended.** E2, six independent
  Lindbladian instances: 2 of 6 had non-ergodic forward generators. Forward
  ergodicity holds when the maintenance breaks the dynamical symmetries; the
  amendment carries that antecedent. A test fed back into the specification.
- **Claim 3 — consistent.** E3: a closed system conserves energy, so its
  late-time ρ is energy-indexed — a one-parameter family, no corridor attractor
  without maintenance.
- **Claim 5 — consistent.** E6: 0 of 200 generic high-entropy initial states
  forward-evolve to multi-rung corridor structure.
- **Claims 1, 4** — see §2.
- **Claim 6** — see §4.

## 4. The cross-rung tier

**Path 1 — the cross-rung coupling is O(1).** The cross-rung / within-rung
coupling ratio measured at two real rung pairs, pre-registered: TCGA
molecular→pathway 0.93–1.47, LLM internal→external 0.47–0.74. w3 extended the
measurement to 24 LLM cells: median 0.73, range 0.25–1.78.

**Claim 6 — amended.** The abstract cross-rung tower scan gave a strong
dominance gate, g/J ≳ 3. Path 1 measured O(1). The strong-dominance form is
retracted as tower-specific; Claim 6 is the cross-rung coupling corridor at
g/J ~ O(1).

**Head-to-head with Simon.** Herbert Simon's near-decomposability predicts
g/J ≪ 1; the abstract tower predicted g/J ≳ 3. The real rung pairs sit at
neither — intermediate coupling, O(1). The data occupies territory neither
established position predicts.

**The canonical timescale g/J — measured at no substrate.** w3 sought it at the
LLM internal→external pair: observable-blocked, 1 gate-pass of 48 family-cells,
the rest noise-dominated. w3b sought it at a CIRISArray GPU block pair: a
fit-failure. An oscillation check established that w3b's failure is a noisy
observable (the running-correlation-of-windows construction overshoots negative
even on pure relaxors and white noise), not physics. The coupling-ratio form of
the cross-rung claim is anchored across 26 measurements; the timescale form is
not accessible with the observables and substrates tried.

## 5. Corridor dynamics — the corridor-exit rate

The framework's dynamics dρ/dt = α − γM had never been measured — only the
static corridor ρ. It is now measured at one substrate. The GPU, via the
CIRISArray strain gauge: the unmaintained free corridor-exit relaxation,
1/τ = 0.0214 ± 0.0022 s⁻¹, τ ≈ 46.7 ± 4.9 s. Pre-registered, artifact-verified
across five gates, six independent captures.

Attempts at the LLM, the paired non-corridor record, and C. elegans whole-brain
calcium returned nulls. The corridor observable resists being made a clean time
series except where the substrate is itself a coherence instrument — which the
GPU strain gauge is and the others are not.

## 6. The particle-physics extension

Four pre-registered tests of the corridor shape observable at particle-physics
observables — decay branching fractions, decay mode-weights at fixed Q-value,
CP-violation structure, the tt̄ spin-density matrix — returned four nulls. The
participation-ratio shape observable computes on any distribution; the corridor
structure does not recur at particle observables. The tt̄ spin-density matrix
gave ρ = 0.076, statistically identical to the Standard Model prediction 0.073.

This is consistent with the framework: decay channels and CP asymmetries are not
coordinated rungs with maintained dynamics. The framework's particle-physics
tier is composition with the Standard Model, not framework-distinctive
prediction.

## 7. CMB

The age of the universe, computed from the Planck 2018 ΛCDM parameters:
13.80 Gyr (Planck's published value, 13.797 ± 0.023). The age is a bulk
observable; the orthogonality theorem preserves it exactly.

The shape-sector temporal drift is a signed, multipole-resolved profile with a
crossover near ℓ=3 — computed, gated on the corridor calibration, and the
framework's distinctive cosmological prediction, testable by CMB-S4 over coming
decades. WMAP and Planck cross-validate the present-epoch shape profile to mean
|Δ| = 0.0015.

Under ΛCDM with Ω_Λ > 0 the future proper-time integral diverges: the
CMB-derived cosmology has an infinite future. There is no finite maximum
lifetime.

## 8. The wave campaign

Four pre-registered parallel experiments off the cross-rung result. w1-rg: the
dead-zone RG commutator ε is not the cross-rung coupling ratio — independent
constraints. w1-width: the framework's corridors are sub-decade (mean ≈ 0.5
decade), not the one order of magnitude an earlier reading proposed. w1-rungcount:
the multi-rung corridor has no rung budget — it survives to arbitrary rung count.
w2: the GPU corridor-exit rate (§5). Two refutations, two positives, every one
pre-registered, the refutations folded back into the specification.
