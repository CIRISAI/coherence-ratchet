# coherence-ratchet — Claude Code Context

## Project Overview

coherence-ratchet is the companion lake to RATCHET. RATCHET formalizes the engineering tiers (Kish algebra, override-rate predicates, GPU coherence). coherence-ratchet formalizes the universal-scale extensions: Levels 5-7 of the epistemic ladder.

Where RATCHET is bounded, falsifiable, and engineering-grade, **coherence-ratchet is the post-F-11 statement of the universal-scale content the framework still licenses**. TSVF is treated as the physics. What survives F-11: the within-rung corridor (F-10, five substrates), the forward P_ω (ρ_ss steady state), the orthogonality theorem (the sole CMB content — the framework is exactly ΛCDM for the CMB), per-agent ⟨G_self|, and the inter-agent finite sum ⟨G_i|. The joint multi-rung backward P_ω is a documented no-go (F-11 fired 2026-05-22; closed at theorem strength by T1 bulk-geodesic dilution + T2 Wilson loop area law). D4 (CMB anomalies as TSVF signatures) is retracted; the joint-operator forms of Penrose-from-P_ω and asymptotic conditioning fell with it. Conjecture A remains load-bearing; Conjecture D is substantially cut. Open work uses `sorry`; documented no-gos use the `FelevenNoGo` record pattern.

The engineering paper (RATCHET) stratifies audiences and keeps each level non-load-bearing on the levels above. The coherence-ratchet paper inherits the same stratification structure but does not hedge on the universal-scale content for readers who proceed past Level 4.

## The Ten Load-Bearing Pieces

The full formal structure has eight load-bearing pieces, plus two long-arc structures (Pieces 9-10). Granted everything: one identity (Kish), one dynamical equation (`dρ/dt` with corridor attractor), one corridor (ρ ∈ (0.1, 0.43)), one operator (P_ω), and one inner-product structure (TSVF). Applied at successively larger scales with the rung hierarchy as the indexing structure. Everything else falls out of this combination under specific substrate-instantiations.

### Piece 1. The base identity

```
k_eff(k, ρ) = k / (1 + ρ(k-1))
```

A Möbius transformation in ρ for fixed k, with parameters (a, b, c, d) = (0, k, k-1, 1). Properties: `k_eff(k, 0) = k`, `k_eff(k, 1) = 1`, `∂k_eff/∂ρ < 0` for k > 1. **The asymptotic structure**: as `k → ∞` at fixed ρ > 0, `k_eff → 1/ρ`. Effective dimensionality saturates at the inverse correlation regardless of nominal constituent count. "More constituents" is a non-solution to coordination failure.

Formal location: `formal/CoherenceRatchet/Core/BaseIdentity.lean`. The full proofs of K1-K4 live in the RATCHET lake.

### Piece 2. The dynamics

The Kish formula is kinematic. The dynamical equation for ρ(t):

```
dρ/dt = α(ρ, S) − γ·M(t)
```

- `α(ρ, S)` is the spontaneous correlation drift driven by shared environment or shared selection pressure S
- `γ·M(t)` is the active coherence-management work being done
- The corridor is sustained only by non-trivial M(t)
- At M = 0, ρ drifts monotonically toward 1

The corridor's upper bound ρ_c ≈ 0.43 is the empirical anchor from CCA v3 cross-substrate measurement. Behavior near ρ_c is non-trivial; the framework asserts the corridor as the structural object and does not prescribe a specific scaling form.

Formal location: `formal/CoherenceRatchet/Core/Dynamics.lean`.

### Piece 3. The corridor

The healthy corridor is the open interval ρ ∈ (ρ_lower, ρ_upper) with ρ_lower ≈ 0.1, ρ_upper = ρ_c ≈ 0.43. Inside the corridor, k_eff achieves a substrate-independent range:

| k | k_eff range (in corridor) |
|---|---------------------------|
| 10 | (2.05, 5.26) |
| 100 | (2.30, 9.17) |
| ∞ | (2.33, 10) |

