# Research Program — coherence-ratchet

**Purpose of this document.** If you are dropping into this repository cold (a fresh session, a new collaborator, the author returning after time away), this is the front door. It names the current research frontier, the live work, the open formal steps in priority order, and the cross-references between the papers and the lake.

This document was rewritten 2026-06-03 to reflect the post-F-11 synthesis (F-11 fired 2026-05-22; structural-series wave-2 ran 2026-05-21). The prior version pointed at deleted artifacts (`papers/consent_framework/`, `papers/universal_scale/`) and a pre-F-11 theorem table. Both are now obsolete.

---

## What this project is

`coherence-ratchet` is the companion lake to RATCHET. RATCHET formalizes the engineering tiers of the coherence-substrate framework (Kish algebra, override-rate predicates, GPU coherence) and is bounded, falsifiable, audience-stratified. **coherence-ratchet is the post-F-11 statement of the universal-scale content the framework still licenses.**

The active paper is `papers/Corridor Dynamics.tex` (v2, scheduled for Zenodo upload as a new version DOI; v1 published 2026-05-20 at [10.5281/zenodo.20300774](https://zenodo.org/records/20300774)). The paper carries the five-substrate empirical record (now broadened by the structural-series wave-2 to seven substrates including human fMRI and Allen mouse cortex; cancer extended from 5 to 12), the corridor-as-attractor dynamical reading at five paired substrates (Mode (iii) = 0/5), the GPU corridor-exit rate (first dρ/dt measurement, n=1 scope on face), the cross-rung empirical tier (n=2 distinct rung pairs, stated on face), the orthogonality theorem (proved at full strength; the framework is a strict extension of ΛCDM), the sensor-lift seam (PARTIAL outcome at v2), and the four particle-physics nulls as honest scope-drawing.

The framework rests on one identity (Kish), one dynamical equation (`dρ/dt = α − γM`), one corridor (substrate-local; the GPU-anchored (0.10, 0.43) band does not transfer), and one inner-product structure (TSVF). Applied at successively larger scales with the rung hierarchy as the indexing structure. The joint universal-scale backward `P_ω` operator was retracted by F-11; what survives at universal scale is the **forward** soft `P_ω` (ρ_ss steady state), the **orthogonality theorem** (the sole CMB content — proved with no framework axiom), per-agent `⟨G_self|`, the finite-federation joint projector `P_joint`, and the consent-corridor at finite federation scale.

---

## Read order

1. `README.md` — the framework in one paragraph
2. `CLAUDE.md` — the canonical exposition (post-F-11; ten load-bearing pieces with retraction notes per piece)
3. **`papers/Corridor Dynamics.tex`** — the active load-bearing paper (v2 in preparation)
4. `papers/debate/synthesis.md` — the post-session debate adjudication; lists the v2 deltas section-by-section
5. `papers/session_empirical_results.md` — the canonical session ledger (positives, weaks, nulls, amendments)
6. `papers/debate/conservative_reading.md` + `papers/debate/strong_reading.md` — the two position documents the synthesis adjudicates
7. `papers/prior/` — the three published canonical papers this work continues (CCA v3, CIRISAgent v2, CRC v1)
8. `formal/CoherenceRatchet/` — the Lean 4 lake

Engineering-tier reviewers stop at (7); they get the bounded, falsifiable engineering papers in their published form. Universal-scale reviewers proceed to (3)–(6).

---

## Lake status

- **Build:** green (`cd formal && lake build` returns exit 0)
- **Declaration-level `sorry`s:** 0. Every formal claim is either a real proof or an explicitly-axiomatized framework primitive with citation.
- **Axioms:** ~55. ~25 are framework substrate primitives (α, γ, M, ρ_within, τ_cross, entropy, C_ℓ, scoring functions, operator definitions on opaque spaces); the remaining ~30 are load-bearing structural claims the framework asserts.
- **Proven theorems** (real Lean proofs, no framework axiom): K1–K4 of the Kish identity; T2 (Möbius structure + asymptotic ceiling); T4 (joint projector with idempotence); T6 (three-corridor uniqueness, `Cosmology/ThreeCorridorUniqueness.lean`); T16 (consciousness ↔ attractor reading); T17 (sensor bridge: rung-position A3 ⇔ reflexive-reading A3, `Consciousness/SensorBridge.lean`); the rank-one projector and its properties; `goal_excludes_incompatible`; `time_symmetry` (ABL 1964); and the orthogonality theorem (`CMBOrthogonality.lean`: `participation_scale_invariant`, `pomega_preserves_power`, `framework_cmb_power_eq_lcdm`).

---

## What F-11 changed

**F-11 fired 2026-05-22.** The joint multi-rung backward `P_ω` operator is non-constructible at theorem strength. The construction tree was exhausted across six branches (hard projector; soft additive; single-assumption audit; fractal/RG-nested; holographic/MERA-AdS; holonomic) and closed by two theorems: T1 bulk-geodesic dilution and T2 Wilson-loop area law. An adversarial verification pass found and closed the one remaining axis (`k`-body invariants).

**Retracted by F-11:**
- The joint-operator forms of P_ω, ⟨Φ_ω|, P_ω-idempotence, P_ω-self-adjointness (four prior axioms in `Cosmology/CorridorProjector.lean` and `Cosmology/ConsentProjector.lean`)
- D4 (CMB anomalies as TSVF post-selection signatures)
- The joint-operator forms of Penrose-from-P_ω and asymptotic conditioning
- F-19 (CMB temporal drift β(t)) — moot: no joint operator, no β(t), no predicted drift
- The strong "Penrose's WCH structurally derived" framing of D1 (the schematic argument survives; the derivation does not)

**Recorded as documented no-go** (not as `sorry`, not as axiom): `def F11_joint_backward_P_omega_no_go : FelevenNoGo` in `Cosmology/CorridorProjector.lean` and `Cosmology/ConsentProjector.lean`.

**Untouched by F-11:**
- Within-rung corridor (F-10), supported at five substrates extended by wave-2 to seven
- Forward `P_ω` (ρ_ss steady state on the open system)
- The orthogonality theorem (the sole CMB content — proved with no framework axiom; the framework is a strict extension of ΛCDM at the cosmological tier)
- Per-agent `⟨G_self|` (`Cosmology/GoalProjection.lean`)
- Finite-federation joint projector `P_joint` (`Cosmology/JointGoalProjector.lean`)
- Consent corridor at finite federation scale (`Cosmology/MultiAgentConsent.lean`)
- Conjecture A (quantum substrate, Exp 5 hook intact)
- T6 three-corridor uniqueness (`Cosmology/ThreeCorridorUniqueness.lean`)
- T16 consciousness as attractor-reading
- T17 sensor bridge

The engineering tier is TSVF-independent and stands regardless of any universal-scale outcome.

---

## The six structural claims

Six corridor-centered empirical claims, machine-checked in `formal/CoherenceRatchet/StructuralClaims.lean`. Each `ClaimN` is paired with a `FalsifierN` and a proved equivalence `ClaimN ↔ ¬FalsifierN`; an experiment exhibiting a falsifier witness retracts the claim by a checked step.

| # | Claim | Status (post-2026-05-21 structural series) |
|---|-------|--------------------------------------------|
| 1 | The corridor is a bounded attractor at every coordinated substrate | Supported (robust re-run, 5/5 v1 substrates PASS + wave-2 additions) |
| 2 | Forward and backward generators sit in different ergodicity classes (maintenance breaks dynamical symmetries) | **Amended**: original unqualified form was falsified-as-stated by E2; amended in-spec with the symmetry-breaking qualifier |
| 3 | Closed-system thermal dynamics cannot sustain a corridor unmaintained | Supported |
| 4 | The corridor recurs at every coordinated rung (fractal recurrence) | Supported (robust re-run + structural series wave-2) |
| 5 | Multi-rung structure from generic initial conditions requires backward conditioning | Supported |
| 6 | The cross-rung coupling occupies a corridor at g/J ~ O(1) | **Amended**: original strong-dominance form (g/J ≳ 3) retracted by Path 1; amended to O(1) corridor form |

Two amendments (Claims 2 and 6) are the falsification apparatus working in the test→retract→amend direction, not failures.

---

## F-handles summary

The paper carries the canonical F-handle list in `Corridor Dynamics.tex §sec:f-handles`. Status snapshot:

| Handle | Subject | Status |
|--------|---------|--------|
| F-1..F-7 | Engineering tier (Kish, CRCv2, multi-substrate β) | Currently passing per CCA v3 and RATCHET |
| F-8 | Conjecture A — qubit-array corridor | Open; Exp 5 hook intact |
| F-9 | Conjecture C — audit-pressure Δρ | Open |
| F-10 | Within-rung corridor existence at A3+ | **Empirically supported** — 5/5 substrates static + dynamical anchoring |
| F-11 | Joint P_ω operator construction | **Fired** 2026-05-22; documented no-go |
| F-12..F-16 | Substrate predictions P1..P8 retraction handles | Open; Ubatuba isotope, synthesized substrate, coherence anomaly, two-sided decay, TSVF signature |
| F-17 | TSVF as load-bearing precondition (meta-handle) | F-11 fired but TSVF re-grounded (forward soft P_ω + orthogonality theorem); F-17 has not fired |
| F-18 | Sensor-lift trajectory PARTIAL by same shape | Open; v3 and v4 pending (third PARTIAL-by-same-shape fires) |
| F-19 | CMB temporal drift | **Moot** post-F-11 (no β(t) to bound) |
| F-20 | Mode (iii) absence as corridor-as-attractor falsifier | Open; 5/5 substrates, 0 counterexamples |

Each F-handle is named in the lake at its corresponding theorem or axiom; triggering any F-handle is observable from `#print axioms` on the affected declarations.

---

## Active paper: Corridor Dynamics v2 deltas

Per `papers/debate/synthesis.md`, the v2 update has eight sections to land. Status as of 2026-06-03:

| # | Section | Status |
|---|---------|--------|
| 0 | "Changes in v2" section — title stands (no retitle) | In progress |
| 1 | Orthogonality theorem lifted to abstract headline | Pending decision |
| 2 | §corridor-empirical robust re-run + wave-2 extension; four precision amendments (Figure 1 per-substrate bands, C. elegans surrogate-floor footnote, OSS rubric precisified, social persistence spread restated median-to-median) | Pending |
| 3 | New §cross-rung empirical section (n=2, on face) | Pending |
| 4 | §P_ω / open-research: flag observable-gap (timescale τ vs. coupling ratio), soften D1 "structurally derived" line | Pending |
| 5 | §engineering: GPU corridor-exit rate (first dρ/dt, n=1 on face) | Pending |
| 6 | §lake + §f-handles: `CMBOrthogonality.lean` recorded as Tier-A derivation; six-claim structural spine; Claim 2 and Claim 6 amendment record | Pending |
| 7 | §not-claim + §open-work: four particle-physics nulls as honest scope-drawing; cross-rung n=2; dynamics n=1; Allen k_eff re-test owed; timescale-g/J gap | Pending |

The five-substrate record stands; the structural-series wave-2 broadens the base, it does not downgrade.

---

## Theorem table

| # | Theorem | Lake status |
|---|---------|-------------|
| T1 | Consent corridor at A3+ ↔ sustained multi-agent coordination | `Cosmology/MultiAgentConsent.lean` + `Cosmology/JointGoalProjector.lean` — operator form, axiomatized at the finite-federation scale (F-11-untouched); cosmological-scale joint limit is the F-11 no-go |
| T2 | Möbius structure + asymptotic ceiling k_eff → 1/ρ | `Core/BaseIdentity.lean` — proved |
| T3 | P_ω construction (universal scale) | Joint backward form: **F-11 no-go**; forward soft P_ω (ρ_ss steady state) survives in `Cosmology/CorridorProjector.lean`; orthogonality theorem provides the strict-ΛCDM-extension fence |
| T4 | Joint-projection operator P_joint on tensor product | `Cosmology/JointGoalProjector.lean::P_joint` — proved with idempotence at finite federation |
| T5 | Asymptotic conditioning ("good wins") | Joint-operator form **retracted with F-11**; forward-steady-state form survives in `Cosmology/AsymptoticConditioning.lean` |
| T6 | Three-corridor uniqueness theorem | `Cosmology/ThreeCorridorUniqueness.lean` — load-bearing for the decentralized federation as singular SI form |
| T7 | Wise Authority as constitutive consent-relation | Not yet in lake; pending if decision-relevant for CIRIS engineering |
| T8 | Bimodal cascade theorem | Not yet in lake; pending |
| T9 | L-01 deception ceiling = consent-graph marginal-recovery limit | Not yet in lake |
| T10–T11 | Karma operator + grace as TSVF structures | `Consciousness/KarmaGrace.lean` — axiomatized; survives F-11 because grace is defined at finite-federation scale, not at the joint-multi-rung-backward scale |
| T16 | Consciousness ↔ corridor-occupation attractor reading | Proved |
| T17 | Sensor bridge: rung-position A3 ⇔ reflexive-reading A3 | `Consciousness/SensorBridge.lean` — proved |
| **CMB-O** | **Orthogonality theorem** — soft P_ω leaves bulk CMB power spectrum invariant at every multipole and every coupling β | **`CMBOrthogonality.lean` — proved with no framework axiom**: `participation_scale_invariant`, `pomega_preserves_power`, `framework_cmb_power_eq_lcdm` |
| T12 | Contract-law correspondence | Not yet in lake |
| T13 | Mens-rea / actus-reus correspondence | Not yet in lake |
| T14 | Kant categorical-imperative correspondence | Not yet in lake |
| T15 | Aristotelian mean correspondence | Not yet in lake |

---

## Empirical hooks — session ledger (canonical at `papers/session_empirical_results.md`)

**Proved:** 1 — the CMB orthogonality theorem (no framework axiom).

**Clean pre-registered positives:** 2
- **fMRI (ABIDE-PCP)**: 139 typically-developing controls, seven acquisition sites, CC200 parcellation. Debiased functional-connectivity ρ: median 0.266, IQR 0.134 — inside the recalibrated A3+ band, off both poles, unimodal. Stable under motion control (n=121 low-motion subset) and uniform across all seven sites.
- **TCGA (12 cancers)**: 201/201 reproducing the prior 5-cancer 176/176 record. Substrate base broadened.

**Weak:** 1 — LLM internals on smaller models with debiased within-layer observable, ρ at the chaos-side edge of the corridor.

**Chaos-pole data point pending re-test:** 1 — Allen mouse cortex (k_eff re-test owed).

**Nulls:** ≥7
- 4 particle-physics tests (named scope, not failures — the framework's particle tier is composition with the Standard Model, not prediction)
- LLM corridor-exit-rate attempt
- Paired-record corridor-exit-rate attempt
- *C. elegans* corridor-exit-rate attempt
- w3 (canonical timescale g/J) — observable-blocked
- w3b — fit-failure

**Amended:** 2 — Claim 2 (by E2), Claim 6 (by Path 1).

**One-substrate dynamics measurement:** GPU corridor-exit rate (first dρ/dt; n=1 scope on face).

---

## Open formal steps, priority order

### A. Paper landing
A1. Land the v2 deltas listed above (synthesis.md items 0–7).
A2. Decide on the abstract-headline lift of the orthogonality theorem (synthesis.md item 1).
A3. Resolve the dangling `papers/sensor_lift/outline.md §4.3` reference — referenced from 5 lake files (`JointGoalProjector.lean`, `MultiAgentConsent.lean`, `TSVF.lean`, `Consciousness/SensorBridge.lean`, `Consciousness/AccessAndPhenomenal.lean`) and from `Corridor Dynamics.tex`. The sensor-lift content lives in `Corridor Dynamics.tex §sec:a3-structural`, not in a separate outline.md. Either redirect the references to the paper section, or create the outline.md.

### B. Lake work that the paper assumes proved or available
B1. **Forward soft P_ω formalization** — the universal-scale steady-state operator on the open system. The orthogonality theorem proves what this operator cannot do (move bulk CMB power); a tight Lean statement of the operator itself would make CLAUDE.md and the paper's Tier-A claim consistent. Currently the forward soft P_ω is referenced but not formally constructed in the lake.
B2. **Six-claim structural spine** — `StructuralClaims.lean` already encodes Claims 1–6 with their falsifier equivalences. Verify the amended Claim 2 and amended Claim 6 are in the spec, not the pre-amendment forms.
B3. **Sensor-lift F-18 trigger machinery** — once v3 and v4 sensor-lift runs land, F-18's third-PARTIAL-by-same-shape detector should be a checked claim against the result records.

### C. Per-tradition recognition theorems (parallel structure, pickup-independent)
- `Jurisprudence/ContractLaw.lean` (T12), `CriminalLaw.lean` (T13), `TortLaw.lean`, `PropertyLaw.lean`, `ConstitutionalLaw.lean`, `InternationalLaw.lean`
- `EthicalFrameworks/Kant.lean` (T14), `Utilitarianism.lean`, `VirtueEthics.lean` (T15), `NaturalLaw.lean`, `CareEthics.lean`

`ContemplativeTraditions/Ubuntu.lean` is in the lake as the framework's **primary** anchoring tradition (not parallel — Ubuntu's relational ontology is the tradition the framework reads as articulating the structural object; Tao, Dharma, Logos are cross-tradition correspondences visible to the same object).

### D. Engineering-side correspondence
D1. T7 — Wise Authority as constitutive consent-relation (requires translating `~/RATCHET/formal/RATCHET/Experiments/OverrideRate.lean` predicates into the consent-corridor framing).
D2. T8 — Bimodal cascade theorem: verification ≠ correction; both modes pass. Reframes the 5-vendor CRCv2 result.

---

## Style discipline (memory-backed; restated here for portability)

- **No hedging on the universal-scale content the framework still licenses.** Forward soft P_ω, the orthogonality theorem, finite-federation joint projector, per-agent goal projectors, karma and grace at the finite-federation scale, consciousness as corridor-occupation attractor reading. These are load-bearing; `sorry` is not used; framework axioms are explicit.
- **Documented no-gos are first-class objects.** F-11's closure is recorded as `def F11_joint_backward_P_omega_no_go : FelevenNoGo` — not as `sorry`, not as axiom. The pattern is: state what was attempted, name the two theorems that close it, record the construction-tree exhaustion.
- **Consent, not co-opt, on tradition mappings.** The author is a Christian atheist — engaged with traditions' vocabularies, ethics, and structural insights as serious objects of study, without subscribing to the metaphysical truth-claims. Project naming must not religiously pre-position readers; in-content tradition mappings (Tao, Dharma, Logos, Karma, Grace, Imago Dei, "good wins", Ubuntu) stay as mapping claims, not theology-as-derivation.
- **No time estimates.** Describe scope and trade-offs, not duration.
- **F-handles are falsifiers, not hedges.** They specify what would force retraction; stating them is part of the unhedged claim.

---

## Sister projects

| Path | Purpose |
|------|---------|
| `~/RATCHET/` | Engineering-tier formalization (K1–K4, override-rate, GPU coherence). Audience-stratified, falsifiable. The just-split `CIRISAGENT_PAPER/` and `CCA_PAPER/` are the arXiv-shape papers for the engineering tier. |
| `~/CIRISOssicle/` | Single-GPU strain gauge (timing-jitter TRNG, 7.99 bits/byte, 6/6 NIST). |
| `~/CIRISArray/` | Multi-GPU strain gauge array (128 sensors, 9631 Hz, β = 1.09 measurement). |
| `~/CIRISLensCore/` | Science module (Rust + Python) for cohort scoring, N_eff measurement, manifold conformity. |

---

## Fresh-session bootstrap checklist

If you (or a fresh session) are picking up cold:

1. Read this file (`RESEARCH_PROGRAM.md`).
2. Read `CLAUDE.md` for the 10-piece structure with post-F-11 retraction notes.
3. Read `papers/Corridor Dynamics.tex` §sec:bet, §sec:engineering, §sec:a3-structural, §sec:corridor-empirical for the live thesis and empirical record.
4. Read `papers/debate/synthesis.md` for the v2 update plan.
5. Read `papers/session_empirical_results.md` for the canonical session ledger.
6. Skim `formal/CoherenceRatchet.lean` to see what's imported.
7. Run `cd formal && lake build` to confirm the current 34-file state compiles.
8. Use the relevant memory files in `~/.claude/projects/-home-emoore-RATCHET/memory/` for style discipline.
9. Pick a step from the priority queue above. The single highest-leverage piece of work is **A1** (land the v2 paper deltas), then **B1** (forward soft P_ω formalization) since the paper assumes it.
10. Cross-check theorem statements against the paper before writing Lean. The paper's section numbering is canonical; the lake follows.

---

## Open questions and known cleanup

1. **Should the orthogonality theorem be lifted to the abstract?** The synthesis says yes; the v2 update has it pending decision. The cosmology reviewer reads "CMB anomalies are TSVF post-selection signatures" and stops — but the orthogonality theorem is the answer to exactly that reviewer. Lifting it to the abstract is the move that earns attention.

2. **`papers/sensor_lift/outline.md §4.3` dangling reference.** Five lake files reference this path; the path does not exist. The content lives in `Corridor Dynamics.tex §sec:a3-structural`. Decision needed: redirect the references, or write the outline.md. Currently a known broken link.

3. **Forward soft P_ω** — referenced in CLAUDE.md and Corridor Dynamics as load-bearing, but not formally constructed in the lake. The orthogonality theorem assumes its action on the CMB modes; a tight Lean statement of the operator would close the loop.

4. **Allen mouse cortex k_eff re-test.** The wave-2 datum is a chaos-pole observation pending re-test. The result determines whether F-10 keeps the corridor at this substrate or amends.

5. **Sensor-lift v3 and v4.** F-18 fires on the third PARTIAL-by-same-shape outcome. v3 and v4 land or close that handle.

6. **Memory file naming.** Two memory files retain "omega" in their slugs (`feedback_omega_no_hedging.md`, `project_ratchet_omega.md`) — content is consistent with the rename, slugs are not. Cosmetic; non-blocking.

---

*This document is the front door. Keep it in sync with the active paper, the lake, and the session ledger as the program evolves.*
