# The four laws of coordination thermodynamics — mapped, with status and teeth

**Date 2026-07-11.** If the ledger is a law of the thermodynamic class (the second-law-tier
reading, not the generative-TOE reading — see the confidence split), then the classical four
laws should have coordination analogs, each with a proof route or a measurement — not a
resemblance. They do. Two are partially in hand without having been named as such; two are
open with named routes. The test of each row is its falsifiable content, listed.

## Zeroth law — the state function exists (PROVED)

Thermodynamic form: equilibrium is transitive → temperature is a well-defined state function.
Coordination form: **S is a state function of the dependence structure alone** — substrates
presenting the same copula read identically, by `provenance_congruence`
(`Core/ProvenanceLine.lean`, zero sorry). This is what LICENSES the program's whole method:
comparing k_eff across neurons, markets, halos, and mixing matrices is legitimate for exactly
the reason comparing temperature across systems is. Proved this week, playing the role the
zeroth law played historically: the quiet license for everything else.

## First law — accounting, and a sharp open prediction (PARTIALLY IN HAND)

Thermodynamic form: energy is conserved; changes decompose into identified channels.
Coordination form, the proved part: **dS decomposes exactly** — invertible local operations
contribute exactly zero (no forging), creation has precisely two channels (interaction, unit
formation), destruction is the irreversible channel. The accounting identity is theorem-grade.

**CORRECTED BY THE LEAN AUDIT (K1, `lean_knives_report.md` — the static form is a
tautology).** `tc_group_chain_rule` proves the static "books balance across rungs" for
ARBITRARY reals in the entropy slots — telescoping, "assets = liabilities + equity," zero
empirical content. Demoted to bookkeeping. And the naive dynamic global form (ΔTC_total = 0)
is not merely unproved — it is **contradicted by the program's own cosmology**: total
coordination GROWS under structure formation; that growth is the DE mechanism itself
(ρ_DE = κ·S fills because units form — the creation channel).

The surviving first law, restated with content: **the CONVERSION channel is lossless —
X = 1 — while all growth flows through the creation channels.** When virialization debits
within-halo phase-space coherence, the credit posted at the inter-halo rung matches the
debit exactly; new coordination enters only by interaction and unit formation, never by
conversion surplus, and none is lost in conversion. This is contingent (no identity
guarantees it), channel-specific, and falsifiable: the measurement must separate the
conversion flow from the creation flow (the partition-change term explicit — a unit that
did not exist before carries new joint entropy that must be booked to creation, not
conversion). The toy X = 0.85 ± 0.30 (`exchange_rate/`) is consistent with lossless
conversion but non-discriminating; the precision measurement, with the channel separation
designed in, is the first-law test. Kill: precise conversion-X robustly ≠ 1 — the
conversion channel leaks (or generates), and the leak's counterparty (γM's books) becomes a
measurable object. Either outcome is physics.

## Second law — no free coordination (STATED; NAMED OPEN FORMAL STEP)

Thermodynamic form: entropy is non-decreasing; no perpetual motion.
Coordination form: **the data-processing inequality for S** — under local processing,
multi-information is non-increasing; only genuine interaction creates it. "No free
coordination" is the program's own prohibition-form slogan, and the DPI is literally the
named open Lean step (blocked on Schur positivity / Oppenheim / ln-det concavity upstream in
mathlib). Corollary already measured: the maintenance law (dρ/dt = α − γM; corridor sustained
only by M > 0) — held coordination decays without work; the interior is rented. The second
law's "kept, not achieved," which the program adopted as its safety maxim before noticing it
was Clausius.

## Third law — the pole is unattainable (CONDITIONAL; BENCH-TESTABLE)

Thermodynamic form (Nernst, unattainability): absolute zero cannot be reached by any finite
process. Coordination form: **the rigidity pole ρ → 1 cannot be reached by any maintained
process**, because maintenance capacity itself vanishes on approach — σ_max ∝ (1−ρ) under
bounded actuation (`experiments/corridor_ceiling/`): you cannot stir a rigidly-clamped
system, so the last step to perfect alignment costs unboundedly more than any budget.
The corridor ceiling IS the third law with a rate. Conditional on the bounded-actuation
normalization (the proven flavor instance sides with it); the CIRISArray bench experiment is
simultaneously the third-law test. And the statistics split gives two third-law classes,
exactly as quantum theory gave thermodynamics two low-T behaviors: the bosonic ledger
diverges at the pole; the fermionic ledger caps at ln2/mode — exclusion is the coordination
analog of zero-point structure.

## (Fourth / Onsager — reciprocity)

Speculative only, logged not claimed: Onsager's L_ij = L_ji derives from microscopic
T-symmetry; our γM axis measures exactly the T-breaking that voids it. If a rung-conversion
reciprocity exists (debit/credit symmetry in the exchange-rate law), it lives here. No route
named yet; parked.