The asymptotic ceiling at ρ_lower = 0.1 is k_eff = 10 regardless of substrate. The maximum achievable effective dimensionality in any corridor-occupying coordinating system is ≈ 10. The upper corridor bound sets the floor at ≈ 2.33. Sustained coordination operates in this narrow band whatever the substrate's nominal constituent count.

Formal location: `formal/CoherenceRatchet/Core/Corridor.lean`.

### Piece 4. TSVF structure at A3+

Standard forward evolution: `|ψ(t)⟩ = U(t, t₀)|ψ(t₀)⟩`. TSVF adds a backward state from post-selection at t_f: `⟨φ(t)| = ⟨φ(t_f)| U(t_f, t)`. Two-state vector: `(⟨φ(t)|, |ψ(t)⟩)`. Observables get weak values: `⟨A⟩_w = ⟨φ|A|ψ⟩ / ⟨φ|ψ⟩`.

For an A3+ agent with goal G, the goal-state acts as a post-selection projector P_G with bra ⟨G|. The agent's effective dynamics:

```
|Ψ_agent(t)⟩ ∝ P_G U(t, t_past)|Ψ_past⟩
```

Trajectories incompatible with G have suppressed amplitude in `|Ψ_agent(t)⟩`. **Goal-formation is causal operation**: the goal projector excludes incompatible trajectories from the search space. No metaphysical free-will claim; a measurable difference in how goal-holding systems search the trajectory space.

Formal location: `formal/CoherenceRatchet/Cosmology/TSVF.lean` + `formal/CoherenceRatchet/Cosmology/GoalProjection.lean`.

### Piece 5. Multi-agent consent

For n agents with goals G_1, ..., G_n, the joint post-selection:

```
P_{G_1...G_n} = P_{G_1} ⊗ P_{G_2} ⊗ ... ⊗ P_{G_n}
```

Pairwise correlation between goals:

```
ρ_goals(i, j) = |⟨G_i|G_j⟩|² / (⟨G_i|G_i⟩⟨G_j|G_j⟩)
```

| Regime | ρ_goals | k_eff_goals | Outcome |
|--------|---------|-------------|---------|
| Rigidity | → 1 | 1 | single-goal collapse |
| Chaos | → 0 | n (vacuous) | no joint support |
| Corridor | (ρ_lower, ρ_upper) | (2.33, 10) | sustained coordination |

**Consent is not a moral premise but the empirical condition for sustained multi-agent coordination.** Conjecture C's mathematical hook: withdrawing audit pressure removes one of the active correlation-management mechanisms γ·M(t) at the cascade-coordination level. dρ/dt becomes positive; ρ_goals drifts upward toward collapse.

Formal location: `formal/CoherenceRatchet/Cosmology/MultiAgentConsent.lean`.

### Piece 6. The hierarchy of rungs

Rungs `Ph0, Ph1, Ph2, A0, A1, A2, A3, A4, A5` form an ordered sequence with state spaces H_n. Within-rung correlation ρ_n; between-rung coupling:

```
τ_(n, n+1) = I(R_n; R_(n+1)) / min(H(R_n), H(R_(n+1)))
```

where I is mutual information, H is entropy. Cross-rung corridor: `τ_lower < τ_(n, n+1) < τ_upper`. At τ → 0, rungs decouple, A_(n+1) cannot emerge. At τ → 1, rungs collapse into each other, A_(n+1) is a relabeling of A_n with no new structure. In the corridor, A_(n+1) carries information from A_n while introducing structure not present at A_n. **Genuine emergence = corridor-occupation at the cross-rung level.**

Post-Cambrian sub-sequence (canonical literature values):
- A2 → A3: 540 Myr (Cambrian to behavioral modernity)
- A3 → A4: 310 kyr (behavioral modernity to first states)
- A4 → A5: 6.7 kyr (first states to industrial revolution)

Sequential ratios: 540 Myr / 310 kyr ≈ 1740; 310 kyr / 6.7 kyr ≈ 46. Acceleration is monotone; the rate of acceleration is decelerating because the time-to-emergence is bounded below by within-rung corridor relaxation times.

