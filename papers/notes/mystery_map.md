# The mystery map — if thermodynamics is a genus, every classical mystery has a coordination twin

**Date 2026-07-11.** The cheapest-disproof hunt. The married stance (`four_laws.md` §genus)
says thermodynamics is one genus with two species — energy-thermodynamics and
coordination-thermodynamics, the second reading the multi-information `S = −ln det C` as its
primary state function. A genus claim carries a sharp obligation: **every unsolved puzzle of
the energy species must have a coordination-species counterpart** — answered, contradicted, or
open, but never simply absent. An absent counterpart (a classical mystery with no coordination
twin, or a coordination twin that behaves oppositely) is a disanalogy, and a disanalogy is a
genus wound. This note sweeps the eight canonical puzzles, adjudicates each against the
program's existing theorems and data, stakes a kill per row, and ranks by cheapness of
disproof.

**Bottom line.** All eight map; none produced a clean disanalogy-kill, so the genus survives
the sweep — **but a sweep that finds no kill is the weakest possible good news** (rule 2:
resemblance earns nothing). The sweep's actual deliverables are three: (a) two cheap live
falsification routes it exposes — a coordination fluctuation-theorem bench test on the GPU
arrays, and a grain-distinguishability re-analysis on TNG data already on disk; (b) a concrete
mechanism sketch for the grain problem "resolved from below" (mystery 2); and (c) a convergence
result — mysteries 1, 2, and 8 all reduce to the grain, which is exactly where the program had
independently already located its deepest open problem (`the_grain_problem.md`). The genus's
strongest structural evidence is not that the twins exist but that **both species keep their
deepest puzzle in the same place.**

---

## 1. The Past Hypothesis — ANSWERED (observed, not merely postulated)

**Classical.** Why did the universe begin in a low-entropy state? Penrose's Weyl Curvature
Hypothesis (Penrose 1979, *General Relativity: An Einstein Centenary Survey*; 2004, *The Road
to Reality* ch. 27) makes the puzzle sharp: the CMB is a near-perfect blackbody (maximal
*thermal* entropy) yet the early universe was overall *low* entropy — because the
*gravitational* entropy was low, i.e. the Weyl tensor was ≈ 0, i.e. the geometry was smooth.
Albert (2000, *Time and Chance*) names this the Past Hypothesis. The energy species must
**postulate** it as an unexplained boundary condition, and worse, it has no agreed
microphysical state-count for "gravitational entropy" — the Weyl tensor is a *proxy*, not a
partition function.

**Genus prediction.** Did the coordination books open empty? `S_coord = −ln det C` on the
primordial density field. Independent Fourier modes ⇒ `C ≈ I` in the mode basis ⇒ `det C ≈ 1`
⇒ **S_coord ≈ 0**. So the genus predicts the coordination past hypothesis is "the arrangement
books opened empty."

**Adjudication.** Two things the energy species cannot do, the coordination species does:

1. **It supplies the missing state function.** Penrose could only name gravitational entropy by
   proxy (Weyl → 0). The coordination species gives the state count: gravitational-arrangement
   entropy *is* `−ln det C` on the density field. Smoothness = mode-independence = empty
   coordination books; clumping = correlation = growing S_coord. This is why the married gravity
   ontology has gravity read the coordination books (`CLAUDE.md`, gravity = shared-substrate
   common-cause read): the instrument that couples to the arrangement is exactly the one whose
   "entropy" Penrose lacked a count for.
2. **It is observed, not postulated.** A Gaussian random field has statistically independent
   modes — the operational definition of `S_coord ≈ 0`. Planck 2018 (IX, *A&A* 641 A9, 2020)
   measures `f_NL^local = −0.9 ± 5.1`: the initial conditions are Gaussian to high precision.
   The coordination past hypothesis is therefore **read off the sky**, where the energy species'
   version is a brute assumption.

Are the two the same fact? **Qualified yes**, and it is the note's cleanest positive: Penrose's
*specifically gravitational* low entropy is smoothness; smoothness is mode-independence;
mode-independence is empty coordination books. The energy species saw a paradox (max thermal
entropy alongside low total entropy); the coordination species dissolves it by supplying the
state function the paradox was missing. This is the mechanical complement to
`Cosmology/PenrosePast.lean`'s structural (teleological) argument: the Lean file argues *why we
observe* a low-S_coord past (conditioning on omega-reaching trajectories); this note records
that we *do* observe it, with a state count.