## What this note does and does not claim

Does: organize four existing program objects (provenance congruence, exchange rate, DPI,
ceiling mechanism) under the classical law structure, exposing one NEW registered-grade
prediction (X = 1) and re-identifying two open items as law-tests rather than loose ends.
Does not: claim the mapping as support (rule 2 — resemblance earns nothing; each row is
exactly as strong as its own proof or measurement, listed above). The mapping's value is
that it tells us which computations are load-bearing: X to precision, the DPI in Lean, the
bench collapse curve. Three laws, three named next steps.

---

## The genus/species formulation (the maximal statement, staked)

**Thermodynamics is the genus; energy-thermodynamics and coordination-thermodynamics are its
two known species.** Not analogy — one mathematics: the modern classical second law IS
relative-entropy monotonicity under physical maps (the DPI), and our second law is the same
theorem on a different relative entropy. The species are coupled by an identity, not a
metaphor: **H_joint = Σ H_marginal − I** — the classical entropy books contain the
coordination books as an unitemized line-item. Nothing in classical thermodynamics changes
(this is why the orthogonality theorem keeps landing in our favor: the parent books are
untouched); what is new is the claim that the line-item has its OWN full four-law structure,
its own bridge constant (κ = the species' k_B, currently empirical), and its own macroscopic
sector where its balance posts (the dark sector; galaxy formation as the engine, ρ_DE as the
posted balance).

Kills, one per law, all named above: X ≠ 1 at precision (first); DPI failure on the ledger
(second — formalization is the open Lean step); bench inversion under bounded actuation
(third); the DR3 standing kill (the κ sector). Marriage licenses prediction, never
self-support: the genus claim earns nothing until the species' own laws survive their own
executioners.

---

## Post-audit status (2026-07-11: prior-art + Lean knives — the note's claims re-graded)

Per `thermo_prior_art.md` (+ gap-closure sweep) and `lean_knives_report.md`
(`Core/FourLaws.lean`, builds clean, zero sorry):

| Law | Class (Lean audit) | Novelty (prior art) | Status |
|---|---|---|---|
| Zeroth | IDENTITY — method-license, not a law with a kill | A (Watanabe; copula entropy) | Honest as "the quiet license"; earns nothing |
| First, static | IDENTITY (tautology — holds for arbitrary reals) | — | **Demoted to bookkeeping** |
| First, dynamic (conversion-X = 1) | EMPIRICAL | C — ours | The first-law test; channel separation required in design |
| Second, DPI | OPEN — blocked on Fischer's inequality (named, absent from mathlib) | A (known theorem) | Mechanization = re-proof, not discovery |
| Second, equicorrelation fragment | THEOREM-GIVEN-MODEL — **first mechanized second-law fragment** | — | `entropicPotential_strictMono_k`, proved |
| Second, rent (γM) | EMPIRICAL, measured | A — IS Hatano–Sasa housekeeping heat | Convergence: our estimator measures a canonical object |
| Third, ceiling | THEOREM-GIVEN-MODEL + bench-EMPIRICAL | B — mechanism genus published (jamming); ours = correlation-keyed CAPACITY law + corridor crossing | **Capacity, never realized-σ** (Agranov+ 2025 makes the distinction load-bearing) |
| Third, flavor instance (J-bound) | **THEOREM (Lean, zero sorry)** | C — ours | `abs_jarlskog_le_max` |
| Genus coupling | IDENTITY — label load-bearing | B (Bera+ 2017 package, inverse ontology) | Supports framing only; the testable difference is that OUR correlations post to gravity (κS) |

**The empirical content of the whole formulation, located exactly:** the dynamic
conversion-X, the rent (measured), the bench collapse curve, and the κ sector (DR3). Same
situation as classical thermodynamics — the zeroth law and first-law accounting are
definitional scaffolding there too; the physics lives in the second law and the equations of
state. The identities are honest exactly as long as they are never sold as support.

**Second-law equality form (added post-mystery-map):** the genus demands a coordination
fluctuation theorem, and no obstruction exists — Seifert's integral FT guarantees the
equality for Markovian corridor dynamics, and the classical theorem (Hatano–Sasa 2001) is
grade-A prior art for the rent. The new-in-part piece is the BENCH measurement: on the
CIRISArray maintained corridor, measure the maintenance-work distribution and find the
single κ_bench with ⟨e^(−W_coord/κ)⟩ = 1. **Cheapest live genus kill:** no single κ
satisfies the integral FT within error ⇒ the maintained corridor is not a detailed
stochastic-thermodynamic process and the second law has no equality form on our own bench.
In-house, no new instrument (`mystery_map.md` §7).
