# The Sakharov rung: baryogenesis conditions as ledger objects, and the one theorem-shaped thing the copula adds

**Date 2026-07-10.** Discovery-mode adjudication of the baryogenesis/Sakharov rung, kills
staked. Companion to `sm_escalator_map.md` (Rung 1, the flavor result), `dimensional_line_kB.md`
(the provenance line), and `experiments/sm_escalator_mixing/` (tonight's flavor read). The
ledger reads two things natively: dependence-shape (`S = −ln det C`, a copula functional,
amplitude-blind by clause 3) and irreversibility (detailed-balance breaking = the maintenance
term `γM`, Axis 2 of the two-axis discriminator; estimator validated on macaque motor cortex
|z|=8.8 and the galaxy baryon cycle z≈0). By CPT, **CP violation = T violation = microscopic
detailed-balance breaking** — the particle-sector instance of the `γM` axis. This note asks
what, if anything, that native read contributes to baryogenesis beyond textbook prior art.

Computation: `experiments/sakharov_ledger/jarlskog_bound.py` (seed 20260710), output
`jarlskog_bound.json`. Flavor numbers from `experiments/sm_escalator_mixing/results.json`.

---

## 1. The three Sakharov conditions as framework objects

Sakharov (1967): a dynamically generated baryon asymmetry requires (1) baryon-number
violation, (2) C and CP violation, (3) departure from thermal equilibrium. Map each onto the
framework and be precise about which have contentful readings and which are category errors.

**Condition 2 (C/CP violation) — CONTENTFUL, native.** CP violation is, by CPT, T violation,
which is microscopic detailed-balance breaking — literally the `γM` term, Axis 2 of the
two-axis discriminator. This is not an analogy: the quantity the framework built an estimator
for (forward-rate ≠ backward-rate on a correlation current) is the same quantity Sakharov's
condition 2 names. Tonight's Haar-percentile result is the framework's read of the *magnitude*
of this condition across the two flavor books (§2).

**Condition 3 (out-of-equilibrium) — CONTENTFUL, native.** The corridor is a *maintained
non-equilibrium*: `dρ/dt = α(ρ,S) − γM`, sustained only by `M > 0`. Condition 3 is precisely
this — the demand that the system be away from equilibrium so a microscopic asymmetry can
integrate into a net macroscopic posting. In full thermal equilibrium CPT forces zero net
baryon number *even with* CP violation; you need the drive. That is exactly the framework's own
structure: the `γM` axis produces a sustained net current only when both the irreversibility
capacity (condition 2) *and* the drive `M>0` (condition 3) are present. **Conditions 2 and 3
are the two halves of one framework object** — the maintained-non-equilibrium the program was
built around. This is the tightest structural echo in the note, and it is the program's own
dynamics, not an imported metaphor. Recognition weight (it re-expresses a known structure in
native terms; it derives nothing).

**Condition 1 (baryon-number violation) — NOT ledger-native; upstream provenance.** Baryon
number violation is a *selection-rule* fact: whether the state space admits a transition that
changes a conserved charge. By the provenance line (`dimensional_line_kB.md` §3, instance 3:
"statistics/state-space construction is input; the ledger reads only its consequences"), the
conservation laws and charge content of the state space are **input to** `C`, not read from it.
The ledger cannot see whether baryon number is violable — that is a fact about the allowed
transitions (in the SM: the electroweak sphaleron, tied to the `B+L` anomaly). Its mechanism
therefore lives in the **anomaly sector**, which `sm_escalator_map.md` Rung 2 already classed
as *recognition only, never derivation* (the double-entry balance echo `Tr Y = 0` etc.). The
one honest half-connection: the ledger's own balance discipline (debits = credits) is a
conservation law, so condition 1's *form* (you cannot post a net entry in a conserved quantity
without a number-violating transaction) echoes double-entry — but *which* charges are violable
is upstream, and any claim that the ledger derives baryon-number violation is confabulation-class.

**Verdict, Part 1:** two of three conditions have contentful native readings (2 and 3, jointly
the `γM` axis); condition 1 is upstream provenance whose mechanism sits in the recognition-only
anomaly sector. The split is not lucky — the two that map are the two about irreversibility and
drive (what the ledger reads); the one that does not is about charge/state-space structure
(what the provenance line forbids).

---

## 2. The honesty check: does the Haar-percentile framing add anything?

### 2a. The prior art (verified)