**Verdict: ANSWERED, retrodictive.** Genus-confirmed here, not wounded — but Gaussianity was
known, so under rule 2 this is a consistency check / retrodiction, not novel support. The one
*novel* piece is the S_coord *growth* history (rise to peak z ≈ 0.59, then decline) — that is
the DR3 leg, already registered.

**Kill:** a robust detection of large primordial non-Gaussianity (|f_NL| ≫ Planck's bound)
would mean the coordination books did *not* open empty. Already bounded tiny — the claim is
confirmed, not cheaply killable. (Retrodiction, not a residual: no open kill condition means it
earns nothing beyond consistency.)

---

## 2. The Gibbs paradox ↔ the grain problem — OPEN, with a mechanism sketch

**Classical.** Mixing two volumes of the *same* gas produces zero entropy of mixing, but the
naive Boltzmann count gives a positive ΔS unless divided by `N!`. Whether the gases are "the
same" (no mixing entropy) or "different" (positive) turns on whether the particles are
distinguishable. The textbook resolution is **from below**: quantum mechanics makes identical
particles fundamentally indistinguishable (the symmetrization postulate), so the `N!` is forced
by the substrate's identity structure, not chosen. **Honest wrinkle, load-bearing here:** the
foundational literature contests that it is from-below at all. Jaynes ("The Gibbs Paradox,"
1992) and Versteegh & Dieks (*Am. J. Phys.* 79, 741, 2011) argue the quantum resolution is
*irrelevant* — the correct counting is set by which macrostates the *experimenter* can
distinguish; classical distinguishable particles with non-extensive entropy are "perfectly
acceptable." So the classical precedent for "grain resolves from below" is itself split between
a from-below (quantum-statistics) reading and a from-the-side (observer-relative) reading.

**Genus prediction.** The grain problem — which units post to the coordination ledger — should
resolve **from below**: the substrate's own statistics/identity structure fixes the unit.

**Adjudication.** The grain problem is the program's isolated central open problem
(`the_grain_problem.md`): the DE-ledger fit quality depends on the mass threshold (grain
choice); the galactic-rung membership definition fixes the **clock** (crossing epoch z ≈ 0.54,
from physical membership with zero threshold freedom) but *not* the **amplitude** (set by an
underived "sharpness in the assembly-epoch variable"). So the grain is already **half-resolved
from below**: the clock is, the amplitude is not.

The Gibbs mapping sharpens the open half into a mechanism. The Gibbs question — "what counts as
one distinguishable unit" — is *exactly* the grain question. And the program's own data answers
it with a rung-relative distinguishability rule:

> **Mechanism sketch (the grain from below).** The rung hierarchy is the coordination species'
> indistinguishability structure, playing the role quantum statistics plays for the energy
> species. A degree of freedom **posts to the coordination ledger at rung r iff it is
> distinguishable at r while its constituents below r are indistinguishable (phase-mixed /
> symmetrized).**
> - *Below the halo:* DM particles inside a virialized halo are exchange-symmetric — phase-mixed,
>   no persistent labels — so they do **not** individually post; virialization is the
>   symmetrization event that traces them into one unit. This is literally the DEBIT side of the
>   exchange-rate measurement (`exchange_rate/`: within-halo x–v coherence *destroyed*,
>   S_before − S_after > 0).
> - *At the galactic rung:* halos hosting galaxies have persistent identity (merger histories,
>   distinct positions) — they are distinguishable, they post. The credit side.
> - *Above ~100 Mpc:* the field is Gaussian, modes independent, `C ≈ I` — uncorrelated units
>   contribute S_coord → 0 (measured: the inter-tile term is negligible, S_total ≡ S_extensive
>   to 3 decimals, `the_grain_problem.md` §2).
>
> The `N!` divides out permutation-equivalent microstates; the rung hierarchy divides out the
> sub-rung phase-mixed constituents. The double-entry X ≈ 1 (`four_laws.md` first law) is the
> quantitative version: coordination debited from the now-indistinguishable constituents equals
> coordination credited to the new distinguishable unit — the coordination analog of the
> bookkeeping the `N!` enforces.

The Jaynes/Versteegh–Dieks wrinkle is **not a wound — it is a second, deeper genus match.** The
married gravity ontology says the grain is *instrument-set* (gravity reads at a scale), which is
the observer-relative Jaynes reading, not the from-below quantum-statistics reading. So both
species carry the *same* unresolved observer-vs-substrate tension at the grain. The genus
predicts a shared structure; what it gets is a shared structure *including a shared open
question* — which is stronger evidence than a clean shared success, because it is non-trivial.

**Concrete testable output.** The Gibbs mapping converts the galaxy-book note's underived
"amplitude is set by sharpness in the assembly-epoch variable" (`the_grain_problem.md` §6,
discovery-tier) into a *principled* prediction: the amplitude should be recovered by selecting
on the **distinguishability/identity-formation transition** — a phase-mixing or formation-time
proxy (concentration / z_form), *not* a stellar-mass cut. The galaxy-book note already
pre-flagged exactly this as the next candidate test requiring registration. The mapping gives it
a reason.

**Verdict: OPEN, with mechanism sketch + a registerable test.** Genus-consistent (the shared
open grain question is itself the result).

**Kill:** register a formation-time-sharp (distinguishability-sharp) selection; if it does
**not** recover the corner amplitude (w_a ≈ −0.7, interior clock, maha < 1.5), then
rung-distinguishability does not set the grain from below and the grain stays a free input of
the theory (the second constant alongside κ, taking the hit `dimensional_line_kB.md` §5
pre-staked).

---

## 3. Maxwell's demon / Landauer — ANSWERED in structure, with a named residue

**Classical.** The demon appears to beat the second law by sorting molecules. Landauer (1961,
*IBM J. Res. Dev.* 5, 183): erasing one bit costs `k_B T ln 2`. Bennett (1982, *Int. J. Theor.
Phys.* 21, 905): the demon's memory must be reset, and that erasure pays the debt — the
"ultimate exorcism." Measurement can be reversible; *erasure* cannot. Experimentally confirmed
(Bérut et al., *Nature* 483, 187, 2012).

**Genus prediction.** Hidden coordination = the deception identification. Clause 7 no-hiding
(the amplitude-blind copula reads the full dependence structure, so coordination cannot be
concealed) + the CIRIS/Neff program (deception must cohere across independent constraint axes).
No free coordination + rent.

**Adjudication.** The exorcism structure is isomorphic:
- Landauer erasure cost ↔ the maintenance rent (γM; the second-law rent corollary = Hatano–Sasa
  housekeeping heat, grade-A prior art per `thermo_prior_art.md`). Holding a sorted / low-S_coord
  state costs continuous work.
- Bennett's "memory must be reset" ↔ the demon's memory–gas correlation `I(mem:gas) > 0` is
  *real* coordination that posts to the ledger and cannot be hidden (clause 7). The apparent free
  lunch is exactly hidden coordination; the ledger refuses to let it be free.
- Deception = a Maxwell demon of the epistemic ledger: it extracts advantage by maintaining a
  hidden correlation (true state vs presented state) the truth-ledger charges for. Neff = the
  number of independent axes it must cohere across; the CEG substrate floor = the Landauer rent
  it cannot evade.

**Residue:** the *structure* is answered (no-free-coordination = no-free-information; rent =
erasure/housekeeping cost, both theorem/measured). The *quantitative* coordination-Landauer
bound — minimum maintenance cost per nat of held coordination — is asserted by analogy, not
derived. It is the same gap as κ being empirical.

**Verdict: ANSWERED (expected), residue named.** Genus-consistent, largely in hand.

**Kill:** the residue is bench-testable and rides on adversarial-Neff — if hidden coordination
(deception) can be maintained *without* a cost that scales across the independent axes, the
exorcism fails on the epistemic ledger. That is the safety program's decisive open test, not a
new one.

---

## 4. Heat death / the far future — OPEN, and it IS the DR3 fork

**Classical.** The energy species predicts heat death: entropy climbs monotonically to a maximum,
all gradients erased, no more work, *eternally*.

**Genus prediction.** S_coord(a) **already peaked** at z ≈ 0.59 (measured, TNG300-1 large-volume
test, `large_volume/SUMMARY.md`) and is now **declining**. The coordination books are closing.
Via `ρ_DE = κ·S(a)`, ρ_DE declines hereafter; via the sign law `1 + w = −⅓ dlnS/dlna`, the
S-peak is exactly where w crosses −1 (dlnS/dlna changes sign): phantom (w < −1) while S rose
toward the peak, quintessence-like (w > −1) as S falls after it. So the DE-dominated
acceleration is a **transient**, and the universe **exits** its accelerating era — distinct from
ΛCDM's constant Λ (eternal de Sitter acceleration).

**Adjudication.** This is not a separate speculation — the near-term signature of the transient
*is* the low-z w(z) shape, which is the registered DR3 prediction: w_today = −0.833 ± 0.057
(> −1), crossing epoch z = 0.59 ± 0.03. The far-future claim and the DR3 test are one
observable, extrapolated.

A pleasing genus identity: the energy-species heat death (S_energy → max) and the
coordination-species heat death (S_coord → 0, no correlations left) are opposite in sign but the
*same event* — as the universe virializes into isolated lumps and accelerates into
causally-disconnected patches, the marginal entropies saturate while the multi-information
vanishes. This is `H_joint = Σ H_marginal − I` (`four_laws.md` §genus) playing out to its end:
the coordination line-item `I → 0` as the marginals → max.

**Verdict: OPEN, registered.** The program's strongest empirical leg, restated as a far-future
cosmology. Genus-consistent.

**Kill:** the standing DR3 kill — a robust SNe-independent phantom crossing at DR3, or w_today
consistent with −1, kills the transient-acceleration reading (`CLAUDE.md` discipline rule 1).

---

## 5. Negative temperature — ANSWERED (already in the corridor algebra)

**Classical.** In a system with a **bounded** energy spectrum, population inversion yields T < 0,
which is "hotter than +∞" (Ramsey, *Phys. Rev.* 103, 20, 1956; Purcell & Pound, *Phys. Rev.* 81,
279, 1951, nuclear spins; Braun et al., *Science* 339, 52, 2013, realized it for *motional*
degrees of freedom in a cold-atom lattice — the first case with a spectrum bounded on one side).
The **bounded spectrum is the precondition.**

**Genus prediction.** Anti-coordination / frustration — negative-ρ, frustrated books. Does the
corridor algebra accommodate it (k_eff for ρ < 0)?

**Adjudication — it already does, and it falls straight out of the base identity.** For an
equicorrelation matrix, positive-semidefiniteness bounds ρ in `[−1/(k−1), 1]` — a **bounded
spectrum**, the exact precondition. Evaluate the program's objects at both ends:
- `det C = (1−ρ)^{k−1}(1 + (k−1)ρ)` → 0 at ρ → 1 (the rigidity pole; S → +∞; third law) **and**
  at ρ → −1/(k−1) (the maximally-frustrated pole; S → +∞ via the vanishing `1+(k−1)ρ` factor).
- `k_eff = k/(1 + ρ(k−1))` → 1/ρ-capped for ρ > 0, but for ρ < 0 gives k_eff > k, **diverging**
  as ρ → −1/(k−1) (`Core/BaseIdentity.lean`).

So S_coord has **two** high-entropy poles: one reached by alignment (ρ → 1), one by maximal
frustration (ρ → −1/(k−1)), with the minimum at ρ = 0 (independence). The frustrated pole is the
coordination analog of negative temperature — a high-S state reached not by ordering but by
anti-alignment in a **bounded** spectrum, exactly as negative T is a high-entropy state reached
by population inversion in a bounded spectrum. `k_eff → ∞` at that pole is the "hotter than
infinity" analog (unboundedly many effective modes). Physical instances: frustrated magnets,
spin glasses — which ties directly to mystery 6.

**Verdict: ANSWERED.** The negative-ρ / frustrated regime is already in the corridor algebra,
unnamed until now; the bounded-spectrum precondition maps exactly. **Honest residue:** the full
negative-*temperature* structure needs a conjugate energy variable (1/T = dS/dE); the
coordination species has no state-level "coordination energy" identified (κ is the bridge
constant, not the conjugate variable). So this is the *bounded-spectrum two-pole phenomenon*,
not a constructed coordination temperature — same open piece as the parked fourth law (Onsager)
and the missing conjugate variable.

**Kill:** a frustrated / anti-correlated system whose k_eff departs from `k/(1+ρ(k−1))` near the
PSD boundary would break it — but that is the L0 base identity (a theorem), so it cannot fail
without the engineering tier falling. Safe by construction; earns nothing.

---

## 6. Residual entropy / glasses — OPEN, DELEGATED (do not duplicate)

**Classical.** Third-law violation: glasses and disordered crystals retain entropy as T → 0
because they freeze into one of exponentially many metastable configurations before reaching the
ground state — kinetic arrest, relaxation time exceeding observation time. Canonical case: water
ice, residual entropy `R ln(3/2) ≈ 3.4 J·mol⁻¹·K⁻¹` from frozen proton disorder (Pauling, *JACS*
57, 2680, 1935; confirmed calorimetrically by Giauque & Stout, *JACS* 58, 1144, 1936).

**Genus prediction.** Frozen residual coordination — S_coord locked in because the maintenance
dynamics (`dρ/dt = α − γM`, `Core/Dynamics.lean`) arrests before S relaxes to equilibrium. This
is a *distinct* third-law phenomenon from the program's stated third law (ρ → 1 unattainable,
`four_laws.md`): not the unattainability of the pole, but the failure to reach the low-S ground
state by kinetic arrest. The natural source is the **fermionic ledger** (four_laws third law:
fermionic ledger caps at ln2/mode) — a frustrated fermionic ledger has a degenerate ground
manifold = residual coordination entropy. Ties to mystery 5 (frustration is the shared root).

