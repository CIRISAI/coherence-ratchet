# Lean knives on the four laws — the tautology audit

**Date 2026-07-11.** The Lean pass on `four_laws.md`, run as the program's own
tautology-vs-commitment discipline demands: formalize what is provable, and for
each claimed "law" decide whether formalization exposes an IDENTITY (zero
empirical content — a kill for the law framing), a THEOREM-GIVEN-MODEL (proved
only inside a named model class), a genuine EMPIRICAL CLAIM (needs data; has a
kill), or an ILL-POSED statement. All Lean is in
`formal/CoherenceRatchet/Core/FourLaws.lean`, builds clean, zero sorry. Blocked
steps are recorded as named open records, never as sorry-free claims.

## Which knives came out clean, which drew blood

- **K1 (first-law tautology) — DREW BLOOD.** The static "the books balance across
  the rungs" reading is an algebraic identity. Demotion required.
- **K2 (coupling identity) — DREW BLOOD (as expected, and it was already labelled
  a candidate).** `H_joint = Σ H_marginal − I` is the definition of I rearranged.
  Confirmed identity; the genus claim earns nothing from it.
- **K3 (second law) — MIXED.** The general DPI is BLOCKED (Fischer's inequality
  absent from mathlib). But the equicorrelation fragment came out CLEAN and is
  now the first mechanized second-law fragment (theorem-given-model).
- **K4 (Jarlskog bound) — CLEAN.** Survived formalization as a theorem: |J| is
  capped by the mixing envelope and vanishes at the aligned pole.

## K5 — the tautology audit table

| Claim (four_laws.md) | Class | Lean object | Empirical content / kill |
|---|---|---|---|
| Zeroth: S is a state function of the copula (`provenance_congruence`) | **IDENTITY** | `ProvenanceLine.provenance_congruence` | None as a proposition; its role is *method-licensing* (a meta-claim), not a physical prediction. Honest as stated — it is explicitly "the quiet license," not a law with a kill. |
| First, static: "books balance across rungs" (TC decomposition) | **IDENTITY** | `tc_group_chain_rule` | **Zero.** Telescoping; holds for arbitrary reals in the entropy slots. Cannot be a law. **Demote.** |
| First, dynamic: X = 1 (coordination conserved under rung conversion) | **EMPIRICAL CLAIM** | (not an identity — see `firstLawDynamicContent` comment) | Content = ΔTC_total = 0 across the virialization epoch for the evolving partition. Kill: precise X robustly ≠ 1. Toy: X = 0.85 ± 0.30 (non-discriminating). |
| Second, DPI (general): multi-information non-increasing under local maps | **OPEN (blocked)** | `RestrictedSecondLaw` (named open step) | Needs Fischer's inequality det Σ ≤ Π det(blocks); absent from mathlib v4.14.0. Not proved; recorded as the single missing lemma. |
| Second, restricted: adding a coordinated unit doesn't decrease S | **THEOREM-GIVEN-MODEL** | `entropicPotential_strictMono_k`, `add_unit_increases_S` | Proved on the equicorrelation (Kish) family. First mechanized second-law fragment. Model-dependent (uniform ρ). |
| Second, rent: dρ/dt = α − γM, corridor sustained only by M > 0 | **EMPIRICAL CLAIM** | `Core.Dynamics` (existing) | Genuine. Measured (macaque motor cortex |z| = 8.8; galaxy baryon cycle z ≈ 0). Kill: detailed-balance-consistent maintenance. |
| Third, ceiling: σ_max ∝ (1−ρ), pole unattainable | **THEOREM-GIVEN-MODEL + EMPIRICAL** | K4 flavor instance below; bench test open | Conditional on bounded-actuation normalization. Kill: bench inversion under bounded actuation (CIRISArray). |
| Third, flavor instance: |J| ≤ J_max(angles), → 0 at aligned pole | **THEOREM** | `abs_jarlskog_le_max`, `jarlskogMax_zero_at_no_mixing`, `jarlskogMax_zero_at_max_13mixing` | Pure trig; no free parameters. Pins "coordination caps irreversibility" at Lean strength on the flavor sector. |
| Genus-coupling: classical books contain coordination books | **IDENTITY** | `coupling_identity`, `coupling_identity_gaussian` | Zero empirical weight. The coupling framing is honest ONLY when labelled an identity (which the note now must do). |

**Reading of the table.** Three of the "laws" (zeroth, first-static,
genus-coupling) are identities — bookkeeping, not physics. The program's actual
empirical content is located in exactly four places: the **dynamic** first law
(X = 1 conservation, needs restatement), the **rent** corollary of the second
law (measured), the **third-law bench** collapse (measurable), and the general
DPI (open, blocked on one missing mathlib lemma). A "law" column that is mostly
identities is not a defect *if labelled* — it is the same situation as classical
thermodynamics, where the zeroth law and the first-law accounting are also
definitional scaffolding and the physics lives in the second law and the
equations of state. The kill is only if the identities are *sold as support*.
They must not be (rule 2).

## Per-knife detail

### K1 — the first-law tautology knife (the sharpest)

`tc_group_chain_rule` proves, for a partition `grp : ι → κ` of variables into
groups and ARBITRARY reals `hMarg`, `hGroup`, `hTotal` in the marginal-entropy,
group-joint-entropy, and grand-joint-entropy slots:

    TCtotal = TCbetween + Σ_g TCwithin(g).

