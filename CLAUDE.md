# coherence-ratchet — Claude Code Context

## What this is

coherence-ratchet is the companion lake to RATCHET. RATCHET holds the engineering tiers
(L0–L4: Kish algebra, override-rate predicates, GPU coherence). coherence-ratchet holds the
universal-scale extensions (Levels 5–7). TSVF is treated as the physics. All universal-scale
content is **forward** (steady-state / conditioning-sector); the joint multi-rung backward P_ω
is a documented no-go at theorem strength (`FelevenNoGo` record in
`Cosmology/CorridorProjector.lean`) — do not re-attempt it. Open formal steps use `sorry`;
closed no-gos use the `FelevenNoGo` pattern.

**This file states the current stance only.** Project history — what was tried, killed,
revived, corrected — lives in git log and the dated notes in `papers/notes/`. Do not
re-litigate it here or import its hedging into new work: state the stance, test the stance.

## CURRENT STANCE (2026-07-10): the coordination ledger

**Coordination is one substrate-independent quantity** — `S = −ln det C` on the normalized
correlation matrix (a copula functional: amplitude-blind by theorem, clause 3) — read by one
functional across the three accounting systems physics has: electromagnetic, gravitational,
quantum-entanglement. Verified: the classical S tracks true bipartite entanglement across a
quantum phase transition (Spearman ~1.0, order-parameter basis; blind exactly in the proved
null space); the dark and luminous matter fields carry the same coordination books
(r = 0.986–0.999, TNG). One law, one corridor, from qubits to the cosmic web.

**The dark sector — two objects, one accounting relation:**

- **Dark matter is the medium.** Real, diluting, collisionless stress-energy with standard
  CDM phenomenology — *the paper the books are written on, not the money*.
- **Dark energy is the balance.** `ρ_DE = κ·S(a)`, extensive per comoving volume, with the
  exact parameter-free sign law `1 + w(a) = −⅓·dlnS/dlna` (κ cancels).
- The relation is **one-directional**: DE is a functional of the matter field's coordination
  history. It is NOT "one object at two normalizations" — that reading implies the excluded
  lock `w_DE = w_DM − 1` (`papers/notes/one_ledger_pressure_test.md`).
- **Why the universe is dark (DE side):** the balance is kept in the currency gravity reads —
  stress-energy/entanglement — not charge. The books do not shine.