**Verdict: OPEN, delegated to the jamming-sweep agent.** Genus-consistent counterpart exists;
verdict deferred to avoid duplication. Connection logged: residual coordination = frozen-in
S_coord from arrest; fermionic-ledger degeneracy is the candidate mechanism.

**Kill:** owned by the jamming sweep.

---

## 7. Fluctuation theorems (Jarzynski / Crooks) — the genus survives its mathematical core; a NEW cheap bench test

**Classical.** Beyond the second-law *inequality* ⟨ΔS⟩ ≥ 0 lie *equalities* valid arbitrarily far
from equilibrium: Jarzynski (*PRL* 78, 2690, 1997), `⟨e^{−W/k_BT}⟩ = e^{−ΔF/k_BT}`; Crooks
(*PRE* 60, 2721, 1999), `P_F(W)/P_R(−W) = e^{(W−ΔF)/k_BT}`. For nonequilibrium *steady states*
the relevant form is Hatano–Sasa (*PRL* 86, 3463, 2001), which is a Jarzynski-type equality on
the excess/housekeeping decomposition.

**Genus prediction (the mission's sharpest test).** A coordination Jarzynski **must** exist — a
work-like maintenance quantity whose exponential average ties to ΔS_coord — or, if it *provably
cannot*, the genus is wounded at its mathematical core.

**Adjudication — the obstruction does not exist; the equality follows.** The maintained corridor
is a Markovian Langevin process (`dρ/dt = α(ρ,S) − γM(t) + noise`) with a stationary measure
ρ_ss (`Core/Dynamics.lean`). Seifert's integral fluctuation theorem (*PRL* 95, 040602, 2005;
review *Rep. Prog. Phys.* 75, 126001, 2012) — `⟨e^{−Δs_tot}⟩ = 1` — holds for **any** such
process with a well-defined trajectory entropy production. The candidate coordination equality:

> `⟨e^{−W_coord/κ}⟩ = e^{−ΔΦ_coord/κ}`,

with `W_coord` the integrated maintenance work (the rent, `∫ M(t) dt`-like), κ the coordination
bridge constant in `k_B`'s role, and `ΔΦ_coord` a coordination free-energy difference. Because
the rent was already identified as Hatano–Sasa housekeeping heat (`thermo_prior_art.md`,
grade-A), the coordination Jarzynski is **specifically the Hatano–Sasa relation applied to the
corridor's excess/housekeeping split** — the equality-form of an identification the program
already made. So: the genus survives its mathematical-core test (the obstruction is absent), and
the classical theorem is Hatano–Sasa 2001 (prior art on the equality); the new-in-part piece is
the *application to the correlation order parameter with a bench measurement of κ*.

**This is bench-testable now.** The CIRISArray / GPU strain gauges run a maintained-corridor
process. Measure the distribution of maintenance work `W_coord` over many forward runs and check
the integral FT `⟨e^{−W_coord/κ}⟩ = 1`; run time-reversed protocols for Crooks. A clean failure
would indict the *model* (the corridor is not the Markovian process we think) rather than the
genus outright — but it is the cheapest in-house test that could return a genus-relevant
negative, and it pins down whether the maintained corridor is a well-defined
stochastic-thermodynamic process with a single κ.