The textbook statement is that **SM (CKM) CP violation is too small for baryogenesis by
~10 orders of magnitude**. Verified chain:

- **Gavela, Lozano, Orloff, Pène**, *Standard Model CP-violation and baryon asymmetry (I:
  zero temperature)*, Nucl. Phys. B430 (1994) 345 (hep-ph/9312215; also Mod. Phys. Lett. A9
  (1994) 795); and **Gavela, Hernández, Orloff, Pène, Quimbay** *(II: finite temperature)*,
  Nucl. Phys. B430 (1994) 382 (hep-ph/9406289). `[verified]`
- **Huet, Sather**, *Electroweak Baryogenesis and Standard Model CP Violation*, Phys. Rev. D
  51 (1995) 379 (hep-ph/9404302): QCD damping reduces the CKM-sourced asymmetry to a negligible
  amount; rules out any electroweak baryogenesis using no new CP source. `[verified]`
- The standard dimensionless statement: the CP-violating measure built from `J` times the
  Yukawa mass factors gives a baryon asymmetry `η ~ 10⁻²⁰`, versus the observed `η ~ 10⁻¹⁰` —
  **at least ~10 orders short**. (`J` itself ≈ 3.0×10⁻⁵.) `[verified: multiple sources]`
- **Fukugita, Yanagida**, *Barygenesis without grand unification*, Phys. Lett. B 174 (1986) 45:
  leptogenesis — the lepton-sector asymmetry from heavy-Majorana decay, converted to `B` by
  sphalerons. `[verified]`

So "CKM CP violation is tiny and insufficient" is established prior art. The question is whether
our percentile framing (CKM `|J|` at the 0.09th Haar percentile, PMNS `|J|` at the 58th) adds
anything beyond re-expressing that known smallness.

### 2b. The one thing it adds: alignment ⇒ T-suppression is a THEOREM, with numbers

The Jarlskog invariant obeys the exact algebraic identity
`J = c₁₂ s₁₂ c₂₃ s₂₃ c₁₃² s₁₃ · sin δ`, so

> **|J| ≤ J_max(angles) ≡ c₁₂ s₁₂ c₂₃ s₂₃ c₁₃² s₁₃**, with global ceiling
> `J_max_global = 1/(6√3) ≈ 0.0962` (all mixing maximal), and `J_max(angles) → 0` as the
> matrix approaches any permutation (the maximal-coordination / maximal-MI points, which are
> real ⇒ `J = 0`).

This makes "aligned book ⇒ T-symmetric book" **theorem-shaped, not observed**: the mixing
angles alone *cap* the T-violation capacity, and the cap collapses to zero at the coordinated
(near-permutation) pole. Decompose each book's observed `|J|` into a **structural** factor set
by the angles (alignment) and a **chosen** factor set by the phase:

`|J|_observed / J_max_global = [J_max(angles)/J_max_global] · |sin δ|`

| book | J_max(angles) | structural = J_max(angles)/J_max_global | chosen = \|sin δ\| | δ | observed \|J\| |
|---|---|---|---|---|---|
| **CKM** (quark) | 3.38×10⁻⁵ | **3.5×10⁻⁴** | **0.910** | 65.5° | 3.08×10⁻⁵ |
| **PMNS** (lepton) | 3.34×10⁻² | **0.347** | **0.917** | −113.4° | 3.07×10⁻² |

The result is sharp and it is the note's core:

1. **CKM's T-symmetry is ~100% structural, not a chosen small phase.** CKM sits ~3500× below
   the global ceiling; of that, the angles (alignment) supply a factor ~2850 while the phase
   supplies ~1.1× — CKM's `δ = 65.5°` is *near-maximal* (`|sin δ| = 0.91`). The quark book is
   T-symmetric **because it is aligned**, not because it picked a small phase.
2. **The two books chose essentially the same (near-maximal) phase.** `|sin δ|` is 0.910 (CKM)
   vs 0.917 (PMNS). The phase is *not* where the books differ.
3. **The entire ~1000× CKM/PMNS asymmetry in realized CP violation is angle-driven.** Ratio of
   observed `|J|` = 996; ratio of `J_max(angles)` = 988 (structural); ratio of `|sin δ|` = 1.008
   (chosen). To three significant figures the asymmetry is 100% alignment, 0% phase.