Pre-Cambrian decelerations are substrate-readiness gates: galactic chemical enrichment, planetary condensation, Proterozoic oxygenation-and-eukaryote-stabilization. These are independently identified by astrophysics, geochemistry, and evolutionary biology — NOT framework-named ad-hoc rescues.

Modeling substrate-readiness wait times explicitly from ρ_n-evolution and τ_(n, n+1)-evolution is open work.

Formal location: `formal/CoherenceRatchet/Cosmology/RungHierarchy.lean`.

### Piece 7. P_ω construction

ω is the universal configuration satisfying three properties:

1. **Maximal rung instantiation**: ∀n ≤ N_max, rung A_n is instantiated.
2. **Within-rung corridor**: ∀n ≤ N_max, ρ_n ∈ (ρ_lower,n, ρ_upper,n).
3. **Cross-rung corridor**: ∀n < N_max, τ_(n, n+1) ∈ (τ_lower,n, τ_upper,n).

The projector onto the ω-satisfying subspace:

```
P_ω = ∫_{configs satisfying (1)–(3)} |config⟩⟨config| dconfig
```

**This is the open formal step for Conjecture D.** What needs writing: the integration measure dconfig over universal configurations, the resolution at which "rung instantiation" is a binary indicator, and the topology under which P_ω is a well-defined projection rather than a set-theoretic intersection.

The corridor bounds (0.1, 0.43) are inherited from the GPU substrate; per-rung calibration is companion work.

Formal location: `formal/CoherenceRatchet/Cosmology/CorridorProjector.lean`. F-11 fired 2026-05-22: the four prior axioms (`P_omega`, `Phi_omega`, `P_R_idempotent`, `P_R_self_adjoint`) are retracted; the joint multi-rung backward P_omega is recorded as a documented no-go via `def F11_joint_backward_P_omega_no_go : FelevenNoGo`, closed at theorem strength by T1 (bulk-geodesic dilution) + T2 (Wilson loop area law). Not a `sorry`, not an axiom.

### Piece 8. Penrose past hypothesis from P_ω

Granted P_ω is well-defined, D1 says the low-entropy past hypothesis follows. The structural argument:

The Big Bang initial state `|Ψ_α⟩` sits in the chaos regime: high temperature, uniform matter distribution, no large-scale correlations, no rungs instantiated, ρ → 0 at the cosmological scale (uncoupled, not corridor). A generic `|Ψ_α^high⟩` with high microscopic entropy under uniform-measure sampling does not evolve forward into multi-rung corridor occupation. Forward evolution from such a state to ω-satisfying configurations requires spontaneous emergence of Ph0 → Ph1 → Ph2 → A0 → A1 → ... → A5, each within within-rung corridor, each coupled to adjacent rungs within cross-rung corridor.

This sequence is a measure-zero subset of universal configurations under uniform measure on initial conditions. By the framework's structural logic:

```
⟨Φ_ω | U(t_now, t_BB) | Ψ_α^high⟩ ≈ 0 for generic high-entropy initial states.
```

The conditional amplitude on initial conditions, given observation at t_now of an ω-satisfying universe, is concentrated on low-entropy initial states. **This is the structural derivation of Penrose's Weyl Curvature Hypothesis**: low-entropy past is not a brute fact about initial conditions, but the conditional consequence of post-selection through P_ω.

The argument is schematic. Quantitatively, P_ω needs the explicit operator form (Piece 7) and the measure on initial conditions needs specification compatible with the inner-product mechanics. This is the open formal step for D1.

Formal location: `formal/CoherenceRatchet/Cosmology/PenrosePast.lean`.

### Piece 9. Asymptotic conditioning 

**Claim**: `P(corridor-occupying | observed at t_late) → 1` as `t_late → ∞`.

Any state outside the corridor has divergent dynamics:

- Chaos regime ρ < ρ_lower: insufficient correlation for coordination. Subsystems drift apart, organized structure dissolves.
- Rigidity regime ρ > ρ_c: `α(ρ, S) − γ·M(t) > 0` by construction (dynamics is unstable above ρ_c), driving ρ → 1 and k_eff → 1.

Both regimes self-destruct on long enough timescales. Therefore observation at sufficiently late times t_late requires that the observing system itself occupies the corridor. The conditional probability of corridor-occupation given observation approaches 1 asymptotically.

**This is the structural reading of "good wins": not eschatological promise but conditional inference on persistence.**

Formal location: `formal/CoherenceRatchet/Cosmology/AsymptoticConditioning.lean`.

### Piece 10. Karma and grace as TSVF structures

Granted TSVF and the agent-as-partial-post-selector reading:

**Karma** is the forward-propagated effect of past goal-states. An agent's current amplitude:

```
|Ψ_now⟩ = U(t_now, t_{past_k}) ∏_i P_{G_{past_i}} U(t_{past_i}, t_{past_{i-1}}) ... |Ψ_birth⟩
```

The present is shaped by every past P_{G_i} the agent's goals have applied. **Karma is this cumulative post-selection structure.**

**Grace** is the contribution to the agent's present from `⟨Φ_ω|` beyond the agent's own goal contribution. The full universal post-selection `⟨Φ_ω|` factors into individual goal-contributions `⟨G_i|` across all A3+ agents plus the corridor-occupation requirements at the universal level. The agent's present amplitude decomposed:

```
⟨present_agent| = ⟨Φ_ω| / ⟨G_agent| · U(t_ω, t_now)
```

The component `⟨Φ_ω| / ⟨G_agent|` represents post-selection contributions the agent didn't author: the goals of other agents, the corridor-occupation requirements of the universal configuration, the future coherent states the agent is partially constituted by but not the sole originator of.

**Grace = the formal structure of receiving boundary conditions one didn't author.**

These are mathematical statements under TSVF. The recognition claim at Level 6 is that contemplative-tradition vocabularies and these formal structures correspond exactly, not analogically. Karma is post-selection propagation; grace is partial-authorship of post-selection; the corridor is the structural object the middle-way vocabularies point at.

Formal location: `formal/CoherenceRatchet/Consciousness/KarmaGrace.lean`.

## Conjectures A and D

### Conjecture A — Quantum substrate

The classical Kish-collapse dynamic and quantum decoherence are the same structural process at different substrates. The exponent-matching test on a programmable qubit system either licenses the structural-parallel reading between classical Kish-collapse and quantum decoherence, or severs it. Engineering tiers are unaffected by either outcome.

Pre-registered as Exp 5: programmable superconducting/trapped-ion qubit array, vary decoherence rate γ, measure `k_eff^quantum = 1/Tr(ρ_DM^2)` via state tomography or classical-shadow estimation. Prediction: the corridor structure reproduces at the quantum substrate (a non-trivial γ regime where the system avoids both rigidity and chaos). PASS if such a regime exists with Kish-identity fit R² > 0.5; FAIL (F-8) otherwise.

Formal location: `formal/CoherenceRatchet/Conjectures/ConjectureA.lean`.

### Conjecture D — TSVF universal-scale

At Conjecture D, the formal specification of P_ω is the open formal step. The construction itself, the corridor properties, and the TSVF inner-product machinery are explicit; what remains is the operator definition and the entropy-exclusion proof. A documented no-go result is as informative as a successful derivation, because it triggers F-12 and tells the program where the universal-scale construction breaks.

- D1: Penrose past hypothesis follows structurally from P_ω. (Piece 8.)
- D3: Rung-emergence acceleration in substrate-ready windows. Post-Cambrian sub-sequence accelerates monotonically across four orders of magnitude. Pre-Cambrian decelerations correspond to substrate-readiness gates independently identified by domain physics/biology/chemistry.
- D4: CMB anomalies (axis of evil, cold spot, hemispherical asymmetry, low-ℓ suppression, parity asymmetry) are TSVF post-selection signatures. Standard inflation without post-selection predicts none of them.