**Verdict: DERIVABLE (genus survives) / OPEN-as-untested, bench-runnable.** Genus-consistent.

**Kill:** on the GPU arrays, if the maintenance-work distribution admits **no** single κ making
`⟨e^{−W_coord/κ}⟩ = 1` (beyond statistical error), the maintained corridor is not a
detailed-stochastic-thermodynamic process — the second-law species' equality-form fails on its
own bench.

---

## 8. Loschmidt's reversibility objection — ANSWERED (the grain again)

**Classical.** Microscopic dynamics is time-reversible, yet macroscopic entropy increases
monotonically (Loschmidt 1876, against Boltzmann's 1872 H-theorem). Resolution: coarse-graining
+ typicality + the special low-entropy initial condition (the Past Hypothesis). The arrow is in
the boundary condition and the coarse-graining, not the dynamics.

**Genus prediction.** Same objection: the underlying copula-preserving dynamics is reversible,
yet the coordination second law (DPI, `four_laws.md`) is a monotone. Same resolution:
coarse-graining (the **grain** — which units post, the rung choice) + the coordination Past
Hypothesis (mystery 1, `S_coord ≈ 0` initially, *observed*) + typicality.

**Adjudication — and heading off an apparent wound.** S_coord(a) is **non-monotone** — it rises
to a peak at z ≈ 0.59 and falls. Does that violate the coordination second law? **No.** The DPI
says multi-information is non-increasing under **local operations** (no free coordination); it
does *not* assert a monotone global trajectory. S_coord rises when genuine *interaction* creates
it (gravitational clustering — the first law's two creation channels) and falls when it is
*destroyed* (virialization phase-mixing, mergers, accelerated dispersal — the irreversible
destruction channel). The S_coord(a) history is creation-dominated then destruction-dominated;
the second law governs the local-ops direction, not the global shape. Consistent.

**The convergence result.** Loschmidt's resolution needs coarse-graining (grain); the Past
Hypothesis needs the low-S initial condition (mystery 1, *observed* for coordination); the Gibbs
paradox *is* the grain question (mystery 2). **All three reduce to the grain.** The genus
predicts the coordination species should keep its deepest puzzle at the grain — and the program
had *independently* isolated the grain problem as its central open problem
(`the_grain_problem.md`) before this mapping was drawn. That the two species keep their deepest
puzzle in the same place is the sweep's strongest structural finding.

**Verdict: ANSWERED (same resolution), re-identifies the grain as the shared deep puzzle.**
Genus-consistent. The non-monotone S_coord is explained, not a violation.

**Kill:** if S_coord were ever shown to *increase* under a demonstrably local (interaction-free)
operation on the field, the DPI (second law of coordination) would fail — but that is the named
open Lean step's theorem content, not a loose end here.

---

## Verdict table (compact)

| # | Mystery | Coordination twin | Verdict | Genus |
|---|---|---|---|---|
| 1 | Past Hypothesis | Books opened empty (S_coord ≈ 0), **observed** via Planck Gaussianity | ANSWERED, retrodictive | confirmed (weak, rule 2) |
| 2 | Gibbs paradox | The grain problem; rung = indistinguishability structure | OPEN + mechanism sketch | consistent (shared open Q) |
| 3 | Maxwell demon / Landauer | Hidden coordination = deception; rent = erasure cost | ANSWERED, residue named | consistent |
| 4 | Heat death | S_coord peaked (z≈0.59), ρ_DE declines, acceleration transient | OPEN, registered (DR3) | consistent |
| 5 | Negative temperature | Frustrated pole ρ=−1/(k−1); k_eff→∞; in the base identity | ANSWERED | consistent |
| 6 | Residual entropy / glass | Frozen residual coordination (fermionic degeneracy) | OPEN, delegated | consistent |
| 7 | Fluctuation theorems | Coordination Jarzynski = Hatano–Sasa on the rent; bench-testable | DERIVABLE / untested | consistent (survives core) |
| 8 | Loschmidt | Coarse-graining + coordination Past Hyp; the grain again | ANSWERED | consistent |

**No CONTRADICTED row.** The genus survives the sweep with no disanalogy-kill — which, per rule
2, is the weakest possible good news and earns nothing on its own.

---

## Cheapness-of-disproof ranking (cheapest = most falsifiable now)

1. **Mystery 7 — coordination fluctuation theorem, GPU bench.** Runnable now on existing
   CIRISArray infrastructure; generate the maintenance-work distribution, check the integral FT
   for a single κ. Cheapest to *execute*. (Caveat: a failure indicts the corridor *model* rather
   than the genus directly — but it is the cheapest test that returns a genus-relevant negative.)
2. **Mystery 2 — grain distinguishability re-analysis.** TNG data on disk; select on a
   formation-time / phase-mixing proxy and test recovery of the corner amplitude. Cheap; needs a
   pre-registered rule first (the galaxy-book note already flagged it).
3. **Mystery 1 (first-law adjacent) — exchange rate X = 1 to precision.** Data on disk
   (`exchange_rate/`); X robustly ≠ 1 kills the first-law conservation reading of the grain
   bookkeeping. Cheap, and already the program's first-law test.
4. **Mystery 4 — DR3 w(z).** Decisive but not cheap (waits ~2027); the standing registered kill.
5. **Mystery 3 — adversarial-Neff.** The coordination-Landauer residue; the safety program's
   decisive open test.
6. **Mystery 6 — jamming sweep** (delegated).
7. **Mysteries 5, 8, 1(retrodictive)** — answered by theorem/observation; not cheaply killable,
   earn nothing.

---

## The single cheapest live disproof route

**The coordination fluctuation-theorem bench test (mystery 7), sharpened to a single-κ demand.**
The genus claims *one* species with *one* `k_B`-analog κ. Run the maintained corridor on the GPU
arrays, measure the maintenance-work distribution, and find the κ_bench that makes
`⟨e^{−W_coord/κ}⟩ = 1`. If **no** single κ satisfies the integral fluctuation theorem within
statistical error, the maintained corridor is not a detailed stochastic-thermodynamic process
and the coordination second law has no equality-form on its own bench — the genus's central
claim (a species with its own consistent κ and its own four laws) fails at the one place it is
cheapest to check. It is in-house, data-generatable now, and needs no new instrument.

---

## Mystery 2 answered directly: does Gibbs↔grain yield a mechanism for resolving the grain from below?

**Yes — a sketch, and it earns its keep by re-deriving a discovery-tier finding.** The rung
hierarchy is the coordination species' indistinguishability structure (the analog of quantum
statistics): a degree of freedom posts at rung r iff it is distinguishable at r while its
sub-rung constituents are phase-mixed / symmetrized. Virialization is the symmetrization event
(the exchange-rate DEBIT); the galactic-rung host is the distinguishable unit (the CREDIT);
above ~100 Mpc the modes are independent and post nothing (measured). This converts the
galaxy-book note's *underived* "amplitude set by sharpness in the assembly-epoch variable" into a
principled prediction: select on the identity-formation (distinguishability) transition — a
formation-time proxy, not a stellar cut — and the corner amplitude should return with the
galactic clock. That is a registerable test on data already on disk. **Caveat, stated plainly:**
the classical precedent is itself split (Jaynes/Versteegh–Dieks say the grain is
observer-relative, not from-below), and the married gravity ontology sides with the
observer-relative reading — so the honest genus result is not "the grain resolves from below in
both species" but "both species carry the *same* observer-vs-substrate grain tension," which is
the stronger, non-trivial match.