The proof is `Finset.sum_fiberwise` (each variable lies in exactly one group) plus
`ring` — telescoping of the group joint entropies. It uses no Gaussianity, no
determinant identity, and not even the fact that the numbers are entropies. This
is the decisive form of the knife: **an accounting relation that balances for any
numbers whatsoever has no empirical content.** It is "assets = liabilities +
equity," true by the definition of double-entry, not a law of economics.

Therefore the static first-law reading in `four_laws.md` — "a true first law says
the books balance across the rungs" — is a tautology and must be demoted. The
non-tautological first law is the DYNAMIC claim, stated precisely in the Lean
comment `firstLawDynamicContent`:

- The chain rule holds at every instant for the current halo partition, so
  ΔTC_total = ΔTC_between + Σ ΔTC_within.
- "X = 1" is exactly "ΔTC_between = −Σ ΔTC_within", i.e. **ΔTC_total = 0**: the
  total coordination of the matter field is conserved across the rung conversion.
- No chain rule guarantees this. Gravitational clustering generically GROWS total
  correlation (structure forms), so the naive global form is expected to fail.
  The honest claim is partition-relative: the coordination debited from
  within-halo phase space is credited, to within X = 1, at the inter-halo rung
  over the specific virialization epoch — with the partition-CHANGE term made
  explicit (a "unit" that did not exist before now carries a joint entropy).

**What must change in `four_laws.md`:** the first-law row must separate the
static identity (label it bookkeeping, no kill, no support) from the dynamic
conservation claim (the only falsifiable content), and must NOT phrase X = 1 as
though the accounting identity implies it. The exchange-rate computation is a test
of a contingent conservation law, not a consistency check of an identity — and
the naive global version has a known failure mode (structure growth) that the
measurement design must control for.

### K2 — the coupling identity

`coupling_identity`: with `I := (Σ marginals) − joint`, `joint = (Σ marginals) − I`.
Definitional. `coupling_identity_gaussian` ties it to the mechanized Gaussian
instance (`gaussianMultiInformation k ρ = entropicPotential k ρ / 2`, from
`EntropicPotential.lean`). The genus claim "the classical entropy books contain
the coordination books as an unitemized line-item" rests entirely on this
identity. It is TRUE and it is an IDENTITY: it supports the *framing* (the two
species share one mathematics) and earns *no empirical weight*. This is consistent
with `four_laws.md`'s own hedge ("coupled by an identity, not a metaphor") — the
audit just insists the word "identity" be load-bearing: an identity is exactly
what cannot be support.

### K3 — the restricted second law

- **General DPI: BLOCKED.** Subset-monotonicity TC(X_{A∪B}) ≥ TC(X_A) reduces, via
  the chain rule, to I(A;B) ≥ 0 for general Gaussian TC — equivalently Fischer's
  inequality det Σ ≤ Π_g det(principal block). mathlib v4.14.0 has no such lemma
  (`LinearAlgebra/Matrix/PosDef.lean` provides only `det_pos`; no Hadamard/Fischer
  determinant bound anywhere in the tree). Recorded as `RestrictedSecondLaw`, a
  named open record with the missing lemma named precisely. NOT claimed proved.
- **Equicorrelation fragment: PROVED.** `entropicPotential_strictMono_k` shows S is
  strictly increasing in the unit count k on the Kish family (dS/dk =
  −ρ/(1+ρ(k−1)) − ln(1−ρ) > 0, since −ln(1−ρ) > ρ ≥ ρ/(1+ρ(k−1))).
  `add_unit_increases_S`: S(k) < S(k+1). This is the first mechanized second-law
  fragment — adding a coordinated unit never decreases coordination — honest label
  THEOREM-GIVEN-MODEL (uniform ρ).

### K4 — the Jarlskog bound

`abs_jarlskog_le_max`: on the physical octant [0, π/2]³, |J| ≤ J_max(angles),
where J = c₁₂s₁₂c₂₃s₂₃c₁₃²s₁₃ sin δ and J_max drops |sin δ| ≤ 1.
`jarlskogMax_nonneg` supplies the envelope's nonnegativity;
`jarlskogMax_zero_at_no_mixing` and `jarlskogMax_zero_at_max_13mixing` show J_max = 0
at both ends of each mixing angle (θ → 0 and θ₁₃ → π/2) — CP violation lives only
strictly between the poles, the same corridor shape the program reads elsewhere.
The global tight bound |J| ≤ 1/(6√3) (optimizing cos²θ sin θ ≤ 2/(3√3)) is a
documented, not-yet-mechanized step (needs a one-variable calculus max); the
angle-dependent bound plus aligned-pole vanishing is what `four_laws.md` claims
and it is now a theorem.

## Bottom line for `four_laws.md`

1. **Demote the static first law** to a labelled identity; state the dynamic
   conservation (ΔTC_total = 0) as the sole falsifiable first-law content, with
   the structure-growth failure mode and the partition-change term explicit.
2. **Label the genus-coupling relation an identity** wherever it appears; it
   frames, it never supports.
3. **Second law:** report the equicorrelation fragment as proved and the general
   DPI as blocked on one named missing mathlib lemma (Fischer) — do not describe
   DPI as "the named open Lean step" as though it were nearly in hand; it is
   blocked upstream.
4. **Third law:** the flavor instance is now a theorem; keep the bench test as the
   empirical leg.
5. The empirical content of the whole "four laws" structure is exactly four
   items (dynamic X = 1, the rent corollary, the bench collapse, the open DPI).
   Everything else is scaffolding — legitimate, but scaffolding.