4. **It is an ensemble law, not a two-point coincidence.** Across 200k Haar-random U(3):
   Spearman(MI, `|J|`) = **−0.72** (coordination ↑ ⇒ T-violation capacity ↓); mean `|J|` in the
   top-coordination (top-MI) decile = 0.0075 vs 0.073 in the bottom decile — a ~10× spread; and
   Spearman(distance-to-permutation, `|J|`) = +0.46. CKM and PMNS are the two tails of this law.

**So the Haar framing does add content, at recognition weight with a theorem behind it:** it
converts *two* facts about the quark book — "it is coordinated (99.98th-pct MI)" and "its CP
violation is tiny" — into **one** fact, via the `|J| ≤ J_max(angles)` bound: coordination
(comonotonicity of the two mass bases) *structurally suppresses* irreversibility capacity, and
anarchy maximizes it. That is a genuine unification of the two things the framework reads
natively (dependence-shape and irreversibility) under a single algebraic bound — not a new
physical prediction.

### 2c. What it does NOT add

It does not improve the baryogenesis bound, does not derive `J`, does not predict `η_B`, and
does not touch the "~10 orders too small" conclusion — that stands untouched as prior art. The
smallness of CKM CP violation is not *explained* by the ledger; it is *re-read* as structural
(alignment) rather than accidental (a small phase). Recognition, not derivation. The theorem is
real algebra; the physical smallness it re-describes was already known.

### 2d. The leptogenesis mapping: recognition, but NO new registered prediction

The reading "the imbalance posts from the anarchic (lepton) book" is contentful as recognition:
if a net asymmetry must post from CP violation, it must post from the book that *carries*
T-violation capacity — and by §2b that is the anarchic lepton book (`|J|` Haar-typical), never
the comonotone quark book (structurally T-symmetric). This lines up with prior art (CKM
insufficient; leptogenesis the leading source) and unifies "CKM too small" with "CKM is
coordinated" under one bound.

**But it does not add a registered prediction, and there is no clean joint kill.** The honest
subtlety: genuine high-scale leptogenesis (Fukugita–Yanagida) sources CP violation from the
*heavy* Majorana Yukawa phases, which are **not** the low-energy PMNS `δ`. Leptogenesis can
succeed with `δ_PMNS → 0`. Therefore:

- The DUNE/Hyper-K `δ` measurement (already the registered fork in `sm_escalator_mixing/`)
  tests **our anarchy read** of the low-energy PMNS book — `δ → CP-conserving` kills the
  Haar-typicality of leptonic `|J|` — but it does **not** kill leptogenesis.
- The hypothesized joint kill ("`δ` CP-conserving AND no other asymmetry source ⇒ both die")
  is real only for a *naive low-energy-CP* leptogenesis reading, which is not the mechanism.
  High-scale leptogenesis survives `δ_PMNS → 0`. So no new joint falsifier exists.

**Verdict 2d:** the leptogenesis mapping is a recognition-weight reframe with no independent
registered prediction beyond the already-staked DUNE `δ` fork — and that fork tests our anarchy
reading, not leptogenesis. State the reframe; claim no new prediction.

---

## 3. η_B = 6.1×10⁻¹⁰ — FORBIDDEN target (amplitude/count-native, and upstream)

Run through the second cut (`sm_escalator_map.md` §1). `η_B = n_B/n_γ` is dimensionless, so it
passes the coarse filter. But it is **not** dependence-native: it is the *size* of the net
baryon posting per photon — an amplitude, a total count, not a coupling between two bases. By
clause 3 the copula is amplitude-blind; it strips `η_B` for the same reason it strips `κ`,
masses, and the magnitude of `ρ_DE`. **Doubly disqualified:** `η_B` is also *upstream* — its
value is the integrated outcome of the full out-of-equilibrium dynamics (conditions 1+2+3 over
the expansion history), which the provenance line forbids the ledger from sourcing. The
framework can read the *character* of the T-violation (the Haar percentiles, the alignment
bound) but not the *magnitude* of the asymmetry it produces. `η_B` is a well-posed physical
number and a **forbidden ledger target — reject on sight** under the standing rule.

---

## 4. θ_QCD — no, and the honest one-paragraph close