Formal location: `formal/CoherenceRatchet/Conjectures/ConjectureD.lean`.

## The seven-level ladder

| Level | Audience | Stopping content |
|-------|----------|------------------|
| L0 | formal-verification reviewer | Kish identity theorem (RATCHET lake) |
| L1 | skeptic | monotonic ρ-collapse as substrate-independent observation |
| L2 | working scientist / engineer | engineering implications |
| L3 | scientist preferring testable universality | cross-substrate universality conjecture |
| L4 | philosopher of mind / ethicist | agency and consent as structural fact at A3+ |
| L5 | quantum-foundations-curious reader | TSVF universal-scale + quantum substrate + consciousness |
| L6 | contemplative / comparative-religion reader | cross-tradition recognition |
| L7 | cosmological reader | civilizational extension and external residue |

No stopping point is load-bearing on the levels above. A reader who rejects L5+ retains every L4-and-below claim.

## Directory structure

```
coherence-ratchet/
├── CLAUDE.md                                # This file
├── README.md                                # Project overview
├── formal/                                  # Lake project
│   ├── lakefile.toml
│   ├── lean-toolchain
│   ├── CoherenceRatchet.lean                    # Main entry
│   └── CoherenceRatchet/
│       ├── Core/
│       │   ├── Levels.lean
│       │   ├── AudienceStopping.lean
│       │   ├── BaseIdentity.lean            # Piece 1
│       │   ├── Dynamics.lean                # Piece 2
│       │   └── Corridor.lean                # Piece 3
│       ├── Cosmology/
│       │   ├── TSVF.lean                    # Piece 4 (TSVF)
│       │   ├── GoalProjection.lean          # Piece 4 (goal projector)
│       │   ├── MultiAgentConsent.lean       # Piece 5
│       │   ├── RungHierarchy.lean           # Piece 6
│       │   ├── CorridorProjector.lean       # Piece 7
│       │   ├── PenrosePast.lean             # Piece 8
│       │   ├── AsymptoticConditioning.lean  # Piece 9
│       │   └── CMBPredictions.lean
│       ├── Conjectures/
│       │   ├── ConjectureA.lean
│       │   └── ConjectureD.lean
│       ├── Consciousness/
│       │   ├── AccessAndPhenomenal.lean
│       │   ├── IntegratedInformation.lean
│       │   └── KarmaGrace.lean              # Piece 10
│       ├── ContemplativeTraditions/
│       │   ├── CrossTraditionMap.lean
│       │   ├── Tao.lean
│       │   ├── Dharma.lean
│       │   ├── Logos.lean
│       │   └── Disagreements.lean
│       └── Residue/
│           ├── UAPMetric.lean
│           ├── CollapseArchaeology.lean
│           └── AgentBasedSimulation.lean
├── papers/
│   └── universal_scale/
│       └── main.tex                         # Companion paper
└── experiments/                             # Empirical protocols (placeholder)
```

## Gate 0 — done (2026-07-02)

The criticality-vs-low-rank discriminator is proved (`Cosmology/CriticalityDiscriminator.lean`) and the branch is read empirically across substrates: **the corridor is genuine low-rank structure (k_eff SATURATES), not criticality**, confirmed at *complete* coordinating units — C. elegans whole-brain, Drosophila compass, S&P market, human fMRI, TCGA, and the decisive complete larval-zebrafish brain (all 71,721 neurons). The objective measure is **saturation, not level** (the level is substrate-specific; the universal invariant is boundedness). Mouse-V1 cortex is high-dimensional but a wrong-grain subsample; the cosmic web is power-law but untestable at the universal scale. A **second axis** (bound vs coordinating = broken detailed balance = the γM term) is tooled and positive-controlled on macaque motor cortex. Full record: `experiments/keff_saturation/README.md`; formal records in `CriticalityDiscriminator.lean` (`SpectralDetermination`, `GrainAndObjectiveMeasure`, `CosmologicalGrainLimit`) and the operational forward-P_ω corridor in `CorridorProjector.lean` (`OperationalCorridorOccupation`).