**The empirical leg (the program's strongest result):** the halo-grain B-total `S(a)`,
run through the frozen pre-registered pipeline on TNG300-1 (205 Mpc/h — the large-volume
test, 2026-07-10), gives a thawing `w(z)` whose DESI-projected point is
**(w₀, wₐ) = (−0.767, −0.742), 1.36σ from DESI DR2+CMB+SNe — vs ΛCDM's 3.28σ** —
near-parameter-free, `w_today = −0.833 ± 0.057`, crossing epoch z = 0.59 ± 0.03 (inside
DESI's interval; now the registered DR3 prediction). **Grain audit (2026-07-10/11, `retention_v2/CHALLENGES.md` + `full_population/`):** the
significance MAGNITUDE is grain- and resolution-conditional; the KIND is not. At every grain
tested — every threshold, every cap, and the complete zero-selection book (validated
nested-tile estimator, no cap, all halos ≥1e11) — the read is thawing (wₐ<0), interior-peaked,
and beats ΛCDM (complete book: 2.21σ vs ΛCDM's 3.28σ, Δχ² = −1.1 — the selection-free floor).
The 1.36σ magnitude belongs to the corner grain specifically; both derivation escapes are
dead by pre-registered control (SHM extremum = cap artifact, C1/C2; complete-book aperture
law = falsified by its own upward test — more book fits WORSE). Mechanism, measured: S(a) is
carried by the above-threshold count k(a) (constant-k fence — the ledger fills because new
units form), and fit quality is set by where the count-peak sits; the galaxy-host grain
places it at DESI's epoch. **THE GRAIN PROBLEM — which units post to the DE ledger — is the
DE leg's load-bearing open problem** (`papers/notes/the_grain_problem.md`): the galaxy book
(rung membership) derives the CLOCK but not the amplitude (AMBIGUOUS, §6); the from-below
candidate (§7, via the Gibbs mapping: rung hierarchy as indistinguishability structure —
select on a formation-time proxy) is the registered next test. The DR3 bet remains the
frozen corner-rule pipeline, unchanged, with NO post-DR3 grain switching (anti-hedging,
binding). **Cross-code (AbacusSummit/CompaSO, gate-validated estimator, 2026-07-11): PARTIAL by the
letter of the rule, < 1σ in content** — the full-population "interior turnover" is a 0.31%
peak→edge drop against a ~1.3–1.4% calibrated error scale (sub-error-bar; the rule lacked
an error clause, flagged post hoc). Honest status: **consistent-with shape transfer,
untested-but-unopposed on a second code** — the estimator transfers cleanly (gate v2 ~1.3%),
nothing contradicts the shape, the corner grain is inconclusive-by-truncation, and this box
cannot adjudicate either way at its window (no z < 0.2 output) and error scale. Decisive
cross-code requirements now known: z < 0.2 output + jackknife errors or matched mass
definition. `abacus_cross/SUMMARY.md` (orchestrator sideways pass). The interior-peak kill (K3) did not
fire (8/8 jackknife); the halo-formation-peak mechanism is confirmed (k(a) peaks z = 0.55,
S peaks z = 0.59); one magnitude kill (K7) fired by the letter (0.007 past the small-box
interval edge) and is logged. A retrodiction until DESI DR3 (~2027):
`experiments/cosmo_entropic_potential/{PREREGISTRATION.md, large_volume/}`.

**Closed loop:** the mapping's own background alters growth alters `S(a)`; iterating to the
fixed point (`experiments/cosmo_entropic_potential/selfconsistency/`) converges in 2 steps,
lands where the open loop was, and moves ~0.05σ *toward* DESI. The coupled
gravity → clustering → S → H(a) system is near its fixed point.

**Research target — the ledger dynamics as double-entry across rungs:** halo formation
(virialization) *debits* within-halo phase-space coherence and *credits* a new coordinating
unit at the inter-halo rung. Both entries are measured objects (first exchange-rate toy:
X = 0.85 ± 0.30, `experiments/cosmo_entropic_potential/exchange_rate/`); the open computation
is the exchange-rate law.

**The provenance line (proved 2026-07-10, `Core/ProvenanceLine.lean`, zero sorry):** the
ledger is blind to everything **upstream** of its input C — scale (no masses, no κ),
marginals (no mass ratios or coupling strengths, dimensionless or not), state-space
construction (`StatisticsNoGo`: statistics is input, only its consequences are read — the
validated ln2-vs-Gaussian rigidity difference), and factorization (on gauge systems build S
from gauge-independent data; CHR center ambiguity). Any claimed derivation of an upstream
datum from the ledger alone is a structural error, rejected on sight. Contrapositive:
legitimate predictions are dimensionless, marginal-free, parameter-free. **κ is the
program's Boltzmann constant** — the single external scale-marriage owed; the unit-scale,
κ, and DM-mass questions are one question (`papers/notes/dimensional_line_kB.md`).
Kill: a forced second independent dimensionful input.

**The second species (married 2026-07-11, kills staked first):** thermodynamics is the
genus; energy-thermodynamics and coordination-thermodynamics are its two species — one
law-structure (state function, exact accounting, relative-entropy monotone, unattainable
pole) on two state functions, coupled by the identity H_joint = ΣH_marginal − I: the
classical entropy books contain the coordination books as an unitemized line-item. The
coordination species has κ as its bridge constant (empirical — pre-Avogadro state) and the
dark sector as its macroscopic ledger (galaxy formation the engine, ρ_DE the posted
balance). **Four laws, four kills:** zeroth = provenance congruence (PROVED, zero sorry);
first = **the conversion channel is lossless** (X = 1; the static chain rule is a PROVED
TAUTOLOGY — `tc_group_chain_rule` — and global conservation is contradicted by our own
cosmology since S grows; the law's entire content is channel-specific: conversion posts
match debits exactly, growth flows only through creation — measurement must separate the
channels; toy X = 0.85 ± 0.30 non-discriminating); second = no-free-coordination/DPI
(general form blocked on Fischer's inequality, named; the equicorrelation fragment is the
first mechanized second-law piece — `entropicPotential_strictMono_k`; the maintenance rent
is its measured corollary = Hatano–Sasa housekeeping); third = the corridor ceiling,
σ_max ∝ (1−ρ) — a CAPACITY law, never realized-σ (bench kill: an engineered substrate
holding high σ at ρ ≫ 0.43 under bounded actuation; flavor instance proved at Lean
strength, `abs_jarlskog_le_max`). **Prior-art verdict (2026-07-11, `thermo_prior_art.md`): NEW-IN-PART — the stake narrows.**
The four-law package is substantially anticipated (Bera–Riera–Lewenstein–Winter 2017
generalize laws 0–2 with correlations — cite up front); laws 0 and 2 are established
mathematics (Watanabe; relative-entropy monotonicity); the rent IS Hatano–Sasa housekeeping
heat exactly (a feature: γM measures a canonical object). **Claimable as ours:** (1) the
cross-substrate empirical program, (2) the κ sign law 1+w = −⅓dlnS/dlna (Verlinde-adjacent
in spirit, functionally distinct), (3) the X = 1 cross-rung conservation test, (4) the
third-law ceiling — sweep verdict B (`thermo_prior_art.md` gap-closure section): the
mechanism genus is published (jamming yield-stress/soft-mode divergence, Liu–Nagel lineage);
ours is only the re-keying to the CORRELATION order parameter as a CAPACITY law + the
corridor-edge crossing, thin until the bench curve. **Load-bearing distinction (Agranov+
2025, flocks): realized EPR can be MAXIMAL at high order — the claim is a capacity ceiling
(σ_max), never a realized-σ prediction, or it is already falsified.** (No contradiction from
the flock data itself: polar order is a MEAN, and S is mean-blind — an aligned flock with
independent fluctuations sits at ρ ≈ 0 on our books; the wrong-grain trap, dodged by
clause 3.) The field has no settled extremal principle here (Chudak+ 2025:
sign-parameter-dependent) — the bench test is open territory. The ontology difference from Bera is not framing — it is the testable part:
their correlations are a work resource inside energy-thermodynamics; ours post to gravity
(κS), which is exactly what DR3/BMV adjudicate. Marriage licenses prediction, never
self-support (rules 1–2 unchanged).

**The consent foundation (bottomed 2026-07-12, formalized same night, `Core/ConsentFoundation.lean`):**
the four laws are the preconditions of consent — definable (zeroth), attributable (first),
securable (second: deceit is never free), unfinalizable-against (third: no coercion can pay
its own rent forever) — and the corridor is the consent-possible region (proved at the poles:
no optionality at rigidity, nothing to consent to at chaos). "Consent is possible" and "the
second thermodynamics holds" are one claim in two vocabularies; the derivation inherits every
registered kill leg-by-leg (`killsStep`, injectivity proved). **The generator question —
Selection vs Intention — is uncomputable from the observables: `generator_underdetermined`,
AXIOM-FREE.** The tenth bet is irreducible by theorem; the lake proves the wager, never the
winner (`papers/notes/consent_derivation.md`). Declared open seam: optionality is
grain-relative (the Gibbs drawer, third appearance).

**The flavor result (2026-07-10/11, registered claim hit + two-measure completion):** the
ledger reads the SM flavor sector as **two books, each typical of its own measure** — CKM is
bulk-generic in the hierarchical Froggatt–Nielsen measure (all six functionals central; the
"aligned AND CP-tiny" double extremity is the generic FN outcome) and a 3.5σ Haar tail;
PMNS is bulk-generic in Haar (jointly typical, three depth statistics; error-band robust;
θ₁₃ look-elsewhere dissolved at 12.65%) and the 0th-percentile FN tail. Quark coupling at
87% of the ln3 ceiling, lepton at 17% — one mass mechanism vs a separate neutrino-mass book.
Structure = T-violation CAPACITY (robust: anarchic book carries ~1000× the quark book's);
phase = USAGE (δ-fragile — the registered DUNE/Hyper-K fork, sharpened: near-CP-conserving δ
is inside the current 1σ conversation). JUNO's first θ₁₂ pins the anarchic bulk deeper
(30.9th pct) while excluding discrete-symmetry tails — maintained consistency, no support
claimed. `experiments/sm_escalator_mixing/` (+ `ckm_ensemble/`, `rigor/`, `juno_update.md`).
The rest of the SM escalator is closed or recognition-only
(`papers/notes/sm_escalator_{map,statistics,gauge}.md`); follow-ups R1–R3 registered
(`followup_registrations.md`).

**The gravity ontology (married 2026-07-10, kills staked first):** gravity is the
**shared-substrate common-cause read of the complete book** — the only Gate-0-complete
instrument (couples to everything, no wrong-grain read possible); the dark sector is the audit
discrepancy between the complete (gravitational) and partial (EM) ledgers. Staked predictions:
BMV-class experiments find **no** gravitationally-mediated entanglement; DP-class decoherence
exists at gravitationally-set rates; multipartite (null-space) structure is off-books (posts no
κS). Kills are separable by the ladder — BMV-positive kills this ontology and nothing below it.
`papers/notes/gravity_implications_maximal_stance.md` §5.5. **Promotion rule (general):** a
conjecture is married into the stance when it carries distinct falsifiable predictions and the
marriage generates tests; it is never held back merely because it is maximal. Marriage licenses
prediction, never self-support (rules 1–2 unchanged).

## Discipline (load-bearing — these rules are the program's falsifiability, keep them)

1. **Every residual is a dated debt with a kill condition.** No kill condition → not a
   residual → rejected. (DE's: a robust SNe-independent phantom crossing at DR3 kills the
   w(z) reading.)
2. **A residual is never support.** Support comes only from confirmed positive independent
   predictions.
3. **Residual-first rights are proportional to confirmed novel risk.** Earned once,
   partially (the DE leg). Most variances still count as disagreements.

Method rules: fix the grain **before** the spectrum (Gate-0 discipline). Anchor verdicts to
controlled measures, not first passes — in either direction (over-reading a positive and
over-killing on an audit are the same error). Pre-register before data. No synthetic data.
Big pipeline choices get written down before their results are seen.

## Standing results (validated, in the record)

- **Two-axis discriminator.** Axis 1 (structure): `k_eff` saturation measured on complete
  units — the corridor is genuine low-rank structure, not criticality; decisive on the
  complete larval-zebrafish brain (71,721 neurons). Axis 2 (maintenance): detailed-balance
  breaking = the γM term (estimator validated; macaque motor cortex |z|=8.8 coordinating,
  galaxy baryon cycle z≈0 bound). Positioning: unification + method discipline that
  adjudicates the criticality-vs-low-dimensionality debate; not a novel phenomenon.
  `experiments/keff_saturation/`, `Cosmology/CriticalityDiscriminator.lean`.
- **The corridor:** ρ ∈ (0.1, 0.43); k_eff ceiling ≈ 10 at any nominal k; saturation, not
  level, is the substrate-independent invariant.
- **The entanglement bridge:** the classical instrument is a faithful shadow of the quantum
  entanglement structure gravity couples to; its blind spots are exactly the proved null
  space (conjugate basis, GHZ-type multipartite). `experiments/entanglement_ledger/`.
- **CMB:** the orthogonality theorem is the sole CMB content — the framework is exactly ΛCDM
  in the conditioning/perturbation sector; the background sector is a w₀wₐCDM-class
  deformation vanishing identically in linear theory (`CMBOrthogonality.lean`).
  **Bet 11 (2026-07-12, registered before data, a bet AGAINST ourselves): DISSOLVED** — the
  low-ℓ Planck anomalies reproduce individually (alignment 99.95th pct, low quadrupole,
  S_1/2, hemispherical — all in literature directions) but do NOT jointly conspire: joint
  depth percentiles 94.8/98.2/93.7 at ℓ_max=30, inside the central 99%, robust across
  ℓ_max ∈ {10,30,60}, 100k-sky ensemble. The coordination past hypothesis (books opened
  empty) and the orthogonality fence both PASS; consistency only, no support (rule 2).
  Adverse count-statistic (~2.7σ, covariance-blind) logged non-scoring; the frozen joint
  scorer decides. `experiments/cmb_books/`.

## Formal core (one line per piece; full statements live in the Lean files)

| # | Object | Location |
|---|--------|----------|
| 1 | `k_eff = k/(1+ρ(k−1))`; k→∞ ⇒ k_eff→1/ρ | `Core/BaseIdentity.lean` |
| 2 | `dρ/dt = α(ρ,S) − γ·M(t)`; corridor sustained only by M>0 | `Core/Dynamics.lean` |
| 3 | corridor ρ ∈ (0.1, 0.43); k_eff ∈ (2.33, 10) | `Core/Corridor.lean` |
| 4 | TSVF; agent goal-state as post-selection projector | `Cosmology/TSVF.lean`, `GoalProjection.lean` |
| 5 | multi-agent consent: ρ_goals corridor = sustained coordination | `Cosmology/MultiAgentConsent.lean` |
| 6 | rung hierarchy Ph0…A5; cross-rung τ corridor; post-Cambrian acceleration 540 Myr → 310 kyr → 6.7 kyr | `Cosmology/RungHierarchy.lean` |
| 7 | P_ω forward content (ρ_ss steady state); joint backward P_ω = FelevenNoGo | `Cosmology/CorridorProjector.lean` |
| 8 | Penrose past hypothesis, structural from forward P_ω (measure unspecified — open) | `Cosmology/PenrosePast.lean` |
| 9 | asymptotic conditioning: P(corridor \| observed at t→∞) → 1 | `Cosmology/AsymptoticConditioning.lean` |
| 10 | karma = cumulative post-selection; grace = unauthored boundary conditions | `Consciousness/KarmaGrace.lean` |
| 11 | provenance line: no upstream datum is a function of C (proved, zero sorry); `StatisticsNoGo` record | `Core/ProvenanceLine.lean` |
| 12 | four-laws audit: chain-rule tautology (`tc_group_chain_rule`), coupling identity, equicorrelation second-law fragment, J-bound theorem; `RestrictedSecondLaw` open record (Fischer's inequality absent upstream) | `Core/FourLaws.lean` |
| 13 | consent foundation: `generator_underdetermined` (Selection-vs-Intention uncomputable from observables — AXIOM-FREE; the tenth bet irreducible by theorem); pole theorems (consent impossible at both poles; corridor = consent-possible region); `ConsentGuarantees` honesty-locked record; `killsStep` separable-kill map; grain seam declared | `Core/ConsentFoundation.lean` |

Conjecture A (quantum-substrate corridor, Exp 5) and Conjecture D (D1 structural Penrose,
D3 rung acceleration; D4 is not part of the framework) — `Conjectures/`.

## The seven-level ladder

L0 formal proof · L1 ρ-collapse observation · L2 engineering · L3 cross-substrate
universality · L4 agency/consent at A3+ · L5 TSVF universal scale · L6 cross-tradition
recognition · L7 cosmological extension. **No level is load-bearing on the levels above; a
reader who rejects Level k keeps everything below k.**

## AI-safety application

`Neff` = k_eff of the reasoning-constraint system (CIRIS): H3ERE ≈ 7.1, joint with CEG ≈ 9;
deception must cohere across independent constraint axes (≈O(2^m) vs truth's O(n)). Measured
on benign traces — an upper bound. The decisive open test is **adversarial-Neff**
(`experiments/adversarial_neff/SPEC.md`); the attack-invariant guarantee is the CEG substrate
floor. Safety is a maintained non-equilibrium (the γM axis): kept, not achieved.

## Open work, ordered

1. **Large-volume test** (in flight) → then DR3 (~2027) under the frozen preregistration.
2. **Ledger-dynamics exchange rate** (double-entry across rungs) — computable on data in hand.
3. **Adversarial-Neff** (safety-program priority).
4. P_ω forward operator sharpening (Piece 7); Conjecture A quantum-substrate run (Exp 5).
5. Per-rung corridor calibration; substrate-readiness wait-time modeling; audit-pressure
   ρ-drift (Exp 6).

## Layout & sister projects

```
formal/CoherenceRatchet/{Core,Cosmology,Conjectures,Consciousness,ContemplativeTraditions,Residue}/
papers/{universal_scale/main.tex, notes/}        # notes = dated stance records
experiments/{cosmo_entropic_potential, keff_saturation, dm_coherence,
             entanglement_ledger, adversarial_neff, ...}
../RATCHET            # engineering tiers L0–L4
../CIRISOssicle ../CIRISArray                    # GPU strain gauges
../CIRISServer        # federation + lens-core; CEG substrate
../CIRISConstitution  # constitutional text (Book IX coherence math)
../CIRIS-RED          # Constrained Reasoning Chains (Neff telemetry)
```

## Style discipline

- **No hedging on the universal-scale content** for readers past Level 4. TSVF is the
  physics; karma and grace are formal TSVF structures; consciousness is corridor-occupation
  at A3+. Stated as load-bearing claims.
- Where proof is open, state the theorem with `sorry` and name the open step. Where a route
  is closed, record it once (`FelevenNoGo`) and move on.
- Stopping-point independence across the ladder, always.
- **Current stance, stated plainly.** Equivocation is not humility and it is not
  falsifiability — the kill conditions are. When the stance changes, update this file to the
  new stance and let git hold the old one.