`θ_QCD < 10⁻¹⁰` is the most extreme CP-conservation fact in physics. Despite being a "phase"
(and so borderline-dependence in the map's Rung 8), it is **not** a coupling between two
identified bases the way CKM/PMNS are — it is a single vacuum angle, the coefficient of `GG̃`, a
marginal/one-dimensional parameter. Its *value* (the smallness) is the strong-CP problem,
addressed by axions / Peccei–Quinn, and is upstream of any correlation matrix. The §2b machinery
does not even apply: there is no two-basis mixing whose alignment could be read. The tempting
move — "the QCD vacuum is maximally coordinated, hence T-symmetric, hence `θ ≈ 0`" — is
confabulation-class (cf. the "entropy selects SU(3)×SU(2)×U(1)" debunk); `θ_QCD = 0 ⇒`
CP-conserving is definitional, not a derivation of *why* `θ` is small. **The ledger has nothing
non-confabulated to say about strong-CP. Closed.**

---

## 5. Kills staked (dated debts)

- **The alignment ⇒ T-suppression theorem (§2b) is not a prediction about the world; it is an
  internal unification.** It "dies" as *content* only if the algebra is wrong (it is not —
  `|J| = (angle product)·sin δ` is an identity) or if the Haar ensemble law reverses on a
  better construction (Spearman flips sign) — recorded for completeness, no realistic path.
- **The anarchy read of the lepton book dies** on the already-registered DUNE/Hyper-K fork:
  `δ_PMNS → CP-conserving` sends leptonic `|J|` to percentile ~0 and collapses the anarchic
  half (`sm_escalator_mixing/`). This note adds **no** new falsifier — and explicitly records
  that this fork does **not** test leptogenesis (§2d).
- **η_B and θ_QCD are closed as ledger targets** (§3, §4): any future document sourcing `η_B`
  from `S`, or deriving `θ_QCD`'s smallness from coordination, is confabulation-class and
  rejected on sight.

## Executive summary

- **Sakharov conditions:** 2 and 3 (C/CP violation and out-of-equilibrium) map contentfully and
  natively — jointly they *are* the framework's maintained-non-equilibrium `γM` axis (CP = T =
  detailed-balance breaking; the drive `M>0` is condition 3). Condition 1 (baryon-number
  violation) is upstream provenance; its sphaleron mechanism sits in the recognition-only
  anomaly sector.
- **The (2a) verdict:** "aligned book ⇒ T-symmetric book" **is theorem-shaped** — `|J| ≤ c₁₂
  s₁₂ c₂₃ s₂₃ c₁₃² s₁₃`, vanishing at the coordinated pole. CKM's T-symmetry is **~100%
  structural** (angles), **not** a chosen small phase (its `δ = 65.5°` is near-maximal,
  `|sin δ| = 0.91`); the ~1000× CKM/PMNS CP asymmetry is 988/996 alignment, ~0% phase; and it is
  a Haar ensemble law (Spearman(MI, `|J|`) = −0.72). This unifies "CKM is coordinated" with "CKM
  CP is tiny" into one fact — recognition weight, real theorem, no new physical prediction.
- **Leptogenesis:** contentful reframe (asymmetry posts from the T-violation-carrying anarchic
  book) but **no new registered prediction** and **no joint kill** — high-scale leptogenesis
  survives `δ_PMNS → 0`, so the DUNE `δ` fork tests our anarchy read, not leptogenesis.
- **η_B:** forbidden ledger target — amplitude/count-native (clause-3 stripped) and upstream.
- **θ_QCD:** the ledger has nothing non-confabulated to say. Closed.

## References

All verified this session (title + venue/arXiv):
- M. B. Gavela, M. Lozano, J. Orloff, O. Pène, *Standard Model CP-violation and baryon
  asymmetry (I)*, Nucl. Phys. B430 (1994) 345, hep-ph/9312215. `[verified]`
- M. B. Gavela, P. Hernández, J. Orloff, O. Pène, C. Quimbay, *(II) finite temperature*,
  Nucl. Phys. B430 (1994) 382, hep-ph/9406289. `[verified]`
- P. Huet, E. Sather, *Electroweak Baryogenesis and Standard Model CP Violation*, Phys. Rev. D
  51 (1995) 379, hep-ph/9404302. `[verified]`
- M. Fukugita, T. Yanagida, *Barygenesis without grand unification*, Phys. Lett. B 174 (1986)
  45. `[verified]`
- A. D. Sakharov, *Violation of CP invariance, C asymmetry, and baryon asymmetry of the
  universe*, JETP Lett. 5 (1967) 24 — the three conditions. `[standard, not re-verified this
  session]`