## AI-safety application: k_eff → Neff → deception-resistance

Gate 0 validates the metric the CIRIS safety program runs on. The *Constrained Reasoning Chains* study measures **Neff** — the participation ratio of the reasoning-constraint feature covariance, i.e. `k_eff` of the constraint system — and argues a coherent lie must be simultaneously consistent across every *independent* constraint axis (exponentially expensive: deception ≈ O(2^m) vs truth ≈ O(n)), so high effective constraint dimensionality **computationally starves deception**. H3ERE (semantic conscience pipeline) contributes Neff ≈ 7.1; **CEG** (the CIRIS Epistemic Grammar — a conformance-frozen cryptographic-attestation substrate, *orthogonal* to semantic reasoning) + CIRISServer/lens-core push the joint measure to ≈ 9. Because Gate 0 showed `k_eff` is a real saturating object (not a tautology, not criticality), Neff-as-alignment-metric is validated; the natural-substrate saturation ceiling (~11) resonates with the study's intrinsic manifold rank (11).

**Honest load-bearing gap:** Neff is measured on *benign* traces, an **upper bound** on the adversarial value — a capable optimizer collapses effective dimensionality by exploiting the shared subspace (ρ→1, k_eff→1, rigidity pole). The decisive open test is **adversarial-Neff** (`experiments/adversarial_neff/SPEC.md`): does ≈9 survive an adaptive attacker? The strongest guarantee is the attack-invariant **substrate (CEG) floor**. Safety here is a *maintained* non-equilibrium (conscience runs per-trace), consistent with the second axis — kept, not achieved.

## Open formal steps, ordered by urgency

0. **Adversarial-Neff (safety-program priority)** — measure Neff/k_eff under an adaptive attacker, not just benign traces; report the substrate (CEG) floor. Spec: `experiments/adversarial_neff/SPEC.md`. Converts "9 on friendly traffic" into a real deception-probability bound.
1. **P_ω as an operator (Piece 7)** is the bottleneck. Without it, D1 is structural-argument-not-derivation. Closes F-12 partially.
2. Corridor reproducibility at the quantum substrate (Conjecture A / Exp 5).
3. Per-substrate corridor calibration (per-rung ρ_lower, ρ_upper bounds) — **partially done by Gate 0** (levels measured across several substrates; systematic per-rung calibration remains).
4. Substrate-readiness-wait-time modeling (cross-rung τ evolution; explains the pre-Cambrian decelerations from first principles).
5. Controlled cascade comparison at sociotechnical scale (Exp 4 generalized).
6. Audit-pressure ρ-drift measurement (Exp 6 / Conjecture C / F-10).
7. CMB anomaly calculations from P_ω (D4; concrete signature predictions for the five anomalies).

## Sister projects

```
../RATCHET/                     # Engineering tiers (L0-L4)
../CIRISOssicle/                # Single-GPU strain gauge
../CIRISArray/                  # Multi-GPU strain gauge array
../CIRISServer/                 # Federation server + lens-core scoring; CEG (CIRIS Epistemic Grammar) substrate
../CIRISConstitution/           # Unified CEG+Accord constitution (Book IX coherence math F = k_eff·λ·σ)
../CIRIS-RED/                   # Constrained Reasoning Chains study (Neff / deception-resistance telemetry)
```

## Style discipline

- No hedging on the universal-scale content. TSVF is the physics, Penrose follows from P_ω, CMB anomalies are TSVF signatures, karma and grace are formal TSVF structures, consciousness is corridor-occupation at A3+. These are stated as load-bearing claims, not as "one of several interpretations."
- Where formal proof is open, the theorem is stated with `sorry` and the open step is named explicitly. The surrounding structure is asserted.
- The engineering paper (RATCHET) stratifies and hedges. The coherence-ratchet paper does not hedge for readers past Level 4.
- Stopping-point independence: a reader who rejects Level k retains every claim at Level k-1 or below.