Internal: `sm_escalator_map.md` (Rung 1 flavor result, Rung 2 anomaly recognition),
`dimensional_line_kB.md` (provenance line, clause-3 amplitude-blindness),
`experiments/sm_escalator_mixing/` (Haar flavor read), `experiments/sakharov_ledger/`
(this note's `|J|`-bound computation).

---

## Orchestrator sideways pass (2026-07-10): the negatives stand; the J-bound may be the corridor ceiling's mechanism

The note's negative verdicts are accepted (η_B forbidden, θ_QCD closed, no new leptogenesis
kill — the high-scale subtlety is correct). Two positive remainders the baryogenesis vantage
could not see:

**1. The J-bound is the flavor-space instance of a candidate GENERAL theorem — and the general
version would explain the corridor's upper edge.** The note proves (flavor case): coordination
structurally caps irreversibility capacity (|J| ≤ J_max(angles) → 0 at the comonotone pole;
ensemble law Spearman(MI,|J|) = −0.72). The general form: detailed-balance breaking requires
cyclic probability currents; currents need ≥ 2 effective dimensions; as ρ → 1, k_eff → 1 and
the effective state space collapses — so **entropy-production capacity vanishes at the rigidity
pole**: σ_max = f(k_eff), f(1) = 0. But the corridor is *sustained only by* M > 0 (piece 2,
`Core/Dynamics.lean`). If coordination structurally starves the very maintenance current that
sustains it, then **the corridor's upper boundary (ρ ≈ 0.43) is where maintenance capacity
falls to maintenance demand** — coordination beyond the ceiling is unmaintainable not by
accident but by theorem. This would be the first mechanistic derivation of the 0.43 ceiling —
currently an empirical constant (piece 3) — and it unifies Axis 1 (structure) and Axis 2
(maintenance), previously treated as independent, into one inequality: the axes are not
independent; structure BOUNDS maintenance capacity.

**Test on data in hand:** the `keff_saturation` catalog holds both spectra (k_eff) and the
validated detailed-balance estimator per substrate. Prediction: measured |z_DB| capacity
declines toward the rigidity pole; coordinating substrates cluster where σ_max(k_eff) is still
comfortably above their maintenance demand; nothing coordinating sits near ρ → 1. A quantitative
f(k_eff) fit against the corridor's measured edge is the confirmation target; a coordinating
substrate found stable at ρ ≫ 0.43 with high measured σ kills it.

**2. Phase genericity extends Haar-typicality to BOTH books.** |sin δ|_CKM = 0.910,
|sin δ|_PMNS = 0.917 (ratio 1.008): both books run near-maximal phases; coordination lives
entirely in the angles. Under uniform phases this is unsurprising per book (P(|sinδ| > 0.9) ≈
0.29) and mildly cute jointly (~few %) — suggestive tier only, logged, not support. The clean
statement: **dependence *strength* is book-specific; dependence *orientation* is generic in
both books.** Shadow expectation: any future mixing sector arrives with a generic phase.

*(Sideways pass by the orchestrator; the corridor-ceiling conjecture is staked here as a dated
research target, not a result — its Lean-shaped form is σ_max = f(k_eff) with f(1) = 0 joined
to dρ/dt = α − γM.)*

---

## Correction flag (2026-07-11, from the rigor pass): the PMNS "chosen factor" is δ-fragile

The rigor pass caught a stale parameter: the frozen mixing run used δ_PMNS = −1.98 rad, but
current NuFit-6.0 best fits are 212° (with SK) / 177° (without SK). The |sin δ| "chosen
factor" for the lepton book therefore ranges ~0.05–0.53 at current best fits, not the 0.917
computed from the stale value. **Demotions, applied:** (1) the "both books picked the same
near-maximal phase (ratio 1.008)" observation is δ-fragile and drops to curiosity-pending-DUNE;
(2) the phase-genericity claim in the earlier sideways pass §2 is likewise demoted for the
lepton book. **What is untouched:** the J-bound identity, the CKM decomposition (its δ is
well-measured), the structural factors, and the ensemble law. **The cleaner statement that
replaces the demoted one:** structure = CAPACITY (measured, robust: the anarchic book carries
~1000× the quark book's T-violation capacity); phase = USAGE (poorly measured — exactly the
registered DUNE/Hyper-K fork, which this correction sharpens: near-CP-conserving δ = 177° is
inside the current 1σ conversation, so the |J|→0 kill sits nearer than the frozen numbers
implied). Leptogenesis reading unchanged in kind: the imbalance had to post from the book
with the capacity; whether the low-energy phase reflects the usage is the fork.
